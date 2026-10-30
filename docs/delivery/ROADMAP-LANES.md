# Seven-lane roadmap ownership checkpoint

> Coordination/engineering reservations only. `progress.json` remains the only task-status source; no code or product gate is claimed by this document.

Plan branch: `devin/1792969169-roadmap-plan`. Inspected source base: `baca8ad9efa531e5f172058845852963d7d5234a`. Builders start from the **pushed plan commit**, not a historical branch tip; `base_commit` in the claims records the inspected source baseline. Obtain the exact plan commit from the coordinator and verify it before creating your assigned new branch. The plan commit adds coordination only.

The inspected remote agency branch had advanced to `2b1b465ebfa1b433c8f128b0478f6806dce9e2e7` with documentation/evidence changes. This checkpoint intentionally starts at the requested base, does not import those later changes, and does not modify PR #5 or main. Integration must reconcile that later ledger/evidence additively, without attributing its native report to this tree.

## Authority and acceptance

- 8BALL is the fixer product; ENDSTATE is the reusable engine, not a replacement app or a new product launch.
- Preserve the working `/` and `/v2/` local app, original alpha import/audit lineage, CSP, current permission/revision checks and native acceptance. Unknown is not false.
- Evidence, proposals, selected courses, reviews, action permission, completion and observed effects stay separate. A lane reservation is not implementation, independent review or acceptance.
- Only fictional data. No implicit external sends, real-client pilot, paid/live inference, model downloads, independent review sign-off, release, deployment, main merge, deferred research runtime or new industry application is authorised here.
- All original task statuses, acceptance text, required flags, dependencies, code/evidence references and blockers remain unchanged. Owner/branch/base/date and a bounded prefix to the prior next action are the only per-task changes. `not_started`, `partial` and `blocked` remain truthful; the owner fields reserve work rather than assert it has started.
- Verified tasks are not reassigned. Unassigned B03-07 and ES02-06 stay optional and unaccepted. Every assigned optional task stays on an explicit no-implementation hold; do not silently expand B02-21/22, ES03-03/07/08 or B04-04. ES03-03/07 would additionally require explicit live/data/provider permission. B03-06 is pilot tooling only.
- Task `code_paths` retain historical evidence locations and are **not** a builder edit allowlist. Only the ownership lists below grant file ownership. Dependencies are contracts to consume, not permission to edit another lane.

## Integration-only shared ownership

Builders must not edit the paths below, dependency manifests/lockfiles anywhere, common routers/state/command services, navigation/global styling, acceptance orchestration or cross-lane wiring. Any unlisted existing runtime path is integration-owned until explicitly assigned. Frozen originals and source-only research are not editable builder scope. Integration itself remains a later stage, not an eighth builder lane.

- `eightball/api.py`
- `eightball/v2/api.py`
- `eightball/v2/store.py`
- `eightball/v2/services.py`
- `eightball/v2/commands.py`
- `eightball/v2/contracts.py`
- `endstate/contracts.py`
- `endstate/api.py`
- `pyproject.toml`
- `endstate/pyproject.toml`
- `requirements*.txt`
- `**/package.json`
- `**/package-lock.json`
- `**/*lock*`
- `scripts/acceptance.py`
- `scripts/delivery.py`
- `scripts/changelog.py`
- `scripts/emergence.py`
- `web/v2/app.js`
- `web/v2/index.html`
- `web/v2/style.css`
- `docs/delivery/progress.json`
- `docs/delivery/PROGRESS.md`
- `docs/delivery/changelog.json`
- `CHANGELOG.md`
- `docs/delivery/emergence.json`
- `docs/delivery/EMERGENCE-REGISTER.md`
- `docs/delivery/ROADMAP-LANES.md`
- `tests/test_delivery_tracking.py`
- `tests/test_changelog.py`
- `tests/test_emergence_register.py`

Frozen/source-only exclusions (override globs): `evals/generation-cases.json`, `docs/reference/8BALL-V0.2-ASTRA-PRD.md`, `research/**`.

## Actual router/service seam

