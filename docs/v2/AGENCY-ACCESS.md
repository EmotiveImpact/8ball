# Agency identity and current-authority development boundary

The normal launcher remains the trusted-local V0.2 application. The optional
`make_app(store, token, agency_access=guard)` boundary and the separate identity
router are engineering seams, not a production multi-tenant launch. Nothing in
this module silently migrates historical local actors, grants a matter at login,
approves an action or enables a model call. 8BALL remains the fixer product;
ENDSTATE remains the reusable read-only engine.

## Current identity and grant adapter

Use the existing `Identity(issuer, subject)`, `Resource(organisation_id,
matter_id, object_id)`, `Operation` and `Grant` from `eightball.authorisation`.
Provision case ownership, keys and grants in server code, never request bodies.
Duplicate case bindings and grant IDs fail instead of overwriting authority.

`AccessRegistry.require(identity, case_id, operations: tuple[Operation, ...], *,
object_ids: tuple[str, ...] = (), db: sqlite3.Connection | None = None) -> Resource`
returns the **server-owned matter scope** after checking every requested operation
against every requested object. Empty `object_ids` means whole-matter access;
an object-only grant cannot authorize a whole case or another object. It does not
assert that supplied object IDs exist or belong to the case: the consuming service
must prove that separately before using any content. Unknown/malformed scopes,
missing/expired/future/revoked/cross-identity grants and cross-tenant/matter/object
checks fail closed. Invalid stored grant data also denies rather than disappearing
from the policy result. SQLite failures must never become an allow result.

With `db`, use an active transaction on the registry's resolved **main database**.
The checker acquires a writer reservation before reading current grants. A stale
WAL read snapshot cannot authorize from a pre-revocation grant. Without `db`, the
checker opens and closes its own `BEGIN IMMEDIATE` transaction; that result is only
a preflight, not authority to consume data later.

`AccessRegistry.transaction(identity, case_id, operations, *, object_ids=())`
yields `(db, scope)` under `BEGIN IMMEDIATE` and rechecks grants before commit.
`CurrentAuthority(registry, current_identity)` exposes the same `require` and
`transaction` signatures **without the identity argument**. Its server-injected
`current_identity: Callable[[], Identity]` must authenticate the current bearer or
durable session on every invocation, not return a cached identity. The wrapper
rechecks identity around grant checks and pins the same identity across the entire
transaction, even when two different identities both have grants. Expiration,
revocation, changed identity or raised exceptions roll back the consuming write.
An injected callback exception propagates; HTTP hosts can translate authentication
failure to 401 and policy denial to a non-enumerating 403. Do not expose DB errors.

Configured agency requests expose `request.state.agency_authority` as this live
wrapper. For trusted host workers explicitly construct it with a verified worker
identity callback. Do not serialize it as a capability or substitute a user body,
arbitrary worker name or local operator bearer for authenticated identity.

All object ownership, policy/quarantine/scan/retention/egress checks, exact reviewed
projection digest, case revision, actor attribution and domain action permission
remain consuming-service checks in the **same transaction**. Missing adapters deny.
Do not hold the authorization DB lock across external provider work: authenticate
and check grants/policy before dispatch, then recheck current identity, grants,
policy and revision before result publication/commit. An already sent request or
downloaded response cannot be recalled. SQLite serialization here is not production
row-level isolation or complete worker enforcement.

## Pinned OIDC code flow and durable browser sessions

`eightball.oidc.login.OIDCConfig` requires operator-pinned HTTPS issuer,
authorization/token endpoints, redirect URI, client ID and a `kid -> PEM public key`
map. `required_acr` can require an exact configured authentication-context claim;
fixture claims are not independent proof of MFA. There is no discovery, JWK fetch,
public provisioning, refresh-token flow, background refresh, retry or provider
session termination. No live provider is configured by default and no network call
occurs on import or login preparation.

Construct `LoginService(path, config, TokenEndpoint(config))` only in an explicitly
configured host. Existing PyJWT[crypto], cryptography and httpx dependencies suffice;
no dependency manifest changes are needed. The HTTP adapter performs one bounded
public-client exchange with S256 PKCE, TLS verification, no redirects/environment
proxy inheritance/retries, a ten-second timeout and a 64 KiB response limit. An
explicit user continuation is required before visiting the external provider.

