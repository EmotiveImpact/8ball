"""Lifecycle experiment contracts with controlled HTTP, never actual inference.

The adapter below drives real SQLite cases, real AnalysisJobs and the compatible
transport. Only the remote HTTP response and owned-server process are controlled.
"""
from copy import deepcopy
from datetime import timedelta
import json
from pathlib import Path
import subprocess
import sys
from threading import Event, Thread

import httpx
import pytest

from evals import provider_lifecycle as lifecycle
from eightball.models import uid, utcnow
from eightball.v2.analysis_jobs import AnalysisJobs, AnalysisRequest
from eightball.v2.commands import Command, merge_object
from eightball.v2.contracts import Case, Evidence
from eightball.v2.intelligence import propose
from eightball.v2.planner import plan
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


def generation_report(tmp_path, *, provider='openai_compatible', **changes):
    """Representative receipts from real proposal code, controlled HTTP only."""
    rows = []
    configured = lifecycle.compatible_settings() if provider == 'openai_compatible' else lifecycle.hosted_settings()
    for index, (title, text, purpose, outcome) in enumerate(FIXTURES):
        case = Case(title=title, client='Controlled test only', summary=text, desired_outcome=outcome,
            deadline=utcnow() + timedelta(days=3), budget=10000,
            evidence=[Evidence(id='source', title='Frozen fixture', source='Controlled test', text=text)])
        if purpose == 'extract':
            responses = [{'items': [{'kind': 'claim', 'text': 'Controlled fictional claim',
                'source': {'evidence_id': 'source', 'quote': text}}]}]
        else:
            frame = deepcopy(STAGED['frame'])
            frame['target_bindings'] = [{'criterion_index': i, 'target_quote': outcome}
                                       for i in range(len(frame['success_criteria']))]
            responses = [frame, deepcopy(STAGED['routes'])]
        def respond(request):
            if getattr(configured, 'api_protocol', None) == 'anthropic_messages':
                return httpx.Response(200, json={'type':'message','role':'assistant','model':'controlled-served-model',
                    'content':[{'type':'text','text':json.dumps(responses.pop(0))}],
                    'stop_reason':'end_turn','usage':{'input_tokens':20,'output_tokens':10}})
            return httpx.Response(200, json={'model': 'controlled-served-model',
                'choices': [{'index': 0, 'finish_reason': 'stop', 'message': {'role': 'assistant',
                    'content': json.dumps(responses.pop(0))}}]})
        before = case.model_dump(mode='json')
        with httpx.Client(transport=httpx.MockTransport(respond)) as client:
            proposal = propose(case, provider, purpose, ['source'], allow_external=True, client=client)
        row = {'fixture_index': index, 'title': title, 'source': text, 'purpose': purpose,
            'desired_outcome': outcome, 'status': 'valid_proposal',
            'live_state_unchanged': case.model_dump(mode='json') == before,
            'proposal': proposal.model_dump(mode='json'), 'proposal_count': len(proposal.items)}
        if purpose == 'graph':
            data = case.model_dump(mode='json')
            for item in proposal.items: merge_object(data, item.kind, item.object)
            projected = Case.model_validate(data)
            routes = plan(projected)
            row.update(candidate_routes=len(routes['routes']), outcome_evidenced=routes['outcome_evidenced'],
                all_actions_need_approval=all(action.approval_required for action in projected.graph.actions),
                exact_human_outcome_preserved=all(objective.title == outcome for objective in projected.graph.objectives))
        rows.append(row)
    report = {'schema_version': 2, 'status': 'passed', 'complete': True,
        'source': deepcopy(SOURCE), 'source_at_finish': deepcopy(SOURCE),
        'source_unchanged_during_run': True, 'provider': provider,
        'requested_model': configured.model,
        'routing_provider': getattr(configured, 'routing_provider', None) or configured.provider,
        'fixture_sha256': lifecycle.FIXTURES_SHA256,
        'planned_fixtures': len(rows), 'completed_fixtures': len(rows), 'results': rows,
        'structural_gate_passed': True, 'actual_hosted_requests': True}
    if provider == 'openai_compatible':
        report['endpoint_host'] = configured.endpoint_host
        report['api_protocol'] = configured.api_protocol
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
    fast_success = False
    http_failure = None
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
            if self.http_failure is not None:
                return httpx.Response(self.http_failure, text='Unread controlled provider error')
            # A fast trial is deliberately a one-call validation failure. It
            # demonstrates that failure is not retried or relabelled lifecycle
            # success. Normal trials stop before parsing this actual envelope.
            frame = deepcopy(STAGED['frame'])
            frame['target_bindings'] = [{'criterion_index': i, 'target_quote': self.current_case.desired_outcome}
                                       for i in range(len(frame['success_criteria']))]
            if self.fast and not self.fast_success:
                frame['verification']['requires_existing'] = ['not-an-existing-condition']
            output = STAGED['routes'] if self.fast_success and len(self.calls) % 2 == 0 else frame
            return httpx.Response(200, json={'model': 'controlled-served-model',
                'choices': [{'finish_reason': 'stop', 'message': {'role': 'assistant',
                    'content': json.dumps(output)}}], 'usage': {'total_tokens': len(self.calls)}})
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
    {'source_unchanged_during_run': False}, {'source_unchanged_during_run': None},
    {'source_unchanged_during_run': 'true'}, {'source_at_finish': None},
    {'source_at_finish': {'sha256': 'changed', 'files': {}}},
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


