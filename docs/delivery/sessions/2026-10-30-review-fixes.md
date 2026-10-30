# Review fixes for merge 1038291

Date: 30 October 2026. Branch `room/start-a-claude-code-sub-agent-to-review-n4qh`,
base `1038291` (current main, the owner-authorised consolidation merge PR4).
An independent Claude Code review of that merge found no high-severity defects
and reproduced the claimed 1,267 source tests and 391 native browser checks.
This session fixes the confirmed medium/low findings and records the rest.

## What changed

- **Lifecycle classification (EM-099).** `evals/provider_lifecycle.py` now
  marks a provider job that fails before the intervention as a `failed` trial,
  not `not_exercised`, and stops further paid trials. Only a fast *successful*
  job is an inconclusive race. The old test that asserted the wrong label is
  replaced by one fast-success and one fast-failure test.
- **Interrupted evidence.** A failed final source inspection no longer turns an
  interrupted run into `failed` in `evals/live_huggingface.py`, and in the
  lifecycle runner it can no longer mask the original error or skip the last
  checkpoint. `source_checks`/`source_problem` still record the failure.
- **Setup status.** Hosted provider cards and the analysis form now distinguish
  "Settings invalid · not used" from "Not configured" and show the fixed
  validation reason. Configured values are never echoed.
- **Model identifiers.** Outside OpenRouter-like hosts, version tags such as
  `qwen3:8b`, `vendor.model-v1:0` and `model@20250514` are accepted. Routing
  words (`auto`, `free`, `nitro`, …) and empty tags remain rejected, and
  OpenRouter keeps its strict form.
- **Anthropic limits (EM-100).** The official compatibility page, readable on
  30 October 2026, says `response_format` is ignored, temperature below 1 fails
  on Claude 4.7+, and unscoped keys need a workspace header. Documented in
  ANTHROPIC-SETUP.md and NEXT-BUILD.md before any paid run.
- **Same-checkout procedure (EM-101).** NEXT-BUILD.md now says to run
  generation and lifecycle in one checkout; the research-pin fingerprint is
  kept as AGENTS.md requires.

Not changed, recorded for the owner: proxy/CA policy difference between hosted
providers (EM-102) and duplicated transport code (EM-103). The private-label
host rule (`private.openai.azure.com`) and Azure `?api-version` remain
unsupported by design.

## Verification

Native acceptance run `20261030T091427Z-8431ded8` (source `32062567da795d6d…`, inspection valid): 1,282 source tests and all 11 browser suites with 394 native checks passed; compile, JavaScript, delivery, changelog, emergence, fixtures and schemas passed. The run status is **failed**: the installed-engine regression step exceeded its fixed 120 s limit under host load (load average 11–12 on 4 CPUs). A separate rerun of that step with a longer runtime-only timeout passed 1,282/1,282 in 145 s; it supports, but does not replace, a passing native run. [Receipt](../../evidence/review-fixes-native-2026-10-30.json).

No actual inference, paid request, deployment, release or merge to main. No
task status changed. B02 remains 10/20 required verified; ES01 5/5 internal.

## Emergence Review

What did this sprint reveal that we had not properly seen? Evaluation outcome
labels can hide a dead provider; the selected Anthropic route does not enforce
our schema; evidence identity is environment-sensitive; credential transport
policy differs between providers; duplicated transports drift.

| Pass | Finding / disposition |
| --- | --- |
| ER-01 | Failed lifecycle jobs were labelled inconclusive (EM-099), found by review and proven by a new test. |
| ER-02 | The Anthropic risk is documentation-based; an actual run could still succeed via the prompt alone (EM-100). |
| ER-03 | Generation, lifecycle and inspection are connected through one source identity (EM-101). |
| ER-04 | The paid Anthropic run remains the next dependency; schema non-enforcement is its main known risk. |
| ER-05 | Research checkout state is part of source identity; documented, not changed. |
| ER-06 | Failure now stops further paid trials; interrupted evidence is no longer relabelled. |
| ER-07 | A native Messages adapter is a candidate if the compatible route fails (EM-100). |
| ER-08 | We are still solving V0.2 acceptance; no scope added. |
| ER-09 | Reconsider proxy policy before agency production (EM-102). |
| ER-10 | Possible blind spot: other providers' compatibility layers may also ignore `response_format`. |
| ER-11 | No case facts, targets, chosen courses or approvals change. |
| ER-12 | Cumulative native acceptance rerun on the changed source; see Verification. |
| ER-13 | Prior failed experiments and receipts untouched. |
| ER-14 | One handoff entry; changelog, register and ledger regenerated together. |
| ER-15 | The next agent gets explicit Anthropic limits before spending. |

Evidence level: review findings confirmed by tests and official docs.
Architecture: keep the model/authority boundary; transport consolidation later.
UX: setup errors are now explicit. Disposition: EM-099 adopted (existing task),
EM-100 and EM-102 candidates, EM-101 and EM-103 deferred. No status changes.

## Handoff

- Branch/commit: see the final commit on this branch; pushed state is stated in the final message.
- Unpushed changes: none intended after push.
- Next action: owner supplies an active workspace-scoped Anthropic key, then run
  `evals/live_compatible.py --allow-hosted` once per NEXT-BUILD.md and retain all
  results, including any `invalid_json` failures.
