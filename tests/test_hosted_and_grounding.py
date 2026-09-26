"""Contract/security tests with HTTP test doubles, not live HF model quality."""
from copy import deepcopy
from datetime import timedelta
import json
import lzma
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from eightball.api import make_app
from eightball.store import Store as LegacyStore
from eightball.v2.store import Store
from eightball.v2.contracts import Case, Evidence, utcnow
from eightball.v2.intelligence import propose
from eightball.v2.hosted import (HuggingFaceSession, HostedFailure, HostedSetupRequired,
                                 configuration_status, settings, strict_schema, HF_ENDPOINT)
from eightball.v2.runtime_status import local_status
from endstate.compilation import (draft_outcome, drafting_schema, GroundedOutcomeFrame,
                                 DraftRequest, DraftFailure, validate_frame)

ROOT = Path(__file__).resolve().parents[1]
FRAME = json.loads((ROOT/'tests/fixtures/drafting/staged.json').read_text())
OUTCOME = "Obtain enough suitable chairs and the venue manager's written acceptance"
TOKEN = 'hf_fake_fixture_only_not_a_live_key'


@pytest.fixture(autouse=True)
def no_ambient_credentials(monkeypatch):
    for key in ('HF_TOKEN', 'EIGHTBALL_HF_MODEL', 'EIGHTBALL_HF_PROVIDER'):
        monkeypatch.delenv(key, raising=False)


def configured(monkeypatch):
    monkeypatch.setenv('HF_TOKEN', TOKEN)
    monkeypatch.setenv('EIGHTBALL_HF_MODEL', 'fictional/Model')
    monkeypatch.setenv('EIGHTBALL_HF_PROVIDER', 'fixture-provider')


def case():
    return Case(title='Fixture', client='Fictional agency', summary='A supply failure.',
                desired_outcome=OUTCOME, deadline=utcnow()+timedelta(days=2),
                evidence=[Evidence(id='source',title='Source',source='Fixture',text='The supplier refused the request.')])


def grounded_frame():
    frame = deepcopy(FRAME['frame'])
    frame['target_bindings'] = [{'criterion_index':i,'target_quote':OUTCOME}
                                for i in range(len(frame['success_criteria']))]
    return frame


def envelope(value):
    return {'model':'fixture-served-model','choices':[{'index':0,'finish_reason':'stop',
            'message':{'role':'assistant','content':json.dumps(value)}}],
            'usage':{'prompt_tokens':20,'completion_tokens':10,'total_tokens':30}}


def client(outputs=None, response=None):
    calls=[];remaining=deepcopy(outputs if outputs is not None else [{'items':[]}])
    def handle(request):
        calls.append(request)
        return response if response is not None else httpx.Response(200,json=envelope(remaining.pop(0)))
    return httpx.Client(transport=httpx.MockTransport(handle)),calls


def test_missing_key_has_no_request_and_no_key_exposure():
    cl,calls=client()
    with pytest.raises(HostedSetupRequired):
        HuggingFaceSession(allow_external=True,client=cl)
    assert not calls
    status=configuration_status()
    assert not status['configured'] and not status['credentials_validated']
    assert 'HF_TOKEN' in status['missing_settings']


@pytest.mark.parametrize('permission',[False,None,'true',1])
def test_explicit_boolean_permission_required(monkeypatch,permission):
    configured(monkeypatch);cl,calls=client()
    with pytest.raises(HostedSetupRequired):
        HuggingFaceSession(allow_external=permission,client=cl)
    assert not calls


@pytest.mark.parametrize('name,value',[
    ('EIGHTBALL_HF_PROVIDER','auto'),('EIGHTBALL_HF_PROVIDER','fastest'),
    ('EIGHTBALL_HF_PROVIDER','preferred'),('EIGHTBALL_HF_PROVIDER','cheapest'),
    ('EIGHTBALL_HF_MODEL','https://other.invalid/collect'),
    ('EIGHTBALL_HF_MODEL','Qwen/Model:fastest'),('EIGHTBALL_HF_MODEL','../secret'),
    ('HF_TOKEN','bad\nheader')])
def test_invalid_routing_or_credentials_fail_locally(monkeypatch,name,value):
    configured(monkeypatch);monkeypatch.setenv(name,value)
    with pytest.raises(HostedSetupRequired):settings()
    assert not configuration_status()['configured']


