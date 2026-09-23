"""Provider contract tests. These are test doubles, separate from evals/live_models.py."""
from datetime import timedelta
import json
import httpx
import pytest
from pydantic import ValidationError
from eightball.models import Evidence,utcnow
from eightball.v2.contracts import Case,Objective,atom,all_of,any_of
from eightball.v2.intelligence import propose,ollama_json,GraphOutput
from eightball.providers import ProviderUnavailable


def case():
    return Case(title='Fictional intake',client='Test',summary='Service interruption.',desired_outcome='Restore service with confirmation',
                deadline=utcnow()+timedelta(days=1),evidence=[Evidence(id='source',title='Source',source='Fixture',text='The client refused the offer.')])


def client(output,**envelope):
    return httpx.Client(transport=httpx.MockTransport(lambda req:httpx.Response(200,json={
        'model':'fixture-model','done':True,'message':{'content':json.dumps(output)},**envelope})))


def extracted(**overrides):
    item={'kind':'claim','text':'The client refused the offer.','source':{'evidence_id':'source','quote':'The client refused the offer.'}}
    item.update(overrides)
    return {'items':[item]}


def test_real_adapter_contract_cannot_change_state():
    c=case();before=c.model_dump(mode='json');seen=[]
    def handle(req):
        body=json.loads(req.content);seen.append(body)
        assert str(req.url)=='http://127.0.0.1:11434/api/chat'
        assert body['think'] is False and body['format']['type']=='object'
        assert body['stream'] is False
        return httpx.Response(200,json={'model':'fixture-model','done':True,'message':{'content':json.dumps(extracted())}})
    p=propose(c,'ollama','extract',['source'],client=httpx.Client(transport=httpx.MockTransport(handle)))
    assert p.model=='fixture-model' and p.items[0].kind=='claim'
    assert p.items[0].object['provenance']['references'][0]['quote']==c.evidence[0].text
    assert p.items[0].disposition=='pending' and p.status=='pending'
    assert c.model_dump(mode='json')==before


@pytest.mark.parametrize('output',[
    extracted(source={'evidence_id':'another-case','quote':'The client refused the offer.'}),
    extracted(source={'evidence_id':'source','quote':'The client accepted the offer.'}),
    extracted(kind='observation',value=True),
    extracted(kind='approval'),
    {'items':[],'observations':[{'value':True}]},
    extracted(actor_kind='government-agent'),
])
def test_model_cannot_add_unsupported_spans_or_privileged_objects(output):
    with pytest.raises((ValueError,ValidationError)):
        propose(case(),'ollama','extract',['source'],client=client(output))


@pytest.mark.parametrize('envelope',[{'done':False},{'done_reason':'length'},{'message':{'content':'not json'}},{'done':'true'}])
def test_incomplete_or_invalid_generation_fails(envelope):
    with pytest.raises(ProviderUnavailable):ollama_json({},'Test',{},client=client({},**envelope))


def test_retracted_sources_cannot_be_sent_to_provider():
    c=case();c.evidence[0].status='retracted'
    with pytest.raises(ValueError):propose(c,'ollama','extract',['source'],client=client(extracted()))


def graph():
    return {'conditions':[
                {'id':'repaired','title':'Service repaired','confirmation':'Technical checks'},
                {'id':'resolved','title':'Service recovered and accepted','confirmation':'Owner confirms recovery'}],
            'actions':[
                {'id':'recover','title':'Recover service','owner':'Operator','requires_all':[],
                 'minutes':60,'produces':['repaired'],'external':True},
                {'id':'verify','title':'Verify and confirm acceptance','owner':'Case lead','requires_all':['repaired'],
                 'minutes':15,'produces':['resolved'],'external':True}],
            'goal_conditions':['resolved'],'final_verification_action_id':'verify'}



def test_graph_generation_is_validated_proposal_only():
    c=case();p=propose(c,'ollama','graph',['source'],client=client(graph()))
    assert len(p.items)==5 and not c.graph.actions and not c.observations
    assert next(i for i in p.items if i.kind=='action').object['approval_required'] is True
    assert all(i.object['provenance']['origin']=='model_proposal' for i in p.items)


@pytest.mark.parametrize('mutator',[
    lambda g:g['actions'][0].update(produces=['nonexistent']),
    lambda g:g['actions'][0].update(decision_id='absent',decision_option='yes'),
    lambda g:g['actions'][0].update(minutes=-1),
    lambda g:g.update(goal_conditions=[]),
    lambda g:g.update(observations=[{'value':True}]),
    lambda g:g.update(questions=[{'id':'q','question':'Accepted?','status':'answered','answer':'yes'}]),
])
def test_bad_graph_and_self_answering_model_rejected(mutator):
    g=graph();mutator(g)
    with pytest.raises((ValueError,ValidationError)):
        propose(case(),'ollama','graph',['source'],client=client(g))


@pytest.mark.parametrize('expr',[all_of(),any_of(atom('a'),all_of()),all_of(any_of(all_of(),atom('a')))])
def test_vacuous_success_cannot_close_case(expr):
    with pytest.raises(ValidationError):Objective(title='Do nothing',success=expr)


def test_ambiguous_repeated_quote_rejected_not_misattributed():
    c=case();c.evidence[0].text='The client refused the offer. The client refused the offer.'
    with pytest.raises(ValueError):propose(c,'ollama','extract',['source'],client=client(extracted()))


def test_questions_are_proposals_and_cannot_answer_themselves():
    c=case();output={'questions':[{'id':'q','question':'Who can confirm recovery?','why':'Obtain reliable confirmation'}]}
    p=propose(c,'ollama','questions',[],client=client(output))
    assert len(p.items)==1 and p.items[0].kind=='question' and not c.questions
    output['questions'][0]['answer']='The model can.'
    with pytest.raises(ValueError):propose(c,'ollama','questions',[],client=client(output))


def test_compact_graph_preserves_contingency_and_unknown_wait():
    c=case();p=propose(c,'ollama','graph',['source'],client=client(graph()))
    a=next(i.object for i in p.items if i.kind=='action')
    assert a['contingent'] is True and a['wait_minutes'] is None
    assert a['approval_required'] is True and not c.graph.conditions


def test_compact_graph_does_not_replace_existing_conditions():
    from eightball.v2.contracts import Condition
    c=case();c.graph.conditions.append(Condition(id='resolved',title='Original meaning',confirmation='Reviewed source'))
    with pytest.raises(ValueError):propose(c,'ollama','graph',['source'],client=client(graph()))


@pytest.mark.parametrize('mutator',[
    lambda g:g['actions'][0].pop('requires_all'),
    lambda g:g.update(final_verification_action_id='missing'),
    lambda g:g['actions'][1].update(requires_all=[]),
    lambda g:g.update(goal_conditions=['repaired']),
    lambda g:g['actions'][0].update(produces=['resolved']),
    lambda g:g['actions'][1].update(requires_all=['resolved']),
])
def test_draft_cannot_omit_dependencies_or_bypass_final_verification(mutator):
    g=graph();mutator(g)
    with pytest.raises((ValueError,ValidationError)):
        propose(case(),'ollama','graph',['source'],client=client(g))
