# 8BALL V0.2 PRD
## Situation Intelligence and Outcome Engineering System
**Build target:** Astra implementation handoff  
**Date:** 22 September 2026  
**Status:** Next production milestone after 0.1.0-alpha.1  
**Repository:** `EmotiveImpact/8ball`  
**Current branch:** `feat/outcome-engine-alpha`

---

# 1. EXECUTIVE VERDICT

The current 8BALL alpha proves that the product idea works technically, but it is not yet the full product.

What exists today is a credible outcome-planning foundation:

- a real Situation object
- evidence-backed condition state
- alternative routes
- prerequisite checking
- budget and deadline constraints
- human approvals
- action completion separated from outcome proof
- scenario testing
- audit history
- a working browser interface
- optional Jev, GLiClass and Ollama adapters

The missing part is the most important part of the original product idea:

> A fixer should be able to give 8BALL a messy real-world situation and have the system construct, challenge, maintain and continuously update a useful model of that situation.

Today the human still has to do too much of that modelling manually.

Therefore V0.2 is not “add more AI”.

V0.2 is:

> **Make 8BALL understand and maintain the Situation Model, then use deterministic planning plus bounded AI judgement to engineer routes from current state to desired state.**

The product should feel like a fixer’s operating system, not a task manager with an AI panel.

---

# 2. PRODUCT DEFINITION

8BALL is a **Situation Intelligence and Outcome Engineering platform** for fixers, crisis teams, agencies, private offices, operators and specialist advisers.

The operator gives the platform:

1. what is happening
2. what is known
3. what is disputed
4. who is involved
5. what outcome is wanted
6. what constraints exist
7. what actions are available

8BALL then maintains:

- the current state
- the evidence behind that state
- the people and organisations involved
- the interests and dependencies between them
- the desired outcome
- the conditions required for that outcome
- the possible routes to those conditions
- the actions required
- the consequences and contingencies of those actions
- the blockers
- the decisions requiring human approval
- what changed since the last plan

The product’s central loop is:

```text
SITUATION
   ↓
STRUCTURE
   ↓
VERIFY
   ↓
DEFINE OUTCOME
   ↓
ENGINEER ROUTES
   ↓
COMPARE
   ↓
APPROVE
   ↓
ACT
   ↓
OBSERVE
   ↓
REPLAN
```

---

# 3. PRODUCT PROMISE

The public product proposition is:

> **Tell us the situation. Define where you need to get to. 8BALL finds the way through.**

The professional product promise is more precise:

> **8BALL converts incomplete and changing case information into an evidence-linked Situation Model and produces conditional, auditable routes towards a human-defined outcome.**

It must never imply that another person’s behaviour or an external real-world outcome can be guaranteed.

---

# 4. USERS

## Primary user: Fixer / Case Lead

Needs to:

- understand the situation quickly
- find missing facts
- identify the critical people
- decide what must happen next
- compare routes
- coordinate specialists
- avoid losing important context
- understand the effect of new information
- explain the plan to the client
- preserve a decision history

## Secondary users

### Specialist
Examples:
- solicitor
- technical specialist
- crisis communications adviser
- security adviser
- accountant
- negotiator

Needs scoped access only to relevant case material.

### Agency Director
Needs:
- portfolio view
- escalations
- workload
- deadlines
- approval bottlenecks
- situation health
- audit visibility

### Client
Needs a deliberately simplified view:
- current status
- what is happening
- what is needed from them
- next milestone
- next update
- secure communication

The full internal reasoning graph should not automatically be exposed to clients.

---

# 5. V0.2 NORTH STAR

A user must be able to paste a messy fictional situation such as:

> “Our largest client has threatened to terminate following Friday’s outage. Their COO wants an incident report by noon tomorrow. Legal says we must not speculate about the root cause. Engineering thinks a database migration caused it but has not confirmed that. The customer account director says they may stay if we can guarantee remediation within seven days.”

Then 8BALL should produce a **draft Situation Model**, not a prose answer.

The draft should include:

- events
- claims
- verified facts
- unverified claims
- conflicts
- deadlines
- people
- organisations
- roles
- interests
- constraints
- desired outcome
- proposed outcome conditions
- proposed actions
- dependencies
- questions that need answering
- possible route branches
- explicit uncertainty

Nothing becomes live merely because the model generated it.

The operator reviews and accepts/rejects the proposed structure.

Only then does it enter the live case.

