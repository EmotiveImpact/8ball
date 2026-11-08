# Operations engineering toolkit

Scope: fictional, offline rehearsals and an **unmounted** agency operations service.
8BALL remains the fixer product. ENDSTATE calculations do not import this package.
These tools do not authorise deployment, real-client use, a real pilot or external sends.
See `docs/v2/PRODUCTION-SECURITY.md` and the source-bound lane receipt for remaining gates.

## Integration contract

1. Integrator explicitly reviews `eightball.operations.journal.SCHEMA` and calls
   `initialize(selected_path)` in a controlled migration. Constructors/imports do not
   provision tables or start a worker. Tables are separate from original case history.
2. Instantiate `Operations(path, authority=authority, probe=probe, clock=aware_clock)`.
   Use the **same database and transaction** as current grants, or supply a separately
   reviewed equivalent transaction boundary. An in-memory/cached permit is insufficient.
3. `authority(db, identity, scope, operation, now)` must return exactly `True` only
   for a freshly verified agency identity and exact organisation/matter/case plus operation.
   Supported operations: `operations.read`, `operations.open`, `operations.transition`,
   `operations.verify_revocation`. Do not map unknown operations to a permissive default.
   The service calls authority inside `BEGIN IMMEDIATE` and again before commit.
   Read denial, adapter exception or post-command revocation rolls everything back.
4. `probe(db, scope, target_id, surface)` returns only `denied`, `access_still_allowed`,
   or `unavailable`. Six surfaces are checked: API, database, object links, search,
   model cache and workers. Resolve targets server-side under that exact scope;
   a caller-supplied handle must not enumerate another matter. Exceptions roll back.
   Missing probes record unavailable, never success. Probes must not send, retry,
   restore, mutate cases or make paid calls. Remote-surface truth cannot be made atomic
   by a SQLite transaction: a host must review leases, consistency and race guarantees.
5. `register_operations_routes(router, service)` registers relative
   `/organisations/{organisation_id}/matters/{matter_id}/cases/{case_id}/operations`
   routes. Mount the router behind the real agency identity dependency, populating
   `request.state.agency_identity`. **Never synthesize this from the local bearer.**
   Retain the host's explicit route-operation mapping, generic validation/error handling,
   confidential-log redaction, rate limits and request-size limits. The route requires
   an identity but service-level transaction checks remain mandatory.
6. Run cross-lane revoke/expiry, unknown-route, cross-object/matter/tenant and
   revoke-after-preview/claim negative tests before advertising the feature.
   This lane does not modify shared routers, dependencies or the acceptance runner.

Existing dependencies suffice: Python 3.12+, SQLite, FastAPI/Pydantic and the maintained
`cryptography` Ed25519 primitives already installed by `PyJWT[crypto]`. Do not create
a new cryptographic scheme or treat a local private key as managed custody.

## Incident and revocation workflow

An authorised operator opens `incident`, `pilot_finding` or `revocation` with an opaque
request ID, constrained category/severity and optional evidence digest. Only revocation
records have a required target handle. No raw source, narrative, client name or token
field is stored. Keep full reports in separately authorised evidence storage.

Use exact `expected_revision` and unique request IDs for transitions:
`open -> investigating -> contained -> resolved -> closed`. Cancellation is allowed
from open/investigating and is terminal. Containment, resolution and closure require
an evidence SHA-256 reference, not an invented reviewer approval. Revocation closure
reruns every probe and requires all six denied. Historical denied results cannot close
newly accessible data. A probe observation is not itself an access revocation command.

Idempotent replay returns the original verified journal receipt only while current
authority remains valid; changing request content under the same key conflicts.
Restart does not repeat a probe or revive a cancelled workflow. The hash-linked journal
detects inconsistent records/receipts; an administrator who rewrites all tables is not
defeated without independent external anchoring.

## Audit checkpoint and recovery rehearsal

An authorised host obtains `store.audit(case_id)` with valid original replay/lineage.
Call `sign_checkpoint(audit, scope, expected_revision=revision, private_key=key,
now=aware_now)` only after verifying the ownership mapping and revision. This offline
function cannot establish agency authority from a local case snapshot. It signs the
exact audit digest, head, revision, scope and capture time using Ed25519. Keep the
trusted public key/checkpoint copy independently from the database and verify custody
out of band. Key rotation, revocation and external anchor services remain unimplemented.

For a **disposable fictional database only**:

