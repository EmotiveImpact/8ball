# Native decision cost policy — bounded provider-specific follow-up

Owner: Devin / integration. Branch `devin/1792969169-roadmap-integrated`.
Starting checkpoint `d89bae35b09207c174135ef0bb237611b73ebe5d`; B02-11 remains
partial. This follows the verified rejection diagnostics, not a retry or repair
of the first five-request coordinated attempt.

## Evidence and scope

The [official gateway funding contract](https://platform.experientiallabs.ai/docs/cost-api)
states that platform-funded `usage.cost` is USD, while BYOK's platform charge
excludes upstream billing. Its native response schemas alone do not define that
extension. The [previous investigation](2026-10-26-provider-diagnostics.md#follow-up-accounting-evidence--read-only-no-inference)
and [three exact-request read-only receipts](../../evidence/native-cost-receipt-read-2026-10-26.json)
support this narrowly scoped interpretation. They do not establish a general
cost unit for arbitrary providers or prove that future requests are free.

Only `DecisionSession`, already fixed to Experiential's native `/v1/systemone`
and `/v1/decisions` routes and the selected Jev/Clef/GPT model IDs, interprets
generic cost. The reusable engine and generic response validator do not infer
monetary units. No price lookup, inference, extra billing HTTP read, retry,
fallback, credential change or case action is added by this software change.

## Accounting contract

Policy: `experiential.native-platform-funded-usd.v1`.

- Generic `usage.cost` needs **literal boolean `is_byok=false`**. Missing,
  malformed or true funding flags do not establish a full platform-funded cost.
- If supplied, `pricing_known` must be true and `currency`, `cost_currency` or
  `cost_unit` must be `USD`. Negative/invalid/nonfinite costs still fail validation.
- Conversion uses the original JSON numeric literal, **not a rounded binary
  float**: bounded Decimal integer-ratio arithmetic must yield exact whole nano-USD.
  Fractions, excessive precision/size or extreme exponents remain unknown.
  Numeric text is limited to 64 characters and decimal exponent magnitude 400
  before integer-ratio arithmetic. There is no rounding, upward or downward.
- Preserve explicit `cost_nano_usd` without reinterpretation when there is no
  known conflict. Fractional explicit nano amounts still cannot become a known
  integer cost. Do not overwrite them from another field.
- Known funding/unit/pricing conflicts, or disagreement between confirmed USD
  and explicit integer nanos, leave the effective cost unknown. Original amounts
  remain in diagnostic metadata; neither field silently wins.
- Preserve the parsed response and its canonical hash. Retain a separate exact
  body hash, bounded original numeric text, raw amounts/funding flags and the
  conversion basis. Standalone and coordinated worker results keep these receipts.
- `charge_status` remains unknown / provider billing not verified. Reported cost
  is not an invoice, guaranteed effective price, total account spend or hard cap.

The policy version is in both worker configuration fingerprints. A queued grant
under a different cost policy requires re-review; changes detected around a
provider request discard publication and stop later stages. The review-spec hash
continues to bind only the spec; it is not the full host configuration hash.

## Controlled verification

616 focused tests passed across native decision, specialist worker, coordinated
planning/evaluation and compatible-provider suites. Python compilation and
whitespace checks passed. Fixtures cover every selected native model, exact
conversion including zero, missing/BYOK funding, conflicting amounts/units,
fractional nanos, raw-number precision, hostile exponents, overflow, retention,
unchanged source response, one POST only, reported-cost limits and authority
changes before/after provider calls. Full native/package acceptance is next.

These are controlled HTTP fixtures through the actual local worker and storage,
not new provider answers. No new live result, billing reconciliation, semantic
quality, prediction, independent review or production acceptance is claimed.

## Emergence Review

**What did this sprint reveal that we had not properly seen, specified or
understood before we built it?** An accounting interpretation changes whether
another model can run; it therefore belongs in the reviewed configuration.
Also, converting a float to Decimal cannot recover digits already rounded away
by JSON parsing, and two individually valid money fields can contradict each other.

- **EM-332, existing_task B02-11:** adopt only verified provider/funding semantics,
  preserving unknowns, BYOK separation and the original failed experiment.
- **EM-333, existing_task B02-11:** bind cost-policy versions to worker authority,
  not only to audit text or request-body schemas.
- **EM-334, existing_task B02-11:** retain exact bounded numeric provenance and
  contradictory fields; normalization is not permission to choose a convenient bill.

ER-1–5: better failure/accounting boundaries, not proven operator benefit or
improved planning. ER-6–10: preserved raw/canonical hashes, exact numeric text,
failed history and missingness; no hidden network or model majority rule.
ER-11–15: no course selection, approval, case facts, intended-effect application,
cross-client learning or expanded required product scope. Independent quality,
prospective outcome scoring and human usability remain open.

## Handoff and next action

Retain a source-bound native/package run, inspect it before any closeout edits,
archive the exact report, and publish additively to PR #6. Any further live
diagnostic needs a new frozen source/protocol; the first five-request attempt
stays closed and failed/partial. No recognised historical rerun. No merge,
deployment, release or dedicated coordinated-report UI acceptance.