def test_transport_shape_receipt_and_immutable_configuration(monkeypatch):
    configured(monkeypatch);cl,calls=client()
    session=HuggingFaceSession(allow_external=True,client=cl)
    monkeypatch.setenv('EIGHTBALL_HF_PROVIDER','different')
    output,model=session.generate({'type':'object','properties':{'items':{'type':'array','items':{'type':'string'},'default':[]}}},'Extract',{'sources':[]})
    assert output=={'items':[]} and model=='fixture-served-model'
    assert len(calls)==1 and str(calls[0].url)==HF_ENDPOINT
    payload=json.loads(calls[0].content)
    assert payload['model']=='fictional/Model:fixture-provider'
    assert payload['response_format']['json_schema']['strict'] is True
    assert payload['response_format']['json_schema']['schema']['required']==['items']
    assert not payload['stream'] and payload['max_tokens']==4096
    assert calls[0].headers['authorization']=='Bearer '+TOKEN
    assert TOKEN not in json.dumps(session.receipt) and TOKEN not in repr(settings())
    assert TOKEN not in calls[0].content.decode()
    assert session.receipt['calls'][0]['usage']['total_tokens']==30
    assert configuration_status()['configuration_state']=='configured_not_tested'
    assert not configuration_status()['live_inference_verified']


@pytest.mark.parametrize('status',[301,302,400,401,402,403,429,500,503])
def test_errors_no_retry_redirect_or_sensitive_body_echo(monkeypatch,status):
    configured(monkeypatch);cl,calls=client(response=httpx.Response(status,text='SourceSecret '+TOKEN,
                             headers={'Location':'https://attacker.invalid/'}))
    s=HuggingFaceSession(allow_external=True,client=cl)
    with pytest.raises(HostedFailure) as caught:s.generate({},'test',{})
    assert len(calls)==1
    assert TOKEN not in str(caught.value) and 'SourceSecret' not in json.dumps(s.receipt)
    assert s.receipt['calls'][0]['status']=='failed'


@pytest.mark.parametrize('change',[
    lambda r:r['choices'][0].update(finish_reason='length'),
    lambda r:r['choices'][0].update(finish_reason='content_filter'),
    lambda r:r['choices'][0]['message'].update(refusal='refused'),
    lambda r:r['choices'][0]['message'].update(tool_calls=[{'x':'tool'}]),
    lambda r:r['choices'][0]['message'].update(role='user'),
    lambda r:r['choices'][0]['message'].update(content='{"value":NaN}'),
    lambda r:r['choices'][0]['message'].update(content='{"value":1e999}'),
    lambda r:r['choices'][0]['message'].update(content='{"x":1,"x":2}'),
    lambda r:r['choices'][0]['message'].update(content='```json\n{}\n```'),
    lambda r:r.update(choices=[]),
    lambda r:r.update(model=None),
    lambda r:r.update(usage={'completion_tokens':True})])
def test_malformed_refused_and_partial_responses_fail(monkeypatch,change):
    configured(monkeypatch);e=envelope({});change(e)
    cl,calls=client(response=httpx.Response(200,json=e))
    with pytest.raises(HostedFailure):HuggingFaceSession(allow_external=True,client=cl).generate({},'test',{})
    assert len(calls)==1


def test_response_size_and_request_size_are_bounded(monkeypatch):
    configured(monkeypatch);cl,calls=client(response=httpx.Response(200,content=b'x'*500001))
    with pytest.raises(HostedFailure,match='response_too_large'):
        HuggingFaceSession(allow_external=True,client=cl).generate({},'test',{})
    assert len(calls)==1
    cl,calls=client()
    with pytest.raises(HostedSetupRequired):
        HuggingFaceSession(allow_external=True,client=cl).generate({},'test',{'value':'x'*160000})
    assert not calls


def test_hosted_extraction_is_review_only_with_exact_source_span(monkeypatch):
    configured(monkeypatch);c=case();before=c.model_dump(mode='json')
    output={'items':[{'kind':'claim','text':c.evidence[0].text,
                    'source':{'evidence_id':'source','quote':c.evidence[0].text}}]}
    cl,calls=client([output]);p=propose(c,'huggingface','extract',['source'],allow_external=True,client=cl)
    assert c.model_dump(mode='json')==before and not c.observations
    assert p.items[0].object['provenance']['references'][0]['quote']==c.evidence[0].text
    assert p.raw_output['transport']['routing_provider']=='fixture-provider'
    assert TOKEN not in p.model_dump_json()


