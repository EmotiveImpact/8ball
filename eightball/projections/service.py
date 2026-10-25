"""Exact-content, exact-recipient disclosure review; no delivery or case mutation."""
import json
from typing import Literal

from pydantic import Field, model_validator

from ..authorisation import Identity
from ..collaboration.contracts import Binding, Record
from ..store import Conflict, canonical, digest


class ClientStatement(Record):
    text: str = Field(min_length=1, max_length=3000)
    evidence_state: Literal['unknown', 'unverified', 'source_supported', 'disputed'] = 'unknown'


class ClientContent(Record):
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=6000)
    statements: tuple[ClientStatement, ...] = Field(default=(), max_length=30)


class DraftRequest(Record):
    id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,100}$')
    expected_binding: Binding
    recipient: Identity
    content: ClientContent

    @model_validator(mode='after')
    def object_scope(self):
        if self.expected_binding.resource.object_id is None:
            raise ValueError('Client projection requires a specific object')
        if len(canonical(self.content.model_dump(mode='json')).encode('utf-8')) > 50000:
            raise ValueError('Client projection exceeds 50000 UTF-8 bytes')
        return self


class ReviewRequest(Record):
    expected_digest: str = Field(pattern=r'^[0-9a-f]{64}$')
    grant_id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,100}$')
    rationale: str = Field(min_length=10, max_length=2000)


