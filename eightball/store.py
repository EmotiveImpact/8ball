"""Transactional local persistence and a verifiable application-level audit chain.

Not a substitute for production identity, encrypted storage or external audit anchoring.
"""
import hashlib
import json
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from .models import Situation, utcnow
from .commands import Command, apply
from .engine import plan, difference


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class Conflict(ValueError):
    pass


class Store:
    def __init__(self, path: str):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript('''
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS situations (id TEXT PRIMARY KEY, revision INTEGER NOT NULL, snapshot TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events (case_id TEXT NOT NULL REFERENCES situations(id), event_id TEXT NOT NULL,
                revision INTEGER NOT NULL, record TEXT NOT NULL, hash TEXT NOT NULL,
                PRIMARY KEY(case_id,event_id), UNIQUE(case_id,revision));
            ''')
        try:
            Path(path).chmod(0o600)
        except OSError:
            pass

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            yield db
        finally:
            db.close()

    def list(self):
        with self.connection() as db:
            return [Situation.model_validate_json(r['snapshot']) for r in db.execute('SELECT snapshot FROM situations ORDER BY rowid DESC')]

    def get(self, case_id):
        with self.connection() as db:
            row = db.execute('SELECT snapshot FROM situations WHERE id=?', (case_id,)).fetchone()
            if not row:
                raise KeyError(case_id)
            return Situation.model_validate_json(row['snapshot'])

    def _append(self, db, case, event_id, kind, payload, actor, request_hash):
        last = db.execute('SELECT hash FROM events WHERE case_id=? ORDER BY revision DESC LIMIT 1', (case.id,)).fetchone()
        record = {'case_id': case.id, 'event_id': event_id, 'revision': case.revision, 'kind': kind,
                  'payload': payload, 'actor': actor, 'recorded_at': utcnow().isoformat(),
                  'previous_hash': last['hash'] if last else None,
                  'state_hash': digest(case.model_dump(mode='json')), 'request_hash': request_hash}
        db.execute('INSERT INTO events VALUES (?,?,?,?,?)', (case.id, event_id, case.revision, canonical(record), digest(record)))

    def create(self, case: Situation, actor='local-operator'):
        if case.revision != 0 or case.approvals or case.completed or case.evidence or case.observations:
            raise ValueError('New situations must begin without imported attestations or approvals')
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                db.execute('INSERT INTO situations VALUES (?,?,?)', (case.id, 0, case.model_dump_json()))
                self._append(db, case, 'created', 'created', case.model_dump(mode='json'), actor, None)
                db.commit()
            except Exception:
                db.rollback()
                raise
        return case

    def change(self, case_id: str, command: Command, actor='local-operator'):
        request_hash = digest(command.model_dump(mode='json'))
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                row = db.execute('SELECT snapshot FROM situations WHERE id=?', (case_id,)).fetchone()
                if not row:
                    raise KeyError(case_id)
                case = Situation.model_validate_json(row['snapshot'])
                previous = db.execute('SELECT record FROM events WHERE case_id=? AND event_id=?', (case_id, command.event_id)).fetchone()
                if previous:
                    if json.loads(previous['record'])['request_hash'] != request_hash:
                        raise Conflict('Idempotency key was already used for a different command')
                    db.rollback()
                    return case, {'duplicate': True}
                if case.revision != command.expected_revision:
                    raise Conflict('Situation changed. Reload before making this decision.')
                if case.revision >= 2000:
                    raise ValueError('Local alpha event limit reached; export the case')
                now = utcnow()
                before = plan(case, now)
                updated = apply(case, command)
                after = plan(updated, now)
                db.execute('UPDATE situations SET revision=?,snapshot=? WHERE id=?', (updated.revision, updated.model_dump_json(), case_id))
                self._append(db, updated, command.event_id, command.kind, command.payload, actor, request_hash)
                db.commit()
                return updated, difference(before, after)
            except Exception:
                db.rollback()
                raise

    def audit(self, case_id):
        # Read snapshot and chain in one transaction so concurrent writes cannot produce a false mismatch.
        with self.connection() as db:
            db.execute('BEGIN')
            row = db.execute('SELECT snapshot FROM situations WHERE id=?', (case_id,)).fetchone()
            if not row:
                raise KeyError(case_id)
            case = Situation.model_validate_json(row['snapshot'])
            rows = db.execute('SELECT record,hash FROM events WHERE case_id=? ORDER BY revision', (case_id,)).fetchall()
            db.rollback()
        prev, valid, events = None, True, []
        for rev, r in enumerate(rows):
            record = json.loads(r['record'])
            valid = valid and record['revision'] == rev and record['previous_hash'] == prev and digest(record) == r['hash']
            events.append({**record, 'hash': r['hash']})
            prev = r['hash']
        valid = bool(valid and events and len(events) == case.revision + 1 and events[-1]['state_hash'] == digest(case.model_dump(mode='json')))
        return {'valid': valid, 'head_hash': prev, 'events': events, 'case': case.model_dump(mode='json')}
