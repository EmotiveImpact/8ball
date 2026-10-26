# Provider rejection diagnostics — 26 October 2026

- **Scope:** existing B02-09/B02-11 transport evidence, not new model authority.
- **Branch/base:** `devin/1792969169-roadmap-integrated`,
  `b43f0560547be82ee4368a675d815ef82d5be4ad`.
- **Retained predecessor:** [first coordinated attempt](2026-10-26-coordinated-evaluation.md)
  remains failed/partial at its exact earlier source. It is not resumed or repaired.

## Change and evidence boundary

Compatible planning replies now retain a narrow diagnostic projection before
strict assistant validation: supplied nonnegative integer prompt/completion/total
counts, recognised stop reasons, and boolean/type labels for assistant role,
content, tools and refusal. Arbitrary provider fields, tool/refusal contents and
hidden reasoning are never copied into that projection. Invalid counters and
unrecognised reasons remain absent, not zero or invented labels.

Anthropic stop reasons are retained even when text content is missing, without
retaining thinking/signature blocks. Native cache accounting is unchanged.
`provider_usage` is supplied diagnostic metadata, not successful completion,
independently verified metering or billing. Successful output still requires
the unchanged model/content/JSON/usage and compiler checks. No repair, retry,
fallback, substitute model, relaxed schema or case mutation was introduced.

These changes cannot recover the omitted DeepSeek response from the first live
attempt. Null content, exhaustion and reasoning-only output are controlled test
cases, **not a diagnosis of that actual response**. GLM's original fenced JSON
remains a failure. The tests retain its fences exactly rather than stripping them.

## Verification

Controlled provider/integration/coordinated-method/specialist tests:
**463 passed**, with the existing Starlette/AnyIO deprecation warning. Includes
three actual-worker-storage fixtures proving failed receipts survive retention,
remain awaiting review, make one attempted request and leave the case unchanged.
Python compilation and whitespace checks passed. Full source-bound native/wheel
acceptance is pending at this preparation checkpoint; no additional inference.
No standalone static linter/type-checker is configured in the project.

## Native decision cost investigation

The coordinator still stops on unknown units; no conversion of generic `cost`
was introduced. Official sources inspected:

- [Experiential cost API](https://platform.experientiallabs.ai/docs/cost-api)
  describes USD inline costs for Chat/Responses/Messages and request-ID lookup.
- [Gateway reference](https://platform.experientiallabs.ai/llms.txt) documents
  native System One separately without a native cost-unit schema.
- [Gateway OpenAPI](https://api.experientiallabs.ai/openapi.json) exposes native
  `/v1/systemone` and `/v1/decisions` with empty response schemas, not a unit contract.
- [TypeSafe response types](https://docs.typesafe.ai/sdk/python/api/types/responses.md)
  document token counts, not the gateway's injected cost fields.

Earlier standalone native receipts retain generic `cost` and `is_byok`, without
currency or nano-USD fields. That does not establish that a chat-specific unit
contract applies to native decision endpoints. The first coordinated archive
also filtered currency/BYOK fields, so it cannot establish their original presence
or absence. A separate documented, request-bound usage lookup may avoid guessing
units; it must be verified and explicitly bounded before runtime adoption.

## Emergence Review

**What did this sprint reveal that we had not properly seen, specified or
understood before we built it?** A strict adapter can correctly refuse output
while losing the safe metadata needed to diagnose it. Conversely, an apparently
familiar cost field can belong to a different protocol contract.

- **EM-331, existing_task B02-09/B02-11:** implement a bounded failure projection,
  preserving unknowns and the original failed record. Evidence is controlled
  HTTP and actual local worker storage, not another provider response.
- **EM-332, existing_task B02-11:** do not inherit accounting semantics across
  protocol families. Keep cost unknown until a verified unit or an exact
  request-bound provider receipt exists. Investigation is not implementation.

ER-1–5: better engineering observability, not demonstrated operator benefit or
prediction. ER-6–10: preserve source/response hashes, original failures, absent
metadata, native cache counts and the no-hidden-reasoning boundary. ER-11–15:
no changes to courses, case facts, permissions, completion/effect separation or
client reuse. Metadata is not approval and hashes cannot recover omitted bytes.
Review burden, model quality and outcome delivery remain unproven. No new
required product scope, hidden ranking or independent quality gate promotion.

## Next action and delivery

Finish source-bound native acceptance, retain its exact report, and publish the
additive checkpoint in existing PR #6. Then verify a documented native cost
receipt path before a separately frozen diagnostic. Do not rerun the recognised
historical case or resume the first coordinated protocol. A dedicated coordinated
report UI and prospective/human quality acceptance remain unimplemented.
No merge, deployment, public SDK release or prediction claim.
