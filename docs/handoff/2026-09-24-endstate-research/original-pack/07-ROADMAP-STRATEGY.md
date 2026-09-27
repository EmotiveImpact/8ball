# Recommended roadmap strategy after this research

## Decision

**Finish the current version first. Preserve the new direction now. Build it at the correct gates.**

## Phase A - now

### 8BALL V0.2

Continue Reviewed Situation Intelligence.

Primary acceptance focus:

- B02-09 reliable graph generation
- B02-10 source/entity/date quality
- B02-11 independent evaluation
- B02-12 full actual-provider journey
- B02-16 accessibility/native environment
- B02-18 V0.2 acceptance/release decision

Finish remaining implemented/partial tasks honestly.

### ENDSTATE V0.1

Finish ES01-05 reusable core acceptance.

The goal is to prove that:

- 8BALL still works through the extracted core
- neutral/sales/support fixtures use the same core
- result/schema compatibility is explicit
- package/internal distribution compatibility is real
- no public SDK claim is made prematurely

## Phase B - immediately after present gates

### ENDSTATE V0.2 - Event-Driven Replanning

Existing core tasks remain:

- normalised event/authority contract
- ordered/idempotent/replayable updates
- reviewed graph amendments
- freshness/cancellation/performance

This is also the natural place to formalise:

- premise dependency
- decision invalidation
- investigation frontier
- scenario branch identity
- event-triggered re-evaluation

Do not silently add those to the release gate. Promote them through an explicit decision/task update.

## Phase C - research in parallel

ENDSTATE Lab can run without blocking production.

First experiments:

1. Wayfinder-style decision frontier
2. premise invalidation
3. deterministic stress scenarios
4. model-proposed stress scenarios
5. prediction baselines
6. Sales/SDR calibration
7. multi-agent possible worlds later

## Phase D - ENDSTATE evaluated intelligence

Use research results to determine whether prediction/simulation deserves first-class contracts.

Provider-independent interfaces should make models replaceable.

A future interface might distinguish:

```text
observe(...)
plan(...)
compare(...)
simulate(...)
forecast(...)
explain_changes(...)
next_actions(...)
next_questions(...)
```

These names are targets, not claims that the public SDK currently exists.

## Phase E - Domain packs / second product

Sales is a strong candidate for the first serious proof after the core and replanning contracts stabilise.

The acceptance question is:

> Can a Sales domain pack use the same ENDSTATE kernel without forking planner semantics?

If not, fix the abstraction before declaring the engine reusable.

## Possible future milestone

Do not create this formally without a roadmap decision, but prediction may eventually justify a dedicated milestone such as:

**ENDSTATE Forecast - behavioural and operational forecasting**

It would require:

- calibrated metrics
- versioned feature/source sets
- shadow evaluation
- uncertainty
- baseline comparison
- observed-outcome feedback
- domain-specific governance

## Why this sequencing wins

It avoids two failure modes.

### Failure mode 1 - freeze

We finish a narrow fixer tool and later discover the engine cannot support prediction, simulation or new domains.

### Failure mode 2 - scope explosion

We stop a promising V0.2 build and try to build fixers, SDR, simulation, prediction, events, SDK, plugins and domain packs at once.

The chosen path is:

**finish the current core while preserving deliberate extension points and running aggressive research beside it.**
