"""Compiler evidence, not real-model accuracy. All inputs are fictional fixtures."""
from __future__ import annotations
from copy import deepcopy
from datetime import timedelta
from pathlib import Path
import json
from hashlib import sha256

import httpx
import pytest
from pydantic import ValidationError

from endstate.compilation import (
    CompileRequest, DraftRequest, OutcomeFrame, RouteDrafts, compile_outcome, draft_outcome, DraftFailure,
    PROMPT_VERSION,
)
from endstate.contracts import Graph, PlanningSnapshot, Condition, literals
from endstate.primitives import Evidence, Observation, utcnow
from endstate.api import calculate
from eightball.v2.intelligence import propose, DraftGraph
from eightball.v2.commands import merge_object, Command, apply
from eightball.v2.contracts import Case
from eightball.v2.planner import plan
from eightball.v2.store import Store

FIXTURE = json.loads((Path(__file__).parent / 'fixtures/drafting/staged.json').read_text())
OUTCOME = 'Obtain enough suitable chairs and the venue manager\'s written acceptance'


def request():
    return {'namespace':'fictional_draft','outcome':OUTCOME,**deepcopy(FIXTURE)}


def case():
    return Case(title='Chair disruption',client='Fictional venue',summary='A supplier cannot deliver; venue spares and local hire are possible alternatives.',
                desired_outcome=OUTCOME,deadline=utcnow()+timedelta(days=2),
                evidence=[Evidence(id='source',title='Fictional note',source='Fixture',text='Spare chairs or a local hire may be available.')])


def http_provider(outputs=None):
    outputs=deepcopy(outputs or [FIXTURE['frame'],FIXTURE['routes']]); calls=[]
    def respond(req):
        body=json.loads(req.content);calls.append(body)
        assert str(req.url)=='http://127.0.0.1:11434/api/chat'
        output=outputs.pop(0)
        if 'target_bindings' in body['format'].get('properties',{}) and 'success_criteria' in output:
            output['target_bindings']=[{'criterion_index':i,'target_quote':OUTCOME} for i in range(len(output['success_criteria']))]
        return httpx.Response(200,json={'model':'fixture-model','done':True,'message':{'content':json.dumps(output)}})
    return httpx.Client(transport=httpx.MockTransport(respond)),calls


def projected(compiled):
    return PlanningSnapshot(id='fixture',owner='Lead',deadline=utcnow()+timedelta(days=2),budget=10000,
                            graph=Graph(conditions=compiled.graph.conditions,actions=compiled.graph.actions,
                                        objectives=compiled.graph.objectives))


def test_compiler_produces_two_complete_alternatives_with_shared_verifier():
    result=compile_outcome(request());snapshot=projected(result)
    response=calculate({'snapshot':snapshot,'as_of':utcnow()})
    assert len(response.plan['routes'])==2
    assert not response.plan['outcome_evidenced']
    verifier=next(o.object_id for o in result.origins if o.draft_pointer=='/frame/verification')
    assert all(verifier==r['actions'][-1] and len(r['actions'])==3 for r in response.plan['routes'])
    assert all(not r['hard_breaches'] for r in response.plan['routes'])
    assert not snapshot.observations and not snapshot.approvals


def test_every_generated_action_has_an_exact_draft_origin_no_synthetic_actions():
    data=request();result=compile_outcome(data)
    mapped={o.object_id:o for o in result.origins}
    for action in result.graph.actions:
        origin=mapped[action.id];value=data
        for key in origin.draft_pointer.strip('/').split('/'):
            value=value[int(key)] if isinstance(value,list) else value[key]
        assert action.title==value['title'] and action.owner==value['owner']
        assert action.minutes==value['minutes'] and action.cost==value['cost']
    assert len(result.graph.actions)==1+sum(len(r['sequential_steps'])+1 for r in data['routes']['routes'])
    assert result.graph.objectives[0].title==OUTCOME


