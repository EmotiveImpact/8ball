"""Exact-change and replay checks across fictional domains; no model calls."""
from copy import deepcopy
from datetime import timedelta

import pytest

from endstate.contracts import Approval, Resource, Decision
from endstate.rehearsal import changed_fields
from endstate.scenarios import Scenario, compare, project, verify
from eightball.store import digest
from eightball.v2.planner import to_snapshot
from eightball.v2.rehearsal import Prepare, prepare
from tests.test_endstate_kernel import domain_snapshot
from tests.test_rehearsal import NOW, draft, env, save


@pytest.mark.parametrize('domain', ['neutral', 'sales', 'support'])
def test_comparison_is_native_and_reusable_without_case_or_client(domain):
    snapshot = domain_snapshot(domain)
    original = snapshot.model_dump(mode='json')
    scenario = Scenario(expected_revision=snapshot.revision, budget=0, conditions={'ready':False})
    first, second = compare(snapshot, scenario, NOW), compare(snapshot, scenario, NOW)
    assert first == second and verify(snapshot, first)
    assert snapshot.model_dump(mode='json') == original
    assert first['result']['condition_states']['ready']['status'] == 'false'
    assert first['baseline']['condition_states']['ready']['status'] == 'unknown'
    assert first['manifest']['overlay']['budget'] == 0
    assert first['manifest']['limits'] == {'max_routes':64,'max_expansions':4096}
    assert not first['manifest']['randomness_used'] and not first['manifest']['persisted']
    if domain != 'neutral':
        assert any(r['unknown_waits'] for r in first['baseline']['routes'])


def test_exact_fields_values_and_original_history_survive_all_overlays():
    snapshot = domain_snapshot('neutral')
    snapshot.resources = [Resource(id='r1',name='Shared resource')]
    snapshot.decisions = [Decision(id='d1',question='Choose a declared option',owner='Fixture',options=[dict(id='x',title='First'),dict(id='y',title='Second')])]
    snapshot.approvals = [Approval(action_id='route_a',revision=snapshot.revision,expires_at=NOW+timedelta(hours=1),actor='Fixture')]
    scenario = Scenario(expected_revision=snapshot.revision, budget=0, deadline=NOW+timedelta(hours=2),
        conditions={'ready':False,'verified':True},unavailable_actions=['route_b'],
        resource_starts={'r1':NOW+timedelta(hours=3)},decisions={'d1':'y'})
    original = snapshot.model_dump(mode='json')
    clone = project(snapshot, scenario, NOW)
    result = compare(snapshot, scenario, NOW)
    changes = result['manifest']['changed_fields']
    assert changes == changed_fields(original, clone.model_dump(mode='json'))
    scalar = {tuple(c['path']):c for c in changes if c['path'][0] not in ('evidence','observations')}
    assert set(scalar) == {('budget',),('deadline',),('approvals',),('graph','actions','route_b','enabled'),('resources','r1','available_from'),('decisions','d1','selected')}
    assert scalar[('budget',)]['after'] == 0 and scalar[('approvals',)]['after'] == []
    assert len(changes) == 10
    assert snapshot.model_dump(mode='json') == original
    assert [a.id for a in clone.graph.actions] == [a.id for a in snapshot.graph.actions]
    assert clone.graph.actions[0] == snapshot.graph.actions[0]
    assert len(clone.observations) == len(snapshot.observations)+2


def test_equivalent_dictionary_order_and_branch_order_do_not_change_results(env):
    snapshot = domain_snapshot('neutral')
    a = compare(snapshot,Scenario(expected_revision=0,conditions={'ready':False,'verified':True}),NOW)
    b = compare(snapshot,Scenario(expected_revision=0,conditions={'verified':True,'ready':False}),NOW)
    assert a == b
    _, case, _ = env
    data = draft(); data['branches'].append({**data['branches'][0],'id':'b2','scenario':{'expected_revision':0,'budget':1}})
    first = prepare(case,Prepare(**data),NOW)
    data['branches'].reverse()
    second = prepare(case,Prepare(**data),NOW)
    assert {b['id']:b for b in first['branches']} == {b['id']:b for b in second['branches']}


