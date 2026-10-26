# Native usage completeness correction — 26 October 2026

- **Scope:** existing B02-09 transport receipts only; 8BALL adapter, not ENDSTATE planning or authority.
- **Branch/base:** `devin/1792969169-roadmap-integrated`, `f7591dab735845bfffc7091d74be5415198fa88d`. Previous native integration and live evidence remain in [the preceding handoff](2026-10-26-sonnet-native.md).
- **Finding:** native `input_tokens` excludes cache creation/read tokens. Missing cache components cannot be zero-filled, and known complete input counts must still be summed when output usage is missing.
- **Correction:** normalize prompt totals only with all three input components; completion counts remain independently usable. Emit total only with complete input and output counts; retain all supplied native counters unchanged.
- **Verification:** before correction, the expanded fixture exposed five failures (four passed), retained in `docs/evidence/native-usage-regression-before-2026-10-26.log.xz`. After correction, 308 provider/integration/compiler/lifecycle checks passed. Full native acceptance is recorded in the final receipt.
- **Live evidence boundary:** no new paid calls. Earlier actual-provider runs used the preceding adapter revision; their native HTTP200 response counters were complete; HTTP400 billing remains unknown, so this correction does not change their recorded estimates. Their source hashes remain historical, not relabelled as this revision.
- **Delivery:** no merge, deploy, release, independent quality, professional or human acceptance. Current PR head is the publication authority; gates and reserved lane ownership are unchanged.

## Emergence Review

**EM-313 — existing_task, B02-09.** A partial meter reading is not a complete total. Native providers split prompt consumption differently, so normalizing names without checking component completeness can erase unknowns or omit known cache use. This belongs in the existing adapter/receipt boundary, not a second billing ledger.

ER-1–5: the observation is an accounting representation error, reproduced with controlled responses rather than a provider invoice. It improves honest operator inspection; no plan recommendation or customer-value claim follows. ER-6–10: preserve native counters, missing values, the failing regression, existing spend permission and bounded calls. No retries, changed validation or further model use. ER-11–15: courses, permissions and evidence authority are untouched; only supplied counters are in scope. Prior live sources/failed outputs remain recoverable. Billing confidence and customer value still need separate evidence; do not infer free usage or confirmed invoice totals.

## Verified closeout

Exact commit `08b1cde2bdf3fa091576b25b2484d45602c69d4b`, source `84be5aaf88603fa10e64f4d9010c0a3eda29e4ab8f1bceda2de5df170666829b`, passed **2,096 source tests, 2,096 installed-wheel tests, compilation, 24 JavaScript modules and 474 checks across all 13 native suites**. Source and artifact inspection passed before this documentation-only closeout; the prior failed controlled tests remain preserved. See [receipt](../../evidence/native-usage-software-2026-10-26.json). Only the existing Starlette/AnyIO deprecation warning remains.

Offline normalization of 12 retained native HTTP200 response receipts matched the earlier complete counts exactly. This checks accounting, not new inference or model quality. The only runtime file changed relative to the preceding native integration is `eightball/v2/compatible.py`. Publication remains the existing PR, with no merge/deploy/release. Next work is independent semantic/human acceptance, not more transport calls.
