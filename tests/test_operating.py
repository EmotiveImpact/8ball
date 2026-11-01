"""Fictional scenario arithmetic and proposal contracts, not market validation."""
from copy import deepcopy
from decimal import Decimal, localcontext

import pytest
from pydantic import ValidationError

from endstate.intelligence.planning import fingerprint
from endstate.operating import (Calculation, OutcomeBrief, OperatingPlan, arithmetic,
                                compare_plans, inspect_plan)


def units(**dimensions):
    return [dict(name=name, power=power) for name, power in dimensions.items()]


def brief():
    return OutcomeBrief(outcome='Earn a fictional GBP 1000 surplus before the stated deadline.',
        requirements=[dict(id='profit', kind='success', text='Surplus, not just gross sales.'),
                      dict(id='budget', kind='constraint', text='No upfront cash spending.')],
        deadline='2026-12-25T00:00:00Z', budget='0', currency='GBP')


def plan(goal=None):
    goal = goal or brief()
    return OperatingPlan(outcome=goal.outcome, brief_sha256=fingerprint(goal.model_dump(mode='json')),
        strategies=[dict(id='direct', title='Test a digital offer', beneficiary='Adult buyers',
            offer_or_deliverable='A reviewed printable kit', why_this_route='A fictional test, not proven demand.',
            delivery_or_distribution=['Permission-based organic demonstrations.'])],
        steps=[dict(id='sample', strategy_id='direct', title='Review an original sample',
            proposed_owner='Designer, subject to approval', prerequisites=[],
            instructions=['Create a sample.', 'Check rights and inspect a physical print.'],
            deliverable='A rights-reviewed, printed sample', estimated_minutes=None,
            cost_variable_ids=['unknown_cost'], proposed_due_at=None,
            completion_evidence='Retain the sample and review record.',
            outcome_evidence='A customer result needs separate observation.',
            reconsider_when=['Stop if rights or print quality remain unresolved.'])],
        variables=[dict(id='price', title='Assumed price', value='20', units=units(GBP=1, orders=-1),
                       basis='assumption', rationale='Fictional price, not measured.', check_next='Test willingness to buy.'),
                   dict(id='orders', title='Assumed orders', value='100', units=units(orders=1),
                       basis='assumption', rationale='A scenario, not sales.', check_next='Observe paid orders.'),
                   dict(id='unknown_cost', title='Unknown cost', value=None, units=units(GBP=1),
                       basis='unknown', rationale='Not yet measured.', check_next='Check actual fees and costs.')],
        calculations=[dict(id='gross', title='Gross revenue', operation='multiply',
                           inputs=['price', 'orders'], units=units(GBP=1)),
                      dict(id='surplus', title='Surplus', operation='subtract',
                           inputs=['gross', 'unknown_cost'], units=units(GBP=1))],
        coverage=[dict(requirement_id=r.id, step_ids=['sample'], explanation='Proposed work; coverage is not success.')
                  for r in goal.requirements], unresolved_questions=['What is the actual acquisition cost?'],
        risks_and_stop_rules=['Do not publish or spend before explicit owner approval.'])


def test_exact_goal_arithmetic_unknowns_and_no_mutation():
    goal, proposal = brief(), plan()
    before = goal.model_dump_json(), proposal.model_dump_json()
    result = inspect_plan(goal, proposal)
    assert result['arithmetic']['valid']
    assert result['arithmetic']['calculations'][0]['value'] == '2000'
    assert result['arithmetic']['calculations'][1]['status'] == 'unknown'
    assert result['arithmetic']['unknown_variable_ids'] == ['unknown_cost']
    assert not result['execution_authorized'] and not result['semantic_quality_approved']
    assert before == (goal.model_dump_json(), proposal.model_dump_json())


@pytest.mark.parametrize('mutate', [
    lambda p: p.update(outcome='Only make a sample, ignoring the full outcome.'),
    lambda p: p.update(brief_sha256='0'*64),
    lambda p: p['coverage'].pop(),
    lambda p: p['coverage'].append(deepcopy(p['coverage'][0])),
    lambda p: p['coverage'][0].update(step_ids=['absent']),
    lambda p: p['steps'][0].update(prerequisites=['sample']),
    lambda p: p['steps'][0].update(prerequisites=['missing']),
    lambda p: p['steps'][0].update(cost_variable_ids=['absent']),
    lambda p: p['steps'][0].update(strategy_id='missing'),
    lambda p: p['strategies'].append(dict(p['strategies'][0], id='unused')),
    lambda p: p['variables'][0].update(id='direct'),
    lambda p: p['calculations'][0].update(inputs=['surplus']),
])
def test_rejects_scope_drift_and_broken_references(mutate):
    value = plan().model_dump(mode='json')
    mutate(value)
    with pytest.raises(ValueError):
        inspect_plan(brief(), OperatingPlan.model_validate(value))


@pytest.mark.parametrize('mutate', [
    lambda p: p['variables'][0].update(value=20),
    lambda p: p['variables'][0].update(value=True),
    lambda p: p['variables'][0].update(value='NaN'),
    lambda p: p['variables'][0].update(value='1e99'),
    lambda p: p['variables'][0].update(value='0.123456789'),
    lambda p: p['variables'][0].update(basis='verified'),
    lambda p: p['variables'][0].update(value=None),
    lambda p: p['variables'][2].update(value='0'),
    lambda p: p['variables'][0].update(units=units(GBP=True)),
    lambda p: p['steps'][0].update(human_authorization_required=False),
    lambda p: p['steps'][0].update(estimated_minutes='-1'),
    lambda p: p['steps'][0].update(completed=True),
    lambda p: p['steps'][0].update(instructions=[]),
    lambda p: p.update(facts_attested=True),
])
def test_strict_model_outputs_cannot_create_authority_or_facts(mutate):
    value = plan().model_dump(mode='json')
    mutate(value)
    with pytest.raises(ValidationError):
        OperatingPlan.model_validate(value)


