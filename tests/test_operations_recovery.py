from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import pytest

from eightball.operations.contracts import Scope
from eightball.operations.recovery import (Checkpoint, ReadOnlyAudit, RecoveryFailure,
    rehearse_restore, sign_checkpoint, verify_checkpoint)
from eightball.v2.playbooks import demo_case
from eightball.v2.store import Store
from eightball.store import Store as LegacyStore
from eightball.seed import create_case
from eightball.v2.services import migrate_legacy

NOW = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)


@pytest.fixture
def source(tmp_path):
    path = tmp_path / 'source.sqlite'
    store = Store(path)
    case = demo_case()
    store.create(case, fixture=True)
    scope = Scope(organisation_id='fictional-org', matter_id='fictional-matter', case_id=case.id)
    key = Ed25519PrivateKey.generate()
    audit = store.audit(case.id)
    checkpoint = sign_checkpoint(audit, scope, expected_revision=0, private_key=key, now=NOW)
    return path, store, case, key, checkpoint, audit


def verify(checkpoint, key, **kwargs):
    values = dict(public_key=key.public_key(), scope=checkpoint.scope, minimum_revision=0,
                  now=NOW, maximum_age_seconds=60)
    values.update(kwargs)
    return verify_checkpoint(checkpoint, **values)


def restore(source, destination, **kwargs):
    path, store, case, key, checkpoint, audit = source
    values = dict(checkpoints=(checkpoint,), public_key=key.public_key(),
                  maximum_age_seconds=60, rto_seconds=30, now=NOW)
    values.update(kwargs)
    return rehearse_restore(path, destination, **values)


def test_real_restore_uses_backup_and_existing_audit_without_mutating_source(source, tmp_path):
    path, store, case, key, checkpoint, audit = source
    original = path.read_bytes()
    restored = tmp_path / 'restored.sqlite'
    report = restore(source, restored)
    assert report['status'] == 'passed'
    assert report['checked_case_count'] == 1
    assert report['rpo_seconds_observed'] == 0
    assert not report['production_recovery_accepted']
    assert not report['independent_anchor_custody_verified']
    assert ReadOnlyAudit(restored).audit(case.id) == audit
    assert path.read_bytes() == original and store.audit(case.id) == audit
    assert os.stat(restored).st_mode & 0o777 == 0o600


@pytest.mark.parametrize('change', ['scope', 'revision', 'digest', 'head', 'signature', 'key', 'future', 'old'])
def test_signatures_scope_revision_and_clock_bounds(source, change):
    _, _, _, key, checkpoint, _ = source
    args = {}
    if change == 'scope':
        args['scope'] = checkpoint.scope.model_copy(update={'matter_id': 'other'})
    if change == 'revision':
        args['minimum_revision'] = 1
    if change == 'digest':
        checkpoint = checkpoint.model_copy(update={'audit_sha256': 'b' * 64})
    if change == 'head':
        checkpoint = checkpoint.model_copy(update={'head_hash': 'b' * 64})
    if change == 'signature':
        checkpoint = checkpoint.model_copy(update={'signature': 'invalid'})
    if change == 'key':
        key = Ed25519PrivateKey.generate()
    if change == 'future':
        args['now'] = NOW - timedelta(seconds=1)
    if change == 'old':
        args['now'] = NOW + timedelta(seconds=61)
    with pytest.raises(RecoveryFailure, match='verification failed'):
        verify(checkpoint, key, **args)


def test_anchor_detects_recomputed_local_chain(source):
    _, _, _, key, checkpoint, audit = source
    altered = {**audit, 'audit_scope': 'rewritten local chain could still say valid'}
    with pytest.raises(RecoveryFailure):
        verify(checkpoint, key, audit=altered)


@pytest.mark.parametrize('change', ['invalid', 'wrong_case', 'stale_revision'])
def test_refuses_signing_invalid_wrong_case_and_stale_audit(source, change):
    _, _, _, key, checkpoint, audit = source
    if change == 'invalid':
        audit = {**audit, 'valid': False}
    scope = checkpoint.scope.model_copy(update={'case_id': 'other'}) if change == 'wrong_case' else checkpoint.scope
    with pytest.raises(RecoveryFailure):
        sign_checkpoint(audit, scope, expected_revision=1 if change == 'stale_revision' else 0,
                        private_key=key, now=NOW)


