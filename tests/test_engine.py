from datetime import timedelta
import pytest
from pydantic import ValidationError
from eightball.models import Evidence, Observation, Graph, Situation, utcnow
from eightball.seed import create_case, recovery_graph
from eightball.engine import plan, condition_states, difference
from eightball.commands import Command, apply


def attest(case, cid, value=True, supersedes=None, status='reviewed'):
    data=case.model_dump(mode='json')
    e=Evidence(title='Test source', source='Fictional test', text='An explicitly reviewed test observation.', status=status)
    o=Observation(condition_id=cid,evidence_id=e.id,value=value,rationale='Test reviewer attestation',supersedes=supersedes or [])
    data['evidence'].append(e.model_dump(mode='json'));data['observations'].append(o.model_dump(mode='json'))
    return Situation.model_validate(data)


def cmd(case, kind, payload):
    return apply(case,Command(event_id='test',expected_revision=case.revision,kind=kind,payload=payload))


def test_three_nonidentical_routes():
    p=plan(create_case())
    assert len(p['routes'])==3
    assert len({r['id'] for r in p['routes']})==3
    assert p['search_truncated'] is False
    assert p['outcome_evidenced'] is False
    assert p['action_states']['preserve']['status']=='ready'
    assert p['action_states']['investigate']['status']=='blocked'


def test_false_is_not_unknown_and_unreviewed_is_not_true():
    c=attest(create_case(),'records',False)
    assert condition_states(c)['records']['status']=='false'
    assert condition_states(attest(create_case(),'records',True,status='unreviewed'))['records']['status']=='unknown'


def test_dispute_requires_explicit_supersession():
    c=attest(attest(create_case(),'records',True),'records',False)
    assert condition_states(c)['records']['status']=='disputed'
    assert all(r['blocked'] for r in plan(c)['routes'])
    c=attest(c,'records',True,supersedes=[o.id for o in c.observations])
    assert condition_states(c)['records']['status']=='true'


def test_reviewed_evidence_is_not_an_observation():
    c=create_case();c.evidence.append(Evidence(title='Reviewed',source='Test',text='Records preserved.',status='reviewed'))
    assert condition_states(c)['records']['status']=='unknown'


def test_retraction_removes_support():
    c=attest(create_case(),'records')
    c=cmd(c,'review_evidence',{'evidence_id':c.evidence[0].id,'status':'retracted'})
    assert condition_states(c)['records']['status']=='unknown'


def test_completion_does_not_verify_effect():
    c=cmd(create_case(),'complete',{'action_id':'preserve'})
    p=plan(c)
    assert p['states']['records']['status']=='unknown'
    assert p['action_states']['preserve']['status']=='completed'
    assert all('records' in r['unverified'] for r in p['routes'])
    assert not p['outcome_evidenced']


def test_blocked_completion_rejected():
    with pytest.raises(ValueError):cmd(create_case(),'complete',{'action_id':'direct'})


def test_completed_work_is_sunk_cost_not_double_counted():
    c=cmd(create_case(),'complete',{'action_id':'preserve'})
    c=attest(c,'records')
    for r in plan(c)['routes']:
        assert r['spent']==100
        assert r['total_cost']==r['remaining_cost']+100
        assert 'preserve' not in r['actions']


def test_approval_is_required_and_revision_scoped():
    c=attest(create_case(),'records')
    assert plan(c)['action_states']['listen']['status']=='approval_required'
    c=cmd(c,'approve',{'action_id':'listen'})
    assert plan(c)['action_states']['listen']['status']=='ready'
    c=cmd(c,'add_evidence',{'title':'Change','source':'Test','text':'New information'})
    assert not c.approvals
    assert plan(c)['action_states']['listen']['status']=='approval_required'


def test_approval_requires_compatible_route():
    c=attest(create_case(budget=1),'records')
    with pytest.raises(ValueError):cmd(c,'approve',{'action_id':'listen'})


