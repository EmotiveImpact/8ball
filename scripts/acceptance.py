"""One evidence-producing verification command. No silent fallback or downloads.

Examples:
  python scripts/acceptance.py --mode native
  python scripts/acceptance.py --mode bridge
  python scripts/acceptance.py --mode code
  python scripts/acceptance.py --inspect artifacts/acceptance/<run>/report.json

Code, browser transport, provider inference and expert judgement are distinct.
A passing selected run is never a production-release or model-quality approval.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import uuid
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

BROWSER_SUITES=[
 ('legacy','tests/browser_smoke.py','browser-report.json'),
 ('workspace','tests/browser_v2.py','browser-v2-report.json'),
 ('providers','tests/browser_development.py','development-browser-report.json'),
 ('connections','tests/browser_graph.py','browser-graph-report.json'),
 ('studio','tests/browser_studio.py','studio-browser-report.json'),
 ('sources','tests/browser_sources.py','source-browser-report.json'),
 ('insights','tests/browser_insights.py','insights-browser-report.json'),
 ('grounding','tests/browser_grounding.py','browser-grounding-report.json'),
 ('plan_review','tests/browser_plan_review.py','browser-plan-review-report.json'),
 ('accessibility','tests/browser_accessibility.py','accessibility-browser-report.json'),
 ('courses','tests/browser_courses.py','browser-courses-report.json'),
]
EXCLUDE={'.git','.venv','__pycache__','.pytest_cache','artifacts','node_modules','build','dist','test-results'}


def now():return datetime.now(timezone.utc).isoformat()
def digest(raw:bytes):return hashlib.sha256(raw).hexdigest()


def source_manifest(root:Path=ROOT):
    files={}
    for path in sorted(root.rglob('*')):
        rel=path.relative_to(root)
        if any(p in EXCLUDE or p.endswith('.egg-info') for p in rel.parts):continue
        if (path.name.startswith('.env') and path.name!='.env.example') or path.suffix in ('.db','.sqlite','.sqlite3','.pyc','.log'):continue
        if path.is_symlink():raise ValueError('Source manifest refuses symbolic links: '+str(rel))
        if path.is_file():files[rel.as_posix()]=digest(path.read_bytes())
    return {'sha256':digest(json.dumps(files,sort_keys=True,separators=(',',':')).encode()),'files':files}


def selected_environment(mode):
    env=os.environ.copy()
    # Standard verification cannot accidentally use configured private providers
    # or an operator's own database. Tests create fictional disposable stores.
    for key in ('HF_TOKEN','HUGGINGFACE_API_TOKEN','TYPESAFE_API_KEY','OPENAI_API_KEY',
                'EIGHTBALL_DB','EIGHTBALL_TOKEN','EIGHTBALL_ARTIFACTS','EIGHTBALL_BROWSER_BRIDGE'):
        env.pop(key,None)
    if mode=='bridge':env['EIGHTBALL_BROWSER_BRIDGE']='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    return env


def execute(name,args,output:Path,env,timeout=180):
    started=now();t=time.monotonic();log=output/(name+'.log')
    with log.open('w',encoding='utf-8') as handle:
        process=subprocess.Popen(args,cwd=ROOT,env=env,stdout=handle,stderr=subprocess.STDOUT,
                                 start_new_session=(os.name=='posix'))
        timed_out=False
        try:code=process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out=True
            if os.name=='posix':os.killpg(process.pid,signal.SIGTERM)
            else:process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if os.name=='posix':os.killpg(process.pid,signal.SIGKILL)
                else:process.kill()
                process.wait()
            code=process.returncode
    return {'name':name,'command':args,'status':'failed' if code else 'passed','exit_code':code,
            'timed_out':timed_out,'started_at':started,'finished_at':now(),
            'seconds':round(time.monotonic()-t,3),'log':log.name,'log_sha256':digest(log.read_bytes())}


def junit_counts(path:Path):
    tree=ET.parse(path);root=tree.getroot()
    suites=[root] if root.tag=='testsuite' else list(root.findall('testsuite'))
    if not suites:raise ValueError('No test suite found in JUnit report')
    totals={k:sum(int(s.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')}
    if totals['tests']<=0:raise ValueError('No tests were executed')
    totals['passed']=totals['tests']-totals['failures']-totals['errors']-totals['skipped']
    return totals


def browser_report(path:Path,mode:str):
    data=json.loads(path.read_text(encoding='utf-8'))
    count=data.get('checks_passed');checks=data.get('checks')
    if type(count) is not int or not count or not isinstance(checks,list) or count!=len(checks):
        raise ValueError('Browser report count does not match its checks')
    transport=str(data.get('network','')).lower()
    if mode=='native' and ('native' not in transport and 'real loopback http' not in transport or 'bridge' in transport):
        raise ValueError('Non-native report cannot satisfy native acceptance')
    if mode=='bridge' and 'bridge' not in transport:
        raise ValueError('Bridge run has mislabelled transport')
    if data.get('errors') or data.get('runtime_errors'):raise ValueError('Browser runtime errors recorded')
    return {'count':count,'transport':data['network'],'sha256':digest(path.read_bytes())}


def native_probe(output:Path,env):
    # Does not relax browser policy or substitute another transport.
    script=r'''
import json,threading,os,shutil
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from playwright.sync_api import sync_playwright
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.end_headers();self.wfile.write(b'<h1>8BALL native probe</h1>')
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
result={'status':'failed','policy_changed':False}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
  try:
   page=browser.new_page();page.goto('http://127.0.0.1:'+str(server.server_port),timeout=8000)
   assert page.locator('h1').inner_text()=='8BALL native probe'
   result.update(status='passed',reason='Native loopback navigation succeeded')
  finally:browser.close()
except Exception as exc:
 message=str(exc)
 blocked='ERR_BLOCKED_BY_ADMINISTRATOR' in message
 result.update(status='blocked' if blocked else 'failed',reason='Native navigation blocked by administrator policy' if blocked else type(exc).__name__,diagnostic=message[:1000])
finally:server.shutdown();server.server_close()
print(json.dumps(result))
'''
    result=execute('native-probe',[sys.executable,'-c',script],output,env,30)
    try:details=json.loads((output/'native-probe.log').read_text().splitlines()[-1])
    except (ValueError,IndexError):details={'status':'failed','reason':'Native probe did not produce a report'}
    return {**result,'status':details['status'],'probe':details}


def ensure_port_available(port=8048):
    with socket.socket() as sock:
        try:sock.bind(('127.0.0.1',port))
        except OSError as exc:raise ValueError('Test port 8048 is occupied; no existing process was stopped') from exc


def output_directory(path,root:Path=ROOT):
    out=Path(path or root/'artifacts/acceptance').resolve()
    if out.is_relative_to(root.resolve()) and not out.is_relative_to((root/'artifacts').resolve()):
        raise ValueError('Verification output must be outside source or inside its artifacts directory')
    return out


def artifact_manifest(directory:Path):
    files={}
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():raise ValueError('Verification artifacts cannot be symbolic links')
        if path.is_file() and path.name not in ('report.json','report.tmp'):
            files[path.relative_to(directory).as_posix()]=digest(path.read_bytes())
    return files


def inspect(report:dict,root:Path=ROOT,artifact_root:Path|None=None):
    def invalid(reason):return {'valid':False,'reason':reason,'model_quality_approved':False,'released':False}
    if report.get('schema_version')!=1 or report.get('complete') is not True:
        return invalid('Verification was not completed')
    current=source_manifest(root)
    if current!=report.get('source') or report.get('source_unchanged_during_run') is not True:
        return invalid('Source changed or its manifest does not match')
    mode=report.get('mode');checks=report.get('checks',[])
    required={'unit','compile','delivery','changelog','emergence','javascript','structural-fixtures','endstate-package','schemas'}
    if mode not in ('code','native','bridge') or not required<={c.get('name') for c in checks}:
        return invalid('Declared verification scope is incomplete')
    if len({c.get('name') for c in checks})!=len(checks):return invalid('Duplicate verification step')
    states={c.get('status') for c in checks}
    if not states<={'passed','failed','blocked'}:return invalid('Unknown verification status')
    expected='failed' if 'failed' in states else 'blocked' if 'blocked' in states else 'passed'
    if report.get('status')!=expected:return invalid('Run status disagrees with its steps')
    suites=[c for c in checks if c['name'].startswith('browser-')]
    complete_browser={c['name'] for c in suites}=={'browser-'+s[0] for s in BROWSER_SUITES}
    native=mode=='native' and complete_browser and all(c['status']=='passed' for c in suites)
    if mode!='code' and expected=='passed' and not complete_browser:
        return invalid('A passing browser run omitted suites')
    if report.get('native_browser_verified') is not native:
        return invalid('Native acceptance disagrees with the recorded transport')
    if artifact_root is None:return invalid('The artifact directory is required to verify the recorded evidence')
    try:
        actual=artifact_manifest(artifact_root)
        if not actual or actual!=report.get('artifacts'):return invalid('Verification evidence is missing or changed')
        for item in checks:
            if 'log' in item and actual.get(item['log'])!=item.get('log_sha256'):
                return invalid('Step log does not match its recorded hash')
            if item.get('report'):
                path=artifact_root/item['report']
                if not path.resolve().is_relative_to(artifact_root.resolve()):return invalid('Unsafe evidence path')
                if browser_report(path,mode)!=item.get('browser'):return invalid('Browser evidence disagrees with summary')
        if junit_counts(artifact_root/'junit.xml')!=next(c for c in checks if c['name']=='unit').get('counts'):
            return invalid('Code-test count disagrees with JUnit evidence')
    except (OSError,ValueError,KeyError,StopIteration,ET.ParseError):return invalid('Verification evidence could not be validated')
    return {'valid':True,'reason':'Source and local evidence bytes match; this is not a signed attestation',
            'run_status':expected,'native_browser_verified':native,'model_quality_approved':False,'released':False}


def run(mode='native',base=None,root_output=None):
    root_output=output_directory(root_output)
    run_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    out=root_output/run_id;out.mkdir(parents=True,exist_ok=False)
    source=source_manifest();env=selected_environment(mode)
    report={'schema_version':1,'run_id':run_id,'started_at':now(),'complete':False,'mode':mode,'source':source,
            'environment':{'python':platform.python_version(),'platform':platform.system()},'checks':[],
            'native_browser_verified':False,'model_inference_performed':False,'model_quality_approved':False,
            'expert_review':'not_performed','merged':False,'released':False,'status':'running'}
    def save():
        temp=out/'report.tmp';temp.write_text(json.dumps(report,indent=2)+'\n');temp.replace(out/'report.json')
    def step(name,args,timeout=180):
        item=execute(name,args,out,env,timeout);report['checks'].append(item);save();print(name+': '+item['status'],flush=True);return item
    save()
    try:
        item=step('unit',[sys.executable,'-m','pytest','-q','--junitxml='+str(out/'junit.xml')],300)
        try:
            item['counts']=junit_counts(out/'junit.xml')
            if item['counts']['failures'] or item['counts']['errors']:item['status']='failed'
        except Exception as exc:item.update(status='failed',diagnostic=type(exc).__name__)
        step('compile',[sys.executable,'-m','compileall','-q','eightball','endstate'])
        for name in ('delivery','changelog','emergence'):
            args=[sys.executable,'scripts/'+name+'.py','--check']
            if base and name!='delivery':args+=['--base',base]
            step(name,args)
        syntax=step('javascript',[sys.executable,'-c',
             "from pathlib import Path;import subprocess;files=[Path('web/app.js'),*sorted(Path('web/v2').glob('*.js'))];[subprocess.run(['node','--check',str(p)],check=True) for p in files];print(len(files),'modules checked')"])
        step('structural-fixtures',[sys.executable,'evals/plan_review_bench.py'])
        step('endstate-package',[sys.executable,'scripts/build_endstate.py','--regressions','--output',str(out/'package')])
        step('schemas',[sys.executable,'scripts/export_endstate_schemas.py','--output',str(out/'schemas')])
        if mode!='code':
            ensure_port_available()
            proceed=True
            if mode=='native':
                probe=native_probe(out,env);report['checks'].append(probe);save();proceed=probe['status']=='passed'
            if proceed:
                for name,script,filename in BROWSER_SUITES:
                    if not (ROOT/script).is_file():
                        report['checks'].append({'name':name,'status':'failed','reason':'Declared test suite missing'});continue
                    destination=out/('browser-'+name);destination.mkdir()
                    suite_env={**env,'EIGHTBALL_ARTIFACTS':str(destination)}
                    item=execute('browser-'+name,[sys.executable,script],out,suite_env,240)
                    try:
                        parsed=browser_report(destination/filename,mode)
                        item['report']=str((destination/filename).relative_to(out));item['browser']=parsed
                    except Exception as exc:item.update(status='failed',diagnostic=str(exc)[:500])
                    report['checks'].append(item);save();print(item['name']+': '+item['status'],flush=True)
                suites=[c for c in report['checks'] if c['name'].startswith('browser-')]
                report['browser_checks_passed']=sum(c.get('browser',{}).get('count',0) for c in suites if c['status']=='passed')
                report['native_browser_verified']=mode=='native' and len(suites)==len(BROWSER_SUITES) and all(c['status']=='passed' for c in suites)
        final_source=source_manifest()
        report['source_unchanged_during_run']=source['sha256']==final_source['sha256']
        if not report['source_unchanged_during_run']:
            report['checks'].append({'name':'source-stability','status':'failed','reason':'Source bytes changed while tests were running'})
        statuses={c['status'] for c in report['checks']}
        report['status']='failed' if 'failed' in statuses else 'blocked' if 'blocked' in statuses else 'passed'
    except Exception as exc:
        report['status']='failed';report['checks'].append({'name':'runner','status':'failed','diagnostic':str(exc)[:1000]})
    finally:
        report['complete']=True;report['finished_at']=now()
        try:report['artifacts']=artifact_manifest(out)
        except (OSError,ValueError) as exc:
            report['status']='failed';report['checks'].append({'name':'artifact-integrity','status':'failed','diagnostic':str(exc)})
        save()
    print('Report: '+str(out/'report.json'),flush=True)
    return report,out/'report.json'


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=['native','bridge','code'],default='native')
    parser.add_argument('--base');parser.add_argument('--output',type=Path);parser.add_argument('--inspect',type=Path)
    args=parser.parse_args()
    if args.inspect:
        result=inspect(json.loads(args.inspect.read_text()),artifact_root=args.inspect.parent);print(json.dumps(result,indent=2));sys.exit(0 if result['valid'] else 1)
    report,_=run(args.mode,args.base,args.output)
    sys.exit(0 if report['status']=='passed' else 2 if report['status']=='blocked' else 1)
