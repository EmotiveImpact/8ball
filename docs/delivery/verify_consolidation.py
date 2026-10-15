"""Offline, documentation-only preservation check for the consolidated handoff."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = '290e310707cf8bef6caf2508c285312b091bd18b'
LINK_DOCS = [
    'START-HERE.md', 'docs/strategy/ENDSTATE-VISION-ADDENDUM.md',
    'docs/strategy/ROADMAP-INTEGRATION.md', 'docs/architecture/ENDSTATE-SYSTEM.md',
    'docs/research/ENDSTATE-REGISTER.md', 'docs/research/ENDSTATE-EXPERIMENTS.md',
    'docs/decisions/0005-research-consolidation.md', 'docs/delivery/V02-CLOSEOUT.md',
    'docs/delivery/NEXT-AGENT-PROMPT.md',
    'docs/delivery/sessions/2026-10-15-documentation-consolidation.md',
]

def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=ROOT)

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default=BASE)
    args = parser.parse_args()
    require(bool(re.fullmatch(r'[0-9a-f]{40}', args.base)), 'Use an exact base commit SHA')
    m = json.loads((ROOT / 'docs/delivery/context-manifest.json').read_text())
    require(args.base == m['application_base_commit'], 'Wrong consolidation base')
    protected = m['preserved_exactly']
    for entry in protected:
        p = ROOT / entry['path']
        require(sha(p) == entry['sha256'], f'Protected file changed: {entry["path"]}')
        require(p.read_bytes() == git('show', f'{args.base}:{entry["path"]}'), f'Base mismatch: {entry["path"]}')
    for path in ['docs/PRD.md', 'docs/ROADMAP.md', 'AGENTS.md', 'docs/delivery/HANDOFF.md']:
        require((ROOT / path).read_bytes().startswith(git('show', f'{args.base}:{path}')), f'Not append-only: {path}')
    require((ROOT / 'README.md').read_bytes().endswith(git('show', f'{args.base}:README.md')), 'Original README lost')
    old_changelog = json.loads(git('show', f'{args.base}:docs/delivery/changelog.json'))['entries']
    current = json.loads((ROOT / 'docs/delivery/changelog.json').read_text())['entries']
    now = {x['id']: x for x in current}
    for x in old_changelog:
        require(now.get(x['id']) == x, f'Historical changelog changed: {x["id"]}')
    old_e = json.loads(git('show', f'{args.base}:docs/delivery/emergence.json'))
    e = json.loads((ROOT / 'docs/delivery/emergence.json').read_text())
    require(e['items'][:len(old_e['items'])] == old_e['items'], 'Prior discoveries changed')
    require(e['required_prompts'] == old_e['required_prompts'], 'Review prompts changed')
    for entry in m['research_archive']['files']:
        p = ROOT / entry['path']
        require(p.is_file() and sha(p) == entry['sha256'], f'Research changed: {p}')
    archive_dir = ROOT / 'docs/reference/endstate-handoff-2026-09-24'
    members = [p for p in archive_dir.rglob('*') if p.is_file()]
    require(len(members) == m['research_archive']['file_count'] == 19, 'Archive membership mismatch')
    entries = re.findall(r'- `([^`]+)` - SHA-256 `([0-9a-f]{64})`', (archive_dir / 'MANIFEST.md').read_text())
    require(len(entries) == 18, 'Expected 18 manifest payloads')
    for path, expected in entries:
        p = (archive_dir / path).resolve()
        require(p.is_relative_to(archive_dir.resolve()), 'Archive path escapes')
        require(sha(p) == expected, f'Original manifest mismatch: {path}')
    q = m['qwen_baseline']
    require(sha(ROOT / q['path']) == q['sha256'], 'Model evidence bytes changed')
    model = json.loads((ROOT / q['path']).read_text())
    require(model['schema_valid'] == 3 and model['total'] == 4, 'Model result mismatch')
    require(model['semantic_accuracy_evaluated'] is False and model['production_approved'] is False, 'False model claim')
    link_count = 0
    for name in LINK_DOCS:
        p = ROOT / name
        require(p.is_file(), f'Missing entry document: {name}')
        for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)', p.read_text()):
            if '://' in target or target.startswith(('#', 'mailto:')):
                continue
            local = target.split('#')[0]
            resolved = (p.parent / local).resolve()
            require(resolved.is_relative_to(ROOT.resolve()) and resolved.exists(), f'Broken link {name}: {target}')
            link_count += 1
    changed = set(git('diff', '--name-only', args.base, '--').decode().splitlines())
    changed.update(git('ls-files', '--others', '--exclude-standard').decode().splitlines())
    for name in changed:
        require(name.startswith('docs/') or name in {'START-HERE.md', 'README.md', 'AGENTS.md', 'CHANGELOG.md'}, f'Out-of-scope runtime/config change: {name}')
    # Check contents and Git file modes for every originally tracked non-document path.
    for record in git('ls-tree', '-r', args.base).decode().splitlines():
        meta, name = record.split('\t', 1)
        if name.startswith('docs/') or name in {'README.md', 'AGENTS.md', 'CHANGELOG.md'}:
            continue
        mode, kind, blob = meta.split()
        require(kind == 'blob', f'Unexpected base object: {name}')
        p = ROOT / name
        require(p.is_file() and p.read_bytes() == git('show', f'{args.base}:{name}'), f'Runtime changed: {name}')
        mode_now = '100755' if p.stat().st_mode & 0o111 else '100644'
        require(mode_now == mode, f'File mode changed: {name}')
    print(json.dumps({'status': 'passed', 'scope': 'documentation preservation and relative-link verification',
                      'base': args.base, 'protected_files': len(protected), 'original_research_files': len(members),
                      'manifest_payloads_checked': len(entries), 'prior_discoveries_preserved': len(old_e['items']),
                      'current_discoveries': len(e['items']), 'relative_links_checked': link_count,
                      'changed_paths': len(changed), 'runtime_unchanged': True, 'progress_unchanged': True,
                      'model_calls': 0, 'native_browser_run': False}, indent=2))
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print(f'Consolidation verification failed: {exc}', file=sys.stderr)
        raise SystemExit(1)
