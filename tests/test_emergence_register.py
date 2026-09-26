from copy import deepcopy
import importlib.util,json,subprocess
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('emergence_check',ROOT/'scripts/emergence.py');checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
def data():return json.loads((ROOT/checker.SOURCE).read_text())

def test_register_complete_valid_and_generated():
 d=data();checker.validate(d);assert checker.render(d)==(ROOT/checker.OUTPUT).read_text()
 assert len(d['items'])>=36
 assert {f'ER-{n:02d}' for n in range(1,11)} <= {p['id'] for p in d['required_prompts']}

def test_declined_and_deferred_are_retained_not_dropped():
 d=data();text=checker.render(d)
 for i in d['items']:
  assert i['id'] in text and i['observation'] in text
  if i['history'][-1]['decision']=='declined':assert '~~'+i['title']+'~~' in text

@pytest.mark.parametrize('mutation',[
 lambda d:d['items'].append(deepcopy(d['items'][0])),
 lambda d:d['items'][0].update(task_ids=['NO-99']),
 lambda d:d['items'][0].update(evidence_paths=['../../private']),
 lambda d:d['items'][0].update(history=[]),
 lambda d:d['items'][0].update(evidence_level='a hunch is a fact'),
 lambda d:d['items'][0].update(owner_review='assumed_yes'),
 lambda d:d['items'][0]['history'][0].update(reason=''),
 lambda d:d.update(required_prompts=[]),
])
def test_register_rejects_bad_data(mutation):
 d=data();mutation(d)
 with pytest.raises(ValueError):checker.validate(d)

def baseline(tmp):
 subprocess.run(['git','init','-q'],cwd=tmp,check=True)
 subprocess.run(['git','config','user.name','Test'],cwd=tmp,check=True);subprocess.run(['git','config','user.email','test@example.invalid'],cwd=tmp,check=True)
 p=tmp/checker.SOURCE;p.parent.mkdir(parents=True);d=data();p.write_text(json.dumps(d))
 subprocess.run(['git','add','.'],cwd=tmp,check=True);subprocess.run(['git','commit','-qm','start'],cwd=tmp,check=True)
 return d

@pytest.mark.parametrize('mutation',[
 lambda d:d['items'].pop(),lambda d:d['items'][0].update(observation='Rewrite the original'),
 lambda d:d['items'][0]['history'][0].update(reason='Hide the earlier rationale'),
 lambda d:d['items'][0].update(evidence_paths=[]),
])
def test_recorded_discovery_cannot_be_silently_removed_or_rewritten(tmp_path,mutation):
 d=baseline(tmp_path);mutation(d)
 with pytest.raises(ValueError):checker.check_base(d,'HEAD',tmp_path)

def test_owner_can_reopen_a_declined_idea_by_appending_not_erasing(tmp_path):
 d=baseline(tmp_path);item=next(i for i in d['items'] if i['history'][-1]['decision']=='declined')
 item['history'].append({'date':'2026-09-24','decision':'candidate','by':'Owner review fixture','reason':'Reconsider under a different implementation'})
 checker.check_base(d,'HEAD',tmp_path);assert len(item['history'])==2

def test_no_fake_completion_from_adoption_only():
 d=data();i=next(i for i in d['items'] if i['id']=='EM-022');text=checker.render(d)
 assert '### [ ] '+i['id'] in text  # product native/operator acceptance remains open

def test_prompts_and_rules_are_referenced_by_build_contracts():
 for path in ['AGENTS.md','docs/delivery/HANDOFF.md','docs/PRD.md','docs/ROADMAP.md']:
  text=(ROOT/path).read_text();assert 'EMERGENCE-REGISTER.md' in text and 'emergence.json' in text or 'progress.json' in text
 assert 'scripts/emergence.py --check --base' in (ROOT/'.github/workflows/ci.yml').read_text()

def test_changelog_links_registered_discoveries():
 d=data();log=json.loads((ROOT/'docs/delivery/changelog.json').read_text());ids=log['entries'][0]['emergence_review']['insight_ids']
 assert ids and set(ids)<={i['id'] for i in d['items']}

def test_complete_register_available_only_to_authenticated_operator(tmp_path):
 from fastapi.testclient import TestClient
 from eightball.api import make_app
 from eightball.store import Store
 client=TestClient(make_app(Store(str(tmp_path/'case.db')),'x'*32))
 assert client.get('/api/v2/build-discoveries').status_code==401
 r=client.get('/api/v2/build-discoveries',headers={'Authorization':'Bearer '+'x'*32}).json()
 assert r['items']==data()['items'] and r['task_states']['B02-21']!='verified'


def test_unknown_comparison_base_cannot_disable_history_guard(tmp_path):
 import subprocess
 subprocess.run(['git','init','-q'],cwd=tmp_path,check=True)
 with pytest.raises(subprocess.CalledProcessError):checker.check_base(data(),'missing-base-ref',tmp_path)


@pytest.mark.parametrize('mutation',[
 lambda d:d['required_prompts'].pop(0),
 lambda d:d['required_prompts'][0].update(text='Silently replace the original question'),
 lambda d:d['required_prompts'][0].update(scope='build'),
 lambda d:d['required_prompts'].reverse(),
])
def test_recorded_prompt_protocol_is_append_only(tmp_path,mutation):
 d=baseline(tmp_path);mutation(d)
 with pytest.raises(ValueError):checker.check_base(d,'HEAD',tmp_path)


def test_additional_review_pass_preserves_original_protocol(tmp_path):
 d=baseline(tmp_path)
 d['required_prompts'].append({'id':'ER-99','scope':'build','text':'Additional review pass fixture'})
 checker.check_base(d,'HEAD',tmp_path)
 checker.validate(d)


def test_original_review_pass_cannot_disappear_even_without_git_comparison():
 d=data();d['required_prompts']=[p for p in d['required_prompts'] if p['id']!='ER-01']
 with pytest.raises(ValueError,match='Original ten'):checker.validate(d)


def test_new_review_pass_requires_stable_identifier():
 d=data();d['required_prompts'].append({'id':'random','scope':'build','text':'Fixture'})
 with pytest.raises(ValueError,match='Invalid review prompt'):checker.validate(d)
