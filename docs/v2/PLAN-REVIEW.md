# Plan Review: live-plan checks, scenario comparisons and human judgement

Developer checkpoint `0.2.0-alpha.6`. This feature is embedded in Plan Studio and Ways through. It is not a new autonomous planning engine, an expert opinion or a production release gate.

## Operator workflow

Open **Plan Studio → Review live plan** or the matching button in **Ways through**. The requested outcome appears beside the graph's actual success conditions and confirmation rules. Read the structural findings: missing targets, recorded failure criteria, disputed conditions, completed work without confirmed effects, unknown waits, declared irreversible actions and outcome conditions without a producing action. An absent producer can mean direct evidence is needed; the checker does not invent an action.

The assessment uses the persisted live case, not uncommitted Plan Studio edits. Finish the existing preview/commit flow first to assess an amended plan. Opening an assessment makes no database changes.

In **Scenario checks**, explicitly select up to three independent hypotheses: remove an enabled, uncompleted action; set a different budget; or advance the calculation clock without adding evidence. Each starts from the same baseline. One scenario is not silently combined with the preceding scenario. Estimates include the planner's stated search/scheduling limits; an unknown wait remains unknown. This is a structural comparison, not a probability of achieving the outcome.

In **Human review**, answer six questions: outcome fidelity, source fidelity, missing dependencies, authority/restrictions, estimates/waits and alternatives/fallbacks. There are no preselected positive judgements. Each needs a reason. A “supported” judgement also needs an inspected case reference. “Not applicable” still requires an explanation. References record what the operator inspected, not a claim that that source establishes the answer.

Recording a review creates a separate history entry. It does not change the case revision, evidence, observations, graph, decisions, approvals or completion records. Structural findings stay visible even when a reviewer marks every rubric item supported. **Review recorded is not plan approved.** Action approvals remain separate.

## Staleness, concurrency and provenance

A saved review is bound to the full case snapshot hash, case revision, exact assessment hash, rubric version, scenarios and as-of clock. New recordings expire 15 minutes after calculation. This is an anti-stale-write window, not a claim that all information becomes false after 15 minutes. Recalculate before recording an old assessment.

Concurrent reviewers cannot overwrite each other: a case-scoped sequence and idempotency key protect writes. Duplicate identical requests return the original result. Reusing a key with different content, replaying a review into another case, changing its scenarios or using a stale snapshot fails. Old reviews are retained and labelled historical when the case changes; their reasons are not rewritten.

The separate linked-hash journal is included in full case export only after it contains records. Existing source-free exports preserve their previous shape. Export verifies the review links against the recorded case-state hashes. This is local application integrity, not independently anchored forensic custody or verified multi-user identity.

## ENDSTATE boundary

`endstate/plan_review.py` is a read-only, provider-free calculation layer. It accepts a detached `PlanningSnapshot` and an explicit clock. `eightball/v2/plan_review.py` adds the fixer outcome, rubric and local journal boundary. Neither can emit an observation command or grant execution authority.

A genuine defect was found during this sprint: routes using the same actions but different producer/dependency ordering could share an ID. The kernel now disambiguates only colliding IDs using the dependency path. Non-colliding legacy IDs and frozen wire/audit fixtures remain unchanged. The regression record preserves a constraint-compatible path and a failing path that previously collided. Their distinct identities now survive route comparison and change dictionaries.

## Evaluation scope

`python evals/plan_review_bench.py` runs eight frozen author-created structural examples without models and writes an **unfilled** human-review sheet. One example is deliberately structurally clean while targeting “offer sent” instead of “customer accepted”. It demonstrates why graph validity cannot establish semantic correctness. It is not evidence that a model or professional reviewer has passed that case.

Read `evals/PLAN-QUALITY-GATE.md` for the proposed independent-review protocol. B02-11 moves from not started to partial infrastructure; model selection, independent labelling and the complete actual-provider journey remain unfinished. The original four-case live-generation fixture file and failed Qwen evidence are unchanged.

## Verification commands

```sh
python -m pytest -q
python evals/plan_review_bench.py
python tests/browser_plan_review.py
```

Run all existing native browser suites as well. The supplied explicit ASGI bridge is a labelled fallback only when native navigation is unavailable. It does not establish native networking, browser storage, downloads, CSP enforcement or professional effectiveness. No model or paid service is called by Plan Review or the offline structural bench.
