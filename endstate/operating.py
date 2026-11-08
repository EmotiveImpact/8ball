"""Detached operating-plan proposals and checked scenario arithmetic, never authority."""
from decimal import Context, Decimal, DecimalException, ROUND_CEILING, ROUND_HALF_EVEN, localcontext
from typing import Annotated, Literal

from pydantic import AwareDatetime, Field, model_validator

from .primitives import Identifier, Strict

Note = Annotated[str, Field(min_length=1, max_length=800, pattern=r'\S')]
Number = Annotated[str, Field(pattern=r'^-?(?:0|[1-9][0-9]{0,17})(?:\.[0-9]{1,8})?$')]
Power = Annotated[int, Field(strict=True, ge=-8, le=8)]


class Dimension(Strict):
    name: Identifier
    power: Power


Units = Annotated[list[Dimension], Field(max_length=6)]


class Requirement(Strict):
    id: Identifier
    text: Note
    kind: Literal['success', 'constraint']


class OutcomeBrief(Strict):
    outcome: Note
    requirements: list[Requirement] = Field(min_length=1, max_length=16)
    deadline: AwareDatetime | None
    budget: Number | None
    currency: Identifier | None

    @model_validator(mode='after')
    def distinct(self):
        _unique(self.requirements)
        if not any(r.kind == 'success' for r in self.requirements):
            raise ValueError('An explicit success requirement is needed')
        if self.budget is not None and (Decimal(self.budget) < 0 or not self.currency):
            raise ValueError('A known budget needs a currency and cannot be negative')
        return self


class Variable(Strict):
    id: Identifier
    title: Note
    value: Number | None
    units: Units
    basis: Literal['assumption', 'unknown']
    rationale: Note
    check_next: Note

    @model_validator(mode='after')
    def missing_is_unknown(self):
        if (self.value is None) != (self.basis == 'unknown'):
            raise ValueError('Missing numbers are unknown, not zero or free')
        return self


class Calculation(Strict):
    id: Identifier
    title: Note
    operation: Literal['add', 'subtract', 'multiply', 'divide', 'ceil']
    inputs: list[Identifier] = Field(min_length=1, max_length=8)
    units: Units


class Strategy(Strict):
    id: Identifier
    title: Note
    beneficiary: Note
    offer_or_deliverable: Note
    delivery_or_distribution: list[Note] = Field(min_length=1, max_length=6)
    why_this_route: Note


class Step(Strict):
    id: Identifier
    strategy_id: Identifier
    title: Note
    proposed_owner: Note
    prerequisites: list[Identifier] = Field(max_length=16)
    instructions: list[Note] = Field(min_length=1, max_length=8)
    deliverable: Note
    estimated_minutes: Number | None
    cost_variable_ids: list[Identifier] = Field(max_length=8)
    proposed_due_at: AwareDatetime | None
    completion_evidence: Note
    outcome_evidence: Note
    reconsider_when: list[Note] = Field(min_length=1, max_length=6)
    human_authorization_required: Literal[True] = True

    @model_validator(mode='after')
    def nonnegative_time(self):
        if self.estimated_minutes is not None and Decimal(self.estimated_minutes) < 0:
            raise ValueError('Estimated work time cannot be negative')
        return self


class Coverage(Strict):
    requirement_id: Identifier
    step_ids: list[Identifier] = Field(min_length=1, max_length=16)
    explanation: Note


class OperatingPlan(Strict):
    outcome: Note
    brief_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    strategies: list[Strategy] = Field(min_length=1, max_length=3)
    steps: list[Step] = Field(min_length=1, max_length=24)
    variables: list[Variable] = Field(max_length=32)
    calculations: list[Calculation] = Field(max_length=32)
    coverage: list[Coverage] = Field(min_length=1, max_length=16)
    unresolved_questions: list[Note] = Field(max_length=16)
    risks_and_stop_rules: list[Note] = Field(min_length=1, max_length=16)


def _unique(items):
    if len({x.id for x in items}) != len(items):
        raise ValueError('Repeated identifier')


def _units(units):
    if not isinstance(units, dict):
        names = [d.name for d in units]
        if len(set(names)) != len(names):
            raise ValueError('Repeated unit dimension')
        units = {d.name: d.power for d in units}
    return {k: v for k, v in sorted(units.items()) if v}


