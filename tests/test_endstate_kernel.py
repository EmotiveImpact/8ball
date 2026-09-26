"""Extraction and cross-domain evidence. Fictional inputs, no provider/model calls."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pathlib import Path
import ast
import copy
import lzma
import hashlib
import json
import os
import shutil
import subprocess
import sys

import pytest
from pydantic import ValidationError
from endstate.api import PlanRequest, calculate
from endstate.contracts import (
    PlanningSnapshot, Graph, Condition, Action, Objective, Constraint, Effect,
    atom, all_of, any_of,
)
from endstate.primitives import Evidence, Observation
from endstate import planner as kernel

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads(lzma.decompress((ROOT / 'tests/fixtures/endstate/pre_extraction.json.xz').read_bytes()))
NOW = datetime.fromisoformat(FIXTURE['now'])


def normal(value, key=''):
    """Only set-derived lists are unordered; route order and schedules are not."""
    if isinstance(value, dict):
        return {k: normal(v, k) for k, v in value.items()}
    if isinstance(value, list):
        vals = [normal(x) for x in value]
        if key in ('ready', 'approvals', 'changed_routes'):
            return sorted(vals, key=lambda x: json.dumps(x, sort_keys=True))
        return vals
    return value


def digest(value):
    return hashlib.sha256(json.dumps(normal(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


@pytest.mark.parametrize('fixture', FIXTURE['cases'], ids=lambda x: x['name'])
def test_pre_extraction_plans_briefings_and_changes_are_unchanged(fixture):
    from eightball.v2.contracts import Case
    from eightball.v2.commands import Command, apply
    from eightball.v2.planner import plan, briefing, changes
    case = Case.model_validate(fixture['case'])
    assert case.model_dump(mode='json') == fixture['case']
    before = plan(case, NOW)
    assert digest(before) == fixture['plan_sha256']
    assert digest(briefing(case, before)) == fixture['briefing_sha256']
    after = apply(case, Command(event_id='fixture_budget', expected_revision=case.revision,
                               kind='metadata', payload={'budget': 0}), now=NOW)
    after_plan = plan(after, NOW)
    assert digest(after_plan) == fixture['budget_zero_plan_sha256']
    assert digest(changes(case, after, before, after_plan)) == fixture['budget_zero_changes_sha256']


@pytest.mark.parametrize('version', ['v1', 'v2'])
def test_original_wire_schemas_are_unchanged(version):
    from eightball.models import Situation
    from eightball.v2.contracts import Case
    model = Situation if version == 'v1' else Case
    assert digest(model.model_json_schema()) == FIXTURE['schemas'][version]


def test_original_legacy_plan_is_unchanged():
    from eightball.models import Situation
    from eightball.engine import plan
    assert digest(plan(Situation.model_validate(FIXTURE['legacy_case']), NOW)) == FIXTURE['legacy_plan_sha256']


def test_pre_extraction_database_rows_and_audit_hashes_still_verify(tmp_path):
    from eightball.store import Store as LegacyStore
    from eightball.v2.store import Store
    store = Store(str(tmp_path / 'old-rows.sqlite3'))
    with store.connection() as db:
        for table in ('situations', 'events', 'v2_cases', 'v2_events', 'v2_proposals', 'v2_lineage'):
            rows = FIXTURE['database_rows'][table]
            for row in rows:
                # Table and columns come only from the fixed, reviewed test fixture.
                columns = ','.join(row)
                db.execute(f'INSERT INTO {table} ({columns}) VALUES ({",".join("?" for _ in row)})', tuple(row.values()))
        db.commit()
    original = copy.deepcopy(FIXTURE['database_rows'])
    legacy_id = original['situations'][0]['id']
    current_id = original['v2_cases'][0]['id']
    assert digest(store.audit(current_id)) == FIXTURE['stored_v2_audit_sha256']
    assert digest(LegacyStore(store.path).audit(legacy_id)) == FIXTURE['stored_v1_audit_sha256']
    assert Store(store.path).audit(current_id)['replay_matches_snapshot'] is True
    with store.connection() as db:
        assert {table: [dict(r) for r in db.execute('SELECT * FROM ' + table)] for table in original} == original


def test_existing_imports_reference_one_shared_implementation():
    from eightball import models, engine
    from eightball.v2 import contracts, planner
    from endstate import contracts as core_contracts, primitives, state
    assert models.Evidence is primitives.Evidence
    assert models.Observation is primitives.Observation
    assert contracts.Action is core_contracts.Action
    assert contracts.Graph is core_contracts.Graph
    assert contracts.Expr is core_contracts.Expr
    assert engine.condition_states is state.condition_states
    assert planner.readiness is kernel.readiness
    assert planner.evaluate is kernel.evaluate


def test_8ball_adapter_passes_only_a_detached_engine_snapshot(monkeypatch):
    from eightball.v2.contracts import Case
    from eightball.v2 import planner
    case = Case.model_validate(FIXTURE['cases'][-2]['case'])
    before = case.model_dump(mode='json')
    invoked = []
    original = kernel.plan
    def observed(snapshot, *args):
        invoked.append(snapshot)
        assert type(snapshot) is PlanningSnapshot
        assert not {'title', 'client', 'summary', 'confidentiality', 'legacy_id'} & set(type(snapshot).model_fields)
        assert snapshot.graph is not case.graph
        return original(snapshot, *args)
    monkeypatch.setattr(kernel, 'plan', observed)
    planner.plan(case, NOW)
    assert len(invoked) == 1
    invoked[0].graph.conditions[0].title = 'Altered detached copy'
    assert case.model_dump(mode='json') == before


def domain_snapshot(domain):
    """Different work and authority policies; the same kernel performs every plan."""
    data = {
        'neutral': ('Resource ready', 'Check primary resource', 'Check backup resource', 'Operator'),
        'sales': ('Meeting invitation accepted', 'Request a direct meeting', 'Request an authorised introduction', 'Account owner'),
        'support': ('Remedy delivered', 'Deliver approved replacement', 'Complete approved refund', 'Support lead'),
    }
    target, route_a, route_b, owner = data[domain]
    conditions = [Condition(id='ready', title=target, confirmation='Reviewed direct confirmation'),
                  Condition(id='verified', title='Required outcome confirmed', confirmation='Reviewed confirmation of the full stated outcome')]
    actions = [
        Action(id='route_a', title=route_a, owner=owner, purpose=route_a,
               effects=[Effect(condition_id='ready')], minutes=20, cost=100,
               approval_required=True, contingent=domain != 'neutral', wait_minutes=None if domain != 'neutral' else 0),
        Action(id='route_b', title=route_b, owner=owner, purpose=route_b,
               effects=[Effect(condition_id='ready')], minutes=40, cost=50,
               approval_required=True, contingent=domain != 'neutral', wait_minutes=None if domain != 'neutral' else 0),
        Action(id='verify', title='Check evidence of the outcome', owner=owner,
               purpose='Verify the actual result separately from completed work', requires=atom('ready'),
               effects=[Effect(condition_id='verified')], minutes=10),
    ]
    restrictions = []
    if domain == 'sales':
        conditions.append(Condition(id='opted_out', title='Recipient has opted out', confirmation='Recorded opt-out'))
        for action in actions[:2]:
            action.guard = atom('opted_out', False)
    if domain == 'support':
        conditions.append(Condition(id='authority', title='Remedy authority established', confirmation='Recorded approval within limits'))
        restrictions.append(Constraint(id='remedy_policy', title='Only offer an authorised remedy',
                                       predicate=atom('authority'), action_ids=['route_a', 'route_b'], confirmed=True))
    return PlanningSnapshot(id=domain, owner=owner, deadline=NOW+timedelta(days=1), budget=1000,
                            graph=Graph(conditions=conditions, actions=actions,
                                        objectives=[Objective(id='outcome', title='Agreed outcome', success=atom('verified'))]),
                            constraints=restrictions)


def observed(snapshot, cid, value):
    data = snapshot.model_dump(mode='json')
    eid = f'source_{cid}_{len(snapshot.evidence)}'
    data['evidence'].append(Evidence(id=eid, title='Fictional source', source='Domain fixture',
                                     text='Fictional explicit confirmation.', status='reviewed', added_at=NOW).model_dump(mode='json'))
    data['observations'].append(Observation(id=f'obs_{cid}_{len(snapshot.observations)}', condition_id=cid,
        evidence_id=eid, value=value, rationale='Fictional reviewed observation', added_at=NOW,
        supersedes=[o.id for o in snapshot.observations if o.condition_id==cid]).model_dump(mode='json'))
    return PlanningSnapshot.model_validate(data)


@pytest.mark.parametrize('domain', ['neutral', 'sales', 'support'])
def test_three_domains_share_the_same_engine_and_keep_human_approval(domain):
    snapshot = domain_snapshot(domain)
    if domain == 'sales':
        snapshot = observed(snapshot, 'opted_out', False)
    if domain == 'support':
        snapshot = observed(snapshot, 'authority', True)
    before = snapshot.model_dump(mode='json')
    response = calculate(PlanRequest(snapshot=snapshot, as_of=NOW))
    assert response.contract_version == 'endstate.plan.v1'
    assert response.snapshot_id == domain
    assert len(response.plan['routes']) == 2
    assert all(not r['hard_breaches'] and not r['evidence_gaps'] for r in response.plan['routes'])
    assert response.plan['action_states']['route_a']['status'] == 'approval_required'
    assert response.plan['action_states']['route_b']['status'] == 'approval_required'
    assert response.plan['action_states']['verify']['status'] == 'blocked'
    assert snapshot.model_dump(mode='json') == before
    assert response.plan['outcome_evidenced'] is False
    # Mutating a returned hypothetical schedule cannot alter the caller's state.
    response.plan['routes'][0]['schedule'].clear()
    assert snapshot.model_dump(mode='json') == before


@pytest.mark.parametrize('opt_out', [None, True, False])
def test_sales_opt_out_policy_requires_explicit_evidence(opt_out):
    snapshot = domain_snapshot('sales')
    if opt_out is not None:
        snapshot = observed(snapshot, 'opted_out', opt_out)
    p = calculate(PlanRequest(snapshot=snapshot, as_of=NOW)).plan
    assert p['action_states']['route_a']['status'] == ('approval_required' if opt_out is False else 'blocked')
    assert bool(p['routes'][0]['evidence_gaps']) is (opt_out is not False)


@pytest.mark.parametrize('authority', [None, False, True])
def test_support_remedies_require_explicit_authority(authority):
    snapshot = domain_snapshot('support')
    if authority is not None:
        snapshot = observed(snapshot, 'authority', authority)
    p = calculate(PlanRequest(snapshot=snapshot, as_of=NOW)).plan
    assert p['action_states']['route_a']['status'] == ('approval_required' if authority is True else 'blocked')
    assert bool(p['routes'][0]['hard_breaches']) is (authority is not True)


def test_real_update_recalculates_without_claiming_observed_success():
    before = domain_snapshot('sales')
    after = observed(before, 'opted_out', False)
    bp, ap = kernel.plan(before, NOW), kernel.plan(after, NOW)
    d = kernel.explain_changes(before, after, bp, ap)
    assert any(c['id']=='opted_out' and c['after']=='false' for c in d['conditions'])
    assert bp['routes'][0]['evidence_gaps'] and not ap['routes'][0]['evidence_gaps']
    assert not ap['outcome_evidenced']


@pytest.mark.parametrize('modify', [
    lambda d: d.update(contract_version='endstate.plan.v999'),
    lambda d: d.update(as_of='2026-09-23T12:00:00'),
    lambda d: d.update(sort_by='highest_success_probability'),
    lambda d: d['snapshot'].update(budget=-1),
    lambda d: d['snapshot']['graph']['actions'][0]['effects'][0].update(condition_id='absent'),
    lambda d: d['snapshot'].update(execute_now=True),
])
def test_invalid_public_requests_fail_closed(modify):
    payload = PlanRequest(snapshot=domain_snapshot('neutral'), as_of=NOW).model_dump(mode='json')
    modify(payload)
    with pytest.raises(ValidationError):
        calculate(payload)


@pytest.mark.parametrize('as_mapping', [False, True])
def test_nested_mutation_is_revalidated_at_the_public_boundary(as_mapping):
    snapshot = domain_snapshot('neutral')
    request = PlanRequest(snapshot=snapshot, as_of=NOW)
    snapshot.graph.actions[0].effects.append(Effect(condition_id='missing'))
    payload = {'snapshot': snapshot, 'as_of': NOW} if as_mapping else request
    with pytest.raises(ValidationError):
        calculate(payload)


def test_core_has_no_application_or_runtime_service_imports():
    allowed = {'__future__', 'dataclasses', 'datetime', 'hashlib', 'json', 'typing', 'uuid', 'pydantic', 're', 'zoneinfo'}
    for path in (ROOT/'endstate').glob('*.py'):
        for n in ast.walk(ast.parse(path.read_text())):
            if isinstance(n, ast.Import):
                assert all(a.name.split('.')[0] in allowed for a in n.names), path.name
            elif isinstance(n, ast.ImportFrom) and n.level == 0:
                assert n.module.split('.')[0] in allowed, path.name


def test_kernel_runs_with_only_its_own_source_and_pydantic(tmp_path):
    shutil.copytree(ROOT/'endstate', tmp_path/'endstate', ignore=shutil.ignore_patterns('__pycache__'))
    payload = PlanRequest(snapshot=observed(domain_snapshot('sales'), 'opted_out', False), as_of=NOW).model_dump(mode='json')
    (tmp_path/'request.json').write_text(json.dumps(payload))
    # Isolated Python ignores working-tree and environment path injections.
    code = '''
import sys, json, importlib.abc
sys.path.insert(0, sys.argv[1])
class RejectApplication(importlib.abc.MetaPathFinder):
    def find_spec(self, name, *args, **kwargs):
        if name.split('.')[0] in ('eightball', 'httpx', 'fastapi', 'sqlite3', 'ollama'):
            raise AssertionError('Core attempted a forbidden import: ' + name)
sys.meta_path.insert(0, RejectApplication())
from endstate.api import calculate
from pathlib import Path
result = calculate(json.loads(Path(sys.argv[1], 'request.json').read_text()))
assert len(result.plan['routes']) == 2
assert not any(n.startswith('eightball') for n in sys.modules)
print('Isolated ENDSTATE: two routes; no 8BALL, storage or model runtime imported.')
'''
    r = subprocess.run([sys.executable, '-I', '-c', code, str(tmp_path)], cwd=tmp_path,
                       text=True, capture_output=True, timeout=15)
    assert r.returncode == 0, r.stderr
    assert 'two routes' in r.stdout
