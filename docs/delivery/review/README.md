# V0.2 acceptance review pack

Prepared 15 October 2026. These are **unperformed review materials**, not acceptance evidence or a second progress tracker. Task states remain in [progress.json](../progress.json). Use a private copy for completed forms, identities, sources and audit exports; this repository is public.

## Start the review

1. Record the exact tested Git commit, model/provider, prompt/compiler versions, dataset hash, browser/OS and review time in each form. Preserve original model outputs and failed attempts before making corrections.
2. The project owner will review the application at the end. Prepare the [human walkthrough](HUMAN-ACCEPTANCE.template.md) for that session. Owner review can cover usability and visual decisions; it does not supply independent professional labels by itself. Establish reviewer qualifications and independence separately.
3. For independent quality evaluation, copy [protocol.template.json](protocol.template.json) and agree the missing values with the owner and qualified reviewer **before** running the held-out study. Then make one [case-review.template.json](case-review.template.json) copy per case, provider configuration, attempt and reviewer. Keep reviewers' initial judgements separate. Safety-critical cases require at least two suitably experienced reviewers under the existing protocol.
4. Complete the human walkthrough on a disposable fictional case using the actual selected model. Record observed results, failures and evidence, including corrections. A blocked or unperformed item stays `BLOCKED` or `NOT_RUN`. Do not sign from the scripted journey report.
5. Return findings for fixes. Repeat affected checks against the corrected source, retaining earlier failed evidence. Only matching completed evidence can support a proposed ledger update; integration/release authority is a separate explicit decision.

No provider, numerical threshold, reviewer approval or completed acceptance is filled in by these templates. Nulls and empty arrays mean **not supplied**, never zero errors or a passing result. Template JSON is a recording aid, not a machine-enforced gate validator. Do not use an overall score to hide a critical failure.

## Existing contracts and evidence

| Purpose | Authoritative material | Use |
| --- | --- | --- |
| All required scope/status | [Canonical generated tracker](../PROGRESS.md) and [ledger](../progress.json) | B02-09/10/11/12/14/15/16/19/20 remain open; B02-18 awaits all gates and an explicit final decision. |
| Prospective semantic protocol | [PLAN-QUALITY-GATE.md](../../../evals/PLAN-QUALITY-GATE.md) | `plan-quality-protocol-v1` is proposed, not approved. Its existing critical-error and six-dimension rules remain unchanged. |
| Case-local plan judgement | [Plan Review](../../v2/PLAN-REVIEW.md), [rubric source](../../../endstate/plan_review.py) | Record live-snapshot judgement; it does not attest facts, approve actions or supply a controlled independent study. |
| Public known generation regression | [generation-cases.json](../../../evals/generation-cases.json) | Four unchanged cases; canonical SHA-256 `6758c54a9e873bf2f67ced368555b871d9cf890b55b4df33762a035be1deaeb3`. These have been used for development and are not held out. |
| Reviewer familiarisation | [Existing unfilled engineering sheet](../../evidence/plan-review/human-review-sheet.json) | Eight public developer-authored cases include review hints. Keep them out of the independently authored acceptance set; do not feed answer hints to the evaluated model. |
| Historical actual inference | [Raw Qwen failure](../../evidence/qwen-baseline-2026-09-27.json) | Preserve failed graph and schema-valid extractions; no independent semantic pass. |
| Latest prior software evidence | [Graph native receipt](../../evidence/graph-keyboard-native-2026-10-15.json), [generation receipt](../../evidence/generation-role-contract-2026-10-15.json) | Source-bound software results at their stated code commits, not a model or human pass for later source. |
| Original human journey | [Original PRD §34](../../reference/8BALL-V0.2-ASTRA-PRD.md#34-v02-definition-of-done) | Twenty steps retained verbatim in the walkthrough; the original PRD is immutable. |
| Provider boundaries | [Hosted development](../../v2/HOSTED-DEVELOPMENT.md), [analysis jobs](../../v2/ANALYSIS-JOBS.md) | Selected service/model, deliberate transmission permission, no silent downloads/retries, no promise to recall an external request. |
| Human interaction scope | [Accessibility](../../v2/ACCESSIBILITY.md), [Source clarity](../../v2/SOURCE-CLARITY.md), [Source Desk](../../v2/SOURCE-DESK.md), [graph](../../v2/GRAPH-EXPLORER.md) | Use current source/ledger/native receipts for current results; older environment-blocked paragraphs remain historical. |

## Running the engineering prerequisites

Use the current pushed development branch containing all earlier fixes, rather than checking out the older application branch from an old README. Set up the existing development dependencies and use a disposable database. Launch the app with `.venv/bin/python -m eightball`; its local operator token is for sign-in, not a provider key. Keep that token out of screenshots and retained reports.

The model running this coding conversation is not automatically a provider for the application. Local Ollama needs a running service and selected installed weights. Hosted Hugging Face needs a selected model/provider, securely configured `HF_TOKEN` and deliberate external-processing permission. A runtime listing weights proves neither successful inference nor model quality.

After the selected model/runtime and permission are available:

```sh
# Local Ollama: export the selected installed EIGHTBALL_OLLAMA_MODEL first.
EIGHTBALL_GRAPH_PROVIDER=ollama_staged .venv/bin/python evals/live_generation.py
EIGHTBALL_BROWSER=/usr/bin/chromium .venv/bin/python evals/full_journey.py --provider ollama_staged --allow-inference --transport native
```

Use `/usr/bin/chromium` only when present on the actual review machine. The full-journey runner uses synthetic engineering observations and scripted review, and always distinguishes itself from full human PRD acceptance. Its twenty checks are not the original twenty human steps. Hosted use follows the separately opted-in command in [the runner guide](../../v2/ACCEPTANCE-RUNNER.md); do not add external permission to a local-only run.

Collect provider-call count, raw parsed output/diagnostics, timestamps, elapsed time, model identity/digest where returned, source hashes and unchanged-state evidence. Failed responses remain in the evaluation denominator. Keep unavailable metrics null, and mark loss of evidence explicitly. Do not substitute repaired or catalogue output. The hosted fixture runner now creates unique checkpointed run directories; earlier fixed-path reports remain historical. Use the [actual-provider evidence guide](../../v2/ACTUAL-PROVIDER-EVIDENCE.md) for generation, lifecycle and native journey. Local lifecycle admission counters do not prove remote receipt or billing.

The developer runs cumulative native acceptance after runtime changes. Human screen-reader/platform, source interpretation, dense-case comprehension and owner visual judgement remain human tasks. No merge, deployment or deferred research is part of this pack.
