# ENDSTATE reviewed consumption — 25 October 2026

Base `cbbe5eaa028bbb9c6427ac721570eaa67a402fad`; branch feat/agency-authorisation-20261025. Continuation of the existing all-ENDSTATE goal, with no new external-action or deployment authority.

Implemented `EventReviews.commit_graph`: a trusted host supplies authenticated reviewer identity, explicit graph command and rationale. The service checks stored case/matter ownership and current write grants inside BEGIN IMMEDIATE in the same database as cases, inbox and work records. It requires an awaiting-review attempt and exact processing/case/command revision. It reuses existing graph validation, approval invalidation and route-change explanations, then records case change, linked review receipt and consumed state atomically. Permission expiry is checked again before commit. Explicit review recording is not proof of genuine human participation or semantic quality.

Receipts bind source and arrival metadata, original processing output, reviewer identity, rationale and explicit command to the case event request hash. Conditional exports verify these bindings plus the recorded explanation/timestamp. Source-free cases retain their original export shape. Matching retries return the original receipt only after fresh permission checks; changed retries conflict. Failed writes roll back both case and consumption.

32 focused event/review/lifecycle tests passed. Full native verification follows. Agency public writes remain disabled. Host identity validation, browser review integration, PostgreSQL isolation, durable worker/outbox, performance comparisons and actual model/human gates remain unfinished.

## Emergence Review

What did this reveal? An explicit reviewed result must be tied to the actual authorised transaction, including expiry during calculation (EM-104).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | Continue the standing all-ENDSTATE goal. |
| ER-02 | Keep neutral event contracts in the kernel and case transactions in the host. |
| ER-03 | Separate durable processing completion from explicit reviewed case consumption. |
| ER-04 | Browser/API integration and worker/outbox remain unfinished. |
| ER-05 | A review record never proves a fact, action approval or genuine human acceptance. |
| ER-06 | Revoked, expired and object-only grants cannot authorise whole-graph amendments. |
| ER-07 | A permission can expire during plan calculation; check again before commit. |
| ER-08 | Controlled local transactions do not establish production tenant isolation. |
| ER-09 | Bind source, receipt, result, reviewer and command to the case chain. |
| ER-10 | Rehashed receipt tampering must not substitute a different original result. |
| ER-11 | Preserve existing approval invalidation and source meaning guards. |
| ER-12 | Test concurrency, rollback, stale versions, permission/scope denial and export compatibility. |
| ER-13 | Preserve previous103 discoveries and all failed native/model evidence. |
| ER-14 | Add export evidence only to cases that actually consumed an event. |
| ER-15 | Connect explicit UI/API review and durable delivery without automatic execution. |

Evidence: controlled local transaction and lifecycle tests. UX: show original source/output alongside explicit reviewed edits and resulting route changes. Disposition: existing ES02 tasks remain partial; no automatic model call, external action, deployment or release.
