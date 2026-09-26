# Delivery checklist: 8BALL + ENDSTATE

> Generated from `docs/delivery/progress.json`. Edit the ledger, then run `python scripts/delivery.py --write`. Do not maintain a second set of statuses here.

Last status review: 2026-09-26.

**8BALL is the fixer product. ENDSTATE is the reusable engine underneath it.**

## Checkpoint and release boundary

- Active integration branch: `feat/situation-intelligence-v2`; PR #2.
- Inspected application baseline: `d27ad600342245d0222b5f4573da8fdcbbf8c1d4`.
- This is a dated snapshot. Refresh the branch, PR and CI at the start of every session.
- At inspection: draft PR = `true`; merged = `false`; production deployed = `false`.
- Standalone ENDSTATE package released = `false`.

## Checkbox meaning

`[x] verified` means the specific acceptance scope has linked evidence. `[ ] implemented` means code exists without complete acceptance. `partial`, `blocked`, `in_progress`, `not_started` and `deferred` remain unchecked. A failed experiment can be recorded without passing its quality gate. Counts are not product-completion percentages.

Built, verified, merged, packaged, deployed and commercially released are distinct. No model-quality claim follows from a software CI pass.

## Next work

**Unpublished development checkpoint:** Alpha.8 itself is published. This narrowly scoped Source Desk correction is prepared for verified publication; new native result remains pending. Historical local-only notes below are preserved, not current remote status.
Base: `d27ad600342245d0222b5f4573da8fdcbbf8c1d4`. See `docs/delivery/sessions/2026-09-26-source-desk-native-closeout.md`.

- **B02-14: Source chunking, duplication and reviewer-safe object reconciliation**. Publish the tested Source Desk request-order correction and run all eleven native suites; then complete the original source/identity/date or human accessibility acceptance scope. Do not introduce deferred research.
- **B02-09: Reliable reviewed graph proposals for new situations**. Apply/push the preserved local patch, run native CI and the unchanged four-case local/hosted generation gate. Target quotations and frame references are now validated early; semantic quality and live provider results remain unverified.
- **B02-11: Independent quality evaluation and production-model selection**. Obtain owner/expert approval of the declared protocol, collect independent labels and run the preserved real-model gate with an explicitly configured provider. Do not count software or operator review as independent model approval.
- **B02-12: Full twenty-step real-model V0.2 acceptance journey**. Run the actual-provider integration command with configured service/token; preserve failures and collect a genuinely human all-native journey separately. No scripted review may satisfy independent semantic acceptance.
- **B02-16: Complete accessibility and supported-environment validation**. Publish the tested Source Desk request-order correction and run all eleven native suites; then complete the original source/identity/date or human accessibility acceptance scope. Do not introduce deferred research.
- **ES01-05: Reusable core acceptance**. Inspect the installed-wheel/source/schema evidence and run the cumulative native application gate in an authorised environment before closing broad package acceptance. Do not claim a public SDK release.

## Version summary

| Track / milestone | Required subparts verified | Acceptance scope | Release |
| --- | ---: | --- | --- |
| Governance 1.1: Naming, PRD and shared delivery control | 6/6 | Scoped gate met | not released |
| 8BALL 0.1: Local outcome-planning foundation | 3/3 | Scoped gate met | not released |
| 8BALL 0.2: Reviewed situation intelligence | 9/20 | Not yet accepted | not released |
| 8BALL 0.3: Secure agency pilot | 0/6 | Not yet accepted | not released |
| 8BALL 0.4: Professionally reviewed resolution intelligence | 0/3 | Not yet accepted | not released |
| 8BALL 1.0: Supported fixer product | 0/2 | Not yet accepted | not released |
| ENDSTATE 0.1: Reusable engine core | 4/5 | Not yet accepted | not released |
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

- [x] **DOC-04 Mandatory changelog and in-app product history**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Every build adds a dated evidence-linked entry; generated CHANGELOG.md and in-app history share one source; base comparison detects missing entries or rewritten history.
  - Next: Enforce a new immutable-history changelog entry in each following session and integration commit. Local documentation/API/render scope verified; no source publication or release implied.
  - Branch/base: `work/plan-studio-jobs-changelog` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Existing code: `scripts/changelog.py`, `docs/delivery/changelog.json`, `web/v2/changelog-view.js`.
  - Evidence: `EV-PLAN-STUDIO-LOCAL` (registry below).

- [x] **DOC-05 Mandatory end-of-sprint emergence review**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Every new build sprint explicitly records what emerged, its evidence level and roadmap disposition; new changelog entries cannot omit the emergence review.
  - Next: Run the Emergence Review at every substantive build handoff; only promote discoveries to required roadmap scope through an explicit ledger or decision update.
  - Branch/base: `work/emergence-review` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `DOC-03`, `DOC-04`.
  - Existing code: `docs/delivery/EMERGENCE-REVIEW.md`, `scripts/changelog.py`, `tests/test_changelog.py`.
  - Evidence: `EV-EMERGENCE-REVIEW` (registry below).

