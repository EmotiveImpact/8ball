# Delivery checklist: 8BALL + ENDSTATE

> Generated from `docs/delivery/progress.json`. Edit the ledger, then run `python scripts/delivery.py --write`. Do not maintain a second set of statuses here.

Last status review: 2026-09-23.

**8BALL is the fixer product. ENDSTATE is the reusable engine underneath it.**

## Checkpoint and release boundary

- Active integration branch: `feat/situation-intelligence-v2`; PR #2.
- Inspected application baseline: `f87f775cb883d6914cff9230731671851a3fc660`.
- This is a dated snapshot. Refresh the branch, PR and CI at the start of every session.
- At inspection: draft PR = `true`; merged = `false`; production deployed = `false`.
- Standalone ENDSTATE package released = `false`.

## Checkbox meaning

`[x] verified` means the specific acceptance scope has linked evidence. `[ ] implemented` means code exists without complete acceptance. `partial`, `blocked`, `in_progress`, `not_started` and `deferred` remain unchecked. A failed experiment can be recorded without passing its quality gate. Counts are not product-completion percentages.

Built, verified, merged, packaged, deployed and commercially released are distinct. No model-quality claim follows from a software CI pass.

## Next work

- **B02-09: Reliable reviewed graph proposals for new situations**. Reproduce the rejected graph, evaluate a constrained multi-stage compiler/provider, and rerun the unchanged gate.
- **ES01-01: Define ENDSTATE contracts and dependency boundary**. Map existing eightball/v2 contracts and avoid a naming-only directory rewrite.

## Version summary

| Track / milestone | Required subparts verified | Acceptance scope | Release |
| --- | ---: | --- | --- |
| Governance 1.1: Naming, PRD and shared delivery control | 3/3 | Scoped gate met | not released |
| 8BALL 0.1: Local outcome-planning foundation | 3/3 | Scoped gate met | not released |
| 8BALL 0.2: Reviewed situation intelligence | 8/18 | Not yet accepted | not released |
| 8BALL 0.3: Secure agency pilot | 0/6 | Not yet accepted | not released |
| 8BALL 0.4: Professionally reviewed resolution intelligence | 0/3 | Not yet accepted | not released |
| 8BALL 1.0: Supported fixer product | 0/2 | Not yet accepted | not released |
| ENDSTATE 0.1: Reusable engine core | 0/5 | Not yet accepted | not released |
| ENDSTATE 0.2: Event-driven replanning | 0/4 | Not yet accepted | not released |
| ENDSTATE 0.3: Evaluated intelligence compilation | 0/4 | Not yet accepted | not released |
| ENDSTATE 0.4: Domain packs and integration interfaces | 0/4 | Not yet accepted | not released |
| ENDSTATE 1.0: Supported reusable engine | 0/2 | Not yet accepted | not released |

## Governance 1.1: Naming, PRD and shared delivery control

- [x] **DOC-01 Lock ENDSTATE name and fixer-first product boundary**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Accepted decision distinguishes 8BALL product, ENDSTATE engine and future applications.
  - Next: Preserve this decision in future work.
  - Evidence: `EV-DECISION` (registry below).

- [x] **DOC-02 Fold the agreed direction into PRD and preserve the original**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Master PRD incorporates naming, reuse, living plans and unchanged original acceptance requirements. Original blob hash matches.
  - Next: Use repository references instead of expecting chat access.
  - Evidence: `EV-DECISION`, `EV-ORIGINAL` (registry below).

- [x] **DOC-03 Create one evidence-linked version/subpart tracker for chat and Codex**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Ledger validates; generated checklist is current; regression checks reject unsupported completion and broken IDs.
  - Next: Use this ledger and session protocol in both chat and Codex; keep the generated checklist in sync.
  - Dependencies: `DOC-01`, `DOC-02`.
  - Existing code: `scripts/delivery.py`.
  - Evidence: `EV-TRACKING` (registry below).


## 8BALL 0.1: Local outcome-planning foundation

