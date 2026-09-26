"""Case-scoped emergence ledger. Review is not evidence attestation.

Reads do not write. An explicit scan records immutable derived output; review
records append to a separate hash chain. Only 'create question' changes the case,
using the same validated command path and an atomic paired insight event.
"""
from __future__ import annotations
from datetime import datetime, timedelta
import json
from typing import Literal
from pydantic import Field, field_validator
from endstate.insights import (Insight, InsightPolicy, RULES, RULE_VERSION, detect,
                              make_insight, reference_index, stable_hash)
from ..models import Strict, Identifier, Title, Text, utcnow, uid
from ..store import Conflict, digest, canonical
from .planner import to_snapshot
from .contracts import Question, Provenance
from .commands import Command, apply

MAX_EVENTS=2000
REVIEW_TTL=timedelta(minutes=15)
TARGET_ALIGNMENT_RULE=('target_alignment','Recorded target-alignment review','Requested outcome wording changed while the objective records remain unchanged. This requests review, not a semantic assertion of drift.')


class ReferenceKey(Strict):
    kind: Literal['condition','action','actor','evidence','observation','objective','decision','question','resource','constraint']
    id: Identifier


class Context(Strict):
    event_id: Identifier
    expected_revision: int = Field(strict=True,ge=0)
    expected_insight_revision: int = Field(strict=True,ge=0)


class Scan(Context):
    policy: InsightPolicy = Field(default_factory=InsightPolicy)


class ReviewInsight(Context):
    insight_id: Identifier
    fingerprint: str = Field(pattern=r'^[a-f0-9]{64}$')
    disposition: Literal['useful','investigating','dismissed','review_complete','unreviewed']
    reason: str = Field(min_length=3,max_length=2000)


class Hypothesis(Context):
    title: Title
    meaning: str = Field(min_length=1,max_length=4000)
    why: Text
    verify: Title
    references: list[ReferenceKey] = Field(min_length=1,max_length=20)

    @field_validator('title','meaning','why','verify')
    @classmethod
    def substantive_text(cls,value):
        if not value.strip():raise ValueError('A hypothesis needs substantive text, not whitespace')
        return value


class RevisitHypothesis(Context):
    insight_id: Identifier
    fingerprint: str = Field(pattern=r'^[a-f0-9]{64}$')
    reason: str = Field(min_length=3,max_length=2000)


class InsightQuestion(Context):
    insight_id: Identifier
    fingerprint: str = Field(pattern=r'^[a-f0-9]{64}$')
    question: Title
    owner: Title
    reason: str = Field(min_length=3,max_length=2000)


def ledger_rows(db,case_id):
    return db.execute('SELECT record, hash FROM v2_insight_events WHERE case_id=? ORDER BY sequence',(case_id,)).fetchall()


def verify_ledger(rows,case_id):
    previous=None;events=[]
    for seq,row in enumerate(rows):
        record=json.loads(row['record'])
        if record.get('sequence')!=seq or record.get('case_id')!=case_id or record.get('previous_hash')!=previous or digest(record)!=row['hash']:
            raise ValueError('Insight ledger integrity check failed')
        events.append({**record,'hash':row['hash']});previous=row['hash']
    return events


def export_ledger(rows,case_id):
    if not rows:return None
    try:
        events=verify_ledger(rows,case_id)
        return {'valid':True,'head_hash':events[-1]['hash'],'events':events,
                'scope':'Separate local insight hash chain, not independent anchoring or proof of truth'}
    except (ValueError,KeyError,TypeError):
        return {'valid':False,'events':[{'record':r['record'],'hash':r['hash']} for r in rows],
                'scope':'Insight integrity failed; history retained for investigation'}


