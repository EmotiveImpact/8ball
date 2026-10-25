"""Explicit reviewed graph consumption in one local database transaction.

The host must authenticate the reviewer before calling this service. It is not
an HTTP endpoint or a replacement for production PostgreSQL tenant policies.
"""
import json
from endstate.events import EventReceipt

from ..agency_access import AccessRegistry
from ..authorisation import Grant, Identity, Operation, Resource, permits
from ..event_inbox import EventInbox
from ..event_work import EventWork
from ..models import utcnow
from ..store import Conflict, canonical, digest
from .commands import Command, apply
from .event_outbox import EventOutbox


class EventReviews:
    def __init__(self, store):
        self.store = store
        # Grants, attempts and cases must share the transaction database.
        AccessRegistry(store.path)
        EventWork(store.path)
        EventOutbox(store)
        with store.connection() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS event_consumptions (
                work_id TEXT PRIMARY KEY REFERENCES event_work(id),
                case_id TEXT NOT NULL REFERENCES v2_cases(id),
                organisation_id TEXT NOT NULL, matter_id TEXT NOT NULL,
                record TEXT NOT NULL, digest TEXT NOT NULL)''')

    def view(self, *, work_id: str, case_id: str, reader: Identity):
        """Read original source and output at one current authorised snapshot."""
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            _, scope = EventOutbox._authorize(db, case_id, reader)
            work = db.execute('SELECT * FROM event_work WHERE id=? AND organisation_id=? AND matter_id=? AND case_id=?',
                              (work_id, *scope, case_id)).fetchone()
            if work is None:
                raise KeyError('Processing attempt not found')
            row = db.execute('''SELECT sequence,received_at,body,digest FROM incoming_events
                WHERE organisation_id=? AND matter_id=? AND sequence=?''',
                (*scope, work['sequence'])).fetchone()
            if row is None:
                raise Conflict('Incoming event is missing')
            receipt = EventInbox._receipt(tuple(row))
            if (receipt.event.organisation_id, receipt.event.matter_id) != scope:
                raise Conflict('Incoming event scope is corrupt')
            case = self.store._get(db, case_id)
            result = dict(work_id=work_id, case_id=case_id, state=work['state'],
                          base_revision=work['base_revision'], current_revision=case.revision,
                          source_receipt=receipt.model_dump(mode='json'), original_result=work['result'],
                          reviewable=work['state']=='awaiting_review' and work['base_revision']==case.revision,
                          command_authority=False)
            EventOutbox._authorize(db, case_id, reader)
            return result

    def commit_graph(self, *, work_id: str, case_id: str, reviewer: Identity,
                     command: Command, rationale: str, require_read: bool = False):
        if not isinstance(reviewer, Identity) or not isinstance(command, Command):
            raise ValueError('Verified identity and typed command required')
        if command.kind != 'replace_graph' or not isinstance(rationale, str) or len(rationale.strip()) < 10 or len(rationale) > 2000:
            raise ValueError('An explicit reviewed graph command and rationale are required')
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            work = db.execute('SELECT * FROM event_work WHERE id=?', (work_id,)).fetchone()
            ownership = db.execute('SELECT organisation_id,matter_id FROM agency_case_scope WHERE case_id=?',
                                   (case_id,)).fetchone()
            if work is None or ownership is None or tuple(ownership) != (work['organisation_id'], work['matter_id']):
                raise PermissionError('Matter access is not permitted')
            if work['case_id'] is not None and work['case_id'] != case_id:
                raise PermissionError('Processing result belongs to a different case')
            scope = Resource(organisation_id=work['organisation_id'], matter_id=work['matter_id'])
            now = utcnow()
            grants = tuple(Grant.model_validate_json(row['body']) for row in
                           db.execute('SELECT body FROM agency_grants WHERE revoked=0'))
            if not permits(reviewer, scope, Operation.WRITE, grants, now=now):
                raise PermissionError('Current matter write permission is required')
            if require_read and not permits(reviewer, scope, Operation.READ, grants, now=now):
                raise PermissionError('Current matter read permission is required')
            source_row = db.execute('''SELECT sequence,received_at,body,digest FROM incoming_events
                WHERE organisation_id=? AND matter_id=? AND sequence=?''',
                (scope.organisation_id, scope.matter_id, work['sequence'])).fetchone()
            if source_row is None:
                raise Conflict('Incoming event is missing')
            receipt = EventInbox._receipt(tuple(source_row))
            if (receipt.event.organisation_id, receipt.event.matter_id) != tuple(ownership):
                raise Conflict('Incoming event scope is corrupt')
            request = dict(work_id=work_id, case_id=case_id,
                           organisation_id=scope.organisation_id, matter_id=scope.matter_id,
                           reviewer=reviewer.model_dump(mode='json'),
                           command=command.model_dump(mode='json'), rationale=rationale,
                           receipt_sha256=digest(receipt.model_dump(mode='json')),
                           source_sha256=receipt.content_sha256, result_sha256=digest(work['result']))
            request_hash = digest(request)
            old = db.execute('SELECT record,digest FROM event_consumptions WHERE work_id=?', (work_id,)).fetchone()
            if old:
                record = json.loads(old['record'])
                if digest(record) != old['digest'] or record['request_hash'] != request_hash:
                    raise Conflict('This processing result has a different or corrupt review')
                return record
            if work['case_id'] is None:
                raise Conflict('Historical attempt has no case binding; create an explicit new case-bound attempt')
            if work['state'] != 'awaiting_review':
                raise Conflict('Processing result is not awaiting review')
            case = self.store._get(db, case_id)
            if command.expected_revision != work['base_revision'] or case.revision != work['base_revision']:
                raise Conflict('Case changed; review a new result against the current revision')
            if case.revision >= 2000:
                raise ValueError('Local event limit reached')
            if db.execute('SELECT 1 FROM v2_events WHERE case_id=? AND event_id=?',
                          (case_id, command.event_id)).fetchone():
                raise Conflict('Review command ID is already used')
            actor = 'identity:' + digest(reviewer.model_dump(mode='json'))
            updated = apply(case, command, actor, now)
            changes = self.store._persist(db, case, updated, command, actor, now,
                                          request_hash=request_hash)
            persisted_event = json.loads(db.execute('SELECT record FROM v2_events WHERE case_id=? AND event_id=?',
                                                   (case_id, command.event_id)).fetchone()['record'])
            record = dict(request=request, request_hash=request_hash,
                          source_receipt=receipt.model_dump(mode='json'),
                          original_result=work['result'], committed_revision=updated.revision,
                          reviewed_at=persisted_event['recorded_at'], actor=actor, changes=changes,
                          explicit_review_recorded=True, unassisted_model_acceptance=False)
            db.execute('INSERT INTO event_consumptions VALUES (?,?,?,?,?,?)',
                       (work_id, case_id, scope.organisation_id, scope.matter_id,
                        canonical(record), digest(record)))
            db.execute("UPDATE event_work SET state='committed',token_hash=NULL WHERE id=?", (work_id,))
            EventOutbox.append(db, record)
            commit_time = utcnow()
            if not permits(reviewer, scope, Operation.WRITE, grants, now=commit_time):
                raise PermissionError('Write permission expired before commit')
            if require_read and not permits(reviewer, scope, Operation.READ, grants, now=commit_time):
                raise PermissionError('Read permission expired before commit')
            db.commit()
            return record


def read_consumptions(db, case_id):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='event_consumptions'").fetchone():
        return []
    return db.execute('SELECT record,digest FROM event_consumptions WHERE case_id=? ORDER BY rowid',
                      (case_id,)).fetchall()


def export_consumptions(rows, case_id, events):
    if not rows:
        return None
    records=[]
    try:
        for row in rows:
            rec=json.loads(row['record']); request=rec['request']
            if digest(rec)!=row['digest'] or digest(request)!=rec['request_hash'] or request['case_id']!=case_id:
                raise ValueError('Corrupt review')
            receipt=EventReceipt.model_validate(rec['source_receipt'])
            if (digest(receipt.model_dump(mode='json'))!=request['receipt_sha256']
                    or digest(receipt.event.model_dump(mode='json'))!=request['source_sha256']
                    or receipt.content_sha256!=request['source_sha256']
                    or digest(rec['original_result'])!=request['result_sha256']
                    or (receipt.event.organisation_id,receipt.event.matter_id)!=(request['organisation_id'],request['matter_id'])
                    or rec['actor']!='identity:'+digest(request['reviewer'])
                    or request['command']['kind']!='replace_graph'
                    or request['command']['expected_revision']+1!=rec['committed_revision']
                    or rec['explicit_review_recorded'] is not True
                    or rec['unassisted_model_acceptance'] is not False):
                raise ValueError('Unbound review source or identity')
            event=next(e for e in events if e['event_id']==request['command']['event_id'])
            if (event['request_hash']!=rec['request_hash'] or event['revision']!=rec['committed_revision']
                    or event['actor']!=rec['actor'] or event['kind']!='replace_graph'
                    or event['payload']!=request['command']['payload']
                    or event['changes']!=rec['changes'] or event['recorded_at']!=rec['reviewed_at']):
                raise ValueError('Unlinked review')
            records.append(rec)
    except (ValueError, TypeError, KeyError, StopIteration):
        return {'valid':False,'error':'Incoming-event review failed verification'}
    return {'valid':True,'records':records}
