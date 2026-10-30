"""Opt-in coordinated planning using the current-authority event worker host."""
from dataclasses import asdict
import json
import os
from time import perf_counter

from endstate.intelligence.coordination import USAGE_FIELDS
from endstate.intelligence.planning import (CoordinatedPlanningSpec, CoordinationStopped,
                                           MAX_GENERATION_CALLS, VERSION, coordinate)

from ..store import digest
from ..v2.compatible import CompatibleSession, MAX_OUTPUT_TOKENS, settings
from ..v2.decision_models import COST_POLICY, DecisionSession
from ..v2.hosted import HostedFailure, HostedSetupRequired
from .specialists import SpecialistReviewProcessor

MAX_PLANNING_RECEIPT_BYTES = 200000


def _planning_receipt(session):
    if session is None:
        return None
    receipt = session.receipt
    if len(json.dumps(receipt, ensure_ascii=False, allow_nan=False).encode()) > MAX_PLANNING_RECEIPT_BYTES:
        for call in receipt['calls']:
            if 'raw_content' in call:
                call.pop('raw_content')
                call['raw_content_omitted'] = 'coordinated_receipt_byte_limit'
    return receipt


def _specialist_receipt(session):
    receipt = dict(session.receipt)
    if 'usage' in receipt:
        receipt['usage'] = {k: v for k, v in receipt['usage'].items() if k in USAGE_FIELDS}
    result = dict(receipt=receipt, response=None)
    if session.response is not None:
        if receipt.get('status') == 'validated_advisory':
            result['response'] = {k: session.response[k] for k in ('model', 'answers')}
            result['response_fields_omitted'] = 'Only declared model and validated native answers retained; envelope hash remains in receipt.'
        else:
            result['response_omitted'] = 'unvalidated_native_payload; envelope hash remains in receipt'
    return result


class CoordinatedPlanningProcessor:
    def __init__(self, spec: CoordinatedPlanningSpec, *, allow_external: bool,
                 planning_session_factory=CompatibleSession,
                 specialist_session_factory=DecisionSession, timer=perf_counter):
        if allow_external is not True:
            raise PermissionError('Explicit external processing permission is required')
        self.spec = CoordinatedPlanningSpec.model_validate(spec.model_dump(mode='python'))
        self.planning_session_factory = planning_session_factory
        self.specialist_session_factory = specialist_session_factory
        self.timer = timer

    def __call__(self, receipt, snapshot):
        raise PermissionError('Coordinated planning requires host authority checkpoints')

    @property
    def configuration_sha256(self):
        spec = CoordinatedPlanningSpec.model_validate(self.spec.model_dump(mode='python'))
        try:
            configuration = asdict(settings())
        except HostedSetupRequired:
            configuration = {'invalid': True}
        return digest(dict(version=VERSION, spec=spec.model_dump(mode='json'),
                           planning_settings=configuration,
                           specialist_credential=os.getenv('EXPERIENTIAL_API_KEY', '').strip(),
                           specialist_cost_policy=COST_POLICY,
                           max_generation_calls=MAX_GENERATION_CALLS,
                           max_output_tokens_per_call=MAX_OUTPUT_TOKENS,
                           max_planning_receipt_bytes=MAX_PLANNING_RECEIPT_BYTES))

    def run(self, receipt, snapshot, checkpoint):
        spec = CoordinatedPlanningSpec.model_validate(self.spec.model_dump(mode='python'))
        checkpoint()
        deadline = self.timer() + spec.max_seconds
        planning_session = None
        specialist_sessions = []

        def generate(schema, instructions, context):
            nonlocal planning_session
            checkpoint()
            if self.timer() >= deadline:
                raise CoordinationStopped('time_budget')
            if planning_session is None:
                try:
                    planning_session = self.planning_session_factory(allow_external=True)
                except HostedSetupRequired:
                    raise CoordinationStopped('planning_setup_failed') from None
            checkpoint()
            if self.timer() >= deadline:
                raise CoordinationStopped('time_budget')
            try:
                result, model = planning_session.generate(schema, instructions, context)
            except (HostedFailure, HostedSetupRequired):
                raise CoordinationStopped('planning_provider_failed') from None
            checkpoint()
            if model != planning_session.receipt.get('requested_model'):
                raise CoordinationStopped('unexpected_planning_model')
            if len(json.dumps(planning_session.receipt, ensure_ascii=False,
                              allow_nan=False).encode()) > MAX_PLANNING_RECEIPT_BYTES:
                raise CoordinationStopped('planning_receipt_budget')
            return result, model

        def specialist_factory(**kwargs):
            session = self.specialist_session_factory(**kwargs)
            specialist_sessions.append(session)
            return session

        reviewer = SpecialistReviewProcessor(spec.review, allow_external=True,
                                            session_factory=specialist_factory, timer=self.timer)

        def review(text, check):
            return reviewer.compare(text, check, deadline=deadline)

        report = coordinate(spec, receipt.event.text, 'coord_' + digest(
            receipt.model_dump(mode='json'))[:32], generate, review, checkpoint)
        checkpoint()
        if self.timer() >= deadline:
            report.update(stop_reason='time_budget', final_synthesis=None)
        report.update(kind='coordinated_planning', case_id=snapshot.id,
                      base_revision=snapshot.revision,
                      receipt_sha256=digest(receipt.model_dump(mode='json')),
                      spec_sha256=digest(spec.model_dump(mode='json')),
                      planning_receipt=_planning_receipt(planning_session),
                      specialist_receipts=[_specialist_receipt(s) for s in specialist_sessions],
                      max_output_tokens_per_planning_call=MAX_OUTPUT_TOKENS,
                      planning_cost_status='unknown_not_provider_reported',
                      charge_status='provider_billing_not_verified')
        return json.dumps(report, ensure_ascii=False, allow_nan=False)
