# ENDSTATE Lab: ordered experiment queue

Specification only. No experiments on this page are reported as run by the consolidation. [Original Lab plan](../reference/endstate-handoff-2026-09-24/03-ENDSTATE-LAB.md); [source register](ENDSTATE-REGISTER.md); [milestone placement](../strategy/ROADMAP-INTEGRATION.md).

Current V0.2 acceptance takes priority. New Lab execution, upstream installation or a second product must be scoped and authorised separately. Keep experiments isolated from runtime dependencies and client state.

## Baseline ladder

Reproduce upstream honestly -> establish a simpler baseline -> find failure modes -> freeze held-out evaluation -> run permitted shadow mode -> propose bounded product adoption. Compare current kernel, kernel plus hand-authored scenarios and kernel plus model-generated scenarios on the same held-out cases.

| Lab ID / original research | Hypothesis and first experiment | Evidence for promotion |
| --- | --- | --- |
| A / R02 | An investigation frontier helps decide what to learn next. Compare current question impact, simple dependency ranking, model ranking and independent operator ranking. | Useful missing questions found; irrelevant questions and review burden measured; no blocked action authorised. |
| B / R01 | Premise links explain which decisions require reconsideration. Retract/update sources, alter authority, change guards/resources and include unrelated updates. | Correct affected dependencies and preserved history. Do not narrow conservative approval invalidation without its own authority tests. |
| C / R03-R05 | Hand-authored adverse worlds expose fragile routes and useful fallbacks. Start from immutable revisions and vary one assumption/family at a time. | Exact deterministic replay; zero live-state mutation; explicit scenario coverage and source/assumption boundaries. |
| D / R04-R05 | Model-proposed stress cases find useful failures beyond C. Bound permitted perturbations and actual call/time/cost exposure. | Independent judgements of new useful contingencies versus false assumptions; same unchanged acceptance thresholds; raw outputs retained. |
| E / operational/behavioural prediction | Timing, reply/no-reply, meeting/no-meeting, objections and stall outcomes can be forecast on authorised data. Use synthetic data only to test plumbing, never to establish human calibration. | Compare historical-frequency/statistical/rules/expert/LLM baselines; temporal and case holdout; calibration, uncertainty, abstention and errors. |
| F / possible worlds | Multi-actor simulation improves a decision beyond single-event forecasts and deterministic stress tests. | Demonstrated incremental benefit; bounded amplification of uncertainty; no fluency-based score or synthetic-frequency success claim. |
| Pack proof / R06 | One engine accepts fixer, sales and support vocabulary/policy. | Versioned pack fixtures, no `eightball` application import from Sales, no planner fork or cross-case leakage. |
| Research continuity / R07 | A new session can recover scope and unresolved decisions without chat memory. | Source-linked register, explicit dispositions, intact originals, valid links and a tested recovery path. This documentation work supports continuity, not future runtime acceptance. |

## Candidate experiment record

For each run retain: hypothesis, owner, explicit scope approval, as-of source revision, upstream commits/licences, dataset provenance, historical cut-off, baseline, frozen metrics/thresholds, protocol version, environment, selected model/provider/revision, actual calls, raw outputs, validation results, latency/cost, failures, reviewer identities/roles where authorised, limitations and promotion decision.

Prediction metrics must match the target: calibration/proper scoring and discrimination for event probabilities, interval coverage/error for timing, and independently assessed usefulness/correction burden for decision support. Predeclare thresholds instead of inventing a pass score after observing results. Do not imply synthetic fixture success is real-world performance.

Keep case-level train/development/test separation and prevent future outcomes leaking into earlier snapshots. Retain no unnecessary private data. Learning/retrieval is permissioned per matter and purpose; no silent cross-client training.

## Working layout, not folders that already contain upstream code

```text
research/lab/                 # optional future worktree/repository
  external/                  # approved pinned upstream snapshots
  source-snapshots/           # manifests and provenance
  licences/                  # rights/security decisions
  experiments/<experiment>/  # baseline, protocol, inputs, runner
  findings/                  # successes, failures, counterevidence
  benchmarks/                # separated, authorised datasets
```

No new runtime import may depend on this layout by default. A candidate graduates only through measured benefit, source/licence and authority/security review, an ADR, explicit canonical task and unchanged regression coverage.