def test_hosted_graph_uses_same_compiler_and_exact_target_review(monkeypatch):
    configured(monkeypatch);c=case();cl,calls=client([grounded_frame(),FRAME['routes']])
    p=propose(c,'huggingface','graph',['source'],allow_external=True,client=cl)
    assert len(calls)==2 and len(p.items)>0 and not c.graph.actions
    trace=p.raw_output['payload']
    assert trace['target_coverage_checked'] is True and trace['target_bindings']
    assert all(i.object['approval_required'] for i in p.items if i.kind=='action')
    assert len(p.raw_output['transport']['calls'])==2


def test_hosted_inputs_scoped_before_network(monkeypatch):
    configured(monkeypatch);c=case();cl,calls=client()
    for ids in (['another_case'],['source','source']):
        with pytest.raises(ValueError):propose(c,'huggingface','extract',ids,allow_external=True,client=cl)
    c.evidence[0].status='retracted'
    with pytest.raises(ValueError):propose(c,'huggingface','extract',['source'],allow_external=True,client=cl)
    assert not calls


def test_api_missing_setup_does_not_record_phantom_model_run(tmp_path):
    old=LegacyStore(str(tmp_path/'s.db'));store=Store(old.path);c=case();store.create(c,fixture=True)
    token='local_fixture_token_is_not_real_12345'
    api=TestClient(make_app(old,token),headers={'Authorization':'Bearer '+token})
    r=api.post('/api/v2/cases/'+c.id+'/analyse',json={'expected_revision':0,'provider':'huggingface',
               'purpose':'graph','source_ids':['source'],'allow_external':True})
    assert r.status_code==422 and not store.proposals(c.id) and store.get(c.id)==c
    assert 'HF_TOKEN' in r.json()['detail']


def test_frame_references_fail_before_a_second_generation_call():
    frame=deepcopy(FRAME['frame']);frame['verification']['requires_existing']=['invented']
    calls=[]
    def generate(*_):calls.append(True);return frame,'fixture'
    with pytest.raises(DraftFailure) as caught:
        draft_outcome({'namespace':'x','outcome':OUTCOME,'brief':'Fictional'},generate)
    assert len(calls)==1 and caught.value.trace['failed_stage']=='frame'
    assert caught.value.trace['diagnostic']['code']=='unknown_existing_reference'


@pytest.mark.parametrize('bindings,code',[
    ([{'criterion_index':0,'target_quote':'The supplier cannot deliver chairs'}],'unsupported_target_quote'),
    ([{'criterion_index':0,'target_quote':'Obtain enough suitable chairs'}],'incomplete_target_coverage'),
    ([{'criterion_index':3,'target_quote':OUTCOME}],'unbound_success_criterion'),
    ([{'criterion_index':0,'target_quote':OUTCOME}]*2,'duplicate_target_binding')])
def test_target_coverage_rejects_source_facts_omissions_bad_indexes(bindings,code):
    frame=grounded_frame()
    # Single combined success criterion allows the tests to isolate quote rules.
    frame['success_criteria']=frame['success_criteria'][:1];frame['target_bindings']=bindings
    with pytest.raises(ValueError) as caught:validate_frame(GroundedOutcomeFrame.model_validate(frame),OUTCOME,[])
    assert getattr(caught.value,'code',None)==code


def test_dynamic_schema_does_not_allow_invented_existing_ids():
    assert drafting_schema(GroundedOutcomeFrame,[])['$defs']['OperationDraft']['properties']['requires_existing']['maxItems']==0
    from endstate.compilation import KnownCondition
    schema=drafting_schema(GroundedOutcomeFrame,[KnownCondition(id='real',title='Actual')])
    assert schema['$defs']['OperationDraft']['properties']['requires_existing']['items']['enum']==['real']


def test_historical_failed_frame_is_still_rejected_before_route_call():
    evidence=json.loads(lzma.decompress((ROOT/'docs/evidence/staged-qwen-attempt1.json.xz').read_bytes()))
    g=next(r for r in evidence['results'] if r['purpose']=='graph')
    frame=json.loads(g['raw_responses'][0]['message']['content']);calls=[]
    def generate(*_):calls.append(True);return frame,'historical-qwen'
    with pytest.raises(DraftFailure) as caught:
        draft_outcome({'namespace':'replay','outcome':OUTCOME,'brief':'Fictional supply problem'},generate)
    assert len(calls)==1 and caught.value.trace['failed_stage']=='frame'


