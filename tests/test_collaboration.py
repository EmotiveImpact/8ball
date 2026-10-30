"""Controlled SQLite adapter tests, not production identity/vault acceptance."""
from datetime import datetime, timedelta, timezone
import json
import sqlite3
from types import SimpleNamespace

import pytest

from eightball.authorisation import Identity, Resource
from eightball.collaboration.contracts import Binding, GrantRequest, SourceVersion, VaultSources
from eightball.collaboration.service import Collaboration
from eightball.projections.service import Projections
from eightball.store import Conflict


AUTHOR = Identity(issuer='https://fictional.invalid', subject='author')
REVIEWER = Identity(issuer=AUTHOR.issuer, subject='reviewer')
EXPERT = Identity(issuer=AUTHOR.issuer, subject='expert')
CLIENT = Identity(issuer=AUTHOR.issuer, subject='client')


class ControlledCases:
    def binding(self, db, case_id, object_id):
        row = db.execute('SELECT * FROM fixture_cases WHERE id=?', (case_id,)).fetchone()
        if row is None:
            raise KeyError('case')
        if object_id is not None and object_id not in ('object-a', 'object-b'):
            raise KeyError('object')
        return Binding(case_id=case_id,
                       resource=Resource(organisation_id=row['tenant'], matter_id=row['matter'], object_id=object_id),
                       case_revision=row['revision'], object_revision=row['object_revision'],
                       sources=(SourceVersion(object_id='opaque-source', version=1, vault_revision=row['vault_revision'],
                                              sha256='a'*64),) if object_id else ())

    def expert_view(self, db, binding):
        return {'id': binding.resource.object_id, 'internal_note': 'Fictional deliberation',
                'source_text': 'Fictional unreleased source quotation'}


class ControlledPolicy:
    def require(self, db, identity, binding, capability):
        if not db.in_transaction:
            raise AssertionError('Authority check must be inside the transaction')
        row = db.execute('SELECT capabilities FROM fixture_members WHERE identity=? AND tenant=?',
                         (identity.model_dump_json(), binding.resource.organisation_id)).fetchone()
        if row is None or capability not in json.loads(row[0]):
            raise PermissionError('No current role')


class ControlledSources:
    def require_current(self, db, binding, *, identity):
        if binding.sources and db.execute('SELECT ready FROM fixture_cases WHERE id=?', (binding.case_id,)).fetchone()[0] != 1:
            raise PermissionError('Source no longer released')


def make_environment(tmp_path):
    path = tmp_path / 'collaboration.sqlite'
    with sqlite3.connect(path) as db:
        db.executescript('''
            CREATE TABLE fixture_cases (id TEXT PRIMARY KEY, tenant TEXT, matter TEXT,
                revision INTEGER, object_revision INTEGER, vault_revision INTEGER, ready INTEGER);
            CREATE TABLE fixture_members (identity TEXT, tenant TEXT, capabilities TEXT,
                PRIMARY KEY(identity,tenant));
        ''')
        db.executemany('INSERT INTO fixture_cases VALUES (?,?,?,?,?,?,?)',
                       [('case-a', 'tenant-a', 'matter-a', 7, 3, 1, 1),
                        ('case-b', 'tenant-a', 'matter-b', 7, 3, 1, 1),
                        ('case-c', 'tenant-b', 'matter-a', 7, 3, 1, 1)])
        for identity, capabilities in (
                (AUTHOR, ['collaboration.manage', 'projection.draft', 'projection.inspect', 'projection.withdraw']),
                (REVIEWER, ['projection.review', 'projection.inspect']),
                (EXPERT, ['collaboration.expert']), (CLIENT, ['projection.client'])):
            db.execute('INSERT INTO fixture_members VALUES (?,?,?)',
                       (identity.model_dump_json(), 'tenant-a', json.dumps(capabilities)))
    clock = [datetime(2026, 10, 25, 12, tzinfo=timezone.utc)]
    host = Collaboration(path, policy=ControlledPolicy(), cases=ControlledCases(), sources=ControlledSources(), clock=lambda: clock[0])
    host.initialize()
    return SimpleNamespace(path=path, host=host, projections=Projections(host), clock=clock)


