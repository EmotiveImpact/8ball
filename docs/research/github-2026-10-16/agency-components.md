# Production foundation candidates for ENDSTATE / 8BALL

Research date: 2026-10-16 UTC. Read-only component fit research, not a security audit, integration result, production certification or authorization to deploy. Public source files only were fetched into `/tmp/8ball-swarm-search/security-components/`; no dependencies, containers, credentials, models or inference were used. Upstream HEADs are evidence pins, not recommended production versions. Choose supported stable releases and run compatibility/security review at adoption.

## Current requirement and recommended composition

8BALL currently has a trusted local operator, local bearer token, SQLite, fictional/non-confidential cases and human command/revision boundaries. `docs/v2/PRODUCTION-SECURITY.md` explicitly calls the future deployment design-only. It requires OIDC/MFA, organisation and matter membership, expiring/revocable specialist grants, reviewed client projections, encrypted evidence storage, auditable access, provider boundaries, recovery and acceptance before real agency use.

**Minimum first production foundation:** Keycloak (or an existing approved OIDC provider) + Postgres + explicit case/matter grants and enforcement in 8BALL. Preserve ENDSTATE as the generic deterministic engine and the application as the authority boundary. Do not add a swarm framework to solve identity or case authorization.

**OpenFGA is the preferred optional fine-grained authorization component** when the target specialist/object/client sharing model justifies a dedicated relationship service. Prototype the exact grants/revocation model before choosing it over application/database grants. Add OpenFGA once, with a documented authoritative grant store and synchronization/revocation strategy; do not create two divergent sources of permission truth. Its natural question is “may this identity read this object in this matter?”

**Do not add OPA simultaneously by default.** OPA is a capable general policy engine, useful later if provider-data policies or action policy rules must be shared/versioned across multiple services. It overlaps permissions work and adds a second policy language/service. A policy answer still requires enforcement in the calling application. Neither OpenFGA nor OPA decides that a proposed real-world outcome is true or gives a model permission to execute work.

## Source-pinned candidates

