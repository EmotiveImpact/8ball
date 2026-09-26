"""Structural inspection and human review are never factual/approval authority."""
import json
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from eightball.api import make_app
from eightball.store import Store as LegacyStore, Conflict
from eightball.v2.store import Store
from eightball.v2.playbooks import demo_case
from eightball.v2.commands import Command
from eightball.v2.plan_review import PlanReviews, Assess, Judgement, SaveReview, assessment, RUBRIC
from eightball.v2.planner import to_snapshot
from endstate.plan_review import inspect_plan, Inspection, Stress
from endstate.contracts import PlanningSnapshot

NOW = datetime(2026, 9, 24, 9, 0, tzinfo=timezone.utc)
TOKEN = 'plan-review-test-only-token-1234567890'


def snap():return to_snapshot(demo_case(NOW))
def inspect(s=None, scenarios=None):return inspect_plan(s or snap(), Inspection(as_of=NOW,scenarios=scenarios or []))


def test_inspection_preserves_snapshot_and_is_deterministic():
    s=snap();before=s.model_dump(mode='json')
    a=inspect(s);b=inspect(s)
    assert a==b and before==s.model_dump(mode='json')
    assert not a['semantics_verified'] and not a['execution_authorised']
    assert any(f['rule']=='unknown_wait' for f in a['flags'])
    assert a['baseline']['candidate_routes']>=3
    assert a['target_trace'][0]['conditions'][0]['confirmation']


def test_negative_goal_and_exact_expression_preserved():
    from endstate.contracts import atom
    s=snap();s.graph.objectives[0].success=atom('refused',False)
    r=inspect(s);assert r['target_trace'][0]['conditions'][0]['required_value'] is False
    assert r['target_trace'][0]['status']=='true'


def test_no_target_is_blocker_not_success():
    s=snap();s.graph.objectives=[];r=inspect(s)
    assert r['counts']['blocker']==1
    assert not r['baseline']['outcome_evidenced']


def test_effect_unproved_and_retracted_sources_not_promoted():
    s=snap();s.completed.append('investigate')
    r=inspect(s);assert any(f['rule']=='completion_unproved' for f in r['flags'])
    for e in s.evidence:e.status='retracted'
    assert not inspect(s)['baseline']['outcome_evidenced']


def test_unknown_producers_question_not_automatic_step():
    s=snap();s.graph.actions=[];s.constraints=[];r=inspect(s)
    assert any(f['rule']=='goal_without_producer' for f in r['flags'])
    assert all(not x['actions'] for x in r['baseline']['routes'])


@pytest.mark.parametrize('spec',[
    {'kind':'remove_action','action_id':'direct'}, {'kind':'budget','amount':0}, {'kind':'elapsed','minutes':1440}])
def test_explicit_scenarios_are_isolated(spec):
    s=snap();before=s.model_dump(mode='json');r=inspect(s,[Stress(**spec)])
    assert r['scenarios'][0]['hypothetical'] and before==s.model_dump(mode='json')
    if spec['kind']=='remove_action':assert all('direct' not in a['actions'] for a in r['scenarios'][0]['result']['routes'])
    if spec['kind']=='budget':assert r['scenarios'][0]['result']['constraint_compatible']==0
    if spec['kind']=='elapsed':assert r['scenarios'][0]['result']['constraint_compatible']==0


def test_scenarios_do_not_accumulate():
    r=inspect(scenarios=[Stress(kind='budget',amount=0),Stress(kind='budget',amount=7000)])
    assert r['scenarios'][0]['result']['constraint_compatible']==0
    assert r['scenarios'][1]['result']==r['baseline']


@pytest.mark.parametrize('data',[
    {'kind':'budget'}, {'kind':'budget','amount':0,'action_id':'direct'},
    {'kind':'elapsed','minutes':True}, {'kind':'elapsed','minutes':10081},
    {'kind':'remove_action','action_id':'../invalid'}, {'kind':'budget','amount':-1},
    {'kind':'remove_action','value':True}, {'kind':'anything'},
])
def test_invalid_stress_contracts_rejected(data):
    with pytest.raises(ValidationError):Stress(**data)


@pytest.mark.parametrize('change',['missing','completed','disabled'])
def test_unavailable_action_scenario_rejected(change):
    s=snap();aid='direct'
    if change=='missing':aid='missing'
    elif change=='completed':s.completed.append(aid)
    else:next(a for a in s.graph.actions if a.id==aid).enabled=False
    with pytest.raises(ValueError):inspect(s,[Stress(kind='remove_action',action_id=aid)])


def test_scenario_and_clock_bounds():
    with pytest.raises(ValidationError):Inspection(as_of='2026-01-01T10:00:00')
    with pytest.raises(ValidationError):Inspection(as_of=NOW,scenarios=[Stress(kind='budget',amount=0)]*4)


