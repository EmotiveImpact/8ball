# Agency access development boundary

The normal launcher remains the trusted-local V0.2 application. The optional
`make_app(store, token, agency_access=guard)` boundary is for isolated engineering
tests, not a production multi-tenant launch or a completed sign-in experience.

`AgencyAccess` validates RS256 signatures against an operator-provisioned public
key and exact issuer/audience, requiring subject, expiry and issued-at claims.
Token headers cannot select algorithms, key URLs or an identity provider. No
automatic network discovery occurs. Configure only keys from the intended trusted
issuer. Browser OIDC authorization-code/PKCE login, MFA, rotation and provider
integration remain required; fixture-signed tokens do not prove those flows.

`AccessRegistry` persists case organisation/matter bindings and grants in SQLite.
Provision these using server-side code, never request bodies. Duplicate ownership
or grant IDs fail rather than silently replacing prior authority. Revocation is
durable and checked on each new authorised request. In-flight responses cannot be
recalled; production transactional enforcement and PostgreSQL row policies remain
unfinished. The registry file must be stored with restricted operator permissions.

The current enabled surface is GET case detail/history and separately permitted
case export. These are whole-case views: object-only grants cannot access them.
All other protected routes deny in agency mode, including legacy APIs, global
case listings, writes, searches and model jobs. Do not expand this allowlist until
the operation carries verified actors and enforces revocation through its complete
transaction/worker path. Local mode retains its existing behaviour.

Next: OIDC browser login and account administration; transaction-scoped
membership and case rows; actor-bound mutations; filtered listings and object
projections; worker revocation; then the evidence vault and collaboration. Preserve
historical local actor labels during migration. This opt-in boundary is not evidence
that the production security gate has passed.
