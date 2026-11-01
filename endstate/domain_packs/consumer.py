"""Read-only, frozen-catalogue consumer seam; the host retains all write authority."""
from typing import Callable, Literal

from pydantic import AwareDatetime, Field

from ..api import Order, PlanRequest, PlanResponse, calculate
from ..contracts import PlanningSnapshot
from ..primitives import Identifier, Strict, Title
from .contracts import DomainPack, PackReference
from .loader import PackError, checked_pack, pack_reference, require_reference


class SnapshotSeed(Strict):
    snapshot_id: Identifier
    owner: Title
    deadline: AwareDatetime
    budget: int = Field(strict=True, ge=0, le=100_000_000)


def instantiate(pack: DomainPack, seed: SnapshotSeed) -> PlanningSnapshot:
    parsed = checked_pack(pack)
    seed = SnapshotSeed.model_validate(seed.model_dump(mode='python'))
    return PlanningSnapshot(id=seed.snapshot_id, owner=seed.owner, deadline=seed.deadline,
                            budget=seed.budget, **parsed.catalogue.model_dump(mode='python'))


class Scope(Strict):
    tenant_id: Identifier
    matter_id: Identifier
    snapshot_id: Identifier


class Principal(Strict):
    subject: Identifier


class BoundSnapshot(Strict):
    scope: Scope
    snapshot: PlanningSnapshot


class ConsumerRequest(Strict):
    contract_version: Literal['endstate.domain-consumer.v1'] = 'endstate.domain-consumer.v1'
    scope: Scope
    pack: PackReference
    expected_revision: int = Field(strict=True, ge=0)
    as_of: AwareDatetime
    sort_by: Order = 'fewest_unknowns'


class ConsumerResponse(Strict):
    contract_version: Literal['endstate.domain-consumer.v1'] = 'endstate.domain-consumer.v1'
    scope: Scope
    pack: PackReference
    result: PlanResponse


class PackConsumer:
    """Injected host grants and scoped reads, no cache or database on import.

    Grant checker must query CURRENT authority and return exactly True or raise.
    Reader must not fall back to another tenant/matter. The final rechecks prevent
    publishing a result after observed revocation or revision change, but do not
    replace host transaction isolation and cannot recall already returned data.
    """
    def __init__(self, pack: DomainPack, *,
                 authorise: Callable[[Principal, Scope, str], bool],
                 read_snapshot: Callable[[Scope], BoundSnapshot]):
        self._pack = checked_pack(pack)
        self._authorise = authorise
        self._read_snapshot = read_snapshot

    def _check_grant(self, principal: Principal, scope: Scope):
        if self._authorise(principal.model_copy(deep=True), scope.model_copy(deep=True), 'plan_read') is not True:
            raise PackError('permission_denied')

    def _read(self, request: ConsumerRequest) -> PlanningSnapshot:
        bound = self._read_snapshot(request.scope.model_copy(deep=True))
        bound = BoundSnapshot.model_validate(bound.model_dump(mode='python'))
        if bound.scope != request.scope or bound.snapshot.id != request.scope.snapshot_id:
            raise PackError('snapshot_scope_mismatch')
        if bound.snapshot.revision != request.expected_revision:
            raise PackError('stale_revision')
        return bound.snapshot

    def calculate(self, principal: Principal, request: ConsumerRequest) -> ConsumerResponse:
        principal = Principal.model_validate(principal.model_dump(mode='python'))
        request = ConsumerRequest.model_validate(request.model_dump(mode='python'))
        self._check_grant(principal, request.scope)
        require_reference(self._pack, request.pack)
        snapshot = self._read(request)
        # This consumer exercises unchanged catalogue inputs, not arbitrary case
        # amendments. It never overlays templates on live evidence or approvals.
        for field in ('graph', 'constraints', 'resources'):
            expected = getattr(self._pack.catalogue, field)
            actual = getattr(snapshot, field)
            if field == 'constraints':
                # A live host may separately record manual policy review; the
                # template itself cannot supply that confirmation.
                actual = [c.model_copy(update={'confirmed': False}) for c in actual]
            if actual != expected:
                raise PackError('catalogue_review_required')
        result = calculate(PlanRequest(snapshot=snapshot, as_of=request.as_of, sort_by=request.sort_by))
        self._check_grant(principal, request.scope)
        latest = self._read(request)
        if latest.model_dump(mode='json') != snapshot.model_dump(mode='json'):
            raise PackError('snapshot_changed_without_revision')
        self._check_grant(principal, request.scope)
        return ConsumerResponse(scope=request.scope, pack=pack_reference(self._pack), result=result)
