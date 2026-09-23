"""8BALL V2 wire compatibility and model-review envelopes.

Shared graph/source contracts now live in ENDSTATE. Keep this import path and
Case/proposal JSON stable for existing clients, archives and audit snapshots.
"""
from __future__ import annotations
from typing import Literal, Annotated
from datetime import datetime
from pydantic import Field, AwareDatetime, model_validator
from ..models import Strict, Identifier, Title, Text, Evidence, Observation, uid, utcnow
from endstate.contracts import (
    Span, Provenance, Sourced, Actor, Relationship, Event, Claim, Expr, atom, all_of, any_of, literals, Condition, Effect, Contingency, Action, Objective, Constraint, Resource, Option, Decision, Question, Graph, Approval, Count, Status, PlanningSnapshot, validate_snapshot_relations
)


class Case(Strict):
    schema_version: Literal[2] = 2
    id: Identifier = Field(default_factory=uid)
    title: Title
    client: Title
    summary: Text
    desired_outcome: Title
    owner: Title = 'Case lead'
    status: Literal['intake','active','stabilising','monitoring','closed'] = 'intake'
    priority: Literal['ordinary','time_sensitive','critical'] = 'ordinary'
    jurisdiction: str = Field(default='', max_length=180)
    confidentiality: Literal['fictional','internal','restricted'] = 'fictional'
    deadline: AwareDatetime
    budget: Count = 10000
    graph: Graph = Field(default_factory=Graph)
    evidence: list[Evidence] = Field(default_factory=list, max_length=200)
    observations: list[Observation] = Field(default_factory=list, max_length=1000)
    actors: list[Actor] = Field(default_factory=list, max_length=80)
    relationships: list[Relationship] = Field(default_factory=list, max_length=160)
    events: list[Event] = Field(default_factory=list, max_length=200)
    claims: list[Claim] = Field(default_factory=list, max_length=200)
    constraints: list[Constraint] = Field(default_factory=list, max_length=40)
    resources: list[Resource] = Field(default_factory=list, max_length=24)
    decisions: list[Decision] = Field(default_factory=list, max_length=40)
    questions: list[Question] = Field(default_factory=list, max_length=80)
    completed: list[Identifier] = Field(default_factory=list, max_length=64)
    approvals: list[Approval] = Field(default_factory=list, max_length=64)
    next_update: AwareDatetime | None = None
    revision: int = Field(default=0, strict=True, ge=0)
    created_at: AwareDatetime = Field(default_factory=utcnow)
    updated_at: AwareDatetime = Field(default_factory=utcnow)
    legacy_id: Identifier | None = None

    @model_validator(mode='after')
    def integrity(self):
        return validate_snapshot_relations(self)


OBJECT_TYPES = {'actor':Actor,'relationship':Relationship,'event':Event,'claim':Claim,'condition':Condition,
                'action':Action,'objective':Objective,'constraint':Constraint,'resource':Resource,
                'question':Question,'decision':Decision}
COLLECTIONS = {'actor':'actors','relationship':'relationships','event':'events','claim':'claims',
               'constraint':'constraints','resource':'resources','question':'questions','decision':'decisions'}


class ProposalItem(Strict):
    id: Identifier = Field(default_factory=uid)
    kind: Literal['actor','relationship','event','claim','condition','action','objective','constraint','resource','question','decision']
    object: dict
    explanation: Title
    disposition: Literal['pending','accepted','edited','rejected'] = 'pending'

    @model_validator(mode='after')
    def typed_object(self):
        object.__setattr__(self, 'object', OBJECT_TYPES[self.kind].model_validate(self.object).model_dump(mode='json'))
        return self


class Proposal(Strict):
    id: Identifier = Field(default_factory=uid)
    case_id: Identifier
    base_revision: int = Field(strict=True, ge=0)
    provider: Title
    model: Title
    schema_version: Literal['8ball-proposal-v2'] = '8ball-proposal-v2'
    purpose: Literal['extract','graph','questions','judgement']
    source_ids: list[Identifier] = Field(default_factory=list, max_length=40)
    items: list[ProposalItem] = Field(default_factory=list, max_length=100)
    created_at: AwareDatetime = Field(default_factory=utcnow)
    output_hash: str
    latency_ms: float = Field(ge=0, allow_inf_nan=False)
    status: Literal['pending','reviewed','failed'] = 'pending'
    note: str = Field(default='', max_length=2000)
    raw_output: dict | None = None