@pytest.mark.parametrize('operation,inputs,units,error', [
    ('add', ['price', 'orders'], {'GBP': 1}, 'incorrect_result_units'),
    ('multiply', ['price', 'orders'], {'orders': 1}, 'incorrect_result_units'),
    ('subtract', ['orders'], {'orders': 1}, 'invalid_operand_count'),
    ('ceil', ['orders', 'orders'], {'orders': 1}, 'invalid_operand_count'),
])
def test_invalid_arithmetic_is_retained_not_repaired(operation, inputs, units, error):
    p = plan()
    p.calculations[0].operation = operation
    p.calculations[0].inputs = inputs
    p.calculations[0].units = [dict(name=k, power=v) for k, v in units.items()]
    report = arithmetic(p)
    assert not report['valid']
    assert report['calculations'][0]['error'] == error
    assert report['calculations'][0]['value'] is None


def test_zero_divisor_does_not_become_unknown_or_free():
    p = plan()
    p.variables[1].value = '0'
    p.calculations[0].operation = 'divide'
    p.calculations[0].units = units(GBP=1, orders=-2)
    assert arithmetic(p)['calculations'][0]['error'] == 'zero_divisor'


def test_decimal_rounding_and_ceiling_for_required_visits():
    p = plan()
    p.variables[0].value = '0.02'
    p.variables[0].units = units(orders=1, visits=-1)
    p.variables[1].value = '3650'
    p.calculations = [dict(id='visits', title='Required visits at assumed conversion',
        operation='divide', inputs=['orders', 'price'], units=units(visits=1))]
    p = OperatingPlan.model_validate(p.model_dump(mode='python'))
    assert arithmetic(p)['calculations'][0]['value'] == '182500'
    p.calculations.append(Calculation(id='whole_visits', title='Whole visits', operation='ceil',
        inputs=['visits'], units=units(visits=1)))
    p.variables[0].value = '0.03'
    with localcontext() as ctx:
        ctx.prec = 3
        result = arithmetic(OperatingPlan.model_validate(p.model_dump(mode='python')))
    assert result['calculations'][1]['value'] == '121667'
    assert result['precision'] == 50


def test_comparison_does_not_claim_coordination_or_customer_benefit():
    original, revised = plan(), plan()
    revised.steps[0].instructions.append('Record the actual fee, not a guessed zero.')
    result = compare_plans(brief(), original, revised)
    assert result['changed_fields'] == ['steps']
    assert not result['improvement_established'] and not result['execution_authorized']


def test_arithmetic_precision_rounding_and_traps_are_not_inherited():
    from decimal import Inexact, ROUND_UP
    p = plan()
    p.variables[0].value = '3'
    p.variables[0].units = units(orders=1, visits=-1)
    p.calculations = [Calculation(id='visits', title='Required visits', operation='divide',
                                 inputs=['orders', 'price'], units=units(visits=1))]
    expected = arithmetic(p)
    with localcontext() as ctx:
        ctx.prec = 2
        ctx.rounding = ROUND_UP
        ctx.traps[Inexact] = True
        assert arithmetic(p) == expected


def test_tiny_computed_magnitudes_fail_before_unbounded_fixed_point_rendering():
    p = plan()
    p.variables = p.variables[:1]
    p.variables[0].value, p.variables[0].units = '0.00000001', []
    p.calculations = []
    previous = 'price'
    for index in range(6):
        name = 'tiny' + str(index)
        p.calculations.append(Calculation(id=name, title='Tiny fictional product',
            operation='multiply', inputs=[previous] * 8, units=[]))
        previous = name
    r = arithmetic(p)
    assert not r['valid']
    assert r['calculations'][0]['error'] == 'result_out_of_range'
    assert all(c['value'] is None for c in r['calculations'])
    assert all(c['status'] == 'unknown' for c in r['calculations'][1:])


def test_exact_zero_results_are_canonical_not_arbitrary_fractional_padding():
    p = plan()
    p.variables = p.variables[:1]
    p.variables[0].value, p.variables[0].units = '0.00000000', []
    p.calculations = [Calculation(id='zero', title='Exact zero', operation='multiply',
                                 inputs=['price'] * 8, units=[])]
    r = arithmetic(p)
    assert r['valid'] and r['calculations'][0]['value'] == '0'


def test_smallest_supported_nonzero_magnitude_is_calculated():
    p = plan()
    p.variables = p.variables[:2]
    p.variables[0].value, p.variables[0].units = '0.00000001', []
    p.variables[1].value, p.variables[1].units = '0.000001', []
    p.calculations = [Calculation(id='tiny', title='Supported lower bound', operation='multiply',
                                 inputs=['price'] * 3 + ['orders'], units=[])]
    r = arithmetic(p)
    assert r['valid'] and r['calculations'][0]['value'] == '0.' + '0' * 29 + '1'


@pytest.mark.parametrize('change', [dict(budget='-1'), dict(budget='0', currency=None),
                                  dict(deadline='2026-12-25T00:00:00'), dict(requirements=[])])
def test_outcome_contract_is_explicit_and_timezone_aware(change):
    value = brief().model_dump(mode='json')
    value.update(change)
    with pytest.raises(ValidationError):
        OutcomeBrief.model_validate(value)
