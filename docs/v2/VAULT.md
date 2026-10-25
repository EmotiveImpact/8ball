# Immutable-original vault: isolated engineering seam

Scope: B03-02; implementation on the vault builder branch, not shared application wiring or agency-production acceptance. Only fictional material was tested. The local `/` and `/v2/` applications, existing Source Desk and alpha import/audit export format are unchanged.

## Construction and authority

`eightball.vault.service.Vault(path, *, authority, keys, scanner=None, deletion_guard=None, clock=..., minimum_retention=timedelta(days=7))` explicitly creates its five lane-local SQLite tables and immutability/audit triggers using `eightball/vault/schema.sql`. Importing the module does not migrate a database, start a daemon or scan storage. Integrators must review the migration and explicitly construct against their shared database; never point this automatically at an operator database.

Dependencies: `cryptography` AESGCM (already installed by current `PyJWT[crypto]` requirements), SQLite, existing Pydantic/identity records and FastAPI. Integration should make the crypto dependency direct and maintained in its manifest; this lane does not edit dependencies. No cryptographic algorithm was invented and no external service was called.

Authority protocol, in `eightball/vault/contracts.py`:

```python
require(db: sqlite3.Connection, *, identity: Identity, case_id: str,
        object_id: str | None, permission: VaultPermission,
        now: datetime) -> Resource
```

The trusted host supplies a verified `Identity`; it cannot come from an upload body or local operator bearer token. The authority must read **current** server-owned case bindings, grants, identity/session validity and policy on the supplied transaction and deny on missing scope/policy. This is not factual evidence, case/action approval or a reusable capability. The service rechecks authority at transaction end and audits before returning bytes or committing changes. `BEGIN IMMEDIATE` serializes writes/revocations on the same database; cross-database or cached grants do not provide this guarantee.

`RegistryAuthority(control=None)` adapts the existing `agency_case_scope`/`agency_grants` tables only. It does not configure OIDC or the identity lane's new session tables. Mapping:

| Vault permission | Existing operations | Extra transactional control |
| --- | --- | --- |
| upload | READ + WRITE | no |
| read / inventory / source handle | READ | no |
| download | READ + DOWNLOAD | no |
| scan / cancel scan | READ + WRITE | yes |
| hold / retention / delete | READ + WRITE | yes |
| audit | READ | yes |

Extra control callback: `control(db, identity, resource, vault_permission, now) -> bool`, requiring literal `True`. Missing callback denies. WRITE alone is never lawful-hold/deletion/scanning authority. Object-only grants cannot enumerate matter inventory/audits or read another object. Missing tables/adapters fail closed, not a local bearer fallback. Integration must implement session revocation/current policy using the identity lane contract or an injected Authority and extend negative route tests.

## Original, encryption and processing lifecycle

- Upload accepts **1–262,144 bytes**, exact valid UTF-8 `.txt`/`.md`, `text/plain` or `text/markdown`, no NUL/path/control-character filename. Capacity is 100 originals and 8 MiB per case, including tombstones. PDFs, archives, arbitrary binary files, external URLs and parsers are unsupported.
- Every upload gets a server-generated UUID-hex object ID and immutable original `version=1`; another upload is a new object, not an overwrite/deduplication. Descriptor records exact content SHA-256/size, case/org/matter binding, filename/type, upload time, representation `utf8-exact-v1` and immutable minimum retention deadline. BOM, Unicode, CRLF and lone-CR bytes are preserved.
- Each original uses fresh 256-bit content key, 12-byte nonce and AES-GCM; canonical immutable descriptor is associated data. An injected key wrapper encrypts the content key. On each read/source gate the vault authenticates ciphertext, descriptor binding, plaintext size and hash. SQL triggers prohibit descriptor update/delete and blob update. An administrator who controls the database/triggers is **outside** the local immutability threat boundary.
- `LocalKeyWrapper(keys: dict[str, bytes], *, active_key_id)` uses maintained AES-GCM for wrapping with explicit key IDs. Keys are injected and never stored in the database, generated on startup or logged. The host must retain/protect them across restart; lost keys make originals unavailable. This adapter is **not managed KMS**, key rotation, backup/recovery or proof of secure custody. Metadata, audit identifiers/timestamps and filenames are not encrypted by this content envelope; whole-storage protection remains an integration/security gate.
- Upload is `quarantined`; no automatic scan, inference, source attestation, fact extraction or external send occurs. Reads/downloads/source publication deny until `released`.
- `scanner.scan(content: bytes, *, sha256, media_type) -> ScanResult(verdict, engine, version, definitions, content_sha256)` runs **only** on explicit scan request. Host must supply a bounded trusted scanner with safe isolation/timeouts and separately approved local/external processing policy. No scanner is bundled. Missing scanner leaves quarantine and returns unavailable. Synthetic test scanners do not establish malware detection.
- Scan claim advances revision to `scanning`; the scanner runs outside the database lock. Publication rechecks current authority, exact scan attempt and vault revision in a fresh transaction. Only `clean` with matching hash and bounded engine/version/definitions releases. `infected` becomes `blocked`; exceptions/invalid/hash-mismatch results become `scan_failed` with a sanitized error. Revocation, cancellation or policy/revision changes prevent publication.
- Interrupted/revoked scans remain `scanning`, not auto-resumed. Explicit cancel sets `quarantined`; another explicit command may scan again. Cancellation forbids result publication but **cannot recall bytes already handed to the scanner**. Adapter must enforce resource limits; this service does not forcibly terminate an external scanner process.
- Command IDs (8–128 characters) are actor/case-bound idempotency keys. Same exact request returns current protected state without repeating work; key reuse for different request conflicts. An interrupted scan command never repeats automatically after restart or replay.

