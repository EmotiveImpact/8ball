"""Versioned in-process calculation boundary. No storage or execution authority.

This internal preview accepts Python/JSON-shaped requests. It is not an HTTP
endpoint. Costs use the caller's consistent whole-unit accounting convention.
"""
from typing import Any, Literal, Mapping
from pydantic import AwareDatetime, Field, model_validator
from . import CONTRACT_VERSION
from .contracts import PlanningSnapshot
from .primitives import Strict, Identifier
from . import planner
from .results import PlanResult, BriefingResult, validate_plan

Order = Literal['fewest_unknowns', 'fastest', 'lowest_cost', 'fewest_external',
                'least_irreversible', 'operator_risk']


class PlanRequest(Strict):
    contract_version: Literal['endstate.plan.v1'] = CONTRACT_VERSION
    snapshot: PlanningSnapshot
    as_of: AwareDatetime
    sort_by: Order = 'fewest_unknowns'


class PlanResponse(Strict):
    contract_version: Literal['endstate.plan.v1'] = CONTRACT_VERSION
    snapshot_id: Identifier
    revision: int = Field(strict=True, ge=0)
    plan: PlanResult
    briefing: BriefingResult

    @model_validator(mode='after')
    def result_integrity(self):
        validated = validate_plan(self.plan)
        if validated['revision'] != self.revision:
            raise ValueError('Response and plan revisions differ')
        if self.briefing['routes'] != self.plan['routes']:
            raise ValueError('Briefing refers to another plan')
        actions = set(validated['action_states'])
        routes = {r['id'] for r in validated['routes']}
        conditions = set(validated['states'])
        if any(n['id'] not in actions for n in self.briefing['now'] + self.briefing['next']):
            raise ValueError('Briefing action is not in the result')
        for q in self.briefing['questions']:
            if not set(q['route_ids']) <= routes or not set(q['condition_ids']) <= conditions:
                raise ValueError('Briefing question refers to another plan')
        return self


def calculate(request: PlanRequest | Mapping[str, Any]) -> PlanResponse:
    """Validate a detached snapshot and calculate; do not mutate caller state.

    Invalid versions, naive clocks, negative budgets and dangling references
    raise Pydantic ValidationError. Unachievable goals instead return gaps or
    constraint failures. A successful calculation does not approve an action.
    """
    data = request.model_dump(mode='python') if isinstance(request, PlanRequest) else dict(request)
    parsed = PlanRequest.model_validate(data)
    validated = PlanRequest.model_validate(parsed.model_dump(mode='python'))
    state = validated.snapshot
    result = planner.plan(state, validated.as_of, validated.sort_by)
    return PlanResponse(snapshot_id=state.id, revision=state.revision,
                        plan=result, briefing=planner.briefing(state, result))