@pytest.mark.parametrize('field', ['source_unchanged_during_run', 'source_at_finish'])
def test_older_receipt_without_source_stability_evidence_is_blocked(tmp_path, field):
    path = generation_report(tmp_path)
    report = json.loads(path.read_text())
    del report[field]
    path.write_text(json.dumps(report))
    with pytest.raises(lifecycle.SetupBlocked, match='prerequisite'):
        lifecycle.generation_prerequisite(path, 'openai_compatible',
            lifecycle.compatible_settings(), SOURCE, FIXTURES)


@pytest.mark.parametrize('fixture_index, path_parts, replacement', [
    (0, ('proposal',), None),
    (0, ('proposal', 'provider'), 'huggingface'),
    (0, ('proposal', 'purpose'), 'graph'),
    (0, ('proposal', 'model'), ''),
    (0, ('proposal', 'raw_output', 'transport', 'calls'), []),
    (3, ('proposal', 'raw_output', 'transport', 'calls'), []),
    (0, ('proposal', 'raw_output', 'transport', 'requested_model'), 'another-model'),
    (0, ('proposal', 'raw_output', 'transport', 'routing_provider'), 'another-provider'),
    (0, ('proposal', 'raw_output', 'transport', 'api_provider'), 'another-service'),
    (0, ('proposal', 'raw_output', 'transport', 'endpoint_host'), 'another.invalid'),
    (0, ('proposal', 'raw_output', 'transport', 'automatic_routing'), True),
    (0, ('proposal', 'raw_output', 'transport', 'explicit_operator_permission'), False),
    (0, ('proposal', 'raw_output', 'transport', 'calls', 0, 'status'), 'failed'),
    (0, ('proposal', 'raw_output', 'transport', 'calls', 0, 'http_status'), 429),
    (0, ('proposal', 'raw_output', 'transport', 'calls', 0, 'finish_reason'), 'length'),
    (0, ('proposal', 'raw_output', 'transport', 'calls', 0, 'served_model'), 'another-served-model'),
])
def test_generation_summary_does_not_replace_captured_matching_calls(tmp_path, monkeypatch, fixture_index, path_parts, replacement):
    server = controlled_server(monkeypatch)
    path = generation_report(tmp_path)
    report = json.loads(path.read_text())
    target = report['results'][fixture_index]
    for part in path_parts[:-1]: target = target[part]
    target[path_parts[-1]] = replacement
    assert report['actual_hosted_requests'] is True
    path.write_text(json.dumps(report))
    result, _ = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=path, output=tmp_path / 'runs')
    assert result['status'] == 'blocked' and result['scenarios'] == []
    assert not server.instances


