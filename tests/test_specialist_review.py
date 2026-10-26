"""Synthetic specialist contracts and real host transactions; no network inference."""
from copy import deepcopy
from datetime import timedelta
import json
import sqlite3

import httpx
import pytest
from pydantic import ValidationError

from endstate.intelligence.coordination import Attempt, ReviewSpec, summarize
from eightball.event_inbox import EventConflict
from eightball.event_workers.specialists import SpecialistReviewProcessor
from eightball.store import digest
from eightball.v2.commands import Command
from eightball.v2.decision_models import DecisionSession
from tests.test_event_dispatch import dispatch, process, status

MODELS = ['jev-latest', 'clef-flash', 'gpt-6-luna-decisions']


def specification():
    return ReviewSpec(id='fictional-review', models=MODELS, max_seconds=30,
        max_reported_cost_nano_usd=10, questions=[dict(id='review',
        instructions='Treat missing evidence as a reason for further review, never as approval.',
        criteria={'accept': 'Supplied evidence supports continuing human review.',
                  'review': 'Important evidence or verification is missing.'})])


def answer(choice='review'):
    return dict(type='choice', choice=choice, confidence=0.7,
                probabilities={key: 0.8 if key == choice else 0.2 for key in ('accept', 'review')})


def attempt(model, choice='review', cost=1):
    return Attempt(model=model, status='answered', answers={'review': answer(choice)},
                   usage={'input_tokens': 10, 'output_tokens': 5, **({'cost_nano_usd': cost} if cost is not None else {})},
                   served_model=model, reported_cost_nano_usd=cost, request_started=True,
                   request_sha256='a'*64, response_sha256='b'*64)


def wire(model, choice='review'):
    value = answer(choice)
    answers = {'review': value}
    if model == 'gpt-6-luna-decisions':
        answers = [{**value, 'name': 'review', 'probabilities':
                    [{'value': key, 'probability': p} for key, p in value['probabilities'].items()]}]
    return dict(model=model, answers=answers, usage=dict(input_tokens=10, output_tokens=5, cost_nano_usd=1))


def test_retains_disagreement_without_voting_or_mutation():
    spec = specification()
    attempts = [attempt(model, choice) for model, choice in zip(MODELS, ['review', 'accept', 'review'])]
    before = [spec.model_dump(), [a.model_dump() for a in attempts]]
    result = summarize(spec, attempts)
    assert result['questions'] == [dict(id='review', choices=dict(zip(MODELS, ['review', 'accept', 'review'])),
                                       missing_models=[], disagreement=True)]
    assert result['answered_models'] == 3 and result['known_reported_cost_nano_usd'] == 3
    assert result['advisory_only'] and not result['facts_attested'] and not result['execution_authorized']
    assert 'recommendation' not in result and 'majority' not in result
    result['attempts'][0]['answers']['review']['probabilities']['accept'] = 0
    assert [spec.model_dump(), [a.model_dump() for a in attempts]] == before


def test_absence_is_not_agreement_or_free_usage():
    empty = summarize(specification(), [])
    assert empty['answered_models'] == 0 and empty['questions'][0]['missing_models'] == MODELS
    unknown = summarize(specification(), [attempt(MODELS[0], cost=None)])
    assert unknown['unknown_cost_attempts'] == [MODELS[0]]
    assert unknown['not_started_models'] == MODELS[1:]
    assert 'billing cap' in unknown['notice']


@pytest.mark.parametrize('patch', [dict(models=[]), dict(models=MODELS+[MODELS[0]]),
    dict(models=[MODELS[0], MODELS[0]]), dict(models=['not-configured']), dict(questions=[]),
    dict(max_seconds=0), dict(max_seconds=True), dict(max_seconds=181),
    dict(max_reported_cost_nano_usd=0), dict(max_reported_cost_nano_usd=True), dict(automatic_retry=True)])
def test_spec_rejects_unsafe_or_implicit_configuration(patch):
    with pytest.raises(ValidationError):
        ReviewSpec.model_validate(specification().model_dump() | patch)


@pytest.mark.parametrize('bad', ['order', 'duplicate', 'after_failure', 'after_unknown_cost',
    'after_budget', 'missing_answer', 'extra_answer', 'invalid_probability', 'no_receipt'])
