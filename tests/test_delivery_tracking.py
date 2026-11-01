"""Checks for progress-document integrity, not application acceptance."""
import importlib.util
import fnmatch
import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('delivery_docs', ROOT / 'scripts/delivery.py')
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)


def ledger():
    return json.loads((ROOT / delivery.LEDGER).read_text())


def test_current_ledger_validates():
    delivery.validate(ledger())


def test_generated_board_is_current():
    assert delivery.render(ledger()) == (ROOT / delivery.BOARD).read_text()


def test_duplicate_json_keys_rejected():
    with pytest.raises(ValueError):
        json.loads('{"status":"blocked","status":"verified"}', object_pairs_hook=delivery.unique_keys)


def test_verified_task_needs_evidence():
    data = ledger()
    data['tasks'][0]['evidence'] = []
    with pytest.raises(ValueError, match='verified tasks need evidence'):
        delivery.validate(data)


def test_blocked_task_needs_reason():
    data = ledger()
    task = next(t for t in data['tasks'] if t['status'] == 'blocked')
    task['blockers'] = []
    with pytest.raises(ValueError, match='blocked task needs'):
        delivery.validate(data)


def test_missing_dependencies_rejected():
    data = ledger()
    data['tasks'][-1]['depends_on'] = ['MISSING-01']
    with pytest.raises(ValueError, match='dependency'):
        delivery.validate(data)


def test_dependency_cycles_rejected():
    data = ledger()
    a = next(t for t in data['tasks'] if t['id'] == 'ES01-01')
    a['depends_on'] = ['ES01-02']
    with pytest.raises(ValueError, match='cycle'):
        delivery.validate(data)


def test_no_release_with_unfinished_gate():
    data = ledger()
    next(m for m in data['milestones'] if m['id'] == 'B02')['release_state'] = 'released'
    with pytest.raises(ValueError, match='release cannot bypass'):
        delivery.validate(data)


def test_unclaimed_in_progress_task_rejected():
    data = ledger()
    task = next(t for t in data['tasks'] if t['id'] == 'ES01-01')
    task['status'] = 'in_progress'
    # This test must stay valid after the real task has an owner.
    task['owner'] = None
    task['working_branch'] = None
    task['base_commit'] = None
    with pytest.raises(ValueError, match='needs owner'):
        delivery.validate(data)


def test_immutable_original_hash_is_checked():
    data = ledger()
    data['evidence']['EV-ORIGINAL']['git_blob_sha'] = '0' * 40
    with pytest.raises(ValueError, match='Immutable reference hash'):
        delivery.validate(data)


def test_blocked_items_never_render_as_checked():
    data = ledger()
    board = delivery.render(data)
    for task in data['tasks']:
        if task['status'] == 'blocked':
            assert f'- [ ] **{task["id"]} ' in board
            assert f'- [x] **{task["id"]} ' not in board


def test_optional_task_is_not_required_release_gate():
    data = ledger()
    assert next(t for t in data['tasks'] if t['id'] == 'ES03-03')['required'] is False
    assert next(t for t in data['tasks'] if t['id'] == 'B02-12')['required'] is True


def partition():
    return ledger()['repository']['roadmap_partition']


def test_seven_lane_order_and_bounded_task_selection():
    lanes = partition()['lanes']
    assert [lane['lane'] for lane in lanes] == [
        'events', 'identity', 'vault', 'collaboration', 'operations',
        'domain-packs', 'intelligence',
    ]
    assert [lane['task_ids'] for lane in lanes[:6]] == [
        ['ES02-01', 'ES02-02', 'ES02-03', 'ES02-04', 'B03-04'],
        ['B03-01'], ['B03-02'], ['B03-03'],
        ['B03-05', 'B10-01', 'B10-02', 'B03-06'],
        ['ES04-01', 'ES04-02', 'ES04-03', 'ES04-04', 'ES10-01', 'ES10-02'],
    ]
    assert lanes[-1]['task_ids'] == [
        'B02-09', 'B02-10', 'B02-11', 'B02-12', 'B02-14', 'B02-15',
        'B02-16', 'B02-18', 'B02-19', 'B02-20', 'B02-21', 'B02-22',
        'ES03-01', 'ES03-02', 'ES03-03', 'ES03-04', 'ES03-05',
        'ES03-07', 'ES03-08', 'B04-01', 'B04-02', 'B04-03', 'B04-04',
    ]
    assigned = [tid for lane in lanes for tid in lane['task_ids']]
    assert len(assigned) == len(set(assigned)) == 41
    assert not set(partition()['unassigned_optional_holds']) & set(assigned)