def test_graph_prerequisite_requires_both_returned_stages(tmp_path):
    path = generation_report(tmp_path)
    report = json.loads(path.read_text())
    graph = next(row for row in report['results'] if row['purpose'] == 'graph')
    graph['proposal']['raw_output']['transport']['calls'].pop()
    path.write_text(json.dumps(report))
    with pytest.raises(lifecycle.SetupBlocked, match='prerequisite'):
        lifecycle.generation_prerequisite(path, 'openai_compatible',
            lifecycle.compatible_settings(), SOURCE, FIXTURES)


def test_huggingface_captured_receipts_remain_valid_without_compatible_fields(tmp_path, monkeypatch):
    monkeypatch.setenv('HF_TOKEN', KEY)
    monkeypatch.setenv('EIGHTBALL_HF_MODEL', 'Qwen/controlled-hf-model')
    monkeypatch.setenv('EIGHTBALL_HF_PROVIDER', 'fixture-provider')
    path = generation_report(tmp_path, provider='huggingface')
    report = json.loads(path.read_text())
    transport = report['results'][0]['proposal']['raw_output']['transport']
    assert 'endpoint_host' not in transport and 'api_provider' not in transport
    assert transport['calls'][0]['served_model'] == 'controlled-served-model'
    result = lifecycle.generation_prerequisite(path, 'huggingface',
        lifecycle.hosted_settings(), SOURCE, FIXTURES)
    assert result['status'] == 'matching_local_report'
    assert not result['independent_approval'] and not result['cryptographically_signed']


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


def test_fast_provider_failure_is_failed_and_never_retried(tmp_path, monkeypatch):
    server_type = controlled_server(monkeypatch, fast=True)
    report, _ = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path), output=tmp_path / 'runs')
    assert report['status'] == 'failed' and not report['complete']
    assert report['scenarios'][0]['status'] == 'failed'
    assert server_type.instances[0].submissions == len(server_type.instances[0].calls) == 1
    assert server_type.instances[0].restarts == 0
    assert all(trial['available_proposals'][0]['status'] == 'failed' for trial in report['scenarios'])


def test_fast_provider_success_remains_inconclusive_without_automatic_retry(tmp_path, monkeypatch):
    server_type = controlled_server(monkeypatch, fast=True, fast_success=True)
    report, _ = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path), output=tmp_path / 'runs')
    assert report['status'] == 'inconclusive' and report['complete']
    assert all(t['status'] == 'not_exercised' and 'intervention' not in t for t in report['scenarios'])
    assert server_type.instances[0].submissions == 3 and len(server_type.instances[0].calls) == 6
    assert all(t['final_job']['status'] == 'succeeded' for t in report['scenarios'])


@pytest.mark.parametrize('status',[401,402,429])
def test_fast_provider_http_failure_stops_lifecycle_as_failed(tmp_path,monkeypatch,status):
    server_type=controlled_server(monkeypatch,fast=True,http_failure=status)
    report,_=lifecycle.run('openai_compatible',allow_inference=True,allow_external=True,
        generation_report=generation_report(tmp_path),output=tmp_path/'runs')
    assert report['status']=='failed' and not report['complete']
    assert len(report['scenarios'])==server_type.instances[0].submissions==len(server_type.instances[0].calls)==1
    assert report['scenarios'][0]['available_proposals'][0]['status']=='failed'


@pytest.mark.parametrize('interrupted',[False,True])
def test_cleanup_failure_does_not_hide_an_interruption_and_still_saves(tmp_path,monkeypatch,interrupted):
    server_type=controlled_server(monkeypatch)
    original=server_type.stop
    def stop(self):
        original(self)
        raise OSError('Private cleanup detail '+KEY)
    monkeypatch.setattr(server_type,'stop',stop)
    if interrupted:
        def interrupt(*args,**kwargs):raise KeyboardInterrupt()
        monkeypatch.setattr(lifecycle,'exercise',interrupt)
    report,path=lifecycle.run('openai_compatible',allow_inference=True,allow_external=True,
        generation_report=generation_report(tmp_path),output=tmp_path/'runs')
    assert report['status']==('interrupted' if interrupted else 'failed')
    assert report['cleanup_error']=={'error_type':'OSError'}
    assert report['finished_at'] and json.loads(path.read_text())==report
    assert KEY not in path.read_text() and 'Private cleanup detail' not in path.read_text()