- [x] **B01-01 Evidence-backed local planner and outcome semantics**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Original bounded planner, supported-state distinctions and completion/effect separation satisfy the scoped alpha tests.
  - Next: Preserve this behaviour through ENDSTATE extraction.
  - Existing code: `eightball/models.py`, `eightball/engine.py`, `eightball/commands.py`.
  - Evidence: `EV-V01` (registry below).

- [x] **B01-02 Local workspace, persistence, scenarios and exports**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Original local browser workflow persists cases and exports actual audit records with isolated scenarios.
  - Next: Keep the legacy UI/data path available or migrate with verified lineage.
  - Existing code: `web/app.js`, `eightball/store.py`, `tests/browser_smoke.py`.
  - Evidence: `EV-V01` (registry below).

- [x] **B01-03 Reproducible alpha acceptance evidence**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Original 86 backend and 27 native browser results are recorded with exact code scope.
  - Next: Merge/release only through a separate explicit decision.
  - Evidence: `EV-V01` (registry below).


## 8BALL 0.2: Reviewed situation intelligence

- [x] **B02-01 Rich typed situation model and evidence provenance**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Case-scoped object IDs, source references, claims/observations and preserved historical meanings pass current tests.
  - Next: Do not change observed meanings during extraction.
  - Existing code: `eightball/v2/contracts.py`, `tests/test_v2_domain.py`.
  - Evidence: `EV-APP` (registry below).

- [x] **B02-02 Human proposal review, accept/edit/reject and stale-state protection**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Review commits selected objects atomically; no privileged facts are created; rejected/stale proposals preserve live state.
  - Next: Retain identical review guarantees for real model outputs.
  - Existing code: `eightball/v2/store.py`, `eightball/v2/intelligence.py`, `tests/test_v2_api.py`.
  - Evidence: `EV-APP`, `EV-UI` (registry below).

- [x] **B02-03 Signed AND/OR planner, guards, waits and resource estimates**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Bounded planning exposes evidence gaps, false/unknown distinctions, projected conflicts, decision incompatibilities and scheduling limits.
  - Next: Benchmark meaningful planning extensions without claiming global optimality.
  - Existing code: `eightball/v2/planner.py`, `tests/test_v2_domain.py`.
  - Evidence: `EV-APP` (registry below).

- [x] **B02-04 Actors, relationships, timeline and decision records**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Reported attributes and case decisions are represented and accessible in tested operator views. No autonomous profiling is claimed.
  - Next: Add authority/source-quality review in the model-quality work.
  - Existing code: `eightball/v2/contracts.py`, `web/v2/views.js`.
  - Evidence: `EV-APP`, `EV-UI` (registry below).

- [x] **B02-05 Questions, What Changed and isolated What If**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Graph-impact questions and recorded revision deltas operate; hypothetical state changes leave the live case unchanged.
  - Next: Connect future ingestion only through reviewed revisioned updates.
  - Existing code: `eightball/v2/planner.py`, `eightball/v2/services.py`.
  - Evidence: `EV-APP`, `EV-UI` (registry below).

- [x] **B02-06 Approvals, completion/effect separation, audit and legacy import**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Expiring approvals, protected decisions/answers, snapshot replay and lineage-preserving import satisfy current checks.
  - Next: Do not confuse local hash-chain integrity with production custody.
  - Existing code: `eightball/v2/commands.py`, `eightball/v2/store.py`, `eightball/v2/services.py`.
  - Evidence: `EV-APP` (registry below).

- [x] **B02-07 Seventeen-view local developer workspace**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Listed desktop/mobile journeys pass with real server, SQLite, native storage and downloads.
  - Next: Keep full accessibility and new model journeys as separate unchecked tasks.
  - Existing code: `web/v2/app.js`, `web/v2/views.js`, `tests/browser_v2.py`.
  - Evidence: `EV-UI` (registry below).

