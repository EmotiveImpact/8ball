"""Conservative event replan cache; this module never commits a case or a course."""
from collections import OrderedDict
from dataclasses import dataclass
from hashlib import sha256
import json
from threading import Lock
from time import perf_counter
from typing import Literal

from endstate.api import PlanRequest, PlanResponse, calculate


@dataclass(frozen=True)
class ReplanResult:
    response: PlanResponse
    mode: Literal['full', 'unchanged_inputs']
    elapsed_seconds: float


class EventReplanner:
    """Reuse only identical planning inputs at the exact same explicit clock.

    Revision-only changes can reuse a result only without revision-bound action
    approvals. Every other change falls back to the existing complete kernel.
    The cache is process-local, bounded and contains no execution authority.
    """
    def __init__(self, *, max_entries=16):
        if type(max_entries) is not int or not 1 <= max_entries <= 64:
            raise ValueError('A cache size between 1 and 64 is required')
        self.max_entries = max_entries
        self._cache = OrderedDict()
        self._lock = Lock()

    def replan(self, request: PlanRequest | dict) -> ReplanResult:
        started = perf_counter()
        parsed = PlanRequest.model_validate(
            request.model_dump(mode='python') if isinstance(request, PlanRequest) else request)
        key_data = parsed.model_dump(mode='json')
        if not parsed.snapshot.approvals:
            key_data['snapshot'].pop('revision')
        key = sha256(json.dumps(key_data, sort_keys=True, ensure_ascii=False,
                                separators=(',', ':')).encode()).hexdigest()
        with self._lock:
            cached = self._cache.get(key)
            if cached is None:
                response = calculate(parsed)
                mode = 'full'
            else:
                data = json.loads(cached)
                data['revision'] = data['plan']['revision'] = parsed.snapshot.revision
                response = PlanResponse.model_validate(data)
                mode = 'unchanged_inputs'
            self._cache[key] = response.model_dump_json()
            self._cache.move_to_end(key)
            while len(self._cache) > self.max_entries:
                self._cache.popitem(last=False)
        return ReplanResult(response=response, mode=mode,
                            elapsed_seconds=max(0, perf_counter()-started))
