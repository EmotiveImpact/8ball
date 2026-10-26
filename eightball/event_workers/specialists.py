"""Explicit reviewed-text decision comparisons; no commands or automatic retry."""
import json
from time import perf_counter

from endstate.intelligence.coordination import Attempt, ReviewSpec, USAGE_FIELDS, summarize
from endstate.intelligence.decisions import DecisionInput

from ..store import digest
from ..v2.decision_models import DecisionSession, MAX_REQUEST_BYTES, payload_for


class SpecialistReviewProcessor:
    def __init__(self, spec: ReviewSpec, *, allow_external: bool,
                 session_factory=DecisionSession, timer=perf_counter):
        if allow_external is not True:
            raise PermissionError('Explicit external processing permission is required')
        self.spec = ReviewSpec.model_validate(spec.model_dump(mode='python'))
        self.session_factory, self.timer = session_factory, timer

    def __call__(self, receipt, snapshot):
        raise PermissionError('Specialist processing requires host authority checkpoints')

    @property
    def configuration_sha256(self):
        spec = ReviewSpec.model_validate(self.spec.model_dump(mode='python'))
        return digest(spec.model_dump(mode='json'))

    def run(self, receipt, snapshot, checkpoint):
        report = self.compare(receipt.event.text, checkpoint)
        report.update(kind='specialist_review', case_id=snapshot.id,
                      base_revision=snapshot.revision,
                      receipt_sha256=digest(receipt.model_dump(mode='json')))
        return json.dumps(report, ensure_ascii=False, allow_nan=False)

    def compare(self, text, checkpoint, *, deadline=None):
        spec = ReviewSpec.model_validate(self.spec.model_dump(mode='python'))
        requests = [DecisionInput(model=model, state=text, questions=spec.questions)
                    for model in spec.models]
        for request in requests:
            if len(json.dumps(payload_for(request)[1], ensure_ascii=False, allow_nan=False).encode()) > MAX_REQUEST_BYTES:
                raise ValueError('Reviewed input exceeds the decision request boundary')
        checkpoint()
        own_deadline = self.timer() + spec.max_seconds
        deadline = own_deadline if deadline is None else min(own_deadline, deadline)
        attempts, stop_reason = [], 'completed'
        for request in requests:
            checkpoint()
            if self.timer() >= deadline:
                stop_reason = 'time_budget'
                break
            session = None
            try:
                session = self.session_factory(allow_external=True)
            except Exception:
                attempts.append(Attempt(model=request.model, status='failed'))
                stop_reason = 'setup_or_provider_failed'
                break
            checkpoint()
            if self.timer() >= deadline:
                stop_reason = 'time_budget'
                break
            try:
                result = session.ask(request)
                if (result.get('requested_model') != request.model or result.get('advisory_only') is not True
                        or result.get('facts_attested') is not False or result.get('execution_authorized') is not False):
                    raise ValueError('Invalid advisory result boundary')
                cost = result['usage'].get('cost_nano_usd')
                cost = cost if type(cost) is int and cost >= 0 else None
                attempt = Attempt(model=request.model, status='answered', answers=result['answers'],
                    usage={k: v for k, v in result['usage'].items() if k in USAGE_FIELDS},
                    served_model=result['served_model'], reported_cost_nano_usd=cost,
                    request_started=session.receipt.get('inference_calls') == 1,
                    request_sha256=session.receipt.get('request_sha256'),
                    response_sha256=session.receipt.get('response_sha256'))
                summarize(spec, [*attempts, attempt])
            except Exception:
                attempt = Attempt(model=request.model, status='failed',
                    request_started=session.receipt.get('inference_calls') == 1,
                    request_sha256=session.receipt.get('request_sha256'),
                    response_sha256=session.receipt.get('response_sha256'))
                stop_reason = 'setup_or_provider_failed'
            checkpoint()
            attempts.append(attempt)
            if attempt.status == 'failed':
                break
            if attempt.reported_cost_nano_usd is None:
                stop_reason = 'unknown_reported_cost'
                break
            if sum(a.reported_cost_nano_usd or 0 for a in attempts) >= spec.max_reported_cost_nano_usd:
                stop_reason = 'reported_cost_budget'
                break
        checkpoint()
        if self.timer() >= deadline:
            stop_reason = 'time_budget'
        report = summarize(spec, attempts)
        report.update(stop_reason=stop_reason, input_sha256=digest(text),
                      spec_sha256=digest(spec.model_dump(mode='json')),
                      automatic_retries=False, automatic_fallback=False,
                      charge_status='provider_billing_not_verified')
        return report
