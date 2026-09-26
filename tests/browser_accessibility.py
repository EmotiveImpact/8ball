"""Focused keyboard/semantic regression checks. Not a WCAG certification.

Uses native browser transport by default. Explicit bridge tests only rendering
and interaction against the application; real assistive-technology review is
still required. No axe engine, models or external services are invoked.
"""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile,time
import httpx
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from browser_v2 import open_document,BRIDGE,TOKEN
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
OUT=Path(os.getenv('EIGHTBALL_ARTIFACTS',str(ROOT/'artifacts/accessibility')));OUT.mkdir(parents=True,exist_ok=True)
checks=[]

def check(name,value):
    assert value,name
    checks.append(name)

AUDIT=r'''() => {
 const visible=e=>e.getClientRects().length>0&&!e.closest('[inert]');
 const labelled=e=>Boolean(e.getAttribute('aria-label')?.trim()||e.getAttribute('title')?.trim()||
 (e.getAttribute('aria-labelledby')??'').split(/\s+/).some(id=>document.getElementById(id)?.textContent.trim())||
 [...(e.labels??[])].some(l=>l.textContent.trim()));
 const missing=[...document.querySelectorAll('input:not([type=hidden]),textarea,select')]
  .filter(e=>visible(e)&&!labelled(e)).map(e=>e.outerHTML.slice(0,170));
 const buttons=[...document.querySelectorAll('button')].filter(e=>visible(e)&&!e.textContent.trim()&&!labelled(e)).map(e=>e.outerHTML.slice(0,170));
 const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
 return {missing,buttons,duplicate_ids:ids.filter((id,i)=>ids.indexOf(id)!==i),
  positive_tabindex:[...document.querySelectorAll('[tabindex]')].filter(e=>Number(e.tabIndex)>0).length,
  active:document.activeElement?.tagName,main:document.querySelectorAll('main').length};
}'''


def main():
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/'cases.db');store=Store(db);case=store.create(demo_case(),fixture=True);before=store.audit(case.id)
        process=subprocess.Popen([sys.executable,'-m','eightball'],cwd=ROOT,env={**os.environ,'EIGHTBALL_DB':db,'EIGHTBALL_TOKEN':TOKEN},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(80):
                try:
                    if httpx.get('http://127.0.0.1:8048/api/health',trust_env=False,timeout=1).status_code==200:break
                except httpx.HTTPError:pass
                time.sleep(.1)
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                try:
                    open_document(page,db);page.locator('[name=token]').fill(TOKEN);page.locator('form[data-form=login] [type=submit]').click()
                    page.locator(f'[data-case="{case.id}"]').click();expect(page.locator('nav [data-tab=room]')).to_have_attribute('aria-current','page')
                    tabs=page.locator('nav [data-tab]').evaluate_all('(els)=>els.map(e=>e.dataset.tab)')
                    audits={}
                    for tab in tabs:
                        page.locator(f'nav [data-tab="{tab}"]').focus();page.keyboard.press('Enter')
                        expect(page.locator(f'nav [data-tab="{tab}"]')).to_have_attribute('aria-current','page')
                        # Async rendering must move focus to the destination title.
                        expect(page.locator('#main h1')).to_be_focused()
                        audit=page.evaluate(AUDIT);audits[tab]=audit
                        check('labelled controls and unique IDs: '+tab,not audit['missing'] and not audit['buttons'] and not audit['duplicate_ids'] and not audit['positive_tabindex'] and audit['main']==1)
                    page.locator('nav [data-tab=room]').click();expect(page.locator('#main h1')).to_be_focused()
                    opener=page.locator('[data-action=metadata]');opener.focus();page.keyboard.press('Enter')
                    dialog=page.get_by_role('dialog',name='Situation details & constraints');expect(dialog).to_be_visible()
                    expect(page.locator('#eightball-dialog-title')).to_be_focused()
                    check('modal has visible accessible title and inert background',page.locator('#app').evaluate('(e)=>e.inert'))
                    page.keyboard.press('Tab');check('title proceeds to close control',page.locator('.dialog [data-action=close]').evaluate('(e)=>e===document.activeElement'))
                    page.keyboard.press('Shift+Tab');check('reverse tab stays inside dialog',page.evaluate("Boolean(document.activeElement.closest('.dialog'))"))
                    page.keyboard.press('Tab');check('last-to-first wrap stays inside dialog',page.evaluate("Boolean(document.activeElement.closest('.dialog'))"))
                    page.keyboard.press('Escape');expect(opener).to_be_focused();check('escape restores original invoker',page.locator('.dialog').count()==0)
                    # A route opens a second modal from within the comparison.
                    page.locator('nav [data-tab=routes]').click();expect(page.locator('#main h1')).to_be_focused()
                    page.locator('[data-route-select]').nth(0).check();page.locator('[data-route-select]').nth(1).check()
                    page.locator('[data-action=compare]').click();page.get_by_role('heading',name='Compare the ways through').wait_for()
                    page.locator('.dialog [data-action=route-detail]').first.click();page.keyboard.press('Escape')
                    expect(page.locator('[data-action=compare]')).to_be_focused();check('replaced dialog restores original workspace invoker',True)
                    # Resize/reflow rather than hiding controls from keyboard users.
                    for width in [320,390,768]:
                        page.set_viewport_size({'width':width,'height':1000});page.locator('nav [data-tab=room]').click()
                        expect(page.locator('#main h1')).to_be_focused()
                        check('room fits narrow viewport '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                    page.set_viewport_size({'width':1440,'height':1000})
                    page.screenshot(path=str(OUT/'8BALL-Integrated-Workspace.png'),full_page=True)
                    check('reduced motion is honoured',page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches"))
                    page.locator('[data-action=metadata]').click();f=page.locator('[data-form=metadata]');f.locator('[name=title]').fill('')
                    f.locator('[type=submit]').click();check('invalid required form remains open',page.locator('.dialog').count()==1)
                    check('invalid form did not alter case state',store.audit(case.id)==before)
                    check('native validity is exposed to assistive technology',f.locator('[name=title]').evaluate('(e)=>e.validity.valueMissing'))
                    page.keyboard.press('Escape');check('no runtime errors',not errors)
                    report={'checks_passed':len(checks),'checks':checks,'network':'Explicit ASGI bridge' if BRIDGE else 'Native loopback HTTP',
                            'audits':audits,'errors':errors,'model_inference_tested':False,'real_sqlite':True,
                            'human_screen_reader_tested':False,'wcag_conformance_claimed':False,
                            'limits':['Focused native-control and keyboard checks, not comprehensive accessibility certification.',
                                      'No human screen-reader, motor-access or inclusive user study has been performed.']}
                    (OUT/'accessibility-browser-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'),full_page=True);(OUT/'failure.html').write_text(page.content());print('Runtime errors:',errors);raise
                finally:browser.close()
        finally:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait()


if __name__=='__main__':main()
