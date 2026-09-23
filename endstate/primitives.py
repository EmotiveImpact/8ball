"""Shared source/observation contracts; no application or provider dependencies."""
from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field, AwareDatetime

Identifier = Annotated[str, Field(min_length=1, max_length=80, pattern=r'^[a-zA-Z0-9_-]+$')]
Title = Annotated[str, Field(min_length=1, max_length=180)]
Text = Annotated[str, Field(min_length=1, max_length=12000)]


def uid() -> str:
    return uuid4().hex


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid', validate_assignment=True, allow_inf_nan=False)


class Evidence(Strict):
    id: Identifier = Field(default_factory=uid)
    title: Title
    source: Title
    text: Text
    status: Literal['unreviewed', 'reviewed', 'retracted'] = 'unreviewed'
    added_at: AwareDatetime = Field(default_factory=utcnow)


class Observation(Strict):
    id: Identifier = Field(default_factory=uid)
    condition_id: Identifier
    evidence_id: Identifier
    value: bool = Field(strict=True)
    rationale: Title
    supersedes: list[Identifier] = Field(default_factory=list, max_length=100)
    added_at: AwareDatetime = Field(default_factory=utcnow)
