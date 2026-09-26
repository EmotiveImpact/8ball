"""Read-only emergence detectors over an explicitly validated planning snapshot.

These are explainable structural findings, not a general causal inference model.
No model, network, storage, approvals or observation mutations are available here.
"""
from __future__ import annotations
from datetime import datetime
from hashlib import sha256
import json
from typing import Literal
from pydantic import AwareDatetime, Field
from .contracts import PlanningSnapshot, literals
from .primitives import Strict, Identifier, Title
from .planner import plan

RULE_VERSION = 'endstate.insights.v1'
RULES = [
    ('shared_condition', 'Shared unresolved prerequisite', 'An unmet signed prerequisite occurs in at least two constraint-compatible candidate routes.'),
    ('evidence_conflict', 'Conflicting active observations', 'Both true and false observations actively support the same condition. No free-text contradiction claim.'),
    ('unconfirmed_effect', 'Completed work without confirmed effect', 'Work is recorded complete, but at least one intended effect is not supported.'),
    ('actor_concentration', 'Concentrated actor links', 'An actor is linked to two or more actions across two or more candidate routes. Involvement is not authority.'),
    ('unknown_wait', 'Unbounded waiting period', 'A selected action has no specified waiting duration. Schedule arithmetic is a lower bound.'),
    ('single_source_cluster', 'Shared evidence dependency', 'One active source record is the only source for two or more relevant supported conditions. Not a claim of independent corroboration.'),
    ('freshness_review', 'Observation age requires review', 'All active supporting observations exceed an explicitly selected age. Recording time is not event time; truth is unchanged.'),
    ('decision_concentration', 'Shared decision gate', 'An unresolved decision appears across at least two candidate routes.'),
    ('side_effect_review', 'Declared possible consequence', 'A selected action declares possible side effects. These remain hypotheses, not observed consequences.'),
    ('objective_failure', 'Recorded failure condition', 'A configured objective failure expression is currently supported. The human must review the objective, not silently change it.'),
    ('deadline_pressure', 'Unresolved condition deadline', 'A relevant unresolved condition is due within the selected horizon or is overdue. The horizon is a declared policy.'),
    ('outcome_definition', 'Missing mandatory success criteria', 'No mandatory objective is defined. A desired-outcome sentence is not executable acceptance criteria.'),
]
RULE_IDS = {r[0] for r in RULES}


def stable_hash(value) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


class InsightPolicy(Strict):
    freshness_hours: int | None = Field(default=None, strict=True, ge=1, le=8760)
    deadline_horizon_hours: int = Field(default=24, strict=True, ge=1, le=720)
    max_findings: int = Field(default=256, strict=True, ge=1, le=1000)


class Reference(Strict):
    kind: Literal['condition','action','actor','evidence','observation','objective','decision','question','resource','constraint']
    id: Identifier
    label: str = Field(min_length=1, max_length=2000)
    record_hash: str = Field(pattern=r'^[a-f0-9]{64}$')


class Insight(Strict):
    id: Identifier
    rule: str
    rule_version: str = RULE_VERSION
    kind: Literal['derived','inferred','hypothesis']
    priority: Literal['review','important','urgent'] = 'review'
    title: str = Field(min_length=1, max_length=500)
    meaning: str = Field(min_length=1, max_length=4000)
    why: list[str] = Field(min_length=1, max_length=32)
    verify: str = Field(min_length=1, max_length=2000)
    caveat: str = Field(min_length=1, max_length=2000)
    references: list[Reference] = Field(default_factory=list, max_length=1400)
    route_ids: list[Identifier] = Field(default_factory=list, max_length=64)
    condition_ids: list[Identifier] = Field(default_factory=list, max_length=64)
    question: str = Field(min_length=1, max_length=180)
    fingerprint: str = ''


def reference_index(snapshot: PlanningSnapshot) -> dict:
    result = {}
    groups = [('condition',snapshot.graph.conditions),('action',snapshot.graph.actions),('objective',snapshot.graph.objectives)]
    groups += [(name, getattr(snapshot, plural)) for name,plural in [('actor','actors'),('evidence','evidence'),
               ('observation','observations'),('decision','decisions'),('question','questions'),('resource','resources'),('constraint','constraints')]]
    for kind, objects in groups:
        for obj in objects:
            data = obj.model_dump(mode='json')
            label = data.get('title') or data.get('name') or data.get('question') or data.get('rationale') or obj.id
            result[(kind,obj.id)] = Reference(kind=kind,id=obj.id,label=label,record_hash=stable_hash(data))
    return result


