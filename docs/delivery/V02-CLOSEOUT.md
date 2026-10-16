# Latest evaluation readiness, 16 October 2026

The [technical direction](../strategy/OWNER-TECHNICAL-DIRECTION-2026-10-16.md) makes the component choices understandable and keeps all deferred runtime research separate. On `feat/v02-evaluation-readiness-20261016`, [actual-provider tooling](../v2/ACTUAL-PROVIDER-EVIDENCE.md) preserves unique generation runs, exact returned assistant text and explicit lifecycle observations. Its final software receipt is separate from actual-model acceptance. All ten required scopes below remain unchanged. The owner already authorises fictional tests up to US$5 with free access expected; the actual service URL/exact model and active secure configuration remain missing. Do not repeat the permission question or infer model access from this coding conversation.

# Current consolidated closeout

Read [BUILD-OVERVIEW](BUILD-OVERVIEW.md), [HANDOFF](HANDOFF.md), [the integration session](sessions/2026-10-15-main-consolidation.md) and [ADR 0006](../decisions/0006-consolidated-development-main.md). The owner authorized combining current source and documentation into main as a development build. All ten required V0.2 scopes listed in the historical table below remain unfinished at their recorded states; integration does not change acceptance.

The old “fix the actual-model planning failure first” instruction has a completed bounded prompt/schema clarification and controlled replay at 8fad411/821d9f5. Subsequent graph focus and failure-provenance/navigation corrections are included through 486c85e. Fresh selected-model generation remains blocked; no model has been selected/authorized or installed in this cloud session. Use the original four frozen fixtures without repairs/substitution, then actual-provider lifecycle/native journey and independent/human reviews. Prepared recording materials are in [review/README](review/README.md). The owner will perform their review at the end; qualified independent review remains separate.

## Preserved original closeout snapshot

The snapshot below retains its original evidence and requirements. Historical source/status and merge-authority paragraphs yield to the newer exact source, canonical ledger and ADR0006. No requirement is waived.

---

# Current V0.2 closeout: work to do, in order

Snapshot: 15 October 2026, application `290e310707cf8bef6caf2508c285312b091bd18b`. This is a work-plan view of [the canonical tracker](progress.json), not an independently editable status ledger. Refresh live source and evidence before starting.

## Completed baseline

Published source is alpha.8, tree `214c4835869dbe70f7c6ff6811977e5bb5a62841`. Native CI `36219680306` passed 938 code tests, 938 installed-kernel tests and 378 checks in eleven Chromium suites. Source Desk race correction is included. ES01-05 is verified, completing the five internal-core scopes; it is not a public SDK release.

B02 required verified scopes are B02-01..08, B02-13 and B02-17: 10/20. Optional B02-21/B02-22 emergence work is not secretly added to the release denominator. The complete required remainder is below.

| Required ID | Recorded state | Remaining evidence / task |
| --- | --- | --- |
| B02-09 | blocked | Genuine new-source graph proposals with every reference, meaningful alternatives and explicit final verification; no template substitution or repaired-output pass. |
| B02-10 | partial | Independent multi-source extraction/identity/date review preserving negation, uncertainty, quoted support and explicit scheduling adoption. |
| B02-11 | partial | Approved expert-labelled held-out data and predeclared semantic/omission/correction/latency/abstention thresholds; model selection based on actual results. |
| B02-12 | blocked | Complete actual-provider twenty-step integration plus genuine human judgement and native persistence/export, not only scripted fixture choices. |
| B02-14 | partial | Professional longer-source/duplicate/reconciliation review; preserve original/excerpt lineage and native race/download checks. |
| B02-15 | partial | Selected real-provider cancellation, interrupted/stale result handling and accurate runtime/model/credential status. |
| B02-16 | partial | Human screen-reader review and supported-browser/OS startup/error/loading checks. Chromium automation is not all-platform accessibility certification. |
| B02-19 | partial | Owner review of black/graphite design, legibility, status/target/provider controls and mobile usability without expanding the design scope. |
| B02-20 | implemented | Representative dense-case graph comprehension and broader usability/accessibility; existing graph controls and audit invariants already pass native checks. |
| B02-18 | blocked | All required scopes evidenced, then explicit final integration/release decision. No implicit merge or tag. |

## Workstream A: fix the actual-model planning failure first

The most recent recovered experiment is **27 September 2026**, run `36340454120`, artifact `10938777673`, archive SHA-256 `62a09fe447cea0d6f76d17b2a8bf13a77f816cd2ddcb3fc17f60dd0b7b98dce0`. It ran the application above, not the old alpha.7 source. The runner wrapper is on the ops branch; it is not a new app version.

