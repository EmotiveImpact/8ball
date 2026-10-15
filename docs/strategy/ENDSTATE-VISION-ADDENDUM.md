# Master PRD addendum: ENDSTATE's long-term outcome-intelligence vision

Revision 1.4 addendum, 15 October 2026. Read with [the preserved master PRD](../PRD.md), [current delivery ledger](../delivery/PROGRESS.md) and [ADR 0005](../decisions/0005-research-consolidation.md). This adds future direction without replacing the original PRD, changing current acceptance thresholds or asserting implementation.

## Product promise

8BALL helps a fixer understand a changing situation, agree what resolution means, select a defensible course, coordinate authorised work and recognise when that course needs reconsideration. ENDSTATE supplies reusable evidence-linked outcome reasoning to 8BALL and, later, other separately designed applications.

The long-term loop is:

```text
Understand the situation and evidence
  -> define the human-authorised end state and boundaries
  -> model available actions and dependencies
  -> identify what must be learnt or decided
  -> forecast where evidence supports forecasting
  -> simulate explicit possible futures
  -> stress-test and compare conditional routes
  -> choose a course; approve eligible actions separately
  -> act within authority; observe actual results separately
  -> update, reconsider, replan and learn from authorised outcomes
```

Only parts of this loop are implemented today. [The architecture map](../architecture/ENDSTATE-SYSTEM.md) labels the boundary.

## 1. World model and decision intelligence

Maintain distinctions among original sources, attributed claims, reviewed observations, disputed/unknown conditions, human decisions, resources and operational commitments. Retain event time, capture time, source lineage and base revision where applicable. A duplicate assertion is not independent corroboration; source availability is not analysis coverage.

Future decision intelligence should make evidence -> premise -> decision -> route -> action dependencies inspectable. A changed premise can trigger review without rewriting the past or silently authorising another action. Existing conservative approval invalidation remains until a separately evaluated narrower policy is approved.

Separate an **investigation frontier** (useful, permitted questions/investigations that can be undertaken) from an **execution frontier** (actions satisfying current conditions, resources, time and authority). An answered question does not itself attest a fact. Structural question impact exists today; calibrated value-of-information optimisation does not.

## 2. End states, mandates and chosen courses

Retain the exact requested outcome, explicit success evidence, restrictions, failure/walk-away boundaries and any separately authorised acceptable fallback. A full client mandate, concession authority and sustained-confirmation interval are future refinements; do not imply they are finished because current objectives and Chosen Course exist.

A selected course is an attributed human intention, not simply the route currently ranked first. Preserve the reason, original snapshot, assumptions, alternatives and review triggers. Ranking changes must not silently switch courses. Review acknowledgement is not warning resolution. Pausing a record does not cancel external activity.

When no route is found, report the catalogue, assumptions, evidence gaps and search bounds. Do not claim universal impossibility or manufacture success.

## 3. Prediction is explicitly within ENDSTATE's ambition

Prediction is not excluded by design. Develop it in evidence-gated layers:

| Layer | Intended capability | Evidence needed before a product claim |
| --- | --- | --- |
| Conditional calculation | Eligibility and schedule consequences under declared inputs | Deterministic compatibility and constraint tests; already present in bounded form. |
| Operational forecasting | Response delays, approval timing, resource or supplier failure | Relevant authorised outcome data; simpler baselines; held-out temporal tests; calibration and drift review. |
| Behavioural forecasting | Reply, refusal, objection, escalation or next-step distributions | Defined population/task, lawful data scope, independent labels, uncertainty, subgroup/error review and abstention. |
| Multi-actor forecasting | Chains of reactions among organisations and people | Demonstrated improvement over single-outcome baselines; propagation of uncertainty; validation of interactions. |

Separate event likelihood from the causal effect of an intervention. Observational association does not prove that sending a particular message will cause a desired response. A model-generated persona is not a verified description of a real person's motives or characteristics.