- [x] **DOC-06 Evolving complete emergence register and owner-review prompt suite**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Every recorded discovery is retained, linked to roadmap scope, and rendered with append-only dispositions; declined items remain visible and no candidate inherits an unrelated completion tick.
  - Next: Preserve all original discoveries and append review history. Use ADR 0004 and docs/vision for the strengthened direction; no optional candidate or delivery claim becomes verified without its own evidence.
  - Branch/base: `feat/emergent-insights-local` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `DOC-05`.
  - Existing code: `scripts/emergence.py`, `docs/delivery/emergence.json`, `docs/prompts/EMERGENT-INSIGHTS.md`.
  - Evidence: `EV-EMERGENT-INSIGHTS-LOCAL`, `EV-VISION-REVIEW` (registry below).


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
  - Status: `verified`. Owner: unassigned. Updated: 2026-09-24.
  - Acceptance: Bounded planning exposes evidence gaps, false/unknown distinctions, projected conflicts, decision incompatibilities and scheduling limits.
  - Next: Retain the frozen non-colliding outputs and the dependency-order identity regression. Native cumulative integration remains separate.
  - Existing code: `eightball/v2/planner.py`, `tests/test_v2_domain.py`, `endstate/planner.py`, `tests/test_plan_review.py`.
  - Evidence: `EV-APP`, `EV-PLAN-REVIEW-LOCAL` (registry below).

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
  - Status: `blocked`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Actual-model graph fixtures pass with all referenced actions present, meaningful alternative paths and explicit final verification. No silent template substitution.
  - Next: Apply/push the preserved local patch, run native CI and the unchanged four-case local/hosted generation gate. Target quotations and frame references are now validated early; semantic quality and live provider results remain unverified.
  - Branch/base: `work/hf-black-drafting` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Existing code: `eightball/v2/intelligence.py`, `evals/live_generation.py`, `endstate/compilation.py`, `tests/test_endstate_compilation.py`.
  - Evidence: `EV-QWEN`, `EV-STAGED-CODE`, `EV-STAGED-MODEL`, `EV-HF-BLACK-LOCAL` (registry below).
  - Blocker: Actual staged Qwen run 35911570117 failed: intermediate results repeated readiness/goal conditions; invented existing-condition references and outcome confusion also remain. New hosted/target-aware development work is unpushed; no HF key or new live-model result is available.

- [ ] **B02-10 Robust source extraction, deadlines and entity reconciliation**
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Reviewed multi-source extraction preserves negation, uncertainty, identity and quoted support; date changes become explicit reviewed scheduling proposals.
  - Next: Run native integration, then evaluate multi-source identity/date workflows with reviewed professional fixtures. Preserve mention-level judgements and preview/apply boundaries; keep the source-to-plan gate unchanged.
  - Branch/base: `work/B02-10/source-clarity` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Existing code: `eightball/v2/intelligence.py`, `endstate/time_review.py`, `eightball/v2/grounding.py`, `web/v2/grounding-view.js`, `tests/test_time_review.py`, `tests/test_grounding.py`, `tests/browser_grounding.py`.
  - Evidence: `EV-QWEN`, `EV-REMAINING`, `EV-SOURCE-DESK-LOCAL`, `EV-SOURCE-CLARITY-LOCAL` (registry below).
  - Blocker: Native cumulative integration and independent multi-source identity/date usefulness review remain outstanding. No automatic coreference, global actor merge, business-calendar semantics or reliable arbitrary model extraction is claimed.

- [ ] **B02-11 Independent quality evaluation and production-model selection**
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Expert-labelled held-out data and predeclared acceptance thresholds measure semantic errors, omissions, corrections, latency and abstention.
  - Next: Obtain owner/expert approval of the declared protocol, collect independent labels and run the preserved real-model gate with an explicitly configured provider. Do not count software or operator review as independent model approval.
  - Branch/base: `work/B02-11/plan-review` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Existing code: `evals/live_generation.py`, `evals/classification-cases.json`, `endstate/plan_review.py`, `eightball/v2/plan_review.py`, `web/v2/plan-review-view.js`, `evals/plan_review_bench.py`, `evals/PLAN-QUALITY-GATE.md`, `tests/test_plan_review.py`, `tests/browser_plan_review.py`.
  - Evidence: `EV-REMAINING`, `EV-PLAN-REVIEW-LOCAL` (registry below).
  - Blocker: Independent reviewer labels, approved prospective protocol and actual-provider comparison are not completed. Local structural fixtures are not a model-quality benchmark. New cumulative native-browser acceptance remains unavailable locally.

