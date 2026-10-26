"""Build and test the actual internal wheel without network or provider access."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
ROOT=Path(__file__).resolve().parents[1]


def run(args,cwd,env=None,*,timeout=120):
    result=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True,timeout=timeout)
    if result.returncode:
        raise RuntimeError('Offline package command failed: '+(result.stdout+'\n'+result.stderr)[-4000:])
    return result.stdout


def build(output:Path,regressions=False):
    output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='endstate-package-') as tmp:
        temp=Path(tmp);wheel_dir=temp/'wheels';wheel_dir.mkdir()
        run([sys.executable,'-m','pip','wheel','--no-deps','--no-build-isolation','--no-index','--disable-pip-version-check',
             '--wheel-dir',str(wheel_dir),str(ROOT)],ROOT)
        wheels=list(wheel_dir.glob('*.whl'))
        if len(wheels)!=1:raise ValueError('Expected exactly one wheel')
        wheel=wheels[0]
        with zipfile.ZipFile(wheel) as z:
            names=z.namelist()
            expected = {str(p.relative_to(ROOT)) for p in (ROOT/'endstate').rglob('*.py')}
            if not expected.issubset(names):
                raise ValueError('Wheel omits kernel packages: ' + ', '.join(sorted(expected - set(names))))
            if any(not (n.startswith('endstate/') or '.dist-info/' in n) for n in names):
                raise ValueError('Wheel contains files outside the kernel and its metadata')
            if any(n.endswith(('.db','.sqlite3','.zip','.gguf','.safetensors')) for n in names):
                raise ValueError('Unexpected data/model file in wheel')
            for name in names:
                if name.startswith('endstate/'):
                    source=ROOT/name
                    if not source.is_file() or source.read_bytes()!=z.read(name):
                        raise ValueError('Wheel module does not match current source: '+name)
        target=temp/'installed'
        run([sys.executable,'-m','pip','install','--no-index','--no-deps','--disable-pip-version-check','--target',str(target),str(wheel)],temp)
        snippet=r'''
import builtins,json,pathlib,sys
sys.path.insert(0,sys.argv[1])
original=builtins.__import__
def guarded(name,*args,**kwargs):
    if name.split('.')[0] in ('eightball','fastapi','httpx','sqlite3'):
        raise ImportError('Runtime dependency forbidden during standalone kernel test')
    return original(name,*args,**kwargs)
builtins.__import__=guarded
from endstate.api import PlanRequest,PlanResponse,calculate
from endstate.contracts import PlanningSnapshot,Graph,Condition,Action,Objective,Effect,atom
from datetime import datetime,timezone,timedelta
now=datetime(2026,9,24,tzinfo=timezone.utc)
snapshot=PlanningSnapshot(id='embedded-fixture',owner='Reviewer',revision=0,
    budget=1000,deadline=now+timedelta(days=1),graph=Graph(
    conditions=[Condition(id='goal',title='Outcome verified',confirmation='Explicit reviewer evidence')],
    actions=[Action(id='a',title='Method A',owner='Lead',purpose='Test',effects=[Effect(condition_id='goal')],minutes=10,approval_required=True),
             Action(id='b',title='Method B',owner='Lead',purpose='Test alternative',effects=[Effect(condition_id='goal')],minutes=20,approval_required=True)],
    objectives=[Objective(id='outcome',title='Verified outcome',success=atom('goal'))]))
r=calculate(PlanRequest(snapshot=snapshot,as_of=now))
assert len(r.plan['routes'])==2 and not r.plan['outcome_evidenced']
assert r.plan['action_states']['a']['status']=='approval_required'
assert PlanResponse.model_validate_json(r.model_dump_json()).model_dump(mode='json')==r.model_dump(mode='json')
from endstate.scenarios import Scenario,compare,verify
from endstate.decision_packet import Selection,project
from endstate.intelligence.decisions import ChoiceQuestion,validate_choice
before=snapshot.model_dump_json()
comparison=compare(snapshot,Scenario(expected_revision=0,budget=0),now)
assert verify(snapshot,comparison) and snapshot.model_dump_json()==before
packet=project({'reference_hashes':{'case:summary':'0'*64},'private':'Fictional private narrative'},
               Selection(mode='reference_index',references=['case:summary']),{'case:summary'})
assert packet['brief'] is None and 'Fictional private narrative' not in json.dumps(packet)
q=ChoiceQuestion(id='review',instructions='Review only',criteria={'review':'Seek evidence','defer':'Defer review'})
assert validate_choice({'type':'choice','choice':'review','confidence':1.0,'probabilities':{'review':1.0,'defer':0.0}},q)['choice']=='review'
from endstate.forecasting import Forecast,Resolution,evaluate,forecast_digest
f=Forecast(id='delivery',event='Delivery confirmed before tomorrow',as_of=now,horizon=now+timedelta(days=1),
           input_sha256='0'*64,predictor='package_fixture',probability=0.5)
o=Resolution(forecast_id=f.id,forecast_sha256=forecast_digest(f),value=False,available_at=now+timedelta(days=2),
             source_reference='Synthetic package fixture',source_sha256='1'*64,basis='synthetic')
evaluation=evaluate([f],[o],as_of=now+timedelta(days=2))
assert evaluation['brier']==0.25 and not evaluation['predictive_quality_approved'] and not evaluation['facts_attested']
from endstate.intelligence.coordination import ReviewSpec,summarize
comparison=summarize(ReviewSpec(id='review',models=['jev-latest'],max_seconds=30,
 max_reported_cost_nano_usd=100,questions=[dict(id='check',instructions='Missing evidence requires review.',
 criteria={'review':'More review needed.','continue':'Continue human review, not approval.'})]),[])
assert comparison['answered_models']==0 and comparison['questions'][0]['missing_models']==['jev-latest']
assert not comparison['facts_attested'] and not comparison['execution_authorized']
import endstate
assert pathlib.Path(endstate.__file__).resolve().is_relative_to(pathlib.Path(sys.argv[1]).resolve())
print(json.dumps({'installed_outside_repository':True,'routes':len(r.plan['routes']),
 'input_unchanged':snapshot.observations==[],'approval_preserved':True,'roundtrip_exact':True,
 'scenario_replay':True,'restricted_packet':True,'typed_advisory_contract':True,
 'forecast_measurement_only':True,
 'specialist_comparison_only':True,
 'forbidden_runtime_imports':[],'model_inference':False}))
'''
        test=json.loads(run([sys.executable,'-I','-c',snippet,str(target)],temp))
        regression=None
        if regressions:
            # Run the unchanged application's full suite with the installed kernel
            # taking precedence. This tests the distribution, not a source-copy alias.
            code=r"""
