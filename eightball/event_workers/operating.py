"""Full-plan method on the existing current-authority, opt-in event host."""
from endstate.intelligence.operating import (
    MAX_GENERATION_CALLS, VERSION, OperatingPlanningSpec, coordinate_operating)

from .planning import CoordinatedPlanningProcessor


class OperatingPlanningProcessor(CoordinatedPlanningProcessor):
    spec_type = OperatingPlanningSpec
    version = VERSION
    max_generation_calls = MAX_GENERATION_CALLS
    method = staticmethod(coordinate_operating)
    kind = 'operating_planning'

    def reviewer(self, spec, session_factory):
        # Written challenges use separate contexts on the pinned planning model.
        return None
