"""Offline fixture-signed protocol tests, not a real IdP/MFA validation."""
import base64
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import hashlib
import sqlite3
from urllib.parse import parse_qs, urlsplit

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import httpx
import jwt
import pytest

from eightball.authorisation import Identity
from eightball.oidc.login import LoginDenied, LoginService, OIDCConfig, TokenEndpoint, digest


@pytest.fixture
def login(tmp_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key().public_bytes(serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    config = OIDCConfig(issuer='https://id.fixture.example', client_id='8ball-browser',
        authorization_endpoint='https://id.fixture.example/authorize',
        token_endpoint='https://id.fixture.example/token',
        redirect_uri='https://testserver/api/v2/identity/callback', signing_keys={'fixture': public})
    service = LoginService(tmp_path/'identity.db', config, None)
    calls = []
    def signed(nonce, **changes):
        now = datetime.now(timezone.utc)
        return jwt.encode(dict(iss=config.issuer, sub='specialist', aud=config.client_id,
            iat=int(now.timestamp()), exp=int((now+timedelta(minutes=20)).timestamp()), nonce=nonce)|changes,
            key, algorithm='RS256', headers={'kid': 'fixture'})
    def start(**changes):
        url, browser = service.begin()
        params = {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}
        def exchange(**request):
            calls.append(request)
            challenge = base64.urlsafe_b64encode(hashlib.sha256(request['verifier'].encode()).digest()).rstrip(b'=').decode()
            assert challenge == params['code_challenge']
            return signed(params['nonce'], **changes)
        service.exchange = exchange
        return dict(state=params['state'], browser=browser, code='fictional-one-use-code', issuer=config.issuer)
    return service, start, signed, calls


def test_code_pkce_nonce_and_opaque_session_survive_restart_then_revoke(login):
    service, start, _, calls = login
    args = start()
    session = service.complete(**args)
    who = Identity(issuer=service.config.issuer, subject='specialist')
    restarted = LoginService(service.path, service.config, service.exchange)
    assert restarted.identity(session) == who
    with sqlite3.connect(service.path) as db:
        assert db.execute('SELECT token_hash FROM agency_browser_session').fetchone()[0] == digest(session)
        assert db.execute('SELECT nonce,verifier,used FROM agency_login_attempt').fetchone() == ('', '', 3)
    with pytest.raises(LoginDenied):
        restarted.complete(**args)
    assert len(calls) == 1
    restarted.revoke_identity(who)
    with pytest.raises(LoginDenied):
        service.identity(session)


@pytest.mark.parametrize('change', [{'nonce': 'wrong'}, {'iss': 'https://other.example'},
    {'aud': 'wrong'}, {'sub': ''}, {'exp': 0}, {'iat': 9999999999}, {'iat': True},
    {'aud': ['8ball-browser', 'other']}, {'azp': 'other'}, {'exp': '9999999999'}])
def test_bad_token_claims_deny_and_consume_attempt(login, change):
    service, start, _, calls = login
    args = start(**change)
    with pytest.raises(LoginDenied):
        service.complete(**args)
    with pytest.raises(LoginDenied):
        service.complete(**args)
    assert len(calls) == 1
    with sqlite3.connect(service.path) as db:
        assert db.execute('SELECT count(*) FROM agency_browser_session').fetchone()[0] == 0


def test_signature_key_id_algorithm_and_acr_are_pinned(login):
    service, start, signed, _ = login
    service.config = replace(service.config, required_acr='urn:fictional:mfa')
    with pytest.raises(LoginDenied):
        service.complete(**start())
    session = service.complete(**start(acr='urn:fictional:mfa', aud=['8ball-browser', 'other'], azp='8ball-browser'))
    assert service.identity(session).subject == 'specialist'
    for token in (jwt.encode({'nonce': 'nonce'}, 'test-only-symmetric-value-not-a-real-secret', algorithm='HS256', headers={'kid':'fixture'}),
                  signed('nonce')[:-4]+'abcd',
                  jwt.encode({'nonce': 'nonce'}, rsa.generate_private_key(public_exponent=65537,key_size=2048),
                             algorithm='RS256', headers={'kid': 'unknown', 'jku': 'https://attacker.example/keys'})):
        with pytest.raises(LoginDenied):
            service.verify(token, nonce='nonce')


def test_wrong_browser_state_or_issuer_never_calls_exchange(login):
    service, start, _, calls = login
    args = start()
    for changes in ({'browser': 'x'*43}, {'state':'x'*43}, {'issuer': 'https://other.example'}, {'code': ''}):
        with pytest.raises(LoginDenied):
            service.complete(**(args|changes))
    assert calls == []
    assert service.identity(service.complete(**args))


def test_cancel_during_exchange_forbids_session_publication(login):
    service, start, _, calls = login
    args = start()
    original = service.exchange
    def cancelled(**request):
        token = original(**request)
        service.cancel(args['browser'])
        return token
    service.exchange = cancelled
    with pytest.raises(LoginDenied):
        service.complete(**args)
    assert len(calls) == 1
    with sqlite3.connect(service.path) as db:
        assert db.execute('SELECT count(*) FROM agency_browser_session').fetchone()[0] == 0


def test_failed_exchange_never_retries_after_restart(login):
    service, start, _, calls = login
    args = start()
    def unavailable(**request):
        calls.append(request)
        raise RuntimeError('private upstream error must not escape')
    service.exchange = unavailable
    with pytest.raises(LoginDenied, match='start a new login'):
        service.complete(**args)
    restarted = LoginService(service.path, service.config, unavailable)
    with pytest.raises(LoginDenied):
        restarted.complete(**args)
    assert len(calls) == 1


def test_expiry_logout_and_cancel_are_durable(login):
    service, start, _, calls = login
    clock = service.clock
    args = start()
    now = service.clock()
    service.clock = lambda: now+301
    with pytest.raises(LoginDenied):
        service.complete(**args)
    assert not calls
    service.clock = clock
    args = start()
    service.cancel(args['browser'])
    with pytest.raises(LoginDenied):
        service.complete(**args)
    session = service.complete(**start())
    service.logout(session)
    service.logout(session)
    with pytest.raises(LoginDenied):
        service.identity(session)
    session = service.complete(**start())
    service.clock = lambda: now+2000
    with pytest.raises(LoginDenied):
        service.identity(session)


def test_session_creation_storage_failure_does_not_publish_or_retry(login):
    service, start, _, calls = login
    args = start()
    with sqlite3.connect(service.path) as db:
        db.execute("CREATE TRIGGER reject_session BEFORE INSERT ON agency_browser_session "
                   "BEGIN SELECT RAISE(ABORT,'fixture storage failure'); END")
    with pytest.raises(sqlite3.IntegrityError):
        service.complete(**args)
    with pytest.raises(LoginDenied):
        service.complete(**args)
    assert len(calls) == 1
    with sqlite3.connect(service.path) as db:
        assert db.execute('SELECT count(*) FROM agency_browser_session').fetchone()[0] == 0


@pytest.mark.parametrize('field,value', [('issuer', 'http://id.example'),
    ('token_endpoint', 'https://user@id.example/token'), ('redirect_uri', 'https://app.example/cb#fragment'),
    ('authorization_endpoint','https://id.example/auth?redirect=bad')])
def test_unsafe_configuration_rejected(login, field, value):
    service, *_ = login
    with pytest.raises(ValueError):
        replace(service.config, **{field: value})


@pytest.mark.parametrize('status,body', [(302, '{}'), (500, 'private error'), (200, 'not json'),
    (200, '{}'), (200, '"not an object"'), (200, '{"id_token": "'+('x'*17000)+'"}'), (200, 'x'*70000)])
def test_controlled_transport_does_not_follow_redirect_retry_or_return_raw_errors(login, status, body):
    service, *_ = login
    calls = []
    def handler(request):
        calls.append(request)
        return httpx.Response(status, content=body, headers={'location':'https://other.example'})
    exchange = TokenEndpoint(service.config, transport=httpx.MockTransport(handler))
    with pytest.raises(LoginDenied):
        exchange(code='fictional', verifier='v'*43)
    assert len(calls) == 1


def test_controlled_transport_uses_exact_pinned_endpoint_and_form(login):
    service, *_ = login
    def handler(request):
        assert str(request.url) == service.config.token_endpoint
        data = parse_qs(request.content.decode())
        assert data == {'code':['fictional'], 'code_verifier':['v'*43],
            'redirect_uri':[service.config.redirect_uri], 'client_id':[service.config.client_id],
            'grant_type':['authorization_code']}
        return httpx.Response(200, json={'id_token': 'fixture-token', 'access_token': 'not-used-or-retained'})
    assert TokenEndpoint(service.config, transport=httpx.MockTransport(handler))(code='fictional', verifier='v'*43) == 'fixture-token'
