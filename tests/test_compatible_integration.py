"""Compatible-provider integration using controlled HTTP and actual SQLite jobs.

These are transport/lifecycle contracts, not real Qwen inference, independent
semantic evaluation, or human acceptance. No ambient credentials are used.
"""
from copy import deepcopy
from datetime import timedelta
from pathlib import Path
from threading import Event, Thread
import json

import httpx
import pytest
from fastapi.testclient import TestClient

from eightball.api import make_app
from eightball.models import uid
from eightball.store import Store as LegacyStore, digest
from eightball.v2.analysis_jobs import AnalysisJobs, AnalysisRequest
from eightball.v2.commands import Command
from eightball.v2.contracts import Case, Evidence, utcnow
from eightball.v2.intelligence import PROMPT_VERSION, propose
from eightball.v2.store import Store


ROOT = Path(__file__).resolve().parents[1]
STAGED = json.loads((ROOT / 'tests/fixtures/drafting/staged.json').read_text())
OUTCOME = "Obtain enough suitable chairs and the venue manager's written acceptance"
KEY = 'fixture_only_not_a_real_compatible_key'
BASE_URL = 'https://fixture-provider.invalid/v1'


@pytest.fixture(autouse=True)
def compatible_configuration(monkeypatch):
    for name in ('EIGHTBALL_API_BASE_URL', 'EIGHTBALL_API_MODEL', 'EIGHTBALL_API_PROVIDER',
                 'EIGHTBALL_API_KEY', 'EIGHTBALL_API_ROUTING_PROVIDER', 'EIGHTBALL_API_JSON_MODE'):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL', BASE_URL)
    monkeypatch.setenv('EIGHTBALL_API_MODEL', 'qwen/fixture-model')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER', 'fixture-provider')
    monkeypatch.setenv('EIGHTBALL_API_KEY', KEY)


def fixture_case():
    return Case(title='Compatible provider fixture', client='Fictional agency',
                summary='A fictional chair supplier refused a request.',
                desired_outcome=OUTCOME, deadline=utcnow() + timedelta(days=2),
                evidence=[Evidence(id='source', title='Fictional source', source='Test fixture',
                                   text='The supplier refused the request.')])


def envelope(output, model='fixture-served-model'):
    return {'model': model, 'choices': [{'index': 0, 'finish_reason': 'stop',
            'message': {'role': 'assistant', 'content': json.dumps(output)}}],
            'usage': {'prompt_tokens': 20, 'completion_tokens': 10, 'total_tokens': 30}}


def frame():
    result = deepcopy(STAGED['frame'])
    result['target_bindings'] = [{'criterion_index': i, 'target_quote': OUTCOME}
                                 for i in range(len(result['success_criteria']))]
    return result


def request(case, purpose='extract', **changes):
    body = dict(request_id=uid(), expected_revision=case.revision,
                provider='openai_compatible', purpose=purpose,
                source_ids=['source'], allow_external=True)
    body.update(changes)
    return AnalysisRequest(**body)


def controlled_provider(outputs=None, handler=None):
    """A real HTTPX stream with controlled responses; never contacts the network."""
    calls = []
    remaining = deepcopy(outputs or [])

    def respond(req):
        calls.append(req)
        if handler:
            return handler(req)
        return httpx.Response(200, json=envelope(remaining.pop(0)))

    def factory(**kwargs):
        return httpx.Client(transport=httpx.MockTransport(respond), **kwargs)

    return factory, calls


