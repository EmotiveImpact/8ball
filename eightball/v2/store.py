"""Versioned snapshots, optimistic transactions and a replayable hash-linked ledger.
V1 tables are left untouched. Model proposals have a separate non-authoritative log.
"""
import json
import sqlite3
from datetime import datetime
from .contracts import Case, Proposal, Provenance, OBJECT_TYPES
from .commands import Command, apply, merge_object, preserve_meaning
from .planner import plan, changes
from ..store import Store as LegacyStore, Conflict, canonical, digest
from ..models import utcnow


class Store(LegacyStore):
    def __init__(self,path):
        super().__init__(path)
        with self.connection() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS v2_cases(id TEXT PRIMARY KEY,revision INTEGER NOT NULL,snapshot TEXT NOT NULL,legacy_id TEXT UNIQUE);
            CREATE TABLE IF NOT EXISTS v2_events(case_id TEXT NOT NULL REFERENCES v2_cases(id),event_id TEXT NOT NULL,
                revision INTEGER NOT NULL,record TEXT NOT NULL,hash TEXT NOT NULL,
                PRIMARY KEY(case_id,event_id),UNIQUE(case_id,revision));
            CREATE TABLE IF NOT EXISTS v2_proposals(case_id TEXT NOT NULL REFERENCES v2_cases(id),id TEXT PRIMARY KEY,
                body TEXT NOT NULL,review_record TEXT);
            CREATE TABLE IF NOT EXISTS v2_lineage(case_id TEXT PRIMARY KEY REFERENCES v2_cases(id),source_export TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS v2_proposals_case ON v2_proposals(case_id);
            CREATE TABLE IF NOT EXISTS v2_source_documents(
                case_id TEXT NOT NULL REFERENCES v2_cases(id), id TEXT NOT NULL,
                metadata TEXT NOT NULL, text TEXT NOT NULL, status TEXT NOT NULL,
                retraction_reason TEXT NOT NULL, PRIMARY KEY(case_id,id));
            CREATE TABLE IF NOT EXISTS v2_source_passages(
                case_id TEXT NOT NULL REFERENCES v2_cases(id), evidence_id TEXT NOT NULL,
                document_id TEXT NOT NULL, start_offset INTEGER NOT NULL, end_offset INTEGER NOT NULL,
                body TEXT NOT NULL, content_sha256 TEXT NOT NULL, PRIMARY KEY(case_id,evidence_id),
                UNIQUE(case_id,document_id,start_offset,end_offset),
                FOREIGN KEY(case_id,document_id) REFERENCES v2_source_documents(case_id,id));
            CREATE TABLE IF NOT EXISTS v2_insight_events(
                case_id TEXT NOT NULL REFERENCES v2_cases(id), event_id TEXT NOT NULL,
                sequence INTEGER NOT NULL, record TEXT NOT NULL, hash TEXT NOT NULL,
                PRIMARY KEY(case_id,event_id), UNIQUE(case_id,sequence));
            CREATE TABLE IF NOT EXISTS v2_grounding_events(
                case_id TEXT NOT NULL REFERENCES v2_cases(id), event_id TEXT NOT NULL,
                sequence INTEGER NOT NULL, record TEXT NOT NULL, hash TEXT NOT NULL,
                PRIMARY KEY(case_id,event_id), UNIQUE(case_id,sequence));
            CREATE TABLE IF NOT EXISTS v2_plan_reviews(
                case_id TEXT NOT NULL REFERENCES v2_cases(id), event_id TEXT NOT NULL,
                sequence INTEGER NOT NULL, record TEXT NOT NULL, hash TEXT NOT NULL,
                PRIMARY KEY(case_id,event_id), UNIQUE(case_id,sequence));
            CREATE TABLE IF NOT EXISTS v2_course_events(
                case_id TEXT NOT NULL REFERENCES v2_cases(id), event_id TEXT NOT NULL,
                sequence INTEGER NOT NULL, record TEXT NOT NULL, hash TEXT NOT NULL,
                PRIMARY KEY(case_id,event_id), UNIQUE(case_id,sequence));
            PRAGMA user_version=2;
            ''')

    def list(self):
        with self.connection() as db:
            return [Case.model_validate_json(r['snapshot']) for r in db.execute('SELECT snapshot FROM v2_cases ORDER BY rowid DESC')]

    def _get(self,db,case_id):
        row=db.execute('SELECT snapshot FROM v2_cases WHERE id=?',(case_id,)).fetchone()
        if not row:raise KeyError(case_id)
        return Case.model_validate_json(row['snapshot'])

    def get(self,case_id):
        with self.connection() as db:return self._get(db,case_id)

    def _append(self,db,case,event_id,kind,payload,actor,request_hash,delta=None):
        previous=db.execute('SELECT hash FROM v2_events WHERE case_id=? ORDER BY revision DESC LIMIT 1',(case.id,)).fetchone()
        state=case.model_dump(mode='json')
        record={'case_id':case.id,'event_id':event_id,'revision':case.revision,'kind':kind,'payload':payload,
                'actor':actor,'recorded_at':utcnow().isoformat(),'previous_hash':previous['hash'] if previous else None,
                'state_hash':digest(state),'request_hash':request_hash,'state_after':state,'changes':delta}
        db.execute('INSERT INTO v2_events VALUES(?,?,?,?,?)',(case.id,event_id,case.revision,canonical(record),digest(record)))

    def create(self,case:Case,actor='local-operator',lineage=None,*,fixture=False):
        if case.revision or (not fixture and not lineage and (case.evidence or case.observations or case.completed or case.approvals)):
            raise ValueError('New cases cannot import attestations through intake')
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                if db.execute('SELECT COUNT(*) FROM v2_cases').fetchone()[0]>=200:raise ValueError('Local case limit reached')
                if case.legacy_id:
                    row=db.execute('SELECT snapshot FROM v2_cases WHERE legacy_id=?',(case.legacy_id,)).fetchone()
                    if row:
                        db.rollback();return Case.model_validate_json(row['snapshot'])
                db.execute('INSERT INTO v2_cases VALUES(?,?,?,?)',(case.id,0,case.model_dump_json(),case.legacy_id))
                if lineage:db.execute('INSERT INTO v2_lineage VALUES(?,?)',(case.id,canonical(lineage)))
                self._append(db,case,'created','legacy_import' if lineage else 'fictional_fixture' if fixture else 'created',
                             {'lineage_hash':digest(lineage)} if lineage else {},actor,None)
                db.commit()
            except Exception:
                db.rollback();raise
        return case

    def _duplicate(self,db,case_id,event_id,request_hash):
        row=db.execute('SELECT record FROM v2_events WHERE case_id=? AND event_id=?',(case_id,event_id)).fetchone()
        if not row:return False
        if json.loads(row['record'])['request_hash']!=request_hash:raise Conflict('Idempotency key already belongs to another command')
        return True

    def _persist(self,db,before,after,command,actor,now,*,request_hash=None,extra_objects=None):
        delta=changes(before,after,plan(before,now),plan(after,now))
        if extra_objects:delta['objects'].extend(extra_objects)
        db.execute('UPDATE v2_cases SET revision=?,snapshot=? WHERE id=?',(after.revision,after.model_dump_json(),after.id))
        self._append(db,after,command.event_id,command.kind,command.payload,actor,request_hash or digest(command.model_dump(mode='json')),delta)
        return delta

    def change(self,case_id,command:Command,actor='local-operator'):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case=self._get(db,case_id)
                if self._duplicate(db,case_id,command.event_id,digest(command.model_dump(mode='json'))):
                    db.rollback();return case,{'duplicate':True}
                if command.expected_revision!=case.revision:raise Conflict('Case changed. Reload before making this decision.')
                if case.revision>=2000:raise ValueError('Local event limit reached')
                now=utcnow();updated=apply(case,command,actor,now)
                delta=self._persist(db,case,updated,command,actor,now);db.commit()
                return updated,delta
            except Exception:
                db.rollback();raise

    def save_proposal(self,proposal:Proposal):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                self._get(db,proposal.case_id)
                if db.execute('SELECT COUNT(*) FROM v2_proposals WHERE case_id=?',(proposal.case_id,)).fetchone()[0]>=200:
                    raise ValueError('Local proposal limit reached')
                db.execute('INSERT INTO v2_proposals VALUES(?,?,?,NULL)',(proposal.case_id,proposal.id,proposal.model_dump_json()))
                db.commit()
            except Exception:db.rollback();raise
        return proposal

    def proposals(self,case_id):
        with self.connection() as db:
            self._get(db,case_id)
            return [json.loads(r['body']) for r in db.execute('SELECT body FROM v2_proposals WHERE case_id=? ORDER BY rowid DESC',(case_id,))]

    def review(self,case_id,proposal_id,event_id,expected_revision,choices,actor='local-operator'):
        """A single transaction applies reviewed objects and records dispositions.
        Rejecting everything updates the proposal log, never the live case revision.
        """
        command=Command(event_id=event_id,expected_revision=expected_revision,kind='apply_proposal',
                        payload={'proposal_id':proposal_id,'choices':choices})
        request_hash=digest(command.model_dump(mode='json'))
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case=self._get(db,case_id)
                row=db.execute('SELECT body,review_record FROM v2_proposals WHERE case_id=? AND id=?',(case_id,proposal_id)).fetchone()
                if not row:raise KeyError(proposal_id)
                if row['review_record']:
                    previous=json.loads(row['review_record'])
                    if previous['request_hash']==request_hash:
                        db.rollback();return case,{'duplicate':True}
                    raise Conflict('This proposal has already been reviewed')
                if self._duplicate(db,case_id,event_id,request_hash):raise Conflict('Command ID is not available')
                proposal=Proposal.model_validate_json(row['body'])
                if proposal.status!='pending':raise ValueError('Only pending proposals can be reviewed')
                if case.revision!=expected_revision or case.revision!=proposal.base_revision:
                    raise Conflict('This proposal is stale. Reanalyse against the current case revision.')
                if len(choices)!=len(proposal.items) or {c['id'] for c in choices}!={i.id for i in proposal.items}:
                    raise ValueError('Review each proposal item exactly once')
                by_id={c['id']:c for c in choices}
                if len(by_id)!=len(choices):raise ValueError('Duplicate review selection')
                data=case.model_dump(mode='json');accepted=0
                for item in proposal.items:
                    choice=by_id[item.id];disposition=choice['disposition']
                    if disposition not in ('accepted','edited','rejected'):raise ValueError('Invalid review disposition')
                    if disposition!='rejected':
                        value=choice.get('object') if disposition=='edited' else item.object
                        if value is None:raise ValueError('Edited proposals require a complete object')
                        obj=OBJECT_TYPES[item.kind].model_validate(value)
                        # Preserve model provenance even when a reviewer edits content.
                        if hasattr(obj,'provenance'):
                            prov=obj.provenance.model_copy(update={'origin':item.object.get('provenance',{}).get('origin','model_proposal'),'run_id':proposal.id})
                            value={**obj.model_dump(mode='json'),'provenance':prov.model_dump(mode='json')}
                        else:value=obj.model_dump(mode='json')
                        if item.kind=='decision' and (obj.selected or obj.decided_at or obj.decided_revision is not None):
                            raise ValueError('A proposal cannot record a human decision')
                        if item.kind=='question' and (obj.status!='open' or obj.answer or obj.evidence_ids):
                            raise ValueError('A proposal cannot resolve a question')
                        if item.kind=='constraint' and obj.confirmed:
                            raise ValueError('Confirm proposed constraints in a separate operator review')
                        if item.kind=='event' and obj.status=='operator_confirmed':
                            raise ValueError('Model-reported events are not confirmed facts')
                        merge_object(data,item.kind,value,allow_replace=False);accepted+=1
                    item.disposition=disposition
                now=utcnow();delta={'no_case_change':True}
                if accepted:
                    data.update(revision=case.revision+1,updated_at=now.isoformat(),approvals=[])
                    updated=preserve_meaning(case,Case.model_validate(data))
                    delta=self._persist(db,case,updated,command,actor,now)
                else:updated=case
                proposal.status='reviewed'
                review_record={'actor':actor,'recorded_at':now.isoformat(),'case_revision':updated.revision,
                               'request_hash':request_hash,'choices':choices,'proposal_hash':digest(json.loads(row['body']))}
                db.execute('UPDATE v2_proposals SET body=?,review_record=? WHERE id=? AND case_id=?',
                           (proposal.model_dump_json(),canonical(review_record),proposal_id,case_id))
                db.commit();return updated,delta
            except Exception:db.rollback();raise

    def audit(self,case_id):
        with self.connection() as db:
            db.execute('BEGIN')
            case=self._get(db,case_id)
            rows=db.execute('SELECT record,hash FROM v2_events WHERE case_id=? ORDER BY revision',(case_id,)).fetchall()
            traces=[{'proposal':json.loads(r['body']),'review':json.loads(r['review_record']) if r['review_record'] else None}
                    for r in db.execute('SELECT body,review_record FROM v2_proposals WHERE case_id=? ORDER BY rowid',(case_id,))]
            from .source_desk import decode_document
            documents=[decode_document(r) for r in db.execute('SELECT * FROM v2_source_documents WHERE case_id=? ORDER BY rowid',(case_id,))]
            passages=[json.loads(r['body']) for r in db.execute('SELECT body FROM v2_source_passages WHERE case_id=? ORDER BY rowid',(case_id,))]
            from .insights import ledger_rows, export_ledger
            insight_rows=ledger_rows(db,case_id)
            from .grounding import read_events as grounding_events, export_reviews
            grounding_error = False
            try: grounding_rows=grounding_events(db,case_id)
            except (ValueError, KeyError, TypeError): grounding_rows=[]; grounding_error=True
            from .plan_review import read_journal, export_journal
            review_rows = read_journal(db,case_id)
            from .courses import read_rows, export_courses
            course_rows = read_rows(db,case_id)
            lineage=db.execute('SELECT source_export FROM v2_lineage WHERE case_id=?',(case_id,)).fetchone()
            db.rollback()
        previous=None;valid=True;events=[];replay=None
        for n,row in enumerate(rows):
            rec=json.loads(row['record'])
            valid=valid and rec['case_id']==case_id and rec['revision']==n and rec['previous_hash']==previous and digest(rec)==row['hash']
            replay=Case.model_validate(rec['state_after'])
            valid=valid and replay.revision==n and digest(replay.model_dump(mode='json'))==rec['state_hash']
            events.append({**rec,'hash':row['hash']});previous=row['hash']
        valid=bool(valid and replay and replay==case and len(events)==case.revision+1)
        from .source_desk import verify_source_store
        source_integrity=verify_source_store(case,events,documents,passages)
        case_valid=valid;valid=valid and source_integrity['valid']
        extras={'source_documents':documents,'source_passages':passages,'source_integrity':source_integrity,'case_chain_valid':case_valid} if documents or passages or not source_integrity['valid'] else {}
        insight_export=export_ledger(insight_rows,case_id)
        if insight_export is not None:
            extras['emergent_insights']=insight_export
            valid=valid and insight_export['valid']
        grounding_export=export_reviews(grounding_rows,events)
        if grounding_error: grounding_export={'valid':False,'error':'Source interpretation journal failed verification'}
        if grounding_export is not None:
            extras['source_interpretations']=grounding_export
            valid=valid and grounding_export['valid']
        course_export = export_courses(course_rows,case_id,events)
        if course_export is not None:
            extras['chosen_courses'] = course_export
            valid = valid and course_export['valid']
        review_export = export_journal(review_rows,case_id,events)
        if review_export is not None:
            extras['plan_reviews'] = review_export
            valid = valid and review_export['valid']
        return {**extras,'format':'eightball-case-v2' ,'valid':valid,'head_hash':previous,'case':case.model_dump(mode='json'),
                'events':events,'model_runs':traces,'legacy_lineage':json.loads(lineage['source_export']) if lineage else None,
                'replay_matches_snapshot':bool(replay==case),'audit_scope':'Application hash chain and snapshot replay; not independently anchored or administrator-proof'}

    def history(self,case_id):
        data=self.audit(case_id)
        return {'valid':data['valid'],'head_hash':data['head_hash'],'events':[{k:v for k,v in e.items() if k!='state_after'} for e in data['events']]}
