"""Deterministic, discarded hypothetical projections. No services or persistence."""
from datetime import datetime

from pydantic import AwareDatetime, Field, model_validator

from . import CONTRACT_VERSION, planner
from .contracts import Count, PlanningSnapshot
from .insights import stable_hash
from .plan_review import compact
from .primitives import Evidence, Identifier, Observation, Strict
from .rehearsal import changed_fields

VERSION = 'endstate.scenario-comparison.v1'


class Scenario(Strict):
    expected_revision: int = Field(strict=True, ge=0)
    budget: Count | None = None
    deadline: AwareDatetime | None = None
    conditions: dict[Identifier, bool] = Field(default_factory=dict, max_length=80)
    unavailable_actions: list[Identifier] = Field(default_factory=list, max_length=64)
    resource_starts: dict[Identifier, AwareDatetime] = Field(default_factory=dict, max_length=24)
    decisions: dict[Identifier, Identifier] = Field(default_factory=dict, max_length=40)

    @model_validator(mode='before')
    @classmethod
    def strict_truth(cls, data):
        if isinstance(data, dict) and (not isinstance(data.get('conditions', {}), dict)
                or any(type(v) is not bool for v in data.get('conditions', {}).values())):
            raise ValueError('Hypothetical conditions must use explicit booleans')
        return data

    @model_validator(mode='after')
    def unique_actions(self):
        if len(set(self.unavailable_actions)) != len(self.unavailable_actions):
            raise ValueError('Repeated unavailable action')
        return self


def project(snapshot: PlanningSnapshot, scenario: Scenario, as_of: datetime) -> PlanningSnapshot:
    snapshot = PlanningSnapshot.model_validate(snapshot.model_dump(mode='python'))
    scenario = Scenario.model_validate(scenario.model_dump(mode='python'))
    if as_of.tzinfo is None or as_of.utcoffset() is None:
        raise ValueError('Scenario calculation clock must include a timezone')
    if scenario.expected_revision != snapshot.revision:
        raise ValueError('Scenario is based on a stale snapshot revision')
    known = {c.id for c in snapshot.graph.conditions}
    actions = {a.id for a in snapshot.graph.actions}
    resources = {r.id for r in snapshot.resources}
    if (not set(scenario.conditions) <= known or not set(scenario.unavailable_actions) <= actions
            or not set(scenario.resource_starts) <= resources):
        raise ValueError('Scenario references a missing snapshot object')
    if set(scenario.unavailable_actions) & set(snapshot.completed):
        raise ValueError('A scenario cannot remove completed history')
    data = snapshot.model_dump(mode='json')
    data['approvals'] = []
    if scenario.budget is not None:
        data['budget'] = scenario.budget
    if scenario.deadline is not None and scenario.deadline != snapshot.deadline:
        data['deadline'] = scenario.deadline.isoformat()
    existing = {x.id for x in [*snapshot.evidence, *snapshot.observations]}

    def synthetic_id(kind, cid):
        number = 0
        while True:
            key = 'scenario_' + stable_hash([kind, cid, scenario.conditions[cid], as_of.isoformat(), number])[:56]
            if key not in existing:
                existing.add(key)
                return key
            number += 1

    for cid, value in sorted(scenario.conditions.items()):
        evidence = Evidence(id=synthetic_id('source', cid), title='Hypothetical assumption', source='Scenario only',
                            text='Not case evidence.', status='reviewed', added_at=as_of)
        data['evidence'].append(evidence.model_dump(mode='json'))
        data['observations'].append(Observation(id=synthetic_id('observation', cid), condition_id=cid,
            evidence_id=evidence.id, value=value, rationale='Scenario only', added_at=as_of,
            supersedes=[o.id for o in snapshot.observations if o.condition_id == cid]).model_dump(mode='json'))
    for action in data['graph']['actions']:
        if action['id'] in scenario.unavailable_actions:
            action['enabled'] = False
    for resource in data['resources']:
        if resource['id'] in scenario.resource_starts and scenario.resource_starts[resource['id']] != next(r.available_from for r in snapshot.resources if r.id == resource['id']):
            resource['available_from'] = scenario.resource_starts[resource['id']].isoformat()
    decisions = {d['id']: d for d in data['decisions']}
    if not set(scenario.decisions) <= decisions.keys():
        raise ValueError('Unknown scenario decision')
    for key, option in scenario.decisions.items():
        decisions[key]['selected'] = option
    return PlanningSnapshot.model_validate(data)


