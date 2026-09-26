"""Fictional chosen-course tests: no network models or external actions."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json

import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient

from endstate.course import CourseAnchor, Watch, anchor_route, assess_course
from endstate.contracts import (PlanningSnapshot, Graph, Condition, Action, Effect,
                                Objective, Actor, Resource, Constraint, all_of, any_of, atom)
from endstate.primitives import Evidence, Observation
from endstate.planner import plan
from eightball.api import make_app
from eightball.models import uid
from eightball.store import Store as LegacyStore, Conflict, digest
from eightball.v2.contracts import Case
from eightball.v2.store import Store
from eightball.v2.commands import Command
from eightball.v2.planner import to_snapshot
from eightball.v2.courses import Courses, PreviewCourse, SelectCourse, CourseEvent, target_digest

NOW = datetime(2026, 9, 25, 12, tzinfo=timezone.utc)
TOKEN = 'fictional-course-test-token-1234567890'


def fixture_case():
    return Case(id='case', title='Fictional recovery', client='Synthetic fixture', summary='Two possible recovery actions.',
        desired_outcome='Recovery verified and accepted', deadline=NOW+timedelta(days=2), budget=10000,
        graph=Graph(conditions=[Condition(id=i,title=i,confirmation='Direct reviewed proof') for i in ['ready','accepted','refused','goal']],
            actions=[Action(id=i,title=i,owner='Case lead',purpose='Fictional work',requires=atom('ready'),
                            effects=[Effect(condition_id='accepted')],minutes=m,cost=c,
                            approval_required=True,contingent=True,wait_minutes=None) for i,m,c in [('first',30,100),('second',60,50)]]+
                    [Action(id='verify',title='Verify accepted result',owner='Reviewer',purpose='Verify actual result',
                            requires=atom('accepted'),effects=[Effect(condition_id='goal')],minutes=15,cost=0)],
            objectives=[Objective(id='outcome',title='Verified recovery',success=atom('goal'))]),
        evidence=[Evidence(id='source',title='Fictional log',source='Fixture only',text='Ready for the recovery attempt.',status='reviewed',added_at=NOW)],
        observations=[Observation(id='o1',condition_id='ready',evidence_id='source',value=True,rationale='Fixture attestation',added_at=NOW)])


def pick(c=None, **kwargs):
    c=c or fixture_case();s=to_snapshot(c)
    route=next(r for r in plan(s,NOW)['routes'] if 'first' in r['actions'])
    return anchor_route(s, route['id'], target_digest(c), NOW, **kwargs)


def update(c, **kwargs):
    d=c.model_dump(mode='python');d.update(kwargs);d['revision']+=1
    return Case.model_validate(d)


def observe(c,cid,value=True):
    obs=Observation(condition_id=cid,evidence_id='source',value=value,rationale='Fictional new observation',added_at=NOW)
    return update(c, observations=[*c.observations,obs])


def assessment(c,anchor=None,**kwargs):
    return assess_course(anchor or pick(),to_snapshot(c),kwargs.pop('target',target_digest(c)),kwargs.pop('as_of',NOW),**kwargs)


def test_anchor_and_reassessment_are_detached_read_only():
    c=fixture_case();before=c.model_dump(mode='json');a=pick(c);before_a=a.model_dump(mode='json')
    r=assessment(c,a)
    assert r.state=='no_trigger_detected' and r.compatible_remainders==1
    assert c.model_dump(mode='json')==before and a.model_dump(mode='json')==before_a
    assert not r.execution_authorised and not r.automatically_switched and r.monitoring=='on_request'
    assert all(set(x['actions'])<={'first','verify'} for x in r.remaining_plan['routes'])
    assert any('second' in x['actions'] for x in r.alternatives)


@pytest.mark.parametrize('change',['unknown-route','empty-route','hard-breach','naive-clock','bad-target','foreign-watch','past-review','duplicate-watch'])
def test_invalid_selection_rejected(change):
    c=fixture_case();s=to_snapshot(c);r=next(x for x in plan(s,NOW)['routes'] if 'first' in x['actions']);rid=r['id'];at=NOW;target=target_digest(c);kwargs={}
    if change=='unknown-route':rid='missing'
    if change=='empty-route':s=to_snapshot(observe(c,'goal'));rid=plan(s,NOW)['routes'][0]['id']
    if change=='hard-breach':s.budget=0;rid=plan(s,NOW)['routes'][0]['id']
    if change=='naive-clock':at=NOW.replace(tzinfo=None)
    if change=='bad-target':target='invalid'
    if change=='foreign-watch':kwargs['watches']=[Watch(condition_id='foreign',state='true')]
    if change=='past-review':kwargs['review_at']=NOW
    if change=='duplicate-watch':kwargs['watches']=[Watch(condition_id='ready',state='true')]*2
    with pytest.raises((ValueError,ValidationError)):anchor_route(s,rid,target,at,**kwargs)


@pytest.mark.parametrize('change',['other-case','earlier-revision','earlier-time','same-revision-change','forged-route'])
def test_assessment_refuses_wrong_context(change):
    c=fixture_case();a=pick(c);s=to_snapshot(c);at=NOW
    if change=='other-case':s.id='another'
    if change=='earlier-revision':c=update(c);a=pick(c);s=to_snapshot(fixture_case())
    if change=='earlier-time':at=NOW-timedelta(seconds=1)
    if change=='same-revision-change':s.budget=0
    if change=='forged-route':a.route['minutes']+=1
    with pytest.raises(ValueError):assess_course(a,s,target_digest(c),at)


@pytest.mark.parametrize('change,code',[
    ('target','target_changed'),('budget','budget_changed'),('deadline','deadline_changed'),
    ('action','actions_changed'),('condition','conditions_changed'),('restriction','restrictions_changed'),
    ('evidence','evidence_changed'),('source','source_context_changed'),('disable','chosen_action_unavailable')])
def test_relevant_changes_produce_reasons(change,code):
    c=fixture_case();a=pick(c);d=c.model_dump(mode='python');d['revision']=1
    if change=='target':d['desired_outcome']='A different target'
    if change=='budget':d['budget']=0
    if change=='deadline':d['deadline']=NOW+timedelta(minutes=1)
    if change=='action':d['graph']['actions'][0]['minutes']=99
    if change=='condition':d['graph']['conditions'][0]['confirmation']='A different confirmation'
    if change=='restriction':d['constraints']=[Constraint(id='restriction',title='Review before acting',confirmed=False).model_dump()]
    if change=='evidence':d['evidence'][0]['status']='retracted'
    if change=='source':d['evidence'].append(Evidence(title='New note',source='Fixture',text='New unreviewed context.').model_dump())
    if change=='disable':d['graph']['actions'][0]['enabled']=False
    r=assessment(Case.model_validate(d),a)
    assert r.state=='review_required' and code in {x.code for x in r.reasons}
    assert r.selected_route_id==a.route['id'] and not r.automatically_switched


def test_completed_work_is_not_repeated_or_assumed_success():
    c=update(fixture_case(),completed=['first']);r=assessment(c)
    assert r.completed_action_ids==['first'] and r.remaining_action_ids==['verify']
    assert r.state=='review_required' and 'verification_gaps' in {x.code for x in r.reasons}
    assert all('first' not in x['actions'] for x in r.remaining_plan['routes'])
    assert r.remaining_plan['states']['accepted']['status']=='unknown'


def test_completed_and_evidenced_progress_does_not_switch_course():
    c=observe(update(fixture_case(),completed=['first']),'accepted');a=pick();r=assessment(c,a)
    assert all(x['actions']==['verify'] for x in r.remaining_plan['routes'])
    assert r.selected_route_id==a.route['id']


def test_fixed_or_branch_cannot_take_a_new_shortcut():
    c=fixture_case();d=c.model_dump();d['graph']['actions'][0]['requires']=any_of('ready','refused').model_dump();c=Case.model_validate(d)
    a=pick(c);assert a.route['prerequisites']['first']==[{'condition_id':'ready','value':True}]
    d=c.model_dump();d['evidence'][0]['status']='retracted';d['revision']=1;c=Case.model_validate(d)
    c=observe(c,'refused')  # Retracted source deliberately cannot make it true.
    r=assessment(c,a)
    assert all('second' not in x['actions'] for x in r.remaining_plan['routes'])
    assert any(x['condition_id']=='ready' for route in r.remaining_plan['routes'] for x in route['evidence_gaps'])


@pytest.mark.parametrize('state',['true','false','unknown','disputed'])
def test_explicit_state_watches(state):
    c=fixture_case()
    if state=='true':c=observe(c,'refused',True)
    if state=='false':c=observe(c,'refused',False)
    if state=='disputed':c=observe(observe(c,'refused',True),'refused',False)
    a=pick(c,watches=[Watch(condition_id='refused',state=state)])
    r=assessment(c,a)
    assert 'watch_triggered' in {x.code for x in r.reasons} and r.state=='review_required'


def test_clock_alone_can_require_reconsideration():
    c=fixture_case();a=pick(c,review_at=NOW+timedelta(hours=1));r=assessment(c,a,as_of=NOW+timedelta(hours=1))
    assert 'review_time_reached' in {x.code for x in r.reasons} and c.revision==0


def test_missing_chosen_objects_are_not_reassuring():
    c=fixture_case();a=pick(c);d=c.model_dump();d['revision']=1;d['graph']['actions']=d['graph']['actions'][1:]
    r=assessment(Case.model_validate(d),a)
    assert r.state=='not_assessable' and r.remaining_plan is None


def test_linked_actor_change_does_not_infer_authority():
    c=fixture_case();c.actors.append(Actor(id='person',name='Fictional person'));c.graph.actions[0].actor_ids=['person'];a=pick(c)
    d=c.model_dump();d['actors'][0]['authority']='Reported new role';d['revision']=1
    r=assessment(Case.model_validate(d),a)
    assert 'actors_changed' in {x.code for x in r.reasons}
    assert not r.execution_authorised


@pytest.fixture
def env(tmp_path,monkeypatch):
    monkeypatch.setattr('eightball.v2.courses.utcnow',lambda:NOW)
    legacy=LegacyStore(str(tmp_path/'cases.db'));store=Store(legacy.path);c=store.create(fixture_case(),fixture=True)
    cl=TestClient(make_app(legacy,TOKEN),headers={'Authorization':'Bearer '+TOKEN})
    return store,c,Courses(store),cl


def select_request(svc,c,**kwargs):
    rid=next(r['id'] for r in plan(to_snapshot(c),NOW)['routes'] if 'first' in r['actions'])
    p=svc.preview(c.id,PreviewCourse(expected_revision=c.revision,route_id=rid))
    return SelectCourse(event_id=kwargs.pop('event_id','choose'),expected_revision=c.revision,expected_sequence=p['sequence'],
         route_id=rid,as_of=p['preview']['as_of'],preview_sha256=p['preview']['preview_sha256'],
         rationale='The operator chooses this fictional recovery route.',acknowledge_limits=True,
         replaces_course_id=p['current_id'],**kwargs)


def event_request(svc,c,operation,**kwargs):
    v=svc.view(c.id);chosen=next(x for x in v['courses'] if x['id']==v['current_id']);a=chosen['assessment']
    return CourseEvent(event_id=kwargs.pop('event_id',uid()),expected_revision=c.revision,expected_sequence=v['sequence'],
          course_id=chosen['id'],operation=operation,rationale='The operator records this explicit course judgement.',
          assessment_as_of=a['as_of'],assessment_sha256=a['assessment_sha256'],**kwargs)


def test_preview_and_reads_do_not_write_case_or_ledger(env):
    store,c,svc,_=env;before=store.audit(c.id)
    select_request(svc,c);assert not svc.view(c.id)['courses'];assert store.audit(c.id)==before


def test_select_record_preserves_original_and_all_authority(env):
    store,c,svc,_=env;before=store.audit(c.id);req=select_request(svc,c)
    reply=svc.select(c.id,req);after=store.audit(c.id)
    assert not reply['live_case_changed'] and not reply['execution_authorised']
    assert after['case']==before['case'] and after['events']==before['events']
    assert after['chosen_courses']['valid'] and after['valid']
    assert svc.view(c.id)['current_id']=='choose'
    assert after['chosen_courses']['records'][0]['selection']['anchor']['route']['id']==req.route_id
    assert Store(store.path).get(c.id)==c


def test_idempotency_and_event_id_collision(env):
    _,c,svc,_=env;req=select_request(svc,c);svc.select(c.id,req)
    assert svc.select(c.id,req)['duplicate']
    with pytest.raises(Conflict):svc.select(c.id,req.model_copy(update={'rationale':'Another meaningful explanation'}))


@pytest.mark.parametrize('tamper',['revision','sequence','digest','watch','past-clock','future-clock','replace'])
def test_stale_or_altered_preview_is_rejected_atomically(env,tamper):
    store,c,svc,_=env;req=select_request(svc,c)
    d=req.model_dump()
    if tamper=='revision':d['expected_revision']=99
    if tamper=='sequence':d['expected_sequence']=99
    if tamper=='digest':d['preview_sha256']='0'*64
    if tamper=='watch':d['watches']=[Watch(condition_id='refused',state='true')]
    if tamper=='past-clock':d['as_of']=NOW-timedelta(minutes=11)
    if tamper=='future-clock':d['as_of']=NOW+timedelta(seconds=1)
    if tamper=='replace':d['replaces_course_id']='missing'
    with pytest.raises(Conflict):svc.select(c.id,SelectCourse(**d))
    assert svc.view(c.id)['sequence']==0 and store.get(c.id)==c


def test_course_lifecycle_is_independent_and_retained(env):
    store,c,svc,_=env;svc.select(c.id,select_request(svc,c))
    for operation,expected in [('pause','paused'),('resume','active'),('review','active'),('retire','retired')]:
        svc.event(c.id,event_request(svc,c,operation))
        v=svc.view(c.id);assert v['courses'][0]['lifecycle']==expected
    assert v['current_id'] is None and len(v['records'])==5 and store.get(c.id)==c
    assert store.audit(c.id)['valid']


def test_replacement_is_explicit_and_old_course_is_preserved(env):
    _,c,svc,_=env;svc.select(c.id,select_request(svc,c))
    req=select_request(svc,c,event_id='replacement')
    with pytest.raises(Conflict):svc.select(c.id,req.model_copy(update={'replaces_course_id':None}))
    svc.select(c.id,req);v=svc.view(c.id)
    assert v['courses'][0]['lifecycle']=='superseded' and v['current_id']=='replacement'


def test_review_does_not_clear_reasons_or_reset_watch(env):
    _,c,svc,_=env
    req0=select_request(svc,c)
    p=svc.preview(c.id,PreviewCourse(expected_revision=0,route_id=req0.route_id,watches=[Watch(condition_id='ready',state='true')]))
    req=req0.model_copy(update={'watches':[Watch(condition_id='ready',state='true')],'preview_sha256':p['preview']['preview_sha256']})
    svc.select(c.id,req);v=svc.view(c.id);assert v['courses'][0]['assessment']['result']['state']=='review_required'
    svc.event(c.id,event_request(svc,c,'review'))
    assert svc.view(c.id)['courses'][0]['assessment']['result']['state']=='review_required'


def test_concurrent_selections_have_exactly_one_winner(env):
    _,c,svc,_=env;req=select_request(svc,c)
    def attempt(i):
        try:svc.select(c.id,req.model_copy(update={'event_id':str(i)}));return 'ok'
        except Conflict:return 'conflict'
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(attempt,[1,2]))==['conflict','ok']
    assert svc.view(c.id)['sequence']==1


def test_cross_case_anchor_cannot_be_applied(env):
    store,c,svc,_=env;d=c.model_dump();d['id']='other';other=store.create(Case.model_validate(d),fixture=True)
    with pytest.raises(Conflict):svc.select(other.id,select_request(svc,c))
    assert not svc.view(other.id)['courses']


def test_cannot_resume_active_or_rewrite_retired_choice(env):
    _,c,svc,_=env;svc.select(c.id,select_request(svc,c))
    with pytest.raises(ValueError):svc.event(c.id,event_request(svc,c,'resume'))
    retirement=event_request(svc,c,'retire');svc.event(c.id,retirement)
    with pytest.raises(Conflict):svc.event(c.id,retirement.model_copy(update={'event_id':'fresh','operation':'resume','expected_sequence':2}))


@pytest.mark.parametrize('tamper',['record','hash','case_binding'])
def test_tampered_ledger_fails_closed(env,tamper):
    store,c,svc,_=env;svc.select(c.id,select_request(svc,c))
    with store.connection() as db:
        row=db.execute('SELECT record FROM v2_course_events').fetchone();r=json.loads(row['record'])
        if tamper=='record':r['rationale']='Altered';db.execute('UPDATE v2_course_events SET record=?',(json.dumps(r),))
        elif tamper=='hash':db.execute("UPDATE v2_course_events SET hash='bad'")
        else:
            r['case_sha256']='0'*64;db.execute('UPDATE v2_course_events SET record=?,hash=?',(json.dumps(r),digest(r)))
        db.commit()
    assert not store.audit(c.id)['valid']
    with pytest.raises(ValueError):svc.view(c.id)


def test_http_preview_select_and_history(env):
    store,c,svc,cl=env;req=select_request(svc,c);base=f'/api/v2/cases/{c.id}/courses'
    assert cl.get(base).status_code==200
    assert cl.post(base+'/select',json=req.model_dump(mode='json')).status_code==200
    event=event_request(svc,c,'pause');assert cl.post(base+'/events',json=event.model_dump(mode='json')).status_code==200
    assert cl.get(base).json()['courses'][0]['lifecycle']=='paused'
    assert store.get(c.id)==c


def test_http_auth_and_extra_privileges_rejected(env):
    _,c,svc,cl=env;req=select_request(svc,c);base=f'/api/v2/cases/{c.id}/courses'
    assert cl.get(base,headers={'Authorization':'Bearer wrong'}).status_code==401
    payload=req.model_dump(mode='json');payload['approve_all']=True
    assert cl.post(base+'/select',json=payload).status_code==422


def test_no_course_export_remains_exactly_compatible(env):
    store,c,_,_=env
    assert 'chosen_courses' not in store.audit(c.id)


def test_new_fact_does_not_replace_selected_course(env):
    store,c,svc,_=env;svc.select(c.id,select_request(svc,c));original=svc.view(c.id)['current_id']
    changed,_=store.change(c.id,Command(event_id='source-add',expected_revision=0,kind='add_evidence',payload={'title':'Update','source':'Fixture','text':'New unreviewed text'}))
    v=svc.view(c.id);assert v['current_id']==original and v['case_revision']==1
    assert v['courses'][0]['assessment']['result']['state']=='review_required'
    assert not changed.observations==[]  # Preserved initial observation only.
    assert len(changed.observations)==1


def test_stale_review_token_cannot_acknowledge_new_case(env):
    store,c,svc,_=env;svc.select(c.id,select_request(svc,c));req=event_request(svc,c,'review')
    store.change(c.id,Command(event_id='budget',expected_revision=0,kind='metadata',payload={'budget':50}))
    with pytest.raises(Conflict):svc.event(c.id,req)
    assert svc.view(c.id)['sequence']==1


def test_review_payload_hash_and_case_context_are_bound(env):
    _,c,svc,_=env;svc.select(c.id,select_request(svc,c));req=event_request(svc,c,'review')
    with pytest.raises(Conflict):svc.event(c.id,req.model_copy(update={'assessment_sha256':'0'*64}))
    assert svc.view(c.id)['sequence']==1


def test_pause_duplicate_cannot_pause_again_or_add_history(env):
    _,c,svc,_=env;svc.select(c.id,select_request(svc,c));req=event_request(svc,c,'pause');svc.event(c.id,req)
    assert svc.event(c.id,req)['duplicate'] and svc.view(c.id)['sequence']==2


def test_corrupt_case_chain_cannot_receive_a_course_record(env):
    store,c,svc,_=env;req=select_request(svc,c)
    with store.connection() as db:
        db.execute("UPDATE v2_events SET hash='broken'");db.commit()
    with pytest.raises(ValueError):svc.select(c.id,req)
    with store.connection() as db:assert db.execute('SELECT COUNT(*) FROM v2_course_events').fetchone()[0]==0


def test_current_outcome_support_does_not_rewrite_original_target(env):
    store,c,svc,_=env;svc.select(c.id,select_request(svc,c))
    changed,_=store.change(c.id,Command(event_id='target',expected_revision=0,kind='metadata',payload={'desired_outcome':'A differently worded outcome'}))
    view=svc.view(c.id);chosen=view['courses'][0]
    assert chosen['requested_outcome']==c.desired_outcome
    assert changed.desired_outcome!=chosen['requested_outcome']
    assert 'target_changed' in {x['code'] for x in chosen['assessment']['result']['reasons']}


def test_neutral_kernel_ignores_model_providers_and_storage():
    from pathlib import Path
    import ast
    source=Path(__file__).resolve().parents[1]/'endstate/course.py'
    imports=[]
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node,ast.Import):imports.extend(n.name for n in node.names)
        if isinstance(node,ast.ImportFrom) and node.level==0:imports.append(node.module or '')
    assert not any(x.startswith(('eightball','httpx','fastapi','sqlite3','ollama')) for x in imports)


def test_replacement_does_not_reuse_previous_review_acknowledgement(env):
    _,c,svc,_=env;svc.select(c.id,select_request(svc,c));svc.event(c.id,event_request(svc,c,'review'))
    svc.select(c.id,select_request(svc,c,event_id='new-choice'));v=svc.view(c.id)
    assert v['courses'][0]['latest_review'] is not None
    assert v['courses'][1]['latest_review'] is None


def test_completing_every_chosen_action_without_evidence_is_not_success():
    c=update(fixture_case(),completed=['first','verify']);r=assessment(c)
    assert r.remaining_action_ids==[] and r.state!='outcome_evidenced'
    assert 'verification_gaps' in {x.code for x in r.reasons}
