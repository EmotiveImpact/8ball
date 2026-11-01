"""Controlled complete-plan method; no provider calls or semantic acceptance."""
from copy import deepcopy

import pytest
from pydantic import ValidationError

from endstate.intelligence.operating import OperatingPlanningSpec, coordinate_operating
from endstate.intelligence.planning import CoordinationStopped
from tests.test_operating import brief, plan, units


def specification():
    return OperatingPlanningSpec(id='fictional-operating-method', brief=brief(),
        roles=[dict(id='commercial', instructions='Challenge distribution and unit economics.'),
               dict(id='delivery', instructions='Challenge rights, quality and practical dependencies.'),
               dict(id='skeptic', instructions='Challenge unsupported assumptions and missing evidence.')],
        max_seconds=120, planning_cost_policy='explicit_unpriced_token_bound')


def outputs():
    p = plan().model_dump(mode='json')
    values = [p]
    for role in specification().roles:
        values.append(dict(role_id=role.id, assessment='The original goal remains conditional.',
            concerns=[dict(id='missing', concern='Actual fees are unknown.', why_it_matters='Surplus cannot be calculated.',
                requirement_ids=['profit'], step_ids=['sample'], calculation_ids=['surplus'],
                source_quote='Fictional reviewed source', evidence_kind='derived',
                suggested_correction='Measure fees before scaling.', check_next='Record actual platform deductions.')],
            limitations=['Role review from the same generative model, not a human or native decision specialist.']))
    revised = deepcopy(p)
    revised['steps'][0]['instructions'].append('Record actual fees before changing the sales target.')
    values.append(dict(plan=revised, dispositions=[dict(concern_ref=r.id+':missing', disposition='unresolved',
        reason='Instructions improved but no actual fee observation is available.', changed_fields=['steps'])
        for r in specification().roles], additional_changes=[]))
    return values


def run(values=None, *, checkpoint=lambda: None, models=None, generate_error=None):
    values = outputs() if values is None else values
    calls = []
    def generate(schema, instructions, context):
        assert isinstance(schema, dict) and schema['type'] == 'object'
        assert 'bare JSON object' in instructions and 'no Markdown fences' in instructions
        assert 'EXACT human outcome' in instructions and 'not private internal chain-of-thought' in instructions
        calls.append(deepcopy(context))
        if generate_error:
            raise generate_error
        # A hostile adapter cannot mutate earlier source/plan/review records.
        context.clear()
        return deepcopy(values[len(calls)-1]), (models[len(calls)-1] if models else 'explicit-fixture-model')
    def no_decision_model(*args):
        raise AssertionError('Never fabricate decision-model explanations')
    report = coordinate_operating(specification(), 'Fictional reviewed source', 'fictional-run',
                                  generate, no_decision_model, checkpoint)
    return report, calls


def test_full_method_preserves_goal_original_reviews_explanations_and_sops():
    result, calls = run()
    assert result['stop_reason'] == 'completed'
    assert result['generation_attempts'] == len(calls) == 5
    assert result['initial']['plan'] == outputs()[0]
    assert all(a['validated'] for a in result['attempts'])
    assert [c['review']['role_id'] for c in result['challenges']] == ['commercial', 'delivery', 'skeptic']
    assert all('challenges' not in c for c in calls[:4])
    assert all(c['original_proposal'] == result['initial'] for c in calls[1:4])
    assert calls[4]['challenges'] == result['challenges']
    assert result['comparison']['changed_fields'] == ['steps']
    assert not result['comparison']['improvement_established']
    assert not result['final_synthesis']['objections_resolved']
    assert result['final_synthesis']['selected_route'] is None
    assert result['final_synthesis']['completed_actions'] == []
    assert result['final_synthesis']['observed_effects'] == []
    assert result['advisory_only'] and not result['execution_authorized']
    assert not result['facts_attested'] and not result['predictive_quality_approved']
    assert result['revision']['plan']['steps'][0]['completion_evidence'] != result['revision']['plan']['steps'][0]['outcome_evidence']


