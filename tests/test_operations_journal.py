"""Fictional transaction-adapter tests, not managed identity/revocation evidence."""
from datetime import datetime, timedelta, timezone
import json
import sqlite3

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.testclient import TestClient
import pytest

from eightball.authorisation import Identity
from eightball.operations.api import register_operations_routes
from eightball.operations.contracts import OpenRecord, Scope, SURFACES, Transition, VerifyRevocation
from eightball.operations.journal import (Operations, OperationsConflict, OperationsUnavailable,
                                          initialize)

NOW = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)
SCOPE = Scope(organisation_id='fictional-org', matter_id='fictional-matter', case_id='fictional-case')
IDENTITY = Identity(issuer='https://fictional.invalid', subject='operator')
EVIDENCE = 'a' * 64


def authorize(db, identity, scope, operation, now):
    row = db.execute('''SELECT expires,revoked FROM fixture_grants WHERE issuer=? AND subject=?
        AND organisation_id=? AND matter_id=? AND case_id=?''',
        (identity.issuer, identity.subject, *Operations._scope(scope))).fetchone()
    return bool(row and not row['revoked'] and now < datetime.fromisoformat(row['expires']))


@pytest.fixture
def service(tmp_path):
    path = tmp_path / 'fictional.sqlite'
    initialize(path)
    with sqlite3.connect(path) as db:
        db.execute('''CREATE TABLE fixture_grants (issuer TEXT, subject TEXT, organisation_id TEXT,
            matter_id TEXT, case_id TEXT, expires TEXT, revoked INTEGER)''')
        db.execute('INSERT INTO fixture_grants VALUES (?,?,?,?,?,?,0)',
                   (IDENTITY.issuer, IDENTITY.subject, *Operations._scope(SCOPE),
                    (NOW + timedelta(hours=1)).isoformat()))
    return Operations(path, authority=authorize, clock=lambda: NOW)


def opened(service, *, kind='incident', request_id='fictional-request'):
    return service.open(IDENTITY, SCOPE, OpenRecord(request_id=request_id, kind=kind,
                        severity='critical', category='confidentiality',
                        target_id='fictional-grant' if kind == 'revocation' else None))


def transition(service, record, state, *, evidence=EVIDENCE, request_id=None):
    return service.transition(IDENTITY, SCOPE, record['id'],
                              Transition(request_id=request_id or f'fictional-{state}',
                                         expected_revision=record['revision'], state=state,
                                         evidence_sha256=evidence))


@pytest.mark.parametrize('field,value', [('organisation_id', 'other-org'), ('matter_id', 'other-matter'),
                                        ('case_id', 'other-case')])
def test_cross_tenant_matter_case_denies_before_record_lookup(service, field, value):
    record = opened(service)
    scope = SCOPE.model_copy(update={field: value})
    with pytest.raises(PermissionError):
        service.view(IDENTITY, scope)
    with pytest.raises(PermissionError):
        service.transition(IDENTITY, scope, record['id'], Transition(
            request_id='fictional-other', expected_revision=0, state='investigating'))


@pytest.mark.parametrize('identity', [None, 'local-operator',
    Identity(issuer='https://other.invalid', subject='operator'),
    Identity(issuer=IDENTITY.issuer, subject='other')])
def test_unknown_or_unverified_identity_denies(service, identity):
    with pytest.raises(PermissionError):
        service.view(identity, SCOPE)


@pytest.mark.parametrize('mode', ['revoked', 'expired'])
def test_current_revocation_and_expiry_deny_even_idempotent_replay(service, mode):
    opened(service)
    with sqlite3.connect(service.path) as db:
        db.execute('UPDATE fixture_grants SET ' + ('revoked=1' if mode == 'revoked' else 'expires=?'),
                   () if mode == 'revoked' else (NOW.isoformat(),))
    with pytest.raises(PermissionError):
        opened(service)
    with pytest.raises(PermissionError):
        service.view(IDENTITY, SCOPE)


def test_idempotency_restart_and_conflict(service):
    record = opened(service)
    restarted = Operations(service.path, authority=authorize, clock=lambda: NOW)
    assert opened(restarted) == record
    assert restarted.view(IDENTITY, SCOPE)['sequence'] == 1
    with pytest.raises(OperationsConflict, match='different content'):
        opened(restarted, kind='pilot_finding')


def test_stale_revision_and_cancellation_are_terminal(service):
    record = opened(service)
    investigating = transition(service, record, 'investigating')
    with pytest.raises(OperationsConflict, match='stale'):
        transition(service, record, 'cancelled')
    cancelled = transition(service, investigating, 'cancelled')
    assert cancelled['state'] == 'cancelled'
    assert transition(service, investigating, 'cancelled') == cancelled
    with pytest.raises(OperationsConflict):
        transition(service, cancelled, 'contained')


