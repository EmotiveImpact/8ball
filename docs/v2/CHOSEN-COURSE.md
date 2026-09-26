# Chosen Course: local operator workflow

Developer checkpoint `0.2.0-alpha.8`, 25 September 2026. This is groundwork for optional B03-07 / ES02-06, not a secure agency or V0.3 release.

## What it does

Choose one current, non-empty candidate with no declared hard breaches. The operator supplies a rationale, optional assumptions, explicit condition-state watches and an optional offset-bearing review time. A preview binds the exact case revision, route, target, watches and clock. Confirming creates a durable local choice without altering the case snapshot, observations, decisions or action approvals. Selecting a course does not restrict all work to that route or confer permission to perform it.

The Situation Room displays the chosen course alongside the target. Ways Through offers the selection control. Inspect the original rationale and target, remaining work, reasons for review and other current options. Alternatives never replace the chosen course without an explicit new selection. No extra top-level page was added. Course judgements appear in the existing timeline and case export.

Pause, resume, retire, review and replace are append-only judgements with reasons. Previous choices remain visible. Review does not clear deterministic warnings or restart a watch clock. A pause or retirement concerns the recorded course, not cancellation of external work or revocation of separate action approvals.

## ENDSTATE boundary

`endstate/course.py` exposes `anchor_route`, `verify_anchor` and `assess_course` with `endstate.course.v1` typed contracts. The host supplies a detached PlanningSnapshot, an explicit aware clock and a SHA-256 of the human target/mandate. ENDSTATE imports no 8BALL, database, web framework or model provider. It never writes state.

Reassessment checks changes in target/criteria, actions, selected requirements, evidence/support, sources, actors, decisions, constraints, budget, resources, deadlines and explicit watches. An elapsed review time can trigger reconsideration at the same case revision. Unknown does not satisfy a true/false watch. Read-only remaining-work calculations enable only recorded actions and pin the chosen prerequisite branch; they check the original declared ordering. Completed work is not rescheduled or treated as proof of its effects. Structural remainders may still contain evidence gaps: their existence is not proof an unavailable action can be performed.

Missing objects produce `not_assessable`. Recorded changes can produce `review_required`. `no_trigger_detected` means no declared trigger was detected within supplied inputs, never reassurance about unmodelled reality. Reassessment is **on request**, not a background event/notification service. Source-set changes trigger review without reading new text as an authorised instruction.

## Persistence and authority

`v2_course_events` is a separate append-only local journal. Each entry links its sequence, previous hash, exact case-event snapshot, actor label, request hash and rationale. Selections preserve the original graph and target. Later reviews preserve the inspected assessment. A SQLite transaction checks the case revision and course sequence before a write. Duplicate event IDs replay the original response; conflicting reuse fails. Preview/review digests expire after ten minutes. A replacement must explicitly name the current course. Foreign-case and stale-context requests fail without partial mutation.

Course and case history hashes are verified before writing. Export includes `chosen_courses` only when such a journal exists, preserving the old source-free export shape. This is local application integrity, **not** independent forensic anchoring, tenant security or authenticated agency identity. `local-operator` is a device-scoped label, not a verified user identity.

## Boundaries still open

No full client mandate, negotiated fallback authorisation, secure team ownership, notifications, background monitoring, model-generation improvement or external execution is added here. V0.2 native, real-model, independent-review and accessibility gates stay open. Existing approval invalidation rules remain unchanged. The previously narrated Draft Repair implementation was not recovered and is not silently included.

## Verification commands

```sh
python -m pytest tests/test_courses.py -q
python scripts/acceptance.py --mode native --base <starting-commit>
```

`tests/browser_courses.py` is native by default and is part of the acceptance runner. An explicit bridge run is a separate, limited test mode. Final aggregate reports in the developer pack bind source/evidence bytes; a blocked native report does not mean acceptance passed.