def test_no_target_bypass_or_verifier_dependency_on_its_own_result():
    result=compile_outcome(request());graph=result.graph
    goals={c for o in graph.objectives for c,_ in literals(o.success)}
    producers=[a for a in graph.actions if goals & {e.condition_id for e in a.effects}]
    assert len(producers)==1
    assert not goals & {c for c,_ in literals(producers[0].requires)}
    assert {e.condition_id for e in producers[0].effects}==goals


def test_no_generated_authority_and_unknown_wait_preserved():
    result=compile_outcome(request())
    assert all(a.approval_required for a in result.graph.actions)
    assert all(a.risk=='high' and a.reversibility=='difficult' for a in result.graph.actions)
    assert all(a.contingent and a.wait_minutes is None for a in result.graph.actions)


def test_compile_is_deterministic_detached_and_namespaced():
    data=request();before=deepcopy(data);a=compile_outcome(data);b=compile_outcome(data)
    assert a.model_dump()==b.model_dump()
    a.graph.actions[0].title='Changed returned object'
    assert data==before and b.graph.actions[0].title!='Changed returned object'
    data['namespace']='other_draft'
    c=compile_outcome(data)
    assert not {x.id for x in b.graph.actions} & {x.id for x in c.graph.actions}


@pytest.mark.parametrize('change',[
 lambda d:d['frame'].pop('verification'),
 lambda d:d['frame'].update(verification=None),
 lambda d:d['frame']['verification'].pop('title'),
 lambda d:d['frame'].update(success_criteria=[]),
 lambda d:d['frame'].update(approaches=[]),
 lambda d:d['routes']['routes'][0].pop('establish_readiness'),
 lambda d:d['routes']['routes'][0].update(sequential_steps=[]),
 lambda d:d['routes']['routes'].pop(),
 lambda d:d['routes']['routes'][1].update(approach_index=0),
 lambda d:d['routes']['routes'][1].update(approach_index=2),
 lambda d:d['frame']['verification'].update(minutes=True),
 lambda d:d['frame']['verification'].update(minutes=-1),
 lambda d:d['frame']['verification'].update(cost=-1),
 lambda d:d['frame']['verification'].update(wait_minutes=-1),
 lambda d:d['frame']['verification'].update(approval_required=False),
 lambda d:d['frame']['verification'].update(external='false'),
 lambda d:d.update(observations=[{'value':True}]),
 lambda d:d['frame'].update(selected_decision='yes'),
 lambda d:d['routes']['routes'][0]['sequential_steps'][0]['action'].update(requires_existing=['not_in_case']),
])
def test_invalid_or_privileged_drafts_fail_closed(change):
    data=request();change(data)
    with pytest.raises((ValueError,ValidationError)):compile_outcome(data)


def test_cosmetic_renaming_does_not_manufacture_alternative_routes():
    data=request();data['routes']['routes'][1]=deepcopy(data['routes']['routes'][0]);data['routes']['routes'][1]['approach_index']=1
    with pytest.raises(ValueError,match='identical work'):compile_outcome(data)


@pytest.mark.parametrize('reserved', ['readiness', 0, 1])
@pytest.mark.parametrize('variant', ['exact', 'case', 'whitespace'])
def test_step_results_cannot_be_declared_success_before_verification(reserved, variant):
    data=request()
    data['frame']['success_criteria'].append({'title':'Independent acceptance confirmed',
                                             'confirmation':'Written acceptance from an authorised reviewer'})
    result=deepcopy(data['frame']['readiness'] if reserved=='readiness' else data['frame']['success_criteria'][reserved])
    if variant=='case':result['title']=result['title'].upper()
    if variant=='whitespace':result['title']='  '+'  '.join(result['title'].split())+'  '
    data['routes']['routes'][0]['sequential_steps'][0]['result']=result
    with pytest.raises(ValueError,match='bypass'):compile_outcome(data)