def test_incident_requires_mitigation_evidence_and_ordered_close(service):
    record = opened(service)
    with pytest.raises(OperationsConflict):
        transition(service, record, 'closed')
    record = transition(service, record, 'investigating')
    with pytest.raises(OperationsConflict, match='evidence'):
        transition(service, record, 'contained', evidence=None)
    for state in ('contained', 'resolved', 'closed'):
        record = transition(service, record, state)
    view = service.view(IDENTITY, SCOPE)
    assert record['state'] == 'closed' and view['sequence'] == 5
    assert not view['production_accepted'] and not view['action_permission']


@pytest.mark.parametrize('surface', SURFACES)
@pytest.mark.parametrize('bad', ['unavailable', 'access_still_allowed'])
def test_revocation_cannot_close_with_any_unknown_or_permitted_surface(service, surface, bad):
    service.probe = lambda db, scope, target, name: bad if name == surface else 'denied'
    record = opened(service, kind='revocation')
    for state in ('investigating', 'contained', 'resolved'):
        record = transition(service, record, state)
    with pytest.raises(OperationsConflict, match='not established'):
        transition(service, record, 'closed')
    assert service.view(IDENTITY, SCOPE)['sequence'] == 4


def test_missing_probes_unknown_and_rechecking_at_close(service):
    record = opened(service, kind='revocation')
    record = service.verify_revocation(IDENTITY, SCOPE, record['id'],
        VerifyRevocation(request_id='fictional-probe', expected_revision=0))
    assert set(record['checks'].values()) == {'unavailable'}
    service.probe = lambda *args: 'denied'
    for state in ('investigating', 'contained', 'resolved'):
        record = transition(service, record, state)
    service.probe = lambda *args: 'access_still_allowed'
    with pytest.raises(OperationsConflict):
        transition(service, record, 'closed')
    service.probe = lambda *args: 'denied'
    assert transition(service, record, 'closed')['state'] == 'closed'


def test_adapter_failure_rolls_back_and_does_not_expose_private_detail(service, caplog):
    record = opened(service, kind='revocation')
    def probe(db, *args):
        db.execute("UPDATE fixture_grants SET revoked=1")
        raise RuntimeError('fictional-secret-source-text')
    service.probe = probe
    with pytest.raises(OperationsUnavailable) as error:
        service.verify_revocation(IDENTITY, SCOPE, record['id'],
            VerifyRevocation(request_id='fictional-failure', expected_revision=0))
    assert 'fictional-secret' not in str(error.value) + caplog.text
    assert service.view(IDENTITY, SCOPE)['sequence'] == 1


def test_authority_rechecked_after_adapter_and_transaction_rolls_back(service):
    record = opened(service, kind='revocation')
    def revoke(db, *args):
        db.execute('UPDATE fixture_grants SET revoked=1')
        return 'denied'
    service.probe = revoke
    with pytest.raises(PermissionError):
        service.verify_revocation(IDENTITY, SCOPE, record['id'],
            VerifyRevocation(request_id='fictional-revoke-mid', expected_revision=0))
    assert service.view(IDENTITY, SCOPE)['sequence'] == 1


@pytest.mark.parametrize('table', ['ops_records', 'ops_journal', 'ops_requests'])
def test_tampered_snapshot_chain_or_cached_receipt_fails_visible(service, table):
    opened(service)
    with sqlite3.connect(service.path) as db:
        column = 'response' if table == 'ops_requests' else 'body'
        db.execute(f'UPDATE {table} SET {column}=?', ('{}',))
    with pytest.raises(OperationsConflict):
        opened(service)


def client(service, *, authenticated=True):
    app = FastAPI()
    def identity(request: Request):
        if authenticated:
            request.state.agency_identity = IDENTITY
    router = APIRouter(prefix='/api/v2', dependencies=[Depends(identity)])
    register_operations_routes(router, service)
    app.include_router(router)
    return TestClient(app)


URL = '/api/v2/organisations/fictional-org/matters/fictional-matter/cases/fictional-case/operations'


def test_routes_require_host_identity_and_enforce_scope(service):
    assert client(service, authenticated=False).get(URL).status_code == 403
    c = client(service)
    body = OpenRecord(request_id='fictional-http', kind='incident', severity='high', category='safety').model_dump()
    created = c.post(URL, json=body)
    assert created.status_code == 200
    assert c.get(URL.replace('fictional-matter', 'other')).status_code == 403
    assert c.post(URL + '/' + created.json()['id'] + '/transition', json={
        'request_id': 'fictional-transition', 'expected_revision': 99,
        'state': 'investigating'}).status_code == 409
    assert c.get(URL).json()['sequence'] == 1
    assert c.post(URL, json={**body, 'raw_source': 'do-not-store'}).status_code == 422


def test_probe_exception_api_is_sanitized(service):
    record = opened(service, kind='revocation')
    def fail(*args):
        raise ValueError('fictional-secret-token')
    service.probe = fail
    response = client(service).post(URL + '/' + record['id'] + '/verify-revocation', json={
        'request_id': 'fictional-probe-http', 'expected_revision': 0})
    assert response.status_code == 503 and 'fictional-secret' not in response.text
