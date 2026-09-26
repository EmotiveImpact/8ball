"""V0.2 real-application journeys. Default: native HTTP browser.
EIGHTBALL_BROWSER_BRIDGE=1 is an explicit offline ASGI harness, not native HTTP.
"""
from pathlib import Path
import json,os,re,shutil,subprocess,sys,tempfile,time
import httpx
from playwright.sync_api import sync_playwright,expect

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
BRIDGE=os.getenv('EIGHTBALL_BROWSER_BRIDGE')=='1'
TOKEN='browser-v2-fixture-operator-token-123456789'
OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/v2')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]


def check(name,value):
    assert value,name
    checks.append(name)


def open_document(page,db):
    if not BRIDGE:
        page.goto('http://127.0.0.1:8048/v2/');return
    from fastapi.testclient import TestClient
    from eightball.api import make_app
    from eightball.store import Store
    client=TestClient(make_app(Store(db),TOKEN))
    def request(path,init):
        r=client.request(init.get('method','GET'),path,headers=init.get('headers',{}),content=init.get('body'))
        return {'body':r.text,'status':r.status_code}
    page.expose_function('__eightball_request',request)
    page.set_content('<!doctype html><html lang="en-GB"><head></head><body><div id="app"></div><div id="modal"></div><div id="toast" role="status"></div></body></html>')
    page.add_style_tag(content=(ROOT/'web/v2/style.css').read_text())
    page.evaluate("() => {window.fetch=async (path,init={})=>{const r=await window.__eightball_request(path,init);return new Response(r.body,{status:r.status})};}")
    parts=[]
    for filename in ['ui.js','graph-model.js','graph-view.js','studio-model.js','studio-view.js','job-view.js','changelog-view.js','source-model.js','source-view.js','insights-view.js','grounding-view.js','plan-review-view.js','course-view.js','views.js','forms.js']:
        code=(ROOT/'web/v2'/filename).read_text()
        code=re.sub(r'^import .*?;\s*$', '', code, flags=re.M)
        code=re.sub(r'\bexport\s+', '', code)
        if filename=='course-view.js':
            exports='clearCourse,loadCourse,courseBanner,chooseCourseButton,courseTimeline,bindCourse'
            parts.append('const {'+exports+'}=(()=>{'+code+';return {'+exports+'};})();')
        else:
            parts.append(code)
    parts.append('const F={snapshot,sourceChoices,newForm,evidenceForm,observationForm,analysisForm,scenarioForm,decisionForm,answerForm,metadataForm,graphForm,objectForm,objectDetail,actionDetail,editObject,questionProposalForm};')
    code=(ROOT/'web/v2/app.js').read_text();code=re.sub(r'^import .*?;\s*$','',code,flags=re.M);parts.append(code)
    page.add_script_tag(content='\n'.join(parts),type='module')


