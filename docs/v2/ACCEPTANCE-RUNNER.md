# Integrated acceptance: source bytes, evidence and scope

`0.2.0-alpha.7`, local unreleased integration checkpoint. This closes fragmentation in the **verification workflow**, not all V0.2 product gates.

## One reproducible command

```sh
python scripts/acceptance.py --mode native --base <starting-commit>
```

Run this after development dependencies and Chromium are explicitly installed. The runner installs no dependencies, downloads no models, reads no client database, calls no model provider and changes no browser policy. It uses disposable fictional databases. Core tests, package tests, generated-document guards, JavaScript syntax, structural fixtures and **all ten** browser suites form one run.

Every run gets a new directory under `artifacts/acceptance/`, a source-file manifest, an atomic report, dated steps, subprocess logs, checksums, observed JUnit counts, actual browser reports, an internal ENDSTATE wheel and exported request/response schemas. Prior reports cannot silently contribute to a new run. Modifying the source while tests run invalidates the source-bound result.

Modes are explicit. `native` requires real browser loopback navigation. `bridge` deliberately uses the existing ASGI harness and **cannot** pass native acceptance. `code` runs no browser tests. There is no fallback from one mode to another. A policy-blocked native probe produces `blocked`, not passed; a failed test produces `failed`. Exit codes: passed 0, failed 1, blocked 2. A occupied test port is not cleared by killing another process.

Run `python scripts/acceptance.py --inspect <run>/report.json` against the corresponding source. Inspection compares current source, recorded artifact bytes, step status, counts and browser transport. `valid=true` means the local evidence is intact and tied to this source, **not** that the run passed. Read `run_status` too. Hashes are not external signatures or protection from an administrator rewriting everything.

The CI workflow uses this same runner. It is configuration until actually executed; writing it does not make the unpushed checkpoint pass CI.

## ENDSTATE distribution check

The runner builds `endstate-engine` as an internal wheel with only ENDSTATE and its metadata. It installs the wheel into a temporary directory without a package index or dependency downloads. An isolated process tests imports, two conditional alternatives, approval preservation and exact JSON roundtrip. It then runs the complete code suite with the installed kernel taking precedence over the repository copy, including existing storage/wire compatibility and fictional neutral/sales/support fixtures.

This is internal reuse verification, not release of a public SDK. The old case data and audit contracts are preserved. No additional production application exists merely because a fictional domain fixture works.

## Actual model use is a different command

```sh
python evals/full_journey.py --provider ollama_staged --allow-inference --transport native
# Or explicitly configure HF_TOKEN, EIGHTBALL_HF_MODEL and EIGHTBALL_HF_PROVIDER:
python evals/full_journey.py --provider huggingface --allow-inference --allow-external --transport native
```

The first route requires an already-running local Ollama service and the selected weights. The second requires a server-side token and an explicit model/provider. No key belongs in a chat, command-line argument, source file or public artifact. The repository also has an opt-in manual workflow with a confirmation phrase; it is not triggered by a push or PR.

The actual-provider runner uses the **unchanged public supplier fixture**, real inference adapters and persisted analysis jobs. It performs a twenty-check API integration loop: blank case, source, actual extraction, mixed scripted review, exact outcome, actual staged graph, graph review, distinct plans, questions, approval, completion separated from effect, explicit synthetic reviewer evidence, replan, isolated scenario, reload/export and case isolation. Native mode additionally opens the real workspace, reloads the case and downloads its real audit. HTTP mode is clearly labelled and does not claim native acceptance.

No model output is fabricated, patched with missing actions or replaced with a catalogue. A fixture with fewer than three extracted objects fails the mixed-review step rather than inventing objects. Provider failures, refusals, absent actions and invalid graphs remain failures. Call counts are retained even on rejection; cancellation forbids publication but cannot recall an in-flight paid request.

**Scripted operator choices are not independent human judgement.** The verification observations in this harness are explicitly synthetic engineering fixtures, not real-world confirmation of a model plan. Even a passing run sets `full_prd_acceptance=false` and `independent_expert_review=false`: the all-native human workflow and independent semantic quality gate remain distinct. Do not relabel this as a complete B02-12 or B02-11 acceptance.

## Current environment boundary

In this session the legitimate native probe returned `ERR_BLOCKED_BY_ADMINISTRATOR`; policy was not changed. Ollama was unavailable, and the selected HF credentials were not configured. Direct checks of the official runtime/registry download hosts also failed DNS resolution. No actual inference or model installation occurred. The actual-provider script reports the missing prerequisites and zero started calls; it is ready for an authorised configured environment, not live-tested here.
