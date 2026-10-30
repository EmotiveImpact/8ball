"""Immutable hosted experiment receipts using controlled responses only."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from types import SimpleNamespace

import httpx
import pytest

from evals import live_huggingface as runner
from eightball.v2.hosted import HostedFailure
from eightball.v2.intelligence import propose as actual_propose

ROOT=Path(__file__).resolve().parents[1]
KEY='fictional-private-retention-test-key'
FIXTURES=json.loads((ROOT/'evals/generation-cases.json').read_text())
STAGED=json.loads((ROOT/'tests/fixtures/drafting/staged.json').read_text())


@pytest.fixture(autouse=True)
def configuration(monkeypatch):
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL','https://retention.example.com/v1')
    monkeypatch.setenv('EIGHTBALL_API_MODEL','qwen-fixture')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER','fixture-provider')
    monkeypatch.setenv('EIGHTBALL_API_KEY',KEY)
    monkeypatch.delenv('EIGHTBALL_API_ROUTING_PROVIDER',raising=False)
    monkeypatch.setattr(runner,'settings',lambda:SimpleNamespace(model='hf-fixture',provider='fixture-provider'))
    # Each test binds a controlled source identity; source-manifest integration
    # itself has separate traversal/fingerprint tests in test_acceptance_runner.
    monkeypatch.setattr(runner,'source_manifest',lambda:{'sha256':'a'*64,'files':{'fixture.py':'b'*64}})
    monkeypatch.setattr(runner,'source_commit',lambda:'c'*40)


def run(output,provider='openai_compatible'):
    return runner.main(['--allow-hosted','--provider',provider,'--output',str(output)])


def report_files(output,name='compatible-report.json'):
    return sorted(output.glob('*/'+name))


def rejected(*args,**kwargs):
    failure=HostedFailure('controlled_rejection')
    failure.trace={'diagnostic':{'code':'controlled_rejection'},
                   'transport':{'calls':[{'raw_content':'Unchanged controlled rejection bytes.'}]}}
    raise failure


@pytest.fixture
def successful_requests(monkeypatch):
    """Actual proposal/compiler paths over controlled remote envelopes only."""
    state=SimpleNamespace(requests=[],on_response=lambda:None)
    responses=[]
    for title,text,purpose,outcome in FIXTURES:
        if purpose=='extract':
            responses.append({'items':[{'kind':'claim','text':'Controlled fictional claim',
                'source':{'evidence_id':'source','quote':text}}]})
        else:
            frame=deepcopy(STAGED['frame'])
            frame['target_bindings']=[{'criterion_index':i,'target_quote':outcome}
                                     for i in range(len(frame['success_criteria']))]
            responses.extend([frame,deepcopy(STAGED['routes'])])
    def respond(request):
        state.requests.append(request)
        output=responses.pop(0)
        state.on_response()
        if request.url.path.endswith('/messages'):
            return httpx.Response(200,json={'type':'message','role':'assistant','model':'controlled-served-model',
                'content':[{'type':'text','text':json.dumps(output)}], 'stop_reason':'end_turn',
                'usage':{'input_tokens':20,'output_tokens':10}})
        return httpx.Response(200,json={'model':'controlled-served-model',
            'choices':[{'index':0,'finish_reason':'stop','message':{'role':'assistant',
                'content':json.dumps(output)}}]})
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        monkeypatch.setattr(runner,'propose',lambda case,provider,purpose,sources,**kwargs:
                            actual_propose(case,provider,purpose,sources,client=client,**kwargs))
        yield state


def test_native_generation_keeps_original_fixtures_and_exact_protocol_evidence(tmp_path,monkeypatch,successful_requests):
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL','https://api.anthropic.com/v1')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER','anthropic')
    monkeypatch.setenv('EIGHTBALL_API_PROTOCOL','anthropic_messages')
    assert run(tmp_path)==0
    report=json.loads(report_files(tmp_path)[0].read_text())
    assert report['api_protocol']=='anthropic_messages'
    assert report['fixture_sha256']==runner.FIXTURES_SHA256
    assert len(successful_requests.requests)==5 and report['structural_gate_passed']
    assert all(call['api_protocol']=='anthropic_messages' and call['native_stop_reason']=='end_turn'
        for row in report['results'] for call in row['proposal']['raw_output']['transport']['calls'])
    assert not report['production_approved'] and not report['independent_semantic_benchmark']


@pytest.mark.parametrize('provider,name',[
    ('openai_compatible','compatible-report.json'),('huggingface','huggingface-report.json')])
def test_successive_rejections_keep_every_prior_receipt_and_snapshot(tmp_path,monkeypatch,provider,name):
    monkeypatch.setattr(runner,'propose',rejected)
    assert run(tmp_path,provider)==1
    first=report_files(tmp_path,name)[0]
    before={p.relative_to(tmp_path):p.read_bytes() for p in first.parent.rglob('*.json')}
    assert run(tmp_path,provider)==1
    reports=report_files(tmp_path,name)
    assert len(reports)==2 and not (tmp_path/name).exists()
    assert all((tmp_path/p).read_bytes()==raw for p,raw in before.items())
    data=[json.loads(p.read_text()) for p in reports]
    assert len({r['run_id'] for r in data})==2
    for r,p in zip(data,reports):
        assert r['run_id']==p.parent.name and r['status']=='failed' and r['complete']
        assert r['planned_fixtures']==r['completed_fixtures']==r['started_fixtures']==4
        assert r['fixture_sha256']==runner.FIXTURES_SHA256
        assert r['fixture_file_sha256']==sha256((ROOT/'evals/generation-cases.json').read_bytes()).hexdigest()
        assert r['source']['sha256']=='a'*64 and r['source_commit']=='c'*40
        assert r['versions']['compiler']==runner.COMPILER_VERSION
        assert r['versions']['graph_prompt']==runner.GRAPH_PROMPT_VERSION
        assert r['versions']['intake_prompt']==runner.INTAKE_PROMPT_VERSION
        assert not r['automatic_retry'] and not r['independent_semantic_benchmark']
        assert not r['production_approved'] and not r['structural_gate_passed']
        assert KEY not in json.dumps(r)
        assert all(x['trace']['transport']['calls'][0]['raw_content']=='Unchanged controlled rejection bytes.'
                   for x in r['results'])
        assert len(list((p.parent/'checkpoints').glob('*.json')))==10


def test_complete_result_is_durable_before_next_fixture_request(tmp_path,monkeypatch):
    seen=[]
    def controlled(case,provider,purpose,sources,*,allow_external):
        path=report_files(tmp_path)[0]
        report=json.loads(path.read_text())
        assert report['status']=='running' and not report['complete']
        assert report['completed_fixtures']==len(seen)
        assert len(report['results'])==len(seen)
        assert report['active_fixture']['title']==case.title
        assert report['active_fixture']['source_sha256']==sha256(case.evidence[0].text.encode()).hexdigest()
        assert report['active_fixture']['outcome_sha256']==sha256(case.desired_outcome.encode()).hexdigest()
        assert report['active_fixture']['fixture_input_sha256']==sha256(
            json.dumps(FIXTURES[len(seen)],ensure_ascii=False).encode()).hexdigest()
        if seen:
            assert report['results'][-1]['trace']['diagnostic']['code']=='controlled_rejection'
        seen.append(case.title)
        rejected()
    monkeypatch.setattr(runner,'propose',controlled)
    assert run(tmp_path)==1
    assert seen==[f[0] for f in FIXTURES]


def test_structural_success_and_raw_transport_survive_a_later_failed_invocation(tmp_path,monkeypatch):
    responses=[]
    requests=[]
    for title,text,purpose,outcome in FIXTURES:
        if purpose=='extract':
            responses.append({'items':[{'kind':'claim','text':'Controlled fictional claim',
                'source':{'evidence_id':'source','quote':text}}]})
        else:
            frame=deepcopy(STAGED['frame'])
            frame['target_bindings']=[{'criterion_index':i,'target_quote':outcome}
                                     for i in range(len(frame['success_criteria']))]
            responses.extend([frame,deepcopy(STAGED['routes'])])
    def respond(req):
        requests.append(req)
        output=responses.pop(0)
        return httpx.Response(200,json={'model':'controlled-served-model',
            'choices':[{'index':0,'finish_reason':'stop','message':{'role':'assistant','content':json.dumps(output)}}],
            'usage':{'prompt_tokens':20,'completion_tokens':10,'total_tokens':30}})
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        monkeypatch.setattr(runner,'propose',lambda case,provider,purpose,sources,**kwargs:
                            actual_propose(case,provider,purpose,sources,client=client,**kwargs))
        assert run(tmp_path)==0
    first=report_files(tmp_path)[0]
    original=first.read_bytes()
    report=json.loads(original)
    assert report['status']=='passed' and report['complete'] and report['structural_gate_passed']
    assert report['source_unchanged_during_run'] and report['source_at_finish']==report['source']
    assert report['source_checks'][-1]['point']=='finish'
    assert all(check['status']=='matched' for check in report['source_checks'])
    assert report['actual_hosted_requests'] and report['all_live_states_unchanged']
    assert len(requests)==5 and not responses
    graph=report['results'][-1]
    assert graph['candidate_routes']>=2
    assert len(graph['proposal']['raw_output']['transport']['calls'])==2
    assert graph['proposal']['model']=='controlled-served-model'
    assert KEY not in original.decode()
    monkeypatch.setattr(runner,'propose',rejected)
    assert run(tmp_path)==1
    assert first.read_bytes()==original and len(report_files(tmp_path))==2


def test_keyboard_interrupt_keeps_completed_raw_evidence_and_stops_future_calls(tmp_path,monkeypatch):
    calls=[]
    previous=signal.getsignal(signal.SIGTERM)
    def interrupted(*args,**kwargs):
        calls.append(args[0].title)
        if len(calls)==2:raise KeyboardInterrupt()
        rejected()
    monkeypatch.setattr(runner,'propose',interrupted)
    with pytest.raises(KeyboardInterrupt):run(tmp_path)
    report=json.loads(report_files(tmp_path)[0].read_text())
    assert report['status']=='interrupted' and not report['complete']
    assert report['structural_gate_passed'] is False
    assert len(calls)==report['started_fixtures']==2 and report['completed_fixtures']==1
    assert report['results'][0]['trace']['transport']['calls'][0]['raw_content']=='Unchanged controlled rejection bytes.'
    assert report['active_fixture']['status']=='interrupted'
    assert report['interruption']['request_may_have_completed_without_returned_trace'] is True
    assert report['interruption']['error_type']=='KeyboardInterrupt'
    assert signal.getsignal(signal.SIGTERM)==previous
    before={p:p.read_bytes() for p in report_files(tmp_path)[0].parent.rglob('*.json')}
    monkeypatch.setattr(runner,'propose',rejected)
    assert run(tmp_path)==1
    assert all(p.read_bytes()==raw for p,raw in before.items())


@pytest.mark.parametrize('error', [KeyboardInterrupt, SystemExit, GeneratorExit])
@pytest.mark.parametrize('source_error', [False, True])
def test_final_source_failure_preserves_interruption_or_abort(tmp_path,monkeypatch,error,source_error):
    def interrupted(*args, **kwargs):
        def inspect():
            if source_error:
                raise OSError('private source path')
            return {'sha256':'changed','files':{}}
        monkeypatch.setattr(runner,'source_manifest',inspect)
        raise error()
    monkeypatch.setattr(runner,'propose',interrupted)
    with pytest.raises(error):run(tmp_path)
    report=json.loads(report_files(tmp_path)[0].read_text())
    assert report['status']==('aborted' if error is GeneratorExit else 'interrupted')
    assert report['source_unchanged_during_run'] is False
    assert report['source_checks'][-1]['status']==('inspection_failed' if source_error else 'changed')
    assert report['interruption']['error_type']==error.__name__
    assert report['completed_fixtures']==0 and report['started_fixtures']==1
    assert 'private source path' not in report_files(tmp_path)[0].read_text()


@pytest.mark.parametrize('signum',[signal.SIGTERM,signal.SIGKILL])
@pytest.mark.skipif(os.name!='posix',reason='POSIX process signal evidence')
def test_process_signal_keeps_prior_completed_receipt_without_another_call(tmp_path,signum):
    script=r'''
import json,os,signal,sys
from pathlib import Path
from evals import live_huggingface as runner
from eightball.v2.hosted import HostedFailure
runner.source_manifest=lambda:{'sha256':'a'*64,'files':{}}
runner.source_commit=lambda:'c'*40
count=0
def controlled(*args,**kwargs):
 global count
 count+=1
 if count==2:os.kill(os.getpid(),int(sys.argv[2]))
 failure=HostedFailure('signal_fixture_rejection')
 failure.trace={'diagnostic':{'code':'signal_fixture_rejection'},'transport':{'calls':[{'raw_content':'first retained response'}]}}
 raise failure
runner.propose=controlled
raise SystemExit(runner.main(['--allow-hosted','--provider','openai_compatible','--output',sys.argv[1]]))
'''
    env={**os.environ,'EIGHTBALL_API_BASE_URL':'https://retention.example.com/v1',
         'EIGHTBALL_API_MODEL':'qwen-fixture','EIGHTBALL_API_PROVIDER':'fixture-provider','EIGHTBALL_API_KEY':KEY}
    env.pop('EIGHTBALL_API_ROUTING_PROVIDER',None)
    result=subprocess.run([sys.executable,'-c',script,str(tmp_path),str(signum)],cwd=ROOT,
                          env=env,capture_output=True,text=True,timeout=15)
    assert result.returncode==(128+signum if signum==signal.SIGTERM else -signum)
    report=json.loads(report_files(tmp_path)[0].read_text())
    assert report['completed_fixtures']==1 and report['started_fixtures']==2
    assert report['results'][0]['trace']['transport']['calls'][0]['raw_content']=='first retained response'
    assert not report['complete'] and not report['structural_gate_passed']
    if signum==signal.SIGTERM:
        assert report['status']=='interrupted' and report['interruption']['signal']==signum
    else:
        # An uncatchable kill cannot fabricate a terminal event or a response.
        assert report['status']=='running' and report['active_fixture']['status']=='request_not_yet_returned'
    assert KEY not in (result.stdout+result.stderr+json.dumps(report))


def test_checkpoint_failure_aborts_before_any_following_provider_request(tmp_path,monkeypatch):
    calls=[]
    original=runner.checkpoint
    def checkpoint(report,*args):
        if report['completed_fixtures']==1:raise OSError('Controlled disk failure')
        original(report,*args)
    def controlled(*args,**kwargs):
        calls.append(args[0].title);rejected()
    monkeypatch.setattr(runner,'checkpoint',checkpoint)
    monkeypatch.setattr(runner,'propose',controlled)
    with pytest.raises(OSError,match='Controlled disk failure'):run(tmp_path)
    assert len(calls)==1
    report=json.loads(report_files(tmp_path)[0].read_text())
    assert report['started_fixtures']==1 and report['completed_fixtures']==0
    assert report['status']=='running' and not report['complete']


def test_source_drift_after_response_retains_output_and_stops_next_fixture(tmp_path,monkeypatch,successful_requests):
    identity={'sha256':'initial','files':{}}
    monkeypatch.setattr(runner,'source_manifest',lambda:deepcopy(identity))
    successful_requests.on_response=lambda:identity.update(sha256='changed')
    assert run(tmp_path)==1
    report=json.loads(report_files(tmp_path)[0].read_text())
    assert report['status']=='failed' and not report['complete']
    assert report['started_fixtures']==report['completed_fixtures']==len(successful_requests.requests)==1
    assert not report['source_unchanged_during_run']
    assert report['source']['sha256']=='initial' and report['source_at_finish']['sha256']=='changed'
    assert report['source_checks'][-2]=={'point':'before_fixture_1','status':'changed','sha256':'changed'}
    returned=report['results'][0]['proposal']['raw_output']['transport']['calls'][0]
    assert returned['raw_content'] and returned['status']=='response_received'
    assert report['results'][0]['status']=='valid_proposal' and report['active_fixture'] is None


def test_source_drift_in_last_response_keeps_structural_result_but_invalidates_evidence(tmp_path,monkeypatch,successful_requests):
    identity={'sha256':'initial','files':{}}
    monkeypatch.setattr(runner,'source_manifest',lambda:deepcopy(identity))
    def drift_last():
        if len(successful_requests.requests)==5:identity.update(sha256='changed')
    successful_requests.on_response=drift_last
    assert run(tmp_path)==1
    report=json.loads(report_files(tmp_path)[0].read_text())
    assert report['status']=='failed' and report['complete']
    assert report['structural_gate_passed'] is True and not report['source_unchanged_during_run']
    assert report['completed_fixtures']==4 and len(successful_requests.requests)==5
    assert len(report['results'][-1]['proposal']['raw_output']['transport']['calls'])==2
    assert report['source_checks'][-2]['point']=='before_result'
    assert report['source_checks'][-2]['status']=='changed'


def test_restored_source_does_not_erase_observed_drift(tmp_path,monkeypatch,successful_requests):
    inspections=[]
    def inspect():
        inspections.append(True)
        return {'sha256':'changed' if len(inspections)==3 else 'initial','files':{}}
    monkeypatch.setattr(runner,'source_manifest',inspect)
    assert run(tmp_path)==1
    report=json.loads(report_files(tmp_path)[0].read_text())
    assert report['status']=='failed' and not report['source_unchanged_during_run']
    assert report['source_at_finish']==report['source']
    assert report['source_checks'][-2]['status']=='changed' and report['source_checks'][-1]['status']=='matched'
    assert len(successful_requests.requests)==1


@pytest.mark.parametrize('after_last_response',[False,True])
def test_source_inspection_error_fails_closed_without_losing_returned_evidence(tmp_path,monkeypatch,successful_requests,after_last_response):
    inspections=[]
    def inspect():
        inspections.append(True)
        if (after_last_response and len(successful_requests.requests)==5
                or not after_last_response and len(inspections)>1):
            raise OSError('private local path or diagnostic must not escape')
        return {'sha256':'initial','files':{}}
    monkeypatch.setattr(runner,'source_manifest',inspect)
    assert run(tmp_path)==1
    path=report_files(tmp_path)[0]
    report=json.loads(path.read_text())
    assert report['status']=='failed' and not report['source_unchanged_during_run']
    assert report['source_at_finish'] is None
    assert report['source_checks'][-1]=={'point':'finish','status':'inspection_failed','error_type':'OSError'}
    assert 'private local path' not in path.read_text()
    assert len(successful_requests.requests)==(5 if after_last_response else 0)
    assert report['completed_fixtures']==(4 if after_last_response else 0)
    if after_last_response:
        assert report['structural_gate_passed'] is True
        assert report['results'][-1]['proposal']['raw_output']['transport']['calls'][-1]['raw_content']
