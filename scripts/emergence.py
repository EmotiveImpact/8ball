#!/usr/bin/env python3
"""Preserve every build discovery and render its owner-review register.
Task delivery states are read only from progress.json, never duplicated here.
"""
from __future__ import annotations
import argparse,json,re,subprocess
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE='docs/delivery/emergence.json'
OUTPUT='docs/delivery/EMERGENCE-REGISTER.md'
DECISIONS={'adopted','candidate','deferred','declined','superseded'}
EVIDENCE={'observed_in_build','supported_by_tests','operator_hypothesis','market_hypothesis'}
IMMUTABLE=('id','title','origin','first_seen','evidence_level','observation','product_implication')

def validate(data,root=ROOT):
 if data.get('schema_version')!=1 or not data.get('items'):raise ValueError('Emergence register is empty or version invalid')
 date.fromisoformat(data['updated_on']);ids=set()
 tasks={t['id']:t for t in json.loads((root/'docs/delivery/progress.json').read_text())['tasks']}
 for item in data['items']:
  if not re.fullmatch(r'EM-\d{3}',item['id']) or item['id'] in ids:raise ValueError('Invalid or duplicate insight ID')
  ids.add(item['id']);date.fromisoformat(item['first_seen'])
  if any(not isinstance(item[k],str) or not item[k].strip() for k in IMMUTABLE):raise ValueError('Missing original insight text')
  if item['evidence_level'] not in EVIDENCE or item['owner_review'] not in ('pending','reviewed_by_owner'):raise ValueError('Invalid evidence/review state')
  for key in ('task_ids','acceptance_task_ids'):
   if not isinstance(item[key],list) or len(set(item[key]))!=len(item[key]) or not set(item[key])<=tasks.keys():raise ValueError('Unknown or repeated roadmap links')
  if not set(item['acceptance_task_ids'])<=set(item['task_ids']):raise ValueError('Acceptance links must also be listed as roadmap links')
  if not item['evidence_paths']:raise ValueError('An insight needs its source or record, including hypotheses')
  for path in item['evidence_paths']:
   p=(root/path).resolve()
   if not p.is_relative_to(root.resolve()) or not p.is_file():raise ValueError('Missing or unsafe discovery evidence path')
  if not item['history']:raise ValueError('Insight needs a disposition and rationale')
  for h in item['history']:
   date.fromisoformat(h['date'])
   if h['decision'] not in DECISIONS or not h['reason'].strip() or not h['by'].strip():raise ValueError('Invalid discovery decision')
  if [h['date'] for h in item['history']]!=sorted(h['date'] for h in item['history']):raise ValueError('Discovery history must be chronological')
  if item['history'][-1]['decision']=='adopted' and not item['task_ids']:raise ValueError('Adoption needs explicit roadmap scope')
 if not data.get('required_prompts') or len({p['id'] for p in data['required_prompts']})!=len(data['required_prompts']):raise ValueError('Missing or duplicated review prompts')
 if not {f'ER-{n:02d}' for n in range(1,11)} <= {p['id'] for p in data['required_prompts']}:
  raise ValueError('Original ten review passes must remain present')
 for p in data['required_prompts']:
  if not re.fullmatch(r'ER-\d{2}',p['id']) or not p['text'].strip() or p['scope'] not in ('build','situation','both'):raise ValueError('Invalid review prompt')

