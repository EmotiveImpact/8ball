"""Register only under a host authenticated router with explicit operation mapping."""
from fastapi import APIRouter, HTTPException, Request

from .contracts import OpenRecord, Scope, Transition, VerifyRevocation
from .journal import OperationsConflict, OperationsUnavailable


def register_operations_routes(router: APIRouter, service):
    def call(request, organisation_id, matter_id, case_id, method, *args):
        identity = getattr(request.state, 'agency_identity', None)
        if identity is None:
            raise HTTPException(403, 'Verified agency identity is required')
        try:
            scope = Scope(organisation_id=organisation_id, matter_id=matter_id, case_id=case_id)
            return method(identity, scope, *args)
        except PermissionError:
            raise HTTPException(403, 'Access is not permitted') from None
        except KeyError:
            raise HTTPException(404, 'Operations record not found') from None
        except OperationsConflict:
            raise HTTPException(409, 'Operations conflict; refresh and review') from None
        except OperationsUnavailable:
            raise HTTPException(503, 'Operations adapter unavailable') from None
        except ValueError:
            raise HTTPException(422, 'Invalid operations request') from None

    prefix = '/organisations/{organisation_id}/matters/{matter_id}/cases/{case_id}/operations'

    @router.get(prefix)
    def view(request: Request, organisation_id: str, matter_id: str, case_id: str):
        return call(request, organisation_id, matter_id, case_id, service.view)

    @router.post(prefix)
    def create(request: Request, organisation_id: str, matter_id: str, case_id: str, body: OpenRecord):
        return call(request, organisation_id, matter_id, case_id, service.open, body)

    @router.post(prefix + '/{record_id}/transition')
    def transition(request: Request, organisation_id: str, matter_id: str, case_id: str,
                   record_id: str, body: Transition):
        return call(request, organisation_id, matter_id, case_id, service.transition, record_id, body)

    @router.post(prefix + '/{record_id}/verify-revocation')
    def verify(request: Request, organisation_id: str, matter_id: str, case_id: str,
               record_id: str, body: VerifyRevocation):
        return call(request, organisation_id, matter_id, case_id, service.verify_revocation, record_id, body)
