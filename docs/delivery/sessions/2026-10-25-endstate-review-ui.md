# ENDSTATE browser event review — 25 October 2026

Base `825c8c3969f6cf723a188cc6ae16094aa15c9e7e`; branch feat/agency-authorisation-20261025, draft PR5. Continue the standing build goal; no release/deployment.

The case/work-scoped `/v2/event-review.html` page displays original source and untouched processing output. It reuses Plan Studio to edit the current case graph, with a reviewer rationale, read-only change preview and explicit commit confirmation. Human editing remains separate from unassisted model acceptance. The API returns a token-free review URL and current review capability. Its new scoped preview uses one current READ-authorised transaction and creates no case event.

Development access uses the configured agency account token held only in module memory; no token is put in URL or browser storage. Real OIDC account sign-in remains unfinished. Ordinary local-token mode has no review API. This page is part of 8BALL, not a new industry application or a production authentication claim.

Read-only, stale or committed results cannot be edited. Locking/revocation clears source, result and draft; late responses cannot repopulate the locked session. A lost commit acknowledgement produces an unknown-outcome state, disables editing and requires explicit refresh. It never automatically resends the mutation. Refreshing an unsaved draft requires deliberate discard. Change-notice acknowledgement remains a delivery fact, not action approval.

## Verification and retained failure

48 focused API/review tests passed before the acceptance-runner tests were added to the focused command. Standalone native browser verification passed 27 checks, including read-only controls, source HTML escaping, source/result preservation, revision conflict, acknowledgement loss, session lock races and editable/read-only reflow at 320/390/768px. Full source-bound results follow at closeout. The new native suite is added after all eleven previous suites; integrated native acceptance now runs twelve suites. The new signed-identity suite deliberately has no bridge substitute.

The initial standalone native run failed on a test assertion inspecting the fieldset rather than its interactive descendants. Retained HTML confirmed the disabled fieldset; the corrected assertion checks the actual input and preview control. [Failure record](../../evidence/event-review-browser-first-failure-2026-10-25.json). No application guard was removed or relaxed.

## Emergence Review

What did this reveal? A lost acknowledgement leaves a possible successful commit, not permission to retry (EM-108). Native disabled-state evidence should inspect the controls users actually operate, not assume a fieldset assertion has equivalent semantics (EM-109).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | Continue the shared ENDSTATE/8BALL goal and existing ES02 review work. |
| ER-02 | Reuse Plan Studio rather than fork graph semantics. |
| ER-03 | Original source/output, editable current graph, preview and commit remain distinct. |
| ER-04 | OIDC login, worker dispatch, production isolation and operator acceptance remain unfinished. |
| ER-05 | Human-authoring UI and automated tests never establish unassisted model or independent acceptance. |
| ER-06 | Read-only controls reflect capability; server transaction remains authoritative. |
| ER-07 | Expiry/revocation and late responses clear rather than repopulate a locked session. |
| ER-08 | Lost acknowledgement requires explicit refresh, not automatic resend. |
| ER-09 | Preserve source/result, case/revision binding and immutable review provenance. |
| ER-10 | Keep the failed test artifact and correct control-level evidence. |
| ER-11 | Amendment does not select a course or approve execution. |
| ER-12 | Test scope, stale revisions, network acknowledgement loss, mobile widths and session races. |
| ER-13 | Keep original failed work and distinguish explicit human editing from model output. |
| ER-14 | Add the twelfth native suite; retain all prior suites and source-bound receipts. |
| ER-15 | Reviewers can inspect, explain and commit an amendment without API scripting; usefulness and accessibility still require genuine user review. |

Disposition: existing ES02/B03-01 implementation work. Native scripted account tokens are not OIDC-provider validation or human acceptance. No external sends, new application or deferred research runtime.

## Integrated failure and next worker boundary

The first integrated checkpoint a448ff7c6a356c2ed4506e81e3f54cb081353637 passed 1,346 source tests, 1,346 installed-engine tests and all preceding 396 native checks, then failed the new screenshot wait because string evaluation violates the unchanged CSP. Exact-source inspection remained valid for this failed run. CI 40212216822 failed identically; downloaded evidence confirms it. [Failure record](../../evidence/event-review-native-csp-failure-2026-10-25.json). A locator assertion replaces the evaluation. Its default 5-second timeout initially expired before the existing 6.5-second toast; the explicit deadline is now 10 seconds. Neither CSP, notification behaviour nor acceptance assertions were weakened (EM-111).

A separate worker-boundary experiment found that the ordinary fictional graph serializes to 16,501 characters, exceeding EventWork's 12,000-character result limit. It was rejected without truncation and the attempt remained running. [Retained experiment](../../evidence/event-result-size-boundary-2026-10-25.json). Worker integration must retain complete output, within justified storage bounds or via an immutable artifact reference, before any claim of full source-to-plan delivery (EM-110). This does not invalidate the bounded-text UI journey; it remains an explicit unmet integration requirement.

Additional Emergence Review: ER-04/09/12 require full structured-result retention and realistic output-size tests; ER-13/14 retain both failed runs and distinguish native software verification from the separate boundary experiment. ER-08 preserves CSP and uses assertions compatible with it. All remaining ER-01–15 findings above still apply.

## Verified closeout and publication blocker

Corrected source `461d3f2cecfcd8c4a00da40a56f56763d0d4fc90` passed 1,346 source tests, 1,346 installed-engine regressions and 423 native browser checks across twelve suites, including 27 new event-review checks. The focused API/review/runner command passed 84 tests. Exact-source/artifact inspection passed before final receipt edits. [Receipt](../../evidence/endstate-review-ui-native-2026-10-25.json). [Desktop screenshot](../../screenshots/8ball-event-review-2026-10-25.png) and [mobile screenshot](../../screenshots/8ball-event-review-mobile-2026-10-25.png) are copied from that exact native run.

The code checkpoint was successfully pushed to feat/agency-authorisation-20261025. GitHub then stopped authenticating: API returned HTTP 401 Bad credentials and Git could not obtain a username. Current cloud status remains connected, but supplies no refreshed GitHub credential. Corrected-checkpoint CI cannot be claimed. The owner was asked to refresh/reconnect the environment GitHub connection while independent local verification continued. Final receipt/screenshots are committed locally, not pushed. No work was discarded and no merge/deployment occurred.

Resume: inspect local HEAD and preserve the local closeout commit; refresh GitHub connection, push this branch, inspect CI and update draft PR5 description. Then resolve the preserved structured-result retention gap before authenticated worker dispatch. Actual OIDC onboarding, production database isolation, measured replanning, model quality and genuine human/independent acceptance remain unfinished. The complete standing goal is not accepted. All 111 discoveries are retained.
