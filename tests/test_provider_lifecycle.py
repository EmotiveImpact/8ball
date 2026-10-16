"""Lifecycle experiment contracts with controlled HTTP, never actual inference.

The adapter below drives real SQLite cases, real AnalysisJobs and the compatible
transport. Only the remote HTTP response and owned-server process are controlled.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from threading import Event, Thread

import httpx
import pytest

from evals import provider_lifecycle as lifecycle
from eightball.models import uid
from eightball.v2.analysis_jobs import AnalysisJobs, AnalysisRequest
from eightball.v2.commands import Command
from eightball.v2.contracts import Case
from eightball.v2.store import Store

ROOT = Path(__file__).resolve().parents[1]
KEY = 'fictional_lifecycle_key_never_a_real_secret'
FIXTURES = json.loads((ROOT / 'evals/generation-cases.json').read_text())
STAGED = json.loads((ROOT / 'tests/fixtures/drafting/staged.json').read_text())
SOURCE = {'sha256': 'controlled-test-source', 'files': {}}


@pytest.fixture(autouse=True)
def configure(monkeypatch):
    for name in ('EIGHTBALL_API_BASE_URL', 'EIGHTBALL_API_MODEL', 'EIGHTBALL_API_PROVIDER',
                 'EIGHTBALL_API_KEY', 'EIGHTBALL_API_ROUTING_PROVIDER'):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL', 'https://fixture.invalid/v1')
    monkeypatch.setenv('EIGHTBALL_API_MODEL', 'qwen/controlled-model')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER', 'controlled-provider')
    monkeypatch.setenv('EIGHTBALL_API_KEY', KEY)
    monkeypatch.setattr(lifecycle, 'source_manifest', lambda: deepcopy(SOURCE))


def generation_report(tmp_path, **changes):
    rows = []
    for title, text, purpose, outcome in FIXTURES:
        row = {'title': title, 'source': text, 'purpose': purpose, 'desired_outcome': outcome,
               'status': 'valid_proposal', 'live_state_unchanged': True}
        if purpose == 'graph':
            row.update(candidate_routes=2, outcome_evidenced=False,
                       all_actions_need_approval=True, exact_human_outcome_preserved=True)
        rows.append(row)
    report = {'schema_version': 2, 'status': 'passed', 'complete': True,
        'source': deepcopy(SOURCE), 'provider': 'openai_compatible',
        'requested_model': 'qwen/controlled-model', 'routing_provider': 'controlled-provider',
        'endpoint_host': 'fixture.invalid', 'fixture_sha256': lifecycle.FIXTURES_SHA256,
        'planned_fixtures': len(rows), 'completed_fixtures': len(rows), 'results': rows,
        'structural_gate_passed': True, 'actual_hosted_requests': True}
    report.update(changes)
    path = tmp_path / 'generation.json'
    path.write_text(json.dumps(report))
    return path


class ControlledAPI:
    def __init__(self, server):
        self.server = server

    def read(self, path):
        server = self.server
        if path == '/cases':
            return [case.model_dump(mode='json') for case in server.store.list()]
        parts = path.strip('/').split('/')
        case_id = parts[1]
        if len(parts) == 2:
            return {'case': server.store.get(case_id).model_dump(mode='json')}
        if parts[2] == 'proposals':
            return server.store.proposals(case_id)
        assert parts[2] == 'analysis-jobs'
        return server.manager.get(case_id, parts[3])

    def post(self, path, body):
        server = self.server
        if path == '/cases':
            case = server.store.create(Case(**body), fixture=True)
            return case.model_dump(mode='json')
        parts = path.strip('/').split('/')
        case_id = parts[1]
        if len(parts) == 3:
            assert parts[2] == 'analysis-jobs'
            server.submissions += 1
            server.release.clear()
            server.current_case = server.store.get(case_id)
            job = server.manager.submit(case_id, AnalysisRequest(**body))
            worker = Thread(target=server.manager.run_next)
            server.workers.append(worker)
            worker.start()
            assert server.entered.wait(5)
            if server.fast:
                server.release.set()
                worker.join(5)
                assert not worker.is_alive()
            return server.manager.get(case_id, job['id'])
        assert parts[-1] == 'cancel'
        result = server.manager.cancel(case_id, parts[3])
        if not server.stuck:
            server.release.set()
        return result

    def command(self, case, kind, payload):
        updated, changes = self.server.store.change(case['id'], Command(event_id=uid(),
            expected_revision=case['revision'], kind=kind, payload=payload))
        if kind == 'metadata':
            self.server.release.set()
        return {'case': updated.model_dump(mode='json'), 'changes': changes}


class ControlledServer:
    instances = []
    fast = False
    stuck = False

    def __init__(self, database):
        self.store = Store(str(database))
        self.entered, self.release = Event(), Event()
        self.workers = []
        self.calls = []
        self.submissions = 0
        self.restarts = 0
        self.api = ControlledAPI(self)
        self.manager = AnalysisJobs(self.store, launch=False, client_factory=self.factory)
        type(self).instances.append(self)

    def factory(self, **kwargs):
        def respond(request):
            self.calls.append(request)
            self.entered.set()
            assert self.release.wait(5)
            # A fast trial is deliberately a one-call validation failure. It
            # demonstrates that failure is not retried or relabelled lifecycle
            # success. Normal trials stop before parsing this actual envelope.
            frame = deepcopy(STAGED['frame'])
            frame['target_bindings'] = [{'criterion_index': 0, 'target_quote': self.current_case.desired_outcome}]
            if self.fast:
                frame['verification']['requires_existing'] = ['not-an-existing-condition']
            return httpx.Response(200, json={'model': 'controlled-served-model',
                'choices': [{'finish_reason': 'stop', 'message': {'role': 'assistant',
                    'content': json.dumps(frame)}}], 'usage': {'total_tokens': len(self.calls)}})
        return httpx.Client(transport=httpx.MockTransport(respond), **kwargs)

    def start(self):
        return self.api

    def stop(self):
        self.release.set()
        for worker in self.workers:
            worker.join(5)
            assert not worker.is_alive()
        return 0

    def restart(self):
        self.restarts += 1
        # Controlled process boundary: a new manager recovers the same actual
        # SQLite database. The owned Popen lifecycle is tested independently.
        self.manager = AnalysisJobs(self.store, launch=False, client_factory=self.factory)
        self.release.set()
        return 0


def controlled_server(monkeypatch, **changes):
    subclass = type('TestServer', (ControlledServer,), {'instances': [], **changes})
    monkeypatch.setattr(lifecycle, 'OwnedServer', subclass)
    return subclass


@pytest.mark.parametrize('inference,external', [(False, False), (True, False)])
def test_preflight_requires_both_permissions_before_owned_server(tmp_path, monkeypatch, inference, external):
    def forbidden(*args):
        pytest.fail('Blocked preflight must not start a server or model request')
    monkeypatch.setattr(lifecycle, 'OwnedServer', forbidden)
    report, path = lifecycle.run('openai_compatible', allow_inference=inference,
        allow_external=external, output=tmp_path / 'runs')
    assert report['status'] == 'blocked' and report['application_calls_admitted_observed'] == 0
    assert report['scenarios'] == [] and path.exists()
    assert not report['actual_remote_receipt_verified']
    assert KEY not in path.read_text()


@pytest.mark.parametrize('changes', [
    {'status': 'failed'}, {'complete': False}, {'completed_fixtures': 3},
    {'actual_hosted_requests': False}, {'fixture_sha256': 'changed'},
    {'requested_model': 'different'}, {'routing_provider': 'different'},
    {'endpoint_host': 'different.example'}, {'source': {'sha256': 'old', 'files': {}}},
    {'structural_gate_passed': False}, {'results': []}, {'schema_version': 1},
])
def test_generation_prerequisite_rejects_mismatched_receipt_without_server(tmp_path, monkeypatch, changes):
    server = controlled_server(monkeypatch)
    path = generation_report(tmp_path, **changes)
    report, _ = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=path, output=tmp_path / 'runs')
    assert report['status'] == 'blocked' and report['scenarios'] == []
    assert not server.instances


def test_missing_and_malformed_generation_reports_are_blocked(tmp_path):
    for name, contents in [('malformed.json', '{'), ('not-object.json', '[]')]:
        path = tmp_path / name
        path.write_text(contents)
        with pytest.raises(lifecycle.SetupBlocked, match='prerequisite'):
            lifecycle.generation_prerequisite(path, 'openai_compatible',
                lifecycle.compatible_settings(), SOURCE, FIXTURES)
    with pytest.raises(lifecycle.SetupBlocked, match='generation gate'):
        lifecycle.generation_prerequisite(None, 'openai_compatible',
            lifecycle.compatible_settings(), SOURCE, FIXTURES)


def test_openrouter_receipt_matches_pinned_routing_provider(tmp_path, monkeypatch):
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL', 'https://openrouter.ai/api/v1')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER', 'openrouter')
    monkeypatch.setenv('EIGHTBALL_API_ROUTING_PROVIDER', 'Provider Name')
    path = generation_report(tmp_path, endpoint_host='openrouter.ai', routing_provider='Provider Name')
    result = lifecycle.generation_prerequisite(path, 'openai_compatible',
        lifecycle.compatible_settings(), SOURCE, FIXTURES)
    assert result['status'] == 'matching_local_report' and not result['independent_approval']


def test_all_lifecycle_outcomes_use_real_jobs_without_publication_or_second_call(tmp_path, monkeypatch):
    server_type = controlled_server(monkeypatch)
    path = generation_report(tmp_path)
    report, output = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=path, output=tmp_path / 'runs', timeout=5)
    assert report['status'] == 'passed' and report['complete']
    server = server_type.instances[0]
    assert server.submissions == len(server.calls) == 3 and server.restarts == 1
    assert report['application_calls_admitted_observed'] == 3
    for trial in report['scenarios']:
        assert trial['status'] == 'passed' and all(trial['checks'].values())
        assert trial['final_job']['status'] == lifecycle.EXPECTED[trial['scenario']]
        assert trial['final_job']['proposal_id'] is None and trial['available_proposals'] == []
        assert trial['requests_submitted'] == 1
        assert trial['intervention']['trigger'] == 'first_application_call_admission_observed'
        assert trial['discarded_response_evidence']['served_model'].startswith('unknown')
    assert not report['actual_remote_receipt_verified'] and not report['automatic_retry']
    assert not report['full_prd_acceptance'] and not report['independent_expert_review']
    assert report['source_unchanged_during_run']
    assert KEY not in output.read_text()
    snapshots = sorted((output.parent / 'checkpoints').glob('*.json'))
    assert len(snapshots) > 10 and json.loads(snapshots[0].read_text())['status'] == 'running'
    assert json.loads(snapshots[-1].read_text()) == report


def test_fast_provider_completion_is_inconclusive_and_never_retried(tmp_path, monkeypatch):
    server_type = controlled_server(monkeypatch, fast=True)
    report, _ = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path), output=tmp_path / 'runs')
    assert report['status'] == 'inconclusive' and report['complete']
    assert all(trial['status'] == 'not_exercised' for trial in report['scenarios'])
    assert server_type.instances[0].submissions == len(server_type.instances[0].calls) == 3
    assert server_type.instances[0].restarts == 0
    assert all(trial['available_proposals'][0]['status'] == 'failed' for trial in report['scenarios'])


@pytest.mark.parametrize('corruption', ['extra_call', 'late_success', 'case_mutation'])
def test_exercised_cancellation_regressions_fail_instead_of_becoming_timing_races(tmp_path, monkeypatch, corruption):
    controlled_server(monkeypatch)
    original = ControlledAPI.read
    def corrupted(self, path):
        result = original(self, path)
        if path.endswith('/proposals') or path == '/cases':
            return result
        if '/analysis-jobs/' in path and result['status'] == 'cancelled':
            if corruption == 'extra_call':
                result['calls_started'] = 2
            elif corruption == 'late_success':
                result['status'] = 'succeeded'
        elif corruption == 'case_mutation' and path.count('/') == 2:
            jobs = self.server.manager.list(result['case']['id'])
            if jobs and jobs[0]['status'] == 'cancelled':
                result['case']['summary'] = 'An unintended analysis mutation'
        return result
    monkeypatch.setattr(ControlledAPI, 'read', corrupted)
    report, _ = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path), output=tmp_path / 'runs')
    cancelled = report['scenarios'][0]
    assert report['status'] == cancelled['status'] == 'failed'
    assert cancelled['intervention']['response_status'] == 'cancelled'
    assert not all(cancelled['checks'].values())


def test_nonfinite_generation_receipt_is_not_accepted(tmp_path):
    path = generation_report(tmp_path)
    report = json.loads(path.read_text())
    next(row for row in report['results'] if row['purpose'] == 'graph')['candidate_routes'] = float('inf')
    path.write_text(json.dumps(report))
    with pytest.raises(lifecycle.SetupBlocked, match='prerequisite'):
        lifecycle.generation_prerequisite(path, 'openai_compatible',
            lifecycle.compatible_settings(), SOURCE, FIXTURES)


def test_trial_timeout_cancels_and_stops_remaining_trials_without_retry(tmp_path, monkeypatch):
    server_type = controlled_server(monkeypatch, stuck=True)
    report, _ = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path),
        output=tmp_path / 'runs', timeout=1)
    assert report['status'] == 'failed' and not report['complete']
    assert len(report['scenarios']) == server_type.instances[0].submissions == 1
    assert len(server_type.instances[0].calls) == 1
    assert report['scenarios'][0]['status'] == 'failed'


def test_current_report_and_numbered_snapshots_do_not_overwrite_prior_attempts(tmp_path, monkeypatch):
    server_type = controlled_server(monkeypatch, fast=True)
    path = generation_report(tmp_path)
    _, first = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=path, output=tmp_path / 'runs')
    previous = first.read_bytes()
    _, second = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=path, output=tmp_path / 'runs')
    assert first != second and first.read_bytes() == previous
    assert sum(server.submissions for server in server_type.instances) == 6


def test_arbitrary_failure_message_cannot_reflect_key_into_report(tmp_path, monkeypatch):
    class Broken:
        def __init__(self, database):
            pass
        def start(self):
            raise RuntimeError('Credential reflected: ' + KEY)
        def stop(self):
            pass
    monkeypatch.setattr(lifecycle, 'OwnedServer', Broken)
    report, path = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path), output=tmp_path / 'runs')
    assert report['status'] == 'failed' and report['reason'].endswith('RuntimeError')
    assert KEY not in path.read_text()


def test_interrupt_preserves_active_snapshot_and_does_not_retry(tmp_path, monkeypatch):
    server_type = controlled_server(monkeypatch)
    original = ControlledAPI.post
    def interrupted(self, path, body):
        result = original(self, path, body)
        if path.endswith('/cancel'):
            raise KeyboardInterrupt()
        return result
    monkeypatch.setattr(ControlledAPI, 'post', interrupted)
    report, path = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path), output=tmp_path / 'runs')
    assert report['status'] == 'interrupted' and not report['complete']
    assert server_type.instances[0].submissions == len(server_type.instances[0].calls) == 1
    assert report['scenarios'][0]['status'] == 'interrupted'
    assert report['scenarios'][0]['job_snapshots'][-1]['job']['calls_started'] == 1
    assert report['scenarios'][0]['evidence_loss']
    assert json.loads(path.read_text()) == report


def test_changed_source_invalidates_lifecycle_evidence(tmp_path, monkeypatch):
    server_type = controlled_server(monkeypatch, fast=True)
    original_stop = server_type.stop
    def changed_stop(self):
        result = original_stop(self)
        monkeypatch.setattr(lifecycle, 'source_manifest', lambda: {'sha256': 'changed', 'files': {}})
        return result
    monkeypatch.setattr(server_type, 'stop', changed_stop)
    report, _ = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path), output=tmp_path / 'runs')
    assert report['status'] == 'failed' and not report['source_unchanged_during_run']


def test_owned_server_restarts_only_its_process_and_same_disposable_database(tmp_path, monkeypatch):
    processes = []
    calls = []
    class Process:
        def __init__(self, args, **kwargs):
            calls.append((args, kwargs))
            self.returncode = None
            processes.append(self)
        def poll(self):
            return self.returncode
        def terminate(self):
            self.returncode = -15
        def wait(self, timeout):
            return self.returncode
    class Client:
        def __init__(self, token):
            self.token = token
            self.client = type('HTTP', (), {})()
        def read(self, path):
            assert path == '/status'
            return {}
        def close(self):
            pass
    ports = []
    monkeypatch.setattr(lifecycle, 'ensure_port_available', lambda: ports.append(8048))
    monkeypatch.setattr(lifecycle.subprocess, 'Popen', Process)
    monkeypatch.setattr(lifecycle, 'API', Client)
    database = tmp_path / 'fictional.sqlite3'
    server = lifecycle.OwnedServer(database)
    server.start()
    assert server.restart() == -15
    server.stop()
    assert len(processes) == len(ports) == 2
    assert all(process.returncode == -15 for process in processes)
    assert all(arguments == [sys.executable, '-m', 'eightball'] for arguments, _ in calls)
    assert all(kwargs['env']['EIGHTBALL_DB'] == str(database) for _, kwargs in calls)
    assert calls[0][1]['env']['EIGHTBALL_TOKEN'] == calls[1][1]['env']['EIGHTBALL_TOKEN']
    assert all(kwargs['stdout'] == kwargs['stderr'] == subprocess.DEVNULL for _, kwargs in calls)


def test_owned_process_still_terminates_when_api_cleanup_raises(tmp_path):
    class Process:
        returncode = None
        terminated = False
        waited = False
        def poll(self):
            return self.returncode
        def terminate(self):
            self.terminated = True
            self.returncode = -15
        def wait(self, timeout):
            self.waited = True
            return self.returncode
    class Client:
        def close(self):
            raise RuntimeError('Controlled client cleanup failure')
    server = lifecycle.OwnedServer(tmp_path / 'disposable.db')
    process = server.process = Process()
    server.api = Client()
    with pytest.raises(RuntimeError, match='cleanup'):
        server.stop()
    assert process.terminated and process.waited
    assert server.process is None and server.api is None


def test_cli_without_opt_in_does_not_start_model_and_records_blocked(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / 'evals/provider_lifecycle.py'),
        '--provider', 'openai_compatible', '--output', str(tmp_path)],
        capture_output=True, text=True, timeout=15)
    assert result.returncode == 2 and 'blocked' in result.stdout
    files = list(tmp_path.glob('*/lifecycle-report.json'))
    assert len(files) == 1
    report = json.loads(files[0].read_text())
    assert report['application_calls_admitted_observed'] == 0 and report['scenarios'] == []
    assert KEY not in files[0].read_text()
