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
