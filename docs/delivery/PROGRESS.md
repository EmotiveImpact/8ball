# Delivery checklist: 8BALL + ENDSTATE

> Generated from `docs/delivery/progress.json`. Edit the ledger, then run `python scripts/delivery.py --write`. Do not maintain a second set of statuses here.

Last status review: 2026-10-26.

**8BALL is the fixer product. ENDSTATE is the reusable engine underneath it.**

Build objective and completion criteria: [BUILD-GOAL.md](BUILD-GOAL.md). The sections below are the current status for both tracks, not separate backlogs.

## Checkpoint and release boundary

- Active integration branch: `feat/agency-authorisation-20261025`; PR #5.
- Inspected application baseline: `48e572e95be8b28d0b317d7bc8b3a18893a3ef76`.
- This is a dated snapshot. Refresh the branch, PR and CI at the start of every session.
- At inspection: draft PR = `true`; merged = `false`; production deployed = `false`.
- Standalone ENDSTATE package released = `false`.

## Checkbox meaning

`[x] verified` means the specific acceptance scope has linked evidence. `[ ] implemented` means code exists without complete acceptance. `partial`, `blocked`, `in_progress`, `not_started` and `deferred` remain unchecked. A failed experiment can be recorded without passing its quality gate. Counts are not product-completion percentages.

Built, verified, merged, packaged, deployed and commercially released are distinct. No model-quality claim follows from a software CI pass.

## Next work

- **ES02-01: Normalised event and authority contract**. Coordination claim: events; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Connect reviewed proposal/commit boundaries and a durable worker/outbox with scope and permission revalidation; preserve exact revision, cancellation and failed-attempt history. Inbox ingestion alone never applies case changes. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
- **ES02-02: Durable ordered updates, idempotency and replay**. Coordination claim: events; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Integrate authenticated host worker dispatch with current case/permission rechecks and retained provider evidence, then measure end-to-end latency and replanning. Preserve actual OIDC, production isolation and independent/model/human gates. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
- **B03-01: Identity, organisations and matter-scoped authorisation**. Coordination claim: identity; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Complete authenticated host worker dispatch, actual OIDC sign-in and measured event-to-review/replanning evidence. The scoped review page now uses the existing graph editor; preserve production isolation and genuine model/human acceptance gates. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
- **B02-09: Reliable reviewed graph proposals for new situations**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Follow docs/delivery/NEXT-BUILD.md from the consolidated current source. Complete the unchanged task acceptance using actual provider and appropriate independent/human evidence; integration does not close this gate. Latest integration: see sessions/2026-10-26-sonnet-native.md. Native actual-provider engineering now passes; retain independent protocol/held-out labels and human gates. Do not re-block this authorised test on dashboard login or assume a provider cap. No reserved lane owner/status/acceptance change.
- **B02-10: Robust source extraction, deadlines and entity reconciliation**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Evaluate multi-source identity/date workflows with professional fixtures; preserve exact source and preview/apply boundaries.
- **B02-11: Independent quality evaluation and production-model selection**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Obtain genuine prospective owner/qualified reviewer approval and independently authored held-out labels. Existing manual v1 forms remain legitimate; optional v2 forms/offline checker identify recording gaps without granting acceptance. Run authorised actual-provider comparisons only afterward; neither templates nor native software checks are semantic approval. Integration follow-up: verify the reviewed specialist worker checkpoint in docs/delivery/sessions/2026-10-26-specialist-worker.md; preserve partial status and all remaining gates. Read-only presentation follow-up: docs/delivery/sessions/2026-10-26-specialist-presentation.md. No acceptance status or reserved lane ownership change. Latest integration: see sessions/2026-10-26-sonnet-native.md. Native actual-provider engineering now passes; retain independent protocol/held-out labels and human gates. Do not re-block this authorised test on dashboard login or assume a provider cap. No reserved lane owner/status/acceptance change.
- **B02-12: Full twenty-step real-model V0.2 acceptance journey**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Follow docs/delivery/NEXT-BUILD.md from the consolidated current source. Complete the unchanged task acceptance using actual provider and appropriate independent/human evidence; integration does not close this gate. Latest integration: see sessions/2026-10-26-sonnet-native.md. Native actual-provider engineering now passes; retain independent protocol/held-out labels and human gates. Do not re-block this authorised test on dashboard login or assume a provider cap. No reserved lane owner/status/acceptance change.
- **B02-15: Model progress/cancellation and accurate installation status**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Follow docs/delivery/NEXT-BUILD.md from the consolidated current source. Complete the unchanged task acceptance using actual provider and appropriate independent/human evidence; integration does not close this gate. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately. Integration lifecycle checkpoint: retain the source-matched Sonnet API/process evidence and unknown remote states. Complete the remaining actual-provider native-UI lifecycle/installation-status review without treating software results as human or provider-side cancellation acceptance.
- **B02-16: Complete accessibility and supported-environment validation**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Complete the recorded human accessibility and supported-platform review, not another UI feature. Use the unperformed docs/delivery/review/HUMAN-ACCEPTANCE.template.md for the owner end review and appropriately qualified reviewers; record actual configurations and observations.
- **B02-19: Black operator visual system and transparent intelligence controls**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Review the current black workspace without expanding scope; preserve passing native controls. Use the unperformed docs/delivery/review/HUMAN-ACCEPTANCE.template.md for the owner end review and appropriately qualified reviewers; record actual configurations and observations.
- **B02-20: Black relationship explorer with local focus, directed flow and records view**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Review realistic graph density and operator comprehension; native graph controls/audit invariants now pass. Use the unperformed docs/delivery/review/HUMAN-ACCEPTANCE.template.md for the owner end review and appropriately qualified reviewers; record actual configurations and observations.
- **B02-18: V0.2 acceptance and release decision**. Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Follow docs/delivery/NEXT-BUILD.md from the consolidated current source. Complete the unchanged task acceptance using actual provider and appropriate independent/human evidence; integration does not close this gate. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.

## Version summary

| Track / milestone | Required subparts verified | Acceptance scope | Release |
| --- | ---: | --- | --- |
| Governance 1.1: Naming, PRD and shared delivery control | 7/7 | Scoped gate met | not released |
| 8BALL 0.1: Local outcome-planning foundation | 3/3 | Scoped gate met | not released |
| 8BALL 0.2: Reviewed situation intelligence | 10/20 | Not yet accepted | not released |
| 8BALL 0.3: Secure agency pilot | 0/6 | Not yet accepted | not released |
| 8BALL 0.4: Professionally reviewed resolution intelligence | 0/3 | Not yet accepted | not released |
| 8BALL 1.0: Supported fixer product | 0/2 | Not yet accepted | not released |
| ENDSTATE 0.1: Reusable engine core | 5/5 | Scoped gate met | not released |
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
  - Status: `verified`. Owner: Codex. Updated: 2026-10-16.
  - Acceptance: Master PRD incorporates naming, reuse, living plans and unchanged original acceptance requirements. Original blob hash matches.
  - Next: Use repository references instead of expecting chat access.
  - Branch/base: `docs/endstate-evolution-plan-20261016` / `bf54f607bb0e13d0c6adfc0f59ee146e75be287b`.
  - Evidence: `EV-DECISION`, `EV-ORIGINAL`, `EV-MAIN-CONSOLIDATION`, `EV-EVOLUTION-RESEARCH`, `EV-TENCENT-MEMORY-RESEARCH`, `EV-RUFLO-RESEARCH` (registry below).

- [x] **DOC-03 Create one evidence-linked version/subpart tracker for chat and Codex**
  - Status: `verified`. Owner: Codex. Updated: 2026-10-16.
  - Acceptance: Ledger validates; generated checklist is current; regression checks reject unsupported completion and broken IDs.
  - Next: Use this ledger and session protocol in both chat and Codex; keep the generated checklist in sync.
  - Branch/base: `docs/endstate-evolution-plan-20261016` / `bf54f607bb0e13d0c6adfc0f59ee146e75be287b`.
  - Dependencies: `DOC-01`, `DOC-02`.
  - Existing code: `scripts/delivery.py`.
  - Evidence: `EV-TRACKING`, `EV-MAIN-CONSOLIDATION`, `EV-EVOLUTION-RESEARCH`, `EV-TENCENT-MEMORY-RESEARCH`, `EV-RUFLO-RESEARCH` (registry below).

- [x] **DOC-04 Mandatory changelog and in-app product history**
  - Status: `verified`. Owner: Codex. Updated: 2026-10-16.
  - Acceptance: Every build adds a dated evidence-linked entry; generated CHANGELOG.md and in-app history share one source; base comparison detects missing entries or rewritten history.
  - Next: Enforce a new immutable-history changelog entry in each following session and integration commit. Local documentation/API/render scope verified; no source publication or release implied.
  - Branch/base: `docs/endstate-evolution-plan-20261016` / `bf54f607bb0e13d0c6adfc0f59ee146e75be287b`.
  - Existing code: `scripts/changelog.py`, `docs/delivery/changelog.json`, `web/v2/changelog-view.js`.
  - Evidence: `EV-PLAN-STUDIO-LOCAL`, `EV-MAIN-CONSOLIDATION`, `EV-EVOLUTION-RESEARCH`, `EV-TENCENT-MEMORY-RESEARCH`, `EV-RUFLO-RESEARCH` (registry below).

- [x] **DOC-05 Mandatory end-of-sprint emergence review**
  - Status: `verified`. Owner: Codex. Updated: 2026-10-16.
  - Acceptance: Every new build sprint explicitly records what emerged, its evidence level and roadmap disposition; new changelog entries cannot omit the emergence review.
  - Next: Run the Emergence Review at every substantive build handoff; only promote discoveries to required roadmap scope through an explicit ledger or decision update.
  - Branch/base: `docs/endstate-evolution-plan-20261016` / `bf54f607bb0e13d0c6adfc0f59ee146e75be287b`.
  - Dependencies: `DOC-03`, `DOC-04`.
  - Existing code: `docs/delivery/EMERGENCE-REVIEW.md`, `scripts/changelog.py`, `tests/test_changelog.py`.
  - Evidence: `EV-EMERGENCE-REVIEW`, `EV-MAIN-CONSOLIDATION`, `EV-EVOLUTION-RESEARCH`, `EV-TENCENT-MEMORY-RESEARCH`, `EV-RUFLO-RESEARCH` (registry below).

