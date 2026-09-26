"""Actual queue/store tests with controlled provider responses, NOT model quality."""
import json
from threading import Thread, Event
from datetime import timedelta
from contextlib import contextmanager
import pytest
import httpx
from eightball.v2.analysis_jobs import AnalysisJobs, AnalysisRequest, ControlledClient, JobStopped, MAX_QUEUE
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Proposal
from eightball.v2.commands import Command
from eightball.models import uid
from eightball.store import digest, Conflict


@pytest.fixture
def setup(tmp_path):
    store=Store(str(tmp_path/'s.db'));case=store.create(demo_case(),fixture=True)
    manager=AnalysisJobs(store,launch=False)
    return store,case,manager


def request(case,**kwargs):
    return AnalysisRequest(request_id=uid(),expected_revision=case.revision,provider='rules',purpose='extract',source_ids=[case.evidence[0].id],**kwargs)


def job_proposal(case):
    return Proposal(case_id=case.id,base_revision=case.revision,provider='rules',model='test-double',purpose='extract',
                    output_hash=digest({}),latency_ms=0,items=[])


def test_manual_job_transitions_real_store_no_live_fact_mutation(setup):
    store,c,m=setup;before=store.get(c.id)
    j=m.submit(c.id,request(c));assert j['status']=='queued'
    assert m.run_next();done=m.get(c.id,j['id'])
    assert done['status']=='succeeded' and done['proposal_id']
    assert store.get(c.id)==before and store.audit(c.id)['valid']
    assert store.proposals(c.id)[0]['status']=='pending'
    assert not m.run_next()


def test_duplicate_submission_is_idempotent_even_after_completion(setup):
    store,c,m=setup;r=request(c);j=m.submit(c.id,r);m.run_next()
    assert m.submit(c.id,r)['id']==j['id'];assert len(m.list(c.id))==1
    assert len(store.proposals(c.id))==1
    with pytest.raises(Conflict):m.submit(c.id,r.model_copy(update={'purpose':'graph'}))


def test_queued_cancel_does_not_call_model_or_publish(setup):
    store,c,m=setup;called=[];m.runner=lambda *a,**k:called.append(True)
    j=m.submit(c.id,request(c));done=m.cancel(c.id,j['id'])
    assert done['status']=='cancelled' and not done['worker_active']
    assert not m.run_next();assert not called and not store.proposals(c.id)
    assert m.cancel(c.id,j['id'])['status']=='cancelled'


def test_cancel_inflight_discards_late_success(setup):
    store,c,m=setup;entered=Event();finish=Event()
    def runner(case,*args,**kw):
        entered.set();assert finish.wait(5);return job_proposal(case)
    m.runner=runner;j=m.submit(c.id,request(c));t=Thread(target=m.run_next);t.start()
    assert entered.wait(5)
    response=m.cancel(c.id,j['id']);assert response['status']=='cancelled' and response['worker_active']
    finish.set();t.join(5);assert not t.is_alive()
    assert not m.get(c.id,j['id'])['worker_active'];assert not store.proposals(c.id)
    assert store.get(c.id).revision==0


def test_case_change_during_inference_discards_late_output(setup):
    store,c,m=setup;entered=Event();finish=Event()
    def runner(case,*args,**kw):
        entered.set();assert finish.wait(5);return job_proposal(case)
    m.runner=runner;j=m.submit(c.id,request(c));t=Thread(target=m.run_next);t.start();assert entered.wait(5)
    store.change(c.id,Command(event_id=uid(),expected_revision=0,kind='metadata',payload={'budget':5000}))
    finish.set();t.join(5)
    assert m.get(c.id,j['id'])['status']=='superseded';assert not store.proposals(c.id)


def test_case_changes_while_queued_no_provider_call(setup):
    store,c,m=setup;called=[];m.runner=lambda *a,**k:called.append(True)
    j=m.submit(c.id,request(c));store.change(c.id,Command(event_id=uid(),expected_revision=0,kind='metadata',payload={'budget':6000}))
    m.run_next();assert m.get(c.id,j['id'])['status']=='superseded' and not called


def test_cancel_cannot_delete_already_published_result(setup):
    store,c,m=setup;j=m.submit(c.id,request(c));m.run_next();p=m.get(c.id,j['id'])['proposal_id']
    assert m.cancel(c.id,j['id'])['status']=='succeeded';assert store.proposals(c.id)[0]['id']==p


def test_restart_marks_unfinished_interrupted_never_resumes(setup):
    store,c,m=setup;j=m.submit(c.id,request(c));again=AnalysisJobs(store,launch=False)
    assert again.get(c.id,j['id'])['status']=='interrupted';assert not again.run_next()
    assert not store.proposals(c.id)


def test_restart_preserves_cancelled_status_and_clears_worker_flag(setup):
    store,c,m=setup;j=m.submit(c.id,request(c));m.cancel(c.id,j['id'])
    with store.connection() as db:
        row=m._get(db,j['id']);row['worker_active']=True;m._save(db,row);db.commit()
    again=AnalysisJobs(store,launch=False);x=again.get(c.id,j['id'])
    assert x['status']=='cancelled' and not x['worker_active']


def test_foreign_case_job_access_denied(setup):
    store,c,m=setup;other=store.create(demo_case(),fixture=True);j=m.submit(c.id,request(c))
    with pytest.raises(KeyError):m.get(other.id,j['id'])
    with pytest.raises(KeyError):m.cancel(other.id,j['id'])
    assert not m.list(other.id)