def test_config_and_import_never_make_network_requests(monkeypatch):
    monkeypatch.setattr(httpx.Client,'send',lambda *a,**k:pytest.fail('Unexpected HTTP'))
    assert not configuration_status()['configured']
    configured(monkeypatch)
    assert configuration_status()['configured']


@pytest.mark.parametrize('present',[True,False])
def test_explicit_local_check_does_not_infer_or_download(monkeypatch,present):
    monkeypatch.setenv('EIGHTBALL_OLLAMA_MODEL','fixture:4b');calls=[]
    def handle(req):
        calls.append(req)
        return httpx.Response(200,json={'version':'fixture'} if req.url.path=='/api/version' else
                       {'models':[{'name':'fixture:4b'}] if present else []})
    data=local_status(httpx.Client(transport=httpx.MockTransport(handle)))
    assert len(calls)==2 and all(r.method=='GET' for r in calls)
    assert data['runtime']=='running' and data['model_present'] is present
    assert not data['inference_performed'] and not data['download_started']


def test_unreachable_runtime_does_not_claim_not_installed():
    def fail(req):raise httpx.ConnectError('not reachable',request=req)
    data=local_status(httpx.Client(transport=httpx.MockTransport(fail)))
    assert data['runtime']=='unreachable' and data['model_present'] is None
    assert 'may be stopped or not installed' in data['note']


def test_question_context_does_not_leak_unselected_source_quotes(monkeypatch):
    from eightball.v2.contracts import Condition, Provenance, Span, Question
    configured(monkeypatch);c=case();secret='Unselected private source sentence.'
    c.evidence.append(Evidence(id='other',title='Not selected',source='Fixture',text=secret))
    c.graph.conditions.append(Condition(id='goal',title='Agreement accepted',confirmation='Written acceptance',
       provenance=Provenance(references=[Span(evidence_id='other',start=0,end=len(secret),quote=secret)])))
    c.questions.append(Question(id='q',question='Who can approve?',why='Authority matters',answer=secret))
    cl,calls=client([{'questions':[]}])
    p=propose(c,'huggingface','questions',['source'],allow_external=True,client=cl)
    sent=json.loads(calls[0].content)
    assert secret not in json.dumps(sent) and 'Agreement accepted' in json.dumps(sent)
    assert len(p.items)==0


def test_fixture_file_keeps_the_original_four_case_gate():
    from hashlib import sha256
    fixtures=json.loads((ROOT/'evals/generation-cases.json').read_text())
    assert len(fixtures)==4
    assert sha256(json.dumps(fixtures).encode()).hexdigest()=='6758c54a9e873bf2f67ced368555b871d9cf890b55b4df33762a035be1deaeb3'


def test_hosted_cli_refuses_without_explicit_flag_or_key(tmp_path):
    import subprocess,sys,os
    env={**os.environ,'HF_TOKEN':'','EIGHTBALL_HF_MODEL':'','EIGHTBALL_HF_PROVIDER':''}
    for arguments in ([],['--allow-hosted']):
        result=subprocess.run([sys.executable,str(ROOT/'evals/live_huggingface.py'),*arguments,'--output',str(tmp_path/'report')],
                              cwd=ROOT,env=env,capture_output=True,text=True,timeout=10)
        assert result.returncode==2 and not (tmp_path/'report').exists()


def test_local_status_endpoint_requires_operator_authentication(tmp_path):
    token='local_fixture_token_is_not_real_12345'
    app=make_app(LegacyStore(str(tmp_path/'auth.db')),token)
    assert TestClient(app).post('/api/v2/intelligence/local-status',json={}).status_code==401


def test_hosted_local_request_limit_failure_is_not_logged_as_inference(tmp_path,monkeypatch):
    configured(monkeypatch)
    def fail_before_request(self,*args):
        raise HostedSetupRequired('Context too large; no request was made.')
    monkeypatch.setattr(HuggingFaceSession,'generate',fail_before_request)
    old=LegacyStore(str(tmp_path/'preflight.db'));store=Store(old.path);c=case();store.create(c,fixture=True)
    token='local_fixture_token_is_not_real_12345'
    api=TestClient(make_app(old,token),headers={'Authorization':'Bearer '+token})
    r=api.post('/api/v2/cases/'+c.id+'/analyse',json={'expected_revision':0,'provider':'huggingface',
               'purpose':'graph','source_ids':['source'],'allow_external':True})
    assert r.status_code==422 and not store.proposals(c.id) and store.get(c.id)==c
