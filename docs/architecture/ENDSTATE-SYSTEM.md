# How the system works: current implementation and future architecture

15 October 2026. Read [implemented architecture](../v2/ARCHITECTURE.md), [ENDSTATE contracts](../endstate/CONTRACTS.md) and [the PRD addendum](../strategy/ENDSTATE-VISION-ADDENDUM.md). This map distinguishes existing code from target interfaces.

## Current runtime

```text
Browser: black HTML/CSS/JavaScript workspace (web/v2)
  -> FastAPI application and local operator token (eightball/v2/api.py)
  -> reviewed commands, proposal validation and case services
  -> case-scoped SQLite persistence and revision/audit history
  -> generic ENDSTATE calculation code (endstate/)
  -> structured routes, questions, review findings and course reconsideration
  -> operator review in the same workspace
```

The default is one trusted local operator on loopback, using fictional/test cases. It is not multi-tenant agency infrastructure. ENDSTATE is an internal separately installable Python package, not an LLM, a hosted platform or an autonomous agent that executes plans.

| Current concern | Representative source |
| --- | --- |
| Objects, revisions, commands and storage | `eightball/v2/contracts.py`, `commands.py`, `store.py`, `services.py` |
| Source originals and traceable excerpts | `source_desk.py`, `source_contracts.py`, `web/v2/source-view.js` |
| Identity and deadline review | `grounding.py`, `endstate/time_review.py` |
| Model proposals and staged compilation | `intelligence.py`, `hosted.py`, `endstate/compilation.py` |
| Job lifecycle / local runtime status | `analysis_jobs.py`, `runtime_status.py` |
| Planning and result contracts | `endstate/planner.py`, `results.py`, `api.py` |
| Chosen Course | `eightball/v2/courses.py`, `endstate/course.py`, `web/v2/course-view.js` |
| Emergent Insights / Plan Review | `endstate/insights.py`, `plan_review.py`, matching 8BALL services and views |

Paths without a directory prefix in the table are under `eightball/v2/` unless explicitly prefixed.

## Current operator loop

Import or select sources -> review proposed objects -> record observations separately -> author/review an outcome graph -> calculate and compare routes -> select a course with a reason -> approve eligible work -> record completion -> collect evidence of the actual result -> recompute and reconsider.

A source import is neither model analysis nor proof. Model acceptance is not factual attestation. Action completion is not its intended effect. Candidate rank is not the chosen course. Course review is not execution authority. A synthetic scenario never mutates the live case.

## Two linked views, not two competing databases

The reality/evidence view describes actors, claims, conditions, uncertainty and provenance. The outcome/action view describes objectives, actions, prerequisites, intended effects and routes. They reference the same case identity/revision and existing records. Emergence compares their relationships to surface patterns, questions and fragility.

These are conceptual views on recorded state. Do not add an independent graph database or duplicate truth model solely to match the terminology. An Obsidian-inspired graph is an exploration interface, not proof of causation or authority.

Keep epistemic labels separate from review workflow: observed/derived/inferred/hypothetical/forecast/simulated describes a record's basis; pending/useful/investigating/dismissed/review-complete describes a human review. A useful hypothesis is not thereby a verified fact.

## Future domain boundary

```text
8BALL experience        Sales/SDR experience       Other product
        |                        |                       |
Fixer domain pack       Sales domain pack         Domain pack
        +------------------------+-----------------------+
                     ENDSTATE contracts/kernel
                                |
              optional approved adapters and services
```

Packs provide versioned vocabulary/entity mappings, permitted action templates, prerequisites, proof rules, constraints, authority policy inputs, prompts, predictor declarations and evaluation fixtures. Applications provide UX, accounts/matter access, storage configuration, billing/support and connector orchestration. Generic engine code must not import product-specific application modules or embed sales/fixer assumptions.

The current neutral/sales/support fixtures demonstrate bounded shared calculation, not a formal production pack loader or a second commercial app. Keep the monorepo while interfaces stabilise. Separate deployment, repositories or SDK distribution only when tested ownership/release requirements justify them.

## Future ingestion and replanning contract

An authorised connector normalises an incoming event, preserving original provenance and event/capture times. A case-scoped service deduplicates/orders it and proposes interpretation. Validation and the appropriate review policy determine whether a command may commit at the expected revision. That command invalidates stale authority as required, recomputes affected routes and explains the change. Decisions and selected courses retain their original basis and visible review reasons.

Real-time means bounded update latency after an event reaches the system, not omniscience or instantaneous model calls. Duplicate/reordered delivery, retries, source retraction, expired credentials, concurrent reviewers and cancelled jobs need explicit tests. Existing request-time course checks are not a background notification daemon.

## Proposed intelligence adapters

Model extraction/compilation, forecasts and rehearsals are different jobs. Share a provider-neutral envelope: purpose, case/matter scope, as-of revision, permitted input references, schema/instruction version, selected provider/model, call/time budget, external-transmission permission and audit identifiers. Outputs preserve raw response, validation errors, lineage, uncertainty and actual usage where exposed. These are future design requirements, not a claim that one current API exports every field.

A rehearsal produces isolated synthetic branches. A forecast describes an event/horizon and its calibration evidence. A deterministic planner checks feasibility under explicit inputs. The application may display all three, but must not treat simulation coverage as a probability or model persuasion as authority.

Learning is a separately permissioned evaluation/calibration pipeline, not a side effect of logging. Store outcome observations with historical cut-offs and tenant/matter boundaries. Never silently reuse one client's case for another.

## Worked example

A fictional conference lacks confirmed chairs. The fixer requests enough suitable chairs plus written venue acceptance. Existing 8BALL can preserve supplier/venue sources, record unresolved stock and approval conditions, compare authored on-site and hire routes, choose a course, approve work and require separate evidence of delivery and acceptance.

Future layers could rank a stock-availability investigation, forecast a response delay from relevant authorised history, and stress both routes against refusal or late delivery. The scenario does not make stock real; a forecast does not authorise hiring; a fallback does not relax the customer's outcome without approval. The actual Qwen graph attempt for this case failed its compiler gate, so the current app must not claim automatic reliable generation of that example.

## Security and release dependencies

The B03 production-security design remains required before confidential agency use: identity, matter-level permissions, protected source storage, client/expert projections, revocation, recovery and operational audit controls. Runtime package independence does not grant those controls. Retain existing CSP, approval checks and source isolation during every change.