@pytest.mark.parametrize('purpose', ['extract', 'graph'])
@pytest.mark.parametrize('transport', ['anthropic', 'prompt_only'])
def test_prompt_only_uses_existing_unassisted_proposal_gate(monkeypatch, purpose, transport):
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL', 'https://api.anthropic.com/v1')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER', 'anthropic')
    monkeypatch.setenv('EIGHTBALL_API_MODEL', 'claude-sonnet-5-5')
    if transport == 'prompt_only':
        monkeypatch.setenv('EIGHTBALL_API_BASE_URL', BASE_URL)
        monkeypatch.setenv('EIGHTBALL_API_PROVIDER', 'fixture-provider')
        monkeypatch.setenv('EIGHTBALL_API_JSON_MODE', 'prompt_only')
    case = fixture_case(); before = case.model_dump(mode='json')
    outputs = ([{'items': [{'kind': 'claim', 'text': 'Supplier refused',
                           'source': {'evidence_id': 'source', 'quote': case.evidence[0].text}}]}]
               if purpose == 'extract' else [frame(), deepcopy(STAGED['routes'])])
    def respond(req):
        assert 'response_format' not in json.loads(req.content)
        if transport == 'prompt_only':
            assert str(req.url) == BASE_URL + '/chat/completions'
            return httpx.Response(200, json=envelope(outputs.pop(0)))
        assert str(req.url) == 'https://api.anthropic.com/v1/messages'
        return httpx.Response(200, json={'model': 'claude-sonnet-5-5', 'type': 'message',
            'role': 'assistant', 'stop_reason': 'end_turn', 'content': [
                {'type': 'thinking', 'thinking': '', 'signature': 'opaque'},
                {'type': 'text', 'text': json.dumps(outputs.pop(0))}],
            'usage': {'input_tokens': 30, 'output_tokens': 20}})
    factory, calls = controlled_provider(handler=respond)
    with factory() as cl:
        proposal = propose(case, 'openai_compatible', purpose, ['source'], allow_external=True, client=cl)
    assert case.model_dump(mode='json') == before
    assert len(calls) == (2 if purpose == 'graph' else 1)
    assert proposal.raw_output['transport']['transport'] == ('anthropic_messages' if transport == 'anthropic' else 'openai_compatible')
    assert proposal.raw_output['transport']['response_mode'] == 'prompt_only'
    assert all(i.kind not in ('observation', 'approval') for i in proposal.items)
    assert all(i.object['approval_required'] for i in proposal.items if i.kind == 'action')


@pytest.mark.parametrize('invalid', ['extra_field', 'target_quote', 'value_type'])
def test_prompt_only_invalid_frame_stops_before_routes(monkeypatch, invalid):
    monkeypatch.setenv('EIGHTBALL_API_JSON_MODE', 'prompt_only')
    case = fixture_case()
    before = case.model_dump(mode='json')
    output = frame()
    if invalid == 'extra_field': output['execution_authorized'] = True
    if invalid == 'target_quote': output['target_bindings'][0]['target_quote'] = 'Unrelated target'
    if invalid == 'value_type': output['verification']['minutes'] = 'one'
    factory, calls = controlled_provider(outputs=[output])
    with factory() as cl, pytest.raises(ValueError):
        propose(case, 'openai_compatible', 'graph', ['source'], allow_external=True, client=cl)
    assert len(calls) == 1 and case.model_dump(mode='json') == before
    assert 'response_format' not in json.loads(calls[0].content)


def queued(tmp_path, outputs=None, handler=None):
    store = Store(str(tmp_path / 'compatible.db'))
    case = store.create(fixture_case(), fixture=True)
    factory, calls = controlled_provider(outputs, handler)
    manager = AnalysisJobs(store, launch=False, client_factory=factory)
    return store, case, manager, calls


def assert_clean_transport(proposal, count):
    transport = proposal['raw_output']['transport']
    assert transport['requested_model'] == 'qwen/fixture-model'
    assert transport['explicit_operator_permission'] is True
    assert transport['automatic_routing'] is False
    assert len(transport['calls']) == count
    assert all(call['elapsed_ms'] >= 0 for call in transport['calls'])
    assert KEY not in json.dumps(proposal)
    return transport


def test_queue_retains_typed_extraction_with_exact_span_without_case_mutation(tmp_path):
    raw = {'items': [{'kind': 'claim', 'text': 'The supplier refused the request.',
                     'source': {'evidence_id': 'source', 'quote': 'The supplier refused the request.'}}]}
    store, case, manager, calls = queued(tmp_path, [raw])
    before = store.audit(case.id)
    job = manager.submit(case.id, request(case))
    assert manager.run_next()
    done = manager.get(case.id, job['id'])
    assert done['status'] == 'succeeded' and not done['worker_active']
    assert done['calls_started'] == done['calls_completed'] == 1
    saved = store.proposals(case.id)
    assert len(saved) == 1 and done['proposal_id'] == saved[0]['id']
    proposal = saved[0]
    assert proposal['status'] == 'pending' and proposal['model'] == 'fixture-served-model'
    assert proposal['provider'] == 'openai_compatible' and proposal['base_revision'] == 0
    assert proposal['raw_output']['payload'] == raw
    item = proposal['items'][0]
    assert item['kind'] == 'claim'
    assert item['object']['provenance']['origin'] == 'model_proposal'
    assert item['object']['provenance']['references'] == [
        {'evidence_id': 'source', 'start': 0, 'end': len(case.evidence[0].text),
         'quote': case.evidence[0].text}]
    transport = assert_clean_transport(proposal, 1)
    assert transport['calls'][0]['usage']['total_tokens'] == 30
    assert proposal['output_hash'] == digest(proposal['raw_output'])
    assert str(calls[0].url) == BASE_URL + '/chat/completions'
    assert calls[0].headers['authorization'] == 'Bearer ' + KEY
    assert KEY not in calls[0].content.decode()
    assert store.get(case.id) == case
    after = store.audit(case.id)
    assert {k: v for k, v in after.items() if k != 'model_runs'} == {
        k: v for k, v in before.items() if k != 'model_runs'}
    assert after['model_runs'] == [{'proposal': proposal, 'review': None}]


