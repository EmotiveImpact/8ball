"""Real registerable HTTP routes with fictional, offline signed tokens."""
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlsplit

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.testclient import TestClient
import jwt
import pytest

from eightball.agency_access import AccessRegistry, AgencyAccess
from eightball.authorisation import Grant, Identity, Operation, Resource
from eightball.oidc.login import ATTEMPT_COOKIE, SESSION_COOKIE, LoginService, OIDCConfig
from eightball.v2.identity_api import register_identity_routes


@pytest.fixture
def browser(tmp_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key().public_bytes(serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    config = OIDCConfig(issuer='https://id.fixture.example', client_id='fixture-browser',
        authorization_endpoint='https://id.fixture.example/authorize', token_endpoint='https://id.fixture.example/token',
        redirect_uri='https://testserver/api/v2/identity/callback', signing_keys={'fixture':public})
    login = LoginService(tmp_path/'case.db', config, None)
    registry = AccessRegistry(login.path)
    scope = Resource(organisation_id='tenant-a', matter_id='matter-a')
    who = Identity(issuer=config.issuer, subject='specialist')
    for case, organisation, matter in [('own','tenant-a','matter-a'), ('other-matter','tenant-a','matter-b'),
                                       ('other-tenant','tenant-b','matter-a')]:
        registry.bind_case(case, Resource(organisation_id=organisation, matter_id=matter))
    now = datetime.now(timezone.utc)
    registry.add_grant('grant', Grant(identity=who, resource=scope, operations=frozenset(Operation),
        valid_from=now-timedelta(minutes=1), expires_at=now+timedelta(minutes=20)))
    guard = AgencyAccess(registry, issuer=config.issuer, audience='fixture-api', public_key=public, sessions=login)
    app = FastAPI()
    router = APIRouter(prefix='/api/v2')
    register_identity_routes(router, login)
    app.include_router(router)
    consumed = []

    # Contract harness only: these are not shared app routes or model inference.
    @app.post('/fixture/cases/{case_id}/{operation}')
    def exercise(request: Request, case_id: str, operation: Operation):
        authority = guard.authority(request)
        try:
            with authority.transaction(case_id, (operation,)):
                consumed.append((case_id, operation))
        except PermissionError:
            raise HTTPException(403, 'Access denied') from None
        return {'checked': operation.value, 'model_inference_performed': False}

    client = TestClient(app, base_url='https://testserver')
    origin = {'Origin':config.origin}
    def signin():
        response = client.post('/api/v2/identity/login', headers=origin)
        assert response.status_code == 200
        assert response.headers['cache-control'] == 'no-store'
        assert 'Secure' in response.headers['set-cookie'] and 'HttpOnly' in response.headers['set-cookie']
        assert 'SameSite=lax' in response.headers['set-cookie']
        params = parse_qs(urlsplit(response.json()['authorization_url']).query)
        assert params['code_challenge_method'] == ['S256']
        login.exchange = lambda **_: jwt.encode(dict(iss=config.issuer, sub=who.subject, aud=config.client_id,
            iat=int(now.timestamp()), exp=int((now+timedelta(minutes=10)).timestamp()), nonce=params['nonce'][0]),
            key, algorithm='RS256', headers={'kid':'fixture'})
        callback = {'state':params['state'][0], 'code':'fictional-code', 'iss':config.issuer}
        result = client.get('/api/v2/identity/callback', params=callback, follow_redirects=False)
        assert result.status_code == 303 and result.headers['location'] == '/v2/'
        assert ATTEMPT_COOKIE not in client.cookies
        return client.cookies.get(SESSION_COOKIE)
    return client, login, registry, guard, signin, consumed, origin


def test_login_session_rotation_logout_and_durable_session_revocation(browser):
    client, service, _, _, signin, _, origin = browser
    assert client.get('/api/v2/identity/session').status_code == 401
    old = signin()
    response = client.get('/api/v2/identity/session')
    assert response.status_code == 200 and response.json()['action_approved'] is False
    assert set(response.json()['identity']) == {'issuer','subject'}
    assert response.headers['cache-control'] == 'no-store'
    new = signin()
    assert new != old
    from eightball.oidc.login import LoginDenied
    with pytest.raises(LoginDenied):
        service.identity(old)
    logout = client.post('/api/v2/identity/logout', headers=origin)
    assert logout.json() == {'logged_out':True, 'provider_session_ended':False}
    assert SESSION_COOKIE not in client.cookies
    with pytest.raises(LoginDenied):
        service.identity(new)


@pytest.mark.parametrize('op', list(Operation))
def test_authenticated_http_denial_covers_every_operation_before_consumption(browser, op):
    client, service, registry, _, signin, consumed, origin = browser
    signin()
    path = '/fixture/cases/'
    assert client.post(path+'own/'+op.value, headers=origin).status_code == 200
    assert consumed == [('own', op)]
    for case in ('other-matter','other-tenant','missing'):
        assert client.post(path+case+'/'+op.value, headers=origin).status_code == 403
    assert consumed == [('own', op)]
    AccessRegistry(registry.path).revoke('grant')
    assert client.post(path+'own/'+op.value, headers=origin).status_code == 403
    assert consumed == [('own', op)]
    service.logout(client.cookies.get(SESSION_COOKIE))
    assert client.post(path+'own/'+op.value, headers=origin).status_code == 401


@pytest.mark.parametrize('origin', [None, 'https://attacker.example', 'null'])
def test_cookie_mutations_and_login_require_exact_origin(browser, origin):
    client, _, _, _, signin, consumed, _ = browser
    signin()
    headers = {} if origin is None else {'Origin':origin}
    for path in ('/api/v2/identity/login','/api/v2/identity/logout','/fixture/cases/own/write'):
        assert client.post(path, headers=headers).status_code == 403
    assert not consumed


def test_bad_bearer_does_not_fall_back_to_good_cookie(browser):
    client, _, _, _, signin, consumed, origin = browser
    signin()
    response = client.post('/fixture/cases/own/read', headers=origin|{'Authorization':'Bearer invalid'})
    assert response.status_code == 401 and not consumed


def test_duplicate_callback_parameters_and_provider_error_fail_closed(browser):
    client, service, _, _, _, _, origin = browser
    response = client.post('/api/v2/identity/login', headers=origin)
    params = parse_qs(urlsplit(response.json()['authorization_url']).query)
    service.exchange = lambda **_: pytest.fail('must not exchange malformed callback')
    invalid = [('state',params['state'][0]),('code','first'),('code','second'),('iss',service.config.issuer)]
    response = client.get('/api/v2/identity/callback', params=invalid)
    assert response.status_code == 401 and 'first' not in response.text
    assert SESSION_COOKIE not in client.cookies
    client.post('/api/v2/identity/login', headers=origin)
    response = client.get('/api/v2/identity/callback', params={'error':'access_denied','error_description':'private'})
    assert response.status_code == 401 and 'private' not in response.text
    assert ATTEMPT_COOKIE not in client.cookies
