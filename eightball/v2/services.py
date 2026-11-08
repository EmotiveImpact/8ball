"""Application read models, isolated scenarios, source-preserving V1 import."""
from datetime import datetime
from .contracts import *
from .planner import plan, briefing, changes, literals, to_snapshot
from endstate.scenarios import Scenario, project as project_scenario
from ..models import Evidence,Observation,uid,utcnow
from ..store import Store as LegacyStore, Conflict
from .store import Store


def detail(case,sort_by='fewest_unknowns'):
    result=plan(case,sort_by=sort_by)
    return {'case':case.model_dump(mode='json'),'plan':result,'briefing':briefing(case,result)}


def scenario_case(case:Case,scenario:Scenario,as_of:datetime):
    if scenario.expected_revision!=case.revision:raise Conflict('Scenario is based on a stale case revision')
    projection=project_scenario(to_snapshot(case),scenario,as_of)
    return Case.model_validate({**case.model_dump(mode='python'),**projection.model_dump(mode='python')})


def simulate(case:Case,scenario:Scenario, *, as_of: datetime | None = None):
    now=as_of if as_of is not None else utcnow()
    clone=scenario_case(case,scenario,now);before=plan(case,now);after=plan(clone,now)
    return {'simulation':True,'persisted':False,'base_revision':case.revision,'assumptions':scenario.model_dump(mode='json'),
            'plan':after,'briefing':briefing(clone,after),'changes':changes(case,clone,before,after)}


def situation_map(case:Case,result:dict,view='outcome'):
    nodes=[];edges=[]
    if view=='people':
        nodes=[{'id':'actor:'+a.id,'object_id':a.id,'kind':'actor','label':a.name,'detail':a.role,'state':'reported'} for a in case.actors]
        edges=[{'from':'actor:'+r.from_actor,'to':'actor:'+r.to_actor,'label':r.kind} for r in case.relationships]
    elif view=='evidence':
        nodes=[{'id':'source:'+e.id,'object_id':e.id,'kind':'evidence','label':e.title,'state':e.status} for e in case.evidence]
        for c in case.graph.conditions:
            nodes.append({'id':'condition:'+c.id,'object_id':c.id,'kind':'condition','label':c.title,'state':result['states'][c.id]['status']})
        for o in case.observations:edges.append({'from':'source:'+o.evidence_id,'to':'condition:'+o.condition_id,'label':'supports' if o.value else 'contradicts'})
    else:
        nodes=[{'id':'condition:'+c.id,'object_id':c.id,'kind':'condition','label':c.title,'state':result['states'][c.id]['status']} for c in case.graph.conditions]
        for a in case.graph.actions:
            nodes.append({'id':'action:'+a.id,'object_id':a.id,'kind':'action','label':a.title,'state':result['action_states'][a.id]['status']})
            edges.extend({'from':'condition:'+cid,'to':'action:'+a.id,'label':'requires true' if v else 'requires false'} for cid,v in sorted(literals(a.requires)))
            edges.extend({'from':'action:'+a.id,'to':'condition:'+e.condition_id,'label':'intends true' if e.value else 'intends false'} for e in a.effects)
        # Edges show membership; expression labels retain AND/OR semantics in detail.
    return {'view':view,'nodes':nodes,'edges':edges,'note':'Edges are declared relationships and hypotheses, not causal proof.'}


def migrate_legacy(store:Store,legacy:LegacyStore,legacy_id):
    export=legacy.audit(legacy_id)
    if not export['valid']:raise ValueError('Legacy audit must verify before migration')
    # The imported state and retained lineage must describe one audited snapshot.
    from ..models import Situation
    old=Situation.model_validate(export['case'])
    prov=Provenance(origin='legacy',note='Imported from V0.1; original audit preserved in lineage.')
    graph=Graph(conditions=[Condition(**c.model_dump(),provenance=prov) for c in old.graph.conditions],
                actions=[Action(id=a.id,title=a.title,owner=a.owner,purpose=a.purpose,requires=all_of(*a.requires),
                                effects=[Effect(condition_id=i) for i in a.produces],minutes=a.minutes,cost=a.cost,risk=a.risk,
                                approval_required=a.approval_required,contingent=a.contingent,wait_minutes=None if a.contingent else 0,provenance=prov) for a in old.graph.actions],
                objectives=[Objective(id='legacy_outcome',title=old.desired_outcome,success=all_of(*old.graph.goals),provenance=prov)])
    case=Case(id=uid(),legacy_id=old.id,title=old.title,client=old.client,summary=old.summary,desired_outcome=old.desired_outcome,
              deadline=old.deadline,budget=old.budget,graph=graph,evidence=old.evidence,observations=old.observations,
              completed=old.completed,approvals=[],status='active',created_at=old.created_at)
    return store.create(case,lineage=export)


def client_brief(case:Case):
    p=plan(case)
    return {'title':case.title,'client':case.client,'desired_outcome':case.desired_outcome,
            'status':'Outcome evidenced; review residual risks' if p['outcome_evidenced'] else case.status,
            'target_deadline':case.deadline.isoformat(),'next_update':case.next_update.isoformat() if case.next_update else None,
            'actions_completed':len(case.completed),'conditions_evidenced':sum(s['status']=='true' for s in p['states'].values()),
            'notice':'Operator preview. Review before sharing. Not an authenticated client portal.'}


def action_brief(case:Case,action_id):
    a=next((a for a in case.graph.actions if a.id==action_id),None)
    if not a:raise KeyError(action_id)
    p=plan(case);state=p['action_states'][a.id];titles={c.id:c.title for c in case.graph.conditions}
    return {'action':a.model_dump(mode='json'),'state':state,
            'confirmation_checks':[{'condition_id':e.condition_id,'expected_value':e.value,'title':titles[e.condition_id],
                'confirmation':next(c.confirmation for c in case.graph.conditions if c.id==e.condition_id)} for e in a.effects],
            'call_brief':{'purpose':a.purpose,'owner':a.owner,'do_not_assume':'Requesting a response is not acceptance. Do not assert unverified claims.',
                          'questions':['What evidence would confirm the intended result?','Who has authority to agree?'],
                          'record_after':['What was said or done','Source and time','Evidence of any outcome, separately from completion']}}
