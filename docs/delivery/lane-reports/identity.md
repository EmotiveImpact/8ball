# Identity lane receipt — 2026-10-25 / d9478f50b2b844fcb292873f9d406d3d

## Scope and recoverable source

- Task: B03-01, bounded engineering-only identity/current-authority component. This receipt is not a second task-status ledger or production acceptance.
- Assigned branch: `devin/1792969169-roadmap-identity`.
- Actual starting partition commit: `56c9b79428a612dff11e2fae0219640d156032ff`; runtime baseline: `baca8ad9efa531e5f172058845852963d7d5234a`.
- Session: https://app.devin.ai/sessions/d9478f50b2b844fcb292873f9d406d3d .
- The containing implementation commit supplies the recoverable source. A commit cannot contain its own final hash; the final handoff provides the exact pushed hash. Any later receipt-only commit must not be confused with the tested source manifest.
- At this initial receipt checkpoint implementation and records are uncommitted/unpushed. Final verification/push evidence is appended below after execution. No PR, merge, deployment, release, real-client pilot, live inference, provider login or independent sign-off is authorized/performed.

## Changed paths and actual behavior

- `eightball/agency_access.py`: same-database current-grant `require`/`transaction`; all-operation/object isolation; stale-WAL writer reservation; reauthenticated identity pinned for the consuming transaction; optional durable cookie sessions and exact mutation Origin checks. Existing bearer route map and `allowed` hook remain compatible.
- `eightball/authorisation.py`: accurate boundary wording; existing Identity/Resource/Operation/Grant policy retained.
- `eightball/oidc/__init__.py`, `eightball/oidc/login.py`: pinned public-client authorization-code/S256-PKCE login, nonce/state/browser binding, one-use attempts, bounded no-retry token adapter, RS256/kid/issuer/audience/time/azp/ACR checks, durable hashed opaque sessions, cancellation/expiry/logout/session revocation.
- `eightball/v2/identity_api.py`: opt-in separate router registration for prepare/callback/session/logout with Secure/HttpOnly/SameSite/__Host cookies; provider errors are redacted and success is no-store/no-referrer.
- `web/v2/identity-access.js`: isolated `mountIdentity(container, {apiBase})` with explicit external continuation, no JS token persistence, disposal abort and truthful sign-in/permission/provider-logout distinctions.
- `tests/test_identity_authority.py`, `tests/test_identity_api.py`, `tests/test_oidc_login.py`: fictional/offline transaction, HTTP and protocol regressions. No shared app routes or live model are substituted by the isolated HTTP operation harness.
- `docs/v2/AGENCY-ACCESS.md`: exact adapter, route, schema, operation and host migration contract.
- This receipt plus `identity-emergence.json` and `identity-changelog.json`: central-integration proposals only. Canonical tracking/generated files remain unchanged per ROADMAP-LANES ownership.

## Task-by-task evidence (B03-01 only)

The focused suite covers all six existing operations (READ, WRITE, EXPORT, SEARCH, INFER, DOWNLOAD), authenticated same-scope success, other-tenant/matter/identity denial, object-only vs aggregate isolation, missing/malformed scopes, expired/future/revoked authority, durable session expiry/logout, mixed bearer/cookie fail-closed behavior, and Origin checks. It also covers rollback/storage failure/stale case revision, stale WAL snapshots, revocation between preflight and consume, changed authenticated identity even when both principals have grants, restart/one-use login, cancellation after exchange, and no exchange retry.

This proves a bounded authorization service/route contract, not mounted product search/export/inference operations, worker/vault policy integration, actual inference, native identity UI behavior, managed production storage, MFA, independent security review or end-to-end multi-tenant deployment. B03-01 must not be marked broadly verified from these tests. The local/manual application and original source/audit import remain unchanged.

## Verification and preserved failures

Environment: Python 3.12.13; Node 24.19.0 from nvm. Prefix both interpreters on PATH. Existing requirements-dev installed; setuptools was absent from this Python and `python -m pip install 'setuptools>=82'` installed 84.2.1, as required by docs/endstate/PACKAGE.md. No dependency manifest changed. Existing browser executable: `/home/ubuntu/.local/bin/google-chrome`; native tests use fictional disposable DBs and controlled loopback fixtures, not a real provider.

Executed before the final consolidated rerun:

| Check | Actual result and scope |
| --- | --- |
| Focused pytest after all identity stability hardening | `python -m pytest -q tests/test_authorisation.py tests/test_agency_access.py tests/test_identity_authority.py tests/test_identity_api.py tests/test_oidc_login.py`: **101 passed, 1 existing Starlette/AnyIO deprecation warning**, 8.68s. |
| Earlier full suite before final two identity-stability tests | **1420 passed, 1 warning**, 73.33s after exposing nvm Node on PATH. This is not the final source total. |
| Initial full suite without Node on PATH | **1324 passed, 96 failed, 1 warning**. Existing Node-backed tests could not find `node` (FileNotFoundError / graph validation assertion); rerunning with documented nvm PATH resolved these failures. |
| Initial implementation compatibility experiment | Two existing agency reviewed-event revocation-hook tests failed when the guard bypassed `registry.allowed`. Restoring the hook while retaining transaction checks fixed both; their failures were not accepted as a new contract. |
| Initial Python environment | Python 3.12 lacked pytest. Installing existing requirements-dev resolved this; no new package manifest was introduced. |
| Native attempt `20261025T232802Z-a6ed6c15` | Overall **failed**, source SHA-256 `20edca1da916a6eb58c19c866a6aa0cdbfb8cc1d29fed7e00382036ab70e7aa5`, source stable during run; source/artifact inspection was valid immediately afterward, before later hardening/docs edits. Unit/compile/delivery/changelog/emergence/JS/structural/schema checks passed. Package failed because setuptools.build_meta was unavailable. Studio failed its frozen line-149 “local unreleased” assertion while the frozen top changelog truthfully says pushed_unreleased. Other eleven native suites passed. It did NOT establish all-native verification. Raw report retained at `artifacts/acceptance/20261025T232802Z-a6ed6c15/report.json` on the builder VM. |
| Initial base changelog check | `scripts/changelog.py --check --base 56c9b79428a612dff11e2fae0219640d156032ff` failed: “Changed build needs a new changelog entry.” Builders cannot write frozen canonical files. This lane supplies a mergeable fragment instead; integrator must append it centrally and rerun. |
| Canonical checks without base | Delivery valid (71 tasks / 11 milestones); changelog valid (58 existing entries); emergence valid (113 existing discoveries). These validate the frozen partition, not adoption of lane proposals. |
| Final consolidated run | Outstanding at the initial receipt checkpoint; actual results and exact tested source are appended, not guessed. |

The first native run was deliberately not represented as green. The Studio failure is outside owned runtime/test paths; do not weaken the test or change truthful shipping state merely to get a builder pass. The integrator must reconcile it explicitly and rerun. Missing setuptools has been repaired, not relabelled as a product defect. No configured lint/type-check tool exists in the dependency manifests; pytest, compilation, Node syntax and repository structural validators are the available checks.

## Exact integration contract and next commands

1. Fetch this assigned branch; integrate its implementation commits on the central integration branch only. Do not merge main or another lane from a builder. Preserve newer upstream `2b1b465ebfa1b433c8f128b0478f6806dce9e2e7` documentation/evidence additively without attaching its tests to this runtime.
2. `AccessRegistry.require(identity, case_id, operations: tuple[Operation,...], *, object_ids: tuple[str,...]=(), db=None) -> Resource`; `transaction(identity, case_id, operations, *, object_ids=())` yields `(db,scope)`. A supplied db must be the same active main-database transaction. Checks require ALL operations against ALL listed objects; no object list means aggregate matter authority. Missing/malformed grants deny. Errors are never authorization success.
3. `CurrentAuthority(registry, current_identity: Callable[[],Identity])` exposes `require(case_id, operations, *, object_ids=(), db=None)` and `transaction(case_id, operations, *, object_ids=())`. The callback reauthenticates on every call, never caches an Identity. Transactions pin one identity throughout. AgencyAccess attaches it as `request.state.agency_authority`.
4. Host consumes server-owned case/object references, checks their existence/ownership, expected revision and reviewed projection digest in the same transaction as authority and mutation/publication. Vault quarantine/scan/retention/processing/egress and action permissions are additional mandatory adapters. Missing adapters fail closed; no local-token fallback. Preflight is not a capability. Never hold the DB lock across a provider request: check before dispatch and recheck at publication.
5. Explicitly construct `OIDCConfig`, `LoginService(path, config, TokenEndpoint(config))` only with reviewed pinned provider configuration, and pass `sessions=service` to the opt-in guard. This lane does not configure a provider. Current API bearer verification and OIDC browser ID-token client audiences are distinct.
6. Mount `register_identity_routes(router, service)` on a separate same-origin `APIRouter(prefix='/api/v2')`, not the protected agency router. Relative routes: POST /identity/login (prepare), GET /identity/callback, GET /identity/session, POST /identity/logout. Callback redirects only to /v2/. Cookie mutation Origin must equal the configured redirect origin. Preserve secure cookies/CSP; do not weaken for local HTTP.
7. Constructors propose only `agency_login_attempt` and `agency_browser_session` opt-in tables. Existing agency registry schema is retained. Review backup/migration policy before construction on any operator DB; this lane touched only test/disposable DBs. Existing PyJWT[crypto]/cryptography/httpx dependencies suffice.
8. Integration owns protected route/method -> Operation mappings, actor-bound commands, worker identity/policy adapters, router attachment and UI navigation. Existing mapped reads/export/event-review/outbox remain; unknown routes and global lists/search/infer still deny. Optional UI: `mountIdentity(container, {apiBase:'/api/v2'})`, disposal returned by mount. No new native identity UI pass claimed.
9. Merge `identity-emergence.json.items` by unique EM-133..EM-140; preserve all old items/history. Append `identity-changelog.json.entries` by ID/newest-first. Update only B03-01 and unique EV evidence centrally on actual combined proof, retaining earlier evidence/blockers. No blanket verified state is proposed. Regenerate emergence/delivery/changelog with their normal --write commands then --check --base against central starting commit.
10. Reconcile Studio's frozen shipping-state assertion truthfully, then run full new-source native acceptance with Node/Python on PATH and inspect its report. Add cross-lane negatives: local operator token never accesses agency data; unknown route denies; cross-case/object IDs do not leak; revoke/expire after preview/claim denies commit/publish/download; missing vault/source policy denies; stale projection/revision and cancellation deny publication/retry.