- [ ] **B02-12 Full twenty-step real-model V0.2 acceptance journey**
  - Status: `blocked`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Blank case -> real extraction -> mixed human review -> valid graph -> distinct routes -> new evidence/replan -> isolated refusal -> approval/completion -> reload/export, all native.
  - Next: Run the actual-provider integration command with configured service/token; preserve failures and collect a genuinely human all-native journey separately. No scripted review may satisfy independent semantic acceptance.
  - Branch/base: `work/acceptance/integration-alpha7` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `B02-09`, `B02-10`, `B02-11`.
  - Existing code: `tests/browser_v2.py`, `evals/full_journey.py`, `scripts/acceptance.py`, `.github/workflows/provider-journey.yml`.
  - Evidence: `EV-QWEN`, `EV-UI`, `EV-STAGED-MODEL`, `EV-INTEGRATION-LOCAL`, `EV-INTEGRATION-BLOCKED` (registry below).
  - Blocker: Both legacy and staged graph generation still fail the required actual-model gate; native application journeys use rules/catalogue, not the full real-model flow. No running local model, authorised HF configuration or native browser navigation in the current environment. The new journey is implemented but has not made an actual inference call.

- [ ] **B02-13 Guided nested graph authoring instead of JSON-only advanced editing**
  - Status: `implemented`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Operators can edit AND/OR, guards, contingencies and verification rules with guided controls and keyboard access.
  - Next: Run the existing authoring and new live-plan review journeys under native CI after authorised cumulative integration.
  - Branch/base: `work/plan-studio-jobs-changelog` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Existing code: `web/v2/studio-model.js`, `web/v2/studio-view.js`, `eightball/v2/authoring.py`, `tests/test_plan_studio.py`, `tests/test_studio_model.py`, `tests/browser_studio.py`, `web/v2/plan-review-view.js`.
  - Evidence: `EV-REMAINING`, `EV-PLAN-STUDIO-LOCAL`, `EV-PLAN-REVIEW-LOCAL` (registry below).
  - Blocker: Native browser CI and authorised source integration have not been run for this local checkpoint.

- [ ] **B02-14 Source chunking, duplication and reviewer-safe object reconciliation**
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-26.
  - Acceptance: Longer sources retain exact provenance; duplicates and entity merges cannot rewrite observed meanings or lose attribution.
  - Next: Publish the tested Source Desk request-order correction and run all eleven native suites; then complete the original source/identity/date or human accessibility acceptance scope. Do not introduce deferred research.
  - Branch/base: `feat/situation-intelligence-v2` / `d27ad600342245d0222b5f4573da8fdcbbf8c1d4`.
  - Existing code: `eightball/v2/source_contracts.py`, `eightball/v2/source_desk.py`, `eightball/v2/request_limits.py`, `web/v2/source-model.js`, `web/v2/source-view.js`, `tests/test_source_desk.py`, `tests/test_source_api.py`, `tests/browser_sources.py`, `endstate/time_review.py`, `eightball/v2/grounding.py`, `web/v2/grounding-view.js`, `tests/test_time_review.py`, `tests/test_grounding.py`, `tests/browser_grounding.py`, `tests/test_source_view_races.py`.
  - Evidence: `EV-REMAINING`, `EV-SOURCE-DESK-LOCAL`, `EV-SOURCE-CLARITY-LOCAL`, `EV-SOURCE-SEARCH-RACE` (registry below).
  - Blocker: Native cumulative integration and independent multi-source identity/date usefulness review remain outstanding. No automatic coreference, global actor merge, business-calendar semantics or reliable arbitrary model extraction is claimed.

- [ ] **B02-15 Model progress/cancellation and accurate installation status**
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: The UI reports actual runtime/weights/credential state and cancels work without stale commits. No silent large model download.
  - Next: Run native CI after authorised integration and validate lifecycle behaviour with the selected real provider. Cancellation suppresses later stages/publication; it cannot recall in-flight provider compute.
  - Branch/base: `work/plan-studio-jobs-changelog` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `ES03-04`.
  - Existing code: `eightball/v2/analysis_jobs.py`, `web/v2/job-view.js`, `tests/test_analysis_jobs.py`.
  - Evidence: `EV-REMAINING`, `EV-HF-BLACK-LOCAL`, `EV-PLAN-STUDIO-LOCAL` (registry below).
  - Blocker: Native browser CI and authorised source integration have not been run for this local checkpoint.