- [x] **B02-08 Explicit playbook registry, case-local search and brief exports**
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Eight labelled starter playbooks, lexical case search and operator-only brief exports work within the documented local scope.
  - Next: Obtain expert playbook approval in B04-01; do not claim secure client accounts.
  - Existing code: `eightball/v2/playbooks.py`, `eightball/v2/intelligence.py`, `eightball/v2/services.py`.
  - Evidence: `EV-APP`, `EV-UI` (registry below).

- [ ] **B02-09 Reliable reviewed graph proposals for new situations**
  - Status: `blocked`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Actual-model graph fixtures pass with all referenced actions present, meaningful alternative paths and explicit final verification. No silent template substitution.
  - Next: Reproduce the rejected graph, evaluate a constrained multi-stage compiler/provider, and rerun the unchanged gate.
  - Existing code: `eightball/v2/intelligence.py`, `evals/live_generation.py`.
  - Evidence: `EV-QWEN` (registry below).
  - Blocker: Latest actual Qwen graph names an absent final verification action.

- [ ] **B02-10 Robust source extraction, deadlines and entity reconciliation**
  - Status: `partial`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Reviewed multi-source extraction preserves negation, uncertainty, identity and quoted support; date changes become explicit reviewed scheduling proposals.
  - Next: Add independent cases for repeated entities, pronouns, contradictions and time resolution.
  - Existing code: `eightball/v2/intelligence.py`.
  - Evidence: `EV-QWEN`, `EV-REMAINING` (registry below).
  - Blocker: Only a few structural extraction fixtures observed; dates need operator resolution.

- [ ] **B02-11 Independent quality evaluation and production-model selection**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Expert-labelled held-out data and predeclared acceptance thresholds measure semantic errors, omissions, corrections, latency and abstention.
  - Next: Freeze evaluation criteria before choosing or tuning a production model.
  - Existing code: `evals/live_generation.py`, `evals/classification-cases.json`.
  - Evidence: `EV-REMAINING` (registry below).

- [ ] **B02-12 Full twenty-step real-model V0.2 acceptance journey**
  - Status: `blocked`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Blank case -> real extraction -> mixed human review -> valid graph -> distinct routes -> new evidence/replan -> isolated refusal -> approval/completion -> reload/export, all native.
  - Next: Add a real-model integration journey distinct from rules/catalogue browser tests.
  - Dependencies: `B02-09`, `B02-10`, `B02-11`.
  - Existing code: `tests/browser_v2.py`.
  - Evidence: `EV-QWEN`, `EV-UI` (registry below).
  - Blocker: Graph generation fails the required gate; current native journeys use rules/catalogue.

- [ ] **B02-13 Guided nested graph authoring instead of JSON-only advanced editing**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Operators can edit AND/OR, guards, contingencies and verification rules with guided controls and keyboard access.
  - Next: Design focused authoring flows while preserving the JSON compatibility path.
  - Existing code: `web/v2/forms.js`.
  - Evidence: `EV-REMAINING` (registry below).

- [ ] **B02-14 Source chunking, duplication and reviewer-safe object reconciliation**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Longer sources retain exact provenance; duplicates and entity merges cannot rewrite observed meanings or lose attribution.
  - Next: Define chunk/source version contracts and adversarial fixtures.
  - Evidence: `EV-REMAINING` (registry below).

- [ ] **B02-15 Model progress/cancellation and accurate installation status**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: The UI reports actual runtime/weights/credential state and cancels work without stale commits. No silent large model download.
  - Next: Add explicit opt-in setup and availability/cancellation checks, not a fictional green badge.
  - Dependencies: `ES03-04`.
  - Evidence: `EV-REMAINING` (registry below).

- [ ] **B02-16 Complete accessibility and supported-environment validation**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Keyboard, screen reader, empty/error/loading states and supported browsers/platform startup paths pass an explicit review.
  - Next: Audit beyond existing viewport fit and Chromium interactions.
  - Evidence: `EV-REMAINING` (registry below).

