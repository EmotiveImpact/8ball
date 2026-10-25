"""Versioned hypotheses and source-local precedent, never evidence or permission."""
from hashlib import sha256
import json
from typing import Annotated, Literal

from pydantic import Field, field_validator, model_validator

from endstate.contracts import Graph
from endstate.primitives import Identifier, Strict, Text, Title

Digest = Annotated[str, Field(pattern=r'^[a-f0-9]{64}$')]
Notes = Annotated[list[Title], Field(min_length=1, max_length=20)]


class KnowledgeScope(Strict):
    organisation_id: Identifier
    matter_id: Identifier
    case_id: Identifier


class KnowledgeContext(KnowledgeScope):
    actor_id: Identifier


class SourceSupport(Strict):
    source_id: Identifier
    sha256: Digest
    start: int = Field(strict=True, ge=0)
    end: int = Field(strict=True, gt=0)
    quote: Text

    @model_validator(mode='after')
    def exact_length(self):
        if self.end - self.start != len(self.quote):
            raise ValueError('Support must use exact Unicode code-point offsets')
        return self


class KnowledgeDraft(Strict):
    kind: Literal['playbook', 'precedent']
    title: Title
    summary: Text
    assumptions: Notes
    authority_requirements: Notes
    confirmation_criteria: Notes
    limitations: Notes
    sources: list[SourceSupport] = Field(default_factory=list, max_length=20)
    graph: Graph | None = None

    @field_validator('title', 'summary', 'assumptions', 'authority_requirements',
                     'confirmation_criteria', 'limitations')
    @classmethod
    def nonblank(cls, value):
        if any(not part.strip() for part in (value if isinstance(value, list) else [value])):
            raise ValueError('Review content must not be blank')
        return value

    @model_validator(mode='after')
    def complete_hypothesis(self):
        if self.kind == 'playbook' and self.graph is None:
            raise ValueError('A playbook needs an explicit graph')
        if self.kind == 'precedent' and not self.sources:
            raise ValueError('A precedent needs exact source support')
        keys = [(s.source_id, s.start, s.end) for s in self.sources]
        if len(keys) != len(set(keys)):
            raise ValueError('Duplicate source support')
        if len(self.model_dump_json().encode()) > 250000:
            raise ValueError('Knowledge draft exceeds the bounded record size')
        return self


class KnowledgeReview(Strict):
    version: int = Field(strict=True, ge=1)
    draft_sha256: Digest
    verdict: Literal['use_as_reference', 'needs_changes', 'reject']
    rationale: Text
    specialist_scope: Title

    @field_validator('rationale', 'specialist_scope')
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError('An explicit review reason and scope are required')
        return value


def content_digest(value: dict) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=False, allow_nan=False).encode()
    return sha256(encoded).hexdigest()


NOTICES = [
    'Reference hypotheses only. Review is not factual verification, action approval or proof of a successful solution.',
    'Search is bounded lexical matching in this case and matter, not semantic accuracy or cross-client learning.',
    'No graph, observation, selected course, approval or external action is changed by this workspace.',
]
