"""Transactional operations records, deliberately separate from case commands.

Host authority/probe adapters must use the supplied transaction, not cached grants.
No callback may send, retry, change case state or restore an operator database.
"""
from contextlib import closing, contextmanager
from datetime import datetime, timezone
import json
import sqlite3
from uuid import uuid4

from eightball.authorisation import Identity
from eightball.store import canonical, digest
from .contracts import Authority, OpenRecord, Scope, SURFACES, Transition, VerifyRevocation


class OperationsConflict(ValueError):
    pass


class OperationsUnavailable(RuntimeError):
    pass


SCHEMA = '''
CREATE TABLE IF NOT EXISTS ops_records (
    organisation_id TEXT NOT NULL, matter_id TEXT NOT NULL, case_id TEXT NOT NULL,
    id TEXT NOT NULL, revision INTEGER NOT NULL, body TEXT NOT NULL,
    PRIMARY KEY (organisation_id,matter_id,case_id,id));
CREATE TABLE IF NOT EXISTS ops_journal (
    organisation_id TEXT NOT NULL, matter_id TEXT NOT NULL, case_id TEXT NOT NULL,
    sequence INTEGER NOT NULL, body TEXT NOT NULL, hash TEXT NOT NULL,
    PRIMARY KEY (organisation_id,matter_id,case_id,sequence));
CREATE TABLE IF NOT EXISTS ops_requests (
    organisation_id TEXT NOT NULL, matter_id TEXT NOT NULL, case_id TEXT NOT NULL,
    actor_hash TEXT NOT NULL, request_id TEXT NOT NULL, request_hash TEXT NOT NULL,
    response TEXT NOT NULL,
    PRIMARY KEY (organisation_id,matter_id,case_id,actor_hash,request_id));
'''


def initialize(path):
    """Explicit proposed lane migration. Integration must approve before use."""
    with closing(sqlite3.connect(path)) as db:
        db.executescript(SCHEMA)


