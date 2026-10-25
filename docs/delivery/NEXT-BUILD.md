# Continue the consolidated 8BALL build

Read this on current main after the owner-authorised October25 integration.
Fetch all remote branches, inspect HEAD/worktree/open PRs and preserve newer work.
Read AGENTS.md, START-HERE.md, progress.json, latest HANDOFF and V02-CLOSEOUT.
The canonical ledger controls statuses; this is a runnable test handoff.

## What is available

The combined build includes the generic hosted provider, exact returned-output
retention, unique checkpointed experiments, source-stability checks, lifecycle
prerequisites, optional prospective study records, earlier graph/keyboard/source
fixes and all preserved research. Research remains optional source material.
ENDSTATE V0.1 remains the engine underneath 8BALL. Original PRDs, generation
fixtures, local validation and approval boundaries remain unchanged.

The remaining acceptance work needs actual provider results, independent held-out
labels/qualified reviews and human accessibility/platform/owner reviews. The
owner will review usability and visuals at the end. Do not count coding-agent
review or automated browser work as those reviews. B02 remains10/20 verified,
ES01 5/5 internally; these are scope counts, not estimates of remaining time.

## Reproduce the software checks

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt setuptools==82.0.1
.venv/bin/python -m pip check
EIGHTBALL_BROWSER=/usr/bin/chromium .venv/bin/python scripts/acceptance.py --mode native --base YOUR_START_COMMIT
.venv/bin/python scripts/acceptance.py --inspect artifacts/acceptance/PRINTED_RUN_ID/report.json
```

Use an existing native Chromium executable, or the repository CI's Playwright
installation procedure. Inspect before editing final documentation. Standard
acceptance strips model credentials and starts disposable local services.

## Prepare the actual model test

Use fresh credentials supplied securely to the execution environment. Never
copy chat credentials or private case records into source, scripts or artifacts.
The user authorises fictional repository fixtures only, with a total US$5 ceiling.
Check service pricing/limits for the whole generation/lifecycle/journey sequence;
there is no application dollar ledger and cancellation cannot recall a request.

The prepared direct Anthropic compatibility settings are:

```text
EIGHTBALL_API_BASE_URL=https://api.anthropic.com/v1
EIGHTBALL_API_MODEL=claude-sonnet-4-6
EIGHTBALL_API_PROVIDER=anthropic
```

The private value belongs in EIGHTBALL_API_KEY; its destination must permit
api.anthropic.com. See ../v2/ANTHROPIC-SETUP.md for the full guide. Runtime
readiness and an actual compatible response are separate. Native Messages and
generic completion APIs differ. The October25 native model metadata request
received401; this does not identify its origin/cause or test chat/completions.
Later configuration observations changed; do not treat that old receipt as a
current diagnosis. Generic HTTP-secret UI save failures did not identify a field;
earlier assertions that the old label definitely caused them were not established.

The owner also supplied an Experiential Labs OpenAI-client example using
https://api.experientiallabs.ai/v1 and gpt-6-luna. It is an alternative candidate,
not authenticated/tested support. If explicitly selected, use provider identity
experiential-labs and a securely supplied key scoped to api.experientiallabs.ai.
Do not silently switch from the selected provider or assume schema support.

Run the unchanged fixtures once after usable access is established:

```sh
.venv/bin/python evals/live_compatible.py --allow-hosted
```

Retain every printed unique report/checkpoint, exact assistant output/failure,
requested/served model, source/prompt/compiler identity and timing. Four frozen
cases make up to five requests. The runner continues after individual failures;
do not repeat known-denied runs. Its actual_hosted_requests flag records attempts,
not necessarily successful inference. Keep source unchanged during the run.
Fix demonstrated failures without weakening gates, repairing responses or
substituting catalogue plans. A new attempt remains a separate experiment.

Only after matching successful generation:

```sh
.venv/bin/python evals/provider_lifecycle.py --provider openai_compatible --allow-inference --allow-external --generation-report artifacts/compatible/PRINTED_RUN_ID/compatible-report.json
EIGHTBALL_BROWSER=/usr/bin/chromium .venv/bin/python evals/full_journey.py --provider openai_compatible --allow-inference --allow-external --transport native
```

Lifecycle races can admit additional calls. Fast races are inconclusive and
discarded responses/billing may be unknown; do not automatically retry.

## Genuine acceptance and continuity

Use review/README.md, the unperformed human walkthrough and unchanged
evals/PLAN-QUALITY-GATE.md. Agree prospective thresholds/qualified reviewers and
independently authored held-out labels before the independent study. Optional
recording-v2 checks do not grant approval or invalidate legitimate manual v1 work.

Every sprint: update changelog.json and progress.json, preserve discoveries in
emergence.json, answer ER-01..15 in the handoff, regenerate canonical documents,
test actual source, commit/push a development branch and report remaining gates.
The authorised consolidation does not authorise deployment or a release label.
