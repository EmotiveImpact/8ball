from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import json
import pytest
from fastapi.testclient import TestClient
from eightball.api import make_app
from eightball.store import Store as LegacyStore
from eightball.v2.store import Store
from eightball.models import utcnow,uid

TOKEN='v2-test-operator-not-real-secret-123456789'


@pytest.fixture
def setup(tmp_path):
    legacy=LegacyStore(str(tmp_path/'cases.db'));store=Store(legacy.path)
    client=TestClient(make_app(legacy,TOKEN),headers={'Authorization':'Bearer '+TOKEN})
    return store,legacy,client


def new(client,playbook=None):
    r=client.post('/api/v2/cases',json={'title':'Fictional situation','client':'Test','summary':'Fixture notes','desired_outcome':'Accepted resolution',
            'deadline':(utcnow()+timedelta(days=1)).isoformat(),'budget':10000,'playbook':playbook})
    assert r.status_code==201,r.text
    return r.json()


def cmd(client,c,kind,payload,event_id=None):
    return client.post(f"/api/v2/cases/{c['id']}/commands",json={'event_id':event_id or uid(),'expected_revision':c['revision'],'kind':kind,'payload':payload})


def source(client,c,text='Root cause is not confirmed. Who can approve the report?'):
    r=cmd(client,c,'add_evidence',{'title':'Test source','source':'Fictional sender','text':text});assert r.status_code==200,r.text
    return r.json()['case']


def analyse(client,c,provider='rules',purpose='extract',**kwargs):
    r=client.post(f"/api/v2/cases/{c['id']}/analyse",json={'expected_revision':c['revision'],'provider':provider,'purpose':purpose,
                           'source_ids':[e['id'] for e in c['evidence']],**kwargs})
    assert r.status_code==200,r.text
    return r.json()['proposal']


def review(client,c,p,choices,event_id=None):
    return client.post(f"/api/v2/cases/{c['id']}/proposals/{p['id']}/review",json={'event_id':event_id or uid(),'expected_revision':c['revision'],'choices':choices})


def test_create_demo_and_full_api_views(setup):
    _,_,cl=setup;c=cl.post('/api/v2/demo',json={}).json();base=f"/api/v2/cases/{c['id']}"
    for route in ['', '/questions','/map','/history','/changes','/export','/client-brief','/proposals','/actions/investigate']:
        assert cl.get(base+route).status_code==200
    data=cl.get(base).json();assert len(data['plan']['routes'])>=3
    assert cl.post(base+'/plan',json={}).status_code==200
    ids=[r['id'] for r in data['plan']['routes'][:2]]
    assert cl.post(base+'/compare',json={'revision':0,'route_ids':ids}).status_code==200


def test_selective_review_edits_preserves_truth_and_records_trace(setup):
    store,_,cl=setup;c=source(cl,new(cl));p=analyse(cl,c)
    assert store.get(c['id']).revision==c['revision']
    choices=[]
    for i,item in enumerate(p['items']):
        if i==0:
            obj=item['object'];obj['statement']='Edited assertion, still just a claim'
            choices.append({'id':item['id'],'disposition':'edited','object':obj})
        else:choices.append({'id':item['id'],'disposition':'rejected'})
    r=review(cl,c,p,choices);assert r.status_code==200,r.text
    c=r.json()['case'];assert len(c['claims'])==1 and not c['observations']
    assert c['claims'][0]['provenance']['run_id']==p['id']
    audit=store.audit(c['id']);assert audit['valid'] and audit['replay_matches_snapshot']
    assert audit['model_runs'][0]['review']['choices']==choices


def test_reject_all_never_changes_case_revision(setup):
    store,_,cl=setup;c=source(cl,new(cl));before=store.get(c['id']);p=analyse(cl,c)
    r=review(cl,c,p,[{'id':i['id'],'disposition':'rejected'} for i in p['items']]);assert r.status_code==200
    assert store.get(c['id'])==before
    assert store.proposals(c['id'])[0]['status']=='reviewed'


