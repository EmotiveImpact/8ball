"""Bounded advisory comparisons, not voting, forecasting or worker scheduling."""
from typing import Literal
import math

from pydantic import Field, model_validator

from ..primitives import Identifier, Strict
from .decisions import ChoiceQuestion, DecisionModel, validate_choice

VERSION = 'endstate.specialist-review.v1'
USAGE_FIELDS = frozenset({'input_tokens', 'output_tokens', 'total_tokens',
                          'cost', 'cost_nano_usd', 'estimated_cost_nano_usd'})


class ReviewSpec(Strict):
    id: Identifier
    models: list[DecisionModel] = Field(min_length=1, max_length=3)
    questions: list[ChoiceQuestion] = Field(min_length=1, max_length=8)
    max_seconds: int = Field(strict=True, ge=1, le=180)
    max_reported_cost_nano_usd: int = Field(strict=True, ge=1)

    @model_validator(mode='after')
    def distinct(self):
        if len(set(self.models)) != len(self.models):
            raise ValueError('Select each specialist model at most once')
        if len({q.id for q in self.questions}) != len(self.questions):
            raise ValueError('Repeated specialist question')
        return self


class Attempt(Strict):
    model: DecisionModel
    status: Literal['answered', 'failed']
    answers: dict = Field(default_factory=dict)
    usage: dict = Field(default_factory=dict)
    reported_cost_nano_usd: int | None = Field(default=None, strict=True, ge=0)
    request_started: bool = Field(default=False, strict=True)
    request_sha256: str | None = Field(default=None, pattern=r'^[0-9a-f]{64}$')
    response_sha256: str | None = Field(default=None, pattern=r'^[0-9a-f]{64}$')
    served_model: str | None = Field(default=None, min_length=1, max_length=100)


def summarize(spec: ReviewSpec, attempts: list[Attempt]):
    spec = ReviewSpec.model_validate(spec.model_dump(mode='python'))
    attempts = [Attempt.model_validate(a.model_dump(mode='python')) for a in attempts]
    if [a.model for a in attempts] != spec.models[:len(attempts)]:
        raise ValueError('Attempts must follow the exact declared model order')
    if len(attempts) > len(spec.models):
        raise ValueError('Undeclared specialist attempt')
    if any(a.status == 'failed' or a.reported_cost_nano_usd is None for a in attempts[:-1]):
        raise ValueError('No further attempt after failure or unknown cost')
    if attempts and sum(a.reported_cost_nano_usd or 0 for a in attempts[:-1]) >= spec.max_reported_cost_nano_usd:
        raise ValueError('No further attempt after exhausting the reported-cost budget')
    answered = []
    for attempt in attempts:
        if attempt.status == 'failed':
            if attempt.answers:
                raise ValueError('Failed attempts cannot supply validated answers')
            continue
        if not attempt.request_started or not attempt.served_model or not attempt.request_sha256 or not attempt.response_sha256:
            raise ValueError('An answer requires an observed request and served model')
        if set(attempt.answers) != {q.id for q in spec.questions}:
            raise ValueError('Missing or unexpected specialist answer')
        usage = attempt.usage
        if set(usage) - USAGE_FIELDS or any(type(usage.get(k)) is not int or usage[k] < 0
                                          for k in ('input_tokens', 'output_tokens')):
            raise ValueError('Missing or invalid specialist token usage')
        if 'total_tokens' in usage and (type(usage['total_tokens']) is not int
                or usage['total_tokens'] != usage['input_tokens'] + usage['output_tokens']):
            raise ValueError('Inconsistent specialist token usage')
        for key in ('cost', 'cost_nano_usd', 'estimated_cost_nano_usd'):
            if key in usage:
                value = usage[key]
                try:
                    valid = type(value) in (int, float) and math.isfinite(value) and value >= 0
                except OverflowError:
                    valid = False
                if not valid:
                    raise ValueError('Invalid specialist cost metadata')
        cost = usage.get('cost_nano_usd')
        if attempt.reported_cost_nano_usd != (cost if type(cost) is int else None):
            raise ValueError('Specialist cost differs from retained usage')
        attempt.answers = {q.id: validate_choice(attempt.answers[q.id], q) for q in spec.questions}
        answered.append(attempt)
    questions = []
    for question in spec.questions:
        choices = {a.model: a.answers[question.id]['choice'] for a in answered}
        questions.append({'id': question.id, 'choices': choices,
                          'missing_models': [m for m in spec.models if m not in choices],
                          'disagreement': len(set(choices.values())) > 1})
    return {'version': VERSION, 'spec': spec.model_dump(mode='json'),
            'attempts': [a.model_dump(mode='json') for a in attempts], 'questions': questions,
            'answered_models': len(answered), 'requested_models': len(spec.models),
            'not_started_models': spec.models[len(attempts):],
            'known_reported_cost_nano_usd': sum(a.reported_cost_nano_usd or 0 for a in attempts),
            'unknown_cost_attempts': [a.model for a in attempts if a.reported_cost_nano_usd is None],
            'facts_attested': False, 'execution_authorized': False, 'advisory_only': True,
            'notice': 'Missing answers are not agreement. Choices and confidence are not votes, '
                      'approval, evidence or calibrated outcome forecasts. Reported-cost stopping '
                      'is not a provider-enforced billing cap.'}