def test_existing_prerequisite_references_are_retained_as_deltas():
    data=request();data['existing_conditions']=[{'id':'permission','title':'Permission obtained'}]
    data['frame']['verification']['requires_existing']=['permission']
    result=compile_outcome(data)
    assert result.graph.required_existing_conditions==['permission']
    assert 'permission' not in {c.id for c in result.graph.conditions}
    graph=Graph(conditions=result.graph.conditions+[Condition(id='permission',title='Permission obtained',confirmation='Written authority')],
                actions=result.graph.actions,objectives=result.graph.objectives)
    snapshot=PlanningSnapshot(id='fixture',owner='Lead',deadline=utcnow()+timedelta(days=2),graph=graph)
    p=calculate({'snapshot':snapshot,'as_of':utcnow()}).plan
    assert all(any(g['condition_id']=='permission' for g in r['evidence_gaps']) for r in p['routes'])


def test_mutated_nested_models_are_revalidated():
    data=CompileRequest.model_validate(request());data.frame.success_criteria.clear()
    with pytest.raises(ValidationError):compile_outcome(data)


def test_provider_independent_pipeline_calls_two_stages_and_retains_trace():
    returned=[deepcopy(FIXTURE['frame']),deepcopy(FIXTURE['routes'])];calls=[]
    def provider(schema,system,context):
        calls.append((schema,context,system));return returned.pop(0),'fake-local-model'
    data={'namespace':'test','outcome':OUTCOME,'brief':'Fictional disrupted supply'}
    compiled,trace,model=draft_outcome(data,provider)
    assert len(calls)==2 and model=='fake-local-model'
    assert calls[1][1]['approach_indices'][1]['approach_index']==1
    rules=calls[1][1]['compilation_rules']
    assert rules['reserved_result_titles']==[FIXTURE['frame']['readiness']['title'],
                                             *[c['title'] for c in FIXTURE['frame']['success_criteria']]]
    assert 'reserved_result_titles' in calls[1][2]
    assert 'frame.verification' in calls[1][0]['$defs']['RouteDraft']['properties']['establish_readiness']['description']
    assert trace['prompt_version']==PROMPT_VERSION
    assert trace['frame']==FIXTURE['frame'] and trace['routes']==FIXTURE['routes']
    assert len(compiled.graph.actions)==5


BASELINE_PATH=Path(__file__).resolve().parents[1]/'docs/evidence/qwen-baseline-2026-09-27.json'
BASELINE=json.loads(BASELINE_PATH.read_text())


@pytest.mark.parametrize('record', [r for r in BASELINE['results'] if r['purpose']=='extract'],
                         ids=lambda record:record['title'])
def test_historical_extractions_replay_without_new_inference_or_case_changes(record):
    c=case();c.evidence[0].text=record['source'];before=c.model_dump(mode='json');calls=[]
    def respond(req):
        calls.append(req)
        return httpx.Response(200,json=deepcopy(record['raw_responses'][len(calls)-1]))
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        proposal=propose(c,'ollama','extract',['source'],client=client)
    assert len(calls)==1 and c.model_dump(mode='json')==before
    assert proposal.raw_output==record['proposal']['raw_output']
    assert len(proposal.items)==record['proposal_count']
    assert all(item.disposition=='pending' for item in proposal.items)


def test_unmodified_september_qwen_graph_remains_rejected_with_exact_trace():
    # Raw historical inference, replayed through a controlled transport. Not a new model run.
    assert sha256(BASELINE_PATH.read_bytes()).hexdigest()=='4db80b5a17816f414cd09f1f27737ca12e3b3cc95f9fb2009854cc5154a82992'
    fixtures=json.loads((BASELINE_PATH.parents[2]/'evals/generation-cases.json').read_text())
    assert sha256(json.dumps(fixtures).encode()).hexdigest()==BASELINE['fixture_sha256']
    record=next(r for r in BASELINE['results'] if r['purpose']=='graph')
    c=case();c.evidence[0].text=record['source'];c.summary=record['source']
    before=c.model_dump(mode='json');calls=[]
    def respond(req):
        calls.append(json.loads(req.content))
        return httpx.Response(200,json=deepcopy(record['raw_responses'][len(calls)-1]))
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        with pytest.raises(DraftFailure) as caught:
            propose(c,'ollama_staged','graph',['source'],client=client)
    trace=caught.value.trace
    assert len(calls)==2 and c.model_dump(mode='json')==before
    assert trace['failed_stage']=='compile' and trace['stage_count']==2
    assert trace['diagnostic']==record['diagnostic']
    assert trace['frame']==json.loads(record['raw_responses'][0]['message']['content'])
    assert trace['routes']==json.loads(record['raw_responses'][1]['message']['content'])
    assert trace['prompt_version']==PROMPT_VERSION


