"""Explicit read-only result contracts for endstate.plan.v1.

Typed dictionaries preserve the established JSON and mapping interface. They
validate outputs without adding defaults, coercing times, or changing old audit
records. They describe calculations, not permission or truth outside the input.
"""
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, TypedDict, NotRequired
from pydantic import (AfterValidator, ConfigDict, Field, StrictBool, StrictFloat,
                      StrictInt, TypeAdapter, with_config)


def aware_iso(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError('Result clock must be timezone-aware')
    return value


ISO = Annotated[str, AfterValidator(aware_iso)]
Number = Annotated[StrictInt | StrictFloat, Field(allow_inf_nan=False)]
Nonnegative = Annotated[Number, Field(ge=0)]
Count = Annotated[StrictInt, Field(ge=0)]
State = Literal['true', 'false', 'unknown', 'disputed']
ActionStatus = Literal['ready', 'blocked', 'approval_required', 'completed']
Order = Literal['fewest_unknowns', 'fastest', 'lowest_cost', 'fewest_external',
                'least_irreversible', 'operator_risk']
strict = with_config(ConfigDict(extra='forbid', strict=True, allow_inf_nan=False))


@strict
class LiteralResult(TypedDict):
    condition_id: str
    value: StrictBool


@strict
class EvidenceGap(LiteralResult):
    status: State
    reason: NotRequired[str]
    action_id: NotRequired[str]


@strict
class ConditionState(TypedDict):
    status: State
    observations: list[str]
    evidence: list[str]


@strict
class ActionState(TypedDict):
    id: str
    status: ActionStatus
    missing: list[EvidenceGap]
    guards: list[EvidenceGap]
    reasons: list[str]
    effects_evidenced: StrictBool
    approval_expires_at: ISO | None
    selected_decision: str | None


@strict
class ScheduleEntry(TypedDict):
    action_id: str
    start_minute: Nonnegative
    active_end_minute: Nonnegative
    end_minute: Nonnegative
    wait_known: StrictBool


@strict
class DecisionGate(TypedDict):
    id: str
    required_option: str
    action_id: str
    reason: NotRequired[str]


@strict
class ExpressionResult(TypedDict):
    op: Literal['atom', 'all', 'any']
    condition_id: str | None
    value: StrictBool
    args: list['ExpressionResult']


@strict
class ContingencyResult(TypedDict):
    action_id: str
    label: str
    when: ExpressionResult
    response: str
    next_action_ids: list[str]
    due_at: ISO | None
    trigger_state: State


@strict
class EvidenceCoverage(TypedDict):
    supported: Count
    required: Count


@strict
class RouteResult(TypedDict):
    id: str
    title: str
    actions: list[str]
    schedule: list[ScheduleEntry]
    prerequisites: dict[str, list[LiteralResult]]
    dependencies: list[Annotated[list[str], Field(min_length=2, max_length=2)]]
    evidence_gaps: list[EvidenceGap]
    used_conditions: list[str]
    hard_breaches: list[str]
    soft_warnings: list[str]
    decisions: list[DecisionGate]
    external_dependencies: list[str]
    unknown_waits: list[str]
    irreversible_actions: list[str]
    contingencies: list[ContingencyResult]
    minutes: Nonnegative
    remaining_cost: Count
    spent: Count
    total_cost: Count
    slack_minutes: Number
    risk: Annotated[StrictInt, Field(ge=0, le=2)]
    provisional: StrictBool
    evidence_coverage: EvidenceCoverage
    objectives: dict[str, State]
    status: Literal['constraint_failure', 'needs_evidence', 'needs_decision', 'conditional']
    ready: list[str]
    approvals: list[str]
    fingerprint: Annotated[str, Field(pattern=r'^[0-9a-f]{64}$')]


@strict
class PlanResult(TypedDict):
    revision: Count
    computed_at: ISO
    states: dict[str, ConditionState]
    action_states: dict[str, ActionState]
    objective_states: dict[str, State]
    objective_failures: list[str]
    routes: list[RouteResult]
    outcome_evidenced: StrictBool
    search_truncated: StrictBool
    expansions: Count
    sort_by: Order
    limits: str


@strict
class NowItem(TypedDict):
    id: str
    title: str
    status: Literal['ready', 'approval_required']


@strict
class NextItem(TypedDict):
    id: str
    title: str
    blockers: list[str]


@strict
class WatchItem(TypedDict):
    condition_id: str
    title: str
    deadline: ISO
    status: State


@strict
class QuestionResult(TypedDict):
    id: str
    question: str
    why: str
    owner: str
    condition_ids: list[str]
    route_ids: list[str]
    blocked_action_ids: list[str]
    objective_ids: list[str]
    due_at: ISO | None
    status: Literal['open', 'answered']
    generated: StrictBool
    recorded_status: NotRequired[Literal['open', 'answered']]
    answer: NotRequired[str]
    evidence_review_required: NotRequired[StrictBool]


# Domain records occur in the briefing in their original JSON form. A local
# TypedDict avoids converting their date strings into datetime/model instances.
@strict
class SourceSpanResult(TypedDict):
    evidence_id: str
    start: Count
    end: Count
    quote: str


@strict
class ProvenanceResult(TypedDict):
    origin: Literal['operator', 'source_claim', 'model_proposal', 'playbook', 'legacy']
    references: list[SourceSpanResult]
    note: str
    run_id: str | None


@strict
class DecisionOptionResult(TypedDict):
    id: str
    title: str
    explanation: str


@strict
class DecisionResult(TypedDict):
    id: str
    provenance: ProvenanceResult
    question: str
    owner: str
    needed_by: ISO | None
    options: list[DecisionOptionResult]
    selected: str | None
    rationale: str
    evidence_ids: list[str]
    decided_at: ISO | None
    decided_revision: Count | None


@strict
class BriefingResult(TypedDict):
    now: list[NowItem]
    next: list[NextItem]
    decisions: list[DecisionResult]
    questions: list[QuestionResult]
    watch: list[WatchItem]
    routes: list[RouteResult]
    summary: str
    notices: list[str]


PLAN_ADAPTER = TypeAdapter(PlanResult)
BRIEFING_ADAPTER = TypeAdapter(BriefingResult)


def validate_plan(value: object) -> PlanResult:
    """Validate nested output and internal references; return a detached mapping."""
    data = PLAN_ADAPTER.validate_python(value)
    conditions = set(data['states'])
    actions = set(data['action_states'])
    objectives = set(data['objective_states'])
    ids = [r['id'] for r in data['routes']]
    if len(ids) != len(set(ids)):
        raise ValueError('Result contains duplicate route identities')
    if not set(data['objective_failures']) <= objectives:
        raise ValueError('Result failure references an unknown objective')
    for key, action in data['action_states'].items():
        if key != action['id']:
            raise ValueError('Result action key and ID differ')
        if any(g['condition_id'] not in conditions for g in action['missing'] + action['guards']):
            raise ValueError('Action readiness references an unknown condition')
    for route in data['routes']:
        selected = set(route['actions'])
        if len(selected) != len(route['actions']) or not selected <= actions:
            raise ValueError('Route has duplicate or unknown actions')
        if route['actions'] != [s['action_id'] for s in route['schedule']]:
            raise ValueError('Route schedule and action order disagree')
        if not set(route['prerequisites']) <= actions:
            raise ValueError('Route prerequisites reference an unknown action')
        if not set(route['used_conditions']) <= conditions or any(g['condition_id'] not in conditions for g in route['evidence_gaps']):
            raise ValueError('Route references unknown conditions')
        if any(lit['condition_id'] not in conditions for ls in route['prerequisites'].values() for lit in ls):
            raise ValueError('Route literal references an unknown condition')
        if any(not set(edge) <= actions for edge in route['dependencies']):
            raise ValueError('Route dependency references an unknown action')
        for key in ('ready', 'approvals', 'external_dependencies', 'unknown_waits', 'irreversible_actions'):
            # An unscheduled cyclic action may appear in metadata of an invalid
            # candidate. Validate membership in the catalogue, not a fake schedule.
            if not set(route[key]) <= actions:
                raise ValueError('Route metadata references an unknown action')
        for step in route['schedule']:
            if not step['start_minute'] <= step['active_end_minute'] <= step['end_minute']:
                raise ValueError('Route schedule has inverted time boundaries')
        if route['spent'] + route['remaining_cost'] != route['total_cost']:
            raise ValueError('Route cost total is inconsistent')
        if route['evidence_coverage']['supported'] > route['evidence_coverage']['required']:
            raise ValueError('Evidence coverage exceeds required literals')
        if set(route['objectives']) != objectives:
            raise ValueError('Route objective set disagrees with result')
    return data