Copyable builder verification command (no live provider):
```sh
PATH="/home/ubuntu/.pyenv/versions/3.12.13/bin:/home/ubuntu/.nvm/versions/node/v24.19.0/bin:$PATH" EIGHTBALL_BROWSER="/home/ubuntu/.local/bin/google-chrome" python scripts/acceptance.py --mode native --base 56c9b79428a612dff11e2fae0219640d156032ff
```
This builder command is expected to retain the canonical-changelog/Studio failures until central reconciliation, not bypass them. The final run report records what actually happened.

## Emergence Review

**What did this sprint reveal that we had not properly seen, specified or understood before we built it?**

An authenticated route is only an entry check: object/operation coverage, current grants, authenticated-principal continuity and a live consuming transaction are separate requirements. SQLite WAL snapshots can retain old grants unless the checker obtains a current writer reservation. Identity may change to another equally permitted principal mid-transaction; authority alone would not preserve actor attribution. A provider exchange has a cancellation boundary after outbound dispatch too: one-use state and publication rechecks avoid retries or sessions published after cancellation. Local logout and provider-account revocation are not interchangeable.

| ID | Classification / evidence | Disposition and operator implication |
| --- | --- | --- |
| EM-133 | existing_task / supported_by_tests | Adopt bounded B03-01 object/aggregate/all-operation checks; missing object ownership/policy adapter still denies. |
| EM-134 | existing_task / supported_by_tests | Adopt stale-WAL fail-closed writer reservation; database contention may deny availability, not silently allow old grants. |
| EM-135 | existing_task / supported_by_tests | Adopt stable authenticated principal for transaction/actor lineage, even if another principal also holds grants. |
| EM-136 | existing_task / supported_by_tests | Adopt one-use attempts and cancellation/expiry recheck after exchange; failed/uncertain exchange needs explicit new login, not retry. |
| EM-137 | decision_record / supported_by_tests | Preserve local session logout vs provider termination/account/grant withdrawal as distinct operations and truthful UI wording. |
| EM-138 | existing_task / observed_in_build | Defer live-provider/MFA/key custody/PostgreSQL/independent review acceptance to its actual external gates; fixtures do not complete production identity. |
| EM-139 | new_candidate / operator_hypothesis | Retain explicit expired-unused-attempt cleanup/account-session administration as bounded host work; no hidden background scans or new required task. |
| EM-140 | decision_record / observed_in_build | Retain frozen shipping-state/test discrepancy as failed evidence for central reconciliation, not a builder authority to rewrite canonical shipping history. |

All findings use reserved IDs; remaining EM-141..EM-152 are unused gaps, not discoveries. Owner review remains pending. All implementation belongs to 8BALL host identity, not the reusable ENDSTATE calculation kernel. No model runtime/research adoption or new industry app is introduced.

## ER-01..15 review prompts and answers