import pathlib,sys
root,target,out=map(pathlib.Path,sys.argv[1:])
sys.path.insert(0,str(root));sys.path.insert(0,str(target))
import endstate
assert pathlib.Path(endstate.__file__).resolve().is_relative_to(target.resolve())
import pytest
result=pytest.main([str(root/'tests'),'-q','--import-mode=importlib','--junitxml='+str(out/'installed-junit.xml')])
assert pathlib.Path(endstate.__file__).resolve().is_relative_to(target.resolve())
sys.exit(result)
"""
            log=run([sys.executable,'-I','-c',code,str(ROOT),str(target),str(output.resolve())],temp,timeout=600)
            (output/'installed-regressions.log').write_text(log)
            import xml.etree.ElementTree as ET
            suites=list(ET.parse(output/'installed-junit.xml').getroot().findall('testsuite'))
            regression={k:sum(int(x.get(k,0)) for x in suites) for k in ('tests','failures','errors','skipped')}
            if not regression['tests'] or regression['errors'] or regression['failures']:
                raise ValueError('Installed-kernel regression run did not pass')
        destination=output/wheel.name;destination.write_bytes(wheel.read_bytes())
        report={'schema_version':1,'status':'passed','distribution':'internal_alpha_only',
                'python':sys.version.split()[0],'wheel':wheel.name,
                'sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),'contents':names,
                'kernel_sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'endstate').rglob('*.py'))},
                'test':test,'installed_regressions':regression,'network_used':False,'published':False,
                'limits':['Current installed Python and Pydantic only; other platforms require their own run.',
                          'Read-only calculation package; no hosted API, action execution or commercial support claim.']}
        (output/'package-verification.json').write_text(json.dumps(report,indent=2)+'\n')
        return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'artifacts/endstate-package')
    parser.add_argument('--regressions',action='store_true',help='Also run all application tests against the installed wheel')
    args=parser.parse_args();print(json.dumps(build(args.output,args.regressions),indent=2))
