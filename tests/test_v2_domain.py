from datetime import timedelta
import pytest
from pydantic import ValidationError
from eightball.models import Evidence,Observation,utcnow
from eightball.v2.contracts import *
from eightball.v2.playbooks import demo_case,get_playbook,list_playbooks
from eightball.v2.planner import plan,evaluate,question_priorities,changes
from eightball.v2.commands import Command,apply


def simple():
    return Case(title='Fixture',client='Fictional client',summary='Fictional incident',desired_outcome='Verified resolution',
                deadline=utcnow()+timedelta(days=2),budget=10000,
                graph=Graph(conditions=[Condition(id=i,title=i,confirmation='Direct evidence') for i in ['a','b','goal']],
                            actions=[Action(id='first',title='First path',owner='Lead',purpose='Establish goal',requires=atom('a'),effects=[Effect(condition_id='goal')],minutes=30,cost=100),
                                     Action(id='second',title='Second path',owner='Lead',purpose='Alternative',requires=atom('b'),effects=[Effect(condition_id='goal')],minutes=60,cost=200)],
                            objectives=[Objective(id='resolution',title='Resolution',success=atom('goal'))]))


def attest(case,cid,value=True,status='reviewed',supersedes=None):
    d=case.model_dump(mode='json');e=Evidence(title='Source',source='Fixture',text='Explicit fixture assertion.',status=status)
    d['evidence'].append(e.model_dump(mode='json'));d['observations'].append(Observation(condition_id=cid,evidence_id=e.id,value=value,rationale='Fictional reviewer',supersedes=supersedes or []).model_dump(mode='json'))
    return Case.model_validate(d)


def command(case,kind,payload):return apply(case,Command(event_id=uid(),expected_revision=case.revision,kind=kind,payload=payload))


@pytest.mark.parametrize('status,expected',[('unknown','unknown'),('true','false'),('false','true'),('disputed','disputed')])
def test_false_requires_explicit_evidence(status,expected):
    assert evaluate(atom('a',False),{'a':{'status':status}})==expected


@pytest.mark.parametrize('op,states,result',[('all',['true','true'],'true'),('all',['true','unknown'],'unknown'),('all',['false','unknown'],'false'),
    ('any',['true','disputed'],'true'),('any',['false','unknown'],'unknown'),('any',['false','false'],'false'),('all',['true','disputed'],'disputed')])
def test_boolean_expression_semantics(op,states,result):
    assert evaluate(Expr(op=op,args=[atom('a'),atom('b')]),{c:{'status':v} for c,v in zip(['a','b'],states)})==result


@pytest.mark.parametrize('bad',[{'op':'any','args':[]},{'op':'atom'},{'op':'all','condition_id':'a'},
    {'op':'atom','condition_id':'a','args':[{'op':'atom','condition_id':'b'}]},{'op':'atom','condition_id':'a','value':'false'}])
def test_bad_expressions_rejected(bad):
    with pytest.raises(ValidationError):Expr.model_validate(bad)


def test_nested_expression_bound():
    e=atom('a').model_dump()
    for _ in range(10):e={'op':'all','args':[e]}
    with pytest.raises(ValidationError):Expr.model_validate(e)


def test_or_routes_keep_selected_preconditions():
    c=simple();d=c.model_dump();d['graph']['actions']=d['graph']['actions'][:1]
    d['graph']['actions'][0]['requires']=any_of('a','b').model_dump();c=Case.model_validate(d)
    p=plan(c);assert len(p['routes'])==2
    assert {tuple(g['condition_id'] for g in r['evidence_gaps']) for r in p['routes']}=={('a',),('b',)}
    assert len({r['id'] for r in p['routes']})==2


def test_mandatory_goals_all_must_hold():
    c=attest(simple(),'goal');d=c.model_dump();d['graph']['objectives'].append(Objective(id='other',title='Other',success=atom('a')).model_dump())
    p=plan(Case.model_validate(d));assert not p['outcome_evidenced']
    assert any(g['condition_id']=='a' for r in p['routes'] for g in r['evidence_gaps'])


