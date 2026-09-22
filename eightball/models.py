"""Strict domain contracts. Expected effects are not observed facts."""
from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field, AwareDatetime, model_validator

Identifier = Annotated[str, Field(min_length=1, max_length=80, pattern=r'^[a-zA-Z0-9_-]+$')]
Title = Annotated[str, Field(min_length=1, max_length=180)]
Text = Annotated[str, Field(min_length=1, max_length=12000)]


def uid() -> str:
    return uuid4().hex


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid', validate_assignment=True, allow_inf_nan=False)


class Condition(Strict):
    id: Identifier
    title: Title
    confirmation: Title
    due_at: AwareDatetime | None = None


class Action(Strict):
    id: Identifier
    title: Title
    owner: Title
    requires: list[Identifier] = Field(default_factory=list, max_length=15)
    produces: list[Identifier] = Field(min_length=1, max_length=10)
    minutes: int = Field(strict=True, ge=1, le=43200)
    cost: int = Field(default=0, strict=True, ge=0, le=100000000)  # whole GBP, operator estimate
    risk: Literal['low', 'medium', 'high'] = 'low'
    approval_required: bool = Field(default=False, strict=True)
    contingent: bool = Field(default=False, strict=True)  # another party/environment controls an expected effect
    purpose: Title


class Graph(Strict):
    conditions: list[Condition] = Field(min_length=1, max_length=40)
    actions: list[Action] = Field(default_factory=list, max_length=50)
    goals: list[Identifier] = Field(min_length=1, max_length=8)

    @model_validator(mode='after')
    def references_and_cycles(self):
        ids = [c.id for c in self.conditions]
        aids = [a.id for a in self.actions]
        if len(set(ids)) != len(ids) or len(set(aids)) != len(aids):
            raise ValueError('Duplicate condition or action ID')
        if len(set(self.goals)) != len(self.goals):
            raise ValueError('Duplicate goal')
        known = set(ids)
        if not set(self.goals) <= known:
            raise ValueError('Unknown goal condition')
        edges = {c: set() for c in ids}
        for action in self.actions:
            if not set(action.requires + action.produces) <= known:
                raise ValueError('Unknown action condition reference')
            if len(set(action.requires)) != len(action.requires) or len(set(action.produces)) != len(action.produces):
                raise ValueError('Repeated dependency or effect')
            for effect in action.produces:
                edges[effect].update(action.requires)
        visiting, visited = set(), set()
        def visit(node):
            if node in visiting:
                raise ValueError('Cyclic outcome graph')
            if node in visited:
                return
            visiting.add(node)
            for dep in edges[node]:
                visit(dep)
            visiting.remove(node)
            visited.add(node)
        for node in ids:
            visit(node)
        return self


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


class Situation(Strict):
    id: Identifier = Field(default_factory=uid)
    title: Title
    client: Title
    summary: Text
    desired_outcome: Title
    graph: Graph
    budget: int = Field(default=10000, strict=True, ge=0, le=100000000)
    deadline: AwareDatetime
    evidence: list[Evidence] = Field(default_factory=list, max_length=200)
    observations: list[Observation] = Field(default_factory=list, max_length=1000)
    completed: list[Identifier] = Field(default_factory=list, max_length=50)
    approvals: dict[Identifier, int] = Field(default_factory=dict)
    revision: int = Field(default=0, strict=True, ge=0)
    created_at: AwareDatetime = Field(default_factory=utcnow)

    @model_validator(mode='after')
    def integrity(self):
        conds = {c.id for c in self.graph.conditions}
        actions = {a.id for a in self.graph.actions}
        evidence = {e.id for e in self.evidence}
        if len(evidence) != len(self.evidence):
            raise ValueError('Duplicate evidence IDs')
        seen = {}
        for o in self.observations:
            if o.id in seen or o.evidence_id not in evidence or o.condition_id not in conds:
                raise ValueError('Invalid observation reference')
            if any(s not in seen or seen[s].condition_id != o.condition_id for s in o.supersedes):
                raise ValueError('Supersession must refer to an earlier observation of the same condition')
            seen[o.id] = o
        if not set(self.completed) <= actions or len(set(self.completed)) != len(self.completed):
            raise ValueError('Invalid completed actions')
        if not set(self.approvals) <= actions:
            raise ValueError('Invalid approval action')
        return self
