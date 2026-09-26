"""Bounded signed backward planning, forward validation, honest lower-bound schedules.

A plan is a conditional proof over a reviewed catalogue, not a prediction. OR
branches retain their chosen prerequisites. Only live evidence unlocks actions.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from hashlib import sha256
import json
from .contracts import PlanningSnapshot, Expr, Action, literals
from .state import condition_states
from .primitives import utcnow

MAX_ROUTES = 64
MAX_EXPANSIONS = 4096
RISK = {'low':0, 'medium':1, 'high':2}
Lit = tuple[str,bool]


def evaluate(expr: Expr, states: dict) -> str:
    if expr.op=='atom':
        value=states.get(expr.condition_id,{}).get('status','unknown')
        if value in ('unknown','disputed'):return value
        return 'true' if (value=='true')==expr.value else 'false'
    vals=[evaluate(a,states) for a in expr.args]
    if expr.op=='all':
        if 'false' in vals:return 'false'
        if 'disputed' in vals:return 'disputed'
        if 'unknown' in vals:return 'unknown'
        return 'true'
    if 'true' in vals:return 'true'
    if 'disputed' in vals:return 'disputed'
    if 'unknown' in vals:return 'unknown'
    return 'false'


def expression_text(expr: Expr, titles: dict[str,str]) -> str:
    if expr.op=='atom':return ('' if expr.value else 'NOT ') + titles.get(expr.condition_id,expr.condition_id)
    if not expr.args:return 'No prerequisites'
    return '(' + (' AND ' if expr.op=='all' else ' OR ').join(expression_text(e,titles) for e in expr.args) + ')'


def unsatisfied(expr: Expr, states: dict) -> list[dict]:
    if evaluate(expr,states)=='true':return []
    if expr.op=='atom':
        return [{'condition_id':expr.condition_id,'value':expr.value,'status':states[expr.condition_id]['status']}]
    return [g for e in expr.args for g in unsatisfied(e,states)]


def applicable_constraints(case: PlanningSnapshot, action: Action, states: dict):
    hard,soft=[],[]
    for c in case.constraints:
        if c.action_ids and action.id not in c.action_ids:continue
        if not c.confirmed or (c.predicate is not None and evaluate(c.predicate,states)!='true'):
            (hard if c.hard else soft).append(c.title)
    return hard,soft


def readiness(case: PlanningSnapshot, action: Action, states: dict, now: datetime) -> dict:
    missing=unsatisfied(action.requires,states)
    guard=unsatisfied(action.guard,states)
    hard,_=applicable_constraints(case,action,states)
    reasons=[]
    if not action.enabled:reasons.append('Action disabled by the operator')
    if missing:reasons.append('Prerequisites are not evidenced')
    if guard:reasons.append('Restriction or guard is not evidenced')
    reasons.extend(hard)
    if action.earliest_start and action.earliest_start>now:reasons.append('Earliest start has not arrived')
    if action.expires_at and action.expires_at<=now:reasons.append('Action has expired')
    resources={r.id:r for r in case.resources}
    for rid in action.resources:
        r=resources[rid]
        if r.available_from and r.available_from>now:reasons.append('Resource not yet available: '+r.name)
        if r.available_until and now+timedelta(minutes=action.minutes)>r.available_until:
            reasons.append('Resource window insufficient: '+r.name)
    selected_decision=None
    if action.decision_id:
        d=next(d for d in case.decisions if d.id==action.decision_id)
        selected_decision=d.selected
        if any(eid not in {e.id for e in case.evidence if e.status=='reviewed'} for eid in d.evidence_ids):
            reasons.append('Decision evidence was retracted; reconsider the decision')
        if d.selected!=action.decision_option:reasons.append('Decision must select the required option')
    spent=sum(a.cost for a in case.graph.actions if a.id in case.completed)
    if spent+action.cost>case.budget:reasons.append('Action would exceed the remaining budget')
    approval=next((a for a in case.approvals if a.action_id==action.id and a.revision==case.revision and a.expires_at>now),None)
    status=('completed' if action.id in case.completed else 'blocked' if reasons else
            'approval_required' if action.approval_required and not approval else 'ready')
    return {'id':action.id,'status':status,'missing':missing,'guards':guard,'reasons':reasons,
            'effects_evidenced':all(states[e.condition_id]['status']==('true' if e.value else 'false') for e in action.effects),
            'approval_expires_at':approval.expires_at.isoformat() if approval else None,
            'selected_decision':selected_decision}


@dataclass
class Bundle:
    needs: dict[str,frozenset[Lit]] = field(default_factory=dict)
    edges: frozenset[tuple[str,str]] = frozenset()
    gaps: frozenset[tuple[str,bool,str]] = frozenset()
    roots: frozenset[str] = frozenset()
    asks: frozenset[Lit] = frozenset()
    used: frozenset[Lit] = frozenset()

    def key(self):
        return (tuple(sorted((a,tuple(sorted(v))) for a,v in self.needs.items())),
                tuple(sorted(self.edges)),tuple(sorted(self.gaps)),tuple(sorted(self.asks)))


def merge(a:Bundle,b:Bundle) -> Bundle:
    needs={**a.needs}
    for key,values in b.needs.items():needs[key]=needs.get(key,frozenset())|values
    return Bundle(needs,a.edges|b.edges,a.gaps|b.gaps,a.roots|b.roots,a.asks|b.asks,a.used|b.used)


def plan(case: PlanningSnapshot, now: datetime | None = None, sort_by: str = 'fewest_unknowns') -> dict:
    now=now or utcnow()
    states=condition_states(case)
    actions={a.id:a for a in case.graph.actions};conditions={c.id:c for c in case.graph.conditions}
    titles={c.id:c.title for c in case.graph.conditions}
    action_states={a.id:readiness(case,a,states,now) for a in actions.values()}
    mandatory=[o for o in case.graph.objectives if o.mandatory]
    objective_states={o.id:evaluate(o.success,states) for o in case.graph.objectives}
    objective_failures=[o.id for o in case.graph.objectives if o.failure and evaluate(o.failure,states)=='true']
    truncated=False;expansions=0
    def trim(items):
        nonlocal truncated
        out=[];seen=set()
        for item in items:
            key=item.key()
            if key in seen:continue
            seen.add(key)
            if len(out)>=MAX_ROUTES:
                truncated=True;break
            out.append(item)
        return out
    def combine(groups):
        result=[Bundle()]
        for group in groups:
            result=trim(merge(a,b) for a in result for b in group)
        return result
    def expr_routes(expr,stack):
        if expr.op=='atom':return resolve((expr.condition_id,expr.value),stack)
        groups=[expr_routes(e,stack) for e in expr.args]
        return combine(groups) if expr.op=='all' else trim(b for g in groups for b in g)
    def resolve(lit,stack):
        nonlocal truncated,expansions
        cid,value=lit;expansions+=1
        if states[cid]['status']==('true' if value else 'false'):
            return [Bundle(asks=frozenset([lit]),used=frozenset([lit]))]
        def gap(reason):return [Bundle(gaps=frozenset([(cid,value,reason)]),asks=frozenset([lit]),used=frozenset([lit]))]
        if expansions>MAX_EXPANSIONS:
            truncated=True;return gap('search_limit')
        if lit in stack:return gap('cyclic_dependency')
        if states[cid]['status']=='disputed':return gap('disputed_evidence')
        producers=[a for a in actions.values() if a.enabled and a.id not in case.completed
                   and any(e.condition_id==cid and e.value==value for e in a.effects)]
        if not producers:return gap('needs_observation')
        options=[]
        for action in producers:
            for deps in expr_routes(action.requires,stack|{lit}):
                if action.id in deps.needs:continue
                chosen={**deps.needs,action.id:deps.asks}
                edges=deps.edges|{(r,action.id) for r in deps.roots}
                options.append(Bundle(chosen,edges,deps.gaps,frozenset([action.id]),frozenset([lit]),deps.used|{lit}))
        return trim(options) or gap('cyclic_dependency')

    candidates=combine([expr_routes(o.success,set()) for o in mandatory]) if mandatory else []
    results=[];identity_paths={};spent=sum(actions[a].cost for a in case.completed)
    resources={r.id:r for r in case.resources}
    for b in candidates:
        selected=set(b.needs);todo=set(selected);ends={};active_ends={};schedule=[];availability={}
        failures=[];warnings=[];decisions=[];external=[];unknown_wait=[];guards=[]
        for aid in sorted(selected):
            a=actions[aid]
            if a.contingent:external.append(aid)
            if a.wait_minutes is None:unknown_wait.append(aid)
            # Guards and policy predicates use current evidence, not planned positive effects.
            for g in unsatisfied(a.guard,states):guards.append({**g,'action_id':aid,'reason':'guard_needs_observation'})
            for constraint in case.constraints:
                if constraint.action_ids and aid not in constraint.action_ids:continue
                if not constraint.confirmed:
                    (failures if constraint.hard else warnings).append('Constraint requires human review: '+constraint.title)
            if a.decision_id:
                d=next(d for d in case.decisions if d.id==a.decision_id)
                if d.selected and d.selected!=a.decision_option:failures.append('Decision excludes: '+a.title)
                elif d.selected is None:decisions.append({'id':d.id,'required_option':a.decision_option,'action_id':aid})
                elif any(eid not in {e.id for e in case.evidence if e.status=='reviewed'} for eid in d.evidence_ids):
                    decisions.append({'id':d.id,'required_option':a.decision_option,'action_id':aid,'reason':'decision_evidence_retracted'})
        required_options={}
        for aid in sorted(selected):
            action=actions[aid]
            if action.decision_id:
                required_options.setdefault(action.decision_id,set()).add(action.decision_option)
        for decision_id,options in required_options.items():
            if len(options)>1:
                failures.append('Mutually exclusive decision options required: '+decision_id)
        while todo:
            eligible=[actions[i] for i in todo if all(before in ends for before,after in b.edges if after==i)]
            if not eligible:
                failures.append('Selected action dependencies contain a cycle');break
            def start_for(a):
                pre=max([ends[p] for p,n in b.edges if n==a.id] or [0])
                earliest=max(0,(a.earliest_start-now).total_seconds()/60) if a.earliest_start else 0
                resource_starts=[max(0,(resources[r].available_from-now).total_seconds()/60)
                                 for r in a.resources if resources[r].available_from]
                return max([pre,earliest,availability.get('owner:'+a.owner,0)]+resource_starts+
                           [availability.get('resource:'+r,0) for r in a.resources])
            def priority(a):
                due=min([conditions[e.condition_id].due_at for e in a.effects if conditions[e.condition_id].due_at] or [case.deadline])
                return (start_for(a),due,a.id)
            a=min(eligible,key=priority);start=start_for(a);active_end=start+a.minutes;end=active_end+(a.wait_minutes or 0)
            availability['owner:'+a.owner]=active_end
            for rid in a.resources:
                availability['resource:'+rid]=active_end
                latest=resources[rid].available_until
                if latest and now+timedelta(minutes=active_end)>latest:failures.append('Resource window exceeded: '+resources[rid].name)
            if a.expires_at and now+timedelta(minutes=active_end)>a.expires_at:failures.append('Action expiry exceeded: '+a.title)
            for effect in a.effects:
                due=conditions[effect.condition_id].due_at
                if due and now+timedelta(minutes=end)>due:failures.append('Condition deadline exceeded: '+conditions[effect.condition_id].title)
            schedule.append({'action_id':a.id,'start_minute':round(start,2),'active_end_minute':round(active_end,2),
                             'end_minute':round(end,2),'wait_known':a.wait_minutes is not None})
            ends[a.id]=end;active_ends[a.id]=active_end;todo.remove(a.id)
        # Recheck chosen prerequisites and signed effects in chronological order.
        # This detects delete effects that would destroy an earlier goal or dependency.
        projected={cid:dict(s) for cid,s in states.items()}
        for cid,value,_ in b.gaps:projected[cid]={'status':'true' if value else 'false'}
        clock=[]
        for s in schedule:
            clock.append((s['start_minute'],1,s['action_id'],'start'))
            clock.append((s['end_minute'],0,s['action_id'],'end'))
        for _,_,aid,phase in sorted(clock):
            a=actions[aid]
            if phase=='start':
                if evaluate(a.guard,projected)!='true':
                    failures.append('Projected guard unmet at action start: '+a.title)
                for constraint in case.constraints:
                    if constraint.action_ids and aid not in constraint.action_ids:continue
                    if constraint.predicate is not None and evaluate(constraint.predicate,projected)!='true':
                        (failures if constraint.hard else warnings).append('Constraint unmet at action start: '+constraint.title)
                for cid,value in b.needs[aid]:
                    if projected[cid]['status']!=('true' if value else 'false'):
                        failures.append('Projected prerequisite conflict: '+conditions[cid].title)
            else:
                for effect in a.effects:projected[effect.condition_id]={'status':'true' if effect.value else 'false'}
        if any(evaluate(o.success,projected)!='true' for o in mandatory):
            failures.append('Final projected state does not satisfy every mandatory objective')
        for objective in case.graph.objectives:
            if objective.failure is not None and evaluate(objective.failure,projected)=='true':
                failures.append('Projected objective failure: '+objective.title)
        minutes=max(ends.values(),default=0);remaining_cost=sum(actions[i].cost for i in selected)
        finish=now+timedelta(minutes=minutes)
        evidenced=bool(mandatory) and not objective_failures and all(objective_states[o.id]=='true' for o in mandatory)
        if not evidenced and finish>case.deadline:failures.append('Outcome deadline exceeded')
        if spent+remaining_cost>case.budget:failures.append('Total estimated cost exceeds case budget')
        if objective_failures:failures.append('A recorded objective failure condition is currently supported')
        gap_items=[{'condition_id':cid,'value':v,'reason':r,'status':states[cid]['status']} for cid,v,r in sorted(b.gaps)]
        gap_items.extend(guards)
        required_gap_values={}
        for gap in gap_items:
            required_gap_values.setdefault(gap['condition_id'],set()).add(gap['value'])
        for cid,values in required_gap_values.items():
            if len(values)>1:
                failures.append('Conflicting evidence assumptions: '+conditions[cid].title)
        risk=max([RISK[actions[i].risk] for i in selected] or [0])
        irreversible=[i for i in sorted(selected) if actions[i].reversibility=='irreversible']
        contingency_items=[{'action_id':i,**c.model_dump(mode='json'),'trigger_state':evaluate(c.when,states)}
                           for i in sorted(selected) for c in actions[i].contingencies]
        goal_roots=[actions[i].title for i in sorted(b.roots)]
        identity=json.dumps({'actions':sorted(selected),'needs':{k:sorted(v) for k,v in sorted(b.needs.items())},
                             'gaps':[(g['condition_id'],g['value']) for g in gap_items]},sort_keys=True)
        route_id=sha256(identity.encode()).hexdigest()[:14]
        result={'id':route_id,'title':' / '.join(goal_roots) or ('Verify outstanding conditions' if gap_items else 'Outcome evidenced'),
                'actions':[s['action_id'] for s in schedule],'schedule':schedule,
                'prerequisites':{a:[{'condition_id':c,'value':v} for c,v in sorted(ls)] for a,ls in b.needs.items()},
                'dependencies':[list(e) for e in sorted(b.edges)],'evidence_gaps':gap_items,
                'used_conditions':sorted({c for c,_ in b.used}),
                'hard_breaches':sorted(set(failures)),'soft_warnings':sorted(set(warnings)),
                'decisions':decisions,'external_dependencies':external,'unknown_waits':unknown_wait,
                'irreversible_actions':irreversible,'contingencies':contingency_items,
                'minutes':round(minutes,2),'remaining_cost':remaining_cost,'spent':spent,'total_cost':spent+remaining_cost,
                'slack_minutes':round((case.deadline-finish).total_seconds()/60,1),
                'risk':risk,'provisional':bool(gap_items or unknown_wait or external or decisions),
                'evidence_coverage':{'supported':sum(states[c]['status']==('true' if value else 'false') for c,value in b.used),'required':len(b.used)},
                'objectives':{o.id:evaluate(o.success,projected) for o in case.graph.objectives},
                'status':'constraint_failure' if failures else 'needs_evidence' if gap_items else 'needs_decision' if decisions else 'conditional',
                'ready':[i for i in selected if action_states[i]['status']=='ready'],
                'approvals':[i for i in selected if action_states[i]['status']=='approval_required']}
        result['fingerprint']=sha256(json.dumps({k:v for k,v in result.items() if k not in ('slack_minutes','ready','approvals')},sort_keys=True).encode()).hexdigest()
        results.append(result)
        identity_paths.setdefault(route_id, []).append((result, {'edges': sorted(b.edges), 'roots': sorted(b.roots), 'asks': sorted(b.asks), 'gaps': sorted(b.gaps)}))
    # Legacy identity omitted producer ordering. The same action set can form
    # distinct dependency paths with different constraint results. Preserve all
    # existing non-colliding IDs, but give colliding paths stable distinct IDs.
    # This fixes comparison/delta dictionaries silently replacing one route.
    for legacy_id, alternatives in identity_paths.items():
        if len(alternatives) < 2:
            continue
        for route, path in alternatives:
            suffix = sha256(json.dumps(path, sort_keys=True).encode()).hexdigest()[:16]
            route['id'] = legacy_id + '_' + suffix
            route['fingerprint'] = sha256(json.dumps({k:v for k,v in route.items()
                if k not in ('fingerprint','slack_minutes','ready','approvals')},sort_keys=True).encode()).hexdigest()
    orders={
        'fewest_unknowns':lambda r:(len(r['evidence_gaps']),len(r['unknown_waits']),r['minutes'],r['id']),
        'fastest':lambda r:(r['minutes'],r['total_cost'],r['id']),
        'lowest_cost':lambda r:(r['total_cost'],r['minutes'],r['id']),
        'fewest_external':lambda r:(len(r['external_dependencies']),len(r['evidence_gaps']),r['id']),
        'least_irreversible':lambda r:(len(r['irreversible_actions']),r['risk'],r['id']),
        'operator_risk':lambda r:(r['risk'],r['minutes'],r['id']),
    }
    if sort_by not in orders:raise ValueError('Unknown route ordering')
    results.sort(key=lambda r:(bool(r['hard_breaches']),*orders[sort_by](r)))
    return {'revision':case.revision,'computed_at':now.isoformat(),'states':states,'action_states':action_states,
            'objective_states':objective_states,'objective_failures':objective_failures,'routes':results,
            'outcome_evidenced':bool(mandatory) and not objective_failures and all(objective_states[o.id]=='true' for o in mandatory),
            'search_truncated':truncated,'expansions':expansions,'sort_by':sort_by,
            'limits':'64 candidate routes; 4,096 recursive expansions. Greedy capacity-one scheduling, not global optimisation. Unknown waits are lower bounds. External outcomes require evidence.'}


def question_priorities(case:PlanningSnapshot, result:dict) -> list[dict]:
    states=result['states'];questions=[]
    for c in case.graph.conditions:
        if states[c.id]['status'] in ('true','false'):continue
        routes=[r['id'] for r in result['routes'] if c.id in r['used_conditions'] or any(g['condition_id']==c.id for g in r['evidence_gaps'])]
        blocked=[a.id for a in case.graph.actions if any(cid==c.id for cid,_ in literals(a.requires)|literals(a.guard)) and result['action_states'][a.id]['status']=='blocked']
        goals=[o.id for o in case.graph.objectives if any(cid==c.id for cid,_ in literals(o.success))]
        if not (routes or blocked or goals):continue
        questions.append({'id':'auto_'+c.id,'question':('Reconcile conflicting evidence: ' if states[c.id]['status']=='disputed' else 'What evidence establishes: ')+c.title+'?',
            'why':c.confirmation,'owner':case.owner,'condition_ids':[c.id],'route_ids':routes,'blocked_action_ids':blocked,
            'objective_ids':goals,'due_at':c.due_at.isoformat() if c.due_at else None,'status':'open','generated':True})
    reviewed_sources={e.id for e in case.evidence if e.status=='reviewed'}
    for q in case.questions:
        unsupported=q.status=='answered' and not set(q.evidence_ids)<=reviewed_sources
        routes=[r['id'] for r in result['routes'] if set(q.condition_ids)&set(r['used_conditions'])]
        blocked=[a.id for a in case.graph.actions if set(q.condition_ids)&{cid for cid,_ in literals(a.requires)} and result['action_states'][a.id]['status']=='blocked']
        questions.append({'id':q.id,'question':q.question,'why':q.why,'owner':q.owner,'condition_ids':q.condition_ids,
                          'route_ids':routes,'blocked_action_ids':blocked,'objective_ids':[],
                          'due_at':q.needed_by.isoformat() if q.needed_by else None,'status':'open' if unsupported else q.status,'recorded_status':q.status,'answer':q.answer,'evidence_review_required':unsupported,'generated':False})
    questions.sort(key=lambda q:(q['status']!='open',-(len(q['route_ids'])),-len(q['blocked_action_ids']),q['due_at'] or '9999',q['id']))
    return questions


def explain_changes(before:PlanningSnapshot,after:PlanningSnapshot,bp:dict,ap:dict) -> dict:
    bstates=bp['states'];astates=ap['states']
    conditions=[{'id':cid,'title':next(c.title for c in after.graph.conditions if c.id==cid),
                 'before':bstates.get(cid,{}).get('status','absent'),'after':a['status'],
                 'source_ids':a['evidence']}
                for cid,a in astates.items() if bstates.get(cid)!=a]
    br={r['id']:r for r in bp['routes']};ar={r['id']:r for r in ap['routes']}
    changed=[{'id':i,'title':ar[i]['title'],'before_status':br[i]['status'],'after_status':ar[i]['status'],
              'new_breaches':sorted(set(ar[i]['hard_breaches'])-set(br[i]['hard_breaches']))}
             for i in ar.keys()&br.keys() if ar[i]['fingerprint']!=br[i]['fingerprint']]
    was={i for i,a in bp['action_states'].items() if a['status']=='ready'}
    ready={i for i,a in ap['action_states'].items() if a['status']=='ready'}
    objects=[]
    for name in ('evidence','actors','relationships','events','claims','constraints','resources','decisions','questions'):
        old={o.id:o.model_dump(mode='json') for o in getattr(before,name)}
        new={o.id:o.model_dump(mode='json') for o in getattr(after,name)}
        for id,value in new.items():
            if old.get(id)!=value:objects.append({'collection':name,'id':id,'change':'added' if id not in old else 'updated'})
    for name in ('conditions','actions','objectives'):
        old={o.id:o.model_dump(mode='json') for o in getattr(before.graph,name)}
        new={o.id:o.model_dump(mode='json') for o in getattr(after.graph,name)}
        for id in sorted(old.keys()|new.keys()):
            if old.get(id)!=new.get(id):objects.append({'collection':name,'id':id,'change':'added' if id not in old else 'removed' if id not in new else 'updated'})
    metadata=['owner'] if before.owner!=after.owner else []
    return {'metadata_changed':metadata,'objects':objects,'approvals_invalidated':len(before.approvals) if before.approvals and not after.approvals else 0,'from_revision':before.revision,'to_revision':after.revision,'conditions':conditions,
            'newly_ready':sorted(ready-was),'no_longer_ready':sorted(was-ready),
            'new_routes':[{'id':i,'title':ar[i]['title']} for i in sorted(ar.keys()-br.keys())],
            'removed_routes':[{'id':i,'title':br[i]['title']} for i in sorted(br.keys()-ar.keys())],
            'changed_routes':changed,'deadline_changed':before.deadline!=after.deadline,'budget_changed':before.budget!=after.budget,
            'questions_before':[q['id'] for q in question_priorities(before,bp) if q['status']=='open'][:5],
            'questions_after':[q['id'] for q in question_priorities(after,ap) if q['status']=='open'][:5]}


def briefing(case:PlanningSnapshot,result:dict) -> dict:
    questions=question_priorities(case,result)
    titles={a.id:a.title for a in case.graph.actions}
    relevant={i for route in result['routes'] for i in route['actions']}
    now=[{'id':i,'title':titles[i],'status':a['status']} for i,a in result['action_states'].items() if i in relevant and a['status'] in ('ready','approval_required')]
    decisions=[d.model_dump(mode='json') for d in case.decisions if d.selected is None]
    watch=[{'condition_id':c.id,'title':c.title,'deadline':c.due_at.isoformat(),'status':result['states'][c.id]['status']}
           for c in case.graph.conditions if c.due_at and result['states'][c.id]['status']!='true']
    return {'now':now,'next':[{'id':i,'title':titles[i],'blockers':a['reasons']} for i,a in result['action_states'].items() if i in relevant and a['status']=='blocked'],
            'decisions':decisions,'questions':questions,'watch':watch,'routes':result['routes'],
            'summary':f"{len(result['routes'])} conditional routes. {len(now)} action(s) ready or awaiting approval. {sum(q['status']=='open' for q in questions)} open questions.",
            'notices':['No guaranteed outcome. Estimates are operator inputs.',result['limits']]+['Manual restriction, not machine-verifiable: '+c.title for c in case.constraints if c.predicate is None]}
