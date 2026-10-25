# Collaboration session receipt — 2026-10-25 — 7e526575ef714b7e8a85f6ef00ee7ca6

## Reproducible checkpoint

- Session/environment: Devin on Linux; Python 3.12.13 `.venv`, Node 24.19.0
  explicitly prefixed from `/home/ubuntu/.nvm/versions/node/v24.19.0/bin`.
- Task/objective: B03-03 engineering portion — revocable expert matter/object
  grants and separately reviewed client projections; no internal default view.
- Branch: `devin/1792969169-roadmap-collaboration`.
- Base/partition: `56c9b79428a612dff11e2fae0219640d156032ff`.
- Source baseline underneath partition: `baca8ad9efa531e5f172058845852963d7d5234a`.
- Implementation checkpoint: the commit containing this initial receipt; its
  exact hash is returned in the final handoff, not fabricated self-referentially.
- Changes: collaboration contracts/service, projection service, agency-only
  registerable API, isolated management/client browser mounts/CSS, controlled
  SQLite/API regressions, feature documentation and lane-local delivery proposals.
- Current delivery state at this checkpoint: local unreleased implementation;
  commit/push and independent native regression result to be appended below.
- No PR/main merge, release, tag, deployment, independent review, external send,
  live inference, model weights, real-client data or provider credentials used.
- Canonical tracking/task status: unchanged by lane ownership. This receipt and
  fragments are proposals for central reconciliation, not a parallel status
  ledger or a verified B03-03 claim. B03-01/B03-02 integration remains required.

## Verification before native checkpoint

Commands run from repository root; `.venv/bin/python` is Python 3.12.13.

| Command | Observed result |
| --- | --- |
| `.venv/bin/python -m pytest -q tests/test_authorisation.py tests/test_agency_access.py` | 35 passed (existing identity/access regressions) |
| `.venv/bin/python -m pytest -q tests/test_collaboration.py tests/test_collaboration_api.py tests/test_projection.py` | 36 passed, 1 pre-existing Starlette/AnyIO deprecation warning |
| Same focused command after public-route anti-enumeration regression | 37 passed, 1 warning in 0.87s |
| `.venv/bin/python -m compileall -q eightball` | passed |
| `/home/ubuntu/.nvm/versions/node/v24.19.0/bin/node --check web/v2/collaboration-view.js` | passed |
| `.venv/bin/python -m playwright install chromium` | explicit Chromium/headless shell/ffmpeg installation succeeded; no model download |
| `.venv/bin/python -m pytest -q` (without Node PATH) | 96 failed, 1296 passed, 1 warning in 62.19s; every observed failure was Node-not-found in existing JS regression harnesses; corrected PATH used for next run |
| `PATH=/home/ubuntu/.nvm/versions/node/v24.19.0/bin:/home/ubuntu/repos/8ball/.venv/bin:$PATH .venv/bin/python -m pytest -q` | 1392 passed, 1 warning in 62.92s on pre-anti-enumeration checkpoint; final native run rechecks latest source |
| Node 24 `--check` on `web/app.js` and all `web/v2/*.js` | 19 modules passed |
| delivery/emergence `--write` + `--check`, emergence `--base 56c9b79...` | passed; generated files unchanged |
| changelog `--write` then `--check --base 56c9b79...` | generation passed, base guard failed: Changed build needs a new changelog entry; expected frozen canonical tracking integration gate, not waived |
| Proposed combined emergence/changelog schema + base-preservation validation in temporary copy | 4 findings + 1 entry valid, no canonical bytes changed |

Retained implementation/test failures (not erased by later passes): first new
suite had two duplicate-keyword errors in test helper overrides (`id`,
`recipient`); corrected via dictionary merge. Added source-gate/cancellation
tests then had a missing `record` helper argument and a query for nonexistent
audit column `kind`; corrected to draft/review setup and JSON record parsing.
One tail assertion was initially attached to the cancellation test instead of
the source-retraction test; rerun stopped after 35 passed with the deliberately
injected KeyboardInterrupt; assertion moved back and all 36 passed. These were
test-writing defects, not deployed incidents. A rejected read-only `git config`
probe was not retried; inspected hook directory instead (sample hooks only).

