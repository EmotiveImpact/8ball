# Local analysis lifecycle

The browser submits `POST /api/v2/cases/{id}/analysis-jobs` with an idempotency ID, expected revision, selected source IDs, operation/provider and explicit external permission. The service validates source scope, provider configuration and permission before admission. `GET` endpoints show case-scoped status; an explicit cancel endpoint stops publication. The original synchronous analysis endpoint remains for compatibility and shares the inference semaphore.

States: queued, running, succeeded, failed, cancelled, superseded, interrupted. Stages name work actually reached: preparing context, provider request, reading response, validating response and validating proposal. Started/completed call counts are actual stage observations, not fabricated percentage-complete estimates. A queue holds at most eight active/draining jobs and one provider runs at a time. Cases have a bounded job history.

Job metadata is durable in local SQLite. It stores request settings and source identifiers, not a bearer token or copied evidence body. The worker validates the current revision before inference, between requests and before publishing. Proposal persistence and success are one transaction. A cancel or case-change race cannot publish a late successful response. A succeeded result is not retroactively deleted by a late cancel; it remains a human-review proposal. No model can commit a case, attest facts or approve actions.

Cancellation is cooperative. A request already in flight may complete or incur provider charges; local Python threads cannot undo a remote request. Cancellation prevents further stages, stops reading between hosted response chunks, and discards late results. The shared worker remains occupied while the current request drains. Timeouts in the existing transports remain enforced, but no global provider-compute cancellation guarantee is made.

A server restart marks unfinished jobs interrupted and never automatically resumes or retries them. The user explicitly starts a new request with fresh permission. This design assumes one server process. It is not a multi-worker/distributed scheduler, production tenancy boundary or secure agency job system.

The Intake Review analysis monitor persists through page refresh by querying the server. Workspace lock clears local rendered state; it does not falsely imply that running inference has stopped. Re-open the case to inspect or cancel outstanding work. Form edits in a pending review are not silently replaced by polling. Unknown runtime availability remains honestly reported by the existing explicit local probe.

Verification includes queued and in-flight cancellation, later-stage suppression, stale results, scope, restart, request idempotency, queue limits, authentication and failure-body redaction. Providers are test doubles for these tests. Live Hugging Face/JEV credentials and real-model quality evaluation are separate requirements.

Implementation reference: Python's concurrent futures documentation says a running call cannot be cancelled through `Future.cancel`; HTTPX documents separate connect/read/write/pool timeouts. These constraints are why the UI promises discard and stage stopping, not provider-side recall. References: https://docs.python.org/3.13/library/concurrent.futures.html and https://www.python-httpx.org/advanced/timeouts/.