@pytest.mark.parametrize('index', range(5))
def test_failed_stage_is_retained_and_stops_without_retry(index):
    values = outputs()
    values[index]['unexpected'] = 'A malformed output remains malformed.'
    result, calls = run(values)
    assert result['stop_reason'] == 'invalid_' + result['phase'] + '_input_or_result'
    assert len(calls) == index + 1
    assert result['attempts'][-1]['output'] == values[index]
    assert not result['attempts'][-1]['validated']
    assert result['final_synthesis'] is None


@pytest.mark.parametrize('mutate', [
    lambda v: v[0].update(outcome='Only create colouring pages, not the original full goal.'),
    lambda v: v[0]['coverage'].pop(),
    lambda v: v[0]['calculations'][0].update(units=units(orders=1)),
    lambda v: v[1].update(role_id='another_role'),
    lambda v: v[1]['concerns'][0].update(source_quote='An invented source quote'),
    lambda v: v[1]['concerns'][0].update(requirement_ids=['invented']),
    lambda v: v[1]['concerns'][0].update(step_ids=['invented']),
    lambda v: v[1]['concerns'][0].update(calculation_ids=['invented']),
    lambda v: v[4]['dispositions'].pop(),
    lambda v: v[4]['dispositions'].append(deepcopy(v[4]['dispositions'][0])),
    lambda v: v[4]['dispositions'][0].update(concern_ref='invented:missing'),
    lambda v: v[4]['dispositions'][0].update(changed_fields=['variables']),
    lambda v: v[4]['dispositions'][0].update(disposition='retained'),
    lambda v: v[4]['plan'].update(unresolved_questions=['Unexplained new change']),
    lambda v: v[4]['additional_changes'].append(dict(field='variables', reason='Claimed but not changed.')),
])
def test_no_scope_drift_invented_attribution_or_unexplained_revisions(mutate):
    values = outputs()
    mutate(values)
    result, _ = run(values)
    assert result['stop_reason'] != 'completed' and result['final_synthesis'] is None


def test_additional_changes_require_their_own_explicit_reason():
    values = outputs()
    values[4]['plan']['unresolved_questions'].append('Which test channel yields actual buyers?')
    values[4]['additional_changes'] = [dict(field='unresolved_questions', reason='Make distribution uncertainty explicit.')]
    result, _ = run(values)
    assert result['stop_reason'] == 'completed'
    assert result['comparison']['changed_fields'] == ['steps', 'unresolved_questions']


def test_a_revision_can_be_unchanged_with_explained_retention():
    values = outputs()
    values[4]['plan'] = deepcopy(values[0])
    for d in values[4]['dispositions']:
        d.update(disposition='retained', changed_fields=[], reason='Keep the explicit unknown until observed.')
    result, _ = run(values)
    assert result['stop_reason'] == 'completed'
    assert result['comparison']['changed_fields'] == []
    assert not result['final_synthesis']['objections_resolved']


@pytest.mark.parametrize('stage', range(1, 5))
def test_model_substitution_stops(stage):
    models = ['explicit-fixture-model']*5
    models[stage] = 'unapproved-fallback'
    result, calls = run(models=models)
    assert result['stop_reason'] == 'changed_planning_model'
    assert len(calls) == stage + 1


def test_provider_failure_and_authority_revocation_never_retry():
    result, calls = run(generate_error=CoordinationStopped('planning_provider_failed'))
    assert result['stop_reason'] == 'planning_provider_failed' and len(calls) == 1
    assert result['attempts'][0]['output'] is None
    with pytest.raises(PermissionError):
        run(checkpoint=lambda: (_ for _ in ()).throw(PermissionError('Current access revoked')))


@pytest.mark.parametrize('field,value', [('roles', []), ('roles', [dict(id='x', instructions='Review')]*2),
                                        ('max_seconds', True), ('max_seconds', 601)])
def test_explicit_roles_and_allowance_required(field, value):
    data = specification().model_dump(mode='json')
    data[field] = value
    with pytest.raises(ValidationError):
        OperatingPlanningSpec.model_validate(data)
