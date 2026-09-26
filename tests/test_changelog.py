from pathlib import Path
from copy import deepcopy
import importlib.util,json,subprocess
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('changelog_checks',ROOT/'scripts/changelog.py');checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)

def data():return json.loads((ROOT/checks.SOURCE).read_text())

def test_changelog_is_valid_and_generated():
    d=data();checks.validate(d);assert checks.render(d)==(ROOT/checks.OUTPUT).read_text()

@pytest.mark.parametrize('mutation',[
 lambda d:d['entries'].append(d['entries'][0]),
 lambda d:d['entries'][0].update(verification=[]),
 lambda d:d['entries'][0].update(limitations=[]),
 lambda d:d['entries'][0].update(evidence_paths=['../../outside']),
 lambda d:d['entries'][0].update(task_ids=['UNKNOWN-01']),
 lambda d:d['entries'][0].update(delivery='production maybe'),
 lambda d:d['entries'][0].update(date='not a date'),
 lambda d:d['entries'][0].update(added=[],changed=[],fixed=[]),
])
def test_bad_changelog_rejected(mutation):
    d=data();mutation(d)
    with pytest.raises(ValueError):checks.validate(d)


def make_git(tmp):
    subprocess.run(['git','init','-q'],cwd=tmp,check=True)
    subprocess.run(['git','config','user.name','Test'],cwd=tmp,check=True);subprocess.run(['git','config','user.email','test@example.invalid'],cwd=tmp,check=True)
    path=tmp/checks.SOURCE;path.parent.mkdir(parents=True);d=data();path.write_text(json.dumps(d))
    subprocess.run(['git','add','.'],cwd=tmp,check=True);subprocess.run(['git','commit','-qm','baseline'],cwd=tmp,check=True)
    (tmp/'code.py').write_text('x=1')
    return d


def test_changed_build_requires_new_entry(tmp_path):
    d=make_git(tmp_path)
    with pytest.raises(ValueError,match='new changelog'):checks.check_base(d,'HEAD',tmp_path)
    d['entries'].insert(0,{**d['entries'][0],'id':'another-build'})
    checks.check_base(d,'HEAD',tmp_path)

def test_new_build_requires_emergence_review(tmp_path):
    d=make_git(tmp_path)
    entry={**d['entries'][0],'id':'missing-emergence'}
    entry.pop('emergence_review',None)
    d['entries'].insert(0,entry)
    with pytest.raises(ValueError,match='emergence review'):checks.check_base(d,'HEAD',tmp_path)


def test_history_cannot_be_rewritten_even_with_new_entry(tmp_path):
    d=make_git(tmp_path);d['entries'].insert(0,{**d['entries'][0],'id':'another-build'})
    d['entries'][1]['summary']='rewritten'
    with pytest.raises(ValueError,match='Historical'):checks.check_base(d,'HEAD',tmp_path)


def test_changelog_api_is_authenticated_and_same_source(tmp_path):
    from eightball.api import make_app
    from eightball.store import Store
    from fastapi.testclient import TestClient
    cl=TestClient(make_app(Store(str(tmp_path/'a.db')),'x'*32))
    assert cl.get('/api/v2/changelog').status_code==401
    cl.headers['Authorization']='Bearer '+'x'*32
    assert cl.get('/api/v2/changelog').json()==data()


def test_agent_instruction_and_handoff_require_changelog():
    for file in ['AGENTS.md','docs/delivery/HANDOFF.md']:
        t=(ROOT/file).read_text();assert 'changelog.json' in t and 'scripts/changelog.py --check --base' in t

def test_agent_instruction_and_handoff_require_emergence_review():
    guide=(ROOT/'docs/delivery/EMERGENCE-REVIEW.md')
    assert guide.is_file()
    for file in ['AGENTS.md','docs/delivery/HANDOFF.md','docs/PRD.md','docs/ROADMAP.md']:
        t=(ROOT/file).read_text()
        assert 'EMERGENCE-REVIEW.md' in t or 'emergence review' in t.lower()
    handoff=(ROOT/'docs/delivery/HANDOFF.md').read_text()
    assert 'What did this sprint reveal that we had not properly seen' in handoff


def test_ci_enforces_changelog():
    text=(ROOT/'.github/workflows/ci.yml').read_text()
    assert 'scripts/changelog.py --check --base' in text and 'CHANGELOG_BASE' in text


def make_pre_changelog_base(tmp):
 subprocess.run(['git','init','-q'],cwd=tmp,check=True)
 subprocess.run(['git','config','user.name','Test'],cwd=tmp,check=True)
 subprocess.run(['git','config','user.email','test@example.invalid'],cwd=tmp,check=True)
 (tmp/'README.md').write_text('Original foundation')
 subprocess.run(['git','add','.'],cwd=tmp,check=True)
 subprocess.run(['git','commit','-qm','Before changelog policies'],cwd=tmp,check=True)
 (tmp/'new.py').write_text('x=1')

def test_cumulative_integration_preserves_exact_pre_policy_history(tmp_path):
 make_pre_changelog_base(tmp_path)
 checks.check_base(data(),'HEAD',tmp_path)

def test_new_entry_cannot_backdate_its_way_around_review(tmp_path):
 make_pre_changelog_base(tmp_path);d=data()
 e={**d['entries'][-1],'id':'2026-01-01-backdated-build'}
 e.pop('emergence_review',None);d['entries'].append(e)
 with pytest.raises(ValueError,match='emergence review'):checks.check_base(d,'HEAD',tmp_path)

def test_historical_policy_exception_is_content_bound(tmp_path):
 make_pre_changelog_base(tmp_path);d=data()
 d['entries'][-1]['summary']='Changed historical claim'
 with pytest.raises(ValueError,match='emergence review'):checks.check_base(d,'HEAD',tmp_path)

def test_exact_historical_exception_set_has_not_expanded():
 assert len(checks.LEGACY_POLICY_EXCEPTIONS)==5
 originals={e['id']:e for e in data()['entries'] if e['id'] in checks.LEGACY_POLICY_EXCEPTIONS}
 assert set(originals)==set(checks.LEGACY_POLICY_EXCEPTIONS)
 assert all(checks.legacy_policy_entry(e) for e in originals.values())

def test_future_review_must_link_full_register(tmp_path):
 d=make_git(tmp_path);entry={**d['entries'][0],'id':'new-missing-register','emergence_review':dict(d['entries'][0]['emergence_review'])}
 entry['emergence_review'].pop('insight_ids',None);d['entries'].insert(0,entry)
 with pytest.raises(ValueError,match='registered insight_ids'):checks.check_base(d,'HEAD',tmp_path)
