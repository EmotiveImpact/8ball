"""Read-only, versioned chosen-course anchoring and reconsideration.

A course is a recorded choice, never an action permission. Computations below
neither persist data nor switch to another candidate. Callers supply an aware
clock and an opaque digest of their human target/mandate.
"""
from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
from typing import Literal

from pydantic import AwareDatetime, Field, model_validator

from .contracts import PlanningSnapshot, all_of, atom, literals
from .primitives import Strict, Identifier
from .results import RouteResult, PlanResult, validate_plan
from .planner import plan

CONTRACT = 'endstate.course.v1'
Hash = str


def checksum(value) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def detached(snapshot: PlanningSnapshot) -> PlanningSnapshot:
    return PlanningSnapshot.model_validate(snapshot.model_dump(mode='python'))


class Watch(Strict):
    condition_id: Identifier
    state: Literal['true', 'false', 'unknown', 'disputed']


class CourseAnchor(Strict):
    contract_version: Literal['endstate.course.v1'] = CONTRACT
    selected_at: AwareDatetime
    target_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    baseline: PlanningSnapshot
    route: RouteResult
    watches: list[Watch] = Field(default_factory=list, max_length=12)
    review_at: AwareDatetime | None = None

    @model_validator(mode='after')
    def references(self):
        known = {c.id for c in self.baseline.graph.conditions}
        if any(w.condition_id not in known for w in self.watches):
            raise ValueError('Watch conditions must belong to this snapshot')
        keys = [(w.condition_id, w.state) for w in self.watches]
        if len(keys) != len(set(keys)):
            raise ValueError('Repeated course watch')
        if self.review_at is not None and self.review_at <= self.selected_at:
            raise ValueError('Choose a review time after the selection time')
        if not self.route['actions'] or self.route['hard_breaches']:
            raise ValueError('Choose a non-empty candidate without recorded hard breaches')
        return self


class Reason(Strict):
    code: str
    detail: str
    references: list[str] = Field(default_factory=list)
    requires_review: bool = Field(default=True, strict=True)


class CourseAssessment(Strict):
    contract_version: Literal['endstate.course.v1'] = CONTRACT
    snapshot_id: Identifier
    revision: int = Field(strict=True, ge=0)
    selected_revision: int = Field(strict=True, ge=0)
    selected_route_id: Identifier
    as_of: AwareDatetime
    state: Literal['review_required', 'no_trigger_detected', 'outcome_evidenced', 'not_assessable']
    reasons: list[Reason]
    remaining_action_ids: list[Identifier]
    completed_action_ids: list[Identifier]
    remaining_plan: PlanResult | None = None
    compatible_remainders: int = Field(strict=True, ge=0)
    alternatives: list[dict] = Field(default_factory=list)
    execution_authorised: Literal[False] = False
    automatically_switched: Literal[False] = False
    monitoring: Literal['on_request'] = 'on_request'
    notice: str = ('Assessment on request, within the recorded catalogue and search bounds. '
                   'No selected course, fact or action approval is changed. No background alert service.')


def anchor_route(snapshot: PlanningSnapshot, route_id: str, target_sha256: str,
                 as_of: datetime, *, watches: list[Watch] | None = None,
                 review_at: datetime | None = None) -> CourseAnchor:
    """Choose exactly a candidate computed at this snapshot and supplied time."""
    snapshot = detached(snapshot)
    # Parsing the aware clock before calculation prevents accidental local-time use.
    from pydantic import TypeAdapter
    as_of = TypeAdapter(AwareDatetime).validate_python(as_of)
    result = plan(snapshot, as_of)
    route = next((r for r in result['routes'] if r['id'] == route_id), None)
    if route is None:
        raise ValueError('Selected route is not in this snapshot calculation')
    return CourseAnchor(selected_at=as_of, target_sha256=target_sha256, baseline=snapshot,
                        route=route, watches=watches or [], review_at=review_at)


def verify_anchor(anchor: CourseAnchor) -> CourseAnchor:
    anchor = CourseAnchor.model_validate(anchor.model_dump(mode='python'))
    result = plan(anchor.baseline, anchor.selected_at)
    expected = next((r for r in result['routes'] if r['id'] == anchor.route['id']), None)
    if expected != anchor.route:
        raise ValueError('Recorded route does not reproduce from its original snapshot and clock')
    return anchor