- [ ] **B02-17 Prove compatibility after ENDSTATE core extraction**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Existing 8BALL cases, imports, approvals, audits, simulations and browser flows pass through the extracted core.
  - Next: Run all legacy/V2 suites against the actual new dependency boundary.
  - Dependencies: `ES01-02`, `ES01-03`.

- [ ] **B02-18 V0.2 acceptance and release decision**
  - Status: `blocked`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: All required V0.2 subparts have scoped evidence; reviews/gates pass; approval to integrate/release is recorded separately.
  - Next: Keep PR #2 draft until the acceptance gate is met; do not infer permission to merge.
  - Dependencies: `B02-01`, `B02-02`, `B02-03`, `B02-04`, `B02-05`, `B02-06`, `B02-07`, `B02-08`, `B02-09`, `B02-10`, `B02-11`, `B02-12`, `B02-13`, `B02-14`, `B02-15`, `B02-16`, `B02-17`.
  - Evidence: `EV-QWEN` (registry below).
  - Blocker: Real-model journey and developer-quality work remain unaccepted.


## 8BALL 0.3: Secure agency pilot

- [ ] **B03-01 Identity, organisations and matter-scoped authorisation**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Authenticated identities and cross-tenant/matter denial tests cover read, write, export, search and model inference.
  - Next: Implement from the approved production threat model.
  - Evidence: `EV-SECURITY` (registry below).

- [ ] **B03-02 Encrypted evidence vault and retention controls**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Immutable originals, hashes, upload quarantine/scanning, encryption, retention/hold/deletion and audited access are tested.
  - Next: Implement without weakening source provenance.
  - Dependencies: `B03-01`.
  - Evidence: `EV-SECURITY` (registry below).

- [ ] **B03-03 Scoped specialist collaboration and real client portal**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Experts receive revocable matter/object grants; clients receive separately reviewed projections, never internal records by default.
  - Next: Build authenticated views rather than relabelling the existing preview.
  - Dependencies: `B03-01`, `B03-02`.
  - Evidence: `EV-SECURITY` (registry below).

- [ ] **B03-04 Authorised ingestion, event handling and notifications**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Actual source connectors, durable updates and notifications respect permissions, source review, ordering and retry limits.
  - Next: Build one authorised connector through ENDSTATE event contracts.
  - Dependencies: `B03-01`, `ES02-01`, `ES02-02`.
  - Evidence: `EV-SECURITY` (registry below).

- [ ] **B03-05 Independent audit checkpoints, recovery and operational monitoring**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Restore rehearsal, audit anchoring, revocation and operational incident tests pass without sensitive log leakage.
  - Next: Set measurable service/recovery targets and test them.
  - Evidence: `EV-SECURITY` (registry below).

- [ ] **B03-06 Limited qualified-fixer pilot acceptance**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Authorised pilot users validate usefulness, safety, corrections and confidentiality; critical findings closed before wider release.
  - Next: Recruit/review pilot criteria only after data and access gates pass.
  - Dependencies: `B02-18`, `B03-01`, `B03-02`, `B03-03`, `B03-04`, `B03-05`.


## 8BALL 0.4: Professionally reviewed resolution intelligence

- [ ] **B04-01 Professionally reviewed fixer and crisis playbooks**
  - Status: `partial`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Specialists approve versioned patterns, assumptions, authority and confirmation criteria; examples are not presented as proven solutions.
  - Next: Review existing starters with qualified operators.
  - Existing code: `eightball/v2/playbooks.py`.
  - Evidence: `EV-REMAINING` (registry below).

- [ ] **B04-02 Governed precedent retrieval**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Permissioned, source-linked precedent is case/matter scoped; access revocation and leakage tests pass. No automatic training.
  - Next: Agree governance and retention before indexing previous cases.
  - Dependencies: `B03-01`, `B03-02`.

- [ ] **B04-03 Measured operator benefit from richer resolution intelligence**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Held-out/pilot evidence shows useful questions and plans without unsupported causal or success-probability claims.
  - Next: Benchmark against the accepted baseline with real professional review.
  - Dependencies: `B03-06`, `B04-01`, `B04-02`.


