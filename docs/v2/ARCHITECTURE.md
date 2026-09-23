# V0.2 architecture and implemented boundaries

## Release boundary

This is a local single-operator developer application. It extends the preserved V0.1 foundation instead of replacing it with an agent framework. There is no hosted agency deployment, real tenant isolation or secure client portal. Fictional or deliberately non-confidential test material only.

## Implemented layers

`eightball/v2/contracts.py` defines versioned situation objects and source provenance. `planner.py` is deterministic planning and state interpretation. `commands.py` is the human write boundary. `store.py` applies transactional revisions, idempotency and proposal review. `intelligence.py` performs bounded advisory extraction, graph proposals, questions and classification. `playbooks.py` is a versioned human-authored registry. `services.py` constructs read models, isolated scenarios, export briefs and lineage-preserving migration. `api.py` exposes these through the same local bearer-authenticated server as the original alpha. `web/v2/` contains the real browser client.

## Situation model

A V0.2 case contains actors, relationships, reported events, source-linked claims, conditions, actions, objectives, restrictions, named resources, decisions and open questions. Evidence and observations retain the original distinction: a document can be reviewed without establishing its assertions as true. Only an operator attestation, citing a reviewed source, supports an evidenced condition. Opposite live observations are disputed until explicitly superseded. Retraction removes active support but preserves history.

Actor role, stance, authority and interests are recorded/reported attributes with provenance, not inferred personality facts. Events preserve unresolved time wording rather than inventing timestamps. Claims are not observations. Question answers and selected decisions retain their evidence and rationale; they do not automatically verify their linked conditions.

## Expressions and planning

A signed atom asks for a condition to be explicitly supported as true or false. `all` and `any` form bounded nested expressions. Unknown is not false. An OR expression can be supported by one known branch despite another unknown or disputed branch. Objective success expressions cannot be vacuous: an empty AND, or an OR containing an always-true empty branch, cannot close a case.

The engine works backwards through producers of each mandatory objective, preserving the exact prerequisites selected for each OR branch. It combines shared work, detects cyclic branches, identifies unmatched evidence conditions, then schedules candidate actions with explicit precedence. Search is capped at 64 partial candidates and 4,096 recursive expansions. Truncation and cyclic/unverified gaps remain visible. The search is not complete or globally optimal.

Forward validation applies hypothetical signed effects in chronological order and checks selected prerequisites and final mandatory goals. This catches an action that would destroy a previously required condition or final outcome. Hypothetical effects never update real observations. Actions already recorded as completed are not repeatedly scheduled as if their intended effects had occurred. If the intended result still lacks evidence, the planner exposes a verification gap.

Mandatory objectives are conjunctive. Optional objectives are evaluated and displayed separately; no hidden utility score makes them mandatory. Explicit supported failure criteria prevent the case being marked resolved. A closed case is reopened if subsequent evidence no longer supports closure.

## Time, cost, resources and restrictions

The scheduler is a deterministic greedy, capacity-one scheduler. Work assigned to one owner is serialised; independent owners can act in parallel unless they share a named resource. Resources have availability windows. Action active duration, known waiting time, earliest start and expiry affect the schedule. An unspecified wait is a lower bound, prominently labelled, not an invented completion forecast. Third-party agreement remains contingent even when arithmetic fits the deadline.

Spent plus remaining estimated costs are checked against the budget. Condition and outcome deadlines are checked. Estimates and action risk categories come from the operator, a catalogue or a proposed model draft and require review. They are not measured business statistics or probabilities of resolution.

Guards are current-evidence gates for execution. Scope-specific restrictions can have evidence predicates, confirmed manual statements, or both. Predicate requirements are checked in projected action order for planning and against live evidence for readiness. Free-text restrictions are recorded human checks, not machine-verified legal interpretation. Side effects and reversibility are disclosed metadata; possible side effects are not asserted as observed facts or calibrated causal predictions.

## Contingencies and decisions

