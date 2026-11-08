"""Current-authority, revision-bound projections of verified derived history."""
from datetime import datetime

from pydantic import Field

from endstate.decision_packet import Selection, DisclosureDenied, project
from .plan_review import reference_catalogue
from .rehearsal import Rehearsals
from ..models import utcnow
from ..store import Conflict, digest


class Request(Selection):
    expected_revision: int = Field(strict=True, ge=0)
    expected_sequence: int = Field(strict=True, ge=1)
    expected_head_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    brief_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')


def local_operator_scope(db, case):
    return {r['id'] for r in reference_catalogue(case)}


class DecisionPackets:
    def __init__(self, store, *, policy):
        self.store, self.policy = store, policy

    def read(self, case_id, request: Request):
        request = Request.model_validate(request.model_dump(mode='python'))
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            case = self.store._get(db, case_id)
            allowed = self.policy(db, case)
            if allowed is None:
                raise DisclosureDenied('Current permission is required')
            allowed = frozenset(allowed)
            case, history = Rehearsals(self.store)._context(db, case_id)
            if (request.expected_revision != case.revision or request.expected_sequence != len(history['records'])
                    or request.expected_head_sha256 != history['head_hash']):
                raise Conflict('Case or challenge history changed; refresh before exporting')
            record = next((r for r in history['records'] if r['brief']['brief_sha256'] == request.brief_sha256), None)
            if record is None:
                raise ValueError('Select a saved brief from this case')
            brief, now = record['brief'], utcnow()
            if (brief['snapshot_sha256'] != digest(case.model_dump(mode='json'))
                    or now < datetime.fromisoformat(brief['as_of']) or now > datetime.fromisoformat(brief['expires_at'])):
                raise Conflict('This brief is stale; recheck and save before exporting a current packet')
            selection = Selection(mode=request.mode, references=request.references)
            packet = project(brief, selection, set(allowed))
            predecessors, cursor = [], brief['draft']['predecessor_sha256']
            by_hash = {r['brief']['brief_sha256']: r for r in history['records']}
            while cursor:
                parent = by_hash.get(cursor)
                if parent is None or len(predecessors) >= len(history['records']):
                    raise ValueError('Predecessor history is missing or cyclic')
                predecessors.append({'brief_sha256': cursor, 'sequence': parent['sequence'],
                                     'case_revision': parent['brief']['case_revision'], 'content_included': False})
                cursor = parent['brief']['draft']['predecessor_sha256']
            packet.update({'case_id': case.id, 'case_revision': case.revision, 'as_of': now.isoformat(),
                'brief_sha256': brief['brief_sha256'], 'history_head_sha256': history['head_hash'],
                'history_sequence': len(history['records']), 'predecessors': predecessors if request.mode == 'operator_review' else None,
                'missing_predecessors': False, 'authority_scope': 'local_operator_only',
                'persisted': False, 'facts_attested': False, 'execution_authorized': False,
                'notice_on_revocation': 'Authority is checked on each request. A downloaded copy cannot be remotely revoked.'})
            current = self.policy(db, case)
            if current is None or set(current) != set(allowed):
                raise DisclosureDenied('Disclosure permission changed during export')
            db.rollback()
        return {**packet, 'packet_sha256': digest(packet)}