- [x] **DOC-06 Evolving complete emergence register and owner-review prompt suite**
  - Status: `verified`. Owner: Codex. Updated: 2026-10-16.
  - Acceptance: Every recorded discovery is retained, linked to roadmap scope, and rendered with append-only dispositions; declined items remain visible and no candidate inherits an unrelated completion tick.
  - Next: Preserve all original discoveries and append review history. Use ADR 0004 and docs/vision for the strengthened direction; no optional candidate or delivery claim becomes verified without its own evidence.
  - Branch/base: `feat/v02-evaluation-readiness-20261016` / `0fed04b5e299f4a2e53050456559133c1231b088`.
  - Dependencies: `DOC-05`.
  - Existing code: `scripts/emergence.py`, `docs/delivery/emergence.json`, `docs/prompts/EMERGENT-INSIGHTS.md`.
  - Evidence: `EV-EMERGENT-INSIGHTS-LOCAL`, `EV-VISION-REVIEW`, `EV-MAIN-CONSOLIDATION`, `EV-EVOLUTION-RESEARCH`, `EV-TENCENT-MEMORY-RESEARCH`, `EV-RUFLO-RESEARCH`, `EV-RUFLO-OWNER-REVIEW`, `EV-WHOLE-SYSTEM-REVIEW` (registry below).

- [x] **DOC-07 Preserve pinned upstream research source checkouts**
  - Status: `verified`. Owner: Codex. Updated: 2026-10-16.
  - Acceptance: All28 inspected repository pins are populated as source-only research checkouts with original licences, exact manifest identities, explicit model/LFS/nested exceptions and reproducible Git-only verification. No runtime adoption or upstream execution.
  - Next: Use the Git-only research helper for later restoration/verification; scope any upstream software installation or adaptation separately.
  - Branch/base: `feat/v02-compatible-provider-20261016` / `c9fd38438ba52e9320bc55b96132086bfe57ce6a`.
  - Dependencies: `DOC-06`.
  - Existing code: `.gitmodules`, `research/README.md`, `research/inventory.json`, `research/sources.py`, `research/AGENTS.md`.
  - Evidence: `EV-RESEARCH-COPY` (registry below).


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
  - Status: `verified`. Owner: Devin / integration. Updated: 2026-10-26.
  - Acceptance: Graph-impact questions and recorded revision deltas operate; hypothetical state changes leave the live case unchanged.
  - Next: Connect future ingestion only through reviewed revisioned updates. Information-loop integration: exact-source verification passed; see docs/delivery/sessions/2026-10-26-information-loop.md; independent operator benefit and agency disclosure remain separate.
  - Branch/base: `devin/1792969169-roadmap-integrated` / `585cb3193e3ff3771870e5917309b2b1e2416227`.
  - Existing code: `eightball/v2/planner.py`, `eightball/v2/services.py`, `endstate/rehearsal.py`, `eightball/v2/rehearsal.py`, `web/v2/rehearsal-view.js`, `tests/test_rehearsal.py`, `tests/browser_plan_review.py`.
  - Evidence: `EV-APP`, `EV-UI`, `EV-INFORMATION-LOOP-20261026` (registry below).

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
  - Status: `blocked`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-26.
  - Acceptance: Actual-model graph fixtures pass with all referenced actions present, meaningful alternative paths and explicit final verification. No silent template substitution.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Follow docs/delivery/NEXT-BUILD.md from the consolidated current source. Complete the unchanged task acceptance using actual provider and appropriate independent/human evidence; integration does not close this gate. Latest integration: see sessions/2026-10-26-sonnet-native.md. Native actual-provider engineering now passes; retain independent protocol/held-out labels and human gates. Do not re-block this authorised test on dashboard login or assume a provider cap. No reserved lane owner/status/acceptance change.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `eightball/v2/intelligence.py`, `evals/live_generation.py`, `endstate/compilation.py`, `tests/test_endstate_compilation.py`, `eightball/v2/compatible.py`, `evals/live_compatible.py`, `evals/live_huggingface.py`, `tests/test_hosted_eval_retention.py`, `docs/v2/ANTHROPIC-SETUP.md`.
  - Evidence: `EV-QWEN`, `EV-STAGED-CODE`, `EV-STAGED-MODEL`, `EV-HF-BLACK-LOCAL`, `EV-NATIVE-CLOSEOUT`, `EV-QWEN-20260927`, `EV-GENERATION-ROLE-CONTRACT`, `EV-PROVIDER-FAILURE-REVIEW`, `EV-COMPATIBLE-CODE`, `EV-EVALUATION-READINESS`, `EV-REVIEW-EVIDENCE-20261018`, `EV-ANTHROPIC-SETUP`, `EV-ANTHROPIC-20261026`, `EV-OCT25-INTEGRATION`, `EV-DECISION-CONTRACTS-20261026`, `EV-SONNET-NATIVE-20261026`, `EV-NATIVE-USAGE-20261026` (registry below).
  - Blocker: Native Sonnet frozen generation and actual-provider native journey now pass. Account cap absence explicitly accepted for bounded fictional tests; no cap is claimed. Independent semantic/reliability acceptance remains outstanding. Independent semantic evaluation must check branch-neutral readiness, relevant confirmation evidence, all target parts, alternatives and final-verification separation. Historical replay does not satisfy this gate.

- [ ] **B02-10 Robust source extraction, deadlines and entity reconciliation**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Reviewed multi-source extraction preserves negation, uncertainty, identity and quoted support; date changes become explicit reviewed scheduling proposals.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Evaluate multi-source identity/date workflows with professional fixtures; preserve exact source and preview/apply boundaries.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `eightball/v2/intelligence.py`, `endstate/time_review.py`, `eightball/v2/grounding.py`, `web/v2/grounding-view.js`, `tests/test_time_review.py`, `tests/test_grounding.py`, `tests/browser_grounding.py`.
  - Evidence: `EV-QWEN`, `EV-REMAINING`, `EV-SOURCE-DESK-LOCAL`, `EV-SOURCE-CLARITY-LOCAL`, `EV-NATIVE-CLOSEOUT`, `EV-PROVIDER-FAILURE-REVIEW` (registry below).
  - Blocker: Independent multi-source identity/date usefulness review remains outstanding. No automatic coreference, global actor merge, business-calendar semantics or reliable arbitrary model extraction is claimed.

- [ ] **B02-11 Independent quality evaluation and production-model selection**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-26.
  - Acceptance: Expert-labelled held-out data and predeclared acceptance thresholds measure semantic errors, omissions, corrections, latency and abstention.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Obtain genuine prospective owner/qualified reviewer approval and independently authored held-out labels. Existing manual v1 forms remain legitimate; optional v2 forms/offline checker identify recording gaps without granting acceptance. Run authorised actual-provider comparisons only afterward; neither templates nor native software checks are semantic approval. Integration follow-up: verify the reviewed specialist worker checkpoint in docs/delivery/sessions/2026-10-26-specialist-worker.md; preserve partial status and all remaining gates. Read-only presentation follow-up: docs/delivery/sessions/2026-10-26-specialist-presentation.md. No acceptance status or reserved lane ownership change. Latest integration: see sessions/2026-10-26-sonnet-native.md. Native actual-provider engineering now passes; retain independent protocol/held-out labels and human gates. Do not re-block this authorised test on dashboard login or assume a provider cap. No reserved lane owner/status/acceptance change.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `evals/live_generation.py`, `evals/classification-cases.json`, `endstate/plan_review.py`, `eightball/v2/plan_review.py`, `web/v2/plan-review-view.js`, `evals/plan_review_bench.py`, `evals/PLAN-QUALITY-GATE.md`, `tests/test_plan_review.py`, `tests/browser_plan_review.py`, `evals/review_readiness.py`, `tests/test_review_readiness.py`, `docs/delivery/review/protocol-v2.template.json`, `docs/delivery/review/dataset-manifest.template.json`.
  - Evidence: `EV-REMAINING`, `EV-PLAN-REVIEW-LOCAL`, `EV-NATIVE-CLOSEOUT`, `EV-PROVIDER-FAILURE-REVIEW`, `EV-EVALUATION-READINESS`, `EV-REVIEW-EVIDENCE-20261018`, `EV-REVIEW-REFRESH-RACE`, `EV-NATIVE-REVIEW-20261026`, `EV-DECISION-SMOKE-20261026`, `EV-FORECAST-MEASUREMENT-20261026`, `EV-SPECIALIST-WORKER-20261026`, `EV-SPECIALIST-PRESENTATION-20261026`, `EV-SONNET-NATIVE-20261026`, `EV-HISTORICAL-REPLAY-20261026` (registry below).
  - Blocker: Independent reviewer labels, approved prospective protocol and actual-provider comparison are not completed.