def test_optional_objective_not_silently_mandatory():
    c=attest(simple(),'goal');d=c.model_dump();d['graph']['objectives'].append(Objective(id='optional',title='Optional',success=atom('a'),mandatory=False).model_dump())
    p=plan(Case.model_validate(d));assert p['outcome_evidenced'];assert p['objective_states']['optional']=='unknown'


def test_no_objective_is_not_success():
    d=simple().model_dump();d['graph']['objectives']=[];p=plan(Case.model_validate(d))
    assert not p['outcome_evidenced'] and not p['routes']


def test_contradictions_block_both_sides():
    c=attest(attest(simple(),'a'),'a',False);p=plan(c)
    assert p['states']['a']['status']=='disputed'
    assert p['action_states']['first']['status']=='blocked'
    assert any(g['reason']=='disputed_evidence' for r in p['routes'] for g in r['evidence_gaps'])


def test_supersession_and_retraction():
    c=attest(attest(simple(),'a'),'a',False)
    c=attest(c,'a',True,supersedes=[o.id for o in c.observations])
    assert plan(c)['states']['a']['status']=='true'
    c=command(c,'review_evidence',{'evidence_id':c.evidence[-1].id,'status':'retracted'})
    assert plan(c)['states']['a']['status']=='unknown'


def test_cycles_bounded_but_valid_alternative_survives():
    c=attest(simple(),'b');d=c.model_dump()
    d['graph']['actions'].append(Action(id='cyclic',title='Cycle',owner='Lead',purpose='Test',requires=atom('goal'),effects=[Effect(condition_id='a')],minutes=5).model_dump())
    p=plan(Case.model_validate(d))
    assert any(not r['evidence_gaps'] and r['actions']==['second'] for r in p['routes'])
    assert p['expansions']<50


def test_signed_effects_cannot_destroy_mandatory_goal_unnoticed():
    c=attest(simple(),'a');d=c.model_dump();d['graph']['actions']=d['graph']['actions'][:1]
    d['graph']['actions'][0]['effects'].append({'condition_id':'a','value':False})
    d['graph']['objectives'][0]['success']=all_of('goal','a').model_dump()
    p=plan(Case.model_validate(d))
    assert all(r['hard_breaches'] for r in p['routes'])
    assert 'Final projected' in ' '.join(p['routes'][0]['hard_breaches'])


def test_negative_effect_can_be_a_legitimate_explicit_target():
    d=simple().model_dump();d['graph']['actions'][0]['effects']=[{'condition_id':'goal','value':False}]
    d['graph']['objectives'][0]['success']=atom('goal',False).model_dump();c=attest(Case.model_validate(d),'a')
    p=plan(c);assert len(p['routes'])==1 and not p['routes'][0]['hard_breaches']
    assert not p['outcome_evidenced']


def test_shared_resource_serialises_different_owners():
    d=simple().model_dump();d['resources']=[Resource(id='room',name='Room').model_dump()]
    d['graph']['conditions'].append(Condition(id='x',title='x',confirmation='Evidence').model_dump())
    d['graph']['objectives'][0]['success']=all_of('a','b').model_dump()
    d['graph']['actions']=[Action(id='one',title='One',owner='Alice',purpose='Test',effects=[Effect(condition_id='a')],minutes=20,resources=['room']).model_dump(),
                           Action(id='two',title='Two',owner='Ben',purpose='Test',effects=[Effect(condition_id='b')],minutes=30,resources=['room']).model_dump()]
    p=plan(Case.model_validate(d));s=p['routes'][0]['schedule']
    assert s[1]['start_minute']>=s[0]['active_end_minute'];assert p['routes'][0]['minutes']==50


def test_known_wait_is_counted_unknown_wait_is_visible():
    c=attest(simple(),'a');d=c.model_dump();d['graph']['actions'][0].update(wait_minutes=90,contingent=True)
    p=plan(Case.model_validate(d));route=next(r for r in p['routes'] if 'first' in r['actions'])
    assert route['minutes']==120 and route['provisional']
    d['graph']['actions'][0]['wait_minutes']=None
    route=next(r for r in plan(Case.model_validate(d))['routes'] if 'first' in r['actions'])
    assert route['minutes']==30 and route['unknown_waits']==['first']


