"""Durable local change notices, not external sends or action authority.

The trusted host authenticates each reader. Pull and acknowledgement require
current whole-matter read access; delivery can repeat until acknowledged.
"""
import json

from ..agency_access import AccessRegistry
from ..authorisation import Grant, Identity, Operation, Resource, permits
from ..models import utcnow
from ..store import Conflict, canonical, digest


class EventOutbox:
    def __init__(self, store):
        self.store = store
        AccessRegistry(store.path)
        with store.connection() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS event_outbox (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    work_id TEXT NOT NULL UNIQUE,
                    case_id TEXT NOT NULL REFERENCES v2_cases(id),
                    body TEXT NOT NULL, digest TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS event_notice_delivery (
                    notice_id INTEGER NOT NULL REFERENCES event_outbox(id),
                    reader TEXT NOT NULL, first_read_at TEXT NOT NULL,
                    acknowledged_at TEXT,
                    PRIMARY KEY(notice_id,reader));
            ''')

    @staticmethod
    def _body(record):
        request = record['request']
        return dict(schema_version='endstate.reviewed-change.v1',
                    case_id=request['case_id'], work_id=request['work_id'],
                    organisation_id=request['organisation_id'], matter_id=request['matter_id'],
                    revision=record['committed_revision'], review_sha256=digest(record),
                    reviewed_at=record['reviewed_at'], command_authority=False)

    @staticmethod
    def append(db, record):
        """Called only inside the owning reviewed-case transaction."""
        request = record['request']
        body = EventOutbox._body(record)
        db.execute('INSERT INTO event_outbox(work_id,case_id,body,digest) VALUES (?,?,?,?)',
                   (request['work_id'], request['case_id'], canonical(body), digest(body)))

    @staticmethod
    def _authorize(db, case_id, reader):
        if not isinstance(reader, Identity):
            raise ValueError('Verified reader identity required')
        scope = db.execute('SELECT organisation_id,matter_id FROM agency_case_scope WHERE case_id=?',
                           (case_id,)).fetchone()
        grants = tuple(Grant.model_validate_json(row['body']) for row in
                       db.execute('SELECT body FROM agency_grants WHERE revoked=0'))
        if scope is None or not permits(reader, Resource(organisation_id=scope[0], matter_id=scope[1]),
                                        Operation.READ, grants, now=utcnow()):
            raise PermissionError('Current matter read permission is required')
        return digest(reader.model_dump(mode='json')), tuple(scope)

    @staticmethod
    def _verified(db, row, scope):
        body = json.loads(row['body'])
        if (digest(body) != row['digest'] or body['case_id'] != row['case_id']
                or body['work_id'] != row['work_id']
                or (body['organisation_id'], body['matter_id']) != scope
                or body['command_authority'] is not False):
            raise Conflict('Change notice failed verification')
        review = db.execute('SELECT record,digest FROM event_consumptions WHERE work_id=? AND case_id=?',
                            (row['work_id'], row['case_id'])).fetchone()
        if review is None or digest(json.loads(review['record'])) != review['digest'] or review['digest'] != body['review_sha256']:
            raise Conflict('Change notice is not bound to its review')
        if body != EventOutbox._body(json.loads(review['record'])):
            raise Conflict('Change notice metadata differs from its review')
        return dict(id=row['id'], **body)

    def pull(self, *, case_id, reader):
        """Return the oldest unacknowledged notice for this reader and case."""
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            reader_key, scope = self._authorize(db, case_id, reader)
            row = db.execute('''SELECT o.* FROM event_outbox o
                LEFT JOIN event_notice_delivery d ON d.notice_id=o.id AND d.reader=?
                WHERE o.case_id=? AND d.acknowledged_at IS NULL ORDER BY o.id LIMIT 1''',
                (reader_key, case_id)).fetchone()
            if row is None:
                return None
            notice = self._verified(db, row, scope)
            db.execute('INSERT OR IGNORE INTO event_notice_delivery VALUES (?,?,?,NULL)',
                       (row['id'], reader_key, utcnow().isoformat()))
            self._authorize(db, case_id, reader)
            db.commit()
            return notice

    def acknowledge(self, *, case_id, reader, notice_id):
        """Acknowledge local delivery only; never approve a case action."""
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            reader_key, scope = self._authorize(db, case_id, reader)
            row = db.execute('SELECT * FROM event_outbox WHERE id=? AND case_id=?',
                             (notice_id, case_id)).fetchone()
            delivery = db.execute('SELECT 1 FROM event_notice_delivery WHERE notice_id=? AND reader=?',
                                  (notice_id, reader_key)).fetchone()
            if row is None or delivery is None:
                raise Conflict('Read this case notice before acknowledging it')
            self._verified(db, row, scope)
            db.execute('''UPDATE event_notice_delivery SET acknowledged_at=COALESCE(acknowledged_at,?)
                WHERE notice_id=? AND reader=?''', (utcnow().isoformat(), notice_id, reader_key))
            self._authorize(db, case_id, reader)
            db.commit()