The current `eightball/api.py:make_app(store, token, *, agency_access=None)` sets CSP/auth boundaries and calls `eightball.v2.api.router(V2Store(store.path), store, authorised, agency_events=...)`. The latter creates `APIRouter(prefix="/api/v2", dependencies=[Depends(authorised)])` and conditionally calls `eightball.v2.event_api.register_event_routes(router, store)` when the configured agency registry and store share the same resolved database path. This is existing source, not a claim of production authentication or a newly running worker.

Use that registration pattern: lane-local `register_<lane>_routes(router: APIRouter, service)` registers relative matter/case-scoped routes; service implementations receive explicit authorised context/current-grant checker, case/object/revision and bounded injected storage/provider/clock adapters. Prefer small protocols/typed result contracts in owned modules, not imports of another lane's concrete internals. A route-level dependency never replaces current operation/matter/object authorisation inside the transaction. Existing event registration signatures stay compatible unless integration explicitly changes both call sites.

Builders supply the service/registration entry point, adapter requirements, migrations as proposed lane-local data (never run against an operator database), relative route/method and operation map, error/revocation semantics, isolated UI module mount API and contract tests. No lane mounts itself in common routers, modifies shared schemas/tables/nav/manifests, or starts a daemon on import. Integration explicitly constructs/injects services, registers relative routes under the existing authenticated router, adds route authorisation mappings, connects state/provenance adapters and navigation, resolves schema/dependency changes, and runs combined native regression/security checks. Any shared-database migration, missing dependency or common API change is an integration request, not an ownership escape hatch.

Events implements dispatch and durable work lifecycle; intelligence implements providers/proposals/analysis services but does not duplicate dispatch. Identity supplies current grants, not event work. Vault supplies immutable source handles/provenance without rewriting Source Desk; collaboration consumes reviewed projections. Domain packs provide neutral contract fixtures without a core fork. Operations consumes evidence rather than lowering acceptance.

## Reproducible builder handoff

1. Fetch the exact pushed plan commit supplied by the coordinator. Verify a clean worktree; create only your reserved branch from that commit. Record the actual builder starting commit separately from the inspected source baseline. Do not reset/discard/force-push/merge main or change a PR.
2. Read AGENTS.md and required current product/delivery/architecture/validation records. Use Python 3.12+, documented dependencies and available nvm Node. Never execute source-only research.
3. Work only in your allowlist. Unlisted new files need an explicit integration assignment; do not invent a cross-lane schema or package manifest change. Produce bounded contract/negative tests and preserve old audit/source compatibility.
4. Do not concurrently edit canonical delivery JSON/generated documents. Write your factual receipt to the lane report path and append-only emergence/changelog proposals to your two lane-local fragments. Use only your reserved IDs; unused IDs are gaps, not discoveries. Fragments must use the existing item/entry schemas, immutable discovery wording and decision history. They are proposals, not a second status source or accepted register.
5. Report exact changed paths, task-by-task engineering evidence, source commit, checks and failures, untouched external/human gates, integration requests, emergence review, pushed/unpushed state and next action. Never mark a broad ledger task verified from a bounded test.
6. Integration serially reconciles lane commits and later upstream evidence, appends fragments to canonical registers/changelog, updates task evidence/status only on actual proof, regenerates documents and runs validators/tracking tests/native acceptance as separately authorised. No merge/deploy/release permission is implied.

## Lane assignments and exact ledger requirements

### 1. events

- Owner: `Devin / roadmap-events`
- Branch: `devin/1792969169-roadmap-events`
- Inspected base: `baca8ad9efa531e5f172058845852963d7d5234a`
- Scope: Bounded event envelopes, durable inbox/work queue, current-authority worker dispatch, reviewed graph impact and notification/connector tooling. No implicit external sends, permission revival or approval bypass. Reserved discoveries: EM-113..EM-132 (20 IDs; reserved, not findings).
- Owned paths (exclusions above take precedence): `endstate/events.py`; `eightball/event_inbox.py`; `eightball/event_work.py`; `eightball/v2/event_api.py`; `eightball/v2/event_reviews.py`; `eightball/v2/event_outbox.py`; `eightball/event_workers/**`; `web/v2/event-review.*`; `web/v2/event-*.js`; `web/v2/event-*.html`; `tests/test_event*.py`; `tests/browser_event_review.py`; `docs/endstate/EVENT-INBOX.md`; `docs/delivery/lane-reports/events.md`; `docs/delivery/lane-reports/events-emergence.json`; `docs/delivery/lane-reports/events-changelog.json`
- Dependencies/integration gates: Identity supplies authenticated worker identity/current-grant authorisation; intelligence supplies provider/proposal services. Keep source/receipt ordering, cancellation, revision and reviewed consumption checks. Integration wires registration and measures combined ingestion/inference/review latency.

