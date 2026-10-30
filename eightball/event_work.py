"""Explicit local event-processing attempts; no automatic execution or retry.

Trusted host callers supply verified scope/revision/permission observations.
Results are pending review, never case changes or execution authorisations.
"""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import secrets
import sqlite3
from uuid import uuid4

from .event_inbox import EventInbox, EventConflict

# Match the supported hosted response envelope bound without importing a
# provider adapter. Count actual UTF-8 bytes, never silently truncate output.
MAX_RESULT_BYTES = 500_000


class EventWork:
    def __init__(self, path, *, clock=None):
        self.path = str(path)
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        EventInbox(path)
        with self._transaction() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS event_work (
                id TEXT PRIMARY KEY, organisation_id TEXT NOT NULL, matter_id TEXT NOT NULL,
                sequence INTEGER NOT NULL, base_revision INTEGER NOT NULL,
                state TEXT NOT NULL, token_hash TEXT, deadline TEXT, result TEXT,
                created_at TEXT NOT NULL, finished_at TEXT,
                FOREIGN KEY(organisation_id,matter_id,sequence)
                    REFERENCES incoming_events(organisation_id,matter_id,sequence))''')
            if 'case_id' not in {row['name'] for row in db.execute('PRAGMA table_info(event_work)')}:
                # Historical attempts have unknown case identity. Preserve them
                # unbound; never infer a case from a coincidentally equal revision.
                db.execute('ALTER TABLE event_work ADD COLUMN case_id TEXT')

    @contextmanager
    def _transaction(self, db=None):
        if db is not None:
            if not db.in_transaction:
                raise ValueError('An owning transaction is required')
            yield db
            return
        with sqlite3.connect(self.path, timeout=10) as db:
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('BEGIN IMMEDIATE')
            yield db

    def _now(self):
        now = self.clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError('A timezone-aware host clock is required')
        return now

    @staticmethod
    def _row(db, scope, work_id):
        row = db.execute('''SELECT * FROM event_work WHERE id=?
            AND organisation_id=? AND matter_id=?''', (work_id, *scope)).fetchone()
        if row is None:
            raise KeyError(work_id)
        return row

    def enqueue(self, *, organisation_id, matter_id, sequence, base_revision, case_id=None, _db=None):
        if type(sequence) is not int or sequence < 1 or type(base_revision) is not int or base_revision < 0:
            raise ValueError('Explicit event sequence and base revision required')
        with self._transaction(_db) as db:
            if case_id is not None:
                if not isinstance(case_id, str) or not case_id or len(case_id) > 100:
                    raise ValueError('Explicit case identity required')
                tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                if not {'agency_case_scope', 'v2_cases'} <= tables:
                    raise EventConflict('Case processing requires a bound case database')
                bound = db.execute('''SELECT 1 FROM agency_case_scope s JOIN v2_cases c ON c.id=s.case_id
                    WHERE s.case_id=? AND s.organisation_id=? AND s.matter_id=?''',
                    (case_id, organisation_id, matter_id)).fetchone()
                if bound is None:
                    raise EventConflict('Case does not belong to the processing scope')
            # Verify the source bytes and scope before admitting a new attempt.
            row = db.execute('''SELECT sequence,received_at,body,digest FROM incoming_events
                WHERE organisation_id=? AND matter_id=? AND sequence=?''',
                (organisation_id, matter_id, sequence)).fetchone()
            if row is None:
                raise KeyError(sequence)
            receipt = EventInbox._receipt(tuple(row))
            if (receipt.event.organisation_id, receipt.event.matter_id) != (organisation_id, matter_id):
                raise EventConflict('Event scope mismatch')
            if receipt.event.base_revision is not None and receipt.event.base_revision != base_revision:
                raise EventConflict('Event base revision mismatch')
            work_id = uuid4().hex
            db.execute('''INSERT INTO event_work
                       (id,organisation_id,matter_id,sequence,base_revision,state,created_at,case_id)
                       VALUES (?,?,?,?,?,?,?,?)''',
                       (work_id, organisation_id, matter_id, sequence, base_revision,
                        'queued', self._now().isoformat(), case_id))
            return work_id

    def claim(self, work_id, *, organisation_id, matter_id, lease_seconds=60, _db=None):
        if type(lease_seconds) is not int or not 1 <= lease_seconds <= 600:
            raise ValueError('Lease must be between one and 600 seconds')
        with self._transaction(_db) as db:
            row = self._row(db, (organisation_id, matter_id), work_id)
            if row['state'] != 'queued':
                raise EventConflict('This attempt cannot be claimed again')
            token = secrets.token_urlsafe(32)
            db.execute('UPDATE event_work SET state=?,token_hash=?,deadline=? WHERE id=?',
                       ('running', sha256(token.encode()).hexdigest(),
                        (self._now()+timedelta(seconds=lease_seconds)).isoformat(), work_id))
            return token

    def finish(self, work_id, token, result, *, organisation_id, matter_id,
               current_revision, permission_valid, _db=None):
        if not isinstance(result, str) or not result or len(result.encode('utf-8')) > MAX_RESULT_BYTES:
            raise ValueError('A bounded result text is required')
        if type(current_revision) is not int or current_revision < 0 or type(permission_valid) is not bool:
            raise ValueError('Explicit host revision and permission observations required')
        with self._transaction(_db) as db:
            row = self._row(db, (organisation_id, matter_id), work_id)
            if row['state'] != 'running' or not isinstance(token, str) or not secrets.compare_digest(
                    row['token_hash'], sha256(token.encode()).hexdigest()):
                raise EventConflict('This attempt cannot publish a result')
            now = self._now()
            state = ('interrupted' if now >= datetime.fromisoformat(row['deadline']) else
                     'permission_denied' if not permission_valid else
                     'stale' if current_revision != row['base_revision'] else 'awaiting_review')
            db.execute('UPDATE event_work SET state=?,result=?,finished_at=?,token_hash=NULL WHERE id=?',
                       (state, result, now.isoformat(), work_id))
            return state

    def cancel(self, work_id, *, organisation_id, matter_id, _db=None):
        with self._transaction(_db) as db:
            row = self._row(db, (organisation_id, matter_id), work_id)
            if row['state'] == 'cancelled':
                return
            if row['state'] not in ('queued', 'running', 'awaiting_review'):
                raise EventConflict('Attempt is already terminal')
            db.execute('UPDATE event_work SET state=?,token_hash=NULL,finished_at=? WHERE id=?',
                       ('cancelled', self._now().isoformat(), work_id))

    def inspect(self, work_id, *, organisation_id, matter_id, _db=None):
        with self._transaction(_db) as db:
            row = self._row(db, (organisation_id, matter_id), work_id)
            if row['state'] == 'running' and self._now() >= datetime.fromisoformat(row['deadline']):
                db.execute('UPDATE event_work SET state=?,token_hash=NULL,finished_at=? WHERE id=?',
                           ('interrupted', self._now().isoformat(), work_id))
                row = self._row(db, (organisation_id, matter_id), work_id)
            return {key: row[key] for key in row.keys() if key != 'token_hash'}