The in-process API fixtures explicitly inject fictional identities; no claim of
OIDC/JWT/managed-vault security comes from them. They prove service behavior,
current controlled roles, tenant/matter/object scope, exact client allowlist,
local bearer denial, reviewer separation, stale hashes/revisions, revoked and
expired grants, source retraction, restart/idempotency, terminal withdrawal,
transaction/audit failure rollback and cancellation rollback. Source gate tests
check exact same transaction, schema/version/hash/scope and no client internal
source-read requirement. New UI has syntax checks, not native usability proof.

## Exact integration instructions

See `docs/v2/COLLABORATION.md` for signatures, nine exact routes/capabilities,
error mapping, migrations and two separate mount APIs. Required central work:

1. Same SQLite database for identity/case/vault/collaboration. Explicitly approve
   `initialize()`'s three new lane-only tables in shared migration/backup policy.
2. Supply `CurrentPolicy` using the agreed `AccessRegistry.require(...,db=db)`
   seam plus **server-owned** capability roles. For the requesting actor, use
   request-bound `request.state.agency_authority` / `CurrentAuthority` to
   reauthenticate current session/token on each invocation, not a cached
   Identity. Recheck stored reviewer durable authority without impersonating a
   new reviewer session. Generic READ/WRITE is insufficient for management,
   review or client disclosure. Collaboration grants supplement, not bypass,
   agency authority; no local operator bearer unlocks agency data.
3. Supply actual `CaseObjects` adapter: exact tenant/matter/object ownership,
   revisions and full selected-source inventory. Never silently omit a blocked
   source or replace an exact-object expert read with a whole-case dump.
4. Supply `VaultSources(vault)`. Vault author explicitly confirmed
   `require_source(db,identity=...,case_id=...,object_id=...,expected_revision=...,
   expected_sha256=...)`, schema 1/version 1, active same-vault-database
   transaction, current READ/source-reference checks, clean release/integrity
   and source_gate audit. Host uses BEGIN IMMEDIATE with no remote work after
   the final check. Missing/different DB/policy/scan/retention/quarantine/revoked
   access denies; gate audit rolls back with projection mutation/audit. Wrapper
   receives current actor on mutations/expert reads and still-current reviewer
   on client reads, without giving clients internal source authority. Returned
   handles are verified then discarded. Actual bytes need separate DOWNLOAD.
5. Register only in authenticated agency router with verified
   `request.state.agency_identity`, exact method/path operation mappings and
   explicit projection-only client policy. Unknown routes deny; inaccessible
   identifiers should deny uniformly before record lookup. Never map a blanket
   prefix to READ/WRITE or broaden client case/list/search/export access.
6. Attach existing 256 KiB `BoundedRequestBody` middleware and no-store handling
   for validation/unhandled errors. Keep existing CSP and CSRF/session boundary.
7. Add internal mount/navigation + CSP-safe stylesheet; separate client mount
   gets only exact projection context. Authenticated injected API throws on
   non-2xx. Call cleanup on navigation. Refresh host binding after revisions;
   unknown mutation outcomes require explicit refresh, never automatic retry.
8. Append lane fragment entries by ID centrally; retain all existing discoveries,
   append-only histories and changelog records. Add evidence only for actual
   combined checks, regenerate shared Markdown and run delivery/changelog/
   emergence validators and full integrated native/security regression. No
   task verified merely because these controlled components pass.

## Limitations / open gates

- Concrete identity/session policy, real case/source inventory, encrypted vault
  and default-deny shared router have not been combined in this lane.
- New mounts are opt-in and not added to shared navigation. No browser-driven
  new collaboration journey, assistive-tech, real participant or usability test.
- Lifecycle readiness is authoritative at server transaction time. Revocation
  cannot recall bytes returned previously; no push wipe or offline recall.
- Hashes are local integrity checks, not signatures/admin-tamper protection.
  One shared SQLite DB is required; multi-service distributed commit is not
  implemented. Host adapters are security-critical, not optional convenience.
