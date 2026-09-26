"""Black workspace, explicit provider controls and target-review browser checks.

Native HTTP by default. Optional existing ASGI bridge is labelled in the report.
The target proposal is a controlled fixture, not live model-quality evidence.
"""
from pathlib import Path
from datetime import timedelta
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

import httpx
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from browser_v2 import open_document, BRIDGE, TOKEN
from eightball.v2.contracts import Case, Proposal, utcnow
from eightball.v2.store import Store
from eightball.v2.intelligence import GraphOutput, graph_items
from endstate.compilation import draft_outcome

OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/development')))
OUT.mkdir(parents=True,exist_ok=True)
checks=[]


def check(name,condition):
    assert condition,name
    checks.append(name)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'cases.sqlite3');store=Store(db)
        outcome="Obtain enough suitable chairs and the venue manager's written acceptance"
        case=Case(title='Target review fixture',client='Fictional test only',summary='A supplier failure.',
                  desired_outcome=outcome,deadline=utcnow()+timedelta(days=2))
        store.create(case)
        fixture=json.loads((ROOT/'tests/fixtures/drafting/staged.json').read_text())
        fixture['frame']['target_bindings']=[{'criterion_index':i,'target_quote':outcome}
                                           for i in range(len(fixture['frame']['success_criteria']))]
        responses=[fixture['frame'],fixture['routes']]
        compiled,trace,_=draft_outcome({'namespace':'browserfixture','outcome':outcome,'brief':case.summary},
                         lambda *_:(responses.pop(0),'controlled-fixture'),require_target_coverage=True)
        objects=GraphOutput(conditions=compiled.graph.conditions,actions=compiled.graph.actions,objectives=compiled.graph.objectives)
        proposal=Proposal(case_id=case.id,base_revision=0,provider='fixture',model='controlled-fixture',purpose='graph',
                         items=graph_items(case,objects,[],'browserfixture'),raw_output=trace,output_hash='fixture-only',latency_ms=0)
        store.save_proposal(proposal)
        env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN,'HF_TOKEN':'','EIGHTBALL_HF_MODEL':'','EIGHTBALL_HF_PROVIDER':''}
        process=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(60):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',timeout=1,trust_env=False).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            else:raise RuntimeError('Local server unavailable')
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1512,'height':1050});page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                try:
                    open_document(page,db)
                    page.locator('[name=token]').fill(TOKEN)
                    page.locator('form[data-form=login] [type=submit]').click()
                    page.locator('[data-case="'+case.id+'"]').click()
                    expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                    check('black canvas uses approved token',page.evaluate('getComputedStyle(document.body).backgroundColor')=='rgb(8, 9, 11)')
                    check('ENDSTATE identity present','POWERED BY ENDSTATE' in page.locator('.sidebar').inner_text())
                    page.locator('nav [data-tab=review]').click()
                    expect(page.locator('nav [data-tab=review]')).to_have_attribute('aria-current','page')
                    expect(page.locator('.target-review')).to_be_visible()
                    check('exact target and proposed criterion displayed for review',outcome in page.locator('.target-review').inner_text())
                    check('target coverage is not represented as semantic proof','not that the model understood it correctly' in page.locator('.target-review').inner_text())
                    page.screenshot(path=str(OUT/'8BALL-Black-Target-Review.png'),full_page=True)
                    page.locator('nav [data-tab=models]').click()
                    expect(page.locator('nav [data-tab=models]')).to_have_attribute('aria-current','page')
                    hf=page.locator('.provider-card').filter(has=page.get_by_role('heading',name='Hugging Face',exact=True))
                    check('absent hosted credentials are accurately shown','Not configured' in hf.inner_text())
                    check('hosted setup does not imply paid calls','Disabled' in hf.inner_text())
                    page.locator('[data-action=hosted-setup]').click()
                    expect(page.get_by_role('heading',name='Hugging Face setup')).to_be_visible()
                    check('setup never requests a browser-stored API key',page.locator('.dialog input').count()==0)
                    page.keyboard.press('Escape')
                    expect(page.locator('.dialog')).to_have_count(0)
                    check('dialog Escape restores control focus',page.locator('[data-action=hosted-setup]').evaluate('(e)=>document.activeElement===e'))
                    page.locator('[data-action=check-runtime]').click()
                    expect(page.locator('.provider-card').filter(has=page.get_by_role('heading',name='Ollama',exact=True)).locator('.meta .badge')).not_to_contain_text('Not checked',timeout=10000)
                    check('runtime probe gives explicit checked result','may be stopped or not installed' in page.locator('main').inner_text() or 'listed locally' in page.locator('main').inner_text() or 'not listed' in page.locator('main').inner_text())
                    expect(page.locator('#toast')).not_to_be_visible(timeout=8000)
                    page.screenshot(path=str(OUT/'8BALL-Black-Intelligence.png'),full_page=True)
                    for width in (1512,390):
                        page.set_viewport_size({'width':width,'height':1050 if width==1512 else 844})
                        check(f'provider controls fit {width}px',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                        expect(page.locator('.topbar [data-action=logout]')).to_be_visible()
                        check(f'workspace lock visible at {width}px',True)
                    page.screenshot(path=str(OUT/'8BALL-Black-Intelligence-Mobile.png'),full_page=True)
                    page.locator('.topbar [data-action=logout]').click()
                    expect(page.locator('form[data-form=login]')).to_be_visible()
                    check('mobile lock clears the active workspace',page.locator('nav').count()==0)
                    check('no page runtime errors',not errors)
                finally:
                    browser.close()
        finally:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill()
    report={'checks_passed':len(checks),'checks':checks,'network':'ASGI bridge' if BRIDGE else 'native loopback HTTP',
            'real_huggingface_inference':False,'proposal_source':'controlled fictional compiler fixture',
            'local_probe_only':True,'live_state_not_attested':True}
    (OUT/'development-browser-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
