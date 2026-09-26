"""Generate the product changelog and enforce an entry for changed builds.

Canonical entries: docs/delivery/changelog.json. Task status remains exclusively
in progress.json. --base checks a Git comparison without rewriting Git history.
"""
from __future__ import annotations
import argparse
from datetime import date
import json
import hashlib
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCE='docs/delivery/changelog.json'
OUTPUT='CHANGELOG.md'

# Exact imported history predates the mandatory review/register policies.
# No timestamp/ID prefix exemption: only these unchanged entry contents qualify.
LEGACY_POLICY_EXCEPTIONS = {'2026-09-24-emergence-review': '2be94830d0942a6c3bda2f29d151b4874a15994691082f0cf6a0a2ea5cd1401d', '2026-09-24-source-desk': 'a7c1cb01bd73e8d67a8787bfd686f760e5dccc3f2acd8d1170f8d37d84b59137', '2026-09-23-plan-studio': '734324d9b2130b7c8313c13bae7ed327892781627a4f32551fbc5a33eb7ccc51', '2026-09-23-connections': '1534de45446c2995740f97cc247c94ddd4dda5894cb451aa877eb6796862c95f', '2026-09-23-hosted-black': '8f40af75831ee3cec7108cb7d69a261babbd37f566e42bb239c7427f0333769e'}

