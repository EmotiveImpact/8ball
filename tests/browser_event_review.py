"""Native signed-identity event review journey using fictional local records.
No real identity provider, model inference or human acceptance is claimed.
"""
import json,os,re,shutil,subprocess,sys,tempfile,time
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
from endstate.intelligence.coordination import Attempt, ReviewSpec, summarize
from endstate.intelligence.planning import coordinate
from hashlib import sha256
from tests.test_coordinated_planning import spec as coordination_spec, outputs
from tests.test_specialist_review import attempt
from eightball.store import digest
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
        def comparison(receipt,case,mode='partial'):
            models=['jev-latest','clef-flash','gpt-6-luna-decisions']
            spec=ReviewSpec(id='fictional-comparison',models=models,max_seconds=30,max_reported_cost_nano_usd=10,
                questions=[dict(id='review',instructions='Does this fictional proposal need more evidence?',
                    criteria={'accept':'Continue review. <img src=x onerror="window.injected=true">',
                              'review':'Missing evidence requires further review.'})])
            attempts=[]
            if mode!='empty':
                for model,choice,cost in [(models[0],'review',1),(models[1],'accept',None)]:
                    attempts.append(Attempt(model=model,status='answered',request_started=True,served_model=model,
                        request_sha256='a'*64,response_sha256='b'*64,reported_cost_nano_usd=cost,
                        usage={'input_tokens':10,'output_tokens':5,**({'cost_nano_usd':cost} if cost is not None else {})},
                        answers={'review':dict(type='choice',choice=choice,confidence=.7,
                            probabilities={k:.8 if k==choice else .2 for k in ('accept','review')})}))
            result=summarize(spec,attempts)
            result.update(kind='specialist_review',stop_reason='time_budget' if mode=='empty' else 'unknown_reported_cost',
                case_id=case.id,base_revision=case.revision,receipt_sha256=digest(receipt.model_dump(mode='json')),
                input_sha256=digest(receipt.event.text),spec_sha256=digest(spec.model_dump(mode='json')),
                automatic_retries=False,automatic_fallback=False,charge_status='provider_billing_not_verified')
            if mode=='invalid':result['questions'][0]['disagreement']=False
            return json.dumps(result)
        def make(sequence,output=None):
            case=store.create(demo_case(),fixture=True);registry.bind_case(case.id,Resource(**scope))
            receipt=EventInbox(db).append(IncomingEvent(**scope,source_id='fictional-source',source_version=str(sequence),event_id='event-'+str(sequence),kind='proposal_received',base_revision=0,text='Original fictional source <img src=x onerror="window.injected=true">'),**scope)
            queue=EventWork(db);work=queue.enqueue(**scope,sequence=receipt.sequence,base_revision=0,case_id=case.id)
            claim=queue.claim(work,**scope);queue.finish(work,claim,output(receipt,case) if output else 'Suggested cost: 2222. This is unreviewed output.',**scope,current_revision=0,permission_valid=True)
            return case,work
        def coordinated_output(receipt,case,mode='completed'):
            spec=coordination_spec();values=outputs();calls=[]
            values[0]['approaches'][0]['rationale']+=' <img src=x onerror="window.injected=true">'
            if mode=='failed':values[2]['readiness']['confirmation']='x'*181
            if mode=='failed_initial':values[0]['readiness']['confirmation']='x'*181
            def generate(*args):
                value=values[len(calls)];raw=json.dumps(value)
                calls.append(dict(raw_content=raw,raw_content_sha256=sha256(raw.encode()).hexdigest(),
                    request_sha256='c'*64,response_sha256='d'*64,response_body_sha256='e'*64,
                    served_model='native-browser-fixture',status='response_received',response_mode='prompt_only'))
                return value,'native-browser-fixture'
            def challenge(state,checkpoint):
                attempts=([attempt(spec.review.models[0],cost=None)] if mode=='partial' else
                    [attempt(m,c) for m,c in zip(spec.review.models,['review','accept','review'])])
                return summarize(spec.review,attempts)|dict(input_sha256=digest(state),
                    stop_reason='unknown_reported_cost' if mode=='partial' else 'completed')
            result=coordinate(spec,receipt.event.text,'coord_'+digest(receipt.model_dump(mode='json'))[:32],generate,challenge,lambda:None)
            result.update(kind='coordinated_planning',case_id=case.id,base_revision=case.revision,
                receipt_sha256=digest(receipt.model_dump(mode='json')),spec_sha256=digest(spec.model_dump(mode='json')),
                planning_receipt=dict(requested_model='native-browser-fixture',calls=calls),
                specialist_receipts=[],max_output_tokens_per_planning_call=4096,
                planning_cost_status='unknown_not_provider_reported',charge_status='provider_billing_not_verified')
            if mode=='invalid':result['challenges']['questions'][0]['disagreement']=False
            if mode=='invalid_hash':result['receipt_sha256']='f'*64
            return json.dumps(result,sort_keys=True)
        case,work=make(1);other,other_work=make(2);uncertain_case,uncertain_work=make(3)
        specialist,specialist_work=make(4,comparison)
        empty,empty_work=make(5,lambda receipt,case:comparison(receipt,case,'empty'))
        invalid,invalid_work=make(6,lambda receipt,case:comparison(receipt,case,'invalid'))
        coordinated,coordinated_work=make(7,coordinated_output)
        partial_plan,partial_plan_work=make(8,lambda receipt,case:coordinated_output(receipt,case,'partial'))
        failed_plan,failed_plan_work=make(9,lambda receipt,case:coordinated_output(receipt,case,'failed'))
        invalid_plan,invalid_plan_work=make(10,lambda receipt,case:coordinated_output(receipt,case,'invalid'))
        initial_failure,initial_failure_work=make(11,lambda receipt,case:coordinated_output(receipt,case,'failed_initial'))
        invalid_hash,invalid_hash_work=make(12,lambda receipt,case:coordinated_output(receipt,case,'invalid_hash'))
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
                    expect(page.locator('#toast')).not_to_have_class(re.compile('.*visible.*'),timeout=10000)
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
                    registry.revoke('write2');open_review(specialist,specialist_work);login()
                    panel=page.locator('.specialist-comparison');expect(panel).to_be_visible()
                    expect(panel).to_contain_text('2 of 3 selected models answered')
                    expect(panel).to_contain_text('Different answers — unresolved')
                    check('individual differences and a missing model stay visible',panel.locator('.specialist-answers li').count()==3 and 'No validated answer' in panel.inner_text())
                    check('read-only users can inspect but not apply model choices',page.locator('#review-rationale').is_disabled() and panel.locator('button').count()==0)
                    check('specialist criteria markup remains inert',panel.locator('img').count()==0 and page.evaluate('window.injected===undefined'))
                    before=store.audit(specialist.id);writes=[]
                    page.on('request',lambda req:writes.append(req.url) if req.method!='GET' else None)
                    page.get_by_text('Request, cost and provenance details',exact=True).click()
                    expect(panel).to_contain_text('Unknown reported cost: Clef Flash')
                    expect(panel).to_contain_text('USD 0.000000001')
                    expect(panel).to_contain_text('a'*64)
                    check('retained hashes usage and cost uncertainty are inspectable','10 input tokens; 5 output tokens' in panel.inner_text() and 'Unknown does not mean free' in panel.inner_text())
                    for width in (320,390,768):
                        page.set_viewport_size({'width':width,'height':1100})
                        check('expanded comparison fits viewport '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                    page.get_by_text('Request, cost and provenance details',exact=True).click()
                    page.set_viewport_size({'width':390,'height':1000});page.screenshot(path=str(OUT/'8BALL-Specialist-Comparison-Mobile.png'),full_page=True)
                    page.set_viewport_size({'width':1500,'height':1100});page.screenshot(path=str(OUT/'8BALL-Specialist-Comparison.png'),full_page=True)
                    check('inspection makes no writes or case changes',writes==[] and store.audit(specialist.id)==before)
                    store.change(specialist.id,Command(event_id='comparison-stale',expected_revision=0,kind='metadata',payload={'budget':555}))
                    page.get_by_role('button',name='Refresh review').click();expect(panel).to_contain_text('Historical comparison for case revision 0; current revision 1')
                    check('stale specialist result remains explicitly historical',page.locator('#review-rationale').is_disabled())
                    open_review(empty,empty_work);login();expect(panel).to_contain_text('0 of 3 selected models answered')
                    check('no responses are not agreement','No validated answers.' in panel.inner_text() and panel.locator('.specialist-answers strong').all_text_contents()==['No validated answer']*3)
                    open_review(invalid,invalid_work);login();expect(page.locator('#app')).to_contain_text('Specialist comparison could not be validated')
                    check('inconsistent comparison falls back to untouched original output',panel.count()==0 and '"disagreement": false' in page.get_by_label('Original processing output',exact=True).inner_text())
                    open_review(specialist,specialist_work);login();registry.revoke('read2')
                    page.get_by_role('button',name='Refresh review').click();expect(page.locator('#review-login')).to_be_visible()
                    check('revocation clears specialist material as well as originals',panel.count()==0 and page.locator('.review-originals').count()==0)
                    grant('read3',Operation.READ)
                    open_review(coordinated,coordinated_work);login()
                    result=page.locator('.coordinated-result');expect(result).to_be_visible()
                    expect(result).to_contain_text('Method completed — quality not approved')
                    expect(result).to_contain_text('Different answers — unresolved')
                    check('coordinated originals challenges and revision stay separate',result.locator('.coordinated-proposal').count()==2 and result.locator('.specialist-answers li').count()==3)
                    before=store.audit(coordinated.id);writes.clear()
                    check('coordinated presentation has no action controls',result.locator('button,input,textarea').count()==0 and page.locator('#review-rationale').is_disabled())
                    result.get_by_text('Planning source and transport details',exact=True).click()
                    expect(result).to_contain_text('Planning cost is unknown, not free')
                    expect(result).to_contain_text('c'*64)
                    check('source and transport hashes and cost boundaries are visible',digest(coordination_spec().model_dump(mode='json')) in result.inner_text())
                    result.locator('.coordinated-proposal details summary').first.focus();page.keyboard.press('Enter')
                    check('keyboard reveals proposed actions without applying them',result.locator('.coordinated-proposal details').first.get_attribute('open') is not None)
                    check('coordinated source and model markup remains inert',result.locator('img').count()==0 and page.evaluate('window.injected===undefined'))
                    check('coordinated details have unique accessible ids',page.evaluate('new Set([...document.querySelectorAll("[id]")].map(e=>e.id)).size===document.querySelectorAll("[id]").length'))
                    for width in (320,390,768):
                        page.set_viewport_size({'width':width,'height':1100})
                        check('expanded coordinated result fits viewport '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                    page.set_viewport_size({'width':390,'height':1000});page.screenshot(path=str(OUT/'8BALL-Coordinated-Result-Mobile.png'),full_page=True)
                    page.set_viewport_size({'width':1500,'height':1100});page.screenshot(path=str(OUT/'8BALL-Coordinated-Result.png'),full_page=True)
                    check('coordinated inspection performs no writes',writes==[] and store.audit(coordinated.id)==before)
                    store.change(coordinated.id,Command(event_id='coordination-stale',expected_revision=0,kind='metadata',payload={'budget':444}))
                    page.get_by_role('button',name='Refresh review').click();expect(result).to_contain_text('Historical result for case revision 0; current revision 1')
                    check('coordinated stale result is historical not current',page.locator('#review-rationale').is_disabled())
                    open_review(partial_plan,partial_plan_work);login();expect(result).to_contain_text('specialist_review_incomplete')
                    expect(result).to_contain_text('1 of 3 selected models answered')
                    check('incomplete panel does not invent revision or agreement','No validated candidate retained' in result.locator('.coordinated-proposal').nth(1).inner_text() and result.locator('.specialist-answers').inner_text().count('No validated answer')==2)
                    open_review(failed_plan,failed_plan_work);login();expect(result).to_contain_text('invalid_revision_draft')
                    check('rejected revision retains original challenge and diagnostic',result.locator('.coordinated-proposal').first.get_by_text('Conditional approaches',exact=True).count()==1 and result.locator('.coordinated-failure').count()==1 and 'string_too_long' in result.inner_text())
                    open_review(invalid_plan,invalid_plan_work);login();expect(page.locator('#app')).to_contain_text('Coordinated result could not be validated')
                    check('invalid coordinated summary leaves only original output',result.count()==0 and '"disagreement": false' in page.get_by_label('Original processing output',exact=True).inner_text())
                    open_review(initial_failure,initial_failure_work);login();expect(result).to_contain_text('invalid_initial_draft')
                    check('failed proposer invents neither original nor challenge',result.locator('.coordinated-proposal').first.inner_text().count('No validated candidate retained')==1 and 'No validated challenge panel retained' in result.inner_text() and result.locator('.specialist-comparison').count()==0)
                    open_review(invalid_hash,invalid_hash_work);login();expect(page.locator('#app')).to_contain_text('Coordinated result could not be validated')
                    check('invalid source hash withholds stages not raw result',result.count()==0 and 'f'*64 in page.get_by_label('Original processing output',exact=True).inner_text())
                    open_review(coordinated,coordinated_work);login();page.get_by_role('button',name='Lock review').click()
                    check('lock clears every coordinated stage',result.count()==0 and page.locator('.review-originals').count()==0)
                    login();registry.revoke('read3');page.get_by_role('button',name='Refresh review').click();expect(page.locator('#review-login')).to_be_visible()
                    check('revocation clears coordinated stages and raw output',result.count()==0 and page.locator('.review-originals').count()==0)
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
