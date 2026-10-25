"""Registerable agency-only routes. No registration or local-token fallback."""
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from ..authorisation import Identity
from ..collaboration.contracts import GrantRequest
from ..projections.service import DraftRequest, ReviewRequest
from ..store import Conflict


def register_collaboration_routes(router: APIRouter, collaboration, projections):
    def verified(request: Request, response: Response):
        response.headers['Cache-Control'] = 'no-store, private'
        response.headers['Pragma'] = 'no-cache'
        identity = getattr(request.state, 'agency_identity', None)
        if not isinstance(identity, Identity):
            raise HTTPException(401, 'Verified agency identity required', headers={'Cache-Control': 'no-store'})
        return identity

    def call(fn, *, public=False):
        try:
            return fn()
        except PermissionError:
            raise HTTPException(403, 'Collaboration access is not permitted', headers={'Cache-Control': 'no-store'}) from None
        except KeyError:
            if public:
                raise HTTPException(403, 'Collaboration access is not permitted', headers={'Cache-Control': 'no-store'}) from None
            raise HTTPException(404, 'Collaboration record not found', headers={'Cache-Control': 'no-store'}) from None
        except Conflict:
            if public:
                raise HTTPException(403, 'Collaboration access is not permitted', headers={'Cache-Control': 'no-store'}) from None
            raise HTTPException(409, 'Collaboration state changed; refresh and review again', headers={'Cache-Control': 'no-store'}) from None
        except ValueError:
            if public:
                raise HTTPException(403, 'Collaboration access is not permitted', headers={'Cache-Control': 'no-store'}) from None
            raise HTTPException(422, 'Invalid collaboration request', headers={'Cache-Control': 'no-store'}) from None
        except sqlite3.IntegrityError:
            if public:
                raise HTTPException(403, 'Collaboration access is not permitted', headers={'Cache-Control': 'no-store'}) from None
            raise HTTPException(409, 'Collaboration request conflicts with stored state', headers={'Cache-Control': 'no-store'}) from None

    @router.get('/cases/{case_id}/collaboration/grants')
    def grants(case_id: str, actor=Depends(verified)):
        return call(lambda: collaboration.grants(actor=actor, case_id=case_id))

    @router.post('/cases/{case_id}/collaboration/grants')
    def create_grant(case_id: str, body: GrantRequest, actor=Depends(verified)):
        return call(lambda: collaboration.create_grant(actor=actor, case_id=case_id, request=body))

    @router.post('/cases/{case_id}/collaboration/grants/{grant_id}/revoke')
    def revoke(case_id: str, grant_id: str, actor=Depends(verified)):
        return call(lambda: collaboration.revoke_grant(actor=actor, case_id=case_id, grant_id=grant_id))

    @router.get('/cases/{case_id}/collaboration/objects/{object_id}/expert/{grant_id}')
    def expert(case_id: str, object_id: str, grant_id: str, actor=Depends(verified)):
        return call(lambda: collaboration.expert_read(actor=actor, case_id=case_id, object_id=object_id, grant_id=grant_id), public=True)

    @router.post('/cases/{case_id}/collaboration/objects/{object_id}/projections')
    def draft(case_id: str, object_id: str, body: DraftRequest, actor=Depends(verified)):
        return call(lambda: projections.draft(actor=actor, case_id=case_id, object_id=object_id, request=body))

    @router.get('/cases/{case_id}/collaboration/objects/{object_id}/projections/{projection_id}/review')
    def inspect(case_id: str, object_id: str, projection_id: str, actor=Depends(verified)):
        return call(lambda: projections.inspect(actor=actor, case_id=case_id, object_id=object_id, projection_id=projection_id))

    @router.post('/cases/{case_id}/collaboration/objects/{object_id}/projections/{projection_id}/review')
    def review(case_id: str, object_id: str, projection_id: str, body: ReviewRequest, actor=Depends(verified)):
        return call(lambda: projections.review(actor=actor, case_id=case_id, object_id=object_id, projection_id=projection_id, request=body))

    @router.post('/cases/{case_id}/collaboration/objects/{object_id}/projections/{projection_id}/withdraw')
    def withdraw(case_id: str, object_id: str, projection_id: str, actor=Depends(verified)):
        return call(lambda: projections.withdraw(actor=actor, case_id=case_id, object_id=object_id, projection_id=projection_id))

    @router.get('/cases/{case_id}/collaboration/objects/{object_id}/projections/{projection_id}')
    def client(case_id: str, object_id: str, projection_id: str, actor=Depends(verified)):
        return call(lambda: projections.client_read(actor=actor, case_id=case_id, object_id=object_id, projection_id=projection_id), public=True)
