# ENDSTATE Lab - research lane

## Purpose

ENDSTATE Lab lets us research aggressively without polluting production.

Production code should not absorb experimental repositories simply because they are exciting.

The Lab should answer:

- does the idea work?
- does it outperform a simpler baseline?
- what failure modes appear?
- what would be safe to promote into ENDSTATE?
- what evidence is needed before a capability can be claimed?

## Recommended structure

```text
endstate-lab/
├── external/
│   ├── simulatrex-engine/
│   ├── possible-worlds/
│   ├── llm-subpopulation-research/
│   ├── wayfinder-maps/
│   ├── mattpocock-skills/
│   └── chartr/
├── experiments/
│   ├── decision-frontier/
│   ├── premise-invalidation/
│   ├── behavioural-simulation/
│   ├── possible-worlds/
│   ├── route-stress-testing/
│   ├── prediction-calibration/
│   └── sales-sdr/
├── benchmarks/
├── findings/
├── licences/
├── source-snapshots/
└── prototypes/
```

This can initially live as a research directory or separate branch. A separate repository can be created later when ownership/size/history justify it.

## External repository rule

For every copied/forked external project record:

- upstream URL
- exact commit SHA/tag
- date captured
- licence
- whether we may copy, modify and redistribute
- dependency licences
- what we are evaluating
- files changed by us
- experiment results
- security notes
- adoption decision
- rejected ideas

Public GitHub does not mean unrestricted commercial reuse.

## Research stages

### Stage 0 - reproduce

Can the upstream project actually run?

Record environment, dependency versions, model/provider, exact inputs, output, cost, latency and failures.

### Stage 1 - baseline

Compare the exciting method with a simpler method.

For behavioural prediction examples:

- historical frequency
- logistic / tree baseline
- retrieval + rules
- expert judgement
- LLM persona
- multi-agent simulation

If the complicated system does not beat a sensible baseline, do not promote it.

### Stage 2 - failure discovery

Use the model as a red-team assistant.

Ask it to find:

- missing actors
- missing dependencies
- hidden assumptions
- alternative explanations
- route fragility
- second-order consequences

This may be valuable before reliable numerical prediction is possible.

### Stage 3 - held-out evaluation

Freeze protocol, evaluation set, metrics and thresholds, then test.

Do not change the gate after seeing failures without recording the decision.

### Stage 4 - shadow mode

Run the predictor/simulator beside real work without allowing it to control decisions.

Record predicted result, actual result, calibration, correction and missed outcomes.

### Stage 5 - bounded product integration

Only now create an ENDSTATE contract/provider and tests.

## Proposed first experiments

### Experiment A - Investigation Frontier

Given a state and goal, identify which unresolved question has the highest expected impact on route selection.

Compare against current question-impact logic, simple graph centrality, LLM ranking and human ranking.

### Experiment B - Premise Invalidation

Build explicit:

`evidence → premise → decision → route`

Then retract/update evidence and verify that only dependent reasoning becomes stale.

This should be deterministic before LLMs are involved.

### Experiment C - Deterministic stress scenarios

Hand-author adverse scenarios first.

Measure whether the engine identifies broken routes, discovers fallback actions, preserves live state and explains failures.

### Experiment D - Model-proposed stress scenarios

Let models suggest additional failure cases.

The model proposes. Deterministic ENDSTATE validates the scenario structure and keeps it isolated.

Measure whether the model discovers valuable cases beyond the hand-authored baseline.

### Experiment E - Sales behavioural forecast

Use fictional/synthetic data first, then real authorised sales data later.

Predict reply/no reply, meeting/no meeting, objection category, next-step delay and route stall reason.

Compare LLM simulation to simple statistical baselines and real outcomes.

### Experiment F - Multi-agent possible worlds

Only after single-outcome calibration.

Test whether multiple actor simulations expose useful contingencies, not whether the generated dialogue feels convincing.

## Promotion rule

Research becomes product scope only after:

1. documented experiment
2. measured benefit
3. safety/authority review
4. licence review
5. architecture decision
6. task/roadmap update
7. regression tests
8. explicit acceptance criteria

Until then it remains Lab work.

## Relationship to current V0.2

ENDSTATE Lab may begin in parallel as a research activity.

It must not block:

- B02-09
- B02-10
- B02-11
- B02-12
- B02-16
- B02-18
- ES01-05

The current product build remains priority.
