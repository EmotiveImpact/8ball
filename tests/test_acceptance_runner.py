"""Verification-tool tests use synthetic records, never claim actual model runs."""
from copy import deepcopy
from pathlib import Path
import json
import os
import subprocess
import sys
import pytest
from scripts import acceptance as a
from evals import full_journey as j


def write(path,content):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content);return path


def fixture_report(tmp_path):
    root=tmp_path/'source';root.mkdir();write(root/'app.py','value=1\n')
    artifacts=tmp_path/'evidence';artifacts.mkdir()
    write(artifacts/'junit.xml','<testsuites><testsuite tests="3" failures="0" errors="0" skipped="1"/></testsuites>')
    checks=[]
    for name in ('unit','compile','delivery','changelog','emergence','javascript','structural-fixtures','endstate-package','schemas'):
        log=write(artifacts/(name+'.log'),'fixture output\n')
        checks.append({'name':name,'status':'passed','log':log.name,'log_sha256':a.digest(log.read_bytes())})
    checks[0]['counts']=a.junit_counts(artifacts/'junit.xml')
    report={'schema_version':1,'source':a.source_manifest(root),'complete':True,'mode':'code',
            'source_unchanged_during_run':True,'status':'passed','checks':checks,
            'native_browser_verified':False,'artifacts':a.artifact_manifest(artifacts)}
    return root,artifacts,report


def test_manifest_excludes_secrets_and_generated_output(tmp_path):
    write(tmp_path/'code.py','pass\n');write(tmp_path/'.env.local','SECRET=do-not-read');write(tmp_path/'.env','secret')
    write(tmp_path/'.env.example','DOCUMENTATION=only');write(tmp_path/'artifacts/run/report.json','{}')
    write(tmp_path/'build/file','generated');write(tmp_path/'thing.egg-info/a','generated')
    write(tmp_path/'__pycache__/a.pyc','generated');write(tmp_path/'client.sqlite3','private')
    assert set(a.source_manifest(tmp_path)['files'])=={'code.py','.env.example'}


def test_manifest_refuses_symbolic_source(tmp_path):
    source=write(tmp_path/'real.py','pass');(tmp_path/'alias.py').symlink_to(source)
    with pytest.raises(ValueError):a.source_manifest(tmp_path)


def test_manifest_bound_to_content_not_only_names(tmp_path):
    p=write(tmp_path/'a.py','first');before=a.source_manifest(tmp_path);p.write_text('second')
    assert a.source_manifest(tmp_path)!=before


def test_manifest_retains_legacy_shape_and_hash_without_research_gitlinks(tmp_path):
    write(tmp_path/'app.py','first\n');write(tmp_path/'docs/readme.md','fixture\n')
    files={'app.py':a.digest(b'first\n'),'docs/readme.md':a.digest(b'fixture\n')}
    assert a.source_manifest(tmp_path)=={
        'files':files,'sha256':a.digest(json.dumps(files,sort_keys=True,separators=(',',':')).encode())}


def test_research_tree_is_pruned_before_traversal_but_app_and_inventory_stay_bound(tmp_path,monkeypatch):
    app=write(tmp_path/'eightball/app.py','value=1\n')
    inventory=write(tmp_path/'research/inventory.json','{"commit":"first"}')
    vendor=write(tmp_path/'research/external/vendor/test_upstream.py','raise RuntimeError("never import")\n')
    (vendor.parent/'upstream-symlink').symlink_to(tmp_path/'missing')
    original_walk=a.os.walk
    visited=[]
    def observe(*args,**kwargs):
        for row in original_walk(*args,**kwargs):
            visited.append(Path(row[0]));yield row
    monkeypatch.setattr(a.os,'walk',observe)
    before=a.source_manifest(tmp_path)
    assert set(before['files'])=={'eightball/app.py','research/inventory.json'}
    assert all(not path.is_relative_to(tmp_path/'research/external') for path in visited)
    vendor.write_text('different upstream source\n')
    assert a.source_manifest(tmp_path)==before
    inventory.write_text('{"commit":"second"}')
    changed_inventory=a.source_manifest(tmp_path)
    assert changed_inventory!=before
    app.write_text('value=2\n')
    assert a.source_manifest(tmp_path)!=changed_inventory