The following are copied verbatim from the canonical acceptance fields, not completion claims:

#### ES02-01 — Normalised event and authority contract

Required: `true`. Bounded mode: `engineering_only`.

Events carry source, version, occurrence/receipt time, matter scope and review status; incoming text never gets command authority.

Ledger prerequisites: ES01-01.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES02-02 — Durable ordered updates, idempotency and replay

Required: `true`. Bounded mode: `engineering_only`.

Duplicate, delayed, reordered and retried events cannot corrupt state or revive expired permissions.

Ledger prerequisites: ES02-01.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES02-03 — Reviewed graph amendments and affected-route explanations

Required: `true`. Bounded mode: `engineering_only`.

New information can propose a graph/dependency change, but cannot remove restrictions until reviewed at the correct revision.

Ledger prerequisites: ES02-01, ES01-02.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES02-04 — Freshness, cancellation and performance evidence

Required: `true`. Bounded mode: `engineering_only`.

Measured latencies include ingestion, inference and review; incremental replan results match full recomputation; cancelled/stale work cannot commit.

Ledger prerequisites: ES02-02, ES02-03.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### B03-04 — Authorised ingestion, event handling and notifications

Required: `true`. Bounded mode: `engineering_only`.

Actual source connectors, durable updates and notifications respect permissions, source review, ordering and retry limits.

Ledger prerequisites: B03-01, ES02-01, ES02-02.
Preserved blockers: none recorded; absence is not a production/semantic pass.

### 2. identity

- Owner: `Devin / roadmap-identity`
- Branch: `devin/1792969169-roadmap-identity`
- Inspected base: `baca8ad9efa531e5f172058845852963d7d5234a`
- Scope: Agency access/authorisation, OIDC login/session contracts, revocation and matter/operation denial coverage. No production identity-provider configuration or credentials presumed. Reserved discoveries: EM-133..EM-152 (20 IDs; reserved, not findings).
- Owned paths (exclusions above take precedence): `eightball/agency_access.py`; `eightball/authorisation.py`; `eightball/oidc/**`; `eightball/v2/identity_api.py`; `web/v2/identity-*`; `tests/test_agency_access.py`; `tests/test_authorisation.py`; `tests/test_identity*.py`; `tests/test_oidc*.py`; `docs/v2/AGENCY-ACCESS.md`; `docs/delivery/lane-reports/identity.md`; `docs/delivery/lane-reports/identity-emergence.json`; `docs/delivery/lane-reports/identity-changelog.json`
- Dependencies/integration gates: Expose a fail-closed current identity/grant service to every lane; use the existing Operation/Identity/Resource/Grant boundary. Provider credentials, independent security review and production isolation remain external gates; integration owns middleware/common router attachment.

The following are copied verbatim from the canonical acceptance fields, not completion claims:

#### B03-01 — Identity, organisations and matter-scoped authorisation

Required: `true`. Bounded mode: `engineering_only`.

Authenticated identities and cross-tenant/matter denial tests cover read, write, export, search and model inference.

Ledger prerequisites: none recorded.
Preserved blockers: none recorded; absence is not a production/semantic pass.

### 3. vault

