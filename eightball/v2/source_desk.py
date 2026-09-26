"""Immutable text originals, explicit passage capture and provenance-safe duplicates.

Full originals are kept outside planning snapshots and provider context. New case
revisions anchor hashes and explicit source operations. Capture/retraction and
case changes commit atomically. Reading/searching/previewing has no write effect.
"""
from __future__ import annotations

import json
import re
from bisect import bisect_right
from .source_contracts import *
from .contracts import Case
from .commands import Command
from .planner import plan
from ..models import Evidence, uid, utcnow
from ..store import Conflict, canonical, digest


def _descriptor(document: dict) -> dict:
    return {k:v for k,v in document.items() if k not in ('text','status','retraction_reason')}


def decode_document(row) -> dict:
    value = json.loads(row['metadata'])
    return {**value, 'text':row['text'], 'status':row['status'], 'retraction_reason':row['retraction_reason']}


def _metadata(document: dict) -> dict:
    return {k:v for k,v in document.items() if k != 'text'}


def _new_revision(case: Case, now) -> Case:
    data=case.model_dump(mode='json')
    data.update(revision=case.revision+1, updated_at=now.isoformat(), approvals=[])
    return Case.model_validate(data)


def _guard_revision(case:Case, expected:int):
    if case.revision != expected:
        raise Conflict('Case changed. Refresh and review the source operation again.')
    if case.revision >= 2000:
        raise ValueError('Local event limit reached')


