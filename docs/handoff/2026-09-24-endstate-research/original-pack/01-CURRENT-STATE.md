# Current build state - 24 September 2026

## Product identity

8BALL is the flagship fixer / situation-handling application.

ENDSTATE is the reusable outcome-engineering technology underneath it.

The accepted dependency direction is:

```text
8BALL application
    ↓
8BALL / fixer domain pack
    ↓
ENDSTATE contracts + kernel
```

Future products should follow the same pattern rather than duplicating the planner.

## Current milestones

| Track | Milestone | Current snapshot | Meaning |
|---|---|---:|---|
| Governance | 1.1 | 6/6 | Scoped governance gate met in latest preserved local checklist |
| 8BALL | V0.1 | 3/3 | Local foundation verified in scope |
| 8BALL | V0.2 | 9/20 | Current build, not accepted |
| 8BALL | V0.3 | 0/6 | Do not start as a release track yet |
| 8BALL | V0.4 | 0/3 | Future |
| 8BALL | V1 | 0/2 | Future |
| ENDSTATE | V0.1 | 4/5 | Reusable core nearly through scoped gate, not accepted |
| ENDSTATE | V0.2 | 0/4 | Required milestone not started |
| ENDSTATE | V0.3 | 0/4 in roadmap summary | Future intelligence compilation |
| ENDSTATE | V0.4 | 0/4 | Future domain packs/integration interfaces |
| ENDSTATE | V1 | 0/2 | Future supported reusable engine |

Counts are **not percentages of product completeness**.

## Current high-priority unfinished work

### B02-09 - reliable reviewed graph proposals for genuinely new situations

This remains a critical blocker.

Earlier actual-model attempts failed. The system must not repair a bad model proposal invisibly, substitute a catalogue route, reduce the fixture set, or call structural validation "semantic quality".

The latest local integration work improves grounding/target validation and staged compilation, but real-provider quality still requires acceptance.

### B02-10 - robust source extraction, deadlines and entity reconciliation

Local Source Desk and Source Clarity work add safer source handling, mention-level review, timezone/deadline interpretation and route-impact preview.

Still outstanding:

- native cumulative integration
- independent multi-source identity/date evaluation
- reliable arbitrary model extraction
- no automatic global coreference/merge claims

### B02-11 - independent quality evaluation and production-model selection

Partial only.

Needs:

- prospective protocol approved before evaluation
- independent reviewer labels
- held-out cases
- explicit thresholds
- actual provider/model comparison
- latency, correction effort, omission, unsupported assertion and abstention measurements

Software tests are not independent model-quality approval.

### B02-12 - full twenty-step real-model V0.2 acceptance journey

Blocked until the actual-provider journey can run.

The required journey must genuinely exercise:

blank case → real extraction → human review → valid graph → alternative routes → new evidence/replan → isolated scenario/refusal → approvals/completion → reload/export.

Rules/catalogue journeys do not satisfy this gate.

### B02-13 / B02-14 / B02-15 / B02-16

Later local work reports substantial implementation for:

- guided graph authoring
- source handling and reconciliation
- analysis progress/cancellation
- accessibility controls

But native authorised acceptance remains outstanding for important parts.

### B02-18 - V0.2 acceptance and release decision

Blocked until the required V0.2 subparts are actually accepted.

Keep PR #2 draft until this gate is met or deliberately changed through an explicit product decision.

### ES01-05 - reusable core acceptance

Latest local checklist records this as implemented, not fully verified.

The remaining action is to inspect package/source/schema compatibility evidence and run the cumulative native application gate in an authorised environment.

Do not call ENDSTATE a public SDK release on the strength of the internal package.

## Preserved local checkpoints

The source-of-truth folder contains a Source Clarity handoff for `0.2.0-alpha.5` and a later integrated checklist.

The Source Clarity checkpoint reported:

- exact local source tree `c057d35ff84c1480243208d9674f4e99f7bf74a6`
- remote ancestor `824ca6421ff3100e1af596347f2d1247dde8f8dc`
- 746 code tests passed
- 275 ASGI-bridge browser checks across eight suites
- native navigation blocked by administrator policy
- no new live Qwen, Hugging Face or JEV inference

The later integrated checklist reports a larger local integration checkpoint:

- 855 code tests
- installed internal wheel rerun
- 344 bridged browser checks across ten suites
- native loopback still blocked in that environment
- model/expert acceptance still unfinished

Use the later cumulative source artifact if it can be located. Do not apply earlier cumulative packages on top of it.

## Recovery hierarchy

When facts disagree, use this order:

1. **Actual current GitHub branch/PR and files** for what is really remote.
2. **Newest exact cumulative local source/patch artifact** for unpublished code.
3. **Canonical `docs/delivery/progress.json` inside that exact source tree** for statuses.
4. **Session handoff and evidence records** for what was tested.
5. **This context pack** for accepted product direction and research implications.
6. Chat memory only as a final fallback.

## Acceptance philosophy

Built, verified, merged, packaged, deployed and commercially released are separate states.

A test can prove software behaviour without proving model quality.

A model can produce a structurally valid object without proving semantic correctness.

A simulated result can test a possible world without proving what will happen.

Those distinctions are core ENDSTATE design principles.