## 8BALL 1.0: Supported fixer product

- [ ] **B10-01 Commercial onboarding, support and launch readiness**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Customer onboarding, support, service terms, brand/licence clearance and operating ownership are ready for the accepted scope.
  - Next: Define commercial acceptance with the product owner; no inferred public release.
  - Dependencies: `B03-06`.

- [ ] **B10-02 8BALL V1 fixer production release**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: All advertised capabilities, security, accessibility, recovery, model policy and customer acceptance are evidenced for supported environments.
  - Next: Record explicit release and deployment decisions after gates.
  - Dependencies: `B10-01`, `B04-03`.


## ENDSTATE 0.1: Reusable engine core

- [ ] **ES01-01 Define ENDSTATE contracts and dependency boundary**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Neutral engine inputs/outputs, version/error semantics and product/domain boundaries are documented with tests planned.
  - Next: Map existing eightball/v2 contracts and avoid a naming-only directory rewrite.
  - Existing code: `eightball/v2/contracts.py`, `eightball/v2/planner.py`.
  - Evidence: `EV-DECISION` (registry below).

- [ ] **ES01-02 Extract shared state, planning and explanation kernel**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: 8BALL calls the extracted core; the core imports no 8BALL UI, named client or fixer playbook.
  - Next: Extract incrementally, retaining compatibility adapters.
  - Dependencies: `ES01-01`.

- [ ] **ES01-03 Preserve storage, imports and audit lineage**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Old data, imports and event meanings remain readable; migrations preserve observations and expiring approval behaviour.
  - Next: Add compatibility fixtures before moving persistence boundaries.
  - Dependencies: `ES01-01`.

- [ ] **ES01-04 Prove reuse through neutral, sales and support fixtures**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: One unchanged kernel plans three domains with domain-specific actions/policies; no duplicated engine or full new app.
  - Next: Create small fictional contract tests, including opt-out and remedy-authority restrictions.
  - Dependencies: `ES01-02`, `ES01-03`.

- [ ] **ES01-05 Reusable core acceptance**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Current 8BALL suites and cross-domain fixtures pass on the proposed shared package; version compatibility is explicit.
  - Next: Accept extracted package only with exact regression evidence.
  - Dependencies: `ES01-02`, `ES01-03`, `ES01-04`.


## ENDSTATE 0.2: Event-driven replanning

- [ ] **ES02-01 Normalised event and authority contract**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Events carry source, version, occurrence/receipt time, matter scope and review status; incoming text never gets command authority.
  - Next: Define the observe/propose/review/commit/replan boundary.
  - Dependencies: `ES01-01`.

- [ ] **ES02-02 Durable ordered updates, idempotency and replay**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Duplicate, delayed, reordered and retried events cannot corrupt state or revive expired permissions.
  - Next: Implement event/outbox contracts and fault-injection tests.
  - Dependencies: `ES02-01`.

- [ ] **ES02-03 Reviewed graph amendments and affected-route explanations**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: New information can propose a graph/dependency change, but cannot remove restrictions until reviewed at the correct revision.
  - Next: Separate observed fact updates from catalogue/graph amendments.
  - Dependencies: `ES02-01`, `ES01-02`.

- [ ] **ES02-04 Freshness, cancellation and performance evidence**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Measured latencies include ingestion, inference and review; incremental replan results match full recomputation; cancelled/stale work cannot commit.
  - Next: Define target workloads and latency budgets before a real-time claim.
  - Dependencies: `ES02-02`, `ES02-03`.


## ENDSTATE 0.3: Evaluated intelligence compilation

- [ ] **ES03-01 Provider-independent reviewed outcome compiler**
  - Status: `partial`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Source interpretation, typed graph drafting and deterministic validation are clean interchangeable interfaces outside the product layer.
  - Next: Evolve existing adapters into ENDSTATE contracts without losing raw output/provenance.
  - Dependencies: `ES01-01`.
  - Existing code: `eightball/v2/intelligence.py`.
  - Evidence: `EV-APP`, `EV-QWEN` (registry below).

