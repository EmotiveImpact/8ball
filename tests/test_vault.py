"""Fictional vault component/security tests; scanner doubles are not malware evidence."""
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
import sqlite3
from types import SimpleNamespace
from uuid import uuid4

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import pytest

from eightball.agency_access import AccessRegistry
from eightball.authorisation import Grant, Identity, Operation, Resource
from eightball.vault.authority import RegistryAuthority
from eightball.vault.contracts import Conflict, IntegrityError, ScanResult, Unavailable, VaultPermission
from eightball.vault.crypto import LocalKeyWrapper
from eightball.vault.service import Vault
from eightball.vault.sources import exact_text


class SyntheticScanner:
    def __init__(self, verdict='clean'):
        self.verdict, self.calls = verdict, 0

    def scan(self, content, *, sha256, media_type):
        self.calls += 1
        assert media_type in {'text/plain', 'text/markdown'}
        return ScanResult(self.verdict, 'fixture-only', 'synthetic-1', 'not-real-definitions', sha256)


@pytest.fixture
def env(tmp_path):
    path = tmp_path / 'fictional.sqlite3'
    registry = AccessRegistry(path)
    identity = Identity(issuer='https://fictional.invalid', subject='operator')
    scope = Resource(organisation_id='org-1', matter_id='matter-1')
    now = [datetime(2026, 10, 25, tzinfo=timezone.utc)]
    registry.bind_case('case-1', scope)
    registry.bind_case('case-2', Resource(organisation_id='org-1', matter_id='matter-2'))
    registry.bind_case('case-3', Resource(organisation_id='org-2', matter_id='matter-1'))
    registry.add_grant('grant-1', Grant(identity=identity, resource=scope,
                       operations=frozenset(Operation), valid_from=now[0]-timedelta(days=1),
                       expires_at=now[0]+timedelta(days=60)))
    keys = LocalKeyWrapper({'fictional-key': AESGCM.generate_key(bit_length=256)}, active_key_id='fictional-key')
    scanner = SyntheticScanner()
    vault = Vault(path, authority=RegistryAuthority(control=lambda *args: True), keys=keys,
                  scanner=scanner, clock=lambda: now[0], deletion_guard=lambda db, handle: True)
    return SimpleNamespace(vault=vault, identity=identity, registry=registry, now=now, keys=keys,
                           path=path, scanner=scanner)


def upload(env, content=b'Fictional original\r\nnot a verified fact.\n', **kwargs):
    return env.vault.upload(identity=env.identity, case_id='case-1', content=content,
                            filename='fictional.txt', media_type='text/plain',
                            retain_until=env.now[0]+timedelta(days=8), command_id=kwargs.pop('command_id', uuid4().hex),
                            **kwargs)


def scan(env, obj, **kwargs):
    return env.vault.scan(identity=env.identity, case_id='case-1', object_id=obj['object_id'],
                          expected_revision=obj['vault_revision'], command_id=kwargs.pop('command_id', uuid4().hex), **kwargs)


def read(env, obj, **kwargs):
    return env.vault.read_original(**(dict(identity=env.identity, case_id='case-1', object_id=obj['object_id'],
                                         expected_revision=obj['vault_revision'], expected_sha256=obj['sha256']) | kwargs))


def control(env, obj, action='set_hold', **kwargs):
    return getattr(env.vault, action)(identity=env.identity, case_id='case-1', object_id=obj['object_id'],
                                      expected_revision=obj['vault_revision'], command_id=kwargs.pop('command_id', uuid4().hex),
                                      reason='Explicit fictional operator policy', **kwargs)


def test_quarantine_exact_original_encryption_and_provenance(env):
    content = '\ufeffFictional 😀 e\u0301\r\nline\runtouched'.encode()
    obj = upload(env, content)
    assert obj['sha256'] == sha256(content).hexdigest()
    assert obj['status'] == 'quarantined' and env.scanner.calls == 0
    with pytest.raises(Conflict):
        read(env, obj)
    with pytest.raises(Conflict):
        env.vault.source_handle(identity=env.identity, case_id='case-1', object_id=obj['object_id'], expected_revision=1)
    assert content not in env.path.read_bytes()
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT ciphertext FROM vault_blobs').fetchone()[0] != content
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("UPDATE vault_blobs SET ciphertext=x'00'")
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("UPDATE vault_originals SET descriptor='{}'")
    obj = scan(env, obj)
    assert obj['status'] == 'released' and obj['vault_revision'] == 3 and obj['version'] == 1
    assert read(env, obj) == content
    result = exact_text(env.vault, identity=env.identity, case_id='case-1', object_id=obj['object_id'],
                        expected_revision=3, expected_sha256=obj['sha256'])
    assert result['text'].encode() == content and result['fact_verified'] is False
    assert 'filename' not in result['source_handle']