---

# 6. CORE DESIGN PRINCIPLES

## 6.1 The graph is the product

Chat is not the product.

The Situation Model is the product.

Every useful AI response should ultimately become one of:

- evidence
- claim
- observation
- actor
- relationship
- event
- condition
- objective
- constraint
- action
- dependency
- contingency
- risk
- decision
- question

If it cannot be represented structurally, it should not silently control the plan.

## 6.2 AI proposes, humans commit

Models can:

- extract
- classify
- summarise
- suggest
- challenge
- generate candidate graph objects
- identify possible missing information

Models cannot directly:

- mark a fact verified
- approve an action
- contact a person
- spend money
- suppress evidence
- delete audit history
- claim the final outcome occurred

## 6.3 Evidence and truth are separate concepts

A document exists.  
A claim appears inside it.  
An operator may decide that the claim supports a condition.

These are three separate things.

8BALL must preserve that separation.

## 6.4 Completion does not equal effect

“Called the client” is an action.

“Client agreed to pause termination” is an observed state.

They are not the same thing.

## 6.5 Uncertainty is visible

The system should prefer:

- unknown
- disputed
- incomplete
- contingent

over false precision.

## 6.6 Plans are conditional routes, not prophecies

Do not generate fake percentages such as “87% chance of success” unless a future validated model genuinely supports that number.

---

# 7. V0.2 SITUATION MODEL

Replace the current simple graph as the sole representation with a richer typed model.

## 7.1 Situation

Fields:

```text
id
title
client
summary
desired_outcome
status
priority
created_at
updated_at
deadline
budget
jurisdiction
confidentiality_level
owner
```

## 7.2 Actor

Represents a person, team, company, authority or external party.

Fields:

```text
id
type: person | team | organisation | authority
name
role
relationship_to_case
influence
decision_authority
stance
interests[]
known_information[]
unknown_information[]
last_contact
contact_restrictions[]
notes
```

Do not pretend inferred interests are facts. Store provenance and confidence separately.

## 7.3 Relationship

```text
from_actor
to_actor
relationship_type
strength
direction
source
status
```

Examples:

- reports_to
- advises
- controls
- depends_on
- opposes
- negotiating_with
- customer_of
- regulator_of

## 7.4 Event

Represents something that happened.

```text
id
timestamp
title
description
actors[]
source_ids[]
status: alleged | supported | disputed | confirmed
```

## 7.5 Claim

A proposition appearing in a source.

```text
id
statement
source_id
source_span
speaker
timestamp
classification
```

## 7.6 Condition

Represents something that is or must become true.

Extend current Condition:

```text
id
title
type:
  fact
  prerequisite
  target
  constraint
  external_state
  verification
status:
  unknown
  supported_true
  supported_false
  disputed
  superseded
confirmation_rule
deadline
criticality
```

## 7.7 Objective

Support multiple objectives.

```text
id
title
priority
mandatory
success_conditions[]
failure_conditions[]
```

Examples:

- retain client
- prevent additional outage
- comply with reporting deadline
- protect affected users

Do not collapse legitimate competing objectives into one score too early.

## 7.8 Constraint

```text
id
type:
  time
  budget
  legal
  policy
  authority
  resource
  communication
  privacy
  operational
description
hard_or_soft
source
```

## 7.9 Action

Extend current action:

```text
id
title
description
owner
requires[]
intended_effects[]
possible_side_effects[]
estimated_duration
estimated_cost
approval_level
reversible
external_party_required
execution_mode
verification_required
playbook_source
```

## 7.10 Decision

```text
id
question
options[]
decision_owner
needed_by
status
selected_option
rationale
case_revision
```

## 7.11 Open Question

This is critical.

```text
id
question
why_it_matters
which_routes_depend_on_it[]
best_source_or_person_to_answer
priority
status
```

8BALL should actively identify the **highest-value unanswered questions**.

---

# 8. INTELLIGENT INTAKE

Build a new intake flow.

## Step 1: Raw Situation

Allow:

- text
- pasted email
- copied chat
- call notes
- document text
- multiple source snippets

For V0.2, keep binary files optional. Text first.

## Step 2: AI Structure Draft

Generate a strict schema:

```text
actors
events
claims
deadlines
constraints
possible_objectives
open_questions
candidate_conditions
candidate_actions
```

Every extracted object should have:

```text
source_span
source_id
model
model_version
confidence/advisory_score where applicable
```