| Project | Inspected HEAD | License | Actual contribution | Limits and work still required |
|---|---|---|---|---|
| [Keycloak](https://github.com/keycloak/keycloak) | `eae20e964b2e23cfd8f4ed18b599343ebb056e8f` | Apache-2.0 | OIDC identity, federation, authentication flows and OTP/MFA, user/session lifecycle; admin code removes user sessions and sends backchannel logout | 8BALL must validate issuer/audience/expiry, secure browser sessions and logout, resolve current app grants, integrate revocation and enforce access on every route. A stateless JWT signature check alone does not observe every later revocation. Not a confidential evidence vault. |
| [OpenFGA](https://github.com/openfga/openfga) | `fb8e7df866742a0c947e3066919ee59ac9e70eea` | Apache-2.0 | Relationship-based fine-grained permission checks, typed authorization models, tuple writes/deletes, conditional evaluation and supplied context, HTTP/gRPC, persistent Postgres backend | Not an identity provider; application must call and enforce checks, supply trusted time/context for expiry, protect grant-management APIs, define cache/freshness behavior and revoke all derived access paths. Read access is distinct from permission to approve or act. |
| [Open Policy Agent](https://github.com/open-policy-agent/opa) | `fdf6011f57fdc25f01de1982e296bb402cf37625` | Apache-2.0 | General declarative Rego policy decisions over supplied input/data; REST or SDK integration | Calling service enforces results. Policy freshness/distribution, input authenticity, fail-closed behavior, logging minimization and semantics remain integration responsibilities. No built-in ENDSTATE evidence or outcome correctness. |
| [PostgreSQL](https://github.com/postgres/postgres) | `eb7cc1d09e742d369540016455d0f55c619106f2` | PostgreSQL License (permissive) | Relational transactions, constraints, row security, structured case/event storage and established backup/recovery mechanisms | RLS only protects as configured. Superusers/BYPASSRLS and normally table owners bypass it; composite matter keys, non-owner service roles, transaction-scoped context, policies, tenant denial tests, encrypted backups and actual restore tests remain required. Does not make a mutable audit chain administrator-proof. |

## Representative source evidence

### Keycloak

- [README](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/README.md), [license](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/LICENSE.txt), [Maven manifest](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/pom.xml). Java/Maven service; development main is a snapshot, not an install recommendation.
- [OIDC documentation](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/docs/documentation/server_admin/topics/sso-protocols/con-oidc.adoc) and [OTP policies](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/docs/documentation/server_admin/topics/authentication/otp-policies.adoc).
- [Session revocation instructions](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/docs/documentation/server_admin/topics/sessions/revocation.adoc) describe not-before policy and pushing to registered OIDC adapters. [Actual UserResource logout](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/services/src/main/java/org/keycloak/services/resources/admin/UserResource.java#L693) requires management authority, sets not-before, calls backchannel logout and records admin event. 8BALL needs its own compatible session lifecycle.
- [Production configuration](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/docs/guides/server/configuration-production.adoc) explicitly addresses TLS, database, hosts/proxies and clustering. A `start-dev` demo is not that deployment.

### OpenFGA

- [README](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/README.md), [license](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/LICENSE), [manifest](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/go.mod). Current source declares Go 1.26/toolchain 1.26.8; runtime service can use a separately reviewed release. README distinguishes ephemeral in-memory demo from production Postgres/MySQL storage and SQLite beta.
- [Write command](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/pkg/server/commands/write.go#L80) validates tuple changes and applies deletes/writes through storage. This is a useful grant/revocation primitive, not end-to-end revocation across 8BALL storage, caches and active jobs.
- [Check command](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/pkg/server/commands/check.go#L209) carries request consistency and uses configured cache wrappers. [Graph check](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/internal/graph/check.go) applies tuple-condition filters.
- [Conditional evaluation](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/internal/condition/condition.go#L201) compiles/evaluates typed CEL conditions and handles missing parameters. An expiry policy needs trusted server time and tests; it is not automatically an expiring object URL or background revocation daemon.
- [Postgres store implementation](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/pkg/storage/postgres/postgres.go) substantiates the storage claim.

### OPA

- [README](https://github.com/open-policy-agent/opa/blob/fdf6011f57fdc25f01de1982e296bb402cf37625/README.md) explicitly says the service must enforce the returned policy result; [license](https://github.com/open-policy-agent/opa/blob/fdf6011f57fdc25f01de1982e296bb402cf37625/LICENSE), [Go manifest](https://github.com/open-policy-agent/opa/blob/fdf6011f57fdc25f01de1982e296bb402cf37625/go.mod).
- [Actual SDK decision method](https://github.com/open-policy-agent/opa/blob/fdf6011f57fdc25f01de1982e296bb402cf37625/v1/sdk/opa.go#L302) evaluates supplied input and returns result/provenance; [language documentation](https://github.com/open-policy-agent/opa/blob/fdf6011f57fdc25f01de1982e296bb402cf37625/docs/docs/policy-language.md).

### PostgreSQL

- [README](https://github.com/postgres/postgres/blob/eb7cc1d09e742d369540016455d0f55c619106f2/README.md), [license](https://github.com/postgres/postgres/blob/eb7cc1d09e742d369540016455d0f55c619106f2/COPYRIGHT), [Meson build manifest](https://github.com/postgres/postgres/blob/eb7cc1d09e742d369540016455d0f55c619106f2/meson.build).
- [Row-security implementation](https://github.com/postgres/postgres/blob/eb7cc1d09e742d369540016455d0f55c619106f2/src/backend/rewrite/rowsecurity.c) describes read/mutation policy application and default-deny. [DDL docs](https://github.com/postgres/postgres/blob/eb7cc1d09e742d369540016455d0f55c619106f2/doc/src/sgml/ddl.sgml#L2925) document bypass roles, owner behavior and caveats. [Backup docs](https://github.com/postgres/postgres/blob/eb7cc1d09e742d369540016455d0f55c619106f2/doc/src/sgml/backup.sgml) cover dump/restore and archival recovery; the product team still needs to select, operate and test them.

## Remaining application responsibilities, even after adoption

1. **Authority:** every case command checks authenticated actor, exact organisation/matter/object scope, expected revision and explicit action authority. Selecting a route, accepting a model proposal and approving a real action remain distinct. Keep inference workers read-only for live commands.
2. **Data segregation and revocation:** enforce at APIs, DB, source downloads, search, exports, caches, model calls, queues and client views. Cached allow results and signed links need bounded/revocable behavior. Test revoked access during long-running jobs and just before publication/command commit; no grant writes by model output.
3. **Evidence attachments:** immutable originals, hashes/exact source spans, derived OCR as a separate provenance record, quarantine/type/size/scanning, encrypted object storage and managed keys, authorised short-lived download mechanism, retention/holds/deletion policy. The researched services do not supply this entire vault.
4. **Audit:** durable actor-aware access and mutation events, append-only privileges, independent checkpoint anchoring, source/export verification, admin separation and break-glass procedures. Authentication logs alone are not a case evidence chain; a database hash chain alone is not administrator-proof.
5. **Secrets, providers and egress:** managed secret injection/rotation, scoped service credentials, allowlisted model gateways, approved matter data processing and budgets, no secrets/raw evidence in telemetry. Swarm agents need the same gates and can multiply disclosure and cost.
6. **Resilience:** encrypted independent backups, recovery objectives and observed restore drills, outbox/retry/idempotency behavior, concurrency and stale-review tests, interruption/restart/cancellation behavior, operational monitoring that avoids content leakage.
7. **Human acceptance:** scoped pilot owner approval, professionals validating the actual workflow, reviewed playbooks and independent held-out model evaluation. A new dependency does not close existing V0.2 gates.

## Bounded integration proof before production

Use fictional data first: two organisations; two matters; director, lead, specialist and client; an expired/revoked object grant; a confidential internal source excluded from client publication. Demonstrate denial for read, mutation, source download, export, search, simulation and model requests across boundaries. Exercise concurrent grant revocation and approved-action submission at the commit boundary. Revoke while a worker runs and ensure no later unauthorised output is published. Restore DB plus evidence objects from independent backup and verify hashes/audit continuity. These are proposed acceptance tests, not results already achieved.

Read-only search outcome: candidate composition and integration requirements established. No runtime adoption, configuration change, app tests or deployment performed.
