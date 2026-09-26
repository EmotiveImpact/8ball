"""Case explorer acceptance checks on actual browser code and SQLite state.
Default uses native HTTP; the optional bridge is explicitly labelled and is not
proof of native CSP, browser networking, session storage or downloaded exports.
No inference requests and no source-to-plan quality claims.
"""
from pathlib import Path
from datetime import timedelta
import json,os,shutil,subprocess,sys,tempfile,time
import httpx
from playwright.sync_api import sync_playwright,expect

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from browser_v2 import open_document,BRIDGE,TOKEN
from eightball.v2.store import Store
from eightball.v2.contracts import Case,Actor,utcnow
from eightball.v2.playbooks import demo_case

OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/graph')))
OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name)

def main():
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'graph.sqlite3');store=Store(db)
        case=store.create(demo_case(),fixture=True)
        second=store.create(Case(title='Separate fictional case',client='Test only',summary='No graph yet.',desired_outcome='A different goal',deadline=utcnow()+timedelta(days=1)))
        unsafe=store.create(Case(title='Escaping fixture',client='Test only',summary='Untrusted text fixture.',desired_outcome='No script execution',deadline=utcnow()+timedelta(days=1),actors=[Actor(id='markup',name='<img src=x onerror="window.graphAttack=1">')]))
        historical=demo_case();historical.title='Historical source fixture';historical.evidence[0].status='retracted';historycase=store.create(historical,fixture=True)
        before=store.audit(case.id)
        proc=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(80):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',trust_env=False,timeout=1).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            else:raise RuntimeError('Test server did not start')
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1600,'height':1160},device_scale_factor=1,reduced_motion='reduce')
                page.set_default_timeout(12000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                try:
                    open_document(page,db)
                    page.locator('[name=token]').fill(TOKEN);page.locator('form[data-form=login] [type=submit]').click()
                    page.locator(f'[data-case="{case.id}"]').click()
                    page.locator('nav [data-tab=map]').click();expect(page.locator('.gx-svg')).to_be_visible()
                    all_count=page.locator('.gx-node').count()
                    check('whole graph contains real case records',all_count==38)
                    check('black canvas uses approved token',page.evaluate('getComputedStyle(document.body).backgroundColor')=='rgb(8, 9, 11)')
                    check('snapshot revision clearly labelled','REV 0' in page.locator('.gx-revision').inner_text())
                    check('records have keyboard button semantics',page.locator('.gx-node[role=button][tabindex="0"]').count()==all_count)
                    check('view-only boundary visible','Layout and filters do not change evidence' in page.locator('.gx-integrity').inner_text())
                    page.mouse.move(10,10)
                    page.screenshot(path=str(OUT/'8BALL-Connections-Whole-Case.png'),full_page=True)
                    coo=page.locator('[data-gx-key="actor:coo"]');coo.focus();page.keyboard.press('Enter')
                    expect(page.locator('.gx-inspector h2')).to_have_text('Customer COO')
                    check('keyboard selection opens source-aware inspector','authority must be confirmed' in page.locator('.gx-inspector').inner_text())
                    check('selected node and immediate connections highlighted',page.locator('.gx-node.selected').count()==1 and page.locator('.gx-link.highlighted').count()>0)
                    page.locator('[data-gx-focus]').click()
                    local_count=page.locator('.gx-node').count();check('local graph narrows to declared neighbours',0<local_count<all_count)
                    page.locator('[data-gx-depth]').select_option('2');check('two-hop neighbourhood expands',page.locator('.gx-node').count()>local_count)
                    page.mouse.move(10,10);page.screenshot(path=str(OUT/'8BALL-Connections-Focus.png'),full_page=True)
                    page.locator('[data-gx-depth]').select_option('1')
                    vb=page.locator('.gx-svg').get_attribute('viewBox');page.locator('[data-gx-zoom=in]').click()
                    check('zoom changes camera only',page.locator('.gx-svg').get_attribute('viewBox')!=vb)
                    page.locator('.gx-svg').focus();page.keyboard.press('Home');check('Home fits graph',page.locator('.gx-svg').get_attribute('viewBox')==vb)
                    page.locator('.gx-svg').focus();page.keyboard.press('ArrowRight');check('keyboard pans graph',page.locator('.gx-svg').get_attribute('viewBox')!=vb)
                    page.locator('[data-gx-fit]').click()
                    node=page.locator('[data-gx-key="actor:coo"]');box=node.locator('.gx-node-core').bounding_box();assert box
                    start_transform=node.get_attribute('transform');page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();page.mouse.move(box['x']+60,box['y']+35,steps=6);page.mouse.up()
                    expect(page.locator('[data-gx-key="actor:coo"]')).to_have_class(__import__('re').compile('.*pinned.*'))
                    check('drag pins a visual coordinate',page.locator('[data-gx-key="actor:coo"]').get_attribute('transform')!=start_transform)
                    page.locator('[data-gx-pin]').click();check('unpin is explicit',page.locator('[data-gx-key="actor:coo"].pinned').count()==0)
                    page.locator('[data-gx-all]').first.click();check('reset restores whole case',page.locator('.gx-node').count()==all_count)
                    page.locator('[data-gx-clear]').click()
                    page.locator('[data-gx-kind=actor]').click();check('record-type filter excludes actors',page.locator('.gx-node.actor').count()==0)
                    page.locator('[data-gx-kind=actor]').click()
                    page.locator('[data-gx-search]').fill('Customer COO');check('search filters by record label and provenance',set(page.locator('.gx-node').evaluate_all('(nodes)=>nodes.map(n=>n.dataset.gxKey)'))=={'actor:coo','evidence:e_customer'})
                    page.locator('[data-gx-search]').fill('no match whatsoever');expect(page.locator('.gx-no-results')).to_be_visible();check('empty filter state is useful','Reset the filters' in page.locator('.gx-no-results').inner_text())
                    page.locator('[data-gx-all]').first.click()
                    page.locator('[data-gx-mode=outcome]').click();check('directed view includes explicit arrows',page.locator('.gx-link[marker-end]').count()>0)
                    check('outcome flow excludes actor/source associations',page.locator('.gx-node.actor,.gx-node.evidence').count()==0)
                    mediated=page.locator('[data-gx-key="action:mediated"]');mediated.focus();page.keyboard.press('Enter')
                    check('inspector preserves OR prerequisite logic',' OR ' in page.locator('.gx-inspector').inner_text())
                    page.locator('[data-gx-key="condition:retained"] .gx-node-core').click()
                    check('directed nodes work with pointer selection',page.locator('.gx-inspector h2').inner_text()=='Continuation agreement accepted')
                    mediated.focus();page.keyboard.press('Enter')
                    page.mouse.move(10,10);page.screenshot(path=str(OUT/'8BALL-Connections-Outcome-Flow.png'),full_page=True)
                    page.locator('[data-gx-mode=list]').click();check('records list is a full alternative to canvas',page.locator('.gx-record-list [data-gx-select]').count()==all_count)
                    page.locator('.gx-record-list [data-gx-select="condition:root"]').focus();page.keyboard.press('Enter')
                    check('record list keeps keyboard focus after selection',page.locator('.gx-record-list [data-gx-select="condition:root"]').evaluate('(e)=>document.activeElement===e'))
                    check('record list keyboard selection inspects the condition','Root cause verified' in page.locator('.gx-inspector h2').inner_text())
                    page.locator('.gx-open-record').click();expect(page.locator('.dialog')).to_be_visible()
                    check('existing full-record flow remains accessible','Confirmation criterion' in page.locator('.dialog').inner_text());page.keyboard.press('Escape')
                    # No graph interaction may create a command, change a revision or mutate an audit.
                    check('all graph interactions leave case audit unchanged',store.audit(case.id)==before)
                    page.locator('[data-gx-mode=network]').click();page.locator('[data-gx-clear]').click()
                    # Return to the room to show graph remains an addition, not a new app.
                    page.locator('nav [data-tab=room]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                    page.mouse.move(10,10);page.screenshot(path=str(OUT/'8BALL-Connections-Operator-Room.png'),full_page=True)
                    check('structured operator room preserved',page.get_by_role('heading',name='Northstar account recovery').is_visible())
                    page.locator('nav [data-tab=command]').click();page.locator(f'[data-case="{second.id}"]').click();page.locator('nav [data-tab=map]').click()
                    expect(page.locator('.gx-no-results')).to_be_visible();check('separate case does not leak previous graph','Northstar' not in page.locator('.constellation').inner_text())
                    page.locator('nav [data-tab=command]').click();page.locator(f'[data-case="{unsafe.id}"]').click();page.locator('nav [data-tab=map]').click()
                    page.locator('[data-gx-key="actor:markup"]').focus();page.keyboard.press('Enter')
                    check('source-derived labels never execute HTML',page.evaluate('window.graphAttack === undefined') and page.locator('.constellation img').count()==0)
                    page.locator('nav [data-tab=command]').click();page.locator(f'[data-case="{case.id}"]').click();page.locator('nav [data-tab=map]').click()
                    page.locator('nav [data-tab=command]').click();page.locator(f'[data-case="{historycase.id}"]').click();page.locator('nav [data-tab=map]').click()
                    check('historical evidence links are hidden by default',page.locator('.gx-link.historical').count()==0)
                    page.locator('[data-gx-history]').check();check('historical links can be inspected explicitly',page.locator('.gx-link.historical').count()>0)
                    page.locator('[data-gx-key="evidence:e_preserve"]').focus();page.keyboard.press('Enter')
                    check('retracted source remains labelled in inspector','Retracted' in page.locator('.gx-inspector').inner_text())
                    page.locator('nav [data-tab=command]').click();page.locator(f'[data-case="{case.id}"]').click();page.locator('nav [data-tab=map]').click()
                    # Mobile/touch and motion preferences. Layout positions stay fixed until explicitly changed.
                    page.set_viewport_size({'width':390,'height':844});page.locator('[data-gx-mode=list]').click()
                    check('mobile records view fits viewport',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
                    page.locator('.gx-record-list [data-gx-select="actor:coo"]').click()
                    page.mouse.move(1,1);page.screenshot(path=str(OUT/'8BALL-Connections-Mobile.png'),full_page=True)
                    page.locator('[data-gx-mode=network]').click();page.locator('[data-gx-focus]').click()
                    check('mobile local graph fits viewport',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
                    check('reduced motion has no perpetual simulation',page.evaluate("[...document.querySelectorAll('.constellation *')].every(e=>getComputedStyle(e).animationName==='none')"))
                    # In-memory graph choices must not survive workspace lock.
                    page.locator('.toptools [data-action=logout]').click();expect(page.locator('form[data-form=login]')).to_be_visible()
                    check('locking clears rendered case records',page.locator('.gx-node').count()==0 and 'Northstar' not in page.locator('body').inner_text())
                    check('no browser runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'ASGI bridge, not browser HTTP' if BRIDGE else 'Native loopback HTTP','actual_browser':'Chromium','real_sqlite':True,'input_data':'Fictional case fixtures','graph_interactions_mutated_case':False,'model_inference_tested':False,'errors':errors}
                    (OUT/'browser-graph-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'),full_page=True);(OUT/'failure.html').write_text(page.content());print('Page errors:',errors);raise
                finally:browser.close()
        finally:
            proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill()

if __name__=='__main__':main()
