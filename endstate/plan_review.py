"""Bounded, read-only plan inspection. Diagnostics are NOT semantic approval.

No database, provider or product imports. Caller supplies the clock and authority.
All stress results describe separate hypothetical snapshots, never live facts.
"""
from datetime import datetime, timedelta
from typing import Literal
from pydantic import Field, AwareDatetime, model_validator
from .contracts import PlanningSnapshot, literals
from .primitives import Strict, Identifier
from .planner import plan, evaluate

REVIEW_VERSION = 'endstate.plan-review.v1'
RUBRIC_VERSION = 'endstate.plan-rubric.v1'
RUBRIC = [
    {'id': 'target', 'title': 'Does this solve the requested outcome?',
     'question': 'Compare every mandatory success criterion with the requested outcome. Has any part been omitted, narrowed or replaced?'},
    {'id': 'sources', 'title': 'Are facts separate from assumptions?',
     'question': 'Check exact source wording, negation, contradictions and attribution. A reviewed claim is not proof that its contents are true.'},
    {'id': 'dependencies', 'title': 'Are the necessary steps present?',
     'question': 'Check prerequisites, alternative branches and final verification. A valid graph can still omit an essential real-world step.'},
    {'id': 'authority', 'title': 'Are authority and restrictions explicit?',
     'question': 'Confirm who can agree, what permission is needed and which constraints govern each action. An actor reference is not proof of authority.'},
    {'id': 'estimates', 'title': 'Are time, cost and waiting defensible?',
     'question': 'Check estimates, available resources and unspecified waits. A schedule fitting the deadline is not a forecast that it will happen.'},
    {'id': 'alternatives', 'title': 'Are alternatives and fallbacks meaningful?',
     'question': 'Check whether routes differ materially and what happens on refusal, delay or failure. Explain why one route is enough when alternatives are unavailable.'},
]


class Stress(Strict):
    kind: Literal['remove_action', 'budget', 'elapsed']
    action_id: Identifier | None = None
    amount: int | None = Field(default=None, strict=True, ge=0, le=100_000_000)
    minutes: int | None = Field(default=None, strict=True, ge=1, le=10080)

    @model_validator(mode='after')
    def checked(self):
        expected = {'remove_action': 'action_id', 'budget': 'amount', 'elapsed': 'minutes'}[self.kind]
        present = {k for k in ('action_id', 'amount', 'minutes') if getattr(self, k) is not None}
        if present != {expected}:
            raise ValueError('Each scenario needs exactly the field for its selected type')
        return self


class Inspection(Strict):
    as_of: AwareDatetime
    scenarios: list[Stress] = Field(default_factory=list, max_length=3)


def compact(result):
    compatible = [r for r in result['routes'] if not r['hard_breaches']]
    supported = [r for r in compatible if not r['evidence_gaps'] and not r['decisions']]
    return {
        'candidate_routes': len(result['routes']), 'constraint_compatible': len(compatible),
        'without_recorded_gaps_or_decisions': len(supported),
        'search_truncated': result['search_truncated'], 'outcome_evidenced': result['outcome_evidenced'],
        'routes': [{'id': r['id'], 'title': r['title'], 'status': r['status'], 'actions': r['actions'],
                    'minutes': r['minutes'], 'total_cost': r['total_cost'], 'provisional': r['provisional'],
                    'hard_breaches': r['hard_breaches'], 'evidence_gaps': r['evidence_gaps'],
                    'decisions': r['decisions'], 'unknown_waits': r['unknown_waits'],
                    'external_dependencies': r['external_dependencies']} for r in result['routes']],
    }


