# Incoming events and the host inbox

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