Every proposed forecast record should declare the predicted event and horizon, as-of revision, feature/source set, predictor/model revision, probability or interval when justified, calibration population/method, limitations and later observed result. These are proposed contract requirements, not current exported API fields.

No universal model winner is selected here. Qwen, Hugging Face and JEV are provider options, not ENDSTATE itself. The current real-model planning gate remains unchanged.

## 4. Possible worlds and route stress testing

Branch scenarios from an immutable, case-scoped base revision. Preserve explicit assumptions, perturbations, model/provider identity, budgets, returned outputs and deterministic validation results. Start with hand-authored alternatives before asking models to propose additional failure cases.

Stress families can include refusal, delayed approval, withdrawn authority, wrong/stale evidence, unavailable resources, changed deadlines, competing commitments and second-order consequences. Compare candidate routes using their failure causes, unresolved prerequisites, fallback coverage and reversal costs.

**Eight favourable synthetic responses out of ten are a simulation count, not an 80% real-world success probability.** Scenario survival depends on the selected scenario family; expose that selection and sensitivity. A seed, where available, does not guarantee reproduction of a hosted model's outputs. Retain actual outputs for replay.

Existing What If scenarios and deterministic Plan Review challenges are limited precursors, not a calibrated possible-world simulator. No synthetic event may become live evidence, grant authority or satisfy outcome verification automatically.

## 5. Learning and calibration

Compare predictions and plans with later authorised observations. Separate development, training and held-out cases; use historical information cut-offs to prevent future evidence leaking backwards. Evaluate corrections, omitted dependencies, false certainty, refusal/abstention, latency, cost and useful decisions, not fluent prose or the number of panels built.

Governed retrieval, prompt/compiler changes, statistical calibration and fine-tuning are different learning mechanisms. Each needs its own permission, test and rollback decision. No cross-client retrieval or training is implied. Human-repaired outputs must remain labelled as repaired, never counted as unassisted model successes.

## 6. Reusable domain packs and applications

Target dependency direction:

```text
8BALL app -> Fixer domain pack -> ENDSTATE contracts/kernel
Sales/SDR app -> Sales domain pack -> ENDSTATE contracts/kernel
Customer Ops app -> Support domain pack -> ENDSTATE contracts/kernel
```

Applications own product UX, identity/tenancy and authorised integrations. Packs own vocabulary, action catalogues, policies, confirmation rules, prompts, domain predictors and evaluation fixtures. The kernel owns generic calculation and contract enforcement. A Sales application must not import `eightball` application services or fork the planner.

Sales/SDR is the preferred candidate for a serious second-domain proof, not an already-approved parallel launch. Preserve human SDR copilot, AI-assisted research/drafting, account navigation, pipeline rescue and conversation-intelligence ideas. Autonomous outreach is a later explicitly authorised mode with recipient/channel/content/scope/expiry controls, revocation and its own safety/security evaluation.

Customer service/success, client/social-media management, crisis teams and private offices remain candidates. Public-office applications refer to casework and operational delivery, not personal-data-based voter persuasion. Every commercial lane needs separate discovery, permissions, evaluation and an owner decision.

## 7. Visual and operating principles

Maintain the black/graphite professional workspace, legible typography, restrained state colours and purposeful graph exploration. Centre the operator on the desired result, selected course, immediate work, important questions and reconsideration reasons. Connections explores; Plan Studio edits; facts and approvals use explicit controls. Avoid a new top-level screen for each research idea.

## 8. Delivery discipline

Finish 8BALL V0.2 and retain verified ENDSTATE V0.1 internal compatibility. Then evaluate the future work through [the milestone map](ROADMAP-INTEGRATION.md) and [Lab experiments](../research/ENDSTATE-EXPERIMENTS.md). Adoption requires source/licence review, measured benefit, authority/security review, an architecture decision and explicit acceptance criteria. Preserve unsuccessful experiments and every deferred idea.