- Owner: `Devin / roadmap-vault`
- Branch: `devin/1792969169-roadmap-vault`
- Inspected base: `baca8ad9efa531e5f172058845852963d7d5234a`
- Scope: New immutable-original vault/quarantine/scan/hash, encryption/retention/hold/deletion and audited-access services plus isolated router/UI modules. Existing source provenance remains compatible; no real client material. Reserved discoveries: EM-153..EM-172 (20 IDs; reserved, not findings).
- Owned paths (exclusions above take precedence): `eightball/vault/**`; `eightball/v2/vault_api.py`; `web/v2/vault-*`; `tests/test_vault*.py`; `docs/v2/VAULT.md`; `docs/delivery/lane-reports/vault.md`; `docs/delivery/lane-reports/vault-emergence.json`; `docs/delivery/lane-reports/vault-changelog.json`
- Dependencies/integration gates: Consume identity current-grant contracts; expose versioned source handles/hash/provenance adapters without editing Source Desk/store/common routers. Integration connects persistence/source adapters; production key management, scanner and recovery evidence are not assumed.

The following are copied verbatim from the canonical acceptance fields, not completion claims:

#### B03-02 — Encrypted evidence vault and retention controls

Required: `true`. Bounded mode: `engineering_only`.

Immutable originals, hashes, upload quarantine/scanning, encryption, retention/hold/deletion and audited access are tested.

Ledger prerequisites: B03-01.
Preserved blockers: none recorded; absence is not a production/semantic pass.

### 4. collaboration

- Owner: `Devin / roadmap-collaboration`
- Branch: `devin/1792969169-roadmap-collaboration`
- Inspected base: `baca8ad9efa531e5f172058845852963d7d5234a`
- Scope: New revocable expert grants and separately reviewed client projections, collaboration router/UI and isolation tests. Internal records are never a default client view; no sharing/send by implication. Reserved discoveries: EM-173..EM-192 (20 IDs; reserved, not findings).
- Owned paths (exclusions above take precedence): `eightball/collaboration/**`; `eightball/projections/**`; `eightball/v2/collaboration_api.py`; `web/v2/collaboration-*`; `tests/test_collaboration*.py`; `tests/test_projection*.py`; `docs/v2/COLLABORATION.md`; `docs/delivery/lane-reports/collaboration.md`; `docs/delivery/lane-reports/collaboration-emergence.json`; `docs/delivery/lane-reports/collaboration-changelog.json`
- Dependencies/integration gates: Consume identity current-grant service and vault opaque source handles; projection review must bind exact object/matter/revision and revocation. Integration supplies case read/service adapter and navigation. No new secure portal/deployment claim.

The following are copied verbatim from the canonical acceptance fields, not completion claims:

#### B03-03 — Scoped specialist collaboration and real client portal

Required: `true`. Bounded mode: `engineering_only`.

Experts receive revocable matter/object grants; clients receive separately reviewed projections, never internal records by default.

Ledger prerequisites: B03-01, B03-02.
Preserved blockers: none recorded; absence is not a production/semantic pass.

### 5. operations

- Owner: `Devin / roadmap-operations`
- Branch: `devin/1792969169-roadmap-operations`
- Inspected base: `baca8ad9efa531e5f172058845852963d7d5234a`
- Scope: New restore/audit/incident/revocation and onboarding/support/release-readiness tooling. B03-06 is fictional pilot preparation/tooling only; B10 deliverables do not confer legal, brand, customer or professional acceptance. Reserved discoveries: EM-193..EM-212 (20 IDs; reserved, not findings).
- Owned paths (exclusions above take precedence): `eightball/operations/**`; `scripts/operations/**`; `docs/operations/**`; `tests/test_operations*.py`; `tests/test_pilot_tooling*.py`; `docs/delivery/lane-reports/operations.md`; `docs/delivery/lane-reports/operations-emergence.json`; `docs/delivery/lane-reports/operations-changelog.json`
- Dependencies/integration gates: Identity/vault/collaboration/events furnish recovery and revocation service contracts. Consume evidence from all lanes without editing the acceptance runner. Real pilot participants, legal/brand/licence clearance, operating owner, customer acceptance and release/deploy authorisation remain external gates.

The following are copied verbatim from the canonical acceptance fields, not completion claims:

#### B03-05 — Independent audit checkpoints, recovery and operational monitoring

Required: `true`. Bounded mode: `engineering_only`.

Restore rehearsal, audit anchoring, revocation and operational incident tests pass without sensitive log leakage.

