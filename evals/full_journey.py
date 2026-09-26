"""Actual-provider integration journey in a disposable local 8BALL instance.

No mock provider, canned graph, catalogue substitution, model download or retry
path exists here. The default preflight does not infer. Explicit --allow-inference
is required; hosted use additionally requires --allow-external and server env.
Scripted review actions test software mechanics, NOT independent human quality.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from datetime import timedelta
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
import httpx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from eightball.models import utcnow
from eightball.v2.runtime_status import local_status
from eightball.v2.hosted import settings,HostedSetupRequired
from scripts.acceptance import native_probe,ensure_port_available,source_manifest,output_directory

STEPS=[
 'Disposable server ready','Blank case has no invented plan','Original source preserved',
 'Actual source extraction completed','Extraction left live state unchanged',
 'Scripted accept/edit/reject recorded','Exact requested outcome retained',
 'Actual staged graph generation completed','Generated graph passed validation',
 'Scripted graph review committed','Distinct conditional routes returned',
 'Graph-linked unanswered questions available','Eligible action explicitly approved',
 'Completion did not prove the result','Separate fixture evidence established the result',
 'Replanning explained the changed condition','Hypothetical refusal left live state untouched',
 'Persisted case reopened','Audit exported with model and review provenance','No cross-case state leakage',
]


class GateFailure(ValueError):pass
class SetupBlocked(ValueError):pass


def preflight(provider,allow_inference=False,allow_external=False):
    if not allow_inference:raise SetupBlocked('Explicit --allow-inference is required. No inference or download started.')
    if provider=='huggingface':
        if not allow_external:raise SetupBlocked('Hosted fixtures require --allow-external. No hosted request started.')
        try:cfg=settings()
        except HostedSetupRequired as exc:raise SetupBlocked(str(exc)) from None
        return {'provider':provider,'model':cfg.model,'inference_provider':cfg.provider,'credentials':'configured_not_authenticated'}
    if provider!='ollama_staged':raise SetupBlocked('Only staged Ollama or explicit Hugging Face is supported')
    local=local_status()
    if local['runtime']!='running' or local['model_present'] is not True:
        raise SetupBlocked(local['note'])
    return {'provider':provider,'model':local['configured_model'],'runtime_version':local['runtime_version'],
            'credentials':'not_required','inference':'not_yet_performed'}


class API:
    def __init__(self,token):
        self.client=httpx.Client(base_url='http://127.0.0.1:8048/api/v2',headers={'Authorization':'Bearer '+token},
                                 timeout=30,trust_env=False,follow_redirects=False)
    def read(self,path):
        r=self.client.get(path);r.raise_for_status();return r.json()
    def post(self,path,body):
        r=self.client.post(path,json=body)
        if r.status_code>=400:
            # Do not dump the request, credentials or arbitrary reflected input.
            raise GateFailure('Application rejected '+path+' with HTTP '+str(r.status_code))
        return r.json()
    def command(self,c,kind,payload):
        return self.post('/cases/'+c['id']+'/commands',{'event_id':uuid.uuid4().hex,'expected_revision':c['revision'],'kind':kind,'payload':payload})
    def analyse(self,c,provider,purpose,source_ids,report,allow_external=False):
        base='/cases/'+c['id'];job=self.post(base+'/analysis-jobs',{
            'request_id':uuid.uuid4().hex,'expected_revision':c['revision'],'provider':provider,
            'purpose':purpose,'source_ids':source_ids,'allow_external':allow_external})
        started=time.monotonic()
        def record(current):
            index=next((i for i,j in enumerate(report['jobs']) if j['id']==current['id']),None)
            if index is None:report['jobs'].append(deepcopy(current))
            else:report['jobs'][index]=deepcopy(current)
            report['actual_model_calls_started']=sum(j.get('calls_started',0) for j in report['jobs'])
            report['call_count_scope']='Latest observed server counts; an in-flight request may finish after cancellation'
        record(job)
        while job['status'] in ('queued','running'):
            if time.monotonic()-started>600:
                cancelled=self.post(base+'/analysis-jobs/'+job['id']+'/cancel',{})
                if isinstance(cancelled,dict) and 'status' in cancelled:record(cancelled)
                raise GateFailure('Actual-provider job exceeded the 600-second journey budget; publication cancelled')
            time.sleep(.25);job=self.read(base+'/analysis-jobs/'+job['id']);record(job)
        proposals=self.read(base+'/proposals')
        p=next((x for x in proposals if x['id']==job.get('proposal_id')),None)
        if p:report['provider_proposals'].append(p)
        if job['status']!='succeeded' or not p or p['status']!='pending':
            raise GateFailure('Actual '+purpose+' did not produce a pending valid proposal: '+job['status'])
        if job.get('calls_started',0)<1:raise GateFailure('No actual provider request was recorded')
        return p
    def close(self):self.client.close()


def choices_for_mixed_review(proposal):
    if len(proposal['items'])<3:
        raise GateFailure('Mixed review needs at least three actual extracted objects; no extra objects will be invented')
    choices=[]
    for i,item in enumerate(proposal['items']):
        choice={'id':item['id'],'disposition':'accepted' if i==0 else 'edited' if i==1 else 'rejected'}
        if i==1:
            obj=deepcopy(item['object'])
            if 'provenance' not in obj:raise GateFailure('Extracted object lacks provenance')
            obj['provenance']['note']='Scripted engineering review annotation. Not independent semantic approval.'
            choice['object']=obj
        choices.append(choice)
    return choices


def native_reopen(token,case_id,title,out):
    from playwright.sync_api import sync_playwright,expect
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
        try:
            page=b.new_page(viewport={'width':1512,'height':1050})
            page.goto('http://127.0.0.1:8048/v2/');page.locator('[name=token]').fill(token)
            page.locator('[data-form=login] [type=submit]').click();page.locator('[data-case="'+case_id+'"]').click()
            expect(page.locator('#main h1')).to_have_text(title)
            page.reload();expect(page.locator('#main h1')).to_have_text(title)
            page.locator('nav [data-tab=audit]').click();expect(page.locator('[data-action=export]')).to_be_visible()
            with page.expect_download() as d:page.locator('[data-action=export]').click()
            data=json.loads(Path(d.value.path()).read_text())
            if not data['valid'] or data['case']['id']!=case_id:raise GateFailure('Native export did not verify')
            page.screenshot(path=str(out/'actual-provider-journey.png'),full_page=True)
            return {'native_reload':True,'native_download':True,'case_id':case_id,'valid':True}
        finally:b.close()


def run(provider,allow_inference=False,allow_external=False,transport='native',output=None):
    out=output_directory(output or ROOT/'artifacts/live-journey')/uuid.uuid4().hex[:12];out.mkdir(parents=True,exist_ok=False)
    report={'schema_version':1,'started_at':utcnow().isoformat(),'source':source_manifest(),
            'provider':provider,'transport':transport,'status':'running','steps':[],
            'jobs':[],'provider_proposals':[],'actual_model_calls_started':0,
            'scripted_operator_review':True,'independent_expert_review':False,'production_approved':False,
            'full_prd_acceptance':False,'native_browser_verified':False,'automatic_retry':False,
            'limits':['Scripted judgement tests integration, not model semantics or independent human judgement.',
                      'HTTP mode does not constitute the required native full-user acceptance.']}
    def save():
        (out/'journey-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    def step(index,ok,details=None):
        record={'number':index,'name':STEPS[index-1],'status':'passed' if ok else 'failed','at':utcnow().isoformat()}
        if details:record['details']=details
        report['steps'].append(record);save()
        if not ok:raise GateFailure(STEPS[index-1])
    api=None;process=None;c=None;temporary=None
    try:
        report['preflight']=preflight(provider,allow_inference,allow_external)
        if os.getenv('EIGHTBALL_BROWSER_BRIDGE'):
            raise SetupBlocked('A bridge is not permitted for the actual-provider acceptance journey')
        if transport=='native':
            probe=native_probe(out,os.environ.copy());report['native_probe']=probe
            if probe['status']!='passed':raise SetupBlocked(probe.get('probe',{}).get('reason','Native browser unavailable'))
        ensure_port_available()
        fixtures=json.loads((ROOT/'evals/generation-cases.json').read_text())
        title,text,_,outcome=next(f for f in fixtures if f[2]=='graph')
        report['fixture_sha256']=hashlib.sha256(json.dumps(fixtures).encode()).hexdigest()
        report['fixture']={'title':title,'source':text,'outcome':outcome}
        temporary=tempfile.TemporaryDirectory(prefix='8ball-live-journey-')
        temp=temporary.name
        token=secrets.token_urlsafe(32)
        env={**os.environ,'EIGHTBALL_DB':str(Path(temp)/'fictional.sqlite3'),'EIGHTBALL_TOKEN':token}
        process=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        api=API(token)
        for _ in range(100):
            try:
                api.read('/status');break
            except httpx.HTTPError:time.sleep(.1)
        else:raise GateFailure('Disposable application did not start')
        step(1,process.poll() is None and api.read('/cases')==[])
        c=api.post('/cases',{'title':'Actual-provider fictional journey','client':'Engineering fixture only',
            'summary':text,'desired_outcome':outcome,'budget':10000,'deadline':(utcnow()+timedelta(days=3)).isoformat()})
        base='/cases/'+c['id'];step(2,not api.read(base)['plan']['routes'] and not c['observations'])
        c=api.command(c,'add_evidence',{'title':'Frozen supplier fixture','source':'Public engineering fixture','text':text})['case']
        source_id=c['evidence'][-1]['id'];step(3,c['evidence'][-1]['text']==text)
        prior=deepcopy(c)
        extraction=api.analyse(c,'ollama' if provider=='ollama_staged' else provider,'extract',[source_id],report,allow_external)
        step(4,extraction['provider'] in ('ollama','huggingface'))
        step(5,api.read(base)['case']==prior and not c['observations'])
        result=api.post(base+'/proposals/'+extraction['id']+'/review',{'event_id':uuid.uuid4().hex,'expected_revision':c['revision'],'choices':choices_for_mixed_review(extraction)})
        c=result['case'];step(6,not c['observations'],{'nature':'Scripted software review only; not independently judged'})
        step(7,c['desired_outcome']==outcome)
        prior=deepcopy(c)
        graph=api.analyse(c,provider,'graph',[source_id],report,allow_external)
        step(8,api.read(base)['case']==prior)
        actions=[i['object'] for i in graph['items'] if i['kind']=='action']
        step(9,bool(actions) and all(a['approval_required'] for a in actions) and all(i['kind'] not in ('observation','approval') for i in graph['items']))
        c=api.post(base+'/proposals/'+graph['id']+'/review',{'event_id':uuid.uuid4().hex,'expected_revision':c['revision'],
                'choices':[{'id':i['id'],'disposition':'accepted'} for i in graph['items']]})['case']
        step(10,not c['observations'] and not c['approvals'])
        data=api.read(base);step(11,len(data['plan']['routes'])>=2 and not data['plan']['outcome_evidenced'])
        step(12,bool(data['briefing']['questions']))
        eligible=[a for a in c['graph']['actions'] if data['plan']['action_states'][a['id']]['status']=='approval_required']
        if not eligible:raise GateFailure('No eligible first action; the graph cannot enter the actual execution-review loop')
        a=eligible[0];c=api.command(c,'approve',{'action_id':a['id']})['case'];step(13,any(x['action_id']==a['id'] for x in c['approvals']))
        before_states=api.read(base)['plan']['states'];c=api.command(c,'complete',{'action_id':a['id']})['case']
        step(14,api.read(base)['plan']['states']==before_states)
        changed=[]
        for effect in a['effects']:
            cond=next(x for x in c['graph']['conditions'] if x['id']==effect['condition_id'])
            verification='Fictional engineering observation only: a test reviewer reports '+cond['title']+'. This is not a real-world model-quality result.'
            c=api.command(c,'add_evidence',{'title':'Explicit integration-test observation','source':'Scripted fictional test reviewer','text':verification})['case']
            eid=c['evidence'][-1]['id'];c=api.command(c,'review_evidence',{'evidence_id':eid,'status':'reviewed'})['case']
            result=api.command(c,'observe',{'condition_id':cond['id'],'evidence_id':eid,'value':effect['value'],'rationale':'Explicit synthetic fixture observation, separate from work completion'})
            c=result['case'];changed.extend(result['changes'].get('conditions',[]))
        step(15,any(o['condition_id']==a['effects'][0]['condition_id'] for o in c['observations']))
        step(16,bool(changed))
        before=api.read(base+'/export');effect=a['effects'][0]
        sim=api.post(base+'/simulate',{'expected_revision':c['revision'],'conditions':{effect['condition_id']:not effect['value']}})
        step(17,sim['persisted'] is False and api.read(base+'/export')==before)
        if transport=='native':
            report['browser']=native_reopen(token,c['id'],c['title'],out);report['native_browser_verified']=True
        step(18,api.read(base)['case']==c,{'transport':transport})
        export=api.read(base+'/export')
        step(19,export['valid'] and export['replay_matches_snapshot'] and len(export['model_runs'])==2)
        (out/'fictional-case-export.json').write_text(json.dumps(export,indent=2)+'\n')
        independent=api.post('/cases',{'title':'Isolation fixture','client':'Separate fictional case','summary':'No sources.',
            'desired_outcome':'Independent target','deadline':(utcnow()+timedelta(days=1)).isoformat(),'budget':1000})
        step(20,api.read('/cases/'+independent['id'])['case']['evidence']==[] and api.read('/cases/'+independent['id']+'/proposals')==[])
        report['status']='passed'
    except SetupBlocked as exc:
        report['status']='blocked';report['reason']=str(exc)
    except Exception as exc:
        report['status']='failed';report['reason']=str(exc)[:1000] if isinstance(exc,GateFailure) else type(exc).__name__
    finally:
        if api:api.close()
        if process:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait()
        if temporary:temporary.cleanup()
        report['source_unchanged_during_run']=report['source']==source_manifest()
        if not report['source_unchanged_during_run']:
            report['status']='failed';report['reason']='Source changed during the run'
        report['finished_at']=utcnow().isoformat();report['complete']=True;save()
    print(json.dumps({k:report[k] for k in ('status','actual_model_calls_started','native_browser_verified','independent_expert_review')},indent=2))
    print('Report: '+str(out/'journey-report.json'))
    return report,out/'journey-report.json'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--provider',choices=['ollama_staged','huggingface'],required=True)
    p.add_argument('--allow-inference',action='store_true');p.add_argument('--allow-external',action='store_true')
    p.add_argument('--transport',choices=['native','http'],default='native');p.add_argument('--output',type=Path)
    a=p.parse_args();r,_=run(a.provider,a.allow_inference,a.allow_external,a.transport,a.output)
    sys.exit(0 if r['status']=='passed' else 2 if r['status']=='blocked' else 1)
