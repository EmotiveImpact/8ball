"""Actual Emergent Insights review journey. Native HTTP default; explicit ASGI
bridge is only a local harness, not evidence of browser networking or storage.
No live or mocked model responses are used by this deterministic feature.
"""
from pathlib import Path
from datetime import timedelta
import json,os,shutil,subprocess,sys,tempfile,time
import httpx
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from browser_v2 import open_document,BRIDGE,TOKEN
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Case
from eightball.v2.insights import Insights
from eightball.v2.commands import Command
from eightball.models import utcnow,uid
OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/insights')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,result):
 assert result,name
 checks.append(name)

def main():
 with tempfile.TemporaryDirectory() as temp:
  db=str(Path(temp)/'test.db');store=Store(db);case=store.create(demo_case(),fixture=True)
  other=store.create(Case(title='Other client isolation fixture',client='Other client',summary='Nothing from Northstar belongs here',desired_outcome='Separate outcome',deadline=utcnow()+timedelta(days=1)))
  initial=store.audit(case.id)
  proc=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  try:
   for _ in range(70):
    try:
     if httpx.get('http://127.0.0.1:8048/api/health',timeout=1,trust_env=False).status_code==200:break
    except httpx.HTTPError:pass
    time.sleep(.1)
   with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1512,'height':1100},device_scale_factor=1);page.set_default_timeout(12000)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    def nav(tab):
     page.locator(f'nav [data-tab={tab}]').click();expect(page.locator(f'nav [data-tab={tab}]')).to_have_attribute('aria-current','page')
    def run_scan():
     page.locator('[data-insight=scan]').click();f=page.locator('form[data-insight-form=scan]');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached');expect(page.locator('.ix-card').first).to_be_visible()
    try:
     open_document(page,db)
     page.locator('[name=token]').fill(TOKEN);page.locator('form[data-form=login] [type=submit]').click()
     page.locator(f'[data-case="{case.id}"]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
     nav('insights')
     check('insight history does not scan or mutate merely by opening',store.audit(case.id)==initial)
     check('no finding is invented before an explicit scan',page.locator('.ix-card').count()==0)
     run_scan();view=Insights(store).view(case.id)
     check('explicit scan produces real deterministic findings',len(view['items'])>=8 and page.locator('.ix-card').count()==len(view['items']))
     check('scan leaves original case snapshot and observations unchanged',store.get(case.id)==case)
     check('scan leaves original case chain unchanged',store.audit(case.id)['events']==initial['events'])
     check('scan writes a verified separate review ledger',store.audit(case.id)['emergent_insights']['valid'])
     check('age review is not enabled silently',view['scan']['policy']['freshness_hours'] is None)
     target=next(r for r in view['items'] if r['insight']['rule']=='shared_condition');iid=target['insight']['id']
     page.locator(f'[data-insight=select][data-id="{iid}"]').focus();page.keyboard.press('Enter')
     expect(page.locator('.ix-inspector')).to_contain_text(target['insight']['meaning'])
     check('keyboard selection opens the intended insight',page.locator(f'[data-insight=select][data-id="{iid}"]').get_attribute('aria-pressed')=='true')
     check('inspector names check caveat and supporting records',all(t in page.locator('.ix-inspector').inner_text() for t in ('CHECK BEFORE RELYING','WHAT WE ARE NOT CLAIMING','SUPPORTING RECORDS')))
     check('typed references contain reproducible record hashes','hash ' in page.locator('.ix-inspector').inner_text())
     page.locator('#toast.visible').wait_for(state='detached');page.screenshot(path=str(OUT/'8BALL-Emergent-Insights.png'),full_page=True)
     page.locator('[data-insight=review]').click();f=page.locator('form[data-insight-form=review]')
     check('human review has no factual confirmed option',f.locator('option[value=confirmed]').count()==0)
     f.locator('[name=disposition]').select_option('dismissed');f.locator('[name=reason]').fill('Investigated separately; retain this finding for later review.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
     check('dismissal leaves the finding in Everything',page.locator(f'[data-insight=select][data-id="{iid}"]').count()==1)
     page.locator('[data-insight=filter][data-id=dismissed]').click();check('dismissed filter retains its reason','Investigated separately' in page.locator('.ix-inspector').inner_text())
     check('dismissal did not attest a condition',store.get(case.id).observations==case.observations)
     page.locator('[data-insight=review]').click();f=page.locator('form[data-insight-form=review]');f.locator('[name=disposition]').select_option('unreviewed');f.locator('[name=reason]').fill('Reopen after operator discussion.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
     check('reopening retains both review decisions',len(next(r for r in Insights(store).view(case.id)['items'] if r['insight']['id']==iid)['reviews'])==2)
     page.locator('[data-insight=question]').click();f=page.locator('form[data-insight-form=question]');f.locator('[name=question]').fill('What direct evidence will settle this shared prerequisite?');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
     current=store.get(case.id)
     check('explicit question promotion creates one linked open question',len(current.questions)==len(case.questions)+1 and current.questions[-1].status=='open')
     check('question promotion increments case revision not factual truth',current.revision==case.revision+1 and current.observations==case.observations)
     check('changed case marks previous scan outdated','The case changed after this scan' in page.locator('main').inner_text())
     check('stale finding cannot be silently re-reviewed',page.locator('[data-insight=review]').is_disabled())
     run_scan();view=Insights(store).view(case.id)
     check('new scan restores current review context',not view['scan_outdated'] and view['case_revision']==current.revision)
     check('question linkage survives rescan',next(r for r in view['items'] if r['insight']['id']==iid)['questions']==[current.questions[-1].id])
     # Inferred actor links have explicit authority qualifications.
     actor=next(r for r in view['items'] if r['insight']['rule']=='actor_concentration');page.locator(f'[data-insight=select][data-id="{actor["insight"]["id"]}"]').click()
     check('actor concentration does not assert decision control','Involvement alone does not establish control' in page.locator('.ix-inspector').inner_text())
     page.locator('#toast.visible').wait_for(state='detached');page.screenshot(path=str(OUT/'8BALL-Insight-Actor-Review.png'),full_page=True)
     # Change an actual action and observe retained no-longer-reproduced history.
     old=next(r for r in view['items'] if r['insight']['rule']=='unknown_wait');aid=next(r['id'] for r in old['insight']['references'] if r['kind']=='action')
     action=next(a for a in current.graph.actions if a.id==aid).model_dump(mode='json');action['wait_minutes']=60
     current,_=store.change(case.id,Command(event_id=uid(),expected_revision=current.revision,kind='upsert_object',payload={'kind':'action','object':action}))
     page.locator('[data-action=refresh]').first.click();expect(page.locator('main')).to_contain_text('The case changed after this scan')
     run_scan();page.locator('[data-insight=filter][data-id=history]').click()
     check('obsolete finding retained not silently deleted',page.locator(f'[data-insight=select][data-id="{old["insight"]["id"]}"]').count()==1)
     check('not reproduced is not labelled verified resolution','not a declaration that the issue is resolved' in page.locator('.ix-inspector').inner_text())
     page.locator('[data-insight=filter][data-id=all]').click()
     page.locator('[data-insight=hypothesis]').click();f=page.locator('form[data-insight-form=hypothesis]')
     attack='<img src=x onerror="window.emergenceAttack=true">'
     f.locator('[name=title]').fill(attack);f.locator('[name=meaning]').fill('Could one reviewer be shared?');f.locator('[name=why]').fill('This is an operator suggestion, not a fact.');f.locator('[name=verify]').fill('Which person can verify this?');f.locator('[name=reference]').select_option('actor|coo');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
     check('operator hypothesis is preserved as a possibility',any(r['manual'] for r in Insights(store).view(case.id)['items']))
     check('untrusted insight text is escaped rather than executed',page.evaluate('window.emergenceAttack === undefined'))
     check('manual hypothesis does not change case state',store.get(case.id)==current)
     manual=next(r for r in Insights(store).view(case.id)['items'] if r['manual']);page.locator(f'[data-insight=select][data-id="{manual["insight"]["id"]}"]').click();page.locator('[data-insight=revisit]').click();f=page.locator('form[data-insight-form=revisit]');f.locator('[name=reason]').fill('Explicitly revisit the current actor record.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
     check('revisiting retains the operator hypothesis identity',len([r for r in Insights(store).view(case.id)['items'] if r['manual']])==1)
     # Select a clean non-malicious item before public screenshot.
     page.locator(f'[data-insight=select][data-id="{iid}"]').click()
     page.set_viewport_size({'width':390,'height':844})
     check('insight workspace fits mobile viewport',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
     page.locator('#toast.visible').wait_for(state='detached');page.screenshot(path=str(OUT/'8BALL-Emergent-Insights-Mobile.png'),full_page=True)
     page.set_viewport_size({'width':1512,'height':1100});nav('discoveries')
     check('build register lists every recorded discovery separately',page.locator('.ix-register article').count()==len(json.loads((ROOT/'docs/delivery/emergence.json').read_text())['items']))
     check('declined product idea remains visible',page.locator('.ix-declined').count()>=1)
     check('build register does not contain case hypothesis',attack not in page.locator('main').inner_text())
     page.locator('#toast.visible').wait_for(state='detached');page.screenshot(path=str(OUT/'8BALL-Build-Discoveries.png'),full_page=False)
     page.set_viewport_size({'width':390,'height':844});check('build discovery register fits mobile',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'));page.set_viewport_size({'width':1512,'height':1100})
     nav('command');page.locator(f'[data-case="{other.id}"]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page');nav('insights')
     check('case switching clears other client insight history',page.locator('.ix-card').count()==0 and 'Northstar' not in page.locator('main').inner_text())
     nav('command');page.locator(f'[data-case="{case.id}"]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page');nav('insights')
     check('reopening case reloads persisted review history',len(Insights(store).view(case.id)['items'])==page.locator('.ix-card').count())
     if not BRIDGE:
      page.reload();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page');nav('insights');check('native reload preserves session and case insight data',page.locator('.ix-card').count()>0)
     if not BRIDGE:
      with page.expect_download() as download:page.locator('[data-insight=export]').click()
      out=json.loads(Path(download.value.path()).read_text())
     else:
      page.evaluate("() => {window.URL.createObjectURL=b=>{window.__insightExport=b.text();return 'blob:bridge'};HTMLAnchorElement.prototype.click=function(){};}")
      page.locator('[data-insight=export]').click();page.wait_for_function('window.__insightExport !== undefined');out=json.loads(page.evaluate('window.__insightExport'))
     check('complete insight export includes every scan and reviewer reason',out['insight_history']['valid'] and any(e['kind']=='review' for e in out['insight_history']['events']) and any(e['kind']=='hypothesis_revisited' for e in out['insight_history']['events']))
     check('legacy case audit remains valid after explicit question creation',store.audit(case.id)['valid'])
     page.locator('[data-action=logout]').first.click();expect(page.locator('form[data-form=login]')).to_be_visible()
     check('lock removes case insight text from the DOM','shared prerequisite' not in page.locator('body').inner_text())
     check('no browser runtime errors',not errors)
     report={'checks_passed':len(checks),'checks':checks,'network':'Explicit ASGI bridge, not browser HTTP' if BRIDGE else 'Native loopback HTTP',
       'native_session_storage_and_download':not BRIDGE,'real_sqlite':True,'model_inference':False,'errors':errors}
     (OUT/'insights-browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    except Exception:
     page.screenshot(path=str(OUT/'failure.png'),full_page=True);(OUT/'failure.html').write_text(page.content());print('Browser errors:',errors);raise
    finally:browser.close()
  finally:
   proc.terminate()
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:proc.kill()
if __name__=='__main__':main()