@pytest.mark.parametrize('part', ['overlay','changed_fields','as_of','limits','result','snapshot_sha256','extra'])
def test_corrupt_replay_cannot_be_fixed_by_rehashing(part):
    snapshot = domain_snapshot('neutral')
    comparison = compare(snapshot,Scenario(expected_revision=0,budget=0),NOW)
    bad = deepcopy(comparison)
    if part == 'overlay': bad['manifest']['overlay']['budget'] = 1
    elif part == 'changed_fields': bad['manifest'][part] = []
    elif part == 'as_of': bad['manifest'][part] = 'not a clock'
    elif part == 'limits': bad['manifest'][part]['max_routes'] = 999
    elif part == 'result': bad['result']['candidate_routes'] += 1
    elif part == 'snapshot_sha256': bad['manifest'][part] = '0'*64
    else: bad['undeclared_authority'] = True
    bad['manifest_sha256'] = digest(bad['manifest'])
    with pytest.raises(ValueError,match='replay'): verify(snapshot,bad)


def test_changed_input_or_naive_clock_and_missing_reference_reject():
    snapshot = domain_snapshot('neutral')
    comparison = compare(snapshot,Scenario(expected_revision=0,budget=0),NOW)
    snapshot.budget += 1
    with pytest.raises(ValueError,match='replay'): verify(snapshot,comparison)
    with pytest.raises(ValueError,match='timezone'): compare(snapshot,Scenario(expected_revision=0,budget=0),NOW.replace(tzinfo=None))
    with pytest.raises(ValueError,match='missing'): project(snapshot,Scenario(expected_revision=0,conditions={'missing':False}),NOW)


@pytest.mark.parametrize('mutation', ['spill','missing_change','extra_observation'])
def test_projection_verifier_detects_extra_or_missing_changes(monkeypatch, mutation):
    import endstate.scenarios as scenarios
    snapshot = domain_snapshot('neutral')
    original = project
    def broken(state, overlay, clock):
        clone = original(state,overlay,clock)
        if mutation == 'spill': clone.owner = 'Unexpected owner'
        elif mutation == 'missing_change': clone.budget = state.budget
        else: clone.observations = []
        return clone
    monkeypatch.setattr(scenarios,'project',broken)
    with pytest.raises(ValueError): compare(snapshot,Scenario(expected_revision=0,budget=0,conditions={'ready':False}),NOW)


def test_search_cutoff_is_not_impossibility(monkeypatch):
    from endstate import planner
    monkeypatch.setattr(planner,'MAX_EXPANSIONS',0)
    result = compare(domain_snapshot('neutral'),Scenario(expected_revision=0,budget=0),NOW)
    assert result['baseline']['stop_reason'] == 'search_cutoff'
    assert result['baseline']['search_truncated']


def test_comparison_preserves_unknown_false_zero_and_absent_values():
    assert changed_fields({'value':None},{})[0]['after_present'] is False
    assert changed_fields({'value':False},{'value':0})[0]['after'] == 0
    snapshot = domain_snapshot('neutral')
    same = compare(snapshot,Scenario(expected_revision=0,budget=snapshot.budget),NOW)
    assert same['manifest']['changed_fields'] == []
    assert same['result']['condition_states']['ready']['status'] == 'unknown'


def test_saved_replay_rejects_rehashed_manifest_corruption(env):
    import json
    from eightball.store import canonical
    store, case, service = env
    result, request = save(service,case)
    record = {k:v for k,v in result['record'].items() if k != 'hash'}
    brief = record['brief']; branch = brief['branches'][0]
    branch['manifest']['changed_fields'] = []
    branch['manifest_sha256'] = digest(branch['manifest'])
    brief['brief_sha256'] = digest({k:v for k,v in brief.items() if k != 'brief_sha256'})
    request.brief_sha256 = brief['brief_sha256']; record['request_hash'] = digest(request.model_dump(mode='json'))
    with store.connection() as db:
        db.execute('UPDATE v2_rehearsals SET record=?,hash=? WHERE case_id=?',(canonical(record),digest(record),case.id));db.commit()
    with pytest.raises(ValueError,match='history'): service.view(case.id)
    assert not store.audit(case.id)['valid']