- [ ] **B02-16 Complete accessibility and supported-environment validation**
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-26.
  - Acceptance: Keyboard, screen reader, empty/error/loading states and supported browsers/platform startup paths pass an explicit review.
  - Next: Publish the tested Source Desk request-order correction and run all eleven native suites; then complete the original source/identity/date or human accessibility acceptance scope. Do not introduce deferred research.
  - Branch/base: `feat/situation-intelligence-v2` / `d27ad600342245d0222b5f4573da8fdcbbf8c1d4`.
  - Existing code: `tests/browser_accessibility.py`, `web/v2/ui.js`, `web/v2/app.js`, `web/v2/style.css`, `scripts/acceptance.py`.
  - Evidence: `EV-REMAINING`, `EV-HF-BLACK-LOCAL`, `EV-GRAPH-EXPLORER-LOCAL`, `EV-INTEGRATION-LOCAL`, `EV-INTEGRATION-BLOCKED`, `EV-SOURCE-SEARCH-RACE` (registry below).
  - Blocker: Native browser policy and human screen-reader/OS validation remain outstanding.

- [x] **B02-17 Prove compatibility after ENDSTATE core extraction**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Existing 8BALL cases, imports, approvals, audits, simulations and browser flows pass through the extracted core.
  - Next: Preserve the extraction baseline and rerun all legacy/V2 suites for subsequent core changes.
  - Branch/base: `feat/situation-intelligence-v2` / `5e2098e9cb12251592eb3889ce7926798484699d`.
  - Dependencies: `ES01-02`, `ES01-03`.
  - Existing code: `tests/test_endstate_kernel.py`, `tests/browser_v2.py`, `tests/browser_smoke.py`.
  - Evidence: `EV-KERNEL` (registry below).

- [ ] **B02-18 V0.2 acceptance and release decision**
  - Status: `blocked`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: All required V0.2 subparts have scoped evidence; reviews/gates pass; approval to integrate/release is recorded separately.
  - Next: Keep PR #2 draft until the acceptance gate is met; do not infer permission to merge.
  - Dependencies: `B02-01`, `B02-02`, `B02-03`, `B02-04`, `B02-05`, `B02-06`, `B02-07`, `B02-08`, `B02-09`, `B02-10`, `B02-11`, `B02-12`, `B02-13`, `B02-14`, `B02-15`, `B02-16`, `B02-17`, `B02-19`, `B02-20`.
  - Evidence: `EV-QWEN` (registry below).
  - Blocker: Real-model journey and developer-quality work remain unaccepted.

- [ ] **B02-19 Black operator visual system and transparent intelligence controls**
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Black/graphite design, legible status labels, exact-target review, provider controls and mobile lock work across the existing native desktop/mobile workflow without losing evidence/approval functions.
  - Next: Integrate the cumulative local build and run all six native browser suites; complete visual/accessibility review before accepting the expanded scope.
  - Branch/base: `work/hf-black-drafting` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `B02-07`.
  - Existing code: `web/v2/style.css`, `web/v2/views.js`, `web/v2/forms.js`, `tests/browser_development.py`.
  - Evidence: `EV-HF-BLACK-LOCAL`, `EV-GRAPH-EXPLORER-LOCAL` (registry below).
  - Blocker: Local Chromium bridge checks passed; current native verification awaits a successful source push.

- [ ] **B02-20 Black relationship explorer with local focus, directed flow and records view**
  - Status: `implemented`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Explore actual case records using Connections, Outcome flow and Records; inspect source/history and exact logic; keyboard/mobile controls and view-only audit invariants pass, including native browser validation.
  - Next: Integrate the cumulative patch after reviewing the exact remote base, run all four native browser suites, then review accessibility and realistic dense-case usability before accepting the scoped task.
  - Branch/base: `work/B02-20/relationship-explorer` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `B02-04`, `B02-07`, `B02-19`.
  - Existing code: `web/v2/graph-model.js`, `web/v2/graph-view.js`, `web/v2/views.js`, `web/v2/app.js`, `web/v2/style.css`, `tests/browser_v2.py`, `tests/browser_graph.py`, `tests/test_graph_explorer.py`, `scripts/design_preview.py`.
  - Evidence: `EV-GRAPH-EXPLORER-LOCAL` (registry below).
  - Blocker: Native browser CI remains pending; code is only in the local checkpoint.

- [ ] **B02-21 Evidence-linked Emergent Insights and review workspace** (optional, not a version gate)
  - Status: `implemented`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Current/historical findings, explicit review and hypotheses, safe question promotion, stale-context handling, reload/export and native desktop/mobile acceptance without changing factual state.
  - Next: Integrate the cumulative source through the authorised workflow, then run the full native insight review journey and operator acceptance. Preserve non-attestation and retained-history boundaries.
  - Branch/base: `feat/emergent-insights-local` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `ES02-05`, `B02-03`.
  - Existing code: `eightball/v2/insights.py`, `web/v2/insights-view.js`.
  - Evidence: `EV-EMERGENT-INSIGHTS-LOCAL` (registry below).
  - Blocker: Native browser navigation is administrator-blocked locally; new native integration acceptance remains required.