- [ ] **ES03-02 Shared real-model semantic acceptance**
  - Status: `blocked`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Use B02-09/B02-11/B02-12 evidence for a valid, useful source-to-plan route, not just JSON or an HTTP response.
  - Next: Resolve the 8BALL gate once and link the same evidence here.
  - Dependencies: `B02-09`, `B02-11`, `B02-12`.
  - Evidence: `EV-QWEN` (registry below).
  - Blocker: Failed real graph generation; no independent quality approval.

- [ ] **ES03-03 Optional Jev live judgement integration** (optional, not a version gate)
  - Status: `blocked`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: An authorised real TypeSafe key exercises bounded classifications; permission, output and quality checks are recorded with secrets excluded.
  - Next: Configure through a secure runtime secret mechanism only when authorised.
  - Existing code: `eightball/providers.py`.
  - Evidence: `EV-QWEN` (registry below).
  - Blocker: No authorised TypeSafe credentials supplied for live evaluation.

- [ ] **ES03-04 Local-model installation and live provider status**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Runtime, selected weights, version and connection status are actually detected; downloads are explicit and user-approved.
  - Next: Distinguish installed weights, running service, API credentials and test-run artefacts.

- [ ] **ES03-05 Failure handling, model trace and governed provider selection**
  - Status: `partial`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Provider replacement, refusal, timeout, malformed output, prompt injection and trace retention satisfy shared gates with measured quality.
  - Next: Extend existing fail-closed tests and preserve negative model results.
  - Existing code: `eightball/v2/intelligence.py`, `eightball/v2/store.py`.
  - Evidence: `EV-APP`, `EV-QWEN`, `EV-CLASSIFIER` (registry below).


## ENDSTATE 0.4: Domain packs and integration interfaces

- [ ] **ES04-01 Versioned domain-pack contract**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Domain packs supply vocabulary, object mappings, action catalogues, policies, confirmation rules, prompts and integrations without core forks.
  - Next: Derive the contract from 8BALL and adjacent fixtures.
  - Dependencies: `ES01-04`.

- [ ] **ES04-02 8BALL domain pack on ENDSTATE**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Fixer terminology/playbooks/experience are product-owned and use the shared contracts; existing routes/data remain compatible.
  - Next: Separate domain responsibilities only where real code supports the boundary.
  - Dependencies: `ES04-01`, `B02-17`.

- [ ] **ES04-03 Adjacent-domain proof and commercial-lane gate**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Sales/support examples run on the same engine with their own evaluation/permissions; new product launches need explicit approval.
  - Next: Demonstrate reuse before considering sales, service or social-client products.
  - Dependencies: `ES04-01`.

- [ ] **ES04-04 Decide and validate distribution interface**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: SDK/API/MCP options have a justified scope, auth/version contracts and consumer tests; do not declare all three products shipped.
  - Next: Choose the smallest actual integration need with the owner.
  - Dependencies: `ES04-02`, `ES04-03`.


## ENDSTATE 1.0: Supported reusable engine

- [ ] **ES10-01 Compatibility, performance, licensing and support policy**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Supported engine consumers, migrations, limits, licences and operational ownership are documented and exercised.
  - Next: Validate against real product/consumer requirements.
  - Dependencies: `ES04-04`.

- [ ] **ES10-02 ENDSTATE V1 release gate**
  - Status: `not_started`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Reusable contracts and quality/support promises have evidence; independent release approval is recorded.
  - Next: Do not block accepted 8BALL sales solely on a standalone-engine release.
  - Dependencies: `ES10-01`, `ES03-02`, `ES02-04`.

## Evidence registry

These references have specific scopes and may be historical. A reference to a design or a failed model run is not a production acceptance result.

### EV-APP