def test_stale_proposals_refuse_to_commit(setup):
    _,_,cl=setup;c=source(cl,new(cl));p=analyse(cl,c);newer=source(cl,c)
    r=review(cl,newer,p,[{'id':i['id'],'disposition':'accepted'} for i in p['items']]);assert r.status_code==409


def test_partial_reference_rejection_is_atomic(setup):
    store,_,cl=setup;c=new(cl);p=analyse(cl,c,'playbook','graph',playbook_id='recovery')
    choices=[{'id':i['id'],'disposition':'rejected' if i['kind']=='condition' else 'accepted'} for i in p['items']]
    r=review(cl,c,p,choices);assert r.status_code==422
    assert store.get(c['id']).revision==0
    assert store.proposals(c['id'])[0]['status']=='pending'


def test_playbook_graph_can_be_reviewed_and_accepted(setup):
    store,_,cl=setup;c=new(cl);p=analyse(cl,c,'playbook','graph',playbook_id='recovery')
    r=review(cl,c,p,[{'id':i['id'],'disposition':'accepted'} for i in p['items']]);assert r.status_code==200,r.text
    assert len(r.json()['plan']['routes'])==2
    assert len(store.get(c['id']).graph.conditions)==5


def test_optimistic_revision_and_idempotency(setup):
    _,_,cl=setup;c=new(cl);payload={'title':'Source','source':'Test','text':'Test'}
    first=cmd(cl,c,'add_evidence',payload,'same');assert first.status_code==200
    assert cmd(cl,c,'add_evidence',payload,'same').json()['changes']['duplicate']
    assert cmd(cl,c,'add_evidence',{**payload,'text':'Different'},'same').status_code==409
    assert cmd(cl,c,'add_evidence',payload).status_code==409


def test_concurrent_command_one_winner(setup):
    _,_,cl=setup;c=new(cl)
    def write(i):return cmd(cl,c,'metadata',{'budget':2000+i}).status_code
    with ThreadPoolExecutor(max_workers=2) as p:assert sorted(p.map(write,[0,1]))==[200,409]


def test_simulation_refusal_changes_routes_without_persistence(setup):
    store,_,cl=setup;c=cl.post('/api/v2/demo',json={}).json();base=f"/api/v2/cases/{c['id']}";before=store.audit(c['id'])
    r=cl.post(base+'/simulate',json={'expected_revision':0,'conditions':{'refused':True,'language':True},'decisions':{'escalation':'mediate'}})
    assert r.status_code==200,r.text
    assert r.json()['persisted'] is False
    p=r.json()['plan'];assert any(not x['hard_breaches'] and not x['evidence_gaps'] for x in p['routes'] if 'mediated' in x['actions'])
    assert all(x['evidence_gaps'] for x in p['routes'] if 'staged' in x['actions'])
    assert store.audit(c['id'])==before


@pytest.mark.parametrize('body',[{'expected_revision':3},{'expected_revision':0,'conditions':{'refused':'false'}},
 {'expected_revision':0,'conditions':{'other_case':True}},{'expected_revision':0,'unavailable_actions':['missing']},
 {'expected_revision':0,'resource_starts':{'missing':'2026-09-23T00:00:00Z'}}, {'expected_revision':0,'decisions':{'missing':'yes'}}])
def test_invalid_simulations_rejected(setup,body):
    _,_,cl=setup;c=cl.post('/api/v2/demo',json={}).json()
    assert cl.post(f"/api/v2/cases/{c['id']}/simulate",json=body).status_code in (409,422)


def test_cross_case_source_cannot_be_analysed_or_attested(setup):
    _,_,cl=setup;c1=source(cl,new(cl));c2=new(cl,'recovery')
    r=cl.post(f"/api/v2/cases/{c2['id']}/analyse",json={'expected_revision':0,'provider':'rules','purpose':'extract','source_ids':[c1['evidence'][0]['id']]})
    assert r.status_code==422
    assert cmd(cl,c2,'observe',{'condition_id':'scope','evidence_id':c1['evidence'][0]['id'],'value':True,'rationale':'Test'}).status_code==422


