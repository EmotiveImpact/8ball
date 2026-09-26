"""Local course choices, independent from case facts and execution approvals.

Selections and reviews are append-only, optimistic and case-scoped. A view is
recalculated on request. It is not a continuously running monitoring service.
"""
from __future__ import annotations

from datetime import datetime, timedelta
import json
from typing import Literal

from pydantic import AwareDatetime, Field, model_validator

from endstate.course import CourseAnchor, Watch, anchor_route, assess_course
from .contracts import Strict, Identifier, Case
from .planner import to_snapshot
from ..models import utcnow
from ..store import Conflict, canonical, digest

TTL = timedelta(minutes=10)
LIMIT = 100


class PreviewCourse(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    route_id: Identifier
    watches: list[Watch] = Field(default_factory=list, max_length=12)
    review_at: AwareDatetime | None = None


class SelectCourse(PreviewCourse):
    event_id: Identifier
    expected_sequence: int = Field(strict=True, ge=0)
    as_of: AwareDatetime
    preview_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    rationale: str = Field(min_length=10, max_length=2000)
    assumptions: list[str] = Field(default_factory=list, max_length=12)
    replaces_course_id: Identifier | None = None
    acknowledge_limits: bool = Field(strict=True)

    @model_validator(mode='after')
    def deliberate(self):
        if not self.acknowledge_limits or len(self.rationale.strip()) < 10:
            raise ValueError('Explain the choice and acknowledge its conditional, non-authorising nature')
        if any(not x.strip() or len(x) > 500 for x in self.assumptions):
            raise ValueError('Assumptions must be non-empty and at most 500 characters each')
        return self


class CourseEvent(Strict):
    event_id: Identifier
    expected_revision: int = Field(strict=True, ge=0)
    expected_sequence: int = Field(strict=True, ge=0)
    course_id: Identifier
    operation: Literal['pause', 'resume', 'retire', 'review']
    rationale: str = Field(min_length=10, max_length=2000)
    assessment_as_of: AwareDatetime
    assessment_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')

    @model_validator(mode='after')
    def reason(self):
        if len(self.rationale.strip()) < 10:
            raise ValueError('Record a meaningful reason for this course judgement')
        return self


def target_digest(case: Case) -> str:
    return digest({'desired_outcome':case.desired_outcome,
                   'objectives':[o.model_dump(mode='json') for o in case.graph.objectives]})


def preview(case: Case, request: PreviewCourse, at: datetime) -> dict:
    anchor = anchor_route(to_snapshot(case), request.route_id, target_digest(case), at,
                          watches=request.watches, review_at=request.review_at)
    body = {'case_id':case.id, 'case_revision':case.revision, 'case_sha256':digest(case.model_dump(mode='json')),
            'requested_outcome':case.desired_outcome, 'as_of':at.isoformat(),
            'expires_at':(at+TTL).isoformat(), 'anchor':anchor.model_dump(mode='json'),
            'notice':'A recorded choice, not permission to act or proof of success. Existing action approvals remain separate.'}
    return {**body, 'preview_sha256':digest(body)}


def read_rows(db, case_id):
    return [dict(r) for r in db.execute('SELECT * FROM v2_course_events WHERE case_id=? ORDER BY sequence', (case_id,))]


def export_courses(rows, case_id, case_events=None):
    if not rows:
        return None  # Preserve exact old export shape for cases with no courses.
    previous = None
    records = []
    courses = {}
    current_id = None
    snapshots = {e['revision']:e['state_hash'] for e in case_events} if case_events is not None else None
    valid = True
    try:
        for seq, row in enumerate(rows, 1):
            r = json.loads(row['record'])
            if (r['sequence'] != seq or row['sequence'] != seq or r['previous_hash'] != previous
                    or r['case_id'] != case_id or row['case_id'] != case_id
                    or r['event_id'] != row['event_id'] or digest(r) != row['hash']
                    or r.get('execution_authorised') is not False or r.get('facts_attested') is not False):
                raise ValueError('Invalid chosen-course history')
            if snapshots is not None and snapshots.get(r['case_revision']) != r['case_sha256']:
                raise ValueError('Course judgement is detached from its case revision')
            if r['operation'] == 'select':
                chosen = r['selection']
                anchor = CourseAnchor.model_validate(chosen['anchor'])
                body = {k:v for k,v in chosen.items() if k != 'preview_sha256'}
                if (chosen['preview_sha256'] != digest(body) or chosen['case_sha256'] != r['case_sha256']
                        or chosen['case_id'] != case_id or anchor.baseline.id != case_id
                        or anchor.baseline.revision != r['case_revision'] or chosen['case_revision'] != r['case_revision']
                        or r['course_id'] in courses):
                    raise ValueError('Invalid course anchor')
                if r.get('replaces_course_id') != current_id:
                    raise ValueError('Course replacement does not match the previous active choice')
                if current_id:
                    courses[current_id]['lifecycle'] = 'superseded'
                current_id = r['course_id']
                courses[current_id] = {'id':current_id, 'lifecycle':'active', 'selection_record':r,
                                       'latest_review':None}
            else:
                if current_id != r['course_id'] or current_id not in courses:
                    raise ValueError('Course event cannot amend retired or unknown choices')
                c = courses[current_id]
                state = c['lifecycle']
                if r['operation'] == 'pause' and state == 'active':
                    c['lifecycle'] = 'paused'
                elif r['operation'] == 'resume' and state == 'paused':
                    c['lifecycle'] = 'active'
                elif r['operation'] == 'retire' and state in ('active', 'paused'):
                    c['lifecycle'] = 'retired'; current_id = None
                elif r['operation'] == 'review':
                    c['latest_review'] = r
                else:
                    raise ValueError('Invalid course state transition')
                view = r['assessment']
                if view['case_id'] != case_id or view['case_revision'] != r['case_revision'] or view['course_id'] != r['course_id']:
                    raise ValueError('Review belongs to another course context')
                body = {k:v for k,v in view.items() if k != 'assessment_sha256'}
                if digest(body) != view['assessment_sha256']:
                    raise ValueError('Course assessment hash mismatch')
            records.append({**r, 'hash':row['hash']})
            previous = row['hash']
    except (ValueError, KeyError, TypeError):
        valid = False
    return {'valid':valid, 'head_hash':previous, 'records':records,
            'current_id':current_id, 'courses':list(courses.values()),
            'authority':'Local course-choice history; not independently anchored, action permission or evidence attestation.'}


def assessment(case: Case, selection_record: dict, now: datetime) -> dict:
    anchor = CourseAnchor.model_validate(selection_record['selection']['anchor'])
    result = assess_course(anchor, to_snapshot(case), target_digest(case), now)
    body = {'case_id':case.id, 'case_revision':case.revision, 'case_sha256':digest(case.model_dump(mode='json')),
            'course_id':selection_record['course_id'], 'as_of':now.isoformat(),
            'expires_at':(now+TTL).isoformat(), 'result':result.model_dump(mode='json')}
    return {**body, 'assessment_sha256':digest(body)}


class Courses:
    def __init__(self, store):
        self.store = store

    def _read(self, db, case_id):
        case = self.store._get(db, case_id)
        rows = read_rows(db, case_id)
        # Bind every course record to its actual immutable case-event snapshot.
        event_rows = db.execute('SELECT record,hash FROM v2_events WHERE case_id=? ORDER BY revision', (case_id,)).fetchall()
        events = []
        previous = None
        try:
            for revision, row in enumerate(event_rows):
                event = json.loads(row['record'])
                if (event['case_id'] != case_id or event['revision'] != revision
                        or event['previous_hash'] != previous or digest(event) != row['hash']
                        or digest(event['state_after']) != event['state_hash']):
                    raise ValueError('Chosen-course assessment requires a valid case history')
                events.append(event); previous = row['hash']
            if (not events or events[-1]['revision'] != case.revision
                    or events[-1]['state_hash'] != digest(case.model_dump(mode='json'))):
                raise ValueError('Chosen-course assessment does not match the latest case history')
        except (KeyError, TypeError, json.JSONDecodeError):
            raise ValueError('Chosen-course assessment requires a readable case history') from None
        exported = export_courses(rows, case_id, events)
        if exported is not None and not exported['valid']:
            raise ValueError('Chosen-course history failed verification')
        return case, rows, exported or {'head_hash':None,'records':[],'courses':[],'current_id':None,'valid':True}

    def view(self, case_id):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case, rows, data = self._read(db, case_id)
            db.rollback()
        now = utcnow()
        result = []
        for c in data['courses']:
            r = c['selection_record']
            a = r['selection']['anchor']
            item = {'id':c['id'], 'lifecycle':c['lifecycle'], 'title':a['route']['title'],
                    'selected_at':r['recorded_at'], 'selected_revision':r['case_revision'],
                    'requested_outcome':r['selection']['requested_outcome'], 'rationale':r['rationale'],
                    'assumptions':r['assumptions'], 'original_route':a['route'], 'watches':a['watches'],
                    'review_at':a['review_at'], 'latest_review':c['latest_review']}
            if c['id'] == data['current_id']:
                # Fail visibly rather than show a false green result for an unreadable calculation.
                item['assessment'] = assessment(case, r, now)
            result.append(item)
        return {'case_id':case_id,'case_revision':case.revision,'sequence':len(rows),'current_id':data['current_id'],
                'courses':result,'records':data['records'],'valid':True,'monitoring':'on_request'}

    def preview(self, case_id, request: PreviewCourse):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case, rows, data = self._read(db, case_id)
            if case.revision != request.expected_revision:
                raise Conflict('The case changed. Refresh before choosing a course.')
            value = preview(case, request, utcnow())
            db.rollback()
        return {'preview':value,'sequence':len(rows),'current_id':data['current_id'],'persisted':False}

    def _append(self, db, case, rows, data, request, operation, details):
        record = {'case_id':case.id,'case_revision':case.revision,'case_sha256':digest(case.model_dump(mode='json')),
                  'event_id':request.event_id,'sequence':len(rows)+1,'previous_hash':data['head_hash'],
                  'recorded_at':utcnow().isoformat(),'actor':'local-operator',
                  'request_hash':digest(request.model_dump(mode='json')),'operation':operation,
                  'rationale':request.rationale,'execution_authorised':False,'facts_attested':False,**details}
        value = digest(record)
        db.execute('INSERT INTO v2_course_events VALUES (?,?,?,?,?)',
                   (case.id, request.event_id, record['sequence'], canonical(record), value))
        return {'record':{**record,'hash':value},'live_case_changed':False,'execution_authorised':False}

    def _check(self, case, rows, data, request):
        earlier = next((r for r in data['records'] if r['event_id'] == request.event_id), None)
        if earlier:
            if earlier['request_hash'] != digest(request.model_dump(mode='json')):
                raise Conflict('Event ID belongs to another course operation')
            return {'duplicate':True,'record':earlier,'live_case_changed':False,'execution_authorised':False}
        if len(rows) >= LIMIT:
            raise ValueError('Local course-history limit reached')
        if case.revision != request.expected_revision or len(rows) != request.expected_sequence:
            raise Conflict('Case or course history changed. Refresh before recording a judgement.')
        return None

    def select(self, case_id, request: SelectCourse):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case, rows, data = self._read(db, case_id)
                duplicate = self._check(case, rows, data, request)
                if duplicate:
                    db.rollback(); return duplicate
                now = utcnow()
                if request.as_of > now or now-request.as_of > TTL:
                    raise Conflict('Course preview expired. Inspect a fresh candidate.')
                if data['current_id'] != request.replaces_course_id:
                    raise Conflict('A current course can only be replaced with an explicit acknowledgement.')
                value = preview(case, request, request.as_of)
                if request.preview_sha256 != value['preview_sha256']:
                    raise Conflict('Selection differs from the previewed case, route, watches or target.')
                result = self._append(db, case, rows, data, request, 'select',
                    {'course_id':request.event_id,'selection':value,'assumptions':request.assumptions,
                     'replaces_course_id':request.replaces_course_id})
                db.commit(); return result
            except Exception:
                db.rollback(); raise

    def event(self, case_id, request: CourseEvent):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case, rows, data = self._read(db, case_id)
                duplicate = self._check(case, rows, data, request)
                if duplicate:
                    db.rollback(); return duplicate
                current = next((c for c in data['courses'] if c['id']==data['current_id']), None)
                if not current or current['id'] != request.course_id:
                    raise Conflict('Only the current course can be amended. Old choices stay in history.')
                allowed = {'active':{'pause','retire','review'},'paused':{'resume','retire','review'}}
                if request.operation not in allowed.get(current['lifecycle'], set()):
                    raise ValueError('This course cannot make that state transition')
                now = utcnow()
                if request.assessment_as_of > now or now-request.assessment_as_of > TTL:
                    raise Conflict('Course assessment expired. Refresh before recording this judgement.')
                value = assessment(case, current['selection_record'], request.assessment_as_of)
                if value['assessment_sha256'] != request.assessment_sha256:
                    raise Conflict('Assessment is no longer the exact reviewed course and case.')
                result = self._append(db, case, rows, data, request, request.operation,
                                      {'course_id':request.course_id,'assessment':value})
                db.commit(); return result
            except Exception:
                db.rollback(); raise