- [ ] **B02-22 Operator usefulness and full Emergent Insights acceptance** (optional, not a version gate)
  - Status: `not_started`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Owner/operator review of false positives, missed patterns, duplicate noise, thresholds and the complete native review journey before the feature is accepted.
  - Next: Review false positives, missed findings, review burden and source interpretation with the owner/fixer; do not claim usefulness from code tests alone.
  - Branch/base: `feat/emergent-insights-local` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `B02-21`.
  - Existing code: `docs/v2/EMERGENT-INSIGHTS.md`.


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

- [ ] **B03-07 Client mandate and human-selected course workflow** (optional, not a version gate)
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-25.
  - Acceptance: Owner-approved mandate and selected-course records preserve target, scope, dependencies and human rationale; change explanations prompt reconsideration without granting approvals, altering facts or silently switching the chosen course. Native/operator acceptance required.
  - Next: Integrate the exact packaged source through the authorised workflow. Run all native suites and operator review; retain original prerequisite and authority boundaries. Do not claim secure agency or background monitoring acceptance.
  - Branch/base: `work/chosen-course-recovery` / `ba0a84a54a0e115ac35b9590c8dc41c931f3e123`.
  - Dependencies: `B03-01`, `ES02-06`.
  - Existing code: `endstate/course.py`, `eightball/v2/courses.py`, `web/v2/course-view.js`, `tests/test_courses.py`, `tests/browser_courses.py`.
  - Evidence: `EV-CHOSEN-COURSE-LOCAL` (registry below).
  - Blocker: Only trusted local single-operator groundwork. Original secure identity/mandate and durable event prerequisites remain unaccepted. Native integration and independent operator acceptance remain outstanding.


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

- [ ] **B04-04 Permissioned correction replay and operator-value evaluation** (optional, not a version gate)
  - Status: `deferred`. Owner: unassigned. Updated: 2026-09-24.
  - Acceptance: An approved evaluation protocol measures the cost and benefit of suggestions/repairs on representative cases. Corrections retain provenance, access and retention limits; no cross-client retrieval or model training occurs without separate permission.
  - Next: Retain as an owner-review candidate. Define metrics and lawful dataset handling before collecting additional client information; no measured benefit is claimed.
  - Dependencies: `B03-01`, `B02-11`.


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

- [x] **ES01-01 Define ENDSTATE contracts and dependency boundary**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Neutral engine inputs/outputs, version/error semantics and product/domain boundaries are documented with tests planned.
  - Next: Preserve the versioned in-process boundary; stabilise nested result contracts in the package review.
  - Branch/base: `feat/situation-intelligence-v2` / `5e2098e9cb12251592eb3889ce7926798484699d`.
  - Existing code: `endstate/api.py`, `endstate/contracts.py`, `docs/endstate/CONTRACTS.md`.
  - Evidence: `EV-DECISION`, `EV-KERNEL` (registry below).

- [x] **ES01-02 Extract shared state, planning and explanation kernel**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: 8BALL calls the extracted core; the core imports no 8BALL UI, named client or fixer playbook.
  - Next: Continue 8BALL through the shared kernel; do not duplicate the planner for another domain.
  - Branch/base: `feat/situation-intelligence-v2` / `5e2098e9cb12251592eb3889ce7926798484699d`.
  - Dependencies: `ES01-01`.
  - Existing code: `endstate/state.py`, `endstate/planner.py`, `eightball/v2/planner.py`.
  - Evidence: `EV-KERNEL` (registry below).

- [x] **ES01-03 Preserve storage, imports and audit lineage**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Old data, imports and event meanings remain readable; migrations preserve observations and expiring approval behaviour.
  - Next: Keep frozen pre-extraction records and wire schemas as regression gates; do not regenerate expected results to hide changes.
  - Branch/base: `feat/situation-intelligence-v2` / `5e2098e9cb12251592eb3889ce7926798484699d`.
  - Dependencies: `ES01-01`.
  - Existing code: `eightball/models.py`, `eightball/v2/contracts.py`, `tests/test_endstate_kernel.py`, `tests/fixtures/endstate/pre_extraction.json.xz`.
  - Evidence: `EV-KERNEL` (registry below).

- [x] **ES01-04 Prove reuse through neutral, sales and support fixtures**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: One unchanged kernel plans three domains with domain-specific actions/policies; no duplicated engine or full new app.
  - Next: Keep these as fictional reuse fixtures; future commercial domains need their own policies and evaluation.
  - Branch/base: `feat/situation-intelligence-v2` / `5e2098e9cb12251592eb3889ce7926798484699d`.
  - Dependencies: `ES01-02`, `ES01-03`.
  - Existing code: `tests/test_endstate_kernel.py`, `endstate/api.py`.
  - Evidence: `EV-KERNEL` (registry below).

