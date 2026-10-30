"""Development dispatch with current authority and explicit, bounded attempts.

The host authenticates identities and deliberately invokes one named work item.
The injected processor may only propose; this service has no action-send adapter.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import secrets
from threading import BoundedSemaphore
from time import perf_counter
from typing import Protocol, runtime_checkable
from uuid import uuid4

from endstate.events import EventReceipt, IncomingEvent

from ..authorisation import Grant, Identity, Operation, Resource, permits
from ..event_inbox import EventConflict, EventInbox
from ..event_work import EventWork, MAX_RESULT_BYTES
from ..store import canonical, digest


class ProposalProcessor(Protocol):
    def __call__(self, receipt: EventReceipt, snapshot) -> str:
        """Return exact proposal text, never commands or observed effects."""


@runtime_checkable
class CooperativeProcessor(Protocol):
    @property
    def configuration_sha256(self) -> str:
        """Bind the reviewed models, questions and budgets to this attempt."""

    def run(self, receipt: EventReceipt, snapshot, checkpoint) -> str:
        """Revalidate host authority before and after every bounded provider call."""


class _ProcessingStopped(Exception):
    def __init__(self, state):
        self.state = state


class SourcePolicy(Protocol):
    def __call__(self, db, identity: Identity, case_id: str,
                 receipt: EventReceipt, now: datetime) -> bool:
        """Check current source access, quarantine, retention and processing/egress policy."""


def current_authority(db, identity, resource, operations, now):
    grants = tuple(Grant.model_validate_json(row['body']) for row in db.execute(
        'SELECT body FROM agency_grants WHERE revoked=0'))
    return all(permits(identity, resource, operation, grants, now=now) for operation in operations)


class EventWorkerService:
    MAX_ATTEMPTS = 3

    def __init__(self, store, *, processor: ProposalProcessor | None = None,
                 authority=current_authority, source_policy: SourcePolicy | None = None,
                 clock=None, timer=perf_counter, inference_slot=None):
        self.store, self.processor, self.authority = store, processor, authority
        self.source_policy = source_policy
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.timer = timer
        self.inference_slot = inference_slot if inference_slot is not None else BoundedSemaphore(1)
        self.inbox = EventInbox(store.path)
        self.queue = EventWork(store.path, clock=self.clock)
        with self.queue._transaction() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS event_processing_reviews (
                    id TEXT PRIMARY KEY, case_id TEXT NOT NULL, sequence INTEGER NOT NULL,
                    base_revision INTEGER NOT NULL, record TEXT NOT NULL,
                    digest TEXT NOT NULL, revoked INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE IF NOT EXISTS event_dispatch_requests (
                    case_id TEXT NOT NULL, request_id TEXT NOT NULL,
                    request_hash TEXT NOT NULL, work_id TEXT NOT NULL UNIQUE
                        REFERENCES event_work(id), review_id TEXT NOT NULL
                        REFERENCES event_processing_reviews(id),
                    PRIMARY KEY(case_id,request_id));
                CREATE TABLE IF NOT EXISTS event_dispatch_runs (
                    work_id TEXT PRIMARY KEY REFERENCES event_work(id),
                    worker_key TEXT NOT NULL, started_at TEXT NOT NULL,
                    finished_at TEXT, inference_seconds REAL, output TEXT,
                    failure_code TEXT);
                CREATE TABLE IF NOT EXISTS event_ingestion_metrics (
                    organisation_id TEXT NOT NULL, matter_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL, ingestion_seconds REAL NOT NULL,
                    PRIMARY KEY(organisation_id,matter_id,sequence));
            ''')

    def _context(self, db, case_id, identity, operations):
        if not isinstance(identity, Identity):
            raise PermissionError('Authenticated identity is required')
        row = db.execute('SELECT organisation_id,matter_id FROM agency_case_scope WHERE case_id=?',
                         (case_id,)).fetchone()
        now = self.queue._now()
        if row is None or not self.authority(db, identity, Resource(
                organisation_id=row[0], matter_id=row[1]), operations, now):
            raise PermissionError('Current matter permission is required')
        return dict(organisation_id=row[0], matter_id=row[1]), self.store._get(db, case_id)

    def _receipt(self, db, scope, sequence):
        if type(sequence) is not int or sequence < 1:
            raise ValueError('Explicit arrival sequence is required')
        row = db.execute('''SELECT sequence,received_at,body,digest FROM incoming_events
            WHERE organisation_id=? AND matter_id=? AND sequence=?''',
            (*scope.values(), sequence)).fetchone()
        if row is None:
            raise KeyError(sequence)
        receipt = EventInbox._receipt(tuple(row))
        if (receipt.event.organisation_id, receipt.event.matter_id) != tuple(scope.values()):
            raise EventConflict('Incoming event scope differs from its inbox')
        return receipt

    @staticmethod
    def _revision(case, revision):
        if type(revision) is not int or case.revision != revision:
            raise EventConflict('Reload and review the current revision')

    def _configuration_sha256(self):
        if not isinstance(self.processor, CooperativeProcessor):
            return None
        try:
            value = self.processor.configuration_sha256
        except (ValueError, TypeError):
            raise EventConflict('Processor configuration is no longer valid') from None
        if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
            raise ValueError('Invalid cooperative processor configuration digest')
        return value

    def _processing_review(self, db, review_id, case_id, receipt, revision):
        record = self._review(db, review_id, case_id, receipt, revision)
        if record.get('processor_configuration_sha256') != self._configuration_sha256():
            raise EventConflict('Processor configuration changed; review processing again')
        return record

    def ingest(self, *, case_id, identity, event: IncomingEvent):
        """Explicit text connector: no URL fetch, path scan, inference or fact adoption."""
        start = self.timer()
        with self.queue._transaction() as db:
            scope, _ = self._context(db, case_id, identity, (Operation.WRITE,))
            receipt = self.inbox.append(event, **scope, _db=db)
            db.execute('INSERT OR IGNORE INTO event_ingestion_metrics VALUES (?,?,?,?)',
                       (*scope.values(), receipt.sequence, max(0, self.timer()-start)))
            self._context(db, case_id, identity, (Operation.WRITE,))
            return receipt

    def review_source(self, *, case_id, identity, sequence, expected_revision,
                      receipt_sha256, rationale):
        if not isinstance(rationale, str) or not 10 <= len(rationale.strip()) <= 2000:
            raise ValueError('Explicit source-processing review rationale is required')
        with self.queue._transaction() as db:
            scope, case = self._context(db, case_id, identity, (Operation.READ, Operation.WRITE))
            self._revision(case, expected_revision)
            receipt = self._receipt(db, scope, sequence)
            self.require_source_policy(db, identity, case_id, receipt, self.source_policy, self.queue._now())
            if digest(receipt.model_dump(mode='json')) != receipt_sha256:
                raise EventConflict('Source receipt changed')
            record = dict(case_id=case_id, sequence=sequence, base_revision=expected_revision,
                          receipt_sha256=receipt_sha256, reviewer=identity.model_dump(mode='json'),
                          rationale=rationale, reviewed_at=self.queue._now().isoformat(),
                          source_facts_verified=False, action_authorised=False)
            configuration = self._configuration_sha256()
            if configuration is not None:
                record['processor_configuration_sha256'] = configuration
            review_id = uuid4().hex
            db.execute('INSERT INTO event_processing_reviews VALUES (?,?,?,?,?,?,0)',
                       (review_id, case_id, sequence, expected_revision, canonical(record), digest(record)))
            self._context(db, case_id, identity, (Operation.READ, Operation.WRITE))
            self.require_source_policy(db, identity, case_id, receipt, self.source_policy, self.queue._now())
            return dict(id=review_id, **record)

    def revoke_source_review(self, *, case_id, identity, review_id):
        with self.queue._transaction() as db:
            self._context(db, case_id, identity, (Operation.READ, Operation.WRITE))
            row = db.execute('SELECT id FROM event_processing_reviews WHERE id=? AND case_id=?',
                             (review_id, case_id)).fetchone()
            if row is None:
                raise KeyError(review_id)
            db.execute('UPDATE event_processing_reviews SET revoked=1 WHERE id=?', (review_id,))
            self._context(db, case_id, identity, (Operation.READ, Operation.WRITE))

    @staticmethod
    def _review(db, review_id, case_id, receipt, revision):
        row = db.execute('SELECT * FROM event_processing_reviews WHERE id=? AND case_id=?',
                         (review_id, case_id)).fetchone()
        if row is None or row['revoked']:
            raise EventConflict('Current explicit source-processing review is required')
        try:
            record = json.loads(row['record'])
            if (digest(record) != row['digest'] or row['base_revision'] != revision
                    or row['sequence'] != receipt.sequence or record['case_id'] != case_id
                    or record['base_revision'] != revision or record['sequence'] != receipt.sequence
                    or record['receipt_sha256'] != digest(receipt.model_dump(mode='json'))):
                raise ValueError('Mismatched review')
        except (ValueError, KeyError, TypeError):
            raise EventConflict('Source-processing review does not match this revision and receipt') from None
        return record

    @staticmethod
    def require_source_policy(db, identity, case_id, receipt, source_policy, now):
        if source_policy is None or not source_policy(db, identity, case_id, receipt, now):
            raise PermissionError('Current source processing policy is required')

    @staticmethod
    def validate_consumption(db, work, receipt, *, identity=None, source_policy=None, now=None):
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if 'event_dispatch_requests' not in tables:
            return
        request = db.execute('SELECT review_id FROM event_dispatch_requests WHERE work_id=?',
                             (work['id'],)).fetchone()
        if request:
            EventWorkerService._review(db, request['review_id'], work['case_id'],
                                       receipt, work['base_revision'])
            EventWorkerService.require_source_policy(db, identity, work['case_id'], receipt,
                                                     source_policy, now)

    def enqueue(self, *, case_id, identity, sequence, expected_revision, review_id, request_id):
        if not isinstance(request_id, str) or not 1 <= len(request_id) <= 100:
            raise ValueError('A bounded idempotency key is required')
        with self.queue._transaction() as db:
            scope, case = self._context(db, case_id, identity, (Operation.READ, Operation.INFER))
            self._revision(case, expected_revision)
            receipt = self._receipt(db, scope, sequence)
            self._processing_review(db, review_id, case_id, receipt, expected_revision)
            self.require_source_policy(db, identity, case_id, receipt, self.source_policy, self.queue._now())
            request_hash = digest(dict(case_id=case_id, sequence=sequence, revision=expected_revision,
                                       review_id=review_id, requester=identity.model_dump(mode='json')))
            old = db.execute('SELECT * FROM event_dispatch_requests WHERE case_id=? AND request_id=?',
                             (case_id, request_id)).fetchone()
            if old:
                if old['request_hash'] != request_hash:
                    raise EventConflict('Idempotency key was used for a different request')
                self._context(db, case_id, identity, (Operation.READ, Operation.INFER))
                self.require_source_policy(db, identity, case_id, receipt, self.source_policy, self.queue._now())
                return old['work_id']
            attempts = db.execute('''SELECT state FROM event_work WHERE case_id=?
                AND organisation_id=? AND matter_id=? AND sequence=?''',
                (case_id, *scope.values(), sequence)).fetchall()
            if len(attempts) >= self.MAX_ATTEMPTS:
                raise EventConflict('Explicit attempt limit reached; inspect the retained failures')
            if any(r['state'] in ('queued', 'running', 'awaiting_review', 'committed') for r in attempts):
                raise EventConflict('An active or consumed attempt already exists for this source')
            work_id = self.queue.enqueue(**scope, sequence=sequence, base_revision=expected_revision,
                                         case_id=case_id, _db=db)
            db.execute('INSERT INTO event_dispatch_requests VALUES (?,?,?,?,?)',
                       (case_id, request_id, request_hash, work_id, review_id))
            self._context(db, case_id, identity, (Operation.READ, Operation.INFER))
            self.require_source_policy(db, identity, case_id, receipt, self.source_policy, self.queue._now())
            return work_id

    def _work(self, db, case_id, scope, work_id):
        row = self.queue._row(db, tuple(scope.values()), work_id)
        if row['case_id'] != case_id:
            raise KeyError(work_id)
        request = db.execute('SELECT * FROM event_dispatch_requests WHERE work_id=? AND case_id=?',
                             (work_id, case_id)).fetchone()
        if request is None:
            raise EventConflict('Attempt is not registered for authorised dispatch')
        return row, request

    def process(self, *, case_id, work_id, worker: Identity, lease_seconds=60):
        """One explicit attempt; cooperative processors checkpoint every bounded call."""
        if self.processor is None:
            raise ValueError('An explicitly configured proposal processor is required')
        cooperative = isinstance(self.processor, CooperativeProcessor)
        with self.queue._transaction() as db:
            scope, case = self._context(db, case_id, worker, (Operation.READ, Operation.INFER))
            row, request = self._work(db, case_id, scope, work_id)
            self._revision(case, row['base_revision'])
            receipt = self._receipt(db, scope, row['sequence'])
            self._processing_review(db, request['review_id'], case_id, receipt, case.revision)
            self.require_source_policy(db, worker, case_id, receipt, self.source_policy, self.queue._now())
            token = self.queue.claim(work_id, **scope, lease_seconds=lease_seconds, _db=db)
            db.execute('INSERT INTO event_dispatch_runs(work_id,worker_key,started_at) VALUES (?,?,?)',
                       (work_id, digest(worker.model_dump(mode='json')), self.queue._now().isoformat()))
            self._context(db, case_id, worker, (Operation.READ, Operation.INFER))
            self.require_source_policy(db, worker, case_id, receipt, self.source_policy, self.queue._now())
        start = None
        def checkpoint():
            with self.queue._transaction() as db:
                try:
                    current_scope, current = self._context(db, case_id, worker, (Operation.READ, Operation.INFER))
                    if current_scope != scope:
                        raise PermissionError('Processing scope changed')
                    live, live_request = self._work(db, case_id, scope, work_id)
                    self._processing_review(db, live_request['review_id'], case_id,
                        self._receipt(db, scope, live['sequence']), live['base_revision'])
                    self.validate_consumption(db, live, self._receipt(db, scope, live['sequence']),
                        identity=worker, source_policy=self.source_policy, now=self.queue._now())
                except (PermissionError, EventConflict):
                    raise _ProcessingStopped('permission_denied') from None
                if current.revision != live['base_revision']:
                    raise _ProcessingStopped('stale')
                if (live['state'] != 'running' or self.queue._now() >= datetime.fromisoformat(live['deadline'])
                        or not isinstance(live['token_hash'], str)
                        or not secrets.compare_digest(live['token_hash'], sha256(token.encode()).hexdigest())):
                    raise _ProcessingStopped('interrupted')

        output, failure, stopped, acquired = None, None, None, False
        try:
            while not acquired:
                checkpoint()
                acquired = self.inference_slot.acquire(timeout=0.1)
            checkpoint()
            start = self.timer()
            if cooperative:
                checkpoint()
                output = self.processor.run(receipt, case.model_copy(deep=True), checkpoint)
                checkpoint()
            else:
                output = self.processor(receipt, case.model_copy(deep=True))
            if not isinstance(output, str) or not output.strip() or len(output.encode('utf-8')) > MAX_RESULT_BYTES:
                output, failure = None, 'invalid_result'
        except _ProcessingStopped as exc:
            output, failure, stopped = None, 'host_checkpoint_stopped', exc.state
        except UnicodeError:
            output, failure = None, 'invalid_result'
        except Exception:
            # Provider exception messages can contain credentials or source bytes.
            output, failure = None, 'processor_failed'
        finally:
            if acquired:
                self.inference_slot.release()
        elapsed = max(0, self.timer()-start) if start is not None else 0
        with self.queue._transaction() as db:
            row, request = self._work(db, case_id, scope, work_id)
            current = self.store._get(db, case_id)
            permitted = True
            try:
                self._context(db, case_id, worker, (Operation.READ, Operation.INFER))
                self._processing_review(db, request['review_id'], case_id,
                    self._receipt(db, scope, row['sequence']), row['base_revision'])
                self.validate_consumption(db, row, self._receipt(db, scope, row['sequence']),
                    identity=worker, source_policy=self.source_policy, now=self.queue._now())
            except (PermissionError, EventConflict):
                permitted = False
            state = self.queue.inspect(work_id, **scope, _db=db)['state']
            if cooperative and (not permitted or current.revision != row['base_revision']):
                output, failure = None, 'host_checkpoint_stopped'
                stopped = 'permission_denied' if not permitted else 'stale'
            if state == 'running':
                if failure:
                    state = stopped or 'failed'
                    db.execute('UPDATE event_work SET state=?,token_hash=NULL,finished_at=? WHERE id=?',
                               (state, self.queue._now().isoformat(), work_id))
                else:
                    state = self.queue.finish(work_id, token, output, **scope,
                        current_revision=current.revision, permission_valid=permitted, _db=db)
            db.execute('''UPDATE event_dispatch_runs SET finished_at=?,inference_seconds=?,
                output=?,failure_code=? WHERE work_id=?''',
                (self.queue._now().isoformat(), elapsed, output, failure, work_id))
            if state == 'awaiting_review':
                try:
                    self._context(db, case_id, worker, (Operation.READ, Operation.INFER))
                    self.require_source_policy(db, worker, case_id, receipt, self.source_policy,
                                               self.queue._now())
                except PermissionError:
                    state = 'permission_denied'
                if self.queue._now() >= datetime.fromisoformat(row['deadline']):
                    state = 'interrupted'
                if state != 'awaiting_review':
                    db.execute('UPDATE event_work SET state=? WHERE id=?', (state, work_id))
            if cooperative and state != 'awaiting_review':
                db.execute('UPDATE event_work SET result=NULL WHERE id=?', (work_id,))
                db.execute('UPDATE event_dispatch_runs SET output=NULL WHERE work_id=?', (work_id,))
            return dict(work_id=work_id, state=state, failure_code=failure, command_authority=False)

    def cancel(self, *, case_id, identity, work_id):
        with self.queue._transaction() as db:
            scope, _ = self._context(db, case_id, identity, (Operation.READ, Operation.WRITE))
            self._work(db, case_id, scope, work_id)
            self.queue.cancel(work_id, **scope, _db=db)
            self._context(db, case_id, identity, (Operation.READ, Operation.WRITE))

    def status(self, *, case_id, identity, work_id):
        with self.queue._transaction() as db:
            scope, _ = self._context(db, case_id, identity, (Operation.READ,))
            row, _ = self._work(db, case_id, scope, work_id)
            receipt = self._receipt(db, scope, row['sequence'])
            self.require_source_policy(db, identity, case_id, receipt, self.source_policy, self.queue._now())
            work = self.queue.inspect(work_id, **scope, _db=db)
            run = db.execute('SELECT * FROM event_dispatch_runs WHERE work_id=?', (work_id,)).fetchone()
            metrics = db.execute('''SELECT ingestion_seconds FROM event_ingestion_metrics
                WHERE organisation_id=? AND matter_id=? AND sequence=?''',
                (*scope.values(), row['sequence'])).fetchone()
            self._context(db, case_id, identity, (Operation.READ,))
            self.require_source_policy(db, identity, case_id, receipt, self.source_policy, self.queue._now())
            return dict(work=work, run=dict(run) if run else None,
                        ingestion_seconds=metrics['ingestion_seconds'] if metrics else None,
                        command_authority=False)
