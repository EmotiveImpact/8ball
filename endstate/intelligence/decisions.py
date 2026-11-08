"""Bounded advisory choices. Probabilities never grant authority."""
from typing import Annotated, Literal
import math

from pydantic import Field, model_validator

from ..primitives import Identifier, Strict

Text = Annotated[str, Field(min_length=1, max_length=1500, pattern=r'\S')]
DecisionModel = Literal['jev-latest', 'clef-flash', 'gpt-6-luna-decisions']


class ChoiceQuestion(Strict):
    id: Identifier
    instructions: Text
    criteria: dict[Identifier, Text] = Field(min_length=2, max_length=8)


class DecisionInput(Strict):
    model: DecisionModel
    state: Annotated[str, Field(min_length=1, max_length=12000, pattern=r'\S')]
    questions: list[ChoiceQuestion] = Field(min_length=1, max_length=8)

    @model_validator(mode='after')
    def unique_questions(self):
        if len({q.id for q in self.questions}) != len(self.questions):
            raise ValueError('Repeated decision question')
        return self


def probability(value):
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError('Invalid reported probability')
    return value


def validate_choice(answer, question: ChoiceQuestion):
    if not isinstance(answer, dict) or set(answer) != {'type', 'choice', 'confidence', 'probabilities'} or answer['type'] != 'choice':
        raise ValueError('Unexpected decision answer')
    probabilities = answer['probabilities']
    if not isinstance(probabilities, dict) or set(probabilities) != set(question.criteria):
        raise ValueError('Decision options differ from the declared question')
    if abs(sum(probability(p) for p in probabilities.values()) - 1) > 0.0001:
        raise ValueError('Decision probabilities must sum to one')
    selected = answer['choice']
    if not isinstance(selected, str) or selected not in probabilities or probabilities[selected] < max(probabilities.values()):
        raise ValueError('Invalid selected option')
    probability(answer['confidence'])
    return {**answer, 'probabilities': dict(probabilities)}
