"""All live state changes cross a validated, human-initiated command boundary."""
from datetime import timedelta
from pydantic import Field, AwareDatetime
from .contracts import *
from .planner import plan, readiness, evaluate
from ..engine import condition_states
from ..models import Evidence, Observation, utcnow


class Command(Strict):
    event_id: Identifier
    expected_revision: int = Field(strict=True, ge=0)
    kind: Literal['add_evidence','review_evidence','observe','metadata','upsert_object','replace_graph',
                  'approve','complete','decide','answer','apply_proposal']
    payload: dict


class EvidenceInput(Strict):
    title: Title
    source: Title
    text: Text


class EvidenceReview(Strict):
    evidence_id: Identifier
    status: Literal['reviewed','retracted']


class ObservationInput(Strict):
    condition_id: Identifier
    evidence_id: Identifier
    value: bool = Field(strict=True)
    rationale: Title
    supersedes: list[Identifier] = Field(default_factory=list, max_length=1000)


class Metadata(Strict):
    title: Title | None = None
    summary: Text | None = None
    desired_outcome: Title | None = None
    owner: Title | None = None
    deadline: AwareDatetime | None = None
    budget: Count | None = None
    status: Literal['intake','active','stabilising','monitoring','closed'] | None = None
    priority: Literal['ordinary','time_sensitive','critical'] | None = None
    next_update: AwareDatetime | None = None


class ObjectInput(Strict):
    kind: Literal['actor','relationship','event','claim','condition','action','objective','constraint','resource','question','decision']
    object: dict


class GraphInput(Strict):
    graph: Graph


class ActionInput(Strict):
    action_id: Identifier


class DecisionInput(Strict):
    decision_id: Identifier
    option_id: Identifier
    rationale: Text
    evidence_ids: list[Identifier] = Field(default_factory=list, max_length=20)


class AnswerInput(Strict):
    question_id: Identifier
    answer: Text
    evidence_ids: list[Identifier] = Field(min_length=1, max_length=12)


PAYLOADS={'add_evidence':EvidenceInput,'review_evidence':EvidenceReview,'observe':ObservationInput,
          'metadata':Metadata,'upsert_object':ObjectInput,'replace_graph':GraphInput,'approve':ActionInput,
          'complete':ActionInput,'decide':DecisionInput,'answer':AnswerInput}


def merge_object(data,kind,value,*,allow_replace=True):
    parsed=OBJECT_TYPES[kind].model_validate(value)
    collection=(data['graph'][{'condition':'conditions','action':'actions','objective':'objectives'}[kind]]
                if kind in ('condition','action','objective') else data[COLLECTIONS[kind]])
    existing=next((i for i,o in enumerate(collection) if o['id']==parsed.id),None)
    if existing is not None and not allow_replace:raise ValueError('Proposal would overwrite an existing object ID; edit it or regenerate')
    value=parsed.model_dump(mode='json')
    if existing is None:collection.append(value)
    else:collection[existing]=value


def preserve_meaning(before:Case,after:Case):
    original={c.id:c for c in before.graph.conditions};updated={c.id:c for c in after.graph.conditions}
    for o in before.observations:
        if o.condition_id not in updated:
            raise ValueError('An observed condition cannot be removed')
        a,b=original[o.condition_id],updated[o.condition_id]
        if (a.title,a.confirmation,a.kind)!=(b.title,b.confirmation,b.kind):
            raise ValueError('Do not redefine an observed condition; create a new condition ID')
    new_actions={a.id:a for a in after.graph.actions};old_actions={a.id:a for a in before.graph.actions}
    if any(new_actions.get(i)!=old_actions[i] for i in before.completed):
        raise ValueError('Completed actions are immutable historical records')
    # Decisions may be superseded through decide, not by editing away their history.
    return after


