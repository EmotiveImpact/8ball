"""Controlled contracts and actual host transactions, never live model quality."""
from copy import deepcopy
from datetime import timedelta
import json
import lzma
from pathlib import Path
import sqlite3

import httpx
import pytest
from pydantic import ValidationError

from endstate.intelligence.coordination import summarize
from endstate.intelligence.planning import CoordinatedPlanningSpec, coordinate, fingerprint
from eightball.event_inbox import EventConflict
from eightball.event_workers.planning import CoordinatedPlanningProcessor
from eightball.store import digest
from eightball.v2.commands import Command
from eightball.v2.compatible import CompatibleSession
from eightball.v2.decision_models import DecisionSession
from eightball.v2.hosted import HostedSetupRequired
from tests.test_compatible_integration import OUTCOME, STAGED, envelope, frame
from tests.test_compatible_provider import configure
from tests.test_event_dispatch import dispatch, process, status
from tests.test_specialist_review import MODELS, attempt, specification, wire


def spec(**changes):
    return CoordinatedPlanningSpec(id='fictional-coordination', outcome=OUTCOME,
        review=specification(), max_seconds=120,
        planning_cost_policy='explicit_unpriced_token_bound', **changes)


def outputs():
    revised = frame()
    revised['verification']['title'] = 'Review delivery evidence and written venue acceptance'
    return [frame(), deepcopy(STAGED['routes']), revised, deepcopy(STAGED['routes'])]


def core_run(values=None, *, text='Fictional source: venue spares or local hire may be available.',
             transform_panel=None, served=None):
    values = outputs() if values is None else values
    calls, panels = [], []
    def generate(schema, instructions, context):
        calls.append(deepcopy(context))
        assert 'bare JSON object' in instructions and 'no Markdown fences' in instructions
        assert 'maxLength' in instructions and 'overlength values are rejected' in instructions
        if len(calls) >= 3:
            assert 'EVERY' in instructions
            context['review_context']['original_proposal']['frame']['verification']['title'] = 'Mutated copy'
        return deepcopy(values[len(calls)-1]), served[len(calls)-1] if served else 'fixture-model'
    def review(state, checkpoint):
        panels.append(state)
        result = summarize(spec().review, [attempt(model, choice) for model, choice
                                          in zip(MODELS, ['review', 'accept', 'review'])])
        result.update(stop_reason='completed', input_sha256=fingerprint(state))
        if transform_panel: transform_panel(result)
        return result
    return coordinate(spec(), text, 'fixture-run', generate, review, lambda: None), calls, panels


def test_core_preserves_baseline_every_challenge_and_separate_revision():
    result, calls, panels = core_run()
    assert result['stop_reason'] == 'completed' and len(calls) == 4 and len(panels) == 1
    assert all('review_context' not in c for c in calls[:2])
    panel = result['challenges']
    assert panel['questions'][0]['disagreement']
    assert panel['questions'][0]['choices'] == dict(zip(MODELS, ['review', 'accept', 'review']))
    assert calls[2]['review_context']['specialists'] == panel == calls[3]['review_context']['specialists']
    assert result['initial']['trace']['frame'] == frame()
    assert result['revision']['trace']['frame'] != frame()
    assert json.loads(panels[0])['original_proposal']['frame'] == frame()
    assert result['initial']['compiled']['graph']['objectives'][0]['title'] == OUTCOME
    assert result['revision']['compiled']['graph']['objectives'][0]['title'] == OUTCOME
    ids = [{a['id'] for a in result[key]['compiled']['graph']['actions']} for key in ('initial', 'revision')]
    assert not ids[0] & ids[1]
    assert result['final_synthesis'] == dict(candidate='revision', requires_operator_review=True,
                                            objections_resolved=False, selected_route=None)
    assert result['advisory_only'] and not result['facts_attested'] and not result['execution_authorized']
    assert not result['predictive_quality_approved']


@pytest.mark.parametrize('stage', range(4))
def test_core_invalid_draft_stops_without_retry_or_silent_target_change(stage):
    values = outputs()
    values[stage] = {}
    result, calls, panels = core_run(values)
    assert len(calls) == stage+1 and result['final_synthesis'] is None
    assert result['failed_draft']['failed_stage'] == ('frame' if stage % 2 == 0 else 'routes')
    assert bool(panels) == (stage >= 2)
    assert bool(result['initial']) == (stage >= 2)


