# Agency authorisation foundation — 25 October 2026

Owner explicitly selected “Build full product” and authorised later roadmap engineering while V0.2 acceptance remains open. Start commit 1038291bf219d04e7fe4a6a01c332d1ac277fdba; branch feat/agency-authorisation-20261025. No deployment, new industry application or deferred research adoption.

Implemented immutable policy records and explicit deny-by-default matching of identity issuer/subject, organisation, matter, object and operation. Expired, future, revoked and naive-clock requests deny. A read-only object grant cannot expand into aggregate access or inference. 13 focused tests passed. These are controlled policy checks, not production security acceptance. The local API is unchanged.

Next engineering: verified OIDC identity, durable scoped grants, all request/worker and transactional enforcement paths, then cross-tenant API/database denial tests. No grants are accepted from request bodies. No silent migration of historical local actors.

## Emergence Review

What did this reveal? Object permissions do not compose automatically into aggregate permissions (EM-099).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | Owner widened scope to the full existing product roadmap. |
| ER-02 | Start with permission foundations before vault/collaboration. |
| ER-03 | Identical subjects at different issuers are different identities. |
| ER-04 | API, identity and database enforcement remain dependencies. |
| ER-05 | A policy permit is separate from domain action approval. |
| ER-06 | Aggregate operations can leak objects beyond a narrow grant. |
| ER-07 | Read-only access must not permit indirect writes or inference. |
| ER-08 | Unit-level isolation is not a production boundary. |
| ER-09 | Every consumed object needs scope enforcement. |
| ER-10 | Fail closed on missing grants and invalid clocks. |
| ER-11 | Existing targets, facts and approvals remain unchanged. |
| ER-12 | Test every operation across organisation and matter boundaries. |
| ER-13 | Preserve all 98 earlier discoveries; append EM-099. |
| ER-14 | Keep the trusted-local application labelled accurately. |
| ER-15 | Continue B03-01 integration before claiming accounts shipped. |

Disposition: existing required task B03-01; no relaxed V0.2 gate. Evidence level: controlled tests. UX implication: eventual client/specialist access must not expose an entire matter because one object is shared.