## Step 3: Review Room

The operator sees:

### ACCEPT
Object enters live Situation Model.

### EDIT
Object enters after human correction.

### REJECT
Object is discarded but optionally retained in model-trace audit.

### NEEDS EVIDENCE
Object becomes an unresolved claim/question.

No generated object silently enters the case.

## Step 4: Desired Outcome

Ask:

> Where do you need to get to?

Then:

> What would prove that this outcome had actually been achieved?

The second question forces confirmation criteria.

## Step 5: Generate Outcome Graph Draft

AI proposes:

- required target conditions
- intermediate conditions
- potential actions
- dependencies
- missing information

The deterministic engine validates the structure.

The operator accepts the draft.

---

# 9. OUTCOME GRAPH V2

The current engine supports positive action effects and conjunctive dependencies.

Upgrade it.

## Required additions

### Alternative prerequisites

Support:

```text
A AND B
A OR B
(A AND B) OR C
```

Use an explicit condition expression tree rather than encoding everything as flat lists.

### Negative and forbidden conditions

Example:

> Do not issue a public statement until legal approval exists.

### Side effects

An action may solve one problem while creating another.

Represent:

```text
intended_effects
possible_side_effects
```

Side effects must not automatically become facts. They are planning assumptions until observed.

### Reversibility

Actions should be labelled:

- reversible
- difficult to reverse
- irreversible

### Contingencies

Represent:

```text
IF customer accepts → route A
IF customer refuses → route B
IF no response by 14:00 → route C
```

### Wait states

The planner needs:

- external wait
- approval wait
- verification wait
- earliest start
- expiry

### Resource constraints

Beyond one owner at a time:

- specialist availability
- budget
- parallel work limits
- hard deadlines

Do not attempt full industrial optimisation in V0.2. Build interfaces that permit a later constraint solver.

---

# 10. ROUTE ENGINE V2

The planner should produce a `Route` object.

```text
route_id
name
goal_ids
required_conditions
actions
decisions
open_questions
contingencies
estimated_time
estimated_cost
hard_constraint_breaches
assumptions
external_dependencies
irreversible_actions
verification_requirements
```

## Route ranking

Do not call a route “best”.

Provide sortable views:

- shortest time
- lowest estimated cost
- fewest unresolved assumptions
- fewest external dependencies
- lowest operator-rated risk
- fewest irreversible actions
- highest evidence coverage

Default ordering can be deterministic, but the UI must tell the user which criterion is being used.

## Route comparison

Show two or more routes side by side.

Example:

```text
QUIET RECOVERY
Time: 8h
Cost: £2,400
External dependencies: 2
Unverified assumptions: 1
Irreversible actions: 0

FORMAL NEGOTIATION
Time: 18h
Cost: £5,200
External dependencies: 1
Unverified assumptions: 0
Irreversible actions: 1
```

No unsupported success score.

---

# 11. THE KEY FEATURE: FIND A WAY THROUGH

Create the flagship button:

# FIND A WAY THROUGH

When pressed, the system should run:

```text
1. Validate current evidence state
2. Identify disputed critical conditions
3. Identify outcome conditions
4. Generate/refresh candidate routes
5. Calculate blockers
6. Calculate unanswered questions
7. Check deadlines
8. Check budget
9. Check approvals
10. Produce operator briefing
```

The briefing should say:

## NOW
What needs immediate attention.

## NEXT
What becomes possible after current blockers are removed.

## DECISIONS
What needs human approval.

## QUESTIONS
What information would most change the available routes.

## ROUTES
Available conditional ways through.

## WATCH
Conditions that would trigger replanning.

This is more important than a general chat interface.

---

# 12. “WHAT CHANGED?” ENGINE

Every persisted case update should generate a structured delta.

Examples:

```text
New deadline discovered
Condition changed: UNKNOWN → SUPPORTED_TRUE
Condition changed: SUPPORTED_TRUE → DISPUTED
Route 01 invalidated
Route 03 became available
Action “Call COO” now needs approval
Open question “Has Legal approved language?” is now critical
```

Create a `ChangeSet`.

```text
from_revision
to_revision
changed_objects[]
newly_available_actions[]
blocked_actions[]
invalidated_routes[]
new_routes[]
new_deadline_pressure[]
new_questions[]
```

The Situation Room should open with this after meaningful changes.

---

