"""Fictional source-only consumers, not model, product or release acceptance."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
from pydantic import ValidationError

from endstate.api import PlanRequest, calculate
from endstate.contracts import PlanningSnapshot
from endstate.domain_packs import (
    BoundSnapshot, ConsumerRequest, DomainPack, PackConsumer, PackError, Principal,
    Scope, SnapshotSeed, compare_packs, instantiate, load_pack_json, pack_reference,
    require_reference,
)
from endstate.primitives import Evidence, Observation
from endstate.state import condition_states

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/domain_packs'
NOW = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)


def data(domain='neutral'):
    return json.loads((FIXTURES / (domain + '.json')).read_text())


def pack(domain='neutral'):
    return load_pack_json((FIXTURES / (domain + '.json')).read_bytes())


def seed():
    return SnapshotSeed(snapshot_id='fictional_case', owner='Fictional operator',
                        deadline=NOW + timedelta(days=1), budget=10000)


def observe(snapshot, cid, value):
    result = snapshot.model_copy(deep=True)
    eid = f'source_{len(result.evidence)}'
    result.evidence.append(Evidence(id=eid, title='Fictional confirmation', source='Synthetic fixture',
                                   text='Fictional reviewed record.', status='reviewed', added_at=NOW))
    result.observations.append(Observation(id=f'obs_{len(result.observations)}', condition_id=cid,
        evidence_id=eid, value=value, rationale='Explicit fictional observation', added_at=NOW,
        supersedes=[o.id for o in result.observations if o.condition_id == cid]))
    result.revision += 1
    return PlanningSnapshot.model_validate(result.model_dump(mode='python'))


def harness(domain='neutral'):
    selected = pack(domain)
    scope = Scope(tenant_id='tenant_a', matter_id='matter_a', snapshot_id='fictional_case')
    state = {'snapshot': instantiate(selected, seed()), 'allowed': True, 'checks': 0, 'reads': 0}

    def authorise(principal, requested, operation):
        state['checks'] += 1
        return state['allowed'] and principal.subject == 'member' and requested == scope and operation == 'plan_read'

    def read(requested):
        state['reads'] += 1
        assert requested == scope
        return BoundSnapshot(scope=scope, snapshot=state['snapshot'])

    request = ConsumerRequest(scope=scope.model_copy(deep=True), pack=pack_reference(selected), expected_revision=0, as_of=NOW)
    service = PackConsumer(selected, authorise=authorise, read_snapshot=read)
    return selected, state, request, service, authorise, read


@pytest.mark.parametrize('domain', ['fixer', 'neutral', 'sales', 'support'])
def test_four_packs_use_native_kernel_without_changing_source_inputs(domain):
    selected, state, request, service, _, _ = harness(domain)
    snapshot = state['snapshot']
    before = snapshot.model_dump(mode='json')
    response = service.calculate(Principal(subject='member'), request)
    assert response.result == calculate(PlanRequest(snapshot=snapshot, as_of=NOW))
    assert response.pack == pack_reference(selected)
    assert response.result.plan['routes']
    assert snapshot.model_dump(mode='json') == before
    assert not snapshot.evidence and not snapshot.observations and not snapshot.approvals
    assert not snapshot.completed and not snapshot.decisions
    assert all(s['status'] == 'unknown' for s in condition_states(snapshot).values())
    assert state['checks'] == 3 and state['reads'] == 2
    response.result.plan['routes'].clear()
    assert service.calculate(Principal(subject='member'), request).result.plan['routes']


def test_fixer_is_product_owned_and_existing_supplier_playbook_graph_stays_exact():
    from eightball.v2.playbooks import get_playbook
    product = get_playbook('supplier')
    selected = pack('fixer')
    assert selected.owner == '8BALL product team'
    assert selected.catalogue.graph == product['graph']
    assert selected.catalogue.questions == product['questions']


def test_sales_needs_explicit_non_opt_out_and_opt_out_blocks_again():
    _, state, request, service, _, _ = harness('sales')
    assert all(r['evidence_gaps'] for r in service.calculate(Principal(subject='member'), request).result.plan['routes'])
    state['snapshot'] = observe(state['snapshot'], 'opted_out', False)
    request.expected_revision = 1
    allowed = service.calculate(Principal(subject='member'), request)
    assert all(not r['evidence_gaps'] for r in allowed.result.plan['routes'])
    assert all(r['approvals'] for r in allowed.result.plan['routes'])
    state['snapshot'] = observe(state['snapshot'], 'opted_out', True)
    request.expected_revision = 2
    assert all(r['evidence_gaps'] for r in service.calculate(Principal(subject='member'), request).result.plan['routes'])


def test_support_requires_both_host_review_and_observed_authority():
    _, state, request, service, _, _ = harness('support')
    assert all(r['hard_breaches'] for r in service.calculate(Principal(subject='member'), request).result.plan['routes'])
    state['snapshot'].constraints[0].confirmed = True
    state['snapshot'].revision = 1
    request.expected_revision = 1
    assert all(r['hard_breaches'] for r in service.calculate(Principal(subject='member'), request).result.plan['routes'])
    state['snapshot'] = observe(state['snapshot'], 'authority', True)
    request.expected_revision = 2
    result = service.calculate(Principal(subject='member'), request)
    assert all(not r['hard_breaches'] and r['approvals'] for r in result.result.plan['routes'])


def test_completion_is_not_observation_or_permission():
    selected = pack()
    snapshot = instantiate(selected, seed())
    snapshot.completed = ['route_a', 'verify']
    calculate(PlanRequest(snapshot=snapshot, as_of=NOW))
    assert all(x['status'] == 'unknown' for x in condition_states(snapshot).values())
    assert snapshot.approvals == []


@pytest.mark.parametrize('payload,code', [
    ('{"x":1,"x":2}', 'duplicate_json_key'),
    ('{"x":{"a":1,"a":2}}', 'duplicate_json_key'),
    ('{"x":NaN}', 'nonfinite_json'), ('{"x":Infinity}', 'nonfinite_json'),
    ('[]', 'pack_object_required'), ('null', 'pack_object_required'),
    ('{} trailing', 'invalid_json'), (b'\xff', 'invalid_json'),
    ('{"x":"\\ud800"}', 'invalid_unicode'),
    ('[' * 40 + '0' + ']' * 40, 'pack_object_required'),
    ('{"x":' + '[' * 40 + '0' + ']' * 40 + '}', 'pack_depth_limit'),
    (' ' * 262145, 'pack_size_limit'),
])
def test_json_limits_and_ambiguities_fail_closed(payload, code):
    with pytest.raises(PackError, match=code):
        load_pack_json(payload)


def test_json_is_explicit_not_paths_or_modules(tmp_path):
    marker = tmp_path / 'should_not_exist'
    malicious = data()
    malicious['prompts'][0]['text'] = f'__import__("pathlib").Path("{marker}").touch()'
    malicious['integrations'][0]['adapter_key'] = 'arbitrary_module'
    assert load_pack_json(json.dumps(malicious)).integrations[0].adapter_key == 'arbitrary_module'
    assert not marker.exists()
    with pytest.raises(PackError, match='invalid_json'):
        load_pack_json(str(FIXTURES / 'neutral.json'))
    with pytest.raises(PackError, match='json_text_required'):
        load_pack_json(data())


@pytest.mark.parametrize('change', [
    lambda d: d.update(schema_version='endstate.domain-pack.v2'),
    lambda d: d.update(engine_contract='endstate.plan.v2'),
    lambda d: d.update(pack_version='1.0'),
    lambda d: d.update(pack_version='01.0.0'),
    lambda d: d.update(execute='os.system'),
    lambda d: d['vocabulary'].append(d['vocabulary'][0]),
    lambda d: d['object_mappings'][0].update(engine_object='constraint'),
    lambda d: d['confirmation_rules'].pop(),
    lambda d: d['confirmation_rules'][0].update(evidence_requirement='Implicit success'),
    lambda d: d['integrations'][0].update(endpoint='https://example.invalid'),
    lambda d: d['integrations'][0]['operations'].append('source_ingest'),
    lambda d: d['integrations'][0].update(required_permissions=[]),
    lambda d: d['prompts'][0].update(disposition='execute'),
    lambda d: d['catalogue'].update(approvals=[]),
    lambda d: d['catalogue']['graph']['conditions'][0].pop('id'),
    lambda d: d['catalogue']['graph']['actions'][0].update(minutes=True),
    lambda d: d['catalogue']['graph']['actions'][0]['effects'][0].update(condition_id='foreign'),
    lambda d: d['catalogue']['graph']['conditions'][0]['provenance'].update(origin='manual'),
    lambda d: d['catalogue']['graph']['conditions'][0].update(due_at='2026-10-26T12:00:00Z'),
])
def test_strict_contract_and_hypothesis_boundary(change):
    value = data()
    change(value)
    with pytest.raises(ValidationError):
        load_pack_json(json.dumps(value))


def test_pack_cannot_confirm_policies_or_answer_questions():
    value = data('support')
    value['catalogue']['constraints'][0]['confirmed'] = True
    with pytest.raises(ValidationError, match='confirm a case policy'):
        load_pack_json(json.dumps(value))
    value = data('fixer')
    value['catalogue']['questions'][0]['answer'] = 'Unreviewed answer'
    with pytest.raises(ValidationError, match='answer a case question'):
        load_pack_json(json.dumps(value))


def test_pins_are_order_independent_but_include_every_section_and_detach_inputs():
    original = data()
    first = load_pack_json(json.dumps(original))
    reverse = load_pack_json(json.dumps(original, sort_keys=True, ensure_ascii=True))
    assert pack_reference(first) == pack_reference(reverse)
    original['owner'] = 'Mutated original'
    assert first.owner != original['owner']
    pin = pack_reference(first)
    first.prompts[0].text += ' Changed proposal instructions.'
    with pytest.raises(PackError, match='pack_reference_mismatch'):
        require_reference(first, pin)


def test_prior_validation_does_not_trust_constructed_or_mutated_objects():
    selected = pack()
    selected.catalogue.graph.actions[0].effects[0].condition_id = 'foreign'
    with pytest.raises(ValidationError):
        instantiate(selected, seed())
    valid = pack()
    forged = DomainPack.model_construct(**{k: getattr(valid, k) for k in DomainPack.model_fields})
    forged.pack_version = '999.0.0'
    assert pack_reference(forged).pack_version == '999.0.0'
    forged.__dict__['engine_contract'] = 'foreign'
    with pytest.raises(ValidationError):
        pack_reference(forged)


def test_migration_is_review_report_only_and_rejects_reused_or_downgraded_versions():
    original = pack()
    original_bytes = original.model_dump_json()
    assert compare_packs(original, original).disposition == 'identical'
    changed = original.model_copy(deep=True)
    changed.prompts[0].text += ' Changed proposal instructions.'
    with pytest.raises(PackError, match='newer_version'):
        compare_packs(original, changed)
    changed.pack_version = '0.2.0'
    report = compare_packs(original, changed)
    assert report.disposition == 'explicit_review_required'
    assert report.changed_sections == ['pack_version', 'prompts']
    assert report.automatic_case_migration is False
    assert original.model_dump_json() == original_bytes
    changed.pack_id = 'other'
    with pytest.raises(PackError, match='different_pack_identity'):
        compare_packs(original, changed)


@pytest.mark.parametrize('subject', ['outsider', 'local_operator_bearer'])
def test_unknown_or_local_principal_never_reads_agency_data(subject):
    _, state, request, service, _, _ = harness()
    with pytest.raises(PackError, match='permission_denied'):
        service.calculate(Principal(subject=subject), request)
    assert state['reads'] == 0


@pytest.mark.parametrize('field', ['tenant_id', 'matter_id', 'snapshot_id'])
def test_cross_scope_requests_are_denied_before_read(field):
    _, state, request, service, _, _ = harness()
    setattr(request.scope, field, 'foreign')
    with pytest.raises(PackError, match='permission_denied'):
        service.calculate(Principal(subject='member'), request)
    assert state['reads'] == 0


def test_truthy_grant_and_missing_adapters_never_create_local_bypass():
    selected, state, request, _, _, read = harness()
    service = PackConsumer(selected, authorise=lambda *_: 'allowed', read_snapshot=read)
    with pytest.raises(PackError, match='permission_denied'):
        service.calculate(Principal(subject='member'), request)
    assert state['reads'] == 0
    with pytest.raises(TypeError):
        PackConsumer(selected)


@pytest.mark.parametrize('phase', ['first_read', 'second_read', 'second_grant'])
def test_revocation_before_result_return_fails_without_retry(phase):
    selected, state, request, _, grant, read = harness()

    def revoking_read(scope):
        bound = read(scope)
        if (phase == 'first_read' and state['reads'] == 1) or (phase == 'second_read' and state['reads'] == 2):
            state['allowed'] = False
        return bound

    def revoking_grant(*args):
        if phase == 'second_grant' and state['checks'] == 1:
            state['allowed'] = False
        return grant(*args)

    service = PackConsumer(selected, authorise=revoking_grant, read_snapshot=revoking_read)
    with pytest.raises(PackError, match='permission_denied'):
        service.calculate(Principal(subject='member'), request)
    assert state['reads'] <= 2


@pytest.mark.parametrize('revised', [True, False])
def test_mid_calculation_snapshot_changes_are_not_returned(monkeypatch, revised):
    from endstate.domain_packs import consumer
    _, state, request, service, _, _ = harness()
    native = consumer.calculate

    def amend(*args):
        result = native(*args)
        state['snapshot'].budget = 0
        if revised:
            state['snapshot'].revision += 1
        return result

    monkeypatch.setattr(consumer, 'calculate', amend)
    with pytest.raises(PackError, match='stale_revision' if revised else 'snapshot_changed_without_revision'):
        service.calculate(Principal(subject='member'), request)


def test_stale_request_pack_change_catalogue_edit_and_reader_misbinding_fail_closed():
    selected, state, request, service, grant, _ = harness()
    request.expected_revision = 1
    with pytest.raises(PackError, match='stale_revision'):
        service.calculate(Principal(subject='member'), request)
    request.expected_revision = 0
    request.pack.sha256 = '0' * 64
    with pytest.raises(PackError, match='pack_reference_mismatch'):
        service.calculate(Principal(subject='member'), request)
    request.pack = pack_reference(selected)
    state['snapshot'].graph.actions[0].approval_required = False
    with pytest.raises(PackError, match='catalogue_review_required'):
        service.calculate(Principal(subject='member'), request)
    wrong = request.scope.model_copy(update={'tenant_id': 'foreign'})
    service = PackConsumer(selected, authorise=grant,
        read_snapshot=lambda _: BoundSnapshot(scope=wrong, snapshot=state['snapshot']))
    with pytest.raises(PackError, match='snapshot_scope_mismatch'):
        service.calculate(Principal(subject='member'), request)


def test_failed_read_is_visible_and_has_no_retry_or_write():
    selected, state, request, _, grant, _ = harness()

    def failed(_):
        state['reads'] += 1
        raise RuntimeError('Injected transaction failure')

    service = PackConsumer(selected, authorise=grant, read_snapshot=failed)
    before = state['snapshot'].model_dump_json()
    with pytest.raises(RuntimeError, match='Injected transaction failure'):
        service.calculate(Principal(subject='member'), request)
    assert state['reads'] == 1 and state['snapshot'].model_dump_json() == before


def test_consumer_requires_versions_timezone_and_exact_revision_types():
    _, _, request, _, _, _ = harness()
    for field, value in [('contract_version', 'future'), ('as_of', '2026-10-25T12:00:00'),
                         ('expected_revision', True), ('expected_revision', -1)]:
        payload = request.model_dump(mode='json')
        payload[field] = value
        with pytest.raises(ValidationError):
            ConsumerRequest.model_validate(payload)


def test_new_pack_consumer_imports_without_application_or_services(tmp_path):
    isolated = tmp_path / 'isolated'
    isolated.mkdir()
    shutil.copytree(ROOT / 'endstate', isolated / 'endstate', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copyfile(FIXTURES / 'neutral.json', isolated / 'pack.json')
    program = '''
import builtins
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if name.split('.')[0] in ('eightball', 'fastapi', 'sqlite3', 'httpx'):
        raise ImportError('Application/service import forbidden')
    return original(name, *args, **kwargs)
builtins.__import__ = guarded
from datetime import datetime, timezone
from pathlib import Path
from endstate.domain_packs import load_pack_json, instantiate, SnapshotSeed, pack_reference
from endstate.api import calculate, PlanRequest
p = load_pack_json(Path('pack.json').read_bytes())
s = instantiate(p, SnapshotSeed(snapshot_id='detached', owner='Operator',
    deadline=datetime(2026,10,26,tzinfo=timezone.utc), budget=10000))
assert calculate(PlanRequest(snapshot=s, as_of=datetime(2026,10,25,tzinfo=timezone.utc))).plan['routes']
assert pack_reference(p).pack_id == 'neutral'
'''
    result = subprocess.run([sys.executable, '-c', program], cwd=isolated, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
