"""Versioned contracts. A source claim, a planning hypothesis and an attested state
are deliberately different types. No model response is a command.
"""
from __future__ import annotations
from typing import Literal, Annotated
from datetime import datetime
from pydantic import Field, AwareDatetime, model_validator
from ..models import Strict, Identifier, Title, Text, Evidence, Observation, uid, utcnow

Count = Annotated[int, Field(strict=True, ge=0, le=100_000_000)]
Status = Literal['unknown', 'true', 'false', 'disputed']


class Span(Strict):
    evidence_id: Identifier
    start: int = Field(strict=True, ge=0)
    end: int = Field(strict=True, ge=1)
    quote: Text

    @model_validator(mode='after')
    def ordered(self):
        if self.end <= self.start or self.end-self.start != len(self.quote):
            raise ValueError('Source span length does not match quotation')
        return self


class Provenance(Strict):
    origin: Literal['operator', 'source_claim', 'model_proposal', 'playbook', 'legacy'] = 'operator'
    references: list[Span] = Field(default_factory=list, max_length=12)
    note: str = Field(default='', max_length=2000)
    run_id: Identifier | None = None


class Sourced(Strict):
    id: Identifier = Field(default_factory=uid)
    provenance: Provenance = Field(default_factory=Provenance)


class Actor(Sourced):
    name: Title
    kind: Literal['person', 'team', 'organisation', 'authority'] = 'person'
    role: str = Field(default='', max_length=500)
    authority: str = Field(default='', max_length=1000)
    stance: str = Field(default='Not established', max_length=1000)
    interests: list[Title] = Field(default_factory=list, max_length=12)
    restrictions: list[Title] = Field(default_factory=list, max_length=12)
    last_contact: AwareDatetime | None = None
    # These are operator-recorded/reported attributes, not personality predictions.


class Relationship(Sourced):
    from_actor: Identifier
    to_actor: Identifier
    kind: Title
    note: str = Field(default='', max_length=1000)


class Event(Sourced):
    title: Title
    description: str = Field(default='', max_length=2000)
    occurred_at: AwareDatetime | None = None
    time_label: str = Field(default='Time not established', max_length=180)
    actor_ids: list[Identifier] = Field(default_factory=list, max_length=12)
    status: Literal['reported', 'disputed', 'operator_confirmed'] = 'reported'


class Claim(Sourced):
    statement: Text
    speaker_id: Identifier | None = None
    condition_id: Identifier | None = None
    status: Literal['recorded_claim', 'disputed_claim'] = 'recorded_claim'


class Expr(Strict):
    """Signed atoms; NOT is explicit false, never absence of true evidence."""
    op: Literal['atom', 'all', 'any']
    condition_id: Identifier | None = None
    value: bool = Field(default=True, strict=True)
    args: list[Expr] = Field(default_factory=list, max_length=8)

    @model_validator(mode='after')
    def shape(self):
        if self.op == 'atom':
            if not self.condition_id or self.args:
                raise ValueError('An atom needs one condition and no child expressions')
        elif self.condition_id is not None or (self.op == 'any' and not self.args):
            raise ValueError('Expression group has an invalid shape')
        def measure(e, depth=0):
            if depth > 8:
                raise ValueError('Expression depth exceeds eight')
            return 1 + sum(measure(a, depth+1) for a in e.args)
        if measure(self)>128:
            raise ValueError('Expression is too large')
        return self


def atom(cid: str, value: bool = True) -> Expr:
    return Expr(op='atom', condition_id=cid, value=value)


def all_of(*items: str | Expr) -> Expr:
    return Expr(op='all', args=[atom(i) if isinstance(i,str) else i for i in items])


def any_of(*items: str | Expr) -> Expr:
    return Expr(op='any', args=[atom(i) if isinstance(i,str) else i for i in items])


def literals(expr: Expr) -> set[tuple[str,bool]]:
    return {(expr.condition_id,expr.value)} if expr.op=='atom' else set().union(*(literals(a) for a in expr.args))


class Condition(Sourced):
    title: Title
    confirmation: Title
    kind: Literal['fact','prerequisite','target','external_state','verification'] = 'prerequisite'
    due_at: AwareDatetime | None = None
    criticality: Literal['ordinary','important','critical'] = 'ordinary'
    actor_id: Identifier | None = None


class Effect(Strict):
    condition_id: Identifier
    value: bool = Field(default=True, strict=True)


