# Explicit provider JSON contract — 26 October 2026

## Scope and source

Owner-authorised continuation on `devin/1792969169-roadmap-integrated`, starting
at `b9b58dcebc3cf67b0d62aa1fe1985b8c68f9c93b`, for
[PR #6](https://github.com/EmotiveImpact/8ball/pull/6). Changes are local and
uncommitted at preparation; no merge, deployment or release.

The authenticated catalogue reports no structured-output capability for the
owner-selected `glm-5.3-uncensored`. The optional server-owned
`EIGHTBALL_API_JSON_MODE=prompt_only` deliberately sends the unchanged strict
schema in the prompt without a remote `response_format` constraint. It is not
an automatic fallback. Compatible default `json_schema` and native Anthropic's
existing prompt-only protocol are preserved. Invalid configuration fails before
HTTP; explicitly requesting a forced native Anthropic schema is not silently
downgraded.

Response mode is frozen with session settings, exposed in configuration status,
and retained with each call's schema/input/instructions and exact request hashes.
Local JSON parsing, typed proposal validation, target-quotation coverage and
compilation are unchanged. Invalid output stops, remains retained, and is not
repaired or retried. The setting is removed from ordinary acceptance's environment
alongside provider credentials and operator database settings.

## Verification

- 261 focused transport, application, CLI and acceptance-runner tests passed
  (one existing Starlette/AnyIO deprecation warning).
- Python compilation and `git diff --check` passed.
- The first direct source run selected an incorrect, nonexistent Node path:
  96 failed, 2070 passed and 6 skipped. Its output is retained in ignored
  `artifacts/provider-json-mode-20261026/initial-path-failure.log`. The installed
  Node v24.19.0 path is now verified; integrated native/wheel verification remains
  pending. No UI testing agent or live model request was used for this change.

These are controlled-HTTP/software checks, not actual GLM or DeepSeek inference,
semantic quality or prediction evidence. Original recognised historical inputs
and all failed experiments remain unchanged. No further recognised-case replay
is planned.

## Emergence Review

EM-326 / `existing_task` B02-11: unsupported remote schema enforcement need not
mean unsupported strict local validation. The selected contract must be explicit
before dispatch, not weakened in response to a failure. The original catalogue
observation is retained and its decision history is appended, not rewritten.

ER-01–10: selected transport capability became explicit; no new reality graph,
information action, clock, identity, detector, target, source authority, route
selection or watch behavior is introduced. Invalid prose/fenced/non-finite JSON,
extra fields, wrong value types and missing target quotations still fail. A
valid response is advisory, not factual evidence or action approval. Model quality
and operator value remain unmeasured.

ER-11–15: retain provider configuration in auditable receipts, preserve single
model versus independent-panel versus coordinated-method identity, keep shared
ENDSTATE versus product-host authority separate, and do not adopt research code,
new products or optional scope. All original human, independent quality,
production and release gates remain open. Reserved lane owners and acceptance
statuses are unchanged.

## Next action

Native software verification is complete (checkpoint below). Next connect
bounded propose → specialist challenge → revised proposal using native
ENDSTATE compilation and current-authority worker checkpoints. Retain the initial
proposal and every reviewer answer; do not use a majority vote or automatically
commit a plan. The next frozen fictional inference diagnostic must include the
exact selected GLM/DeepSeek variants and must not claim empirical prediction.

## Source-bound verification checkpoint

Functional commit `e1e714276cbdd400c76a121337c7f0cf0b17991d` passed native run
`20261026T114121Z-9fa4e813`, source digest
`b7ab9ea110242fc01f2cc339dcc4db2fc91dd75b7179e9c3334fac3ecf025c4a`:
**2172 source tests, 2172 installed-wheel regressions, 24 JavaScript modules and
475 checks across 13 native browser suites**. All guards and Python compilation
passed. The source was unchanged during the run. `--inspect` returned valid=true
before this documentation-only closeout; later documentation is not that tested
snapshot. The [receipt](../../evidence/provider-json-mode-software-2026-10-26.json)
binds the complete compressed report. Earlier path failure remains retained.

This checkpoint and its documentation closeout are published on the existing
branch/PR, not merged or deployed. No runtime work is omitted from that checkpoint.
Remote `progress` and `verify` passed at preceding pushed head `b9b58dc`; current
push checks must settle separately. Devin Review remained errored without a job
ID or findings at that head and earlier heads; no review gate is bypassed.

Emergence correction: the preparatory implementation history was appended to
EM-325 instead of EM-326. Both original notes are retained; appended decisions
explicitly correct the link. Passing provider-contract tests is not coordinated
method evidence. B02-11 stays partial, including independent labels, prospective
approval, held-out data and human acceptance. No live request was made in this
slice and no new product scope was adopted.
