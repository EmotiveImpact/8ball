"""Hosted evaluation opt-in/report checks; no inference or client database."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from evals import full_journey, live_huggingface
from eightball.v2.hosted import HostedFailure

ROOT = Path(__file__).resolve().parents[1]
KEY = 'fictional-private-key-for-cli-test'


def configure(monkeypatch):
    monkeypatch.setenv('EIGHTBALL_API_BASE_URL', 'https://api.example.com/v1')
    monkeypatch.setenv('EIGHTBALL_API_MODEL', 'qwen-fixture')
    monkeypatch.setenv('EIGHTBALL_API_PROVIDER', 'fixture-provider')
    monkeypatch.setenv('EIGHTBALL_API_KEY', KEY)
    monkeypatch.delenv('EIGHTBALL_API_ROUTING_PROVIDER', raising=False)


@pytest.mark.parametrize('flags', [[], ['--allow-hosted']])
def test_compatible_cli_blocks_without_opt_in_or_configuration(tmp_path, flags):
    env = {k: v for k, v in os.environ.items() if not k.startswith('EIGHTBALL_API_')}
    output = tmp_path / 'not-created'
    result = subprocess.run([sys.executable, str(ROOT / 'evals/live_compatible.py'),
                             *flags, '--output', str(output)], cwd=ROOT, env=env,
                            text=True, capture_output=True, timeout=15)
    assert result.returncode == 2
    assert not output.exists()
    assert 'No hosted request was made' in result.stderr or '--allow-hosted is required' in result.stderr


def test_compatible_journey_preflight_is_local_and_requires_both_permissions(monkeypatch):
    configure(monkeypatch)
    with pytest.raises(full_journey.SetupBlocked, match='allow-inference'):
        full_journey.preflight('openai_compatible')
    with pytest.raises(full_journey.SetupBlocked, match='allow-external'):
        full_journey.preflight('openai_compatible', True, False)
    result = full_journey.preflight('openai_compatible', True, True)
    assert result['credentials'] == 'configured_not_authenticated'
    assert result['model'] == 'qwen-fixture' and result['endpoint_host'] == 'api.example.com'
    assert KEY not in json.dumps(result)


def test_compatible_eval_preserves_all_frozen_rejections_without_fallback(tmp_path, monkeypatch):
    configure(monkeypatch)
    calls = []

    def rejected(case, provider, purpose, sources, *, allow_external):
        calls.append((case.title, case.desired_outcome, provider, purpose, sources, allow_external))
        failure = HostedFailure('controlled_fixture_rejection')
        failure.trace = {'failed': True, 'diagnostic': {'code': failure.code},
                         'transport': {'transport': 'openai_compatible', 'calls': []}}
        raise failure

    monkeypatch.setattr(live_huggingface, 'propose', rejected)
    result = live_huggingface.main(['--allow-hosted', '--output', str(tmp_path)],
                                   default_provider='openai_compatible')
    reports = list(tmp_path.glob('*/compatible-report.json'))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text())
    frozen = json.loads((ROOT / 'evals/generation-cases.json').read_text())
    assert result == 1 and not report['structural_gate_passed']
    assert report['fixture_sha256'] == live_huggingface.FIXTURES_SHA256
    assert [x[0] for x in calls] == [x[0] for x in frozen]
    assert [x[1] for x in calls] == [x[3] for x in frozen]
    assert all(x[2] == 'openai_compatible' and x[5] is True for x in calls)
    assert len(report['results']) == report['planned_fixtures'] == report['completed_fixtures'] == 4
    assert report['all_live_states_unchanged'] and not report['actual_hosted_requests']
    assert not report['production_approved'] and not report['independent_semantic_benchmark']
    assert all(r['status'] == 'rejected_or_unavailable' and
               r['trace']['diagnostic']['code'] == 'controlled_fixture_rejection'
               for r in report['results'])
    assert KEY not in json.dumps(report)
