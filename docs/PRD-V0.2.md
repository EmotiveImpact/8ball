# 8BALL V0.2 implementation requirements and acceptance index

## Authority and scope

This is the repository implementation index to the accepted 37-section **8BALL V0.2 Astra PRD**, supplied in the conversation as `8BALL-V0.2-ASTRA-PRD.md`. The exact supplied reference has Git blob hash `cdaa878bcfdee65a62e2096eae085af64a5377c6`. This index does not supersede or silently remove requirements from that product vision. `docs/v2/ACCEPTANCE.md` maps implemented features to code; `docs/v2/REMAINING.md` identifies deferred or only partly validated work. A green software test is not proof of model judgement or operational effectiveness.

The current delivery is a **local, single-operator developer release**, not the full production agency service. Do not label it production-ready or introduce real confidential client cases. Main remains unchanged until an explicit, validated merge decision.

## Product outcome

A fixer supplies a messy situation and a legitimate desired outcome. 8BALL structures sources into a proposed situation model, the operator reviews it, and the engine calculates conditional routes between the current evidenced state and the desired state. New evidence changes the state, blockers, decisions and routes. The operator can inspect why.

The core loop is: situation, structure, review, define success, engineer routes, compare, authorise, perform work, observe the actual result, replan. The core product is the situation and outcome graph, not a chat transcript.

## Users and role boundaries

The case lead needs the operational model, evidence, route trade-offs, questions and a record of decisions. The agency director needs portfolio visibility, deadlines and escalations. Specialists need matter-scoped access to authorised material. Clients need a reviewed projection of status, agreed actions and next updates, not access to internal deliberation.

The local release supplies an operator workspace and an operator-only client brief preview. Actual specialist/client identities, organisation permissions and protected sharing remain production work, not hidden functionality of the local token.

## Non-negotiable invariants

1. Source existence, a claim within that source and an operator's evidence-backed observation are separate records. Reviewing a source never attests every sentence in it.
2. Unknown is not false. Opposing active observations remain disputed until explicitly reconciled. Retracted sources cease supporting live state without deleting the history.
3. Completing work does not prove that its intended effect occurred. Sending an offer is not evidence of acceptance.
4. Models propose; humans commit. A model cannot create observations, approve actions, select a human decision, resolve its own questions or execute external actions.
5. Proposals are bound to a case revision. Reviewing a subset must be atomic and preserve valid references. Stale proposals cannot overwrite newer evidence.
6. Approval is specific, expiring and revision-bound. New substantive information requires reconsideration.
7. Simulations cannot mutate live evidence, approvals, decisions or audit history.
8. No invented success probability, automatic best-route claim, cross-client retrieval or automatic confidential-data training.
9. Recorded answers and decisions cannot be erased through a generic object editor. New evidence supports an explicit revision of the answer or decision.
10. Illegal concealment, evidence destruction, intimidation, unauthorised tracking and evasion are not supported product outcomes. Professional judgement and reviewed restrictions remain essential; text constraints alone are not an automatic legal-compliance engine.

## Functional requirements

### Situation model

Maintain typed actors, organisations, relationships, reported events, source-linked claims, conditions, objectives, constraints, actions, resources, decisions and open questions. Use stable IDs and validate references within the case. Maintain provenance on model/source/playbook-derived objects. Roles, authority, interests and stance must remain labelled as recorded or reported attributes unless appropriately supported.

A condition needs a precise title and evidence-based confirmation criterion. Objectives distinguish mandatory and optional success conditions and can name failure conditions. An objective cannot be vacuously true. An action names prerequisites, intended effects, ownership, estimated time and cost, required approval, external dependency, reversibility, possible side effects and verification requirements.

### Intake and review

Allow multiple attributed text snippets, copied messages and call/document excerpts. Preserve original wording and offsets. Local extraction can propose actors, claims, events, restrictions and questions; a separate proposal drafts the outcome graph. The review interface permits accept, edit and reject, defaults to no silent acceptance, and records the disposition and model/source provenance. No accepted claim automatically becomes an attestation. Ambiguous timestamps need human resolution, not silently invented UTC times.

A manual/rules route must work when models are absent. Identify rules capture as rules, and catalogue proposals as catalogue templates. Do not pass them off as real model inference.

### Outcome planning

Support nested AND/OR prerequisites, explicit false requirements, guards, signed effects, mandatory/optional objectives, deadline and budget checks, resource windows, known and unknown waits, earliest start and expiry. Retain each selected OR branch's exact requirements. Deduplicate shared actions. Bound the search and disclose truncation.

