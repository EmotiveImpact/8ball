# 8BALL and ENDSTATE version roadmap

Planning revision: 23 September 2026. This is the delivery map for [the master PRD](PRD.md). Exact task states and evidence live in [PROGRESS.md](delivery/PROGRESS.md), generated from [progress.json](delivery/progress.json).

**8BALL stays the fixer product. ENDSTATE is the engine it creates and uses.** Versions describe maturity of those two deliverables; outcome engineering is the underlying concept from the start. These labels are not existing Git tags or claims of released software. No dates or completion percentages are inferred from task counts.

## Delivery order

Preserve the tested fixer workflow and its unresolved acceptance gates. Establish ENDSTATE naming/contracts now. Extract its shared core incrementally while continuing V0.2 intelligence and operator work; do not block the fixer product on a speculative public SDK. Validate a limited secure agency pilot before real client use. Prove adjacent-domain reuse with small fixtures, then expand only after an explicit commercial decision.

Two workstreams can proceed in parallel when they touch different files: kernel extraction/compatibility and model-quality improvements. Both rebase on the actual current source and preserve V0.2 semantics. Never run two unsynchronised agents against the same code or progress record.

## 8BALL track

| Milestone | Subparts | Exit gate |
| --- | --- | --- |
| **V0.1: local outcome-planning foundation** | B01-01 state/planner; B01-02 operator UI and persistence; B01-03 reproducible verification | Original local scope demonstrated; approvals and evidence separation intact. Merge/deployment remain separate decisions. |
| **V0.2: reviewed situation intelligence** | B02-01 to B02-08 implemented developer workflow; B02-09 to B02-12 intelligence quality and real-model journey; B02-13 to B02-17 guided authoring, source handling and accessibility; B02-18 release gate; B02-19 black operator visual system | Full original V0.2 journey, credible model evaluation and usable operator review. Failed AI generation is a blocker, not a reason to relabel templates as AI. |
| **V0.3: secure agency pilot** | B03-01 identity/matter access; B03-02 evidence vault; B03-03 experts/client projection; B03-04 intake/connectors; B03-05 audit/recovery/operations; B03-06 pilot validation | The full confidentiality/permission/revocation/recovery gate and a limited authorised fixer pilot. Design documents alone do not complete this milestone. |
| **V0.4: reviewed resolution intelligence** | B04-01 specialist playbooks; B04-02 governed precedent retrieval; B04-03 measured route/question improvements | Permissioned, evidence-linked precedent with no cross-client leakage and demonstrable operator benefit. No automatic training on confidential cases. |
| **V1: supported fixer product** | B10-01 commercial onboarding and operations; B10-02 release acceptance | Production support, model/service policies, security, recovery, accessibility and customer acceptance evidenced. This is the first full fixer product, not a generic dashboard for every lane. |

## ENDSTATE track

| Milestone | Subparts | Exit gate |
| --- | --- | --- |
| **V0.1: reusable core** | ES01-01 contracts/dependency boundary; ES01-02 extract state/planner; ES01-03 persistence/import compatibility; ES01-04 shared-kernel fixtures; ES01-05 package gate | 8BALL runs unchanged through the separated core; neutral, sales and support test inputs use the same calculation code. No launched sales/support product is implied. |
| **V0.2: event-driven replanning** | ES02-01 normalised events/authority; ES02-02 durable replay/order/idempotency; ES02-03 reviewable graph amendments; ES02-04 freshness and incremental recomputation | Duplicate/reordered events are safe, stale work cannot commit, and declared response-time measurements include model/review/connector delays. Current command-triggered recomputation is not silently described as a live inbox service. |
| **V0.3: evaluated intelligence compilation** | ES03-01 provider-independent compiler; ES03-02 real-model and semantic gate; ES03-03 bounded judgement providers; ES03-04 model installation/status; ES03-05 refusal/fallback/audit | Source-to-model proposals and graph validation meet agreed tests without changing authority boundaries. Reuse B02 evidence rather than inventing a second pass. Optional Jev requires a real authorised key and its own live evaluation. |
| **V0.4: domain packs and integration interfaces** | ES04-01 pack contract; ES04-02 8BALL pack; ES04-03 adjacent-domain proof; ES04-04 SDK/API/MCP decision and contracts | A second domain uses the same engine, not a fork. Policies, action mappings and confirmation rules stay domain-specific. API/SDK/MCP are options to justify and scope, not automatic simultaneous releases. |
| **V1: supported reusable engine** | ES10-01 compatibility/performance/support; ES10-02 release gate | Stable public contracts and migration policy, appropriate licences, operational evidence and commercial support. Can still be embedded inside 8BALL; cloud infrastructure is not mandatory solely because it is called a platform. |