```sh
python scripts/operations/rehearse.py --fictional-only \
  --source selected-fictional.sqlite --sandbox new-private-sandbox.sqlite \
  --checkpoints signed-checkpoints.json --trusted-public-key trusted-public.pem \
  --maximum-age-seconds 3600 --rto-seconds 60
```

The source is opened read-only; SQLite backup copies it into a new 0600 file with
exclusive creation. Existing files/symlinks cannot be overwritten. Integrity/reference
checks and original audit validators run against explicitly supplied checkpoints,
including embedded alpha import lineage. Source data is not restored in place.

**Whole database copy:** organisation/matter labels on a checkpoint do not filter
the backup. Never expose this as a scoped agency HTTP operation or point it at live
client data. No database discovery, encryption, retention/deletion, remote storage,
managed recovery or production RTO/RPO claim exists. `rpo_seconds_observed` is checkpoint
age, explicitly not measured replication lag. The RTO budget is local elapsed time.
Cancellation/failure preserves the private sandbox; inspect it deliberately and start
a new explicit destination. Never automatically retry or overwrite the failed evidence.

## Readiness evidence and commercial onboarding

`ReadinessManifest` requires an exact 40-character source commit, declared supported
environments and evidence objects. Each evidence object has unique ID, capability,
environment, kind, status, relative artifact path, SHA-256, source commit and aware
recorded time. Use `Evidence.model_json_schema()` for the machine contract. No hidden
file scan occurs: only explicitly supplied, bounded artifacts under `--root` are read.

```sh
python scripts/operations/check.py readiness manifest.json --root evidence-root
python scripts/operations/check.py pilot fictional-pilot.json
```

Exit 1 means blocked; 2 means invalid input. Exit 0 means artifacts were supplied
consistently or fictional observations recorded, **never release permission**. Evidence
must be passed, fresh (30 days by default), digest-matching and source-bound. Every
capability/environment needs the required software/human/owner/legal/independent kinds.
Copies of a claimed legal decision do not authenticate that decision. All supplied
evidence still reports `human_decisions_authenticated: false`, release/deploy/real-pilot
authorization false and `evidence_supplied_pending_authentication` rather than ready.

Onboarding rehearsal procedure (fictional only):

1. Owner declares a supported environment, accepted capability list and named access,
   support, retention, model-processing and operating responsibilities outside this tool.
2. Run the native existing local onboarding and case/export journeys. Review identity,
   scope, evidence and provider permissions independently; do not reuse a component pass
   as production identity/storage evidence.
3. Obtain actual reviewed service terms, brand/licence clearance and operating ownership
   from authorised humans. Do not draft acceptance signatures or infer them from files.
4. Build the artifact manifest with original receipts; preserve failed/blocked/unknown
   statuses. Run readiness. Resolve missing software evidence by testing, not by relabeling
   human/independent evidence as software, or vice versa.
5. Only the authorised owner can decide commercial scope after upstream pilot and
   production gates. No readiness CLI or fixture can make that decision.

## Support triage and monitoring

Support intake uses constrained incident categories and opaque evidence digests.
Obtain permission before collecting any diagnostic artifact. Never request a raw
client database, source, credential or model trace in a public issue or ordinary log.
Verify access scope and affected source revision before investigating. Contain via
the separately authorised host control, then attach its evidence digest; creating an
operations record does not revoke credentials, stop providers or cancel external work.
Use explicit current probes before closing access incidents. Escalate critical/high
findings to the independently named operating/security owner, not an invented default.

The read projection supplies sequence/head, open states and per-surface observations
for an authorised host to aggregate. Monitoring infrastructure, notifications, on-call
ownership, numeric SLOs and real incident response are external unaccepted gates. Do
not publish client-scoped metrics or start a daemon from this package.

## Fictional pilot protocol

`FictionalPilot` requires `fictional: true`, unique `fictional-*` participant handles
and uniquely identified observations. Each participant needs usefulness, safety,
corrections and confidentiality observations. Preserve pass/fail/unknown, severity,
correction counts, optional observed decision seconds and optional resolution digest.
Missing/failed/unknown observations block. Critical/high failed observations without
a resolution digest are explicit blockers. Supplying a digest never erases the original
failure or constitutes authenticated closure; an explicit later protocol/retest is needed.

Use these fictional observations to rehearse review burden and correction timing, not
as measured operator benefit or qualified-fixer/customer acceptance. Real recruitment,
consent, confidentiality, critical-finding closure review and pilot authorisation are
external. No real participant or personal data is permitted by this engineering scope.