- [ ] **ES01-05 Reusable core acceptance**
  - Status: `implemented`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Current 8BALL suites and cross-domain fixtures pass on the proposed shared package; version compatibility is explicit.
  - Next: Inspect the installed-wheel/source/schema evidence and run the cumulative native application gate in an authorised environment before closing broad package acceptance. Do not claim a public SDK release.
  - Branch/base: `work/acceptance/integration-alpha7` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `ES01-02`, `ES01-03`, `ES01-04`.
  - Existing code: `endstate/api.py`, `docs/endstate/CONTRACTS.md`, `tests/test_endstate_kernel.py`, `endstate/results.py`, `pyproject.toml`, `scripts/build_endstate.py`, `scripts/export_endstate_schemas.py`, `tests/test_endstate_results.py`.
  - Evidence: `EV-KERNEL`, `EV-INTEGRATION-LOCAL`, `EV-INTEGRATION-BLOCKED` (registry below).
  - Blocker: Actual internal distribution and code compatibility pass on this environment; cumulative native application acceptance remains policy-blocked.


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

- [x] **ES02-05 Bounded structural emergence detectors and typed explanations** (optional, not a version gate)
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Revalidated snapshots produce reproducible, source/graph-linked findings with explicit limits, signed semantics and no mutation/network/model calls; independent fixtures exercise each implemented rule.
  - Next: Preserve the scoped deterministic/governance contract and rerun its regression tests at every integration. This tick is not native, commercial or model-quality approval.
  - Branch/base: `feat/emergent-insights-local` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `ES01-02`.
  - Existing code: `endstate/insights.py`, `tests/test_insight_engine.py`.
  - Evidence: `EV-EMERGENT-INSIGHTS-LOCAL` (registry below).

- [ ] **ES02-06 Selected-course and bounded reconsideration contracts** (optional, not a version gate)
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-25.
  - Acceptance: Versioned neutral input/output contracts distinguish candidate routes from a host-authorised course; changes to consulted sources, targets, guards, authority, estimates, clocks and resources produce traceable reconsideration results. Unknown scope requires review. Existing approval invalidation is preserved.
  - Next: Integrate the exact packaged source through the authorised workflow. Run all native suites and operator review; retain original prerequisite and authority boundaries. Do not claim secure agency or background monitoring acceptance.
  - Branch/base: `work/chosen-course-recovery` / `ba0a84a54a0e115ac35b9590c8dc41c931f3e123`.
  - Dependencies: `ES02-01`, `ES02-03`.
  - Existing code: `endstate/course.py`, `eightball/v2/courses.py`, `web/v2/course-view.js`, `tests/test_courses.py`, `tests/browser_courses.py`.
  - Evidence: `EV-CHOSEN-COURSE-LOCAL` (registry below).
  - Blocker: Only trusted local single-operator groundwork. Original secure identity/mandate and durable event prerequisites remain unaccepted. Native integration and independent operator acceptance remain outstanding.


## ENDSTATE 0.3: Evaluated intelligence compilation

- [ ] **ES03-01 Provider-independent reviewed outcome compiler**
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Source interpretation, typed graph drafting and deterministic validation are clean interchangeable interfaces outside the product layer.
  - Next: Validate the target-aware compiler on real providers without weakening acceptance; retain independent semantic review. This local change does not complete the compiler quality gate.
  - Branch/base: `work/hf-black-drafting` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `ES01-01`.
  - Existing code: `eightball/v2/intelligence.py`, `endstate/compilation.py`, `tests/test_endstate_compilation.py`.
  - Evidence: `EV-APP`, `EV-QWEN`, `EV-STAGED-CODE`, `EV-STAGED-MODEL`, `EV-HF-BLACK-LOCAL` (registry below).

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
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Runtime, selected weights, version and connection status are actually detected; downloads are explicit and user-approved.
  - Next: Retain truthful runtime/configuration status; complete setup/cancellation and actual-provider verification separately.
  - Branch/base: `work/hf-black-drafting` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Existing code: `eightball/v2/runtime_status.py`, `eightball/v2/hosted.py`.
  - Evidence: `EV-HF-BLACK-LOCAL` (registry below).

- [ ] **ES03-05 Failure handling, model trace and governed provider selection**
  - Status: `partial`. Owner: unassigned. Updated: 2026-09-23.
  - Acceptance: Provider replacement, refusal, timeout, malformed output, prompt injection and trace retention satisfy shared gates with measured quality.
  - Next: Extend existing fail-closed tests and preserve negative model results.
  - Existing code: `eightball/v2/intelligence.py`, `eightball/v2/store.py`.
  - Evidence: `EV-APP`, `EV-QWEN`, `EV-CLASSIFIER` (registry below).

