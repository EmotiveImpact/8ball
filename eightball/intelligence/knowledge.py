"""Transactional review/reference seam with injected current-authority adapters.

The embedding application owns transactions, identity, immutable source access
and case revisions. Schema creation is explicit, never an import side effect.
"""
from contextlib import AbstractContextManager
from dataclasses import dataclass
import json
import re
import sqlite3
from typing import Callable

from endstate.intelligence.knowledge import (
    KnowledgeContext, KnowledgeDraft, KnowledgeReview, NOTICES, content_digest,
)
from endstate.primitives import Identifier, utcnow
from pydantic import TypeAdapter


SCHEMA = (
    '''CREATE TABLE intelligence_knowledge_events (
        organisation_id TEXT NOT NULL, matter_id TEXT NOT NULL, case_id TEXT NOT NULL,
        revision INTEGER NOT NULL, item_id TEXT NOT NULL, actor_id TEXT NOT NULL,
        request_id TEXT NOT NULL, request_sha256 TEXT NOT NULL, event_json TEXT NOT NULL,
        PRIMARY KEY (organisation_id, matter_id, case_id, revision),
        UNIQUE (organisation_id, matter_id, case_id, actor_id, request_id))''',
)


class KnowledgeConflict(ValueError):
    """A stale revision, changed request or changed source requires human reload."""


class KnowledgeUnavailable(ValueError):
    """Missing/retracted/changed source; never expose its body in an error."""


@dataclass(frozen=True)
class SourceSnapshot:
    text: str
    active: bool


Transaction = Callable[[], AbstractContextManager[sqlite3.Connection]]