Ledger prerequisites: none recorded.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### B10-01 — Commercial onboarding, support and launch readiness

Required: `true`. Bounded mode: `engineering_only`.

Customer onboarding, support, service terms, brand/licence clearance and operating ownership are ready for the accepted scope.

Ledger prerequisites: B03-06.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### B10-02 — 8BALL V1 fixer production release

Required: `true`. Bounded mode: `engineering_only`.

All advertised capabilities, security, accessibility, recovery, model policy and customer acceptance are evidenced for supported environments.

Ledger prerequisites: B10-01, B04-03.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### B03-06 — Limited qualified-fixer pilot acceptance

Required: `true`. Bounded mode: `fictional_pilot_tooling_only`.

Authorised pilot users validate usefulness, safety, corrections and confidentiality; critical findings closed before wider release.

Ledger prerequisites: B02-18, B03-01, B03-02, B03-03, B03-04, B03-05.
Preserved blockers: none recorded; absence is not a production/semantic pass.

### 6. domain-packs

- Owner: `Devin / roadmap-domain-packs`
- Branch: `devin/1792969169-roadmap-domain-packs`
- Inspected base: `baca8ad9efa531e5f172058845852963d7d5234a`
- Scope: New ENDSTATE domain-pack schemas/loader contracts, fixer/neutral/sales/support fictional fixtures and consumer/version/migration tooling. Demonstrate reuse without core forks; no second application, public SDK/API/MCP launch or independent ENDSTATE release. Reserved discoveries: EM-213..EM-232 (20 IDs; reserved, not findings).
- Owned paths (exclusions above take precedence): `endstate/domain_packs/**`; `tests/fixtures/domain_packs/**`; `tests/test_domain_pack*.py`; `docs/endstate/DOMAIN-PACKS.md`; `docs/delivery/lane-reports/domain-packs.md`; `docs/delivery/lane-reports/domain-packs-emergence.json`; `docs/delivery/lane-reports/domain-packs-changelog.json`
- Dependencies/integration gates: Use existing engine contracts and keep endstate free of eightball imports. Intelligence supplies fixer playbook adapter inputs. Integration approves any shared contract/manifests or API exposure. Distribution, licence/support commitments and independent release approval remain gated.

The following are copied verbatim from the canonical acceptance fields, not completion claims:

#### ES04-01 — Versioned domain-pack contract

Required: `true`. Bounded mode: `engineering_only`.

Domain packs supply vocabulary, object mappings, action catalogues, policies, confirmation rules, prompts and integrations without core forks.

Ledger prerequisites: ES01-04.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES04-02 — 8BALL domain pack on ENDSTATE

Required: `true`. Bounded mode: `engineering_only`.

Fixer terminology/playbooks/experience are product-owned and use the shared contracts; existing routes/data remain compatible.

Ledger prerequisites: ES04-01, B02-17.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES04-03 — Adjacent-domain proof and commercial-lane gate

Required: `true`. Bounded mode: `engineering_only`.

Sales/support examples run on the same engine with their own evaluation/permissions; new product launches need explicit approval.

Ledger prerequisites: ES04-01.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES04-04 — Decide and validate distribution interface

Required: `true`. Bounded mode: `engineering_only`.

SDK/API/MCP options have a justified scope, auth/version contracts and consumer tests; do not declare all three products shipped.

Ledger prerequisites: ES04-02, ES04-03.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES10-01 — Compatibility, performance, licensing and support policy

Required: `true`. Bounded mode: `engineering_only`.

Supported engine consumers, migrations, limits, licences and operational ownership are documented and exercised.

Ledger prerequisites: ES04-04.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES10-02 — ENDSTATE V1 release gate

Required: `true`. Bounded mode: `engineering_only`.

Reusable contracts and quality/support promises have evidence; independent release approval is recorded.

Ledger prerequisites: ES10-01, ES03-02, ES02-04.
Preserved blockers: none recorded; absence is not a production/semantic pass.

### 7. intelligence