def inspect_plan(snapshot: PlanningSnapshot, request: Inspection) -> dict:
    state = PlanningSnapshot.model_validate(snapshot.model_dump(mode='python'))
    request = Inspection.model_validate(request.model_dump(mode='python'))
    now = request.as_of
    result = plan(state, now)
    flags = []

    def flag(rule, severity, title, detail, refs):
        flags.append({'rule': rule, 'severity': severity, 'title': title, 'detail': detail, 'references': sorted(set(refs))})

    mandatory = [o for o in state.graph.objectives if o.mandatory]
    if not mandatory:
        flag('no_target', 'blocker', 'No mandatory outcome criteria',
             'Define explicit success conditions before treating this as a route to an outcome.', [])
    if result['search_truncated']:
        flag('search_bound', 'limit', 'Candidate search reached its bound',
             'Comparisons cover the returned candidates only. A missing route is not proof that no route exists.', [])
    if result['objective_failures']:
        flag('failure_supported', 'blocker', 'An objective failure condition is supported',
             'Inspect the recorded failure criterion and evidence. Do not declare resolution.',
             ['objective:' + i for i in result['objective_failures']])
    if mandatory and not any(not r['hard_breaches'] for r in result['routes']):
        flag('no_compatible_candidate', 'attention', 'No returned candidate fits all hard constraints',
             'Inspect the breaches and search limits. This is not proof that the real situation is impossible.', [])
    for c in state.graph.conditions:
        if result['states'][c.id]['status'] == 'disputed':
            flag('disputed_condition', 'attention', c.title + ': conflicting evidence',
                 'Resolve conflicting observations explicitly; a model or review cannot settle them automatically.', ['condition:' + c.id])
    covered = set().union(*(set(r['actions']) for r in result['routes'])) if result['routes'] else set()
    for a in state.graph.actions:
        refs = ['action:' + a.id]
        if a.id in state.completed and not result['action_states'][a.id]['effects_evidenced']:
            flag('completion_unproved', 'attention', a.title + ': result not established',
                 'The work is recorded as complete, but at least one intended effect lacks supporting evidence.', refs)
        if a.id not in covered:
            continue
        if a.wait_minutes is None:
            flag('unknown_wait', 'attention', a.title + ': waiting time unspecified',
                 'The displayed duration is a lower bound, not a reliable finish time.', refs)
        if a.contingent and not a.contingencies:
            flag('external_no_branch', 'question', a.title + ': external response has no declared fallback',
                 'Review refusal and no-response handling. This flag does not prove that a fallback is required or possible.', refs)
        if a.reversibility == 'irreversible':
            flag('irreversible', 'attention', a.title + ': irreversible action',
                 'Review authority and consequences before using this candidate route.', refs)
    for o in mandatory:
        for cid, value in sorted(literals(o.success)):
            producers = [a for a in state.graph.actions if a.enabled and any(e.condition_id == cid and e.value == value for e in a.effects)]
            supported = result['states'][cid]['status'] == ('true' if value else 'false')
            if not supported and not producers:
                flag('goal_without_producer', 'question', 'Outcome condition has no declared producing action',
                     'It may require direct evidence rather than another action. Confirm how this condition will be established.', ['condition:' + cid, 'objective:' + o.id])
    target_trace = [{
        'objective_id': o.id, 'title': o.title, 'status': result['objective_states'][o.id],
        'success_expression': o.success.model_dump(mode='json'),
        'conditions': [{'id': cid, 'required_value': value,
                       'title': next(c.title for c in state.graph.conditions if c.id == cid),
                       'confirmation': next(c.confirmation for c in state.graph.conditions if c.id == cid),
                       'current_state': result['states'][cid]['status'],
                       'supporting_source_ids': result['states'][cid]['evidence'],
                       'declared_producers': [a.id for a in state.graph.actions if any(e.condition_id == cid and e.value == value for e in a.effects)]}
                      for cid, value in sorted(literals(o.success))],
    } for o in mandatory]
    baseline = compact(result)
    trials = []
    for spec in request.scenarios:
        spec.checked()
        copy = state.model_dump(mode='python')
        # Scenario approvals are always removed; results have no execution authority.
        copy['approvals'] = []
        clock = now
        if spec.kind == 'remove_action':
            action = next((a for a in copy['graph']['actions'] if a['id'] == spec.action_id), None)
            if not action or not action['enabled'] or action['id'] in state.completed:
                raise ValueError('Select an enabled action that has not already been completed')
            action['enabled'] = False
            label = 'Without action: ' + action['title']
        elif spec.kind == 'budget':
            copy['budget'] = spec.amount
            label = f'Budget set to {spec.amount} accounting units'
        else:
            clock += timedelta(minutes=spec.minutes)
            label = f'After {spec.minutes} minutes without new evidence'
        trial = compact(plan(PlanningSnapshot.model_validate(copy), clock))
        trials.append({'assumption': spec.model_dump(mode='json', exclude_none=True), 'label': label,
                       'as_of': clock.isoformat(), 'hypothetical': True, 'result': trial,
                       'compatible_change': trial['constraint_compatible'] - baseline['constraint_compatible'],
                       'note': 'Independent scenario. No live state, facts, approval or selected route changed.'})
    return {'contract_version': REVIEW_VERSION, 'as_of': now.isoformat(), 'snapshot_id': state.id,
            'revision': state.revision, 'target_trace': target_trace, 'flags': flags,
            'baseline': baseline, 'scenarios': trials,
            'counts': {s: sum(f['severity'] == s for f in flags) for s in ('blocker', 'attention', 'question', 'limit')},
            'semantics_verified': False, 'execution_authorised': False,
            'scope': 'Bounded structural inspection, not a success prediction or professional judgement. A clean graph may still describe the wrong plan.'}