## Dependencies without product drift

8BALL V0.2 can remain a developer application while ENDSTATE V0.1 is extracted. It does not become production-ready just because extraction passes. ENDSTATE V0.3's core semantic gate reuses B02-09 through B02-12; do not duplicate status claims. 8BALL V0.3 connector work depends on the event/authority contract from ENDSTATE V0.2. 8BALL V0.4 learning/retrieval needs its own permission and evaluation gate. A standalone ENDSTATE V1 release is not a prerequisite for selling an accepted 8BALL V1 product.

## Future lanes, deliberately not parallel product commitments

Sales teams, customer service/success, social-media/client managers, crisis managers and public-office staff are reuse candidates. Start with a sales and a support **fixture pack**, not new production apps. Political/public-office scope here is casework, service/policy delivery and operational coordination, not personal-data-based voter persuasion. Each commercial expansion needs its own market decision, policy review, action authority and domain evaluation.


## End-of-sprint emergence rule

Every substantive build sprint closes with the mandatory review in `docs/delivery/EMERGENCE-REVIEW.md`: **what did the build reveal that we had not properly seen before?** Findings are evidence-labelled and classified as an existing task, candidate, required task, decision record or no action. Discovery can change the roadmap, but only through an explicit canonical-ledger / decision update; it never silently changes a version gate.

## Milestone completion rule

Every required subpart must be `verified` with its scope, source/test evidence and applicable code revision. Any failed, partial or blocked required item keeps the milestone unaccepted. A recorded failed model experiment can be a completed experiment while its model-quality gate remains blocked. Merge, packaging, deployment and customer release are always recorded independently. A documentation-only change cannot mark a runtime feature built.


## Accepted development addition

The owner requested a black visual identity and optional Hugging Face development support (key to follow). B02-19 tracks the visual acceptance separately. ES03-06 tracks the transport/permission contract without claiming live inference; ES03-07 tracks the actual hosted comparison once authorised credentials are configured. These optional hosted tasks do not replace B02-09 through B02-12 or reduce the original model-quality gate.


## Current authoring and lifecycle checkpoint

`0.2.0-alpha.2` is an unreleased developer checkpoint **inside V0.2**. It adds the guided Plan Studio (B02-13), local analysis job lifecycle (B02-15) and mandatory shared changelog (DOC-04). Connections remains the read-only exploration surface; Plan Studio is the deliberate authoring surface. These additions do not replace or weaken the original real-model, source-handling, accessibility or V0.2 acceptance requirements.

Every future change adds an immutable-history entry in `docs/delivery/changelog.json`, regenerates `CHANGELOG.md`, and updates the affected task in the sole progress ledger. A changelog entry records a build; only a verified exit gate changes milestone acceptance. After V0.2 acceptance comes V0.3's secure agency pilot, not a parallel sales product.

## Emergence increment inside V0.2, not a new product lane

- **DOC-06:** Preserve all identified build discoveries with owner-review decisions, prompt coverage and generated evolving register.
- **ES02-05:** A bounded, deterministic emergence calculation contract. It does not imply event-driven ingestion or a general causal model.
- **B02-21:** Black case-level Emergent Insights workspace, append-only review history, manual hypotheses and explicit verification-question promotion.
- **B02-22:** Native workflow and operator-usefulness acceptance, including false positives, missed findings and duplicate noise.