def legacy_policy_entry(entry):
    fingerprint=hashlib.sha256(json.dumps(entry,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    return LEGACY_POLICY_EXCEPTIONS.get(entry['id'])==fingerprint


def validate(data,root=ROOT):
    if data.get('schema_version')!=1 or not data.get('entries'):raise ValueError('Missing changelog entries')
    ids=set()
    task_ids={t['id'] for t in json.loads((root/'docs/delivery/progress.json').read_text())['tasks']}
    dates=[]
    for e in data['entries']:
        if not re.fullmatch(r'[a-z0-9-]{4,100}',e['id']) or e['id'] in ids:raise ValueError('Invalid or repeated changelog ID')
        ids.add(e['id']);dates.append(date.fromisoformat(e['date']))
        for name in ('version','title','summary','delivery'):
            if not isinstance(e[name],str) or not e[name].strip():raise ValueError('Missing changelog '+name)
        if e['delivery'] not in ('local_unreleased','pushed_unreleased','released'):raise ValueError('Unknown delivery state')
        for name in ('added','changed','fixed','verification','limitations','task_ids','evidence_paths'):
            if not isinstance(e[name],list) or any(not isinstance(x,str) or not x.strip() for x in e[name]):raise ValueError('Invalid changelog '+name)
        if not (e['added'] or e['changed'] or e['fixed']):raise ValueError('Entry has no changes')
        if not e['verification'] or not e['limitations'] or not e['evidence_paths']:raise ValueError('Entry needs evidence and limitations')
        if not set(e['task_ids'])<=task_ids:raise ValueError('Unknown task in changelog')
        review=e.get('emergence_review')
        if review is not None:
            if not isinstance(review,dict) or not {'discoveries','risks','architecture_implications','roadmap_decision'}<=set(review) or set(review)-{'discoveries','risks','architecture_implications','roadmap_decision','insight_ids'}:
                raise ValueError('Invalid emergence review')
            for name in ('discoveries','risks','architecture_implications'):
                if not isinstance(review[name],list) or any(not isinstance(x,str) or not x.strip() for x in review[name]):
                    raise ValueError('Invalid emergence review '+name)
            if not isinstance(review['roadmap_decision'],str) or not review['roadmap_decision'].strip():
                raise ValueError('Invalid emergence review roadmap decision')
        if review is not None and 'insight_ids' in review:
            if not isinstance(review['insight_ids'],list) or any(not re.fullmatch(r'EM-\d{3}',i) for i in review['insight_ids']):raise ValueError('Invalid registered insight IDs')
            registry=json.loads((root/'docs/delivery/emergence.json').read_text())
            if not set(review['insight_ids'])<={i['id'] for i in registry['items']}:raise ValueError('Unknown registered insight ID')
        for path in e['evidence_paths']:
            resolved=(root/path).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():raise ValueError('Missing changelog evidence: '+path)
    if dates!=sorted(dates,reverse=True):raise ValueError('Changelog must be newest first')


def render(data):
    lines=['# 8BALL + ENDSTATE changelog','',
           '> Generated from `docs/delivery/changelog.json`. Update that source, then run `python scripts/changelog.py --write`. The in-app What’s new page reads the same entries.',
           '', 'This is product history, not the case decision trail. A build entry is not evidence of a merge, deployment or production-model approval.','']
    for e in data['entries']:
        lines += [f'## {e["version"]} · {e["title"]}', '', f'{e["date"]} · `{e["delivery"]}`', '', e['summary'],'']
        for key in ('added','changed','fixed','verification','limitations'):
            if e[key]:lines += [f'### {key.title()}','',*[f'- {s}' for s in e[key]],'']
        review=e.get('emergence_review')
        if review:
            lines += ['### Emergence review','',
                      '**What did this sprint reveal that we had not properly seen before?**','',
                      *[f'- Discovery: {s}' for s in review['discoveries']],
                      *[f'- Risk: {s}' for s in review['risks']],
                      *[f'- Architecture: {s}' for s in review['architecture_implications']],
                      f'- Roadmap decision: {review["roadmap_decision"]}',
                      *(['Registered discoveries: '+(', '.join(review['insight_ids']) or 'none identified')+'.'] if 'insight_ids' in review else []),'']
        lines += ['Roadmap items: '+', '.join('`'+x+'`' for x in e['task_ids'])+'.','',
                  'Evidence: '+', '.join(f'[{p}]({p})' for p in e['evidence_paths'])+'.','']
    return '\n'.join(lines).rstrip()+'\n'


def check_base(data,base,root=ROOT):
    if base.startswith('-') or not re.fullmatch(r'[a-zA-Z0-9_./^-]{1,150}',base):raise ValueError('Invalid comparison reference')
    proc=subprocess.run(['git','diff','--name-only',base,'--'],cwd=root,text=True,capture_output=True,check=True)
    paths=set(proc.stdout.splitlines())
    # Include newly created files in local worktrees, not only tracked edits.
    proc=subprocess.run(['git','ls-files','--others','--exclude-standard'],cwd=root,text=True,capture_output=True,check=True)
    paths.update(proc.stdout.splitlines())
    if not paths:return
    previous=subprocess.run(['git','show',base+':'+SOURCE],cwd=root,text=True,capture_output=True)
    old=json.loads(previous.stdout)['entries'] if previous.returncode==0 else []
    current={e['id']:e for e in data['entries']}
    if any(current.get(e['id'])!=e for e in old):raise ValueError('Historical changelog entries cannot be removed or rewritten; add a correction entry')
    new_ids=current.keys()-{e['id'] for e in old}
    if not new_ids:raise ValueError('Changed build needs a new changelog entry')
    for eid in new_ids:
        if legacy_policy_entry(current[eid]):continue
        if not current[eid].get('emergence_review'):
            raise ValueError('New changelog entry needs an emergence review')
        # Historical entries predate the complete register; all new sprint entries link it.
        if 'insight_ids' not in current[eid]['emergence_review']:
            raise ValueError('New emergence review needs registered insight_ids (an empty list is allowed when no finding was identified)')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--base')
    args=p.parse_args()
    try:
        data=json.loads((ROOT/SOURCE).read_text());validate(data)
        text=render(data)
        if args.write:(ROOT/OUTPUT).write_text(text)
        elif not (ROOT/OUTPUT).exists() or (ROOT/OUTPUT).read_text()!=text:raise ValueError('CHANGELOG.md is stale. Run python scripts/changelog.py --write')
        if args.base:check_base(data,args.base)
        print(f'Changelog valid: {len(data["entries"])} entries. No release is implied.')
    except (ValueError,KeyError,OSError,subprocess.CalledProcessError) as e:p.exit(1,'Changelog error: '+str(e)+'\n')
if __name__=='__main__':main()
