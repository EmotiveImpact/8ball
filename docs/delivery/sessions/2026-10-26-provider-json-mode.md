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

Finish native software verification and retain a source-bound receipt. Then
connect bounded propose → specialist challenge → revised proposal using native
ENDSTATE compilation and current-authority worker checkpoints. Retain the initial
proposal and every reviewer answer; do not use a majority vote or automatically
commit a plan. The next frozen fictional inference diagnostic must include the
exact selected GLM/DeepSeek variants and must not claim empirical prediction.