- Owner: `Devin / roadmap-intelligence`
- Branch: `devin/1792969169-roadmap-intelligence`
- Inspected base: `baca8ad9efa531e5f172058845852963d7d5234a`
- Scope: Unfinished source interpretation, graph compilation, provider/runtime, source clarity, evaluation/quality/review/UX and intelligence/playbook tooling within existing contracts. Optional tasks are explicit holds, not automatic implementation; no worker/auth/common-router ownership or actual inference/model downloads. Reserved discoveries: EM-233..EM-252 (20 IDs; reserved, not findings).
- Owned paths (exclusions above take precedence): `eightball/v2/intelligence.py`; `eightball/v2/analysis_jobs.py`; `eightball/v2/runtime_status.py`; `eightball/v2/hosted.py`; `eightball/v2/compatible.py`; `eightball/v2/grounding.py`; `eightball/v2/source_desk.py`; `eightball/v2/source_contracts.py`; `eightball/v2/playbooks.py`; `eightball/v2/plan_review.py`; `eightball/v2/insights.py`; `endstate/compilation.py`; `endstate/time_review.py`; `endstate/plan_review.py`; `endstate/insights.py`; `web/v2/job-view.js`; `web/v2/source-model.js`; `web/v2/source-view.js`; `web/v2/grounding-view.js`; `web/v2/plan-review-view.js`; `web/v2/insights-view.js`; `web/v2/graph-model.js`; `web/v2/graph-view.js`; `evals/**`; `tests/test_intelligence*.py`; `tests/test_analysis_jobs.py`; `tests/test_runtime_status.py`; `tests/test_hosted_and_grounding.py`; `tests/test_hosted_eval_retention.py`; `tests/test_compatible*.py`; `tests/test_provider*.py`; `tests/test_grounding.py`; `tests/test_time_review.py`; `tests/test_source_desk.py`; `tests/test_source_view_races.py`; `tests/test_plan_review.py`; `tests/test_insight*.py`; `tests/test_playbooks.py`; `tests/test_endstate_compilation.py`; `tests/test_graph_explorer.py`; `docs/delivery/lane-reports/intelligence.md`; `docs/delivery/lane-reports/intelligence-emergence.json`; `docs/delivery/lane-reports/intelligence-changelog.json`; `eightball/intelligence/**`; `endstate/intelligence/**`; `web/v2/intelligence-*`; `tests/test_evaluation*.py`; `tests/test_learning*.py`
- Dependencies/integration gates: Events owns dispatch/inbox/worker; identity owns auth. Consume source-handle/domain-pack contracts via adapters; integration owns common state/command/router/nav changes and full acceptance. Actual-model B02-09/B02-12/ES03-02, expert-labelled B02-11, human accessibility/security and release gates remain open. Optional live classifiers/research/rebuild candidates stay held.

The following are copied verbatim from the canonical acceptance fields, not completion claims:

#### B02-09 — Reliable reviewed graph proposals for new situations

Required: `true`. Bounded mode: `engineering_only`.

Actual-model graph fixtures pass with all referenced actions present, meaningful alternative paths and explicit final verification. No silent template substitution.

Ledger prerequisites: none recorded.
Preserved blockers: Native Sonnet frozen generation and actual-provider native journey now pass. Account cap absence explicitly accepted for bounded fictional tests; no cap is claimed. Independent semantic/reliability acceptance remains outstanding.; Independent semantic evaluation must check branch-neutral readiness, relevant confirmation evidence, all target parts, alternatives and final-verification separation. Historical replay does not satisfy this gate..

#### B02-10 — Robust source extraction, deadlines and entity reconciliation

Required: `true`. Bounded mode: `engineering_only`.

Reviewed multi-source extraction preserves negation, uncertainty, identity and quoted support; date changes become explicit reviewed scheduling proposals.

Ledger prerequisites: none recorded.
Preserved blockers: Independent multi-source identity/date usefulness review remains outstanding.; No automatic coreference, global actor merge, business-calendar semantics or reliable arbitrary model extraction is claimed..

#### B02-11 — Independent quality evaluation and production-model selection

Required: `true`. Bounded mode: `engineering_only`.

Expert-labelled held-out data and predeclared acceptance thresholds measure semantic errors, omissions, corrections, latency and abstention.