def test_aggregation_rejects_invalid_attempts(bad):
    rows = [attempt(m) for m in MODELS]
    if bad == 'order': rows.reverse()
    if bad == 'duplicate': rows[1] = rows[0]
    if bad == 'after_failure': rows[0] = Attempt(model=MODELS[0], status='failed')
    if bad == 'after_unknown_cost': rows[0].reported_cost_nano_usd = None
    if bad == 'after_budget': rows[0].reported_cost_nano_usd = 10
    if bad == 'missing_answer': rows[0].answers = {}
    if bad == 'extra_answer': rows[0].answers['other'] = answer()
    if bad == 'invalid_probability': rows[0].answers['review']['probabilities']['accept'] = True
    if bad == 'no_receipt': rows[0].request_sha256 = None
    with pytest.raises(ValueError): summarize(specification(), rows)


@pytest.fixture
def specialists(dispatch, monkeypatch, request):
    d = dispatch
    monkeypatch.setenv('EXPERIENTIAL_API_KEY', 'fictional-specialist-transport-token')
    calls, after, transform = [], [None], [None]
    def serve(req):
        payload = json.loads(req.content)
        calls.append(payload)
        result = wire(payload['model'], 'accept' if payload['model'] == 'clef-flash' else 'review')
        if transform[0]: result = transform[0](result)
        if after[0]: after[0]()
        return httpx.Response(200, json=result)
    client = httpx.Client(transport=httpx.MockTransport(serve))
    request.addfinalizer(client.close)
    processor = SpecialistReviewProcessor(specification(), allow_external=True,
        session_factory=lambda **kwargs: DecisionSession(client=client, **kwargs))
    d['service'].cancel(case_id=d['case'].id, identity=d['operator'], work_id=d['work_id'])
    d['service'].processor = processor
    review = d['service'].review_source(case_id=d['case'].id, identity=d['operator'],
        sequence=d['receipt'].sequence, expected_revision=d['case'].revision,
        receipt_sha256=digest(d['receipt'].model_dump(mode='json')),
        rationale='Explicit fictional processing review of the configured specialist comparison.')
    d['source_review'] = review
    d['work_id'] = d['service'].enqueue(**(d['enqueue'] | {'request_id': 'specialists', 'review_id': review['id']}))
    return d, processor, calls, after, transform


def report(d):
    return json.loads(status(d)['work']['result'])


def test_native_specialists_use_only_reviewed_text_and_never_commit(specialists):
    d, processor, calls, _, _ = specialists
    before = d['store'].audit(d['case'].id)
    assert process(d)['state'] == 'awaiting_review'
    r = report(d)
    assert r['stop_reason'] == 'completed' and r['answered_models'] == 3
    assert r['questions'][0]['disagreement']
    assert all(a['usage'] == dict(input_tokens=10, output_tokens=5, cost_nano_usd=1) for a in r['attempts'])
    assert [c['model'] for c in calls] == MODELS
    assert all(c.get('state', c.get('input')) == d['event'].text for c in calls)
    assert r['spec_sha256'] == processor.configuration_sha256
    assert r['receipt_sha256'] == digest(d['receipt'].model_dump(mode='json'))
    assert d['store'].audit(d['case'].id) == before
    assert d['store'].get(d['case'].id).revision == 0
    assert status(d)['run']['output'] == status(d)['work']['result']
    with pytest.raises(EventConflict): process(d)
    assert len(calls) == 3


@pytest.mark.parametrize('change,expected', [
    ('cancel', 'cancelled'), ('revision', 'stale'), ('grant', 'permission_denied'),
    ('source_policy', 'permission_denied'), ('review', 'permission_denied'),
    ('configuration', 'permission_denied'), ('lease', 'interrupted')])
def test_each_call_checks_current_authority_and_discards_late_results(specialists, change, expected):
    d, processor, calls, after, _ = specialists
    def mutate():
        if change == 'cancel': d['service'].cancel(case_id=d['case'].id, identity=d['operator'], work_id=d['work_id'])
        if change == 'grant': d['registry'].revoke('worker')
        if change == 'source_policy': d['policy_state']['allowed'] = False
        if change == 'review':
            d['service'].revoke_source_review(case_id=d['case'].id, identity=d['operator'], review_id=d['source_review']['id'])
        if change == 'configuration': processor.spec.max_reported_cost_nano_usd += 1
        if change == 'lease': d['clock'][0] += timedelta(seconds=61)
        if change == 'revision':
            d['store'].change(d['case'].id, Command(event_id='concurrent', expected_revision=0,
                kind='replace_graph', payload={'graph': d['case'].graph.model_dump(mode='json')}))
    after[0] = mutate
    assert process(d)['state'] == expected
    assert len(calls) == 1
    with sqlite3.connect(d['store'].path) as db:
        assert db.execute('SELECT result FROM event_work WHERE id=?', (d['work_id'],)).fetchone()[0] is None
        assert db.execute('SELECT output FROM event_dispatch_runs WHERE work_id=?', (d['work_id'],)).fetchone()[0] is None
    assert d['service'].inference_slot.acquire(blocking=False)
    d['service'].inference_slot.release()


