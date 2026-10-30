"""Native by default. Explicit bridge is labelled; no models or external actions."""
import json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from datetime import timedelta
import httpx
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from browser_v2 import open_document, BRIDGE, TOKEN
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Case
from eightball.v2.commands import Command
from eightball.models import utcnow
from endstate.contracts import Graph, Condition, Action, Effect, Objective, all_of, atom
OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/courses')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'cases.db');store=Store(db);case=store.create(demo_case(),fixture=True)
        other=store.create(Case(title='Independent case',client='Fictional',summary='Separate context.',desired_outcome='Another outcome',deadline=utcnow()+timedelta(days=1)))
        nested=store.create(Case(title='Nested prerequisite course',client='Fictional',summary='Nine explicit signed prerequisites.',
            desired_outcome='Verify the reviewed result',deadline=utcnow()+timedelta(days=1),
            graph=Graph(conditions=[Condition(id='p'+str(i),title='Prerequisite '+str(i),confirmation='Direct evidence') for i in range(9)]+
                        [Condition(id='goal',title='Verified result',confirmation='Direct result evidence')],
                        actions=[Action(id='work',title='Reviewed work',owner='Operator',purpose='Reach the result',minutes=1,
                                        approval_required=True,requires=all_of(all_of(*(atom('p'+str(i),i%2==0) for i in range(8))),atom('p8')),
                                        effects=[Effect(condition_id='goal')])],
                        objectives=[Objective(id='target',title='Result',success=atom('goal'))])))
        before=store.audit(case.id)
        server=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(60):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',timeout=1,trust_env=False).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1600,'height':1100},reduced_motion='reduce');page.set_default_timeout(12000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                def nav(which):
                    page.locator(f'nav [data-tab={which}]').click();expect(page.locator(f'nav [data-tab={which}]')).to_have_attribute('aria-current','page')
                def close():page.locator('.dialog [data-action=close]').click();page.locator('.dialog').wait_for(state='detached')
                try:
                    open_document(page,db);page.locator('[name=token]').fill(TOKEN);page.locator('form[data-form=login] [type=submit]').click()
                    page.locator(f'[data-case="{case.id}"]').click();expect(page.locator('.course-empty')).to_be_visible()
                    check('course feature is in the existing Situation Room',page.locator('nav [data-tab=course]').count()==0)
                    check('opening unselected case is read-only',store.audit(case.id)==before)
                    nav('routes');page.locator('[data-course-action=choose]').first.click()
                    f=page.locator('[data-course-form=preview]');f.locator('[name=watch_condition]').select_option('refused')
                    f.locator('[name=watch_state]').select_option('true');f.locator('[name=review_at]').fill((utcnow()+timedelta(hours=1)).isoformat())
                    f.locator('[type=submit]').click();f=page.locator('[data-course-form=select]');f.wait_for()
                    check('preview shows exact human target',case.desired_outcome in page.locator('.course-target').inner_text())
                    check('preview does not choose or change case',store.audit(case.id)==before)
                    check('selection requires acknowledgement',f.locator('[name=acknowledge]').get_attribute('required') is not None)
                    f.locator('[name=rationale]').fill('Staged recovery preserves time for verified reporting. <script>window.courseLeak=true</script>')
                    f.locator('[name=assumptions]').fill('Customer willingness must be evidenced, not assumed.')
                    f.locator('[name=acknowledge]').check();f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    nav('room');expect(page.locator('[data-course-current]')).to_be_visible()
                    check('selected course appears on the Situation Room',page.locator('.course-banner').is_visible())
                    check('untrusted human notes are escaped',page.evaluate('window.courseLeak === undefined'))
                    after=store.audit(case.id);check('selection leaves factual snapshot unchanged',after['case']==before['case'])
                    check('selection leaves action approvals unchanged',after['case']['approvals']==before['case']['approvals'])
                    check('course history is linked into export',after['valid'] and after['chosen_courses']['valid'])
                    chosen=after['chosen_courses']['current_id']
                    page.locator('#toast.visible').wait_for(state='hidden')
                    page.screenshot(path=str(OUT/'8BALL-Chosen-Course.png'),full_page=True)
                    page.locator('[data-course-action=inspect]').click();expect(page.get_by_role('heading',name='Chosen course',exact=True)).to_be_visible()
                    check('original rationale remains visible','Staged recovery preserves time' in page.locator('.dialog').inner_text())
                    check('review distinguishes declared assumptions from facts','Operator-declared assumptions, not facts' in page.locator('.dialog').inner_text())
                    check('inspection cannot execute an action',page.locator('.dialog [data-action=complete],.dialog [data-action=approve]').count()==0)
                    page.screenshot(path=str(OUT/'8BALL-Course-Inspector.png'),full_page=True);close()
                    check('dialog returns focus to original control',page.evaluate("document.activeElement?.dataset.courseAction==='inspect'"))
                    # Same choice survives order changes. The operator is not silently rerouted.
                    nav('routes');sorter=page.locator('[data-sort]').element_handle()
                    page.locator('[data-sort]').select_option('lowest_cost')
                    page.wait_for_function('(sorter) => !sorter.isConnected',arg=sorter);sorter.dispose()
                    expect(page.locator('nav [data-tab=routes]')).to_have_attribute('aria-current','page')
                    check('sorting candidates does not replace course',store.audit(case.id)['chosen_courses']['current_id']==chosen)
                    # A substantive fact/constraint update recalculates the course, but never switches it.
                    current=store.get(case.id);store.change(case.id,Command(event_id='budget-change',expected_revision=current.revision,kind='metadata',payload={'budget':1}))
                    # Hold the real detail response after transport completes.
                    # A later explicit navigation must survive this older refresh;
                    # forwarding the same response still has to refresh case data.
                    page.evaluate('''caseId => {
                        const originalFetch=window.fetch;
                        const gate={held:false,released:false};
                        window.__courseRefreshRace=gate;
                        window.fetch=async (input,init)=>{
                            const response=await originalFetch(input,init);
                            if(!gate.held&&typeof input==='string'&&input.startsWith('/api/v2/cases/'+caseId+'?sort_by=')){
                                gate.held=true;
                                await new Promise(resolve=>{gate.release=()=>{gate.released=true;resolve();};});
                                window.fetch=originalFetch;
                            }
                            return response;
                        };
                    }''',case.id)
                    page.locator('[data-action=refresh]').first.click()
                    page.wait_for_function('() => window.__courseRefreshRace.held')
                    nav('room');expect(page.locator('#main h1')).to_be_focused()
                    page.evaluate('() => window.__courseRefreshRace.release()')
                    expect(page.locator('#toast')).to_have_text('Workspace refreshed from the server.')
                    expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                    expect(page.locator('#main h1')).to_be_focused()
                    check('explicit Room navigation survives an earlier delayed refresh',True)
                    expect(page.locator('.course-banner')).to_contain_text('Review required')
                    page.locator('[data-action=metadata]').click()
                    expect(page.locator('[data-form=metadata] [name=budget]')).to_have_value('1');close()
                    check('delayed refresh still applies the changed case data',True)
                    check('budget change is explained in chosen-course banner','budget changed' in page.locator('.course-banner').inner_text().lower())
                    check('constraint failure preserves chosen course',store.audit(case.id)['chosen_courses']['current_id']==chosen)
                    page.screenshot(path=str(OUT/'8BALL-Course-Reconsideration.png'),full_page=True)
                    page.locator('[data-course-action=inspect]').click();page.locator('[data-course-action=transition][data-operation=review]').click()
                    f=page.locator('[data-course-form=event]');f.locator('[name=rationale]').fill('Budget reduction needs a new mandate; this review grants no authority.')
                    f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    expect(page.locator('.course-banner')).to_contain_text('Review required')
                    check('human review does not clear deterministic warnings','Review required' in page.locator('.course-banner').inner_text())
                    page.locator('[data-course-action=inspect]').click();page.locator('[data-course-action=transition][data-operation=pause]').click()
                    f=page.locator('[data-course-form=event]');f.locator('[name=rationale]').fill('Pause the recorded course pending explicit client direction.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    expect(page.locator('.course-banner')).to_contain_text('Course paused')
                    check('pause is an explicit lifecycle judgement',store.audit(case.id)['chosen_courses']['courses'][0]['lifecycle']=='paused')
                    nav('timeline');check('course judgements appear in timeline','Course pause' in page.locator('main').inner_text())
                    nav('room');page.set_viewport_size({'width':390,'height':844});check('course banner fits mobile',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
                    page.screenshot(path=str(OUT/'8BALL-Chosen-Course-Mobile.png'),full_page=True)
                    page.locator('[data-course-action=inspect]').click();check('course inspector fits mobile',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'));close()
                    page.set_viewport_size({'width':1600,'height':1100})
                    nav('command');page.locator(f'[data-case="{other.id}"]').click();expect(page.locator('.course-empty')).to_be_visible()
                    check('course content does not leak into another case',page.locator('[data-course-current]').count()==0 and 'Staged recovery preserves time' not in page.locator('main').inner_text())
                    nav('command');page.locator(f'[data-case="{case.id}"]').click();expect(page.locator('.course-banner')).to_contain_text('Course paused')
                    check('reopening restores persisted choice and lifecycle',page.locator('[data-course-current]').get_attribute('data-course-current')==chosen)
                    page.locator('[data-course-action=inspect]').click();page.locator('[data-course-action=transition][data-operation=retire]').click()
                    f=page.locator('[data-course-form=event]');f.locator('[name=rationale]').fill('Retire this course; options will be reconsidered explicitly.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    expect(page.locator('.course-empty')).to_be_visible();page.locator('[data-course-action=history]').click()
                    check('retired course remains visible','Retired' in page.locator('.dialog').inner_text())
                    exported=store.audit(case.id);check('export preserves selection and every review',len(exported['chosen_courses']['records'])==4 and exported['valid'])
                    check('only intentional budget change altered case facts',exported['case']['revision']==1 and len(exported['events'])==2)
                    close();nav('command');page.locator(f'[data-case="{nested.id}"]').click();nav('routes')
                    page.locator('[data-course-action=choose]').first.click()
                    page.locator('[data-course-form=preview] [type=submit]').click()
                    f=page.locator('[data-course-form=select]');f.locator('[name=rationale]').fill('Keep all nine reviewed signed requirements in this course.')
                    f.locator('[name=acknowledge]').check();f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    nav('room');expect(page.locator('[data-course-current]')).to_be_visible()
                    check('nested nine-prerequisite course remains readable after selection',True)
                    nested_export=store.audit(nested.id);nested_choice=nested_export['chosen_courses']['current_id']
                    selected=nested_export['chosen_courses']['records'][0]['selection']['anchor']['route']['prerequisites']['work']
                    check('nested selection retains all signed prerequisites',len(selected)==9 and any(x['value'] is False for x in selected))
                    page.reload();expect(page.locator('[data-course-current]')).to_have_attribute('data-course-current',nested_choice)
                    page.locator('[data-course-action=inspect]').click();expect(page.get_by_role('heading',name='Chosen course',exact=True)).to_be_visible()
                    check('nested course survives native reload and inspection','Reviewed work' in page.locator('.dialog').inner_text())
                    check('nested course inspection grants no action authority',page.locator('.dialog [data-action=complete],.dialog [data-action=approve]').count()==0)
                    page.locator('[data-course-action=transition][data-operation=pause]').click()
                    f=page.locator('[data-course-form=event]');f.locator('[name=rationale]').fill('Pause this recorded choice without changing any case facts.')
                    f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    expect(page.locator('.course-banner')).to_contain_text('Course paused')
                    check('nested course lifecycle remains usable',store.audit(nested.id)['chosen_courses']['courses'][0]['lifecycle']=='paused')
                    check('nested course leaves observations approvals and completion unchanged',store.get(nested.id)==nested)
                    page.locator('[data-action=logout]').first.click();expect(page.locator('form[data-form=login]')).to_be_visible()
                    check('locking clears selected-course content',page.locator('[data-course-current]').count()==0)
                    check('no browser runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'Explicit local ASGI bridge' if BRIDGE else 'Native loopback HTTP',
                            'native_storage_and_download_tested':False,'model_calls':0,'real_sqlite':True,'errors':errors}
                    (OUT/'browser-courses-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'),full_page=True);(OUT/'failure.html').write_text(page.content());print(errors);raise
                finally:browser.close()
        finally:
            server.terminate()
            try:server.wait(timeout=5)
            except subprocess.TimeoutExpired:server.kill()

if __name__=='__main__':main()