def make_insight(rule, key, *, refs, **kwargs) -> Insight:
    """Stable identity, versioned content. A title is never used as an object ID."""
    item=Insight(id='ins_'+stable_hash([rule,key])[:28],rule=rule,references=refs,**kwargs)
    payload=item.model_dump(mode='json',exclude={'fingerprint'})
    item.fingerprint=stable_hash(payload)
    return item


def detect(snapshot: PlanningSnapshot, as_of: datetime, policy: InsightPolicy | None = None) -> dict:
    # Revalidate mutable caller collections; reject naive clocks and malformed references.
    class Input(Strict):
        snapshot: PlanningSnapshot
        as_of: AwareDatetime
        policy: InsightPolicy
    request=Input.model_validate({'snapshot':snapshot.model_dump(mode='python'), 'as_of':as_of,
                                 'policy':(policy or InsightPolicy()).model_dump()})
    s=request.snapshot; as_of=request.as_of; policy=request.policy
    p=plan(s,as_of); states=p['states']; refs=reference_index(s)
    cs={c.id:c for c in s.graph.conditions}; actions={a.id:a for a in s.graph.actions}
    observations={o.id:o for o in s.observations}
    # Once mandatory outcomes are evidenced, spare OR alternatives are not blockers.
    candidates=[] if p['outcome_evidenced'] else [r for r in p['routes'] if not r['hard_breaches']]
    selected={aid for r in candidates for aid in r['actions']}
    findings=[]
    def R(*keys):
        return [refs[key] for key in sorted(set(keys)) if key in refs]
    def support(cid):
        state=states[cid]
        return [('condition',cid)]+[('evidence',e) for e in state['evidence']]+[('observation',o) for o in state['observations']]
    def add(rule,key,**kw):
        findings.append(make_insight(rule,key,**kw))
    def question(prefix,label):
        return prefix + label[:max(1,178-len(prefix))] + '?'
    # Selected prerequisites only. OR alternatives do not all become required.
    obligations={}
    for r in candidates:
        signed={(x['condition_id'],x['value']) for v in r['prerequisites'].values() for x in v}
        signed|={(x['condition_id'],x['value']) for x in r['evidence_gaps']}
        for cid,value in signed:
            obligations.setdefault((cid,value),set()).add(r['id'])
    relevant={cid for cid,_ in obligations}|{cid for o in s.graph.objectives for cid,_ in literals(o.success)}
    for (cid,value),routes in sorted(obligations.items()):
        expected='true' if value else 'false'
        if len(routes)<2 or states[cid]['status']==expected:continue
        add('shared_condition',[cid,value],refs=R(*support(cid)),kind='derived',priority='important',
            title='Several routes share an unresolved prerequisite',
            meaning=f'{cs[cid].title} must be supported as {expected} in {len(routes)} calculated candidate routes.',
            why=[f'Selected route prerequisites explicitly require {expected}.',f'Current evidence state: {states[cid]["status"]}.'],
            verify=cs[cid].confirmation,caveat='These are bounded, constraint-compatible candidates, not every possible real-world route. This does not prove a single point of failure.',
            route_ids=sorted(routes),condition_ids=[cid],question=question('What establishes ',cs[cid].title))
    for cid,state in states.items():
        if state['status']=='disputed':
            add('evidence_conflict',cid,refs=R(*support(cid)),kind='derived',priority='urgent',title='The active record supports opposing assertions',
                meaning=cs[cid].title,why=['Active, reviewed-source observations include both true and false.'],
                verify='Review the full sources and reconcile explicitly. Do not average or silently discard one side.',
                caveat='This detects conflicting recorded observations, not whether a witness is truthful.',
                route_ids=sorted({rid for (x,_),rr in obligations.items() if x==cid for rid in rr}),condition_ids=[cid],
                question=question('How do we reconcile ',cs[cid].title))
        if policy.freshness_hours and state['status'] in ('true','false') and cid in relevant:
            active=[observations[i] for i in state['observations']]
            if active and all((as_of-o.added_at).total_seconds()>policy.freshness_hours*3600 for o in active):
                newest=max(o.added_at for o in active)
                add('freshness_review',cid,refs=R(*support(cid)),kind='derived',priority='review',
                    title='Supporting observations are older than the selected review threshold',meaning=cs[cid].title,
                    why=[f'Explicit threshold: {policy.freshness_hours} hours.',f'Newest active observation recorded at {newest.isoformat()}.'],
                    verify='Ask whether the assertion still holds. Record fresh evidence separately when warranted.',
                    caveat='This measures observation recording time, not when an event occurred. Age is not falsity; the condition remains unchanged.',
                    condition_ids=[cid],question=question('Is this still supported: ',cs[cid].title))
        if cs[cid].due_at and cid in relevant:
            unmet=any(x==cid and state['status']!=('true' if v else 'false') for x,v in obligations)
            unmet=unmet or any(evaluate_goal_atom[0]==cid and state['status']!=('true' if evaluate_goal_atom[1] else 'false') for o in s.graph.objectives if o.mandatory and p['objective_states'][o.id]!='true' for evaluate_goal_atom in literals(o.success))
            hours=(cs[cid].due_at-as_of).total_seconds()/3600
            if unmet and hours<=policy.deadline_horizon_hours:
                add('deadline_pressure',cid,refs=R(*support(cid)),kind='derived',priority='urgent',title='An unresolved condition is at its review deadline',
                    meaning=cs[cid].title,why=[f'Declared due time: {cs[cid].due_at.isoformat()}.',f'Review horizon: {policy.deadline_horizon_hours} hours; {"overdue" if hours<0 else "within horizon"}.'],
                    verify='Confirm the deadline and the evidence needed; inspect alternative routes before acting.',
                    caveat='A deadline entered in the graph is not proof of a legal obligation. No deadline or action is changed.',
                    condition_ids=[cid],question=question('Who can verify the deadline for ',cs[cid].title))
    for aid in sorted(s.completed):
        action=actions[aid]
        missing=[e.condition_id for e in action.effects if states[e.condition_id]['status']!=('true' if e.value else 'false')]
        if not missing:continue
        add('unconfirmed_effect',aid,refs=R(('action',aid),*[k for cid in missing for k in support(cid)]),kind='derived',priority='important',
            title='Completed work still needs evidence of its result',meaning=action.title,
            why=[f'The completion record exists, but {len(missing)} intended effect(s) are not supported.'],
            verify='Review the outcome with the responsible person. Add a separate evidence-backed observation, not another completion click.',
            caveat='Missing confirmation does not mean the work failed. Neither success nor failure is inferred.',
            condition_ids=sorted(missing),question=question('What confirms the result of ',action.title))
    for actor in s.actors:
        linked={aid for aid in selected if actor.id in actions[aid].actor_ids}
        routes=[r['id'] for r in candidates if linked&set(r['actions'])]
        if len(linked)<2 or len(routes)<2:continue
        add('actor_concentration',actor.id,refs=R(('actor',actor.id),*[('action',a) for a in linked]),kind='inferred',priority='review',
            title='Several routes converge on the same recorded actor',meaning=actor.name,
            why=[f'{len(linked)} candidate actions explicitly link this actor across {len(routes)} candidate routes.'],
            verify='Confirm the actual decision authority and availability. Involvement alone does not establish control.',
            caveat='A structural lead, not a fact about influence, motives or authority. The actor links are operator/model-reviewed records.',
            route_ids=sorted(routes),question=question('What authority and availability does this actor have: ',actor.name))
    for aid in sorted(selected):
        action=actions[aid];routes=sorted(r['id'] for r in candidates if aid in r['actions'])
        if action.wait_minutes is None:
            add('unknown_wait',aid,refs=R(('action',aid)),kind='derived',priority='important',title='An unspecified wait limits the time estimate',
                meaning=action.title,why=['The action has wait_minutes=null.',f'Included in {len(routes)} candidate route(s).'],
                verify='Obtain a response window or agree a review time. Do not substitute an invented duration.',
                caveat='The active-work estimate is not an end-to-end completion forecast.',route_ids=routes,
                question=question('What waiting or response window applies to ',action.title))
        if action.side_effects:
            add('side_effect_review',aid,refs=R(('action',aid)),kind='hypothesis',priority='review',title='A proposed action has declared possible consequences',
                meaning=action.title,why=list(action.side_effects),verify='Challenge the stated consequence and check affected objectives with the relevant specialist.',
                caveat='These are authored hypotheses. Their presence does not mean the consequence occurred or has a measured likelihood.',route_ids=routes,
                question=question('What else could follow from ',action.title))
    for evidence in s.evidence:
        dependent=sorted(cid for cid in relevant if states[cid]['status'] in ('true','false') and states[cid]['evidence']==[evidence.id])
        if len(dependent)<2:continue
        add('single_source_cluster',evidence.id,refs=R(('evidence',evidence.id),*[('condition',i) for i in dependent]),kind='derived',priority='review',
            title='Several supported conditions rely on one source record',meaning=evidence.title,
            why=[f'This is the only active evidence record for {len(dependent)} relevant conditions.'],
            verify='Inspect the full source and whether independent confirmation is needed. Separate excerpts may share an original.',
            caveat='Record count is not independent corroboration, reliability or a finding that the source is wrong.',
            condition_ids=dependent,question=question('Do we need independent confirmation beyond ',evidence.title))
    for decision in s.decisions:
        routes=[r['id'] for r in candidates if any(d['id']==decision.id for d in r['decisions'])]
        if len(routes)<2:continue
        add('decision_concentration',decision.id,refs=R(('decision',decision.id)),kind='derived',priority='important',title='One decision affects multiple candidate routes',
            meaning=decision.question,why=[f'{len(routes)} candidates carry this unresolved or review-required decision gate.'],
            verify='Ask the named decision owner to review the options and evidence. Do not choose a direction automatically.',
            caveat='Counted alternatives may overlap. This is not a score of decision value or an instruction to pressure the owner.',route_ids=sorted(routes),
            question=question('What evidence is needed to decide ',decision.question))
    for oid in p['objective_failures']:
        obj=next(o for o in s.graph.objectives if o.id==oid)
        cids=sorted({c for c,_ in literals(obj.failure)})
        add('objective_failure',oid,refs=R(('objective',oid),*[k for cid in cids for k in support(cid)]),kind='derived',priority='urgent',
            title='A configured failure condition is supported',meaning=obj.title,why=['The recorded failure expression evaluates true in the current evidence state.'],
            verify='Review the objective, constraints and any acceptable fallback with the client. Preserve the original target and record a deliberate decision.',
            caveat='This concerns the authored failure criteria, not a claim that no real-world solution exists. No objective is amended.',
            condition_ids=cids,question=question('Does this outcome need explicit reconsideration: ',obj.title))
    if not any(o.mandatory for o in s.graph.objectives):
        add('outcome_definition','mandatory',refs=[],kind='derived',priority='important',title='The requested outcome needs explicit success criteria',
            meaning='The graph has no mandatory objective.',why=['A written aspiration does not establish a verifiable outcome contract.'],
            verify='Define what would prove success in Plan Studio, then review candidate actions.',caveat='No objective or action is invented by this detector.',
            question='What evidence would prove the desired outcome has actually been achieved?')
    rank={'urgent':0,'important':1,'review':2}
    findings.sort(key=lambda i:(rank[i.priority],-len(i.route_ids),i.rule,i.id))
    return {'contract_version':RULE_VERSION,'snapshot_id':s.id,'revision':s.revision,'as_of':as_of.isoformat(),
            'policy':policy.model_dump(mode='json'),'findings':[i.model_dump(mode='json') for i in findings[:policy.max_findings]],
            'total_detected':len(findings),'findings_truncated':len(findings)>policy.max_findings,
            'candidate_route_count':len(candidates),'search_truncated':p['search_truncated'],
            'routes':[{'id':r['id'],'title':r['title'],'status':r['status']} for r in p['routes']],
            'rules_evaluated':sorted(RULE_IDS-({'freshness_review'} if policy.freshness_hours is None else set())),
            'rules_disabled':['freshness_review'] if policy.freshness_hours is None else [],
            'limits':['Read-only structural findings, not independent factual verification.',
                      'Counts refer to bounded, constraint-compatible candidates while mandatory outcomes remain unevidenced; routes can overlap.',
                      'No interpretation of unstructured contradictions, motives or causal effects.',
                      'No model calls, autonomous actions or background monitoring.']}
