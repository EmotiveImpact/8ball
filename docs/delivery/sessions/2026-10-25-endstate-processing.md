# ENDSTATE durable processing — 25 October 2026

Base5f72a356790b0cd3f0a27e79ba1e9801f4a14937; branch feat/agency-authorisation-20261025. Automatic continuation of the existing owner goal to build all ENDSTATE; no new deployment, external-action or inference permission.

Built EventWork, a host-owned durable attempt lifecycle linked to the scoped inbox. Explicit enqueue creates a distinct attempt; exclusive claim returns an opaque token whose hash alone is stored. Bounded leases, durable cancellation and restart behaviour prevent silent reclaim/retry. Returned output becomes awaiting_review only when the trusted host reports matching revision and valid permission; stale, denied or expired results retain their own dispositions. No result applies a case command.

18 focused inbox/lifecycle tests passed. Full native verification follows. This is not an automatic worker, outbox, reviewed commit integration or production access boundary. Host-supplied revision/permission values are not independently verified by this component. Review/commit must revalidate them inside the actual case transaction. In-flight provider work cannot be recalled; cancelled/interrupted late completion raises a conflict and the caller remains responsible for preserving any external raw response. No external calls occur here.

## Emergence Review

What did this reveal? A lease timeout cannot prove whether an external service already acted (EM-102).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | Continue the existing all-ENDSTATE goal. |
| ER-02 | Persist attempt state in the host; keep the kernel calculation-only. |
| ER-03 | Restart cannot establish the outcome of an in-flight external operation. |
| ER-04 | Worker/outbox and transactional reviewed consumption remain dependencies. |
| ER-05 | A processing claim does not grant case or action authority. |
| ER-06 | Automatic lease reclamation could duplicate paid calls. |
| ER-07 | Preserve interrupted attempts and require explicit new attempts. |
| ER-08 | Controlled lifecycle tests are not live-provider cancellation evidence. |
| ER-09 | One concurrent claimant, scoped lookup and strict revision checks. |
| ER-10 | Stale and denied results must not appear ready for normal review. |
| ER-11 | No facts, target, selected course or approvals changed. |
| ER-12 | Test restart, cancellation, expiry, forged claim and concurrent claiming. |
| ER-13 | Preserve earlier101 discoveries and prior attempt evidence. |
| ER-14 | Host permission observations need transactional revalidation at commit. |
| ER-15 | Build reviewed case integration and durable outbox next. |

Evidence: controlled persistence/lifecycle tests. UX: distinguish interrupted, cancelled, stale and permission-denied work. Architecture: no automatic service execution/retry. Disposition: existing ES02-02/04 tasks remain partial.

## Demonstrated review race and correction

The first cumulative native run20261025T151314Z-2277beb7 failed Plan Review: opening while a refresh completed changed the snapshot stamp, and discarded responses left the dialog loading indefinitely. Exact source/artifact inspection was valid/failed before editing. Both remote checkpoint workflows passed, showing why the retained local failure still matters. Receipt: docs/evidence/endstate-processing-failed-2026-10-25.json.

The review now displays an explicit context-changed state with a manual reopen button; it neither publishes the stale assessment nor retries automatically. Responses from superseded dialogs cannot overwrite the current one. The native journey now waits for the actual refreshed revision and separately forces an in-flight revision change. All35 focused native Plan Review checks passed after the fix. Full cumulative rerun follows.

Emergence addendum (ER-03/06/12/13): rejecting stale data is not a complete UI outcome; pending indicators need a terminal recovery state (EM-103). Preserve the failed run and actual focused reproduction. Existing lease behaviour also relies on a trusted host wall clock; clock-skew handling and transactional permission checks remain production work, not claims of this component.

## Final verified checkpoint

Source `e95401aa289be03ab98810955e4fe02fdd8bbea2` passed **1,309 source tests, 1,309 installed-engine regressions and 396 native browser checks across all 11 suites**. Exact source/artifact inspection was valid/passed before final receipt edits. Both checkpoint CI workflows40206717456 and40206717459 passed. One existing Starlette/AnyIO warning per Python run. The prior failed run remains retained and linked. Receipt: docs/evidence/endstate-processing-native-2026-10-25.json.

Next concrete implementation: bind a reviewed graph-amendment command to a specific awaiting-review attempt, original event and case revision; check current reviewer permission and apply the command plus consumption record atomically. Reuse existing graph validation and approval invalidation. Test duplicate consumption, stale revision, revoked permission, cross-matter input, failure rollback and route-change explanation. Preserve both the original result and explicit human edits; assisted work never passes the unassisted model gate. Do not expose writes through the agency API until complete transaction/actor enforcement exists. Then implement explicit durable worker/outbox delivery and full-versus-incremental replan evidence.
