import json
import math
import httpx
import pytest
from eightball.providers import LABELS, jev_classify, gliclass_classify, ollama_extract, ProviderUnavailable, finite_score


def mock_client(result,status=200,check=None):
    def handle(request):
        if check:check(request)
        return httpx.Response(status,json=result)
    return httpx.Client(transport=httpx.MockTransport(handle))


def jev_result():
    return {'model':'jev-1.13.0','answers':{'event_type':{'type':'choice','choice':'deadline_change',
        'confidence':0.86,'probabilities':{k:0.9 if k=='deadline_change' else 0.025 for k in LABELS}}}}


def test_jev_contract_and_human_review(monkeypatch):
    monkeypatch.setenv('TYPESAFE_API_KEY','fixture-only')
    def check(r):
        assert str(r.url)=='https://api.typesafe.ai/v1/systemone'
        body=json.loads(r.content);assert body['model']=='jev-1.13.0'
        assert body['questions']['event_type']['type']=='choice'
        assert body['state']=={'untrusted_evidence_text':'A deadline tomorrow.'}
    out=jev_classify('A deadline tomorrow.',allow_external=True,client=mock_client(jev_result(),check=check))
    assert out['needs_review'] and out['label']=='deadline_change'
    assert out['provider_confidence']==0.86


@pytest.mark.parametrize('status',[401,422,429,500,529])
def test_provider_failures_abstain(monkeypatch,status):
    monkeypatch.setenv('TYPESAFE_API_KEY','fixture-only')
    with pytest.raises(ProviderUnavailable):jev_classify('Test',allow_external=True,client=mock_client({},status))


def test_external_use_requires_permission(monkeypatch):
    monkeypatch.setenv('TYPESAFE_API_KEY','fixture-only')
    with pytest.raises(ProviderUnavailable):jev_classify('Test',allow_external=False)


@pytest.mark.parametrize('mutation',[
    lambda r:r['answers']['event_type'].update(choice='delete_evidence'),
    lambda r:r['answers']['event_type'].update(confidence=2),
    lambda r:r['answers']['event_type']['probabilities'].update(routine=0.9),
    lambda r:r['answers']['event_type']['probabilities'].pop('unclear'),
    lambda r:r['answers']['event_type'].update(choice='routine'),
    lambda r:r.update(answers={}),
])
def test_invalid_jev_answers_rejected(monkeypatch,mutation):
    monkeypatch.setenv('TYPESAFE_API_KEY','fixture-only');r=jev_result();mutation(r)
    with pytest.raises(ProviderUnavailable):jev_classify('Test',allow_external=True,client=mock_client(r))


def test_gliclass_scores_not_misrepresented_as_calibrated_probabilities():
    def pipeline(text,labels,threshold):
        return [[{'label':label,'score':0.92 if i==0 else 0.12} for i,label in enumerate(labels)]]
    out=gliclass_classify('Fictional deadline',pipeline=pipeline)
    assert out['provider_confidence'] is None and out['needs_review']
    assert out['label']=='deadline_change'
    assert sum(out['scores'].values())>1


def test_gliclass_ambiguous_outputs_abstain():
    def pipeline(text,labels,threshold):return [[{'label':label,'score':0.6} for label in labels]]
    assert gliclass_classify('Ambiguous',pipeline=pipeline)['abstained']


@pytest.mark.parametrize('value',[-1,1.1,float('nan'),float('inf'),True,'0.9',None])
def test_bad_model_scores_rejected(value):
    with pytest.raises(ValueError):finite_score(value)


def extraction(proposal):return {'message':{'content':json.dumps({'proposals':[proposal]})}}


def test_local_source_exact_extraction():
    item={'condition_id':'root','value':True,'quote':'Root cause verified.'}
    out=ollama_extract('Notes: Root cause verified.',[{'id':'root','title':'Root cause established'}],client=mock_client(extraction(item)))
    assert out['proposals'][0]['source_start']==7
    assert out['proposals'][0]['status']=='unverified_proposal'
    assert out['needs_review']


@pytest.mark.parametrize('item',[
    {'condition_id':'root','value':True,'quote':'Invented quote'},
    {'condition_id':'unknown','value':True,'quote':'Root cause verified.'},
    {'condition_id':'root','value':'true','quote':'Root cause verified.'},
    {'condition_id':'root','value':True,'quote':'Root cause verified.','approve':True},
    {'condition_id':'root','value':True,'quote':''},
])
def test_unsupported_extraction_rejected(item):
    with pytest.raises(ProviderUnavailable):ollama_extract('Root cause verified.',[{'id':'root'}],client=mock_client(extraction(item)))


def test_local_pipeline_runtime_failure_is_unavailable():
    def unavailable(*args,**kwargs):
        raise RuntimeError('Local inference failure')
    with pytest.raises(ProviderUnavailable):
        gliclass_classify('Fixture text',pipeline=unavailable)