@pytest.mark.parametrize('interrupted', [False, True])
def test_final_inspection_error_saves_receipt_without_erasing_outcome(tmp_path, monkeypatch, interrupted):
    server_type = controlled_server(monkeypatch)
    original_stop = server_type.stop
    def stop(self):
        original_stop(self)
        def broken():
            raise OSError('private path and ' + KEY)
        monkeypatch.setattr(lifecycle, 'source_manifest', broken)
    monkeypatch.setattr(server_type, 'stop', stop)
    if interrupted:
        def interrupt(*args, **kwargs):
            raise KeyboardInterrupt()
        monkeypatch.setattr(lifecycle, 'exercise', interrupt)
    report, path = lifecycle.run('openai_compatible', allow_inference=True,
        allow_external=True, generation_report=generation_report(tmp_path), output=tmp_path / 'runs')
    assert report['status'] == ('interrupted' if interrupted else 'failed')
    assert report['source_unchanged_during_run'] is False
    assert report['source_at_finish'] is None
    assert report['source_checks'][-1]['status'] == 'inspection_failed'
    assert report['finished_at'] and json.loads(path.read_text()) == report
    assert 'private path' not in path.read_text() and KEY not in path.read_text()


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
    assert sum(server.submissions for server in server_type.instances) == 2


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