@pytest.fixture
def env(tmp_path):
    legacy=LegacyStore(str(tmp_path/'case.db'));store=Store(legacy.path)
    c=store.create(demo_case(),fixture=True);cl=TestClient(make_app(legacy,TOKEN),headers={'Authorization':'Bearer '+TOKEN})
    return store,c,PlanReviews(store),cl


def request_for(resp,verdict='uncertain',**kwargs):
    a=resp['assessment']
    return SaveReview(event_id='review1',expected_revision=a['case_revision'],expected_sequence=resp['sequence'],
                      as_of=a['inspection']['as_of'],assessment_sha256=a['assessment_sha256'],
                      scenarios=[Stress(**s['assumption']) for s in a['inspection']['scenarios']],
                      judgements=[Judgement(criterion=r['id'],verdict=verdict,rationale='Fixture reviewer records this judgement.',
                         references=['case:desired_outcome'] if verdict=='supported' else []) for r in RUBRIC],**kwargs)


def test_assess_read_only_and_record_not_live_mutation(env):
    store,c,svc,_=env;before=store.audit(c.id)
    result=svc.assess(c.id,Assess(expected_revision=0))
    assert store.audit(c.id)==before and result['persisted'] is False
    saved=svc.save(c.id,request_for(result))
    after=store.audit(c.id)
    assert after['case']==before['case'] and after['events']==before['events']
    assert after['valid'] and len(after['plan_reviews']['records'])==1
    assert saved['record']['disposition']=='uncertainty_recorded'
    assert not saved['live_case_changed'] and not saved['record']['execution_authorised']
    assert svc.view(c.id)['records'][0]['case_changed'] is False
    assert svc.view(c.id)['records'][0]['time_expired'] is False


def test_supported_review_cannot_clear_flags_or_approve(env):
    store,c,svc,_=env;r=svc.assess(c.id,Assess(expected_revision=0))
    out=svc.save(c.id,request_for(r,'supported'))
    assert out['record']['assessment']['inspection']['flags']==r['assessment']['inspection']['flags']
    assert not store.get(c.id).approvals and not out['record']['facts_attested']


def test_idempotency_after_case_change_and_second_review_history(env):
    store,c,svc,_=env;r=svc.assess(c.id,Assess(expected_revision=0));request=request_for(r)
    svc.save(c.id,request)
    store.change(c.id,Command(event_id='changed',expected_revision=0,kind='metadata',payload={'budget':6000}))
    assert svc.save(c.id,request)['duplicate']
    assert svc.view(c.id)['records'][0]['case_changed']
    next_r=svc.assess(c.id,Assess(expected_revision=1));next_req=request_for(next_r);next_req.event_id='review2'
    svc.save(c.id,next_req)
    assert len(svc.view(c.id)['records'])==2 and store.audit(c.id)['valid']


def test_stale_case_or_sequence_fails(env):
    store,c,svc,_=env;r=svc.assess(c.id,Assess(expected_revision=0))
    req=request_for(r);other=request_for(r);other.event_id='other'
    svc.save(c.id,req)
    with pytest.raises(Conflict):svc.save(c.id,other)
    store.change(c.id,Command(event_id='changed',expected_revision=0,kind='metadata',payload={'budget':5000}))
    with pytest.raises(Conflict):svc.assess(c.id,Assess(expected_revision=0))


@pytest.mark.parametrize('mutation',['digest','reference','scenario','clock_future','clock_expired','reused_id'])
def test_altered_or_expired_assessment_cannot_save(env,mutation):
    store,c,svc,_=env;r=svc.assess(c.id,Assess(expected_revision=0));req=request_for(r)
    if mutation=='digest':req.assessment_sha256='0'*64
    if mutation=='reference':req.judgements[0].references=['source:other_case']
    if mutation=='scenario':req.scenarios=[Stress(kind='budget',amount=0)]
    if mutation=='clock_future':req.as_of+=timedelta(hours=1)
    if mutation=='clock_expired':req.as_of-=timedelta(hours=1)
    if mutation=='reused_id':
        svc.save(c.id,req);req.judgements[0].rationale='A different review reuses this key.'
    with pytest.raises(ValueError):svc.save(c.id,req)


@pytest.mark.parametrize('mutation',['empty','duplicate','short_reason','unsupported','extra_authority'])
def test_required_rubric_and_nonempty_judgements(env,mutation):
    _,c,svc,_=env;d=request_for(svc.assess(c.id,Assess(expected_revision=0))).model_dump(mode='json')
    if mutation=='empty':d['judgements']=[]
    if mutation=='duplicate':d['judgements'][1]=d['judgements'][0]
    if mutation=='short_reason':d['judgements'][0]['rationale']='  '
    if mutation=='unsupported':d['judgements'][0]['verdict']='supported'
    if mutation=='extra_authority':d['observations']=[{'value':True}]
    with pytest.raises(ValidationError):SaveReview.model_validate(d)