def apply(case:Case,cmd:Command,actor='local-operator',now=None) -> Case:
    if cmd.kind=='apply_proposal':raise ValueError('Proposals must be reviewed through the proposal service')
    now=now or utcnow()
    p=PAYLOADS[cmd.kind].model_validate(cmd.payload)
    data=case.model_dump(mode='json');data['approvals']=[]
    revision=case.revision+1
    if cmd.kind=='add_evidence':
        data['evidence'].append(Evidence(**p.model_dump()).model_dump(mode='json'))
    elif cmd.kind=='review_evidence':
        e=next((e for e in data['evidence'] if e['id']==p.evidence_id),None)
        if not e:raise ValueError('Source is not in this case')
        if e['status']=='retracted' and p.status!='retracted':raise ValueError('Retracted sources require a new source, not reinstatement')
        e['status']=p.status
    elif cmd.kind=='observe':
        e=next((e for e in case.evidence if e.id==p.evidence_id and e.status=='reviewed'),None)
        if not e:raise ValueError('Review the source before attesting a condition')
        data['observations'].append(Observation(**p.model_dump()).model_dump(mode='json'))
    elif cmd.kind=='metadata':
        update=p.model_dump(mode='json',exclude_none=True)
        if update.get('status')=='closed' and not plan(case,now)['outcome_evidenced']:
            raise ValueError('Closure requires evidence for all mandatory objectives; revise the objectives explicitly first')
        data.update(update)
    elif cmd.kind=='upsert_object':
        obj=OBJECT_TYPES[p.kind].model_validate(p.object)
        # Cannot forge approval/decision/question attestations via generic editing.
        if p.kind=='decision' and any(getattr(obj,k) is not None for k in ('selected','decided_at','decided_revision')):
            raise ValueError('Record a decision using the decision command')
        if p.kind=='decision' and any(d.id==obj.id and d.selected for d in case.decisions):
            raise ValueError('A recorded decision cannot be erased by editing its object')
        if p.kind=='question' and (obj.status!='open' or obj.answer or obj.evidence_ids):
            raise ValueError('Answer questions through the evidence-backed answer command')
        if p.kind=='question' and any(q.id==obj.id and (q.status=='answered' or q.answer or q.evidence_ids) for q in case.questions):
            raise ValueError('A recorded answer cannot be erased by editing its question; record a revised answer instead')
        merge_object(data,p.kind,obj.model_dump(mode='json'))
    elif cmd.kind=='replace_graph':data['graph']=p.graph.model_dump(mode='json')
    elif cmd.kind in ('approve','complete'):
        action=next((a for a in case.graph.actions if a.id==p.action_id),None)
        if not action:raise ValueError('Unknown action')
        state=readiness(case,action,condition_states(case),now)
        if cmd.kind=='approve':
            if state['status']!='approval_required':raise ValueError('This action is not eligible for approval')
            routes=plan(case,now)['routes']
            if not any(action.id in r['actions'] and not r['hard_breaches'] and not r['evidence_gaps'] and not r['decisions'] for r in routes):
                raise ValueError('No currently supported, constraint-compatible route authorises this action')
            data['approvals']=[{**a.model_dump(mode='json'),'revision':revision} for a in case.approvals if a.revision==case.revision and a.expires_at>now and a.action_id!=action.id]
            data['approvals'].append(Approval(action_id=action.id,revision=revision,expires_at=now+timedelta(minutes=30),actor=actor).model_dump(mode='json'))
        else:
            if state['status']!='ready':raise ValueError('Action is not ready, or its approval has expired')
            data['completed'].append(action.id)
    elif cmd.kind=='decide':
        d=next((d for d in data['decisions'] if d['id']==p.decision_id),None)
        if not d:raise ValueError('Unknown decision')
        if not set(p.evidence_ids)<={e.id for e in case.evidence if e.status=='reviewed'}:
            raise ValueError('Decision evidence must be reviewed and belong to this case')
        d.update(selected=p.option_id,rationale=p.rationale,evidence_ids=p.evidence_ids,decided_at=now.isoformat(),decided_revision=revision)
    elif cmd.kind=='answer':
        q=next((q for q in data['questions'] if q['id']==p.question_id),None)
        if not q:raise ValueError('This is not a stored question; attest the linked condition instead')
        if not set(p.evidence_ids)<={e.id for e in case.evidence if e.status=='reviewed'}:
            raise ValueError('Question answers require reviewed evidence from this case')
        q.update(answer=p.answer,evidence_ids=p.evidence_ids,status='answered')
    data['revision']=revision;data['updated_at']=now.isoformat()
    updated=preserve_meaning(case,Case.model_validate(data))
    if updated.status=='closed' and not plan(updated,now)['outcome_evidenced']:
        updated.status='active'
    return updated
