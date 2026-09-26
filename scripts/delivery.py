#!/usr/bin/env python3
"""Validate the delivery ledger and deterministically render its checklist.

Standard library only. This checks documentation integrity, not application
behaviour, model quality, remote CI results or permission to merge/deploy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEDGER = Path('docs/delivery/progress.json')
BOARD = Path('docs/delivery/PROGRESS.md')
STATES = {'not_started', 'in_progress', 'implemented', 'partial', 'blocked', 'deferred', 'verified'}
TASK_KEYS = {'id', 'milestone', 'title', 'status', 'required', 'owner', 'working_branch', 'base_commit',
             'updated_on', 'code_paths', 'depends_on', 'acceptance', 'evidence', 'blockers', 'next_action'}


def unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def repository_file(root: Path, name: str) -> Path:
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError(f'Path must remain inside the repository: {name}')
    result = (root / relative).resolve()
    if not result.is_relative_to(root.resolve()) or not result.is_file():
        raise ValueError(f'Missing repository file: {name}')
    return result


def validate(data: dict[str, Any], root: Path = ROOT) -> None:
    if data.get('schema_version') != 1 or data.get('product') != '8BALL' or data.get('engine') != 'ENDSTATE':
        raise ValueError('Unsupported ledger schema or product/engine identity')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', data.get('updated_on', '')):
        raise ValueError('Ledger needs an ISO update date')
    milestones = data['milestones']
    mids = {m['id'] for m in milestones}
    if len(mids) != len(milestones):
        raise ValueError('Duplicate milestone ID')
    evidence = data['evidence']
    for eid, item in evidence.items():
        if not item.get('result') or not item.get('kind'):
            raise ValueError(f'Evidence {eid} needs its scope/result and kind')
        contents = repository_file(root, item['path']).read_bytes()
        if item.get('git_blob_sha'):
            actual = hashlib.sha1(b'blob ' + str(len(contents)).encode() + b'\0' + contents).hexdigest()
            if actual != item['git_blob_sha']:
                raise ValueError(f'Immutable reference hash differs: {eid}')
        if 'code_commit' in item and not re.fullmatch(r'[0-9a-f]{40}', item['code_commit']):
            raise ValueError(f'Evidence {eid} needs an exact code commit')
    tasks = data['tasks']
    by_id = {t['id']: t for t in tasks}
    if len(by_id) != len(tasks):
        raise ValueError('Duplicate task ID')
    for t in tasks:
        name = t['id']
        if set(t) != TASK_KEYS:
            raise ValueError(f'{name}: missing or unknown task fields')
        if not re.fullmatch(r'[A-Z][A-Z0-9]*-\d{2}', name) or t['milestone'] not in mids:
            raise ValueError(f'{name}: invalid task or milestone ID')
        if t['status'] not in STATES or type(t['required']) is not bool:
            raise ValueError(f'{name}: invalid status or required flag')
        if not t['acceptance'] or not t['next_action']:
            raise ValueError(f'{name}: needs acceptance criterion and next action')
        if any(e not in evidence for e in t['evidence']):
            raise ValueError(f'{name}: unknown evidence ID')
        if any(d not in by_id or d == name for d in t['depends_on']):
            raise ValueError(f'{name}: missing or self-referencing dependency')
        if t['status'] == 'verified':
            if not t['evidence'] or t['blockers']:
                raise ValueError(f'{name}: verified tasks need evidence and no unresolved blockers')
            if any(by_id[d]['status'] != 'verified' for d in t['depends_on']):
                raise ValueError(f'{name}: verified task has unverified prerequisites')
        if t['status'] == 'blocked' and not t['blockers']:
            raise ValueError(f'{name}: blocked task needs an explicit reason')
        if t['status'] == 'in_progress' and not all(t[k] for k in ('owner', 'working_branch', 'base_commit')):
            raise ValueError(f'{name}: active work needs owner, branch and base commit')
        if t['base_commit'] is not None and not re.fullmatch(r'[0-9a-f]{40}', t['base_commit']):
            raise ValueError(f'{name}: invalid base commit')
        for path in t['code_paths']:
            repository_file(root, path)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            raise ValueError(f'Delivery dependency cycle at {name}')
        if name in visited:
            return
        visiting.add(name)
        for dependency in by_id[name]['depends_on']:
            visit(dependency)
        visiting.remove(name)
        visited.add(name)

    for name in by_id:
        visit(name)
    if any(name not in by_id for name in data['next_task_ids']):
        raise ValueError('Unknown next task ID')
    for m in milestones:
        required = [t for t in tasks if t['milestone'] == m['id'] and t['required']]
        if not required:
            raise ValueError(f'{m["id"]}: milestone needs at least one required task')
        if m['release_state'] == 'released' and any(t['status'] != 'verified' for t in required):
            raise ValueError(f'{m["id"]}: release cannot bypass required acceptance tasks')


def render(data: dict[str, Any]) -> str:
    r = data['repository']
    lines = [
        '# Delivery checklist: 8BALL + ENDSTATE', '',
        '> Generated from `docs/delivery/progress.json`. Edit the ledger, then run '
        '`python scripts/delivery.py --write`. Do not maintain a second set of statuses here.', '',
        f'Last status review: {data["updated_on"]}.', '',
        '**8BALL is the fixer product. ENDSTATE is the reusable engine underneath it.**', '',
        '## Checkpoint and release boundary', '',
        f'- Active integration branch: `{r["development_branch"]}`; PR #{r["pull_request"]}.',
        f'- Inspected application baseline: `{r["inspected_code_commit"]}`.',
        '- This is a dated snapshot. Refresh the branch, PR and CI at the start of every session.',
        f'- At inspection: draft PR = `{str(r["pr_draft"]).lower()}`; merged = '
        f'`{str(r["merged"]).lower()}`; production deployed = `{str(r["production_deployed"]).lower()}`.',
        f'- Standalone ENDSTATE package released = `{str(r["standalone_endstate_package_released"]).lower()}`.', '',
        '## Checkbox meaning', '',
        '`[x] verified` means the specific acceptance scope has linked evidence. '
        '`[ ] implemented` means code exists without complete acceptance. `partial`, `blocked`, '
        '`in_progress`, `not_started` and `deferred` remain unchecked. A failed experiment can be '
        'recorded without passing its quality gate. Counts are not product-completion percentages.', '',
        'Built, verified, merged, packaged, deployed and commercially released are distinct. '
        'No model-quality claim follows from a software CI pass.', '',
        '## Next work', '',
    ]
    local = data.get('unpublished_checkpoint')
    if local:
        lines += ['**Unpublished development checkpoint:** ' + local['reason'],
                  'Base: `' + local['base_commit'] + '`. See `' + local['session'] + '`.', '']
    by_id = {t['id']: t for t in data['tasks']}
    for tid in data['next_task_ids']:
        t = by_id[tid]
        lines.append(f'- **{tid}: {t["title"]}**. {t["next_action"]}')
    lines += ['', '## Version summary', '',
              '| Track / milestone | Required subparts verified | Acceptance scope | Release |',
              '| --- | ---: | --- | --- |']
    for m in data['milestones']:
        required = [t for t in data['tasks'] if t['milestone'] == m['id'] and t['required']]
        done = sum(t['status'] == 'verified' for t in required)
        state = 'Scoped gate met' if done == len(required) else 'Not yet accepted'
        lines.append(f'| {m["track"]} {m["version"]}: {m["title"]} | {done}/{len(required)} | '
                     f'{state} | {m["release_state"].replace("_", " ")} |')
    for m in data['milestones']:
        lines += ['', f'## {m["track"]} {m["version"]}: {m["title"]}', '']
        for t in (t for t in data['tasks'] if t['milestone'] == m['id']):
            checked = 'x' if t['status'] == 'verified' else ' '
            optional = ' (optional, not a version gate)' if not t['required'] else ''
            lines += [f'- [{checked}] **{t["id"]} {t["title"]}**{optional}',
                      f'  - Status: `{t["status"]}`. Owner: {t["owner"] or "unassigned"}. '
                      f'Updated: {t["updated_on"]}.',
                      f'  - Acceptance: {t["acceptance"]}',
                      f'  - Next: {t["next_action"]}']
            if t['working_branch']:
                lines.append(f'  - Branch/base: `{t["working_branch"]}` / `{t["base_commit"]}`.')
            if t['depends_on']:
                lines.append('  - Dependencies: ' + ', '.join(f'`{d}`' for d in t['depends_on']) + '.')
            if t['code_paths']:
                lines.append('  - Existing code: ' + ', '.join(f'`{p}`' for p in t['code_paths']) + '.')
            if t['evidence']:
                lines.append('  - Evidence: ' + ', '.join(f'`{e}`' for e in t['evidence']) + ' (registry below).')
            if t['blockers']:
                lines.append('  - Blocker: ' + ' '.join(t['blockers']))
            lines.append('')
    lines += ['## Evidence registry', '',
              'These references have specific scopes and may be historical. A reference to a design '
              'or a failed model run is not a production acceptance result.', '']
    for eid, e in data['evidence'].items():
        lines += [f'### {eid}', '', f'- Kind: `{e["kind"]}`.',
                  f'- Repository evidence: [{e["path"]}](../../{e["path"]}).',
                  f'- Result/scope: {e["result"]}']
        if e.get('code_commit'):
            lines.append(f'- Code revision: `{e["code_commit"]}`.')
        if e.get('git_blob_sha'):
            lines.append(f'- Preserved Git blob: `{e["git_blob_sha"]}`.')
        if e.get('url'):
            lines.append(f'- External record: [verification source]({e["url"]}).')
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--write', action='store_true', help='Regenerate the readable checklist')
    group.add_argument('--check', action='store_true', help='Fail when the generated checklist is stale')
    args = parser.parse_args()
    try:
        data = json.loads((ROOT / LEDGER).read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
        validate(data)
        expected = render(data)
        if args.write:
            (ROOT / BOARD).write_text(expected, encoding='utf-8')
        elif not (ROOT / BOARD).exists() or (ROOT / BOARD).read_text(encoding='utf-8') != expected:
            raise ValueError('Checklist is stale. Run python scripts/delivery.py --write')
        print(f'Delivery ledger valid: {len(data["tasks"])} tasks, {len(data["milestones"])} milestones. '
              'Checklist current. This is not an application or release acceptance check.')
        return 0
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(1, f'Delivery documentation error: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