class Projections:
    def __init__(self, collaboration):
        self.host = collaboration

    def record(self, db, case_id, object_id, projection_id):
        row = db.execute('SELECT * FROM collaboration_projections WHERE id=? AND case_id=?',
                         (projection_id, case_id)).fetchone()
        record = self.host.checked(row)
        binding = Binding.model_validate(record['binding'])
        if binding.resource.object_id != object_id or binding.case_id != case_id:
            raise PermissionError('Projection does not belong to this object')
        live = self.host.binding(db, case_id, object_id)
        if live.resource != binding.resource:
            raise PermissionError('Projection ownership changed')
        return row, record, binding

    def authorized_record(self, db, actor, case_id, object_id, projection_id, capability):
        binding = self.host.binding(db, case_id, object_id)
        self.host.require(db, actor, binding, capability)
        return self.record(db, case_id, object_id, projection_id)

    def draft(self, *, actor, case_id, object_id, request: DraftRequest):
        host = self.host
        if not isinstance(request, DraftRequest):
            raise ValueError('Typed projection draft required')
        with host.transaction() as db:
            binding = host.binding(db, case_id, object_id)
            host.require(db, actor, binding, 'projection.draft')
            if binding != request.expected_binding:
                raise Conflict('Draft requires the exact current case/object/source revision')
            if actor == request.recipient:
                raise PermissionError('Internal authors cannot assign themselves client access')
            host.current(db, binding, identity=actor)
            record = dict(binding=binding.model_dump(mode='json'), recipient=request.recipient.model_dump(mode='json'),
                          content=request.content.model_dump(mode='json'), author=actor.model_dump(mode='json'),
                          id=request.id)
            old = db.execute('SELECT * FROM collaboration_projections WHERE id=?', (request.id,)).fetchone()
            if old is not None:
                if host.checked(old) != record or old['state'] == 'withdrawn':
                    raise Conflict('Projection ID is already used or withdrawn; create a new draft')
                host.require(db, actor, binding, 'projection.draft')
                return self.internal(old)
            db.execute('INSERT INTO collaboration_projections VALUES (?,?,?,?,?,NULL)',
                       (request.id, case_id, canonical(record), digest(record), 'draft'))
            host.audit(db, actor=actor, binding=binding, kind='projection_drafted', record_id=request.id)
            host.current(db, binding, identity=actor)
            host.require(db, actor, binding, 'projection.draft')
            return self.internal(db.execute('SELECT * FROM collaboration_projections WHERE id=?', (request.id,)).fetchone())

    def internal(self, row):
        record = self.host.checked(row)
        return dict(record, digest=row['digest'], state=row['state'], review=self.review_record(row),
                    action_permission=False, external_send=False)

    @staticmethod
    def review_record(row):
        if row['review'] is None:
            if row['state'] == 'reviewed':
                raise Conflict('Projection review is missing')
            return None
        review = json.loads(row['review'])
        if (set(review) != {'record', 'digest'} or digest(review['record']) != review['digest']
                or review['record']['projection_digest'] != row['digest']):
            raise Conflict('Projection review integrity check failed')
        return review['record']

    def inspect(self, *, actor, case_id, object_id, projection_id):
        host = self.host
        with host.transaction() as db:
            row, record, binding = self.authorized_record(db, actor, case_id, object_id, projection_id, 'projection.inspect')
            host.require(db, actor, binding, 'projection.inspect')
            result = self.internal(row)
            result['stale'] = host.binding(db, case_id, object_id) != binding
            host.require(db, actor, binding, 'projection.inspect')
            return result

    def review(self, *, actor, case_id, object_id, projection_id, request: ReviewRequest):
        host = self.host
        if not isinstance(request, ReviewRequest) or len(request.rationale.strip()) < 10:
            raise ValueError('Typed exact review and meaningful rationale required')
        with host.transaction() as db:
            row, record, binding = self.authorized_record(db, actor, case_id, object_id, projection_id, 'projection.review')
            host.require(db, actor, binding, 'projection.review')
            host.current(db, binding, identity=actor)
            if actor == Identity.model_validate(record['author']) or actor == Identity.model_validate(record['recipient']):
                raise PermissionError('A separate internal reviewer must review client disclosure')
            if row['state'] == 'withdrawn' or row['digest'] != request.expected_digest:
                raise Conflict('Projection is withdrawn or the reviewed digest is stale')
            recipient = Identity.model_validate(record['recipient'])
            grant, grant_record = host.grant_record(db, request.grant_id, case_id)
            host.active(grant, grant_record, recipient, binding, purpose='client_projection', projection_id=projection_id)
            review = dict(projection_digest=row['digest'], grant_id=request.grant_id,
                          grant_digest=grant['digest'], reviewer=actor.model_dump(mode='json'), rationale=request.rationale)
            prior = self.review_record(row)
            if prior is not None:
                if {key: prior[key] for key in review} != review:
                    raise Conflict('This projection has a different review')
                host.require(db, actor, binding, 'projection.review')
                return self.internal(row)
            review['reviewed_at'] = host.now().isoformat()
            db.execute("UPDATE collaboration_projections SET state='reviewed',review=? WHERE id=?",
                       (canonical(dict(record=review, digest=digest(review))), projection_id))
            host.audit(db, actor=actor, binding=binding, kind='projection_reviewed', record_id=projection_id)
            host.current(db, binding, identity=actor)
            host.require(db, actor, binding, 'projection.review')
            grant, grant_record = host.grant_record(db, request.grant_id, case_id)
            host.active(grant, grant_record, recipient, binding, purpose='client_projection', projection_id=projection_id)
            return self.internal(db.execute('SELECT * FROM collaboration_projections WHERE id=?', (projection_id,)).fetchone())

    def withdraw(self, *, actor, case_id, object_id, projection_id):
        host = self.host
        with host.transaction() as db:
            row, record, binding = self.authorized_record(db, actor, case_id, object_id, projection_id, 'projection.withdraw')
            host.require(db, actor, binding, 'projection.withdraw')
            if row['state'] != 'withdrawn':
                db.execute("UPDATE collaboration_projections SET state='withdrawn' WHERE id=?", (projection_id,))
                host.audit(db, actor=actor, binding=binding, kind='projection_withdrawn', record_id=projection_id)
            host.require(db, actor, binding, 'projection.withdraw')
            return {'id': projection_id, 'state': 'withdrawn', 'external_cancellation': False}

    def client_read(self, *, actor, case_id, object_id, projection_id):
        host = self.host
        with host.transaction() as db:
            row, record, binding = self.authorized_record(db, actor, case_id, object_id, projection_id, 'projection.client')
            host.require(db, actor, binding, 'projection.client')
            if actor != Identity.model_validate(record['recipient']) or row['state'] != 'reviewed':
                raise PermissionError('A separately reviewed projection for this client is required')
            review = self.review_record(row)
            reviewer = Identity.model_validate(review['reviewer'])
            host.require(db, reviewer, binding, 'projection.review')
            host.current(db, binding, identity=reviewer)
            grant, grant_record = host.grant_record(db, review['grant_id'], case_id)
            host.active(grant, grant_record, actor, binding, purpose='client_projection', projection_id=projection_id)
            if grant['digest'] != review['grant_digest']:
                raise Conflict('Reviewed grant changed')
            # Deliberate allowlist: never return binding, handles, authors or review rationale.
            result = dict(id=projection_id, content=ClientContent.model_validate(record['content']).model_dump(mode='json'),
                          reviewed_at=review['reviewed_at'], action_permission=False, external_send=False)
            host.audit(db, actor=actor, binding=binding, kind='projection_read', record_id=projection_id)
            host.current(db, binding, identity=reviewer)
            host.require(db, actor, binding, 'projection.client')
            host.require(db, reviewer, binding, 'projection.review')
            grant, grant_record = host.grant_record(db, review['grant_id'], case_id)
            host.active(grant, grant_record, actor, binding, purpose='client_projection', projection_id=projection_id)
            return result