- [ ] **B02-12 Full twenty-step real-model V0.2 acceptance journey**
  - Status: `blocked`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-26.
  - Acceptance: Blank case -> real extraction -> mixed human review -> valid graph -> distinct routes -> new evidence/replan -> isolated refusal -> approval/completion -> reload/export, all native.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Follow docs/delivery/NEXT-BUILD.md from the consolidated current source. Complete the unchanged task acceptance using actual provider and appropriate independent/human evidence; integration does not close this gate. Latest integration: see sessions/2026-10-26-sonnet-native.md. Native actual-provider engineering now passes; retain independent protocol/held-out labels and human gates. Do not re-block this authorised test on dashboard login or assume a provider cap. No reserved lane owner/status/acceptance change.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B02-09`, `B02-10`, `B02-11`.
  - Existing code: `tests/browser_v2.py`, `evals/full_journey.py`, `scripts/acceptance.py`, `.github/workflows/provider-journey.yml`, `evals/provider_lifecycle.py`, `tests/test_provider_lifecycle.py`.
  - Evidence: `EV-QWEN`, `EV-UI`, `EV-STAGED-MODEL`, `EV-INTEGRATION-LOCAL`, `EV-INTEGRATION-BLOCKED`, `EV-NATIVE-CLOSEOUT`, `EV-PROVIDER-FAILURE-REVIEW`, `EV-COMPATIBLE-CODE`, `EV-EVALUATION-READINESS`, `EV-REVIEW-EVIDENCE-20261018`, `EV-OCT25-INTEGRATION`, `EV-NATIVE-REVIEW-20261026`, `EV-DECISION-SMOKE-20261026`, `EV-SONNET-NATIVE-20261026` (registry below).
  - Blocker: Actual-provider scripted native twenty-step journey now passes; genuinely human acceptance and independent quality remain unperformed. Scripted review and synthetic observations do not meet those gates.

- [x] **B02-13 Guided nested graph authoring instead of JSON-only advanced editing**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-26.
  - Acceptance: Operators can edit AND/OR, guards, contingencies and verification rules with guided controls and keyboard access.
  - Next: Preserve the verified guided-authoring scope; broader human/platform accessibility remains B02-16.
  - Branch/base: `feat/situation-intelligence-v2` / `14c57907d26ea914e372e544bba4b0bd3988f5dc`.
  - Existing code: `web/v2/studio-model.js`, `web/v2/studio-view.js`, `eightball/v2/authoring.py`, `tests/test_plan_studio.py`, `tests/test_studio_model.py`, `tests/browser_studio.py`, `web/v2/plan-review-view.js`.
  - Evidence: `EV-REMAINING`, `EV-PLAN-STUDIO-LOCAL`, `EV-PLAN-REVIEW-LOCAL`, `EV-NATIVE-CLOSEOUT` (registry below).

- [ ] **B02-14 Source chunking, duplication and reviewer-safe object reconciliation**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Longer sources retain exact provenance; duplicates and entity merges cannot rewrite observed meanings or lose attribution.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Complete professional source/reconciliation review; keep native original/excerpt/export and request-order regressions. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `eightball/v2/source_contracts.py`, `eightball/v2/source_desk.py`, `eightball/v2/request_limits.py`, `web/v2/source-model.js`, `web/v2/source-view.js`, `tests/test_source_desk.py`, `tests/test_source_api.py`, `tests/browser_sources.py`, `endstate/time_review.py`, `eightball/v2/grounding.py`, `web/v2/grounding-view.js`, `tests/test_time_review.py`, `tests/test_grounding.py`, `tests/browser_grounding.py`, `tests/test_source_view_races.py`, `docs/delivery/lane-reports/intelligence.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-REMAINING`, `EV-SOURCE-DESK-LOCAL`, `EV-SOURCE-CLARITY-LOCAL`, `EV-SOURCE-SEARCH-RACE`, `EV-NATIVE-CLOSEOUT`, `EV-PROVIDER-FAILURE-REVIEW`, `EV-LANE-INTELLIGENCE-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).
  - Blocker: Independent multi-source identity/date usefulness review remains outstanding. No automatic coreference, global actor merge, business-calendar semantics or reliable arbitrary model extraction is claimed.

- [ ] **B02-15 Model progress/cancellation and accurate installation status**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-26.
  - Acceptance: The UI reports actual runtime/weights/credential state and cancels work without stale commits. No silent large model download.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Follow docs/delivery/NEXT-BUILD.md from the consolidated current source. Complete the unchanged task acceptance using actual provider and appropriate independent/human evidence; integration does not close this gate. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately. Integration lifecycle checkpoint: retain the source-matched Sonnet API/process evidence and unknown remote states. Complete the remaining actual-provider native-UI lifecycle/installation-status review without treating software results as human or provider-side cancellation acceptance.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES03-04`.
  - Existing code: `eightball/v2/analysis_jobs.py`, `web/v2/job-view.js`, `tests/test_analysis_jobs.py`, `eightball/v2/compatible.py`, `tests/test_compatible_integration.py`, `evals/provider_lifecycle.py`, `tests/test_provider_lifecycle.py`, `docs/delivery/lane-reports/intelligence.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-REMAINING`, `EV-HF-BLACK-LOCAL`, `EV-PLAN-STUDIO-LOCAL`, `EV-NATIVE-CLOSEOUT`, `EV-PROVIDER-FAILURE-REVIEW`, `EV-COMPATIBLE-CODE`, `EV-EVALUATION-READINESS`, `EV-ANTHROPIC-SETUP`, `EV-OCT25-INTEGRATION`, `EV-LANE-INTELLIGENCE-20261026`, `EV-INTEGRATION-ENGINEERING-20261026`, `EV-NATIVE-REVIEW-20261026`, `EV-DECISION-SMOKE-20261026`, `EV-SONNET-LIFECYCLE-20261026`, `EV-LIFECYCLE-SOFTWARE-20261026` (registry below).
  - Blocker: Selected Sonnet API/process cancellation, supersession and restart observations pass; actual-provider native-UI lifecycle/installation-status acceptance remain unverified. Remote receipt, cancellation and billing are not established by local job states.

- [ ] **B02-16 Complete accessibility and supported-environment validation**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Keyboard, screen reader, empty/error/loading states and supported browsers/platform startup paths pass an explicit review.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Complete the recorded human accessibility and supported-platform review, not another UI feature. Use the unperformed docs/delivery/review/HUMAN-ACCEPTANCE.template.md for the owner end review and appropriately qualified reviewers; record actual configurations and observations.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `tests/browser_accessibility.py`, `web/v2/ui.js`, `web/v2/app.js`, `web/v2/style.css`, `scripts/acceptance.py`.
  - Evidence: `EV-REMAINING`, `EV-HF-BLACK-LOCAL`, `EV-GRAPH-EXPLORER-LOCAL`, `EV-INTEGRATION-LOCAL`, `EV-INTEGRATION-BLOCKED`, `EV-SOURCE-SEARCH-RACE`, `EV-NATIVE-CLOSEOUT`, `EV-GRAPH-KEYBOARD-FOCUS`, `EV-PROVIDER-FAILURE-REVIEW` (registry below).
  - Blocker: Human screen-reader and supported-browser/OS review remains outstanding; Linux/Chromium native software tests passed.

- [x] **B02-17 Prove compatibility after ENDSTATE core extraction**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Existing 8BALL cases, imports, approvals, audits, simulations and browser flows pass through the extracted core.
  - Next: Preserve the extraction baseline and rerun all legacy/V2 suites for subsequent core changes.
  - Branch/base: `feat/situation-intelligence-v2` / `5e2098e9cb12251592eb3889ce7926798484699d`.
  - Dependencies: `ES01-02`, `ES01-03`.
  - Existing code: `tests/test_endstate_kernel.py`, `tests/browser_v2.py`, `tests/browser_smoke.py`.
  - Evidence: `EV-KERNEL` (registry below).

- [ ] **B02-18 V0.2 acceptance and release decision**
  - Status: `blocked`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: All required V0.2 subparts have scoped evidence; reviews/gates pass; approval to integrate/release is recorded separately.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Follow docs/delivery/NEXT-BUILD.md from the consolidated current source. Complete the unchanged task acceptance using actual provider and appropriate independent/human evidence; integration does not close this gate. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B02-01`, `B02-02`, `B02-03`, `B02-04`, `B02-05`, `B02-06`, `B02-07`, `B02-08`, `B02-09`, `B02-10`, `B02-11`, `B02-12`, `B02-13`, `B02-14`, `B02-15`, `B02-16`, `B02-17`, `B02-19`, `B02-20`.
  - Existing code: `docs/delivery/lane-reports/intelligence.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-QWEN`, `EV-MAIN-CONSOLIDATION`, `EV-OCT25-INTEGRATION`, `EV-LANE-INTELLIGENCE-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).
  - Blocker: Real-model journey and developer-quality work remain unaccepted.

- [ ] **B02-19 Black operator visual system and transparent intelligence controls**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Black/graphite design, legible status labels, exact-target review, provider controls and mobile lock work across the existing native desktop/mobile workflow without losing evidence/approval functions.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Review the current black workspace without expanding scope; preserve passing native controls. Use the unperformed docs/delivery/review/HUMAN-ACCEPTANCE.template.md for the owner end review and appropriately qualified reviewers; record actual configurations and observations.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B02-07`.
  - Existing code: `web/v2/style.css`, `web/v2/views.js`, `web/v2/forms.js`, `tests/browser_development.py`.
  - Evidence: `EV-HF-BLACK-LOCAL`, `EV-GRAPH-EXPLORER-LOCAL`, `EV-NATIVE-CLOSEOUT`, `EV-PROVIDER-FAILURE-REVIEW`, `EV-AGENCY-API` (registry below).
  - Blocker: Owner visual review and broader human accessibility acceptance remain outstanding.

- [ ] **B02-20 Black relationship explorer with local focus, directed flow and records view**
  - Status: `implemented`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Explore actual case records using Connections, Outcome flow and Records; inspect source/history and exact logic; keyboard/mobile controls and view-only audit invariants pass, including native browser validation.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Review realistic graph density and operator comprehension; native graph controls/audit invariants now pass. Use the unperformed docs/delivery/review/HUMAN-ACCEPTANCE.template.md for the owner end review and appropriately qualified reviewers; record actual configurations and observations.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B02-04`, `B02-07`, `B02-19`.
  - Existing code: `web/v2/graph-model.js`, `web/v2/graph-view.js`, `web/v2/views.js`, `web/v2/app.js`, `web/v2/style.css`, `tests/browser_v2.py`, `tests/browser_graph.py`, `tests/test_graph_explorer.py`, `scripts/design_preview.py`.
  - Evidence: `EV-GRAPH-EXPLORER-LOCAL`, `EV-NATIVE-CLOSEOUT`, `EV-GRAPH-KEYBOARD-FOCUS`, `EV-PROVIDER-FAILURE-REVIEW` (registry below).
  - Blocker: Representative dense-case operator usability and broader accessibility review remain outstanding.

- [ ] **B02-21 Evidence-linked Emergent Insights and review workspace** (optional, not a version gate)
  - Status: `implemented`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Current/historical findings, explicit review and hypotheses, safe question promotion, stale-context handling, reload/export and native desktop/mobile acceptance without changing factual state.
  - Next: Coordination claim: intelligence; optional_hold_no_implementation. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Perform owner/fixer insight review without changing evidence/authority semantics.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES02-05`, `B02-03`.
  - Existing code: `eightball/v2/insights.py`, `web/v2/insights-view.js`.
  - Evidence: `EV-EMERGENT-INSIGHTS-LOCAL`, `EV-NATIVE-CLOSEOUT` (registry below).
  - Blocker: Operator acceptance remains outstanding; the complete native insight journey now passes.