def test_lane_claims_have_exact_branch_owner_and_source_baseline():
    data = ledger()
    plan = data['repository']['roadmap_partition']
    tasks = {t['id']: t for t in data['tasks']}
    assert plan['source_base'] == 'baca8ad9efa531e5f172058845852963d7d5234a'
    assert len(plan['source_ledger_sha256']) == 64
    for lane in plan['lanes']:
        assert lane['branch'] == 'devin/1792969169-roadmap-' + lane['lane']
        assert lane['base_commit'] == plan['source_base']
        assert set(lane['task_ids']) == set(lane['task_modes'])
        for tid in lane['task_ids']:
            task = tasks[tid]
            assert task['owner'] == lane['owner']
            assert task['working_branch'] == lane['branch']
            assert task['base_commit'] == plan['source_base']
            assert task['next_action'].startswith('Coordination claim: ' + lane['lane'])
            assert 'Prior next action (still subject to this bounded claim): ' in task['next_action']


def test_optional_work_is_held_and_pilot_is_tooling_only():
    data = ledger()
    tasks = {t['id']: t for t in data['tasks']}
    for lane in partition()['lanes']:
        for tid, mode in lane['task_modes'].items():
            if not tasks[tid]['required']:
                assert mode == 'optional_hold_no_implementation'
            elif tid == 'B03-06':
                assert mode == 'fictional_pilot_tooling_only'
            else:
                assert mode == 'engineering_only'
    for tid in ('B03-07', 'ES02-06', 'ES03-08', 'B04-04'):
        assert tasks[tid]['required'] is False
        assert tasks[tid]['status'] != 'verified'


def test_emergence_ranges_are_twenty_ids_each_and_disjoint():
    plan = partition()
    assert plan['source_emergence_max'] == 112
    reserved = set()
    for index, lane in enumerate(plan['lanes']):
        start, end = [int(value[3:]) for value in lane['emergence_ids']]
        assert start == plan['source_emergence_max'] + 1 + index * 20
        assert end == start + 19
        assert not reserved & set(range(start, end + 1))
        reserved.update(range(start, end + 1))
        assert f'EM-{start}..EM-{end}' in lane['scope']
    assert len(reserved) == 140
    assert 253 not in reserved


def matches(path, patterns):
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def test_implementation_ownership_is_disjoint_with_shared_exclusions():
    plan = partition()
    lanes = plan['lanes']
    paths = set()
    for base in ('eightball', 'endstate', 'web', 'tests', 'docs', 'scripts', 'evals'):
        for parent, dirs, files in os.walk(ROOT / base):
            dirs[:] = [d for d in dirs if d not in ('__pycache__', 'node_modules', 'build')]
            paths.update((Path(parent) / f).relative_to(ROOT).as_posix() for f in files)
    # Include future paths represented by the reserved globs, not just today's files.
    for lane in lanes:
        for pattern in lane['owned_paths']:
            paths.add(pattern.replace('**', 'ownership/probe.py').replace('*', 'probe'))
    for path in paths:
        if matches(path, plan['integration_paths'] + plan['frozen_paths']):
            continue
        owners = [lane['lane'] for lane in lanes if matches(path, lane['owned_paths'])]
        assert len(owners) <= 1, (path, owners)
    for path in ('eightball/api.py', 'eightball/v2/api.py', 'eightball/v2/store.py',
                 'pyproject.toml', 'requirements-dev.txt', 'scripts/acceptance.py',
                 'web/v2/app.js', 'web/v2/index.html', 'docs/delivery/progress.json'):
        assert matches(path, plan['integration_paths'])
        assert not any(matches(path, lane['owned_paths']) for lane in lanes)
    for path in ('eightball/agency_access.py', 'eightball/authorisation.py',
                 'eightball/event_work.py', 'eightball/event_inbox.py',
                 'eightball/v2/event_api.py', 'eightball/event_workers/probe.py'):
        assert not matches(path, lanes[-1]['owned_paths'])


def test_lane_requirements_are_exact_ledger_text_not_a_second_status_board():
    text = (ROOT / 'docs/delivery/ROADMAP-LANES.md').read_text()
    tasks = {t['id']: t for t in ledger()['tasks']}
    for lane in partition()['lanes']:
        assert lane['branch'] in text
        for tid in lane['task_ids']:
            task = tasks[tid]
            heading = f'#### {tid} — {task["title"]}'
            assert text.count(heading) == 1
            section = text.split(heading, 1)[1].split('\n#### ', 1)[0]
            assert task['acceptance'] in section
            assert f'Required: `{str(task["required"]).lower()}`' in section
            assert all(blocker in section for blocker in task['blockers'])


def test_lane_local_delivery_fragments_have_unique_paths():
    paths = set()
    for lane in partition()['lanes']:
        for key in ('report_path', 'emergence_fragment_path', 'changelog_fragment_path'):
            path = lane[key]
            assert path.startswith('docs/delivery/lane-reports/' + lane['lane'])
            assert path in lane['owned_paths']
            assert path not in paths
            paths.add(path)
