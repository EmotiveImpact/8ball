"""Masked historical forecast replay (retrospective diagnostic, not validation).

Two separate steps. ``forecast`` sends only the pre-cutoff masked case to the
configured provider and freezes a typed Forecast. ``resolve`` later binds the
known outcome to that frozen forecast digest and scores it. The model never
receives the outcome file. A renamed historical story does not prevent model
memorisation; one case cannot establish predictive accuracy. Nothing here
creates evidence, approval, route selection or external action.
"""
from datetime import date, datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json
import sys
from typing import Annotated, Literal

from pydantic import AnyHttpUrl, AwareDatetime, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eightball.v2.compatible import CompatibleSession, settings  # noqa: E402
from eightball.v2.hosted import HostedFailure  # noqa: E402
from endstate.api import PlanRequest, calculate  # noqa: E402
from endstate.contracts import PlanningSnapshot, Graph, Condition, Action, Effect, Objective, atom  # noqa: E402
from endstate.forecasting import Digest, Forecast, Resolution, Probability, Statement, evaluate, forecast_digest  # noqa: E402
from endstate.primitives import Identifier, Strict  # noqa: E402
from scripts.acceptance import output_directory  # noqa: E402

VERSION = 'historical-replay.v2'
PROMPT_VERSION = 'historical-forecast.v2'
MAX_INPUT_BYTES = 16000
MODEL = 'claude-sonnet-5-5'


class Context(Strict):
    situation: Statement
    terms: list[Statement] = Field(min_length=1, max_length=20)
    known_unknowns: list[Statement] = Field(max_length=20)
    instructions: Statement


class CaseInput(Strict):
    version: Literal['endstate.historical-replay.v1']
    id: Identifier
    kind: Literal['retrospective_masked_replay']
    as_of: AwareDatetime
    horizon: AwareDatetime
    event: Statement
    masking: Statement
    context: Context


class Answer(Strict):
    probability: Probability | None
    abstention_reason: Statement | None
    assumptions: list[Annotated[str, Field(min_length=1, max_length=400, pattern=r'\S')]] = Field(max_length=8)
    most_informative_observation: Annotated[str, Field(min_length=1, max_length=600, pattern=r'\S')]
    recognises_real_case: bool = Field(strict=True)
    recognition_note: Annotated[str, Field(min_length=1, max_length=600, pattern=r'\S')]


class RetrievedSource(Strict):
    id: Identifier
    url: AnyHttpUrl
    sha256: Digest
    retrieved: date


SCHEMA = Answer.model_json_schema()
INSTRUCTIONS = (
    'You are an advisory forecaster inside a decision-review tool. Use only the supplied case, '
    'as of its information cutoff. Give either a probability (0-1) that the stated event occurs by '
    'the horizon, or null with an explicit abstention_reason. Never give both. List the assumptions '
    'your number depends on and the single observation that would most change it. Report honestly '
    'whether you believe you recognise the specific real transaction; if so, still answer only from '
    'the supplied information. Your output is advice for human review, not evidence or a decision.'
)


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()


def digest(value) -> str:
    return sha256(canonical(value)).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def now():
    return datetime.now(timezone.utc)