Model: `qwen3.5:4b`; recorded Ollama `0.34.3`; model digest `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd`. These identify the historical experiment, not a recommendation to download a model now.

Results: three extraction fixtures schema-valid; novel supplier graph rejected with `DraftFailure`, code `result_bypasses_verification`, path `/routes`, message `Step results must not duplicate or bypass readiness and final verification`. All four live states unchanged. `semantic_accuracy_evaluated=false`, `production_approved=false`.

Read [raw report](../evidence/qwen-baseline-2026-09-27.json), `endstate/compilation.py`, `eightball/v2/intelligence.py`, `evals/live_generation.py`, `evals/generation-cases.json` and `tests/test_endstate_compilation.py`. Inspect the raw frame/routes to determine where readiness/final verification is duplicated. Propose the smallest prompt/schema/compiler clarification that preserves the rule, add a regression and rerun the original fixtures deliberately. This is the next engineering task, not a new feature screen.

The unchanged generation fixture hash is `6758c54a9e873bf2f67ced368555b871d9cf890b55b4df33762a035be1deaeb3`. It is a known four-case regression, not an independent holdout. Do not tune on it and then call it independent model validation.

No Hugging Face key or selected provider/model is available in the recovered work. The owner said they would provide credentials later. Never request a secret in chat/PR/code. Use approved server-side configuration and deliberate external-transmission permission. No new paid calls, downloads or upstream installations are authorised by this documentation handoff. JEV/GLiClass remain optional and separately evaluated; the old GLiClass result was not production acceptable.

## Workstream B: prepare and obtain real quality judgements

Use `evals/PLAN-QUALITY-GATE.md`, `evals/plan_review_bench.py`, the existing unfilled review sheet and independent professional input. Freeze cases, historical cut-offs, rubric and thresholds before the final evaluation. Preserve target drift, false authority, negation errors, missing dependencies, unsupported dates, poor alternatives and corrections even when JSON validates.

Owners needed: authorised provider setup from the project owner; independent reviewers for source/plan judgement; explicit approval of protocol/labels. An agent can prepare and run tooling but must not sign as an independent human operator. Do not invent a passing sheet to remove a blocker.

## Workstream C: verify the real-provider lifecycle and full journey

Read [acceptance-runner guide](../v2/ACCEPTANCE-RUNNER.md) and [hosted-development policy](../v2/HOSTED-DEVELOPMENT.md). Its historical references to ten browser suites are superseded by the current eleven-suite runner and native receipt.

After deliberate provider setup and permission, the current full-journey interfaces are:

```sh
python evals/full_journey.py --provider ollama_staged --allow-inference --transport native
# Only with explicitly authorised hosted configuration and external transmission:
python evals/full_journey.py --provider huggingface --allow-inference --allow-external --transport native
```

The runner includes scripted review and synthetic verification observations for its engineering fixture. This is valuable integration evidence, not independent semantic acceptance or proof of a real outcome. Also test cancelled and stale work against the selected actual provider; an in-flight external request may still finish/be billed.

## Workstream D: complete operator and accessibility review

Use the existing black interface and graph, representative fictional cases, supported environments and `docs/v2/ACCESSIBILITY.md`. Record screen-reader/keyboarding results, source interpretation, dense graph comprehension, loading/errors, exact-target comparison, review burden and source/approval explanations. Fix regressions; do not use owner feedback as permission for unrelated new screens or a framework rewrite.

## Always preserve software regression evidence

```sh
python -m pip install -r requirements-dev.txt
# Explicit development dependency/browser setup, not an automatic model installation:
python -m pip install 'setuptools==82.0.1'
python -m playwright install chromium
python scripts/acceptance.py --mode native --base <your-actual-starting-commit>
python scripts/acceptance.py --inspect <matching-run-directory>/report.json
```

Run with disposable fictional data. Keep mode, exact source hash, all failures and actual provider call counts. `--inspect` validates a report's integrity, not that its run passed. A native policy block is a block, not permission to disguise a bridge as native. The prior CI pass does not automatically validate subsequently changed source.

## Last step, not a shortcut

Update statuses only with genuinely matching evidence in `progress.json`; regenerate its checklist. When every required B02 scope passes, obtain the explicit final decision, perform the agreed cumulative PR #2 integration and superseded #1 cleanup, and label/tag the accepted version. These are future actions, not performed by this document. V0.3 agency security and the deferred research remain later work.

No defensible time estimate follows from test counts or checkbox percentages. Scope stays fixed; blockers and actual evidence control completion.