@pytest.mark.parametrize('stage', [0, 2])
@pytest.mark.parametrize('field', ['readiness', 'success_criteria'])
@pytest.mark.parametrize('length', [180, 181])
def test_confirmation_limits_are_identical_before_and_after_challenge(stage, field, length):
    values = outputs()
    criterion = values[stage][field] if field == 'readiness' else values[stage][field][0]
    criterion['confirmation'] = 'x' * length
    result, calls, panels = core_run(values)
    if length == 180:
        assert result['stop_reason'] == 'completed' and len(calls) == 4
    else:
        assert result['stop_reason'] == 'invalid_' + ('initial' if stage == 0 else 'revision') + '_draft'
        assert len(calls) == stage + 1 and bool(panels) == (stage == 2)
        assert result['failed_draft']['frame'] == values[stage]
        assert result['failed_draft']['diagnostic']['fields'][0]['type'] == 'string_too_long'
        assert result['revision'] is None and result['final_synthesis'] is None


@pytest.mark.parametrize('index,expected_calls', [(0, 3), (1, 1)])
def test_retained_native_cost_failures_are_not_repaired_by_prompt_changes(index, expected_calls):
    path = Path(__file__).resolve().parents[1] / 'docs/evidence/coordinated-native-cost-live-2026-10-26.json.xz'
    files = json.loads(lzma.decompress(path.read_bytes()))['files']
    original = json.loads(files['report.json'])['results'][index]['result']
    fixture = json.loads(files['protocol.json'])['protocol']['fixture']
    retained_calls = original['planning_receipt']['calls']
    calls = []

    def generate(schema, instructions, context):
        content = retained_calls[len(calls)]['raw_content']
        calls.append(content)
        return json.loads(content), original['planning_receipt']['requested_model']

    def review(state, checkpoint):
        panel = deepcopy(original['challenges'])
        assert panel['input_sha256'] == fingerprint(state)
        return panel

    result = coordinate(CoordinatedPlanningSpec.model_validate(original['spec']),
                        fixture['text'], 'offline-retained-content-replay', generate, review, lambda: None)
    assert len(calls) == expected_calls
    assert result['revision'] is None and result['final_synthesis'] is None
    assert result['failed_draft']['failed_stage'] == 'frame'
    if index == 0:
        assert result['initial']['trace']['frame'] == original['initial']['trace']['frame']
        assert result['failed_draft']['frame'] == original['failed_draft']['frame']
        assert result['challenges'] == original['challenges']
    else:
        assert result['initial'] is None and result['challenges'] is None


@pytest.mark.parametrize('field', ['unknown_cost', 'failed', 'missing', 'budget', 'summary', 'binding'])
def test_core_no_revision_after_partial_or_inconsistent_panel(field):
    def change(panel):
        if field in ('summary', 'binding'):
            panel['answered_models' if field == 'summary' else 'input_sha256'] = 99
            return
        rows = [attempt(MODELS[0])]
        if field == 'unknown_cost': rows = [attempt(MODELS[0], cost=None)]
        if field == 'failed': rows[0].status = 'failed'; rows[0].answers = {}
        if field == 'budget': rows = [attempt(MODELS[0], cost=10)]
        panel.update(summarize(spec().review, rows))
    result, calls, _ = core_run(transform_panel=change)
    assert len(calls) == 2 and result['initial'] is not None
    assert result['revision'] is None and result['final_synthesis'] is None
    assert result['stop_reason'] != 'completed'


def test_core_oversized_challenge_is_not_truncated_and_initial_is_preserved():
    result, calls, panels = core_run(text='x'*11900)
    assert len(calls) == 2 and not panels
    assert result['initial'] and result['stop_reason'] == 'invalid_challenge_input_or_result'


def test_core_cross_phase_model_change_cannot_produce_final_synthesis():
    result, _, _ = core_run(served=['one', 'one', 'two', 'two'])
    assert result['stop_reason'] == 'changed_planning_model'
    assert result['initial'] and result['revision'] and not result['final_synthesis']


def test_unchanged_revision_is_valid_but_not_evidence_of_improvement():
    original = [frame(), deepcopy(STAGED['routes'])]
    result, calls, _ = core_run(original + deepcopy(original))
    assert result['stop_reason'] == 'completed' and len(calls) == 4
    for key in ('frame', 'routes'):
        assert result['initial']['trace'][key] == result['revision']['trace'][key]
    assert not result['final_synthesis']['objections_resolved']
    assert result['final_synthesis']['selected_route'] is None


@pytest.mark.parametrize('patch', [dict(max_seconds=True), dict(max_seconds=0),
    dict(max_seconds=601), dict(planning_cost_policy='free'), dict(automatic_retry=True)])
