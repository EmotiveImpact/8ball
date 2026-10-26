# Historical prediction diagnostic: inconclusive

## Result in plain English

We tested a masked version of the 2018 Rent-A-Center acquisition by Vintage.
The model saw a summary of the publicly announced deal, with Company A / Buyer B
instead of real names, and no later termination or court result.

| Question | Result |
|---|---|
| Would the announced deal close by 31 December 2018? | Sonnet assigned **45%** |
| What actually happened? | The original transaction did **not** close |
| Did the model recognise the story? | **Yes; it reported remembering the transaction and outcome** |
| Does this demonstrate predictive skill? | **No — inconclusive** |

It leaned slightly toward the eventual outcome, but we cannot count this as a
clean prediction. Its proposed next check was antitrust clearance; we have not
shown that this question would improve an operator's decision.

## Method and actual inference

- User requested a real historical scenario with names disguised, after the
  lifecycle work. This extends the earlier fictional-fixture testing permission
  to this public historical diagnostic, within the existing US$5 working budget.
- Information cutoff: **18 June 2018, 23:59:59 UTC**. Horizon: **31 December 2018,
  23:59:59 UTC**. The event is consummation of the original announced merger, not
  litigation success, settlement, a later deal or a share-price move.
- Actual request timestamp is in the retained receipt, **26 October 2026**. The
  historical `as_of` is an information cutoff, not the date we made a prediction.
- One request to direct Anthropic Messages, selected `claude-sonnet-5-5`, forecast
  prompt `historical-forecast.v1`; no retry, fallback, output repair or second
  model. Managed model identity is known; an immutable weights revision is not.
- The v1 runner used 8BALL's existing native provider transport and ENDSTATE's
  typed forecast/resolution scorer. It did **not** run the full application
  planning/challenge/review journey. A separate, deliberately simple ENDSTATE
  planning control ran afterward, without a provider call; it is not part of
  Sonnet's forecast and is not a complete model of the merger.
- The outcome file was read by the resolver after the forecast report was
  written. The model-facing context and schema were reconstructed from unchanged
  input/source afterward and matched the hashes in the original report. This is
  not independently timestamped preregistration or proof of author blinding.

The forecast is 0.45 and the observed binary outcome is 0. Brier loss is
`(0.45 - 0)^2 = 0.2025`; the fixed 0.5 baseline loss is `0.25`. Lower loss is
better, but **one contaminated case cannot demonstrate accuracy, calibration or
an improvement over a realistic merger base-rate forecast**. No accuracy
percentage or statistical significance is claimed.

The actual receipt contains 1,329 input tokens, 508 output tokens and zero
reported cache creation/read tokens. At the previously verified US$2 / US$10 per
million rates, the estimate is **US$0.007738**. Known Sonnet estimates now total
US$0.131566, plus US$0.000008547 reported by the decision providers. These are not
invoices; billing for earlier rejected/interrupted calls remains unknown.

## Source audit and limitations

