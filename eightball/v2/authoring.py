"""Read-only graph amendment preview using the exact live command semantics.

A preview neither reserves an action nor certifies a plan. Commit still uses the
existing revisioned command boundary; no observation or approval is manufactured.
"""
from .contracts import Case, Graph, Strict, Identifier
from .commands import Command, apply
from .planner import plan, changes
from ..models import utcnow
from ..store import Conflict, digest
from pydantic import Field


class GraphPreview(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    graph: Graph


def preview_graph(case: Case, request: GraphPreview) -> dict:
    if case.revision != request.expected_revision:
        raise Conflict('This draft is based on an older case revision. Reload before previewing.')
    now = utcnow()
    command = Command(event_id='graph_preview', expected_revision=case.revision,
                      kind='replace_graph', payload={'graph': request.graph.model_dump(mode='json')})
    candidate = apply(case, command, now=now)
    before, after = plan(case, now), plan(candidate, now)
    edits = []
    for kind in ('conditions', 'actions', 'objectives'):
        old = {x.id: x.model_dump(mode='json') for x in getattr(case.graph, kind)}
        new = {x.id: x.model_dump(mode='json') for x in getattr(candidate.graph, kind)}
        for key in sorted(old.keys() | new.keys()):
            if old.get(key) != new.get(key):
                fields = sorted(k for k in (old.get(key, {}).keys() | new.get(key, {}).keys())
                                if old.get(key, {}).get(k) != new.get(key, {}).get(k))
                edits.append({'collection': kind, 'id': key,
                              'title': new.get(key, old.get(key, {})).get('title', key),
                              'change': 'added' if key not in old else 'removed' if key not in new else 'edited',
                              'fields': fields})
    warnings = []
    if not any(o.mandatory for o in candidate.graph.objectives):
        warnings.append('No mandatory objective: this case has no completion target.')
    if case.graph.objectives != candidate.graph.objectives:
        warnings.append('Success or failure criteria changed. Review this with the case owner.')
    if case.approvals:
        warnings.append(f'Committing will invalidate {len(case.approvals)} current approval record(s).')
    if after['search_truncated']:
        warnings.append('Route search reached its bound. Candidate routes are incomplete.')
    if any(r['hard_breaches'] for r in after['routes']):
        warnings.append('Some candidate routes breach constraints; inspect them before deciding.')
    if case.status == 'closed' and candidate.status != 'closed':
        warnings.append('This amendment would reopen the closed case.')
    return {'preview': True, 'persisted': False, 'base_revision': case.revision,
            'graph_sha256': digest(request.graph.model_dump(mode='json')), 'edits': edits,
            'warnings': warnings, 'approvals_invalidated': len(case.approvals),
            'live_routes': len(before['routes']), 'plan': after,
            'changes': changes(case, candidate, before, after),
            'note': 'Draft preview only. A revision-checked human commit is still required. No facts were attested.'}