def _result(snapshot, as_of):
    result = planner.plan(snapshot, as_of)
    return {**compact(result), 'condition_states': result['states'],
            'stop_reason': 'search_cutoff' if result['search_truncated'] else 'declared_catalogue_evaluated',
            'notice': 'A route count is not a probability. Empty results concern this bounded declared catalogue only.'}


def compare(snapshot: PlanningSnapshot, scenario: Scenario, as_of: datetime):
    snapshot = PlanningSnapshot.model_validate(snapshot.model_dump(mode='python'))
    scenario = Scenario.model_validate(scenario.model_dump(mode='python'))
    before = snapshot.model_dump(mode='json')
    clone = project(snapshot, scenario, as_of)
    changes = changed_fields(before, clone.model_dump(mode='json'))
    allowed = {('approvals',)} if snapshot.approvals else set()
    if scenario.budget is not None and scenario.budget != snapshot.budget:
        allowed.add(('budget',))
    if scenario.deadline is not None and scenario.deadline != snapshot.deadline:
        allowed.add(('deadline',))
    allowed.update(('graph', 'actions', a.id, 'enabled') for a in snapshot.graph.actions if a.id in scenario.unavailable_actions and a.enabled)
    allowed.update(('resources', r.id, 'available_from') for r in snapshot.resources
                   if r.id in scenario.resource_starts and scenario.resource_starts[r.id] != r.available_from)
    allowed.update(('decisions', d.id, 'selected') for d in snapshot.decisions
                   if d.id in scenario.decisions and scenario.decisions[d.id] != d.selected)
    new_sources = [e for e in clone.evidence if e.id not in {x.id for x in snapshot.evidence}]
    new_observations = [o for o in clone.observations if o.id not in {x.id for x in snapshot.observations}]
    if (len(new_sources) != len(scenario.conditions) or len(new_observations) != len(scenario.conditions)
            or {o.condition_id: o.value for o in new_observations} != scenario.conditions
            or {o.evidence_id for o in new_observations} != {e.id for e in new_sources}):
        raise ValueError('Scenario hypothetical observations differ from the declared overlay')
    allowed.update(('evidence', e.id) for e in new_sources)
    allowed.update(('observations', o.id) for o in new_observations)
    if snapshot.model_dump(mode='json') != before or {tuple(c['path']) for c in changes} != allowed:
        raise ValueError('Scenario changed a field outside its declared overlay')
    baseline, result = _result(snapshot, as_of), _result(clone, as_of)
    manifest = {'contract_version': VERSION, 'planner_version': CONTRACT_VERSION,
                'snapshot_sha256': stable_hash(before), 'revision': snapshot.revision, 'as_of': as_of.isoformat(),
                'overlay': scenario.model_dump(mode='json'), 'scenario_sha256': stable_hash(clone.model_dump(mode='json')),
                'changed_fields': changes, 'baseline_sha256': stable_hash(baseline), 'result_sha256': stable_hash(result),
                'limits': {'max_routes': planner.MAX_ROUTES, 'max_expansions': planner.MAX_EXPANSIONS},
                'randomness_used': False, 'hypothetical': True, 'persisted': False,
                'notice': 'Synthetic observations and approval removal exist only in the discarded hypothetical copy.'}
    return {'baseline': baseline, 'result': result, 'manifest': manifest, 'manifest_sha256': stable_hash(manifest)}


def verify(snapshot: PlanningSnapshot, comparison: dict):
    """Recompute against the supplied exact input. Digests alone are not replay."""
    try:
        manifest = comparison['manifest']
        expected = compare(snapshot, Scenario.model_validate(manifest['overlay']), datetime.fromisoformat(manifest['as_of']))
        if expected != comparison:
            raise ValueError('Scenario comparison differs from deterministic replay')
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        raise ValueError('Scenario comparison failed replay verification') from exc
    return True
