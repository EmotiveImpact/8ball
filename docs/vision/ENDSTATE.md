# ENDSTATE vision: evidence-linked planning and reconsideration

Revision 1.0, 24 September 2026. **Engineering direction and proposed contracts; not new exported APIs or implemented services.**

## The proposition

**ENDSTATE turns an explicit outcome, a versioned evidence snapshot, an action catalogue and constraints into conditional routes, questions and explanations. It should also help an application determine when a selected course needs reconsideration.**

8BALL is the first product and proving ground. ENDSTATE remains a neutral, testable calculation package. It does not need to become an agent swarm, an always-online cloud service or a second user-facing product to support this direction.

## Retain the boundaries that already work

Evidence-backed state, hypothetical plan effects, model proposals, operator reviews and execution permissions are separate. Unknown is not false. Completed work does not establish its effect. Every result belongs to an explicit input snapshot. Bounded search and estimated schedules do not establish feasibility outside the supplied model or predict another person's behaviour.

The host application owns identities, storage, case/matter access, model-processing permission, approvals, communications and operational jobs. ENDSTATE accepts neutral data and returns calculations; it must not silently acquire network, database, credential or execution capabilities.

## Evolving conceptual contracts

These names describe candidate responsibilities, **not** symbols currently exported by the package. Prefer extending existing typed contracts when the meaning is genuinely the same.

| Candidate responsibility | Required meaning | Kept outside the calculation kernel |
| --- | --- | --- |
| Outcome contract | Explicit success/failure conditions, optional authorised fallback, constraints, who can confirm or change the target, and any required confirmation window | Legal interpretation and granting client mandate |
| Course reference | Exact route, dependency path, target and snapshot references selected by the host's authorised operator | Selecting a route for the operator or approving execution |
| Reconsideration result | Typed reasons, affected dependencies, missing/changed inputs and a result such as needs review, unchanged within checked scope, or not established | Switching strategy or carrying forward invalidated approvals |
| Coverage record | Supplied, processed, omitted and rejected inputs, source relationships, search bounds and absent context | A universal probability of truth or assurance of completeness |
| Recovery record | Original failure, validated repair lineage and human/provider contribution | Fabricating the missing step or counting a repair as model success |

## Event-driven does not mean self-authorising

The intended loop is: preserve event, interpret, validate, review, commit a new snapshot, recompute, explain material differences, ask the authorised operator to reconsider, then observe subsequent results.

Inputs must distinguish occurrence time, receipt time, review time and explicitly declared validity or review deadlines. Unknown clocks remain unknown. Imported text carries no command authority. Duplicate and out-of-order events need deterministic handling; interrupted jobs and paid requests must not be replayed silently.

A timer without new evidence may show that a deadline or explicit review time has elapsed; it cannot invent a refusal or mark a fact false. A normalised event contract and durable host job layer remain prerequisites for a real monitoring service.

## Stable action without false reassurance

Recompute freely, but keep the operator's chosen course separate from the newest ranked alternatives. Detect changed support, constraints, decision authority, route dependencies, estimates and target revision. Expose the reasons rather than one unvalidated “confidence” score.

A complete dependency fingerprint must include everything consulted by the calculation, not only visible graph edges: policies, decision gates, resources, timestamps, catalogue version and applicable target. Missing or stale context must fail closed to review. Existing global approval invalidation must stay in place until narrower authority handling is separately designed, authorised and proven.

Plan materiality is therefore a proposed explanation capability, not permission to suppress changes or retain authorisation. If the engine can only guarantee the current snapshot, it must say that and avoid claiming a persisted course remains valid.

## Model independence means resilient degraded operation

A selected provider may time out, refuse, omit a required field or return a valid structure with the wrong meaning. Preserve that result and allow labelled human recovery. Bound correction requests; never silently switch data processors or repeat paid requests.

The authoritative calculation path remains usable with reviewed human-authored inputs. This is valuable in its own right and does not cancel the original real-model acceptance requirements for advertised AI generation.

Evaluation reports should distinguish unassisted success, human-assisted recovery, abstention, invalid output, operator rejection, transport failure and unavailable prerequisites. Count corrections and operator time as costs, not evidence that the original model was correct.

## Reuse without a generic product losing its domain

Sales, support and other domains can supply their own conditions, action catalogues, policies, confirmation rules and authorised connectors. They must not inherit 8BALL-specific claims of expertise or permissions. Use the unchanged core on small fixtures before committing to another application, API service or SDK launch.

The reusable asset is the combination of state semantics, route checking, traceable changes and recoverable decisions. It is not confidential client data. Case corrections can support opt-in replay and evaluation only under explicit retention and access policy. No automatic training or cross-client retrieval is implied.

## Proof obligations before implementation is accepted

For course/reconsideration work, test selection without approval, stale snapshots, signed and OR conditions, conflicting objectives, changes to policy/authority/resources, time-only expiry, source retraction, changed lineage, duplicate/out-of-order events, same actions with different dependency order, cancellation and failure recovery. A changed candidate ordering must not change a human decision. A favourable review must not become a factual observation.

Do not claim that no alternative exists when a search was truncated. Do not let a case-level graph imply source independence or actual actor control without an evidence-backed record. Keep domain-specific judgement with a qualified operator.

## Roadmap mapping

ES01-05 remains the package/native acceptance gate. ES02-01 through ES02-04 retain the required event, ordering, amendment and freshness work. ES02-06 is an **optional, not-started design candidate** for course/reconsideration contracts. ES03-08 records the **blocked recovery and reproduction** of the reported Draft Repair implementation. Existing ES03-01/02/05 and B02 model gates remain unchanged. No public API, production service or standalone release is authorised by this document.
