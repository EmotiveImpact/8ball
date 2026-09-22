"""Bounded backward planner. No language model, probabilities or external effects.

Routes describe conditional plans over a human-authored action catalogue.
Scheduling is greedy per owner, not a proof of globally optimal scheduling.
"""
from datetime import datetime, timedelta
from hashlib import sha256
from itertools import product
from .models import Situation, utcnow

LIMIT = 64
RISK = {'low': 0, 'medium': 1, 'high': 2}


def condition_states(case: Situation) -> dict:
    evidence = {e.id: e for e in case.evidence}
    superseded = {s for o in case.observations for s in o.supersedes}
    result = {}
    for c in case.graph.conditions:
        active = [o for o in case.observations if o.condition_id == c.id and o.id not in superseded
                  and evidence[o.evidence_id].status == 'reviewed']
        values = {o.value for o in active}
        status = 'disputed' if len(values) == 2 else ('true' if True in values else 'false' if values else 'unknown')
        result[c.id] = {'status': status, 'observations': [o.id for o in active],
                        'evidence': sorted({o.evidence_id for o in active})}
    return result


def action_status(case: Situation, action, states: dict) -> dict:
    missing = [c for c in action.requires if states[c]['status'] != 'true']
    if action.id in case.completed:
        state = 'completed'
    elif missing:
        state = 'blocked'
    elif action.approval_required and case.approvals.get(action.id) != case.revision:
        state = 'approval_required'
    else:
        state = 'ready'
    return {'id': action.id, 'status': state, 'missing': missing,
            'effects_verified': all(states[c]['status'] == 'true' for c in action.produces)}