@pytest.fixture
def env(tmp_path):
    return make_environment(tmp_path)


def grant_request(env, **updates):
    return GrantRequest.model_validate(dict(id='expert-grant', recipient=EXPERT, purpose='expert', object_id='object-a',
                                           valid_from=env.clock[0], expires_at=env.clock[0]+timedelta(hours=1),
                                           rationale='Fictional specialist engagement') | updates)


def grant(env, **updates):
    return env.host.create_grant(actor=AUTHOR, case_id='case-a', request=grant_request(env, **updates))


def read(env, **updates):
    return env.host.expert_read(**(dict(actor=EXPERT, case_id='case-a', object_id='object-a', grant_id='expert-grant') | updates))


def test_construction_requires_adapters_and_does_not_migrate(tmp_path):
    path = tmp_path / 'untouched.sqlite'
    Collaboration(path, policy=ControlledPolicy(), cases=ControlledCases(), sources=ControlledSources())
    assert not path.exists()
    with pytest.raises(ValueError):
        Collaboration(path, policy=None, cases=ControlledCases(), sources=ControlledSources())


def test_administrator_can_revoke_after_object_is_removed(env):
    grant(env)
    original = env.host.cases
    class RemovedObject:
        def binding(self, db, case_id, object_id):
            if object_id:
                raise KeyError('Removed object')
            return original.binding(db, case_id, object_id)
    env.host.cases = RemovedObject()
    assert env.host.revoke_grant(actor=AUTHOR, case_id='case-a', grant_id='expert-grant')['revoked']


def test_expert_matter_grant_never_turns_into_whole_case_export(env):
    grant(env, object_id=None)
    with pytest.raises(PermissionError):
        read(env, object_id=None)


def test_vault_gate_uses_same_transaction_and_exact_version_scope(env):
    with pytest.raises(ValueError):
        VaultSources(object())
    calls = []
    class Gate:
        def require_source(self, db, **request):
            assert db.in_transaction
            calls.append(request)
            return dict(schema_version=1, object_id=request['object_id'], version=1, vault_revision=request['expected_revision'],
                        sha256=request['expected_sha256'], case_id=request['case_id'], organisation_id='tenant-a', matter_id='matter-a')
    gate = Gate()
    sources = VaultSources(gate)
    with env.host.transaction() as db:
        binding = env.host.binding(db, 'case-a', 'object-a')
        sources.require_current(db, binding, identity=AUTHOR)
        assert calls[-1] == dict(identity=AUTHOR, case_id='case-a', object_id='opaque-source', expected_revision=1, expected_sha256='a'*64)
    with sqlite3.connect(env.path) as db:
        with pytest.raises(PermissionError):
            sources.require_current(db, binding, identity=AUTHOR)
    original = gate.require_source
    for field, value in (('organisation_id', 'other'), ('matter_id', 'other'), ('case_id', 'other'), ('version', 2), ('sha256', 'b'*64), ('schema_version', True), ('schema_version', 2)):
        gate.require_source = lambda db, field=field, value=value, **kwargs: original(db, **kwargs) | {field: value}
        with env.host.transaction() as db, pytest.raises(PermissionError):
            sources.require_current(db, binding, identity=AUTHOR)


def test_object_grant_is_narrow_and_requires_current_role(env):
    grant(env)
    assert read(env)['object']['id'] == 'object-a'
    for args in ({'object_id': 'object-b'}, {'case_id': 'case-b'}, {'case_id': 'case-c'}, {'actor': CLIENT},
                 {'actor': Identity(issuer='https://different.invalid', subject=EXPERT.subject)}):
        with pytest.raises((PermissionError, KeyError)):
            read(env, **args)
    with sqlite3.connect(env.path) as db:
        db.execute('DELETE FROM fixture_members WHERE identity=?', (EXPERT.model_dump_json(),))
    with pytest.raises(PermissionError):
        read(env)