def test_generation_runner_retains_versions_and_raw_responses_on_replayed_failure(monkeypatch):
    from evals import live_generation
    record=next(r for r in BASELINE['results'] if r['purpose']=='graph')
    class ReplayRecorder:
        def __init__(self):
            self.responses=[]
            self.client=httpx.Client(transport=httpx.MockTransport(self.respond))
        def respond(self,req):
            raw=deepcopy(record['raw_responses'][len(self.responses)])
            self.responses.append(raw)
            return httpx.Response(200,json=raw)
        def post(self,*args,**kwargs):return self.client.post(*args,**kwargs)
    monkeypatch.setattr(live_generation,'Recorder',ReplayRecorder)
    monkeypatch.setenv('EIGHTBALL_GRAPH_PROVIDER','ollama_staged')
    result=live_generation.run_one(record['title'],record['source'],'graph',record['desired_outcome'])
    assert result['status']=='rejected_or_unavailable' and result['live_state_unchanged']
    assert result['compiler_version']=='endstate.draft.v1' and result['prompt_version']==PROMPT_VERSION
    assert result['diagnostic']==record['diagnostic']
    assert result['raw_responses']==record['raw_responses']


def test_invalid_first_stage_never_runs_second_stage():
    calls=[]
    def provider(*_):calls.append(True);return {'readiness':{}},'mock'
    with pytest.raises(DraftFailure):draft_outcome({'namespace':'test','outcome':OUTCOME,'brief':'Fictional case'},provider)
    assert len(calls)==1


def test_target_quotes_keep_connectives_without_relaxing_coverage():
    from endstate.compilation import GroundedOutcomeFrame, validate_frame, DraftValidationError, TARGET_PROMPT
    outcome = 'Deliver supplies and record acceptance'
    raw = deepcopy(FIXTURE['frame'])
    raw['success_criteria'] = [deepcopy(raw['success_criteria'][0]) for _ in range(2)]
    raw['success_criteria'][1]['title'] = 'Acceptance recorded'
    raw['target_bindings'] = [
        {'criterion_index': 0, 'target_quote': 'Deliver supplies'},
        {'criterion_index': 1, 'target_quote': 'record acceptance'}]
    with pytest.raises(DraftValidationError) as caught:
        validate_frame(GroundedOutcomeFrame.model_validate(raw), outcome, [])
    assert caught.value.code == 'incomplete_target_coverage'
    raw['target_bindings'][1]['target_quote'] = 'and record acceptance'
    validate_frame(GroundedOutcomeFrame.model_validate(raw), outcome, [])
    assert 'connecting words' in TARGET_PROMPT and 'quotes may overlap' in TARGET_PROMPT


def test_model_switch_between_stages_is_rejected():
    outputs=[(FIXTURE['frame'],'one'),(FIXTURE['routes'],'two')]
    with pytest.raises(DraftFailure,match='routes'):
        draft_outcome({'namespace':'test','outcome':OUTCOME,'brief':'Fictional'},lambda *_:outputs.pop(0))


def test_staged_http_adapter_does_not_mutate_case_or_claim_live_inference():
    c=case();before=c.model_dump(mode='json');client,calls=http_provider()
    p=propose(c,'ollama_staged','graph',['source'],client=client)
    assert len(calls)==2 and c.model_dump(mode='json')==before
    assert p.provider=='ollama_staged' and p.raw_output['stage_count']==2 and p.model=='fixture-model'
    assert all(i.disposition=='pending' for i in p.items)
    assert not c.observations and not c.graph.objectives


