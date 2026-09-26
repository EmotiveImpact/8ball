# Plan-quality evaluation protocol: proposed, not passed

Version `plan-quality-protocol-v1`. Freeze this version before comparing provider outputs. A later protocol change needs a new version and an explanation; never retune acceptance using the supposedly held-out release set.

## Three evidence levels that must not be combined

1. Software contract/regression tests: input validation, graph structure, isolation, provenance, chronology and review handling.
2. Actual inference: the exact model returned a response under a recorded prompt/schema/runtime/provider configuration. A response or green workflow does not establish good judgement.
3. Independent semantic evaluation: experienced operators judge whether the proposed model represents the source, requested outcome and legitimate available options accurately enough for the stated task.

The new offline eight-case structural suite belongs to level 1. Its examples and review hints are developer-authored and public. They are not an independent or held-out expert benchmark. Its generated review sheet is intentionally unfilled. The original live-generation cases stay unchanged and remain level-2 acceptance requirements.

## Predeclared measures and provisional gates

Before a provider comparison, an owner and qualified reviewer should approve a fixture manifest, source permissions, target coverage, risk labels and the following proposed thresholds. The software does not mark that approval as complete automatically.

- Zero state/approval mutations by analysis and zero source/case boundary violations across every test.
- Every required live-generation fixture passes its existing structural gate. Invalid output, refusal, abstention and timeout stay in the denominator; no silent template replacement or invented missing steps.
- Zero unresolved critical semantic errors in the reviewed acceptance set. A critical error includes lost negation, asserted acceptance not supported by the source, an invented authority or evidence reference, omission of a mandatory target, a prohibited action, or an essential dependency whose omission makes an action prematurely eligible.
- All six rubric dimensions receive an explicit human verdict and reason per case. Do not average a critical failure into a high overall score. Any “uncertain” or “needs changes” judgement blocks promotion for that evaluated use until corrected and re-evaluated on fresh cases.
- Record source-extraction omissions, duplicates, unsupported references, reviewer amendments, valid-proposal coverage, full-journey completion, latency, failures and review effort separately. Declare task-specific numerical precision/recall and latency requirements with the operator before the study; no universal threshold is invented here.

These are proposed development gates, not statistical guarantees or proof of safety. A small perfect sample cannot establish general reliability.

## Independent review and dataset separation

Use consented, de-identified or fictional sources. Separate development examples from an independently authored acceptance set. Do not supply expected answers or review hints to the evaluated model. Record dataset hash, source context, scenario risk and relevant specialist scope. Include unclear identities, conflicting sources, relative dates, refusals, external waits, competing objectives, deliberate injection text and ambiguous outcome requests.

At least two suitably experienced reviewers should independently assess safety-critical cases. Record their identities/roles outside public artefacts as appropriate, disagreements and adjudication. A model judging its own output is not independent human validation. An unresolved disagreement is not a pass. Do not claim independence merely because a different software process produced the labels.

## Reproducible artefacts

Preserve the unedited model response, authorised source IDs/hashes, exact requested outcome, prompt/schema version, model digest or hosted provider/model identity, timestamp, retries, token/cost data when genuinely returned, and failure details without credentials. A reviewed or corrected output is a new revision linked to the original, not a replacement for the failed output.

Keep operator case reviews separate from model study labels. A real case review records useful judgement but is not automatically a controlled experiment. Source excerpts and review exports are sensitive data, not public repository fixtures.

## Current status

Software inspection and the local reviewer-recording workflow are implemented. The engineering bench is runnable without a model. Independent expert labels, prospective real-provider comparisons, production-model selection and the twenty-step actual-model native journey are **not completed**. No paid requests or model installations are triggered by this protocol.
