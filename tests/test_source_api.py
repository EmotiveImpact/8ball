"""API limits, original storage and explicit evidence integration. No live AI."""
import asyncio
from datetime import timedelta
import json
from pathlib import Path
import subprocess

import httpx
import pytest
from fastapi.testclient import TestClient
from eightball.api import make_app
from eightball.store import Store as LegacyStore
from eightball.v2.store import Store
from eightball.v2.source_contracts import text_hash, SOURCE_BODY_LIMIT
from eightball.v2.request_limits import BoundedRequestBody,body_limit
from eightball.models import uid,utcnow

TOKEN='source-api-local-operator-token-1234567890'

@pytest.fixture
def setup(tmp_path):
    old=LegacyStore(str(tmp_path/'case.db'));store=Store(old.path)
    cl=TestClient(make_app(old,TOKEN),headers={'Authorization':'Bearer '+TOKEN})
    c=cl.post('/api/v2/cases',json={'title':'Source test','client':'Fictional client','summary':'A fictional situation','desired_outcome':'Verified recovery',
                'deadline':(utcnow()+timedelta(days=1)).isoformat(),'budget':10000}).json()
    return store,cl,c


def source_body(c,text='UTF-8 source 👋\r\nStill not accepted.'):
    return {'event_id':uid(),'expected_revision':c['revision'],'title':'Text original','source':'Test sender','text':text}


def import_api(cl,c,text=None):
    body=source_body(c,**({'text':text} if text is not None else {}))
    r=cl.post(f"/api/v2/cases/{c['id']}/sources/import",json=body)
    assert r.status_code==201,r.text
    return r.json(),body


def test_full_api_import_selection_capture_origin_export(setup):
    store,cl,c=setup;base=f"/api/v2/cases/{c['id']}/sources"
    out,body=import_api(cl,c);c=out['case'];doc=out['document']
    assert not c['evidence'] and not c['observations']
    p=cl.get(base+'/'+doc['id']).json();assert p['text']==body['text']
    selection=cl.post(base+'/'+doc['id']+'/selection',json={'start':0,'end':8}).json()
    body={'event_id':uid(),'expected_revision':c['revision'],'passages':[{'document_id':doc['id'],'start':0,'end':8,'content_sha256':selection['content_sha256']}]}
    preview=cl.post(base+'/passages/preview',json={k:v for k,v in body.items() if k!='event_id'})
    assert preview.json()['persisted'] is False
    out=cl.post(base+'/passages',json=body);assert out.status_code==200,out.text
    c=out.json()['case'];e=c['evidence'][0]
    assert e['status']=='unreviewed'
    origin=cl.get(base+'/origin/'+e['id']).json();assert origin['linked'] and origin['text']==e['text']
    quote=cl.post(base+'/resolve-span',json={'evidence_id':e['id'],'start':0,'end':5,'quote':e['text'][:5]}).json()
    assert quote['original_start']==0
    exported=cl.get(f"/api/v2/cases/{c['id']}/export").json()
    assert exported['valid'] and exported['source_integrity']['valid'] and exported['source_documents'][0]['text']==p['text']


def test_up_to_200k_unicode_text_import_not_small_body_limit(setup):
    _,cl,c=setup;text='🤝'*199999
    body=json.dumps(source_body(c,text),ensure_ascii=False).encode('utf-8')
    assert len(body)>300000
    out=cl.post(f"/api/v2/cases/{c['id']}/sources/import",content=body,headers={'Content-Type':'application/json'})
    assert out.status_code==201,out.text
    assert out.json()['document']['characters']==199999


def test_only_source_import_routes_have_larger_body_allowance(setup):
    _,cl,c=setup
    assert body_limit(f"/api/v2/cases/{c['id']}/sources/import")==SOURCE_BODY_LIMIT
    assert body_limit('/api/v2/cases/id/sources/import/anything')==300000
    assert body_limit('/api/v2/cases/id/sources/passages')==300000
    r=cl.post(f"/api/v2/cases/{c['id']}/commands",json={'x':'x'*300001})
    assert r.status_code==413


