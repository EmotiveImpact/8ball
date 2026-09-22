# Delivery status

22 September 2026. `0.1.0-alpha.1`. Working local single-operator developer release.

Implemented: responsive eight-view workspace; persisted cases; two human-authored editable playbooks; bounded backward outcome planning; condition/evidence provenance; conflicting observations; revision-scoped human approvals; completion distinct from success; route estimates and constraints; scenario comparison; transactional SQLite audit chain and export; optional advisory Jev, GLiClass and Ollama adapter code.

Validated: 86 engine/API/provider-contract pytest checks and 27 Chromium interaction/layout checks. Initial local checks used an explicit ASGI bridge. The subsequent native GitHub Actions run **35752284823** passed on application commit `32db6226a04f88335c3a3ae2abcb34247c1934e0`, including real browser HTTP, native sessionStorage and a genuine downloaded export with the existing CSP enabled. See `docs/VALIDATION.md` and the checked-in native browser report.

Not delivered: hosted deployment; production agency security; accounts/tenants; secure client portal; uploads/OCR; automatic email ingestion; novel playbook generation from a free-text brief; actual live model inference or calibrated outcome prediction. Model responses are advisory only and their current tests use doubles.

## Next implementation priorities

1. Configure one real local model in a disposable environment. Record compatible dependencies and a held-out evaluation, not just a successful model response. Keep the now-passing native-browser CI as a regression gate.
2. Add reviewed graph proposals from free-text intake and explicit playbook authoring with provenance. Extend route modelling to third-party refusal/withdrawal and verification wait times without promising outcomes.
3. Build authenticated, tenant-isolated agency infrastructure and a proper evidence vault before testing real client information. Then add expert permissions, scoped client access and authorised ingestion connectors.

No automatic background monitoring or external execution is running. The source branch and pull request, rather than a deployment claim, are the delivery boundary.
