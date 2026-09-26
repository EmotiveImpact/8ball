"""Explicit local analysis jobs with durable status and discard-on-cancel.

Single trusted server process, bounded queue, one shared inference slot. No job is
resumed after a restart and no automatic retry can repeat paid requests. Running
HTTP inference cannot be recalled from the provider: cancellation forbids further
stages and publication, while the current request may finish at the provider.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import json
from threading import Thread, RLock, BoundedSemaphore
from time import perf_counter
from typing import Callable

import httpx
from pydantic import Field, ValidationError
from .contracts import Strict, Identifier, Proposal, Literal
from .intelligence import propose, validate_request
from .hosted import HostedFailure, HostedSetupRequired
from ..models import uid, utcnow
from ..store import canonical, digest, Conflict
from ..providers import ProviderUnavailable
from endstate.compilation import DraftFailure

ACTIVE = {'queued', 'running'}
TERMINAL = {'succeeded', 'failed', 'cancelled', 'superseded', 'interrupted'}
MAX_QUEUE = 8
MAX_CASE_JOBS = 200


class AnalysisRequest(Strict):
    request_id: Identifier
    expected_revision: int = Field(strict=True, ge=0)
    provider: Literal['rules', 'playbook', 'ollama', 'ollama_staged', 'huggingface', 'jev', 'gliclass']
    purpose: Literal['extract', 'graph', 'questions', 'judgement']
    source_ids: list[Identifier] = Field(default_factory=list, max_length=40)
    playbook_id: Identifier | None = None
    allow_external: bool = Field(default=False, strict=True)


class JobStopped(Exception):
    """Cooperative stop, never a successful proposal."""


class JobConflict(Conflict):
    pass


def public_job(row: dict) -> dict:
    # No source content, request headers or credentials are ever part of a job.
    return {key: row[key] for key in ('id', 'case_id', 'base_revision', 'provider', 'purpose',
            'status', 'stage', 'created_at', 'updated_at', 'started_at', 'finished_at',
            'proposal_id', 'message', 'calls_started', 'calls_completed', 'worker_active')}


class ControlledClient:
    """Wrap both local JSON calls and hosted streaming with stage checkpoints."""
    def __init__(self, manager, job_id, factory=httpx.Client):
        self.manager, self.job_id = manager, job_id
        self.client = factory(follow_redirects=False, trust_env=False)

    def post(self, *args, **kwargs):
        self.manager.checkpoint(self.job_id, 'provider_request', starting=True)
        response = self.client.post(*args, **kwargs)
        self.manager.checkpoint(self.job_id, 'validating_response', completed=True)
        return response

    @contextmanager
    def stream(self, *args, **kwargs):
        self.manager.checkpoint(self.job_id, 'provider_request', starting=True)
        with self.client.stream(*args, **kwargs) as response:
            self.manager.checkpoint(self.job_id, 'reading_response')
            # Check cancellation between received chunks as well as between stages.
            original = response.iter_bytes
            def checked_bytes(*a, **kw):
                for chunk in original(*a, **kw):
                    self.manager.checkpoint(self.job_id, 'reading_response')
                    yield chunk
            response.iter_bytes = checked_bytes
            yield response
        self.manager.checkpoint(self.job_id, 'validating_response', completed=True)

    def close(self):
        self.client.close()


class AnalysisJobs:
    def __init__(self, store, inference_slot=None, *, runner: Callable = propose,
                 client_factory=httpx.Client, launch=True):
        self.store = store
        self.slot = inference_slot or BoundedSemaphore(1)
        self.runner, self.client_factory = runner, client_factory
        self.launch = launch
        self.lock = RLock()
        self.worker = None
        with self.store.connection() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS v2_analysis_jobs (
                id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES v2_cases(id),
                request_id TEXT NOT NULL, body TEXT NOT NULL,
                UNIQUE(case_id, request_id))''')
            db.execute('CREATE INDEX IF NOT EXISTS v2_jobs_case ON v2_analysis_jobs(case_id)')
            # This server supports one process. A new manager means an explicit
            # server restart; unfinished work is interrupted, NEVER auto-resumed.
            for record in db.execute('SELECT id, body FROM v2_analysis_jobs').fetchall():
                job = json.loads(record['body'])
                if job['status'] in ACTIVE or job['worker_active']:
                    if job['status'] in ACTIVE:
                        job.update(status='interrupted', stage='interrupted', finished_at=utcnow().isoformat(),
                                   message='Server restarted. No automatic retry was made; submit a new request explicitly.')
                    job.update(worker_active=False, updated_at=utcnow().isoformat())
                    self._save(db, job)
            db.commit()

    def _save(self, db, job):
        db.execute('UPDATE v2_analysis_jobs SET body=? WHERE id=?', (canonical(job), job['id']))

    def _get(self, db, job_id, case_id=None):
        row = db.execute('SELECT body FROM v2_analysis_jobs WHERE id=?', (job_id,)).fetchone()
        if not row: raise KeyError(job_id)
        job = json.loads(row['body'])
        if case_id is not None and job['case_id'] != case_id: raise KeyError(job_id)
        return job

    def get(self, case_id, job_id):
        with self.store.connection() as db:
            self.store._get(db, case_id)
            return public_job(self._get(db, job_id, case_id))

    def list(self, case_id):
        with self.store.connection() as db:
            self.store._get(db, case_id)
            rows = [json.loads(x['body']) for x in db.execute(
                'SELECT body FROM v2_analysis_jobs WHERE case_id=? ORDER BY rowid DESC', (case_id,))]
        return [public_job(x) for x in rows]

    def submit(self, case_id, request: AnalysisRequest):
        # Validate before queue admission. Misconfiguration is not a model result.
        with self.lock, self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                case = self.store._get(db, case_id)
                body = request.model_dump(mode='json')
                rhash = digest(body)
                old = db.execute('SELECT body FROM v2_analysis_jobs WHERE case_id=? AND request_id=?',
                                 (case_id, request.request_id)).fetchone()
                if old:
                    existing = json.loads(old['body'])
                    if existing['request_hash'] != rhash:
                        raise JobConflict('Request ID already belongs to different analysis settings.')
                    db.rollback()
                    return public_job(existing)
                if case.revision != request.expected_revision:
                    raise Conflict('Reload before requesting analysis.')
                validate_request(case, request.provider, request.purpose, request.source_ids,
                                 playbook_id=request.playbook_id, allow_external=request.allow_external)
                rows = [json.loads(r['body']) for r in db.execute('SELECT body FROM v2_analysis_jobs')]
                if sum(j['status'] in ACTIVE or j['worker_active'] for j in rows) >= MAX_QUEUE:
                    raise JobConflict('The local analysis queue is full. Cancel or finish existing work first.')
                if sum(j['case_id'] == case_id for j in rows) >= MAX_CASE_JOBS:
                    raise ValueError('Local per-case analysis job limit reached.')
                if db.execute('SELECT COUNT(*) FROM v2_proposals WHERE case_id=?', (case_id,)).fetchone()[0] >= 200:
                    raise ValueError('Local proposal limit reached.')
                now = utcnow().isoformat()
                job = dict(id=uid(), case_id=case_id, base_revision=case.revision,
                           provider=request.provider, purpose=request.purpose, status='queued', stage='queued',
                           created_at=now, updated_at=now, started_at=None, finished_at=None,
                           proposal_id=None, message='Queued. No case facts changed.', calls_started=0,
                           calls_completed=0, worker_active=False, request=body, request_hash=rhash)
                db.execute('INSERT INTO v2_analysis_jobs VALUES (?,?,?,?)',
                           (job['id'], case_id, request.request_id, canonical(job)))
                db.commit()
            except Exception:
                db.rollback(); raise
            self._kick()
            return public_job(job)

    def _kick(self):
        if self.launch and (self.worker is None or not self.worker.is_alive()):
            self.worker = Thread(target=self._drain, daemon=True, name='8ball-analysis')
            self.worker.start()

    def cancel(self, case_id, job_id):
        with self.lock, self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            job = self._get(db, job_id, case_id)
            if job['status'] in ACTIVE:
                now = utcnow().isoformat()
                job.update(status='cancelled', stage='cancelled', updated_at=now, finished_at=now,
                           message='Cancelled. Any in-flight provider call may still complete or be billed; its result will not be published.')
                self._save(db, job)
            db.commit()
        return public_job(job)

    def checkpoint(self, job_id, stage, *, starting=False, completed=False):
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            job = self._get(db, job_id)
            if job['status'] not in ACTIVE:
                db.rollback(); raise JobStopped()
            case = self.store._get(db, job['case_id'])
            if case.revision != job['base_revision']:
                job.update(status='superseded', stage='superseded', updated_at=utcnow().isoformat(),
                           finished_at=utcnow().isoformat(), message='Case changed during analysis. Result discarded; review new facts before retrying.')
                self._save(db, job); db.commit(); raise JobStopped()
            job.update(stage=stage, updated_at=utcnow().isoformat())
            job['calls_started'] += int(starting)
            job['calls_completed'] += int(completed)
            self._save(db, job); db.commit()

    def _finish(self, job_id, proposal=None, error=None):
        """Publish proposal and completion atomically, after checking cancel/stale."""
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                job = self._get(db, job_id)
                case = self.store._get(db, job['case_id'])
                if job['status'] in ACTIVE:
                    if case.revision != job['base_revision']:
                        job.update(status='superseded', message='Case changed. No proposal was published.')
                    elif proposal is not None:
                        if proposal.case_id != case.id or proposal.base_revision != case.revision:
                            raise ValueError('Analysis returned a proposal for another case or revision.')
                        if db.execute('SELECT COUNT(*) FROM v2_proposals WHERE case_id=?', (case.id,)).fetchone()[0] >= 200:
                            job.update(status='failed', message='Proposal storage limit reached; nothing was published.')
                        else:
                            db.execute('INSERT INTO v2_proposals VALUES(?,?,?,NULL)',
                                       (case.id, proposal.id, proposal.model_dump_json()))
                            job.update(status='failed' if proposal.status == 'failed' else 'succeeded',
                                       proposal_id=proposal.id,
                                       message='Analysis failed validation. Inspect its diagnostic; no case facts changed.' if proposal.status == 'failed' else 'Proposal ready for human review. No case facts changed.')
                    else:
                        # Never echo provider exception bodies, which can contain secrets.
                        job.update(status='failed', message=error or 'Analysis stopped. No proposal or case changes were published.')
                    job.update(stage=job['status'], finished_at=utcnow().isoformat())
                job.update(worker_active=False, updated_at=utcnow().isoformat())
                self._save(db, job); db.commit()
            except Exception:
                db.rollback(); raise

    def _execute(self, job_id):
        started = perf_counter()
        request = None
        client = None
        try:
            self.checkpoint(job_id, 'preparing_context')
            with self.store.connection() as db:
                job = self._get(db, job_id)
                case = self.store._get(db, job['case_id'])
            request = AnalysisRequest.model_validate(job['request'])
            client = ControlledClient(self, job_id, self.client_factory)
            p = self.runner(case, request.provider, request.purpose, request.source_ids,
                            playbook_id=request.playbook_id, allow_external=request.allow_external, client=client)
            self.checkpoint(job_id, 'validating_proposal')
            self._finish(job_id, Proposal.model_validate(p))
        except JobStopped:
            self._finish(job_id)
        except Exception as exc:
            # Retain bounded structured draft diagnostics, never raw exception text.
            p = None
            if request is not None and isinstance(exc, (DraftFailure, HostedFailure)):
                trace = getattr(exc, 'trace', {'failed': True})
                p = Proposal(case_id=job['case_id'], base_revision=job['base_revision'],
                             provider=request.provider, model=getattr(exc, 'model', 'unavailable'),
                             purpose=request.purpose, source_ids=request.source_ids, status='failed',
                             output_hash=digest(trace), raw_output=trace,
                             latency_ms=round((perf_counter()-started)*1000, 2),
                             note='Validation failed. No case state changed. Review the structured diagnostic.')
            try: self._finish(job_id, p)
            except Exception:
                # Last-resort safe terminal record; no model trace or source is logged.
                self._finish(job_id, error='Analysis could not publish a valid result.')
        finally:
            if client is not None: client.close()

    def run_next(self):
        """Synchronous pump also used by deterministic queue tests."""
        with self.slot:
            with self.lock, self.store.connection() as db:
                db.execute('BEGIN IMMEDIATE')
                jobs = [json.loads(r['body']) for r in db.execute('SELECT body FROM v2_analysis_jobs ORDER BY rowid')]
                job = next((j for j in jobs if j['status'] == 'queued'), None)
                if job is None: db.rollback(); return False
                job.update(status='running', worker_active=True, stage='preparing_context', started_at=utcnow().isoformat(), updated_at=utcnow().isoformat())
                self._save(db, job); db.commit()
            self._execute(job['id'])
            return True

    def _drain(self):
        while True:
            if self.run_next(): continue
            # Close the admission/worker-exit race under the same lock as submit.
            with self.lock, self.store.connection() as db:
                pending = any(json.loads(r['body'])['status'] == 'queued'
                              for r in db.execute('SELECT body FROM v2_analysis_jobs'))
                if pending: continue
                self.worker = None
                return