def project(events,case_revision,now):
    """Retain all unique findings, including dismissed and no-longer-reproduced.

    A finding which disappears then recurs starts a new occurrence. Reviews never
    attach silently to a changed fingerprint, even under the same stable ID.
    """
    records={};scan=None;previous_scan=None
    for e in events:
        body=e['body'];kind=e['kind']
        if kind=='scan':
            previous_scan=scan;scan=body
            current={i['id'] for i in body['findings']}
            for rid,r in records.items():
                if not r['manual'] and rid not in current:
                    r['present']=False
                    r['presence']='not_evaluated' if body['findings_truncated'] or r['insight']['rule'] in body['rules_disabled'] else 'not_reproduced'
            for item in body['findings']:
                old=records.get(item['id'])
                occurrence=old['occurrence'] if old and old['present'] else e['event_id']
                change='first_seen' if old is None else 'reappeared' if not old['present'] else 'changed' if old['insight']['fingerprint']!=item['fingerprint'] else 'unchanged'
                records[item['id']]={'insight':item,'manual':False,'present':True,'presence':'present',
                    'occurrence':occurrence,'first_seen':old['first_seen'] if old else e['recorded_at'],
                    'last_seen':e['recorded_at'],'change':change,'case_revision':body['revision'],
                    'reviews':old['reviews'] if old else [],'questions':old['questions'] if old else []}
        elif kind in ('hypothesis_added','hypothesis_revisited'):
            item=body['insight'];old=records.get(item['id'])
            records[item['id']]={'insight':item,'manual':True,'present':True,'presence':'operator_hypothesis',
                'occurrence':e['event_id'],'first_seen':old['first_seen'] if old else e['recorded_at'],'last_seen':e['recorded_at'],
                'case_revision':e['case_revision'],'change':'revisited' if old else 'first_seen','reviews':list(old['reviews']) if old else [],'questions':old['questions'] if old else []}
            if kind=='hypothesis_revisited':
                records[item['id']]['reviews'].append({'kind':kind,'at':e['recorded_at'],'actor':e['actor'],'fingerprint':item['fingerprint'],'occurrence':e['event_id'],'disposition':'unreviewed','reason':body['reason']})
        elif kind in ('review','question_created'):
            rid=body['insight_id']
            if rid not in records:raise ValueError('Review references a missing insight')
            records[rid]['reviews'].append({'kind':kind,'at':e['recorded_at'],'actor':e['actor'],**body})
            if kind=='question_created':records[rid]['questions'].append(body['question_id'])
    for r in records.values():
        matching=[v for v in r['reviews'] if v['fingerprint']==r['insight']['fingerprint'] and v['occurrence']==r['occurrence']]
        r['review_status']=matching[-1].get('disposition','investigating') if matching else 'unreviewed'
        r['review_outdated']=bool(r['reviews'] and not matching)
        r['case_outdated']=r['case_revision']!=case_revision
        # A manual hypothesis never auto-renews its evidential context.
        observed_at=datetime.fromisoformat(r['last_seen'])
        r['review_expired']=now-observed_at>REVIEW_TTL
        r['can_review']=r['present'] and not r['case_outdated'] and not r['review_expired']
    route_delta=None
    if scan and previous_scan:
        old={r['id']:r for r in previous_scan['routes']};new={r['id']:r for r in scan['routes']}
        route_delta={'compared_from_revision':previous_scan['revision'],'compared_to_revision':scan['revision'],
            'new_candidates':[new[k] for k in sorted(new.keys()-old.keys())],
            'no_longer_listed':[old[k] for k in sorted(old.keys()-new.keys())],
            'changed':[{'id':k,'before':old[k]['status'],'after':new[k]['status']} for k in sorted(old.keys()&new.keys()) if old[k]['status']!=new[k]['status']],
            'note':'Compared with the preceding explicit scan, not every intervening event. New IDs can reflect changed prerequisites rather than novel strategies.'}
    priority={'urgent':0,'important':1,'review':2}
    items=sorted(records.values(),key=lambda x:(not x['present'],priority[x['insight']['priority']],x['insight']['id']))
    return {'insight_revision':len(events),'case_revision':case_revision,'as_of':scan['as_of'] if scan else None,
            'scan':scan,'scan_outdated':bool(scan and scan['revision']!=case_revision),
            'items':items,'route_changes':route_delta,'total_recorded':len(items),
            'counts':{state:sum(i['review_status']==state for i in items) for state in ('unreviewed','useful','investigating','dismissed','review_complete')},
            'limits':['Manual scans only; no live inbox or background monitoring.',
                      'Derived patterns and hypotheses are not attested facts.',
                      'Dismissed and no-longer-reproduced findings remain in this history.',
                      'Review requires current case revision and a scan/context less than 15 minutes old.']}