## Retention, holds and local deletion

Every change requires an exact `expected_revision`, command ID, current authority and a 10–1,000 character explicit human rationale (only rationale hash enters audit). Hold is an explicit boolean, never inferred. Retention may not precede immutable upload-time server minimum. Hold/retention changes advance mutable `vault_revision`, never immutable version/hash; earlier reviewed handles become stale.

Delete denies during a hold, before retention expiry, while scanning, or without `deletion_guard(db, safe_source_handle) is True`. The guard must check dependent Source Desk/projection/legal/retention references on the **same** transaction and fail closed if unknown. A fixture returning True is not production dependency clearance. On allowed deletion the local ciphertext row is removed and status becomes `deleted_local`; original descriptor/tombstone and audit remain. `PRAGMA secure_delete=ON` is set, but no filesystem, WAL, backup, replica, provider-retention, key-destruction or derived-copy erasure is claimed. Status exposes `deletion_scope=local_vault_ciphertext_only`. No purge scheduler or backup recovery is implemented.

## Source/provenance and collaboration adapters

```python
metadata(*, identity, case_id, object_id) -> dict
inventory(*, identity, case_id) -> list[dict]
source_handle(*, identity, case_id, object_id, expected_revision: int) -> dict
read_original(*, identity, case_id, object_id, expected_revision: int,
              expected_sha256: str) -> bytes
require_source(db, *, identity, case_id, object_id, expected_revision: int,
               expected_sha256: str) -> dict
```

`metadata` is authorized, content-free metadata but includes the filename; it is **not** safe to copy wholesale into a client projection. `source_handle` returns only `schema_version`, `object_id`, immutable `version`, `case_id`, `organisation_id`, `matter_id`, `sha256`, `size_bytes`, `media_type`, `representation` and `vault_revision`; no filename/path/text/key/token. It requires current READ, exact revision, clean released scan and available authenticated ciphertext. Handles do **not** authorize later access. `read_original` also requires READ + DOWNLOAD and matching reviewed SHA-256; returned bytes are exact, not normalized or factual assertions.

`require_source` is the collaboration **final commit/publish gate**, not an alternative bearer token. The caller MUST:

1. Use a connection whose main database resolves to the same Vault path, begin `BEGIN IMMEDIATE`, and authorize its own current mutation/publish operation.
2. Call `require_source` on **that connection**, as the final source check immediately before publication/commit, with the exact reviewed vault revision and SHA-256 for every source. Do not await/external-call or write source policy after this gate.
3. Commit its mutation/projection/audit on this same connection; rollback on any error. This source gate adds a `source_gate` audit that rolls back with the caller mutation. The caller owns denial audit and its final session/operation checks.

The method rejects no transaction/different database/revoked/cross-scope with PermissionError, stale revision/hash/quarantine/blocked/deleted with Conflict, missing/corrupt/unavailable ciphertext/key with IntegrityError. It verifies clean scan/hash and authenticates encrypted bytes without returning them. It does not begin/commit a transaction or bless a future transaction. `db.in_transaction` alone cannot prove the caller chose IMMEDIATE; the integrator must enforce that transaction mode. Independent database snapshots/caches or separate-connection metadata prechecks are **not atomic revocation**.