@pytest.mark.parametrize('existing', ['file', 'symlink', 'source'])
def test_never_overwrites_existing_destination_or_source(source, tmp_path, existing):
    destination = tmp_path / 'existing'
    sentinel = tmp_path / 'sentinel'
    sentinel.write_bytes(b'keep me')
    if existing == 'file':
        destination.write_bytes(b'keep me too')
    if existing == 'symlink':
        destination.symlink_to(sentinel)
    if existing == 'source':
        destination = source[0]
    before = destination.read_bytes()
    with pytest.raises((RecoveryFailure, FileExistsError)):
        restore(source, destination)
    assert destination.read_bytes() == before and sentinel.read_bytes() == b'keep me'


def test_corrupt_database_fails_preserves_failed_sandbox_and_no_sensitive_error(source, tmp_path):
    with sqlite3.connect(source[0]) as db:
        db.execute("UPDATE v2_events SET hash=?", ('b' * 64,))
    destination = tmp_path / 'failed.sqlite'
    with pytest.raises(RecoveryFailure) as error:
        restore(source, destination)
    assert destination.is_file()
    assert source[2].client not in str(error.value)


def test_cancel_before_start_no_file_and_cancel_during_backup_retains_sandbox(source, tmp_path):
    destination = tmp_path / 'cancelled.sqlite'
    with pytest.raises(RecoveryFailure, match='cancelled'):
        restore(source, destination, cancelled=lambda: True)
    assert not destination.exists()
    calls = []
    def cancel():
        calls.append(True)
        return len(calls) > 1
    with pytest.raises(RecoveryFailure, match='cancelled'):
        restore(source, destination, cancelled=cancel)
    assert destination.exists()
    # Restart needs a deliberate fresh destination; no automatic retry/overwrite.
    with pytest.raises(FileExistsError):
        restore(source, destination)
    assert restore(source, tmp_path / 'explicit-restart.sqlite')['status'] == 'passed'


@pytest.mark.parametrize('rto', [0, -1, float('nan'), float('inf'), True])
def test_invalid_recovery_target_rejected(source, tmp_path, rto):
    with pytest.raises(RecoveryFailure):
        restore(source, tmp_path / 'invalid.sqlite', rto_seconds=rto)


def test_rto_budget_enforced(source, tmp_path, monkeypatch):
    ticks = iter([0, 0, 50])
    monkeypatch.setattr('eightball.operations.recovery.time.monotonic', lambda: next(ticks))
    with pytest.raises(RecoveryFailure, match='RTO'):
        restore(source, tmp_path / 'slow.sqlite', rto_seconds=1)


def test_alpha_import_and_audit_lineage_survive_rehearsal(tmp_path):
    path = tmp_path / 'alpha.sqlite'
    legacy = LegacyStore(path)
    old = create_case()
    legacy.create(old)
    store = Store(path)
    imported = migrate_legacy(store, legacy, old.id)
    audit = store.audit(imported.id)
    assert audit['legacy_lineage'] == legacy.audit(old.id)
    key = Ed25519PrivateKey.generate()
    scope = Scope(organisation_id='fictional-org', matter_id='fictional-matter', case_id=imported.id)
    checkpoint = sign_checkpoint(audit, scope, expected_revision=0, private_key=key, now=NOW)
    restored = tmp_path / 'alpha-restored.sqlite'
    rehearse_restore(path, restored, checkpoints=(checkpoint,), public_key=key.public_key(),
                     maximum_age_seconds=60, rto_seconds=30, now=NOW)
    assert ReadOnlyAudit(restored).audit(imported.id) == audit
    assert ReadOnlyAudit(restored, legacy=True).audit(old.id) == legacy.audit(old.id)


def test_rehearsal_cli_with_real_key_and_offline_checkpoint(source, tmp_path):
    path, _, _, key, checkpoint, _ = source
    # A fresh wall-clock checkpoint for the actual CLI freshness check.
    checkpoint = sign_checkpoint(source[-1], checkpoint.scope, expected_revision=0,
        private_key=key, now=datetime.now(timezone.utc))
    public = tmp_path / 'public.pem'
    public.write_bytes(key.public_key().public_bytes(serialization.Encoding.PEM,
                                                    serialization.PublicFormat.SubjectPublicKeyInfo))
    checkpoints = tmp_path / 'checkpoints.json'
    checkpoints.write_text(json.dumps([checkpoint.model_dump()]))
    result = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / 'scripts/operations/rehearse.py'), '--source', str(path),
        '--sandbox', str(tmp_path / 'cli.sqlite'), '--checkpoints', str(checkpoints),
        '--trusted-public-key', str(public), '--maximum-age-seconds', '60', '--rto-seconds', '30',
        '--fictional-only'], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)['status'] == 'passed'
