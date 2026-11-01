# The build goal: 8BALL powered by ENDSTATE

Build 8BALL into a secure, usable application that helps a person turn a difficult
situation into an evidence-backed outcome, compare possible paths, choose a course,
and reconsider it as facts change. ENDSTATE provides the reusable planning engine.

The owner authorised the full existing product roadmap and clearer interface on
25 October 2026, including continuing engineering while external acceptance is
pending. This goal supplements the original PRDs; it does not rewrite or relax them.

## What completion means

| Workstream | Required result | Canonical tasks |
| --- | --- | --- |
| Clear operator workflow | Understand the situation, inspect evidence, compare paths, select a course, act with approval and review changes | B02 |
| Accounts and permissions | Verified sign-in, organisations, durable scoped grants, API/database/worker enforcement and revocation | B03-01 |
| Evidence vault | Controlled uploads, scanning, immutable originals, encryption, retention/holds and authorised deletion | B03-02 |
| Collaboration | Specialist grants and separately reviewed client projections | B03-03 |
| Reliable processing | Durable ingestion/events, idempotency, ordering, recovery and authorised notifications | ES02-01–04, B03-04 |
| Proven intelligence | Actual source-to-plan generation, refusal/cancellation/staleness tests and independent quality evaluation | B02-09–12, B02-15, ES03 |
| Useful decision support | Reviewed playbooks, governed precedent and measured operator benefit | B04 |
| Production readiness | Recovery, monitoring, security, accessibility, onboarding, human acceptance and a limited authorised pilot | B03-05–06, B10 |
| Reusable engine | Domain-pack contracts, justified integration interfaces and compatibility/support evidence | ES04, ES10 |

All applicable acceptance criteria must pass before declaring these results
complete. Software checks, human judgement, independent review, model evidence,
merge and deployment are separate facts. No invented reviewer decisions or
substituted model results count. Multiple scenario comparison remains part of the
goal; unvalidated swarm simulations are not a promised outcome predictor.

## Where to see progress

[PROGRESS.md](PROGRESS.md) is generated from the sole editable status ledger,
[progress.json](progress.json). It shows each task's current state, evidence,
blockers and next action for both 8BALL and ENDSTATE. [HANDOFF.md](HANDOFF.md)
identifies the current source and most recent sprint. [CHANGELOG](../../CHANGELOG.md)
preserves completed changes; [EMERGENCE-REGISTER.md](EMERGENCE-REGISTER.md) preserves
every recorded discovery. This goal document deliberately carries no second set
of completion checkboxes.

## Execution rules

Continue implementation in dependency order without asking the owner to reapprove
routine engineering. Where one acceptance dependency is unavailable, continue
independent engineering and record the exact missing evidence. Every sprint tests
the actual source, updates the canonical ledger/handoff/changelog, performs the
full emergence review, and commits/pushes recoverable work.

Preserve existing data and historical actor/source lineage. Never turn an incoming
event, model output, route selection or completed action into factual evidence or
execution authority. Keep the local development application available while the
agency implementation is built. No production deployment, real-client pilot,
new industry application or deferred research runtime is authorised merely by
this build goal; their explicit gates remain in force.
