"""Source-grounded identity judgements and explicit deadline amendments.

A separate hash-linked review journal preserves all interpretations. It never
merges actors, rewrites quotations or treats a name match as authority. Only the
explicit deadline-apply transaction changes a planning snapshot.
"""
from __future__ import annotations
import json
import re
import unicodedata
from datetime import datetime
from typing import Literal
from pydantic import Field, field_validator, model_validator
from endstate.time_review import TimeInterpretation, interpret_time
from .contracts import Strict, Identifier, Title, Case, uid, utcnow
from .commands import Command, preserve_meaning
from .planner import plan, changes
from .source_contracts import text_hash
from ..store import Conflict, canonical, digest

MAX_EVENTS = 600
MAX_REVIEWS = 150


class SourceMention(Strict):
    evidence_id: Identifier
    start: int = Field(strict=True, ge=0)
    end: int = Field(strict=True, ge=1)
    quote: str = Field(min_length=1, max_length=2000)
    content_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')

    @model_validator(mode='after')
    def exact_length(self):
        if self.end - self.start != len(self.quote):
            raise ValueError('Quotation and Unicode code-point offsets disagree')
        return self


class ReviewContext(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    expected_review_revision: int = Field(strict=True, ge=0)


class WriteContext(ReviewContext):
    event_id: Identifier


class NewReview(WriteContext):
    kind: Literal['identity', 'deadline']
    mention: SourceMention
    note: str = Field(min_length=3, max_length=2000)

    @field_validator('note')
    @classmethod
    def reason(cls, value):
        if len(value.strip()) < 3:
            raise ValueError('Record what needs review')
        return value


class IdentityDecision(WriteContext):
    review_id: Identifier
    disposition: Literal['linked', 'distinct', 'unresolved']
    actor_id: Identifier | None = None
    reason: str = Field(min_length=3, max_length=2000)

    @model_validator(mode='after')
    def valid_decision(self):
        if self.disposition in ('linked', 'distinct') and not self.actor_id:
            raise ValueError('Select the actor being linked or explicitly distinguished')
        if self.disposition == 'unresolved' and self.actor_id is not None:
            raise ValueError('An unresolved mention cannot silently link an actor')
        if len(self.reason.strip()) < 3:
            raise ValueError('State the basis for this identity judgement')
        return self


class Disposition(WriteContext):
    review_id: Identifier
    disposition: Literal['dismissed', 'open']
    reason: str = Field(min_length=3, max_length=2000)

    @field_validator('reason')
    @classmethod
    def meaningful(cls, value):
        if len(value.strip()) < 3: raise ValueError('A meaningful review reason is required')
        return value


class DeadlineTarget(Strict):
    kind: Literal['case', 'condition', 'decision', 'question']
    id: Identifier


class DeadlinePreview(ReviewContext):
    review_id: Identifier
    interpretation: TimeInterpretation
    target: DeadlineTarget
    reason: str = Field(min_length=3, max_length=2000)

    @field_validator('reason')
    @classmethod
    def meaningful(cls, value):
        if len(value.strip()) < 3: raise ValueError('Explain why this interpretation applies to the selected target')
        return value


class ApplyDeadline(DeadlinePreview):
    event_id: Identifier
    preview_digest: str = Field(pattern=r'^[0-9a-f]{64}$')


def read_events(db, case_id):
    rows = db.execute('SELECT record,hash FROM v2_grounding_events WHERE case_id=? ORDER BY sequence', (case_id,)).fetchall()
    events, previous, known = [], None, set()
    for sequence, row in enumerate(rows, 1):
        rec = json.loads(row['record'])
        if (rec.get('case_id') != case_id or rec.get('sequence') != sequence or
            rec.get('previous_hash') != previous or digest(rec) != row['hash']):
            raise ValueError('Identity/deadline review journal failed verification')
        value = rec['review']
        SourceMention.model_validate(value['mention'])
        if value['kind'] not in ('identity', 'deadline') or value['id'] != rec['review_id']:
            raise ValueError('Review journal identity mismatch')
        if rec['operation'] == 'created':
            if value['id'] in known: raise ValueError('Repeated review creation')
            known.add(value['id'])
        elif value['id'] not in known:
            raise ValueError('Review history has no creation record')
        events.append({**rec, 'hash': row['hash']})
        previous = row['hash']
    return events


def _project(events):
    records = {}
    for event in events:
        records[event['review_id']] = event['review']
    return records


def _source(case, mention: SourceMention, *, reviewed=False):
    source = next((e for e in case.evidence if e.id == mention.evidence_id), None)
    if source is None: raise ValueError('Selected source is not in this case')
    if source.status == 'retracted': raise ValueError('A retracted source cannot support a new interpretation')
    if text_hash(source.text) != mention.content_sha256 or source.text[mention.start:mention.end] != mention.quote:
        raise ValueError('Source quotation/hash/offset mismatch. Reopen the exact source')
    if reviewed and source.status != 'reviewed':
        raise ValueError('Review the evidence source before linking an identity or applying a deadline')
    return source


def _target(case, target):
    if target.kind == 'case':
        if target.id != case.id: raise ValueError('Deadline target belongs to another case')
        return case, 'deadline', case.title
    collections = {'condition': case.graph.conditions, 'decision': case.decisions, 'question': case.questions}
    obj = next((o for o in collections[target.kind] if o.id == target.id), None)
    if obj is None: raise ValueError('Deadline target no longer exists in this case')
    return obj, 'due_at' if target.kind == 'condition' else 'needed_by', getattr(obj, 'title', None) or obj.question


def _normalise(text):
    return ' '.join(unicodedata.normalize('NFC', text).casefold().split())


def actor_candidates(case, mention):
    """Lexical candidates only. Exact name matches are not identity confirmation."""
    words = set(re.findall(r'\w+', _normalise(mention.quote)))
    options = []
    for actor in case.actors:
        name = _normalise(actor.name)
        exact = name == _normalise(mention.quote)
        overlap = sorted(words & set(re.findall(r'\w+', name)))
        if exact or overlap:
            options.append({'id': actor.id, 'name': actor.name, 'role': actor.role,
                            'match': 'same_name_text' if exact else 'shared_name_tokens',
                            'matched_tokens': overlap, 'not_identity_proof': True})
    return sorted(options, key=lambda o: (o['match'] != 'same_name_text', o['name'], o['id']))


def view_records(case, events):
    records = []
    for row in _project(events).values():
        value = json.loads(canonical(row))
        warnings = []
        try:
            source = _source(case, SourceMention.model_validate(value['mention']))
            if source.status != 'reviewed': warnings.append('source_needs_review')
        except ValueError:
            warnings.append('source_unavailable_or_retracted')
        if value.get('actor_id'):
            actor = next((a for a in case.actors if a.id == value['actor_id']), None)
            if actor is None or digest(actor.model_dump(mode='json')) != value.get('actor_hash'):
                warnings.append('actor_record_changed')
        applied = value.get('application')
        if applied:
            try:
                target, field, _ = _target(case, DeadlineTarget.model_validate(applied['target']))
                current = getattr(target, field)
                if current is None or current != datetime.fromisoformat(applied['utc']):
                    warnings.append('deadline_has_subsequently_changed')
            except ValueError:
                warnings.append('deadline_target_removed')
        value.update(warnings=warnings, needs_attention=bool(warnings),
                     can_interpret=not warnings or warnings == ['actor_record_changed'],
                     candidates=actor_candidates(case, SourceMention.model_validate(value['mention'])) if value['kind'] == 'identity' else [],
                     history=[{**{k:v for k,v in e.items() if k != 'review'}, 'reason':e['review']['reason'], 'disposition':e['review']['status'], 'actor_name':e['review'].get('actor_name')} for e in events if e['review_id'] == value['id']])
        records.append(value)
    return {'case_id':case.id, 'case_revision':case.revision, 'review_revision':len(events),
            'records':list(reversed(records)), 'needs_attention':sum(r['needs_attention'] for r in records),
            'review_chain_valid':True,
            'notice':'Human interpretations, not verified facts. Identity links never merge actor records. Deadline application is a separate explicit case amendment.'}


def export_reviews(events, case_events):
    """Verify the review-to-case application link; preserve old export shape."""
    applies = [e for e in case_events if e['kind'] == 'apply_deadline_review']
    if not events and not applies: return None
    application_events = {e['event_id']:e for e in events if e['operation'] == 'deadline_applied'}
    valid = len(applies) == len(application_events)
    for event in applies:
        review_event = application_events.get(event['event_id'])
        valid = valid and bool(review_event and event['payload'].get('review_hash') == digest(review_event['review']) and
                              review_event['case_revision'] == event['revision'])
    return {'valid': bool(valid), 'events': events, 'head_hash':events[-1]['hash'] if events else None,
            'scope':'Local hash-linked review journal and linked case amendments, not independently anchored forensic custody.'}


class GroundingDesk:
    def __init__(self, store):
        self.store = store

    def view(self, case_id):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case = self.store._get(db, case_id)
            events = read_events(db, case_id)
            result = view_records(case, events)
            result['sources'] = [{'id': e.id, 'title':e.title, 'source':e.source, 'status':e.status,
                                  'text':e.text, 'content_sha256':text_hash(e.text)} for e in case.evidence]
            db.rollback()
            return result

    def _context(self, db, case_id, request):
        case = self.store._get(db, case_id)
        events = read_events(db, case_id)
        if case.revision != request.expected_revision or len(events) != request.expected_review_revision:
            raise Conflict('The case or interpretation history changed. Refresh and review again')
        return case, events

    def _duplicate(self, db, case_id, request):
        row = db.execute('SELECT record FROM v2_grounding_events WHERE case_id=? AND event_id=?', (case_id, request.event_id)).fetchone()
        if row:
            if json.loads(row['record'])['request_hash'] != digest(request.model_dump(mode='json')):
                raise Conflict('This event ID already belongs to a different review request')
            read_events(db, case_id)
            return True
        if db.execute('SELECT 1 FROM v2_events WHERE case_id=? AND event_id=?', (case_id, request.event_id)).fetchone():
            raise Conflict('This event ID is already used by a case command')
        return False

    def _append(self, db, case, events, request, operation, review, actor):
        if len(events) >= MAX_EVENTS: raise ValueError('Local interpretation event limit reached')
        record = {'case_id':case.id, 'event_id':request.event_id, 'review_id':review['id'], 'operation':operation,
                  'sequence':len(events)+1, 'previous_hash':events[-1]['hash'] if events else None,
                  'request_hash':digest(request.model_dump(mode='json')), 'case_revision':case.revision,
                  'actor':actor, 'recorded_at':utcnow().isoformat(), 'review':review}
        db.execute('INSERT INTO v2_grounding_events VALUES (?,?,?,?,?)',
                   (case.id,request.event_id,len(events)+1,canonical(record),digest(record)))

    def _record(self, events, review_id, kind=None):
        record = _project(events).get(review_id)
        if not record: raise KeyError(review_id)
        if kind and record['kind'] != kind: raise ValueError('Review kind does not match the requested operation')
        return json.loads(canonical(record))

    def create(self, case_id, request:NewReview, actor='local-operator'):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                if self._duplicate(db,case_id,request): db.rollback(); return self.view(case_id)
                case,events=self._context(db,case_id,request)
                source=_source(case,request.mention)
                if len(_project(events)) >= MAX_REVIEWS: raise ValueError('Local source-review limit reached')
                if any(r['kind']==request.kind and r['mention']==request.mention.model_dump() for r in _project(events).values()):
                    raise Conflict('This exact source mention already has a review. Reopen that record instead of creating a duplicate')
                record={'id':uid(),'kind':request.kind,'mention':request.mention.model_dump(mode='json'),'note':request.note,
                        'source_title':source.title,'source_attribution':source.source,'status':'open','reason':request.note,
                        'created_at':utcnow().isoformat(),'created_revision':case.revision,
                        'actor_id':None,'actor_hash':None,'application':None}
                self._append(db,case,events,request,'created',record,actor);db.commit()
            except Exception: db.rollback(); raise
        return self.view(case_id)

    def identity(self, case_id, request:IdentityDecision, actor='local-operator'):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                if self._duplicate(db,case_id,request): db.rollback(); return self.view(case_id)
                case,events=self._context(db,case_id,request)
                record=self._record(events,request.review_id,'identity')
                _source(case,SourceMention.model_validate(record['mention']),reviewed=request.disposition!='unresolved')
                linked=next((a for a in case.actors if a.id==request.actor_id),None) if request.actor_id else None
                if request.actor_id and linked is None: raise ValueError('Actor is not in this case')
                record.update(status=request.disposition,reason=request.reason,actor_id=request.actor_id,
                              actor_hash=digest(linked.model_dump(mode='json')) if linked else None,
                              actor_name=linked.name if linked else None,reviewed_revision=case.revision)
                self._append(db,case,events,request,'identity_reviewed',record,actor);db.commit()
            except Exception: db.rollback(); raise
        return self.view(case_id)

    def dispose(self, case_id, request:Disposition, actor='local-operator'):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                if self._duplicate(db,case_id,request):db.rollback();return self.view(case_id)
                case,events=self._context(db,case_id,request);record=self._record(events,request.review_id)
                record.update(status=request.disposition,reason=request.reason)
                self._append(db,case,events,request,'review_disposition',record,actor);db.commit()
            except Exception:db.rollback();raise
        return self.view(case_id)

    def _preview(self, case, events, request:DeadlinePreview):
        record=self._record(events,request.review_id,'deadline')
        _source(case,SourceMention.model_validate(record['mention']),reviewed=True)
        target,field,title=_target(case,request.target)
        old=getattr(target,field)
        resolution=interpret_time(request.interpretation)
        preview={'review_id':record['id'],'quoted_wording':record['mention']['quote'], 'source_title':record['source_title'],
                 'target':request.target.model_dump(),'target_title':title,'before':old.isoformat() if old else None,
                 'resolution':resolution,'can_apply':resolution['selected'] is not None,
                 'case_revision':case.revision,'review_revision':len(events),'changes':None}
        token_payload={'request':DeadlinePreview.model_validate(request.model_dump(include=set(DeadlinePreview.model_fields))).model_dump(mode='json'),
                       'case_hash':digest(case.model_dump(mode='json')), 'review_hash':digest(record),
                       'resolved_utc':resolution['selected']['utc'] if resolution['selected'] else None}
        preview['preview_digest']=digest(token_payload)
        if resolution['selected'] is not None:
            updated=self._amend(case,request.target,datetime.fromisoformat(resolution['selected']['utc']),utcnow())
            now=utcnow();bp,ap=plan(case,now),plan(updated,now)
            preview['changes']=changes(case,updated,bp,ap)
            preview['route_summary']={'before':len(bp['routes']),'after':len(ap['routes']),
                                      'constraint_failures_before':sum(bool(r['hard_breaches']) for r in bp['routes']),
                                      'constraint_failures_after':sum(bool(r['hard_breaches']) for r in ap['routes'])}
            preview['approvals_to_invalidate']=len(case.approvals)
        return preview,record

    @staticmethod
    def _amend(case,target,value,now):
        data=case.model_dump(mode='json')
        if target.kind=='case':data['deadline']=value.isoformat()
        else:
            rows=data['graph']['conditions'] if target.kind=='condition' else data['decisions'] if target.kind=='decision' else data['questions']
            row=next(o for o in rows if o['id']==target.id)
            row['due_at' if target.kind=='condition' else 'needed_by']=value.isoformat()
        data.update(revision=case.revision+1,updated_at=now.isoformat(),approvals=[])
        return preserve_meaning(case,Case.model_validate(data))

    def preview(self,case_id,request:DeadlinePreview):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case,events=self._context(db,case_id,request)
            result,_=self._preview(case,events,request)
            db.rollback();return result

    def apply_deadline(self,case_id,request:ApplyDeadline,actor='local-operator'):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                if self._duplicate(db,case_id,request):db.rollback();return {'duplicate':True,'reviews':self.view(case_id)}
                case,events=self._context(db,case_id,request)
                if case.revision>=2000:raise ValueError('Local case event limit reached')
                preview,record=self._preview(case,events,request)
                if preview['preview_digest']!=request.preview_digest:raise Conflict('The reviewed preview does not match this amendment')
                if not preview['can_apply']:raise ValueError('Resolve the ambiguous or nonexistent local time before applying a deadline')
                selected=preview['resolution']['selected'];now=utcnow()
                updated=self._amend(case,request.target,datetime.fromisoformat(selected['utc']),now)
                record.update(status='applied',reason=request.reason,reviewed_revision=case.revision,
                              application={'target':request.target.model_dump(),'before':preview['before'],'utc':selected['utc'],
                                           'local':selected['local'],'time_zone':request.interpretation.time_zone,
                                           'basis':request.interpretation.model_dump(mode='json'),'applied_revision':updated.revision})
                cmd=Command(event_id=request.event_id,expected_revision=case.revision,kind='apply_deadline_review',
                            payload={'review_id':record['id'],'review_hash':digest(record),'interpretation':record})
                delta=self.store._persist(db,case,updated,cmd,actor,now,request_hash=digest(request.model_dump(mode='json')),
                                          extra_objects=[{'collection':'source_interpretations','id':record['id'],'change':'deadline_applied'}])
                self._append(db,updated,events,request,'deadline_applied',record,actor);db.commit()
            except Exception:db.rollback();raise
        return {'changes':delta,'reviews':self.view(case_id)}