@pytest.mark.parametrize('mode,reason', [('missing_cost', 'unknown_reported_cost'),
    ('fractional_cost', 'unknown_reported_cost'), ('over_budget', 'reported_cost_budget'),
    ('malformed', 'setup_or_provider_failed')])
def test_unknown_cost_budget_and_failure_stop_without_retry(specialists, mode, reason):
    d, _, calls, _, transform = specialists
    def alter(value):
        value = deepcopy(value)
        if mode == 'missing_cost': value['usage'].pop('cost_nano_usd')
        if mode == 'fractional_cost': value['usage']['cost_nano_usd'] = 0.5
        if mode == 'over_budget': value['usage']['cost_nano_usd'] = 11
        if mode == 'malformed': value['answers'] = {}
        return value
    transform[0] = alter
    assert process(d)['state'] == 'awaiting_review'
    r = report(d)
    assert r['stop_reason'] == reason and len(calls) == 1
    assert r['not_started_models'] == MODELS[1:]
    assert not r['automatic_retries'] and not r['automatic_fallback']
    if mode != 'over_budget': assert r['unknown_cost_attempts'] == [MODELS[0]]


def test_changed_configuration_requires_new_review_before_any_request(specialists):
    d, processor, calls, _, _ = specialists
    processor.spec.models.reverse()
    with pytest.raises(EventConflict, match='configuration changed'): process(d)
    assert calls == [] and status(d)['work']['state'] == 'queued'


def test_time_stop_and_in_flight_non_recall(specialists):
    d, processor, calls, after, _ = specialists
    clock = [0]
    processor.timer = lambda: clock[0]
    after[0] = lambda: clock.__setitem__(0, 31)
    assert process(d)['state'] == 'awaiting_review'
    r = report(d)
    assert len(calls) == 1 and r['answered_models'] == 1 and r['stop_reason'] == 'time_budget'


def test_shared_slot_wait_rechecks_authority_without_a_provider_call(specialists):
    d, _, calls, _, _ = specialists
    class BusySlot:
        def acquire(self, **kwargs):
            d['registry'].revoke('worker')
            return False
        def release(self):
            pytest.fail('An unacquired slot must not be released')
    d['service'].inference_slot = BusySlot()
    assert process(d)['state'] == 'permission_denied' and calls == []


def test_explicit_permission_and_host_checkpoint_are_required(specialists):
    d, processor, calls, _, _ = specialists
    with pytest.raises(PermissionError): SpecialistReviewProcessor(specification(), allow_external=False)
    with pytest.raises(PermissionError): processor(d['receipt'], d['case'])
    assert calls == []


@pytest.mark.parametrize('mode', ['grant', 'configuration', 'cancel', 'revision'])
def test_final_transaction_closes_post_checkpoint_publication_race(specialists, mode):
    d, processor, calls, _, _ = specialists
    slot = d['service'].inference_slot
    class FinalRace:
        def acquire(self, **kwargs): return slot.acquire(**kwargs)
        def release(self):
            slot.release()
            if mode == 'grant': d['registry'].revoke('worker')
            if mode == 'configuration': processor.spec.max_seconds += 1
            if mode == 'cancel': d['service'].cancel(case_id=d['case'].id, identity=d['operator'], work_id=d['work_id'])
            if mode == 'revision':
                d['store'].change(d['case'].id, Command(event_id='publication-race', expected_revision=0,
                    kind='replace_graph', payload={'graph': d['case'].graph.model_dump(mode='json')}))
    d['service'].inference_slot = FinalRace()
    assert process(d)['state'] != 'awaiting_review'
    assert len(calls) == 3
    with sqlite3.connect(d['store'].path) as db:
        assert db.execute('SELECT result FROM event_work WHERE id=?', (d['work_id'],)).fetchone()[0] is None
        assert db.execute('SELECT output FROM event_dispatch_runs WHERE work_id=?', (d['work_id'],)).fetchone()[0] is None


