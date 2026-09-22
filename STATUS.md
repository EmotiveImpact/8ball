# Delivery status

22 September 2026. `0.1.0-alpha.1`. Working local single-operator developer release.

Implemented: responsive eight-view workspace; persisted cases; two human-authored editable playbooks; bounded backward outcome planning; condition/evidence provenance; conflicting observations; revision-scoped human approvals; completion distinct from success; route estimates and constraints; scenario comparison; transactional SQLite audit chain and export; optional advisory Jev, GLiClass and Ollama adapter code.

Locally validated: 86 engine/API/provider-contract pytest checks and 27 Chromium interaction/layout checks using an explicit ASGI bridge. The bridge reached the real application and SQLite store. It did not validate native browser networking, CSP enforcement, sessionStorage or downloads. See `docs/VALIDATION.md`.

Not delivered: hosted deployment; production agency security; accounts/tenants; secure client portal; uploads/OCR; automatic email ingestion; novel playbook generation from a free-text brief; actual live model inference or calibrated outcome prediction. Model responses are advisory only and their current tests use doubles.

## Next implementation priorities

1. Run the supplied native-browser CI and configure one real local model in a disposable environment. Record compatible dependencies and a held-out evaluation, not just a successful model response.
2. Add reviewed graph proposals from free-text intake and explicit playbook authoring with provenance. Extend route modelling to third-party refusal/withdrawal and verification wait times without promising outcomes.
3. Build authenticated, tenant-isolated agency infrastructure and a proper evidence vault before testing real client information. Then add expert permissions, scoped client access and authorised ingestion connectors.

No automatic background monitoring or external execution is running. The source branch and pull request, rather than a deployment claim, are the delivery boundary.