class SourceDesk:
    def __init__(self,store):
        self.store=store

    def _document(self,db,case_id,document_id):
        row=db.execute('SELECT * FROM v2_source_documents WHERE case_id=? AND id=?',(case_id,document_id)).fetchone()
        if not row:raise KeyError(document_id)
        doc=decode_document(row)
        if doc['id']!=document_id or doc['case_id']!=case_id:
            raise ValueError('Stored source metadata does not match its case-scoped identity')
        if doc['content_sha256'] != text_hash(doc['text']):
            raise ValueError('Stored source failed its content-hash check. Inspect the audit before proceeding.')
        return doc

    def _duplicates(self,db,case_id,text):
        exact,normal=text_hash(text),comparison_hash(text)
        matches=[]
        for row in db.execute('SELECT * FROM v2_source_documents WHERE case_id=? ORDER BY rowid',(case_id,)):
            metadata=json.loads(row['metadata'])
            kind = 'exact_text' if metadata['content_sha256']==exact else 'normalised_whitespace_candidate' if metadata['comparison_sha256']==normal else None
            if kind:
                matches.append({'document_id':metadata['id'],'title':metadata['title'],'source':metadata['source'],
                                'status':row['status'],'kind':kind})
        return matches

    def index(self,case_id):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case=self.store._get(db,case_id)
            documents=[{**json.loads(r['metadata']), 'status':r['status'],'retraction_reason':r['retraction_reason']}
                       for r in db.execute('SELECT metadata,status,retraction_reason FROM v2_source_documents WHERE case_id=? ORDER BY rowid DESC',(case_id,))]
            links=[json.loads(r['body']) for r in db.execute('SELECT body FROM v2_source_passages WHERE case_id=? ORDER BY rowid',(case_id,))]
            db.rollback()
        for doc in documents:
            ranges=sorted((p['start'],p['end']) for p in links if p['document_id']==doc['id'])
            merged=[]
            for start,end in ranges:
                if merged and start<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],end)
                else:merged.append([start,end])
            doc['captured_characters']=sum(end-start for start,end in merged)
            doc['passage_count']=len(ranges)
        return {'case_id':case_id,'revision':case.revision,'documents':documents,'passages':links,
                'limits':{'document_characters':MAX_SOURCE_CHARS,'document_bytes':MAX_SOURCE_BYTES,
                          'case_bytes':MAX_CASE_SOURCE_BYTES,'documents_per_case':MAX_DOCUMENTS,
                          'selection_characters':MAX_BATCH_CHARS},
                'notice':'Text originals only. No OCR, binary vault, automatic model analysis or automatic truth verification.'}

    def preview_import(self,case_id,request:ImportPreview):
        with self.store.connection() as db:
            db.execute('BEGIN')
            case=self.store._get(db,case_id);_guard_revision(case,request.expected_revision)
            if request.previous_document_id:self._document(db,case_id,request.previous_document_id)
            duplicates=self._duplicates(db,case_id,request.text)
            db.rollback()
        return {'persisted':False,'revision':case.revision,'characters':len(request.text),'utf8_bytes':len(request.text.encode('utf-8')),
                'content_sha256':text_hash(request.text),'chunks':len(chunks(request.text)),
                'warnings':source_warnings(request.text),'duplicates':duplicates,
                'notice':'Original text will be retained unchanged. Matching text is not evidence that two people or sources are the same.'}

    def import_source(self,case_id,request:ImportSource):
        # Hash the complete intent without repeating long text in every audit event.
        intent=request.model_dump(mode='json');intent['text']=text_hash(request.text)
        request_hash=digest(intent)
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case=self.store._get(db,case_id)
                if self.store._duplicate(db,case_id,request.event_id,request_hash):
                    rec=json.loads(db.execute('SELECT record FROM v2_events WHERE case_id=? AND event_id=?',(case_id,request.event_id)).fetchone()['record'])
                    doc=self._document(db,case_id,rec['payload']['document']['id']);db.rollback()
                    return case,{'duplicate':True},_metadata(doc)
                _guard_revision(case,request.expected_revision)
                if request.previous_document_id:self._document(db,case_id,request.previous_document_id)
                rows=db.execute('SELECT metadata FROM v2_source_documents WHERE case_id=?',(case_id,)).fetchall()
                if len(rows)>=MAX_DOCUMENTS:raise ValueError('Local per-case document limit reached')
                if sum(json.loads(r['metadata'])['utf8_bytes'] for r in rows)+len(request.text.encode('utf-8'))>MAX_CASE_SOURCE_BYTES:
                    raise ValueError('Local per-case source storage limit reached')
                duplicates=self._duplicates(db,case_id,request.text)
                if duplicates and request.duplicate_policy=='reject':
                    raise Conflict('Matching source text already exists. Use it, or explicitly record a separate source with a reason.')
                now=utcnow();doc_id=uid()
                metadata={'id':doc_id,'case_id':case_id,'title':request.title,'source':request.source,'filename':request.filename,
                          'previous_document_id':request.previous_document_id,'created_at':now.isoformat(),
                          'created_revision':case.revision+1,'content_sha256':text_hash(request.text),
                          'comparison_sha256':comparison_hash(request.text),'characters':len(request.text),
                          'utf8_bytes':len(request.text.encode('utf-8')),'line_count':len(line_starts(request.text)),
                          'warnings':source_warnings(request.text),'text_format':'utf8-codepoints-v1'}
                db.execute('INSERT INTO v2_source_documents VALUES(?,?,?,?,?,?)',
                           (case_id,doc_id,canonical(metadata),request.text,'active',''))
                updated=_new_revision(case,now)
                cmd=Command(event_id=request.event_id,expected_revision=case.revision,kind='import_source',
                            payload={'document':metadata,'duplicate_reason':request.duplicate_reason,
                                     'duplicate_matches':duplicates})
                delta=self.store._persist(db,case,updated,cmd,'local-operator',now,request_hash=request_hash,
                                          extra_objects=[{'collection':'source_documents','id':doc_id,'change':'added'}])
                db.commit()
                return updated,delta,{**metadata,'status':'active','retraction_reason':''}
            except Exception:db.rollback();raise

    def read(self,case_id,document_id,start=0,limit=CHUNK_SIZE):
        if type(start) is not int or type(limit) is not int or start<0 or not 1<=limit<=MAX_BATCH_CHARS:
            raise ValueError('Invalid source page range')
        with self.store.connection() as db:
            db.execute('BEGIN');self.store._get(db,case_id);doc=self._document(db,case_id,document_id);db.rollback()
        if start>=len(doc['text']):raise ValueError('Source offset is outside the original')
        end=min(len(doc['text']),start+limit);part=doc['text'][start:end];lines=line_starts(doc['text'])
        return {'document':_metadata(doc),'start':start,'end':end,'text':part,'content_sha256':text_hash(part),
                'line_start':bisect_right(lines,start),'line_end':bisect_right(lines,end-1),
                'partial':start!=0 or end!=len(doc['text']),'next_start':end if end<len(doc['text']) else None,
                'chunks':chunks(doc['text']),'offset_unit':'unicode_code_points_end_exclusive'}

    def search(self,case_id,document_id,query):
        if not isinstance(query,str) or not 2<=len(query)<=200 or not query.strip():
            raise ValueError('Use a non-blank query of 2 to 200 characters')
        with self.store.connection() as db:
            db.execute('BEGIN');self.store._get(db,case_id);doc=self._document(db,case_id,document_id);db.rollback()
        matches=[];truncated=False
        for m in re.finditer(re.escape(query),doc['text'],flags=re.IGNORECASE):
            if len(matches)==50:truncated=True;break
            lo=max(0,m.start()-90);hi=min(len(doc['text']),m.end()+130)
            matches.append({'start':m.start(),'end':m.end(),'quote':m.group(),'context':doc['text'][lo:hi],
                            'context_start':lo,'context_end':hi})
        return {'matches':matches,'truncated':truncated,'persisted':False,'notice':'Literal, case-insensitive search. No semantic inference.'}

    def selection(self,case_id,document_id,request:SourceSelection):
        page=self.read(case_id,document_id,request.start,request.end-request.start)
        if page['end']!=request.end:raise ValueError('Selection extends beyond the original')
        if page['document']['status']!='active':raise ValueError('Cannot select evidence from a retracted original')
        return {k:v for k,v in page.items() if k!='chunks'}

    def resolve_span(self,case_id,span):
        case=self.store.get(case_id)
        evidence=next((e for e in case.evidence if e.id==span.evidence_id),None)
        if not evidence:raise KeyError(span.evidence_id)
        if evidence.text[span.start:span.end]!=span.quote:
            raise ValueError('Quotation does not match this evidence excerpt')
        source=self.origin(case_id,span.evidence_id)
        if not source['linked']:
            return {**source,'quote':span.quote,'evidence_start':span.start,'evidence_end':span.end,'evidence_status':evidence.status}
        link=source['passage']
        return {**source,'text':span.quote,'quote':span.quote,'original_start':link['start']+span.start,
                'original_end':link['start']+span.end,'evidence_start':span.start,'evidence_end':span.end}

    def _passages(self,db,case,request):
        _guard_revision(case,request.expected_revision)
        results=[]
        if len(case.evidence)+len(request.passages)>200:raise ValueError('Local evidence limit reached')
        for p in request.passages:
            doc=self._document(db,case.id,p.document_id)
            if doc['status']!='active':raise ValueError('Retracted originals cannot supply new passages')
            if p.end>len(doc['text']):raise ValueError('Passage is outside the source text')
            text=doc['text'][p.start:p.end]
            if not text.strip():raise ValueError('An empty/whitespace passage is not evidence')
            if text_hash(text)!=p.content_sha256:raise Conflict('The selected text does not match the original passage hash. Refresh and review it.')
            existing=db.execute('SELECT evidence_id FROM v2_source_passages WHERE case_id=? AND document_id=? AND start_offset=? AND end_offset=?',
                                (case.id,p.document_id,p.start,p.end)).fetchone()
            if existing:raise Conflict('This exact passage is already evidence. Open the existing excerpt rather than duplicating it.')
            same=[e.id for e in case.evidence if text_hash(e.text)==p.content_sha256]
            results.append({'document_id':doc['id'],'title':doc['title'],'source':doc['source'],'start':p.start,'end':p.end,
                            'text':text,'content_sha256':p.content_sha256,'original_sha256':doc['content_sha256'],
                            'same_text_evidence_ids':same})
        return results

    def preview_passages(self,case_id,request:PassagePreview):
        with self.store.connection() as db:
            db.execute('BEGIN');case=self.store._get(db,case_id);items=self._passages(db,case,request);db.rollback()
        return {'revision':case.revision,'passages':items,'characters':sum(len(i['text']) for i in items),'persisted':False,
                'notice':'Only these passages will become unreviewed evidence. Reading, previewing and selection do not send anything to a model.'}

    def capture(self,case_id,request:CapturePassages):
        request_hash=digest(request.model_dump(mode='json'))
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case=self.store._get(db,case_id)
                if self.store._duplicate(db,case_id,request.event_id,request_hash):
                    rec=json.loads(db.execute('SELECT record FROM v2_events WHERE case_id=? AND event_id=?',(case_id,request.event_id)).fetchone()['record']);db.rollback()
                    return case,{'duplicate':True},[p['evidence_id'] for p in rec['payload']['passages']]
                items=self._passages(db,case,request);now=utcnow();data=case.model_dump(mode='json');links=[]
                for item in items:
                    suffix=f" [{item['start']}:{item['end']}]"
                    title=item['title'][:180-len(suffix)]+suffix
                    e=Evidence(title=title,source=item['source'],text=item['text'])
                    data['evidence'].append(e.model_dump(mode='json'))
                    link={'case_id':case_id,'document_id':item['document_id'],'evidence_id':e.id,'start':item['start'],'end':item['end'],
                          'content_sha256':item['content_sha256'],'original_sha256':item['original_sha256'],
                          'created_revision':case.revision+1}
                    db.execute('INSERT INTO v2_source_passages VALUES(?,?,?,?,?,?,?)',
                               (case_id,e.id,item['document_id'],item['start'],item['end'],canonical(link),link['content_sha256']))
                    links.append(link)
                data.update(revision=case.revision+1,updated_at=now.isoformat(),approvals=[])
                updated=Case.model_validate(data)
                cmd=Command(event_id=request.event_id,expected_revision=case.revision,kind='capture_passages',payload={'passages':links})
                delta=self.store._persist(db,case,updated,cmd,'local-operator',now,request_hash=request_hash)
                db.commit();return updated,delta,[x['evidence_id'] for x in links]
            except Exception:db.rollback();raise

    def retract(self,case_id,document_id,request:RetractSource):
        request_hash=digest({'document_id':document_id,**request.model_dump(mode='json')})
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case=self.store._get(db,case_id)
                if self.store._duplicate(db,case_id,request.event_id,request_hash):db.rollback();return case,{'duplicate':True}
                _guard_revision(case,request.expected_revision);doc=self._document(db,case_id,document_id)
                if doc['status']=='retracted':raise ValueError('Source is already retracted; its history is preserved')
                eids=[r['evidence_id'] for r in db.execute('SELECT evidence_id FROM v2_source_passages WHERE case_id=? AND document_id=?',(case_id,document_id))]
                data=case.model_dump(mode='json');now=utcnow()
                for e in data['evidence']:
                    if e['id'] in eids:e['status']='retracted'
                data.update(revision=case.revision+1,updated_at=now.isoformat(),approvals=[])
                updated=Case.model_validate(data)
                if updated.status=='closed' and not plan(updated,now)['outcome_evidenced']:updated.status='active'
                db.execute('UPDATE v2_source_documents SET status=?,retraction_reason=? WHERE case_id=? AND id=?',
                           ('retracted',request.reason,case_id,document_id))
                cmd=Command(event_id=request.event_id,expected_revision=case.revision,kind='retract_source',
                            payload={'document_id':document_id,'reason':request.reason,'evidence_ids':eids})
                delta=self.store._persist(db,case,updated,cmd,'local-operator',now,request_hash=request_hash,
                                          extra_objects=[{'collection':'source_documents','id':document_id,'change':'retracted'}])
                db.commit();return updated,delta
            except Exception:db.rollback();raise

    def origin(self,case_id,evidence_id):
        with self.store.connection() as db:
            db.execute('BEGIN');case=self.store._get(db,case_id)
            e=next((e for e in case.evidence if e.id==evidence_id),None)
            if not e:raise KeyError(evidence_id)
            row=db.execute('SELECT body FROM v2_source_passages WHERE case_id=? AND evidence_id=?',(case_id,evidence_id)).fetchone()
            if not row:
                db.rollback();return {'linked':False,'evidence_id':evidence_id,'notice':'This excerpt predates Source Desk or was added directly. No original-text location is invented.'}
            link=json.loads(row['body']);doc=self._document(db,case_id,link['document_id']);db.rollback()
        if e.text!=doc['text'][link['start']:link['end']] or text_hash(e.text)!=link['content_sha256']:
            raise ValueError('Source lineage does not match this evidence excerpt')
        return {'linked':True,'passage':link,'document':_metadata(doc),'evidence_status':e.status,'text':e.text}