- [ ] **B02-22 Operator usefulness and full Emergent Insights acceptance** (optional, not a version gate)
  - Status: `not_started`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Owner/operator review of false positives, missed patterns, duplicate noise, thresholds and the complete native review journey before the feature is accepted.
  - Next: Coordination claim: intelligence; optional_hold_no_implementation. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Review false positives, missed findings, review burden and source interpretation with the owner/fixer; do not claim usefulness from code tests alone.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B02-21`.
  - Existing code: `docs/v2/EMERGENT-INSIGHTS.md`.


## 8BALL 0.3: Secure agency pilot

- [ ] **B03-01 Identity, organisations and matter-scoped authorisation**
  - Status: `partial`. Owner: Devin / roadmap-identity. Updated: 2026-10-25.
  - Acceptance: Authenticated identities and cross-tenant/matter denial tests cover read, write, export, search and model inference.
  - Next: Coordination claim: identity; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Complete authenticated host worker dispatch, actual OIDC sign-in and measured event-to-review/replanning evidence. The scoped review page now uses the existing graph editor; preserve production isolation and genuine model/human acceptance gates. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-identity` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `eightball/authorisation.py`, `tests/test_authorisation.py`, `eightball/agency_access.py`, `tests/test_agency_access.py`, `eightball/v2/event_api.py`, `web/v2/event-review.js`, `tests/browser_event_review.py`, `docs/delivery/lane-reports/identity.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-SECURITY`, `EV-AGENCY-POLICY`, `EV-AGENCY-API`, `EV-EVENT-API`, `EV-EVENT-REVIEW-UI`, `EV-LANE-IDENTITY-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B03-02 Encrypted evidence vault and retention controls**
  - Status: `partial`. Owner: Devin / roadmap-vault. Updated: 2026-10-25.
  - Acceptance: Immutable originals, hashes, upload quarantine/scanning, encryption, retention/hold/deletion and audited access are tested.
  - Next: Coordination claim: vault; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Implement without weakening source provenance. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-vault` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B03-01`.
  - Existing code: `docs/delivery/lane-reports/vault.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-SECURITY`, `EV-LANE-VAULT-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B03-03 Scoped specialist collaboration and real client portal**
  - Status: `partial`. Owner: Devin / roadmap-collaboration. Updated: 2026-10-25.
  - Acceptance: Experts receive revocable matter/object grants; clients receive separately reviewed projections, never internal records by default.
  - Next: Coordination claim: collaboration; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Build authenticated views rather than relabelling the existing preview. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-collaboration` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B03-01`, `B03-02`.
  - Existing code: `docs/delivery/lane-reports/collaboration.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-SECURITY`, `EV-LANE-COLLABORATION-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B03-04 Authorised ingestion, event handling and notifications**
  - Status: `partial`. Owner: Devin / roadmap-events. Updated: 2026-10-26.
  - Acceptance: Actual source connectors, durable updates and notifications respect permissions, source review, ordering and retry limits.
  - Next: Coordination claim: events; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Build one authorised connector through ENDSTATE event contracts. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately. Integration follow-up: verify the reviewed specialist worker checkpoint in docs/delivery/sessions/2026-10-26-specialist-worker.md; preserve partial status and all remaining gates. Read-only presentation follow-up: docs/delivery/sessions/2026-10-26-specialist-presentation.md. No acceptance status or reserved lane ownership change.
  - Branch/base: `devin/1792969169-roadmap-events` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B03-01`, `ES02-01`, `ES02-02`.
  - Existing code: `docs/delivery/lane-reports/events.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-SECURITY`, `EV-LANE-EVENTS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026`, `EV-SPECIALIST-WORKER-20261026`, `EV-SPECIALIST-PRESENTATION-20261026` (registry below).