@pytest.mark.parametrize('invalid,code', [
    ('shape', 'invalid_extraction_shape'), ('span', 'unsupported_extraction_span')])
def test_queue_retains_invalid_parsed_extraction_and_transport(tmp_path, invalid, code):
    raw = {'items': [{'kind': 'claim', 'text': 'A fictional unsupported statement.',
                     'source': {'evidence_id': 'source', 'quote': 'An absent quote.'}}]}
    if invalid == 'shape':
        raw['items'][0]['kind'] = 'observation'
    store, case, manager, calls = queued(tmp_path, [raw])
    job = manager.submit(case.id, request(case))
    assert manager.run_next()
    done = manager.get(case.id, job['id'])
    proposal = store.proposals(case.id)[0]
    assert done['status'] == proposal['status'] == 'failed'
    assert done['proposal_id'] == proposal['id'] and not proposal['items']
    assert len(calls) == done['calls_started'] == done['calls_completed'] == 1
    trace = proposal['raw_output']
    assert trace['failed_stage'] == 'extraction' and trace['extraction'] == raw
    assert trace['diagnostic']['code'] == code and trace['prompt_version'] == PROMPT_VERSION
    assert proposal['model'] == 'fixture-served-model' and store.get(case.id) == case
    assert proposal['output_hash'] == digest(trace)
    assert_clean_transport(proposal, 1)
    assert AnalysisJobs(store, launch=False).get(case.id, job['id'])['proposal_id'] == proposal['id']


def test_actual_queue_compiles_both_stages_without_acceptance_or_case_changes(tmp_path):
    store, case, manager, calls = queued(tmp_path, [frame(), STAGED['routes']])
    job = manager.submit(case.id, request(case, 'graph'))
    assert manager.run_next()
    done = manager.get(case.id, job['id'])
    assert done['status'] == 'succeeded' and done['calls_started'] == done['calls_completed'] == 2
    proposal = store.proposals(case.id)[0]
    trace = proposal['raw_output']['payload']
    assert trace['frame'] == frame() and trace['routes'] == STAGED['routes']
    assert trace['stage_count'] == 2 and trace['target_coverage_checked'] is True
    assert trace['target_bindings'] == frame()['target_bindings']
    assert trace['prompt_version'] and trace['compiler_version']
    actions = [item['object'] for item in proposal['items'] if item['kind'] == 'action']
    assert actions and all(action['approval_required'] for action in actions)
    assert len(calls) == 2 and store.get(case.id) == case and not case.graph.actions
    assert_clean_transport(proposal, 2)


def test_bad_frame_preserves_raw_failure_and_prevents_second_stage(tmp_path):
    invalid = frame()
    invalid['verification']['requires_existing'] = ['invented-existing-condition']
    store, case, manager, calls = queued(tmp_path, [invalid])
    job = manager.submit(case.id, request(case, 'graph'))
    assert manager.run_next()
    done = manager.get(case.id, job['id'])
    proposal = store.proposals(case.id)[0]
    assert done['status'] == 'failed' and len(calls) == 1
    assert not proposal['items'] and proposal['raw_output']['frame'] == invalid
    assert proposal['raw_output']['failed_stage'] == 'frame'
    assert proposal['raw_output']['diagnostic']['code'] == 'unknown_existing_reference'
    assert store.get(case.id) == case
    assert_clean_transport(proposal, 1)


def test_served_model_change_between_stages_is_a_retained_failure(tmp_path):
    responses = [envelope(frame(), 'fixture-model-a'),
                 envelope(STAGED['routes'], 'fixture-model-b')]

    def respond(req):
        return httpx.Response(200, json=responses.pop(0))

    store, case, manager, calls = queued(tmp_path, handler=respond)
    job = manager.submit(case.id, request(case, 'graph'))
    assert manager.run_next()
    done = manager.get(case.id, job['id'])
    proposal = store.proposals(case.id)[0]
    assert done['status'] == 'failed' and len(calls) == 2
    assert not proposal['items'] and proposal['model'] == 'fixture-model-a'
    trace = proposal['raw_output']
    assert trace['failed_stage'] == 'routes' and trace['stage_count'] == 2
    assert trace['frame'] == frame() and trace['routes'] == STAGED['routes']
    transport = assert_clean_transport(proposal, 2)
    assert [call['served_model'] for call in transport['calls']] == ['fixture-model-a', 'fixture-model-b']
    assert store.get(case.id) == case and not manager.run_next()


