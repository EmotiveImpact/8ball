"""Checks for progress-document integrity, not application acceptance."""
import importlib.util
import json
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
