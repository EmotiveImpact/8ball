"""Regression checks added during the V0.2 release audit."""
from datetime import timedelta
import json
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from eightball.api import make_app
from eightball.models import uid, utcnow, Evidence, Observation
from eightball.store import Store as LegacyStore
from eightball.v2.store import Store
from eightball.v2.contracts import (Case, Graph, Condition, Action, Effect, Objective,
    Decision, Option, Question, Resource, all_of, atom)
from eightball.v2.commands import Command, apply
from eightball.v2.planner import plan


def fixture():
    return Case(title='Release fixture', client='Fictional', summary='Release regression',
        desired_outcome='Verified outcome', deadline=utcnow()+timedelta(days=2),
        graph=Graph(conditions=[Condition(id=x,title=x,confirmation='Reviewed evidence') for x in ['a','b','goal']],
        actions=[],objectives=[Objective(id='target',title='Target',success=atom('goal'))]))


def action(id, produces, requires=None, **kwargs):
    return Action(id=id,title=id,owner='Lead',purpose='Fictional test',requires=requires or all_of(),
        effects=[Effect(condition_id=x,value=v) for x,v in produces],minutes=10,**kwargs)


def attest(c,cid,value=True):
    data=c.model_dump();e=Evidence(title='Reviewed',source='Fixture',text='Test assertion',status='reviewed')
    data['evidence'].append(e.model_dump());data['observations'].append(Observation(condition_id=cid,evidence_id=e.id,value=value,rationale='Fixture').model_dump())
    return Case.model_validate(data)


def command(c,kind,payload):
    return apply(c,Command(event_id=uid(),expected_revision=c.revision,kind=kind,payload=payload))


def test_answer_cannot_be_removed_through_object_edit():
    c=attest(fixture(),'a');c.questions.append(Question(id='q',question='What happened?',why='Clarify',condition_ids=['a']))
    c=command(c,'answer',{'question_id':'q','answer':'Confirmed in the source','evidence_ids':[c.evidence[0].id]})
    with pytest.raises(ValueError,match='recorded answer'):
        command(c,'upsert_object',{'kind':'question','object':Question(id='q',question='Blank',why='Rewrite').model_dump()})
    assert c.questions[0].answer=='Confirmed in the source'
    updated=command(c,'answer',{'question_id':'q','answer':'Corrected answer','evidence_ids':[c.evidence[0].id]})
    assert updated.questions[0].answer=='Corrected answer'


def test_route_cannot_require_two_options_of_one_decision():
    c=fixture();c.decisions=[Decision(id='d',question='Which option?',owner='Lead',options=[Option(id='x',title='X'),Option(id='y',title='Y')])]
    c.graph.actions=[action('one',[('a',True)],decision_id='d',decision_option='x'),action('two',[('b',True)],decision_id='d',decision_option='y'),action('finish',[('goal',True)],all_of('a','b'))]
    p=plan(c)
    assert p['routes'] and all(any('Mutually exclusive' in x for x in r['hard_breaches']) for r in p['routes'])


def test_later_guard_is_rechecked_after_signed_effects():
    c=attest(fixture(),'a')
    c.graph.actions=[action('remove',[('a',False),('b',True)]),action('finish',[('goal',True)],atom('b'),guard=atom('a'))]
    p=plan(c)
    assert all(any('Projected guard' in x for x in r['hard_breaches']) for r in p['routes'])


def test_projected_failure_is_not_a_viable_resolution():
    c=fixture();c.graph.objectives[0].failure=atom('a')
    c.graph.actions=[action('bad_resolution',[('goal',True),('a',True)])]
    assert any('Projected objective failure' in x for x in plan(c)['routes'][0]['hard_breaches'])


def test_evidence_coverage_counts_the_required_signed_value():
    c=attest(fixture(),'a',False);c.graph.actions=[action('finish',[('goal',True)],atom('a'))]
    r=plan(c)['routes'][0]
    assert r['evidence_coverage']['supported']==0
    assert any(x['condition_id']=='a' and x['value'] is True for x in r['evidence_gaps'])


