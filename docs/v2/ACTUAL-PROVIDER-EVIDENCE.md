# Actual-provider evidence: retained experiments and lifecycle trials

Read with [Qwen setup](QWEN-SETUP.md), [acceptance runner](ACCEPTANCE-RUNNER.md)
and the [independent/human review pack](../delivery/review/README.md). These manual
commands may call a paid service. Ordinary acceptance strips provider settings
and makes no model calls. Tooling tests do not establish actual-provider,
semantic or human acceptance.

## Prerequisites

Use the latest source and configure the owner's exact endpoint/model/provider
and private key securely. The owner already authorises fictional repository
examples up to US$5 and expects free access. Confirm actual service limits and
provider-enforced spending controls before paid use. Fictional case budgets and
token limits are not an inference dollar ledger.

The compatible transport requires hosted HTTPS DNS:443, a nonempty key and
strict JSON-schema support. OpenRouter also requires an exact routing provider.
Explicit catalog `namespace/model:free` variants are supported only on the exact
OpenRouter host; `openrouter/free` and automatic routing remain rejected.
Availability, free entitlement and selected-endpoint support still need testing.

## 1. Run unchanged frozen generation

Only after actual configuration and access are ready:

```sh
.venv/bin/python evals/live_compatible.py --allow-hosted
```

The program prints its report path. Each invocation creates a unique timestamp/
UUID directory under `artifacts/compatible/`; `--output` selects an output root.
Hugging Face uses the same scheme under `artifacts/huggingface/`. Earlier
fixed-path reports remain historical and are not overwritten or treated as fresh.

Schema-2 reports retain source fingerprint/commit, prompt/compiler versions,
provider/model/host, unchanged fixture hash, input hashes, timings and returned
transport traces. Numbered exclusive checkpoints bracket each fixture. The
current report within that run updates atomically; earlier runs and checkpoints
are never replaced. Write failure prevents starting a subsequent fixture.

`actual_hosted_requests` records a nonempty transport-attempt trace, including a
denied or timed-out attempt. It does not establish successful remote inference.
Inspect individual HTTP/status/served-model/returned-text records. The fixture
runner continues after individual errors; check authentication before starting
it to avoid a sequence of redundant denied requests.

Current reports also record `source_checks`, `source_at_finish` and
`source_unchanged_during_run`. Source is inspected before each fixture and final
success. Observed drift or an inspection error is sticky, blocks later fixtures
and fails the evidence gate even if every returned structure passes. Raw returned
responses and partial checkpoints remain. These discrete checks cannot prove
continuous stability or which code was loaded; a graph's internal second stage
can already have started before the next check. Do not edit source during a run.

Compatible receipts preserve exact bounded assistant text on success and
attributed rejection, plus separate literal-text, canonical-output and outer
HTTP-body hashes. UTF-8, credential-reflection, size, refusal, truncation and
schema guards remain. HTTP error bodies, headers/cookies and full outer envelopes
are not retained. This archives assistant output, not every transport byte.

SIGTERM/Ctrl-C records interruption where possible. SIGKILL leaves the last
durable checkpoint; an in-flight response can be unavailable. Checkpoints bracket
fixtures: a graph's internal first stage is not durably saved until the proposal/
trace returns. Missing evidence stays explicit. Never repair, retry or substitute
a catalogue output into the original evaluation denominator.

## 2. Exercise application lifecycle against the selected provider

After successful generation from the same source/provider, replace the run ID:

```sh
.venv/bin/python evals/provider_lifecycle.py --provider openai_compatible --allow-inference --allow-external --generation-report 'artifacts/compatible/REPLACE_WITH_RUN_ID/compatible-report.json'
```

The runner checks a complete schema-2 receipt, all four exact fixtures and the
original structural gate, per-fixture returned-call evidence, stable final source,
endpoint host,
requested model and routing provider. This is an unsigned engineering receipt,
not independent approval. Changed source/configuration requires fresh evidence.
Older reports lacking source-stability/returned-call records cannot establish
this prerequisite. Existing failures remain historical, without fabrication or
retroactive filling of missing records. Host identity does not distinguish
different API base paths on the same host; review that residual configuration
limitation before interpreting a receipt as evidence for a changed service path.

It starts only its own disposable local app/database and submits one graph job
per fresh case for cancel, metadata supersession and actual owned-process restart
against the same database. It never reuses or kills an unrelated server.
Checkpoints retain case/job snapshots, hashes, interventions, counts and available
proposal traces in unique `artifacts/provider-lifecycle/` directories.

**Timing is application call admission.** `calls_started` increments before
HTTP. These trials do not prove remote delivery, completion, billed usage or
provider-side cancellation. Cancelled/interrupted jobs publish no proposal, so
their response/served-model receipt may be unavailable; that reason is recorded.

Exercised trials require the expected terminal state, no proposal/unintended
case mutation, only the first admitted stage and no later observed work. Fast
results winning the race are **not_exercised**, making the run inconclusive;
there is no automatic repeat. Timeouts stop further trials. Cleanup terminates
only the owned process, even if client close fails. The recorded post-terminal
observation interval is bounded and is not continuous monitoring.

A pass supports only these local application lifecycle observations. Remote/
model evidence, native UI behaviour and human acceptance remain separate gates.

## 3. Run the native actual-provider journey

```sh
EIGHTBALL_BROWSER=/usr/bin/chromium .venv/bin/python evals/full_journey.py --provider openai_compatible --allow-inference --allow-external --transport native
```

Use that browser path only when present. The journey retains its own unique
artifacts and scripted engineering choices; it is not the original human PRD
walkthrough or independent semantic evaluation. Keep every failed attempt.

Generation makes up to five requests: three extraction cases and a two-stage
graph. Lifecycle submits three graph jobs once each; a timing race can allow a
second stage, which is reported rather than retried. The journey also performs
extraction/graph calls. Confirm aggregate service limits/cost before the sequence.
Cancellation cannot recall requests already sent.

Independent evaluation still needs prospectively approved qualified reviewers,
held-out labels, thresholds and adjudication. Owner usability/visual and qualified
screen-reader/platform reviews remain human tasks. These runners do not accept a
model for production, authorise case actions, merge, release or deploy.