def render(data,root=ROOT):
 tasks={t['id']:t for t in json.loads((root/'docs/delivery/progress.json').read_text())['tasks']}
 lines=['# Evolving emergence register: nothing silently discarded','',
  '> Generated from `docs/delivery/emergence.json`. Decision history lives there; delivery status comes only from `progress.json`. Run `python scripts/emergence.py --write`.','',
  '8BALL remains the fixer product. ENDSTATE supplies reusable calculations. This is the build-discovery register, not a client-case insight ledger.','',
  f'Last review: {data["updated_on"]}. **{len(data["items"])} recorded discoveries.**','',
  '**Read the marks correctly:** `[x]` requires the linked acceptance scope to be verified. `[ ]` means open, partial, implemented-but-unaccepted, or a candidate. Strikethrough means declined or superseded, not deleted. An owner can reopen any decision with a new history entry.','',
  '## Mandatory questions at sprint close','']
 for p in data['required_prompts']:lines += [f'- **{p["id"]} ({p["scope"]}):** {p["text"]}']
 lines += ['','## Complete owner-review register','']
 for i in data['items']:
  decision=i['history'][-1]['decision'];accepted=i['acceptance_task_ids']
  done=bool(accepted) and decision=='adopted' and all(tasks[t]['status']=='verified' for t in accepted)
  title='~~'+i['title']+'~~' if decision in ('declined','superseded') else i['title']
  lines += [f'### [{"x" if done else " "}] {i["id"]}: {title}','',
   f'**Disposition:** {decision}. **Owner review:** {i["owner_review"]}. **Original evidence level:** {i["evidence_level"]}.',
   f'**First recorded:** {i["first_seen"]}. **Origin:** {i["origin"]}.','',i['observation'],'',
   '**Product implication:** '+i['product_implication'],'',
   '**Roadmap links:** '+(', '.join('`'+t+'` ('+tasks[t]['status']+')' for t in i['task_ids']) or 'Candidate only; no delivery commitment')+'.',
   '**Completion scope:** '+(', '.join('`'+t+'`' for t in accepted) or 'No scoped completion gate yet; do not tick this idea off')+'.',
   '**Evidence / source record:** '+', '.join('`'+p+'`' for p in i['evidence_paths'])+'.','', '**Decision history:**','']
  lines += [f'- {h["date"]} · {h["decision"]} · {h["by"]}: {h["reason"]}' for h in i['history']]
  lines += ['']
 return '\n'.join(lines).rstrip()+'\n'

def check_base(data,base,root=ROOT):
 if not re.fullmatch(r'[a-zA-Z0-9_./^-]{1,150}',base) or base.startswith('-'):raise ValueError('Invalid base reference')
 commit=subprocess.check_output(['git','rev-parse','--verify',base+'^{commit}'],cwd=root,text=True,stderr=subprocess.PIPE).strip()
 names=subprocess.check_output(['git','ls-tree','--name-only',commit,'--',SOURCE],cwd=root,text=True)
 if not names.strip():return
 old=json.loads(subprocess.check_output(['git','show',base+':'+SOURCE],cwd=root,text=True))
 original_prompts=old.get('required_prompts',[])
 if data['required_prompts'][:len(original_prompts)]!=original_prompts:
  raise ValueError('Recorded review prompts cannot be removed, reordered or rewritten; append a new pass')
 by_id={i['id']:i for i in data['items']}
 for before in old['items']:
  after=by_id.get(before['id'])
  if after is None:raise ValueError('A recorded discovery cannot be removed')
  if any(before[k]!=after[k] for k in IMMUTABLE):raise ValueError('Original discovery text is immutable; add a linked correction')
  if after['history'][:len(before['history'])]!=before['history']:raise ValueError('Discovery decision history cannot be rewritten')
  if not set(before['evidence_paths'])<=set(after['evidence_paths']):raise ValueError('Prior evidence cannot be silently removed')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--base');a=p.parse_args()
 try:
  data=json.loads((ROOT/SOURCE).read_text());validate(data);text=render(data)
  if a.base:check_base(data,a.base)
  if a.write:(ROOT/OUTPUT).write_text(text)
  elif (ROOT/OUTPUT).read_text()!=text:raise ValueError('Emergence register is stale. Run --write')
  print(f'Emergence register validated: {len(data["items"])} discoveries retained; no completion claim follows from a candidate.')
 except (ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as e:p.exit(1,str(e)+'\n')
if __name__=='__main__':main()