def test_manifest_binds_research_gitlink_pin_and_checkout_head(tmp_path):
    def git(root,*args):
        return subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True,text=True).stdout.strip()
    root=tmp_path/'source';root.mkdir();git(root,'init','-q')
    vendor=root/'research/external/vendor';vendor.mkdir(parents=True);git(vendor,'init','-q')
    write(vendor/'upstream.py','first\n');git(vendor,'add','upstream.py')
    git(vendor,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','first')
    first=git(vendor,'rev-parse','HEAD')
    git(root,'update-index','--add','--cacheinfo',f'160000,{first},research/external/vendor')
    before=a.source_manifest(root)
    assert before['research_gitlinks']=={'research/external/vendor':{'index_commit':first,'checkout_commit':first}}
    write(vendor/'upstream.py','second\n');git(vendor,'add','upstream.py')
    git(vendor,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','second')
    second=git(vendor,'rev-parse','HEAD')
    drifted=a.source_manifest(root)
    assert drifted['sha256']!=before['sha256']
    assert drifted['research_gitlinks']['research/external/vendor']=={'index_commit':first,'checkout_commit':second}
    git(root,'update-index','--cacheinfo',f'160000,{second},research/external/vendor')
    assert a.source_manifest(root)['sha256']!=drifted['sha256']
    # Uninitialized checkouts still retain their declared pin without looking up
    # the containing application's HEAD as if it were the vendor's HEAD.
    import shutil
    shutil.rmtree(vendor/'.git')
    uninitialized=a.source_manifest(root)
    assert uninitialized['research_gitlinks']['research/external/vendor']=={'index_commit':second,'checkout_commit':None}


@pytest.mark.parametrize('explicit_root',[False,True])
def test_repository_pytest_config_never_collects_external_research(tmp_path,explicit_root):
    write(tmp_path/'pytest.ini',(a.ROOT/'pytest.ini').read_text())
    write(tmp_path/'tests/test_application.py','def test_app():\n    pass\n')
    write(tmp_path/'research/external/vendor/conftest.py','raise RuntimeError("upstream conftest executed")\n')
    write(tmp_path/'research/external/vendor/test_vendor.py','invalid Python syntax !\n')
    command=[sys.executable,'-m','pytest','--collect-only','-q']
    if explicit_root:command.append('.')
    result=subprocess.run(command,cwd=tmp_path,capture_output=True,text=True,timeout=30)
    assert result.returncode==0,result.stdout+result.stderr
    assert 'tests/test_application.py::test_app' in result.stdout
    assert 'vendor' not in result.stdout and '1 test collected' in result.stdout


def test_outputs_cannot_pollute_source(tmp_path):
    root=tmp_path/'source';root.mkdir()
    with pytest.raises(ValueError):a.output_directory(root/'docs/reports',root)
    assert a.output_directory(root/'artifacts/reports',root)==root/'artifacts/reports'
    assert a.output_directory(tmp_path/'outside',root)==tmp_path/'outside'


@pytest.mark.parametrize('mode',['native','code','bridge'])
def test_standard_verification_removes_credentials_and_case_path(monkeypatch,mode):
    private=('HF_TOKEN','TYPESAFE_API_KEY','OPENAI_API_KEY','EIGHTBALL_DB','EIGHTBALL_TOKEN',
             'EIGHTBALL_API_KEY','EIGHTBALL_API_BASE_URL','EIGHTBALL_API_MODEL',
             'EIGHTBALL_API_PROVIDER','EIGHTBALL_API_ROUTING_PROVIDER')
    for k in private:
        monkeypatch.setenv(k,'not-a-real-secret')
    monkeypatch.setenv('EIGHTBALL_BROWSER_BRIDGE','1')
    env=a.selected_environment(mode)
    assert not any(k in env for k in private)
    assert ('EIGHTBALL_BROWSER_BRIDGE' in env)==(mode=='bridge')


@pytest.mark.parametrize('mode,network,ok',[
    ('native','Native loopback HTTP',True),('native','ASGI bridge',False),
    ('bridge','Native loopback HTTP',False),('bridge','ASGI bridge, not browser HTTP',True),
    ('native','real loopback HTTP',True),('native','native bridge',False),
])
def test_transport_cannot_masquerade(tmp_path,mode,network,ok):
    p=write(tmp_path/'report.json',json.dumps({'checks_passed':2,'checks':['a','b'],'network':network}))
    if ok:assert a.browser_report(p,mode)['count']==2
    else:
        with pytest.raises(ValueError):a.browser_report(p,mode)


@pytest.mark.parametrize('change',[{'checks_passed':0},{'checks_passed':True},{'checks':['a']},{'errors':['runtime failure']}])
def test_empty_or_inconsistent_browser_reports_rejected(tmp_path,change):
    d={'checks_passed':2,'checks':['a','b'],'network':'Native loopback HTTP'};d.update(change)
    p=write(tmp_path/'report.json',json.dumps(d))
    with pytest.raises(ValueError):a.browser_report(p,'native')


def test_inspection_verifies_both_source_and_artifacts(tmp_path):
    root,out,report=fixture_report(tmp_path)
    assert not a.inspect(report,root)['valid']
    result=a.inspect(report,root,out)
    assert result['valid'] and not result['native_browser_verified'] and not result['model_quality_approved']
    write(out/'unit.log','modified output')
    assert not a.inspect(report,root,out)['valid']


@pytest.mark.parametrize('field,value',[('complete',False),('native_browser_verified',True),('source_unchanged_during_run',False),('status','blocked')])
def test_inspection_rejects_unearned_claims(tmp_path,field,value):
    root,out,report=fixture_report(tmp_path);report[field]=value
    assert not a.inspect(report,root,out)['valid']


def test_completed_blocked_record_is_evidence_not_acceptance(tmp_path):
    root,out,report=fixture_report(tmp_path);report['checks'].append({'name':'native-probe','status':'blocked'})
    report.update(mode='native',status='blocked')
    result=a.inspect(report,root,out)
    assert result['valid'] and result['run_status']=='blocked' and not result['native_browser_verified']


def test_inspection_rejects_missing_steps_and_changed_source(tmp_path):
    root,out,report=fixture_report(tmp_path);copy=deepcopy(report);copy['checks'].pop()
    assert not a.inspect(copy,root,out)['valid']
    write(root/'app.py','value=2\n');assert not a.inspect(report,root,out)['valid']


def test_no_provider_requests_without_explicit_permission(monkeypatch):
    def forbidden():pytest.fail('No provider or local probe should run without consent')
    monkeypatch.setattr(j,'local_status',forbidden);monkeypatch.setattr(j,'settings',forbidden)
    for provider in ('ollama_staged','huggingface'):
        with pytest.raises(j.SetupBlocked):j.preflight(provider)
    with pytest.raises(j.SetupBlocked):j.preflight('huggingface',True,False)


def test_missing_provider_returns_blocked_zero_calls(monkeypatch,tmp_path):
    for key in ('HF_TOKEN','EIGHTBALL_HF_MODEL','EIGHTBALL_HF_PROVIDER'):monkeypatch.delenv(key,raising=False)
    report,path=j.run('huggingface',True,True,'http',tmp_path)
    assert report['complete'] and report['status']=='blocked' and report['actual_model_calls_started']==0
    assert not report['full_prd_acceptance'] and not report['independent_expert_review']
    assert path.is_file()


def test_local_probe_is_not_model_inference(monkeypatch):
    monkeypatch.setattr(j,'local_status',lambda:{'runtime':'running','model_present':True,'configured_model':'fixture:4b','runtime_version':'fixture'})
    result=j.preflight('ollama_staged',True)
    assert result['inference']=='not_yet_performed'


def test_no_mixed_review_objects_are_invented():
    with pytest.raises(j.GateFailure):j.choices_for_mixed_review({'items':[{'id':'one','object':{}}]})
    p={'items':[{'id':str(i),'object':{'title':'original','provenance':{'note':'source'}}} for i in range(4)]}
    original=deepcopy(p);choices=j.choices_for_mixed_review(p)
    assert p==original and [x['disposition'] for x in choices]==['accepted','edited','rejected','rejected']
    assert choices[1]['object']['title']=='original'


def test_model_call_accounting_survives_rejection(monkeypatch):
    """Test double checks logging only; never reported as live inference."""
    client=j.API('fixture-only');state={'read':0}
    job={'id':'job','status':'queued','calls_started':0}
    def post(path,body):return deepcopy(job)
    def read(path):
        if path.endswith('/proposals'):return []
        state['read']+=1
        return {'id':'job','status':'running' if state['read']==1 else 'failed','calls_started':2}
    monkeypatch.setattr(client,'post',post);monkeypatch.setattr(client,'read',read)
    monkeypatch.setattr(j.time,'sleep',lambda _:None)
    report={'jobs':[],'provider_proposals':[],'actual_model_calls_started':0}
    try:
        with pytest.raises(j.GateFailure):client.analyse({'id':'case','revision':0},'ollama_staged','graph',['e'],report)
        assert report['actual_model_calls_started']==2 and len(report['jobs'])==1
        assert report['jobs'][0]['status']=='failed'
    finally:client.close()


@pytest.mark.parametrize('invalid',['schema','span'])
def test_journey_report_preserves_actual_queue_rejection_after_disposable_database_cleanup(monkeypatch,tmp_path,invalid):
    """Controlled responses exercise the queue/report path, never actual inference."""
    import tempfile
    import httpx
    from eightball.v2.analysis_jobs import AnalysisJobs,AnalysisRequest
    from eightball.v2.store import Store
    from eightball.v2.playbooks import demo_case
    from eightball.v2.intelligence import PROMPT_VERSION
    raw={'items':[{'kind':'claim','text':'Unsupported claim',
                  'source':{'evidence_id':'missing','quote':'Unsupported quotation'}}]}
    if invalid=='schema':raw['items'][0]['kind']='observation'
    report={'jobs':[],'provider_proposals':[],'actual_model_calls_started':0}
    path=tmp_path/'retained-report.json'
    with tempfile.TemporaryDirectory(dir=tmp_path) as disposable:
        database=Path(disposable)/'case.db';store=Store(str(database));c=store.create(demo_case(),fixture=True)
        def factory(**kw):
            return httpx.Client(transport=httpx.MockTransport(lambda req:httpx.Response(200,json={
                'model':'controlled-model','done':True,'message':{'content':json.dumps(raw)}})))
        manager=AnalysisJobs(store,launch=False,client_factory=factory)
        client=j.API('fixture-only')
        def post(url,body):
            assert url==f'/cases/{c.id}/analysis-jobs'
            queued=manager.submit(c.id,AnalysisRequest.model_validate(body))
            assert manager.run_next()
            return queued
        def read(url):
            if url.endswith('/proposals'):return store.proposals(c.id)
            return manager.get(c.id,url.rsplit('/',1)[1])
        monkeypatch.setattr(client,'post',post);monkeypatch.setattr(client,'read',read)
        try:
            with pytest.raises(j.GateFailure):
                client.analyse({'id':c.id,'revision':0},'ollama','extract',[c.evidence[0].id],report)
        finally:client.close()
        path.write_text(json.dumps(report,allow_nan=False))
    assert not database.exists()
    retained=json.loads(path.read_text())
    assert retained['actual_model_calls_started']==1 and retained['jobs'][0]['status']=='failed'
    failure=retained['provider_proposals'][0]
    assert failure['status']=='failed' and failure['model']=='controlled-model' and failure['latency_ms']>=0
    assert failure['raw_output']['prompt_version']==PROMPT_VERSION and failure['raw_output']['extraction']==raw
