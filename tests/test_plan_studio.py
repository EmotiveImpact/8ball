"""Real authoring preview, no model or database writes."""
from copy import deepcopy
from datetime import timedelta
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from eightball.api import make_app
from eightball.store import Store as LegacyStore
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.authoring import GraphPreview, preview_graph
from eightball.v2.commands import Command
from endstate.contracts import atom, any_of, all_of
from eightball.models import utcnow, uid


def graph(case):return case.graph.model_dump(mode='json')

def test_preview_is_detached_and_preserves_every_source():
    c=demo_case(); before=c.model_dump(mode='json'); draft=graph(c);draft['actions'][0]['minutes']=42
    p=preview_graph(c,GraphPreview(expected_revision=c.revision,graph=draft))
    assert c.model_dump(mode='json')==before
    assert p['persisted'] is False and p['preview'] is True
    assert p['edits']==[{'collection':'actions','id':'preserve','title':'Preserve incident records','change':'edited','fields':['minutes']}]


def test_preview_matches_live_command_route_result():
    from eightball.v2.commands import apply
    from eightball.v2.planner import plan
    c=demo_case();draft=graph(c);draft['actions'][1]['cost']=1234
    p=preview_graph(c,GraphPreview(expected_revision=0,graph=draft))
    candidate=apply(c,Command(event_id=uid(),expected_revision=0,kind='replace_graph',payload={'graph':draft}))
    expected=plan(candidate)
    assert [(r['id'],r['total_cost'],r['status']) for r in p['plan']['routes']]==[(r['id'],r['total_cost'],r['status']) for r in expected['routes']]


def test_preview_stale_revision_rejected():
    from eightball.store import Conflict
    c=demo_case()
    with pytest.raises(Conflict):preview_graph(c,GraphPreview(expected_revision=1,graph=graph(c)))


@pytest.mark.parametrize('mutate',[
 lambda g:g['conditions'][0].update(title='Another fact'),
 lambda g:g['conditions'][0].update(confirmation='Another meaning'),
 lambda g:g['conditions'].pop(0),
 lambda g:g['actions'][0].update(requires={'op':'atom','condition_id':'foreign'}),
 lambda g:g['objectives'][0].update(success={'op':'all','args':[]}),
 lambda g:g['actions'][0].update(minutes=True),
 lambda g:g['actions'][0].update(resources=['foreign']),
 lambda g:g['actions'][0].update(decision_id='missing',decision_option='yes'),
 lambda g:g['actions'][0].update(contingencies=[{'label':'Accept','when':{'op':'atom','condition_id':'retained'},'response':'Continue','next_action_ids':['foreign']}]),
])
def test_invalid_or_historical_edit_rejected(mutate):
    c=demo_case();d=graph(c);mutate(d)
    with pytest.raises(ValueError):preview_graph(c,GraphPreview(expected_revision=0,graph=d))


def test_observed_due_date_edit_preserves_assertion():
    c=demo_case();g=graph(c);g['conditions'][0]['due_at']=(utcnow()+timedelta(hours=2)).isoformat()
    p=preview_graph(c,GraphPreview(expected_revision=0,graph=g))
    assert p['edits'][0]['fields']==['due_at']
    assert p['plan']['states']['records']['status']=='true'


def test_nested_negative_guards_roundtrip():
    c=demo_case();g=graph(c)
    g['actions'][0]['requires']=all_of(any_of('language',atom('refused',False)),'records').model_dump(mode='json')
    g['actions'][0]['guard']=atom('refused',False).model_dump(mode='json')
    p=preview_graph(c,GraphPreview(expected_revision=0,graph=g))
    assert p['plan']['action_states']['preserve']['status']=='ready'


def test_preview_rejects_completed_action_redefinition():
    c=demo_case();c.completed=['preserve'];g=graph(c);g['actions'][0]['cost']=999
    with pytest.raises(ValueError,match='immutable'):preview_graph(c,GraphPreview(expected_revision=0,graph=g))


def test_no_mandatory_goal_warns_does_not_close():
    c=demo_case();g=graph(c)
    for o in g['objectives']:o['mandatory']=False
    p=preview_graph(c,GraphPreview(expected_revision=0,graph=g))
    assert p['warnings'] and not p['plan']['outcome_evidenced']


def test_graph_hash_identifies_exact_draft():
    c=demo_case();g=graph(c)
    a=preview_graph(c,GraphPreview(expected_revision=0,graph=g))
    b=preview_graph(c,GraphPreview(expected_revision=0,graph=g))
    assert a['graph_sha256']==b['graph_sha256']
    g['actions'][0]['cost']+=1
    assert preview_graph(c,GraphPreview(expected_revision=0,graph=g))['graph_sha256']!=a['graph_sha256']


def test_api_preview_then_commit_and_stale_rejection(tmp_path):
    legacy=LegacyStore(str(tmp_path/'s.db'));store=Store(legacy.path);c=store.create(demo_case(),fixture=True)
    cl=TestClient(make_app(legacy,'a'*32),headers={'Authorization':'Bearer '+'a'*32})
    g=graph(c);g['actions'][1]['cost']=1500;base=f'/api/v2/cases/{c.id}'
    before=store.audit(c.id)
    r=cl.post(base+'/graph/preview',json={'expected_revision':0,'graph':g});assert r.status_code==200,r.text
    assert store.audit(c.id)==before
    r=cl.post(base+'/commands',json={'event_id':'edit','expected_revision':0,'kind':'replace_graph','payload':{'graph':g}})
    assert r.status_code==200 and store.get(c.id).revision==1
    assert store.audit(c.id)['valid']
    assert cl.post(base+'/graph/preview',json={'expected_revision':0,'graph':g}).status_code==409


def test_preview_auth_required(tmp_path):
    cl=TestClient(make_app(LegacyStore(str(tmp_path/'a.db')),'a'*32))
    assert cl.post('/api/v2/cases/none/graph/preview',json={'expected_revision':0,'graph':{}}).status_code==401