def test_shared_transaction_source_gate_is_current_and_rolls_back_with_mutation(env):
    obj = scan(env, upload(env))
    args = dict(identity=env.identity, case_id='case-1', object_id=obj['object_id'],
                expected_revision=3, expected_sha256=obj['sha256'])
    with env.vault._connect() as db:
        with pytest.raises(PermissionError):
            env.vault.require_source(db, **args)
        db.execute('BEGIN IMMEDIATE')
        db.execute('CREATE TABLE fictional_projection(id TEXT)')
        db.execute("INSERT INTO fictional_projection VALUES ('projection-1')")
        assert env.vault.require_source(db, **args)['sha256'] == obj['sha256']
        db.rollback()
        assert not db.execute("SELECT name FROM sqlite_master WHERE name='fictional_projection'").fetchall()
        assert not db.execute("SELECT record FROM vault_audit WHERE record LIKE '%source_gate%'").fetchall()
        db.execute('BEGIN IMMEDIATE')
        with pytest.raises(Conflict):
            env.vault.require_source(db, **(args | {'expected_revision':1}))
        db.rollback()
        db.execute('BEGIN IMMEDIATE')
        db.execute("UPDATE agency_grants SET revoked=1 WHERE id='grant-1'")
        with pytest.raises(PermissionError):
            env.vault.require_source(db, **args)
        db.rollback()
    other = sqlite3.connect(':memory:')
    other.execute('BEGIN IMMEDIATE')
    with pytest.raises(PermissionError):
        env.vault.require_source(other, **args)
    other.close()


@pytest.mark.parametrize('content', [b'', b'\xff', b'embedded\0binary', b'x'*(Vault.MAX_BYTES+1)])
def test_rejects_unsafe_or_unbounded_uploads(env, content):
    with pytest.raises(ValueError):
        upload(env, content)
    assert env.vault.inventory(identity=env.identity, case_id='case-1') == []


@pytest.mark.parametrize('filename,media_type', [('../x.txt','text/plain'), ('x.html','text/html'),
                                                ('x\r.txt','text/plain'), ('x.pdf','application/pdf')])
def test_upload_type_and_filename_policy(env, filename, media_type):
    with pytest.raises(ValueError):
        env.vault.upload(identity=env.identity, case_id='case-1', content=b'fiction', filename=filename,
                          media_type=media_type, retain_until=env.now[0]+timedelta(days=8), command_id=uuid4().hex)


def test_unavailable_scanner_fails_closed_without_start_or_auto_retry(env):
    obj = upload(env)
    env.vault.scanner = None
    with pytest.raises(Unavailable):
        scan(env, obj)
    assert env.vault.metadata(identity=env.identity, case_id='case-1', object_id=obj['object_id'])['status'] == 'quarantined'
    assert env.scanner.calls == 0


@pytest.mark.parametrize('verdict,status', [('infected','blocked'), ('error','scan_failed'), ('invented','scan_failed')])
def test_scan_non_clean_results_never_release(env, verdict, status):
    env.scanner.verdict = verdict
    obj = scan(env, upload(env))
    assert obj['status'] == status
    with pytest.raises(Conflict):
        read(env, obj)
    assert env.scanner.calls == 1


def test_scanner_hash_mismatch_or_exception_is_preserved_failed_scan(env):
    class BadScanner:
        def scan(self, *args, **kwargs):
            return ScanResult('clean', 'fixture', 'v1', 'fixture', '0'*64)
    env.vault.scanner = BadScanner()
    obj = scan(env, upload(env))
    assert obj['status'] == 'scan_failed' and obj['scan']['error'] == 'scanner_failed'
    class ErrorScanner:
        def scan(self, *args, **kwargs):
            raise RuntimeError('DO NOT LOG FICTIONAL CONTENT')
    env.vault.scanner = ErrorScanner()
    obj = scan(env, obj)
    assert obj['status'] == 'scan_failed'
    assert 'DO NOT LOG' not in env.path.read_bytes().decode(errors='ignore')


