"""Source Desk operator journey over actual API/SQLite.
Native HTTP by default; explicit bridge does not verify browser transport, storage
or native downloads. No model service or mocked model responses are used.
"""
from pathlib import Path
from datetime import timedelta
import json,os,subprocess,sys,tempfile,time,shutil
import httpx
from playwright.sync_api import sync_playwright,expect

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from browser_v2 import open_document,BRIDGE,TOKEN
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.contracts import Case
from eightball.models import utcnow

OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/sources')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,value):
    assert value,name
    checks.append(name)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'case.db');store=Store(db)
        c=store.create(demo_case(),fixture=True)
        other=store.create(Case(title='Separate client fixture',client='Other test client',summary='Separate case',desired_outcome='Another outcome',deadline=utcnow()+timedelta(days=1)))
        original=('\ufeffNORTHSTAR / INCIDENT REVIEW\r\n'
                  'PREPARED BY: Fictional technical lead\r\n'
                  'ACKNOWLEDGEMENT: Received 🤝\r\n\r\n'
                  'The root cause has NOT been verified.\r\n'
                  'No customer acceptance has been established.\r\n\r\n'
                  '01 / CURRENT PICTURE\r\n'
                  'The service is stable under temporary controls. The investigation remains open. '
                  'The case lead is preparing a factual interim report for professional review.\r\n\r\n')
        original+='\r\n'.join(f'{i:02d} / REVIEW NOTE\r\nA fictional source note preserves the investigation record without treating an untested hypothesis as a verified fact. '*7 for i in range(2,31))
        original+='\r\nPRIVATE APPENDIX / UNSELECTED-SENTINEL\r\n<script>window.sourceAttack=true</script>'
        initial_evidence=len(c.evidence);before=store.audit(c.id)
        proc=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(60):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',timeout=1,trust_env=False).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            with sync_playwright() as pw:
                browser=pw.chromium.launch(executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),headless=True,args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1512,'height':1050},device_scale_factor=1)
                page.set_default_timeout(12000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                try:
                    open_document(page,db)
                    page.locator('[name=token]').fill(TOKEN);page.locator('form[data-form=login] [type=submit]').click()
                    page.locator(f'[data-case="{c.id}"]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                    page.locator('nav [data-tab=evidence]').click();expect(page.locator('nav [data-tab=evidence]')).to_have_attribute('aria-current','page')
                    page.locator('[data-source-action=open]').click();expect(page.locator('.sd-workspace')).to_be_visible()
                    check('source desk opens inside evidence without removing existing excerpts',store.audit(c.id)==before)
                    page.locator('[data-source-action=import]').first.click()
                    f=page.locator('form[data-source-form=import-preview]')
                    f.locator('[name=title]').fill('Northstar incident review · full original')
                    f.locator('[name=source]').fill('Fictional technical lead')
                    f.locator('[name=file]').set_input_files({'name':'northstar-review.txt','mimeType':'text/plain','buffer':original.encode('utf-8')})
                    expect(page.locator('#sd-file-note')).to_contain_text('File text and line endings retained')
                    check('file is loaded as retained text, not truncated to old excerpt limit',len(original)>12000)
                    f.locator('[type=submit]').click();page.get_by_role('heading',name='Review this source import').wait_for()
                    check('import preview has no case or evidence effect',store.audit(c.id)==before)
                    page.locator('form[data-source-form=import-commit] [type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    expect(page.locator('#sd-reader')).to_be_visible();expect(page.locator('.sd-document')).to_have_count(1)
                    imported=store.audit(c.id);doc=imported['source_documents'][0]
                    check('UTF-8 BOM emoji and CRLF source survive exact import',doc['text']==original)
                    check('import is anchored as one case revision',store.get(c.id).revision==1)
                    check('import does not create evidence observations or model work',len(store.get(c.id).evidence)==initial_evidence and store.get(c.id).observations==c.observations and not store.proposals(c.id))
                    check('original hash and inventory verify in audit',imported['valid'] and imported['source_integrity']['documents']==1)
                    check('reader identifies partial source and explicit positions','Showing part of the original' in page.locator('.sd-read-controls').inner_text())
                    # Textarea uses UTF-16 and normalises CRLF. Mapping must return original code-point offsets.
                    phrase='The root cause has NOT been verified.'
                    page.locator('#sd-reader').evaluate('(el,phrase)=>{const i=el.value.indexOf(phrase);el.focus();el.setSelectionRange(i,i+phrase.length);}',phrase)
                    page.locator('[data-source-action=select-text]').click();expect(page.locator('.sd-cart-item')).to_have_count(1)
                    check('selection is read-only and cannot attest a fact',store.audit(c.id)==imported)
                    check('selected text preserves negation',phrase in page.locator('.sd-cart-item').inner_text())
                    page.locator('#toast.visible').wait_for(state='hidden')
                    page.screenshot(path=str(OUT/'8BALL-Source-Desk.png'),full_page=False)
                    page.locator('[data-source-action=preview-capture]').click();page.get_by_role('heading',name='Capture exact evidence passages').wait_for()
                    check('capture requires a separate review',store.audit(c.id)==imported)
                    check('review shows exact selected text only',phrase in page.locator('.sd-capture-preview pre').inner_text() and 'UNSELECTED-SENTINEL' not in page.locator('.dialog').inner_text())
                    page.screenshot(path=str(OUT/'8BALL-Source-Passage-Review.png'),full_page=False)
                    page.locator('form[data-source-form=capture-commit] [type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    expect(page.locator('.source-card')).to_have_count(initial_evidence+1)
                    current=store.get(c.id);last=current.evidence[-1]
                    check('capture creates unreviewed evidence not a fact',last.text==phrase and last.status=='unreviewed' and current.observations==c.observations)
                    link=store.audit(c.id)['source_passages'][0]
                    check('selection maps through emoji CRLF into original Unicode offsets',original[link['start']:link['end']]==phrase and link['start']==original.index(phrase))
                    page.locator('.source-card').last.locator('[data-source-action=origin]').click();page.get_by_role('heading',name='Trace this evidence to the original').wait_for()
                    check('evidence opens an exact original source link',phrase in page.locator('.dialog .source-text').inner_text())
                    page.screenshot(path=str(OUT/'8BALL-Source-Origin.png'),full_page=False)
                    page.locator('.dialog [data-action=close]').click()
                    # Source review and explicit false attestation are still necessary.
                    page.locator('.source-card').last.locator('[data-action=review-source]').click();page.locator('form[data-form=source-review] [type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    page.locator('.source-card').last.locator('[data-action=observe]').click();f=page.locator('form[data-form=observe]')
                    f.locator('[name=condition_id]').select_option('root');f.locator('[name=value]').select_option('false');f.locator('[name=rationale]').fill('The original explicitly states the root cause has not been verified.');f.locator('[type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    check('human false attestation is recorded separately',store.get(c.id).observations[-1].value is False)
                    page.locator('[data-source-action=open]').click();expect(page.locator('#sd-reader')).to_be_visible()
                    # Literal search gets the final appendix despite only displaying one page.
                    search=page.locator('form[data-source-form=search]');search.locator('[name=query]').fill('UNSELECTED-SENTINEL');search.locator('[type=submit]').click();expect(page.locator('.sd-search-results>button')).to_have_count(1)
                    page.locator('.sd-search-results>button').click();expect(page.locator('#sd-reader')).to_have_value(__import__('re').compile('.*UNSELECTED-SENTINEL.*',__import__('re').S))
                    check('whole original search reaches text beyond displayed page',True)
                    check('source HTML is displayed as text not executed',page.evaluate('window.sourceAttack===undefined'))
                    unchanged=store.audit(c.id)
                    # Export full stored text, not just the current window.
                    if not BRIDGE:
                        with page.expect_download() as d:page.locator('[data-source-action=export]').click()
                        exported=Path(d.value.path()).read_bytes().decode('utf-8')
                    else:
                        page.evaluate("()=>{window.URL.createObjectURL=b=>{window.__sourceExport=b.arrayBuffer().then(bytes=>Array.from(new Uint8Array(bytes)));return 'blob:source-test'};HTMLAnchorElement.prototype.click=function(){};}")
                        page.locator('[data-source-action=export]').click()
                        page.wait_for_function('window.__sourceExport!==undefined')
                        exported=bytes(page.evaluate('window.__sourceExport')).decode('utf-8')
                    check('export contains the complete stored text not just visible passage',exported==original)
                    check('reading search and export leave case audit unchanged',store.audit(c.id)==unchanged)
                    # Duplicate check is explicit and separate from case identity.
                    page.locator('[data-source-action=import]').first.click();f=page.locator('form[data-source-form=import-preview]')
                    f.locator('[name=title]').fill('Duplicate delivery from client');f.locator('[name=source]').fill('Fictional account director')
                    f.locator('[name=file]').set_input_files({'name':'same-original.txt','mimeType':'text/plain','buffer':original.encode('utf-8')});expect(page.locator('#sd-file-note')).to_contain_text('line endings retained')
                    f.locator('[type=submit]').click();page.get_by_role('heading',name='Review this source import').wait_for()
                    check('duplicate text is detected before a write','Exact text match' in page.locator('.dialog').inner_text())
                    check('duplicate needs explicit separate provenance reason',page.locator('[name=record_separately]').get_attribute('required') is not None and page.locator('[name=duplicate_reason]').get_attribute('required') is not None)
                    page.screenshot(path=str(OUT/'8BALL-Source-Duplicate-Review.png'),full_page=False)
                    page.locator('.dialog [data-action=close]').click();check('cancelling duplicate import does not merge or add a source',len(store.audit(c.id)['source_documents'])==1)
                    # Corrected version is linked, never a silent replacement.
                    page.locator('[data-source-action=import]').first.click();f=page.locator('form[data-source-form=import-preview]')
                    f.locator('[name=title]').fill('Northstar review · corrected version');f.locator('[name=source]').fill('Fictional technical lead')
                    f.locator('[name=file]').set_input_files({'name':'prior.txt','mimeType':'text/plain','buffer':b'Previously chosen file'})
                    expect(page.locator('#sd-file-note')).to_contain_text('line endings retained')
                    f.locator('[name=file]').set_input_files({'name':'unsupported.bin','mimeType':'application/octet-stream','buffer':b'bad'})
                    expect(page.locator('#toast')).to_contain_text('Choose a UTF-8')
                    check('invalid replacement file clears prior loaded original',f.locator('[name=text]').input_value()=='' and len(store.audit(c.id)['source_documents'])==1)
                    f.locator('[data-source-action=paste-mode]').click()
                    check('switching to paste explicitly resets file selection',f.locator('[name=file]').input_value()=='' and f.locator('[name=text]').is_editable())
                    f.locator('[name=text]').fill('Corrected report: the root cause remains under investigation.');f.locator('[name=previous_document_id]').select_option(doc['id']);f.locator('[type=submit]').click()
                    page.get_by_role('heading',name='Review this source import').wait_for();page.locator('form[data-source-form=import-commit] [type=submit]').click();page.locator('.dialog').wait_for(state='detached');expect(page.locator('.sd-version-link')).to_be_visible()
                    originals=store.audit(c.id)['source_documents'];check('linked version retains both original texts and statuses',len(originals)==2 and originals[0]['status']=='active' and originals[1]['previous_document_id']==doc['id'])
                    page.locator('.sd-version-link [data-source-action=document]').click();expect(page.locator('.sd-reader-head h2')).to_have_text(doc['title'])
                    # Retraction goes through a separate review and reaches linked evidence.
                    page.locator('[data-source-action=retract]').click();page.locator('form[data-source-form=retract] [name=reason]').fill('Superseded working copy, retain history for review.');page.locator('form[data-source-form=retract] [type=submit]').click();page.locator('.dialog').wait_for(state='detached')
                    expect(page.locator('.sd-reader-head .badge')).to_contain_text('Historical')
                    state=store.get(c.id);check('retracting original retracts linked evidence but keeps observations',next(e for e in state.evidence if e.id==last.id).status=='retracted' and len(state.observations)==len(c.observations)+1)
                    check('original text is retained after retraction',store.audit(c.id)['source_documents'][0]['text']==original)
                    from eightball.v2.planner import plan
                    check('retracted original removes support from dependent condition',plan(state)['states']['root']['status']=='unknown')
                    check('retracted source and excerpt hashes still verify',store.audit(c.id)['valid'])
                    # Mobile + keyboard interaction, no horizontal document overflow.
                    page.set_viewport_size({'width':390,'height':844});check('source desk fits 390px viewport',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                    expect(page.locator('#toast')).not_to_be_visible(timeout=8000)
                    page.screenshot(path=str(OUT/'8BALL-Source-Desk-Mobile.png'),full_page=True)
                    page.locator('#sd-reader').focus();page.keyboard.press('Tab');check('keyboard can leave the source reader',page.evaluate('document.activeElement.id!=="sd-reader"&&document.activeElement!==document.body'))
                    page.set_viewport_size({'width':1512,'height':1050});check('source desk fits 1512px viewport',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                    page.locator('nav [data-tab=command]').click();page.locator(f'[data-case="{other.id}"]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                    page.locator('nav [data-tab=evidence]').click();page.locator('[data-source-action=open]').click();expect(page.locator('.sd-library-list')).to_contain_text('No originals stored yet')
                    check('switching cases clears source reader and selection',page.locator('#sd-reader').count()==0 and page.locator('.sd-cart-item').count()==0 and doc['title'] not in page.locator('main').inner_text())
                    if not BRIDGE:
                        page.reload();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                        check('native session restores correct case after source work','Separate client fixture' in page.locator('main').inner_text())
                    check('no browser runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'explicit ASGI bridge' if BRIDGE else 'native HTTP',
                            'native_storage_and_download_verified':not BRIDGE,'real_sqlite':True,'model_inference_tested':False,
                            'original_characters':len(original),'errors':errors}
                    (OUT/'source-browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'),full_page=True);(OUT/'failure.html').write_text(page.content());print('Runtime errors',errors);raise
                finally:browser.close()
        finally:
            proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill()

if __name__=='__main__':main()
