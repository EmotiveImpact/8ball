# Source Desk native closeout correction

26 September 2026. Current build: 8BALL 0.2.0-alpha.8. Scope is a bug fix and acceptance, not a new version or feature lane.

## Verified starting point

The cumulative alpha.8 source is now published at d27ad600342245d0222b5f4573da8fdcbbf8c1d4, tree dafc6e3d2d0a28f081695aea634c57834ff81515. Local source ZIP reproduced that exact tree. Local Git history was reconstructed because direct clone could not resolve github.com; it must not be force-pushed. Publish the reviewed patch over the exact real remote parent instead.

Native run 36217951370 on that source passed code, installed package, schemas and ten of eleven browser suites. Source Desk alone failed at its existing whole-original search assertion. Artifact 10896994626 was retrieved; SHA-256 56106bb2c50a3ddfb25f40de8c6f851e6cfa45625df4863d804387e9ee14bce5. Its failure screenshot shows an empty required query field, not an API error. The source log is preserved alongside this record.

## Cause and correction

The query lived only in the input until search completed. A late index/page render could therefore replace a phrase already typed with the old empty state. Search and document navigation also shared one request counter, letting an unrelated refresh invalidate a valid result.

Persist the query on input, restore its focus/selection only in the same case/document, separate search and navigation generations, reject responses for superseded queries/closed workspaces/other cases, and ensure an old reopen cannot override a later document choice. No change to original-text storage, quotation offsets, model input, case facts, permissions or CSP.

## Verification

Twelve deterministic component tests exercise controlled response order. Against unchanged alpha.8 they produce 8 failures and 4 passes; the correction passes all 12. These are regression assertions, not 8 independent vulnerabilities. The local full code suite passed 938 tests. The Source Desk real-API/SQLite bridge journey passed 38 checks, including three new controlled-delay assertions for query, caret and unchanged audit. All original search, export, BOM/CRLF/emoji, duplicate, retraction and case-isolation checks remain present. No increased search timeout, canned response, removed assertion or CSP relaxation.

The browser regression temporarily holds one index request then forwards it unchanged to the real selected transport. This is an explicit scheduling perturbation, not a mocked API result. A local native attempt remains administrator-blocked. The patched all-native GitHub run is the next gate; its result must be recorded separately once observed. No inference, independent professional or human screen-reader review is performed by this correction.

## Finish the current stretch

The owner has frozen optional scope. Preserve the current features and all research references, but do not merge the research backup branch or introduce Sales/SDR, Lab, prediction/simulation architecture or V0.3 agency work now. Finish native integration, actual-provider/independent-quality, source interpretation and human accessibility requirements. Only verified required items may close. Keep PR #2 draft; do not merge/main-tag/deploy from this fix alone.

## Emergence Review

This sprint adds concrete evidence to existing EM-035 (asynchronous work must preserve the right context), EM-053 (operator orientation must survive replacement) and EM-051 (verification belongs to exact source). A render can lose intent without any runtime error; a successful fast bridge run cannot establish response-order safety. Separate request generations by responsibility, preserve drafts and directly perturb scheduling. The operator's latest query is not a new case fact. These findings and their evidence are retained here and in the changelog under the existing IDs; no new optional scope is promoted.

ER-01..15: observed failure and regression reproduce the problem; alternate explanation of absent source is rejected by the retained original and screenshot; no new actor/causal inference; the highest-value question was which request replaced the input; target and authority are unchanged; obsolete async responses are the reconsideration trigger; fix existing B02-14/B02-16 and preserve deferred ideas; new native/semantic/human evidence remains separate; slower response order is now an explicit test; source/import/analysis coverage is unchanged; no outcome promise, model calibration or attention score is introduced. The owner can reopen a wider draft-preservation review after current acceptance.