The case insight workflow is an additive development increment. Existing version gates, source/model failures and agency-security work are retained. Do not tick the broad feature off solely because individual detectors pass. Use `docs/delivery/EMERGENCE-REGISTER.md` to see all candidates and `docs/delivery/progress.json` for actual task state. Declined/deferred product ideas remain reviewable and can be reopened by the owner; no discovery vanishes because a developer judged it lower priority.


## Source clarity checkpoint within V0.2

B02-10/B02-14 now include implemented human source-mention/identity/deadline review. Their overall status remains partial pending native integration and independent multi-source evaluation. The reusable time helper is not a new product lane or SDK release. EM-038 to EM-043 are retained in the owner register; business-calendar handling is deferred rather than silently added to the mandatory scope. The next release remains gated by the existing V0.2 criteria, not the alpha.5 version label.

## Current bounded increment: Plan Review

The alpha.6 checkpoint advances existing B02-03/B02-11/B02-13, not a new product lane or release milestone. B02-11 remains partial until independent semantic evaluation is actually performed. B02-09/B02-12 retain their source-to-plan blockers, and native acceptance remains outstanding. Route structural identities, assessment checks and human review are now separately testable. The canonical status ledger remains `docs/delivery/progress.json`; all discoveries EM-044 through EM-049 remain owner-reviewable, including the deferred review-burden hypothesis.


## Integrated verification checkpoint, alpha.7

The existing ES01-05/B02-12/B02-16 work now includes explicit nested result schemas, an internal wheel installation test, one source-bound acceptance runner, improved keyboard/dialog focus and a separately authorised actual-provider integration command. See `docs/v2/ACCEPTANCE-RUNNER.md` and the canonical ledger for actual status. Native policy restrictions and missing model prerequisites remain blockers, not reasons to substitute mock results. Scripted inference integration is not independent semantic evaluation or the complete native-user workflow. All prior scope and failed model evidence remain preserved. EM-050 through EM-055 record this sprint's discoveries without creating additional product lanes.

## Vision 1.3 refinement: optional scope, unchanged required gates

See `vision/8BALL.md`, `vision/ENDSTATE.md` and ADR 0004. This documentation review adds no runtime release, changes no existing required flag/status and supplies no new model, native-browser or operator-quality pass.

| Task | Intended home | Disposition in this review |
| --- | --- | --- |
| B03-07 | 8BALL client mandate and chosen course | Optional, not started. Design inside the existing situation room; no authority from selection alone. |
| ES02-06 | ENDSTATE course/reconsideration contract | Optional, not started. Explain material changes without auto-switching plans or retaining stale approvals. |
| ES03-08 | Model-failure recovery | Optional, blocked on recovering or explicitly rebuilding the reported Draft Repair source, then reproducing actual evidence. |
| B04-04 | Permissioned correction replay and operator value | Optional, deferred pending an approved protocol and data/access safeguards. |

Outcome fallback and watch-condition ideas are promoted in design priority, not retroactively ticked off. Do not add them to required release totals without an explicit owner scope decision. The canonical task ledger remains `delivery/progress.json`.

Immediate sequence: recover/verify the exact cumulative source, publish through the authorised workflow, run native acceptance, then the unchanged actual-provider and independent operator gates. Do not add more runtime features on an unrecovered purported base. The alpha.7 source is recoverable; the later Draft Repair handoff is a reported-only record until its implementation is found or rebuilt.

## Chosen Course local checkpoint, 25 September 2026

Optional B03-07 and ES02-06 are partial: local chosen-course records and on-request reconsideration are implemented. Their original dependencies on secure identity and event contracts remain outstanding. No required gate is removed, accepted or expanded by this checkpoint. See `v2/CHOSEN-COURSE.md` and the generated delivery ledger. First integrate the cumulative source, then run native acceptance and qualified operator review.