def test_earliest_start_and_expiry_gate():
    now=utcnow();c=attest(simple(),'a');d=c.model_dump();d['graph']['actions'][0]['earliest_start']=now+timedelta(minutes=60)
    p=plan(Case.model_validate(d),now);r=next(r for r in p['routes'] if 'first' in r['actions'])
    assert r['minutes']==90;assert p['action_states']['first']['status']=='blocked'
    d['graph']['actions'][0].update(earliest_start=None,expires_at=now-timedelta(seconds=1))
    p=plan(Case.model_validate(d),now);assert p['action_states']['first']['status']=='blocked'


def test_guard_cannot_treat_unknown_as_false():
    c=attest(simple(),'a');d=c.model_dump();d['graph']['actions'][0]['guard']=atom('b',False).model_dump()
    p=plan(Case.model_validate(d));assert p['action_states']['first']['status']=='blocked'
    c=attest(Case.model_validate(d),'b',False);assert plan(c)['action_states']['first']['status']=='ready'


def test_condition_deadline_budget_and_resource_windows():
    now=utcnow();c=attest(simple(),'a');d=c.model_dump();d['graph']['conditions'][-1]['due_at']=now+timedelta(minutes=2);d['budget']=0
    p=plan(Case.model_validate(d),now)
    assert all(len(r['hard_breaches'])>=2 for r in p['routes'])


def test_policy_can_be_satisfied_earlier_in_the_projected_route():
    c=demo_case();p=plan(c)
    assert any(not r['hard_breaches'] for r in p['routes'])
    assert p['action_states']['direct']['status']=='blocked'


def test_decision_excludes_other_branch_and_is_recorded():
    c=demo_case();p=plan(c)
    assert any(r['decisions'] for r in p['routes'])
    c=command(c,'decide',{'decision_id':'escalation','option_id':'hold','rationale':'Continue direct engagement','evidence_ids':[]})
    assert all(any('Decision excludes' in x for x in r['hard_breaches']) for r in plan(c)['routes'] if 'mediated' in r['actions'])


def test_completion_does_not_prove_effect():
    c=command(attest(simple(),'a'),'complete',{'action_id':'first'})
    p=plan(c);assert p['states']['goal']['status']=='unknown' and not p['outcome_evidenced']
    assert p['action_states']['first']['status']=='completed'
    assert all(r['spent']==100 for r in p['routes'])


def test_approval_expiry_and_revisions():
    now=utcnow();c=attest(simple(),'a');d=c.model_dump();d['graph']['actions'][0]['approval_required']=True;c=Case.model_validate(d)
    c=command(c,'approve',{'action_id':'first'})
    assert plan(c)['action_states']['first']['status']=='ready'
    assert plan(c,now+timedelta(hours=1))['action_states']['first']['status']=='approval_required'
    c=command(c,'metadata',{'budget':9000});assert not c.approvals


def test_observed_condition_semantics_locked_but_deadline_editable():
    c=attest(simple(),'a');d=c.graph.model_dump();d['conditions'][0]['title']='Another fact'
    with pytest.raises(ValueError):command(c,'replace_graph',{'graph':d})
    d=c.graph.model_dump();d['conditions'][0]['due_at']=utcnow()+timedelta(hours=2)
    command(c,'replace_graph',{'graph':d})


def test_completed_action_immutable():
    c=command(attest(simple(),'a'),'complete',{'action_id':'first'});d=c.graph.model_dump();d['actions'][0]['cost']=0
    with pytest.raises(ValueError):command(c,'replace_graph',{'graph':d})


def test_closure_requires_evidence_and_retraction_reopens():
    with pytest.raises(ValueError):command(simple(),'metadata',{'status':'closed'})
    c=command(attest(simple(),'goal'),'metadata',{'status':'closed'});assert c.status=='closed'
    c=command(c,'review_evidence',{'evidence_id':c.evidence[0].id,'status':'retracted'});assert c.status=='active'