Public sources: [agreement](https://www.sec.gov/Archives/edgar/data/933036/000119312518196340/d407444dex21.htm),
[June filing](https://www.sec.gov/Archives/edgar/data/933036/000119312518196340/d407444d8k.htm),
[June announcement](https://www.sec.gov/Archives/edgar/data/933036/000119312518196340/d407444dex991.htm),
and [later settlement announcement](https://www.sec.gov/Archives/edgar/data/933036/000119312519116716/d734946dex991.htm).
All four local raw HTML hashes match the retained source manifest. The later
announcement reports termination, the court ruling and settlement, not merger
completion. No later source text or real-party source URL was sent to the model.

The first input has two **author-introduced errors**, retained without rewriting
the original fixture or rerunning for a better score:

1. It describes a reverse fee as roughly 9% of *equity value*. That comparison
   used announced transaction value including net debt, not equity value.
2. It narrows extension eligibility to antitrust-related conditions being the
   only outstanding conditions. Section 8.01(b)(i) instead refers to any unmet
   7.01(b) or 7.01(c) condition, covering governmental consents and legal restraints.

Even without those errors, the author already knew the outcome and could bias
source selection and emphasis. Renaming parties and rounding amounts does not
prevent recognition. The supplied text is a limited summary, not all public
information available at the cutoff. The model's assumptions about financing,
competitive overlap and regulatory timing are not factual findings.

**Verdict: retain as an exploratory forecast-component diagnostic, exclude it
from independent predictive-quality claims.** No model score, completed review,
source digest or outcome resolution becomes case evidence, authority or an action.

## Protocol repairs and verification

Two preflight attempts made zero provider requests: an overbroad keyword check
rejected legitimate termination clauses, then a property was mistakenly called
as a function. The audit preserves these transcript-derived observations; they
are not fabricated contemporaneous runner receipts.

The actual v1 runner bytes are archived separately. The current v2 runner is
**offline-tested, not live-retested**. It requires both inference/external opt-ins,
pins the selected direct provider/model, bounds input and output, persists input
and planning control before one request, strictly validates all answer fields,
retains failed/interrupted checkpoints without secret-bearing exception text,
and prevents overwriting runs or resolutions. Resolution binds the exact case,
input, answer, forecast and source references. Hashes are integrity aids, not
independent attestation. No automatic keyword filter can prove a historical
information cutoff; a human source audit is still required.

Focused verification: **52 new protocol tests plus 34 forecast tests passed**.
Full native acceptance and publication are recorded in the subsequent source-bound
closeout below; do not attach an older lifecycle test count to this new source.

## Emergence Review

**What did this sprint reveal that we had not properly seen before?**

- **EM-318, observed_in_build:** name masking demonstrably failed to establish
  blindness in this selected case. Record recognition and exclude the result
  from independent claims; a denial of recognition would not prove blindness.
- **EM-319, observed_in_build:** de-identification/paraphrase can change financial
  denominators and contractual logic. Check semantic fidelity before inference;
  preserve errata and original output instead of silently improving the test.
- **EM-320, supported_by_tests:** a trusted transport does not automatically make
  its experiment wrapper strict or durable. The wrapper needs its own preflight,
  checkpoint, non-coercion, source-binding and non-overwrite tests.

All are **existing_task B02-11** refinements, not new required scope. Reuse the
native ENDSTATE measurement primitives and 8BALL provider adapter; do not add a
second authority system or a production forecasting feature. UX implication:
show validity limitations beside any numerical score, not hidden in a footnote.

ER-01–03: preserve probability, conditional route, observed outcome, source
error and recognition as different facts about the experiment. ER-04–06: the
useful next check is independent input review and a genuinely unseen outcome,
not repeated calls to improve this answer. ER-07–10: retain all three findings;
no held-out, human or production gate is promoted. ER-11–12: no course or action
changes; all unprocessed context and summarisation limits remain explicit.
ER-13–14: first-run code/input/raw response, preparation failures and errata stay
recoverable and distinguishable from later repairs. ER-15: suggesting a question
does not establish operator value; no benefit or calibration measure was tested.

## Handoff

- **Session/environment:** Devin; https://app.devin.ai/sessions/dba6fbb6c7fc4ec0ad09d1333b6ab159.
- **Task/objective:** B02-11 integration-owned historical diagnostic, not acceptance.
- **Branch/base:** `devin/1792969169-roadmap-integrated` /
  `3ddaa2f42f88b0bdb8ad41212f454b01588e29b4`.
- **Files:** `evals/historical_replay.py`, preserved case/outcome fixtures,
  `tests/test_historical_replay.py`, source/response/audit evidence and delivery records.
- **Implementation:** v1 was uncommitted at inference, with its exact runner
  archived after the call; do not attribute it to the later hardened v2 commit.
- **Evidence:** [audit and artifact hashes](../../evidence/historical-replay-audit-2026-10-26.json),
  [actual forecast](../../evidence/historical-replay-forecast-2026-10-26.json),
  [resolution](../../evidence/historical-replay-resolution-2026-10-26.json),
  [post-forecast control](../../evidence/historical-replay-planning-control-2026-10-26.json).
- **Status:** B02-11 remains partial; reserved lane ownership and acceptance are unchanged.
- **Remaining:** predictive ability, calibration, independent labels/source review,
  full live forecast-loop integration and production acceptance are unverified.
- **Publication:** see [PR #6](https://github.com/EmotiveImpact/8ball/pull/6) and
  source-bound closeout; no merge, deployment, release or public SDK publication.
- **Next:** design independently reviewed, predeclared forecasts on genuinely
  unseen outcomes with a task-appropriate baseline and enough resolved cases.
  Another renamed famous case is not a clean validation substitute. Recheck the
  retained protocol without inference using
  `python -m pytest -q tests/test_historical_replay.py tests/test_forecasting.py`.
