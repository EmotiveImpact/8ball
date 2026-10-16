# Current closeout and future milestone mapping

15 October 2026. Supplemental planning map, not a new completion tracker. [The existing roadmap](../ROADMAP.md) and `docs/delivery/progress.json` retain all task IDs, required flags, dependencies, statuses and acceptance criteria.

## Work order

| Stage | Existing milestone | Plan and boundary |
| --- | --- | --- |
| Now | 8BALL B02 / ENDSTATE ES01 | Finish the ten open required B02 scopes. ES01 is already 5/5 for internal compatibility; preserve it, do not restart extraction. |
| Next accepted product increment | 8BALL B03 | Secure agency pilot: identity/matter access, protected evidence, client/specialist collaboration, authorised integrations, recovery and pilot review. |
| Replanning foundation | ENDSTATE ES02 | Event identity/order/replay, revision-scoped interpretation and amendments, freshness and bounded recomputation. Extend current primitives rather than introduce another truth store. |
| Evaluated intelligence | ENDSTATE ES03 | Provider-independent compilation, held-out semantic quality, guarded failure/recovery, operational/behavioural prediction experiments and calibration candidates. Reuse B02 evidence, do not double-count it. |
| Reuse proof | ENDSTATE ES04 | Versioned domain-pack contract, fixer pack, adjacent-domain fixtures, then a bounded Sales proof after explicit approval. Decide SDK/API/MCP needs rather than shipping all three. |
| Professional usefulness | 8BALL B04 | Reviewed playbooks, permissioned precedents, measured question/route usefulness; consume only evaluated engine capabilities. |
| Supported products | B10 / ES10 | Separate commercial release gates, compatibility, support, security and operational evidence. A public ENDSTATE service is not automatically required to ship 8BALL. |

Calendar dates are not assigned by this map. A version is not finished because its code was pushed or its branch name changed.

## Candidate placement without new required tasks

The following `F-*` identifiers are planning references only. None is a canonical task, deadline or implementation claim. R01-R07 and A-F refer to the preserved research handoff.

| Candidate | Existing milestone home | Prerequisite and first bounded test |
| --- | --- | --- |
| F-01 premise/decision dependency and invalidation (R01; B) | ES02, related optional ES02-06 | Recorded evidence/revisions and current Chosen Course semantics; retract a premise and compare affected decisions. Retain conservative approvals. |
| F-02 investigation versus execution frontier (R02; A) | ES02 then ES03 evaluation | Existing question impact and action eligibility; compare independent operator rankings without authorising blocked work. |
| F-03 explicit competing assumptions and scenario identity (R03) | ES02 | Existing isolated scenarios; replay from a fixed snapshot with unchanged live evidence. |
| F-04 deterministic stress testing and robustness explanation (R04/R05; C) | ES02/ES03 | Hand-authored scenario families; compare with current Plan Review, disclose coverage and reversal costs. |
| F-05 model-proposed stress scenarios (R04/R05; D) | ES03 | F-03/F-04 baseline plus bounded model adapter; measure useful new failure discovery, not narrative plausibility. |
| F-06 operational prediction | ES03 | Authorised outcome data and temporal holdout; compare timing/risk models with simple statistical baselines. |
| F-07 behavioural prediction and Sales calibration (E) | ES03/ES04 | Defined prediction target/population, lawful data, independent labels and calibration; no outreach execution. |
| F-08 multi-actor possible worlds (F) | ES03 research, ES04 domain evaluation, beyond V1 if needed | Single-outcome validation first; demonstrate value over simpler methods and uncertainty propagation. |
| F-09 expertise-to-domain packs (R06) | ES04 and B04 | Versioned vocabulary/actions/policies/proof rules; run neutral/fixer/sales/support fixtures without planner duplication. |
| F-10 research memory and selective engineering skills (R07) | Delivery practice, no runtime dependency | Link findings to decisions and sources; keep one authoritative tracker. |
| F-11 mandate/outcome envelope and commitments | B03-07 / ES02-06 candidates | Use existing Chosen Course and objective concepts; no silent objective relaxation or concession authority. |
| F-12 calibrated information value, attention burden and outcome learning | B04 / ES03, related B04-04 / ES03-08 candidates | Measure operator burden and usefulness with authorised data; no automatic training or unsupported numeric scores. |

The existing B03-07, ES02-06, ES03-08 and B04-04 scopes remain optional/unaccepted as recorded. The bounded Chosen Course implementation does not complete their wider requirements.

## Promotion procedure

Start in a research worktree with fictional or explicitly authorised data. Pin sources and licences. Define a baseline, hypothesis, inputs, metrics and thresholds before evaluation. Preserve failed findings. Only an approved decision may introduce a real task ID or change required scope in `progress.json`. Regenerate the checklist and cross-link the experiment, decision and tests.

Documentation consolidation is authorised now. A new Sales product, imported simulation runtime, external skill installation, revised approval policy, background connector or model training is not authorised by these pages.

## Closing this stretch

Use [V02-CLOSEOUT.md](../delivery/V02-CLOSEOUT.md), not the future table, for today's work. Keep PR #2 draft until its required gates pass and the final integration decision is explicitly recorded. Then the agreed route is one cumulative merge, superseded PR #1 cleanup and an accepted version tag. No merge, closure, tag or deployment is performed by this documentation branch.

## Concrete component plan, 16 October 2026

The [evolution plan](ENDSTATE-EVOLUTION-PLAN-2026-10-16.md) now maps this same sequence to current GitHub candidates, prototype gates and costs. It retains F-01..12, Lab A–F and all canonical task requirements. Research source pins and limitations are in [the component register](../research/GITHUB-COMPONENTS-2026-10-16.md). This supplements the historical map; current source is already consolidated on main, while V0.2 acceptance remains open.