class Insights:
    def __init__(self,store):self.store=store

    def _read(self,db,case_id):
        case=self.store._get(db,case_id)
        events=verify_ledger(ledger_rows(db,case_id),case_id)
        return case,events

    def view(self,case_id):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case,events=self._read(db,case_id)
            result=project(events,case.revision,utcnow());db.rollback()
        return result

    def _prepare(self,db,case_id,request,kind):
        case,events=self._read(db,case_id)
        request_hash=digest({'kind':kind,'request':request.model_dump(mode='json')})
        previous=next((e for e in events if e['event_id']==request.event_id),None)
        if previous:
            if previous['request_hash']!=request_hash:raise Conflict('Insight event ID already used for different content')
            return case,events,request_hash,True
        if case.revision!=request.expected_revision:raise Conflict('Case changed. Refresh and rerun the insight scan before reviewing.')
        if len(events)!=request.expected_insight_revision:raise Conflict('Insight history changed. Reload before continuing.')
        if len(events)>=MAX_EVENTS:raise ValueError('Local insight history limit reached; export before starting another review')
        return case,events,request_hash,False

    def _append(self,db,case,events,request,kind,body,request_hash):
        record={'sequence':len(events),'case_id':case.id,'case_revision':case.revision,'event_id':request.event_id,
                'kind':kind,'recorded_at':utcnow().isoformat(),'actor':'local-operator','body':body,
                'previous_hash':events[-1]['hash'] if events else None,'request_hash':request_hash}
        encoded=canonical(record)
        if len(encoded.encode())>3_000_000:raise ValueError('Insight event exceeds the local storage bound')
        db.execute('INSERT INTO v2_insight_events VALUES(?,?,?,?,?)',(case.id,request.event_id,len(events),encoded,digest(record)))

    def scan(self,case_id,request:Scan):
        # Compute outside the write lock, then recheck both optimistic revisions.
        with self.store.connection() as db:
            db.execute('BEGIN')
            case,events,h,duplicate=self._prepare(db,case_id,request,'scan')
            result=None if duplicate else detect(to_snapshot(case),utcnow(),request.policy)
            if result is not None:
                # Target edits are detectable; semantic objective drift is not claimed.
                target_events=db.execute("SELECT record FROM v2_events WHERE case_id=? AND json_extract(record,'$.kind')='metadata' ORDER BY revision DESC",(case_id,)).fetchall()
                for row in target_events:
                    event=json.loads(row['record'])
                    if 'desired_outcome' not in (event.get('changes') or {}).get('metadata_changed',[]):continue
                    if event['state_after']['graph']['objectives']==case.graph.model_dump(mode='json')['objectives']:
                        snapshot=to_snapshot(case);refindex=reference_index(snapshot)
                        item=make_insight('target_alignment','target',refs=[refindex[('objective',o.id)] for o in case.graph.objectives],
                            kind='inferred',priority='important',title='The requested outcome changed without changed success criteria',
                            meaning=case.desired_outcome,why=[f'Target wording changed at revision {event["revision"]}; objective records still match that revision.'],
                            verify='Review target-to-objective alignment explicitly in Plan Studio. The existing criteria may still be appropriate.',
                            caveat='A comparison of recorded changes, not a semantic judgement that the target is wrong.',
                            question='Do the current success criteria still cover the requested outcome?')
                        result['total_detected']+=1
                        if len(result['findings'])<request.policy.max_findings:result['findings'].append(item.model_dump(mode='json'))
                        else:result['findings_truncated']=True
                    break
                result['rules_evaluated'].append('target_alignment')
            db.rollback()
        if duplicate:return self.view(case_id)
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case,events,h,duplicate=self._prepare(db,case_id,request,'scan')
                if not duplicate:self._append(db,case,events,request,'scan',result,h)
                db.commit()
            except Exception:db.rollback();raise
        return self.view(case_id)

    def _current(self,case,events,request):
        view=project(events,case.revision,utcnow())
        item=next((i for i in view['items'] if i['insight']['id']==request.insight_id),None)
        if item is None:raise KeyError(request.insight_id)
        if not item['can_review']:raise Conflict('This finding is historical or its review context is stale. Refresh the case and scan again; for an operator hypothesis use explicit revisit.')
        if request.fingerprint!=item['insight']['fingerprint']:raise Conflict('The insight content changed. Read the current finding before deciding.')
        return item

    def review(self,case_id,request:ReviewInsight):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case,events,h,duplicate=self._prepare(db,case_id,request,'review')
                if not duplicate:
                    item=self._current(case,events,request)
                    if not request.reason.strip():raise ValueError('A review reason is required')
                    self._append(db,case,events,request,'review',{'insight_id':request.insight_id,'fingerprint':request.fingerprint,
                        'occurrence':item['occurrence'],'disposition':request.disposition,'reason':request.reason},h)
                db.commit()
            except Exception:db.rollback();raise
        return self.view(case_id)

    def add_hypothesis(self,case_id,request:Hypothesis):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case,events,h,duplicate=self._prepare(db,case_id,request,'hypothesis_added')
                if not duplicate:
                    index=reference_index(to_snapshot(case));selected=[]
                    for key in request.references:
                        if (key.kind,key.id) not in index:raise ValueError('Hypothesis references must name existing records in this case')
                        selected.append(index[(key.kind,key.id)])
                    if len({(r.kind,r.id) for r in selected})!=len(selected):raise ValueError('Repeated hypothesis reference')
                    item=make_insight('operator_hypothesis',request.event_id,refs=sorted(selected,key=lambda r:(r.kind,r.id)),
                        kind='hypothesis',title=request.title,meaning=request.meaning,why=[request.why],verify=request.verify,
                        caveat='An operator-authored possibility. Referencing evidence does not mean the source proves the hypothesis.',
                        condition_ids=sorted(r.id for r in selected if r.kind=='condition'),question=request.verify)
                    self._append(db,case,events,request,'hypothesis_added',{'insight':item.model_dump(mode='json')},h)
                db.commit()
            except Exception:db.rollback();raise
        return self.view(case_id)

    def revisit_hypothesis(self,case_id,request:RevisitHypothesis):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case,events,h,duplicate=self._prepare(db,case_id,request,'hypothesis_revisited')
                if not duplicate:
                    row=next((r for r in project(events,case.revision,utcnow())['items'] if r['insight']['id']==request.insight_id),None)
                    if not row or not row['manual']:raise ValueError('Only a recorded operator hypothesis can be revisited')
                    if row['insight']['fingerprint']!=request.fingerprint:raise Conflict('Hypothesis content changed; reload it before revisiting')
                    if not request.reason.strip():raise ValueError('A revisit reason is required')
                    index=reference_index(to_snapshot(case));value=dict(row['insight']);updated_refs=[]
                    for r in value['references']:
                        key=(r['kind'],r['id'])
                        if key not in index:raise Conflict('A referenced record was removed. Add a new, explicitly linked hypothesis with the replacement context.')
                        updated_refs.append(index[key].model_dump(mode='json'))
                    value['references']=updated_refs;value['fingerprint']=stable_hash({k:v for k,v in value.items() if k!='fingerprint'})
                    Insight.model_validate(value)
                    self._append(db,case,events,request,'hypothesis_revisited',{'insight':value,'reason':request.reason,'prior_fingerprint':request.fingerprint},h)
                db.commit()
            except Exception:db.rollback();raise
        return self.view(case_id)

    def create_question(self,case_id,request:InsightQuestion):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case,events,h,duplicate=self._prepare(db,case_id,request,'question_created')
                if duplicate:
                    record=next(e for e in events if e['event_id']==request.event_id)
                    qid=record['body']['question_id']
                else:
                    if case.revision>=2000:raise ValueError('Local case event limit reached')
                    item=self._current(case,events,request)
                    if item['questions']:raise Conflict('This finding already has a linked question. Review that question rather than creating duplicates.')
                    qid='q_ins_'+uid()
                    if not request.reason.strip():raise ValueError('A question-creation reason is required')
                    q=Question(id=qid,question=request.question,why=request.reason[:180],owner=request.owner,
                        condition_ids=item['insight']['condition_ids'],
                        provenance=Provenance(origin='operator',note=f'Explicitly created from insight {request.insight_id}; fingerprint {request.fingerprint}. No observation attested.'))
                    cmd=Command(event_id=request.event_id,expected_revision=case.revision,kind='upsert_object',
                                payload={'kind':'question','object':q.model_dump(mode='json')})
                    if db.execute('SELECT 1 FROM v2_events WHERE case_id=? AND event_id=?',(case.id,request.event_id)).fetchone():
                        raise Conflict('Event ID already belongs to a case command')
                    now=utcnow();updated=apply(case,cmd,now=now)
                    self.store._persist(db,case,updated,cmd,'local-operator',now)
                    self._append(db,updated,events,request,'question_created',{'insight_id':request.insight_id,'fingerprint':request.fingerprint,
                        'occurrence':item['occurrence'],'reason':request.reason,'question_id':qid,'disposition':'investigating'},h)
                db.commit()
            except Exception:db.rollback();raise
        return {'question_id':qid,'case':self.store.get(case_id).model_dump(mode='json'),'insights':self.view(case_id)}
