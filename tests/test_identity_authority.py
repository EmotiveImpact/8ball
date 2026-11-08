"""Controlled same-database authority seam; no production row-policy claim."""
from datetime import datetime, timedelta, timezone
import sqlite3

import pytest

from eightball.agency_access import AccessRegistry, CurrentAuthority
from eightball.authorisation import Grant, Identity, Operation, Resource


@pytest.fixture
def policy(tmp_path):
    registry = AccessRegistry(tmp_path/'case.db')
    who = Identity(issuer='https://fixture.example', subject='specialist')
    scope = Resource(organisation_id='tenant-a', matter_id='matter-a')
    registry.bind_case('case-a', scope)
    registry.bind_case('case-other-matter', Resource(organisation_id='tenant-a', matter_id='matter-b'))
    registry.bind_case('case-other-tenant', Resource(organisation_id='tenant-b', matter_id='matter-a'))
    now = datetime.now(timezone.utc)
    def add(name='grant', resource=scope, operations=frozenset(Operation)):
        registry.add_grant(name, Grant(identity=who, resource=resource, operations=operations,
            valid_from=now-timedelta(minutes=1), expires_at=now+timedelta(minutes=10)))
    with sqlite3.connect(registry.path) as db:
        db.execute('CREATE TABLE fixture_case (id TEXT PRIMARY KEY, revision INTEGER NOT NULL)')
        db.execute('INSERT INTO fixture_case VALUES (?,?)', ('case-a', 0))
    return registry, who, scope, add


@pytest.mark.parametrize('op', list(Operation))
def test_every_operation_denies_cross_tenant_matter_identity_and_revocation(policy, op):
    registry, who, scope, add = policy
    add()
    assert registry.require(who, 'case-a', (op,)) == scope
    for case in ('case-other-matter', 'case-other-tenant', 'missing', "case-a' OR 1=1 --"):
        with pytest.raises(PermissionError):
            registry.require(who, case, (op,))
    for identity in (who.model_copy(update={'subject': 'other'}),
                     who.model_copy(update={'issuer': 'https://other.example'})):
        with pytest.raises(PermissionError):
            registry.require(identity, 'case-a', (op,))
    AccessRegistry(registry.path).revoke('grant')
    with pytest.raises(PermissionError):
        registry.require(who, 'case-a', (op,))


@pytest.mark.parametrize('op', list(Operation))
def test_object_grant_never_expands_to_aggregate_or_another_object(policy, op):
    registry, who, scope, add = policy
    add(resource=scope.model_copy(update={'object_id': 'source-a'}))
    assert registry.require(who, 'case-a', (op,), object_ids=('source-a',)) == scope
    for objects in ((), ('source-b',), ('source-a', 'source-b')):
        with pytest.raises(PermissionError):
            registry.require(who, 'case-a', (op,), object_ids=objects)


def test_all_operations_required_not_any(policy):
    registry, who, _, add = policy
    add(operations=frozenset({Operation.READ}))
    with pytest.raises(PermissionError):
        registry.require(who, 'case-a', (Operation.READ, Operation.INFER))


@pytest.mark.parametrize('ops,objects', [((), ()), (('read',), ()), ((Operation.READ,), ('',)),
                                       ((Operation.READ,), ['source-a'])])
def test_malformed_authority_denies(policy, ops, objects):
    registry, who, _, add = policy
    add()
    with pytest.raises(PermissionError):
        registry.require(who, 'case-a', ops, object_ids=objects)


def test_transaction_requires_same_database_and_active_transaction(policy, tmp_path):
    registry, who, _, add = policy
    add()
    for path in (registry.path, tmp_path/'wrong.db'):
        with sqlite3.connect(path) as db:
            with pytest.raises(PermissionError):
                registry.require(who, 'case-a', (Operation.READ,), db=db)
            if str(path) != registry.path:
                db.execute('BEGIN IMMEDIATE')
                with pytest.raises(PermissionError):
                    registry.require(who, 'case-a', (Operation.READ,), db=db)