class Operations:
    def __init__(self, path, *, authority: Authority, probe=None, clock=None):
        self.path, self.authority, self.probe = str(path), authority, probe
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    @contextmanager
    def _transaction(self, identity, scope, operation):
        if not isinstance(identity, Identity) or not isinstance(scope, Scope):
            raise PermissionError('Access is not permitted')
        with closing(sqlite3.connect(self.path, timeout=10)) as db, db:
            db.row_factory = sqlite3.Row
            db.execute('BEGIN IMMEDIATE')
            self._authorize(db, identity, scope, operation)
            yield db
            self._authorize(db, identity, scope, operation)

    def _now(self):
        now = self.clock()
        if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
            raise ValueError('An aware host clock is required')
        return now

    def _authorize(self, db, identity, scope, operation):
        try:
            allowed = self.authority(db, identity, scope, operation, self._now())
        except Exception:
            raise PermissionError('Access is not permitted') from None
        if allowed is not True:
            raise PermissionError('Access is not permitted')

    @staticmethod
    def _scope(scope):
        return (scope.organisation_id, scope.matter_id, scope.case_id)

    def _history(self, db, scope):
        rows = db.execute('''SELECT sequence,body,hash FROM ops_journal
            WHERE organisation_id=? AND matter_id=? AND case_id=? ORDER BY sequence''',
            self._scope(scope)).fetchall()
        previous, events, snapshots = None, [], {}
        for sequence, row in enumerate(rows, 1):
            try:
                body = json.loads(row['body'])
                valid = (row['sequence'] == sequence and body['sequence'] == sequence
                         and body['scope'] == scope.model_dump()
                         and body['previous_hash'] == previous and digest(body) == row['hash'])
                snapshot = body['record']
                old = snapshots.get(snapshot['id'])
                valid = valid and snapshot['revision'] == (old['revision'] + 1 if old else 0)
                if not valid:
                    raise ValueError
                snapshots[snapshot['id']] = snapshot
                previous = row['hash']
                events.append({**body, 'hash': previous})
            except (ValueError, KeyError, TypeError):
                raise OperationsConflict('Operations journal failed verification') from None
        persisted = db.execute('''SELECT id,revision,body FROM ops_records
            WHERE organisation_id=? AND matter_id=? AND case_id=?''', self._scope(scope)).fetchall()
        try:
            actual = {r['id']: json.loads(r['body']) for r in persisted}
            if (actual != snapshots or any(r['revision'] != actual[r['id']]['revision'] for r in persisted)):
                raise ValueError
        except (ValueError, KeyError, TypeError):
            raise OperationsConflict('Operations snapshot failed verification') from None
        return events, snapshots

    def _command(self, identity, scope, operation, request, record_id, change):
        actor_hash = digest(identity.model_dump())
        request_hash = digest({'operation': operation, 'record_id': record_id,
                               'body': request.model_dump()})
        with self._transaction(identity, scope, operation) as db:
            events, snapshots = self._history(db, scope)
            old = db.execute('''SELECT request_hash,response FROM ops_requests WHERE
                organisation_id=? AND matter_id=? AND case_id=? AND actor_hash=? AND request_id=?''',
                (*self._scope(scope), actor_hash, request.request_id)).fetchone()
            if old:
                if old['request_hash'] != request_hash:
                    raise OperationsConflict('Idempotency key has different content')
                response = json.loads(old['response'])
                if not any(e.get('request_hash') == request_hash
                           and e['actor_hash'] == actor_hash
                           and e.get('request_id') == request.request_id
                           and e['record'] == response for e in events):
                    raise OperationsConflict('Idempotency receipt failed verification')
                return response
            record = change(db, snapshots)
            body = {'sequence': len(events) + 1, 'scope': scope.model_dump(),
                    'actor_hash': actor_hash, 'operation': operation,
                    'request_hash': request_hash, 'request_id': request.request_id,
                    'recorded_at': self._now().isoformat(), 'record': record,
                    'previous_hash': events[-1]['hash'] if events else None}
            db.execute('INSERT INTO ops_journal VALUES (?,?,?,?,?,?)',
                       (*self._scope(scope), body['sequence'], canonical(body), digest(body)))
            db.execute('''INSERT INTO ops_records VALUES (?,?,?,?,?,?)
                ON CONFLICT (organisation_id,matter_id,case_id,id)
                DO UPDATE SET revision=excluded.revision,body=excluded.body''',
                       (*self._scope(scope), record['id'], record['revision'], canonical(record)))
            db.execute('INSERT INTO ops_requests VALUES (?,?,?,?,?,?,?)',
                       (*self._scope(scope), actor_hash, request.request_id, request_hash, canonical(record)))
            return record

    def open(self, identity, scope, request: OpenRecord):
        if (request.kind == 'revocation') != (request.target_id is not None):
            raise ValueError('A revocation requires exactly one target handle')

        def change(db, snapshots):
            return {'id': uuid4().hex, 'revision': 0, 'state': 'open',
                    **request.model_dump(exclude={'request_id'}), 'checks': {}}
        return self._command(identity, scope, 'operations.open', request, None, change)

    @staticmethod
    def _record(snapshots, record_id, revision):
        record = snapshots.get(record_id)
        if record is None:
            raise KeyError('Operations record not found')
        if record['revision'] != revision:
            raise OperationsConflict('Operations revision is stale')
        return record

    def transition(self, identity, scope, record_id, request: Transition):
        def change(db, snapshots):
            record = self._record(snapshots, record_id, request.expected_revision)
            allowed = {'open': {'investigating', 'cancelled'},
                       'investigating': {'contained', 'cancelled'}, 'contained': {'resolved'},
                       'resolved': {'closed'}, 'closed': set(), 'cancelled': set()}
            if request.state not in allowed[record['state']]:
                raise OperationsConflict('Transition is not permitted')
            if request.state in ('contained', 'resolved', 'closed') and request.evidence_sha256 is None:
                raise OperationsConflict('Mitigation or review evidence is required')
            if record['kind'] == 'revocation' and request.state == 'closed':
                # Never close from historical probe observations.
                record = {**record, 'checks': self._probes(db, scope, record)}
                if any(v != 'denied' for v in record['checks'].values()):
                    raise OperationsConflict('Revocation is not established on every surface')
            return {**record, 'state': request.state, 'revision': record['revision'] + 1,
                    'evidence_sha256': request.evidence_sha256 or record['evidence_sha256']}
        return self._command(identity, scope, 'operations.transition', request, record_id, change)

    def _probes(self, db, scope, record):
        checks = {}
        for surface in SURFACES:
            try:
                result = self.probe(db, scope, record['target_id'], surface) if self.probe else 'unavailable'
            except Exception:
                raise OperationsUnavailable('Revocation probe unavailable') from None
            if result not in ('denied', 'access_still_allowed', 'unavailable'):
                raise OperationsConflict('Invalid revocation probe result')
            checks[surface] = result
        return checks

    def verify_revocation(self, identity, scope, record_id, request: VerifyRevocation):
        def change(db, snapshots):
            record = self._record(snapshots, record_id, request.expected_revision)
            if record['kind'] != 'revocation' or record['state'] in ('closed', 'cancelled'):
                raise OperationsConflict('Record is not an active revocation check')
            return {**record, 'checks': self._probes(db, scope, record),
                    'revision': record['revision'] + 1}
        return self._command(identity, scope, 'operations.verify_revocation', request, record_id, change)

    def view(self, identity, scope):
        with self._transaction(identity, scope, 'operations.read') as db:
            events, snapshots = self._history(db, scope)
            return {'scope': scope.model_dump(), 'records': list(snapshots.values()),
                    'sequence': len(events), 'head_hash': events[-1]['hash'] if events else None,
                    'valid': True, 'independently_anchored': False,
                    'action_permission': False, 'production_accepted': False}