def test_resource_window_cannot_run_backwards():
    now=utcnow()
    with pytest.raises(ValidationError):Resource(id='r',name='Room',available_from=now,available_until=now-timedelta(minutes=1))


@pytest.fixture
def api(tmp_path):
    legacy=LegacyStore(str(tmp_path/'case.db'));store=Store(legacy.path)
    cl=TestClient(make_app(legacy,'a'*40),headers={'Authorization':'Bearer '+'a'*40})
    c=store.create(fixture())
    c,_=store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='add_evidence',payload={'title':'Source','source':'Fixture','text':'The client declined.'}))
    return cl,store,c


@pytest.mark.parametrize('provider,purpose', [('ollama','extract'),('jev','judgement'),('gliclass','judgement')])
@pytest.mark.parametrize('mistake',['unknown_source','retracted_source','repeated_source','empty_sources','unsupported_purpose'])
def test_operator_input_error_does_not_create_failed_model_run(api,provider,purpose,mistake):
    cl,store,c=api
    sources=[c.evidence[0].id]
    if mistake=='unknown_source':sources=['othercase']
    if mistake=='repeated_source':sources*=2
    if mistake=='empty_sources':sources=[]
    if mistake=='unsupported_purpose':purpose='judgement' if provider=='ollama' else 'graph'
    if mistake=='retracted_source':
        c,_=store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='review_evidence',payload={'evidence_id':sources[0],'status':'retracted'}))
    before=store.audit(c.id)
    response=cl.post(f'/api/v2/cases/{c.id}/analyse',json={'expected_revision':c.revision,'provider':provider,'purpose':purpose,'source_ids':sources,'allow_external':True})
    assert response.status_code==422, response.text
    assert store.audit(c.id)==before


def test_external_permission_failure_is_not_an_inference_run(api):
    cl,store,c=api
    r=cl.post(f'/api/v2/cases/{c.id}/analyse',json={'expected_revision':c.revision,'provider':'jev','purpose':'judgement','source_ids':[c.evidence[0].id],'allow_external':False})
    assert r.status_code==422 and 'permission' in r.json()['detail']
    assert not store.proposals(c.id)


def test_invalid_model_output_is_recorded_as_provider_failure(api,monkeypatch):
    from eightball.v2 import api as v2api
    cl,store,c=api
    def bad(*args,**kwargs):raise ValueError('Malformed output fixture')
    monkeypatch.setattr(v2api,'propose',bad)
    r=cl.post(f'/api/v2/cases/{c.id}/analyse',json={'expected_revision':c.revision,'provider':'ollama','purpose':'extract','source_ids':[c.evidence[0].id]})
    assert r.status_code==503
    assert store.get(c.id)==c and len(store.proposals(c.id))==1
    assert store.proposals(c.id)[0]['status']=='failed'


def test_older_pending_proposals_are_accessible(api):
    from eightball.v2.intelligence import propose
    cl,store,c=api
    for _ in range(51):store.save_proposal(propose(c,'rules','extract',[c.evidence[0].id]))
    r=cl.get(f'/api/v2/cases/{c.id}/proposals')
    assert r.status_code==200 and len(r.json())==51


def test_answer_edit_failure_is_transactional(api):
    cl,store,c=api
    c,_=store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='upsert_object',payload={'kind':'question','object':Question(id='q',question='Why?',why='Context').model_dump()}))
    eid=c.evidence[0].id
    c,_=store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='review_evidence',payload={'evidence_id':eid,'status':'reviewed'}))
    c,_=store.change(c.id,Command(event_id=uid(),expected_revision=c.revision,kind='answer',payload={'question_id':'q','answer':'Documented answer','evidence_ids':[eid]}))
    before=store.audit(c.id)
    r=cl.post(f'/api/v2/cases/{c.id}/commands',json={'event_id':uid(),'expected_revision':c.revision,'kind':'upsert_object','payload':{'kind':'question','object':Question(id='q',question='Why?',why='Rewrite').model_dump()}})
    assert r.status_code==422
    assert store.audit(c.id)==before