def test_explicit_spec_rejects_implicit_or_unsafe_limits(patch):
    value = spec().model_dump(mode='python') | patch
    with pytest.raises(ValidationError): CoordinatedPlanningSpec.model_validate(value)


def test_unpriced_planning_requires_explicit_declared_policy():
    value = spec().model_dump(mode='python')
    value.pop('planning_cost_policy')
    with pytest.raises(ValidationError): CoordinatedPlanningSpec.model_validate(value)


@pytest.fixture
def coordinated(dispatch, monkeypatch, request):
    d = dispatch
    configure(monkeypatch)
    for key in ('EIGHTBALL_API_JSON_MODE', 'EIGHTBALL_API_ROUTING_PROVIDER'):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv('EXPERIENTIAL_API_KEY', 'fictional-specialist-transport-token')
    calls, after, transform, ticks = [], [None], [None], [0]
    planned = outputs()
    def serve(req):
        payload = json.loads(req.content)
        planning = req.url.host == 'api.fixture.example'
        value = envelope(planned.pop(0), model=payload['model']) if planning else wire(
            payload['model'], 'accept' if payload['model'] == 'clef-flash' else 'review')
        calls.append(dict(kind='planning' if planning else 'specialist', payload=payload))
        if transform[0]: value = transform[0](value, len(calls), planning)
        if after[0]: after[0](len(calls))
        return value if isinstance(value, httpx.Response) else httpx.Response(200, json=value)
    client = httpx.Client(transport=httpx.MockTransport(serve))
    request.addfinalizer(client.close)
    processor = CoordinatedPlanningProcessor(spec(), allow_external=True,
        planning_session_factory=lambda **kw: CompatibleSession(client=client, **kw),
        specialist_session_factory=lambda **kw: DecisionSession(client=client, **kw),
        timer=lambda: ticks[0])
    d['service'].cancel(case_id=d['case'].id, identity=d['operator'], work_id=d['work_id'])
    d['service'].processor = processor
    review = d['service'].review_source(case_id=d['case'].id, identity=d['operator'],
        sequence=d['receipt'].sequence, expected_revision=d['case'].revision,
        receipt_sha256=digest(d['receipt'].model_dump(mode='json')),
        rationale='Explicit fictional reviewed-text coordinated planning and unpriced token allowance.')
    d['work_id'] = d['service'].enqueue(**(d['enqueue'] | {'request_id':'coordinated', 'review_id':review['id']}))
    return d, processor, calls, after, transform, ticks


def retained(d):
    return json.loads(status(d)['work']['result'])


def test_real_host_and_transports_preserve_the_full_advisory_method(coordinated):
    d, _, calls, _, _, _ = coordinated
    before = d['store'].audit(d['case'].id)
    assert process(d)['state'] == 'awaiting_review'
    result = retained(d)
    assert [c['kind'] for c in calls] == ['planning']*2 + ['specialist']*3 + ['planning']*2
    assert result['stop_reason'] == 'completed' and result['generation_attempts'] == 4
    assert result['receipt_sha256'] == digest(d['receipt'].model_dump(mode='json'))
    assert result['base_revision'] == d['case'].revision and result['case_id'] == d['case'].id
    states = [c['payload'].get('state', c['payload'].get('input')) for c in calls[2:5]]
    assert len(set(states)) == 1 and 'specialists' not in json.loads(states[0])
    for call in calls[5:]:
        context = json.loads(call['payload']['messages'][1]['content'])
        assert context['review_context']['specialists']['questions'][0]['disagreement']
    assert len(result['planning_receipt']['calls']) == 4
    assert all(c['raw_content'] and c['request_sha256'] and c['response_body_sha256']
               for c in result['planning_receipt']['calls'])
    assert len(result['specialist_receipts']) == 3
    assert all(r['response'] and r['receipt']['response_sha256'] for r in result['specialist_receipts'])
    assert d['store'].audit(d['case'].id) == before
    assert d['case'].summary and d['case'].summary not in json.dumps(calls)
    assert 'explicit_unpriced_token_bound' in json.dumps(result)
    assert result['planning_cost_status'] == 'unknown_not_provider_reported'


