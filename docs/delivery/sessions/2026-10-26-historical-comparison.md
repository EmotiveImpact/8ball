# Corrected five-model diagnostic — 26 October 2026

## Status and scope

Branch `devin/1792969169-roadmap-integrated`, base `6c7b28fa9d2a441b6295a4471e1cd0383c994d05`, existing [PR #6](https://github.com/EmotiveImpact/8ball/pull/6). Evidence-only checkpoint: no application code or default model changed, no merge/release/deployment. B02-11 remains partial and its reserved owner is unchanged. The owner authorised running rather than further price checks, and requested a separate agent's explanation of the previous result.

The owner subsequently challenged the value of recognised historical examples. Agreed: **stop rerunning this transaction**. This is an inconclusive diagnostic, not a win. Recommend a prospectively locked, representative multi-case forecasting trial and a separately authorised real-task pilot; neither has started or been validated here. A useful practical pilot still needs an operator's actual objective, permissions and observable success criteria. No new external actions are authorised by that recommendation.

## What ran

New HR-002 retains the event, cutoff and horizon of HR-001, correcting the fee denominator and extension clause against the agreement/announcement. HR-001 and its original answer remain unchanged. The author knew the outcome; name masking is not blindness. Before inference, the manifest, model-facing context, schema/questions, band mapping, instructions, source-code hash and illustrative read-only planning control were frozen to disk. The control is not a complete merger model and was not presented as the event probability.

Five single requests, no retries or substitutions: direct Anthropic Messages for Sonnet/Opus; native `/v1/systemone` for Jev/Clef; native `/v1/decisions` for GPT-6 Luna. Models received the same corrected case context, not other models' answers or the resolution. Output contracts differ: Claude returns a continuous event probability; native models choose one predeclared point from 5%, 20%, 35%, 50%, 65%, 80%, 95%, or abstain. The selected point is an explicitly elicited estimate, **not provider confidence or option probability**. Native models also answer recognition and next-check questions. Gateway routing preflight observed one platform deployment/model, not an atomic upstream identity/fallback guarantee.

| Model | Completion estimate | Mechanical Brier (outcome false) | Recognition |
|---|---:|---:|---|
| Sonnet 5.5 | 55% | 0.3025 | yes |
| Opus 5.5 | 40% | 0.1600 | yes |
| Jev | 80% coarse point | 0.6400 | yes |
| Clef Flash | 65% coarse point | 0.4225 | yes |
| GPT-6 Luna Decisions | 80% coarse point | 0.6400 | yes |

Fixed-half baseline is 0.25. Scores are arithmetic diagnostics, not a model ranking: all five indicate recognition, precision differs, the author knew the event and this is one selected outcome, not five independent cases. No abstentions occurred. A self-report of recognition is not independent proof of memory; a denial would not prove blindness either. The original 45% Sonnet estimate cannot be compared as a controlled model-only change: the input and request changed and sampling varies.

All five prioritised antitrust progress as the next observation. No observation was obtained and no revised forecast tested. Agreement does not demonstrate that the question is optimal or useful to an operator.

## Reasoning counterexamples

- Sonnet states that closing within the first extension would still land in 2018, despite the extension reaching March 2019. Its recollection also names a different financial partner. Preserve these, rather than patching the answer into apparent success.
- Both Claude answers assume a premium absent from the masked input. Opus infers regulatory risk from fee/extension structure; that is an inference, not independently supplied evidence.
- Jev's selected 80% estimate is distinct from its 0.47 reported confidence and 0.54 probability assigned to selecting that option.

## Recovery and evidence

[Complete frozen inputs, five answers/receipts, source manifest and separate evaluations](../../evidence/historical-comparison-2026-10-26.json). Archived [inference script](../../evidence/historical-comparison-runner.py-2026-10-26.xz) and [separate scorer](../../evidence/historical-comparison-resolve.py-2026-10-26.xz) preserve exact bytes. For reproduction, restore these as `runner.py` and `resolve.py` in `artifacts/historical-comparison-20261026`; the original source data/relative paths are retained in this session. Do not execute inference again to reproduce the score.

The frozen script's unused resolution phase contained an adapter error: `source_ref` rather than `source_reference`, and a source dictionary rather than the actual outcome URL. It was found before invoking resolution. A separate post-inference scorer corrected this without editing frozen code or rerunning models, validates forecast/input/answer bindings and exact outcome-source bytes, and scores each model separately. This continues the wrapper-durability finding EM-320; freezing does not itself prove a harness is correct.

Provider usage is retained as returned; no further price lookup or account/billing change. No provider-enforced cap or independently verified invoice is claimed. The study used public historical data only and does not mutate a real case, evidence, approvals, chosen course or effects.

## Verification and delivery

149 focused forecasting, historical-runner and native-decision tests passed. Offline checks passed for native endpoints, all eight probability/abstention mappings, confidence separation, frozen hash verification and non-overwrite behavior. Both archived scripts compile. Full native software verification runs separately before publication; its exact retained report/CI status, not these model scores, determines software acceptance. The pre-existing review-service error remains unresolved unless a later completed review supplies findings.

This document is committed with its evidence and generated delivery records; the eventual commit is its Git history. There are no production source changes to cherry-pick and no unrecorded default-model switch. Local raw artifacts remain in the ignored study directory. No report's existence establishes predictive quality, a full multi-agent product journey, or real customer value.

## Emergence Review

EM-321–EM-324 refine existing B02-11: distinct uncertainty quantities; reasoning errors despite valid schemas; confounded reruns; untested value of next-question agreement. Prior EM-318–EM-320 remain relevant. No new required feature or model winner adopted.

ER-01–ER-05: probabilistic forecasts, decision confidence, factual evidence and authority remain distinct; a correction creates a new record, not a replacement, and old inputs remain stale for a different experiment. ER-06–ER-10: retrospective selection and memory can alter apparent quality; one clean-looking number hides explanatory errors; question priority remains a hypothesis; independent held-out/prospective evidence is still missing. ER-11: no human-selected course or action approval. ER-12: five selected responses, one public event, bounded facts, no representative coverage or calibration. ER-13: preserve model errors and separate scorer correction, with no paid repair. ER-14: frozen source/outputs are archived and original diagnostic unchanged. ER-15: neither more model answers nor agreement demonstrates improved real outcomes; assess operator value in an authorised practical pilot with clear success criteria and a comparison baseline.

## Software closeout and next model selection

At exact commit `cd9335f76e9a16fa285b28eb880475c38c3e1e83`, native acceptance passed: 2,152 source tests, 2,152 installed-wheel regressions, 24 JavaScript module checks, compilation/schema checks and 475 browser checks across 13 native suites. The source was unchanged and inspection matched before this documentation-only closeout. See [source-bound receipt](../../evidence/historical-comparison-software-2026-10-26.json). No application runtime code changed afterward.

The owner's next-set additions are `glm-5.3-uncensored` and `deepseek-v4.1-flash`, confirmed in the authenticated catalogue, with native Chat Completions protocol documented. No inference or pricing checks for either. GLM's catalogue lacks structured-output support, so the next harness needs an explicit prompt-only response contract and unchanged strict local validation—not a silent fallback. See [catalogue receipt](../../evidence/next-comparison-models-2026-10-26.json) and [evaluation guide](../../v2/FORECAST-EVALUATION.md). No default-model change.

The user also asked whether this used swarm intelligence. It did not: five independent requests do not demonstrate coordinated cross-challenge, plan revision or synthesis. That remains a separate build/evaluation requirement. A future comparison must distinguish single model, independent panel and coordinated workflow; even coordination cannot cure memorised historical outcomes.
