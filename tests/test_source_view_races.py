"""Deterministic scheduling tests for the actual Source Desk view module.

A minimal DOM adapter supplies event targets; deferred promises control delivery.
These are component tests, not substitutes for the native browser journey.
"""
from pathlib import Path
import json
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
HARNESS = r'''
import assert from 'node:assert/strict';
import {S} from __UI__;
import * as view from __VIEW__;
const listeners={}, pending=[];
let renders=0, removed=0;
const toast={setAttribute(){},className:'',textContent:''};
let query, html='', reader={value:''};
function field(value=''){
 const form={dataset:{sourceForm:'search',sourceCase:S.current.case.id,sourceDocument:S.sourceDesk.page.document.id}};
 const el={id:'sd-query',value,selectionStart:2,selectionEnd:5,selectionDirection:'forward',
  closest:()=>form,focus(){document.activeElement=this;},setSelectionRange(start,end,direction){this.selectionStart=start;this.selectionEnd=end;this.selectionDirection=direction;}};
 form.elements={query:el};form.querySelector=()=>null;
 return el;
}
globalThis.document={activeElement:null,addEventListener(name,fn){listeners[name]=fn;},
 querySelector(sel){return sel==='#toast'?toast:sel==='#sd-query'?query:sel==='#sd-reader'?reader:sel==='.sd-search-results'?{remove(){removed++;}}:null;}};
globalThis.FormData=class{constructor(form){this.form=form;}*[Symbol.iterator](){yield ['query',this.form.elements.query.value];}};
// Toast expiry is irrelevant to component assertions and must not keep Node alive.
globalThis.setTimeout=()=>0;globalThis.clearTimeout=()=>{};
const makePage=id=>({document:{id,title:id,source:'Fictional source',status:'active',characters:20,
 content_sha256:'a'.repeat(64),filename:null,created_at:'2026-09-26T00:00:00Z',warnings:[]},text:'Fictional original.',
 start:0,end:19,chunks:[],line_start:1,line_end:1,partial:false});
S.current={case:{id:'case-A',revision:1}};S.epoch=1;S.tab='evidence';
S.sourceDesk={caseId:'case-A',open:true,index:{documents:[]},page:makePage('doc-A'),query:'',matches:[],selected:[]};
query=field();
function render(){
 const focus=view.captureSourceFocus?.();
 html=view.sourceDeskView();renders++;
 query=field(S.sourceDesk.query);document.activeElement=null;view.mountSourceReader(focus);
}
view.bindSourceDesk({render,refreshCases:async()=>{},api(path){return new Promise(resolve=>pending.push({path,resolve}));}});
const click=(action,extra={})=>listeners.click({preventDefault(){},target:{closest(){return {dataset:{sourceAction:action,...extra}};}}});
const type=value=>{query.value=value;document.activeElement=query;listeners.input?.({target:query});};
const submit=()=>listeners.submit({preventDefault(){},target:query.closest()});
const tick=async()=>{for(let i=0;i<8;i++)await Promise.resolve();};
const matches=value=>({matches:[{start:4,context_start:0,context_end:19,context:value}],truncated:false});
'''

