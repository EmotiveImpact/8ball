"""Read-only reconstruction of retained advisory stages; never calls a provider."""
from hashlib import sha256
import json
import re

from endstate.compilation import DraftRequest, draft_outcome
from endstate.intelligence.coordination import Attempt, summarize
from endstate.intelligence.planning import (CoordinatedPlanningSpec, MAX_GENERATION_CALLS,
    VERSION, challenge_input, draft_namespace)

from ..event_work import MAX_RESULT_BYTES
from ..store import digest


STOPS = frozenset({'completed', 'specialist_review_incomplete', 'time_budget',
    'planning_setup_failed', 'planning_provider_failed', 'unexpected_planning_model',
    'planning_receipt_budget', 'generation_call_budget', 'changed_planning_model',
    'invalid_specialist_summary', 'invalid_specialist_input_binding',
    *('invalid_' + phase + suffix for phase in ('initial', 'challenge', 'revision')
      for suffix in ('_draft', '_input_or_result'))})
PANEL_STOPS = frozenset({'completed', 'time_budget', 'setup_or_provider_failed',
                        'unknown_reported_cost', 'reported_cost_budget'})


def _same(actual, expected):
    if digest(actual) != digest(expected):
        raise ValueError('Inconsistent retained report')


def _proposal(value, phase, spec, text, namespace, calls):
    trace = dict(value['trace'])
    if trace['prompt_version'] not in ('endstate.draft.prompts.v3', 'endstate.draft.prompts.v4'):
        raise ValueError('Unsupported draft version')
    # Canonical report serialization may reorder objects. Recover the original
    # provider object order for the byte-bound challenge input where available.
    offset = 0 if phase == 'initial' else 2
    for i, field in enumerate(('frame', 'routes')):
        if len(calls) > offset+i and 'raw_content' in calls[offset+i]:
            call = calls[offset+i]
            raw = call['raw_content']
            _same(sha256(raw.encode()).hexdigest(), call['raw_content_sha256'])
            parsed = json.loads(raw)
            _same(parsed, trace[field])
            trace[field] = parsed
    remaining = iter((trace['frame'], trace['routes']))
    compiled, checked, model = draft_outcome(
        DraftRequest(outcome=spec.outcome, brief=text, namespace=draft_namespace(namespace, phase)),
        lambda *args: (next(remaining), value['model']), require_target_coverage=True)
    _same(value['compiled'], compiled.model_dump(mode='json'))
    checked['prompt_version'] = trace['prompt_version']
    _same(trace, checked)
    return dict(model=model, frame=trace['frame'], routes=trace['routes'],
                prompt_version=trace['prompt_version'], review_notices=checked['review_notices']), trace


