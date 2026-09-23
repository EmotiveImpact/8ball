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
| **V0.2: reviewed situation intelligence** | B02-01 to B02-08 implemented developer workflow; B02-09 to B02-12 intelligence quality and real-model journey; B02-13 to B02-17 guided authoring, source handling and accessibility; B02-18 release gate | Full original V0.2 journey, credible model evaluation and usable operator review. Failed AI generation is a blocker, not a reason to relabel templates as AI. |
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

## Milestone completion rule

Every required subpart must be `verified` with its scope, source/test evidence and applicable code revision. Any failed, partial or blocked required item keeps the milestone unaccepted. A recorded failed model experiment can be a completed experiment while its model-quality gate remains blocked. Merge, packaging, deployment and customer release are always recorded independently. A documentation-only change cannot mark a runtime feature built.
