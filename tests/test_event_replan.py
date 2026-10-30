"""Fictional local cache parity; not a production latency or provider benchmark."""
from datetime import datetime, timedelta, timezone

import pytest

from endstate.api import PlanRequest, calculate
from endstate.contracts import Approval
from eightball.event_workers.replan import EventReplanner
from eightball.v2.planner import to_snapshot
from eightball.v2.playbooks import demo_case

NOW = datetime(2026, 10, 25, tzinfo=timezone.utc)


def request():
    return PlanRequest(snapshot=to_snapshot(demo_case()), as_of=NOW)


def parity(planner, req, mode):
    result = planner.replan(req)
    assert result.mode == mode
    assert result.response == calculate(req)
    assert result.elapsed_seconds >= 0
    return result


def test_revision_only_replan_reuses_only_identical_inputs_and_detaches_results(monkeypatch):
    from eightball.event_workers import replan
    planner, req = EventReplanner(), request()
    first = parity(planner, req, 'full')
    first.response.plan['states'].clear()
    req.snapshot.revision += 1
    original = replan.calculate
    def no_recompute(*_):
        pytest.fail('No complete kernel call is needed for unchanged planning inputs')
    monkeypatch.setattr(replan, 'calculate', no_recompute)
    parity(planner, req, 'unchanged_inputs')
    monkeypatch.setattr(replan, 'calculate', original)


@pytest.mark.parametrize('change', ['graph', 'clock', 'sort', 'budget', 'completed', 'snapshot'])
def test_any_other_change_uses_complete_recomputation(change):
    planner, req = EventReplanner(), request()
    parity(planner, req, 'full')
    if change == 'graph':
        req.snapshot.graph.actions[0].cost += 1
    elif change == 'clock':
        req.as_of += timedelta(seconds=1)
    elif change == 'sort':
        req.sort_by = 'fastest'
    elif change == 'budget':
        req.snapshot.budget += 1
    elif change == 'completed':
        req.snapshot.completed.append(req.snapshot.graph.actions[0].id)
    else:
        req.snapshot.id = 'different-case'
    req.snapshot.revision += 1
    parity(planner, req, 'full')
    parity(planner, req, 'unchanged_inputs')


def test_revision_change_cannot_revive_an_approval_from_the_cache():
    planner, req = EventReplanner(), request()
    action = req.snapshot.graph.actions[0]
    action.approval_required = True
    req.snapshot.approvals = [Approval(action_id=action.id, revision=0, actor='fixture',
        expires_at=NOW+timedelta(minutes=1))]
    approved = parity(planner, req, 'full').response
    req.snapshot.revision = 1
    revoked = parity(planner, req, 'full').response
    assert approved.plan['action_states'][action.id] != revoked.plan['action_states'][action.id]
    req.as_of += timedelta(minutes=2)
    parity(planner, req, 'full')


def test_bounded_cache_eviction_and_invalid_input_fail_before_reuse():
    planner, req = EventReplanner(max_entries=1), request()
    parity(planner, req, 'full')
    second = req.model_copy(deep=True)
    second.snapshot.budget += 1
    parity(planner, second, 'full')
    parity(planner, req, 'full')
    req = req.model_dump(mode='python')
    req['snapshot']['budget'] = -1
    with pytest.raises(ValueError):
        planner.replan(req)
    with pytest.raises(ValueError):
        EventReplanner(max_entries=True)