class KnowledgeService:
    def __init__(self, transaction: Transaction, *, authorise, resolve_source,
                 case_revision, clock=utcnow):
        self.transaction = transaction
        self.authorise = authorise
        self.resolve_source = resolve_source
        self.case_revision = case_revision
        self.clock = clock

    def _scope(self, context):
        c = KnowledgeContext.model_validate(context)
        return c, (c.organisation_id, c.matter_id, c.case_id)

    def _permit(self, conn, context, operation, item_id):
        if self.authorise(conn, context, operation, item_id) is not True:
            raise PermissionError('Current knowledge permission required')

    def _rows(self, conn, scope):
        return [json.loads(row[0]) for row in conn.execute(
            'SELECT event_json FROM intelligence_knowledge_events '
            'WHERE organisation_id=? AND matter_id=? AND case_id=? ORDER BY revision', scope)]

    def _support(self, conn, context, draft):
        for support in draft.sources:
            source = self.resolve_source(conn, context, support.source_id)
            if (not isinstance(source, SourceSnapshot) or source.active is not True
                    or not isinstance(source.text, str)
                    or content_digest_text(source.text) != support.sha256
                    or source.text[support.start:support.end] != support.quote):
                raise KnowledgeUnavailable('Source support is no longer available unchanged')

    def _current(self, rows, item_id):
        history = [row for row in rows if row['item_id'] == item_id]
        drafts = [row for row in history if row['operation'] == 'draft']
        if not drafts:
            raise KnowledgeUnavailable('Reference is not available')
        latest = drafts[-1]
        reviews = [row for row in history if row['operation'] == 'review'
                   and row['version'] == latest['version']]
        return latest, reviews

    def _view(self, rows, item_id):
        latest, reviews = self._current(rows, item_id)
        return {**latest, 'reviews': reviews,
                'review_status': reviews[-1]['review']['verdict'] if reviews else 'unreviewed',
                'factual_verification': False, 'action_approved': False}

    def _case_revision(self, conn, context):
        revision = self.case_revision(conn, context)
        if type(revision) is not int or revision < 0:
            raise KnowledgeUnavailable('Current case revision is not available')
        return revision

    def _revision(self, conn, context, expected):
        if self._case_revision(conn, context) != expected:
            raise KnowledgeConflict('Case changed; reload before reviewing references')

    def write(self, context, *, item_id: str, expected_revision: int,
              expected_case_revision: int, request_id: str,
              draft: KnowledgeDraft | None = None, review: KnowledgeReview | None = None,
              retire: bool = False):
        c, scope = self._scope(context)
        identifier = TypeAdapter(Identifier)
        item_id, request_id = identifier.validate_python(item_id), identifier.validate_python(request_id)
        if (type(expected_revision) is not int or expected_revision < 0
                or type(expected_case_revision) is not int or expected_case_revision < 0):
            raise ValueError('Nonnegative exact revisions required')
        if sum((draft is not None, review is not None, retire is True)) != 1 or type(retire) is not bool:
            raise ValueError('Choose one explicit knowledge operation')
        draft = KnowledgeDraft.model_validate(draft.model_dump() if isinstance(draft, KnowledgeDraft) else draft) if draft is not None else None
        review = KnowledgeReview.model_validate(review.model_dump() if isinstance(review, KnowledgeReview) else review) if review is not None else None
        operation = 'draft' if draft else 'review' if review else 'retire'
        payload = (draft or review).model_dump(mode='json') if draft or review else None
        fingerprint = content_digest({'item_id': item_id, 'operation': operation, 'payload': payload,
                                      'revision': expected_revision, 'case_revision': expected_case_revision})
        with self.transaction() as conn:
            self._permit(conn, c, 'knowledge.' + operation, item_id)
            rows = self._rows(conn, scope)
            duplicate = conn.execute(
                'SELECT request_sha256, event_json FROM intelligence_knowledge_events '
                'WHERE organisation_id=? AND matter_id=? AND case_id=? AND actor_id=? AND request_id=?',
                (*scope, c.actor_id, request_id)).fetchone()
            if duplicate:
                if duplicate[0] != fingerprint:
                    raise KnowledgeConflict('Request ID already used for different content')
                event = json.loads(duplicate[1])
                # Idempotency is not a capability to retrieve revoked or stale source text.
                self._revision(conn, c, expected_case_revision)
                history = [r for r in rows if r['item_id'] == item_id]
                for row in history if operation != 'retire' else []:
                    if row['operation'] == 'draft':
                        self._support(conn, c, KnowledgeDraft.model_validate(row['draft']))
                self._permit(conn, c, 'knowledge.' + operation, item_id)
                return event
            self._revision(conn, c, expected_case_revision)
            if expected_revision != len(rows):
                raise KnowledgeConflict('Knowledge changed; reload before writing')
            if len(rows) >= 500 and operation != 'retire':
                raise KnowledgeConflict('Local reference history limit reached')
            history = [r for r in rows if r['item_id'] == item_id]
            if history and history[-1]['operation'] == 'retire':
                raise KnowledgeConflict('Retired references cannot be revived')
            latest = self._current(rows, item_id)[0] if history else None
            if draft:
                if latest and draft.kind != latest['draft']['kind']:
                    raise KnowledgeConflict('Reference kind is immutable')
                self._support(conn, c, draft)
                version = latest['version'] + 1 if latest else 1
            else:
                if latest is None:
                    raise KnowledgeUnavailable('Reference is not available')
                version = latest['version']
                if review:
                    self._support(conn, c, KnowledgeDraft.model_validate(latest['draft']))
                if review and (review.version != version or review.draft_sha256 != latest['draft_sha256']):
                    raise KnowledgeConflict('Review must name the exact current draft version and digest')
                if review and latest['actor_id'] == c.actor_id:
                    raise PermissionError('Draft authors cannot review their own version')
            event = {'item_id': item_id, 'operation': operation, 'version': version,
                     'revision': len(rows) + 1, 'case_revision': expected_case_revision,
                     'scope': dict(zip(('organisation_id', 'matter_id', 'case_id'), scope)),
                     'actor_id': c.actor_id, 'recorded_at': self.clock().isoformat()}
            if draft:
                event.update(draft=payload, draft_sha256=content_digest(payload))
            if review:
                event['review'] = payload
            conn.execute('INSERT INTO intelligence_knowledge_events VALUES (?,?,?,?,?,?,?,?,?)',
                         (*scope, event['revision'], item_id, c.actor_id, request_id,
                          fingerprint, json.dumps(event, ensure_ascii=False, allow_nan=False)))
            self._revision(conn, c, expected_case_revision)
            self._permit(conn, c, 'knowledge.' + operation, item_id)
            return event

    def read(self, context, item_id, *, history=False):
        c, scope = self._scope(context)
        item_id = TypeAdapter(Identifier).validate_python(item_id)
        with self.transaction() as conn:
            self._permit(conn, c, 'knowledge.read', item_id)
            rows = self._rows(conn, scope)
            selected = [r for r in rows if r['item_id'] == item_id]
            current = self._view(rows, item_id)
            for row in selected if history else [current]:
                if row['operation'] == 'draft':
                    self._support(conn, c, KnowledgeDraft.model_validate(row['draft']))
            self._permit(conn, c, 'knowledge.read', item_id)
            return {'revision': len(rows), 'case_revision': self._case_revision(conn, c),
                    'scope': dict(zip(('organisation_id', 'matter_id', 'case_id'), scope)),
                    'retired': selected[-1]['operation'] == 'retire',
                    'item': current, **({'history': selected} if history else {}), 'notices': list(NOTICES)}

    def search(self, context, query='', *, limit=20):
        c, scope = self._scope(context)
        if not isinstance(query, str) or len(query) > 300 or type(limit) is not int or not 1 <= limit <= 50:
            raise ValueError('Search requires a query of at most 300 characters and limit 1..50')
        terms = set(re.findall(r'\w+', query.casefold()))
        with self.transaction() as conn:
            self._permit(conn, c, 'knowledge.search', None)
            rows = self._rows(conn, scope)
            candidates = []
            for item_id in sorted({r['item_id'] for r in rows}):
                history = [r for r in rows if r['item_id'] == item_id]
                if history[-1]['operation'] == 'retire':
                    continue
                try:
                    self._permit(conn, c, 'knowledge.read', item_id)
                    item = self._view(rows, item_id)
                    draft = KnowledgeDraft.model_validate(item['draft'])
                    self._support(conn, c, draft)
                    if draft.kind == 'precedent' and item['review_status'] != 'use_as_reference':
                        continue
                    words = set(re.findall(r'\w+', (draft.title + ' ' + draft.summary).casefold()))
                    matched = sorted(terms & words)
                    if terms and not matched:
                        continue
                    self._permit(conn, c, 'knowledge.read', item_id)
                    candidates.append({**item, 'matched_terms': matched})
                except (PermissionError, KnowledgeUnavailable):
                    continue
            candidates.sort(key=lambda item: (-len(item['matched_terms']), item['item_id']))
            self._permit(conn, c, 'knowledge.search', None)
            return {'items': candidates[:limit], 'revision': len(rows),
                    'scope': dict(zip(('organisation_id', 'matter_id', 'case_id'), scope)),
                    'case_revision': self._case_revision(conn, c), 'limit': limit,
                    'truncated': len(candidates) > limit, 'notices': list(NOTICES)}


def content_digest_text(text):
    from hashlib import sha256
    return sha256(text.encode()).hexdigest()
