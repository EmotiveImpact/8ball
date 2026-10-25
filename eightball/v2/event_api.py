"""Explicit agency event review routes; no ingestion, inference or external send."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import Field

from .commands import Command
from .contracts import Strict
from .event_reviews import EventReviews
from .event_outbox import EventOutbox


class ReviewedGraph(Strict):
    command: Command
    rationale: str = Field(min_length=10, max_length=2000)


def register_event_routes(router: APIRouter, store):
    reviews = EventReviews(store)
    outbox = EventOutbox(store)

    def call(request, operation, **kwargs):
        identity = getattr(request.state, 'agency_identity', None)
        if identity is None:
            raise HTTPException(403, 'Verified agency identity is required')
        try:
            return operation(identity, **kwargs)
        except PermissionError:
            raise HTTPException(403, 'Access is not permitted') from None

    @router.get('/cases/{case_id}/event-work/{work_id}')
    def view(request: Request, case_id: str, work_id: str):
        return call(request, lambda identity: reviews.view(case_id=case_id, work_id=work_id, reader=identity))

    @router.post('/cases/{case_id}/event-work/{work_id}/review')
    def review(request: Request, case_id: str, work_id: str, body: ReviewedGraph):
        return call(request, lambda identity: reviews.commit_graph(
            case_id=case_id, work_id=work_id, reviewer=identity, command=body.command,
            rationale=body.rationale, require_read=True))

    @router.post('/cases/{case_id}/change-notices/pull')
    def pull(request: Request, case_id: str):
        return call(request, lambda identity: outbox.pull(case_id=case_id, reader=identity))

    @router.post('/cases/{case_id}/change-notices/{notice_id}/acknowledge')
    def acknowledge(request: Request, case_id: str, notice_id: int):
        call(request, lambda identity: outbox.acknowledge(case_id=case_id, reader=identity, notice_id=notice_id))
        return {'delivery_acknowledged': True, 'action_approved': False}