def verify_source_store(case:Case,events:list[dict],documents:list[dict],passages:list[dict]) -> dict:
    """Check immutable originals and exact bindings against case-chain anchors."""
    problems=[];expected_docs={};expected_links={};retracted={}
    for e in events:
        payload=e.get('payload',{})
        if e['kind']=='import_source':
            d=payload['document'];expected_docs[d['id']]=d
        elif e['kind']=='capture_passages':
            for p in payload['passages']:expected_links[p['evidence_id']]=p
        elif e['kind']=='retract_source':retracted[payload['document_id']]=payload['reason']
    actual={d['id']:d for d in documents};links={p['evidence_id']:p for p in passages};es={e.id:e for e in case.evidence}
    if actual.keys()!=expected_docs.keys():problems.append('Source inventory does not match case-chain imports')
    if links.keys()!=expected_links.keys():problems.append('Passage inventory does not match case-chain captures')
    for id,d in actual.items():
        if _descriptor(d)!=expected_docs.get(id):problems.append('Source metadata differs from its import anchor: '+id)
        if d['case_id']!=case.id or text_hash(d['text'])!=d['content_sha256']:problems.append('Original text hash or case mismatch: '+id)
        expected_status='retracted' if id in retracted else 'active'
        if d['status']!=expected_status or d['retraction_reason']!=retracted.get(id,''):problems.append('Source retraction history mismatch: '+id)
    for eid,p in links.items():
        d=actual.get(p['document_id']);e=es.get(eid)
        if p!=expected_links.get(eid):problems.append('Passage descriptor differs from capture anchor: '+eid)
        if not d or not e or p['case_id']!=case.id:
            problems.append('Passage has missing or cross-case references: '+eid);continue
        if not 0<=p['start']<p['end']<=len(d['text']) or e.text!=d['text'][p['start']:p['end']]:
            problems.append('Passage does not match the original text: '+eid)
        if text_hash(e.text)!=p['content_sha256'] or p['original_sha256']!=d['content_sha256']:
            problems.append('Passage hash mismatch: '+eid)
        if d['status']=='retracted' and e.status!='retracted':problems.append('Retracted source still supplies active evidence: '+eid)
    return {'valid':not problems,'problems':problems,'documents':len(documents),'passages':len(passages),
            'scope':'Source hashes and spans anchored in the same local case chain. Not independently notarised or administrator-proof.'}