def arithmetic(plan: OperatingPlan):
    """50-digit Decimal arithmetic; units and unknowns propagate independently."""
    plan = OperatingPlan.model_validate(plan.model_dump(mode='python'))
    _unique([*plan.variables, *plan.calculations])
    values = {v.id: (None if v.value is None else Decimal(v.value), _units(v.units))
              for v in plan.variables}
    rows = []
    for calc in plan.calculations:
        if any(ref not in values for ref in calc.inputs):
            raise ValueError('Calculation references must exist in dependency order')
        operands = [values[ref] for ref in calc.inputs]
        numbers = [x[0] for x in operands]
        units = operands[0][1].copy()
        op, error = calc.operation, None
        if op in ('add', 'subtract'):
            if any(u != units for _, u in operands):
                error = 'incompatible_units'
        elif op in ('multiply', 'divide'):
            units = {}
            for index, (_, dimensions) in enumerate(operands):
                for key, power in dimensions.items():
                    units[key] = units.get(key, 0) + power * (-1 if op == 'divide' and index else 1)
            units = _units(units)
        if (op in ('subtract', 'divide') and len(operands) != 2
                or op == 'ceil' and len(operands) != 1):
            error = 'invalid_operand_count'
        if units != _units(calc.units):
            error = 'incorrect_result_units'
        if op == 'divide' and len(numbers) == 2 and numbers[1] == 0:
            error = 'zero_divisor'
        value = None
        if error is None and all(n is not None for n in numbers):
            try:
                with localcontext(Context(prec=50, rounding=ROUND_HALF_EVEN)):
                    if op == 'add':
                        value = sum(numbers, Decimal(0))
                    elif op == 'subtract':
                        value = numbers[0] - numbers[1]
                    elif op == 'multiply':
                        value = Decimal(1)
                        for n in numbers:
                            value *= n
                    elif op == 'divide':
                        value = numbers[0] / numbers[1]
                    else:
                        value = numbers[0].to_integral_value(rounding=ROUND_CEILING)
                    if (not value.is_finite() or value != 0
                            and not Decimal('1e-30') <= abs(value) <= Decimal('1e30')):
                        error, value = 'result_out_of_range', None
                    elif value == 0:
                        value = Decimal(0)
            except DecimalException:
                error, value = 'invalid_arithmetic', None
        values[calc.id] = (value, units)
        rows.append(dict(id=calc.id, value=None if value is None else format(value, 'f'),
                         units=units, status='invalid' if error else 'unknown' if value is None else 'calculated',
                         error=error))
    return dict(calculations=rows, valid=not any(r['error'] for r in rows),
                unknown_variable_ids=[v.id for v in plan.variables if v.value is None],
                precision=50, rounding='ROUND_HALF_EVEN', scenario_only=True,
                facts_attested=False, predictive_quality_approved=False)


def inspect_plan(brief: OutcomeBrief, plan: OperatingPlan):
    from .intelligence.planning import fingerprint

    brief = OutcomeBrief.model_validate(brief.model_dump(mode='python'))
    plan = OperatingPlan.model_validate(plan.model_dump(mode='python'))
    if plan.outcome != brief.outcome or plan.brief_sha256 != fingerprint(brief.model_dump(mode='json')):
        raise ValueError('The exact human goal and requirements cannot be replaced by a subtask')
    _unique([*plan.strategies, *plan.steps, *plan.variables, *plan.calculations])
    strategies = {s.id for s in plan.strategies}
    variables = {v.id for v in plan.variables}
    steps = set()
    used_strategies = set()
    for step in plan.steps:
        if (step.strategy_id not in strategies or not set(step.prerequisites) <= steps
                or len(set(step.prerequisites)) != len(step.prerequisites)
                or not set(step.cost_variable_ids) <= variables):
            raise ValueError('Unknown, cyclic, forward or repeated step prerequisite/reference')
        steps.add(step.id)
        used_strategies.add(step.strategy_id)
    if used_strategies != strategies:
        raise ValueError('Every strategy needs practical work, not just a title')
    coverage_ids = [c.requirement_id for c in plan.coverage]
    if (len(set(coverage_ids)) != len(coverage_ids)
            or set(coverage_ids) != {r.id for r in brief.requirements}
            or any(not set(c.step_ids) <= steps for c in plan.coverage)):
        raise ValueError('Every original success criterion and constraint needs explicit coverage')
    return dict(arithmetic=arithmetic(plan), structural_coverage_only=True,
                semantic_quality_approved=False, execution_authorized=False)


def compare_plans(brief: OutcomeBrief, original: OperatingPlan, revision: OperatingPlan):
    """Inspectable changes, not a claim that coordination improved the outcome."""
    before, after = inspect_plan(brief, original), inspect_plan(brief, revision)
    old, new = original.model_dump(mode='json'), revision.model_dump(mode='json')
    return dict(changed_fields=[k for k in old if old[k] != new[k]],
                original=before, revision=after, improvement_established=False,
                semantic_quality_approved=False, execution_authorized=False)
