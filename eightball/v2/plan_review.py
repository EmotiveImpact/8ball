"""Human plan-quality review, separate from factual state and action approval.

Assessments are read-only. Saving appends a case-scoped journal and never changes
case revision, observations, decisions or approvals. Reviewed != safe or true.
"""
from datetime import datetime, timedelta
import json
from typing import Literal
from pydantic import Field, AwareDatetime, model_validator
from endstate.plan_review import Inspection, Stress, RUBRIC, RUBRIC_VERSION, inspect_plan
from .contracts import Strict, Identifier, Text, Case
from .planner import to_snapshot
from ..models import utcnow
from ..store import Conflict, digest, canonical

TTL_MINUTES = 15


class Assess(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    scenarios: list[Stress] = Field(default_factory=list, max_length=3)


class Judgement(Strict):
    criterion: Literal['target', 'sources', 'dependencies', 'authority', 'estimates', 'alternatives']
    verdict: Literal['supported', 'needs_changes', 'uncertain', 'not_applicable']
    rationale: str = Field(min_length=10, max_length=2000)
    references: list[str] = Field(default_factory=list, max_length=12)

    @model_validator(mode='after')
    def meaningful(self):
        if len(self.rationale.strip()) < 10:
            raise ValueError('Explain the review judgement, not just its label')
        if self.verdict == 'supported' and not self.references:
            raise ValueError('A supported judgement needs at least one inspected case reference')
        if len(set(self.references)) != len(self.references) or any(len(x) > 110 for x in self.references):
            raise ValueError('Invalid or repeated review references')
        return self


class SaveReview(Strict):
    event_id: Identifier
    expected_revision: int = Field(strict=True, ge=0)
    expected_sequence: int = Field(strict=True, ge=0)
    as_of: AwareDatetime
    assessment_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    scenarios: list[Stress] = Field(default_factory=list, max_length=3)
    judgements: list[Judgement] = Field(min_length=6, max_length=6)

    @model_validator(mode='after')
    def full_rubric(self):
        if {j.criterion for j in self.judgements} != {r['id'] for r in RUBRIC}:
            raise ValueError('Review every rubric criterion exactly once')
        return self


def reference_catalogue(case):
    refs = [{'id': 'case:desired_outcome', 'title': case.desired_outcome, 'kind': 'requested outcome'},
            {'id': 'case:summary', 'title': 'Operator-provided situation brief', 'kind': 'brief'}]
    for kind, objects in [('objective', case.graph.objectives), ('condition', case.graph.conditions),
                          ('action', case.graph.actions), ('source', case.evidence), ('actor', case.actors),
                          ('constraint', case.constraints), ('decision', case.decisions)]:
        for obj in objects:
            refs.append({'id': kind + ':' + obj.id, 'title': getattr(obj, 'title', getattr(obj, 'name', getattr(obj, 'question', obj.id))), 'kind': kind})
    return refs


def assessment(case: Case, scenarios, as_of):
    report = inspect_plan(to_snapshot(case), Inspection(as_of=as_of, scenarios=scenarios))
    value = {'case_id': case.id, 'case_revision': case.revision,
             'case_sha256': digest(case.model_dump(mode='json')),
             'requested_outcome': case.desired_outcome, 'rubric_version': RUBRIC_VERSION,
             'rubric': RUBRIC, 'references': reference_catalogue(case),
             'inspection': report, 'expires_at': (as_of + timedelta(minutes=TTL_MINUTES)).isoformat(),
             'notice': 'Human review of the LIVE case only, not unsaved Plan Studio changes. No quality score, verified fact, approval or release decision is created.'}
    return {**value, 'assessment_sha256': digest(value)}


def read_journal(db, case_id):
    return [dict(row) for row in db.execute('SELECT case_id,event_id,sequence,record,hash FROM v2_plan_reviews WHERE case_id=? ORDER BY sequence', (case_id,))]


def export_journal(rows, case_id, case_events=None):
    if not rows:
        return None
    valid = True
    records, previous = [], None
    snapshots = {e['revision']: e['state_hash'] for e in case_events} if case_events is not None else None
    for seq, row in enumerate(rows, 1):
        try:
            r = json.loads(row['record'])
            body = r['assessment']; content = {k: v for k, v in body.items() if k != 'assessment_sha256'}
            valid = valid and r['sequence'] == seq == row['sequence'] and r['case_id'] == case_id == row['case_id'] and r['event_id'] == row['event_id'] and r['previous_hash'] == previous
            valid = valid and digest(r) == row['hash'] and digest(content) == body['assessment_sha256']
            valid = valid and body['case_id'] == case_id and r['case_revision'] == body['case_revision']
            if snapshots is not None:
                valid = valid and snapshots.get(body['case_revision']) == body['case_sha256']
            records.append({**r, 'hash': row['hash']})
            previous = row['hash']
        except (ValueError, KeyError, TypeError):
            valid = False
    return {'valid': bool(valid), 'head_hash': previous, 'records': records,
            'authority': 'Local human review history. Not independently anchored or an action-approval ledger.'}


class PlanReviews:
    def __init__(self, store):
        self.store = store

    def view(self, case_id):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case = self.store._get(db, case_id)
            rows = read_journal(db, case_id)
            db.rollback()
        data = export_journal(rows, case_id)
        if data is not None and not data['valid']:
            raise ValueError('Plan-review journal failed verification')
        now = utcnow()
        records = []
        for r in (data or {}).get('records', []):
            a = r['assessment']
            records.append({**r, 'case_changed': a['case_sha256'] != digest(case.model_dump(mode='json')),
                            'time_expired': now > datetime.fromisoformat(a['expires_at'])})
        return {'case_id': case_id, 'case_revision': case.revision, 'sequence': len(rows), 'records': records,
                'rubric': RUBRIC, 'rubric_version': RUBRIC_VERSION, 'valid': True}

    def assess(self, case_id, request: Assess):
        case = self.store.get(case_id)
        if case.revision != request.expected_revision:
            raise Conflict('The case changed. Refresh before reviewing the live plan.')
        # The same revision can get a concurrent review; save still checks sequence.
        with self.store.connection() as db:
            seq = db.execute('SELECT COUNT(*) FROM v2_plan_reviews WHERE case_id=?', (case_id,)).fetchone()[0]
        return {'assessment': assessment(case, request.scenarios, utcnow()), 'sequence': seq, 'persisted': False}

    def save(self, case_id, request: SaveReview):
        request_hash = digest(request.model_dump(mode='json'))
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case = self.store._get(db, case_id)
                rows = read_journal(db, case_id)
                exported = export_journal(rows, case_id)
                if exported is not None and not exported['valid']:
                    raise ValueError('Plan-review journal failed verification')
                prior = next((r for r in (exported or {}).get('records', []) if r['event_id'] == request.event_id), None)
                if prior:
                    if prior['request_hash'] != request_hash:
                        raise Conflict('This event ID already belongs to a different review')
                    db.rollback()
                    return {'duplicate': True, 'record': prior, 'live_case_changed': False}
                if len(rows) != request.expected_sequence or case.revision != request.expected_revision:
                    raise Conflict('The case or review history changed. Refresh before recording this review.')
                if len(rows) >= 100:
                    raise ValueError('Local plan-review limit reached; export the case')
                now = utcnow()
                if request.as_of > now or now - request.as_of > timedelta(minutes=TTL_MINUTES):
                    raise Conflict('This assessment expired. Recalculate before recording a judgement.')
                current = assessment(case, request.scenarios, request.as_of)
                if request.assessment_sha256 != current['assessment_sha256']:
                    raise Conflict('This assessment does not match the current case, scenarios or review contract')
                known = {r['id'] for r in current['references']}
                if any(not set(j.references) <= known for j in request.judgements):
                    raise ValueError('Review references must belong to the inspected case')
                verdicts = {j.verdict for j in request.judgements}
                disposition = ('changes_requested' if 'needs_changes' in verdicts else
                               'uncertainty_recorded' if 'uncertain' in verdicts else 'review_recorded')
                # This is a record, not an approval. Even six supported labels cannot clear diagnostics.
                record = {'case_id': case_id, 'case_revision': case.revision, 'event_id': request.event_id,
                          'sequence': len(rows) + 1, 'previous_hash': exported['head_hash'] if exported else None,
                          'recorded_at': now.isoformat(), 'actor': 'local-operator', 'request_hash': request_hash,
                          'assessment': current, 'judgements': [j.model_dump(mode='json') for j in request.judgements],
                          'disposition': disposition, 'execution_authorised': False, 'facts_attested': False}
                checksum = digest(record)
                db.execute('INSERT INTO v2_plan_reviews VALUES (?,?,?,?,?)',
                           (case_id, request.event_id, record['sequence'], canonical(record), checksum))
                db.commit()
                return {'record': {**record, 'hash': checksum}, 'live_case_changed': False}
            except Exception:
                db.rollback()
                raise