Ledger prerequisites: none recorded.
Preserved blockers: Independent reviewer labels, approved prospective protocol and actual-provider comparison are not completed..

#### B02-12 — Full twenty-step real-model V0.2 acceptance journey

Required: `true`. Bounded mode: `engineering_only`.

Blank case -> real extraction -> mixed human review -> valid graph -> distinct routes -> new evidence/replan -> isolated refusal -> approval/completion -> reload/export, all native.

Ledger prerequisites: B02-09, B02-10, B02-11.
Preserved blockers: Actual-provider scripted native twenty-step journey now passes; genuinely human acceptance and independent quality remain unperformed. Scripted review and synthetic observations do not meet those gates..

#### B02-14 — Source chunking, duplication and reviewer-safe object reconciliation

Required: `true`. Bounded mode: `engineering_only`.

Longer sources retain exact provenance; duplicates and entity merges cannot rewrite observed meanings or lose attribution.

Ledger prerequisites: none recorded.
Preserved blockers: Independent multi-source identity/date usefulness review remains outstanding.; No automatic coreference, global actor merge, business-calendar semantics or reliable arbitrary model extraction is claimed..

#### B02-15 — Model progress/cancellation and accurate installation status

Required: `true`. Bounded mode: `engineering_only`.

The UI reports actual runtime/weights/credential state and cancels work without stale commits. No silent large model download.

Ledger prerequisites: ES03-04.
Preserved blockers: Selected Sonnet API/process cancellation, supersession and restart observations pass; actual-provider native-UI lifecycle/installation-status acceptance remain unverified. Remote receipt, cancellation and billing are not established by local job states..

#### B02-16 — Complete accessibility and supported-environment validation

Required: `true`. Bounded mode: `engineering_only`.

Keyboard, screen reader, empty/error/loading states and supported browsers/platform startup paths pass an explicit review.

Ledger prerequisites: none recorded.
Preserved blockers: Human screen-reader and supported-browser/OS review remains outstanding; Linux/Chromium native software tests passed..

#### B02-18 — V0.2 acceptance and release decision

Required: `true`. Bounded mode: `engineering_only`.

All required V0.2 subparts have scoped evidence; reviews/gates pass; approval to integrate/release is recorded separately.

Ledger prerequisites: B02-01, B02-02, B02-03, B02-04, B02-05, B02-06, B02-07, B02-08, B02-09, B02-10, B02-11, B02-12, B02-13, B02-14, B02-15, B02-16, B02-17, B02-19, B02-20.
Preserved blockers: Real-model journey and developer-quality work remain unaccepted..

#### B02-19 — Black operator visual system and transparent intelligence controls

Required: `true`. Bounded mode: `engineering_only`.

Black/graphite design, legible status labels, exact-target review, provider controls and mobile lock work across the existing native desktop/mobile workflow without losing evidence/approval functions.

Ledger prerequisites: B02-07.
Preserved blockers: Owner visual review and broader human accessibility acceptance remain outstanding..

#### B02-20 — Black relationship explorer with local focus, directed flow and records view

Required: `true`. Bounded mode: `engineering_only`.

Explore actual case records using Connections, Outcome flow and Records; inspect source/history and exact logic; keyboard/mobile controls and view-only audit invariants pass, including native browser validation.

Ledger prerequisites: B02-04, B02-07, B02-19.
Preserved blockers: Representative dense-case operator usability and broader accessibility review remain outstanding..

#### B02-21 — Evidence-linked Emergent Insights and review workspace

Required: `false`. Bounded mode: `optional_hold_no_implementation`.

Current/historical findings, explicit review and hypotheses, safe question promotion, stale-context handling, reload/export and native desktop/mobile acceptance without changing factual state.

Ledger prerequisites: ES02-05, B02-03.
Preserved blockers: Operator acceptance remains outstanding; the complete native insight journey now passes..

#### B02-22 — Operator usefulness and full Emergent Insights acceptance

Required: `false`. Bounded mode: `optional_hold_no_implementation`.

Owner/operator review of false positives, missed patterns, duplicate noise, thresholds and the complete native review journey before the feature is accepted.

