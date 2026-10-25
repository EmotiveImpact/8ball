# Incoming events and the host inbox
## Current reviewed-consumption increment

The local host service `eightball.v2.event_reviews.EventReviews` now commits explicit graph reviews atomically with current scope, permission and revision checks. It preserves source/result/reviewer provenance and links conditional exports to the case audit chain. Public agency writes, browser review integration, production database isolation and durable worker/outbox remain unfinished. The earlier sections below describe preceding checkpoints.


`endstate.events.IncomingEvent` is the neutral, versioned input contract. It
records organisation/matter, source and source version, event identity, optional
occurrence time/base revision, text and pending review. It cannot carry approved
review status, commands or authority. Unknown occurrence time remains unknown.

`eightball.event_inbox.EventInbox` is a durable local host implementation. Its
caller must first authenticate and authorise the supplied matter scope. No public
endpoint, connector, automatic model call or case mutation is installed by this
component. ENDSTATE itself acquires no database or network dependency.

The inbox assigns receipt time and an increasing arrival sequence per matter.
Occurrence time does not reorder the inbox. A duplicate identity consists of
organisation, matter, source and event ID. Identical retries return the original
receipt; changed content, source version or base revision raises a conflict.
Concurrent appends serialize in a transaction. A process restart retains receipts
and deduplication. Pages use an exclusive sequence cursor with a bounded limit.
Stored content hashes detect body corruption; they are not signatures or
independent tamper-proof audit anchors.

This completes an engineering increment inside ES02-01/02. The durable worker,
outbox, processing acknowledgements, reviewed amendments, expected-revision
commit, permission revalidation, cancellation and measured full-versus-incremental
replanning remain unfinished. Reading/replaying inbox records cannot execute
actions or revive an expired grant because this inbox has no such capability.

The future boundary is: observe → retain → propose → review → commit at the
correct revision → replan → explain → ask for reconsideration. Never skip review
or carry an old permission forward merely because an event is retried.

## Durable processing attempts

The host `eightball.event_work.EventWork` now stores explicit attempts linked to scoped inbox records. It supports exclusive claim, bounded lease, retained output disposition, cancellation and interruption. Expiry never automatically reschedules an attempt. A fresh enqueue is an explicit new attempt and preserves the old record. Claim-token hashes stay private and are omitted from inspection output.

Results can await review; they cannot mutate a case. Permission and revision observations are trusted host inputs, not proof of transaction-wide authorisation. The real worker/outbox, reviewed commit, transactional revalidation and performance gate remain unfinished.

## Transactional local notice outbox

`eightball.v2.event_outbox.EventOutbox` inserts a small reviewed-change notice in the same transaction as graph consumption. Trusted authenticated readers require current whole-matter READ grants to pull or acknowledge. The oldest unacknowledged case notice repeats until acknowledged; delivery is durable and independent for each reader. Acknowledgement never approves an action or modifies the case. Notices verify their metadata against the review record. No external sender, worker daemon, browser surface or historical backfill is installed. See [session](../delivery/sessions/2026-10-25-endstate-outbox.md).

## Authenticated event API

With agency mode configured against the same database as cases, `/api/v2/cases/{case_id}/event-work/{work_id}` returns original source/result and reviewability under current READ permission. POST `.../review` accepts only an explicit `command` and `rationale`; the verified JWT supplies reviewer identity and the transaction requires READ plus WRITE. POST `/api/v2/cases/{case_id}/change-notices/pull` and `.../{notice_id}/acknowledge` use current READ permission and never approve actions. Other unsupported agency mutation/model routes remain denied. These routes are absent for local-token mode or a separate access database. No browser review UI or external delivery is installed. [Session](../delivery/sessions/2026-10-25-endstate-event-api.md).
