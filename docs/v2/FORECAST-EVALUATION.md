# Forecast evaluation: measurement is not prediction

The native planner calculates conditional routes. No empirical outcome predictor is currently wired into the app. The Jev/Clef/GPT fictional decision smoke establishes transport compatibility, not predictive skill. A model's choice confidence is not automatically a calibrated event probability.

`endstate.forecasting` adds provider-free, read-only measurement contracts:

- `Forecast`: a binary event, information cutoff, horizon, input digest, predictor identity and either a bounded probability or an explicit abstention reason.
- `Resolution`: an exact forecast digest, explicit Boolean result, available-at time, source reference/digest and synthetic/observed basis. This is an evaluation record, not a case observation command or independent source attestation.
- `evaluate`: scores only resolved, non-abstained forecasts with Brier loss; reports coverage, absent outcomes and abstentions separately. It compares the same scored subset with a preregistered fixed 0.5 baseline and reports that baseline over all resolved rows separately. No predictions means no skill score, not perfect accuracy.

Duplicate/unknown identifiers, mismatched forecast hashes, nonfinite probabilities, naive clocks, future/premature resolutions and mixed synthetic/observed evaluation sets fail closed. The conservative resolution contract requires the full event horizon to have elapsed, including for positive results. No storage, provider call, action approval, execution, calibration claim or human review is implied. Hashes bind bytes; they do not prove the author withheld future information, prospectively registered the prediction or supplied truthful outcomes.

## Current diagnostic

```sh
python evals/prediction_bench.py --output artifacts/prediction-new-run
```

The directory must not already exist. The runner prepares six fictional cases, freezes their inputs and planning results, then reads separately stored hypothetical outcomes. Three identical-context pairs represent supplier delivery, client acceptance and repair confirmation; each pair has opposite author-created outcomes. No real person or client is used. This is an underdetermination demonstration, not an independently blinded or representative benchmark.

The real ENDSTATE planner returns a conditional route for each case, preserving unknown waits, approvals and an unevidenced goal. It does not return an event probability. The harness therefore records six explicit `not_configured` forecast gaps; these are not model refusals or successful model abstentions. Result: **0/6 forecast coverage, no predictive score, empirical prediction NOT TESTED**. The fixed-half baseline's Brier loss of 0.25 measures only these synthetic labels; no model has beaten it.

## Before claiming predictive skill

### Historical replay diagnostic (26 October 2026)

The separate `evals/historical_replay.py` experiment uses the native application
provider transport and these ENDSTATE scoring contracts; it is not an app
forecasting endpoint or production feature. One actual Sonnet 5.5 response gave
a masked 2018 acquisition a 0.45 completion probability. It did not complete:
Brier 0.2025 against the fixed-half 0.25. **The model admitted recognising the
transaction/outcome, and the author found two source-summary errors. This result
is inconclusive, not predictive-quality evidence.** See the
[retained report, errata and exact chronology](../delivery/sessions/2026-10-26-historical-replay.md).

The initial v1 input and response remain unchanged. The later v2 runner has only
offline protocol tests: both `--allow-inference` and `--allow-external` are
required, the direct Anthropic model is pinned, requests are bounded and never
retried, inputs are persisted before inference, and runs/resolutions cannot be
overwritten. A simple author-created conditional planning control is explicitly
not an event probability or a full historical model. The first actual response
preceded that control; no later changes retroactively improve it.

Outcome files stay separate; the v2 resolver also requires their `case_sha256`
to match the exact frozen case. Only public authorised data may enter this
experiment. No JSON schema or word blacklist can establish historical cutoff
integrity or semantic fidelity. Require independent source review before a new
quality study; a negative self-report of recognition is not proof of blindness.

### Unfinished quality requirements

1. Define the event, horizon, target population, outcome source and permissioned information cutoff before inference.
2. Configure one explicit forecast-producing adapter; record its model/version, complete input/response hashes, budget, usage and missing outputs. Do not turn arbitrary choice confidence into outcome probability silently.
3. Freeze forecasts before learning outcomes. Separate training/tuning from evaluation and use time-appropriate data. An old public event may already be in a model's training data, so retrospective results need that limitation.
4. Resolve outcomes from independently justified sources, preserving unavailable, disputed and unresolved results rather than converting them to false.
5. Compare with an appropriate declared baseline on the same cases; report sample size, coverage, uncertainty, subgroup failures and calibration. Retain counterexamples. Synthetic tests remain separate from real-world validation.

Forecasts may inform a human's review but cannot select a course, establish facts, approve actions or execute anything. Named-person psychological prediction and cross-client learning are outside this implementation.