def assess_course(anchor: CourseAnchor, current: PlanningSnapshot, target_sha256: str,
                  as_of: datetime) -> CourseAssessment:
    """Reconsider a fixed choice, rather than relabel the newest top-ranked route.

    Remaining calculations are constrained to selected actions and the exact
    chosen prerequisite branch. Already-completed work is not scheduled again.
    Graph/meaning changes remain reasons to review, never silent acceptance.
    """
    anchor = verify_anchor(anchor)
    current = detached(current)
    old = anchor.baseline
    from pydantic import TypeAdapter
    as_of = TypeAdapter(AwareDatetime).validate_python(as_of)
    if old.id != current.id or current.revision < old.revision or as_of < anchor.selected_at:
        raise ValueError('Cannot assess a course against another case or an earlier revision/clock')
    if current.revision == old.revision and current != old:
        raise ValueError('A changed snapshot cannot retain the same revision')
    if len(target_sha256) != 64 or any(c not in '0123456789abcdef' for c in target_sha256):
        raise ValueError('Target digest is invalid')

    baseline_result = plan(old, anchor.selected_at)
    current_result = plan(current, as_of)
    reasons: list[Reason] = []
    def add(code, detail, refs=(), review=True):
        reasons.append(Reason(code=code, detail=detail, references=list(refs), requires_review=review))
    selected = set(anchor.route['actions'])
    before_actions = {a.id: a for a in old.graph.actions}
    after_actions = {a.id: a for a in current.graph.actions}
    relevant = set(anchor.route['used_conditions']) | {w.condition_id for w in anchor.watches}
    for aid in selected:
        a = before_actions[aid]
        relevant |= {cid for cid, _ in literals(a.requires) | literals(a.guard)}
        relevant |= {e.condition_id for e in a.effects}
    relevant |= {cid for obj in old.graph.objectives for cid, _ in literals(obj.success)}
    for obj in old.graph.objectives:
        if obj.failure:
            relevant |= {cid for cid, _ in literals(obj.failure)}

    if target_sha256 != anchor.target_sha256 or old.graph.objectives != current.graph.objectives:
        add('target_changed', 'The target or success/failure criteria differ from the recorded choice.', ['target'])
    if current.budget != old.budget:
        add('budget_changed', 'The available budget changed; review the chosen estimates.', ['budget'])
    if current.deadline != old.deadline:
        add('deadline_changed', 'The outcome deadline changed.', ['deadline'])
    missing_actions = sorted(selected - after_actions.keys())
    missing_conditions = sorted(relevant - current_result['states'].keys())
    if missing_actions:
        add('actions_missing', 'Recorded actions are no longer in the current graph.', ['action:'+i for i in missing_actions])
    if missing_conditions:
        add('conditions_missing', 'Conditions needed to assess the chosen course are missing.', ['condition:'+i for i in missing_conditions])
    unavailable = sorted(i for i in selected & after_actions.keys()
                         if i not in current.completed and not after_actions[i].enabled)
    if unavailable:
        add('chosen_action_unavailable', 'An uncompleted action in the recorded course is disabled. A verification-only remainder is not proof the original work can proceed.', ['action:'+i for i in unavailable])
    changed_actions = sorted(i for i in selected & after_actions.keys() if before_actions[i] != after_actions[i])
    if changed_actions:
        add('actions_changed', 'The recorded actions or their declared requirements changed.', ['action:'+i for i in changed_actions])
    before_conditions = {c.id: c for c in old.graph.conditions}
    after_conditions = {c.id: c for c in current.graph.conditions}
    changed_conditions = sorted(i for i in relevant & before_conditions.keys() & after_conditions.keys()
                                if before_conditions[i] != after_conditions[i])
    if changed_conditions:
        add('conditions_changed', 'Condition meaning, confirmation rules or deadlines changed.', ['condition:'+i for i in changed_conditions])
    support_changes = sorted(i for i in relevant & current_result['states'].keys() & baseline_result['states'].keys()
                             if baseline_result['states'][i] != current_result['states'][i])
    if support_changes:
        add('evidence_changed', 'Evidence state or supporting records changed for the chosen course.', ['condition:'+i for i in support_changes])
    evidence_before = {e.id: e for e in old.evidence}
    if any(evidence_before.get(e.id) != e for e in current.evidence) or len(old.evidence) != len(current.evidence):
        add('source_context_changed', 'The source set changed. New or withdrawn text is not automatically interpreted.', ['sources'])

    def relevant_constraints(snapshot):
        return [x.model_dump(mode='json') for x in snapshot.constraints if not x.action_ids or selected.intersection(x.action_ids)]
    if relevant_constraints(old) != relevant_constraints(current):
        add('restrictions_changed', 'Restrictions applying to the chosen work changed.', ['constraints'])
    actor_ids = {i for aid in selected for i in before_actions[aid].actor_ids}
    actor_ids |= {before_conditions[i].actor_id for i in relevant & before_conditions.keys() if before_conditions[i].actor_id}
    resource_ids = {i for aid in selected for i in before_actions[aid].resources}
    decision_ids = {before_actions[i].decision_id for i in selected if before_actions[i].decision_id}
    for name, ids in [('actors', actor_ids), ('resources', resource_ids), ('decisions', decision_ids)]:
        old_values = {x.id: x for x in getattr(old, name) if x.id in ids}
        new_values = {x.id: x for x in getattr(current, name) if x.id in ids}
        if old_values != new_values:
            add(name+'_changed', 'Recorded '+name+' linked to this choice changed.', [name+':'+i for i in sorted(ids)])
    for watch in anchor.watches:
        state = current_result['states'].get(watch.condition_id, {}).get('status')
        if state == watch.state:
            add('watch_triggered', 'An explicit watch condition now matches '+watch.state+'.', ['condition:'+watch.condition_id])
    if anchor.review_at is not None and as_of >= anchor.review_at:
        add('review_time_reached', 'The operator-selected review time has been reached.', ['review_at'])
    if current_result['search_truncated']:
        add('search_incomplete', 'The current candidate search reached a declared bound. Completeness is not established.')

    completed = sorted(selected.intersection(current.completed))
    remaining = sorted(selected - set(completed))
    residual = None
    compatible = 0
    if not missing_actions and not missing_conditions:
        data = current.model_dump(mode='python')
        for a in data['graph']['actions']:
            if a['id'] not in selected:
                a['enabled'] = False
            else:
                # Preserve the exact selected OR/sign branch. Never silently use a new shortcut.
                chosen = anchor.route['prerequisites'].get(a['id'], [])
                a['requires'] = all_of(*(atom(x['condition_id'], x['value']) for x in chosen)).model_dump(mode='python')
        restricted = PlanningSnapshot.model_validate(data)
        residual = plan(restricted, as_of)
        validate_plan(residual)
        for candidate in residual['routes']:
            scheduled = {s['action_id']: s for s in candidate['schedule']}
            order_ok = all(u not in scheduled or v not in scheduled or
                           scheduled[v]['start_minute'] >= scheduled[u]['end_minute']
                           for u, v in anchor.route['dependencies'])
            if not candidate['hard_breaches'] and order_ok:
                compatible += 1
        if not residual['outcome_evidenced'] and not compatible:
            add('no_compatible_remainder', 'No compatible remainder was found using the recorded actions and prerequisite branches. This is not proof no solution exists.')
        if any(r['evidence_gaps'] for r in residual['routes']):
            add('verification_gaps', 'The remaining chosen work has unresolved evidence or guard requirements.')
        if any(r['decisions'] for r in residual['routes']):
            add('decisions_outstanding', 'The chosen work still needs an explicit decision.')
        if residual['search_truncated']:
            add('remainder_search_incomplete', 'The restricted remainder search is incomplete.')
        if any(r['unknown_waits'] for r in residual['routes']):
            add('unspecified_waits', 'Some waiting periods are still unspecified; time estimates are lower bounds.', review=False)
    else:
        add('assessment_incomplete', 'The original course cannot be fully assessed against the current record.')
    if current.revision != old.revision and not reasons:
        add('context_revision_changed', 'The case revision changed; no declared dependency trigger was detected. Unmodelled implications still need human judgement.', review=False)
    state = ('not_assessable' if missing_actions or missing_conditions else
             'review_required' if any(r.requires_review for r in reasons) else
             'outcome_evidenced' if current_result['outcome_evidenced'] else 'no_trigger_detected')
    # Alternatives are suggestions for inspection, never a replacement or a selected route.
    alternatives = [{'id':r['id'], 'title':r['title'], 'status':r['status'],
                     'hard_breaches':r['hard_breaches'], 'actions':r['actions']}
                    for r in current_result['routes'] if set(r['actions']) - selected][:8]
    return CourseAssessment(snapshot_id=current.id, revision=current.revision,
                            selected_revision=old.revision, selected_route_id=anchor.route['id'], as_of=as_of,
                            state=state, reasons=reasons, remaining_action_ids=remaining,
                            completed_action_ids=completed, remaining_plan=residual,
                            compatible_remainders=compatible, alternatives=alternatives)
