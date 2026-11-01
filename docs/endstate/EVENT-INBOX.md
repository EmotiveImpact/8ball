# Incoming events and the host inbox
## Current explicit local dispatch (events lane)

`eightball.event_workers.EventWorkerService` now combines the existing durable
inbox, queue, current grants and case revision in owning SQLite transactions.
It provides explicit text intake, source-processing review, idempotent enqueue,
one-call processing, cancellation and content status. No import/startup loop,
URL fetch, folder/vault scan, automatic inference/retry or external send exists.
The original local app and alpha import/audit paths are unchanged.

The host authenticates identities. `authority(db, identity, resource,
operations, now) -> bool` defaults to current `agency_grants`; operations are a
tuple of `eightball.authorisation.Operation`. Whole-matter READ/INFER is required
to request/run processing; READ/WRITE to review source processing, revoke that
review or cancel. Text intake requires WRITE; content status requires READ.
Object-only grants do not become whole-matter access.

### Required current source policy

Both dispatch and graph review require the same trusted host callback:

```python
source_policy(db, identity: Identity, case_id: str,
              receipt: EventReceipt, now: datetime) -> bool
```

The callback checks current source/object access, quarantine/scan status,
retention/withdrawal and processing/egress permission. Missing/false policy
**fails closed** at source-processing review, enqueue, claim, result publication,
content status, preview and graph commit. Never substitute an allow-all callback
for a missing vault/provider policy adapter. The tests' explicitly fictional
local-text policy is not a managed service. Callbacks must be synchronous,
side-effect-free current checks on the supplied transaction; independent policy
stores still need a production revocation/transaction design.

`review_source` binds an explicit reviewer/rationale to receipt digest, case and
revision. This is neither factual verification nor action permission. Review
revocation blocks processing/publication/consumption. A changed case requires a
fresh review. An old revision-bound envelope cannot silently be rebased; retain
it and supply an explicit new envelope/review for a new revision if intended.

`enqueue` requires sequence, revision, review ID and bounded request ID. Identical
retries return the same work ID only after current checks. Concurrent requests
cannot duplicate active work. At most three explicit attempts exist per
case/receipt. A new attempt requires a new request ID and terminal prior work.

The host explicitly invokes `process(case_id=..., work_id=...,
worker=verified_identity)`. A durable claim/run marker precedes one configured
`processor(receipt, detached_case_snapshot) -> str` call. There is deliberately
no processing/provider-execution HTTP route. Processor text is bounded and
retained, never a command or observed effect. Provider selection, timeouts,
resource/budget and external consent remain host/provider obligations; this
service never grants permission for a paid call. An absent processor is an
error, not invented success. Exceptions retain only a safe `processor_failed`
code; invalid/oversize output becomes `invalid_result`, without truncation.

Finalization rechecks grants, source review/policy, case revision, lease and
cancellation. Late/stale/denied output is inert retained trace, not a reviewable
amendment. Cancellation cannot recall an in-flight request. A crash after claim
or failed result persistence requires explicit inspection, never silent provider
repetition; expiry becomes `interrupted`, not automatically requeued.

### Optional integration and reviewed consumption

On a protected agency router, after verified authentication and operation-policy
mapping, call `register_event_worker_routes(router, service)` and
`register_event_routes(router, store, source_policy=policy)` from
`eightball.v2.event_api`. Construct both the worker and `EventReviews` with the
same current source policy. Missing policy denies dispatched graph consumption
even for a reviewer with grants. Unknown agency routes must remain denied;
never mount these as a local-token fallback. No shared router changes are made
by this lane. OIDC, PostgreSQL isolation and production object policies are not
implemented by these SQLite services.

The existing graph preview stays read-only. Reviewed consumption requires exact
case/matter/revision, current READ/WRITE, source-review/policy and explicit graph
command/rationale. It atomically persists the audit, original receipt/result,
review and local outbox notice. Approvals are invalidated by the existing command
service; intended effects never become observed truth. Notices are local pull/
acknowledgement records, not external notification delivery or action approval.

### Conservative replan parity and local timing

`eightball.event_workers.replan.EventReplanner.replan(PlanRequest)` returns a
typed response, mode and measured elapsed duration. Its bounded, detached cache
reuses only identical planning inputs at the exact explicit as-of clock. A
revision-only change is reusable only without revision-bound action approvals.
Every graph/evidence/clock/sort/other input change uses full ENDSTATE calculation;
revision changes with approvals also force full calculation. Tests compare the
complete response to fresh `endstate.api.calculate`. This is conservative
unchanged-input reuse, not general partial-graph computation or a performance
guarantee. Replanning never changes a case, action authority or chosen course.

Review records include available ingestion, processor-stage, pre-commit review
processing, review-wait and receipt-to-review durations. Ingestion/review
durations stop before their owning transaction commits; absent historical
metrics remain null. Local instrumentation and a fictional processor exercise
are not actual-model inference or human-review latency evidence. Full combined
provider/review and general incremental-graph performance acceptance remain open.

Exact tests, limitations and integration steps: [lane receipt](../delivery/lane-reports/events.md).
No broad ES02/B03 acceptance, native-browser result, real provider success,
independent review, release or deployment follows from this increment.

## Historical checkpoint notes (superseded capability gaps)

The sections below retain earlier component descriptions and historical gaps.
The current section above, live source and lane receipt control this increment;
past statements that worker/outbox/UI are absent are not current implementation
claims. Historical receipts remain bound only to their own source bytes.

### Reviewed-consumption checkpoint

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

## Case binding and historical migration

New case-processing attempts pass `case_id` to `EventWork.enqueue`, which verifies the case belongs to the supplied matter. An event's matter and base revision alone cannot identify its case. Unbound generic/historical attempts remain retained, but new reviewed consumption rejects them. Migration adds a nullable case column without inferring ownership. Already committed historical review receipts retain their prior duplicate-acknowledgement and export behaviour. No automatic retry or backfill occurs.

## Browser review

The event detail response includes a token-free `/v2/event-review.html?case=...&work=...` link. Configured agency users can open the source/result, edit the current graph through the existing Plan Studio, preview, supply rationale and commit explicitly. The scoped preview endpoint is read-only. Account tokens stay in memory only; actual OIDC sign-in is unfinished. Read-only/stale states and unknown save outcomes cannot commit; refresh resolves uncertain outcomes without automatic replay. [Session](../delivery/sessions/2026-10-25-endstate-review-ui.md).

## Complete bounded processing output

`EventWork.finish` retains exact result text up to 500,000 UTF-8 bytes, matching the supported hosted response envelope. This replaces the provisional 12,000-character cap that rejected the ordinary full graph. Original output survives restart, review and export without truncation. Over-bound results fail without mutating the attempt; caller-owned transport failure evidence remains necessary. This does not authorise automatic inference or retries.
