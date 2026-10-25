"""Registerable vault routes. The host supplies verified identity and service."""
import base64
import binascii
import json

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, ValidationError
from starlette.concurrency import run_in_threadpool

from eightball.vault.contracts import Conflict, IntegrityError, Unavailable


class Record(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class Upload(Record):
    content_base64: str = Field(min_length=1, max_length=349_528)
    filename: str = Field(min_length=1, max_length=120)
    media_type: str
    retain_until: AwareDatetime
    command_id: str = Field(min_length=8, max_length=128)


class Command(Record):
    expected_revision: int = Field(ge=1)
    command_id: str = Field(min_length=8, max_length=128)


class Control(Command):
    reason: str = Field(min_length=10, max_length=1000)


class Hold(Control):
    hold: bool


class Retention(Control):
    retain_until: AwareDatetime


class Download(Record):
    expected_revision: int = Field(ge=1)
    expected_sha256: str = Field(pattern='^[0-9a-f]{64}$')


async def read_body(request, model, limit=8192):
    raw = bytearray()
    async for chunk in request.stream():
        raw.extend(chunk)
        if len(raw) > limit:
            raise HTTPException(413, 'Vault request exceeds the bounded size')
    try:
        return model.model_validate_json(bytes(raw))
    except (ValidationError, ValueError):
        raise HTTPException(422, 'Invalid vault request') from None


def register_vault_routes(router: APIRouter, service):
    """Relative routes belong below the existing authenticated /api/v2 router."""

    def identity(request):
        actor = getattr(request.state, 'agency_identity', None)
        if actor is None:
            raise HTTPException(403, 'Verified agency identity is required')
        return actor

    def call(request, operation, **kwargs):
        try:
            return operation(identity=identity(request), **kwargs)
        except PermissionError:
            raise HTTPException(403, 'Access is not permitted') from None
        except Conflict as exc:
            raise HTTPException(409, str(exc)) from None
        except (IntegrityError, Unavailable):
            raise HTTPException(503, 'Vault unavailable; content remains protected') from None
        except (ValueError, UnicodeError, binascii.Error):
            raise HTTPException(422, 'Invalid vault request') from None

    def output(value):
        return Response(json.dumps(value, ensure_ascii=False), media_type='application/json',
                        headers={'Cache-Control': 'no-store, private', 'X-Content-Type-Options': 'nosniff'})

    @router.get('/cases/{case_id}/vault')
    def inventory(request: Request, case_id: str):
        return output(call(request, service.inventory, case_id=case_id))

    @router.post('/cases/{case_id}/vault')
    async def upload(request: Request, case_id: str):
        identity(request)
        body = await read_body(request, Upload, 400_000)
        try:
            content = base64.b64decode(body.content_base64, validate=True)
        except (ValueError, binascii.Error):
            raise HTTPException(422, 'Invalid original encoding') from None
        return output(call(request, service.upload, case_id=case_id, content=content,
                           **body.model_dump(exclude={'content_base64'})))

    @router.get('/cases/{case_id}/vault/audit')
    def audit(request: Request, case_id: str, after: int = 0, limit: int = 100):
        return output(call(request, service.audit, case_id=case_id, after=after, limit=limit))

    @router.get('/cases/{case_id}/vault/{object_id}')
    def metadata(request: Request, case_id: str, object_id: str):
        return output(call(request, service.metadata, case_id=case_id, object_id=object_id))

    @router.post('/cases/{case_id}/vault/{object_id}/download')
    async def download(request: Request, case_id: str, object_id: str):
        identity(request)
        body = await read_body(request, Download)
        content = call(request, service.read_original, case_id=case_id, object_id=object_id, **body.model_dump())
        return Response(content, media_type='application/octet-stream', headers={
            'Content-Disposition': 'attachment; filename="original.txt"',
            'Cache-Control': 'no-store, private', 'X-Content-Type-Options': 'nosniff'})

    @router.post('/cases/{case_id}/vault/{object_id}/scan')
    async def scan(request: Request, case_id: str, object_id: str):
        identity(request)
        body = await read_body(request, Command)
        return output(await run_in_threadpool(call, request, service.scan, case_id=case_id,
                                             object_id=object_id, **body.model_dump()))

    @router.post('/cases/{case_id}/vault/{object_id}/cancel-scan')
    async def cancel(request: Request, case_id: str, object_id: str):
        identity(request)
        body = await read_body(request, Control)
        return output(call(request, service.cancel_scan, case_id=case_id, object_id=object_id, **body.model_dump()))

    @router.post('/cases/{case_id}/vault/{object_id}/hold')
    async def hold(request: Request, case_id: str, object_id: str):
        identity(request)
        body = await read_body(request, Hold)
        return output(call(request, service.set_hold, case_id=case_id, object_id=object_id, **body.model_dump()))

    @router.post('/cases/{case_id}/vault/{object_id}/retention')
    async def retention(request: Request, case_id: str, object_id: str):
        identity(request)
        body = await read_body(request, Retention)
        return output(call(request, service.set_retention, case_id=case_id, object_id=object_id, **body.model_dump()))

    @router.post('/cases/{case_id}/vault/{object_id}/delete-local')
    async def delete(request: Request, case_id: str, object_id: str):
        identity(request)
        body = await read_body(request, Control)
        return output(call(request, service.delete, case_id=case_id, object_id=object_id, **body.model_dump()))
