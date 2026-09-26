"""Guided Plan Studio, job cancellation and changelog operator journeys.

Native HTTP by default. The explicit ASGI bridge does NOT test native browser
HTTP/storage. A disposable loopback provider stub tests cancellation only; it is
NOT Qwen, a live hosted model, or model-quality evidence.
"""
from pathlib import Path
from datetime import timedelta
from threading import Event, Thread
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os,json,subprocess,sys,tempfile,time,shutil
import httpx
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from browser_v2 import open_document, BRIDGE, TOKEN
from eightball.v2 import VERSION
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Case
from eightball.v2.commands import Command
from eightball.models import uid,utcnow
OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/studio')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name)


def main():
    entered,release=Event(),Event()
    class FakeModel(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_POST(self):
            # Test-only HTTP double at the normal local-model address.
            body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            context=json.loads(body['messages'][-1]['content']);source=context['sources'][0]
            entered.set();release.wait(15)
            content={'items':[{'kind':'claim','text':source['text'][:180],'source':{'evidence_id':source['id'],'quote':source['text']}}]}
            out=json.dumps({'model':'controlled-local-test-double','done':True,'message':{'content':json.dumps(content)}}).encode()
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(out)));self.end_headers()
            try:self.wfile.write(out)
            except (BrokenPipeError,ConnectionResetError):pass
    server=ThreadingHTTPServer(('127.0.0.1',11434),FakeModel)
    stub=Thread(target=server.serve_forever,daemon=True);stub.start()
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'cases.db');store=Store(db);c=store.create(demo_case(),fixture=True)
        other=store.create(Case(title='Another fictional case',client='Test',summary='Empty fixture',desired_outcome='Another target',deadline=utcnow()+timedelta(days=1)))
        before=store.audit(c.id)
        proc=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(60):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',trust_env=False,timeout=1).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            else:raise RuntimeError('Local app did not start')
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1600,'height':1100},reduced_motion='reduce');page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                def nav(tab):
                    page.locator(f'nav [data-tab={tab}]').click();expect(page.locator(f'nav [data-tab={tab}]')).to_have_attribute('aria-current','page')
                def select(kind,id):
                    page.locator(f'[data-studio=select][data-kind={kind}][data-id={id}]').click()
                def field(path):return page.locator(f'[data-studio-field="{path}"]')
                def set_text(path,value):field(path).fill(value);field(path).press('Tab')
                def act(action):page.locator(f'[data-studio={action}]').first.click()
                try:
                    open_document(page,db);page.locator('[name=token]').fill(TOKEN);page.locator('form[data-form=login] [type=submit]').click();page.locator(f'[data-case="{c.id}"]').click()
                    nav('studio');expect(page.get_by_role('heading',name='Engineer the route.')).to_be_visible()
                    check('draft starts at explicit live revision','Based on case revision 0' in page.locator('.st-statusbar').inner_text())
                    check('no commit before preview',page.locator('[data-studio=commit]').is_disabled())
                    select('conditions','records');check('observed meaning cannot be edited',field('title').is_disabled() and field('confirmation').is_disabled())
                    select('actions','mediated')
                    check('existing nested AND OR expression preserved',page.locator('[data-studio-field="requires.args.3.op"]').input_value()=='any')
                    # Edit cost while preserving mouse/keyboard intent.
                    set_text('cost','1900');check('editing stays draft',store.audit(c.id)==before)
                    act('undo');check('undo restores original value',field('cost').input_value()=='2200')
                    act('redo');check('redo restores amendment',field('cost').input_value()=='1900')
                    # Nested negative literal inside an existing alternative.
                    field('requires.args.3.args.1.value').select_option('false')
                    check('negative prerequisite is explicit',field('requires.args.3.args.1.value').input_value()=='false')
                    # Return to truthful source recipe rather than keeping a gratuitous test edit.
                    act('undo')
                    act('preview');expect(page.locator('.st-preview-metrics')).to_be_visible()
                    check('preview computes real draft routes',page.locator('.st-draft-route').count()>1)
                    check('preview does not write any live event',store.audit(c.id)==before)
                    check('preview names exact changed field','cost' in page.locator('.st-impact-body').inner_text())
                    expect(page.locator('[data-studio=commit]')).to_be_enabled()
                    page.mouse.move(3,3);page.screenshot(path=str(OUT/'8BALL-Plan-Studio.png'),full_page=False)
                    field('requires.args.3.op').scroll_into_view_if_needed()
                    page.screenshot(path=str(OUT/'8BALL-Plan-Studio-Rules.png'),full_page=False)
                    # Edits invalidate the previous preview.
                    set_text('cost','1850');check('editing invalidates preview approval',page.locator('[data-studio=commit]').is_disabled())
                    # Guard and contingency are authored without JSON.
                    select('actions','staged');page.locator('.st-section>summary').filter(has_text='Restrictions / guard').click()
                    check('existing false guard retained',field('guard.value').input_value()=='false')
                    field('guard.value').focus();page.keyboard.press('Tab');check('keyboard can leave guard control',page.evaluate('document.activeElement !== document.body'))
                    select('actions','pause');page.locator('.st-section>summary').filter(has_text='Contingencies').click()
                    check('all three existing response branches shown',page.locator('.st-contingency').count()==3)
                    set_text('contingencies.1.response','Review professional mediation with the case lead')
                    check('contingency edit preserves expanded section',field('contingencies.1.response').is_visible())
                    page.screenshot(path=str(OUT/'8BALL-Plan-Contingencies.png'),full_page=True)
                    act('preview');expect(page.locator('.st-preview-metrics')).to_be_visible()
                    act('commit');expect(page.get_by_role('heading',name='Commit this plan amendment?')).to_be_visible()
                    check('commit requires separate confirmation',store.get(c.id).revision==0)
                    page.locator('.dialog [data-studio=commit-confirm]').click();page.locator('.dialog').wait_for(state='detached')
                    check('one explicit amendment creates one case revision',store.get(c.id).revision==1)
                    updated=store.get(c.id)
                    check('commit preserves all original observations',updated.observations==c.observations)
                    check('commit updates requested cost',next(a.cost for a in updated.graph.actions if a.id=='mediated')==1850)
                    check('audit and replay remain valid',store.audit(c.id)['valid'])
                    # Empty or unknown rules fail preview rather than inventing structure.
                    select('actions','investigate');page.locator('[data-studio=add-group][data-path=requires]').click()
                    field('requires.args.1.op').select_option('any')
                    act('preview');expect(page.locator('#toast')).to_have_class(__import__('re').compile('.*error.*'))
                    check('invalid empty OR never enables commit',page.locator('[data-studio=commit]').is_disabled())
                    act('discard');page.locator('.dialog [data-studio=discard-confirm]').click();page.locator('.dialog').wait_for(state='detached')
                    check('discard never creates an event',store.get(c.id).revision==1)
                    # Local draft stays when navigating to read-only Connections.
                    select('actions','investigate');set_text('cost','1234');nav('map');expect(page.locator('.gx-svg')).to_be_visible();nav('studio');select('actions','investigate')
                    check('draft survives view navigation',field('cost').input_value()=='1234')
                    # Competing mutation from another operator view forces conflict.
                    store.change(c.id,Command(event_id=uid(),expected_revision=1,kind='metadata',payload={'budget':6100}))
                    act('preview');expect(page.locator('#toast')).to_contain_text('older case revision')
                    check('stale draft cannot overwrite case',store.get(c.id).budget==6100 and store.get(c.id).revision==2)
                    # Switching case explicitly discards rather than silently leaking the draft.
                    nav('command');page.locator(f'[data-case="{other.id}"]').click();expect(page.get_by_role('heading',name='Leave this plan draft?')).to_be_visible()
                    check('switching case warns about uncommitted draft',True)
                    page.locator('.dialog [data-action=discard-open-case]').click();page.locator('.dialog').wait_for(state='detached');nav('studio')
                    check('draft is isolated to newly selected case','Another target' in page.locator('.st-welcome').inner_text() and page.locator('.st-object').count()==0)
                    # Reopen primary case for explicit controlled analysis cancellation.
                    nav('command');page.locator(f'[data-case="{c.id}"]').click();nav('review');page.locator('[data-action=analyse]').first.click();f=page.locator('form[data-form=analyse]')
                    f.locator('[name=provider]').select_option('ollama');f.locator('[name=source_ids]').first.check();f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    assert entered.wait(5)
                    expect(page.locator('.analysis-job').first).to_contain_text('Waiting for a provider response')
                    check('analysis returns browser control while provider is running',page.locator('[data-action=cancel-analysis]').is_visible())
                    page.screenshot(path=str(OUT/'8BALL-Analysis-Monitor.png'),full_page=True)
                    page.locator('[data-action=cancel-analysis]').first.click();expect(page.locator('.analysis-job').first).to_contain_text('Cancelled')
                    check('cancel explains in-flight provider limitation','may still complete or be billed' in page.locator('.analysis-job').first.inner_text())
                    release.set()
                    expect(page.locator('.analysis-job').first).not_to_contain_text('draining',timeout=6000)
                    check('late result is not published',not store.proposals(c.id))
                    check('cancel never modifies case facts',store.get(c.id).revision==2)
                    # Changelog is a separate product history, not another case event feed.
                    nav('changelog');expect(page.get_by_role('heading',name='The build, in the open.')).to_be_visible()
                    expect(page.locator('.changelog-entry').first).to_contain_text(VERSION)
                    check('current build and limits visible',VERSION.lower() in page.locator('.changelog-entry').first.inner_text().lower() and 'local unreleased' in page.locator('.changelog-entry').first.inner_text().lower())
                    check('previous Plan Studio changelog retained','0.2.0-alpha.2' in page.locator('main').inner_text().lower())
                    page.screenshot(path=str(OUT/'8BALL-Changelog.png'),full_page=True)
                    for width in (1600,1024,390):
                        page.set_viewport_size({'width':width,'height':1000 if width>400 else 844})
                        for tab in ('studio','review','changelog'):
                            nav(tab);check(f'{tab} fits {width}px',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                        if width==390:
                            nav('studio');select('actions','mediated')
                            page.screenshot(path=str(OUT/'8BALL-Plan-Studio-Mobile.png'),full_page=True)
                    page.locator('.topbar [data-action=logout]').click();expect(page.locator('form[data-form=login]')).to_be_visible()
                    check('locking clears authoring and analysis view',page.locator('.studio-layout,.analysis-monitor').count()==0)
                    check('no page runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'explicit ASGI bridge' if BRIDGE else 'native loopback HTTP','model_inference_tested':False,'provider':'controlled loopback HTTP test double','native_browser_storage_and_downloads_tested':False,'errors':errors}
                    (OUT/'studio-browser-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'),full_page=True);(OUT/'failure.html').write_text(page.content());print('Errors',errors);raise
                finally:browser.close()
        finally:
            release.set();server.shutdown();server.server_close();proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill()

if __name__=='__main__':main()
