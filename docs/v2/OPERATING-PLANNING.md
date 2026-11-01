# Full operating-plan method (internal v1)

This opt-in method extends ENDSTATE's reusable engine; 8BALL remains the fixer
workspace. It does not replace `endstate.coordinated-planning.v1`, its native
decision specialists or historical reports. No existing result is migrated.

## Contract and method

`endstate.operating.OutcomeBrief` is caller-authored: the exact outcome, explicit
success requirements/constraints, timezone-aware deadline, known budget/currency
or explicit unknowns. `OperatingPlan` must retain the exact outcome and canonical
brief hash. Every original requirement needs a link to proposed work. These are
structural checks, **not proof that the plan meaningfully satisfies the goal**.

`OperatingPlanningSpec` declares one to three review roles, a 1–600 second host
allowance and `planning_cost_policy='explicit_unpriced_token_bound'`. The method
`coordinate_operating(spec, text, namespace, generate, review, checkpoint)` uses:

1. One complete-plan proposal, not a narrower substitute for the human outcome.
2. Separate review contexts, each seeing only the brief, original source and
   original proposal—not other reviewers' answers.
3. One separate revision seeing every retained challenge. Each concern needs one
   changed/retained/unresolved disposition and written reason. Every changed
   top-level plan field needs a reason corresponding to an actual change.

The `generate` callback receives a JSON schema, instructions and detached context;
it returns `(raw_object, served_model)`. The compatibility `review` argument is
unused: this method never asks native choice models for explanations they cannot
supply. All roles currently use the **same explicitly configured generative
model**, independently contextualised. They are not independent human experts,
different model families, a native specialist panel, votes or simulated customers.
The report is `endstate.operating-planning.v1`, with a baseline, all returned
outputs, validation failures, written reviews, a revision and a structural diff.
No private internal chain-of-thought is requested or stored.

## Plans, arithmetic and SOPs

Each strategy declares its beneficiary, offer/deliverable, delivery/distribution
and rationale. Each proposed step has an owner, ordered prerequisite IDs,
instructions, deliverable, time/cost assumptions, due date, separate completion
and outcome evidence, reconsideration conditions and required human permission.
The schema is neutral: it is not a hardcoded business-plan template.

Variables are assumptions or explicit unknowns, never newly attested facts.
Arithmetic supports add/subtract/multiply/divide/ceil with 50-digit Decimal
precision and ROUND_HALF_EVEN independent of the caller's Decimal context.
Units use bounded `{name, power}` lists, not free-form object keys that a strict
provider schema would close. Duplicate dimensions, incompatible units, invalid
arity, zero division, forward/cyclic references and out-of-range results fail.
Every nonzero computed magnitude is bounded to 1e-30–1e30 before rendering;
exact zero is canonical. This prevents tiny chained values expanding into
megabyte fixed-point strings or silently underflowing into a calculated zero.
Unknown inputs propagate as unknown results; unknown costs cannot become zero
or free profit. No arithmetic result validates sales, traffic, conversion or tax.

## Existing host, not a new execution service

Configure `eightball.event_workers.operating.OperatingPlanningProcessor(spec,
allow_external=True)` as the existing `EventWorkerService` processor. The same
server-owned provider settings, explicit source-processing review, configuration
digest, scoped identity grants, current revision checks and revocation/cancellation
checkpoints apply. No browser preference or incoming source can enable inference.
The processor cannot be invoked without authority checkpoints. No HTTP auto-run,
approval, selected-course transfer, task completion or external send is added.

`EventReviews.view` reconstructs the complete method offline from retained
attempts and transport hashes, rechecking source/configuration binding, typed
outputs, coverage, arithmetic and dispositions. Corruption withholds interpreted
stages but preserves original output. Hashes are local integrity references, not
independent provider signatures. Source-review revocation suppresses material.

The existing event-review page shows original plan, SOPs, unknowns, arithmetic,
written challenges, separate revision, changes/reasons, unresolved items and
transport details. Inspection has no action/approval controls or case writes.
Reload, stale revisions, locking and revoked-read clearing retain existing rules.
There is no automatic conversion into the execution graph: a human must still
use the existing reviewed amendment/observation/approval workflows. Completing
work never applies its intended effects.

## Explicit bounds and acceptance limits

- Maximum five generation calls; no retry, repair, truncation, fallback or model
  substitution. Failure or a missing stage stays visible.
- Host request/response/token/receipt bounds are unchanged: 4,096 output tokens
  per call, 150,000-byte request limit, bounded retained transport and 500,000-byte
  result. Cost is unknown, not free or provider-capped. Large plans may fail these
  limits; no claim of arbitrary-size planning is made.
- Known arithmetic is scenario arithmetic, not observed economics or a forecast.
- A completed method is not a semantically approved or commercially viable plan.
  Structural comparison explicitly does not establish coordination improvement.
- No live inference, genuine human review, real-world effects, £100k result,
  production readiness, public SDK, merge, deployment or release is established
  by this software sprint. Existing B02/ES03 and production gates remain open.

`scripts/export_endstate_schemas.py` exports the brief, plan, spec, review and
revision schemas alongside the original plan/course contracts. The internal
wheel includes the neutral contracts/method, not adapters or credentials.
Run standard native acceptance and installed-wheel regressions; see the
[source-bound session record](../delivery/sessions/2026-11-01-operating-planning.md).