def test_real_owned_process_restart_over_loopback_http_does_not_resume_or_publish(tmp_path, monkeypatch):
    """Real Popen/HTTP/SQLite; loopback Ollama fixture, not actual inference."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    import time
    from scripts.acceptance import selected_environment

    entered, release, returned = Event(), Event(), Event()
    requests = []
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_POST(self):
            assert self.path == '/api/chat'
            requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
            entered.set()
            if not release.wait(20):
                return
            raw = json.dumps({'model':'controlled-loopback-model', 'done':True,
                'message':{'role':'assistant','content':'{}'}}).encode()
            try:
                self.send_response(200)
                self.send_header('Content-Type','application/json')
                self.send_header('Content-Length',str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            except (BrokenPipeError, ConnectionResetError):
                pass  # The killed consumer cannot accept a late fixture result.
            finally:
                returned.set()

    # Fixed local-provider address is the actual application contract. Never
    # reuse or stop a service that already owns either application/provider port.
    provider = ThreadingHTTPServer(('127.0.0.1',11434), Handler)
    provider_thread = Thread(target=provider.serve_forever, daemon=True)
    server = lifecycle.OwnedServer(tmp_path/'real-restart.sqlite3')
    server.env = {**selected_environment('code'), 'EIGHTBALL_DB':str(tmp_path/'real-restart.sqlite3'),
                  'EIGHTBALL_TOKEN':server.token, 'EIGHTBALL_OLLAMA_MODEL':'controlled-loopback-model'}
    processes = []
    restart = server.restart
    def restart_after_remote_arrival():
        assert entered.wait(5), 'Controlled HTTP request never arrived'
        processes.append(server.process)
        code = restart()
        processes.append(server.process)
        release.set()
        return code
    monkeypatch.setattr(server,'restart',restart_after_remote_arrival)
    provider_thread.start()
    try:
        server.start()
        assert server.api.read('/cases') == []
        trial = {'status':'running','job_snapshots':[],'max_application_calls_admitted':0}
        fixture = next(row for row in FIXTURES if row[2]=='graph')
        assert lifecycle.exercise(server,'restart','ollama_staged',False,fixture,trial,lambda:None,15)
        assert trial['status']=='passed' and all(trial['checks'].values())
        assert processes[0].pid != processes[1].pid
        assert processes[0].poll() is not None and processes[1].poll() is None
        assert returned.wait(5) and len(requests)==1
        assert requests[0]['model']=='controlled-loopback-model'
        assert trial['final_job']['status']=='interrupted'
        assert trial['final_job']['calls_started']==1 and trial['final_job']['calls_completed']==0
        assert trial['after_case']==trial['before_case'] and trial['available_proposals']==[]
        # Reload over real HTTP after the late response. No resumed work or
        # second stage may appear, and original case audit must still verify.
        time.sleep(.1)
        base='/cases/'+trial['case_id']
        assert server.api.read(base+'/analysis-jobs/'+trial['job_id'])['status']=='interrupted'
        assert server.api.read(base+'/proposals')==[] and len(requests)==1
        assert server.api.read(base+'/export')['valid'] is True
    finally:
        release.set()
        server.stop()
        provider.shutdown()
        provider.server_close()
        provider_thread.join(5)
    assert not provider_thread.is_alive()
    assert all(process.poll() is not None for process in processes)


def portable_source(checkout):
    from scripts.acceptance import application_digest, digest
    files = {'app.py': 'a'*64}
    links = {'research/external/fixture': {'index_commit':'b'*40, 'checkout_commit':checkout}}
    return {'manifest_version':2, 'files':files, 'research_gitlinks':links,
        'application_sha256':application_digest(files,links),
        'sha256':digest(json.dumps({'files':files,'research_gitlinks':links},sort_keys=True,separators=(',',':')).encode())}


def test_generation_receipt_can_cross_pinned_checkout_availability_without_rewriting_it(tmp_path):
    recorded = portable_source('b'*40)
    current = portable_source(None)
    path = generation_report(tmp_path, source=recorded, source_at_finish=recorded)
    before = path.read_bytes()
    result = lifecycle.generation_prerequisite(path,'openai_compatible',lifecycle.compatible_settings(),current,FIXTURES)
    assert not result['checkout_observations_match']
    assert path.read_bytes() == before
    for invalid in (portable_source('c'*40), {**current,'application_sha256':'forged'}):
        with pytest.raises(lifecycle.SetupBlocked):
            lifecycle.generation_prerequisite(path,'openai_compatible',lifecycle.compatible_settings(),invalid,FIXTURES)
    mismatched = json.loads(before);mismatched['source_at_finish'] = current
    path.write_text(json.dumps(mismatched))
    with pytest.raises(lifecycle.SetupBlocked):
        lifecycle.generation_prerequisite(path,'openai_compatible',lifecycle.compatible_settings(),current,FIXTURES)


def test_native_protocol_cannot_reuse_a_compatibility_generation_receipt(tmp_path,monkeypatch):
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL','https://api.anthropic.com/v1')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER','anthropic')
    path = generation_report(tmp_path)
    monkeypatch.setenv('EIGHTBALL_API_PROTOCOL','anthropic_messages')
    with pytest.raises(lifecycle.SetupBlocked):
        lifecycle.generation_prerequisite(path,'openai_compatible',lifecycle.compatible_settings(),SOURCE,FIXTURES)


def test_native_generation_prerequisite_requires_native_receipts_on_both_graph_stages(tmp_path,monkeypatch):
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL','https://api.anthropic.com/v1')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER','anthropic')
    monkeypatch.setenv('EIGHTBALL_API_PROTOCOL','anthropic_messages')
    path = generation_report(tmp_path)
    assert lifecycle.generation_prerequisite(path,'openai_compatible',lifecycle.compatible_settings(),SOURCE,FIXTURES)
    report = json.loads(path.read_text())
    report['results'][-1]['proposal']['raw_output']['transport']['calls'][1]['native_stop_reason'] = 'max_tokens'
    path.write_text(json.dumps(report))
    with pytest.raises(lifecycle.SetupBlocked):
        lifecycle.generation_prerequisite(path,'openai_compatible',lifecycle.compatible_settings(),SOURCE,FIXTURES)
