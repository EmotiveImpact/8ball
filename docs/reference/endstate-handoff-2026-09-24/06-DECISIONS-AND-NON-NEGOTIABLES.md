# Accepted direction and non-negotiables

This file records the product direction accepted in the 24 September 2026 continuation conversation. It is a handoff decision record, not a claim that all items are implemented.

## Product family

1. **8BALL remains the flagship fixer product.**
2. **ENDSTATE remains the reusable engine/platform underneath it.**
3. Future applications can use ENDSTATE through domain packs without becoming part of the 8BALL UI.
4. A Sales/SDR application is a strong candidate for the first serious second-domain proof.
5. Customer-facing products may have separate names and UX while sharing ENDSTATE.

## Prediction

Prediction is explicitly part of the long-term ENDSTATE ambition.

The rule is not "do not predict people".

The rule is:

> Predict where evidence and calibration justify prediction. Simulate where assumptions dominate. Never silently convert synthetic simulation into observed truth or a calibrated real-world probability.

ENDSTATE should eventually be able to model:

- operational forecasts
- human response distributions
- organisational behaviour
- multi-actor reactions
- possible futures
- route robustness

## Simulation

Simulation must be isolated from live state.

A simulated event cannot:

- become evidence automatically
- complete a real action
- grant authority
- prove an intended effect
- silently modify the live graph

Promotion from simulation to live state requires actual evidence/review through the normal contract.

## Wayfinding

Future architecture should support:

- investigation frontier
- execution frontier
- explicit premise/decision dependencies
- invalidation of reasoning when supporting premises change
- route recomputation with explanation

These are architectural directions to integrate deliberately, not excuses to rewrite the planner during V0.2 acceptance.

## ENDSTATE Lab

External projects should be copied/forked into a separate research lane where licences permit.

Research is not production adoption.

Every external snapshot must preserve upstream identity, commit, licence, purpose, changes, evaluation and adoption/rejection decision.

## Development strategy

Do not interrupt the present build.

Finish:

- 8BALL V0.2 acceptance
- ENDSTATE V0.1 reusable-core acceptance

Then progress into:

- ENDSTATE V0.2 event-driven replanning
- the agreed research experiments
- prediction/scenario contracts at the correct gate

## Safety and evidence invariants

- unknown is not false
- disputed is not resolved
- model output is a proposal
- completing an action does not prove its intended effect
- source existence is not proof of a claim
- synthetic simulation is not live evidence
- human/domain authority remains explicit
- stale approvals must not survive incompatible revisions
- no silent cross-client learning
- no real confidential data in the public repository
- no autonomous external execution merely because a model recommends it

## Architecture rule

Keep generic ENDSTATE concepts generic:

- entity
- actor
- evidence
- condition
- objective
- action
- constraint
- authority
- resource
- event
- decision
- scenario
- route
- verification

Keep product-specific language in domain/application layers:

- client
- fixer
- specialist
- case
- lead
- prospect
- buyer
- deal
- CRM

## Repository strategy

Keep the current combined repository while extraction is still stabilising.

Do not create multiple codebases for ENDSTATE, 8BALL and Sales yet.

Split repositories only when packaging, independent release, ownership or operational requirements justify it.

## Release truth

A developer alpha can be useful without being accepted.

Do not collapse implemented, verified, integrated, merged, packaged, deployed and commercially released into one status.
