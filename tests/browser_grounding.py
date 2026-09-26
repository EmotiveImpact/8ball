"""Source clarity UI against real API/SQLite. Native by default; bridge explicit."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile,time
import httpx
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from browser_v2 import open_document,BRIDGE
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Actor,Evidence,Case,uid,utcnow
from eightball.v2.commands import Command
from eightball.v2.grounding import GroundingDesk
from datetime import timedelta
TOKEN='browser-v2-fixture-operator-token-123456789'
OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/grounding')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,value):
 assert value,name
 checks.append(name)

def main():
 with tempfile.TemporaryDirectory() as tmp:
  db=str(Path(tmp)/'grounding.db');store=Store(db);case=demo_case()
  case.actors.extend([Actor(id='alex_legal',name='Alex Morgan',role='Legal adviser'),Actor(id='alex_finance',name='Alex Morgan',role='Customer finance')])
  case.evidence.extend([
    Evidence(id='source_names',title='Customer finance briefing',source='Fictional account director, 24 September 2026',text='😀\r\nAlex Morgan in customer finance asked for the approved report by noon tomorrow, London time.',status='reviewed'),
    Evidence(id='source_clock',title='Clock change review',source='Fictional operations note',text='The review deadline is 01:30 on 25 October 2026 in Europe/London.',status='reviewed')])
  case=store.create(case,fixture=True);desk=GroundingDesk(store);initial=store.audit(case.id)
  other=store.create(Case(title='Separate client fixture',client='Other client',summary='Isolated test case',desired_outcome='Separate outcome',deadline=utcnow()+timedelta(days=1)))
  proc=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  try:
   for _ in range(80):
    try:
     if httpx.get('http://127.0.0.1:8048/api/health',timeout=1,trust_env=False).status_code==200:break
    except httpx.HTTPError:pass
    time.sleep(.1)
   with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1512,'height':1080},device_scale_factor=1);page.set_default_timeout(12000)
    errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
    def nav(tab):
     page.locator(f'nav [data-tab="{tab}"]').click();expect(page.locator(f'nav [data-tab="{tab}"]')).to_have_attribute('aria-current','page')
    def create(source,text,kind):
     page.locator('[data-grounding="new"]').first.click();f=page.locator('[data-grounding-form="new"]')
     f.locator('[name=evidence_id]').select_option(source)
     f.locator('#gd-reader').evaluate('(el,text)=>{const start=el.value.indexOf(text);el.focus();el.setSelectionRange(start,start+text.length)}',text)
     f.locator('[name=kind]').select_option(kind);f.locator('[name=note]').fill('Confirm who or when the quoted source describes, without changing the original.')
     f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
    try:
     open_document(page,db);page.locator('[name=token]').fill(TOKEN);page.locator('[data-form=login] [type=submit]').click()
     page.locator(f'[data-case="{case.id}"]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page');nav('grounding')
     check('Opening source clarity is read-only',store.audit(case.id)==initial)
     create('source_names','Alex Morgan','identity');r=desk.view(case.id)['records'][0]
     check('Exact source selection maps emoji and CRLF to original offsets',r['mention']['start']==3 and r['mention']['quote']=='Alex Morgan')
     check('Both same-name actors are shown without auto-selection',page.locator('.gd-candidates article').count()==2 and not r['actor_id'])
     check('Creating a review preserves live case and evidence',store.get(case.id)==case)
     page.locator('[data-grounding=identity]').click();f=page.locator('[data-grounding-form=identity]')
     check('Identity defaults to unresolved, not a guessed actor',f.locator('[name=disposition]').input_value()=='unresolved')
     f.locator('[name=disposition]').select_option('distinct');f.locator('[name=actor_id]').select_option('alex_legal');f.locator('[name=reason]').fill('The source specifically identifies customer finance, not legal.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
     check('Distinct identity judgement does not merge actor records',len(store.get(case.id).actors)==len(case.actors))
     page.locator('[data-grounding=identity]').click();f=page.locator('[data-grounding-form=identity]');f.locator('[name=disposition]').select_option('linked');f.locator('[name=actor_id]').select_option('alex_finance');f.locator('[name=reason]').fill('The case lead confirmed the quoted finance reference.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
     check('Revised identity retains the original negative identification',len(desk.view(case.id)['records'][0]['history'])==3)
     check('Linking a mention never changes authority or observations',store.get(case.id)==case)
     page.locator('#toast.visible').wait_for(state='detached');page.screenshot(path=str(OUT/'8BALL-Identity-Review.png'),full_page=True)
     create('source_names','noon tomorrow','deadline')
     page.locator('[data-grounding=deadline]').click();f=page.locator('[data-grounding-form=deadline]')
     check('Date and timezone do not silently use browser defaults',f.locator('[name=calendar_date]').input_value()=='' and f.locator('[name=time_zone]').input_value()=='')
     f.locator('[name=target]').select_option('condition|report');f.locator('[name=basis]').select_option('relative_days')
     f.locator('[name=anchor_date]').fill('2026-09-24');f.locator('[name=day_offset]').fill('1');f.locator('[name=anchor_reason]').fill('Fictional source was written on 24 September, not merely imported then.')
     f.locator('[name=wall_time]').fill('12:00');f.locator('[name=time_zone]').fill('Europe/London');f.locator('[name=zone_reason]').fill('The source explicitly states London time.');f.locator('[name=reason]').fill('This refers to the approved incident report requested by the customer.')
     before=store.audit(case.id);f.locator('[type=submit]').click();expect(page.locator('.gd-preview')).to_be_visible()
     check('Preview is read-only for review history and case state',store.audit(case.id)==before)
     check('Relative date anchored to source becomes the correct UTC instant','2026-09-25T11:00:00+00:00' in page.locator('.gd-preview').inner_text())
     check('Preview explains target and approval invalidation','Incident report approved' in page.locator('.gd-preview').inner_text() and 'approval(s) will be invalidated' in page.locator('.gd-preview').inner_text())
     page.screenshot(path=str(OUT/'8BALL-Deadline-Preview.png'),full_page=True)
     f.locator('[name=reason]').fill('Rechecked with the case lead: only the report deadline changes.')
     check('Editing after preview removes the apply control',page.locator('[data-grounding=apply-deadline]').count()==0)
     f.locator('[type=submit]').click();page.locator('[data-grounding=apply-deadline]').click();page.locator('.dialog').wait_for(state='detached')
     now=store.get(case.id)
     check('Explicit apply changes only the selected schedule field',now.deadline==case.deadline and next(c for c in now.graph.conditions if c.id=='report').due_at.isoformat()=='2026-09-25T11:00:00+00:00')
     check('Deadline apply never attests an outcome',now.observations==case.observations and now.completed==case.completed)
     check('Case and interpretation journals are linked and valid',store.audit(case.id)['source_interpretations']['valid'])
     page.locator('#toast.visible').wait_for(state='detached');page.screenshot(path=str(OUT/'8BALL-Source-Clarity.png'),full_page=True)
     # Ambiguous daylight-saving clock: show both real instants and block apply.
     create('source_clock','01:30 on 25 October 2026','deadline');page.locator('[data-grounding=deadline]').click();f=page.locator('[data-grounding-form=deadline]')
     f.locator('[name=calendar_date]').fill('2026-10-25');f.locator('[name=wall_time]').fill('01:30');f.locator('[name=time_zone]').fill('Europe/London');f.locator('[name=zone_reason]').fill('The operations note names the IANA zone.');f.locator('[name=reason]').fill('Clarify the repeated-clock deadline before scheduling.')
     f.locator('[type=submit]').click();expect(page.locator('#gd-preview')).to_contain_text('clock time occurs twice')
     check('Ambiguous clock requires explicit occurrence selection',page.locator('[data-grounding=apply-deadline]').count()==0)
     page.screenshot(path=str(OUT/'8BALL-Ambiguous-Time-Review.png'),full_page=True)
     f.locator('[name=fold]').select_option('1');f.locator('[type=submit]').click();expect(page.locator('[data-grounding=apply-deadline]')).to_be_visible()
     check('Second occurrence converts distinctly to UTC','2026-10-25T01:30:00+00:00' in page.locator('.gd-preview').inner_text())
     page.locator('.dialog [data-action=close]').click()
     check('Closing a preview does not apply the second deadline',store.get(case.id)==now)
     # On source retraction, preserve the adopted deadline but flag its basis.
     now,_=store.change(case.id,Command(event_id=uid(),expected_revision=now.revision,kind='review_evidence',payload={'evidence_id':'source_names','status':'retracted'}))
     page.locator('[data-action=refresh]').first.click();expect(page.locator('.gd-summary')).to_contain_text('2')
     page.locator('[data-grounding=filter][data-id=attention]').click()
     check('Retracted sources visibly require reconsideration',page.locator('.gd-item').count()==2)
     check('Source retraction does not silently remove the deadline',next(c for c in store.get(case.id).graph.conditions if c.id=='report').due_at.isoformat()=='2026-09-25T11:00:00+00:00')
     check('History warns that adopted deadlines remain until changed','remains in force' in page.locator('.gd-inspector').inner_text())
     page.set_viewport_size({'width':390,'height':844})
     check('Source clarity fits mobile width',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
     page.locator('#toast.visible').wait_for(state='detached');page.screenshot(path=str(OUT/'8BALL-Source-Clarity-Mobile.png'),full_page=True)
     page.set_viewport_size({'width':1512,'height':1080});nav('changes')
     check('Applied source interpretation appears in the case change trail','Apply deadline review' in page.locator('main').inner_text())
     nav('command');page.locator(f'[data-case="{other.id}"]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page');nav('grounding')
     check('Another case cannot inherit the previous interpretation cache',page.locator('.gd-item').count()==0 and 'Customer finance briefing' not in page.locator('main').inner_text())
     check('No browser runtime errors',not errors)
     report={'checks_passed':len(checks),'checks':checks,'network':'Explicit ASGI bridge' if BRIDGE else 'Native loopback HTTP',
             'real_sqlite':True,'model_inference_tested':False,'native_storage_and_download_tested':False,'runtime_errors':errors}
     (OUT/'browser-grounding-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    except Exception:
     page.screenshot(path=str(OUT/'failure.png'),full_page=True);(OUT/'failure.html').write_text(page.content());print('Runtime errors',errors);raise
    finally:browser.close()
  finally:
   proc.terminate()
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:proc.kill()

if __name__=='__main__':main()