def invalidate(d, processor, monkeypatch, mode):
    if mode == 'grant': d['registry'].revoke('worker')
    if mode == 'source': d['policy_state']['allowed'] = False
    if mode == 'cancel': d['service'].cancel(case_id=d['case'].id, identity=d['operator'], work_id=d['work_id'])
    if mode == 'lease': d['clock'][0] += timedelta(seconds=61)
    if mode == 'configuration': processor.spec.max_seconds += 1
    if mode == 'provider': monkeypatch.setenv('EIGHTBALL_API_MODEL', 'changed-model')
    if mode == 'credential': monkeypatch.setenv('EIGHTBALL_API_KEY', 'rotated-fixture-api-key')
    if mode == 'specialist_credential': monkeypatch.setenv('EXPERIENTIAL_API_KEY', 'rotated-fictional-specialist-key')
    if mode == 'revision':
        d['store'].change(d['case'].id, Command(event_id='change-after-request', expected_revision=0,
            kind='replace_graph', payload={'graph':d['case'].graph.model_dump(mode='json')}))


@pytest.mark.parametrize('after_call', range(1, 8))
@pytest.mark.parametrize('mode', ['grant', 'source', 'cancel', 'lease', 'configuration', 'provider', 'credential', 'specialist_credential', 'revision'])
def test_every_actual_request_rechecks_authority_before_next_stage_or_publication(coordinated, monkeypatch, mode, after_call):
    d, processor, calls, after, _, _ = coordinated
    after[0] = lambda count: invalidate(d, processor, monkeypatch, mode) if count == after_call else None
    assert process(d)['state'] != 'awaiting_review'
    assert len(calls) == after_call
    with sqlite3.connect(d['store'].path) as db:
        assert db.execute('SELECT result FROM event_work WHERE id=?', (d['work_id'],)).fetchone()[0] is None
        assert db.execute('SELECT output FROM event_dispatch_runs WHERE work_id=?', (d['work_id'],)).fetchone()[0] is None
    assert d['service'].inference_slot.acquire(blocking=False)
    d['service'].inference_slot.release()


@pytest.mark.parametrize('mode', ['configuration', 'provider', 'credential', 'specialist_credential'])
def test_changed_queued_configuration_requires_review_before_http(coordinated, monkeypatch, mode):
    d, processor, calls, _, _, _ = coordinated
    invalidate(d, processor, monkeypatch, mode)
    with pytest.raises(EventConflict): process(d)
    assert not calls


@pytest.mark.parametrize('at_call', [0, 1, 3, 5, 7])
def test_cost_policy_change_invalidates_queued_or_inflight_authority(coordinated, monkeypatch, at_call):
    d, processor, calls, after, _, _ = coordinated
    original = processor.configuration_sha256
    def mutate(count):
        if count == at_call:
            monkeypatch.setattr('eightball.event_workers.planning.COST_POLICY', 'changed_policy')
    if at_call:
        after[0] = mutate
        assert process(d)['state'] == 'permission_denied'
    else:
        mutate(0)
        with pytest.raises(EventConflict): process(d)
    assert processor.configuration_sha256 != original and len(calls) == at_call
    assert status(d)['work']['result'] is None


@pytest.mark.parametrize('at_call', [3, 4, 5])
@pytest.mark.parametrize('mode', ['cost_missing', 'cost_budget', 'invalid_answer'])
def test_incomplete_specialist_panel_preserves_initial_and_stops_revision(coordinated, at_call, mode):
    d, _, calls, _, transform, _ = coordinated
    def alter(value, count, planning):
        if count == at_call:
            if mode == 'cost_missing': value['usage'].pop('cost_nano_usd')
            if mode == 'cost_budget': value['usage']['cost_nano_usd'] = 10
            if mode == 'invalid_answer': value['answers'] = {}
        return value
    transform[0] = alter
    assert process(d)['state'] == 'awaiting_review'
    result = retained(d)
    assert len(calls) == at_call and result['initial'] and not result['revision']
    assert result['stop_reason'] == 'specialist_review_incomplete'
    assert len(result['specialist_receipts']) == at_call-2


@pytest.mark.parametrize('at_call', [1, 2, 3, 4, 5, 6, 7])
def test_global_deadline_stops_later_requests_but_cannot_recall_inflight(coordinated, at_call):
    d, _, calls, after, _, ticks = coordinated
    after[0] = lambda count: ticks.__setitem__(0, 121) if count == at_call else None
    assert process(d)['state'] == 'awaiting_review'
    result = retained(d)
    assert len(calls) == at_call and result['stop_reason'] == 'time_budget'
    assert result['final_synthesis'] is None