def checkpoint(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_bytes(canonical(value) + b'\n')
    temp.replace(path)


def prepare(case):
    CaseInput.model_validate(case)
    if len(canonical(case)) > MAX_INPUT_BYTES:
        raise ValueError('Input exceeds the bounded one-request protocol')
    context = {'as_of': case['as_of'], 'horizon': case['horizon'], 'event': case['event'],
               'case': case['context']}
    cutoff = datetime.fromisoformat(case['as_of'].replace('Z', '+00:00'))
    if cutoff >= now():
        raise ValueError('This protocol is retrospective, not a prospective register')
    placeholder = Forecast(id=case['id'], event=case['event'], as_of=case['as_of'],
                           horizon=case['horizon'], input_sha256=digest(context),
                           predictor='not_invoked', abstention_reason='Preparation only')
    if placeholder.horizon >= now():
        raise ValueError('A historical replay requires a past horizon')
    snapshot = PlanningSnapshot(id=case['id'], deadline=placeholder.horizon, graph=Graph(
        conditions=[Condition(id='confirmed', title=case['event'], confirmation='Independent observed outcome evidence')],
        actions=[Action(id='attempt', title='Attempt the declared objective', owner='Operator',
                        purpose=case['event'], minutes=15, contingent=True, wait_minutes=None,
                        approval_required=True, effects=[Effect(condition_id='confirmed')])],
        objectives=[Objective(id='goal', title=case['event'], success=atom('confirmed'))]))
    before = snapshot.model_dump_json()
    plan = calculate(PlanRequest(snapshot=snapshot, as_of=placeholder.as_of)).plan
    if snapshot.model_dump_json() != before:
        raise ValueError('Read-only planning changed its input')
    planning = {'snapshot': snapshot.model_dump(mode='json'), 'result': plan,
                'input_unchanged': True, 'kind': 'illustrative_author_created_graph',
                'notice': 'A conditional-route control, not a complete merger model or an event forecast. '
                          'Its duration is an author-created placeholder, not historical evidence.'}
    return context, planning


def make_forecast(case, context, answer, served):
    answer = Answer.model_validate(answer)
    if served != MODEL:
        raise ValueError('Unexpected served model; no substitution')
    return Forecast(id=case['id'], event=case['event'], as_of=case['as_of'],
                    horizon=case['horizon'], input_sha256=digest(context),
                    predictor=f'anthropic:{served}:{PROMPT_VERSION}',
                    probability=answer.probability, abstention_reason=answer.abstention_reason)


def forecast(case_path, output, *, allow_inference=False, allow_external=False):
    if allow_inference is not True or allow_external is not True:
        raise ValueError('Both explicit inference and external-provider permissions are required')
    out = output_directory(output)
    out.mkdir(parents=True, exist_ok=False)
    started = now()
    path = out / 'forecast-report.json'
    report = {'version': VERSION, 'prompt_version': PROMPT_VERSION,
              'requested_at': started.isoformat(), 'status': 'preflight',
              'provider_call_attempted': False, 'actual_model_inference': False,
              'outcome_supplied_to_model': False, 'forecast': None, 'maximum_requests': 1}
    report['runner_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    session = None
    checkpoint(path, report)
    try:
        raw = Path(case_path).read_bytes()
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError('Input exceeds the bounded one-request protocol')
        case = json.loads(raw)
        context, planning = prepare(case)
        configured = settings()
        if (configured.provider != 'anthropic' or configured.model != MODEL
                or configured.endpoint != 'https://api.anthropic.com/v1/messages'
                or configured.routing_provider is not None):
            raise ValueError('Only the selected direct Anthropic model is authorised')
        session = CompatibleSession(allow_external=True)
        frozen = {'case': case, 'context': context, 'schema': SCHEMA, 'instructions': INSTRUCTIONS}
        checkpoint(out / 'frozen-input.json', frozen)
        report.update(case_id=case['id'], case_sha256=digest(case), input_sha256=digest(context),
                      frozen_input_sha256=digest(frozen), schema_sha256=digest(SCHEMA),
                      instructions_sha256=digest(INSTRUCTIONS), kind=case['kind'], masking=case['masking'],
                      provider=session.receipt, planning=planning, status='request_admitted',
                      provider_call_attempted=True)
        checkpoint(path, report)
        answer, served = session.generate(SCHEMA, INSTRUCTIONS, context)
        report['served_model'] = served
        canonical(answer)
        report['answer'] = answer
        report['actual_model_inference'] = True
        record = make_forecast(case, context, answer, served)
        report['forecast'] = record.model_dump(mode='json')
        report['forecast_sha256'] = forecast_digest(record)
        report['status'] = 'forecast_frozen'
        report['validity'] = ('recognition_contaminated' if answer['recognises_real_case']
                              else 'retrospective_unverified')
    except Exception as exc:  # retained, never retried
        report['status'] = 'failed'
        report['error_type'] = type(exc).__name__
        report['error_code'] = exc.code if isinstance(exc, HostedFailure) else 'invalid_experiment'
    except BaseException:
        report['status'] = 'interrupted'
        raise
    finally:
        report['completed_at'] = now().isoformat()
        report['receipt'] = session.receipt if session else None
        report['runner_unchanged'] = report['runner_sha256'] == sha256(Path(__file__).read_bytes()).hexdigest()
        report['notice'] = ('Retrospective replay recorded after the real outcome existed. The forecast '
                            'as_of is the information cutoff, not when this request was made. Recognition '
                            'of the masked case or memorised history cannot be excluded.')
        checkpoint(path, report)
        print(path)
    return report


def resolve(report_path, outcome_path, sources_path):
    report = load(report_path)
    path = Path(report_path).with_name('resolution-report.json')
    if path.exists():
        raise FileExistsError('Resolution already exists; never replace retained results')
    if report.get('version') != VERSION or report.get('status') != 'forecast_frozen':
        raise ValueError('Only a frozen forecast can be resolved')
    if report.get('runner_unchanged') is not True:
        raise ValueError('Runner changed during inference')
    requested = datetime.fromisoformat(report['requested_at'])
    completed = datetime.fromisoformat(report['completed_at'])
    if requested.utcoffset() is None or completed.utcoffset() is None or not requested <= completed <= now():
        raise ValueError('Invalid actual request chronology')
    frozen = load(Path(report_path).with_name('frozen-input.json'))
    if digest(frozen) != report['frozen_input_sha256']:
        raise ValueError('Frozen input digest mismatch')
    case = frozen['case']
    context, _ = prepare(case)
    if (context != frozen['context'] or digest(context) != report['input_sha256']
            or digest(case) != report['case_sha256'] or case['id'] != report['case_id']
            or frozen['schema'] != SCHEMA or frozen['instructions'] != INSTRUCTIONS
            or digest(SCHEMA) != report['schema_sha256']
            or digest(INSTRUCTIONS) != report['instructions_sha256']):
        raise ValueError('Forecast input bindings differ')
    record = Forecast.model_validate(report['forecast'])
    if record != make_forecast(case, context, report['answer'], report['served_model']):
        raise ValueError('Forecast differs from the frozen input or answer')
    if forecast_digest(record) != report['forecast_sha256']:
        raise ValueError('Forecast report digest mismatch')
    outcome = load(outcome_path)
    sources = load(sources_path)
    if (outcome['case_id'] != report['case_id']
            or outcome['case_sha256'] != report['case_sha256']):
        raise ValueError('Outcome refers to a different case')
    if not sources:
        raise ValueError('Observed resolution needs retained public source references')
    for source in sources:
        RetrievedSource.model_validate(source)
    outcome_urls = {source['url'] for source in outcome['sources'] if source['role'] == 'outcome'}
    if not outcome_urls.intersection(source['url'] for source in sources):
        raise ValueError('No retained source matches the declared outcome references')
    bundle = {'outcome': outcome, 'outcome_sha256': digest(outcome), 'retrieved_sources': sources}
    resolution = Resolution(forecast_id=record.id, forecast_sha256=report['forecast_sha256'],
                            value=outcome['value'], available_at=outcome['available_at'],
                            source_reference=outcome['summary'], source_sha256=digest(bundle),
                            basis='observed')
    result = evaluate([record], [resolution], as_of=now())
    scored = {'version': VERSION, 'forecast_report': str(report_path),
              'forecast_sha256': report['forecast_sha256'], 'resolution': resolution.model_dump(mode='json'),
              'resolution_bundle': bundle, 'evaluation': result,
              'retrospective': True, 'held_out_validation': False, 'cases': 1,
              'predictive_quality_approved': False,
              'recognises_real_case': report['answer']['recognises_real_case'],
              'notice': 'One retrospective masked case. Hindsight contamination, model recognition and '
                        'sample size of one prevent any accuracy claim. Scores are diagnostic only.'}
    with path.open('x') as stream:
        stream.write(json.dumps(scored, indent=2, ensure_ascii=False, allow_nan=False) + '\n')
    print(path)
    return scored


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    f = sub.add_parser('forecast')
    f.add_argument('--case', required=True)
    f.add_argument('--output', required=True)
    f.add_argument('--allow-external', action='store_true')
    f.add_argument('--allow-inference', action='store_true')
    r = sub.add_parser('resolve')
    r.add_argument('--report', required=True)
    r.add_argument('--outcome', required=True)
    r.add_argument('--sources', required=True)
    args = parser.parse_args(argv)
    if args.command == 'forecast':
        return 0 if forecast(args.case, args.output, allow_inference=args.allow_inference,
                             allow_external=args.allow_external)['status'] == 'forecast_frozen' else 1
    resolve(args.report, args.outcome, args.sources)
    return 0


if __name__ == '__main__':
    sys.exit(main())