- [ ] **B03-05 Independent audit checkpoints, recovery and operational monitoring**
  - Status: `partial`. Owner: Devin / roadmap-operations. Updated: 2026-10-25.
  - Acceptance: Restore rehearsal, audit anchoring, revocation and operational incident tests pass without sensitive log leakage.
  - Next: Coordination claim: operations; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Set measurable service/recovery targets and test them. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-operations` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `docs/delivery/lane-reports/operations.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-SECURITY`, `EV-LANE-OPERATIONS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B03-06 Limited qualified-fixer pilot acceptance**
  - Status: `not_started`. Owner: Devin / roadmap-operations. Updated: 2026-10-25.
  - Acceptance: Authorised pilot users validate usefulness, safety, corrections and confidentiality; critical findings closed before wider release.
  - Next: Coordination claim: operations; fictional_pilot_tooling_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Recruit/review pilot criteria only after data and access gates pass. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-operations` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B02-18`, `B03-01`, `B03-02`, `B03-03`, `B03-04`, `B03-05`.
  - Existing code: `docs/delivery/lane-reports/operations.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-OPERATIONS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B03-07 Client mandate and human-selected course workflow** (optional, not a version gate)
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-26.
  - Acceptance: Owner-approved mandate and selected-course records preserve target, scope, dependencies and human rationale; change explanations prompt reconsideration without granting approvals, altering facts or silently switching the chosen course. Native/operator acceptance required.
  - Next: Preserve existing local course work; defer remaining optional expansion under the owner freeze.
  - Branch/base: `feat/situation-intelligence-v2` / `14c57907d26ea914e372e544bba4b0bd3988f5dc`.
  - Dependencies: `B03-01`, `ES02-06`.
  - Existing code: `endstate/course.py`, `eightball/v2/courses.py`, `web/v2/course-view.js`, `tests/test_courses.py`, `tests/browser_courses.py`.
  - Evidence: `EV-CHOSEN-COURSE-LOCAL`, `EV-NATIVE-CLOSEOUT` (registry below).
  - Blocker: Secure identity/full mandate and durable event prerequisites remain unaccepted. Independent operator acceptance remains outstanding; native local workflow passes.


## 8BALL 0.4: Professionally reviewed resolution intelligence

- [ ] **B04-01 Professionally reviewed fixer and crisis playbooks**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Specialists approve versioned patterns, assumptions, authority and confirmation criteria; examples are not presented as proven solutions.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Review existing starters with qualified operators. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `eightball/v2/playbooks.py`, `docs/delivery/lane-reports/intelligence.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-REMAINING`, `EV-LANE-INTELLIGENCE-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B04-02 Governed precedent retrieval**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Permissioned, source-linked precedent is case/matter scoped; access revocation and leakage tests pass. No automatic training.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Agree governance and retention before indexing previous cases. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B03-01`, `B03-02`.
  - Existing code: `docs/delivery/lane-reports/intelligence.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-INTELLIGENCE-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B04-03 Measured operator benefit from richer resolution intelligence**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Held-out/pilot evidence shows useful questions and plans without unsupported causal or success-probability claims.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Benchmark against the accepted baseline with real professional review. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B03-06`, `B04-01`, `B04-02`.
  - Existing code: `docs/delivery/lane-reports/intelligence.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-INTELLIGENCE-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B04-04 Permissioned correction replay and operator-value evaluation** (optional, not a version gate)
  - Status: `deferred`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: An approved evaluation protocol measures the cost and benefit of suggestions/repairs on representative cases. Corrections retain provenance, access and retention limits; no cross-client retrieval or model training occurs without separate permission.
  - Next: Coordination claim: intelligence; optional_hold_no_implementation. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Retain as an owner-review candidate. Define metrics and lawful dataset handling before collecting additional client information; no measured benefit is claimed.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B03-01`, `B02-11`.


## 8BALL 1.0: Supported fixer product

- [ ] **B10-01 Commercial onboarding, support and launch readiness**
  - Status: `not_started`. Owner: Devin / roadmap-operations. Updated: 2026-10-25.
  - Acceptance: Customer onboarding, support, service terms, brand/licence clearance and operating ownership are ready for the accepted scope.
  - Next: Coordination claim: operations; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Define commercial acceptance with the product owner; no inferred public release. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-operations` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B03-06`.
  - Existing code: `docs/delivery/lane-reports/operations.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-OPERATIONS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **B10-02 8BALL V1 fixer production release**
  - Status: `not_started`. Owner: Devin / roadmap-operations. Updated: 2026-10-25.
  - Acceptance: All advertised capabilities, security, accessibility, recovery, model policy and customer acceptance are evidenced for supported environments.
  - Next: Coordination claim: operations; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Record explicit release and deployment decisions after gates. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-operations` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B10-01`, `B04-03`.
  - Existing code: `docs/delivery/lane-reports/operations.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-OPERATIONS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).


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
  - Next: Continue 8BALL through the shared kernel; do not duplicate the planner for another domain. Information-loop integration: exact-source verification passed; see docs/delivery/sessions/2026-10-26-information-loop.md; independent operator benefit and agency disclosure remain separate.
  - Branch/base: `feat/situation-intelligence-v2` / `5e2098e9cb12251592eb3889ce7926798484699d`.
  - Dependencies: `ES01-01`.
  - Existing code: `endstate/state.py`, `endstate/planner.py`, `eightball/v2/planner.py`.
  - Evidence: `EV-KERNEL`, `EV-INFORMATION-LOOP-20261026` (registry below).

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

- [x] **ES01-05 Reusable core acceptance**
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-26.
  - Acceptance: Current 8BALL suites and cross-domain fixtures pass on the proposed shared package; version compatibility is explicit.
  - Next: Internal reusable-core compatibility scope verified. Maintain regression coverage; public SDK/commercial release and other platforms remain separate.
  - Branch/base: `feat/situation-intelligence-v2` / `14c57907d26ea914e372e544bba4b0bd3988f5dc`.
  - Dependencies: `ES01-02`, `ES01-03`, `ES01-04`.
  - Existing code: `endstate/api.py`, `docs/endstate/CONTRACTS.md`, `tests/test_endstate_kernel.py`, `endstate/results.py`, `pyproject.toml`, `scripts/build_endstate.py`, `scripts/export_endstate_schemas.py`, `tests/test_endstate_results.py`.
  - Evidence: `EV-KERNEL`, `EV-INTEGRATION-LOCAL`, `EV-INTEGRATION-BLOCKED`, `EV-NATIVE-CLOSEOUT`, `EV-NATIVE-REVIEW-20261026`, `EV-LIFECYCLE-SOFTWARE-20261026` (registry below).


## ENDSTATE 0.2: Event-driven replanning

- [ ] **ES02-01 Normalised event and authority contract**
  - Status: `partial`. Owner: Devin / roadmap-events. Updated: 2026-10-25.
  - Acceptance: Events carry source, version, occurrence/receipt time, matter scope and review status; incoming text never gets command authority.
  - Next: Coordination claim: events; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Connect reviewed proposal/commit boundaries and a durable worker/outbox with scope and permission revalidation; preserve exact revision, cancellation and failed-attempt history. Inbox ingestion alone never applies case changes. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-events` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES01-01`.
  - Existing code: `endstate/events.py`, `eightball/event_inbox.py`, `tests/test_event_inbox.py`, `docs/delivery/lane-reports/events.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-EVENT-INBOX`, `EV-LANE-EVENTS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES02-02 Durable ordered updates, idempotency and replay**
  - Status: `partial`. Owner: Devin / roadmap-events. Updated: 2026-10-25.
  - Acceptance: Duplicate, delayed, reordered and retried events cannot corrupt state or revive expired permissions.
  - Next: Coordination claim: events; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Integrate authenticated host worker dispatch with current case/permission rechecks and retained provider evidence, then measure end-to-end latency and replanning. Preserve actual OIDC, production isolation and independent/model/human gates. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-events` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES02-01`.
  - Existing code: `endstate/events.py`, `eightball/event_inbox.py`, `tests/test_event_inbox.py`, `eightball/event_work.py`, `tests/test_event_work.py`, `eightball/v2/event_reviews.py`, `tests/test_event_reviews.py`, `eightball/v2/event_outbox.py`, `docs/delivery/lane-reports/events.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-EVENT-INBOX`, `EV-EVENT-WORK`, `EV-EVENT-CONSUMPTION`, `EV-EVENT-OUTBOX`, `EV-EVENT-CASE-BINDING-GAP`, `EV-EVENT-RESULT-SIZE`, `EV-EVENT-RESULT-RETENTION`, `EV-LANE-EVENTS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES02-03 Reviewed graph amendments and affected-route explanations**
  - Status: `partial`. Owner: Devin / roadmap-events. Updated: 2026-10-25.
  - Acceptance: New information can propose a graph/dependency change, but cannot remove restrictions until reviewed at the correct revision.
  - Next: Coordination claim: events; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Complete authenticated host worker dispatch, actual OIDC sign-in and measured event-to-review/replanning evidence. The scoped review page now uses the existing graph editor; preserve production isolation and genuine model/human acceptance gates. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-events` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES02-01`, `ES01-02`.
  - Existing code: `eightball/v2/event_reviews.py`, `tests/test_event_reviews.py`, `eightball/v2/event_api.py`, `tests/test_agency_access.py`, `web/v2/event-review.js`, `tests/browser_event_review.py`, `docs/delivery/lane-reports/events.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-EVENT-CONSUMPTION`, `EV-EVENT-API`, `EV-EVENT-CASE-BINDING-GAP`, `EV-EVENT-REVIEW-UI`, `EV-EVENT-REVIEW-CSP-FAILURE`, `EV-LANE-EVENTS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES02-04 Freshness, cancellation and performance evidence**
  - Status: `partial`. Owner: Devin / roadmap-events. Updated: 2026-10-25.
  - Acceptance: Measured latencies include ingestion, inference and review; incremental replan results match full recomputation; cancelled/stale work cannot commit.
  - Next: Coordination claim: events; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Integrate authenticated host worker dispatch with current case/permission rechecks and retained provider evidence, then measure end-to-end latency and replanning. Preserve actual OIDC, production isolation and independent/model/human gates. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-events` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES02-02`, `ES02-03`.
  - Existing code: `eightball/event_work.py`, `tests/test_event_work.py`, `eightball/v2/event_reviews.py`, `tests/test_event_reviews.py`, `eightball/v2/event_outbox.py`, `eightball/v2/event_api.py`, `tests/test_agency_access.py`, `web/v2/event-review.js`, `tests/browser_event_review.py`, `docs/delivery/lane-reports/events.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-EVENT-WORK`, `EV-EVENT-CONSUMPTION`, `EV-EVENT-OUTBOX`, `EV-EVENT-API`, `EV-EVENT-REVIEW-UI`, `EV-EVENT-RESULT-SIZE`, `EV-EVENT-RESULT-RETENTION`, `EV-LANE-EVENTS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [x] **ES02-05 Bounded structural emergence detectors and typed explanations** (optional, not a version gate)
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-24.
  - Acceptance: Revalidated snapshots produce reproducible, source/graph-linked findings with explicit limits, signed semantics and no mutation/network/model calls; independent fixtures exercise each implemented rule.
  - Next: Preserve the scoped deterministic/governance contract and rerun its regression tests at every integration. This tick is not native, commercial or model-quality approval.
  - Branch/base: `feat/emergent-insights-local` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `ES01-02`.
  - Existing code: `endstate/insights.py`, `tests/test_insight_engine.py`.
  - Evidence: `EV-EMERGENT-INSIGHTS-LOCAL` (registry below).

- [ ] **ES02-06 Selected-course and bounded reconsideration contracts** (optional, not a version gate)
  - Status: `partial`. Owner: ChatGPT. Updated: 2026-09-26.
  - Acceptance: Versioned neutral input/output contracts distinguish candidate routes from a host-authorised course; changes to consulted sources, targets, guards, authority, estimates, clocks and resources produce traceable reconsideration results. Unknown scope requires review. Existing approval invalidation is preserved.
  - Next: Preserve bounded local calculations; defer optional durable-event expansion under the owner freeze.
  - Branch/base: `feat/situation-intelligence-v2` / `14c57907d26ea914e372e544bba4b0bd3988f5dc`.
  - Dependencies: `ES02-01`, `ES02-03`.
  - Existing code: `endstate/course.py`, `eightball/v2/courses.py`, `web/v2/course-view.js`, `tests/test_courses.py`, `tests/browser_courses.py`.
  - Evidence: `EV-CHOSEN-COURSE-LOCAL`, `EV-NATIVE-CLOSEOUT`, `EV-FOUR-SOURCE-20261026` (registry below).
  - Blocker: Original durable event prerequisites remain unaccepted. Independent operator acceptance remains outstanding; native local workflow passes.


## ENDSTATE 0.3: Evaluated intelligence compilation

- [ ] **ES03-01 Provider-independent reviewed outcome compiler**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Source interpretation, typed graph drafting and deterministic validation are clean interchangeable interfaces outside the product layer.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Validate the target-aware compiler on real providers without weakening acceptance; retain independent semantic review. This local change does not complete the compiler quality gate. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES01-01`.
  - Existing code: `eightball/v2/intelligence.py`, `endstate/compilation.py`, `tests/test_endstate_compilation.py`, `docs/delivery/lane-reports/intelligence.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-APP`, `EV-QWEN`, `EV-STAGED-CODE`, `EV-STAGED-MODEL`, `EV-HF-BLACK-LOCAL`, `EV-GENERATION-ROLE-CONTRACT`, `EV-LANE-INTELLIGENCE-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES03-02 Shared real-model semantic acceptance**
  - Status: `blocked`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Use B02-09/B02-11/B02-12 evidence for a valid, useful source-to-plan route, not just JSON or an HTTP response.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Resolve the 8BALL gate once and link the same evidence here.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `B02-09`, `B02-11`, `B02-12`.
  - Evidence: `EV-QWEN` (registry below).
  - Blocker: Failed real graph generation; no independent quality approval.

- [ ] **ES03-03 Optional Jev live judgement integration** (optional, not a version gate)
  - Status: `blocked`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: An authorised real TypeSafe key exercises bounded classifications; permission, output and quality checks are recorded with secrets excluded.
  - Next: Coordination claim: intelligence; optional_hold_no_implementation. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Configure through a secure runtime secret mechanism only when authorised.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `eightball/providers.py`.
  - Evidence: `EV-QWEN` (registry below).
  - Blocker: No authorised TypeSafe credentials supplied for live evaluation.

- [ ] **ES03-04 Local-model installation and live provider status**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Runtime, selected weights, version and connection status are actually detected; downloads are explicit and user-approved.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Retain truthful runtime/configuration status; complete setup/cancellation and actual-provider verification separately. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `eightball/v2/runtime_status.py`, `eightball/v2/hosted.py`, `docs/delivery/lane-reports/intelligence.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-HF-BLACK-LOCAL`, `EV-LANE-INTELLIGENCE-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES03-05 Failure handling, model trace and governed provider selection**
  - Status: `partial`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Provider replacement, refusal, timeout, malformed output, prompt injection and trace retention satisfy shared gates with measured quality.
  - Next: Coordination claim: intelligence; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Retain new strict API transport traces and controlled failure evidence; evaluate the selected actual model and independent source/plan quality before closing the broader gate.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Existing code: `eightball/v2/intelligence.py`, `eightball/v2/store.py`.
  - Evidence: `EV-APP`, `EV-QWEN`, `EV-CLASSIFIER`, `EV-COMPATIBLE-CODE`, `EV-EVALUATION-READINESS`, `EV-REVIEW-EVIDENCE-20261018`, `EV-ANTHROPIC-SETUP` (registry below).

- [x] **ES03-06 Opt-in Hugging Face development transport contract** (optional, not a version gate)
  - Status: `verified`. Owner: ChatGPT. Updated: 2026-09-23.
  - Acceptance: Implemented transport is tested with controlled HTTP responses for permission, configuration, explicit routing, errors, size bounds, source scoping and no state mutation. This scope does not claim live inference.
  - Next: Publish the local checkpoint and configure credentials later for ES03-07; do not reinterpret mocked contract tests as hosted model evaluation.
  - Branch/base: `work/hf-black-drafting` / `824ca6421ff3100e1af596347f2d1247dde8f8dc`.
  - Dependencies: `DOC-01`.
  - Existing code: `eightball/v2/hosted.py`, `tests/test_hosted_and_grounding.py`, `evals/live_huggingface.py`.
  - Evidence: `EV-HF-BLACK-LOCAL` (registry below).

- [ ] **ES03-07 Actual hosted-model comparison on preserved fixtures** (optional, not a version gate)
  - Status: `blocked`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Authorised real HF requests record exact selected model/provider, outputs, same-fixture structural gate and human semantic review. No automatic or fictitious success.
  - Next: Coordination claim: intelligence; optional_hold_no_implementation. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): After explicit configuration, run the manual hosted harness without changing the original four inputs; then use independent labelled cases before model selection.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES03-06`.
  - Existing code: `evals/live_huggingface.py`, `evals/generation-cases.json`.
  - Evidence: `EV-HF-BLACK-LOCAL`, `EV-EVALUATION-READINESS` (registry below).
  - Blocker: No authorised HF token/model/provider configured; no real hosted inference performed.

- [ ] **ES03-08 Recover and reproduce reported human draft-repair implementation** (optional, not a version gate)
  - Status: `blocked`. Owner: Devin / roadmap-intelligence. Updated: 2026-10-25.
  - Acceptance: Recovered or rebuilt exact source preserves the original failure, human edits, source/base revision and separate pending-proposal review; reproduction, stale-state denial and native interaction pass. Assisted repair never satisfies the unassisted model gate.
  - Next: Coordination claim: intelligence; optional_hold_no_implementation. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Recover the exact later source/package or explicitly rebuild the bounded repair on the last verified source. Reproduce its actual tests before marking implemented; never relabel alpha.7 as the reported repair build.
  - Branch/base: `devin/1792969169-roadmap-intelligence` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES03-01`, `B02-02`.
  - Evidence: `EV-DRAFT-RECOVERY-GAP` (registry below).
  - Blocker: The latest supplied repair handoff explicitly reports that no completed working tree was found. Only verified alpha.7 source was recovered in this review.

