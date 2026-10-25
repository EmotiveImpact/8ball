"""Bounded encrypted SQLite vault with explicit authority and processing adapters."""
from contextlib import closing, contextmanager
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
from uuid import uuid4

from cryptography.exceptions import InvalidTag

from eightball.authorisation import Identity
from .contracts import Conflict, IntegrityError, ScanResult, Unavailable, VaultPermission as P
from .crypto import decrypt, encrypt


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(value):
    return sha256(canonical(value).encode('utf-8')).hexdigest()


def timestamp(value):
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('An aware timestamp is required')
    return value.astimezone(timezone.utc).isoformat()


class Vault:
    MAX_BYTES = 262_144
    MAX_CASE_BYTES = 8_388_608
    MAX_CASE_OBJECTS = 100

    def __init__(self, path, *, authority, keys, scanner=None, deletion_guard=None,
                 clock=lambda: datetime.now(timezone.utc), minimum_retention=timedelta(days=7)):
        if minimum_retention < timedelta(0):
            raise ValueError('Retention must not be negative')
        self.path = str(path)
        self.authority, self.keys, self.scanner = authority, keys, scanner
        self.deletion_guard, self.clock = deletion_guard, clock
        self.minimum_retention = minimum_retention
        with closing(self._connect()) as db, db:
            db.executescript(Path(__file__).with_name('schema.sql').read_text())

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA secure_delete=ON')
        return db

    def _now(self):
        now = self.clock()
        timestamp(now)
        return now

    def _actor(self, identity):
        if not isinstance(identity, Identity):
            raise PermissionError('Verified identity required')
        return digest(identity.model_dump(mode='json'))

    def _audit(self, db, *, identity, case_id, object_id, operation, outcome, details=None):
        last = db.execute('SELECT record_hash FROM vault_audit ORDER BY sequence DESC LIMIT 1').fetchone()
        previous = last[0] if last else '0' * 64
        record = dict(schema_version=1, event_id=uuid4().hex, actor=self._actor(identity),
                      case_id=case_id, object_id=object_id, operation=operation,
                      outcome=outcome, at=timestamp(self._now()), details=details or {})
        raw = canonical(record)
        db.execute('INSERT INTO vault_audit(record,previous_hash,record_hash) VALUES (?,?,?)',
                   (raw, previous, digest({'previous_hash': previous, 'record': record})))

    @contextmanager
    def _tx(self, identity, case_id, object_id, permission):
        self._actor(identity)
        with closing(self._connect()) as db, db:
            try:
                db.execute('BEGIN IMMEDIATE')
                scope = self.authority.require(db, identity=identity, case_id=case_id,
                                               object_id=object_id, permission=permission, now=self._now())
                yield db, scope
                final_scope = self.authority.require(db, identity=identity, case_id=case_id,
                                                     object_id=object_id, permission=permission,
                                                     now=self._now())
                if final_scope != scope:
                    raise PermissionError('Scope changed during operation')
                self._audit(db, identity=identity, case_id=case_id, object_id=object_id,
                            operation=permission.value, outcome='allowed')
                db.commit()
            except Exception as exc:
                db.rollback()
                db.execute('BEGIN IMMEDIATE')
                self._audit(db, identity=identity, case_id=case_id, object_id=object_id,
                            operation=permission.value,
                            outcome='denied' if isinstance(exc, PermissionError) else 'rejected')
                db.commit()
                raise

    def _row(self, db, scope, case_id, object_id):
        cursor = db.execute('''SELECT o.*,s.revision,s.status,s.retain_until,s.hold,s.scan_attempt,s.scan_record
                            FROM vault_originals o JOIN vault_state s ON s.object_id=o.id
                            WHERE o.id=? AND o.case_id=? AND o.organisation_id=? AND o.matter_id=?''',
                            (object_id, case_id, scope.organisation_id, scope.matter_id))
        cursor.row_factory = sqlite3.Row
        row = cursor.fetchone()
        if row is None:
            raise PermissionError('Access is not permitted')
        descriptor = json.loads(row['descriptor'])
        if (descriptor['object_id'] != object_id or descriptor['case_id'] != case_id
                or descriptor['organisation_id'] != scope.organisation_id
                or descriptor['matter_id'] != scope.matter_id):
            raise IntegrityError('Original descriptor binding failed')
        return row

    def _metadata(self, row):
        return {**json.loads(row['descriptor']), 'vault_revision': row['revision'],
                'status': row['status'], 'retain_until': row['retain_until'],
                'hold': bool(row['hold']),
                'scan': json.loads(row['scan_record']) if row['scan_record'] else None,
                'deletion_scope': 'local_vault_ciphertext_only' if row['status'] == 'deleted_local' else None}

    def _revision(self, row, revision):
        if type(revision) is not int or row['revision'] != revision:
            raise Conflict('Vault revision changed; reload and review')

    def _command(self, db, identity, case_id, command_id, request):
        if not isinstance(command_id, str) or not 8 <= len(command_id) <= 128:
            raise ValueError('A bounded idempotency key is required')
        old = db.execute('SELECT * FROM vault_commands WHERE actor=? AND case_id=? AND command_id=?',
                         (self._actor(identity), case_id, command_id)).fetchone()
        if old and old['request_hash'] != digest(request):
            raise Conflict('Idempotency key already used for a different request')
        return old['object_id'] if old else None

    def _remember(self, db, identity, case_id, command_id, request, object_id):
        db.execute('INSERT INTO vault_commands VALUES (?,?,?,?,?)',
                   (self._actor(identity), case_id, command_id, digest(request), object_id))

    def _bytes(self, db, row):
        blob = db.execute('SELECT * FROM vault_blobs WHERE object_id=?', (row['id'],)).fetchone()
        if blob is None:
            raise IntegrityError('Original ciphertext is unavailable')
        try:
            content = decrypt(blob['nonce'], blob['ciphertext'], json.loads(blob['envelope']), self.keys,
                              context=row['descriptor'].encode('utf-8'))
        except (InvalidTag, KeyError, ValueError, TypeError) as exc:
            raise IntegrityError('Original authentication failed') from exc
        descriptor = json.loads(row['descriptor'])
        if sha256(content).hexdigest() != descriptor['sha256'] or len(content) != descriptor['size_bytes']:
            raise IntegrityError('Original content hash failed')
        return content

    def upload(self, *, identity, case_id, content, filename, media_type, retain_until, command_id):
        if not isinstance(content, bytes) or not 1 <= len(content) <= self.MAX_BYTES:
            raise ValueError('Original exceeds the bounded upload size')
        if media_type not in {'text/plain', 'text/markdown'}:
            raise ValueError('Only exact UTF-8 text originals are supported')
        text = content.decode('utf-8', errors='strict')
        if '\x00' in text:
            raise ValueError('Binary text is not supported')
        if (not isinstance(filename, str) or not 1 <= len(filename) <= 120
                or any(ord(c) < 32 or c in '/\\' for c in filename)
                or not filename.lower().endswith(('.txt', '.md'))):
            raise ValueError('A descriptive .txt or .md filename without path characters is required')
        until = timestamp(retain_until)
        request = dict(operation='upload', sha256=sha256(content).hexdigest(), filename=filename,
                       media_type=media_type, retain_until=until)
        with self._tx(identity, case_id, None, P.UPLOAD) as (db, scope):
            old = self._command(db, identity, case_id, command_id, request)
            if old:
                return self._metadata(self._row(db, scope, case_id, old))
            now = self._now()
            if retain_until < now + self.minimum_retention:
                raise ValueError('Retention is below the server minimum')
            originals = db.execute('SELECT descriptor FROM vault_originals WHERE case_id=?', (case_id,)).fetchall()
            if (len(originals) >= self.MAX_CASE_OBJECTS
                    or sum(json.loads(r[0])['size_bytes'] for r in originals) + len(content) > self.MAX_CASE_BYTES):
                raise Conflict('Case vault capacity reached, including retained tombstones')
            object_id = uuid4().hex
            descriptor = dict(schema_version=1, object_id=object_id, version=1, case_id=case_id,
                              organisation_id=scope.organisation_id, matter_id=scope.matter_id,
                              sha256=request['sha256'], size_bytes=len(content), filename=filename,
                              media_type=media_type, representation='utf8-exact-v1',
                              uploaded_at=timestamp(now), minimum_retain_until=timestamp(now + self.minimum_retention))
            raw = canonical(descriptor)
            nonce, ciphertext, envelope = encrypt(content, self.keys, context=raw.encode('utf-8'))
            db.execute('INSERT INTO vault_originals VALUES (?,?,?,?,?)',
                       (object_id, case_id, scope.organisation_id, scope.matter_id, raw))
            db.execute('INSERT INTO vault_blobs VALUES (?,?,?,?)',
                       (object_id, nonce, ciphertext, canonical(envelope)))
            db.execute('INSERT INTO vault_state VALUES (?,1,?,?,0,NULL,NULL)',
                       (object_id, 'quarantined', until))
            self._remember(db, identity, case_id, command_id, request, object_id)
            self._audit(db, identity=identity, case_id=case_id, object_id=object_id,
                        operation='original_quarantined', outcome='committed',
                        details={'sha256': request['sha256'], 'version': 1})
            return self._metadata(self._row(db, scope, case_id, object_id))

    def metadata(self, *, identity, case_id, object_id):
        with self._tx(identity, case_id, object_id, P.READ) as (db, scope):
            return self._metadata(self._row(db, scope, case_id, object_id))

    def inventory(self, *, identity, case_id):
        with self._tx(identity, case_id, None, P.READ) as (db, scope):
            ids = db.execute('''SELECT id FROM vault_originals WHERE case_id=? AND organisation_id=?
                                AND matter_id=? ORDER BY id LIMIT ?''',
                             (case_id, scope.organisation_id, scope.matter_id, self.MAX_CASE_OBJECTS)).fetchall()
            return [self._metadata(self._row(db, scope, case_id, row[0])) for row in ids]

    def _handle(self, row):
        descriptor = json.loads(row['descriptor'])
        return {key: descriptor[key] for key in ('schema_version', 'object_id', 'version', 'case_id',
                'organisation_id', 'matter_id', 'sha256', 'size_bytes', 'media_type', 'representation')} | {
                    'vault_revision': row['revision']}

    def _released(self, row):
        if row['status'] != 'released':
            raise Conflict('Original is not released by a clean scan')
        scan = json.loads(row['scan_record']) if row['scan_record'] else {}
        if scan.get('verdict') != 'clean' or scan.get('content_sha256') != json.loads(row['descriptor'])['sha256']:
            raise IntegrityError('Clean scan binding failed')

    def source_handle(self, *, identity, case_id, object_id, expected_revision):
        with self._tx(identity, case_id, object_id, P.READ) as (db, scope):
            row = self._row(db, scope, case_id, object_id)
            self._revision(row, expected_revision)
            self._released(row)
            self._bytes(db, row)
            return self._handle(row)

    def require_source(self, db, *, identity, case_id, object_id, expected_revision, expected_sha256):
        """Final source gate inside a caller-owned, same-database write transaction.

        The caller must use BEGIN IMMEDIATE and commit its own mutation/audit on
        this connection. This never authorizes a later transaction or byte read.
        """
        self._actor(identity)
        if not db.in_transaction:
            raise PermissionError('A shared transaction is required')
        attached = {str(Path(row[2]).resolve()) for row in db.execute('PRAGMA database_list') if row[1] == 'main'}
        if str(Path(self.path).resolve()) not in attached:
            raise PermissionError('The source and mutation must share the database')
        scope = self.authority.require(db, identity=identity, case_id=case_id, object_id=object_id,
                                       permission=P.READ, now=self._now())
        row = self._row(db, scope, case_id, object_id)
        self._revision(row, expected_revision)
        self._released(row)
        if expected_sha256 != json.loads(row['descriptor'])['sha256']:
            raise Conflict('Original hash does not match the reviewed handle')
        self._bytes(db, row)
        self._audit(db, identity=identity, case_id=case_id, object_id=object_id,
                    operation='source_gate', outcome='allowed', details={'revision': expected_revision})
        return self._handle(row)

    def read_original(self, *, identity, case_id, object_id, expected_revision, expected_sha256):
        with self._tx(identity, case_id, object_id, P.DOWNLOAD) as (db, scope):
            row = self._row(db, scope, case_id, object_id)
            self._revision(row, expected_revision)
            self._released(row)
            if expected_sha256 != json.loads(row['descriptor'])['sha256']:
                raise Conflict('Original hash does not match the reviewed handle')
            return self._bytes(db, row)

    def scan(self, *, identity, case_id, object_id, expected_revision, command_id):
        request = dict(operation='scan', object_id=object_id, expected_revision=expected_revision)
        with self._tx(identity, case_id, object_id, P.SCAN) as (db, scope):
            row = self._row(db, scope, case_id, object_id)
            if self._command(db, identity, case_id, command_id, request):
                return self._metadata(row)
            self._revision(row, expected_revision)
            if row['status'] not in {'quarantined', 'scan_failed'}:
                raise Conflict('Cancel an interrupted scan explicitly before starting another')
            if self.scanner is None:
                raise Unavailable('No malware scanner has been configured; original remains quarantined')
            content = self._bytes(db, row)
            descriptor = json.loads(row['descriptor'])
            attempt = uuid4().hex
            db.execute("UPDATE vault_state SET revision=revision+1,status='scanning',scan_attempt=? WHERE object_id=?",
                       (attempt, object_id))
            self._remember(db, identity, case_id, command_id, request, object_id)
        try:
            result = self.scanner.scan(content, sha256=descriptor['sha256'], media_type=descriptor['media_type'])
            if (not isinstance(result, ScanResult) or result.verdict not in {'clean', 'infected', 'error'}
                    or result.content_sha256 != descriptor['sha256']
                    or any(not isinstance(v, str) or not 1 <= len(v) <= 128
                           for v in (result.engine, result.version, result.definitions))):
                raise ValueError('Invalid scanner result')
            record = dict(verdict=result.verdict, engine=result.engine, version=result.version,
                          definitions=result.definitions, content_sha256=result.content_sha256)
        except Exception:
            record = dict(verdict='error', content_sha256=descriptor['sha256'], error='scanner_failed')
        with self._tx(identity, case_id, object_id, P.SCAN) as (db, scope):
            row = self._row(db, scope, case_id, object_id)
            if row['status'] != 'scanning' or row['scan_attempt'] != attempt:
                raise Conflict('Scan cancelled or replaced; result was not published')
            # Hold/retention updates during a scan also invalidate publication.
            self._revision(row, expected_revision + 1)
            record['at'] = timestamp(self._now())
            status = {'clean': 'released', 'infected': 'blocked', 'error': 'scan_failed'}[record['verdict']]
            db.execute('''UPDATE vault_state SET revision=revision+1,status=?,scan_record=?,scan_attempt=NULL
                          WHERE object_id=?''', (status, canonical(record), object_id))
            self._audit(db, identity=identity, case_id=case_id, object_id=object_id,
                        operation='scan_disposition', outcome=status, details=record)
            return self._metadata(self._row(db, scope, case_id, object_id))

    def cancel_scan(self, *, identity, case_id, object_id, expected_revision, command_id, reason):
        return self._control(identity, case_id, object_id, expected_revision, command_id,
                             reason, 'cancel_scan', P.SCAN)

    def set_hold(self, *, identity, case_id, object_id, expected_revision, command_id, reason, hold):
        if type(hold) is not bool:
            raise ValueError('Explicit hold state required')
        return self._control(identity, case_id, object_id, expected_revision, command_id,
                             reason, 'hold', P.HOLD, hold=hold)

    def set_retention(self, *, identity, case_id, object_id, expected_revision, command_id, reason, retain_until):
        return self._control(identity, case_id, object_id, expected_revision, command_id,
                             reason, 'retention', P.RETENTION, retain_until=timestamp(retain_until))

    def delete(self, *, identity, case_id, object_id, expected_revision, command_id, reason):
        return self._control(identity, case_id, object_id, expected_revision, command_id,
                             reason, 'delete_local', P.DELETE)

    def _control(self, identity, case_id, object_id, revision, command_id, reason, operation, permission, **changes):
        if not isinstance(reason, str) or not 10 <= len(reason.strip()) <= 1000:
            raise ValueError('A bounded explicit human rationale is required')
        request = dict(operation=operation, object_id=object_id, expected_revision=revision,
                       reason_sha256=sha256(reason.encode('utf-8')).hexdigest(), **changes)
        with self._tx(identity, case_id, object_id, permission) as (db, scope):
            row = self._row(db, scope, case_id, object_id)
            if self._command(db, identity, case_id, command_id, request):
                return self._metadata(row)
            self._revision(row, revision)
            if row['status'] == 'deleted_local':
                raise Conflict('Local content was already deleted')
            if operation == 'hold':
                db.execute('UPDATE vault_state SET hold=?,revision=revision+1 WHERE object_id=?',
                           (int(changes['hold']), object_id))
            elif operation == 'retention':
                until = datetime.fromisoformat(changes['retain_until'])
                minimum = datetime.fromisoformat(json.loads(row['descriptor'])['minimum_retain_until'])
                if until < minimum:
                    raise Conflict('Retention cannot precede the immutable server minimum')
                db.execute('UPDATE vault_state SET retain_until=?,revision=revision+1 WHERE object_id=?',
                           (changes['retain_until'], object_id))
            elif operation == 'cancel_scan':
                if row['status'] != 'scanning':
                    raise Conflict('No active scan to cancel')
                db.execute("UPDATE vault_state SET status='quarantined',scan_attempt=NULL,revision=revision+1 WHERE object_id=?",
                           (object_id,))
            elif operation == 'delete_local':
                if row['hold'] or self._now() < datetime.fromisoformat(row['retain_until']):
                    raise Conflict('Hold or retention policy forbids deletion')
                if row['status'] == 'scanning':
                    raise Conflict('Cancel the active scan explicitly before deletion')
                if self.deletion_guard is None or self.deletion_guard(db, self._handle(row)) is not True:
                    raise Conflict('Dependent source/replica deletion clearance is not established')
                db.execute('DELETE FROM vault_blobs WHERE object_id=?', (object_id,))
                db.execute("UPDATE vault_state SET status='deleted_local',revision=revision+1 WHERE object_id=?", (object_id,))
            self._remember(db, identity, case_id, command_id, request, object_id)
            self._audit(db, identity=identity, case_id=case_id, object_id=object_id,
                        operation=operation, outcome='committed', details=request)
            return self._metadata(self._row(db, scope, case_id, object_id))

    def audit(self, *, identity, case_id, after=0, limit=100):
        if type(after) is not int or after < 0 or type(limit) is not int or not 1 <= limit <= 200:
            raise ValueError('Bounded audit page required')
        with self._tx(identity, case_id, None, P.AUDIT) as (db, _):
            previous, records = '0' * 64, []
            for row in db.execute('SELECT * FROM vault_audit ORDER BY sequence'):
                record = json.loads(row['record'])
                if (row['previous_hash'] != previous
                        or row['record_hash'] != digest({'previous_hash': previous, 'record': record})):
                    raise IntegrityError('Vault audit chain failed')
                previous = row['record_hash']
                if record['case_id'] == case_id and row['sequence'] > after and len(records) < limit:
                    records.append({'sequence': row['sequence'], **record, 'record_hash': row['record_hash']})
            return {'schema_version': 1, 'records': records, 'verified_local_chain': True,
                    'independently_anchored': False, 'next_after': records[-1]['sequence'] if records else after}