- [x] **ES03-06 Opt-in Hugging Face development transport contract** (optional, not a version gate)
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Implemented transport is tested with controlled HTTP responses for permission, configuration, explicit routing, errors, size bounds, source scoping and no state mutation. This scope does not claim live inference.
  - Next: Publish the local checkpoint and configure credentials later for ES03-07; do not reinterpret mocked contract tests as hosted model evaluation.
  - Branch/base: `work/hf-black-drafting` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `DOC-01`.
  - Existing code: `eightball/v2/hosted.py`, `tests/test_hosted_and_grounding.py`, `evals/live_huggingface.py`.
  - Evidence: `EV-HF-BLACK-LOCAL` (registry below).

- [ ] **ES03-07 Actual hosted-model comparison on preserved fixtures** (optional, not a version gate)
  - Status: `blocked`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Authorised real HF requests record exact selected model/provider, outputs, same-fixture structural gate and human semantic review. No automatic or fictitious success.
  - Next: After explicit configuration, run the manual hosted harness without changing the original four inputs; then use independent labelled cases before model selection.
  - Branch/base: `work/hf-black-drafting` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `ES03-06`.
  - Existing code: `evals/live_huggingface.py`, `evals/generation-cases.json`.
  - Evidence: `EV-HF-BLACK-LOCAL` (registry below).
  - Blocker: No authorised HF token/model/provider configured; no real hosted inference performed.

- [ ] **ES03-08 Recover and reproduce reported human draft-repair implementation** (optional, not a version gate)
  - Status: `blocked`. Owner: unassigned. Updated: 2026-09-24.
  - Acceptance: Recovered or rebuilt exact source preserves the original failure, human edits, source/base revision and separate pending-proposal review; reproduction, stale-state denial and native interaction pass. Assisted repair never satisfies the unassisted model gate.
  - Next: Recover the exact later source/package or explicitly rebuild the bounded repair on the last verified source. Reproduce its actual tests before marking implemented; never relabel alpha.7 as the reported repair build.
  - Dependencies: `ES03-01`, `B02-02`.
  - Evidence: `EV-DRAFT-RECOVERY-GAP` (registry below).
  - Blocker: The latest supplied repair handoff explicitly reports that no completed working tree was found. Only verified alpha.7 source was recovered in this review.


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

### EV-KERNEL

- Kind: `software_validation`.
- Repository evidence: [docs/endstate/VALIDATION.md](../../docs/endstate/VALIDATION.md).
- Result/scope: 269 local tests, including 36 extraction/compatibility checks; 51 V0.2 and 27 legacy native browser checks passed. Shared neutral/sales/support kernel fixtures, not new products or model-quality approval.
- Code revision: `0c4104a675600c20a290766909bca60088766b35`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35904869115).

### EV-STAGED-CODE

- Kind: `software_validation`.
- Repository evidence: [docs/evidence/staged-compilation-verification.json](../../docs/evidence/staged-compilation-verification.json).
- Result/scope: 306 pytest tests including 37 new compiler regressions; 51 V0.2 and 27 legacy native browser checks passed. Two-stage provider-independent compilation is implemented; this does not verify model quality.
- Code revision: `3a33866f375be355658d8e5d82addb25bcc7eed9`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35911570084).

### EV-STAGED-MODEL

- Kind: `failed_real_model_evaluation`.
- Repository evidence: [docs/evidence/staged-compilation-verification.json](../../docs/evidence/staged-compilation-verification.json).
- Result/scope: Actual staged Qwen test: 3/4 fixtures valid; supplier graph rejected for repeated readiness/goal results and also contained invented prerequisite IDs. Manual inspection found desired-outcome confusion. All live case states unchanged; B02-09 remains blocked.
- Code revision: `3a33866f375be355658d8e5d82addb25bcc7eed9`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/35911570117).

### EV-HF-BLACK-LOCAL

- Kind: `local_test_and_visual_evidence`.
- Repository evidence: [docs/evidence/hf-black-local-verification.json](../../docs/evidence/hf-black-local-verification.json).
- Result/scope: 362 local pytest checks; 93 explicitly bridged browser checks. No hosted inference, native browser networking or remote push for this change.

### EV-GRAPH-EXPLORER-LOCAL

- Kind: `local_code_and_bridged_browser_evidence`.
- Repository evidence: [docs/evidence/relationship-explorer-local-verification.json](../../docs/evidence/relationship-explorer-local-verification.json).
- Result/scope: 399 pytest tests, including 37 pure projection/layout checks; 131 bridged browser checks including 38 new graph checks. Graph interactions preserve audit state. No native CI or model inference claimed.

### EV-PLAN-STUDIO-LOCAL

