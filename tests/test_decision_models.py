"""Native decision wire/negative fixtures. No live network or inference."""
from copy import deepcopy
import json

import httpx
import pytest
from pydantic import ValidationError

from endstate.intelligence.decisions import DecisionInput
from eightball.v2.decision_models import COST_POLICY, DecisionSession, payload_for, validate_response
from eightball.store import digest
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


@pytest.mark.parametrize('model', MODELS)
@pytest.mark.parametrize('cost,nanos', [(0,0), (0.0,0), (8.547e-6,8547),
    (3.5868e-5,35868), (1e-9,1), (0.01,10000000), (12.345678901,12345678901)])
def test_platform_cost_translation_preserves_original_response_and_billing_unknown(model, cost, nanos):
    data = response(model)
    data['usage'].update(cost=cost, is_byok=False)
    original = deepcopy(data)
    calls = []
    def serve(r):
        calls.append(r)
        return httpx.Response(200, json=data)
    with httpx.Client(transport=httpx.MockTransport(serve)) as client:
        session = DecisionSession(allow_external=True, client=client)
        result = session.ask(request(model))
    assert len(calls) == 1 and calls[0].method == 'POST'
    assert result['usage']['cost_nano_usd'] == nanos and type(result['usage']['cost_nano_usd']) is int
    assert result['usage']['cost'] == cost
    assert session.response == data == original
    assert session.receipt['response_sha256'] == digest(original)
    assert 'cost_nano_usd' not in validate_response(request(model), original)['usage']
    assert session.receipt['charge_status'] == 'unknown' and session.receipt['cost_policy'] == COST_POLICY
    assert session.receipt['cost_normalization'] == dict(status='normalized', basis=COST_POLICY,
        source_cost_usd=cost, source_is_byok=False, cost_nano_usd=nanos, arithmetic='exact_decimal_no_rounding',
        source_cost_decimal=str(cost))


@pytest.mark.parametrize('model', MODELS)
@pytest.mark.parametrize('overrides', [{}, {'is_byok':True}, {'is_byok':None}, {'is_byok':0},
    {'is_byok':'false'}, {'is_byok':False,'currency':'EUR'}, {'is_byok':False,'cost_currency':'GBP'},
    {'is_byok':False,'cost_unit':'nano_usd'}, {'is_byok':False,'currency':None},
    {'is_byok':False,'pricing_known':False}, {'is_byok':False,'pricing_known':1},
    {'is_byok':False,'cost':1e-10}, {'is_byok':False,'cost':1.0000000000000002e-9}])
def test_unconfirmed_funding_units_and_fractional_nanos_remain_unknown(model, overrides):
    data = response(model)
    data['usage'].update(overrides)
    with httpx.Client(transport=httpx.MockTransport(lambda _:httpx.Response(200,json=data))) as client:
        session = DecisionSession(allow_external=True,client=client)
        result = session.ask(request(model))
    assert 'cost_nano_usd' not in result['usage']
    assert session.receipt['cost_normalization']['status'] == 'unknown'
    assert session.receipt['inference_calls'] == 1 and session.receipt['charge_status'] == 'unknown'


@pytest.mark.parametrize('nanos', [0,1,0.5])
def test_explicit_nanos_are_never_overwritten_with_generic_cost(nanos):
    data = response(MODELS[0])
    data['usage'].update(cost=0.5, cost_nano_usd=nanos)
    with httpx.Client(transport=httpx.MockTransport(lambda _:httpx.Response(200,json=data))) as client:
        session = DecisionSession(allow_external=True,client=client)
        result = session.ask(request(MODELS[0]))
    assert result['usage']['cost_nano_usd'] == nanos
    assert session.receipt['cost_normalization'] == {'status':'explicit_field_preserved'}


@pytest.mark.parametrize('extra', [{'cost':0.5,'is_byok':False},
    {'is_byok':True}, {'is_byok':False,'pricing_known':False},
    {'is_byok':False,'currency':'EUR'}])
def test_explicit_cost_cannot_override_known_funding_or_unit_conflicts(extra):
    data = response(MODELS[0]); data['usage'].update(cost_nano_usd=0, **extra)
    original = deepcopy(data)
    with httpx.Client(transport=httpx.MockTransport(lambda _:httpx.Response(200,json=data))) as client:
        session = DecisionSession(allow_external=True,client=client)
        result = session.ask(request(MODELS[0]))
    assert 'cost_nano_usd' not in result['usage']
    assert session.response == original and session.receipt['response_sha256'] == digest(original)
    assert session.receipt['cost_normalization']['source_cost_nano_usd'] == 0
    assert session.receipt['cost_normalization']['status'] == 'unknown'


def test_consistent_explicit_cost_is_preserved():
    data = response(MODELS[0]); data['usage'].update(cost=1e-9,is_byok=False,cost_nano_usd=1)
    with httpx.Client(transport=httpx.MockTransport(lambda _:httpx.Response(200,json=data))) as client:
        session = DecisionSession(allow_external=True,client=client)
        result = session.ask(request(MODELS[0]))
    assert result['usage']['cost_nano_usd'] == 1
    assert session.receipt['cost_normalization'] == {'status':'explicit_field_preserved'}


@pytest.mark.parametrize('literal,nanos', [('0.0000000010000000000000000001',None),
    ('0.0000000009999999999999999999',None), ('1e-100000000',None), ('0.'+'0'*100+'1',None),
    ('0.000000001000',1), ('8.547e-6',8547)])
def test_original_numeric_lexeme_is_not_rounded_by_float_parsing(literal, nanos):
    from hashlib import sha256
    data = response(MODELS[0]); data['usage']['is_byok'] = False
    raw = json.dumps(data).replace('"cost": 0', '"cost": '+literal).encode()
    with httpx.Client(transport=httpx.MockTransport(lambda _:httpx.Response(200,content=raw))) as client:
        session = DecisionSession(allow_external=True,client=client)
        result = session.ask(request(MODELS[0]))
    assert result['usage'].get('cost_nano_usd') == nanos
    assert session.receipt['response_body_sha256'] == sha256(raw).hexdigest()
    if len(literal) <= 64:
        assert session.receipt['cost_normalization']['source_cost_decimal'] == literal
    else:
        assert 'source_cost_decimal' not in session.receipt['cost_normalization']
    assert session.response == json.loads(raw)


def test_oversized_reported_cost_fails_without_unhandled_overflow():
    data = response(MODELS[0]); data['usage']['cost'] = 10**400
    with httpx.Client(transport=httpx.MockTransport(lambda _:httpx.Response(200,json=data))) as client:
        session = DecisionSession(allow_external=True,client=client)
        with pytest.raises(HostedFailure): session.ask(request(MODELS[0]))
    assert session.receipt['status'] == 'failed_validation_or_transport'