class Contingency(Strict):
    label: Title
    when: Expr
    response: Title
    next_action_ids: list[Identifier] = Field(default_factory=list, max_length=12)
    due_at: AwareDatetime | None = None


class Action(Sourced):
    title: Title
    owner: Title
    purpose: Title
    requires: Expr = Field(default_factory=lambda: all_of())
    # A guard cannot be made true by hypothesising this action's own effects.
    guard: Expr = Field(default_factory=lambda: all_of())
    effects: list[Effect] = Field(min_length=1, max_length=8)
    minutes: int = Field(strict=True, ge=1, le=43200)
    cost: Count = 0
    risk: Literal['low','medium','high'] = 'low'
    approval_required: bool = Field(default=False, strict=True)
    contingent: bool = Field(default=False, strict=True)
    wait_minutes: int | None = Field(default=0, strict=True, ge=0, le=43200)
    earliest_start: AwareDatetime | None = None
    expires_at: AwareDatetime | None = None
    reversibility: Literal['reversible','difficult','irreversible'] = 'reversible'
    side_effects: list[Title] = Field(default_factory=list, max_length=12)
    actor_ids: list[Identifier] = Field(default_factory=list, max_length=12)
    resources: list[Identifier] = Field(default_factory=list, max_length=8)
    decision_id: Identifier | None = None
    decision_option: Identifier | None = None
    enabled: bool = Field(default=True, strict=True)
    contingencies: list[Contingency] = Field(default_factory=list, max_length=8)

    @model_validator(mode='after')
    def consistent_effects(self):
        ids=[x.condition_id for x in self.effects]
        if len(ids)!=len(set(ids)):
            raise ValueError('An action cannot have repeated or contradictory effects')
        if bool(self.decision_id)!=bool(self.decision_option):
            raise ValueError('Decision gate needs both decision and option IDs')
        if self.earliest_start and self.expires_at and self.expires_at<=self.earliest_start:
            raise ValueError('Action expires before it is available')
        return self


class Objective(Sourced):
    title: Title
    mandatory: bool = Field(default=True, strict=True)
    priority: int = Field(default=1, strict=True, ge=1, le=5)
    success: Expr
    failure: Expr | None = None

    @model_validator(mode='after')
    def meaningful_target(self):
        def unconditional(e):
            if e.op == 'atom': return False
            return all(unconditional(x) for x in e.args) if e.op == 'all' else any(unconditional(x) for x in e.args)
        if not literals(self.success) or unconditional(self.success):
            raise ValueError('An objective needs non-vacuous, evidence-backed success conditions')
        if self.failure is not None and (not literals(self.failure) or unconditional(self.failure)):
            raise ValueError('An objective failure expression must name meaningful conditions')
        return self


class Constraint(Sourced):
    title: Title
    kind: Literal['time','budget','legal','policy','authority','resource','communication','privacy','operational'] = 'operational'
    hard: bool = Field(default=True, strict=True)
    # Evidence predicate necessary for eligible actions; empty action_ids applies to all.
    predicate: Expr | None = None
    action_ids: list[Identifier] = Field(default_factory=list, max_length=64)
    confirmed: bool = Field(default=False, strict=True)


class Resource(Strict):
    id: Identifier
    name: Title
    available_from: AwareDatetime | None = None
    available_until: AwareDatetime | None = None
    # Capacity-one named resources are real scheduling constraints in V0.2.


class Option(Strict):
    id: Identifier
    title: Title
    explanation: str = Field(default='', max_length=2000)


class Decision(Sourced):
    question: Title
    owner: Title
    needed_by: AwareDatetime | None = None
    options: list[Option] = Field(min_length=2, max_length=8)
    selected: Identifier | None = None
    rationale: str = Field(default='', max_length=2000)
    evidence_ids: list[Identifier] = Field(default_factory=list, max_length=20)
    decided_at: AwareDatetime | None = None
    decided_revision: int | None = None

    @model_validator(mode='after')
    def valid_choice(self):
        ids=[o.id for o in self.options]
        if len(ids)!=len(set(ids)) or (self.selected is not None and self.selected not in ids):
            raise ValueError('Invalid decision option')
        return self


class Question(Sourced):
    question: Title
    why: Title
    condition_ids: list[Identifier] = Field(default_factory=list, max_length=20)
    owner: Title = 'Case lead'
    needed_by: AwareDatetime | None = None
    answer: str = Field(default='', max_length=2000)
    evidence_ids: list[Identifier] = Field(default_factory=list, max_length=12)
    status: Literal['open','answered'] = 'open'