- Kind: `local_software_and_interaction_evidence`.
- Repository evidence: [docs/evidence/plan-studio-local-verification.json](../../docs/evidence/plan-studio-local-verification.json).
- Result/scope: 484 local automated tests; 174 bridge browser checks, including 43 Plan Studio/job/changelog checks. No native browser or new actual-model inference claim.

### EV-SOURCE-DESK-LOCAL

- Kind: `local_software_and_interaction_evidence`.
- Repository evidence: [docs/evidence/source-desk-local-verification.json](../../docs/evidence/source-desk-local-verification.json).
- Result/scope: 566 local automated tests, including 82 new source/API/Unicode selection tests. Source Desk is local; no native CI or model-quality acceptance is implied.

### EV-EMERGENCE-REVIEW

- Kind: `documentation_validation`.
- Repository evidence: [docs/delivery/sessions/2026-09-24-emergence-review-local.md](../../docs/delivery/sessions/2026-09-24-emergence-review-local.md).
- Result/scope: Mandatory end-of-sprint emergence review is documented across agent/handoff/PRD/roadmap and regression-tested. It governs discovery; it does not by itself add runtime scope.

### EV-EMERGENT-INSIGHTS-LOCAL

- Kind: `local_code_and_bridged_browser_evidence`.
- Repository evidence: [docs/evidence/emergent-insights-local-verification.json](../../docs/evidence/emergent-insights-local-verification.json).
- Result/scope: 672 automated tests and 249 explicit ASGI-bridge browser checks across seven suites; 39 new Emergent Insights journey checks. No native or model-quality acceptance. 37 discoveries retained with prospective changelog policy.

### EV-SOURCE-CLARITY-LOCAL

- Kind: `local_code_and_bridged_browser_evidence`.
- Repository evidence: [docs/evidence/source-clarity-local-verification.json](../../docs/evidence/source-clarity-local-verification.json).
- Result/scope: 746 automated tests, including 74 new checks; 275 explicit ASGI-bridge browser checks across eight suites, including 26 source-clarity checks. Native navigation was attempted and administrator-blocked. No model-quality or production acceptance.

### EV-PLAN-REVIEW-LOCAL

- Kind: `local_software_validation`.
- Repository evidence: [docs/evidence/plan-review-local-verification.json](../../docs/evidence/plan-review-local-verification.json).
- Result/scope: Plan Review, quality-review infrastructure and route-identity regression. Actual checks and boundaries recorded in the linked file; not an independent expert evaluation.

### EV-INTEGRATION-LOCAL

- Kind: `software_validation`.
- Repository evidence: [docs/evidence/integration-acceptance-local-verification.json](../../docs/evidence/integration-acceptance-local-verification.json).
- Result/scope: 855 code tests and a complete rerun against the installed internal wheel passed. All 344 browser checks across ten suites passed explicitly bridged. Source-bound reports are packaged separately; no new native/model/expert acceptance.

### EV-INTEGRATION-BLOCKED

- Kind: `environment_blocker`.
- Repository evidence: [docs/evidence/integration-acceptance-local-verification.json](../../docs/evidence/integration-acceptance-local-verification.json).
- Result/scope: Native loopback navigation administrator-blocked; local inference runtime unavailable and HF configuration absent. No runtime policy altered and no provider calls started.

### EV-VISION-REVIEW

- Kind: `documentation_and_source_inventory`.
- Repository evidence: [docs/delivery/sessions/2026-09-24-vision-strengthening.md](../../docs/delivery/sessions/2026-09-24-vision-strengthening.md).
- Result/scope: Vision/roadmap refinement over recovered alpha.7; no runtime feature or new required acceptance pass. Exact source inventory and document/history checks are recorded in this session.

### EV-DRAFT-RECOVERY-GAP

- Kind: `reported_delivery_limitation`.
- Repository evidence: [docs/reference/2026-09-24-draft-repair-delivery-record.md](../../docs/reference/2026-09-24-draft-repair-delivery-record.md).
- Result/scope: The supplied Draft Repair handoff states that no completed draft-repair working tree was found. Reported 905-test results are not reproduced implementation evidence for recovered alpha.7.

### EV-CHOSEN-COURSE-LOCAL

- Kind: `local_focused_code_and_bridge`.
- Repository evidence: [docs/evidence/chosen-course-focused-verification.json](../../docs/evidence/chosen-course-focused-verification.json).
- Result/scope: 64 focused code tests and 29 explicit bridge browser checks passed. Native probe blocked. No model or production acceptance.

### EV-SOURCE-SEARCH-RACE

- Kind: `reproduced_failure_and_local_regression`.
- Repository evidence: [docs/evidence/source-desk-native-closeout.json](../../docs/evidence/source-desk-native-closeout.json).
- Result/scope: Original native failure inspected; new component checks fail 8/12 on original source and pass 12/12 after correction. 938 local code tests, 38 explicit bridge Source Desk checks. Patched native acceptance pending.
