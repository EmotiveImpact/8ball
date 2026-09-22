"""Chromium/API/SQLite journeys. Offline bridge mode does not verify browser HTTP.
Run: python tests/browser_smoke.py. Requires Chromium or playwright install chromium.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import httpx
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
BRIDGE=os.getenv('EIGHTBALL_BROWSER_BRIDGE')=='1'
TOKEN='browser-fixture-token-not-for-real-use-12345'
OUT=Path(os.environ.get('EIGHTBALL_ARTIFACTS',ROOT/'artifacts'))
OUT.mkdir(parents=True,exist_ok=True)
checks=[]


def check(name,condition):
    assert condition,name
    checks.append(name)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        env={**os.environ,'EIGHTBALL_DB':str(Path(tmp)/'browser.sqlite3'),'EIGHTBALL_TOKEN':TOKEN,'PYTHONUNBUFFERED':'1'}
        process=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        try:
            for _ in range(60):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',timeout=1,trust_env=False).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            else:raise RuntimeError('Local test server did not start')
            with sync_playwright() as p:
                executable=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium')
                browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1512,'height':1050},device_scale_factor=1)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                if BRIDGE:
                    # Offline document rendering, respecting this environment's browser URL block.
                    # Requests reach the real FastAPI app in process, not browser HTTP.
                    from fastapi.testclient import TestClient
                    from eightball.api import make_app
                    from eightball.store import Store
                    api_client=TestClient(make_app(Store(env['EIGHTBALL_DB']),TOKEN))
                    def bridge(path,init):
                        r=api_client.request(init.get('method','GET'),path,headers=init.get('headers',{}),content=init.get('body'))
                        return {'body':r.text,'status':r.status_code}
                    page.expose_function('__eightball_request',bridge)
                    page.set_content('<!doctype html><html lang="en-GB"><head></head><body><div id="app"></div><div id="toast" role="status"></div><div id="modal-root"></div></body></html>')
                    page.add_style_tag(content=(ROOT/'web/style.css').read_text())
                    page.evaluate("() => {window.fetch=async (path,init={})=>{const r=await window.__eightball_request(path,init);return new Response(r.body,{status:r.status})};}")
                    page.add_script_tag(content=(ROOT/'web/app.js').read_text(),type='module')
                else:
                    page.goto('http://127.0.0.1:8048')
                page.locator('[name=token]').fill(TOKEN)
                page.get_by_role('button',name='Open workspace').click()
                page.get_by_role('button',name='Open fictional case').click()
                page.get_by_role('heading',name='Northstar account recovery').wait_for()
                check('fictional case opens against real API'+(' through ASGI bridge' if BRIDGE else ' over HTTP'),True)
                page.screenshot(path=str(OUT/'8BALL-Situation-Room.png'),full_page=True)
                for width in [1512,390]:
                    page.set_viewport_size({'width':width,'height':1050 if width==1512 else 844})
                    for tab in ['command','room','graph','routes','evidence','actions','audit','client']:
                        page.locator(f'nav [data-tab="{tab}"]').click()
                        check(f'{tab} fits viewport {width}',page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1'))
                    if width==390:
                        page.locator('nav [data-tab="room"]').click()
                        page.screenshot(path=str(OUT/'8BALL-Mobile.png'),full_page=True)
                page.set_viewport_size({'width':1512,'height':1050})
                page.locator('nav [data-tab="evidence"]').click()
                page.locator('[data-act="add-evidence"]').first.click()
                page.locator('#evidence-form [name=title]').fill('Incident preservation log')
                page.locator('#evidence-form [name=source]').fill('Fictional case lead')
                text='Incident records preserved. <script>window.attacked = true</script>'
                page.locator('#evidence-form [name=text]').fill(text)
                page.locator('#evidence-form [type=submit]').click()
                page.get_by_role('heading',name='Incident preservation log').wait_for()
                check('evidence text renders without executing markup',page.evaluate('window.attacked === undefined'))
                page.locator('[data-act="review-source"]').first.click()
                page.locator('[data-act="confirm-source"]').click()
                page.locator('[data-act="observe"]').first.wait_for()
                page.locator('[data-act="observe"]').first.click()
                page.locator('#observe-form [name=condition_id]').select_option('records')
                page.locator('#observe-form [name=evidence_id]').select_option(index=1)
                page.locator('#observe-form [name=rationale]').fill('The preservation log was checked by the case lead.')
                page.locator('#observe-form [type=submit]').click()
                page.locator('.modal').wait_for(state='detached')
                page.locator('nav [data-tab="actions"]').click()
                row=page.locator('.row').filter(has=page.get_by_role('heading',name='Establish the root cause',exact=True))
                check('verified condition unlocks downstream work',row.locator('.pill').inner_text()=='Ready')
                page.locator('[data-act="approve"][data-id="listen"]').click()
                page.locator('[data-act="confirm-action"]').click()
                page.locator('[data-act="complete"][data-id="listen"]').wait_for()
                check('approval unlocks eligible external-contact record',True)
                page.locator('[data-act="complete"][data-id="listen"]').click()
                page.locator('[data-act="confirm-action"]').click()
                page.locator('.modal').wait_for(state='detached')
                check('completion does not verify outcome','intended result still unverified' in page.locator('main').inner_text())
                if not BRIDGE:
                    page.reload()
                else:
                    # about:blank has no origin storage. Do not pretend to test native persistence.
                    page.locator('nav [data-tab="command"]').click()
                page.locator('[data-open-case]').first.click()
                page.get_by_role('heading',name='Northstar account recovery').wait_for()
                check('reopening case preserves server state' if BRIDGE else 'native session token and server state survive reload',page.locator('[data-condition="records"]').count()==1)
                page.locator('[data-act="simulate"]').click()
                page.locator('#scenario-form [name=budget]').fill('1')
                page.locator('#scenario-form [type=submit]').click()
                page.get_by_role('heading',name='Scenario comparison').wait_for()
                check('sandbox compares changed constraints','3 constraint failures' in page.locator('.modal').inner_text())
                page.locator('[data-act="close"]').click()
                page.locator('nav [data-tab="audit"]').click()
                page.locator('[data-act="audit-load"]').click()
                page.get_by_text('Hash chain and latest snapshot verified.',exact=False).wait_for()
                check('browser verifies real audit chain',True)
                if not BRIDGE:
                    with page.expect_download() as d:
                        page.locator('[data-act="export"]').click()
                    exported=json.loads(Path(d.value.path()).read_text())
                else:
                    # Verify generated export payload, not a native browser download.
                    page.evaluate("() => {window.URL.createObjectURL = b => {window.__lastExport=b.text(); return 'blob:offline-test'}; HTMLAnchorElement.prototype.click=function(){};}")
                    page.locator('[data-act="export"]').click()
                    page.wait_for_function('window.__lastExport !== undefined')
                    exported=json.loads(page.evaluate('window.__lastExport'))
                check('export payload contains actual case JSON and audit' if BRIDGE else 'download is actual case JSON with audit',exported['valid'] and len(exported['events'])==6)
                check('sandbox left no persistent event',all(e['kind']!='simulate' for e in exported['events']))
                page.locator('nav [data-tab="graph"]').click()
                page.screenshot(path=str(OUT/'8BALL-Outcome-Graph.png'),full_page=True)
                page.locator('nav [data-tab="routes"]').click()
                page.screenshot(path=str(OUT/'8BALL-Routes.png'),full_page=True)
                check('no browser runtime errors',not errors)
                browser.close()
        finally:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill()
    report={'checks_passed':len(checks),'checks':checks,'browser':'real Chromium','persistence':'real SQLite; native sessionStorage NOT tested' if BRIDGE else 'real SQLite and native sessionStorage','network':'in-process ASGI bridge; browser HTTP, CSP and downloads NOT tested' if BRIDGE else 'real loopback HTTP','model_inference_tested':False}
    (OUT/'browser-report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