# 13. STAKEHOLDER INTELLIGENCE

Build an actor map.

The operator should be able to click any person/organisation and see:

- role
- influence
- authority
- stated position
- known interests
- relevant evidence
- communications
- actions involving them
- decisions they control
- unresolved questions about them

AI can suggest:

> “The COO appears to control the standstill decision.”

But this must display as:

**AI PROPOSAL**
not
**FACT**

until accepted by the operator.

---

# 14. JEV ROLE

Jev should not own the plan.

Use it for bounded judgement where the output space is deliberately defined.

Good examples:

### Update classification

```text
deadline_change
new_evidence
stakeholder_response
constraint_change
routine_update
unclear
```

### Urgency

Rubric:

```text
not urgent
time sensitive
critical
```

### Relevance

Does this new source materially affect:

- current state
- deadline
- route
- stakeholder stance
- constraint

### Support check

Given one source and one proposed condition:

> Does this source explicitly support the condition?

This remains advisory unless a human attests it.

### Route review

Ask atomic questions such as:

- Does this route rely on an unverified assumption?
- Is this action controlled by an external party?
- Does this source explicitly contain a new deadline?

Do not ask Jev:

> “Solve this whole situation.”

The planner and graph own the case structure.

---

# 15. LOCAL SMALL-MODEL ROLE

Maintain a provider interface so models are replaceable.

## Recommended first generative candidate

Use a small local structured-output model for:

- entity extraction
- event extraction
- graph proposals
- open-question proposals
- source-linked claim extraction
- summarisation

The current candidate is Qwen3.5 4B through Ollama.

Do not hard-wire the product to it.

Interface:

```python
class SituationModelProvider:
    extract_objects(...)
    propose_graph(...)
    propose_questions(...)
    summarise_changes(...)
```

All returned objects must validate against strict Pydantic schemas.

## Recommended tiny classifier

Use GLiClass Edge as a local classification experiment.

Candidate use:

- message type
- case domain
- stakeholder response type
- urgency class
- routing

Do not use it for long-form planning.

## Larger models

Create adapters for an optional stronger provider, but keep the core product operational without it.

The system should record:

```text
provider
model
version
prompt/schema version
timestamp
source ids
output hash
human disposition
```

---

# 16. MODEL ROUTER

Build a simple model router.

```text
Need deterministic calculation?
→ Python engine

Need fixed-choice judgement?
→ Jev / classifier

Need extraction?
→ local generative model

Need graph proposal?
→ local generative model or configured larger model

Need final factual state?
→ evidence + human attestation
```

This routing discipline prevents the architecture from becoming an LLM agent soup.

---

# 17. PLAYBOOK SYSTEM

Turn the current hard-coded seed logic into a real playbook registry.

A Playbook contains:

```text
id
name
domain
version
description
conditions[]
actions[]
decision_templates[]
question_templates[]
route_patterns[]
safety_constraints[]
author
review_status
```

Initial playbooks:

1. Client retention after service failure
2. Service recovery
3. Supplier failure
4. Executive communications incident
5. Account compromise
6. Travel disruption
7. Contract dispute triage
8. Reputation incident triage

These should be **starting structures**, not prescriptive solutions.

The AI intake layer should search relevant playbooks and propose reusable objects.

---

# 18. CASE MEMORY AND RETRIEVAL

Within one case, build retrieval over:

- evidence
- events
- claims
- actors
- decisions
- observations
- previous plans

Do not dump the entire case into every model call.

Create a retrieval service:

```text
query
case_id
object_types
time_range
top_k
```

Return source-linked context.

Future cross-case learning should be a separate governance decision.

Do not train or retrieve across confidential clients automatically.

---

# 19. UI / UX REDESIGN TARGET

The existing visual direction is credible, but V0.2 should become more distinctive and operational.

The primary case experience should have four simultaneous mental models:

```text
WHAT IS TRUE?
WHERE ARE WE GOING?
WHAT BLOCKS US?
WHAT DO WE DO NEXT?
```

## Main Situation Room

### Header

```text
SITUATION: Northstar
STATE: Stabilising
TARGET: Retain client under recovery agreement
DEADLINE: 17h 42m
```

Primary CTA:

**FIND A WAY THROUGH**

Secondary:

**WHAT CHANGED?**  
**WHAT IF?**

### Centre: Situation Map

Interactive graph of:

- actors
- conditions
- events
- dependencies
- target