CASES = {
    'typing_survives_delayed_index_and_page': r'''
const opening=click('open');type('UNSELECTED-SENTINEL');
pending.shift().resolve({documents:[]});await tick();
assert.equal(query.value,'UNSELECTED-SENTINEL');
pending.shift().resolve(makePage('doc-A'));await opening;
assert.equal(query.value,'UNSELECTED-SENTINEL');assert(html.includes('value="UNSELECTED-SENTINEL"'));
''',
    'editing_invalidates_old_search_without_rewriting_new_query': r'''
type('old');const searching=submit();type('new');
pending.shift().resolve(matches('old result'));await searching;
assert.equal(S.sourceDesk.query,'new');assert.deepEqual(S.sourceDesk.matches,[]);
assert.equal(query.value,'new');
''',
    'same_document_refresh_cannot_cancel_search': r'''
const opening=click('open');type('needle');const searching=submit();
const index=pending.shift(),search=pending.shift();index.resolve({documents:[]});await tick();
const page=pending.shift();search.resolve(matches('needle'));await searching;
page.resolve(makePage('doc-A'));await opening;
assert.equal(S.sourceDesk.matches.length,1);assert.equal(S.sourceDesk.query,'needle');
''',
    'reopening_cannot_supersede_later_document_choice': r'''
const opening=click('open'),index=pending.shift();
const navigating=click('document',{id:'doc-B'}),other=pending.shift();
index.resolve({documents:[]});await opening;
assert.equal(pending.length,0,'outdated open must not request old document');
other.resolve(makePage('doc-B'));await navigating;assert.equal(S.sourceDesk.page.document.id,'doc-B');
''',
    'closing_invalidates_inflight_search': r'''
type('needle');const searching=submit(),response=pending.shift();
await click('evidence');const before=renders;response.resolve(matches('needle'));await searching;
assert.deepEqual(S.sourceDesk.matches,[]);assert.equal(renders,before);
''',
    'switching_tabs_cannot_publish_old_search': r'''
type('needle');const searching=submit(),response=pending.shift();S.tab='room';
response.resolve(matches('needle'));await searching;
assert.deepEqual(S.sourceDesk.matches,[]);assert.equal(renders,0);
''',
    'input_from_old_document_cannot_change_current_query': r'''
const stale=query;S.sourceDesk.page=makePage('doc-B');S.sourceDesk.query='current';
stale.value='old context';listeners.input?.({target:stale});
assert.equal(S.sourceDesk.query,'current');
''',
    'case_change_rejects_search_and_pending_document': r'''
type('needle');const searching=submit(),response=pending.shift();
const opening=click('document',{id:'doc-B'}),documentResponse=pending.shift();
view.clearSourceDesk();S.current={case:{id:'case-B',revision:0}};S.epoch++;
response.resolve(matches('secret from A'));documentResponse.resolve(makePage('doc-B'));
await Promise.all([searching,opening]);assert.equal(S.sourceDesk,null);assert.equal(renders,0);
''',
    'new_query_removes_stale_visible_results': r'''
S.sourceDesk.matches=matches('old result').matches;S.sourceDesk.searchTruncated=true;
type('new');assert.deepEqual(S.sourceDesk.matches,[]);assert.equal(S.sourceDesk.searchTruncated,false);
assert.equal(removed,1);assert.equal(pending.length,0,'typing is not auto-analysis or a request');
''',
    'refresh_preserves_keyboard_focus_and_selection': r'''
type('find me');query.selectionStart=1;query.selectionEnd=4;
render();assert.equal(document.activeElement,query);assert.equal(query.value,'find me');
assert.equal(query.selectionStart,1);assert.equal(query.selectionEnd,4);
''',
    'different_document_cannot_restore_previous_focus': r'''
type('find me');const focus=view.captureSourceFocus?.();S.sourceDesk.page=makePage('doc-B');
query=field();document.activeElement=null;view.mountSourceReader(focus);
assert.equal(document.activeElement,null);
''',
    'latest_of_two_searches_wins': r'''
type('first');const first=submit(),a=pending.shift();type('second');const second=submit(),b=pending.shift();
b.resolve(matches('second result'));await second;a.resolve(matches('first result'));await first;
assert.equal(S.sourceDesk.query,'second');assert.equal(S.sourceDesk.matches[0].context,'second result');
''',
}

@pytest.mark.parametrize('case_name', CASES)
def test_source_view_request_ordering(case_name):
    assert shutil.which('node'), 'Node is required for browser-module regression tests'
    code = HARNESS.replace('__UI__', json.dumps((ROOT/'web/v2/ui.js').as_uri())).replace(
        '__VIEW__', json.dumps((ROOT/'web/v2/source-view.js').as_uri())) + CASES[case_name]
    result = subprocess.run(['node', '--input-type=module', '-e', code],
                            capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stdout + result.stderr
