"""Durable, narrowed collaboration grants with transaction-local authority checks."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import sqlite3

from ..authorisation import Identity
from ..store import Conflict, canonical, digest
from .contracts import Binding, GrantRequest


class Collaboration:
    def __init__(self, path, *, policy, cases, sources, clock=None):
        if any(adapter is None for adapter in (policy, cases, sources)):
            raise ValueError('Explicit current-policy, case and source adapters required')
        self.path, self.policy, self.cases, self.sources = str(path), policy, cases, sources
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def initialize(self):
        """Explicit lane-table migration; never invoked on import or construction."""
        with sqlite3.connect(self.path) as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS collaboration_grants (
                    id TEXT PRIMARY KEY, case_id TEXT NOT NULL, record TEXT NOT NULL,
                    digest TEXT NOT NULL, revoked INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE IF NOT EXISTS collaboration_audit (
                    sequence INTEGER PRIMARY KEY, record TEXT NOT NULL, digest TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS collaboration_projections (
                    id TEXT PRIMARY KEY, case_id TEXT NOT NULL, record TEXT NOT NULL,
                    digest TEXT NOT NULL, state TEXT NOT NULL, review TEXT);
            ''')

    def now(self):
        now = self.clock()
        if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
            raise PermissionError('An aware current clock is required')
        return now

    @contextmanager
    def transaction(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def binding(self, db, case_id, object_id=None):
        binding = self.cases.binding(db, case_id, object_id)
        if (not isinstance(binding, Binding) or binding.case_id != case_id
                or binding.resource.object_id != object_id):
            raise PermissionError('Case/object binding is not permitted')
        return binding

    def require(self, db, actor, binding, capability):
        if not isinstance(actor, Identity):
            raise PermissionError('Verified identity required')
        self.now()
        self.policy.require(db, actor, binding, capability)

    def current(self, db, binding, *, identity):
        if self.binding(db, binding.case_id, binding.resource.object_id) != binding:
            raise Conflict('Case, object or source revision changed; prepare a new review')
        self.sources.require_current(db, binding, identity=identity)

    def audit(self, db, *, actor, binding, kind, record_id):
        record = dict(actor=actor.model_dump(mode='json'), binding=binding.model_dump(mode='json'),
                      kind=kind, record_id=record_id, recorded_at=self.now().isoformat())
        db.execute('INSERT INTO collaboration_audit(record,digest) VALUES (?,?)',
                   (canonical(record), digest(record)))

    @staticmethod
    def checked(row):
        if row is None:
            raise KeyError('Collaboration record not found')
        record = json.loads(row['record'])
        if digest(record) != row['digest']:
            raise Conflict('Collaboration record integrity check failed')
        return record

    def grant_record(self, db, grant_id, case_id):
        row = db.execute('SELECT * FROM collaboration_grants WHERE id=? AND case_id=?',
                         (grant_id, case_id)).fetchone()
        return row, self.checked(row)

    def active(self, row, record, recipient, binding, *, purpose, projection_id=None):
        request = GrantRequest.model_validate(record['request'])
        scope = Binding.model_validate(record['binding'])
        now = self.now()
        if (row['revoked'] or request.recipient != recipient or request.purpose != purpose
                or request.projection_id != projection_id or scope.case_id != binding.case_id
                or scope.resource.organisation_id != binding.resource.organisation_id
                or scope.resource.matter_id != binding.resource.matter_id
                or (scope.resource.object_id is not None and scope.resource.object_id != binding.resource.object_id)
                or not request.valid_from <= now < request.expires_at):
            raise PermissionError('Current scoped collaboration grant required')

    def create_grant(self, *, actor, case_id, request: GrantRequest):
        if not isinstance(request, GrantRequest):
            raise ValueError('Typed grant request required')
        with self.transaction() as db:
            binding = self.binding(db, case_id, request.object_id)
            self.require(db, actor, binding, 'collaboration.manage')
            if request.expires_at <= self.now():
                raise ValueError('A new grant must not be expired')
            if request.purpose == 'client_projection':
                row = db.execute('SELECT * FROM collaboration_projections WHERE id=? AND case_id=?',
                                 (request.projection_id, case_id)).fetchone()
                projection = self.checked(row)
                if (row['state'] == 'withdrawn' or projection['recipient'] != request.recipient.model_dump(mode='json')
                        or projection['binding'] != binding.model_dump(mode='json')):
                    raise Conflict('Client grant must bind the exact current projection and recipient')
            record = dict(request=request.model_dump(mode='json'), binding=binding.model_dump(mode='json'),
                          granted_by=actor.model_dump(mode='json'))
            old = db.execute('SELECT * FROM collaboration_grants WHERE id=?', (request.id,)).fetchone()
            if old is not None:
                prior = self.checked(old)
                # Case revisions may move after an expert grant; its original scope stays immutable.
                if (old['case_id'] != case_id or prior['request'] != record['request']
                        or prior['granted_by'] != record['granted_by']
                        or Binding.model_validate(prior['binding']).resource != binding.resource):
                    raise Conflict('Grant ID already has a different request')
                if old['revoked']:
                    raise Conflict('A revoked grant cannot be revived')
                self.require(db, actor, binding, 'collaboration.manage')
                return dict(prior, revoked=False)
            self.current(db, binding, identity=actor)
            db.execute('INSERT INTO collaboration_grants VALUES (?,?,?,?,0)',
                       (request.id, case_id, canonical(record), digest(record)))
            self.audit(db, actor=actor, binding=binding, kind='grant_created', record_id=request.id)
            self.current(db, binding, identity=actor)
            self.require(db, actor, binding, 'collaboration.manage')
            return dict(record, revoked=False)

    def revoke_grant(self, *, actor, case_id, grant_id):
        with self.transaction() as db:
            row, record = self.grant_record(db, grant_id, case_id)
            old_binding = Binding.model_validate(record['binding'])
            binding = self.binding(db, case_id)
            if binding.resource != old_binding.resource.model_copy(update={'object_id': None}):
                raise PermissionError('Grant scope changed')
            self.require(db, actor, binding, 'collaboration.manage')
            if not row['revoked']:
                db.execute('UPDATE collaboration_grants SET revoked=1 WHERE id=?', (grant_id,))
                self.audit(db, actor=actor, binding=binding, kind='grant_revoked', record_id=grant_id)
            self.require(db, actor, binding, 'collaboration.manage')
            return {'id': grant_id, 'revoked': True}

    def grants(self, *, actor, case_id):
        with self.transaction() as db:
            binding = self.binding(db, case_id)
            self.require(db, actor, binding, 'collaboration.manage')
            rows = db.execute('SELECT * FROM collaboration_grants WHERE case_id=? ORDER BY rowid DESC LIMIT 200',
                              (case_id,)).fetchall()
            result = [dict(self.checked(row), revoked=bool(row['revoked'])) for row in rows]
            if any(Binding.model_validate(item['binding']).resource.model_copy(update={'object_id': None})
                   != binding.resource for item in result):
                raise PermissionError('Grant ownership changed')
            self.require(db, actor, binding, 'collaboration.manage')
            return result

    def expert_read(self, *, actor, case_id, object_id, grant_id):
        with self.transaction() as db:
            if object_id is None:
                raise PermissionError('Expert reads require an explicit object')
            binding = self.binding(db, case_id, object_id)
            self.require(db, actor, binding, 'collaboration.expert')
            row, record = self.grant_record(db, grant_id, case_id)
            self.active(row, record, actor, binding, purpose='expert')
            self.current(db, binding, identity=actor)
            view = self.cases.expert_view(db, binding)
            if not isinstance(view, dict) or len(canonical(view).encode('utf-8')) > 100000:
                raise ValueError('Expert object view exceeds its bounded contract')
            self.audit(db, actor=actor, binding=binding, kind='expert_read', record_id=grant_id)
            self.require(db, actor, binding, 'collaboration.expert')
            row, record = self.grant_record(db, grant_id, case_id)
            self.active(row, record, actor, binding, purpose='expert')
            self.current(db, binding, identity=actor)
            return {'binding': binding.model_dump(mode='json'), 'object': view, 'action_permission': False}
