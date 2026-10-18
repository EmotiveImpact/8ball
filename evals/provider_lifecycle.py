"""Opt-in real-provider job lifecycle observations in a disposable application.

Run the unchanged frozen generation gate first and supply its matching report.
Each trial makes one explicit graph request. Interventions follow APPLICATION
CALL ADMISSION, not confirmed remote receipt. A fast result is inconclusive and
is never retried. This does not exercise remote cancellation or human acceptance.
No model downloads, substitute outputs, provider hooks or automatic retries exist.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import timedelta
from hashlib import sha256
import json
import os
from pathlib import Path
import secrets
import signal
import subprocess
import sys
import tempfile
import time
import uuid

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from eightball.models import utcnow
from eightball.v2.compatible import settings as compatible_settings
from eightball.v2.hosted import settings as hosted_settings
from evals.full_journey import API, SetupBlocked, preflight
from evals.live_huggingface import FIXTURES_SHA256
from scripts.acceptance import ensure_port_available, output_directory, source_manifest

SCENARIOS = ('cancel', 'stale', 'restart')
ACTIVE = {'queued', 'running'}
EXPECTED = {'cancel': 'cancelled', 'stale': 'superseded', 'restart': 'interrupted'}
REPORT_NAME = 'lifecycle-report.json'
VERSION = 'provider-lifecycle.v1'


class LifecycleFailure(ValueError):
    """Fixed safe diagnostic; never include arbitrary HTTP/provider text."""


class EvaluationInterrupted(BaseException):
    pass


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def checkpoint(report, directory):
    """Immutable numbered receipts plus atomic current report; no credentials."""
    report['checkpoint_number'] = report.get('checkpoint_number', 0) + 1
    report['checkpoint_at'] = utcnow().isoformat()
    raw = (json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    snapshots = directory / 'checkpoints'
    snapshots.mkdir(exist_ok=True)
    with (snapshots / f"{report['checkpoint_number']:06d}.json").open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    temporary = directory / ('.' + REPORT_NAME + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with temporary.open('xb') as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, directory / REPORT_NAME)
    finally:
        temporary.unlink(missing_ok=True)


def matching_returned_calls(row, provider, configured):
    """Check captured engineering receipts, never authenticate a remote event.

    The report is unsigned. Its summary flag alone cannot stand in for the
    returned calls and model/configuration identity of each frozen fixture.
    """
    proposal = row['proposal']
    transport = proposal['raw_output']['transport']
    calls = transport['calls']
    served_model = proposal['model']
    routing = getattr(configured, 'routing_provider', None) or configured.provider
    expected_transport = ('openai_compatible' if provider == 'openai_compatible'
                          else 'huggingface_inference_providers')
    matches = (
        proposal['provider'] == provider and proposal['purpose'] == row['purpose']
        and isinstance(served_model, str) and 1 <= len(served_model) <= 180
        and transport['transport'] == expected_transport
        and transport['requested_model'] == configured.model
        and transport['routing_provider'] == routing
        and transport['automatic_routing'] is False
        and transport['explicit_operator_permission'] is True
        and isinstance(calls, list) and len(calls) == (2 if row['purpose'] == 'graph' else 1)
        and all(call['status'] == 'response_received' and call['http_status'] == 200
                and call['finish_reason'] == 'stop' and call['served_model'] == served_model
                for call in calls)
    )
    if provider == 'openai_compatible':
        matches = (matches and transport['endpoint_host'] == configured.endpoint_host
                   and transport['api_provider'] == configured.provider)
    return matches


def generation_prerequisite(path, provider, configured, source, fixtures):
    """Local matching evidence, not a signature or independent approval."""
    if path is None:
        raise SetupBlocked('Run the unchanged frozen generation gate first and supply --generation-report. No request was started.')
    try:
        selected = Path(path)
        if selected.is_symlink() or not selected.is_file() or selected.stat().st_size > 32 * 1024 * 1024:
            raise ValueError()
        raw = selected.read_bytes()
        def reject_constant(value):
            raise ValueError('Nonfinite receipt data')
        report = json.loads(raw, parse_constant=reject_constant)
        rows = report['results']
        graph = next(row for row in rows if row['purpose'] == 'graph')
        routing = getattr(configured, 'routing_provider', None) or configured.provider
        expected = (
            report['schema_version'] == 2 and report['status'] == 'passed'
            and report['complete'] is True and report['structural_gate_passed'] is True
            and report['actual_hosted_requests'] is True
            and report['provider'] == provider and report['requested_model'] == configured.model
            and report['routing_provider'] == routing and report['source'] == source
            and report['source_unchanged_during_run'] is True and report['source_at_finish'] == source
            and report['fixture_sha256'] == FIXTURES_SHA256
            and report['planned_fixtures'] == report['completed_fixtures'] == len(rows) == len(fixtures)
            and all(row['status'] == 'valid_proposal' and row['live_state_unchanged'] is True
                    and [row['title'], row['source'], row['purpose'], row['desired_outcome']] == fixtures[index]
                    and matching_returned_calls(row, provider, configured)
                    for index, row in enumerate(rows))
            and type(graph['candidate_routes']) is int and graph['candidate_routes'] >= 2
            and graph['outcome_evidenced'] is False
            and graph['all_actions_need_approval'] is True and graph['exact_human_outcome_preserved'] is True
        )
        if provider == 'openai_compatible':
            expected = expected and report['endpoint_host'] == configured.endpoint_host
        if not expected:
            raise ValueError()
    except (OSError, ValueError, TypeError, KeyError, StopIteration, RecursionError):
        raise SetupBlocked('Generation prerequisite is absent, malformed, incomplete, failed or does not match this source, fixture and provider configuration. No request was started.') from None
    return {'report_sha256': sha256(raw).hexdigest(), 'status': 'matching_local_report',
            'independent_approval': False, 'cryptographically_signed': False}


class OwnedServer:
    """Own only our process/database. Never inspect, reuse or kill another server."""
    def __init__(self, database):
        token = secrets.token_urlsafe(32)
        self.env = {**os.environ, 'EIGHTBALL_DB': str(database), 'EIGHTBALL_TOKEN': token}
        self.token = token
        self.process = None
        self.api = None

    def start(self):
        ensure_port_available()
        self.process = subprocess.Popen([sys.executable, '-m', 'eightball'], cwd=ROOT,
                                        env=self.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.api = API(self.token)
        self.api.client.timeout = httpx.Timeout(3)
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise LifecycleFailure('Owned application stopped before readiness.')
            try:
                self.api.read('/status')
                return self.api
            except httpx.HTTPError:
                time.sleep(.1)
        raise LifecycleFailure('Owned application did not become ready within 15 seconds.')

    def stop(self):
        api, process = self.api, self.process
        self.api = self.process = None
        try:
            if api is not None:
                api.close()
        finally:
            # Client cleanup must not leave an owned server alive against a
            # temporary database that is about to be removed.
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
        return process.returncode if process is not None else None

    def restart(self):
        code = self.stop()
        self.start()
        return code


def _record_job(trial, job, save):
    if not trial['job_snapshots'] or trial['job_snapshots'][-1]['job'] != job:
        trial['job_snapshots'].append({'at': utcnow().isoformat(), 'job': deepcopy(job)})
        trial['max_application_calls_admitted'] = max(trial['max_application_calls_admitted'], job['calls_started'])
        save()


def exercise(server, scenario, provider, allow_external, fixture, trial, save, timeout):
    """One request per scenario; no retry even when the intervention loses a race."""
    api = server.api
    expected_status_seen = False
    _, text, _, outcome = fixture
    case = api.post('/cases', {'title': 'Fictional lifecycle ' + scenario,
        'client': 'Engineering fixture only', 'summary': text, 'desired_outcome': outcome,
        'budget': 10000, 'deadline': (utcnow() + timedelta(days=3)).isoformat()})
    case = api.command(case, 'add_evidence', {'title': 'Unchanged frozen supplier fixture',
        'source': 'Public engineering fixture', 'text': text})['case']
    base = '/cases/' + case['id']
    trial.update(case_id=case['id'], before_case=deepcopy(case), before_case_sha256=digest(case),
                 before_proposals_sha256=digest(api.read(base + '/proposals')))
    expected_case = deepcopy(case)
    job = api.post(base + '/analysis-jobs', {'request_id': uuid.uuid4().hex,
        'expected_revision': case['revision'], 'provider': provider, 'purpose': 'graph',
        'source_ids': [case['evidence'][-1]['id']], 'allow_external': allow_external})
    trial['job_id'] = job['id']
    trial['requests_submitted'] = 1
    _record_job(trial, job, save)
    path = base + '/analysis-jobs/' + job['id']
    deadline = time.monotonic() + timeout
    while job['status'] in ACTIVE and job['calls_started'] == 0:
        if time.monotonic() >= deadline:
            trial.update(status='failed', reason='Application call admission was not observed before the trial timeout.')
            trial['cleanup_cancel'] = api.post(path + '/cancel', {})
            save()
            return False
        time.sleep(.02)
        job = api.read(path)
        _record_job(trial, job, save)
    if job['status'] not in ACTIVE or job['calls_started'] != 1:
        trial.update(status='not_exercised', reason='The job finished or advanced beyond its first admitted call before intervention; no automatic retry.')
        trial['available_proposals'] = api.read(base + '/proposals')
        trial['after_case'] = api.read(base)['case']
        trial['after_case_sha256'] = digest(trial['after_case'])
        trial['response_evidence_status'] = 'Only the available proposals contain returned transport evidence; literal successful HTTP bodies are not archived by this runner.'
        save()
        return not job['worker_active']

    trial['intervention'] = {'at': utcnow().isoformat(), 'kind': scenario,
        'trigger': 'first_application_call_admission_observed',
        'remote_receipt': 'unknown', 'remote_completion': 'unknown', 'remote_billing': 'unknown'}
    save()
    if scenario == 'cancel':
        after = api.post(path + '/cancel', {})
        trial['intervention']['response_status'] = after['status']
        expected_status_seen = after['status'] == EXPECTED[scenario]
        if after['status'] != EXPECTED[scenario]:
            trial.update(status='not_exercised', reason='Publication completed before cancel was applied; no automatic retry.')
            _record_job(trial, after, save)
    elif scenario == 'stale':
        # Snapshot before and after the deliberate metadata command separates
        # expected operator changes from forbidden analysis changes.
        expected_case = api.command(case, 'metadata', {'budget': 9999})['case']
        trial['intervention']['expected_case_sha256'] = digest(expected_case)
    elif scenario == 'restart':
        trial['intervention']['owned_process_exit_code'] = server.restart()
        api = server.api
        trial['intervention']['owned_process_restarted'] = True
        save()
    else:
        raise LifecycleFailure('Unknown lifecycle scenario.')

    # Drain the observed worker. A cancellation response by itself is not proof
    # that a late result cannot publish. Restarted jobs must remain interrupted.
    while True:
        job = api.read(path)
        _record_job(trial, job, save)
        expected_status_seen |= job['status'] == EXPECTED[scenario]
        if job['status'] not in ACTIVE and not job['worker_active']:
            break
        if time.monotonic() >= deadline:
            trial.update(status='failed', reason='Worker did not drain within the trial budget; remote completion remains unknown.')
            api.post(path + '/cancel', {})
            save()
            return False
        time.sleep(.05)

    # Observe a second snapshot without submitting work, especially after a
    # restart. This proves only the stated local observation interval.
    time.sleep(.25)
    later = api.read(path)
    _record_job(trial, later, save)
    proposals = api.read(base + '/proposals')
    after_case = api.read(base)['case']
    trial.update(final_job=deepcopy(later), available_proposals=proposals,
                 after_case=after_case, expected_case=expected_case,
                 after_case_sha256=digest(after_case), expected_case_sha256=digest(expected_case),
                 after_proposals_sha256=digest(proposals), observation_interval_seconds=.25)
    if (trial.get('status') == 'not_exercised'
            or (not expected_status_seen and later['status'] in ('succeeded', 'failed'))):
        trial.update(status='not_exercised', reason='Job finished before the intervention could suppress publication; no automatic retry.')
    else:
        checks = {'expected_terminal_status': later['status'] == EXPECTED[scenario],
            'worker_inactive': later['worker_active'] is False,
            'no_proposal_id': later['proposal_id'] is None, 'no_published_proposal': proposals == [],
            'no_unintended_case_mutation': after_case == expected_case,
            'only_first_call_admitted': later['calls_started'] == trial['max_application_calls_admitted'] == 1,
            'no_later_call_observed': job['calls_started'] == later['calls_started'],
            'status_stable': job['status'] == later['status']}
        trial.update(checks=checks, status='passed' if all(checks.values()) else 'failed')
    trial['discarded_response_evidence'] = {
        'raw_response': 'unavailable_for_discarded_or_interrupted_job',
        'served_model': 'unknown_without_attested_returned_transport_receipt',
        'reason': 'Analysis jobs publish no proposal for cancelled, superseded or interrupted work; application admission does not prove remote receipt.',
        'remote_completion': 'unknown', 'remote_billing': 'unknown'}
    save()
    return True


def run(provider, *, allow_inference=False, allow_external=False,
        generation_report=None, output=None, timeout=180):
    if type(timeout) is not int or not 1 <= timeout <= 600:
        raise ValueError('Trial timeout must be an integer between 1 and 600 seconds.')
    directory = output_directory(output or ROOT / 'artifacts/provider-lifecycle') / uuid.uuid4().hex
    directory.mkdir(parents=True, exist_ok=False)
    report = {'schema_version': 1, 'runner_version': VERSION, 'run_id': directory.name,
        'started_at': utcnow().isoformat(), 'status': 'running', 'complete': False,
        'source': source_manifest(), 'provider': provider, 'scenarios': [],
        'automatic_retry': False, 'substitute_outputs': False, 'actual_remote_receipt_verified': False,
        'remote_completion': 'unknown', 'remote_billing': 'unknown',
        'native_browser_verified': False, 'independent_expert_review': False,
        'full_prd_acceptance': False, 'production_approved': False,
        'limits': ['Interventions follow application call admission; remote receipt is unverified.',
                  'A fast completion is NOT_EXERCISED, never retried automatically.',
                  'Discarded or killed responses may be unavailable; no fabricated trace or served model.',
                  'No provider-side cancellation guarantee or human/model-quality acceptance.',
                  'Lifecycle checks are application-process/HTTP observations, not native UI acceptance.']}
    save = lambda: checkpoint(report, directory)
    save()
    server = None
    previous_signal = None
    signal_installed = False
    try:
        if provider not in ('huggingface', 'openai_compatible'):
            raise SetupBlocked('This lifecycle runner requires an explicitly configured hosted provider.')
        report['preflight'] = preflight(provider, allow_inference, allow_external)
        configured = compatible_settings() if provider == 'openai_compatible' else hosted_settings()
        fixtures = json.loads((ROOT / 'evals/generation-cases.json').read_text())
        if sha256(json.dumps(fixtures).encode()).hexdigest() != FIXTURES_SHA256:
            raise SetupBlocked('Frozen fixture identity changed. No request was started.')
        report['fixture_sha256'] = FIXTURES_SHA256
        report['generation_prerequisite'] = generation_prerequisite(
            generation_report, provider, configured, report['source'], fixtures)
        save()
        try:
            previous_signal = signal.getsignal(signal.SIGTERM)
            def terminate(signum, frame):
                raise EvaluationInterrupted()
            signal.signal(signal.SIGTERM, terminate)
            signal_installed = True
        except ValueError:
            pass
        fixture = next(row for row in fixtures if row[2] == 'graph')
        with tempfile.TemporaryDirectory(prefix='8ball-provider-lifecycle-') as temporary:
            server = OwnedServer(Path(temporary) / 'fictional.sqlite3')
            try:
                server.start()
                if server.api.read('/cases') != []:
                    raise LifecycleFailure('Disposable application unexpectedly contained cases.')
                for scenario in SCENARIOS:
                    trial = {'scenario': scenario, 'status': 'running', 'started_at': utcnow().isoformat(),
                        'requests_submitted': 0, 'job_snapshots': [], 'max_application_calls_admitted': 0,
                        'response_evidence_status': 'No returned model receipt has been captured; application snapshots do not establish remote receipt.'}
                    report['scenarios'].append(trial)
                    save()
                    can_continue = exercise(server, scenario, provider, allow_external, fixture, trial, save, timeout)
                    trial['finished_at'] = utcnow().isoformat()
                    save()
                    if not can_continue:
                        report['status'] = 'failed'
                        break
                else:
                    statuses = [trial['status'] for trial in report['scenarios']]
                    report['status'] = ('failed' if 'failed' in statuses else
                                        'inconclusive' if 'not_exercised' in statuses else 'passed')
                report['complete'] = len(report['scenarios']) == len(SCENARIOS)
            finally:
                server.stop()
    except SetupBlocked as exc:
        report.update(status='blocked', reason=str(exc))
    except BaseException as exc:
        # Do not echo configuration, sources, provider exceptions or local tokens.
        interrupted = isinstance(exc, (KeyboardInterrupt, EvaluationInterrupted, SystemExit))
        report.update(status='interrupted' if interrupted else 'failed',
                      reason='Lifecycle run interrupted; no request will be retried.' if interrupted else
                             'Lifecycle observation failed: ' + type(exc).__name__)
        if report['scenarios'] and report['scenarios'][-1]['status'] == 'running':
            report['scenarios'][-1].update(status=report['status'], evidence_loss='Last job snapshot is the available evidence; remote response may be unavailable.')
    finally:
        if signal_installed:
            signal.signal(signal.SIGTERM, previous_signal)
        report['source_unchanged_during_run'] = report['source'] == source_manifest()
        if not report['source_unchanged_during_run']:
            report.update(status='failed', reason='Source changed during the lifecycle run.')
        report['finished_at'] = utcnow().isoformat()
        report['application_calls_admitted_observed'] = sum(t['max_application_calls_admitted'] for t in report['scenarios'])
        save()
    return report, directory / REPORT_NAME


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider', required=True, choices=['huggingface', 'openai_compatible'])
    parser.add_argument('--allow-inference', action='store_true')
    parser.add_argument('--allow-external', action='store_true')
    parser.add_argument('--generation-report', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--timeout', type=int, default=180, help='Per-trial observation budget, 1–600 seconds.')
    args = parser.parse_args(argv)
    report, path = run(args.provider, allow_inference=args.allow_inference,
        allow_external=args.allow_external, generation_report=args.generation_report,
        output=args.output, timeout=args.timeout)
    print(json.dumps({'status': report['status'],
                      'application_calls_admitted_observed': report['application_calls_admitted_observed'],
                      'actual_remote_receipt_verified': False}))
    print('Report: ' + str(path))
    return 0 if report['status'] == 'passed' else 2 if report['status'] in ('blocked', 'inconclusive') else 1


if __name__ == '__main__':
    raise SystemExit(main())
