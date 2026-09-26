"""Derive supported conditions from validated sources and observations.

Accepts the common graph/evidence/observations shape, including preserved V1
records. No expected action effect is promoted into observed state here.
"""

def condition_states(case) -> dict:
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
