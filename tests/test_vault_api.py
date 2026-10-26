"""ASGI route contract tests, not native-browser or real malware evidence."""
import base64
from datetime import timedelta

from fastapi import APIRouter, FastAPI, Request
from fastapi.testclient import TestClient
import pytest

from eightball.v2.vault_api import register_vault_routes
from tests.test_vault import env, upload, scan


@pytest.fixture
def client(env):
    app = FastAPI()
    @app.middleware('http')
    async def fictional_identity(request: Request, call_next):
        if request.headers.get('x-fixture-identity') == 'fictional-operator':
            request.state.agency_identity = env.identity
        return await call_next(request)
    router = APIRouter(prefix='/api/v2')
    register_vault_routes(router, env.vault)
    app.include_router(router)
    with TestClient(app) as client:
        client.headers['x-fixture-identity'] = 'fictional-operator'
        yield client


BASE = '/api/v2/cases/case-1/vault'


def body(env):
    return dict(content_base64=base64.b64encode(b'Fictional original\r\n').decode(), filename='fictional.txt',
                media_type='text/plain', retain_until=(env.now[0]+timedelta(days=8)).isoformat(), command_id='upload-route-001')


def test_api_upload_quarantine_explicit_scan_download_and_no_implicit_fact(env, client):
    response = client.post(BASE, json=body(env))
    assert response.status_code == 200
    obj = response.json()
    path = f"{BASE}/{obj['object_id']}"
    assert obj['status'] == 'quarantined' and env.scanner.calls == 0
    assert client.get(path).headers['cache-control'] == 'no-store, private'
    assert client.post(path+'/download', json={'expected_revision':1,'expected_sha256':obj['sha256']}).status_code == 409
    released = client.post(path+'/scan', json={'expected_revision':1,'command_id':'scan-route-001'})
    assert released.status_code == 200 and released.json()['status'] == 'released'
    download = client.post(path+'/download', json={'expected_revision':3,'expected_sha256':obj['sha256']})
    assert download.content == b'Fictional original\r\n'
    assert download.headers['content-type'] == 'application/octet-stream'
    assert download.headers['x-content-type-options'] == 'nosniff'
    assert 'attachment' in download.headers['content-disposition']
    assert client.get(BASE+'/audit').json()['independently_anchored'] is False


def test_api_body_cannot_supply_identity_or_scan_result(env, client):
    assert client.post(BASE, json=body(env) | {'identity':env.identity.model_dump()}).status_code == 422
    obj = upload(env)
    path = f"{BASE}/{obj['object_id']}"
    assert client.post(path+'/scan', json={'expected_revision':1,'command_id':'scan-route-001','verdict':'clean'}).status_code == 422
    client.headers.pop('x-fixture-identity')
    assert client.get(path).status_code == 403
    assert client.post(BASE, json=body(env)).status_code == 403


def test_api_checks_actual_streamed_size_and_encoding(env, client):
    def chunks():
        yield b'{"content_base64":"'
        yield b'x'*400_001
    assert client.post(BASE, content=chunks()).status_code == 413
    assert client.post(BASE, json=body(env) | {'content_base64':'not base64!'}).status_code == 422
    assert client.post(BASE, content=b'{broken').status_code == 422
    assert client.get(BASE).json() == []


def test_api_revocation_stale_hash_and_cross_scope_fail_closed(env, client):
    obj = scan(env, upload(env))
    path = f"{BASE}/{obj['object_id']}"
    assert client.post(path+'/download', json={'expected_revision':1,'expected_sha256':obj['sha256']}).status_code == 409
    assert client.post(path+'/download', json={'expected_revision':3,'expected_sha256':'0'*64}).status_code == 409
    assert client.get(path.replace('case-1','case-2')).status_code == 403
    env.registry.revoke('grant-1')
    assert client.get(path).status_code == 403
    assert client.post(path+'/download', json={'expected_revision':3,'expected_sha256':obj['sha256']}).status_code == 403


def test_api_scanner_missing_is_unavailable_not_clean(env, client):
    obj = upload(env)
    env.vault.scanner = None
    response = client.post(f"{BASE}/{obj['object_id']}/scan", json={'expected_revision':1,'command_id':'scan-route-001'})
    assert response.status_code == 503
    assert client.get(f"{BASE}/{obj['object_id']}").json()['status'] == 'quarantined'


def test_api_policy_revision_controls_and_local_deletion_scope(env, client):
    obj = upload(env)
    path = f"{BASE}/{obj['object_id']}"
    command = dict(expected_revision=1, command_id='hold-route-001', reason='Fictional reviewed policy')
    held = client.post(path+'/hold', json=command | {'hold':True})
    assert held.status_code == 200 and held.json()['hold'] is True
    assert client.post(path+'/retention', json=command | {'retain_until':(env.now[0]+timedelta(days=12)).isoformat()}).status_code == 409
    assert client.post(path+'/delete-local', json=command | {'expected_revision':2,'command_id':'delete-route-001'}).status_code == 409
    assert client.post(path+'/hold', json=command | {'hold':1}).status_code == 422