@pytest.mark.parametrize('mutation',[
 {'provider':'huggingface','purpose':'graph','allow_external':False},
 {'source_ids':['not-in-case']}, {'expected_revision':1},
 {'purpose':'graph','provider':'rules'},
])
def test_invalid_submission_preflight_no_job_created(setup,mutation):
    store,c,m=setup;r=request(c).model_copy(update=mutation)
    with pytest.raises(ValueError):m.submit(c.id,r)
    assert not m.list(c.id) and not store.proposals(c.id)


def test_hosted_missing_configuration_no_job_no_network(setup,monkeypatch):
    store,c,m=setup;monkeypatch.delenv('HF_TOKEN',raising=False)
    with pytest.raises(ValueError):m.submit(c.id,request(c).model_copy(update={'provider':'huggingface','allow_external':True}))
    assert not m.list(c.id)


def test_queue_limit_and_slot_reclaimed_after_cancel(setup):
    store,c,m=setup;js=[m.submit(c.id,request(c)) for _ in range(MAX_QUEUE)]
    with pytest.raises(Conflict):m.submit(c.id,request(c))
    m.cancel(c.id,js[0]['id']);assert m.submit(c.id,request(c))['status']=='queued'


def test_exception_text_never_echoed_in_job(setup):
    store,c,m=setup
    def bad(*args,**kwargs):raise RuntimeError('HF_TOKEN=secret-fixture DO NOT LEAK')
    m.runner=bad;j=m.submit(c.id,request(c));m.run_next();result=m.get(c.id,j['id'])
    assert result['status']=='failed' and 'secret-fixture' not in json.dumps(result)
    assert not store.proposals(c.id)


def test_wrong_case_provider_output_rejected(setup):
    store,c,m=setup;other=store.create(demo_case(),fixture=True)
    m.runner=lambda *a,**k:job_proposal(other);j=m.submit(c.id,request(c));m.run_next()
    assert m.get(c.id,j['id'])['status']=='failed' and not store.proposals(c.id)


def test_transport_post_progress_and_cancel_before_second_call(setup):
    store,c,m=setup;j=m.submit(c.id,request(c));calls=[]
    def factory(**kwargs):
        return httpx.Client(transport=httpx.MockTransport(lambda r:(calls.append(str(r.url)) or httpx.Response(200,json={}))))
    controlled=ControlledClient(m,j['id'],factory)
    try:
        controlled.post('http://127.0.0.1:11434/api/chat')
        row=m.get(c.id,j['id']);assert row['calls_started']==row['calls_completed']==1
        m.cancel(c.id,j['id'])
        with pytest.raises(JobStopped):controlled.post('http://127.0.0.1:11434/api/chat')
        assert len(calls)==1
    finally:controlled.close()


def test_stream_checks_each_chunk_and_never_leaks_headers(setup):
    store,c,m=setup;j=m.submit(c.id,request(c))
    class Stream(httpx.SyncByteStream):
        def __iter__(self):
            yield b'one'
            m.cancel(c.id,j['id'])
            yield b'two'
    def factory(**kwargs):return httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(200,stream=Stream())))
    controlled=ControlledClient(m,j['id'],factory)
    with pytest.raises(JobStopped):
        with controlled.stream('POST','https://router.huggingface.co/v1/chat/completions',headers={'Authorization':'Bearer secret-fixture'}) as r:
            list(r.iter_bytes())
    assert 'secret-fixture' not in json.dumps(m.list(c.id));controlled.close()


def test_launch_worker_admission_does_not_lose_jobs(tmp_path):
    store=Store(str(tmp_path/'s.db'));c=store.create(demo_case(),fixture=True)
    m=AnalysisJobs(store,runner=lambda case,*a,**k:job_proposal(case))
    jobs=[m.submit(c.id,request(c)) for _ in range(5)]
    if m.worker:m.worker.join(5)
    assert all(m.get(c.id,j['id'])['status']=='succeeded' for j in jobs)
    assert len(store.proposals(c.id))==5


@pytest.mark.parametrize('method,suffix',[
    ('GET','/analysis-jobs'),('GET','/analysis-jobs/missing'),
    ('POST','/analysis-jobs/missing/cancel'),('POST','/analysis-jobs'),
    ('POST','/graph/preview'),
])
def test_new_endpoints_require_operator_auth(tmp_path,method,suffix):
    from eightball.api import make_app
    from eightball.store import Store as LegacyStore
    from fastapi.testclient import TestClient
    app=make_app(LegacyStore(str(tmp_path/'api.db')),'x'*32)
    cl=TestClient(app)
    kwargs={'json':{}} if method=='POST' else {}
    assert cl.request(method,'/api/v2/cases/missing'+suffix,**kwargs).status_code==401


def test_async_http_api_publishes_only_review_proposal(tmp_path):
    from eightball.api import make_app
    from eightball.store import Store as LegacyStore
    from fastapi.testclient import TestClient
    app=make_app(LegacyStore(str(tmp_path/'api.db')),'x'*32)
    cl=TestClient(app,headers={'Authorization':'Bearer '+'x'*32})
    c=cl.post('/api/v2/demo',json={}).json();base=f"/api/v2/cases/{c['id']}"
    before=cl.get(base).json()['case']
    req={'request_id':uid(),'expected_revision':0,'provider':'rules','purpose':'extract','source_ids':[c['evidence'][0]['id']]}
    response=cl.post(base+'/analysis-jobs',json=req)
    assert response.status_code==202
    worker=app.state.analysis_jobs.worker
    if worker:worker.join(5)
    job=cl.get(base+'/analysis-jobs/'+response.json()['id']).json()
    assert job['status']=='succeeded' and job['proposal_id']
    assert cl.get(base).json()['case']==before
    assert cl.get(base+'/history').json()['valid']
    assert cl.post(base+'/analysis-jobs',json=req).json()['id']==job['id']