def test_case_isolation_and_authentication(env):
    store,c,svc,cl=env
    other=store.create(demo_case(),fixture=True);r=svc.assess(c.id,Assess(expected_revision=0))
    with pytest.raises(Conflict):svc.save(other.id,request_for(r))
    assert not svc.view(other.id)['records']
    base=f'/api/v2/cases/{c.id}/plan-reviews'
    assert cl.get(base,headers={'Authorization':'Bearer wrong'}).status_code==401
    assert cl.post(base+'/assess',json={'expected_revision':0}).status_code==200
    assert cl.post(base+'/record',json=request_for(r).model_dump(mode='json')).status_code==200
    assert cl.get(base).json()['sequence']==1
    assert cl.get('/api/v2/cases/missing/plan-reviews').status_code==404


def test_concurrent_human_reviews_one_winner(env):
    _,c,svc,_=env;r=svc.assess(c.id,Assess(expected_revision=0))
    def work(n):
        req=request_for(r);req.event_id='concurrent'+str(n)
        try:svc.save(c.id,req);return True
        except Conflict:return False
    with ThreadPoolExecutor(max_workers=2) as pool:assert sorted(pool.map(work,[0,1]))==[False,True]


@pytest.mark.parametrize('tamper',['hash','sequence','event_id','record'])
def test_journal_tamper_detected_not_mislabelled_safe(env,tamper):
    store,c,svc,_=env;svc.save(c.id,request_for(svc.assess(c.id,Assess(expected_revision=0))))
    with store.connection() as db:
        if tamper=='hash':db.execute('UPDATE v2_plan_reviews SET hash=?',('tampered',))
        elif tamper=='sequence':db.execute('UPDATE v2_plan_reviews SET sequence=2')
        elif tamper=='event_id':db.execute('UPDATE v2_plan_reviews SET event_id=?',('forged',))
        else:db.execute('UPDATE v2_plan_reviews SET record=?',('{malformed',))
        db.commit()
    assert not store.audit(c.id)['valid']
    with pytest.raises(ValueError):svc.view(c.id)


def test_source_free_exports_keep_original_shape(env):
    store,c,svc,_=env
    assert 'plan_reviews' not in store.audit(c.id)
    svc.assess(c.id,Assess(expected_revision=0))
    assert 'plan_reviews' not in store.audit(c.id)


def test_clean_structure_does_not_certify_semantic_alignment():
    from evals.plan_review_bench import build_case
    r=inspect_plan(build_case('wrong-but-valid-outcome'),Inspection(as_of=NOW))
    assert not r['flags'] and not r['semantics_verified'] and not r['execution_authorised']


def test_offline_bench_leaves_human_labels_unfilled(tmp_path):
    from evals.plan_review_bench import run_bench
    r=run_bench(tmp_path)
    assert r['structural_checks_passed']==r['total']==8
    assert r['quality_gate']=='NOT_ASSESSED' and not r['actual_model_inference']
    sheet=json.loads((tmp_path/'human-review-sheet.json').read_text())
    assert sheet['status']=='UNREVIEWED'
    assert all(x['verdict'] is None and x['reviewer'] is None for row in sheet['reviews'] for x in row['rubric'])


def test_kernel_review_has_no_application_imports():
    import ast
    from pathlib import Path
    tree=ast.parse((Path(__file__).resolve().parents[1]/'endstate/plan_review.py').read_text())
    names=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module]
    assert not any(n.startswith(('eightball','sqlite','httpx','requests')) for n in names)


def test_distinct_dependency_paths_never_share_route_ids():
    from evals.plan_review_bench import build_case
    from endstate.planner import plan
    s=build_case('destructive-effect');s.budget=3000
    routes=plan(s,NOW)['routes']
    assert len({r['id'] for r in routes})==len(routes)
    # Identical action sets can legitimately have different producer orderings.
    pairs=[(a,b) for a in routes for b in routes if a['id']!=b['id'] and set(a['actions'])==set(b['actions']) and a['status']!=b['status']]
    assert pairs
    assert {r['id'] for r in plan(s,NOW,'lowest_cost')['routes']}=={r['id'] for r in routes}
    s.graph.actions.reverse()
    assert {r['id'] for r in plan(s,NOW)['routes']}=={r['id'] for r in routes}


def test_route_change_records_keep_colliding_paths_separate():
    from evals.plan_review_bench import build_case
    from endstate.planner import plan,explain_changes
    s=build_case('destructive-effect');s.budget=3000
    new=PlanningSnapshot.model_validate(s.model_dump(mode='python'));new.budget=900;new.revision=1
    before,after=plan(s,NOW),plan(new,NOW)
    delta=explain_changes(s,new,before,after)
    assert any(r['after_status']=='constraint_failure' and r['before_status']=='conditional' for r in delta['changed_routes'])
    assert len({r['id'] for r in delta['changed_routes']})==len(delta['changed_routes'])
