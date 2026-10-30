"""Offline protocol checks with controlled replies; not prediction-quality evidence."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import json

import pytest

from endstate.forecasting import Forecast, forecast_digest
from evals import historical_replay as replay


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'evals/historical/rto-merger-2018.case.json'
OUTCOME = ROOT / 'evals/historical/rto-merger-2018.outcome.json'
SOURCES = ROOT / 'docs/evidence/historical-replay-sources-2026-10-26.json'


def write(path, value):
    path.write_text(json.dumps(value))
    return path


@pytest.fixture
def controlled(monkeypatch, tmp_path):
    state = SimpleNamespace(calls=[], answer={
        'probability': 0.45, 'abstention_reason': None,
        'assumptions': ['All supplied terms are accurate.'],
        'most_informative_observation': 'The documented regulatory decision.',
        'recognises_real_case': True, 'recognition_note': 'Controlled test fixture only.',
    }, error=None, served=replay.MODEL)

    class Session:
        def __init__(self, **kwargs):
            assert kwargs == {'allow_external': True}

        @property
        def receipt(self):
            return {'calls': [{'status': 'controlled_reply'} for _ in state.calls]}

        def generate(self, schema, instructions, context):
            path = tmp_path / 'run'
            before = replay.load(path / 'forecast-report.json')
            frozen = replay.load(path / 'frozen-input.json')
            assert before['status'] == 'request_admitted'
            assert frozen['context'] == context
            assert before['frozen_input_sha256'] == replay.digest(frozen)
            assert before['planning']['result']['outcome_evidenced'] is False
            state.calls.append(deepcopy((schema, instructions, context)))
            if state.error:
                raise state.error
            return deepcopy(state.answer), state.served

    state.configuration = SimpleNamespace(provider='anthropic', model=replay.MODEL,
                                          endpoint='https://api.anthropic.com/v1/messages',
                                          routing_provider=None)
    monkeypatch.setattr(replay, 'settings', lambda: state.configuration)
    monkeypatch.setattr(replay, 'CompatibleSession', Session)
    state.run = lambda case=CASE: replay.forecast(case, tmp_path / 'run', allow_external=True, allow_inference=True)
    state.report_path = tmp_path / 'run/forecast-report.json'
    state.outcome = replay.load(OUTCOME) | {'case_sha256': replay.digest(replay.load(CASE))}
    state.outcome_path = write(tmp_path / 'outcome.json', state.outcome)
    return state


def test_plan_is_read_only_and_not_an_event_forecast():
    case = replay.load(CASE)
    before = deepcopy(case)
    context, planning = replay.prepare(case)
    assert case == before and context['event'] == case['event']
    result = planning['result']
    assert len(result['routes']) == 1
    assert all(route['provisional'] for route in result['routes'])
    assert result['action_states']['attempt']['status'] == 'approval_required'
    assert result['outcome_evidenced'] is False
    assert planning['input_unchanged'] is True
    assert planning['kind'] == 'illustrative_author_created_graph'


def test_forecast_is_frozen_before_any_outcome_read(controlled, monkeypatch):
    original = replay.load

    def no_outcome(path):
        assert 'outcome' not in str(path)
        return original(path)

    with monkeypatch.context() as scope:
        scope.setattr(replay, 'load', no_outcome)
        report = controlled.run()
    assert report['status'] == 'forecast_frozen'
    assert report['validity'] == 'recognition_contaminated'
    assert report['outcome_supplied_to_model'] is False
    assert report['requested_at'].startswith('20') and report['runner_unchanged']
    assert len(controlled.calls) == 1
    sent = json.dumps(controlled.calls)
    for withheld in ('Rent-A-Center', 'Vintage', 'Riley', '2019-04-22', '92.5 million'):
        assert withheld not in sent
    result = replay.resolve(controlled.report_path, controlled.outcome_path, SOURCES)
    assert result['evaluation']['brier'] == pytest.approx(0.2025)
    assert result['evaluation']['fixed_half_baseline_brier_same_subset'] == 0.25
    assert result['recognises_real_case'] is True
    assert result['retrospective'] is True and result['held_out_validation'] is False
    assert result['predictive_quality_approved'] is False
    assert result['evaluation']['execution_authorized'] is False
    assert result['evaluation']['facts_attested'] is False
    assert len(controlled.calls) == 1


@pytest.mark.parametrize('permissions', [{}, {'allow_external': True}, {'allow_inference': True},
                                       {'allow_inference': 1, 'allow_external': True}])
def test_explicit_opt_ins_are_required_before_any_request(controlled, tmp_path, permissions):
    with pytest.raises(ValueError, match='permissions'):
        replay.forecast(CASE, tmp_path / 'run', **permissions)
    assert not controlled.calls
    assert not (tmp_path / 'run').exists()


@pytest.mark.parametrize('field,value', [
    ('provider', 'substitute'), ('model', 'substitute'), ('routing_provider', 'automatic'),
    ('endpoint', 'https://example.com/v1/messages'),
])
def test_selected_model_and_provider_cannot_be_substituted(controlled, field, value):
    setattr(controlled.configuration, field, value)
    report = controlled.run()
    assert report['status'] == 'failed' and report['provider_call_attempted'] is False
    assert not report['actual_model_inference'] and not controlled.calls


@pytest.mark.parametrize('changes', [
    {'probability': True}, {'probability': '0.45'}, {'probability': float('nan')},
    {'probability': float('inf')}, {'probability': -0.1}, {'probability': 1.1}, {'probability': None},
    {'abstention_reason': 'Also abstaining'}, {'recognises_real_case': 'true'},
    {'recognises_real_case': 1}, {'recognition_note': ' '},
    {'most_informative_observation': 'x' * 601}, {'assumptions': ['x'] * 9},
    {'execution_authorized': True}, {'assumptions': [1]},
])
def test_invalid_answers_are_retained_without_coercion_repair_or_retry(controlled, changes):
    controlled.answer.update(changes)
    report = controlled.run()
    assert report['status'] == 'failed' and report['forecast'] is None
    assert len(controlled.calls) == 1
    assert 'error_type' in replay.load(controlled.report_path)


def test_abstention_is_not_a_zero_probability_or_correct_prediction(controlled):
    controlled.answer.update(probability=None, abstention_reason='Insufficient information', recognises_real_case=False)
    report = controlled.run()
    assert report['validity'] == 'retrospective_unverified'
    result = replay.resolve(controlled.report_path, controlled.outcome_path, SOURCES)['evaluation']
    assert result['coverage'] == 0 and result['abstained'] == 1
    assert result['brier'] is None and result['fixed_half_baseline_brier_same_subset'] is None
    assert result['fixed_half_baseline_brier_all_resolved'] == 0.25


@pytest.mark.parametrize('error', [RuntimeError('do not log credential-shaped details'), KeyboardInterrupt()])
def test_failed_or_interrupted_requests_keep_checkpoint_and_do_not_retry(controlled, error):
    controlled.error = error
    if isinstance(error, KeyboardInterrupt):
        with pytest.raises(KeyboardInterrupt):
            controlled.run()
    else:
        controlled.run()
    report = replay.load(controlled.report_path)
    assert report['status'] in ('failed', 'interrupted')
    assert report['forecast'] is None and len(controlled.calls) == 1
    assert 'credential-shaped' not in json.dumps(report)
    with pytest.raises(ValueError):
        replay.resolve(controlled.report_path, controlled.outcome_path, SOURCES)


def test_wrong_served_model_is_not_accepted(controlled):
    controlled.served = 'substitute'
    assert controlled.run()['status'] == 'failed'
    assert len(controlled.calls) == 1


@pytest.mark.parametrize('mutation', ['forecast', 'digest', 'input', 'answer', 'source', 'chronology'])
def test_changed_forecast_or_context_is_not_scored(controlled, mutation):
    report = controlled.run()
    if mutation == 'forecast':
        report['forecast']['event'] = 'Different event'
        report['forecast_sha256'] = forecast_digest(Forecast.model_validate(report['forecast']))
    elif mutation == 'digest':
        report['forecast_sha256'] = 'f' * 64
    elif mutation == 'input':
        p = controlled.report_path.with_name('frozen-input.json')
        original = replay.load(p)
        original['context']['event'] = 'Different event'
        write(p, original)
    elif mutation == 'answer':
        report['answer']['probability'] = 0.8
    elif mutation == 'source':
        report['runner_unchanged'] = False
    else:
        report['completed_at'] = '2000-01-01T00:00:00+00:00'
    write(controlled.report_path, report)
    with pytest.raises(ValueError):
        replay.resolve(controlled.report_path, controlled.outcome_path, SOURCES)


@pytest.mark.parametrize('change', [
    {'case_id': 'different'}, {'case_sha256': 'a' * 64}, {'value': 'false'}, {'value': 0},
    {'available_at': '2018-06-19T00:00:00+00:00'}, {'available_at': '2099-01-01T00:00:00+00:00'},
])
def test_wrong_case_unknown_or_premature_outcomes_cannot_resolve(controlled, change):
    controlled.run()
    write(controlled.outcome_path, controlled.outcome | change)
    with pytest.raises(ValueError):
        replay.resolve(controlled.report_path, controlled.outcome_path, SOURCES)


@pytest.mark.parametrize('sources', [[], [{'sha256': 'bad'}], [
    {'id': 'other', 'url': 'https://example.com', 'sha256': 'a' * 64, 'retrieved': '2026-10-26'},
]])
def test_resolution_needs_bound_source_references(controlled, tmp_path, sources):
    controlled.run()
    path = write(tmp_path / 'sources.json', sources)
    with pytest.raises(ValueError):
        replay.resolve(controlled.report_path, controlled.outcome_path, path)


def test_existing_run_and_resolution_are_not_overwritten(controlled):
    controlled.run()
    before = controlled.report_path.read_bytes()
    with pytest.raises(FileExistsError):
        controlled.run()
    assert controlled.report_path.read_bytes() == before and len(controlled.calls) == 1
    replay.resolve(controlled.report_path, controlled.outcome_path, SOURCES)
    path = controlled.report_path.with_name('resolution-report.json')
    before = path.read_bytes()
    with pytest.raises(FileExistsError):
        replay.resolve(controlled.report_path, controlled.outcome_path, SOURCES)
    assert path.read_bytes() == before


@pytest.mark.parametrize('changes', [{'horizon': '2018-01-01T00:00:00Z'},
                                    {'horizon': '2099-01-01T00:00:00Z'},
                                    {'outcome': False}, {'as_of': '2018-06-18'}])
def test_invalid_case_is_retained_without_provider_call(controlled, tmp_path, changes):
    case = write(tmp_path / 'case.json', replay.load(CASE) | changes)
    report = controlled.run(case)
    assert report['status'] == 'failed' and not controlled.calls


def test_oversized_input_is_not_sent(controlled, tmp_path):
    path = tmp_path / 'large.json'
    path.write_text('x' * (replay.MAX_INPUT_BYTES + 1))
    assert controlled.run(path)['status'] == 'failed' and not controlled.calls


def test_source_directory_is_not_an_output_location(controlled):
    with pytest.raises(ValueError, match='outside source'):
        replay.forecast(CASE, ROOT / 'evals/prohibited', allow_external=True, allow_inference=True)
    assert not controlled.calls


def test_original_actual_response_and_its_reconstructed_input_stay_bound():
    root = ROOT / 'docs/evidence'
    original = replay.load(root / 'historical-replay-forecast-2026-10-26.json')
    inputs = replay.load(root / 'historical-replay-input-2026-10-26.json')
    result = replay.load(root / 'historical-replay-resolution-2026-10-26.json')
    assert original['version'] == 'historical-replay.v1'
    assert replay.digest(replay.load(CASE)) == original['case_sha256']
    assert replay.digest(inputs['context']) == original['input_sha256']
    assert replay.digest(inputs['schema']) == original['schema_sha256']
    answer = replay.Answer.model_validate(original['answer'])
    assert answer.probability == 0.45 and answer.recognises_real_case is True
    assert forecast_digest(Forecast.model_validate(original['forecast'])) == original['forecast_sha256']
    assert len(original['receipt']['calls']) == 1
    assert original['receipt']['calls'][0]['raw_content']
    assert result['evaluation']['brier'] == pytest.approx(0.2025)
    assert result['predictive_quality_approved'] is False
