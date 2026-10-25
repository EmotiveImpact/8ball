"""Explicit fictional SQLite restore rehearsal, not a managed backup service.

The host owns key custody and an independent checkpoint copy. This module never
discovers databases, mutates the source, restores in place or runs on import.
"""
import base64
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from hashlib import sha256
import os
from pathlib import Path
import sqlite3
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from pydantic import Field

from eightball.store import canonical, digest
from .contracts import Scope, Strict


class RecoveryFailure(ValueError):
    pass


class Checkpoint(Strict):
    version: int = Field(default=1, ge=1, le=1)
    scope: Scope
    revision: int = Field(ge=0)
    audit_sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    head_hash: str = Field(pattern=r'^[a-f0-9]{64}$')
    captured_at: str
    signature: str


def _aware(value):
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise RecoveryFailure('An aware host timestamp is required')
    return value


def sign_checkpoint(audit, scope: Scope, *, expected_revision: int,
                    private_key: Ed25519PrivateKey, now: datetime) -> Checkpoint:
    """Sign bytes returned by the existing store.audit, without changing its format."""
    if (audit.get('valid') is not True or audit.get('case', {}).get('id') != scope.case_id
            or type(expected_revision) is not int
            or audit.get('case', {}).get('revision') != expected_revision):
        raise RecoveryFailure('Valid audit at the exact case revision is required')
    values = {'version': 1, 'scope': scope.model_dump(), 'revision': expected_revision,
              'audit_sha256': digest(audit), 'head_hash': audit['head_hash'],
              'captured_at': _aware(now).isoformat()}
    values['signature'] = base64.b64encode(private_key.sign(canonical(values).encode())).decode('ascii')
    return Checkpoint.model_validate(values)


def verify_checkpoint(checkpoint: Checkpoint, *, public_key: Ed25519PublicKey,
                      scope: Scope, minimum_revision: int, now: datetime,
                      maximum_age_seconds: int, audit=None):
    try:
        if (type(minimum_revision) is not int or minimum_revision < 0
                or type(maximum_age_seconds) is not int or maximum_age_seconds < 0):
            raise ValueError
        captured = _aware(datetime.fromisoformat(checkpoint.captured_at))
        age = (_aware(now) - captured).total_seconds()
        if (checkpoint.scope != scope or checkpoint.revision < minimum_revision
                or age < 0 or age > maximum_age_seconds):
            raise ValueError
        public_key.verify(base64.b64decode(checkpoint.signature, validate=True),
                          canonical(checkpoint.model_dump(exclude={'signature'})).encode())
        if audit is not None and (audit.get('valid') is not True
                                  or digest(audit) != checkpoint.audit_sha256
                                  or audit.get('head_hash') != checkpoint.head_hash
                                  or audit.get('case', {}).get('revision') != checkpoint.revision
                                  or audit.get('case', {}).get('id') != scope.case_id):
            raise ValueError
    except (ValueError, TypeError, InvalidSignature):
        raise RecoveryFailure('Checkpoint verification failed') from None


class ReadOnlyAudit:
    """Reuse original audit/replay validators without running Store constructors."""
    def __init__(self, path, *, legacy=False):
        from eightball.store import Store as LegacyStore
        from eightball.v2.store import Store as V2Store

        class Reader(LegacyStore if legacy else V2Store):
            def __init__(self, location):
                self.path = location

            @contextmanager
            def connection(self):
                db = sqlite3.connect(Path(self.path).resolve().as_uri() + '?mode=ro', uri=True)
                db.row_factory = sqlite3.Row
                try:
                    yield db
                finally:
                    db.close()

        self.store = Reader(path)

    def audit(self, case_id):
        return self.store.audit(case_id)


def rehearse_restore(source, destination, *, checkpoints: tuple[Checkpoint, ...],
                     public_key: Ed25519PublicKey, maximum_age_seconds: int,
                     rto_seconds: float, now=None, cancelled=None, legacy=False):
    """Copy one explicitly selected database into a NEW private sandbox file.

    Verifies all explicitly supplied cases, not every tenant or every table.
    Leaves a failed sandbox for deliberate inspection. No automatic retries.
    """
    now = _aware(now or datetime.now(timezone.utc))
    if (not checkpoints or len({c.scope.case_id for c in checkpoints}) != len(checkpoints)
            or isinstance(rto_seconds, bool) or not isinstance(rto_seconds, (int, float))
            or not 0 < rto_seconds <= 86400):
        raise RecoveryFailure('Explicit unique checkpoints and bounded RTO are required')
    source, destination = Path(source), Path(destination)
    if not source.is_file() or source.resolve() == destination.resolve():
        raise RecoveryFailure('An existing source and new sandbox are required')
    for checkpoint in checkpoints:
        verify_checkpoint(checkpoint, public_key=public_key, scope=checkpoint.scope,
                          minimum_revision=checkpoint.revision, now=now,
                          maximum_age_seconds=maximum_age_seconds)
    start = time.monotonic()

    def progress(*args):
        if cancelled is not None and cancelled():
            raise RecoveryFailure('Restore rehearsal cancelled')
        if time.monotonic() - start > rto_seconds:
            raise RecoveryFailure('Restore rehearsal exceeded RTO')

    progress()
    # O_EXCL refuses an existing file or symlink. The sandbox may contain whole-DB
    # confidential bytes; caller must use disposable fictional data and private storage.
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(fd)
    try:
        with closing(sqlite3.connect(source.resolve().as_uri() + '?mode=ro', uri=True)) as src:
            with closing(sqlite3.connect(destination)) as dst, dst:
                src.backup(dst, pages=64, progress=progress, sleep=0)
                if dst.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    raise RecoveryFailure('Restored database failed integrity verification')
                if dst.execute('PRAGMA foreign_key_check').fetchone() is not None:
                    raise RecoveryFailure('Restored database failed reference verification')
        reader = ReadOnlyAudit(destination, legacy=legacy)
        for checkpoint in checkpoints:
            verify_checkpoint(checkpoint, public_key=public_key, scope=checkpoint.scope,
                              minimum_revision=checkpoint.revision, now=now,
                              maximum_age_seconds=maximum_age_seconds,
                              audit=reader.audit(checkpoint.scope.case_id))
        progress()
    except RecoveryFailure:
        raise
    except Exception:
        raise RecoveryFailure('Restore rehearsal failed; inspect private sandbox') from None
    return {'status': 'passed', 'scope': 'fictional_local_sqlite_rehearsal',
            'elapsed_seconds': round(time.monotonic() - start, 6),
            'checked_case_count': len(checkpoints),
            'checkpoint_sha256': [sha256(c.model_dump_json().encode()).hexdigest() for c in checkpoints],
            'rpo_seconds_observed': max((now - datetime.fromisoformat(c.captured_at)).total_seconds()
                                        for c in checkpoints),
            'rpo_basis': 'checkpoint age; not measured replication lag',
            'independent_anchor_custody_verified': False,
            'production_recovery_accepted': False}