def test_oversize_body_rejected_before_parsing(setup):
    _,cl,c=setup
    r=cl.post(f"/api/v2/cases/{c['id']}/sources/import",content=b'a'*(SOURCE_BODY_LIMIT+1),headers={'Content-Type':'application/json'})
    assert r.status_code==413


def test_lying_content_length_rejected_streaming_not_buffered_unbounded():
    calls=[];messages=[]
    async def app(*args):calls.append(True)
    queue=[{'type':'http.request','body':b'a'*200000,'more_body':True},{'type':'http.request','body':b'b'*200000,'more_body':False}]
    async def receive():return queue.pop(0)
    async def send(msg):messages.append(msg)
    scope={'type':'http','method':'POST','path':'/api/v2/cases/id/commands','headers':[(b'content-length',b'10')]}
    asyncio.run(BoundedRequestBody(app)(scope,receive,send))
    assert not calls and messages[0]['status']==413


@pytest.mark.parametrize('text',['','x'*200001,'bad\x00file'])
def test_source_field_bounds_are_422_without_echoing_text(setup,text):
    _,cl,c=setup
    r=cl.post(f"/api/v2/cases/{c['id']}/sources/import",json=source_body(c,text))
    assert r.status_code==422
    if text:assert text not in r.text


def test_plain_text_and_unauthorised_cross_origin_rejected(setup):
    _,cl,c=setup;base=f"/api/v2/cases/{c['id']}/sources"
    assert cl.post(base+'/import',content='text',headers={'Content-Type':'text/plain'}).status_code==415
    assert cl.post(base+'/import',json=source_body(c),headers={'Origin':'https://other.example'}).status_code==403
    assert cl.get(base,headers={'Authorization':'Bearer wrong'}).status_code==401


def test_model_context_contains_only_explicitly_captured_evidence(setup,monkeypatch):
    from eightball.v2 import intelligence
    _,cl,c=setup
    text='A reviewed excerpt.'+'a'*8000+'UNSELECTED PRIVATE APPENDIX'
    out,_=import_api(cl,c,text);c=out['case'];doc=out['document'];base=f"/api/v2/cases/{c['id']}/sources"
    e=cl.post(base+'/passages',json={'event_id':uid(),'expected_revision':c['revision'],'passages':[{'document_id':doc['id'],'start':0,'end':19,'content_sha256':text_hash(text[:19])}]}).json()
    c=e['case'];eid=c['evidence'][0]['id'];seen=[]
    def model(schema,system,context,client=None):
        seen.append(context)
        src=context['sources'][0]
        return {'items':[{'kind':'claim','text':src['text'],'source':{'evidence_id':src['id'],'quote':src['text']}}]},'test-double'
    monkeypatch.setattr(intelligence,'ollama_json',model)
    from eightball.v2.contracts import Case
    p=intelligence.propose(Case.model_validate(c),'ollama','extract',[eid])
    assert p.items and 'UNSELECTED' not in json.dumps(seen)
    assert seen[0]['sources'][0]['text']==text[:19]


def test_import_does_not_start_analysis_or_leak_to_client_brief(setup):
    _,cl,c=setup
    out,_=import_api(cl,c,'PrivateOriginalSentinel')
    base=f"/api/v2/cases/{c['id']}"
    assert cl.get(base+'/analysis-jobs').json()==[]
    assert cl.get(base+'/proposals').json()==[]
    assert 'PrivateOriginalSentinel' not in cl.get(base+'/client-brief').text
    assert 'PrivateOriginalSentinel' not in cl.get('/api/v2/cases').text


def test_unselected_whole_source_is_not_a_valid_model_source_id(setup):
    _,cl,c=setup;out,_=import_api(cl,c);c=out['case']
    r=cl.post(f"/api/v2/cases/{c['id']}/analyse",json={'expected_revision':c['revision'],'provider':'rules','purpose':'extract','source_ids':[out['document']['id']]})
    assert r.status_code==422