def test_shared_dependencies_deduplicated_and_per_owner_serialised():
    c=create_case()
    for r in plan(c)['routes']:
        assert len(r['actions'])==len(set(r['actions']))
        owner_intervals={}
        for s in r['schedule']:
            owner=next(a.owner for a in c.graph.actions if a.id==s['action_id'])
            for start,end in owner_intervals.get(owner,[]):
                assert s['start_minute']>=end or s['end_minute']<=start
            owner_intervals.setdefault(owner,[]).append((s['start_minute'],s['end_minute']))


def test_deadline_budget_changes_and_difference():
    c=create_case();now=utcnow();before=plan(c,now)
    c.deadline=now+timedelta(minutes=5);c.budget=1
    after=plan(c,now);diff=difference(before,after)
    assert diff['constraint_failures_before']==0
    assert diff['constraint_failures_after']==3
    assert all(len(r['breaches'])>=2 for r in after['routes'])


def test_earlier_condition_deadline_checked():
    c=create_case();c.graph.conditions[1].due_at=utcnow()+timedelta(minutes=1)
    assert all(any('Root cause' in m for m in r['breaches']) for r in plan(c)['routes'])


def test_unknown_terminal_goal_is_not_invented():
    c=create_case();c.graph=Graph(conditions=[{'id':'goal','title':'Agreement','confirmation':'Signed agreement'}],actions=[],goals=['goal'])
    p=plan(c)
    assert p['routes'][0]['blocked']
    assert p['routes'][0]['unverified']==['goal']
    assert not p['outcome_evidenced']


def test_all_goals_require_observations():
    c=create_case();c=attest(c,'retained')
    p=plan(c)
    assert p['outcome_evidenced']
    assert p['routes'][0]['actions']==[]


def test_second_playbook_is_not_retention_script():
    c=create_case(template='recovery')
    assert c.graph.goals==['accepted']
    assert len(plan(c)['routes'])==2


def test_search_bound_is_visible():
    conditions=[dict(id=f'c{i}',title=f'Condition {i}',confirmation='Reviewed source') for i in range(8)]
    actions=[]
    for i in range(8):
        for j in range(2):
            actions.append(dict(id=f'a{i}_{j}',title='Option',owner=f'Owner {j}',requires=[],produces=[f'c{i}'],minutes=10,purpose='Test'))
    c=create_case();c.graph=Graph(conditions=conditions,actions=actions,goals=[f'c{i}' for i in range(8)])
    p=plan(c)
    assert p['search_truncated']
    assert len(p['routes'])==64


@pytest.mark.parametrize('mutation',[
    lambda g:g['conditions'].append(g['conditions'][0]),
    lambda g:g['actions'].append(g['actions'][0]),
    lambda g:g['goals'].append('missing'),
    lambda g:g['actions'][0]['requires'].append('missing'),
    lambda g:g['actions'][0]['requires'].append('records'),
    lambda g:g['actions'][0].update(minutes=-1),
    lambda g:g['actions'][0].update(minutes=True),
    lambda g:g['actions'][0].update(cost=-10),
    lambda g:g['actions'][0].update(unknown_field='no'),
    lambda g:g['actions'][1]['requires'].extend(['records']),
])
def test_invalid_graphs_rejected(mutation):
    g=create_case().graph.model_dump();mutation(g)
    with pytest.raises(ValidationError):Graph.model_validate(g)


@pytest.mark.parametrize('payload',[
    {'budget':-1}, {'budget':True}, {'deadline':'not-a-date'}, {'deadline':'2026-09-23T12:00:00'},
    {'title':''}, {'title':'x'*181}, {'id':'../other'}, {'revision':-1},
])
def test_invalid_case_fields_rejected(payload):
    d=create_case().model_dump(mode='json');d.update(payload)
    with pytest.raises(ValidationError):Situation.model_validate(d)


def test_observed_condition_cannot_be_redefined():
    c=attest(create_case(),'records');g=c.graph.model_dump();g['conditions'][0]['title']='Entirely different claim'
    with pytest.raises(ValueError):cmd(c,'replace_graph',{'graph':g})


def test_supersession_cannot_cross_conditions():
    c=attest(create_case(),'records')
    with pytest.raises(ValidationError):attest(c,'root',supersedes=[c.observations[0].id])
