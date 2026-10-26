"""Fictional, provider-free challenge contracts and durable no-authority boundaries."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from endstate.rehearsal import Draft, coverage
from eightball.api import make_app
from eightball.store import Store as LegacyStore, Conflict, canonical, digest
from eightball.v2.commands import Command
from eightball.v2.playbooks import demo_case
from eightball.v2.rehearsal import Prepare, Save, Rehearsals, export_rows, prepare, read_rows
from eightball.v2.store import Store

NOW = datetime(2026, 10, 26, 9, 0, tzinfo=timezone.utc)
TOKEN = 'fictional-challenge-test-token-only-1234567890'


def draft(revision=0):
    return dict(run_id='fictional', expected_revision=revision,
        perspectives=[dict(id='supplier', label='Fictional supplier', kind='archetype',
            objective='Maintain a lawful supply arrangement.', information_boundary='Only the declared brief; no private knowledge.',
            permitted_references=['case:summary'])],
        contributions=[dict(id='a1', role_id='supplier', kind='assumption', text='Supply may remain available.',
            references=['case:summary'], verification_needed='Obtain current source-backed confirmation.'),
            dict(id='o1', role_id='supplier', kind='objection', text='The supplier might refuse; this is not an actual refusal.',
            references=['case:summary'], counters=['a1'], verification_needed='Check actual consent.'),
            dict(id='q1', role_id='supplier', kind='question', text='What information would change the choice?',
            references=['case:summary'], verification_needed='Ask an authorised person; no automatic send.')],
        branches=[dict(id='b1', title='No remaining budget', rationale='Compare this explicit adverse assumption.',
            assumption_ids=['a1'], scenario=dict(expected_revision=revision, budget=0))])


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr('eightball.v2.rehearsal.utcnow', lambda: NOW)
    store = Store(str(tmp_path/'challenge.db'))
    case = store.create(demo_case(NOW), fixture=True)
    return store, case, Rehearsals(store)


def save(service, case, data=None, event_id='save-1'):
    preview = service.prepare(case.id, Prepare(**(data or draft(case.revision))))
    brief = preview['brief']
    request = Save(event_id=event_id, expected_sequence=preview['sequence'], as_of=brief['as_of'],
                   brief_sha256=brief['brief_sha256'], draft=brief['draft'])
    return service.save(case.id, request), request


def test_missing_coverage_is_not_agreement_and_explicit_not_applicable_is_separate():
    empty = Draft(run_id='empty')
    assert coverage(empty)['state'] == 'not_supplied'
    empty.perspectives_not_applicable_reason = 'This comparison has no stakeholder perspective.'
    assert coverage(empty)['state'] == 'not_applicable'
    data = draft(); data['perspectives'].append({**data['perspectives'][0], 'id':'silent'})
    result = coverage(Prepare(**data))
    assert result['missing_contributions'] == ['silent']
    assert result['unresolved_objections'] == ['o1']
    assert result['unanswered_questions'] == ['q1']


@pytest.mark.parametrize('mutation', [
    lambda d: d['perspectives'].append(d['perspectives'][0]),
    lambda d: d['contributions'].append(d['contributions'][0]),
    lambda d: d['branches'].append(d['branches'][0]),
    lambda d: d['perspectives'][0].update(kind='real_person'),
    lambda d: d['contributions'][0].update(role_id='missing'),
    lambda d: d['contributions'][0].update(references=['case:desired_outcome']),
    lambda d: d['contributions'][0].update(counters=['a1']),
    lambda d: d['contributions'][0].update(counters=['missing']),
    lambda d: d['contributions'][0].update(text='   '),
    lambda d: d['branches'][0].update(assumption_ids=['o1']),
    lambda d: d['branches'][0]['scenario'].update(budget=None),
    lambda d: d['branches'][0]['scenario'].update(conditions={'paid':'false'}),
    lambda d: d.update(perspectives_not_applicable_reason='Not applicable'),
    lambda d: d.update(dispositions=[dict(contribution_id='missing',status='open',rationale='Unknown')]),
    lambda d: d.update(dispositions=[dict(contribution_id='o1',status='verified',rationale='Invalid authority')]),
    lambda d: d.update(operator_decision=dict(outcome='approve',rationale='No authority')),
    lambda d: d.update(operator_decision=dict(outcome='continue_review',rationale='Missing acknowledgement')),
    lambda d: d.update(operator_decision=dict(outcome='reconsider',rationale='R',contribution_ids=['o1','o1'])),
    lambda d: d.update(operator_decision=dict(outcome='reconsider',rationale='R',contribution_ids=['missing'])),
    lambda d: d.update(perspectives=[{**d['perspectives'][0],'id':f'p{i}'} for i in range(5)]),
    lambda d: d.update(contributions=[{**d['contributions'][0],'id':f'c{i}'} for i in range(13)]),
    lambda d: d.update(branches=[{**d['branches'][0],'id':f'b{i}'} for i in range(4)]),
])
def test_invalid_contracts_fail_closed(mutation):
    data = draft(); mutation(data)
    with pytest.raises(ValidationError): Prepare(**data)


def test_prepare_and_record_preserve_case_and_original_objection(env):
    store, case, service = env
    before = store.audit(case.id)
    data = draft()
    data['dispositions'] = [dict(contribution_id='o1',status='retained_concern',rationale='No supporting response yet.')]
    data['operator_decision'] = dict(outcome='continue_review',rationale='Consider other routes without acting.',contribution_ids=['o1'])
    result, request = save(service, case, data)
    after = store.audit(case.id)
    assert before['case'] == after['case'] and before['events'] == after['events']
    assert after['valid'] and len(after['assumption_challenges']['records']) == 1
    brief = result['record']['brief']
    assert brief['coverage']['unresolved_objections'] == ['o1']
    assert brief['draft']['contributions'][1]['text'] == data['contributions'][1]['text']
    assert brief['provider'] is None and brief['inference_calls'] == 0 and brief['cost_not_incurred']
    assert brief['hypothetical'] and not brief['facts_attested'] and not brief['execution_authorised']
    assert not result['live_case_changed'] and result['artifact_persisted']
    assert service.save(case.id, request)['duplicate']
    assert len(service.view(case.id)['records']) == 1
    request.draft.run_id = 'different'
    with pytest.raises(Conflict): service.save(case.id, request)


def test_addressed_review_is_not_attestation_and_original_remains(env):
    store, case, service = env
    data = draft(); data['dispositions'] = [dict(contribution_id='o1',status='addressed_in_review',rationale='Discussed only, not independently verified.')]
    data['operator_decision'] = dict(outcome='seek_information',rationale='Obtain actual evidence.',contribution_ids=['q1'])
    result, _ = save(service, case, data)
    brief = result['record']['brief']
    assert brief['coverage']['all_objections'] == ['o1']
    assert not brief['coverage']['unresolved_objections']
    assert brief['coverage']['operator_addressed'] == ['o1']
    assert store.get(case.id) == case


@pytest.mark.parametrize('change', ['revision','branch_revision','reference','completed','predecessor'])
def test_invalid_snapshot_or_reference_denies(env, change):
    _, case, _ = env
    data = draft()
    if change == 'revision': data['expected_revision'] = 1
    elif change == 'branch_revision': data['branches'][0]['scenario']['expected_revision'] = 1
    elif change == 'reference': data['perspectives'][0]['permitted_references'].append('source:missing')
    elif change == 'completed':
        case.completed.append('direct'); data['branches'][0]['scenario']['unavailable_actions'] = ['direct']
    else: data['predecessor_sha256'] = 'a'*64
    with pytest.raises((ValueError, Conflict)): prepare(case, Prepare(**data), NOW)


@pytest.mark.parametrize('change', ['digest','sequence','expired','future'])
def test_invalid_save_denies_without_record(env, change, monkeypatch):
    store, case, service = env
    p = service.prepare(case.id, Prepare(**draft()))
    request = Save(event_id='e', expected_sequence=0, as_of=p['brief']['as_of'], brief_sha256=p['brief']['brief_sha256'], draft=p['brief']['draft'])
    if change == 'digest': request.brief_sha256 = '0'*64
    elif change == 'sequence': request.expected_sequence = 1
    else: monkeypatch.setattr('eightball.v2.rehearsal.utcnow',lambda: NOW+timedelta(minutes=16) if change == 'expired' else NOW-timedelta(seconds=1))
    with pytest.raises(Conflict): service.save(case.id, request)
    assert service.view(case.id)['records'] == [] and store.get(case.id) == case


def test_recheck_appends_immutable_predecessor_and_detects_changed_basis(env):
    store, case, service = env
    first, _ = save(service, case)
    changed, _ = store.change(case.id, Command(event_id='change',expected_revision=0,kind='metadata',payload={'summary':'Changed fictional brief.'}))
    data = draft(changed.revision); data['predecessor_sha256'] = first['record']['brief']['brief_sha256']
    data['dispositions'] = [dict(contribution_id='o1',status='deferred',rationale='Original objection still matters.')]
    second, _ = save(service, changed, data, 'save-2')
    assert 'case:summary' in second['record']['brief']['reconsideration']['changed_references']
    history = service.view(case.id)
    assert history['records'][0]['case_changed'] and not history['records'][1]['case_changed']
    assert history['records'][0]['brief'] == first['record']['brief']
    data['contributions'][1]['text'] = 'Erase the original objection.'
    with pytest.raises(ValueError, match='original'): service.prepare(case.id, Prepare(**data))
    other = store.create(demo_case(NOW), fixture=True)
    data['expected_revision'] = 0
    with pytest.raises(Conflict): service.prepare(other.id, Prepare(**data))


@pytest.mark.parametrize('table,change', [('v2_rehearsals','record'),('v2_rehearsals','sequence'),('v2_rehearsals','hash'),('v2_events','record'),('v2_events','hash')])
def test_corrupt_histories_never_export_or_append(env, table, change):
    store, case, service = env
    save(service, case)
    with store.connection() as db:
        db.execute(f'UPDATE {table} SET {change}=? WHERE case_id=?', (99 if change == 'sequence' else 'corrupt', case.id))
        db.commit()
    with pytest.raises(ValueError, match='history'): service.view(case.id)
    with pytest.raises(ValueError, match='history'): service.prepare(case.id, Prepare(**draft()))


def test_missing_predecessor_and_oversized_brief_fail(env, monkeypatch):
    store, case, service = env
    first, _ = save(service, case)
    data = draft(); data['predecessor_sha256'] = first['record']['brief']['brief_sha256']
    save(service, case, data, 'second')
    with store.connection() as db:
        rows = read_rows(db, case.id)
    assert not export_rows(rows[1:], case.id)['valid']
    monkeypatch.setattr('eightball.v2.rehearsal.MAX_BYTES', 10)
    with pytest.raises(ValueError, match='artifact limit'): prepare(case, Prepare(**draft()), NOW)


def test_authenticated_local_api_and_legacy_export_compatibility(env):
    store, case, _ = env
    before = store.audit(case.id)
    assert 'assumption_challenges' not in before
    with TestClient(make_app(LegacyStore(store.path), TOKEN)) as client:
        path = f'/api/v2/cases/{case.id}/plan-reviews/rehearsals'
        assert client.get(path).status_code == 401
        client.headers['Authorization'] = 'Bearer '+TOKEN
        response = client.post(path+'/prepare', json=draft())
        assert response.status_code == 200, response.text
        p = response.json()
        response = client.post(path+'/record', json=dict(event_id='api-save',expected_sequence=0,
            as_of=p['brief']['as_of'],brief_sha256=p['brief']['brief_sha256'],draft=p['brief']['draft']))
        assert response.status_code == 200, response.text
        assert client.get(path).json()['sequence'] == 1
        assert client.post(path+'/prepare',json={**draft(),'expected_revision':1}).status_code == 409
    assert store.get(case.id) == case
