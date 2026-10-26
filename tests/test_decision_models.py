"""Native decision wire/negative fixtures. No live network or inference."""
from copy import deepcopy
import json

import httpx
import pytest
from pydantic import ValidationError

from endstate.intelligence.decisions import DecisionInput
from eightball.v2.decision_models import DecisionSession, payload_for, validate_response
from eightball.v2.hosted import HostedFailure, HostedSetupRequired

MODELS = ['jev-latest','clef-flash','gpt-6-luna-decisions']


def request(model):
    return DecisionInput(model=model,state='Fictional change. Integration tests are missing.',questions=[{
        'id':'review','instructions':'Treat missing evidence as a reason to review.',
        'criteria':{'accept':'Relevant evidence supports the change.','review':'Evidence is missing.'}}])


def response(model):
    answer = {'type':'choice','choice':'review','confidence':0.7,'probabilities':{'accept':0.1,'review':0.9}}
    answers = {'review':answer}
    if model == 'gpt-6-luna-decisions':
        answers = [{**answer,'name':'review','probabilities':[{'value':k,'probability':v} for k,v in answer['probabilities'].items()]}]
    return {'model':model,'answers':answers,'usage':{'input_tokens':100,'output_tokens':12,'cost':0}}


@pytest.fixture(autouse=True)
def fake_token(monkeypatch):
    monkeypatch.setenv('EXPERIENTIAL_API_KEY','fictional-native-decision-token')


@pytest.mark.parametrize('model',MODELS)
def test_exact_native_transport_and_one_request_only(model):
    calls = []
    def serve(r):
        calls.append(r)
        path,payload = payload_for(request(model))
        assert str(r.url) == 'https://api.experientiallabs.ai'+path
        assert json.loads(r.content) == payload
        assert 'chat' not in path and 'messages' not in payload
        return httpx.Response(200,json=response(model))
    with httpx.Client(transport=httpx.MockTransport(serve)) as client:
        session = DecisionSession(allow_external=True,client=client)
        result = session.ask(request(model))
        assert result['answers']['review']['choice'] == 'review'
        assert result['advisory_only'] and not result['facts_attested'] and not result['execution_authorized']
        assert session.receipt['inference_calls'] == 1
        with pytest.raises(HostedSetupRequired):session.ask(request(model))
    assert len(calls) == 1


@pytest.mark.parametrize('status',[301,302,307,400,401,403,429,500,503])
def test_errors_never_redirect_retry_or_expose_body(status):
    calls = []
    def serve(r):
        calls.append(r)
        return httpx.Response(status,headers={'Location':'https://evil.invalid'},text='fictional-native-decision-token')
    with httpx.Client(transport=httpx.MockTransport(serve),follow_redirects=True) as client:
        session = DecisionSession(allow_external=True,client=client)
        with pytest.raises(HostedFailure) as exc:session.ask(request('jev-latest'))
        assert 'fictional-native-decision-token' not in str(exc.value)
        assert session.receipt['charge_status'] == 'unknown'
    assert len(calls) == 1 and session.response is None


@pytest.mark.parametrize('model',MODELS)
@pytest.mark.parametrize('bad',['missing','extra','wrong_model','refusal','top_refusal','incomplete','probability','boolean','sum','choice','usage','missing_usage','total_usage','cost'])
def test_invalid_decisions_fail_closed(model,bad):
    data = response(model)
    answer = data['answers'][0] if isinstance(data['answers'],list) else data['answers']['review']
    if bad == 'missing':data.pop('answers')
    elif bad == 'extra':answer['execute'] = True
    elif bad == 'wrong_model':data['model'] = 'unapproved'
    elif bad == 'refusal':answer['type'] = 'refusal'
    elif bad == 'top_refusal':data['refusal'] = 'Insufficient context'
    elif bad == 'incomplete':data['status'] = 'incomplete'
    elif bad == 'probability':answer['confidence'] = float('nan')
    elif bad == 'boolean':answer['confidence'] = True
    elif bad == 'sum':
        if model == MODELS[2]:answer['probabilities'][0]['probability'] = .8
        else:answer['probabilities']['accept'] = .8
    elif bad == 'choice':answer['choice'] = 'accept'
    elif bad == 'usage':data['usage']['input_tokens'] = -1
    elif bad == 'missing_usage':data['usage'].pop('output_tokens')
    elif bad == 'total_usage':data['usage']['total_tokens'] = 1
    else:data['usage']['cost'] = float('inf')
    with pytest.raises(ValueError):validate_response(request(model),data)


@pytest.mark.parametrize('raw',['{}','{"model":"jev-latest","model":"jev-latest"}','NaN','[]','x'*128001,'{"secret":"fictional-native-decision-token"}'])
def test_malformed_oversized_and_credential_reflection(raw):
    with httpx.Client(transport=httpx.MockTransport(lambda _:httpx.Response(200,text=raw))) as client:
        session = DecisionSession(allow_external=True,client=client)
        with pytest.raises(HostedFailure):session.ask(request('jev-latest'))
        assert 'fictional-native-decision-token' not in json.dumps(session.receipt)


def test_timeout_unknown_charge_and_no_retry():
    calls = []
    def serve(r):
        calls.append(r);raise httpx.ReadTimeout('private provider detail')
    with httpx.Client(transport=httpx.MockTransport(serve)) as client:
        session = DecisionSession(allow_external=True,client=client)
        with pytest.raises(HostedFailure):session.ask(request('jev-latest'))
        with pytest.raises(HostedSetupRequired):session.ask(request('jev-latest'))
        assert session.receipt['charge_status'] == 'unknown'
    assert len(calls) == 1


def test_permission_and_input_bounds_before_network(monkeypatch):
    with pytest.raises(HostedSetupRequired):DecisionSession(allow_external=False)
    monkeypatch.delenv('EXPERIENTIAL_API_KEY')
    with pytest.raises(HostedSetupRequired):DecisionSession(allow_external=True)
    value = request('jev-latest').model_dump()
    value['questions'] *= 2
    with pytest.raises(ValidationError):DecisionInput(**value)
    value = request('jev-latest').model_dump();value['state'] = 'x'*12001
    with pytest.raises(ValidationError):DecisionInput(**value)


def test_duplicate_gpt_probability_rejected():
    data = response(MODELS[2]);data['answers'][0]['probabilities'].append(deepcopy(data['answers'][0]['probabilities'][0]))
    with pytest.raises(ValueError):validate_response(request(MODELS[2]),data)
