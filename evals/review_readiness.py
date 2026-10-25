"""Offline checks for optional prospective study records; never human acceptance.

Version 2 is a recording format for the unchanged plan-quality-protocol-v1.
Its hashes and approval/independence declarations are unsigned local records.
No network, provider settings, case stores or progress ledgers are consulted.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import stat

VERSION = 'v02-prospective-review.v2'
DATASET_VERSION = 'v02-independent-dataset.v1'
PROTOCOL_VERSION = 'plan-quality-protocol-v1'
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024
MAX_FILES = 512
SHA = re.compile(r'^[0-9a-f]{64}$')
COVERAGE = ('negation', 'contradiction', 'unclear_identity', 'authority',
            'relative_dates_and_timezones', 'missing_dependencies',
            'meaningful_alternatives', 'final_verification',
            'refusal_and_external_wait', 'competing_objectives',
            'injection_text', 'ambiguous_outcome')
METRICS = ('extraction_precision', 'extraction_recall_and_omissions',
           'valid_proposal_coverage', 'correction_effort', 'latency',
           'abstention_refusal_timeout', 'review_effort_and_operator_usefulness')
GATES = {
    'state_or_approval_mutations_allowed': 0,
    'source_or_case_boundary_violations_allowed': 0,
    'every_required_frozen_generation_case_must_pass_structure': True,
    'unresolved_critical_semantic_errors_allowed': 0,
    'all_six_dimensions_need_human_verdict_and_reason': True,
    'uncertain_or_needs_changes_blocks_promotion': True,
    'safety_critical_cases_need_at_least_two_qualified_independent_reviews': True,
    'unresolved_disagreement_is_a_pass': False,
}


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate key')
            result[key] = value
        return result

    def constant(_):
        raise ValueError('nonfinite number')

    def number(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError('nonfinite number')
        return result

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=number)


def finite_number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


class Checker:
    def __init__(self, root, as_of):
        self.root = Path(root).resolve()
        self.as_of = as_of
        self.diagnostics = []
        self.files = {}
        self.total = 0

    def issue(self, pointer, code):
        item = {'pointer': pointer, 'code': code}
        if item not in self.diagnostics:
            self.diagnostics.append(item)

    def obj(self, value, pointer, keys):
        if type(value) is not dict:
            self.issue(pointer, 'object_required')
            return {}
        for key in sorted(set(value) - set(keys)):
            # Do not echo unknown keys: they may contain private material.
            self.issue(pointer, 'unexpected_field')
        for key in keys:
            if key not in value:
                self.issue(pointer + '/' + key, 'missing_field')
        return value

    def text(self, value, pointer):
        if type(value) is not str or not value.strip():
            self.issue(pointer, 'nonempty_text_required')
            return False
        try:
            value.encode('utf-8')
        except UnicodeError:
            self.issue(pointer, 'valid_unicode_required')
            return False
        return True

    def equal(self, value, expected, pointer):
        if type(value) is not type(expected) or value != expected:
            self.issue(pointer, 'required_value_changed')

    def sha(self, value, pointer):
        if type(value) is not str or not SHA.fullmatch(value):
            self.issue(pointer, 'sha256_required')
            return False
        return True

    def date(self, value, pointer):
        try:
            if type(value) is not str:
                raise ValueError()
            result = datetime.fromisoformat(value.replace('Z', '+00:00'))
            if result.tzinfo is None or result.utcoffset() is None:
                raise ValueError()
            return result
        except ValueError:
            self.issue(pointer, 'aware_timestamp_required')
            return None

    def sequence(self, value, pointer, maximum=128):
        if type(value) is not list or not 1 <= len(value) <= maximum:
            self.issue(pointer, 'nonempty_bounded_array_required')
            return []
        return value

    def unique_texts(self, value, pointer, maximum=128):
        values = self.sequence(value, pointer, maximum)
        good = []
        for i, item in enumerate(values):
            if self.text(item, f'{pointer}/{i}'):
                if item in good:
                    self.issue(f'{pointer}/{i}', 'duplicate_identifier')
                good.append(item)
        return good

    def read(self, ref, pointer):
        if not self.text(ref, pointer):
            return None
        try:
            path = Path(ref)
            if path.is_absolute() or '..' in path.parts or ':' in ref or '\\' in ref:
                raise ValueError()
            target = self.root / path
            resolved = target.resolve(strict=True)
            if not resolved.is_relative_to(self.root):
                raise ValueError()
            if any(part.is_symlink() for part in (target, *target.parents) if part != self.root and part.is_relative_to(self.root)):
                raise ValueError()
            info = resolved.stat()
            if not stat.S_ISREG(info.st_mode):
                raise ValueError()
            if resolved in self.files:
                return self.files[resolved]
            if info.st_size > MAX_FILE_BYTES or len(self.files) >= MAX_FILES:
                self.issue(pointer, 'artifact_limit_exceeded')
                return None
            with resolved.open('rb') as stream:
                raw = stream.read(MAX_FILE_BYTES + 1)
            if len(raw) > MAX_FILE_BYTES or self.total + len(raw) > MAX_TOTAL_BYTES:
                self.issue(pointer, 'artifact_limit_exceeded')
                return None
            self.total += len(raw)
            self.files[resolved] = raw
            return raw
        except (OSError, ValueError, RuntimeError):
            self.issue(pointer, 'local_regular_artifact_required')
            return None

    def json(self, raw, pointer):
        try:
            return strict_json(raw)
        except (ValueError, UnicodeError, RecursionError):
            self.issue(pointer, 'invalid_strict_json')
            return None

    def artifact(self, value, pointer):
        value = self.obj(value, pointer, ('ref', 'sha256'))
        raw = self.read(value.get('ref'), pointer + '/ref')
        if raw == b'':
            self.issue(pointer + '/ref', 'empty_artifact')
        if self.sha(value.get('sha256'), pointer + '/sha256') and raw is not None:
            if hashlib.sha256(raw).hexdigest() != value['sha256']:
                self.issue(pointer + '/sha256', 'artifact_hash_mismatch')
        return raw


def known_public_sources():
    """Exact public source reuse is detectable; concealed/paraphrased reuse is not."""
    directory = Path(__file__).resolve().parent
    generation = strict_json((directory / 'generation-cases.json').read_bytes())
    engineering = strict_json((directory / 'plan-review-cases.json').read_bytes())
    return [row[1] for row in generation] + [row['source_text'] for row in engineering['cases']]


def contains_public_source(raw, known):
    try:
        text = raw.decode('utf-8')
    except UnicodeError:
        return False
    texts = [text]
    try:
        def collect(value):
            if type(value) is str:
                texts.append(value)
            elif type(value) is list:
                for item in value:
                    collect(item)
            elif type(value) is dict:
                for item in value.values():
                    collect(item)
        collect(strict_json(raw))
    except (ValueError, RecursionError):
        pass
    return any(source in value for source in known for value in texts)


def check_dataset(c, data, frozen):
    p = '/dataset_manifest'
    data = c.obj(data, p, ('manifest_version', 'dataset_id', 'author_ref',
        'author_role_and_qualifications_ref', 'independently_authored',
        'development_exposure_and_exclusions', 'source_permission_and_retention_ref',
        'frozen_at', 'required_coverage', 'case_count', 'reviewers', 'cases'))
    c.equal(data.get('manifest_version'), DATASET_VERSION, p + '/manifest_version')
    for key in ('dataset_id', 'author_ref', 'author_role_and_qualifications_ref',
                'development_exposure_and_exclusions', 'source_permission_and_retention_ref'):
        c.text(data.get(key), p + '/' + key)
    c.equal(data.get('independently_authored'), True, p + '/independently_authored')
    at = c.date(data.get('frozen_at'), p + '/frozen_at')
    if at and frozen and at > frozen:
        c.issue(p + '/frozen_at', 'dataset_not_frozen_before_protocol')
    coverage = c.unique_texts(data.get('required_coverage'), p + '/required_coverage')
    if set(coverage) != set(COVERAGE):
        c.issue(p + '/required_coverage', 'required_coverage_changed')
    reviewers = {}
    for i, value in enumerate(c.sequence(data.get('reviewers'), p + '/reviewers', 64)):
        q = f'{p}/reviewers/{i}'
        value = c.obj(value, q, ('ref', 'qualifications_ref', 'independence_ref'))
        for key in ('ref', 'qualifications_ref', 'independence_ref'):
            c.text(value.get(key), q + '/' + key)
        ref = value.get('ref')
        if type(ref) is str:
            if ref in reviewers:
                c.issue(q + '/ref', 'duplicate_identifier')
            reviewers[ref] = value
    cases = c.sequence(data.get('cases'), p + '/cases')
    if type(data.get('case_count')) is not int or data.get('case_count') != len(cases) or not cases:
        c.issue(p + '/case_count', 'case_count_mismatch')
    ids, seen_coverage, inputs, labels = set(), set(), [], []
    known = known_public_sources()
    for i, value in enumerate(cases):
        q = f'{p}/cases/{i}'
        value = c.obj(value, q, ('id', 'source_artifacts', 'model_input', 'expected_labels',
            'exact_requested_outcome', 'historical_information_cutoff',
            'risk_and_specialist_scope', 'safety_critical', 'coverage', 'reviewer_refs'))
        for key in ('id', 'exact_requested_outcome', 'risk_and_specialist_scope'):
            c.text(value.get(key), q + '/' + key)
        if type(value.get('id')) is str:
            if value['id'] in ids:
                c.issue(q + '/id', 'duplicate_identifier')
            ids.add(value['id'])
        cutoff = c.date(value.get('historical_information_cutoff'), q + '/historical_information_cutoff')
        if cutoff and at and cutoff > at:
            c.issue(q + '/historical_information_cutoff', 'cutoff_after_dataset_freeze')
        tags = c.unique_texts(value.get('coverage'), q + '/coverage')
        if not set(tags) <= set(COVERAGE):
            c.issue(q + '/coverage', 'unknown_coverage')
        seen_coverage.update(tags)
        assigned = c.unique_texts(value.get('reviewer_refs'), q + '/reviewer_refs', 64)
        if any(ref not in reviewers for ref in assigned):
            c.issue(q + '/reviewer_refs', 'unregistered_reviewer')
        if type(value.get('safety_critical')) is not bool:
            c.issue(q + '/safety_critical', 'explicit_boolean_required')
        elif value['safety_critical'] and len(set(assigned)) < 2:
            c.issue(q + '/reviewer_refs', 'two_reviewers_required')
        for j, artifact in enumerate(c.sequence(value.get('source_artifacts'), q + '/source_artifacts', 32)):
            raw = c.artifact(artifact, f'{q}/source_artifacts/{j}')
            if raw is not None:
                inputs.append((q + '/source_artifacts', raw))
        raw = c.artifact(value.get('model_input'), q + '/model_input')
        if raw is not None:
            inputs.append((q + '/model_input', raw))
        raw = c.artifact(value.get('expected_labels'), q + '/expected_labels')
        if raw is not None:
            labels.append((q + '/expected_labels', raw))
    if not set(COVERAGE) <= seen_coverage:
        c.issue(p + '/cases', 'required_coverage_missing')
    label_hashes = {hashlib.sha256(raw).digest() for _, raw in labels}
    for pointer, raw in inputs:
        if hashlib.sha256(raw).digest() in label_hashes:
            c.issue(pointer, 'labels_shared_with_model_inputs')
        if contains_public_source(raw, known):
            c.issue(pointer, 'known_public_development_source')


def check_protocol(c, data):
    if type(data) is not dict or data.get('template_version') != VERSION:
        c.issue('/template_version', 'unsupported_recording_version')
        return
    data = c.obj(data, '', ('template_version', 'protocol_reference', 'protocol_version',
        'notice', 'study_id', 'intended_use_and_specialist_scope', 'owner_approval',
        'qualified_reviewer_approval', 'frozen_at', 'dataset', 'provider_comparison',
        'existing_protocol_gates', 'prospective_task_specific_thresholds',
        'review_procedure', 'evidence_storage_and_redaction_policy'))
    c.equal(data.get('protocol_reference'), 'evals/PLAN-QUALITY-GATE.md', '/protocol_reference')
    c.equal(data.get('protocol_version'), PROTOCOL_VERSION, '/protocol_version')
    for key in ('notice', 'study_id', 'intended_use_and_specialist_scope', 'evidence_storage_and_redaction_policy'):
        c.text(data.get(key), '/' + key)
    frozen = c.date(data.get('frozen_at'), '/frozen_at')
    if frozen and frozen > c.as_of:
        c.issue('/frozen_at', 'freeze_in_future')
    for key in ('owner_approval', 'qualified_reviewer_approval'):
        p = '/' + key
        keys = ('reviewer_ref', 'decision', 'at', 'reason') + (('qualifications_ref',) if key == 'qualified_reviewer_approval' else ())
        approval = c.obj(data.get(key), p, keys)
        for field in keys:
            if field not in ('decision', 'at'):
                c.text(approval.get(field), p + '/' + field)
        c.equal(approval.get('decision'), 'approve', p + '/decision')
        at = c.date(approval.get('at'), p + '/at')
        if at and frozen and at > frozen:
            c.issue(p + '/at', 'approval_after_freeze')
    p = '/existing_protocol_gates'
    gates = c.obj(data.get('existing_protocol_gates'), p, tuple(GATES))
    for key, value in GATES.items():
        c.equal(gates.get(key), value, p + '/' + key)
    p = '/prospective_task_specific_thresholds'
    metrics = c.obj(data.get('prospective_task_specific_thresholds'), p, METRICS)
    for key in METRICS:
        q = p + '/' + key
        metric = c.obj(metrics.get(key), q, ('definition', 'units_and_denominator', 'thresholds'))
        for field in ('definition', 'units_and_denominator'):
            c.text(metric.get(field), q + '/' + field)
        for i, item in enumerate(c.sequence(metric.get('thresholds'), q + '/thresholds', 32)):
            r = f'{q}/thresholds/{i}'
            item = c.obj(item, r, ('measure', 'comparison', 'value', 'unit', 'rationale'))
            for field in ('measure', 'unit', 'rationale'):
                c.text(item.get(field), r + '/' + field)
            if item.get('comparison') not in ('<', '<=', '==', '>=', '>'):
                c.issue(r + '/comparison', 'numeric_comparison_required')
            if not finite_number(item.get('value')):
                c.issue(r + '/value', 'finite_number_required')
    p = '/review_procedure'
    procedure = c.obj(data.get('review_procedure'), p, ('reviewer_assignment_and_independence_ref',
        'initial_labels_recorded_separately', 'blinding_and_model_order_policy', 'adjudicator_ref',
        'disagreement_and_adjudication_record_ref', 're_evaluation_on_fresh_cases_policy'))
    c.equal(procedure.get('initial_labels_recorded_separately'), True, p + '/initial_labels_recorded_separately')
    for key in procedure:
        if key != 'initial_labels_recorded_separately':
            c.text(procedure[key], p + '/' + key)
    p = '/provider_comparison'
    comparison = c.obj(data.get('provider_comparison'), p, ('source_commit', 'source_manifest_sha256',
        'configurations', 'attempt_and_retry_policy', 'all_failures_in_denominator',
        'silent_repair_or_catalogue_substitution_permitted'))
    if type(comparison.get('source_commit')) is not str or not re.fullmatch(r'[0-9a-f]{40}', comparison['source_commit']):
        c.issue(p + '/source_commit', 'git_commit_required')
    c.sha(comparison.get('source_manifest_sha256'), p + '/source_manifest_sha256')
    c.text(comparison.get('attempt_and_retry_policy'), p + '/attempt_and_retry_policy')
    c.equal(comparison.get('all_failures_in_denominator'), True, p + '/all_failures_in_denominator')
    c.equal(comparison.get('silent_repair_or_catalogue_substitution_permitted'), False, p + '/silent_repair_or_catalogue_substitution_permitted')
    ids = set()
    for i, config in enumerate(c.sequence(comparison.get('configurations'), p + '/configurations', 32)):
        q = f'{p}/configurations/{i}'
        keys = ('id', 'provider', 'inference_provider', 'runtime', 'model_id', 'runtime_version', 'prompt_version',
                'compiler_version', 'schema_version', 'parameters', 'concurrency', 'timeout_seconds',
                'ordering_policy', 'permitted_data_scope', 'authorized_budget', 'authorized_downloads')
        config = c.obj(config, q, keys)
        for key in keys:
            if key not in ('parameters', 'concurrency', 'timeout_seconds', 'authorized_budget'):
                c.text(config.get(key), q + '/' + key)
        if type(config.get('id')) is str:
            if config['id'] in ids:
                c.issue(q + '/id', 'duplicate_identifier')
            ids.add(config['id'])
        if config.get('model_id') in ('auto', 'default', 'openrouter/free'):
            c.issue(q + '/model_id', 'exact_model_required')
        if type(config.get('parameters')) is not dict:
            c.issue(q + '/parameters', 'explicit_parameters_object_required')
        if type(config.get('concurrency')) is not int or config['concurrency'] < 1:
            c.issue(q + '/concurrency', 'positive_integer_required')
        timeout = config.get('timeout_seconds')
        if not finite_number(timeout) or timeout <= 0:
            c.issue(q + '/timeout_seconds', 'positive_finite_number_required')
        budget = c.obj(config.get('authorized_budget'), q + '/authorized_budget', ('currency', 'maximum_amount'))
        c.text(budget.get('currency'), q + '/authorized_budget/currency')
        amount = budget.get('maximum_amount')
        if not finite_number(amount) or amount < 0:
            c.issue(q + '/authorized_budget/maximum_amount', 'nonnegative_finite_number_required')
    artifact = data.get('dataset')
    raw = c.artifact(artifact, '/dataset')
    if raw is not None:
        parsed = c.json(raw, '/dataset_manifest')
        if parsed is not None:
            check_dataset(c, parsed, frozen)


def inspect_bundle(root, protocol_ref, expected_protocol_sha256=None, *, as_of=None):
    as_of = as_of or datetime.now(timezone.utc)
    if as_of.tzinfo is None or as_of.utcoffset() is None:
        raise ValueError('as_of must be timezone aware')
    checker = Checker(root, as_of)
    raw = checker.artifact({'ref': protocol_ref, 'sha256': expected_protocol_sha256}, '/protocol')
    if raw is not None:
        parsed = checker.json(raw, '/protocol')
        if parsed is not None:
            check_protocol(checker, parsed)
    return {
        'report_version': 'v02-prospective-readiness-report.v1',
        'checked_at': as_of.isoformat(),
        'protocol_sha256': hashlib.sha256(raw).hexdigest() if raw is not None else None,
        'status': 'blocked' if checker.diagnostics else 'mechanically_ready_for_prospective_study',
        'diagnostics': checker.diagnostics,
        'notice': 'Unsigned recording consistency only. Approvals, qualifications, permissions and independence are recorded claims, not authenticated. Timestamp checks compare supplied records; execution receipts and retrospective approval are not verified. Exact-content checks cannot prove held-out status or absence of embedded labels. Existing v1 manual reviews remain legitimate; this optional format adds no semantic acceptance gate.',
        'actual_model_calls': 0,
        'independent_professional_review_performed': False,
        'human_acceptance_performed': False,
        'production_model_selected': False,
        'v02_acceptance_completed': False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True, help='Private local bundle directory')
    parser.add_argument('--protocol', required=True, help='Protocol path relative to root')
    parser.add_argument('--protocol-sha256', required=True, help='SHA-256 of final frozen protocol bytes, recorded externally')
    args = parser.parse_args(argv)
    report = inspect_bundle(args.root, args.protocol, args.protocol_sha256)
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if report['status'] == 'mechanically_ready_for_prospective_study' else 2


if __name__ == '__main__':
    raise SystemExit(main())