def test_duplicate_upload_and_scan_are_idempotent_but_reuse_conflicts(env):
    obj = upload(env, command_id='upload-key-001')
    assert upload(env, command_id='upload-key-001') == obj
    with pytest.raises(Conflict):
        upload(env, b'different fictional source', command_id='upload-key-001')
    scanned = scan(env, obj, command_id='scan-key-001')
    assert scan(env, obj, command_id='scan-key-001') == scanned and env.scanner.calls == 1
    env.registry.revoke('grant-1')
    with pytest.raises(PermissionError):
        scan(env, obj, command_id='scan-key-001')
    with pytest.raises(PermissionError):
        upload(env, command_id='upload-key-001')


@pytest.mark.parametrize('case_id', ['case-2','case-3','missing'])
def test_cross_matter_tenant_and_case_access_denied(env, case_id):
    obj = scan(env, upload(env))
    with pytest.raises(PermissionError):
        env.vault.metadata(identity=env.identity, case_id=case_id, object_id=obj['object_id'])
    with pytest.raises(PermissionError):
        read(env, obj, case_id=case_id)


def test_forged_case_binding_denied_even_with_other_matter_grant(env):
    obj = scan(env, upload(env))
    env.registry.add_grant('grant-2', Grant(identity=env.identity,
        resource=Resource(organisation_id='org-1', matter_id='matter-2'), operations=frozenset(Operation),
        valid_from=env.now[0]-timedelta(days=1), expires_at=env.now[0]+timedelta(days=60)))
    with pytest.raises(PermissionError):
        read(env, obj, case_id='case-2')


def test_object_only_grants_do_not_list_or_read_other_objects(env):
    obj, other = scan(env, upload(env)), upload(env)
    env.registry.revoke('grant-1')
    env.registry.add_grant('object-grant', Grant(identity=env.identity,
        resource=Resource(organisation_id='org-1', matter_id='matter-1', object_id=obj['object_id']),
        operations=frozenset({Operation.READ, Operation.DOWNLOAD}),
        valid_from=env.now[0]-timedelta(days=1), expires_at=env.now[0]+timedelta(days=60)))
    assert read(env, obj)
    with pytest.raises(PermissionError):
        env.vault.inventory(identity=env.identity, case_id='case-1')
    with pytest.raises(PermissionError):
        env.vault.metadata(identity=env.identity, case_id='case-1', object_id=other['object_id'])
    with pytest.raises(PermissionError):
        env.vault.audit(identity=env.identity, case_id='case-1')


def test_read_grant_is_not_download_or_control_authority(env):
    obj = scan(env, upload(env))
    env.registry.revoke('grant-1')
    env.registry.add_grant('read-only', Grant(identity=env.identity,
        resource=Resource(organisation_id='org-1', matter_id='matter-1'), operations=frozenset({Operation.READ}),
        valid_from=env.now[0]-timedelta(days=1), expires_at=env.now[0]+timedelta(days=60)))
    assert env.vault.metadata(identity=env.identity, case_id='case-1', object_id=obj['object_id'])
    with pytest.raises(PermissionError):
        read(env, obj)
    with pytest.raises(PermissionError):
        control(env, obj, hold=True)


def test_write_grant_alone_never_confers_hold_delete_or_scanner_control(env):
    obj = upload(env)
    env.vault.authority = RegistryAuthority()
    with pytest.raises(PermissionError):
        control(env, obj, hold=True)
    with pytest.raises(PermissionError):
        control(env, obj, action='delete')
    with pytest.raises(PermissionError):
        scan(env, obj)


def test_expiry_at_transaction_end_rolls_back_write_and_content_release(env):
    obj = upload(env)
    def expiring_policy(db, identity, scope, permission, now):
        env.now[0] += timedelta(days=61)
        return True
    env.vault.authority = RegistryAuthority(control=expiring_policy)
    with pytest.raises(PermissionError):
        control(env, obj, hold=True)
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT hold,revision FROM vault_state').fetchone() == (0, 1)
        assert db.execute("SELECT count(*) FROM vault_audit WHERE record LIKE '%denied%'").fetchone()[0]


def test_revocation_during_scan_forbids_result_publication(env):
    def scanning(content, **kwargs):
        env.registry.revoke('grant-1')
        return ScanResult('clean', 'fixture', 'v1', 'fixture', kwargs['sha256'])
    env.scanner.scan = scanning
    with pytest.raises(PermissionError):
        scan(env, upload(env))
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT status FROM vault_state').fetchone()[0] == 'scanning'
        assert db.execute('SELECT scan_record FROM vault_state').fetchone()[0] is None


