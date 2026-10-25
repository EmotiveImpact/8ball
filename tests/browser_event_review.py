"""Native signed-identity event review journey using fictional local records.
No real identity provider, model inference or human acceptance is claimed.
"""
import json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
from datetime import timedelta
import httpx,jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from eightball.store import Store as LegacyStore
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.event_reviews import EventReviews
from eightball.v2.commands import Command
from eightball.event_work import EventWork
from eightball.event_inbox import EventInbox
from eightball.agency_access import AccessRegistry
from eightball.authorisation import Grant,Identity,Operation,Resource
from eightball.models import utcnow
from endstate.events import IncomingEvent
OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/event-review')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,result):
    assert result,name
    checks.append(name)


def main():
    if os.getenv('EIGHTBALL_BROWSER_BRIDGE')=='1':raise RuntimeError('Event review suite requires native HTTP; no bridge substitution')
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'cases.db');LegacyStore(db);store=Store(db);EventReviews(store)
        registry=AccessRegistry(db);scope=dict(organisation_id='fictional-agency',matter_id='fictional-matter')
        identity=Identity(issuer='https://identity.fixture.example',subject='reviewer');key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        public=Path(tmp)/'public.pem';public.write_bytes(key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
        token=jwt.encode(dict(iss=identity.issuer,sub=identity.subject,aud='8ball',iat=utcnow(),exp=utcnow()+timedelta(minutes=15)),key,algorithm='RS256')
        def grant(name,op):registry.add_grant(name,Grant(identity=identity,resource=Resource(**scope),operations=frozenset({op}),valid_from=utcnow()-timedelta(minutes=1),expires_at=utcnow()+timedelta(hours=1)))
        grant('read',Operation.READ);grant('write',Operation.WRITE)
        def make(sequence):
            case=store.create(demo_case(),fixture=True);registry.bind_case(case.id,Resource(**scope))
            receipt=EventInbox(db).append(IncomingEvent(**scope,source_id='fictional-source',source_version=str(sequence),event_id='event-'+str(sequence),kind='proposal_received',base_revision=0,text='Original fictional source <img src=x onerror="window.injected=true">'),**scope)
            queue=EventWork(db);work=queue.enqueue(**scope,sequence=receipt.sequence,base_revision=0,case_id=case.id)
            claim=queue.claim(work,**scope);queue.finish(work,claim,'Suggested cost: 2222. This is unreviewed output.',**scope,current_revision=0,permission_valid=True)
            return case,work
        case,work=make(1);other,other_work=make(2);uncertain_case,uncertain_work=make(3)
        code='''import os,uvicorn
from pathlib import Path
from eightball.api import make_app
from eightball.store import Store
from eightball.agency_access import AccessRegistry,AgencyAccess
s=Store(os.environ['REVIEW_TEST_DB'])
a=AgencyAccess(AccessRegistry(s.path),issuer='https://identity.fixture.example',audience='8ball',public_key=Path(os.environ['REVIEW_TEST_PUBLIC']).read_text())
uvicorn.run(make_app(s,'unused-local-token-with-32-characters',agency_access=a),host='127.0.0.1',port=8048,log_level='error')
'''
        server=subprocess.Popen([sys.executable,'-c',code],cwd=ROOT,env={**os.environ,'REVIEW_TEST_DB':db,'REVIEW_TEST_PUBLIC':str(public)},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(60):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',trust_env=False,timeout=1).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1500,'height':1100},reduced_motion='reduce');page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
                def open_review(c,w):page.goto(f'http://127.0.0.1:8048/v2/event-review.html?case={c.id}&work={w}')
                def login():page.locator('[name=token]').fill(token);page.get_by_role('button',name='Open review',exact=True).click();page.get_by_role('heading',name='Original source',exact=True).wait_for()
                def edit():page.locator('[data-studio=select][data-kind=actions][data-id=direct]').click();page.locator('[data-studio-field=cost]').fill('2222');page.locator('[data-studio-field=cost]').press('Tab')
                try:
                    open_review(case,work);login()
                    check('source markup is rendered as inert text',page.evaluate('window.injected===undefined') and page.locator('.review-originals img').count()==0)
                    check('token is not persisted in browser storage',page.evaluate('localStorage.length===0&&sessionStorage.length===0'))
                    check('opening review does not change the case',store.get(case.id).revision==0)
                    edit();page.get_by_role('button',name='Preview changes',exact=True).click();expect(page.locator('[data-studio=commit]')).to_be_enabled()
                    check('preview has no case write',store.get(case.id).revision==0)
                    page.locator('[data-studio=commit]').click();expect(page.locator('#review-rationale')).to_be_focused()
                    check('commit requires reviewer rationale',page.locator('.dialog').count()==0)
                    page.locator('#review-rationale').fill('Checked the cost against the original fictional source.')
                    page.wait_for_function("!document.querySelector('#toast').classList.contains('visible')")
                    for width in (320,390,768):
                        page.set_viewport_size({'width':width,'height':1000})
                        check('editable review fits viewport '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                    page.set_viewport_size({'width':390,'height':1000});page.screenshot(path=str(OUT/'8BALL-Event-Review-Editor-Mobile.png'),full_page=True)
                    page.set_viewport_size({'width':1500,'height':1100});page.screenshot(path=str(OUT/'8BALL-Event-Review-Editor.png'),full_page=True)
                    page.locator('[data-studio=commit]').click();expect(page.get_by_role('heading',name='Commit this plan amendment?')).to_be_visible()
                    check('confirmation makes workspace inert',page.locator('#app').evaluate('(el)=>el.inert'))
                    page.get_by_role('button',name='Commit reviewed amendment',exact=True).click();expect(page.locator('.review-status')).to_contain_text('committed at case revision 1')
                    check('review commits one case revision',store.get(case.id).revision==1)
                    saved=store.audit(case.id)['incoming_event_reviews']['records'][0]
                    check('original output and reviewer retained',saved['original_result'].startswith('Suggested cost:') and saved['request']['reviewer']['subject']=='reviewer')
                    check('human editing never claims unassisted model acceptance',saved['unassisted_model_acceptance'] is False)
                    page.get_by_role('button',name='Check change notices').click();page.get_by_role('button',name='Acknowledge receipt').click()
                    check('delivery acknowledgement does not change the case',store.get(case.id).revision==1)
                    page.get_by_role('button',name='Refresh review').click();expect(page.locator('.review-status')).to_contain_text('Review committed')
                    check('committed result cannot be committed again in UI',page.locator('[data-studio=commit]').count()==0)
                    page.get_by_role('button',name='Lock review').click();expect(page.locator('#review-login')).to_be_visible()
                    check('locking clears original material from screen',page.locator('.review-originals').count()==0)
                    registry.revoke('write');open_review(other,other_work);login()
                    expect(page.locator('.review-status')).to_contain_text('Read-only access')
                    check('read-only reviewer cannot edit',page.locator('#review-rationale').is_disabled() and page.locator('[data-studio=preview]').is_disabled())
                    grant('write2',Operation.WRITE);page.get_by_role('button',name='Refresh review').click();expect(page.locator('#review-rationale')).to_be_enabled();edit()
                    store.change(other.id,Command(event_id='outside-change',expected_revision=0,kind='metadata',payload={'budget':888}))
                    page.get_by_role('button',name='Preview changes').click();expect(page.locator('.review-status')).to_contain_text('stale')
                    check('stale preview blocks amendment',page.locator('#review-rationale').is_disabled() and page.locator('[data-studio=preview]').is_disabled() and store.get(other.id).revision==1)
                    page.get_by_role('button',name='Lock review').click();open_review(uncertain_case,uncertain_work);login();edit()
                    page.locator('#review-rationale').fill('Explicitly reviewed the fictional cost change before committing.')
                    page.get_by_role('button',name='Preview changes',exact=True).click();expect(page.locator('[data-studio=commit]')).to_be_enabled()
                    sent=[]
                    def lose_ack(route):
                        route.fetch();sent.append(True);route.abort()
                    page.route('**/event-work/'+uncertain_work+'/review',lose_ack)
                    page.locator('[data-studio=commit]').click();page.get_by_role('button',name='Commit reviewed amendment',exact=True).click()
                    expect(page.locator('.review-status')).to_contain_text('save outcome is unknown')
                    check('lost acknowledgement cannot cause automatic replay',len(sent)==1 and store.get(uncertain_case.id).revision==1)
                    check('uncertain save disables further edits',page.locator('#review-rationale').is_disabled())
                    page.get_by_role('button',name='Refresh review').click();page.get_by_role('button',name='Discard edits and refresh').click()
                    expect(page.locator('.review-status')).to_contain_text('Review committed')
                    check('explicit refresh resolves committed outcome after lost acknowledgement',store.get(uncertain_case.id).revision==1)
                    page.unroute('**/event-work/'+uncertain_work+'/review')
                    page.get_by_role('button',name='Lock review').click();open_review(case,work);login()
                    registry.revoke('read');page.get_by_role('button',name='Check change notices').click();expect(page.locator('#review-login')).to_be_visible()
                    check('revocation clears cached source and result',page.locator('.review-originals').count()==0)
                    grant('read2',Operation.READ)
                    held=[];page.route('**/event-work/'+work,lambda route:held.append(route))
                    page.locator('[name=token]').fill(token);page.get_by_role('button',name='Open review',exact=True).click()
                    expect(page.get_by_role('button',name='Lock review')).to_be_visible()
                    for _ in range(30):
                        if held:break
                        page.wait_for_timeout(20)
                    check('late-load fixture intercepted actual request',bool(held))
                    page.get_by_role('button',name='Lock review').click()
                    for route in held:route.continue_()
                    page.wait_for_timeout(100);expect(page.locator('#review-login')).to_be_visible()
                    check('late read cannot repopulate locked session',page.locator('.review-originals').count()==0)
                    page.unroute('**/event-work/'+work);login()
                    for width in (320,390,768):
                        page.set_viewport_size({'width':width,'height':1000})
                        check('review fits viewport '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                    page.screenshot(path=str(OUT/'8BALL-Event-Review-Mobile.png'),full_page=True)
                    page.set_viewport_size({'width':1500,'height':1100});page.screenshot(path=str(OUT/'8BALL-Event-Review.png'),full_page=True)
                    check('no browser runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'Native loopback HTTP','model_inference_tested':False,'independent_review_performed':False,'human_accessibility_tested':False,'errors':errors,'limits':['Test-generated signed JWTs, not actual OIDC browser sign-in.','Native automated review is not genuine human acceptance.']}
                    (OUT/'browser-event-review-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'),full_page=True);(OUT/'failure.html').write_text(page.content());raise
                finally:browser.close()
        finally:
            server.terminate()
            try:server.wait(timeout=5)
            except subprocess.TimeoutExpired:server.kill();server.wait()


if __name__=='__main__':main()