Toggle views:

- Outcome
- People
- Evidence
- Timeline

### Right Rail: NOW

Shows:

- 3 urgent actions
- 2 blocking questions
- 1 decision required
- 1 deadline risk

### Bottom: Routes

Horizontal route cards.

---

# 20. REQUIRED SCREENS

V0.2 should contain:

1. Agency Command
2. New Situation
3. AI Intake Review
4. Situation Room
5. Situation Map
6. Outcome Graph
7. Route Comparison
8. Action Detail
9. Evidence Vault
10. Actor / Organisation Detail
11. Timeline
12. Decisions
13. Open Questions
14. What Changed
15. What If / Simulation
16. Playbooks
17. Decision Trail
18. Client Brief Preview

Do not build 18 unrelated pages before the core flow works.

Priority build order:

```text
Intake Review
→ Situation Room
→ Map
→ Routes
→ Questions
→ Evidence
→ What Changed
→ Decisions
→ remaining views
```

---

# 21. OPEN QUESTIONS ENGINE

This should become a signature feature.

The system asks:

> Which unknown fact would most alter our possible routes?

For each question calculate structural importance, not fake model certainty.

Example:

```text
QUESTION
Will the customer accept a seven-day remediation window?

WHY IT MATTERS
2 of 3 routes require this condition.

HOW TO RESOLVE
Ask Account Director to confirm directly.

DEADLINE
Before 14:00.

STATUS
Unanswered.
```

Basic priority can be deterministic:

```text
number_of_routes_affected
+ number_of_actions_blocked
+ deadline_criticality
+ goal_distance
```

A model may help phrase the question, but code should calculate its graph impact.

---

# 22. SIMULATION ENGINE

Upgrade “What if?”

Allow operators to temporarily alter:

- condition state
- stakeholder stance
- deadline
- budget
- resource availability
- action availability
- external response
- constraint

Then rerun routes.

Examples:

> What if the COO refuses a standstill?

> What if engineering confirms the root cause at 11:00?

> What if legal blocks external communication?

The output must display:

**SIMULATION, NOT LIVE STATE**

and never mutate the case.

---

# 23. DECISION SYSTEM

Build explicit decisions rather than hiding them inside tasks.

Example:

```text
DECISION
Request standstill now or wait for root-cause confirmation?

OWNER
Case Lead

NEEDED BY
10:30

OPTION A
Request now

OPTION B
Wait

AFFECTED ROUTES
01 / 02 / 03

SUPPORTING EVIDENCE
4 items

OPEN QUESTIONS
1
```

Record:

- option selected
- person selecting
- time
- rationale
- revision
- evidence considered

---

# 24. EXECUTION BOUNDARY

V0.2 remains human-executed.

8BALL may prepare:

- message drafts
- call briefs
- checklists
- document outlines
- meeting agendas

But no connector should send automatically.

Future external actions need:

```text
recipient
content
scope
human approval
expiry
idempotency
audit
```

---

# 25. SAFETY BOUNDARY

8BALL should support legitimate crisis management and situation resolution.

It should not become a system for:

- destroying or concealing evidence
- deceiving investigators
- evading lawful authorities
- threatening or coercing people
- stalking or tracking people without a lawful basis
- concealing crimes
- retaliating against witnesses
- bypassing legal or platform controls

If a requested outcome or action creates one of these issues, the product should stop that path and route the operator to an appropriate lawful alternative or professional review.

---

# 26. BACKEND ARCHITECTURE

Keep the current Python core.

Suggested modules:

```text
eightball/
  domain/
    situation.py
    actor.py
    evidence.py
    graph.py
    route.py
    decision.py
    question.py

  engine/
    state.py
    graph_validator.py
    planner.py
    scheduler.py
    route_compare.py
    deltas.py
    simulation.py
    question_priority.py

  intelligence/
    router.py
    schemas.py
    intake.py
    extraction.py
    graph_proposal.py
    jev.py
    local_classifier.py
    local_llm.py
    retrieval.py

  playbooks/
    registry.py
    loader.py
    validator.py

  services/
    cases.py
    audit.py
    export.py

  api/
    cases.py
    evidence.py
    planning.py
    intelligence.py
    simulation.py
```

Do not create hundreds of files prematurely.

---

# 27. STORAGE

V0.2 may continue using SQLite locally, but structure the repository/service boundary so Postgres can replace it.

Add tables or equivalent persistent objects for:

