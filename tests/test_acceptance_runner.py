"""Verification-tool tests use synthetic records, never claim actual model runs."""
from copy import deepcopy
from pathlib import Path
import json
import os
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


def test_outputs_cannot_pollute_source(tmp_path):
    root=tmp_path/'source';root.mkdir()
    with pytest.raises(ValueError):a.output_directory(root/'docs/reports',root)
    assert a.output_directory(root/'artifacts/reports',root)==root/'artifacts/reports'
    assert a.output_directory(tmp_path/'outside',root)==tmp_path/'outside'


@pytest.mark.parametrize('mode',['native','code','bridge'])
def test_standard_verification_removes_credentials_and_case_path(monkeypatch,mode):
    for k in ('HF_TOKEN','TYPESAFE_API_KEY','OPENAI_API_KEY','EIGHTBALL_DB','EIGHTBALL_TOKEN'):
        monkeypatch.setenv(k,'not-a-real-secret')
    monkeypatch.setenv('EIGHTBALL_BROWSER_BRIDGE','1')
    env=a.selected_environment(mode)
    assert not any(k in env for k in ('HF_TOKEN','TYPESAFE_API_KEY','OPENAI_API_KEY','EIGHTBALL_DB','EIGHTBALL_TOKEN'))
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