def test_policy_change_during_scan_invalidates_the_exact_attempt(env):
    obj = upload(env)
    def scanning(content, **kwargs):
        current = env.vault.metadata(identity=env.identity, case_id='case-1', object_id=obj['object_id'])
        control(env, current, hold=True)
        return ScanResult('clean', 'fixture', 'v1', 'fixture', kwargs['sha256'])
    env.scanner.scan = scanning
    with pytest.raises(Conflict):
        scan(env, obj)
    current = env.vault.metadata(identity=env.identity, case_id='case-1', object_id=obj['object_id'])
    assert current['status'] == 'scanning' and current['scan'] is None and current['hold']
    with pytest.raises(Conflict):
        read(env, current)
    assert control(env, current, action='cancel_scan')['status'] == 'quarantined'


def test_source_gate_rejects_quarantine_and_changed_policy_after_preview(env):
    obj = upload(env)
    args = dict(identity=env.identity, case_id='case-1', object_id=obj['object_id'],
                expected_revision=1, expected_sha256=obj['sha256'])
    with sqlite3.connect(env.path) as db:
        db.execute('BEGIN IMMEDIATE')
        with pytest.raises(Conflict):
            env.vault.require_source(db, **args)
    obj = scan(env, obj)
    handle = env.vault.source_handle(identity=env.identity, case_id='case-1', object_id=obj['object_id'], expected_revision=3)
    control(env, obj, hold=True)
    with sqlite3.connect(env.path) as db:
        db.execute('BEGIN IMMEDIATE')
        with pytest.raises(Conflict):
            env.vault.require_source(db, **(args | {'expected_revision':handle['vault_revision']}))


def test_plaintext_corruption_detected_even_if_storage_triggers_are_removed(env):
    obj = scan(env, upload(env))
    with sqlite3.connect(env.path) as db:
        db.execute('DROP TRIGGER vault_blob_no_update')
        db.execute("UPDATE vault_blobs SET ciphertext=x'00000000000000000000000000000000'")
    with pytest.raises(IntegrityError):
        read(env, obj)


def test_case_capacity_is_bounded_without_deleting_tombstones(env):
    env.vault.MAX_CASE_OBJECTS = 1
    upload(env)
    with pytest.raises(Conflict):
        upload(env)


def test_scan_cancellation_suppresses_result_and_restart_never_auto_resumes(env):
    obj = upload(env)
    def scanning(content, **kwargs):
        live = env.vault.metadata(identity=env.identity, case_id='case-1', object_id=obj['object_id'])
        control(env, live, action='cancel_scan')
        return ScanResult('clean', 'fixture', 'v1', 'fixture', kwargs['sha256'])
    env.scanner.scan = scanning
    with pytest.raises(Conflict):
        scan(env, obj, command_id='cancelled-scan-key')
    restarted = Vault(env.path, authority=env.vault.authority, keys=env.keys, clock=lambda: env.now[0])
    live = restarted.metadata(identity=env.identity, case_id='case-1', object_id=obj['object_id'])
    assert live['status'] == 'quarantined' and live['vault_revision'] == 3
    assert restarted.scan(identity=env.identity, case_id='case-1', object_id=obj['object_id'],
                          expected_revision=1, command_id='cancelled-scan-key')['status'] == 'quarantined'


def test_interrupted_scan_requires_explicit_cancel_and_new_command(env):
    obj = upload(env)
    def crash(*args, **kwargs):
        raise KeyboardInterrupt()
    env.scanner.scan = crash
    with pytest.raises(KeyboardInterrupt):
        scan(env, obj)
    restarted = Vault(env.path, authority=env.vault.authority, keys=env.keys, scanner=SyntheticScanner(), clock=lambda: env.now[0])
    live = restarted.metadata(identity=env.identity, case_id='case-1', object_id=obj['object_id'])
    assert live['status'] == 'scanning'
    with pytest.raises(Conflict):
        restarted.scan(identity=env.identity, case_id='case-1', object_id=obj['object_id'], expected_revision=2, command_id=uuid4().hex)
    env.vault = restarted
    assert scan(env, control(env, live, action='cancel_scan'))['status'] == 'released'


