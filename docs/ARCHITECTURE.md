# Architecture: outcomes first, models second

## Decision

Own the state machine, graph and constraints in ordinary testable code. Use models only for bounded advisory interpretation. Keep execution authority with the human operator. This avoids treating generated prose, a model confidence score or an expected action effect as a fact about the world.

```text
Browser workspace
    | bearer-authenticated local HTTP
FastAPI boundary and typed commands
    | optimistic revision check + idempotency
SQLite snapshot + transactional application event ledger
    | read validated snapshot
Evidence-supported condition state
    | backward expansion over human-authored actions
Bounded route search + greedy owner scheduling + constraint checks
    | routes / blockers / deltas
Human review, authorisation and execution outside this application

Optional, read-only side path:
Selected evidence -> Jev / local GLiClass / local Ollama -> advisory response
                                    No write capability to the case store
```

## Core objects and semantics

A Situation contains a brief, client label, desired outcome, whole-pound budget, timezone-aware deadline, graph, evidence, observations, approvals and completion records. The graph contains Conditions and Actions. Goals are condition IDs; an action has prerequisites, intended positive effects, an owner, estimated minutes/cost, an operator-authored risk category, an approval flag and a third-party contingency flag.

A source starts unreviewed. Reviewing it permits an operator to attest claims from it; reviewing the source alone changes no condition. Each observation states true or false for one existing condition and cites a source. Multiple live observations with opposing values produce `disputed`, not an averaged confidence. Explicit supersession references earlier observations of the same condition. Retracted sources stop supporting conditions. Historical entries are retained. Supersession is not automatically undone when a superseding source is retracted; uncertainty is safer than silent reinstatement.

`true` means supported by the active, operator-reviewed case record, not independently proven objective truth. There is no automatic semantic validation of an operator's attestation in this release.

Completion records that work occurred. It does not apply the action's intended effects to reality. Plans can simulate those effects conditionally while clearly distinguishing them from evidenced state. Downstream execution readiness requires actual supported prerequisites, not hypothetical route effects.

## The first planner

The engine regresses each goal through actions that could produce it, recursively resolves prerequisites and combines alternatives. Shared actions are deduplicated. Unsupported inputs remain explicit evidence gaps. Contradictions block the relevant condition. At most 64 partial alternatives survive each expansion; truncation is visible. This is a bounded heuristic search over a supplied catalogue, not unrestricted autonomous problem-solving.

For each candidate, a deterministic greedy scheduler respects prerequisite ordering and serialises work assigned to the same owner. Different owners can run in parallel. It checks the remaining schedule against outcome and condition deadlines, and completed plus planned costs against the case budget. It ranks by constraint fit, evidence gaps, highest action risk, duration and cost. Risk is supplied by the playbook author, not estimated by AI. The first route is not a probability-based recommendation or a proof of optimality.

Estimates omit unknown evidence-verification delays, working calendars, approval waiting and third-party waiting. A plan that requires a customer agreement is conditional even when its arithmetic fits. If an action was completed but its outcome was not confirmed, the route exposes a verification gap rather than endlessly repeating it automatically.

The graph currently allows only positive action effects and conjunctive prerequisites. It rejects cycles in the combined dependency graph, including some otherwise feasible alternative-path cycles. There are no negative preconditions, delete effects, stochastic transitions, negotiated utility models, independent action-failure probabilities or automatic retry loops. A false condition describes current evidence; it does not permanently prohibit trying an action intended to change that condition. Resource optimisation beyond single-owner serialisation is future work.

## Commands, approvals and changes

All changes require a typed command, case revision and idempotency key. SQLite obtains a write transaction before checking revision and applying the command. Reusing a key with different content fails. A stale revision returns 409 and cannot overwrite newer work.

Approvals are human-scoped records tied to the current case revision and eligible routes. Substantive new information invalidates outstanding approvals. Approving additional actions preserves existing approvals across the approval-only revision. Completion or evidence change requires reconsideration. No application endpoint sends a message, initiates payment or contacts a third party.

After a change the engine computes before/after condition statuses, action readiness, route identity and constraint failures at the same timestamp. The scenario endpoint clones the state, applies hypothetical constraints/conditions and returns a labelled comparison without storing events or approvals. This is scenario arithmetic, not calibrated counterfactual causal inference.

## Persistence and audit

SQLite stores the latest validated snapshot and an application-level, append-only event ledger in one transaction. Event records include local actor, command, revision, previous hash, current state hash and request hash. Export checks the chain and latest snapshot together in one read transaction. The database and local files are not a production evidence vault.

This is not yet a complete replay engine: some generated identifiers and timestamps are represented in snapshots rather than replayable domain events. An administrator able to rewrite the entire database can recompute hashes. No independent timestamp authority, external hash anchoring, qualified electronic signature, forensic chain of custody or disaster-recovery guarantee is claimed.

## Security boundary

This alpha is one trusted local operator on one device, fictional cases only. The CLI binds to 127.0.0.1. A generated or operator-supplied bearer token gates APIs; it is not an agency identity system. The browser retains the token in sessionStorage when available. Source text is escaped for rendering and treated as untrusted data by provider prompts. Strict schemas, body-size bounds, local host checks, same-origin restrictions and CSP headers are present. Local disk confidentiality still depends on the device and its protections.

No hosted deployment, multi-tenancy, roles, secure expert room, encrypted blob store, upload scanning, data residency controls, redaction guarantees, production rate limiting or authenticated client portal exists. The client brief is an operator preview/export, not a secure client account. Jev calls require explicit transmission permission and transmit one selected excerpt; Ollama is fixed to loopback. Request failures never promote model output into state.

## Production evolution

First stabilise the alpha with native-browser CI and real-model evaluation against human-labelled fictional/consented examples. Then add human-reviewed graph proposals from unstructured intake and more specialist-authored playbooks. Keep provenance and graph validation between generation and execution.

For agency trials, migrate persistence behind authenticated tenant-scoped services, introduce Postgres transactions and enforced tenant predicates/row policies, encrypted object storage, role-scoped evidence access and independently anchored audit records. Test cross-tenant denial, revocation and recovery before adding connectors. Use a durable job/workflow engine for scheduled ingestion only after idempotency, cancellation, permissions and approval gates have been proven. Any connector capable of external action needs separate, expiring authorisation for its exact recipient/content/scope.

Only after those boundaries hold should we evaluate richer contingent planning, resource constraint solvers, grounded precedent retrieval and cross-case aggregate learning. Aggregation is not automatic anonymisation: do not train on confidential agency cases without permission, data minimisation and a defensible governance process.
