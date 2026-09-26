"""Native by default; the existing explicit bridge is not native browser evidence.
No providers are called. Tests use fictional cases and the real API/SQLite store.
"""
import json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
import httpx
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from browser_v2 import open_document,BRIDGE,TOKEN
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Case
from eightball.v2.commands import Command
from eightball.models import utcnow
from datetime import timedelta
OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/plan-review')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(title,ok):
    assert ok,title
    checks.append(title)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'cases.db');store=Store(db)
        case=store.create(demo_case(),fixture=True)
        other=store.create(Case(title='Second case',client='Fictional',summary='Blank independent case.',desired_outcome='A different objective',deadline=utcnow()+timedelta(days=1)))
        before=store.audit(case.id)
        server=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(60):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',trust_env=False,timeout=1).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1600,'height':1100},reduced_motion='reduce');page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                def tab(which):page.locator(f'[data-pr-tab="{which}"]').click()
                def nav(which):
                    page.locator(f'nav [data-tab={which}]').click();expect(page.locator(f'nav [data-tab={which}]')).to_have_attribute('aria-current','page')
                try:
                    open_document(page,db);page.locator('[name=token]').fill(TOKEN);page.locator('form[data-form=login] [type=submit]').click()
                    page.locator(f'[data-case="{case.id}"]').click();nav('studio')
                    page.locator('[data-studio=select][data-kind=actions][data-id=direct]').click()
                    page.locator('[data-studio-field=cost]').fill('2222');page.locator('[data-studio-field=cost]').press('Tab')
                    page.locator('[data-pr-action=open]').click();page.locator('.pr-target').wait_for()
                    check('review is anchored to the exact requested outcome',case.desired_outcome in page.locator('.pr-target').inner_text())
                    check('review explicitly excludes unsaved graph edits','not unsaved Plan Studio changes' in page.locator('[data-pr-root]').inner_text())
                    check('opening assessment is read-only',store.audit(case.id)==before)
                    check('target verification criteria are visible',page.locator('.pr-condition blockquote').count()>0)
                    check('structural diagnostics include unspecified waits','waiting time unspecified' in page.locator('.pr-content').inner_text())
                    check('there is no success percentage','%' not in page.locator('.pr-metrics').inner_text())
                    page.screenshot(path=str(OUT/'8BALL-Plan-Review.png'),full_page=False)
                    tab('scenarios');f=page.locator('[data-pr-form=scenarios]')
                    f.locator('[name=action]').select_option('direct');f.locator('[name=budget]').fill('1');f.locator('[name=minutes]').fill('120');f.locator('[type=submit]').click()
                    expect(page.locator('.pr-trial')).to_have_count(4)
                    check('three explicit hypothetical checks plus baseline shown',page.locator('.pr-trial').count()==4)
                    check('live case unchanged after checks',store.audit(case.id)==before)
                    check('scenario values are distinguished from live baseline','HYPOTHETICAL' in page.locator('.pr-trials').inner_text())
                    check('original action cost unchanged',next(a.cost for a in store.get(case.id).graph.actions if a.id=='direct')==800)
                    page.screenshot(path=str(OUT/'8BALL-Plan-Review-Scenarios.png'),full_page=False)
                    tab('human');f=page.locator('[data-pr-form=judgements]')
                    expect(f.locator('.pr-rubric')).to_have_count(6)
                    check('all six human checks require deliberate choices',all(v=='' for v in f.locator('select[name^=verdict]').evaluate_all('(els)=>els.map(e=>e.value)')))
                    f.locator('[name=verdict_target]').select_option('needs_changes');f.locator('[name=reason_target]').fill('Recheck every part of the desired outcome before proceeding.')
                    tab('findings');tab('human');f=page.locator('[data-pr-form=judgements]')
                    check('unsubmitted reviewer notes survive section switching',f.locator('[name=reason_target]').input_value().startswith('Recheck every'))
                    for criterion in ['sources','dependencies','authority','estimates','alternatives']:
                        f.locator(f'[name=verdict_{criterion}]').select_option('uncertain')
                        f.locator(f'[name=reason_{criterion}]').fill('Fictional review: further checking is required before use.')
                    f.locator('[name=ref_sources]').select_option('source:'+case.evidence[0].id)
                    refpanel=f.locator('[data-pr-reference=sources]');refpanel.locator('xpath=..').locator('summary').click()
                    check('selected source content can be inspected inside review',case.evidence[0].text in refpanel.inner_text())
                    check('inspecting a source does not attest its claims',store.audit(case.id)==before)
                    f.locator('[name=reason_target]').focus();page.keyboard.press('Tab')
                    check('keyboard can move between review controls',page.evaluate('document.activeElement !== document.body'))
                    page.screenshot(path=str(OUT/'8BALL-Plan-Review-Rubric.png'),full_page=False)
                    for width in [390,1600]:
                        page.set_viewport_size({'width':width,'height':844 if width==390 else 1100})
                        for which in ['findings','scenarios','human','history']:
                            tab(which)
                            check(f'{which} review section fits {width}px',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
                        if width==390:
                            tab('findings');page.screenshot(path=str(OUT/'8BALL-Plan-Review-Mobile.png'),full_page=False)
                    tab('human');page.locator('[data-pr-form=judgements] [type=submit]').click()
                    expect(page.locator('.pr-history')).to_have_count(1)
                    after=store.audit(case.id)
                    check('review reason and disposition persist','Changes requested' in page.locator('.pr-history').inner_text())
                    check('recording judgement does not alter case revision or facts',after['case']==before['case'] and after['events']==before['events'])
                    check('review export preserves exact assessment and rubric',after['valid'] and len(after['plan_reviews']['records'][0]['judgements'])==6)
                    check('review cannot grant action approval',not store.get(case.id).approvals)
                    # Later changes do not erase the earlier human review.
                    store.change(case.id,Command(event_id='later',expected_revision=0,kind='metadata',payload={'budget':6000}))
                    page.keyboard.press('Escape');page.locator('[data-action=refresh]').click();expect(page.locator('nav [data-tab=studio]')).to_have_attribute('aria-current','page')
                    page.locator('[data-pr-action=open]').click();page.locator('.pr-target').wait_for();tab('history')
                    check('old review is marked historical after case changes','case has changed since this review' in page.locator('.pr-history').inner_text())
                    page.keyboard.press('Escape');nav('command');page.locator(f'[data-case="{other.id}"]').click();page.locator('[data-action=discard-open-case]').click();nav('studio')
                    page.locator('[data-pr-action=open]').click();page.locator('.pr-target').wait_for()
                    check('case switching does not leak preceding review or outcome','A different objective' in page.locator('.pr-target').inner_text() and case.desired_outcome not in page.locator('[data-pr-root]').inner_text())
                    check('blank case raises no-mandatory-outcome diagnostic','No mandatory outcome criteria' in page.locator('[data-pr-root]').inner_text())
                    tab('history');check('review history is case-scoped',page.locator('.pr-history').count()==0)
                    page.keyboard.press('Escape');check('escape closes modal',page.locator('.dialog').count()==0)
                    check('no browser runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'Explicit ASGI bridge' if BRIDGE else 'Native loopback HTTP',
                       'real_api':True,'real_sqlite':True,'native_browser_http':not BRIDGE,'native_storage_downloads_tested':False,
                       'models_called':False,'independent_expert_review':False,'errors':errors}
                    (OUT/'browser-plan-review-report.json').write_text(json.dumps(report,indent=2))
                    print(json.dumps(report,indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'),full_page=True)
                    (OUT/'failure.html').write_text(page.content());print(errors);raise
                finally:browser.close()
        finally:
            server.terminate()
            try:server.wait(timeout=5)
            except subprocess.TimeoutExpired:server.kill();server.wait()


if __name__=='__main__':main()