Ledger prerequisites: B02-21.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES03-01 — Provider-independent reviewed outcome compiler

Required: `true`. Bounded mode: `engineering_only`.

Source interpretation, typed graph drafting and deterministic validation are clean interchangeable interfaces outside the product layer.

Ledger prerequisites: ES01-01.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES03-02 — Shared real-model semantic acceptance

Required: `true`. Bounded mode: `engineering_only`.

Use B02-09/B02-11/B02-12 evidence for a valid, useful source-to-plan route, not just JSON or an HTTP response.

Ledger prerequisites: B02-09, B02-11, B02-12.
Preserved blockers: Failed real graph generation; no independent quality approval..

#### ES03-03 — Optional Jev live judgement integration

Required: `false`. Bounded mode: `optional_hold_no_implementation`.

An authorised real TypeSafe key exercises bounded classifications; permission, output and quality checks are recorded with secrets excluded.

Ledger prerequisites: none recorded.
Preserved blockers: No authorised TypeSafe credentials supplied for live evaluation..

#### ES03-04 — Local-model installation and live provider status

Required: `true`. Bounded mode: `engineering_only`.

Runtime, selected weights, version and connection status are actually detected; downloads are explicit and user-approved.

Ledger prerequisites: none recorded.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES03-05 — Failure handling, model trace and governed provider selection

Required: `true`. Bounded mode: `engineering_only`.

Provider replacement, refusal, timeout, malformed output, prompt injection and trace retention satisfy shared gates with measured quality.

Ledger prerequisites: none recorded.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### ES03-07 — Actual hosted-model comparison on preserved fixtures

Required: `false`. Bounded mode: `optional_hold_no_implementation`.

Authorised real HF requests record exact selected model/provider, outputs, same-fixture structural gate and human semantic review. No automatic or fictitious success.

Ledger prerequisites: ES03-06.
Preserved blockers: No authorised HF token/model/provider configured; no real hosted inference performed..

#### ES03-08 — Recover and reproduce reported human draft-repair implementation

Required: `false`. Bounded mode: `optional_hold_no_implementation`.

Recovered or rebuilt exact source preserves the original failure, human edits, source/base revision and separate pending-proposal review; reproduction, stale-state denial and native interaction pass. Assisted repair never satisfies the unassisted model gate.

Ledger prerequisites: ES03-01, B02-02.
Preserved blockers: The latest supplied repair handoff explicitly reports that no completed working tree was found. Only verified alpha.7 source was recovered in this review..

#### B04-01 — Professionally reviewed fixer and crisis playbooks

Required: `true`. Bounded mode: `engineering_only`.

Specialists approve versioned patterns, assumptions, authority and confirmation criteria; examples are not presented as proven solutions.

Ledger prerequisites: none recorded.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### B04-02 — Governed precedent retrieval

Required: `true`. Bounded mode: `engineering_only`.

Permissioned, source-linked precedent is case/matter scoped; access revocation and leakage tests pass. No automatic training.

Ledger prerequisites: B03-01, B03-02.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### B04-03 — Measured operator benefit from richer resolution intelligence

Required: `true`. Bounded mode: `engineering_only`.

Held-out/pilot evidence shows useful questions and plans without unsupported causal or success-probability claims.

Ledger prerequisites: B03-06, B04-01, B04-02.
Preserved blockers: none recorded; absence is not a production/semantic pass.

#### B04-04 — Permissioned correction replay and operator-value evaluation

Required: `false`. Bounded mode: `optional_hold_no_implementation`.

An approved evaluation protocol measures the cost and benefit of suggestions/repairs on representative cases. Corrections retain provenance, access and retention limits; no cross-client retrieval or model training occurs without separate permission.

Ledger prerequisites: B03-01, B02-11.
Preserved blockers: none recorded; absence is not a production/semantic pass.

## Completion boundary for this coordination checkpoint

The coordination change can pass only its document/ledger invariants and tracking tests. It cannot pass any assigned product requirement. New coordination discovery EM-253 is outside the reserved builder ranges. The session receipt records actual checks and the pushed handoff lookup; no builder branch or implementation is created here.
