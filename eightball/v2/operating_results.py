"""Reconstruct retained operating-plan checks without providers or case commands."""
from hashlib import sha256
import json
import re

from endstate.intelligence.operating import (
    MAX_GENERATION_CALLS, VERSION, OperatingPlanningSpec, coordinate_operating)
from endstate.intelligence.planning import CoordinationStopped

from ..event_work import MAX_RESULT_BYTES
from ..store import digest
from .hosted import json_object

STOPS = frozenset({'completed', 'time_budget', 'planning_setup_failed', 'planning_provider_failed',
    'unexpected_planning_model', 'planning_receipt_budget', 'generation_call_budget',
    'changed_planning_model', 'invalid_initial_arithmetic', 'invalid_revision_arithmetic',
    *('invalid_' + phase + '_input_or_result' for phase in ('initial', 'challenge', 'revision'))})


def _same(actual, expected):
    if digest(actual) != digest(expected):
        raise ValueError('Inconsistent retained operating-plan result')


def project_operating(raw, receipt, case_id, revision):
    if not isinstance(raw, str) or len(raw.encode()) > MAX_RESULT_BYTES:
        return None
    recognized = False
    try:
        r = json_object(raw)
        if not isinstance(r, dict) or r.get('kind') != 'operating_planning':
            return None
        recognized = True
        spec = OperatingPlanningSpec.model_validate(r['spec'])
        binding = dict(version=VERSION, case_id=case_id, base_revision=revision,
            receipt_sha256=digest(receipt.model_dump(mode='json')),
            spec_sha256=digest(spec.model_dump(mode='json')),
            planning_cost_status='unknown_not_provider_reported', charge_status='provider_billing_not_verified')
        _same({k: r.get(k) for k in binding}, binding)
        if r['stop_reason'] not in STOPS:
            raise ValueError('Unknown stop reason')
        attempts = r['attempts']
        if (not isinstance(attempts, list) or len(attempts) > MAX_GENERATION_CALLS
                or type(r['generation_attempts']) is not int or r['generation_attempts'] != len(attempts)):
            raise ValueError('Invalid attempt bound')
        planning = r['planning_receipt'] or {}
        calls = planning.get('calls', [])
        if not isinstance(calls, list) or len(calls) > len(attempts):
            raise ValueError('Invalid transport receipts')
        for index, call in enumerate(calls):
            for key in ('request_sha256', 'response_sha256', 'response_body_sha256', 'raw_content_sha256'):
                if call.get(key) is not None and not re.fullmatch('[0-9a-f]{64}', call[key]):
                    raise ValueError('Invalid transport hash')
            if 'raw_content' in call:
                _same(call['raw_content_sha256'], sha256(call['raw_content'].encode()).hexdigest())
                if attempts[index]['output_sha256'] is not None:
                    _same(json_object(call['raw_content']), attempts[index]['output'])
        for index, attempt in enumerate(attempts):
            if attempt['validated']:
                if index >= len(calls) or not all(calls[index].get(k) for k in
                    ('request_sha256', 'response_sha256', 'raw_content_sha256')):
                    raise ValueError('Validated stage without a transport receipt')
                _same(attempt['model'], planning['requested_model'])
                _same(calls[index]['served_model'], attempt['model'])
        remaining = iter(attempts)
        replay_count = 0

        def replay(schema, instructions, context):
            nonlocal replay_count
            attempt = next(remaining)
            replay_count += 1
            _same(attempt['input_sha256'], digest(context))
            if attempt['output_sha256'] is None:
                raise CoordinationStopped(r['stop_reason'])
            _same(attempt['output_sha256'], digest(attempt['output']))
            return attempt['output'], attempt['model']

        namespace = 'coord_' + binding['receipt_sha256'][:32]
        expected = coordinate_operating(spec, receipt.event.text, namespace, replay, None, lambda: None)
        if expected['stop_reason'] == 'completed' and r['stop_reason'] == 'time_budget':
            expected.update(stop_reason='time_budget', final_synthesis=None)
        _same({k: r.get(k) for k in expected}, expected)
        if replay_count != len(attempts):
            raise ValueError('Unreplayed attempts')
        fields = ('request_sha256', 'response_sha256', 'raw_content_sha256', 'status', 'served_model',
                  'finish_reason', 'provider_stop_reason', 'error_code', 'usage', 'provider_usage')
        return binding | expected | dict(available=True,
            planning_calls=[{k: c[k] for k in fields if k in c} for c in calls])
    except (ValueError, TypeError, KeyError, AttributeError, RecursionError, StopIteration):
        return {'available': False} if recognized else None