- [x] **ES03-09 Opt-in OpenAI-compatible hosted endpoint contract** (optional, not a version gate)
  - Status: `verified`. Owner: Codex. Updated: 2026-10-16.
  - Acceptance: Controlled HTTP and native UI checks verify explicit server-owned endpoint/model/provider, permission, pinned routing, bounded strict responses/failure evidence, secrets protection, stage/cancellation/stale/restart guards and unchanged frozen-fixture harness. This transport scope does not claim actual inference or semantic/human acceptance.
  - Next: Bounded software transport contract remains verified. Activate the actual selected endpoint/model and run unchanged generation plus matching lifecycle/native journey within authorised fictional-only scope and confirmed service limits; explicit :free support does not prove free availability or semantic quality.
  - Branch/base: `feat/v02-evaluation-readiness-20261016` / `0fed04b5e299f4a2e53050456559133c1231b088`.
  - Dependencies: `ES03-06`.
  - Existing code: `eightball/v2/compatible.py`, `tests/test_compatible_provider.py`, `tests/test_compatible_integration.py`, `tests/test_compatible_cli.py`, `evals/live_compatible.py`, `docs/v2/QWEN-SETUP.md`.
  - Evidence: `EV-COMPATIBLE-CODE`, `EV-EVALUATION-READINESS` (registry below).


## ENDSTATE 0.4: Domain packs and integration interfaces

- [ ] **ES04-01 Versioned domain-pack contract**
  - Status: `partial`. Owner: Devin / roadmap-domain-packs. Updated: 2026-10-25.
  - Acceptance: Domain packs supply vocabulary, object mappings, action catalogues, policies, confirmation rules, prompts and integrations without core forks.
  - Next: Coordination claim: domain-packs; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Derive the contract from 8BALL and adjacent fixtures. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-domain-packs` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES01-04`.
  - Existing code: `docs/delivery/lane-reports/domain-packs.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-DOMAIN-PACKS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES04-02 8BALL domain pack on ENDSTATE**
  - Status: `partial`. Owner: Devin / roadmap-domain-packs. Updated: 2026-10-25.
  - Acceptance: Fixer terminology/playbooks/experience are product-owned and use the shared contracts; existing routes/data remain compatible.
  - Next: Coordination claim: domain-packs; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Separate domain responsibilities only where real code supports the boundary. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-domain-packs` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES04-01`, `B02-17`.
  - Existing code: `docs/delivery/lane-reports/domain-packs.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-DOMAIN-PACKS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES04-03 Adjacent-domain proof and commercial-lane gate**
  - Status: `partial`. Owner: Devin / roadmap-domain-packs. Updated: 2026-10-25.
  - Acceptance: Sales/support examples run on the same engine with their own evaluation/permissions; new product launches need explicit approval.
  - Next: Coordination claim: domain-packs; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Demonstrate reuse before considering sales, service or social-client products. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-domain-packs` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES04-01`.
  - Existing code: `docs/delivery/lane-reports/domain-packs.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-DOMAIN-PACKS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES04-04 Decide and validate distribution interface**
  - Status: `partial`. Owner: Devin / roadmap-domain-packs. Updated: 2026-10-25.
  - Acceptance: SDK/API/MCP options have a justified scope, auth/version contracts and consumer tests; do not declare all three products shipped.
  - Next: Coordination claim: domain-packs; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Choose the smallest actual integration need with the owner. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-domain-packs` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES04-02`, `ES04-03`.
  - Existing code: `docs/delivery/lane-reports/domain-packs.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-DOMAIN-PACKS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).


## ENDSTATE 1.0: Supported reusable engine

