# Production architecture and release gate

**Design only. Not deployed or verified infrastructure.** V0.2 is for a trusted local operator and fictional cases. Neither the bearer token nor local SQLite is a sufficient boundary for real agency matters.

## Assets and adversaries

Protect client identities, privileged/confidential documents, allegations, contact information, evidence provenance, drafts, expert notes, approvals and model traces. Threat actors include an external attacker, a malicious source document, a compromised specialist account, a curious employee, one tenant probing another, an abusive administrator, a stolen device and a compromised model/provider dependency. Do not treat an accepted model proposal as evidence or an expert's access as organisation-wide access.

## Proposed deployment boundary

A browser communicates with an authenticated API over TLS. An OIDC identity provider supplies verified identities and MFA. The API resolves organisation and matter membership server-side. Postgres stores structured objects and domain events; encrypted object storage holds evidence. A durable worker/outbox processes approved ingestion and notifications. Model gateways enforce source allowlists and provider/data-processing policy. Separate signing/anchoring infrastructure protects audit checkpoints. None of these services is provisioned by this release.

## Tenant and matter authorisation

Every case-owned row must carry `organisation_id` and `matter_id`. Foreign keys between case objects must include the same organisation/matter keys, not merely globally unique IDs. Database row policies and application membership checks must agree. A service account must not expose unrestricted SQL to the browser. Set tenant context inside the transaction, not in a reusable pooled connection outside its scope. Tests must show that a user in organisation A cannot read, mutate, export, search, simulate, download or request model inference on organisation B's data, including through malformed IDs and cached results.

Roles should include agency director, case lead, specialist and client. A specialist receives an explicit matter-scoped, object-scoped grant with expiry and revocation. Client brief publication is a separate reviewed projection: no internal source text, assumptions or deliberations are exposed by default. Revoke access at the API, database, object links, search index and model cache together. “Read only” must prevent proposal review and indirect changes too.

## Evidence vault

Uploads require size/type limits, malware scanning, quarantine, immutable original bytes, cryptographic content hashes and server-controlled source metadata. Preserve source spans against the exact immutable representation. Derived text/OCR is a separate version with provenance and uncertainty, not a replacement for the original. Signed object URLs must expire and be scoped to one authorised object. Use envelope encryption backed by managed keys, independent backups and documented residency. Do not imply that encryption creates legal privilege.

Retention, deletion, lawful holds and exports require an explicit policy with authorised human owners. Deletion must reconcile backups, indexes, replicas, provider retention and derived data. Do not automatically destroy evidence in response to a source instruction or a client's desire to conceal wrongdoing.

## Model and action boundaries

Provider processing must be approved for each matter's data classification. Source excerpts are minimised and optionally redacted; provider retention/data-use settings must be verified under the applicable agreement. Do not train on confidential cases by default. Model output is untrusted input, even when it validates as JSON. Human review remains separate from source verification. Prompt-injection tests must attempt tool requests, hidden instructions, cross-case references, source forgery and unsupported acceptance/authority.

Keep inference workers read-only with respect to case commands. Any future external send requires exact recipient, content digest, scope, expiry, named authoriser, current case revision and idempotency key. Two-person approval may be required for high-impact, irreversible or regulated actions. An approval to draft is not approval to send. No free-form agent shell or unbounded autonomous execution should sit inside a case.

## Audit and operational resilience

Use append-only database privileges, authenticated actor identity, durable event IDs and independently anchored checkpoints. Record access to sensitive objects, not only edits. Administrators need separated roles and break-glass procedures. Audit exports must verify source hashes, event completeness and anchoring. Logs must avoid raw evidence, credentials and bearer tokens.

Backups need encryption, separate credentials, defined recovery point/time objectives and observed restoration tests. Test stale writes, concurrent approval, duplicate webhooks, worker crashes, outbox replay, cancellation, clock skew, lost internet, model timeouts and partial storage failure. Metrics should include unresolved critical questions, stale evidence, failed ingestion, approval age and access anomalies without exposing client content.

## Production acceptance gate

Do not call the product production-ready until these are demonstrated in an isolated pilot: identity and MFA; cross-tenant and cross-matter denial tests; specialist/client scoping and revocation; safe uploads and source hashing; encrypted storage/backups; recovery rehearsal; externally anchored audit verification; dependency and penetration review; provider processing authorisation; action approval abuse tests; retention/hold policy; operator/expert review of playbooks and model evaluation. An agency director must explicitly authorise a limited pilot before real client information is introduced.

## Persistence migration proposal

Keep the domain contracts independent of SQL. Introduce repository transactions that accept identity/matter context. Backfill V0.2 snapshots into a tenant-owned staging area, validate every foreign key and source hash, preserve original export/chain lineage, and reconcile counts before cutover. Never invent historical users from the local `local-operator` actor label. Preserve those historical entries as imported device records. Run dual-read comparison and rollback rehearsal before replacing SQLite. Production proposals, evidence objects, observations, decisions and action approvals should be separately addressable, versioned rows with enforced matter keys.