- Kind: `software_validation`.
- Repository evidence: [docs/v2/VALIDATION.md](../../docs/v2/VALIDATION.md).
- Result/scope: Recorded 221 pytest checks and native application journeys passed; exact scope in validation record.
- Code revision: `117957d3ba4475c6644ff4833d036061d8be6d2c`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35881920598).

### EV-HEAD

- Kind: `ci`.
- Repository evidence: [docs/evidence/release-verification.json](../../docs/evidence/release-verification.json).
- Result/scope: Delivery-head application CI passed. Not model-quality or production approval.
- Code revision: `f87f775cb883d6914cff9230731671851a3fc660`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35883330332).

### EV-UI

- Kind: `native_browser`.
- Repository evidence: [docs/evidence/native-v2-browser-report.json](../../docs/evidence/native-v2-browser-report.json).
- Result/scope: 51 V0.2 native checks, 17 views at desktop/mobile widths; rules/catalogue proposals, not live model quality.
- Code revision: `117957d3ba4475c6644ff4833d036061d8be6d2c`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35881920598).

### EV-V01

- Kind: `historical_software_validation`.
- Repository evidence: [docs/VALIDATION.md](../../docs/VALIDATION.md).
- Result/scope: Original scope: 86 pytest and 27 native browser checks. Local alpha, not a public service.
- Code revision: `32db6226a04f88335c3a3ae2abcb34247c1934e0`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35752284823).

### EV-QWEN

- Kind: `failed_real_model_evaluation`.
- Repository evidence: [docs/v2/AI-EVALUATION.md](../../docs/v2/AI-EVALUATION.md).
- Result/scope: Three extraction fixtures structurally valid; novel supplier graph rejected because final verification action was absent. Full graph gate failed.
- Code revision: `117957d3ba4475c6644ff4833d036061d8be6d2c`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35881916301).

### EV-CLASSIFIER

- Kind: `real_model_evaluation`.
- Repository evidence: [docs/v2/AI-EVALUATION.md](../../docs/v2/AI-EVALUATION.md).
- Result/scope: Initial GLiClass configuration: 6/30 raw top-one labels, 100% abstention. Not production-approved.
- Code revision: `fa069ca19fdbb2bff5440fb0c116be8f52f948c5`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35798129246).

### EV-REMAINING

- Kind: `scope_audit`.
- Repository evidence: [docs/v2/REMAINING.md](../../docs/v2/REMAINING.md).
- Result/scope: Recorded guided-editor, source-handling, model-quality and production work remains.
- Code revision: `f87f775cb883d6914cff9230731671851a3fc660`.

### EV-SECURITY

- Kind: `design_only`.
- Repository evidence: [docs/v2/PRODUCTION-SECURITY.md](../../docs/v2/PRODUCTION-SECURITY.md).
- Result/scope: Agency identity, vault, authorisation, revocation and recovery design; no provisioned services.
- Code revision: `f87f775cb883d6914cff9230731671851a3fc660`.

### EV-DECISION

- Kind: `user_decision`.
- Repository evidence: [docs/decisions/0001-endstate.md](../../docs/decisions/0001-endstate.md).
- Result/scope: User selected ENDSTATE; 8BALL remains the fixer application and reusable engine development supports it.

### EV-ORIGINAL

- Kind: `preserved_reference`.
- Repository evidence: [docs/reference/8BALL-V0.2-ASTRA-PRD.md](../../docs/reference/8BALL-V0.2-ASTRA-PRD.md).
- Result/scope: Exact original 37-section PRD preserved, not replaced by an abbreviated status index.
- Preserved Git blob: `cdaa878bcfdee65a62e2096eae085af64a5377c6`.

### EV-TRACKING

- Kind: `documentation_validation`.
- Repository evidence: [docs/delivery/sessions/2026-09-23-endstate-naming.md](../../docs/delivery/sessions/2026-09-23-endstate-naming.md).
- Result/scope: Documentation-only verification recorded in this session checkpoint. Not proof of a runtime feature.
