"""Opt-in agency event routes; no implicit processing or external sending."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import Field

from .commands import Command
from .contracts import Strict
from .event_reviews import EventReviews
from .event_outbox import EventOutbox
from .authoring import GraphPreview
from endstate.events import IncomingEvent
from ..store import Conflict


class ReviewedGraph(Strict):
    command: Command
    rationale: str = Field(min_length=10, max_length=2000)


class ProcessingReview(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    receipt_sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    rationale: str = Field(min_length=10, max_length=2000)


class DispatchRequest(Strict):
    sequence: int = Field(strict=True, ge=1)
    expected_revision: int = Field(strict=True, ge=0)
    review_id: str = Field(min_length=1, max_length=100)
    request_id: str = Field(min_length=1, max_length=100)


def register_event_worker_routes(router: APIRouter, service):
    """Integrator opts in and maps auth operations; no dispatch/provider HTTP route."""
    def invoke(request, operation, **kwargs):
        identity = getattr(request.state, 'agency_identity', None)
        if identity is None:
            raise HTTPException(403, 'Verified agency identity is required')
        try:
            return operation(identity=identity, **kwargs)
        except PermissionError:
            raise HTTPException(403, 'Access is not permitted') from None
        except KeyError:
            raise HTTPException(404, 'Event record not found') from None
        except ValueError:
            raise HTTPException(409, 'Event state changed or request is not admissible') from None

    @router.post('/cases/{case_id}/incoming-events')
    def ingest(request: Request, case_id: str, body: IncomingEvent):
        return invoke(request, service.ingest, case_id=case_id, event=body)

    @router.post('/cases/{case_id}/incoming-events/{sequence}/processing-review')
    def source_review(request: Request, case_id: str, sequence: int, body: ProcessingReview):
        return invoke(request, service.review_source, case_id=case_id, sequence=sequence,
                      **body.model_dump())

    @router.post('/cases/{case_id}/processing-reviews/{review_id}/revoke')
    def revoke(request: Request, case_id: str, review_id: str):
        invoke(request, service.revoke_source_review, case_id=case_id, review_id=review_id)
        return {'processing_review_revoked': True, 'external_request_recalled': False}

    @router.post('/cases/{case_id}/event-attempts')
    def enqueue(request: Request, case_id: str, body: DispatchRequest):
        work_id = invoke(request, service.enqueue, case_id=case_id, **body.model_dump())
        return {'work_id': work_id, 'state': 'inspect_current_state', 'command_authority': False}

    @router.post('/cases/{case_id}/event-work/{work_id}/cancel')
    def cancel(request: Request, case_id: str, work_id: str):
        invoke(request, service.cancel, case_id=case_id, work_id=work_id)
        return {'local_attempt_cancelled': True, 'external_request_recalled': False}

    @router.get('/cases/{case_id}/event-work/{work_id}/dispatch-status')
    def status(request: Request, case_id: str, work_id: str):
        return invoke(request, service.status, case_id=case_id, work_id=work_id)


def register_event_routes(router: APIRouter, store, *, source_policy=None, current_identity=None):
    reviews = EventReviews(store, source_policy=source_policy, current_identity=current_identity)
    outbox = EventOutbox(store, current_identity=current_identity)

    def call(request, operation, **kwargs):
        identity = getattr(request.state, 'agency_identity', None)
        if identity is None:
            raise HTTPException(403, 'Verified agency identity is required')
        try:
            return operation(identity, **kwargs)
        except PermissionError:
            raise HTTPException(403, 'Access is not permitted') from None
        except KeyError:
            raise HTTPException(404, 'Event record not found') from None
        except (ValueError, Conflict):
            raise HTTPException(409, 'Event state changed or request is not admissible') from None

    @router.get('/cases/{case_id}/event-work/{work_id}')
    def view(request: Request, case_id: str, work_id: str):
        return call(request, lambda identity: reviews.view(case_id=case_id, work_id=work_id, reader=identity))

    @router.post('/cases/{case_id}/event-work/{work_id}/review')
    def review(request: Request, case_id: str, work_id: str, body: ReviewedGraph):
        return call(request, lambda identity: reviews.commit_graph(
            case_id=case_id, work_id=work_id, reviewer=identity, command=body.command,
            rationale=body.rationale, require_read=True))

    @router.post('/cases/{case_id}/event-work/{work_id}/preview')
    def preview(request: Request, case_id: str, work_id: str, body: GraphPreview):
        return call(request, lambda identity: reviews.preview(
            case_id=case_id, work_id=work_id, reader=identity, request=body))

    @router.post('/cases/{case_id}/change-notices/pull')
    def pull(request: Request, case_id: str):
        return call(request, lambda identity: outbox.pull(case_id=case_id, reader=identity))

    @router.post('/cases/{case_id}/change-notices/{notice_id}/acknowledge')
    def acknowledge(request: Request, case_id: str, notice_id: int):
        call(request, lambda identity: outbox.acknowledge(case_id=case_id, reader=identity, notice_id=notice_id))
        return {'delivery_acknowledged': True, 'action_approved': False}