def plan(case: Situation, now: datetime | None = None) -> dict:
    now = now or utcnow()
    states = condition_states(case)
    actions = {a.id: a for a in case.graph.actions}
    conditions = {c.id: c for c in case.graph.conditions}
    truncated = False
    memo = {}
    def trim(items):
        nonlocal truncated
        unique = list(dict.fromkeys(items))
        if len(unique) > LIMIT:
            truncated = True
        return unique[:LIMIT]
    def combine(groups):
        result = [(frozenset(), frozenset())]
        for group in groups:
            result = trim([(a | c, b | d) for (a, b), (c, d) in product(result, group)])
        return result
    def resolve(cid):
        if cid in memo:
            return memo[cid]
        if states[cid]['status'] == 'true':
            return [(frozenset(), frozenset())]
        # Contradictory observations must be reconciled before using this condition.
        if states[cid]['status'] == 'disputed':
            return [(frozenset(), frozenset([cid]))]
        producers = [a for a in case.graph.actions if cid in a.produces and a.id not in case.completed]
        routes = []
        for a in producers:
            for ids, unknowns in combine([resolve(c) for c in a.requires]):
                routes.append((ids | {a.id}, unknowns))
        if not routes:
            routes = [(frozenset(), frozenset([cid]))]
        memo[cid] = trim(routes)
        return memo[cid]
    candidates = combine([resolve(g) for g in case.graph.goals])
    results = []
    statuses = {a.id: action_status(case, a, states) for a in case.graph.actions}
    spent = sum(actions[a].cost for a in case.completed)
    for selected, unverified in candidates:
        remaining = set(selected)
        known_times = {c: 0.0 for c, v in states.items() if v['status'] == 'true'}
        # Unknown inputs get a provisional zero-minute verification time; prominently blocked.
        known_times.update({c: 0.0 for c in unverified})
        owner_available, schedule = {}, []
        while remaining:
            eligible = [actions[i] for i in remaining if all(c in known_times for c in actions[i].requires)]
            if not eligible:
                break
            def priority(a):
                dates = [conditions[c].due_at for c in a.produces if conditions[c].due_at]
                return (min(dates) if dates else case.deadline, a.id)
            a = min(eligible, key=priority)
            start = max([owner_available.get(a.owner, 0.0)] + [known_times[c] for c in a.requires])
            end = start + a.minutes
            owner_available[a.owner] = end
            for c in a.produces:
                known_times[c] = min(known_times.get(c, end), end)
            schedule.append({'action_id': a.id, 'start_minute': start, 'end_minute': end})
            remaining.remove(a.id)
        mins = max([s['end_minute'] for s in schedule] or [0])
        cost = sum(actions[a].cost for a in selected)
        breaches = []
        finish = now + timedelta(minutes=mins)
        if not all(states[g]['status'] == 'true' for g in case.graph.goals) and finish > case.deadline:
            breaches.append('Outcome deadline exceeded by the estimated remaining schedule')
        for c, minute in known_times.items():
            due = conditions[c].due_at
            if due and states[c]['status'] != 'true' and now + timedelta(minutes=minute) > due:
                breaches.append('Condition deadline exceeded: ' + conditions[c].title)
        if spent + cost > case.budget:
            breaches.append('Total estimated spend exceeds the case budget')
        gaps = sorted(unverified)
        ready = [i for i in sorted(selected) if statuses[i]['status'] == 'ready']
        approvals = [i for i in sorted(selected) if statuses[i]['status'] == 'approval_required']
        contingent = [i for i in sorted(selected) if actions[i].contingent]
        route_id = sha256(('|'.join(sorted(selected)) + ':' + '|'.join(gaps)).encode()).hexdigest()[:12]
        roots = [actions[i].title for i in sorted(selected) if set(actions[i].produces) & set(case.graph.goals)]
        results.append({'id': route_id, 'title': ' / '.join(roots) or ('Verify outstanding conditions' if gaps else 'Outcome evidenced'),
                        'actions': [s['action_id'] for s in schedule], 'schedule': schedule,
                        'unverified': gaps, 'ready': ready, 'approvals': approvals, 'contingent': contingent,
                        'minutes': mins, 'remaining_cost': cost, 'spent': spent, 'total_cost': spent + cost,
                        'max_risk': max([RISK[actions[i].risk] for i in selected] or [0]),
                        'slack_minutes': round((case.deadline - finish).total_seconds() / 60, 1),
                        'breaches': breaches, 'blocked': bool(gaps or remaining),
                        'schedule_is_provisional': bool(gaps or contingent),
                        'status': 'constraint_failure' if breaches else 'needs_evidence' if gaps or remaining else 'conditional_plan'})
    # Transparent preference order, not an outcome probability or global optimum.
    results.sort(key=lambda p: (bool(p['breaches']), p['blocked'], p['max_risk'], p['minutes'], p['remaining_cost'], p['id']))
    return {'revision': case.revision, 'computed_at': now.isoformat(), 'states': states,
            'action_states': statuses, 'routes': results, 'search_truncated': truncated,
            'outcome_evidenced': all(states[g]['status'] == 'true' for g in case.graph.goals),
            'ranking': 'Constraint fit, evidence gaps, highest action risk, duration, remaining cost. Not likelihood of success.',
            'limits': 'At most 64 partial routes per expansion; optimistic durations exclude unknown verification and third-party waiting. Per-owner greedy scheduling.'}


def difference(before: dict, after: dict) -> dict:
    changes = [{'condition_id': cid, 'before': old['status'], 'after': after['states'][cid]['status']}
               for cid, old in before['states'].items() if cid in after['states'] and old['status'] != after['states'][cid]['status']]
    ready_before = {k for k, v in before['action_states'].items() if v['status'] == 'ready'}
    ready_after = {k for k, v in after['action_states'].items() if v['status'] == 'ready'}
    return {'conditions': changes, 'newly_ready': sorted(ready_after - ready_before),
            'no_longer_ready': sorted(ready_before - ready_after),
            'previous_route': before['routes'][0]['id'] if before['routes'] else None,
            'current_route': after['routes'][0]['id'] if after['routes'] else None,
            'constraint_failures_before': sum(bool(r['breaches']) for r in before['routes']),
            'constraint_failures_after': sum(bool(r['breaches']) for r in after['routes'])}
