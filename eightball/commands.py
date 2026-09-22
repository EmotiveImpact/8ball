"""Only human commands can change evidence, graph, approval or completion state."""
from typing import Literal
from pydantic import Field, AwareDatetime
from .models import Strict, Identifier, Title, Text, Situation, Evidence, Observation, Graph
from .engine import plan, action_status, condition_states


class Command(Strict):
    event_id: Identifier
    expected_revision: int = Field(strict=True, ge=0)
    kind: Literal['add_evidence', 'review_evidence', 'observe', 'constraints', 'approve', 'complete', 'replace_graph']
    payload: dict


class AddEvidence(Strict):
    title: Title
    source: Title
    text: Text


class ReviewEvidence(Strict):
    evidence_id: Identifier
    status: Literal['reviewed', 'retracted']


class Observe(Strict):
    condition_id: Identifier
    evidence_id: Identifier
    value: bool = Field(strict=True)
    rationale: Title
    supersedes: list[Identifier] = Field(default_factory=list, max_length=100)


class Constraints(Strict):
    budget: int = Field(strict=True, ge=0, le=100000000)
    deadline: AwareDatetime


class ActionCommand(Strict):
    action_id: Identifier


class ReplaceGraph(Strict):
    graph: Graph


PAYLOADS = {'add_evidence': AddEvidence, 'review_evidence': ReviewEvidence, 'observe': Observe,
            'constraints': Constraints, 'approve': ActionCommand, 'complete': ActionCommand,
            'replace_graph': ReplaceGraph}


def apply(case: Situation, cmd: Command) -> Situation:
    payload = PAYLOADS[cmd.kind].model_validate(cmd.payload)
    data = case.model_dump(mode='json')
    next_revision = case.revision + 1
    data['approvals'] = {}  # all substantive changes require fresh approval
    if cmd.kind == 'add_evidence':
        data['evidence'].append(Evidence(**payload.model_dump()).model_dump(mode='json'))
    elif cmd.kind == 'review_evidence':
        match = next((e for e in data['evidence'] if e['id'] == payload.evidence_id), None)
        if match is None:
            raise ValueError('Evidence not found in this situation')
        if match['status'] == 'retracted' and payload.status != 'retracted':
            raise ValueError('A retracted source cannot be silently reinstated; add a new source')
        match['status'] = payload.status
    elif cmd.kind == 'observe':
        e = next((e for e in case.evidence if e.id == payload.evidence_id), None)
        if not e or e.status != 'reviewed':
            raise ValueError('Review the evidence source before attesting a condition')
        data['observations'].append(Observation(**payload.model_dump()).model_dump(mode='json'))
    elif cmd.kind == 'constraints':
        data['budget'], data['deadline'] = payload.budget, payload.deadline.isoformat()
    elif cmd.kind in ('approve', 'complete'):
        action = next((a for a in case.graph.actions if a.id == payload.action_id), None)
        if action is None:
            raise ValueError('Action not found in this situation')
        status = action_status(case, action, condition_states(case))
        if cmd.kind == 'approve':
            if status['status'] != 'approval_required':
                raise ValueError('Only an eligible action awaiting approval can be approved')
            routes = plan(case)['routes']
            if not any(action.id in r['actions'] and not r['breaches'] and not r['blocked'] for r in routes):
                raise ValueError('No constraint-compatible, evidence-supported route contains this action')
            data['approvals'] = {a: next_revision for a, rev in case.approvals.items() if rev == case.revision}
            data['approvals'][action.id] = next_revision
        else:
            if status['status'] != 'ready':
                raise ValueError('Action is blocked, already complete, or needs a current approval')
            data['completed'].append(action.id)
    elif cmd.kind == 'replace_graph':
        # Preserve evidential meaning: observed conditions and completed actions cannot be redefined.
        new_conditions = {c.id: c for c in payload.graph.conditions}
        old_conditions = {c.id: c for c in case.graph.conditions}
        for o in case.observations:
            if new_conditions.get(o.condition_id) != old_conditions[o.condition_id]:
                raise ValueError('An observed condition cannot be removed or redefined; add a new ID')
        new_actions = {a.id: a for a in payload.graph.actions}
        old_actions = {a.id: a for a in case.graph.actions}
        if any(new_actions.get(i) != old_actions[i] for i in case.completed):
            raise ValueError('A completed action cannot be removed or redefined')
        data['graph'] = payload.graph.model_dump(mode='json')
    data['revision'] = next_revision
    return Situation.model_validate(data)