def test_two_stages_keep_the_same_explicit_configuration(monkeypatch):
    responses = [frame(), STAGED['routes']]

    def respond(req):
        raw = responses.pop(0)
        if responses:
            # A config edit during a call applies only to a later analysis.
            monkeypatch.setenv('EIGHTBALL_API_BASE_URL', 'https://different.invalid/v1')
            monkeypatch.setenv('EIGHTBALL_API_MODEL', 'different/model')
            monkeypatch.setenv('EIGHTBALL_API_PROVIDER', 'different-provider')
            monkeypatch.setenv('EIGHTBALL_API_KEY', 'different_fixture_key')
        return httpx.Response(200, json=envelope(raw))

    factory, calls = controlled_provider(handler=respond)
    case = fixture_case()
    with factory() as client:
        proposal = propose(case, 'openai_compatible', 'graph', ['source'],
                           allow_external=True, client=client)
    assert len(calls) == 2 and proposal.status == 'pending'
    assert all(str(call.url) == BASE_URL + '/chat/completions' for call in calls)
    assert all(json.loads(call.content)['model'] == 'qwen/fixture-model' for call in calls)
    assert all(call.headers['authorization'] == 'Bearer ' + KEY for call in calls)
    assert_clean_transport(proposal.model_dump(mode='json'), 2)
    assert 'different_fixture_key' not in proposal.model_dump_json()


@pytest.mark.parametrize('stop', ['cancel', 'stale', 'restart'])
@pytest.mark.parametrize('native', [False, True])
def test_inflight_stage_one_stop_discards_output_and_never_sends_stage_two(tmp_path, stop, native, monkeypatch):
    if native:
        monkeypatch.setenv('EIGHTBALL_API_BASE_URL', 'https://api.anthropic.com/v1')
        monkeypatch.setenv('EIGHTBALL_API_PROVIDER', 'anthropic')
        monkeypatch.setenv('EIGHTBALL_API_MODEL', 'claude-sonnet-5-5')
    entered, release = Event(), Event()

    def respond(req):
        entered.set()
        assert release.wait(5)
        result = ({'model': 'claude-sonnet-5-5', 'type': 'message', 'role': 'assistant',
                   'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': json.dumps(frame())}]}
                  if native else envelope(frame()))
        return httpx.Response(200, json=result)

    store, case, manager, calls = queued(tmp_path, handler=respond)
    job = manager.submit(case.id, request(case, 'graph'))
    worker = Thread(target=manager.run_next)
    worker.start()
    assert entered.wait(5)
    try:
        if stop == 'cancel':
            cancelled = manager.cancel(case.id, job['id'])
            assert cancelled['worker_active'] and cancelled['status'] == 'cancelled'
        elif stop == 'stale':
            store.change(case.id, Command(event_id=uid(), expected_revision=0,
                         kind='metadata', payload={'budget': 5000}))
        else:
            restarted = AnalysisJobs(store, launch=False)
            assert restarted.get(case.id, job['id'])['status'] == 'interrupted'
            assert not restarted.run_next()
    finally:
        release.set()
        worker.join(5)
    assert not worker.is_alive()
    done = manager.get(case.id, job['id'])
    assert done['status'] == {'cancel': 'cancelled', 'stale': 'superseded',
                              'restart': 'interrupted'}[stop]
    assert len(calls) == done['calls_started'] == 1 and not done['worker_active']
    assert not done['proposal_id'] and not store.proposals(case.id)
    assert not manager.run_next()
    assert store.get(case.id).observations == case.observations


@pytest.mark.parametrize('stop', ['cancel', 'stale', 'restart'])
def test_pending_stop_never_opens_provider_connection(tmp_path, stop):
    store, case, manager, calls = queued(tmp_path, [frame(), STAGED['routes']])
    job = manager.submit(case.id, request(case, 'graph'))
    if stop == 'cancel':
        manager.cancel(case.id, job['id'])
    elif stop == 'stale':
        store.change(case.id, Command(event_id=uid(), expected_revision=0,
                     kind='metadata', payload={'budget': 5000}))
    else:
        manager = AnalysisJobs(store, launch=False)
    manager.run_next()
    done = manager.get(case.id, job['id'])
    assert done['status'] == {'cancel': 'cancelled', 'stale': 'superseded',
                              'restart': 'interrupted'}[stop]
    assert not calls and done['calls_started'] == done['calls_completed'] == 0
    assert not store.proposals(case.id)


