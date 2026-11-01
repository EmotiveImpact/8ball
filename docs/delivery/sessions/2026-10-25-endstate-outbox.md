# ENDSTATE local change outbox — 25 October 2026

Base `e0ae9b081629239a16ce79e95628cf504227fbc6`; branch feat/agency-authorisation-20261025, draft PR5. The existing goal authorises continued engineering, not external sends or deployment.

The reviewed graph transaction now inserts a durable change notice atomically with the case, consumption record and work completion. Failed insertion rolls the entire transaction back. Notices hold revision/provenance references, not original source or model text. Duplicate review acknowledgement creates no second notice.

A trusted host supplies authenticated readers. Pull checks current whole-matter READ permission, returns the oldest unacknowledged case notice and durably records that reader's delivery. Acknowledgement requires prior delivery and rechecks current permission; it never changes the case or grants action authority. Permission expiry is rechecked before committing delivery/acknowledgement. Repeated delivery is expected until acknowledgement, and each reader has separate state. Notices are verified against retained review metadata.

This is a local SQLite pull-based foundation, not an external sender, background daemon, browser notification interface, PostgreSQL tenant guarantee or actual-provider acceptance. Existing historical consumed reviews are not backfilled silently. Future migration must explicitly reconcile old records. Current tracked statuses remain partial.

## Verification

Focused and full native results are recorded in the closeout below when complete. Tests cover rollback after outbox insertion, restart persistence, duplicate review, concurrent delivery, ordered notices, per-reader acknowledgement, missing read access, revocation, expiry during pull and rehashed metadata corruption.

## Emergence Review

What did this reveal? Acknowledging delivery is a separate durable per-reader fact from reviewing a graph change or approving an action (EM-105).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | Continue the standing ENDSTATE/8BALL goal with the existing ES02 work. |
| ER-02 | Keep delivery persistence in the host, not the kernel. |
| ER-03 | Atomically bind notice creation to reviewed case commit. |
| ER-04 | Browser review, daemon, production isolation and external delivery remain incomplete. |
| ER-05 | Delivery acknowledgement never attests a fact or approves an action. |
| ER-06 | Require fresh READ grants; a writer need not be allowed to read notifications. |
| ER-07 | Recheck expiry before persisting delivery. |
| ER-08 | At-least-once delivery permits repeats; no exactly-once external effect is claimed. |
| ER-09 | Verify notice metadata against the original review digest. |
| ER-10 | Never silently backfill historical consumption records. |
| ER-11 | A change notice cannot select or switch a course. |
| ER-12 | Test ordered/concurrent reads, rollback and permission failures. |
| ER-13 | Preserve all prior attempts, receipts and failed evidence. |
| ER-14 | Commit recoverable source and exact-source native receipt on the existing branch. |
| ER-15 | Reliable notice persistence can reduce missed updates; usefulness needs actual operator evaluation. |

Evidence: controlled local transactions. Risk: recipients can repeat a delivery after restart, so later consumers must remain idempotent. UX: distinguish delivered/acknowledged from reviewed/approved. Disposition: existing ES02-02/04 remain partial; all original model/human gates remain open.

## Verified closeout

40 focused event/review/outbox tests passed. Source `49f5e04fe8f4f122818c09343aba030338a26347` passed 1,331 source tests, 1,331 installed-engine regressions and 396 native browser checks across eleven suites. Exact source/artifact inspection passed before receipt edits. Both checkpoint CI workflows passed: 40209159166 and 40209159271. [Receipt](../../evidence/endstate-outbox-native-2026-10-25.json). Code is pushed on feat/agency-authorisation-20261025 in draft PR5; this documentation closeout is committed separately. No release, merge or deployment occurred.

Next: explicit event review UI/API and authenticated host worker dispatch, preserving duplicate/cancellation/revocation checks. Migration, performance comparisons and all original production/model/human gates remain unfinished. EM-105 records this sprint discovery; no further scope is adopted by this verification.