def test_question_priorities_are_graph_counts_not_probability():
    c=simple();p=plan(c);questions=question_priorities(c,p)
    assert questions[0]['condition_ids']==['goal']
    assert len(questions[0]['route_ids'])==2
    assert not any('probability' in k for q in questions for k in q)


def test_delta_reports_truth_and_route_changes():
    before=simple();after=attest(before,'a');delta=changes(before,after,plan(before),plan(after))
    assert 'first' in delta['newly_ready']
    assert delta['conditions'][0]['after']=='true'
    assert delta['new_routes'] or delta['changed_routes']


@pytest.mark.parametrize('id',list(CATALOGUE) if False else ['retention','recovery','supplier','communications','compromise','travel','dispute','reputation'])
def test_all_playbooks_validate_and_have_distinct_routes(id):
    c=Case(title='Fictional',client='Test',summary='Test',desired_outcome='Test',deadline=utcnow()+timedelta(days=2),**get_playbook(id))
    p=plan(c);assert len(p['routes'])>=2;assert not p['outcome_evidenced']


def test_search_limits_are_honest():
    d=simple().model_dump();d['graph']['conditions']=[Condition(id='c'+str(i),title='Condition '+str(i),confirmation='Evidence').model_dump() for i in range(8)]
    d['graph']['objectives']=[Objective(id='all',title='All',success=all_of(*['c'+str(i) for i in range(8)])).model_dump()]
    d['graph']['actions']=[Action(id=f'a{i}{j}',title='Option',owner='Lead',purpose='Test',effects=[Effect(condition_id=f'c{i}')],minutes=1).model_dump() for i in range(8) for j in range(2)]
    p=plan(Case.model_validate(d));assert p['search_truncated'];assert len(p['routes'])==64


def test_provenance_span_is_case_scoped():
    c=simple();d=c.model_dump();d['claims']=[Claim(statement='Invented',provenance=Provenance(references=[Span(evidence_id='othercase',start=0,end=8,quote='Invented')])).model_dump()]
    with pytest.raises(ValidationError):Case.model_validate(d)


def test_briefing_excludes_work_whose_effect_is_already_evidenced():
    from eightball.v2.planner import briefing
    c=demo_case();b=briefing(c,plan(c))
    assert 'preserve' not in {a['id'] for a in b['now']}
    assert not briefing(attest(simple(),'goal'),plan(attest(simple(),'goal')))['now']


def test_source_addition_and_target_edit_are_in_changes():
    c=simple();after=command(c,'add_evidence',{'title':'Source','source':'Test','text':'New assertion.'})
    delta=changes(c,after,plan(c),plan(after))
    assert any(o['collection']=='evidence' and o['change']=='added' for o in delta['objects'])
    changed=command(c,'metadata',{'desired_outcome':'Different desired state'})
    assert 'desired_outcome' in changes(c,changed,plan(c),plan(changed))['metadata_changed']


def test_success_and_failure_together_cannot_close_case():
    c=attest(attest(simple(),'goal'),'a');d=c.model_dump();d['graph']['objectives'][0]['failure']=atom('a').model_dump();c=Case.model_validate(d)
    assert not plan(c)['outcome_evidenced']
    with pytest.raises(ValueError):command(c,'metadata',{'status':'closed'})


def test_retracted_answer_is_reopened_in_question_priority():
    c=attest(simple(),'a');q=Question(id='q',question='Confirmed?',why='Need confirmation',condition_ids=['a'],status='answered',answer='Yes',evidence_ids=[c.evidence[0].id])
    c.questions.append(q);c=command(c,'review_evidence',{'evidence_id':c.evidence[0].id,'status':'retracted'})
    effective=next(x for x in question_priorities(c,plan(c)) if x['id']=='q')
    assert effective['status']=='open' and effective['evidence_review_required']
    assert c.questions[0].status=='answered'  # Historical answer is not erased.