def test_commit_rollback_stale_revision_and_grant_failure_are_atomic(policy):
    registry, who, _, add = policy
    add()
    def change(expected, fail=False):
        with registry.transaction(who, 'case-a', (Operation.WRITE,)) as (db, _):
            if db.execute('SELECT revision FROM fixture_case WHERE id=?', ('case-a',)).fetchone()[0] != expected:
                raise ValueError('stale revision')
            db.execute('UPDATE fixture_case SET revision=revision+1 WHERE id=?', ('case-a',))
            if fail:
                raise RuntimeError('storage operation failed')
    with pytest.raises(RuntimeError):
        change(0, fail=True)
    change(0)
    with pytest.raises(ValueError):
        change(0)
    registry.revoke('grant')
    with pytest.raises(PermissionError):
        change(1)
    with sqlite3.connect(registry.path) as db:
        assert db.execute('SELECT revision FROM fixture_case').fetchone()[0] == 1


def test_reauthentication_after_work_rolls_back_expired_session(policy):
    registry, who, _, add = policy
    add()
    active = True
    def current():
        if not active:
            raise PermissionError('session expired')
        return who
    authority = CurrentAuthority(registry, current)
    with pytest.raises(PermissionError):
        with authority.transaction('case-a', (Operation.WRITE,)) as (db, _):
            db.execute('UPDATE fixture_case SET revision=1')
            active = False
    with sqlite3.connect(registry.path) as db:
        assert db.execute('SELECT revision FROM fixture_case').fetchone()[0] == 0


def test_preflight_is_not_a_cached_capability_and_corrupt_grants_fail_closed(policy):
    registry, who, _, add = policy
    add()
    authority = CurrentAuthority(registry, lambda: who)
    authority.require('case-a', (Operation.INFER,))
    registry.revoke('grant')
    with pytest.raises(PermissionError):
        authority.require('case-a', (Operation.INFER,))
    with sqlite3.connect(registry.path) as db:
        db.execute("INSERT INTO agency_grants VALUES ('corrupt','{}',0)")
    assert not registry.allowed(who, 'case-a', Operation.READ)


def test_stale_wal_transaction_cannot_read_pre_revocation_grants(policy):
    registry, who, _, add = policy
    add()
    with sqlite3.connect(registry.path) as db:
        db.execute('PRAGMA journal_mode=WAL')
    with sqlite3.connect(registry.path) as stale:
        stale.execute('BEGIN')
        assert stale.execute('SELECT count(*) FROM agency_grants WHERE revoked=0').fetchone()[0] == 1
        registry.revoke('grant')
        with pytest.raises(PermissionError, match='Current authority transaction'):
            registry.require(who, 'case-a', (Operation.READ,), db=stale)


def test_identity_change_between_authentication_and_lock_denies(policy):
    registry, who, _, add = policy
    add()
    calls = iter((who, who.model_copy(update={'subject':'other'})))
    authority = CurrentAuthority(registry, lambda: next(calls, who))
    with pytest.raises(PermissionError, match='identity changed'):
        authority.require('case-a', (Operation.READ,))


def test_identity_change_during_transaction_denies_even_if_both_have_grants(policy):
    registry, who, scope, add = policy
    add()
    other = who.model_copy(update={'subject': 'another-specialist'})
    now = datetime.now(timezone.utc)
    registry.add_grant('other-grant', Grant(identity=other, resource=scope,
        operations=frozenset(Operation), valid_from=now-timedelta(minutes=1),
        expires_at=now+timedelta(minutes=10)))
    active = who
    authority = CurrentAuthority(registry, lambda: active)
    with pytest.raises(PermissionError, match='identity changed'):
        with authority.transaction('case-a', (Operation.WRITE,)) as (db, _):
            db.execute('UPDATE fixture_case SET revision=1')
            active = other
    with sqlite3.connect(registry.path) as db:
        assert db.execute('SELECT revision FROM fixture_case').fetchone()[0] == 0


def test_identity_change_before_transaction_yield_never_consumes_work(policy):
    registry, who, scope, add = policy
    add()
    other = who.model_copy(update={'subject': 'another-specialist'})
    now = datetime.now(timezone.utc)
    registry.add_grant('other-grant', Grant(identity=other, resource=scope,
        operations=frozenset(Operation), valid_from=now-timedelta(minutes=1),
        expires_at=now+timedelta(minutes=10)))
    calls = iter((who, other, other, other))
    authority = CurrentAuthority(registry, lambda: next(calls))
    with pytest.raises(PermissionError, match='identity changed'):
        with authority.transaction('case-a', (Operation.READ,)):
            pytest.fail('No work may be consumed')
