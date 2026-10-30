from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest

from eightball.operations.readiness import (CAPABILITIES, Evidence, ReadinessManifest,
                                            evaluate_readiness)

NOW = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)
COMMIT = 'a' * 40


def evidence(tmp_path, **kwargs):
    artifact = tmp_path / 'receipt.json'
    artifact.write_text('{"fictional":true}')
    values = dict(id='fictional-evidence', capability='security', environment='linux-chromium',
                  kind='software', status='passed', path=artifact.name,
                  sha256=sha256(artifact.read_bytes()).hexdigest(), source_commit=COMMIT, recorded_at=NOW)
    values.update(kwargs)
    return Evidence(**values)


def evaluate(tmp_path, entries=(), **kwargs):
    manifest = ReadinessManifest(source_commit=COMMIT, environments=('linux-chromium',),
                                 evidence=tuple(entries))
    return evaluate_readiness(manifest, root=tmp_path, now=NOW, **kwargs)


def test_empty_readiness_has_exact_missing_human_and_software_gates(tmp_path):
    report = evaluate(tmp_path)
    assert report['status'] == 'blocked'
    assert len(report['gaps']) == sum(len(kinds) for kinds in CAPABILITIES.values())
    assert not report['release_authorized'] and not report['deployment_authorized']
    assert not report['human_decisions_authenticated'] and not report['real_pilot_authorized']


@pytest.mark.parametrize('change,reason', [
    ({'path': '../outside'}, 'unsafe_path'), ({'path': '/etc/passwd'}, 'unsafe_path'),
    ({'path': 'absent'}, 'missing_artifact'), ({'sha256': 'b' * 64}, 'artifact_digest_mismatch'),
    ({'source_commit': 'b' * 40}, 'source_mismatch'),
    ({'recorded_at': NOW - timedelta(days=31)}, 'stale_or_future_evidence'),
    ({'recorded_at': NOW + timedelta(seconds=1)}, 'stale_or_future_evidence'),
    ({'recorded_at': NOW.replace(tzinfo=None)}, 'unknown_timestamp'),
    ({'status': 'failed'}, 'not_passed'), ({'status': 'blocked'}, 'not_passed'),
    ({'status': 'unknown'}, 'not_passed')])
def test_missing_tampered_stale_failed_unknown_never_counts_as_pass(tmp_path, change, reason):
    report = evaluate(tmp_path, [evidence(tmp_path, **change)])
    assert report['status'] == 'blocked'
    assert report['evidence'][0]['reason'] == reason


def test_symlink_outside_explicit_root_refused(tmp_path):
    outside = tmp_path.parent / 'private-other-receipt'
    outside.write_text('not approved')
    (tmp_path / 'link').symlink_to(outside)
    report = evaluate(tmp_path, [evidence(tmp_path, path='link')])
    assert report['evidence'][0]['reason'] == 'unsafe_path'


def test_software_pass_cannot_substitute_independent_human_or_other_environment(tmp_path):
    report = evaluate(tmp_path, [evidence(tmp_path)])
    assert {'environment': 'linux-chromium', 'capability': 'security', 'kind': 'independent'} in report['gaps']
    entry = evidence(tmp_path, environment='windows-firefox')
    report = evaluate(tmp_path, [entry])
    assert {'environment': 'linux-chromium', 'capability': 'security', 'kind': 'software'} in report['gaps']


def test_all_supplied_claims_still_need_authentication_and_release_decision(tmp_path):
    entries = [evidence(tmp_path, id=f'fictional-{capability}-{kind}', capability=capability, kind=kind)
               for capability, kinds in CAPABILITIES.items() for kind in kinds]
    report = evaluate(tmp_path, entries)
    assert report['gaps'] == []
    assert report['status'] == 'evidence_supplied_pending_authentication'
    assert not report['release_authorized'] and not report['human_decisions_authenticated']
    assert all(not e['authenticity_verified'] for e in report['evidence'])


def test_duplicate_ids_do_not_inflate_coverage(tmp_path):
    entry = evidence(tmp_path)
    with pytest.raises(ValueError, match='unique'):
        evaluate(tmp_path, [entry, entry])


def test_readiness_cli_blocks_without_evidence_and_sanitizes_invalid_input(tmp_path):
    path = tmp_path / 'manifest.json'
    path.write_text(json.dumps({'source_commit': COMMIT, 'environments': ['linux-chromium'], 'evidence': []}))
    cmd = [sys.executable, str(Path(__file__).resolve().parents[1] / 'scripts/operations/check.py'), 'readiness', str(path), '--root', str(tmp_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 1
    assert json.loads(result.stdout)['status'] == 'blocked'
    path.write_text('fictional-private-input-invalid')
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 2
    assert 'fictional-private' not in result.stdout + result.stderr