`eightball.vault.sources.exact_text(...)` composes authorized handle + bytes into exact decoded text and sets `fact_verified=False`. Integration must map versioned Source Desk IDs/excerpts and retraction/deletion clearance without rewriting source offsets or treating clean scanning as evidential support. No shared Source Desk persistence is wired by this lane.

## Audited access

Authorized metadata/inventory/download/source and control operations are recorded; permission/operation failures inside service transactions append denied/rejected records after rolling back changes. Body/encoding validation failures before a service transaction require host security logging; they are not asserted present in the vault audit. Actor identity is hashed, original body and filename are excluded, rationale is hashed. Safe details include version/hash/scan disposition. Append-only triggers and local previous-hash/record-hash chain detect ordinary tampering; `audit` verifies the entire local chain before returning a bounded case-only page. It exposes `verified_local_chain=True`, `independently_anchored=False`; database-root rewrite/truncation and independent custody are not solved. Audit insertion failure rolls back writes and command receipt rather than releasing unaudited bytes. Production volume/partitioning is unmeasured.

## API integration

Call `eightball.v2.vault_api.register_vault_routes(router, service)` once under `/api/v2` and the host's verified agency-identity middleware. Actor comes only from `request.state.agency_identity`. Local operator auth must never mount/reach these agency routes. Integration must add explicit operation/matter route mappings; unknown agency routes must deny. Routes are relative:

| Method | Route suffix under `/cases/{case_id}/vault` | Policy |
| --- | --- | --- |
| GET / POST | empty | inventory / upload |
| GET | `/audit?after=0&limit=100` | audit (bounded limit <= 200) |
| GET | `/{object_id}` | metadata |
| POST | `/{object_id}/download` | exact revision + SHA-256, READ/DOWNLOAD |
| POST | `/{object_id}/scan` | explicit scanner control |
| POST | `/{object_id}/cancel-scan` | control + rationale |
| POST | `/{object_id}/hold` | control + rationale + explicit boolean |
| POST | `/{object_id}/retention` | control + rationale + aware `retain_until` |
| POST | `/{object_id}/delete-local` | control + rationale + guard |

Upload body: base64 bytes, filename, media_type, aware retain_until and command_id; bounded streamed JSON (400,000 bytes; other bodies 8,192). Strict schemas reject injected identity/scan decisions/unknown fields. The scanner runs off the ASGI event loop. Protected successful JSON/download responses set no-store/private and nosniff; downloads force attachment/octet-stream. Host should apply no-store to error responses too. 403 denies scope; 409 rejects stale/policy/state conflicts; 422 invalid body; 413 oversize; 503 unavailable/integrity/scanner. No signed links/cookies/provider configuration are added here.

## Isolated UI mount (not browser-accepted)

Load `web/v2/vault-panel.css` explicitly and import `mountVault` from `vault-panel.js`. Call `mountVault(root, {caseId, request})`, then call returned `.dispose()` on logout/case change/navigation; `.refresh()` explicitly reloads. No shared index/router/nav/style file is edited. Host request contract:

- `request(path)` returns parsed GET JSON.
- `request(path, {method:'POST', body})` JSON-encodes body with host-verified agency credentials and returns parsed JSON, throwing on non-2xx.
- `request(path, {method:'POST', body, responseType:'blob'})` returns Blob for successful attachment download and throws on non-2xx.
- Host must clear/dispose immediately on revoked/changed session; do not silently retry or persist credentials in this panel.

The panel supports upload, explicit scan/cancel, retention/hold, guarded local deletion and attachment download. It shows hash, original version vs vault revision, quarantine/deletion scope explanations and uncertain-command recovery. Untrusted filenames use textContent, not HTML. Generation/disposal guards drop late responses, failed/unknown mutations clear object displays and disable more mutations until explicit refresh; there are no background polls/retries. Server checks remain authoritative; visible buttons do not imply permission. UI syntax is checked; no native/browser/accessibility or operator-value claim is made for this unmounted module.

## Integration acceptance still required

Review migrations/permissions/key custody; implement current session authority and separate controls; configure/test a real bounded scanner; connect Source Desk and collaboration final same-transaction gates/deletion clearance; explicitly mount routes/UI without any local bearer bypass; test cross-lane revocation after preview and scan claim, stale projection, cross-tenant/object IDs, missing policy/scanner/keys and unknown routes. Run source-bound integrated native acceptance, production security and independent operator/legal/retention/recovery review. Do not mark all B03-02 verified from these component tests or remove its B03-01 prerequisite. No main merge, PR change, release, deployment, real-client pilot, inference, model download or external send is implied.