Actions can carry accepted/refused/no-response branches, explicit condition triggers, follow-up action references and review times. Actual responses are evidenced as conditions, then the engine replans. The scenario service can assume a response to compare routes without committing it. This is not a complete stochastic contingent-policy solver. No automatic external branching execution is running.

Decision-gated actions require a specific recorded option. A contrary decision excludes a route. Missing decisions remain visible blockers. If supporting decision evidence is retracted, the decision must be reconsidered rather than silently trusted. Action approval expires after 30 minutes and is tied to the current case revision. Substantive case changes invalidate approvals. Approval-only updates preserve other current approvals without granting an external action capability.

## Intelligence and review

The default rules provider captures source sentences as claims or questions and explicitly identifies itself as non-AI. Local Ollama extraction proposes actor names, claims, reported events, possible restrictions and questions. Every extracted item must include a quotation that occurs exactly once in the authorised source set; offsets are calculated by the server. A valid span proves location, not truth or semantic entailment.

Local graph generation returns typed planning hypotheses and is validated against existing case references. Generated object IDs cannot overwrite existing objects. Models cannot create observations, approvals, selected decisions, answered questions or confirmed source facts. Every generated action starts with human approval required. Graph drafting uses a compact positive-effect wire format compiled into the full domain graph. More complex signed guards, resource assignments and contingencies can be added in the reviewed graph editor; they are not silently inferred by the small model.

Proposals are stored separately from case state. The review room defaults to rejection. Operators accept, edit or reject each item. Related objects are applied together in one transaction so rejecting a prerequisite cannot leave an accepted action with dangling references. Edits retain the model/source provenance and review history. Stale proposals cannot overwrite a case that has changed. Rejecting all items records only the model disposition and does not change the live case revision.

Jev and GLiClass remain optional bounded classifiers. Jev requires explicit external-transmission permission and server-side credentials. Ollama is fixed to loopback. A single inference slot limits concurrent local requests. Missing models, invalid output and source-forgery attempts fail closed without changing case state. Evaluation records distinguish actual inference from test doubles and from quality approval.

## Questions, changes and retrieval

Open-question ordering uses observable graph structure: routes affected, actions blocked and deadline. It is not a calibrated expected value of information. Questions may be human-authored, model-proposed or deterministically derived from unresolved conditions. An answer whose source is retracted reopens in the effective question view while its historical record remains intact.

Every committed case change records a before/after comparison at one timestamp: condition state/provenance, typed objects, graph objects, metadata, readiness, route identity/status/fingerprint, constraints, approval invalidation and leading questions. The change view reads this persisted ledger, not an LLM-generated recollection.

Retrieval is case-local lexical matching across sources and typed records, with source IDs and provenance. It does not silently search other clients, embed the entire case into every model call or train on the case archive. Semantic retrieval and governed cross-case learning are later work.

## Persistence and migration

V0.2 uses separate `v2_cases`, `v2_events`, `v2_proposals` and `v2_lineage` tables in the same local SQLite file. Original alpha tables and UI remain untouched. Legacy import verifies the original audit chain, creates a new V0.2 case, clears legacy approvals and stores the original export as lineage. Repeating the import is idempotent.

Commands execute inside a SQLite write transaction with optimistic revision and idempotency checks. Each event stores a canonical `state_after` snapshot, predecessor hash and current state hash. Export validates the hash chain and replays the recorded snapshots to the latest state. This gives exact snapshot replay, not event reduction by re-running future versions of business logic. Model-run raw output, hashes and reviewer dispositions are exported separately.

An administrator able to rewrite the database can rewrite an unanchored hash chain. This is not certified forensic custody, independent timestamping, production access logging or administrator-proof evidence storage.

## Client and execution boundary

The client brief is an operator-only preview/export that omits internal source excerpts and deliberations. It is not an authenticated account or share link. Action briefs prepare the operator for a call or task, but no email, phone call, payment or investigation is executed by the application. Authority to communicate and act remains outside the local alpha. Production security and expert/client access must be built before introducing confidential client records.