class Graph(Strict):
    conditions: list[Condition] = Field(default_factory=list, max_length=64)
    actions: list[Action] = Field(default_factory=list, max_length=64)
    objectives: list[Objective] = Field(default_factory=list, max_length=8)

    @model_validator(mode='after')
    def valid_graph(self):
        for objects in (self.conditions,self.actions,self.objectives):
            if len({o.id for o in objects})!=len(objects):
                raise ValueError('Duplicate graph object ID')
        known={c.id for c in self.conditions};aids={a.id for a in self.actions}
        expressions=[o.success for o in self.objectives]+[o.failure for o in self.objectives if o.failure]
        for a in self.actions:
            expressions.extend([a.requires,a.guard]);expressions.extend(b.when for b in a.contingencies)
            if any(e.condition_id not in known for e in a.effects):
                raise ValueError('Unknown action effect')
            if any(not set(b.next_action_ids)<=aids for b in a.contingencies):
                raise ValueError('Unknown contingency action')
        if any(any(cid not in known for cid,_ in literals(e)) for e in expressions):
            raise ValueError('Unknown expression condition')
        # Cycles are bounded during branch expansion, rather than banning a valid OR alternative.
        return self


class Approval(Strict):
    action_id: Identifier
    revision: int = Field(strict=True, ge=0)
    expires_at: AwareDatetime
    actor: Title


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
        groups=(self.evidence,self.observations,self.actors,self.relationships,self.events,self.claims,
                self.constraints,self.resources,self.decisions,self.questions)
        for group in groups:
            if len({o.id for o in group})!=len(group):
                raise ValueError('Duplicate case object ID')
        sources={e.id:e for e in self.evidence};actors={a.id for a in self.actors}
        conds={c.id for c in self.graph.conditions};actions={a.id for a in self.graph.actions}
        resources={r.id for r in self.resources};decisions={d.id:d for d in self.decisions}
        def spans(prov):
            for r in prov.references:
                if r.evidence_id not in sources or sources[r.evidence_id].text[r.start:r.end]!=r.quote:
                    raise ValueError('Source reference is not an exact span in this case')
        for group in (self.actors,self.relationships,self.events,self.claims,self.constraints,
                      self.decisions,self.questions,self.graph.conditions,self.graph.actions,self.graph.objectives):
            for obj in group:spans(obj.provenance)
        for rel in self.relationships:
            if rel.from_actor not in actors or rel.to_actor not in actors or rel.from_actor==rel.to_actor:
                raise ValueError('Relationship must connect two different actors in this case')
        for obj in [*self.events,*self.graph.actions]:
            if not set(obj.actor_ids)<=actors:raise ValueError('Unknown actor reference')
        for c in self.graph.conditions:
            if c.actor_id and c.actor_id not in actors:raise ValueError('Unknown condition actor')
        for claim in self.claims:
            if claim.speaker_id and claim.speaker_id not in actors:raise ValueError('Unknown claim speaker')
            if claim.condition_id and claim.condition_id not in conds:raise ValueError('Unknown claim condition')
        for a in self.graph.actions:
            if not set(a.resources)<=resources:raise ValueError('Unknown action resource')
            if a.decision_id:
                if a.decision_id not in decisions or a.decision_option not in {o.id for o in decisions[a.decision_id].options}:
                    raise ValueError('Unknown action decision or option')
        for constraint in self.constraints:
            if not set(constraint.action_ids)<=actions:raise ValueError('Unknown constrained action')
            if constraint.predicate and any(c not in conds for c,_ in literals(constraint.predicate)):
                raise ValueError('Unknown constraint condition')
        for question in self.questions:
            if not set(question.condition_ids)<=conds or not set(question.evidence_ids)<=sources.keys():
                raise ValueError('Unknown question reference')
        for decision in self.decisions:
            if not set(decision.evidence_ids)<=sources.keys():raise ValueError('Unknown decision evidence')
        seen={}
        for o in self.observations:
            if o.condition_id not in conds or o.evidence_id not in sources:
                raise ValueError('Observation references another case or missing object')
            if any(s not in seen or seen[s].condition_id!=o.condition_id for s in o.supersedes):
                raise ValueError('Supersession must target earlier observations of the same condition')
            seen[o.id]=o
        if not set(self.completed)<=actions or len(self.completed)!=len(set(self.completed)):
            raise ValueError('Invalid completed actions')
        if any(a.action_id not in actions or a.revision>self.revision for a in self.approvals):
            raise ValueError('Invalid approval scope')
        return self


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