@pytest.mark.parametrize('problem', ['missing_key', 'insecure_endpoint', 'no_permission', 'foreign_source'])
def test_invalid_setup_or_scope_is_rejected_before_job_admission(tmp_path, monkeypatch, problem):
    store, case, manager, calls = queued(tmp_path)
    changes = {}
    if problem == 'missing_key':
        monkeypatch.delenv('EIGHTBALL_API_KEY')
    elif problem == 'insecure_endpoint':
        monkeypatch.setenv('EIGHTBALL_API_BASE_URL', 'http://untrusted.invalid/v1')
    elif problem == 'no_permission':
        changes['allow_external'] = False
    else:
        changes['source_ids'] = ['foreign-case-source']
    with pytest.raises(ValueError):
        manager.submit(case.id, request(case, **changes))
    assert not calls and not manager.list(case.id) and not store.proposals(case.id)
    assert store.get(case.id) == case


@pytest.mark.parametrize('status,code', [(401, 'authentication_failed'), (429, 'rate_limited'),
                                       (500, 'provider_rejected_request')])
def test_transport_failure_persists_safe_receipt_without_error_body_or_retry(tmp_path, status, code):
    def respond(req):
        return httpx.Response(status, text='Private upstream body ' + KEY)

    store, case, manager, calls = queued(tmp_path, handler=respond)
    job = manager.submit(case.id, request(case))
    assert manager.run_next()
    done = manager.get(case.id, job['id'])
    proposal = store.proposals(case.id)[0]
    assert done['status'] == proposal['status'] == 'failed' and len(calls) == 1
    trace = proposal['raw_output']
    assert trace['diagnostic']['code'] == code
    assert trace['transport']['calls'][0]['http_status'] == status
    assert trace['transport']['calls'][0]['status'] == 'failed'
    assert 'Private upstream body' not in json.dumps(proposal)
    assert KEY not in json.dumps(manager.list(case.id)) and store.get(case.id) == case
    assert_clean_transport(proposal, 1)


def test_authenticated_job_api_uses_compatible_transport_and_retains_review_only_result(tmp_path):
    old = LegacyStore(str(tmp_path / 'compatible-api.db'))
    store = Store(old.path)
    case = store.create(fixture_case(), fixture=True)
    operator_token = 'fixture_local_operator_token_not_live_1234'
    app = make_app(old, operator_token)
    factory, calls = controlled_provider([{'items': []}])
    manager = app.state.analysis_jobs
    manager.launch = False
    manager.client_factory = factory
    api = TestClient(app, headers={'Authorization': 'Bearer ' + operator_token})
    base = '/api/v2/cases/' + case.id
    body = request(case).model_dump(mode='json')
    assert TestClient(app).post(base + '/analysis-jobs', json=body).status_code == 401
    assert not calls
    response = api.post(base + '/analysis-jobs', json=body)
    assert response.status_code == 202
    assert manager.run_next()
    done = api.get(base + '/analysis-jobs/' + response.json()['id']).json()
    assert done['status'] == 'succeeded' and done['proposal_id']
    assert api.post(base + '/analysis-jobs', json=body).json()['id'] == done['id']
    assert not manager.run_next() and len(calls) == 1
    saved = api.get(base + '/proposals').json()
    assert len(saved) == 1 and saved[0]['status'] == 'pending'
    assert_clean_transport(saved[0], 1)
    assert store.get(case.id) == case and store.audit(case.id)['valid']


def test_compatible_question_context_excludes_unselected_source_and_answers():
    from eightball.v2.contracts import Condition, Provenance, Question, Span
    case = fixture_case()
    secret = 'Unselected fictional source whose content must remain local.'
    case.evidence.append(Evidence(id='other-source', title='Not selected', source='Fixture', text=secret))
    case.graph.conditions.append(Condition(id='goal', title='Approval received', confirmation='Reviewed written approval',
        provenance=Provenance(references=[Span(evidence_id='other-source', start=0,
                                               end=len(secret), quote=secret)])))
    case.questions.append(Question(id='authority', question='Who approves?', why='Authority needs checking', answer=secret))
    factory, calls = controlled_provider([{'questions': []}])
    with factory() as client:
        proposal = propose(case, 'openai_compatible', 'questions', ['source'],
                           allow_external=True, client=client)
    assert len(calls) == 1 and not proposal.items
    payload = json.loads(calls[0].content)
    assert secret not in json.dumps(payload) and 'Approval received' in json.dumps(payload)
    assert KEY not in proposal.model_dump_json()