def test_matter_expert_grant_allows_objects_not_other_matters(env):
    grant(env, object_id=None)
    assert read(env, object_id='object-b')['action_permission'] is False
    with pytest.raises((PermissionError, KeyError)):
        read(env, case_id='case-b')


def test_revocation_survives_restart_is_idempotent_never_revives(env):
    request = grant_request(env)
    first = grant(env)
    assert grant(env) == first
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT COUNT(*) FROM collaboration_audit').fetchone()[0] == 1
    assert env.host.revoke_grant(actor=AUTHOR, case_id='case-a', grant_id=request.id)['revoked']
    assert env.host.revoke_grant(actor=AUTHOR, case_id='case-a', grant_id=request.id)['revoked']
    restarted = Collaboration(env.path, policy=env.host.policy, cases=env.host.cases, sources=env.host.sources, clock=env.host.clock)
    restarted.initialize()
    env.host = restarted
    with pytest.raises(PermissionError):
        read(env)
    with pytest.raises(Conflict):
        grant(env)
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT COUNT(*) FROM collaboration_audit').fetchone()[0] == 2


def test_id_collision_or_unauthorised_management_cannot_replace_grant(env):
    grant(env)
    with pytest.raises(Conflict):
        grant(env, object_id='object-b')
    with pytest.raises(PermissionError):
        env.host.revoke_grant(actor=EXPERT, case_id='case-a', grant_id='expert-grant')
    with pytest.raises(PermissionError):
        env.host.grants(actor=CLIENT, case_id='case-a')
    assert env.host.grants(actor=AUTHOR, case_id='case-a')[0]['revoked'] is False


@pytest.mark.parametrize('offset', [-1, 60])
def test_grant_time_window(env, offset):
    grant(env)
    env.clock[0] += timedelta(minutes=offset)
    with pytest.raises(PermissionError):
        read(env)


def test_clock_and_source_lifecycle_fail_closed(env):
    grant(env)
    env.clock[0] = env.clock[0].replace(tzinfo=None)
    with pytest.raises(PermissionError):
        read(env)
    env.clock[0] = env.clock[0].replace(tzinfo=timezone.utc)
    with sqlite3.connect(env.path) as db:
        db.execute("UPDATE fixture_cases SET ready=0 WHERE id='case-a'")
    with pytest.raises(PermissionError):
        read(env)


def test_audit_failure_rolls_back_grant_and_revoke(env):
    with sqlite3.connect(env.path) as db:
        db.execute("CREATE TRIGGER fail_audit BEFORE INSERT ON collaboration_audit BEGIN SELECT RAISE(ABORT,'test failure'); END")
    with pytest.raises(sqlite3.IntegrityError):
        grant(env)
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT COUNT(*) FROM collaboration_grants').fetchone()[0] == 0
        db.execute('DROP TRIGGER fail_audit')
    grant(env)
    with sqlite3.connect(env.path) as db:
        db.execute("CREATE TRIGGER fail_audit BEFORE INSERT ON collaboration_audit BEGIN SELECT RAISE(ABORT,'test failure'); END")
    with pytest.raises(sqlite3.IntegrityError):
        env.host.revoke_grant(actor=AUTHOR, case_id='case-a', grant_id='expert-grant')
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT revoked FROM collaboration_grants').fetchone()[0] == 0


def test_expiry_before_publication_rolls_back_read_receipt(env):
    grant(env)
    original = env.host.cases.expert_view
    def expiring(db, binding):
        env.clock[0] += timedelta(hours=1)
        return original(db, binding)
    env.host.cases.expert_view = expiring
    with pytest.raises(PermissionError):
        read(env)
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT COUNT(*) FROM collaboration_audit').fetchone()[0] == 1


def test_corrupt_grant_and_misbound_adapter_fail_closed(env):
    grant(env)
    with sqlite3.connect(env.path) as db:
        db.execute("UPDATE collaboration_grants SET digest='bad'")
    with pytest.raises(Conflict):
        read(env)
    original = env.host.cases.binding
    def misbound(db, case_id, object_id):
        return original(db, 'case-b', object_id)
    env.host.cases.binding = misbound
    with pytest.raises(PermissionError):
        read(env)
