# Agency API boundary and clearer overview — 25 October 2026

Base75fb95f; branch feat/agency-authorisation-20261025. Owner authorised full product implementation and the proposed clearer interface. Existing source, original PRDs and frozen fixtures preserved.

Implemented persistent server-provisioned organisation/matter grants, durable revocation and signed RS256 token verification with exact issuer/audience. An opt-in API boundary allows scoped whole-case read/history and independently granted export. Other routes deny until they support verified actors and full transaction/worker enforcement. This is not browser OIDC/MFA or production database isolation. Local launcher remains single-operator. See [agency access](../../v2/AGENCY-ACCESS.md).

Situation Room now leads with the recorded plain-language summary and evidence/change links. The graph is collapsed and keyboard-expandable, preserving the dedicated explorer. No invented narrative or model inference. Initial 24 policy/API tests and 51 native workspace checks passed; cumulative run follows with new disclosure checks.

## Emergence Review

What did this reveal? Existing local aggregate and asynchronous routes need their own enforcement; sign-in alone cannot make them safe (EM-100).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | Full-product scope and clearer interface explicitly authorised. |
| ER-02 | Permissions precede vault and collaboration work. |
| ER-03 | Existing routes encode single-operator assumptions. |
| ER-04 | OIDC browser/MFA, transaction policy and worker checks remain dependencies. |
| ER-05 | Authenticated identity is distinct from domain action approval. |
| ER-06 | Global listing, legacy and background-job paths can bypass a naive scope check. |
| ER-07 | Use explicit allowlists until each operation is integrated. |
| ER-08 | Controlled signed-token tests are not live identity-provider acceptance. |
| ER-09 | Preserve immutable case ownership and durable revocation. |
| ER-10 | Summaries should show recorded text; do not invent AI understanding. |
| ER-11 | No facts, targets, approvals or chosen courses changed. |
| ER-12 | Exercise forged/expired/wrong-audience tokens and cross-scope API denial. |
| ER-13 | Preserve all earlier discoveries; append EM-100. |
| ER-14 | Retain local compatibility while introducing explicit agency mode. |
| ER-15 | Continue authenticated transaction/worker integration, then vault/collaboration. |

Evidence level: controlled API and native browser tests. UX: summary before graph detail. Architecture: no automatic trust in token header key URLs or algorithms. Disposition: existing tasks; no acceptance promotion, real client data, release or deployment.

## Completed verification and limits

Checkpoint7fbb34ac346e5e884a7f0dc52908e38be514c4de passed 1291 source tests, 1291 installed-engine regressions and 394 native browser checks across11 suites; exact-source/artifact inspection valid before final edits. GitHub runs40203256823/40203256857 both passed. Earlier attempt20261025T143801Z-f1e3e17b was interrupted after an abbreviated ledger base SHA failed the documentation guard; retained as nonpassing, then corrected and rerun.

Final overview wording now separately counts unknown and disputed conditions. After this small UI correction, node syntax and all54 native workspace checks passed. Exact receipt: docs/evidence/agency-api-overview-native-2026-10-25.json. Final-head CI remains a separate run. Screenshot: docs/screenshots/8ball-overview-2026-10-25.png. No model or live identity-provider calls.

Next: complete OIDC browser login/PKCE/MFA integration and account administration, PostgreSQL transaction-scoped access and verified-actor mutation/worker enforcement; then vault/collaboration/durable processing. The remaining production roadmap is not implemented by this read boundary. Original required gates remain intact.

Emergence addendum: unknown and disputed evidence are different states; overview counts must preserve that distinction (existing engine rule, applied in the UI correction; no scope expansion).