Forward-check candidate plans for incompatible signed effects, guards violated by earlier actions, failure conditions and contradictory decision options. Show hard constraint failures rather than hiding them behind a favourable ranking. Unknown waits remain lower bounds. Another party's response is contingent even when the schedule arithmetic fits.

### Routes and the operator briefing

Find a Way Through produces Now, Next, Decisions, Questions, Routes and Watch. Allow explicit ordering by duration, cost, unresolved inputs, external dependencies, reversibility and operator-rated risk. Compare two to four routes and identify shared work. Display assumptions, source gaps, estimates, possible side effects and verification requirements. Do not treat the first sorted candidate as a validated recommendation.

### Questions and changes

Calculate question impact from graph structure: affected routes, blocked actions and deadlines. Model phrasing must not invent an expected value of information. Keep stored questions and derived verification questions distinct. Answering a question does not attest its linked condition. Retraction reopens the effective question without erasing the historical answer.

Persist revision-to-revision changes in evidence, state, objects, goals, readiness, routes, constraints and approvals. Explain route changes and leading questions using the actual before/after state, not an LLM's memory.

### Scenarios and decisions

Temporarily vary truth state, deadline, budget, action availability, resource start or a decision option. A stakeholder response is represented as an explicit hypothetical condition, not a personality forecast. Display simulation status throughout. Contingency records cover acceptance, refusal and non-response; full stochastic policy optimisation is outside this release.

Decisions record options, owner, due time, selection, rationale, evidence, timestamp and revision. Actions can require a specific option. A candidate that simultaneously requires incompatible options must fail validation.

### Playbooks and retrieval

Maintain versioned starter structures for customer retention, service recovery, supplier failure, executive communications, account compromise, travel disruption, contract dispute triage and reputation incident triage. These are reviewed starting hypotheses, not guaranteed resolutions or substitutes for qualified advice.

Retrieve case-local source-linked context. Production semantic retrieval, extensive professionally validated playbooks and governed cross-case precedent learning are later milestones. Do not silently use other clients' evidence.

### Persistence, execution and client projection

Preserve the V0.1 code and data. Import into a separate versioned case with original audit lineage, clear previous approvals and make repeat imports idempotent. Use transactions, current revisions and idempotency keys. Export evidence, snapshots, decisions, model traces and review dispositions. Snapshot replay must match the latest stored case. Hash chaining is application-level integrity, not administrator-proof forensic custody.

Prepare action/call briefs and client-status projections. No autonomous messages, calls, payments or investigation. A future external send needs recipient/content/scope, expiry, named authority, revision and idempotency controls.

## Interface requirements

Agency command, new situation intake, intake review, situation room, outcome/people/evidence maps, route comparison, action detail, evidence/claims, actor detail, timeline, decisions, questions, changes, simulation, playbooks, audit, client preview and intelligence configuration. These may be combined pages and dialogs rather than unrelated routes.

The main room must answer: what is true, where are we going, what blocks us and what happens next. Preserve accessible labels, escaped text, keyboard focus, mobile fit and explicit empty/error/loading states. A generated concept board is not proof these controls exist.

## Evaluation and definition of done

The release journey starts from a blank fictional case, captures several source excerpts, produces real model proposals where configured, reviews some with edits and rejections, accepts a valid goal/action graph and compares at least two materially different routes. Resolving an evidence gap changes the plan and its explanation. A refusal scenario changes only hypothetical state. Approval and completion leave intended effects unknown until separately evidenced. Reload and export preserve source lineage and review decisions. Desktop/mobile native browser journeys pass.

Evaluate software contracts separately from actual model requests, and actual requests separately from accuracy. Record exact model/runtime revisions, dataset identity, latency, invalid output and all failures. The classifier experiment, source extraction and graph proposals need specialist-reviewed quality evaluation before production use. Do not claim that a few engineering fixtures constitute an independent held-out quality benchmark.

## Delivery phases and production gate

Preserve the agreed phase sequence: typed model and compatibility; intelligent intake/review; richer planner; questions and changes; situation room; actual-model evaluation; production architecture. Do not expand into an autonomous agent swarm or silently replace the deterministic engine.

The next agency milestone needs authenticated identities, matter/organisation authorisation, encrypted evidence storage, secure uploads and client/expert rooms, retention and revocation, independent audit anchoring, backup recovery, observability and approved provider processing. `docs/v2/PRODUCTION-SECURITY.md` specifies the design gate. Those systems are not delivered merely by creating this document.