- [ ] **ES10-01 Compatibility, performance, licensing and support policy**
  - Status: `partial`. Owner: Devin / roadmap-domain-packs. Updated: 2026-10-25.
  - Acceptance: Supported engine consumers, migrations, limits, licences and operational ownership are documented and exercised.
  - Next: Coordination claim: domain-packs; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Validate against real product/consumer requirements. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-domain-packs` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES04-04`.
  - Existing code: `docs/delivery/lane-reports/domain-packs.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-DOMAIN-PACKS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

- [ ] **ES10-02 ENDSTATE V1 release gate**
  - Status: `partial`. Owner: Devin / roadmap-domain-packs. Updated: 2026-10-25.
  - Acceptance: Reusable contracts and quality/support promises have evidence; independent release approval is recorded.
  - Next: Coordination claim: domain-packs; engineering_only. Implement only the owned paths in ROADMAP-LANES.md; shared wiring and canonical ledger updates belong to integration. Prior next action (still subject to this bounded claim): Do not block accepted 8BALL sales solely on a standalone-engine release. Integration checkpoint: see docs/delivery/sessions/2026-10-26-roadmap-integration.md; preserve all existing blockers and complete required external acceptance separately.
  - Branch/base: `devin/1792969169-roadmap-domain-packs` / `baca8ad9efa531e5f172058845852963d7d5234a`.
  - Dependencies: `ES10-01`, `ES03-02`, `ES02-04`.
  - Existing code: `docs/delivery/lane-reports/domain-packs.md`, `eightball/agency_host.py`, `docs/v2/AGENCY-HOST.md`.
  - Evidence: `EV-LANE-DOMAIN-PACKS-20261026`, `EV-INTEGRATION-ENGINEERING-20261026` (registry below).

## Evidence registry

These references have specific scopes and may be historical. A reference to a design or a failed model run is not a production acceptance result.

### EV-SPECIALIST-WORKER-20261026

- Kind: `local_engineering`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-specialist-worker.md](../../docs/delivery/sessions/2026-10-26-specialist-worker.md).
- Result/scope: 204 focused checks plus full native:2026 source,2026 installed-wheel,24 JavaScript modules,13 browser suites/454 checks. Exact-source inspection matched; no prediction-quality, production or release acceptance.

### EV-ANTHROPIC-20261026

- Kind: `failed_real_model_evaluation_and_catalogue_selection`.
- Repository evidence: [docs/evidence/anthropic-selection-2026-10-26.json](../../docs/evidence/anthropic-selection-2026-10-26.json).
- Result/scope: Four Sonnet 4.6 fixtures rejected HTTP400; exact cause unknown. Later read-only catalogue lists owner-selected Sonnet 5.5 active. No successful inference or billing-cap verification. Further inference held; exact failed report retained. New request parameters have only controlled tests so far.
- Code revision: `f4ecde62529fc5525220bba6afe4b0ae0c06b63b`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/commit/f4ecde62529fc5525220bba6afe4b0ae0c06b63b).

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

### EV-NATIVE-CLOSEOUT

- Kind: `native_software_acceptance`.
- Repository evidence: [docs/evidence/native-closeout-2026-09-26.json](../../docs/evidence/native-closeout-2026-09-26.json).
- Result/scope: 938 code and 938 installed-kernel checks; all 11 native Chromium suites pass (378 checks). Artifact and source-bound evidence verified. No actual model, independent professional or human accessibility acceptance.
- Code revision: `14c57907d26ea914e372e544bba4b0bd3988f5dc`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/36219154611).

### EV-QWEN-20260927

- Kind: `failed_real_model_evaluation`.
- Repository evidence: [docs/evidence/qwen-baseline-2026-09-27.json](../../docs/evidence/qwen-baseline-2026-09-27.json).
- Result/scope: Recovered historical actual Qwen baseline: three schema-valid extractions; graph rejected with result_bypasses_verification. All live states unchanged. No semantic benchmark or production approval.
- Code revision: `290e310707cf8bef6caf2508c285312b091bd18b`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/actions/runs/36340454120).

### EV-GENERATION-ROLE-CONTRACT

- Kind: `controlled_regression_validation`.
- Repository evidence: [docs/evidence/generation-role-contract-2026-10-15.json](../../docs/evidence/generation-role-contract-2026-10-15.json).
- Result/scope: Native software acceptance passed: 951 code tests, 951 installed-kernel tests, 378 checks in eleven native Chromium suites; source/artifact inspection valid. Zero actual model calls; fresh provider and independent/human gates remain blocked/unaccepted.
- Code revision: `8fad4118f07f91ac1884713530bac9479a7b51b7`.

### EV-GRAPH-KEYBOARD-FOCUS

- Kind: `native_keyboard_regression`.
- Repository evidence: [docs/evidence/graph-keyboard-native-2026-10-15.json](../../docs/evidence/graph-keyboard-native-2026-10-15.json).
- Result/scope: Four native baseline focus failures corrected. 951 code tests, 951 installed-kernel tests and 382 native checks across eleven browser suites passed; source/artifact inspection valid. No human accessibility, dense-case operator or model acceptance.
- Code revision: `5312c6c2f9ef39a68c320b2e1684897c6ac33265`.

### EV-PROVIDER-FAILURE-REVIEW

- Kind: `native_software_validation_and_unperformed_review_preparation`.
- Repository evidence: [docs/evidence/provider-failure-native-2026-10-15.json](../../docs/evidence/provider-failure-native-2026-10-15.json).
- Result/scope: Final cumulative native passed 964 source, 964 installed-kernel tests and 384 browser checks across eleven suites after preserving/correcting an earlier failed navigation run. Inspection valid/passed at tested commit. Review templates remain unperformed; no actual-model, independent semantic or human acceptance.
- Code revision: `294ff578b963dcf50cc8d91d060182894773d159`.

### EV-MAIN-CONSOLIDATION

- Kind: `merged_source_and_native_software_validation`.
- Repository evidence: [docs/evidence/main-consolidation-native-2026-10-15.json](../../docs/evidence/main-consolidation-native-2026-10-15.json).
- Result/scope: Owner-authorized main source integration confirmed; PRs1/2/3 observed Merged. Native source-bound run passed964 source,964 installed-kernel tests and384 browser checks. All74 discoveries, both histories/archives and original task acceptance unchanged. No model/human pass, release or deployment.
- Code revision: `6b57a4503c9e88b4aa97f36b4a24d36ecd82d31f`.

### EV-EVOLUTION-RESEARCH

- Kind: `source_research_and_documentation_validation`.
- Repository evidence: [docs/evidence/evolution-research-2026-10-16.json](../../docs/evidence/evolution-research-2026-10-16.json).
- Result/scope: 26 pinned external repositories mapped to original product goals and proposed staged experiments. Source research and documentation validation only; no runtime, model, human or release acceptance.
- Code revision: `d7d36b842464d7ad0e974a59730a682f1739fccf`.

### EV-TENCENT-MEMORY-RESEARCH

- Kind: `bounded_source_research_and_documentation_validation`.
- Repository evidence: [docs/evidence/tencent-memory-research-2026-10-16.json](../../docs/evidence/tencent-memory-research-2026-10-16.json).
- Result/scope: Tencent memory candidate assessed and combined architecture sharpened. Source-only findings and documentation checks; no upstream runtime, model, independent/human acceptance or required-scope change.
- Code revision: `7309f54539f17b973511e940147a817958891e42`.

### EV-RUFLO-RESEARCH

- Kind: `bounded_source_research_and_documentation_validation`.
- Repository evidence: [docs/evidence/ruflo-research-2026-10-16.json](../../docs/evidence/ruflo-research-2026-10-16.json).
- Result/scope: Ruflo coordination/execution/memory contracts assessed; candidate optional harness, no runtime adoption or model/professional/human acceptance.
- Code revision: `bf54f607bb0e13d0c6adfc0f59ee146e75be287b`.

### EV-RESEARCH-COPY

- Kind: `pinned_source_copy_verification`.
- Repository evidence: [docs/evidence/research-copy-2026-10-16.json](../../docs/evidence/research-copy-2026-10-16.json).
- Result/scope: 28 exact source checkouts, explicit model/LFS/nested exceptions and128 preserved licence/notice blobs verified; no runtime adoption.

### EV-COMPATIBLE-CODE

- Kind: `controlled_transport_and_software_validation`.
- Repository evidence: [docs/evidence/compatible-native-2026-10-16.json](../../docs/evidence/compatible-native-2026-10-16.json).
- Result/scope: Tested ddfead7: 1,104 source tests, 1,104 installed-kernel tests and 391 native checks across 11 suites passed; exact source/artifact inspection valid. No actual provider, semantic or human acceptance.

### EV-RUFLO-OWNER-REVIEW

- Kind: `bounded_source_research`.
- Repository evidence: [docs/evidence/ruflo-owner-review-2026-10-16.json](../../docs/evidence/ruflo-owner-review-2026-10-16.json).
- Result/scope: Current upstream pin rechecked; plain-English owner explanation distinguishes orchestration, free model access, confidence/feedback targets, mocked benchmarks and historical remediations. Source-only; no runtime acceptance.

### EV-WHOLE-SYSTEM-REVIEW

- Kind: `bounded_source_investigation`.
- Repository evidence: [docs/research/github-2026-10-16/whole-system-review.md](../../docs/research/github-2026-10-16/whole-system-review.md).
- Result/scope: All 28 candidate dispositions and source-specific operating/evidence/dependency limits preserved; deferred runtime remains unadopted.

### EV-EVALUATION-READINESS

- Kind: `controlled_software_verification`.
- Repository evidence: [docs/evidence/whole-system-readiness-2026-10-16.json](../../docs/evidence/whole-system-readiness-2026-10-16.json).
- Result/scope: 1,171 source tests, 1,171 installed-kernel regressions and 391 native checks across all 11 suites passed; source/artifact inspection valid. No actual model or independent/human acceptance.

### EV-REVIEW-EVIDENCE-20261018

- Kind: `controlled_software_verification`.
- Repository evidence: [docs/evidence/review-evidence-native-2026-10-18.json](../../docs/evidence/review-evidence-native-2026-10-18.json).
- Result/scope: 1,267 source tests, 1,267 installed-kernel regressions and 391 native browser checks across all 11 suites passed; exact-source/artifact inspection valid before final documentation edits. No actual-model, independent professional or human acceptance.
- Code revision: `25ca5e2dce4f28ec33d9b132cccabfa15b23683e`.

### EV-ANTHROPIC-SETUP

- Kind: `configuration_and_source_inspection`.
- Repository evidence: [docs/evidence/anthropic-setup-2026-10-18.json](../../docs/evidence/anthropic-setup-2026-10-18.json).
- Result/scope: Prepared Anthropic compatibility settings; 142 existing controlled transport/CLI tests passed and isolated format check made no requests. Live compatibility/account access remain unverified; owner must edit old secret destination and supply key securely.

### EV-OCT25-INTEGRATION

- Kind: `integration_and_test_handoff`.
- Repository evidence: [docs/evidence/build-consolidation-native-2026-10-25.json](../../docs/evidence/build-consolidation-native-2026-10-25.json).
- Result/scope: 1267 source + 1267 installed-engine + 391 native browser checks passed; exact inspection valid; both checkpoint CI workflows passed. PR3 closed as already integrated. No model/independent/human acceptance.

### EV-AGENCY-POLICY

- Kind: `controlled_policy_tests`.
- Repository evidence: [docs/evidence/agency-authorisation-native-2026-10-25.json](../../docs/evidence/agency-authorisation-native-2026-10-25.json).
- Result/scope: 1280 source tests, 1280 installed-engine regressions and 391 native browser checks passed; source inspection valid. Policy only, not integrated production enforcement.

### EV-AGENCY-API

- Kind: `controlled_api_and_browser`.
- Repository evidence: [docs/evidence/agency-api-overview-native-2026-10-25.json](../../docs/evidence/agency-api-overview-native-2026-10-25.json).
- Result/scope: 1291 source +1291 installed-engine +394 native browser checks and checkpoint CI passed. Final uncertainty wording passed54 native workspace checks. Agency boundary remains read-only and pre-production.

### EV-EVENT-INBOX

- Kind: `controlled_event_persistence`.
- Repository evidence: [docs/evidence/endstate-event-inbox-native-2026-10-25.json](../../docs/evidence/endstate-event-inbox-native-2026-10-25.json).
- Result/scope: 1302 source tests,1302 installed-engine regressions and394 native browser checks passed; exact inspection valid and both checkpoint CI runs passed. Incoming events remain pending, with no live worker or case mutation.

### EV-EVENT-WORK

- Kind: `controlled_durable_processing`.
- Repository evidence: [docs/evidence/endstate-processing-native-2026-10-25.json](../../docs/evidence/endstate-processing-native-2026-10-25.json).
- Result/scope: 1309 source +1309 installed-engine +396 native browser checks passed; exact inspection valid and checkpoint CI green. Original failed Plan Review race retained and corrected with deterministic native coverage. No actual-model/independent/human acceptance.

### EV-REVIEW-REFRESH-RACE

- Kind: `native_regression_fix`.
- Repository evidence: [docs/evidence/endstate-processing-native-2026-10-25.json](../../docs/evidence/endstate-processing-native-2026-10-25.json).
- Result/scope: Retained local native failure; explicit stale-context recovery and deterministic in-flight revision-change coverage now pass.

### EV-EVENT-CONSUMPTION

- Kind: `controlled_atomic_review`.
- Repository evidence: [docs/evidence/endstate-reviewed-consumption-native-2026-10-25.json](../../docs/evidence/endstate-reviewed-consumption-native-2026-10-25.json).
- Result/scope: 1323 source /1323 installed-engine /396 native browser checks passed; exact inspection and checkpoint CI passed. Public writes, worker/outbox, model and human acceptance remain unfinished.

### EV-EVENT-OUTBOX

- Kind: `controlled_local_delivery`.
- Repository evidence: [docs/evidence/endstate-outbox-native-2026-10-25.json](../../docs/evidence/endstate-outbox-native-2026-10-25.json).
- Result/scope: 1331 source /1331 installed-engine /396 native browser checks passed; exact inspection and both checkpoint CI workflows passed. Local pull-based delivery only; daemon/browser/production/model/human gates remain unfinished.

### EV-EVENT-API

- Kind: `controlled_authenticated_api`.
- Repository evidence: [docs/evidence/endstate-event-api-native-2026-10-25.json](../../docs/evidence/endstate-event-api-native-2026-10-25.json).
- Result/scope: 1345 source /1345 installed-engine /396 native browser checks passed; exact inspection and both checkpoint CI workflows passed. Includes explicit case binding; no browser login/review, worker dispatch or production/model/human acceptance.

### EV-EVENT-CASE-BINDING-GAP

- Kind: `preserved_correctness_failure`.
- Repository evidence: [docs/evidence/endstate-event-api-case-binding-gap-2026-10-25.json](../../docs/evidence/endstate-event-api-case-binding-gap-2026-10-25.json).
- Result/scope: Failure preserved at f75dad5; corrected in cd4ec0c with four case-binding/migration tests and cumulative 1345 source /1345 installed /396 native checks. See EV-EVENT-API.

### EV-EVENT-REVIEW-UI

- Kind: `native_scoped_review_ui`.
- Repository evidence: [docs/evidence/endstate-review-ui-native-2026-10-25.json](../../docs/evidence/endstate-review-ui-native-2026-10-25.json).
- Result/scope: 1346 source /1346 installed-engine /423 native browser checks across 12 suites passed; exact inspection valid. Corrected checkpoint CI unavailable after GitHub authentication failure. Browser review implemented for configured account tokens; not genuine human or OIDC acceptance.

### EV-EVENT-REVIEW-CSP-FAILURE

- Kind: `native_failed`.
- Repository evidence: [docs/evidence/event-review-native-csp-failure-2026-10-25.json](../../docs/evidence/event-review-native-csp-failure-2026-10-25.json).
- Result/scope: Failed native/CI runs preserved. CSP-safe locator assertion with explicit deadline passes corrected full 1346 source /1346 installed /423 native run; see EV-EVENT-REVIEW-UI.

### EV-EVENT-RESULT-SIZE

- Kind: `controlled_boundary_failure`.
- Repository evidence: [docs/evidence/event-result-size-boundary-2026-10-25.json](../../docs/evidence/event-result-size-boundary-2026-10-25.json).
- Result/scope: Historical 12000-character rejection preserved. Bound corrected to 500000 UTF-8 bytes; focused restart/review/export tests passed. See EV-EVENT-RESULT-RETENTION.

### EV-EVENT-RESULT-RETENTION

- Kind: `controlled_full_result_retention`.
- Repository evidence: [docs/delivery/sessions/2026-10-25-complete-result-retention.md](../../docs/delivery/sessions/2026-10-25-complete-result-retention.md).
- Result/scope: 36 focused work/review tests passed; full native verification pending. Complete graph output retained at a 500000-byte UTF-8 bound.

### EV-INTEGRATION-ENGINEERING-20261026

- Kind: `software_validation`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-roadmap-integration.md](../../docs/delivery/sessions/2026-10-26-roadmap-integration.md).
- Result/scope: Shared host, controls and transaction-local identity/source adapters; partial engineering only. No broad acceptance statuses promoted. Final native acceptance pending.

### EV-LANE-COLLABORATION-20261026

- Kind: `lane_software_validation`.
- Repository evidence: [docs/delivery/lane-reports/collaboration.md](../../docs/delivery/lane-reports/collaboration.md).
- Result/scope: Preserved lane-local source/tests/failed experiments and external gates; not a combined-tree acceptance receipt.

### EV-LANE-DOMAIN-PACKS-20261026

- Kind: `lane_software_validation`.
- Repository evidence: [docs/delivery/lane-reports/domain-packs.md](../../docs/delivery/lane-reports/domain-packs.md).
- Result/scope: Preserved lane-local source/tests/failed experiments and external gates; not a combined-tree acceptance receipt.

### EV-LANE-EVENTS-20261026

- Kind: `lane_software_validation`.
- Repository evidence: [docs/delivery/lane-reports/events.md](../../docs/delivery/lane-reports/events.md).
- Result/scope: Preserved lane-local source/tests/failed experiments and external gates; not a combined-tree acceptance receipt.

### EV-EVENTS-DISPATCH-20261025

- Kind: `software_validation`.
- Repository evidence: [docs/delivery/lane-reports/events.md](../../docs/delivery/lane-reports/events.md).
- Result/scope: 1410 full/101 focused tests passed; current grant/source-policy, cross-scope, stale/revocation/cancellation/restart/idempotency/rollback behavior only. No real provider/native/production acceptance.
- Code revision: `f749627f9f7456ddcc5744f22374c57f8c5e64be`.

### EV-EVENTS-REPLAN-20261025

- Kind: `software_validation`.
- Repository evidence: [tests/test_event_replan.py](../../tests/test_event_replan.py).
- Result/scope: Complete typed-response parity for exact-input reuse and full fallback; clock, approval revision, graph/budget/completion/sort/snapshot and detached cache cases. Not general incremental performance proof.
- Code revision: `f749627f9f7456ddcc5744f22374c57f8c5e64be`.

### EV-EVENTS-FROZEN-CHANGELOG-20261025

- Kind: `software_validation`.
- Repository evidence: [docs/delivery/lane-reports/events.md](../../docs/delivery/lane-reports/events.md).
- Result/scope: Expected base-relative canonical changelog failure retained: Changed build needs a new changelog entry. Partition freezes canonical tracking; validate/merge lane fragments centrally.
- Code revision: `f749627f9f7456ddcc5744f22374c57f8c5e64be`.

### EV-LANE-IDENTITY-20261026

- Kind: `lane_software_validation`.
- Repository evidence: [docs/delivery/lane-reports/identity.md](../../docs/delivery/lane-reports/identity.md).
- Result/scope: Preserved lane-local source/tests/failed experiments and external gates; not a combined-tree acceptance receipt.

### EV-LANE-INTELLIGENCE-20261026

- Kind: `lane_software_validation`.
- Repository evidence: [docs/delivery/lane-reports/intelligence.md](../../docs/delivery/lane-reports/intelligence.md).
- Result/scope: Preserved lane-local source/tests/failed experiments and external gates; not a combined-tree acceptance receipt.

### EV-LANE-OPERATIONS-20261026

- Kind: `lane_software_validation`.
- Repository evidence: [docs/delivery/lane-reports/operations.md](../../docs/delivery/lane-reports/operations.md).
- Result/scope: Preserved lane-local source/tests/failed experiments and external gates; not a combined-tree acceptance receipt.

### EV-LANE-VAULT-20261026

- Kind: `lane_software_validation`.
- Repository evidence: [docs/delivery/lane-reports/vault.md](../../docs/delivery/lane-reports/vault.md).
- Result/scope: Preserved lane-local source/tests/failed experiments and external gates; not a combined-tree acceptance receipt.

### EV-FOUR-SOURCE-20261026

- Kind: `source_inspection`.
- Repository evidence: [docs/research/github-2026-10-26/README.md](../../docs/research/github-2026-10-26/README.md).
- Result/scope: Four new pins verified; native design recommendations and unrun experiments only. No upstream runtime/inference. Full32 verification blocked by five older VM discrepancies.

### EV-DECISION-CONTRACTS-20261026

- Kind: `provider_contract_investigation`.
- Repository evidence: [docs/v2/DECISION-PROVIDERS.md](../../docs/v2/DECISION-PROVIDERS.md).
- Result/scope: Owner confirmed native non-chat Jev/Clef/GPT contracts; authenticated catalogue HTTP200 only. No inference, billing or model-quality acceptance.

### EV-NATIVE-REVIEW-20261026

- Kind: `local_engineering`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-native-review-and-decisions.md](../../docs/delivery/sessions/2026-10-26-native-review-and-decisions.md).
- Result/scope: Bounded native review/packet implementation; focused tests and49 native Plan Review checks passed. Full source-bound acceptance is separate. No acceptance/status promotion.

### EV-DECISION-SMOKE-20261026

- Kind: `fictional_provider_smoke`.
- Repository evidence: [docs/v2/DECISION-PROVIDERS.md](../../docs/v2/DECISION-PROVIDERS.md).
- Result/scope: One validated native response each from Jev/Clef/GPT, conflicting choices retained; gateway-recorded total USD0.000008547. Not quality, hard-cap or production acceptance.

### EV-FORECAST-MEASUREMENT-20261026

- Kind: `local_engineering`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-forecast-measurement.md](../../docs/delivery/sessions/2026-10-26-forecast-measurement.md).
- Result/scope: Typed scoring and six fictional worlds: zero configured forecasts; no predictive accuracy. Full native engineering acceptance passed:1979 source and installed-wheel regressions and454 browser checks. No status or model-quality promotion.

### EV-SPECIALIST-PRESENTATION-20261026

- Kind: `local_engineering`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-specialist-presentation.md](../../docs/delivery/sessions/2026-10-26-specialist-presentation.md).
- Result/scope: Exact ba1fd41 native source/artifacts matched:2038 source tests,2038 installed-wheel regressions,24 JS modules,466 checks across13 native suites. Read-only retained comparison only; no inference, quality approval, merge or release.

### EV-INFORMATION-LOOP-20261026

- Kind: `local_engineering`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-information-loop.md](../../docs/delivery/sessions/2026-10-26-information-loop.md).
- Result/scope: Exact a7cc1d6 native source/artifacts matched:2057 source tests,2057 installed-wheel regressions,24 JS modules,474 checks across13 native suites. Explicit questions and separate observations/rechecks only; no inference, predictive/quality/production approval.

### EV-SONNET-NATIVE-20261026

- Kind: `real_model_evaluation`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-sonnet-native.md](../../docs/delivery/sessions/2026-10-26-sonnet-native.md).
- Result/scope: Actual Sonnet four-fixture generation and scripted 20-step native journey passed; failed attempts retained. Exact software code 6ce6151 passed 2090 source + 2090 installed-wheel tests, 24 JS modules and all 13 native suites/474 checks; inspected before documentation closeout. Independent quality/human/production gates remain open.
- Code revision: `6ce61517d7dac347d98170b66274917f3f2e5006`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/commit/6ce61517d7dac347d98170b66274917f3f2e5006).

### EV-NATIVE-USAGE-20261026

- Kind: `controlled_http_tests`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-native-usage.md](../../docs/delivery/sessions/2026-10-26-native-usage.md).
- Result/scope: Five controlled failures retained before correction. Exact 08b1cde code passed 2096 source + 2096 installed-wheel tests, 24 JS modules, compilation and all 13 native suites / 474 checks. Inspected before documentation closeout. No additional model calls or change to prior complete usage estimates; independent gates remain open.
- Code revision: `08b1cde2bdf3fa091576b25b2484d45602c69d4b`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/commit/08b1cde2bdf3fa091576b25b2484d45602c69d4b).

### EV-SONNET-LIFECYCLE-20261026

- Kind: `real_model_evaluation`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-provider-lifecycle.md](../../docs/delivery/sessions/2026-10-26-provider-lifecycle.md).
- Result/scope: Five fresh Sonnet generation requests passed all four frozen fixtures; source-matched configured-provider lifecycle passed cancel, supersede and owned restart with three first-stage admissions and no publication, further stage or unintended mutation. Remote receipt/completion/billing unknown; no UI/human/semantic acceptance. Full software verification recorded separately.
- Code revision: `a31283785f6ccc2a5c31b9b936a9da353dcfb3fe`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/commit/a31283785f6ccc2a5c31b9b936a9da353dcfb3fe).

### EV-HISTORICAL-REPLAY-20261026

- Kind: `real_model_evaluation`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-historical-replay.md](../../docs/delivery/sessions/2026-10-26-historical-replay.md).
- Result/scope: One masked actual Sonnet response: p=0.45, observed=false, Brier=0.2025 versus 0.25. Model admitted recognition; two source-summary errors retained. Inconclusive retrospective diagnostic, not independent prediction evidence. 52 offline protocol and 34 forecast tests pass; full software closeout remains separate.

### EV-LIFECYCLE-SOFTWARE-20261026

- Kind: `native_browser`.
- Repository evidence: [docs/delivery/sessions/2026-10-26-provider-lifecycle.md](../../docs/delivery/sessions/2026-10-26-provider-lifecycle.md).
- Result/scope: Exact e3c92f0 software passed 2100 source and installed-wheel tests, 24 JS modules and 475 native checks in 13 suites. All failed/partial runs retained. No model inference during software repair; actual-provider evidence retains its original source binding. Independent semantic, human, predictive and production gates remain open.
- Code revision: `e3c92f05db73627d0c368aad919d00142fc85819`.
- External record: [verification source](https://github.com/EmotiveImpact/8ball/commit/e3c92f05db73627d0c368aad919d00142fc85819).
