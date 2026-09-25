# 8BALL + ENDSTATE master continuation handoff

**Date:** 24 September 2026

## Product identity

8BALL remains the fixer-facing flagship product. ENDSTATE is the reusable outcome-engineering engine beneath it. Future applications should use domain packs on top of the same ENDSTATE kernel rather than duplicate the planner.

## Current build, not a new rewrite

We are finishing:

- **8BALL V0.2 - Reviewed Situation Intelligence**
- **ENDSTATE V0.1 - Reusable Core**

At the last remote refresh, draft PR #2 remained open/unmerged on `feat/situation-intelligence-v2` at `824ca6421ff3100e1af596347f2d1247dde8f8dc`.

The latest preserved local checklist is newer than the remote. It records Governance 6/6, 8BALL V0.2 at 9/20 required subparts verified, and ENDSTATE V0.1 at 4/5. It also records later local integration work with 855 code tests, an installed internal ENDSTATE wheel rerun, and 344 explicitly bridged browser checks. Native browser, real-provider and independent expert/model-quality acceptance remain unfinished. These local results are not evidence that the source is already on GitHub.

## Recovery strategy

Before coding:

1. Refresh PR #2, remote branch, CI and current HEAD.
2. Locate the newest cumulative local source/patch artifact.
3. Do not stack older cumulative patches on a newer one.
4. Reconcile onto a fresh working branch without force-resetting or overwriting dirty work.
5. Run all relevant regression, generated-document and native browser gates.
6. Update the canonical ledger and changelog only after observed results.

## Current priority gates

- `B02-09` reliable reviewed graph proposals from genuinely new material
- `B02-10` robust source extraction, deadlines and reviewer-safe entity reconciliation
- `B02-11` independent held-out model evaluation / production-model selection
- `B02-12` full genuine actual-provider twenty-step V0.2 journey
- `B02-16` accessibility and supported-environment validation
- `B02-18` V0.2 acceptance/release decision, blocked until required gates pass
- `ES01-05` reusable-core acceptance

Do not move to V0.3 or call ENDSTATE a public SDK merely because local package tests pass.

## New accepted ENDSTATE direction

The research expanded the ceiling without replacing the current architecture.

Long-term ENDSTATE should move towards:

```text
understand world
→ define end state
→ model actions/causality
→ identify what must be learnt
→ predict what may happen
→ simulate possible futures
→ stress-test routes
→ approve/act
→ observe reality
→ replan
→ learn from outcomes
```

Prediction is explicitly part of the vision. The rule is not "do not predict people". The rule is: **predict where calibration/evidence justify prediction; simulate where assumptions dominate; never silently treat synthetic simulation as observed evidence or a calibrated real-world probability.**

Future architecture candidates include:

- investigation frontier vs execution frontier
- evidence/premise/decision/route dependencies
- decision invalidation when supporting premises change
- possible-world branching from explicit base revisions
- route stress testing
- behavioural and operational forecasting
- multi-actor simulation
- calibration from observed outcomes

These are not permission to rewrite V0.2 during its acceptance push. Promote them through explicit decisions/tasks at the appropriate version gates.

## Research lane - ENDSTATE Lab

Copy/fork useful external projects into a separate research lane where licences permit. For every upstream snapshot record URL, commit, licence, purpose, changes, security notes, experiment results and adoption/rejection decision.

Primary research references:

- Simulatrex organisation and engine
- Simulatrex possible-worlds
- Simulatrex llm-subpopulation-research
- Wayfinder / Wayfinder Maps
- Matt Pocock skills
- chartr

First experiments should be: investigation frontier, premise invalidation, deterministic stress scenarios, model-proposed stress scenarios, prediction baselines, Sales/SDR calibration, and only later multi-agent possible worlds.

External research code is not production adoption.

## Sales / SDR future product lane

A Sales/SDR product is a strong candidate for the first serious second-domain proof, but do not build it during the current V0.2 acceptance push.

Target dependency direction:

```text
Sales application
    ↓
Sales domain pack
    ↓
ENDSTATE

8BALL
    ↓
Fixer domain pack
    ↓
ENDSTATE
```

The Sales lane can eventually support human SDR copiloting, AI-assisted SDR, tightly authorised AI outreach, account navigation, pipeline rescue and conversation intelligence. It is attractive for prediction research because replies, meetings, objections, timing and won/lost outcomes are measurable.

If Sales requires forking the planner, that reveals an ENDSTATE abstraction problem.

## Non-negotiable semantics

- unknown is not false
- disputed is not resolved
- model output is a proposal
- completing an action does not prove its intended effect
- source existence is not proof of a claim
- simulations remain isolated from live state
- synthetic outcomes do not become evidence automatically
- human/domain authority remains explicit
- stale approvals must not survive incompatible revisions
- no silent cross-client learning
- no confidential client data or secrets in the public repository
- no automatic external execution is authorised by the current milestone

## Roadmap recommendation

1. Finish 8BALL V0.2 and ENDSTATE V0.1.
2. Preserve ENDSTATE Lab research in parallel.
3. Use ENDSTATE V0.2 event-driven replanning as the natural place to formalise premise invalidation, investigation frontiers and scenario identity after explicit roadmap promotion.
4. Use evaluated-intelligence work to determine which prediction/simulation interfaces deserve first-class engine contracts.
5. Use Sales as the first serious second-domain proof only after the core/replanning abstractions are stable.

## End every builder session with durable continuity

Record exact branch/base/commit, files, tests, provider/model runs, failed/unverified work, task status changes, unpushed artifacts, next command, merge/deployment state and emergence review. Do not leave critical decisions only in chat.
