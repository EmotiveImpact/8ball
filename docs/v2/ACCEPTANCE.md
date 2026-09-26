# V0.2 requirement-to-implementation map

This document maps the approved PRD in `docs/PRD-V0.2.md` to actual code and deliberate boundaries. It is not an assertion that production security or model judgement has been solved.

| Requirement | Implementation / verification |
| --- | --- |
| Preserve V0.1 and migrate safely | Original modules and `/` retained. Separate V0.2 tables; lineage-preserving import in `services.py`; migration/reload tests. |
| Rich situation model | `contracts.py`: actors, relationships, events, claims, signed conditions, objectives, restrictions, actions, decisions, resources and questions. Reference and provenance tests. |
| Messy intake and review | Text evidence, `.txt` excerpt loading, rules capture or local model extraction. `intelligence.py`, proposal ledger/review in `store.py`, review UI. Accept/edit/reject and stale-proposal tests. |
| AI proposals never become facts | No observation/approval fields accepted in proposal schema. Exact quotes checked in selected sources. Attestation remains separate. Tests include fabricated spans, unknown IDs, extra privileges and vacuous objectives. |
| Novel graph proposals | Local Ollama structured graph endpoint plus explicit human-authored catalogue. Model actions require approval. Strict references; no invented proof. Live model evidence is reported separately from contract tests. |
| AND/OR and explicit false | Signed expressions, per-branch prerequisite retention, forward checking, bounded cycle handling in `planner.py`. |
| Contingencies and wait states | Accepted/refused/no-response metadata and follow-up actions, live trigger evaluation, wait lower bounds, earliest/expiry. Replan or sandbox after the actual response. Not a complete stochastic policy optimiser. |
| Restrictions, side effects, multiple goals | Hard/soft scoped predicates, signed effects, disclosed possible side effects, mandatory/optional objectives, failure/closure guard. Free-text restrictions remain manual checks. |
| Resource-aware route calculation | Owners plus capacity-one named resources, availability windows, active/wait durations, budget and deadline checks. Bounded greedy schedule, not global optimum. |
| Find a Way Through | API plan plus deterministic briefing, actual Situation Room target/map/Now/questions/routes, explicit sort criteria. |
| Open questions | Graph-impact counts, manual/AI-proposed questions, evidence-backed answers, retraction reopening. No fake information-value score. |
| What Changed | Persisted per-event deltas, evidence and graph-object changes, readiness, route fingerprints, deadlines/budget and question priority. |
| What If | Isolated clone with hypothetical conditions, budget, deadline, decisions, disabled actions and resource starts. No live writes or scenario event. Actor response is represented by an explicit condition, not inferred personality. |
| Stakeholder intelligence | Actor cards/detail/editor and declared relationship graph. Authority/stance provenance remains explicit. No autonomous profiling or tracking. |
| Decisions and approvals | Named local operator record, rationale, source IDs, required option, current revision, 30-minute action approval expiry and invalidation. No external execution. |
| Playbook registry | Eight versioned, human-authored starter structures in `playbooks.py`, browsable catalogue and reviewed template proposals. Specialist approval is not claimed. |
| Retrieval | Case-local lexical search across typed objects and sources with provenance. No cross-client retrieval/training or semantic-index claim. |
| Workspace and client view | Seventeen navigation views and focused intake/detail/review dialogs, responsive desktop/mobile. Client brief is an operator preview/export, not a secure portal. |
| Persistence and audit | Transactional revisions/idempotency, snapshot-event replay, linked hashes and exports, source lineage and model-run history. Not administrator-proof or independently anchored. |
| Evaluation | Frozen fictional classifier dataset and actual-model scripts/workflows, plus unit/API/provider-contract and browser suites. See `VALIDATION.md` for observed runs, failures and limitations. |
| Production design | `PRODUCTION-SECURITY.md` describes tenancy, OIDC, permissions, vault, retention, audit, backups and pilot acceptance. These are design deliverables, not deployed features. |

## Reproducible operator journey

Open V0.2 and the fictional Northstar case. Inspect the outcome graph and alternative routes. Add a source, review it and record a supported condition. Verify readiness changes. Record a decision with supporting sources. Approve an eligible action and record external work; its intended effect must still need separate evidence. Inspect the change trail and simulate an explicit refusal without altering the case. Open a blank case, paste several sources, run capture or configured local extraction, then accept/edit/reject items. Generate a graph proposal, review related items together, compare routes and inspect open questions. Reload and export the audit with model-run dispositions.

## Honest non-goals

No public hosted service, real client portal, tenant accounts, secure file vault, OCR, messaging connectors, autonomous phone/email/payment actions, automatic cross-client learning, causal outcome likelihoods or native mobile app is shipped. Jev requires credentials and authorised processing. Running model requests is not a validated model-quality benchmark. Refer to source-linked evaluation results rather than inferring capability from a model's size or a green CI badge.


## Additive Emergent Insights scope (alpha.4)

DOC-06 maintains the complete owner-review register; ES02-05 is the bounded deterministic detector contract. B02-21 implements the case review UI, separate history and explicit verification-question path; B02-22 is the independent usefulness/full acceptance gate. These additive items do not replace or complete the original V0.2 real-model, source interpretation or production requirements. An insight review cannot establish truth. Register adoption is not delivery verification.