def test_proposal_review_persistence_routes_and_completion_stay_separate(tmp_path):
    c=case();store=Store(str(tmp_path/'cases.db'));store.create(c,fixture=True)
    client,_=http_provider();p=propose(c,'ollama_staged','graph',['source'],client=client);store.save_proposal(p)
    accepted,_=store.review(c.id,p.id,'review',0,[{'id':i.id,'disposition':'accepted'} for i in p.items])
    assert not accepted.observations and len(plan(accepted)['routes'])==2
    first=accepted.graph.actions[0]
    accepted,_=store.change(c.id,Command(event_id='approve',expected_revision=accepted.revision,kind='approve',payload={'action_id':first.id}))
    accepted,_=store.change(c.id,Command(event_id='complete',expected_revision=accepted.revision,kind='complete',payload={'action_id':first.id}))
    assert plan(accepted)['states'][first.effects[0].condition_id]['status']=='unknown'
    assert store.audit(c.id)['valid'] and store.audit(c.id)['replay_matches_snapshot']


def test_reject_all_staged_proposals_preserves_the_live_case(tmp_path):
    c=case();store=Store(str(tmp_path/'cases.db'));store.create(c,fixture=True);client,_=http_provider()
    p=propose(c,'ollama_staged','graph',['source'],client=client);store.save_proposal(p)
    updated,delta=store.review(c.id,p.id,'reject',0,[{'id':i.id,'disposition':'rejected'} for i in p.items])
    assert updated==c and delta['no_case_change']


def test_real_historical_bad_graph_is_still_rejected_not_repaired():
    path=Path(__file__).resolve().parents[1]/'docs/evidence/rejected-qwen-graph.json'
    raw=json.loads(path.read_text())
    # The preserved file contains the actual model graph, not a repaired fixture.
    assert raw['final_verification_action_id'] not in {a['id'] for a in raw['actions']}
    with pytest.raises(ValidationError):DraftGraph.model_validate(raw)


def test_failed_second_stage_trace_preserves_real_raw_data_without_live_changes():
    outputs=[(FIXTURE['frame'],'mock'),({'routes':[]},'mock')]
    with pytest.raises(DraftFailure) as caught:
        draft_outcome({'namespace':'test','outcome':OUTCOME,'brief':'Fictional'},lambda *_:outputs.pop(0))
    trace=caught.value.trace
    assert trace['failed_stage']=='routes' and trace['stage_count']==2
    assert trace['frame']==FIXTURE['frame'] and trace['routes']=={'routes':[]}
    assert 'input_value' not in str(caught.value)


def test_api_records_failed_staged_trace_separately_from_live_case(tmp_path,monkeypatch):
    from fastapi.testclient import TestClient
    from eightball.api import make_app
    from eightball.store import Store as LegacyStore
    from eightball.v2 import intelligence
    old=LegacyStore(str(tmp_path/'api.db'));store=Store(old.path);c=case();store.create(c,fixture=True)
    token='fictional-api-test-token-long-enough-123456789'
    grounded=deepcopy(FIXTURE['frame']);grounded['target_bindings']=[{'criterion_index':i,'target_quote':OUTCOME} for i in range(len(grounded['success_criteria']))]
    responses=[(grounded,'mock'),({'routes':[]},'mock')]
    monkeypatch.setattr(intelligence,'ollama_json',lambda *args,**kwargs:responses.pop(0))
    api=TestClient(make_app(old,token),headers={'Authorization':'Bearer '+token})
    result=api.post('/api/v2/cases/'+c.id+'/analyse',json={'expected_revision':0,'provider':'ollama_staged','purpose':'graph','source_ids':['source']})
    assert result.status_code==503 and store.get(c.id)==c
    saved=store.proposals(c.id)[0]
    assert saved['status']=='failed' and saved['raw_output']['failed_stage']=='routes'
    assert saved['raw_output']['frame']==grounded and saved['model']=='mock'