def project_coordinated(raw, receipt, case_id, revision):
    if not isinstance(raw, str) or len(raw.encode()) > MAX_RESULT_BYTES:
        return None
    recognized = False
    try:
        r = json.loads(raw)
        if not isinstance(r, dict) or r.get('kind') != 'coordinated_planning':
            return None
        recognized = True
        spec = CoordinatedPlanningSpec.model_validate(r['spec'])
        binding = dict(version=VERSION, case_id=case_id, base_revision=revision,
            receipt_sha256=digest(receipt.model_dump(mode='json')),
            input_sha256=digest(receipt.event.text), spec_sha256=digest(spec.model_dump(mode='json')),
            method='single_proposer_independent_challenges_revision', advisory_only=True,
            facts_attested=False, execution_authorized=False, predictive_quality_approved=False,
            automatic_retries=False, automatic_fallback=False,
            max_generation_calls=MAX_GENERATION_CALLS,
            planning_cost_status='unknown_not_provider_reported', charge_status='provider_billing_not_verified')
        _same({k: r.get(k) for k in binding}, binding)
        if r['stop_reason'] not in STOPS or r['phase'] not in ('initial', 'challenge', 'revision'):
            raise ValueError('Unknown stop or stage')
        if type(r['generation_attempts']) is not int or not 0 <= r['generation_attempts'] <= MAX_GENERATION_CALLS:
            raise ValueError('Invalid generation bound')
        planning = r['planning_receipt'] or {}
        calls = planning.get('calls', [])
        if not isinstance(calls, list) or len(calls) > r['generation_attempts']:
            raise ValueError('Invalid call records')
        for call in calls:
            for key in ('request_sha256', 'response_sha256', 'response_body_sha256', 'raw_content_sha256'):
                if call.get(key) is not None and not re.fullmatch('[0-9a-f]{64}', call[key]):
                    raise ValueError('Invalid transport hash')
        namespace = 'coord_' + binding['receipt_sha256'][:32]
        initial = revised = panel = trace = None
        if r['initial'] is not None:
            initial, trace = _proposal(r['initial'], 'initial', spec, receipt.event.text, namespace, calls)
            if r['phase'] == 'initial' or r['generation_attempts'] < 2 or len(calls) < 2:
                raise ValueError('Inconsistent original stage')
        elif r['phase'] != 'initial' or r['challenges'] is not None or r['revision'] is not None:
            raise ValueError('Later stages without original')
        eligible = False
        if r['challenges'] is not None:
            if initial is None:
                raise ValueError('Challenge without original')
            p = r['challenges']
            panel = summarize(spec.review, [Attempt.model_validate(a) for a in p['attempts']])
            _same({k: p.get(k) for k in panel}, panel)
            state_hash = digest(challenge_input(spec.outcome, receipt.event.text, trace))
            _same(p['input_sha256'], state_hash)
            if p['stop_reason'] not in PANEL_STOPS:
                raise ValueError('Unknown challenge stop')
            eligible = (p['stop_reason'] == 'completed' and not panel['not_started_models']
                and not panel['unknown_cost_attempts'] and panel['answered_models'] == panel['requested_models']
                and panel['known_reported_cost_nano_usd'] < spec.review.max_reported_cost_nano_usd)
            cost = panel['known_reported_cost_nano_usd']
            panel.update(available=True, input_sha256=state_hash, spec_sha256=digest(panel['spec']),
                base_revision=revision, stop_reason=p['stop_reason'],
                known_reported_cost_usd=f'{cost // 1_000_000_000}.{cost % 1_000_000_000:09d}')
            if not eligible and (r['revision'] is not None or r['phase'] != 'challenge'
                    or r['stop_reason'] not in ('specialist_review_incomplete', 'time_budget')):
                raise ValueError('Revision after incomplete challenge')
        if r['phase'] == 'revision' and not eligible:
            raise ValueError('Revision without eligible challenge')
        if eligible and r['phase'] != 'revision':
            raise ValueError('Complete challenge without revision stage')
        if r['phase'] == 'challenge' and r['generation_attempts'] != 2:
            raise ValueError('Generation after stopped challenge')
        for phase in ('initial', 'challenge', 'revision'):
            if r['stop_reason'].startswith('invalid_' + phase + '_') and r['phase'] != phase:
                raise ValueError('Failure belongs to a different stage')
        if r['revision'] is not None:
            if not eligible or r['phase'] != 'revision' or r['generation_attempts'] != 4 or len(calls) != 4:
                raise ValueError('Invalid revision stage')
            revised, _ = _proposal(r['revision'], 'revision', spec, receipt.event.text, namespace, calls)
            _same(revised['model'], initial['model'])
        for draft in (initial, revised):
            if draft:
                _same(draft['model'], planning['requested_model'])
        expected_synthesis = (dict(candidate='revision', requires_operator_review=True,
            objections_resolved=False, selected_route=None) if r['stop_reason'] == 'completed' else None)
        _same(r['final_synthesis'], expected_synthesis)
        if r['stop_reason'] == 'completed' and revised is None:
            raise ValueError('Completion without revision')
        if r['stop_reason'] == 'specialist_review_incomplete' and (panel is None or eligible):
            raise ValueError('Inconsistent incomplete panel')
        failed = r.get('failed_draft')
        if failed is not None and (r['stop_reason'] == 'completed' or r['phase'] == 'challenge'
                or failed.get('failed_stage') not in ('frame', 'routes', 'compile')):
            raise ValueError('Inconsistent failed draft')
        fields = ('request_sha256', 'response_sha256', 'response_body_sha256', 'raw_content_sha256',
            'status', 'served_model', 'response_mode', 'finish_reason', 'provider_stop_reason',
            'error_code', 'usage', 'provider_usage', 'raw_content_omitted')
        return binding | dict(available=True, spec=spec.model_dump(mode='json'), initial=initial,
            challenges=panel, revision=revised, final_synthesis=expected_synthesis,
            phase=r['phase'], stop_reason=r['stop_reason'], generation_attempts=r['generation_attempts'],
            failed_draft=({'failed_stage': failed['failed_stage'], 'diagnostic': failed.get('diagnostic')}
                          if failed is not None else None),
            planning_calls=[{k: c[k] for k in fields if k in c} for c in calls])
    except (ValueError, TypeError, KeyError, AttributeError, RecursionError, StopIteration):
        return {'available': False} if recognized else None