@pytest.mark.parametrize('at_call', [1, 2, 6, 7])
@pytest.mark.parametrize('mode', ['fenced', 'model'])
def test_invalid_or_substituted_planning_response_stops_and_retains_failure(coordinated, at_call, mode):
    d, _, calls, _, transform, _ = coordinated
    def alter(value, count, planning):
        if count == at_call:
            if mode == 'fenced': value['choices'][0]['message']['content'] = '```json\n{}\n```'
            if mode == 'model': value['model'] = 'unselected-model'
        return value
    transform[0] = alter
    assert process(d)['state'] == 'awaiting_review'
    result = retained(d)
    assert len(calls) == at_call and result['stop_reason'] != 'completed'
    assert result['final_synthesis'] is None
    assert result['planning_receipt']['calls'][-1]['raw_content']


def test_no_unreviewed_callable_entry(coordinated):
    d, processor, calls, _, _, _ = coordinated
    with pytest.raises(PermissionError): processor(d['receipt'], d['case'])
    with pytest.raises(PermissionError): CoordinatedPlanningProcessor(spec(), allow_external=False)
    assert not calls


@pytest.mark.parametrize('mode', ['grant', 'source', 'cancel', 'lease', 'configuration', 'provider', 'credential', 'specialist_credential', 'revision'])
def test_final_publication_rechecks_after_all_model_answers(coordinated, monkeypatch, mode):
    d, processor, calls, _, _, _ = coordinated
    slot = d['service'].inference_slot
    class FinalRace:
        def acquire(self, **kwargs): return slot.acquire(**kwargs)
        def release(self):
            slot.release()
            invalidate(d, processor, monkeypatch, mode)
    d['service'].inference_slot = FinalRace()
    assert process(d)['state'] != 'awaiting_review' and len(calls) == 7
    with sqlite3.connect(d['store'].path) as db:
        assert db.execute('SELECT result FROM event_work WHERE id=?', (d['work_id'],)).fetchone()[0] is None


@pytest.mark.parametrize('planner', [True, False])
def test_setup_refusal_retains_partial_status_without_leaking_errors(coordinated, planner):
    d, processor, calls, _, _, _ = coordinated
    def reject(**kwargs): raise HostedSetupRequired('Sensitive fictional setup detail')
    if planner: processor.planning_session_factory = reject
    else: processor.specialist_session_factory = reject
    assert process(d)['state'] == 'awaiting_review'
    result = retained(d)
    assert len(calls) == (0 if planner else 2) and result['final_synthesis'] is None
    assert 'Sensitive fictional setup detail' not in json.dumps(result)


@pytest.mark.parametrize('at_call', range(1, 8))
def test_provider_http_error_stops_without_repeating_or_retaining_error_body(coordinated, at_call):
    d, _, calls, _, transform, _ = coordinated
    transform[0] = lambda value, count, planning: httpx.Response(503, text='sensitive-error-body') if count == at_call else value
    assert process(d)['state'] == 'awaiting_review'
    result = retained(d)
    assert len(calls) == at_call and result['final_synthesis'] is None
    assert result['stop_reason'] != 'completed' and 'sensitive-error-body' not in json.dumps(result)


def test_unrequested_native_envelope_fields_are_not_persisted_or_sent_to_revision(coordinated):
    d, _, calls, _, transform, _ = coordinated
    def alter(value, count, planning):
        if not planning:
            value['unrequested_field'] = 'unrequested-provider-content'
            value['usage']['unrequested_field'] = 'unrequested-provider-content'
        return value
    transform[0] = alter
    assert process(d)['state'] == 'awaiting_review'
    result = retained(d)
    assert result['stop_reason'] == 'completed'
    assert 'unrequested-provider-content' not in json.dumps(result)
    assert 'unrequested-provider-content' not in json.dumps(calls[5:])
    assert all(r['response_fields_omitted'] and r['response']['answers'] for r in result['specialist_receipts'])


@pytest.mark.parametrize('valid', [True, False])
def test_oversized_raw_planning_receipt_stops_later_stages_and_preserves_hashes(coordinated, valid):
    d, _, calls, _, transform, _ = coordinated
    def alter(value, count, planning):
        value['choices'][0]['message']['content'] = (' ' * 210000
            + (json.dumps(frame()) if valid else 'not json'))
        return value
    transform[0] = alter
    assert process(d)['state'] == 'awaiting_review'
    result = retained(d)
    assert len(calls) == 1 and result['final_synthesis'] is None
    receipt = result['planning_receipt']['calls'][0]
    assert 'raw_content' not in receipt
    assert receipt['raw_content_omitted'] == 'coordinated_receipt_byte_limit'
    assert receipt['raw_content_sha256'] and receipt['response_body_sha256']