def test_legacy_migration_preserves_chain_and_is_idempotent(setup):
    store,legacy,cl=setup;old=cl.post('/api/demo',json={}).json();before=legacy.audit(old['id'])
    r=cl.post('/api/v2/legacy/'+old['id']+'/import',json={});assert r.status_code==200,r.text
    newcase=r.json();assert newcase['legacy_id']==old['id'];assert newcase['approvals']==[]
    assert legacy.audit(old['id'])==before
    assert store.audit(newcase['id'])['legacy_lineage']==before
    assert cl.post('/api/v2/legacy/'+old['id']+'/import',json={}).json()['id']==newcase['id']


def test_audit_tamper_detected(setup):
    store,_,cl=setup;c=new(cl)
    with store.connection() as db:db.execute('UPDATE v2_events SET hash=? WHERE case_id=?',('tamper',c['id']));db.commit()
    assert not store.audit(c['id'])['valid']


def test_replay_round_trip_and_reload(setup):
    store,_,cl=setup;c=source(cl,new(cl));a=store.audit(c['id'])
    assert a['valid'] and a['replay_matches_snapshot']
    assert Store(store.path).get(c['id']).model_dump(mode='json')==a['case']


def test_search_case_scoped_and_retracted_sources_hidden(setup):
    _,_,cl=setup;c=source(cl,new(cl),'UniqueSentinel source text');other=new(cl)
    q={'query':'UniqueSentinel'}
    assert cl.post(f"/api/v2/cases/{c['id']}/search",json=q).json()
    assert not cl.post(f"/api/v2/cases/{other['id']}/search",json=q).json()
    c=cmd(cl,c,'review_evidence',{'evidence_id':c['evidence'][0]['id'],'status':'retracted'}).json()['case']
    assert not cl.post(f"/api/v2/cases/{c['id']}/search",json=q).json()


def test_client_brief_does_not_leak_source_content(setup):
    _,_,cl=setup;c=source(cl,new(cl),'UniqueSentinel confidential fixture')
    body=cl.get(f"/api/v2/cases/{c['id']}/client-brief").text
    assert 'UniqueSentinel' not in body
    assert 'Operator preview' in body


def test_model_failure_recorded_without_false_success(setup,monkeypatch):
    store,_,cl=setup;monkeypatch.delenv('TYPESAFE_API_KEY',raising=False)
    c=source(cl,new(cl));base=f"/api/v2/cases/{c['id']}";before=store.get(c['id'])
    r=cl.post(base+'/analyse',json={'expected_revision':c['revision'],'provider':'jev','purpose':'judgement',
                                  'source_ids':[c['evidence'][0]['id']],'allow_external':True})
    assert r.status_code==503
    assert store.get(c['id'])==before
    assert store.proposals(c['id'])[0]['status']=='failed'


def test_auth_and_no_input_echo(setup):
    _,legacy,_=setup;app=make_app(legacy,TOKEN);cl=TestClient(app)
    assert cl.get('/api/v2/cases').status_code==401
    cl.headers['Authorization']='Bearer '+TOKEN
    r=cl.post('/api/v2/cases',json={'title':'UniqueSecretErrorInput'})
    assert r.status_code==422 and 'UniqueSecretErrorInput' not in r.text
    assert cl.get('/v2/').status_code==200
    assert 'unsafe-eval' not in cl.get('/v2/').headers['content-security-policy']


def test_model_cannot_mark_decision_selected_via_generic_update(setup):
    _,_,cl=setup;c=new(cl)
    obj={'id':'d','question':'Approve?','owner':'Lead','options':[{'id':'yes','title':'Yes'},{'id':'no','title':'No'}],'selected':'yes'}
    assert cmd(cl,c,'upsert_object',{'kind':'decision','object':obj}).status_code==422
