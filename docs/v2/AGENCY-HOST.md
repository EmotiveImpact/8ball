# Optional shared agency engineering host

8BALL remains the fixer; ENDSTATE is the calculation kernel. The original `/` and `/v2/` local operator workflows remain available when agency configuration is absent. The separate `/v2/agency.html` desk is discoverable directly and explicitly reports missing configuration. It is not a production client portal or a second application.

## Opt-in startup and policies

`EIGHTBALL_AGENCY_CONFIG` names a private server JSON file. `python -m eightball` loads it with `eightball.agency_host.load_host`. Do not commit this configuration or any key material. Allowed top-level fields are `issuer`, `audience`, `public_key_file`, optional `vault_key_file`, optional `oidc`. API keys/provider tokens do not belong in this file. Ordinary acceptance strips this setting and provider credentials.

`oidc` uses the strict `OIDCConfig` fields described in AGENCY-ACCESS.md; replace its in-memory `signing_keys` with server-owned `signing_key_files` mapping approved key IDs to local public-key paths. `client_id` must equal the API audience. Login/callback/session/logout are on a separate router, never behind authenticated case routes. Cookies require TLS, the exact configured origin on mutations, and the existing host allowlist. The local CLI is HTTP: it does **not** establish a production TLS/IdP deployment. Use an explicitly managed loopback TLS host for fictional browser/session work; no arbitrary-host or CSP relaxation is supplied here.

Configuration does not provision people, matters, grants or capabilities. The server must bind an existing case with `AccessRegistry.bind_case`, explicitly add time-bounded current operation grants, and grant named capabilities through `AgencyHost.grant_capability`. Provisioning has no HTTP endpoint. Object-only client grants do not authorize whole-case reads, listings, knowledge search or original downloads. The local operator bearer never substitutes for an agency principal, including when a cookie is also present.

The JSON loader deliberately supplies **no** scanner, processing-consent/egress/retention policy, processor, dependent-copy deletion guard or revocation probe. Upload/metadata require keys and current vault capabilities; scan/release/source-consumption/deletion/probe operations fail closed if their required adapter is missing. To run controlled engineering fixtures, construct `AgencyHost` programmatically with vetted server-owned adapters. Never load arbitrary callback code from request/configuration JSON. A local AES-GCM wrapper is not independent KMS custody. Quarantined files cannot become projection/reference/event sources.

## Shared transaction boundaries

All modules use the same SQLite database as the case registry. A request-scoped current authority pins the identity and reauthenticates inside consuming service transactions. Vault source gates recheck exact object/revision/hash, scope and source lifecycle on that transaction. Collaboration separately checks recipient, author/reviewer, source/case revision and the current disclosure grant. The client reader's live identity is never replaced by the stored reviewer's identity. Expert views deliberately expose bounded metadata, not an unrestricted whole-case/source download.

Explicit source processing review is distinct from READ, INFER and current processing policy. Event source IDs must identify the exact released vault object, source version and original UTF-8 hash. `with host.as_current(live_authority): host.events.process(...)` is a server-only, single-invocation worker seam. The resolver must reauthenticate the real current worker principal, not return a captured identity. There is no HTTP provider-execution route. No background loop, retry or automatic external send is started. Cancellation/logout/source-review or policy revocation after claim forbids publication and another paid call. Cancellation cannot recall an already-sent request.

## Usable controls and limits

The desk mounts the lane vault, collaboration, client-projection and knowledge components, explicit incoming/review/attempt/cancel forms, scoped operations and four pinned fictional read-only domain packs. Exact version-bound JSON forms are engineering controls, not polished production authoring. Knowledge drafts can be inspected by exact ID; unreviewed precedents do not appear in search. Search absence is not a global negative. Event attempts link to the existing source/result/Studio review page with `session=1`; opening it is explicit and the API still checks current authority. Bearer review links retain their original behavior. Hidden/locked/changed/revoked private views are cleared; the original CSP remains unchanged.

Domain-pack previews cannot overlay an arbitrary live graph; only an exact matching catalogue, current scoped snapshot, content pin and revision can calculate. The fixture catalogue lives in this source checkout, not a released package product. ENDSTATE's wheel contains nested pure kernel packages, not the agency host.

## Verification boundary

`tests/test_agency_host.py` covers real shared service/HTTP boundaries, body limits, current-session rechecks, scope denial, exact client projections and post-claim worker invalidation. `tests/browser_agency.py` uses actual loopback TLS requests with seeded fictional durable sessions and a controlled scanner. It intercepts no routes. This is not real IdP acceptance, malware efficacy, live model inference, independent security, human accessibility, legal advice, operator-value evaluation or a real client pilot. Existing software and external acceptance gates stay distinct.
