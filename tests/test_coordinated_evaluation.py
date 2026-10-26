"""Controlled HTTP and actual worker storage; never live inference or quality proof."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import os

import httpx
import pytest

from evals import coordinated_planning as evaluation
from eightball.store import digest
from eightball.v2.compatible import CompatibleSession
from eightball.v2.decision_models import DecisionSession
from tests.test_compatible_integration import OUTCOME, STAGED, envelope, frame

PERMISSION = dict(allow_inference=True, allow_external=True, allow_unpriced_planning=True)
GLM, DEEPSEEK, SONNET, OPUS = evaluation.PROFILES


@pytest.fixture
def diagnostic(tmp_path, monkeypatch):
    monkeypatch.setenv('EXPERIENTIAL_API_KEY', 'fictional_specialist_token_for_tests')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'fictional_anthropic_token_for_tests')
    case = evaluation.FictionalCase(id='fictional-venue-diagnostic', outcome=OUTCOME,
        text='Fictional venue spares or local hire may be available; no approval is supplied.',
        deadline=datetime(2026, 11, 3, 16, tzinfo=timezone.utc))
    case_path = tmp_path/'case.json'
    case_path.write_text(case.model_dump_json())
    calls, transforms = [], {}
    stages = {}
    def serve(request):
        payload = json.loads(request.content)
        model = payload['model']
        calls.append((str(request.url), payload))
        if model in evaluation.PROFILES:
            stage = stages.get(model, 0)
            stages[model] = stage + 1
            data = frame() if stage % 2 == 0 else deepcopy(STAGED['routes'])
            if stage == 2: data['verification']['title'] = 'Review written acceptance and availability evidence'
            if model in (SONNET, OPUS):
                data = dict(id='message-fixture', type='message', role='assistant', model=model,
                    content=[dict(type='text', text=json.dumps(data))], stop_reason='end_turn',
                    usage=dict(input_tokens=20, output_tokens=10, cache_read_input_tokens=0, cache_creation_input_tokens=0))
            else:
                data = envelope(data, model=model)
        else:
            choice = 'needs_work' if model == 'clef-flash' else 'preserved'
            answers = {q.id: dict(type='choice', choice=choice, confidence=0.8,
                probabilities={k: 0.8 if k==choice else 0.1 for k in q.criteria})
                for q in evaluation.specification(case).review.questions}
            if model == 'gpt-6-luna-decisions':
                answers = [dict(**{k:v for k,v in answer.items() if k!='probabilities'}, name=name,
                    probabilities=[dict(value=k, probability=v) for k,v in answer['probabilities'].items()])
                    for name, answer in answers.items()]
            data = dict(model=model, answers=answers, usage=dict(input_tokens=10, output_tokens=5, cost_nano_usd=1))
        if 'effect' in transforms: transforms['effect'](model, payload)
        if model in transforms: data = transforms[model](data)
        return data if isinstance(data, httpx.Response) else httpx.Response(200, json=data)
    with httpx.Client(transport=httpx.MockTransport(serve)) as client:
        def run(path):
            return evaluation.run(path, **PERMISSION,
                planning_factory=lambda **kw: CompatibleSession(client=client, **kw),
                specialist_factory=lambda **kw: DecisionSession(client=client, **kw))
        def freeze(models=None):
            return evaluation.freeze(case_path, tmp_path/'run', models=models)
        yield dict(calls=calls, transforms=transforms, run=run, freeze=freeze, case=case,
                   case_path=case_path, root=tmp_path)


def test_all_declared_models_use_exact_protocols_and_real_non_mutating_host(diagnostic):
    d = diagnostic
    path = d['freeze']()
    report = d['run'](path)
    assert report['status'] == 'completed', report
    assert report['recorded_provider_call_attempts'] == 28 == len(d['calls'])
    assert report['source_unchanged'] and report['validated_initial_proposal_observed']
    assert report['known_specialist_cost_nano_usd'] == 12
    assert not report['not_started_models']
    assert all(row['case_audit_unchanged'] for row in report['results'])
    assert all(row['work_state']=='awaiting_review' for row in report['results'])
    for row in report['results']:
        data = row['result']
        assert data['initial'] and data['revision'] and data['final_synthesis']['requires_operator_review']
        assert data['initial']['trace']['frame'] != data['revision']['trace']['frame']
        assert data['challenges']['questions'][0]['disagreement']
        assert data['advisory_only'] and not data['facts_attested'] and not data['execution_authorized']
        transport = json.loads((path.parent/row['model']/'transports.json').read_text())
        assert len(transport['planning'][0]['calls']) == 4 and len(transport['specialists']) == 3
    for url, payload in d['calls']:
        if payload['model']==DEEPSEEK: assert payload['response_format']['type']=='json_schema'
        elif payload['model'] in evaluation.PROFILES: assert 'response_format' not in payload
        if payload['model'] in (SONNET, OPUS):
            assert url=='https://api.anthropic.com/v1/messages'
            assert payload['output_config']==dict(effort='medium')
        elif payload['model'] in (GLM, DEEPSEEK):
            assert url=='https://api.experientiallabs.ai/v1/chat/completions'
    with pytest.raises(FileExistsError): d['run'](path)
    assert len(d['calls']) == 28
    assert not any(report[k] for k in ('facts_attested','execution_authorized','predictive_quality_approved',
                                      'independent_quality_approved','native_ui_tested'))


@pytest.mark.parametrize('flag', PERMISSION)
@pytest.mark.parametrize('value', [False, 1, None])
def test_permissions_fail_before_provider_creation(diagnostic, flag, value):
    path = diagnostic['freeze']([GLM])
    with pytest.raises(PermissionError): evaluation.run(path, **(PERMISSION | {flag:value}))
    assert not diagnostic['calls'] and not (path.parent/'started.json').exists()


@pytest.mark.parametrize('change', ['hash', 'route', 'mode', 'source', 'question', 'budget'])
def test_frozen_protocol_and_source_reject_tampering(diagnostic, monkeypatch, change):
    path = diagnostic['freeze']([GLM])
    frozen = json.loads(path.read_text())
    if change=='hash': frozen['sha256']='0'*64
    if change=='route': frozen['protocol']['profiles'][0]['base_url']='https://elsewhere.invalid/v1'
    if change=='mode': frozen['protocol']['profiles'][0]['json_mode']='json_schema'
    if change=='question': frozen['protocol']['spec']['review']['questions'][0]['instructions']='Approve everything'
    if change=='budget': frozen['protocol']['maximum_requests']+=1
    if change=='source': monkeypatch.setattr(evaluation, 'source_manifest', lambda: dict(sha256='changed'))
    if change!='hash': frozen['sha256']=digest(frozen['protocol'])
    path.write_text(json.dumps(frozen))
    with pytest.raises(ValueError): diagnostic['run'](path)
    assert not diagnostic['calls']


@pytest.mark.parametrize('mode', ['unknown_cost', 'missing_answer', 'budget', 'http'])
def test_incomplete_panel_stops_entire_remaining_set(diagnostic, mode):
    d = diagnostic
    def change(data):
        if mode=='unknown_cost': data['usage'].pop('cost_nano_usd')
        if mode=='missing_answer': data['answers'].pop('next_check')
        if mode=='budget': data['usage']['cost_nano_usd']=evaluation.PANEL_COST_NANO_USD
        if mode=='http': return httpx.Response(503, text='untrusted provider diagnostic')
        return data
    d['transforms']['jev-latest'] = change
    report = d['run'](d['freeze']())
    assert report['status']=='partial_or_failed' and report['recorded_provider_call_attempts']==3
    assert report['not_started_models']==[DEEPSEEK, SONNET, OPUS]
    data = report['results'][0]['result']
    assert data['initial'] and not data['revision'] and not data['final_synthesis']
    assert data['challenges']['not_started_models']==['clef-flash','gpt-6-luna-decisions']
    assert 'untrusted provider diagnostic' not in json.dumps(report)


@pytest.mark.parametrize('kind', ['invalid', 'model', 'http'])
def test_planning_failure_is_retained_without_retry_and_next_distinct_model_runs(diagnostic, kind):
    d = diagnostic
    def change(data):
        if kind=='http': return httpx.Response(400, text='untrusted diagnostic')
        if kind=='invalid': data['choices'][0]['message']['content']='{}'
        if kind=='model': data['model']='substituted-model'
        return data
    d['transforms'][GLM]=change
    report = d['run'](d['freeze']([GLM,DEEPSEEK]))
    assert report['status']=='partial_or_failed' and report['recorded_provider_call_attempts']==8
    assert report['results'][0]['status']=='incomplete' and not report['results'][0]['result']['initial']
    assert report['results'][1]['status']=='completed'
    assert [p['model'] for _,p in d['calls']].count(GLM)==1
    assert 'untrusted diagnostic' not in json.dumps(report)


def test_authentication_failure_stops_later_models(diagnostic):
    d = diagnostic
    d['transforms'][GLM]=lambda data: httpx.Response(401)
    report = d['run'](d['freeze']())
    assert report['recorded_provider_call_attempts']==1 and report['not_started_models']==[DEEPSEEK,SONNET,OPUS]
    assert report['stop_reason']=='planning_access_failed_no_later_methods'


@pytest.mark.parametrize('model,stop,error', [
    (GLM, 'stop', 'invalid_json'), (DEEPSEEK, 'length', 'unsupported_response'),
    (SONNET, 'max_tokens', 'unsupported_response')])
def test_rejection_diagnostics_survive_real_host_retention(diagnostic, model, stop, error):
    d = diagnostic
    def change(data):
        if model == SONNET:
            data['stop_reason'] = stop
            data['content'] = [dict(type='thinking', thinking='private-hidden-reasoning')]
        else:
            data['choices'][0]['finish_reason'] = stop
            data['choices'][0]['message'].update(reasoning_content='private-hidden-reasoning',
                content='```json\n{}\n```' if model == GLM else None)
        return data
    d['transforms'][model] = change
    path = d['freeze']([model])
    report = d['run'](path)
    assert report['recorded_provider_call_attempts'] == 1 == len(d['calls'])
    row = report['results'][0]
    assert row['case_audit_unchanged'] and row['work_state'] == 'awaiting_review'
    assert not row['result']['initial'] and not row['result']['revision']
    call = row['result']['planning_receipt']['calls'][0]
    assert call['provider_stop_reason'] == stop and call['error_code'] == error
    assert call['provider_usage'] and call['response_body_sha256']
    saved = (path.parent/model/'transports.json').read_text()
    assert json.loads(saved)['planning'][0]['calls'][0] == call
    assert 'private-hidden-reasoning' not in saved and 'private-hidden-reasoning' not in json.dumps(report)


def test_all_selected_credentials_are_preflighted_and_environment_restored(diagnostic, monkeypatch):
    d = diagnostic
    monkeypatch.setenv('EIGHTBALL_API_MODEL','original-configuration')
    monkeypatch.delenv('ANTHROPIC_API_KEY')
    report = d['run'](d['freeze']())
    assert report['status']=='failed' and report['not_started_models']==list(evaluation.PROFILES)
    assert not d['calls'] and report['recorded_provider_call_attempts']==0
    assert os.environ['EIGHTBALL_API_MODEL']=='original-configuration'
    assert 'fictional_specialist_token' not in json.dumps(report)


def test_interrupt_retains_attempt_and_forbids_resume(diagnostic):
    d = diagnostic
    def interrupt(model, payload): raise KeyboardInterrupt()
    d['transforms']['effect']=interrupt
    path = d['freeze']()
    report = d['run'](path)
    assert report['status']=='interrupted' and report['recorded_provider_call_attempts']==1
    assert report['results'][0]['status']=='interrupted_or_harness_failed'
    assert (path.parent/GLM/'transports.json').exists()
    with pytest.raises(FileExistsError): d['run'](path)


def test_source_change_during_run_invalidates_record(diagnostic, monkeypatch):
    d = diagnostic
    path = d['freeze']([GLM, DEEPSEEK])
    d['transforms']['effect']=lambda *_: monkeypatch.setattr(evaluation, 'source_manifest', lambda: {})
    report = d['run'](path)
    assert report['status']=='failed_source_changed' and not report['source_unchanged']
    assert report['recorded_provider_call_attempts']==1 and report['not_started_models']==[DEEPSEEK]


@pytest.mark.parametrize('models', [[], [GLM,GLM], ['deepseek-v4.1']])
def test_no_implicit_substitution_or_duplicate_models(diagnostic, models):
    with pytest.raises(ValueError): diagnostic['freeze'](models)
    assert not diagnostic['calls']