def test_model_input_cap_still_12000(setup):
    _,cl,c=setup;out,_=import_api(cl,c,'z'*16000);c=out['case'];base=f"/api/v2/cases/{c['id']}/sources";did=out['document']['id']
    for start,end in [(0,8000),(8000,16000)]:
        out=cl.post(base+'/passages',json={'event_id':uid(),'expected_revision':c['revision'],'passages':[{'document_id':did,'start':start,'end':end,'content_sha256':text_hash('z'*8000)}]}).json();c=out['case']
    r=cl.post(f"/api/v2/cases/{c['id']}/analyse",json={'expected_revision':c['revision'],'provider':'rules','purpose':'extract','source_ids':[e['id'] for e in c['evidence']]})
    assert r.status_code==422


def test_bad_search_is_literal_not_regex_or_code(setup):
    _,cl,c=setup;out,_=import_api(cl,c,'Text [.*] <script>alert(1)</script> quote.')
    base=f"/api/v2/cases/{c['id']}/sources/{out['document']['id']}"
    result=cl.get(base+'/search',params={'q':'[.*]'}).json();assert len(result['matches'])==1
    assert result['matches'][0]['quote']=='[.*]'


ROOT=Path(__file__).resolve().parents[1]
CASES={
'astral_indices':"assert.deepEqual(sourceOriginalRange('🤝ab',10,2,4),{start:11,end:13});",
'crlf_indices':"assert.deepEqual(sourceOriginalRange('a\\r\\nb',0,2,3),{start:3,end:4});",
'cr_indices':"assert.equal(sourceDisplayMap('a\\rb').text,'a\\nb');",
'surrogate_split_rejected':"assert.throws(()=>sourceOriginalRange('🤝x',0,1,2));",
'empty_selection_rejected':"assert.throws(()=>sourceOriginalRange('abc',0,1,1));",
'out_of_bounds_rejected':"assert.throws(()=>sourceOriginalRange('abc',0,0,5));",
'negative_range_rejected':"assert.throws(()=>sourceOriginalRange('abc',0,-1,2));",
'combining_marks_preserved':"assert.equal(sourceDisplayMap('e\\u0301').originalCharacters,2);",
'limits':"assert.throws(()=>addSourcePassage([{document_id:'a',start:0,end:8000}],{document_id:'b',start:0,end:4001}));",
'overlap':"assert.throws(()=>addSourcePassage([{document_id:'a',start:0,end:10}],{document_id:'a',start:9,end:20}));",
'adjacent_allowed':"assert.equal(addSourcePassage([{document_id:'a',start:0,end:10}],{document_id:'a',start:10,end:20}).length,2);",
'wire_only_intent':"assert.deepEqual(sourceWirePassages([{document_id:'a',start:0,end:2,content_sha256:'hash',text:'secret',title:'private'}]),[{document_id:'a',start:0,end:2,content_sha256:'hash'}]);",
'utf16_exhaustive_roundtrip':r"const raw='\ufeff🤝x\r\ne\u0301\r👩🏾\u200d💻\nThe client has NOT accepted.';const m=sourceDisplayMap(raw);for(let i=0;i<m.boundaries.length;i++)for(let j=i+1;j<m.boundaries.length;j++){if(m.boundaries[i]===null||m.boundaries[j]===null)continue;const r=sourceOriginalRange(raw,0,i,j);const sliced=Array.from(raw).slice(r.start,r.end).join('');assert.equal(sourceDisplayMap(sliced).text,m.text.slice(i,j));}",
}
@pytest.mark.parametrize('case',list(CASES))
def test_source_selection_javascript(case):
    code=f"import assert from 'node:assert/strict';import {{sourceDisplayMap,sourceOriginalRange,addSourcePassage,sourceWirePassages}} from {json.dumps((ROOT/'web/v2/source-model.js').as_uri())};"+CASES[case]
    r=subprocess.run(['node','--input-type=module','-e',code],capture_output=True,text=True,timeout=10)
    assert r.returncode==0,r.stderr
