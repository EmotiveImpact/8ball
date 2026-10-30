"""Register explicitly under the authenticated v2 router; no global wiring."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import Field

from endstate.intelligence.knowledge import KnowledgeContext, KnowledgeDraft, KnowledgeReview
from endstate.primitives import Identifier, Strict
from .knowledge import KnowledgeConflict, KnowledgeUnavailable


class KnowledgeWrite(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    expected_case_revision: int = Field(strict=True, ge=0)
    request_id: Identifier
    draft: KnowledgeDraft | None = None
    review: KnowledgeReview | None = None
    retire: bool = Field(default=False, strict=True)


def register_intelligence_routes(router: APIRouter, service, *, context_for_request):
    """context_for_request resolves verified actor + org/matter/case server-side.

    It must reject absent/expired identity and wrong case scope. It is not a
    replacement for service operation/object checks inside each transaction.
    """
    def call(request, case_id, operation):
        try:
            context = context_for_request(request, case_id)
            if context is None:
                raise PermissionError()
            context = KnowledgeContext.model_validate(context)
            if context.case_id != case_id:
                raise PermissionError()
            return operation(context)
        except PermissionError:
            raise HTTPException(403, 'Current intelligence permission required') from None
        except KnowledgeConflict:
            raise HTTPException(409, 'Reference or case changed; reload before continuing') from None
        except KnowledgeUnavailable:
            raise HTTPException(404, 'Reference or source is not available') from None
        except ValueError:
            raise HTTPException(400, 'Invalid reference request') from None

    @router.get('/cases/{case_id}/knowledge')
    def search(request: Request, case_id: str, q: str = '', limit: int = 20):
        return call(request, case_id, lambda context: service.search(context, q, limit=limit))

    @router.get('/cases/{case_id}/knowledge/{item_id}')
    def read(request: Request, case_id: str, item_id: str, history: bool = False):
        return call(request, case_id, lambda context: service.read(context, item_id, history=history))

    @router.post('/cases/{case_id}/knowledge/{item_id}')
    def write(request: Request, case_id: str, item_id: str, body: KnowledgeWrite):
        return call(request, case_id, lambda context: service.write(
            context, item_id=item_id, **body.model_dump(exclude={'draft', 'review'}),
            draft=body.draft, review=body.review))
