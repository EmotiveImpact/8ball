# Authenticated ENDSTATE event review API — 25 October 2026

Base `fd57f16dd66a1ce52a3f60144ddbeaf8fcfc117c`; branch feat/agency-authorisation-20261025, draft PR5. Continue the existing build goal without release or deployment.

Agency mode now exposes four explicit routes: GET case event-work detail, POST its reviewed graph, POST pull a change notice, and POST acknowledge a notice. The existing pinned-key JWT guard supplies identity and still rejects all other unsupported mutation/model routes. Event routes are registered only when the access registry and case store resolve to the same database. Local operator mode and separate-registry deployments retain their preceding routes.

Event detail reads original source/result and current revision from one permission-checked snapshot without consuming it. HTTP review requires current READ and WRITE permission because its receipt contains original material; both permissions are rechecked in the case transaction and before commit. No caller-controlled reviewer identity is accepted. Read-only notice acknowledgement remains distinct from case write authority. Generic denial responses do not disclose private permission details.

No browser event-review screen, OIDC browser login, remote identity discovery, external notification or ingestion/inference endpoint was added. PostgreSQL tenant enforcement, worker dispatch, lifecycle migration and actual-provider/human acceptance remain unfinished. The trusted-host review method retains its preceding write-only default; the HTTP caller explicitly requires READ as well.

## Verification

61 focused agency/event/review/lifecycle tests passed. Full native results are recorded at closeout. New tests exercise signed identities, exact source/output view, idempotent review and notice delivery, both grants, revocation between route guard and transaction, stale/cancelled results, injection of a reviewer, other matters, unknown work and absent routes in local/separate-registry mode.

## Emergence Review

What did this reveal? A verified route identity is insufficient if the case transaction reads grants from another database, or if a write response discloses source material without current read permission (EM-106).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | Continue the existing ENDSTATE/8BALL goal and ES02/B03-01 tasks. |
| ER-02 | Keep verified identity in the host API and neutral calculation in ENDSTATE. |
| ER-03 | Enable event routes only with a shared grant/case transaction database. |
| ER-04 | Browser review, OIDC login, worker dispatch and PostgreSQL isolation remain incomplete. |
| ER-05 | A stored review or notice acknowledgement does not attest facts or genuine human acceptance. |
| ER-06 | HTTP review needs READ and WRITE because it returns original source/result provenance. |
| ER-07 | Revocation after the route guard must still deny the transaction. |
| ER-08 | Unknown routes and ordinary command/model paths remain denied in agency mode. |
| ER-09 | Original source, raw result, reviewer and request hashes retain existing bindings. |
| ER-10 | Caller-supplied reviewer fields fail validation instead of overriding JWT identity. |
| ER-11 | No route silently selects a course or approves an action. |
| ER-12 | Retain scope, cancellation, stale revision, duplicate and revocation denial coverage. |
| ER-13 | Do not replace old evidence or count controlled API fixtures as model/human acceptance. |
| ER-14 | Push exact source and preserve full native receipt separately from final documentation. |
| ER-15 | Reviewers can inspect original material and submit explicit amendments; actual usability still needs a browser surface and operator review. |

Evidence: controlled signed-JWT API and database tests. UX implication: distinguish read permission from review authority and delivery acknowledgement. Disposition: existing tasks stay partial, no new research runtime or external-action authority.

## Additional demonstrated gap and correction

The preceding API checkpoint f75dad585a86deb75b3e8703be70cbe042c49f7a passed its existing 1,341 source /1,341 installed /396 native checks with valid source inspection and green CI. A separate temporary-database reproduction demonstrated an uncovered failure: an unbound processing result could change another case in the same matter at revision 0. [Preserved result](../../evidence/endstate-event-api-case-binding-gap-2026-10-25.json). The passing suite does not erase that failure.

Correction: EventWork optionally binds a case at enqueue against actual case/matter ownership. Reviewed consumption requires this binding. Generic/unbound event attempts remain retained but cannot create case changes. A migration adds a nullable case column without guessing historical ownership. Previously committed historical receipts retain their exact idempotent acknowledgement and export semantics; no new case change is allowed from an unbound attempt. New tests cover two cases in one matter, unknown/wrong-scope enqueue, old-schema migration and historical committed acknowledgements.

### Additional Emergence Review

EM-107: matter scope and matching revision are insufficient processing lineage when a matter contains several cases. ER-02/03 require an explicit host case binding; ER-06/09 preserve transactional scope and original result; ER-10/13 forbid invented migration identity; ER-12 adds the missing same-matter and migration regressions; ER-14 preserves the earlier passing suite and separate failure. The remaining ER-01–15 answers above remain applicable. Disposition: existing ES02-02/03 correctness correction, with task status still partial.

## Verified corrected closeout

65 focused API/event/review/lifecycle tests passed. Corrected source `cd4ec0c9613c959688c701f293edcdc2dd986fd3` passed 1,345 source tests, 1,345 installed-engine regressions and 396 native checks across all eleven browser suites. Exact-source/artifact inspection passed before final receipt edits. Both checkpoint CI workflows passed: 40210692080 and 40210692192. [Receipt](../../evidence/endstate-event-api-native-2026-10-25.json) links the preserved additional failure.

Code is pushed to feat/agency-authorisation-20261025, draft PR5; documentation receipt is committed separately. No merge, release or deployment. Next: browser event-review UI and authenticated host worker dispatch, followed by migration/performance evidence. Original real-model, independent/human acceptance, OIDC login and production isolation remain open. EM-106/107 and all previous discoveries are retained.