Login uses random one-use state, browser binding, nonce and PKCE verifier. State and
browser/session identifiers are stored only as hashes; nonce/verifier are cleared
when consumed/cancelled. Exchange failure or restart requires a new login, not a
replayed request. Cancellation/expiry is rechecked after exchange before publishing
a session. ID tokens require pinned RS256/kid, exact issuer/client audience,
subject, nonce, integer issued-at/expiry, authorized-party and optional ACR checks.
No access or refresh token is retained. Durable session lookup checks expiry and
revocation on each use. `logout(session)` revokes that session;
`revoke_identity(identity)` revokes all **existing local sessions**, not provider
accounts, future sign-ins or independently issued API bearers. Remove/revoke grants
separately when withdrawing matter authority. Protect the SQLite file with operator
permissions. Expired unused attempt cleanup, account administration, key rotation,
managed encrypted storage and production retention remain host/deployment work.

## Explicit integration (not mounted by this lane)

1. Mount `register_identity_routes(router: APIRouter, service)` from
   `eightball.v2.identity_api` on a **separate same-origin router** with the intended
   `/api/v2` prefix, not the agency-protected dependency: login must work before
   authentication. Validate the configured redirect path against that mount.
2. Relative routes: `POST /identity/login` prepares a provider URL,
   `GET /identity/callback` consumes one exact code/state/issuer response,
   `GET /identity/session` returns current identity (not grants), and
   `POST /identity/logout` revokes local session/attempt. Callback redirects only to
   `/v2/`. Login/logout and cookie-authenticated agency mutations require the exact
   configured Origin. Callback error details/codes are not returned to the browser.
3. Cookies are `__Host-eightball-session` and `__Host-eightball-login`, Secure,
   HttpOnly, SameSite=Lax, Path=/, with no Domain. Identity success responses are
   no-store/no-referrer. Serve behind correctly configured same-origin HTTPS;
   do not weaken cookies/CSP to make HTTP fixtures a deployment.
4. Pass `sessions=service` to the opt-in `AgencyAccess` guard. Bearer authorization,
   when present, takes precedence and fails closed rather than falling back to a
   cookie. Bearers still require exact issuer/audience/subject/expiry/issued-at and
   an operator-provisioned RS256 verification key. Route guards are only preflights.
5. Explicitly wire each consuming service's transaction/current-authority adapter.
   Add new operation/path pairs centrally only after complete policy/revision tests.
   Current guard mappings allow case/history/export and existing reviewed event
   reads/preview/review/outbox routes only. All other protected routes, including
   legacy/global listings/search/model jobs, continue to deny. Unknown routes do
   not become local-token fallbacks.
6. Optional UI mount: import `mountIdentity(container, {apiBase: '/api/v2'})` from
   `web/v2/identity-access.js`; its return value aborts pending fetches and clears the
   mount. It never reads/stores tokens in JS and requires a click to follow the
   configured HTTPS provider link. Navigation/common app files are intentionally
   untouched. No native identity UI acceptance is claimed here.
7. Constructors add only the opt-in `agency_login_attempt` and
   `agency_browser_session` tables; existing agency tables are unchanged. Let the
   integrator review backup/migration policy before constructing on an operator DB.
   No operator database migration or live provider call was performed by this lane.

Offline signed fixtures and same-database denial/rollback tests exercise read,
write, export, search, infer and download **authority**, not actual inference or
production vault operations. Review the lane receipt in
`docs/delivery/lane-reports/identity.md`. B03-01 still requires combined middleware,
consumer/worker checks, provider/MFA configuration, production isolation and
independent security review before a broad production claim. Local mode, original
alpha import and historical audit lineage are unchanged.

Protocol references: [OIDC Core code flow](https://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth),
[RFC 7636 PKCE](https://www.rfc-editor.org/rfc/rfc7636),
[RFC 9700 OAuth security BCP](https://www.rfc-editor.org/rfc/rfc9700).