- **ER-01 — What did we discover that was not explicit before, and what exact evidence made it visible?** EM-133..EM-140 above; especially stale-WAL and two-allowed-principals transaction counterexamples demonstrated by focused tests. Token exchange cancellation and persisted used-state tests expose the publication boundary.
- **ER-02 — What could disprove the finding, and what conflicting or missing evidence have we considered?** Different DB isolation/adapters can change locking behavior; no PostgreSQL/provider deployment was tested. The tests prove this local seam only. Successful fixture claims cannot disprove missing MFA/provider custody gates.
- **ER-03 — Which declared dependencies, actors, decisions or sources connect apparently separate candidate routes?** Identity/current grants are shared by vault, collaboration, events and intelligence, but their ownership/policy/revision/action checks remain separate. No client situation or candidate course was supplied in this lane.
- **ER-04 — Which verification question or review could most change our available options?** Verify every integrated consuming adapter reauthenticates/rechecks exact objects and reviewed revisions at commit. Then configured-provider/MFA and independent security review determine production feasibility.
- **ER-05 — Are we still working towards the client's explicit target and success criteria?** Yes: bounded B03-01 engineering under the existing fixer roadmap, not a replacement app, automatic action execution or production launch.
- **ER-06 — What may be stale, what could follow from our actions, and what event should make us reconsider?** Grants, sessions, provider keys, projections and case revisions can stale independently. Expiry/revocation/cancellation/identity changes deny publication. Key rotation, migration or a new deployment must trigger explicit reevaluation.
- **ER-07 — Which findings belong in 8BALL, ENDSTATE, an existing task, or a retained future candidate?** All identity changes belong in the 8BALL host/B03-01. ENDSTATE has no service imports added. EM-139 remains a candidate, not silently required scope.
- **ER-08 — What are we not implementing, why, and where can the owner review or reopen that choice?** Shared integration and production provider/MFA/rotation/admin/PostgreSQL/storage/security review remain central/external. Review EM-138/139 and this receipt; no fake provider acceptance or background cleanup daemon was added.
- **ER-09 — What actually passed, what failed, and which claimed capabilities still need independent or native verification?** Exact executed results and all retained failures are above and in the final append. Native identity UI and real-provider/security acceptance remain untested; existing native regression success elsewhere cannot imply them.
- **ER-10 — What might we still have missed, and how can the operator or owner record their own hypothesis?** Production proxy/cookie policy, distributed session/grant revocation, service-account lifecycle, signing-key rotation, rate limiting and retention need host review. Append new findings/decision history centrally rather than inventing acceptance.
- **ER-11 — What course has an authorised human selected, and what exactly would require reconsideration rather than an automatic switch?** No client selected-course record exists here. Owner selected existing-roadmap engineering, not a course/action permission. Changed provider/security policy requires review; no automatic course switch exists.
- **ER-12 — Which available inputs were not processed, what limits bound this conclusion, and what could exist outside the current catalogue?** Only repository source, fictional signed fixtures and controlled local HTTP/native regressions were processed. No real client data/provider account/token/model/research runtime was processed. Denials cover named resources/operations, not global impossibility.
- **ER-13 — When analysis fails, what safe recovery is available, who contributed the correction, and is the original failure still recorded?** Deterministic implementation/tests were authored by this coding agent, not generated model inference or independent human review. Missing tools/PATH/setuptools and the allowed-hook regression were repaired and retained above; uncertain exchanges require a user-started new login. Frozen Studio failure remains visible.
- **ER-14 — Can the exact implementation and evidence for every delivery claim be recovered, or must that claim remain reported-only?** Branch/base, containing source commit, raw VM artifact locations, final report/hash and unchanged code-byte comparison are recorded. VM-only raw artifacts are not automatically remote Git evidence; the compact final receipt preserves actual outcomes and source binding. No older upstream native report is attributed to this tree.
- **ER-15 — Does this improve the operator's next decision or merely increase reviews, alerts and screens? How would we measure the difference?** Hypothesis: current-scope denial and explicit session/provider status reduce accidental cross-matter work. Measure denied cross-scope attempts, time to establish intended access and false-denial/support burden in a separately authorized fictional usability/security exercise. Test counts/screens are not customer value.

## Handoff state / next action

No broad B03-01 status was edited. Final acceptance, fragment validation, commit/push and remote verification remain to be appended at this initial checkpoint. Next owner is central integration, not deployment. See exact adapters and frozen-test limitation above.

### Proposal validation before the implementation commit

Merged copies of the lane fragments and unchanged canonical data were regenerated
in the ignored `artifacts/identity-register-validation/` scratch directory. Copies
of the real `scripts/delivery.py`, `scripts/emergence.py` and `scripts/changelog.py`
ran their normal `--write` and `--check` commands there (emergence/changelog checks
also used `--base 56c9b79428a612dff11e2fae0219640d156032ff`). All passed: 71 tasks,
11 milestones, 121 retained/proposed discoveries and 59 changelog entries. Historical
discovery/changelog preservation checks passed. These are proposal validation
results, not an adopted canonical register or an upgraded task status.

Python compilation of `eightball`/`endstate`, changed UI `node --check` and
`git diff --check` passed. No configured pre-commit file or executable repository
hook was found (only Git sample hooks); normal commit hooks are not bypassed.