```text
situations
actors
relationships
events
evidence
claims
observations
conditions
objectives
constraints
actions
routes
decisions
questions
model_runs
audit_events
playbooks
```

For the alpha, JSON columns may be acceptable where they reduce migration complexity, but primary relationships should have stable IDs.

---

# 28. EVENT MODEL

Every meaningful change should be a domain event.

Examples:

```text
EvidenceAdded
EvidenceReviewed
ClaimAccepted
ObservationRecorded
ActorAdded
ConditionChanged
ObjectiveChanged
ConstraintChanged
GraphProposalAccepted
ActionApproved
ActionCompleted
DecisionRecorded
SimulationRun
RouteGenerated
```

Eventually, the full case should be reconstructable from events.

V0.2 does not need perfect event sourcing, but move closer to it.

---

# 29. API CONTRACTS

Add:

```text
POST /api/cases/:id/intake/analyse
POST /api/cases/:id/intake/accept

GET  /api/cases/:id/situation-model
GET  /api/cases/:id/map

POST /api/cases/:id/plan
GET  /api/cases/:id/routes
POST /api/cases/:id/routes/compare

GET  /api/cases/:id/questions
POST /api/cases/:id/questions/:qid/resolve

GET  /api/cases/:id/changes

POST /api/cases/:id/simulate

GET  /api/playbooks
GET  /api/playbooks/:id
```

Model endpoints should return proposals, never direct mutations.

---

# 30. SECURITY BEFORE REAL CLIENT DATA

Do not call V0.2 production-ready.

Before real agency use:

- user authentication
- organisation membership
- role permissions
- tenant isolation
- encrypted storage
- secure evidence objects
- malware scanning for uploads
- retention controls
- data deletion
- audit log protection
- secrets management
- rate limiting
- backup and restore testing
- controlled model-provider data transmission
- access revocation
- expert-room permissions

The current local operator token is suitable only for the developer alpha.

---

# 31. MODEL EVALUATION SUITE

Create `evals/`.

Use fictional cases first.

Dataset should include:

- clean incident report
- contradictory sources
- missing deadline
- explicit deadline change
- stakeholder acceptance
- stakeholder refusal
- indirect language
- quoted third-party claims
- misleading instruction inside a source
- irrelevant evidence
- duplicate event
- ambiguous pronouns
- multiple actors with same surname
- changing desired outcome

Measure:

## Extraction

- precision
- recall
- invalid schema rate
- fabricated source-span rate
- duplicate-object rate

## Classification

- per-class precision/recall
- abstention rate
- false urgency rate
- missed critical update rate

## Graph proposal

Human review:

- valid dependency
- missing dependency
- unsafe dependency
- redundant condition
- invented action
- incorrect actor authority
- missing contingency

## End to end

- time for operator to reach a usable plan
- number of model corrections
- number of dangerous premature-ready actions
- amount of manual graph editing
- route changes after new evidence
- operator trust rating

---

# 32. TEST REQUIREMENTS

Maintain all existing tests.

Add tests for:

- OR dependencies
- forbidden conditions
- side-effect representation
- wait states
- contingency branches
- irreversible actions
- multiple objectives
- hard vs soft constraints
- actor relationships
- open-question priority
- new evidence invalidating routes
- disputed actor stance
- AI proposal rejection
- AI proposal edit before acceptance
- model failure fallback
- model prompt injection in evidence
- route comparison
- simulation isolation
- model run audit
- case reload
- mobile screens
- keyboard navigation

No PR should reduce evidence-state integrity to make a browser test pass.

---

# 33. DELIVERY PHASES

## PHASE 1: Situation Model V2

Build:

- new typed domain objects
- migrations
- graph expression tree
- actors
- events
- claims
- objectives
- constraints
- questions

Acceptance:

- existing 0.1 cases migrate or load through compatibility adapter
- current tests remain green
- new domain validation tests pass

## PHASE 2: Intelligent Intake

Build:

- raw situation input
- structured extraction provider
- review/accept/edit/reject UI
- source spans
- model-run logs

Acceptance:

- paste fictional case
- receive schema-valid draft
- reject all AI proposals without changing live state
- selectively accept proposals into case

## PHASE 3: Planner V2

Build:

- OR conditions
- negative/forbidden conditions
- waits
- contingencies
- side-effect metadata
- reversibility
- multi-objective support

Acceptance:

