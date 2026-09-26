# Sprint checkpoint: Plan Review and structural identity regression

24 September 2026. Local developer build `0.2.0-alpha.6`, within unfinished V0.2.

## Input and delivery

The supplied Source Clarity alpha.5 source has exact tree `c057d35ff84c1480243208d9674f4e99f7bf74a6`. It was imported as local comparison commit `ae6e2ac246b44309197aed6b7a047d8a88e10afa`, and all 746 baseline tests passed again. That comparison commit is not a pushed branch.

The inspected GitHub integration branch remains `feat/situation-intelligence-v2`, PR #2, head `824ca6421ff3100e1af596347f2d1247dde8f8dc`. PR #2 is draft and unmerged. The earlier source-write safety block was not bypassed. This sprint is delivered as complete cumulative source plus exact-base and incremental patches. No deployment or provider request was made.

## Bounded work

- Add a provider-free ENDSTATE Plan Review assessment with target/confirmation tracing, structural diagnostics and up to three independently reset hypothetical checks: remove an available action, change budget, or let time elapse without new evidence.
- Embed the review in existing Plan Studio and Ways Through rather than create another main navigation view. The black interface shows exact source/typed references, six explicit human judgements and historical review records.
- Preserve case facts, objectives, decisions, approvals and case revision. Review records live in their own case-scoped, hash-linked journal, included in audit exports only when present. Save validates the exact assessment, clock window, source snapshot and review sequence.
- Add eight offline synthetic engineering fixtures and an unfilled professional-review sheet. The quality-gate protocol is proposed, not a claim that independent reviewers or live models have passed it.
- Correct an observed planner defect: two candidate dependency paths could share a route ID even when one failed constraints and another did not. Only colliding IDs receive a structural suffix. Existing noncolliding wire IDs and original fixtures remain compatible.

## Verification

**794 code tests, 308 explicitly bridged browser checks across nine suites, and 8/8 offline structural fixtures passed.** Python compilation, JavaScript syntax and generated-document/history guards passed. The authoritative observed results and boundaries are in `docs/evidence/plan-review-local-verification.json`. Actual old/new kernel output is retained in `docs/evidence/route-identity-regression.json`. Native browser navigation was attempted and returned `ERR_BLOCKED_BY_ADMINISTRATOR`; the policy was not changed. Subsequent local browser runs use the explicit ASGI bridge, not purported native HTTP or provider inference.

Run the complete code suite, all nine browser journeys and generated-document guards. Do not infer model quality from successful deterministic checks. No reviewer identities, semantic quality labels or independent acceptance percentages were fabricated.

## Emergence Review

What did this sprint reveal that we had not properly seen, specified or understood before we built it?

- **EM-044, existing task / adopted:** route identity must retain semantically different producer ordering. Four candidates had only three IDs before the fix; all four are distinct afterwards.
- **EM-045, existing task / adopted:** a clean dependency graph can still describe sending an offer when the target requires acceptance. Separate structural inspection and human target-alignment judgement.
- **EM-046, existing task / adopted:** favourable review is not truth or permission. Record human judgement without modifying case evidence or action approval.
- **EM-047, existing task / adopted:** stress comparisons must start from the same snapshot. Independent trials are labelled and never accumulated silently.
- **EM-048, retained candidate / deferred:** a six-part review may create operator burden. This is a hypothesis to observe in user testing, not justification to auto-complete checks or add another score.
- **EM-049, existing task / adopted:** a destructive effect can be followed by a legitimate recovery action. The fixture must state its actual constraints rather than assume all negative effects make a route impossible.

All six discoveries remain in `docs/delivery/emergence.json` with owner review pending. The original 43 entries and earlier failures are preserved. The register now contains 49 discoveries.

## Next handoff

B02-11 is partial: usable review/evaluation infrastructure exists, but independent expert review and prospective real-provider quality evidence do not. B02-09/B02-12 remain blocked by the unchanged source-to-plan acceptance gate. B02-16 and new native integration acceptance remain unfinished. Integrate the cumulative patch without applying older local packages twice, run native CI in an authorised environment, then use the reviewed evaluation protocol to measure providers when credentials/runtime are deliberately available. Do not merge, mark release-ready or deploy solely because the unit tests pass.
