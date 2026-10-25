"""In-process fixture authentication only; not browser/OIDC acceptance."""
import pytest
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.testclient import TestClient

from eightball.v2.collaboration_api import register_collaboration_routes
from eightball.v2.request_limits import BoundedRequestBody
from test_collaboration import AUTHOR, REVIEWER, CLIENT, EXPERT, env
from test_projection import draft, client_grant


def fixture_app(env):
    app = FastAPI()
    app.add_middleware(BoundedRequestBody)
    def controlled_identity(request: Request):
        # Explicit test identity injection; no bearer validation claim.
        identity = {'author': AUTHOR, 'reviewer': REVIEWER, 'client': CLIENT, 'expert': EXPERT}.get(request.headers.get('x-fixture-actor'))
        if identity:
            request.state.agency_identity = identity
    router = APIRouter(prefix='/api/v2', dependencies=[Depends(controlled_identity)])
    register_collaboration_routes(router, env.host, env.projections)
    app.include_router(router)
    return app


@pytest.fixture
def client(env):
    return TestClient(fixture_app(env))


BASE = '/api/v2/cases/case-a/collaboration'
PROJECTION = BASE + '/objects/object-a/projections/projection-a'


def test_local_bearer_is_not_agency_identity(client):
    response = client.get(BASE + '/grants', headers={'Authorization': 'Bearer local-fictional-token'})
    assert response.status_code == 401
    assert response.headers['cache-control'] == 'no-store'


def test_route_client_cannot_read_internal_review_or_grants(client, env):
    draft(env)
    for path in (BASE + '/grants', PROJECTION+'/review', PROJECTION):
        response = client.get(path, headers={'x-fixture-actor': 'client'})
        assert response.status_code == 403
        assert 'internal_note' not in response.text


def test_review_api_exact_digest_client_allowlist_and_revoke(client, env):
    record = draft(env)
    client_grant(env)
    review = dict(expected_digest=record['digest'], grant_id='client-grant', rationale='Reviewed fictional disclosure content')
    assert client.post(PROJECTION+'/review', json=review, headers={'x-fixture-actor': 'reviewer'}).status_code == 200
    response = client.get(PROJECTION, headers={'x-fixture-actor': 'client'})
    assert response.status_code == 200
    assert response.headers['cache-control'] == 'no-store, private'
    assert set(response.json()) == {'id', 'content', 'reviewed_at', 'action_permission', 'external_send'}
    assert client.post(BASE+'/grants/client-grant/revoke', json={}, headers={'x-fixture-actor': 'author'}).json()['revoked']
    assert client.get(PROJECTION, headers={'x-fixture-actor': 'client'}).status_code == 403


def test_api_stale_revision_and_wrong_object_do_not_publish(client, env):
    record = draft(env)
    client_grant(env)
    response = client.post(PROJECTION+'/review', json=dict(expected_digest='0'*64, grant_id='client-grant', rationale='Wrong exact content hash'), headers={'x-fixture-actor':'reviewer'})
    assert response.status_code == 409
    assert response.headers['cache-control'] == 'no-store'
    assert client.get(PROJECTION.replace('object-a','object-b')+'/review', headers={'x-fixture-actor':'reviewer'}).status_code == 403
    assert client.get(PROJECTION, headers={'x-fixture-actor':'client'}).status_code == 403


def test_api_rejects_identity_forgery_and_oversized_request(client):
    forged = dict(expected_digest='0'*64, grant_id='client-grant', rationale='Fictional rationale', reviewer=REVIEWER.model_dump(mode='json'))
    response = client.post(PROJECTION+'/review', json=forged, headers={'x-fixture-actor':'client'})
    assert response.status_code == 422
    response = client.post(PROJECTION+'/review', content=b'x'*300001, headers={'x-fixture-actor':'reviewer','content-type':'application/json'})
    assert response.status_code == 413


def test_api_route_paths_do_not_register_global_or_default_case_views(client):
    assert client.get('/api/v2/cases/case-a', headers={'x-fixture-actor':'client'}).status_code == 404
    assert client.get('/api/v2/collaboration', headers={'x-fixture-actor':'client'}).status_code == 404


def test_public_reads_do_not_enumerate_missing_or_foreign_records(client, env):
    draft(env)
    headers = {'x-fixture-actor': 'client'}
    responses = [client.get(path, headers=headers) for path in (
        PROJECTION, PROJECTION.replace('projection-a', 'absent'),
        PROJECTION.replace('case-a','case-b'), PROJECTION.replace('case-a','case-c'),
        PROJECTION.replace('object-a','object-b'), PROJECTION.replace('object-a','absent'),
        PROJECTION.replace('case-a','absent'))]
    assert {response.status_code for response in responses} == {403}
    assert len({response.text for response in responses}) == 1
    expert = BASE + '/objects/object-a/expert/'
    responses = [client.get(expert+grant, headers={'x-fixture-actor':'expert'}) for grant in ('absent', 'another')]
    assert {response.status_code for response in responses} == {403}