- at least three fixture situations produce structurally different valid routes
- unsupported assumptions are visible
- no route uses disputed prerequisites as verified

## PHASE 4: Questions + Change Intelligence

Build:

- open-question priority
- ChangeSet
- What Changed view
- route invalidation
- plan refresh

Acceptance:

- adding one critical source visibly alters question priority and routes
- operator sees exactly what changed and why

## PHASE 5: Situation Room V2

Build:

- new main room
- situation map
- right-rail NOW view
- route strip
- decisions
- actor detail

Acceptance:

- one screen answers:
  - where are we?
  - where are we going?
  - what blocks us?
  - what do we do next?

## PHASE 6: AI Evaluation

Run:

- Jev classification
- GLiClass comparison
- local generative model extraction
- graph proposal evaluation

Do not choose the final model before measurement.

Acceptance:

- evaluation results stored in repository
- exact model revisions recorded
- failures documented
- provider can be replaced without changing the domain engine

## PHASE 7: Production Architecture Design

Do not necessarily deploy yet.

Deliver:

- multi-tenant threat model
- auth architecture
- evidence vault design
- data handling model
- deployment plan
- migration from SQLite to Postgres

---

# 34. V0.2 DEFINITION OF DONE

V0.2 is complete when this fictional journey works:

1. Operator creates a situation.
2. Pastes several messy source snippets.
3. AI proposes actors, events, claims, deadlines and constraints.
4. Operator accepts some, edits some and rejects others.
5. Operator defines the desired outcome.
6. AI proposes the outcome conditions and candidate actions.
7. Operator accepts the graph.
8. 8BALL produces at least two materially different routes.
9. It identifies the most important unanswered questions.
10. Operator records evidence resolving one question.
11. One route changes.
12. “What Changed?” explains the delta.
13. Operator tests a hypothetical stakeholder refusal.
14. Simulation produces different routes without changing live state.
15. Operator approves an eligible action.
16. Operator records that action as completed.
17. The intended effect remains unknown until evidenced.
18. Case reload preserves everything.
19. Audit export reconstructs all important human decisions and model proposals.
20. Desktop and mobile browser tests pass.

---

# 35. NON-GOALS FOR V0.2

Do not derail this milestone with:

- autonomous phone calls
- autonomous email sending
- payment execution
- a public marketplace
- cross-client machine learning
- mobile native apps
- complex billing
- full enterprise SSO
- “success probability”
- agent swarms
- fully autonomous investigations
- dozens of niche playbooks

Those come later if justified.

---

# 36. WHAT COMES AFTER V0.2

## V0.3: Agency OS

- accounts
- organisations
- permissions
- expert rooms
- client portal
- secure evidence uploads
- notifications
- assignments
- Postgres
- background jobs
- production observability

## V0.4: Resolution Intelligence

- precedent retrieval
- playbook authoring tools
- anonymised aggregate structural learning where legally permitted
- outcome pattern analysis
- resource optimisation
- richer temporal planning
- specialist model packs

## V1

The full proposition:

> A client brings an agency a situation.
>
> The agency places the case into 8BALL.
>
> 8BALL constructs the live situation model, shows what is known and unknown, engineers the available ways through, coordinates decisions and specialists, and continuously replans until the desired state is evidenced or the objective changes.

---

# 37. ASTRA BUILD INSTRUCTION

Astra should treat the current repository as the source of truth.

Do not throw away the working 0.1 engine and rebuild a generic AI agent.

Preserve:

- evidence-linked condition state
- unknown/false/true/disputed semantics
- transactional persistence
- revision checks
- audit history
- human approvals
- completion not equalling outcome
- simulation isolation
- the deterministic planning core
- existing passing tests

Extend the architecture in the phase order above.

Before coding each phase:

1. inspect the existing models, engine, commands, API, browser client and tests
2. write the migration/compatibility strategy
3. add tests for the new domain semantics
4. implement the backend
5. integrate the UI
6. run existing and new tests
7. run native browser journeys
8. document exactly what is verified and what is still simulated

Do not claim model accuracy until an actual held-out evaluation has been run.

Do not automatically merge to `main` until the complete V0.2 acceptance journey passes.

The target is not “an AI that gives fixer advice”.

The target is:

> **A trustworthy operating system that turns a changing situation into an evidence-backed model of reality, then engineers and continuously updates the legitimate routes from that state to a human-defined outcome.**
