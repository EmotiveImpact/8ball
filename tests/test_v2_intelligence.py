"""Provider contract tests. These are test doubles, separate from evals/live_models.py."""
from datetime import timedelta
import json
import httpx
import pytest
from pydantic import ValidationError
from eightball.models import Evidence,utcnow
from eightball.v2.contracts import Case,Objective,atom,all_of,any_of
from eightball.v2.intelligence import propose,ollama_json,GraphOutput,ExtractionFailure
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


@pytest.mark.parametrize('output,code',[
    (extracted(kind='observation',value=True),'invalid_extraction_shape'),
    (extracted(source={'evidence_id':'source','quote':'The client accepted the offer.'}), 'unsupported_extraction_span'),
])
def test_rejected_parsed_extraction_retains_detached_output_and_safe_diagnostic(output,code):
    from copy import deepcopy
    from hashlib import sha256
    from eightball.v2.intelligence import PROMPT_VERSION,ExtractionOutput
    from eightball.store import digest
    c=case();before=c.model_dump(mode='json');original=deepcopy(output)
    with client(output) as transport:
        with pytest.raises(ExtractionFailure) as caught:
            propose(c,'ollama','extract',['source'],client=transport)
    failure=caught.value
    assert failure.model=='fixture-model' and failure.trace['model']=='fixture-model'
    assert failure.trace['prompt_version']==PROMPT_VERSION
    assert failure.trace['schema_sha256']==digest(ExtractionOutput.model_json_schema())
    assert failure.trace['sources']==[{'id':'source','text_sha256':sha256(c.evidence[0].text.encode()).hexdigest()}]
    assert failure.trace['diagnostic']['code']==code and failure.trace['extraction']==original
    assert 'input' not in json.dumps(failure.trace['diagnostic']) and 'accepted' not in str(failure)
    output.clear()
    assert failure.trace['extraction']==original and c.model_dump(mode='json')==before


@pytest.mark.parametrize('raw,omission',[
    ({'items':[],'unexpected':'x'*500001},'parsed_output_exceeds_limit'),
    ({'items':[],'unexpected':float('inf')},'parsed_output_not_finite_json'),
])
def test_rejected_output_audit_cannot_store_oversized_or_nonfinite_json(monkeypatch,raw,omission):
    from eightball.v2 import intelligence
    monkeypatch.setattr(intelligence,'ollama_json',lambda *a,**k:(raw,'fixture-model'))
    with pytest.raises(ExtractionFailure) as caught:propose(case(),'ollama','extract',['source'])
    trace=caught.value.trace
    assert trace['output_omitted']==omission and 'extraction' not in trace
    json.dumps(trace,allow_nan=False)


def test_hosted_extraction_rejection_retains_parsed_output_and_transport_without_credentials(monkeypatch):
    token='hf_controlled-fixture-token'
    monkeypatch.setenv('HF_TOKEN',token)
    monkeypatch.setenv('EIGHTBALL_HF_MODEL','fixture/selected-model')
    monkeypatch.setenv('EIGHTBALL_HF_PROVIDER','fixture-provider')
    raw=extracted(kind='observation')
    envelope={'model':'served-fixture-model','choices':[{'finish_reason':'stop',
              'message':{'role':'assistant','content':json.dumps(raw)}}]}
    with httpx.Client(transport=httpx.MockTransport(lambda req:httpx.Response(200,json=envelope))) as transport:
        with pytest.raises(ExtractionFailure) as caught:
            propose(case(),'huggingface','extract',['source'],allow_external=True,client=transport)
    trace=caught.value.trace
    assert trace['extraction']==raw and caught.value.model=='served-fixture-model'
    assert len(trace['transport']['calls'])==1 and trace['transport']['calls'][0]['served_model']=='served-fixture-model'
    assert token not in json.dumps(trace) and token not in str(caught.value)


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