def test_oversized_input_and_missing_configuration_make_no_requests(specialists):
    d, processor, calls, _, _ = specialists
    receipt = d['receipt'].model_copy(deep=True)
    receipt.event = receipt.event.model_copy(update={'text': 'x'*12001})
    with pytest.raises(ValueError): processor.run(receipt, d['case'], lambda: None)
    assert calls == []
    def absent(**kwargs): raise RuntimeError('fictional secret that must not be exposed')
    processor.session_factory = absent
    assert process(d)['state'] == 'awaiting_review'
    result = report(d)
    assert result['stop_reason'] == 'setup_or_provider_failed' and result['answered_models'] == 0
    assert not result['attempts'][0]['request_started']
    assert 'fictional secret' not in json.dumps(result) and calls == []


@pytest.mark.parametrize('usage', [{'input_tokens': True, 'output_tokens': 0},
    {'input_tokens': 1, 'output_tokens': 0, 'total_tokens': 5},
    {'input_tokens': 1, 'output_tokens': 0, 'cost_nano_usd': float('inf')}])
def test_invalid_usage_is_not_a_validated_answer(usage):
    row = attempt(MODELS[0])
    row.usage = usage
    with pytest.raises(ValueError): summarize(specification(), [row])


def test_timeout_retains_request_digest_without_error_text_or_retry(specialists):
    d, _, calls, _, transform = specialists
    def timeout(_): raise httpx.ReadTimeout('fictional-secret-response-body')
    transform[0] = timeout
    assert process(d)['state'] == 'awaiting_review'
    result = report(d)
    assert len(calls) == 1 and result['answered_models'] == 0
    assert result['attempts'][0]['request_started'] and result['attempts'][0]['request_sha256']
    assert result['unknown_cost_attempts'] == [MODELS[0]]
    assert 'fictional-secret-response-body' not in json.dumps(result)


def test_retained_comparison_is_read_only_and_source_bound(specialists):
    d, _, calls, _, _ = specialists
    process(d)
    before = d['store'].audit(d['case'].id)
    raw = status(d)['work']['result']
    view = d['reviews'].view(work_id=d['work_id'], case_id=d['case'].id, reader=d['worker'])
    comparison = view['specialist_review']
    assert comparison['available'] and comparison['questions'][0]['disagreement']
    assert comparison['known_reported_cost_usd'] == '0.000000003'
    assert not view['can_review'] and view['original_result'] == raw
    assert comparison['attempts'] == json.loads(raw)['attempts']
    assert d['store'].audit(d['case'].id) == before and len(calls) == 3


@pytest.mark.parametrize('field,value', [('case_id', 'other-case'), ('base_revision', False),
    ('receipt_sha256', '0'*64), ('input_sha256', '0'*64), ('spec_sha256', '0'*64),
    ('version', 'endstate.specialist-review.v99'), ('facts_attested', True),
    ('automatic_retries', True), ('answered_models', 0), ('stop_reason', 'approved')])
def test_invalid_retained_comparison_does_not_gain_a_typed_presentation(specialists, field, value):
    d, _, _, _, _ = specialists
    process(d)
    changed = report(d) | {field: value}
    raw = json.dumps(changed)
    with d['store'].connection() as db:
        db.execute('UPDATE event_work SET result=? WHERE id=?', (raw, d['work_id']))
        db.commit()
    view = d['reviews'].view(work_id=d['work_id'], case_id=d['case'].id, reader=d['operator'])
    assert view['specialist_review'] == {'available': False}
    assert view['original_result'] == raw and d['store'].get(d['case'].id).revision == 0


def test_stale_comparison_is_historical_and_source_revocation_withholds_it(specialists):
    d, _, _, _, _ = specialists
    process(d)
    d['store'].change(d['case'].id, Command(event_id='after-review', expected_revision=0,
        kind='metadata', payload={'budget': 3}))
    view = d['reviews'].view(work_id=d['work_id'], case_id=d['case'].id, reader=d['operator'])
    assert not view['reviewable'] and view['specialist_review']['base_revision'] == 0
    assert view['current_revision'] == 1
    d['service'].revoke_source_review(case_id=d['case'].id, identity=d['operator'],
                                     review_id=d['source_review']['id'])
    view = d['reviews'].view(work_id=d['work_id'], case_id=d['case'].id, reader=d['operator'])
    assert 'specialist_review' not in view and view['original_result'] is None
    assert view['source_receipt'] is None