- Curated content still needs competent independent human disclosure review;
  author-selected evidence-state labels do not attest facts or approve actions.
- Canonical status/changelog/emergence files are frozen to builders. Any
  changelog-base guard or native shipping-label failure is retained for central
  integration, never bypassed or represented as a lane-wide acceptance pass.

## Emergence Review — ER-01 through ER-15

**What did this sprint reveal that we had not properly seen, specified or
understood before we built it?** Disclosure is not just a redacted case view:
the review must bind recipient, immutable grant and source lifecycle, and remain
revocable without granting clients internal source rights.

| Prompt | Answer |
| --- | --- |
| ER-01 — discovery and evidence | EM-173..176 proposals: exact recipient/grant digest, same-transaction source gate, reviewer-authority lifecycle without client READ, and stale/removed object recovery. Controlled regression failures/negative tests and concrete vault/identity seam discussions made these boundaries explicit. |
| ER-02 — disconfirmation/missing evidence | Actual host role mapping or cross-database deployment could invalidate the assumptions; no combined tenant infrastructure, participant or independent reviewer evidence exists. Tests do not disprove malicious host adapters. |
| ER-03 — connected dependencies | Client disclosure depends on current client/grant, still-current independent reviewer, exact case/object/source revision and clean source lifecycle; none implies action authority or external send. |
| ER-04 — next discriminating review | Prove the concrete agency/case/vault adapters in one transaction, including revoke-after-preview, stale/blocked source and client route isolation; then obtain independent disclosure/usability review. |
| ER-05 — requested target | Remains B03-03 revocable expert grants/separate projections. No replacement app, model or secure portal is claimed; no client target/course is rewritten. |
| ER-06 — staleness and reconsideration | Case/object/vault revision, expiry, source retraction/quarantine/retention, reviewer/client revocation and withdrawal deny subsequent access. Reconsider with a new exact reviewed projection, not silent refresh of approval. |
| ER-07 — product/disposition | Bounded 8BALL B03-03 existing-task refinements; no new required roadmap scope or ENDSTATE runtime dependency. EM-176 operator benefit remains a candidate, not a scope promotion. |
| ER-08 — not implemented | Deployed portal/session infrastructure, remote source policy, external delivery/recall, multi-DB transactions, native new-flow review and human acceptance remain out of lane. Owner can review/reopen the retained fragments and open gates. |
| ER-09 — actual results | 36 controlled regressions and compile/changed syntax pass. Full initial command failed only where Node was absent from PATH; exact total retained above. Independent native run and final documentation results appended after checkpoint, never inferred from parent/lane totals. |
| ER-10 — blind spots | Grant UX review burden, semantic leakage in curated text, browser memory/caching, compromised host adapters and external administrator tampering are not excluded by these tests. Record owner hypotheses as append-only discoveries/decisions, not fake accepted scope. |
| ER-11 — chosen course | No client course was supplied or selected here; local authorization/design work must not pick a case route. Reconsider disclosure after exact revised review; no automatic route switch/action approval. |
| ER-12 — coverage/limits | Only fictional SQLite records, in-process API identity injection and existing native regression app are covered. No real client sources, paid model calls, production directory or independent semantic review. Empty/bounded results are not global impossibility claims. |
| ER-13 — recovery/attribution | Original helper failures and missing Node PATH retained. Devin corrected deterministic test setup; no model output was repaired or counted as inference success. Refresh exact state after uncertain mutations, use fresh IDs/review when stale; never silently resend/retry. |
| ER-14 — recoverable source | Assigned branch from exact partition; implementation commit and later receipt-only commit returned in final handoff. Native artifacts bound to exact tested checkpoint, not later upstream/combined code. No merge/deploy claim at a missing evidence link. |
| ER-15 — measurable value | Hypothesis: exact scoped grants/digests and explicit refresh reduce misdirected disclosure and recovery work. Need measured reviewer time, correction frequency, wrong-recipient prevention and review burden in fictional usability studies before benefit claims. Test/screen counts are not customer value. |

## Native and final delivery appendix

Pending at the source checkpoint; append exact native and remote evidence after
the independently executed run. This preserves the prior local/pending state.