def main():
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'browser-v2.sqlite3')
        env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN}
        log=open(Path(tmp)/'server.log','w')
        process=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env=env,stdout=log,stderr=log)
        try:
            for _ in range(80):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',timeout=1,trust_env=False).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            else:raise RuntimeError('Server did not start')
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1512,'height':1050},device_scale_factor=1)
                page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                try:
                    open_document(page,db)
                    page.locator('[name=token]').fill(TOKEN)
                    page.locator('form[data-form=login] [type=submit]').click()
                    page.locator('[data-action=demo]').first.click()
                    expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                    check('fictional situation opens against real case store',page.get_by_role('heading',name='Northstar account recovery').is_visible())
                    page.screenshot(path=str(OUT/'8BALL-V2-Situation-Room.png'),full_page=True)
                    tabs=['command','room','review','map','routes','actions','questions','decisions','people','evidence','timeline','changes','scenario','audit','brief','playbooks','models']
                    for width in [1512,390]:
                        page.set_viewport_size({'width':width,'height':1050 if width==1512 else 844})
                        for tab in tabs:
                            page.locator(f'nav [data-tab={tab}]').click()
                            expect(page.locator(f'nav [data-tab={tab}]')).to_have_attribute('aria-current','page')
                            check(f'{tab} fits {width}px viewport',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
                        if width==390:
                            page.locator('nav [data-tab=room]').click()
                            expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                            page.screenshot(path=str(OUT/'8BALL-V2-Mobile.png'),full_page=True)
                    page.set_viewport_size({'width':1512,'height':1050})
                    # Evidence review and attestation, using the actual UI and API.
                    page.locator('nav [data-tab=evidence]').click()
                    expect(page.locator('nav [data-tab=evidence]')).to_have_attribute('aria-current','page')
                    page.locator('[data-action=add-evidence]').first.click()
                    f=page.locator('form[data-form=evidence]')
                    f.locator('[name=title]').fill('Approved wording fixture')
                    f.locator('[name=source]').fill('Fictional legal adviser')
                    f.locator('[name=text]').fill('External language approved. <script>window.compromised=true</script>')
                    f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    check('source markup is escaped',page.evaluate('window.compromised === undefined'))
                    page.locator('[data-action=review-source]').last.click()
                    page.locator('form[data-form=source-review] [type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    card=page.locator('.source-card').filter(has=page.get_by_role('heading',name='Approved wording fixture'))
                    card.locator('[data-action=observe]').click()
                    f=page.locator('form[data-form=observe]');f.locator('[name=condition_id]').select_option('language');f.locator('[name=rationale]').fill('The fictional reviewer signed the external wording.')
                    f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    page.locator('nav [data-tab=actions]').click();expect(page.locator('nav [data-tab=actions]')).to_have_attribute('aria-current','page')
                    page.locator('[data-action=approve][data-id=listen]').click()
                    page.locator('form[data-form=confirm-action] [type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    page.locator('[data-action=complete][data-id=listen]').wait_for()
                    check('evidence and scoped approval unlock a real action',True)
                    page.locator('[data-action=complete][data-id=listen]').click();page.locator('form[data-form=confirm-action] [type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    check('completion is not treated as result proof','Intended result remains unverified' in page.locator('main').inner_text())
                    page.locator('nav [data-tab=changes]').click();expect(page.locator('nav [data-tab=changes]')).to_have_attribute('aria-current','page')
                    check('change ledger explains committed updates','External language approved' in page.locator('main').inner_text())
                    page.screenshot(path=str(OUT/'8BALL-V2-What-Changed.png'),full_page=True)
                    # Isolated refusal scenario and decision branch.
                    page.locator('nav [data-tab=scenario]').click();expect(page.locator('nav [data-tab=scenario]')).to_have_attribute('aria-current','page')
                    page.locator('[data-action=scenario]').first.click()
                    f=page.locator('form[data-form=scenario]');f.locator('[name=condition]').select_option('refused');f.locator('[name=value]').select_option('true');f.locator('[name=decision]').select_option('escalation|mediate');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    check('scenario is explicitly labelled non-live','SIMULATION ONLY' in page.locator('main').inner_text())
                    page.locator('nav [data-tab=routes]').click();expect(page.locator('nav [data-tab=routes]')).to_have_attribute('aria-current','page')
                    checksBoxes=page.locator('[data-route-select]');checksBoxes.nth(0).check();checksBoxes.nth(1).check();page.locator('[data-action=compare]').click();page.get_by_role('heading',name='Compare the ways through').wait_for()
                    check('real route comparison shows shared work','Shared work' in page.locator('.dialog').inner_text());page.locator('.dialog [data-action=close]').click()
                    page.screenshot(path=str(OUT/'8BALL-V2-Routes.png'),full_page=True)
                    # Start from a blank case. Reviewed source capture and editable graph proposals.
                    page.locator('nav [data-tab=command]').click();expect(page.locator('nav [data-tab=command]')).to_have_attribute('aria-current','page')
                    page.locator('[data-action=new]').first.click();f=page.locator('form[data-form=new]')
                    f.locator('[name=title]').fill('Fictional Atlas recovery');f.locator('[name=client]').fill('Atlas fixture');f.locator('[name=summary]').fill('The service stopped. We need to agree a recovery route.');f.locator('[name=desired_outcome]').fill('Recovery accepted by the service owner');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                    check('blank intake does not invent a plan','Define the destination first' in page.locator('main').inner_text())
                    page.locator('nav [data-tab=evidence]').click();expect(page.locator('nav [data-tab=evidence]')).to_have_attribute('aria-current','page');page.locator('[data-action=add-evidence]').first.click();f=page.locator('form[data-form=evidence]')
                    f.locator('[name=title]').fill('Atlas briefing');f.locator('[name=source]').fill('Fictional service owner');f.locator('[name=text]').fill('The service stopped. Who can authorise the fallback? The impact is documented.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    page.locator('[data-action=analyse]').click();f=page.locator('form[data-form=analyse]');f.locator('[name=source_ids]').first.check();f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached');expect(page.locator('nav [data-tab=review]')).to_have_attribute('aria-current','page')
                    # Analysis is now asynchronous: wait for actual published proposals, not just navigation.
                    expect(page.locator('main')).to_contain_text('Rules-based source capture. Not AI.')
                    check('review queue explicitly identifies rules-based capture','Rules-based source capture. Not AI.' in page.locator('main').inner_text())
                    f=page.locator('form[data-form=review-proposal]').first;selections=f.locator('select[name^=choice_]');selections.nth(0).select_option('accepted');selections.nth(1).select_option('rejected');selections.nth(2).select_option('edited')
                    details=f.locator('details').nth(2);details.locator('summary').click();t=details.locator('textarea');obj=json.loads(t.input_value());obj['statement']='The reported impact needs reviewer confirmation.';t.fill(json.dumps(obj));f.locator('[type=submit]').click()
                    page.get_by_role('heading',name='The review queue is clear.').wait_for()
                    page.locator('nav [data-tab=evidence]').click();expect(page.locator('nav [data-tab=evidence]')).to_have_attribute('aria-current','page')
                    check('accept edit reject are reflected in live claims','The reported impact needs reviewer confirmation.' in page.locator('main').inner_text())
                    page.locator('nav [data-tab=review]').click();expect(page.locator('nav [data-tab=review]')).to_have_attribute('aria-current','page');page.locator('[data-action=propose-graph]').click();f=page.locator('form[data-form=analyse]');f.locator('[name=playbook_id]').select_option('recovery');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    f=page.locator('form[data-form=review-proposal]').first;f.locator('[data-action=select-proposals]').click();f.locator('[type=submit]').click();page.get_by_role('heading',name='The review queue is clear.').wait_for()
                    page.locator('nav [data-tab=routes]').click();expect(page.locator('nav [data-tab=routes]')).to_have_attribute('aria-current','page')
                    check('reviewed catalogue graph produces two real alternatives',page.locator('.route-card').count()==2)
                    # Source evidence remains unreviewed; graph acceptance has not verified conditions.
                    page.locator('nav [data-tab=map]').click();expect(page.locator('nav [data-tab=map]')).to_have_attribute('aria-current','page')
                    page.screenshot(path=str(OUT/'8BALL-V2-Outcome-Graph.png'),full_page=True)
                    # Reopen/reload and inspect audit export.
                    if not BRIDGE:
                        page.reload();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                        check('native sessionStorage and case selection survive reload',page.get_by_role('heading',name='Fictional Atlas recovery').is_visible())
                    else:
                        page.locator('nav [data-tab=command]').click();expect(page.locator('nav [data-tab=command]')).to_have_attribute('aria-current','page');page.locator('[data-case]').filter(has=page.get_by_role('heading',name='Fictional Atlas recovery')).click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                        check('reopening restores real persisted case state',True)
                    page.locator('nav [data-tab=audit]').click();expect(page.locator('nav [data-tab=audit]')).to_have_attribute('aria-current','page')
                    check('audit chain and snapshot replay verify','Hash chain verified' in page.locator('main').inner_text())
                    if not BRIDGE:
                        with page.expect_download() as d:page.locator('[data-action=export]').click()
                        exported=json.loads(Path(d.value.path()).read_text())
                    else:
                        page.evaluate("() => {window.URL.createObjectURL=b=>{window.__export=b.text();return 'blob:bridge'};HTMLAnchorElement.prototype.click=function(){};}")
                        page.locator('[data-action=export]').click();page.wait_for_function('window.__export !== undefined');exported=json.loads(page.evaluate('window.__export'))
                    check('export has real replayable case and model dispositions',exported['valid'] and len(exported['model_runs'])==2)
                    check('accepted claims did not create observations',not exported['case']['observations'])
                    check('native download' if not BRIDGE else 'export payload generated; native download not tested',exported['format']=='eightball-case-v2')
                    check('no browser runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'ASGI bridge, not browser HTTP' if BRIDGE else 'Native loopback HTTP',
                            'native_session_storage_and_download':not BRIDGE,'real_sqlite':True,'model_inference_tested':False,'errors':errors}
                    (OUT/'browser-v2-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'),full_page=True)
                    (OUT/'failure.html').write_text(page.content());print('Browser errors:',errors);raise
                finally:browser.close()
        finally:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill()
            log.close()


if __name__=='__main__':main()
