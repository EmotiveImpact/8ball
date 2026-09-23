"""Compatibility adapter: 8BALL V2 now calculates through the ENDSTATE kernel.

There is no second copy of the planning algorithm here. Wire-format plans and
product metadata deltas remain compatible; persistence/commands stay in 8BALL.
"""
from datetime import datetime
from endstate import planner as kernel
from endstate.contracts import PlanningSnapshot
from endstate.state import condition_states
from .contracts import Case, Expr, Action, literals
from ..models import utcnow

# Existing internal callers and tools retain these imports.
MAX_ROUTES = kernel.MAX_ROUTES
MAX_EXPANSIONS = kernel.MAX_EXPANSIONS
RISK = kernel.RISK
Lit = kernel.Lit
Bundle = kernel.Bundle
merge = kernel.merge
evaluate = kernel.evaluate
expression_text = kernel.expression_text
unsatisfied = kernel.unsatisfied
applicable_constraints = kernel.applicable_constraints
readiness = kernel.readiness


def to_snapshot(case: Case) -> PlanningSnapshot:
    """Copy only the declared engine input, never product/client metadata.

    Serialising to Python values and validating from a dict rechecks nested
    mutable collections too. model_copy(update=...) alone would not do that.
    """
    return PlanningSnapshot.model_validate(
        case.model_dump(mode='python', include=set(PlanningSnapshot.model_fields))
    )


def plan(case: Case, now: datetime | None = None, sort_by: str = 'fewest_unknowns') -> dict:
    return kernel.plan(to_snapshot(case), now, sort_by)


def question_priorities(case: Case, result: dict) -> list[dict]:
    return kernel.question_priorities(to_snapshot(case), result)


def briefing(case: Case, result: dict) -> dict:
    return kernel.briefing(to_snapshot(case), result)


def changes(before: Case, after: Case, bp: dict, ap: dict) -> dict:
    result = kernel.explain_changes(to_snapshot(before), to_snapshot(after), bp, ap)
    result['metadata_changed'] = [
        name for name in ('title', 'desired_outcome', 'status', 'priority', 'owner', 'next_update')
        if getattr(before, name) != getattr(after, name)
    ]
    return result