def test_hold_and_retention_are_explicit_versioned_and_guard_deletion(env):
    obj = scan(env, upload(env))
    with pytest.raises(Conflict):
        control(env, obj, action='delete')
    held = control(env, obj, hold=True, command_id='hold-key-001')
    assert control(env, obj, hold=True, command_id='hold-key-001') == held
    assert held['version'] == 1 and held['sha256'] == obj['sha256']
    with pytest.raises(Conflict):
        read(env, obj)
    env.now[0] += timedelta(days=9)
    with pytest.raises(Conflict):
        control(env, held, action='delete')
    unheld = control(env, held, hold=False)
    env.vault.deletion_guard = None
    with pytest.raises(Conflict):
        control(env, unheld, action='delete')
    env.vault.deletion_guard = lambda db, handle: True
    deleted = control(env, unheld, action='delete', command_id='delete-key-001')
    assert deleted['status'] == 'deleted_local' and deleted['deletion_scope'] == 'local_vault_ciphertext_only'
    assert control(env, unheld, action='delete', command_id='delete-key-001') == deleted
    with pytest.raises(Conflict):
        read(env, deleted)
    with sqlite3.connect(env.path) as db:
        assert db.execute('SELECT count(*) FROM vault_blobs').fetchone()[0] == 0
        assert db.execute('SELECT count(*) FROM vault_originals').fetchone()[0] == 1


def test_retention_minimum_and_stale_revision_cannot_be_bypassed(env):
    obj = upload(env)
    with pytest.raises(Conflict):
        control(env, obj, action='set_retention', retain_until=env.now[0])
    later = control(env, obj, action='set_retention', retain_until=env.now[0]+timedelta(days=20))
    assert later['vault_revision'] == 2
    with pytest.raises(Conflict):
        control(env, obj, hold=True)
    with pytest.raises(Conflict):
        env.vault.source_handle(identity=env.identity, case_id='case-1', object_id=obj['object_id'], expected_revision=1)


def test_audit_is_atomic_append_only_content_free_and_detects_tampering(env):
    obj = scan(env, upload(env, b'Fictional secret body not in audit'))
    read(env, obj)
    audit = env.vault.audit(identity=env.identity, case_id='case-1')
    assert audit['verified_local_chain'] and not audit['independently_anchored']
    assert any(r['operation'] == 'download' for r in audit['records'])
    assert 'Fictional secret body' not in json.dumps(audit) and 'fictional.txt' not in json.dumps(audit)
    with sqlite3.connect(env.path) as db:
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("UPDATE vault_audit SET record='{}'")
        db.execute('DROP TRIGGER vault_audit_no_update')
        db.execute("UPDATE vault_audit SET record='{}' WHERE sequence=1")
    with pytest.raises(IntegrityError):
        env.vault.audit(identity=env.identity, case_id='case-1')


def test_failed_audit_insert_rolls_back_upload_and_idempotency(env):
    with sqlite3.connect(env.path) as db:
        db.execute("CREATE TRIGGER fail_audit BEFORE INSERT ON vault_audit BEGIN SELECT RAISE(ABORT,'fixture failure'); END")
    with pytest.raises(sqlite3.IntegrityError):
        upload(env, command_id='rollback-upload-key')
    with sqlite3.connect(env.path) as db:
        for table in ('vault_originals','vault_blobs','vault_state','vault_commands'):
            assert db.execute(f'SELECT count(*) FROM {table}').fetchone()[0] == 0
        db.execute('DROP TRIGGER fail_audit')
    assert upload(env, command_id='rollback-upload-key')['status'] == 'quarantined'


def test_deleted_ciphertext_or_wrong_key_fails_closed(env):
    obj = scan(env, upload(env))
    env.vault.keys = LocalKeyWrapper({'other-key': AESGCM.generate_key(bit_length=256)}, active_key_id='other-key')
    with pytest.raises(IntegrityError):
        read(env, obj)
    with pytest.raises(IntegrityError):
        env.vault.source_handle(identity=env.identity, case_id='case-1', object_id=obj['object_id'], expected_revision=3)
    env.vault.keys = env.keys
    with sqlite3.connect(env.path) as db:
        db.execute('DELETE FROM vault_blobs')
    with pytest.raises(IntegrityError):
        read(env, obj)
    with sqlite3.connect(env.path) as db:
        db.execute('BEGIN IMMEDIATE')
        with pytest.raises(IntegrityError):
            env.vault.require_source(db, identity=env.identity, case_id='case-1', object_id=obj['object_id'],
                                     expected_revision=3, expected_sha256=obj['sha256'])


def test_wrong_hash_wrong_identity_and_expired_grants_deny(env):
    obj = scan(env, upload(env))
    with pytest.raises(Conflict):
        read(env, obj, expected_sha256='0'*64)
    with pytest.raises(PermissionError):
        read(env, obj, identity=Identity(issuer='https://other.invalid', subject='operator'))
    env.now[0] += timedelta(days=61)
    with pytest.raises(PermissionError):
        read(env, obj)
