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
                    if not BRIDGE:
                        # Deterministically refresh the client snapshot while its
                        # assessment request is in flight; stale results must
                        # leave an explicit recovery state, not an endless spinner.
                        def change_context(route):
                            page.evaluate("async()=>{const {S}=await import('/v2/ui.js');S.current.case.revision+=1;}")
                            route.continue_()
                        page.route('**/plan-reviews/assess',change_context)
                        page.locator('[data-pr-action=open]').click()
                        expect(page.locator('[data-pr-root]')).to_contain_text('Case context changed')
                        check('stale assessment offers explicit reopening instead of endless loading',page.get_by_role('button',name='Reopen Plan Review').is_visible())
                        check('stale assessment is not rendered as current',page.locator('.pr-target').count()==0)
                        page.unroute('**/plan-reviews/assess',change_context)
                        page.evaluate("async()=>{const {S}=await import('/v2/ui.js');S.current.case.revision-=1;}")
                        page.keyboard.press('Escape')
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
                    tab('challenge');f=page.locator('[data-pr-form=challenge]')
                    declarations={'r1_label':'Fictional supplier','r1_objective':'Keep lawful supply available.',
                        'r1_boundary':'Only this declared case brief; no private stakeholder knowledge.',
                        'r1_assumption':'Supply may remain available.', 'r1_objection':'Supplier refusal is possible, not observed.',
                        'r1_question':'What confirmation would change this choice?',
                        'r1_verification':'Obtain current source-backed consent through a separate authorised workflow.',
                        'b1_title':'No remaining budget','b1_rationale':'Compare a declared adverse assumption.','b1_budget':'0'}
                    for name,value in declarations.items():f.locator(f'[name={name}]').fill(value)
                    for name,value in {'r1_kind':'archetype','r1_reference':'case:summary','r1_counter':'a1','b1_assumption':'a1'}.items():
                        f.locator(f'[name={name}]').select_option(value)
                    f.locator('[type=submit]').click();expect(page.locator('[data-challenge-result]')).to_be_visible()
                    check('declared scenario comparison changes no live case or audit',store.audit(case.id)==after)
                    check('challenge labels hypotheses and retains original objection','HYPOTHETICAL' in page.locator('[data-challenge-result]').inner_text() and declarations['r1_objection'] in page.locator('[data-challenge-result]').inner_text())
                    review=page.locator('[data-pr-form=challenge-disposition]')
                    review.locator('[name=status_o1]').select_option('retained_concern')
                    review.locator('[name=rationale_o1]').fill('Retain this objection until direct confirmation exists.')
                    review.locator('[name=outcome]').select_option('continue_review')
                    review.locator('[name=reason]').fill('Continue review without treating this as consent or approval.')
                    with page.expect_response(lambda r:r.url.endswith('/rehearsals/prepare')) as rejected:
                        review.locator('[type=submit]').click()
                    check('continuing review cannot silently drop an unresolved objection',rejected.value.status==422)
                    review.locator('[name=ack_o1]').check()
                    tab('findings');tab('challenge');review=page.locator('[data-pr-form=challenge-disposition]')
                    check('unsubmitted disposition survives tab switching',review.locator('[name=status_o1]').input_value()=='retained_concern' and review.locator('[name=ack_o1]').is_checked())
                    page.locator('[data-pr-action=challenge-save]').click()
                    expect(page.get_by_text('Preview your operator disposition before saving this brief.',exact=True)).to_be_visible()
                    check('saving refuses to ignore unpreviewed disposition edits','assumption_challenges' not in store.audit(case.id))
                    review.locator('[type=submit]').click()
                    expect(page.locator('[data-challenge-result]')).to_contain_text('Continue review without treating this as consent or approval.')
                    page.locator('[data-pr-action=challenge-save]').click()
                    expect(page.locator('[data-pr-form=challenge-packet]')).to_have_count(1)
                    challenged=store.audit(case.id)
                    saved=challenged['assumption_challenges']['records'][0]['brief']
                    check('separate immutable brief preserves dissent and exact overlay',saved['coverage']['unresolved_objections']==['o1'] and saved['branches'][0]['manifest']['overlay']['budget']==0)
                    check('saving a challenge changes no evidence, course, approvals or case event',challenged['case']==after['case'] and challenged['events']==after['events'])
                    if not BRIDGE:
                        packet_form=page.locator('[data-pr-form=challenge-packet]')
                        with page.expect_download() as download:packet_form.locator('[type=submit]').click()
                        full=json.loads(Path(download.value.path()).read_text())
                        check('operator packet uses verified saved brief and no execution authority',full['brief']['brief_sha256']==saved['brief_sha256'] and not full['execution_authorized'] and not full['facts_attested'])
                        packet_form.locator('[name=mode]').select_option('reference_index')
                        packet_form.locator('[name=reference]').select_option('case:summary')
                        with page.expect_download() as download:packet_form.locator('[type=submit]').click()
                        restricted=json.loads(Path(download.value.path()).read_text())
                        check('restricted packet omits all narrative and marks incomplete audit',restricted['brief'] is None and not restricted['complete_audit'] and restricted['omissions'] and declarations['r1_objection'] not in json.dumps(restricted) and case.summary not in json.dumps(restricted))
                        check('restricted packet has only selected reference hash',restricted['references']==[{'reference':'case:summary','sha256':saved['reference_hashes']['case:summary']}])
                        check('packet downloads do not write case or derived history',store.audit(case.id)==challenged)
                    page.screenshot(path=str(OUT/'8BALL-Assumption-Challenge.png'),full_page=False)
                    # Later changes do not erase the earlier human review.
                    store.change(case.id,Command(event_id='later',expected_revision=0,kind='metadata',payload={'budget':6000}))
                    if not BRIDGE:
                        downloaded=[];page.on('download',lambda item:downloaded.append(item))
                        with page.expect_response(lambda r:r.url.endswith('/rehearsals/packet')) as rejected:
                            page.locator('[data-pr-form=challenge-packet] [type=submit]').click()
                        check('server refuses stale packet even before browser refresh',rejected.value.status==409)
                        expect(page.get_by_text('Case or challenge history changed; refresh before exporting',exact=True)).to_be_visible()
                        check('stale packet request cannot download cached narrative',not downloaded)
                    page.keyboard.press('Escape');page.locator('[data-action=refresh]').click();expect(page.locator('.page-footer')).to_contain_text('CASE REV 1')
                    expect(page.locator('nav [data-tab=studio]')).to_have_attribute('aria-current','page')
                    page.locator('[data-pr-action=open]').click();page.locator('.pr-target').wait_for();tab('history')
                    check('old review is marked historical after case changes','case has changed since this review' in page.locator('.pr-history').inner_text())
                    tab('challenge');page.locator('[data-pr-action=challenge-history]').click()
                    expect(page.locator('.pr-history')).to_contain_text('Historical: case changed')
                    check('historical brief prompts recheck rather than current export',page.locator('[data-pr-form=challenge-packet]').count()==0)
                    page.locator('[data-pr-action=challenge-recheck]').last.click()
                    page.locator('[data-pr-action=challenge-save]').click()
                    expect(page.locator('[data-information-loop]')).to_have_count(2)
                    candidate=page.locator('[data-information-loop]').first.locator('[data-check-id=a1]')
                    candidate.locator('summary').click()
                    form=candidate.locator('[data-pr-form=challenge-check]')
                    form.locator('[name=question]').fill('What would confirm this assumption?')
                    form.locator('[name=owner]').fill('Fictional operator')
                    form.locator('[name=reason]').fill('Resolve the retained uncertainty before proceeding.')
                    tab('findings');tab('challenge')
                    candidate=page.locator('[data-information-loop]').first.locator('[data-check-id=a1]')
                    candidate.locator('summary').click()
                    form=candidate.locator('[data-pr-form=challenge-check]')
                    check('unsubmitted check survives review tab switches',form.locator('[name=question]').input_value()=='What would confirm this assumption?')
                    before_check=store.get(case.id)
                    form.locator('[type=submit]').click()
                    expect(page.locator('.page-footer')).to_contain_text('CASE REV 2')
                    expect(page.locator('[data-information-loop]')).to_have_count(2)
                    created=store.get(case.id)
                    check('explicit check creates one open case question without observation or execution',len(created.questions)==len(before_check.questions)+1 and created.observations==before_check.observations and created.completed==before_check.completed and not created.approvals)
                    candidate=page.locator('[data-information-loop]').first.locator('[data-check-id=a1]')
                    candidate.locator('summary').click()
                    expect(candidate).to_contain_text('What would confirm this assumption?')
                    check('current-state projection exposes separate evidence-backed answer control',candidate.locator('[data-action=answer]').count()==1 and candidate.locator('[data-pr-form=challenge-check]').count()==0)
                    check('question creation preserves the original saved brief',store.audit(case.id)['assumption_challenges']['records'][0]['brief']==saved)
                    candidate.locator('[data-action=answer]').click()
                    answer=page.locator('[data-form=answer]')
                    answer.locator('[name=answer]').fill('Fictional reviewed response; conditions still require separate observations.')
                    answer.locator('[name=evidence_ids]').first.check()
                    answer.locator('[type=submit]').click()
                    expect(page.locator('.page-footer')).to_contain_text('CASE REV 3')
                    answered=store.get(case.id)
                    check('linked question uses existing source-backed answer without attesting a condition',answered.questions[-1].status=='answered' and answered.observations==before_check.observations)
                    page.locator('[data-pr-action=open]').click();tab('challenge');page.locator('[data-pr-action=challenge-history]').click()
                    expect(page.locator('[data-information-loop]').first).to_contain_text('Recorded answer')
                    page.locator('[data-pr-action=challenge-recheck]').first.click();page.locator('[data-pr-action=challenge-save]').click()
                    expect(page.locator('[data-information-loop]')).to_have_count(3)
                    latest=page.locator('[data-information-loop]').first.locator('[data-check-id=a1]');latest.locator('summary').click()
                    check('reconsideration retains existing answer instead of duplicating its check',latest.locator('[data-action=answer]').count()==1 and latest.locator('[data-pr-form=challenge-check]').count()==0 and len(store.get(case.id).questions)==len(created.questions))
                    for width in [390,1600]:
                        page.set_viewport_size({'width':width,'height':844 if width==390 else 1100})
                        check(f'information loop fits {width}px',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
                    page.screenshot(path=str(OUT/'8BALL-Information-Loop.png'),full_page=False)
                    page.keyboard.press('Escape');nav('command');page.locator(f'[data-case="{other.id}"]').click();page.locator('[data-action=discard-open-case]').click();nav('studio')
                    page.locator('[data-pr-action=open]').click();page.locator('.pr-target').wait_for()
                    check('case switching does not leak preceding review or outcome','A different objective' in page.locator('.pr-target').inner_text() and case.desired_outcome not in page.locator('[data-pr-root]').inner_text())
                    check('blank case raises no-mandatory-outcome diagnostic','No mandatory outcome criteria' in page.locator('[data-pr-root]').inner_text())
                    tab('history');check('review history is case-scoped',page.locator('.pr-history').count()==0)
                    page.keyboard.press('Escape');check('escape closes modal',page.locator('.dialog').count()==0)
                    check('no browser runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'Explicit ASGI bridge' if BRIDGE else 'Native loopback HTTP',
                       'real_api':True,'real_sqlite':True,'native_browser_http':not BRIDGE,'native_storage_downloads_tested':not BRIDGE,
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
