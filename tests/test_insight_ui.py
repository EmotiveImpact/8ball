"""Actual UI module/state boundaries tested with Node. These are not native
browser/network tests; full interaction tests live in browser_insights.py.
"""
from pathlib import Path
import json,subprocess
import pytest
ROOT=Path(__file__).resolve().parents[1]
MODULE=(ROOT/'web/v2/insights-view.js').as_uri()
UI=(ROOT/'web/v2/ui.js').as_uri()
CHECKS={
 'late_case_response_is_dropped': "let finish;S.current={case:{id:'one'}};const pending=loadInsights(()=>new Promise(r=>finish=r));S.current={case:{id:'two'}};finish({items:[{secret:'one'}]});await pending;assert.equal(S.insights,null);",
 'late_locked_session_response_is_dropped': "let finish;S.current={case:{id:'one'}};const pending=loadInsights(()=>new Promise(r=>finish=r));S.epoch++;S.current=null;finish({items:[{secret:'one'}]});await pending;assert.equal(S.insights,null);",
 'current_response_updates_only_its_case': "S.current={case:{id:'one'}};let path;await loadInsights(async x=>{path=x;return {case_revision:4,items:[]}});assert.equal(path,'/cases/one/insights');assert.equal(S.insights.case_revision,4);",
 'no_case_means_no_request': "S.current=null;let called=false;await loadInsights(async()=>called=true);assert.equal(called,false);",
 'clearing_discards_case_data': "S.insights={items:[{text:'client'}]};clearInsights();assert.equal(S.insights,null);",
 'build_register_retains_every_entry': "S.buildDiscoveries={...input.register,task_states:input.states};const html=buildDiscoveriesPage();assert.equal((html.match(/<article class=/g)||[]).length,input.register.items.length);for(const i of input.register.items)assert(html.includes(i.id));",
 'build_register_escapes_untrusted_idea': "const r=structuredClone(input.register);r.items[0].title='<script>window.attack=true</script>';S.buildDiscoveries={...r,task_states:input.states};const html=buildDiscoveriesPage();assert(!html.includes('<script>'));assert(html.includes('&lt;script&gt;'));",
 'adoption_without_verified_scope_stays_unchecked': "const r=structuredClone(input.register);r.items=r.items.filter(i=>i.history.at(-1).decision==='adopted'&&i.acceptance_task_ids.length).slice(0,1);const states=Object.fromEntries(Object.keys(input.states).map(k=>[k,'implemented']));S.buildDiscoveries={...r,task_states:states};assert(!buildDiscoveriesPage().includes('☑'));assert(buildDiscoveriesPage().includes('☐'));",
 'question_detail_response_cannot_replace_newly_selected_case': r"""
 const listeners={};globalThis.document={addEventListener:(name,fn)=>listeners[name]=fn};
 globalThis.FormData=class {constructor(){}*[Symbol.iterator](){yield ['question','Verify?'];yield ['owner','Lead'];yield ['reason','Check the source'];}};
 S.current={case:{id:'one',revision:0}};S.epoch=0;let finish,resolveRequested;const requested=new Promise(r=>resolveRequested=r);let refreshes=0;
 bindInsights({api:async path=>{if(path.endsWith('/insights/question'))return {insights:{case_revision:1,items:[]}};resolveRequested();return new Promise(r=>finish=r);},render:()=>{},refreshCases:async()=>refreshes++});
 const btn={disabled:false,isConnected:false};const form={dataset:{insightForm:'question',caseId:'one',caseRevision:'0',insightRevision:'1',eventId:'fixture',id:'insight',fingerprint:'a'.repeat(64)},querySelector:()=>btn};
 const pending=listeners.submit({target:form,preventDefault(){}});await requested;S.current={case:{id:'two',revision:0}};finish({case:{id:'one',revision:1}});await pending;assert.equal(S.current.case.id,'two');assert.equal(refreshes,0);
 """,
}
@pytest.mark.parametrize('name',CHECKS)
def test_insight_ui_boundaries(name):
 data={'register':json.loads((ROOT/'docs/delivery/emergence.json').read_text()),
       'states':{t['id']:t['status'] for t in json.loads((ROOT/'docs/delivery/progress.json').read_text())['tasks']}}
 code=f"import assert from 'node:assert/strict';import fs from 'node:fs';import {{S}} from {json.dumps(UI)};import {{loadInsights,clearInsights,buildDiscoveriesPage,bindInsights}} from {json.dumps(MODULE)};const input=JSON.parse(fs.readFileSync(0,'utf8'));clearInsights();"+CHECKS[name]
 result=subprocess.run(['node','--input-type=module','-e',code],input=json.dumps(data),capture_output=True,text=True,timeout=10)
 assert result.returncode==0,result.stderr
