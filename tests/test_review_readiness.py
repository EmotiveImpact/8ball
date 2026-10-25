"""Prospective recording checks cannot manufacture a professional acceptance."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys

import pytest

from evals import review_readiness as rr

ROOT = Path(__file__).resolve().parents[1]
FORMS = ROOT / 'docs/delivery/review'
AS_OF = datetime(2026, 10, 18, 12, tzinfo=timezone.utc)


def write_json(path, value):
    raw = (json.dumps(value, indent=2, allow_nan=False) + '\n').encode()
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def artifact(root, name, content):
    raw = content.encode()
    (root / name).write_bytes(raw)
    return {'ref': name, 'sha256': hashlib.sha256(raw).hexdigest()}


@pytest.fixture
def bundle(tmp_path):
    """Fictional recording claims and thresholds, never a real approved study."""
    protocol = json.loads((FORMS / 'protocol-v2.template.json').read_bytes())
    dataset = json.loads((FORMS / 'dataset-manifest.template.json').read_bytes())
    protocol.update(study_id='fictional-record-test',
        intended_use_and_specialist_scope='Fictional engineering test of recording consistency only.',
        frozen_at='2026-10-18T10:00:00+00:00',
        evidence_storage_and_redaction_policy='Fictional private records; no actual persons or client data.')
    for role in ('owner_approval', 'qualified_reviewer_approval'):
        protocol[role].update(reviewer_ref='fictional-' + role, decision='approve',
            at='2026-10-18T09:30:00+00:00', reason='Fictional recorded claim for the test, not a real approval.')
    protocol['qualified_reviewer_approval']['qualifications_ref'] = 'fictional-qualification-record'
    protocol['provider_comparison'].update(source_commit='a' * 40, source_manifest_sha256='b' * 64,
        attempt_and_retry_policy='Fictional one attempt, no silent retries; all failures retained.',
        configurations=[{'id': 'fictional-config', 'provider': 'fictional-service',
            'inference_provider': 'fictional-pinned-worker', 'runtime': 'fictional-runtime',
            'model_id': 'fictional-model-1', 'runtime_version': 'fictional-1',
            'prompt_version': 'fictional-prompt-1', 'compiler_version': 'fictional-compiler-1',
            'schema_version': 'fictional-schema-1', 'parameters': {}, 'concurrency': 1,
            'timeout_seconds': 30, 'ordering_policy': 'Fictional fixed order defined before study.',
            'permitted_data_scope': 'Fictional records only; not permission for an actual call.',
            'authorized_budget': {'currency': 'USD', 'maximum_amount': 0},
            'authorized_downloads': 'None; no model or dependency downloads.'}])
    for group in protocol['prospective_task_specific_thresholds'].values():
        group.update(definition='Fictional measurement for recording-format testing only.',
            units_and_denominator='Fictional count per recorded test case, including failed attempts.',
            thresholds=[{'measure': 'fictional-count', 'comparison': '<=', 'value': 7,
                'unit': 'fictional-count/case', 'rationale': 'Arbitrary test-only value, not a project acceptance requirement.'}])
    for key in protocol['review_procedure']:
        if key != 'initial_labels_recorded_separately':
            protocol['review_procedure'][key] = 'Fictional private procedure reference: ' + key
    dataset.update(dataset_id='fictional-dataset', author_ref='fictional-reviewer-1',
        author_role_and_qualifications_ref='fictional-author-role-record', independently_authored=True,
        development_exposure_and_exclusions='Fictional exposure declaration; public development examples excluded.',
        source_permission_and_retention_ref='fictional-private-permissions',
        frozen_at='2026-10-18T09:00:00+00:00', case_count=1,
        reviewers=[{'ref': 'fictional-reviewer-1', 'qualifications_ref': 'fictional-qualifications-1',
                    'independence_ref': 'fictional-independence-1'},
                   {'ref': 'fictional-reviewer-2', 'qualifications_ref': 'fictional-qualifications-2',
                    'independence_ref': 'fictional-independence-2'}],
        cases=[{'id': 'fictional-case',
            'source_artifacts': [artifact(tmp_path, 'source.txt', 'A fictional museum is deciding where to store an unexamined crate.')],
            'model_input': artifact(tmp_path, 'input.json', json.dumps({'source': 'A fictional crate needs storage.', 'outcome': 'Choose authorised storage.'})),
            'expected_labels': artifact(tmp_path, 'labels.json', '{"private_label":"Human must check storage permission."}'),
            'exact_requested_outcome': 'Choose authorised storage for the fictional crate.',
            'historical_information_cutoff': '2026-10-17T10:00:00+00:00',
            'risk_and_specialist_scope': 'Fictional risk declaration, not a risk classifier.',
            'safety_critical': True, 'coverage': list(rr.COVERAGE),
            'reviewer_refs': ['fictional-reviewer-1', 'fictional-reviewer-2']}])
    return tmp_path, protocol, dataset


def inspect(bundle):
    root, protocol, dataset = bundle
    digest = write_json(root / 'dataset.json', dataset)
    protocol['dataset'] = {'ref': 'dataset.json', 'sha256': digest}
    digest = write_json(root / 'protocol.json', protocol)
    return rr.inspect_bundle(root, 'protocol.json', digest, as_of=AS_OF)


def codes(report):
    return {row['code'] for row in report['diagnostics']}


def test_complete_fictional_bundle_is_only_mechanically_ready(bundle, monkeypatch):
    def forbidden(*_, **__):
        raise AssertionError('Offline recording checks must not open a network connection')
    monkeypatch.setattr(socket, 'socket', forbidden)
    monkeypatch.setenv('EIGHTBALL_API_KEY', 'private-poison-value-must-not-appear')
    report = inspect(bundle)
    assert report['status'] == 'mechanically_ready_for_prospective_study'
    assert report['diagnostics'] == []
    assert report['protocol_sha256'] == hashlib.sha256((bundle[0] / 'protocol.json').read_bytes()).hexdigest()
    assert report['actual_model_calls'] == 0
    for field in ('independent_professional_review_performed', 'human_acceptance_performed',
                  'production_model_selected', 'v02_acceptance_completed'):
        assert report[field] is False
    assert 'private-poison-value' not in json.dumps(report)
    assert 'not authenticated' in report['notice']
    # Dataset author may be a reviewer: no invented diversity requirement.
    assert bundle[2]['author_ref'] == bundle[2]['reviewers'][0]['ref']


def test_unfilled_template_stays_blocked(tmp_path):
    path = tmp_path / 'protocol.json'
    path.write_bytes((FORMS / 'protocol-v2.template.json').read_bytes())
    report = rr.inspect_bundle(tmp_path, path.name, hashlib.sha256(path.read_bytes()).hexdigest(), as_of=AS_OF)
    assert report['status'] == 'blocked'
    assert 'nonempty_text_required' in codes(report)
    assert 'nonempty_bounded_array_required' in codes(report)


def test_v1_is_unsupported_by_optional_tool_without_invalidating_manual_review(tmp_path):
    path = tmp_path / 'protocol.json'
    path.write_bytes((FORMS / 'protocol.template.json').read_bytes())
    report = rr.inspect_bundle(tmp_path, path.name, hashlib.sha256(path.read_bytes()).hexdigest(), as_of=AS_OF)
    assert codes(report) == {'unsupported_recording_version'}
    assert 'Existing v1 manual reviews remain legitimate' in report['notice']


@pytest.mark.parametrize('mutate,expected', [
    (lambda p, d: p['owner_approval'].update(decision=None), 'required_value_changed'),
    (lambda p, d: p['qualified_reviewer_approval'].update(qualifications_ref=' '), 'nonempty_text_required'),
    (lambda p, d: p['owner_approval'].update(at='2026-10-18T10:01:00Z'), 'approval_after_freeze'),
    (lambda p, d: p.update(frozen_at='2026-10-18T13:00:00Z'), 'freeze_in_future'),
    (lambda p, d: p.update(frozen_at='2026-10-18T10:00:00'), 'aware_timestamp_required'),
    (lambda p, d: d.update(frozen_at='2026-10-18T10:01:00Z'), 'dataset_not_frozen_before_protocol'),
    (lambda p, d: d['cases'][0].update(historical_information_cutoff='2026-10-18T11:00:00Z'), 'cutoff_after_dataset_freeze'),
    (lambda p, d: d.update(case_count=True), 'case_count_mismatch'),
    (lambda p, d: d.update(case_count=2), 'case_count_mismatch'),
    (lambda p, d: d.update(independently_authored=False), 'required_value_changed'),
    (lambda p, d: d['cases'][0].update(reviewer_refs=['fictional-reviewer-1']), 'two_reviewers_required'),
    (lambda p, d: d['cases'][0].update(reviewer_refs=['fictional-reviewer-1'] * 2), 'duplicate_identifier'),
    (lambda p, d: d['cases'][0].update(reviewer_refs=['fictional-reviewer-1', 'missing']), 'unregistered_reviewer'),
    (lambda p, d: d['cases'][0].update(safety_critical=1), 'explicit_boolean_required'),
    (lambda p, d: d['cases'][0].update(coverage=['negation']), 'required_coverage_missing'),
    (lambda p, d: d.update(required_coverage=['negation']), 'required_coverage_changed'),
    (lambda p, d: p['provider_comparison'].update(source_commit='latest'), 'git_commit_required'),
    (lambda p, d: p['provider_comparison'].update(all_failures_in_denominator=False), 'required_value_changed'),
    (lambda p, d: p['provider_comparison'].update(silent_repair_or_catalogue_substitution_permitted=True), 'required_value_changed'),
    (lambda p, d: p['provider_comparison']['configurations'][0].update(model_id='openrouter/free'), 'exact_model_required'),
    (lambda p, d: p['provider_comparison']['configurations'][0].update(inference_provider=None), 'nonempty_text_required'),
    (lambda p, d: p['provider_comparison']['configurations'][0].update(concurrency=True), 'positive_integer_required'),
    (lambda p, d: p['provider_comparison']['configurations'][0].update(timeout_seconds=10**500), 'positive_finite_number_required'),
    (lambda p, d: p['provider_comparison']['configurations'][0]['authorized_budget'].update(maximum_amount=True), 'nonnegative_finite_number_required'),
    (lambda p, d: p['prospective_task_specific_thresholds']['latency'].update(thresholds=[]), 'nonempty_bounded_array_required'),
    (lambda p, d: p['prospective_task_specific_thresholds']['latency']['thresholds'][0].update(value='decide later'), 'finite_number_required'),
    (lambda p, d: p['prospective_task_specific_thresholds']['latency']['thresholds'][0].update(value=True), 'finite_number_required'),
    (lambda p, d: p['prospective_task_specific_thresholds']['latency']['thresholds'][0].update(comparison='maybe'), 'numeric_comparison_required'),
    (lambda p, d: p['existing_protocol_gates'].update(state_or_approval_mutations_allowed=False), 'required_value_changed'),
    (lambda p, d: p['existing_protocol_gates'].update(unresolved_critical_semantic_errors_allowed=1), 'required_value_changed'),
    (lambda p, d: p.update(independent_review_completed=True), 'unexpected_field'),
])
def test_adversarial_records_are_blocked(bundle, mutate, expected):
    mutate(bundle[1], bundle[2])
    report = inspect(bundle)
    assert report['status'] == 'blocked'
    assert expected in codes(report)


def test_all_existing_gates_have_strict_type_and_value(bundle):
    for key, value in rr.GATES.items():
        candidate = deepcopy(bundle)
        candidate[1]['existing_protocol_gates'][key] = not value if type(value) is bool else value + 1
        assert 'required_value_changed' in codes(inspect(candidate)), key


@pytest.mark.parametrize('raw', [b'{"template_version":1,"template_version":2}',
    b'{"value":NaN}', b'{"value":Infinity}', b'{"value":1e999}', b'\xff', b'[]'])
def test_bad_json_or_shape_never_ready(tmp_path, raw):
    (tmp_path / 'protocol.json').write_bytes(raw)
    report = rr.inspect_bundle(tmp_path, 'protocol.json', hashlib.sha256(raw).hexdigest(), as_of=AS_OF)
    assert report['status'] == 'blocked'
    assert codes(report) <= {'invalid_strict_json', 'unsupported_recording_version'}


def test_protocol_and_nested_artifact_hashes_bind_exact_bytes(bundle):
    root, protocol, dataset = bundle
    inspect(bundle)
    raw = (root / 'protocol.json').read_bytes()
    (root / 'protocol.json').write_bytes(raw + b' ')
    report = rr.inspect_bundle(root, 'protocol.json', hashlib.sha256(raw).hexdigest(), as_of=AS_OF)
    assert 'artifact_hash_mismatch' in codes(report)
    dataset['cases'][0]['source_artifacts'][0]['sha256'] = '0' * 64
    assert 'artifact_hash_mismatch' in codes(inspect(bundle))


def test_labels_shared_with_any_case_input_are_blocked(bundle):
    bundle[2]['cases'][0]['model_input'] = deepcopy(bundle[2]['cases'][0]['expected_labels'])
    assert 'labels_shared_with_model_inputs' in codes(inspect(bundle))


@pytest.mark.parametrize('public_source', rr.known_public_sources())
def test_renamed_public_sources_are_not_held_out(bundle, public_source):
    root, _, dataset = bundle
    # JSON escaping and a new case ID must not conceal exact public input reuse.
    dataset['cases'][0]['id'] = 'renamed-as-independent'
    dataset['cases'][0]['model_input'] = artifact(root, 'renamed-input.json', json.dumps({'source': public_source}))
    assert 'known_public_development_source' in codes(inspect(bundle))


@pytest.mark.parametrize('ref', ['../outside.txt', '/etc/passwd', 'https://example.test/private', 'source.txt/../labels.json', 'missing.txt'])
def test_nonlocal_or_escaping_artifact_references_are_blocked(bundle, ref):
    bundle[2]['cases'][0]['model_input']['ref'] = ref
    assert 'local_regular_artifact_required' in codes(inspect(bundle))


def test_symlink_escape_and_nonregular_file_are_rejected(bundle, tmp_path):
    root, _, dataset = bundle
    outside = root.parent / (root.name + '-outside.txt')
    outside.write_text('Private outside data must never appear in diagnostics.')
    (root / 'escape.txt').symlink_to(outside)
    dataset['cases'][0]['model_input']['ref'] = 'escape.txt'
    report = inspect(bundle)
    assert 'local_regular_artifact_required' in codes(report)
    assert 'Private outside data' not in json.dumps(report)
    dataset['cases'][0]['model_input']['ref'] = '.'
    assert 'local_regular_artifact_required' in codes(inspect(bundle))


def test_size_and_total_limits_fail_closed(bundle, monkeypatch):
    root, _, dataset = bundle
    dataset['cases'][0]['model_input'] = artifact(root, 'large-input.txt', 'x' * 30_000)
    monkeypatch.setattr(rr, 'MAX_FILE_BYTES', 20_000)
    assert 'artifact_limit_exceeded' in codes(inspect(bundle))
    monkeypatch.setattr(rr, 'MAX_FILE_BYTES', 100_000)
    monkeypatch.setattr(rr, 'MAX_TOTAL_BYTES', 20_000)
    assert 'artifact_limit_exceeded' in codes(inspect(bundle))


def test_diagnostics_do_not_echo_private_keys_or_unknown_field_names(bundle):
    bundle[1]['very-private-unknown-field'] = 'private-token-value'
    bundle[2]['cases'][0]['model_input']['ref'] = 'private-missing-client-record.txt'
    report = inspect(bundle)
    rendered = json.dumps(report)
    assert 'unexpected_field' in rendered
    for secret in ('very-private-unknown-field', 'private-token-value', 'private-missing-client-record'):
        assert secret not in rendered


def test_invalid_unicode_file_reference_is_diagnostic_not_crash(bundle):
    bundle[2]['cases'][0]['model_input']['ref'] = '\ud800'
    assert 'valid_unicode_required' in codes(inspect(bundle))


def test_cli_exit_status_and_read_only_files(bundle):
    root, _, _ = bundle
    inspect(bundle)
    before = {path.name: path.read_bytes() for path in root.iterdir() if path.is_file()}
    args = [sys.executable, str(ROOT / 'evals/review_readiness.py'), '--root', str(root),
            '--protocol', 'protocol.json', '--protocol-sha256', hashlib.sha256(before['protocol.json']).hexdigest()]
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['status'] == 'mechanically_ready_for_prospective_study'
    result = subprocess.run(args[:-1] + ['0' * 64], capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert 'artifact_hash_mismatch' in codes(json.loads(result.stdout))
    assert before == {path.name: path.read_bytes() for path in root.iterdir() if path.is_file()}


def test_caller_supplied_clock_must_be_aware(bundle):
    root, _, _ = bundle
    with pytest.raises(ValueError, match='timezone aware'):
        rr.inspect_bundle(root, 'protocol.json', '0' * 64, as_of=datetime(2026, 10, 18))
