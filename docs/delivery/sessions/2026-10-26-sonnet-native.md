# Sonnet native integration — 26 October 2026

## Scope and source

B02-09/B02-11/B02-12 on `devin/1792969169-roadmap-integrated`, starting from
`3c758b51389dcee5fdc02679136cfa98dce9db37`. Existing
[PR #6](https://github.com/EmotiveImpact/8ball/pull/6), not merged or deployed.
Functional checkpoint is local pending full native regression and publication.

Owner explicitly authorised bounded Sonnet 5.5 fictional tests within US$5,
confirmed sufficient credit/top-up off, and accepted an uncapped account. No
dashboard login, account setting change or persistent secret change was needed.

## Implementation

Exact direct Anthropic host/provider/base selects native Messages before sending.
The application provider ID stays `openai_compatible`; transport receipts state
`anthropic_messages`. Other endpoints are unchanged. Native headers, bounded
streaming, text blocks, exact served-model checks and native usage reuse the
current proposal path. Thinking/signatures are not proposal content. Tool use,
refusal, truncation, bad JSON/usage, credential reflection and invalid local
grounding/graphs remain rejected. No remote schema enforcement is claimed.

Prompt `endstate.draft.prompts.v3` explains the existing exact target-quote
coverage rule, including connectors. Compiler/version/validators and frozen
fixtures are unchanged. No output repair, automatic retries or model fallback.
Lifecycle prerequisites now match the configured actual transport protocol.

## Actual results and preserved failures

Lossless compressed reports and hashes: [evidence index](../../evidence/sonnet-native-2026-10-26.json).

| Run | Actual result | Requests | Usage-based USD |
| --- | --- | ---: | ---: |
| Original compatibility | HTTP 400; exact cause unknown | 1 | unknown |
| Separate native probe | HTTP 200, served Sonnet 5.5 | 1 | 0.000288 |
| First native frozen set | 3 extractions pass; frame quote coverage rejects omitted `and` | 4 | 0.021042 |
| Fresh prompt-v3 frozen set | all 4 fixtures pass; 3 conditional routes | 5 | 0.035742 |
| Actual-provider native journey | all 20 scripted steps, reload/download and audit pass | 3 | 0.031428 |

Known Sonnet estimate totals **US$0.088500** at US$2/M input and US$10/M output;
prior specialist reported cost was US$0.000008547. These are not verified invoices.
Rejected requests have unknown billing, not zero. Requests were manually bounded
with 4096 output tokens each and no retries; no global dollar ledger/account cap
is claimed. No further paid calls are needed for this slice.

Each run preserved source stability. The passing generation preceded one
test-only fixture correction; the subsequent native journey uses that correction
with identical runtime code. These full-tree manifests are not interchangeable.
Earlier Sonnet 4.6 failures remain intact, with no invented explanation.

Disposable journey cases use scripted accept/edit/reject and explicitly synthetic
observations. Model answers never establish real facts or authorise actions.
Live cancellation/stale/restart testing was not run; native controlled HTTP tests
cover these boundaries, not remote recall or billing cancellation.

## Verification

375 focused compiler/grounding/compatible/lifecycle/retention tests passed.
Two new test setup defects were corrected: encode the lone surrogate as escaped
JSON bytes, and use distinct success-criterion titles before testing coverage.
Full source-bound native/wheel regression and publication will be appended.

## Emergence Review

**EM-311 — transport success is separate from generation acceptance.** Observed
live: native API worked after compatibility rejection, but the first graph still
failed local validation. `existing_task`, B02-09/B02-12: native transport and
truthful receipts belong in the product adapter, not an engine rewrite. UX must
distinguish connection, contract and quality failures.

**EM-312 — lexical coverage failure is not a semantic omission judgement.**
Both requested criteria existed while a connector was unquoted. Supported by live
output and regression; `existing_task`, B02-09/B02-11: explain the exact contract
in a versioned prompt without weakening validation. Risk: mechanical rejection
and extra prompt complexity; a passing familiar fixture is not held-out quality.

ER-01..05: explicit protocol/prompt deltas and retained source/failure/usage
bindings; four fixtures leave substantial unknown coverage. ER-06..10: no real
effects, target change, watcher, model vote or probability. ER-11: scripted review
is not human acceptance. ER-12: familiar fixtures are not representative client
coverage. ER-13: no paid retry loop/output repair. ER-14: recoverable reports and
full source manifests; native software closeout remains separate. ER-15: no
measured operator benefit or professional acceptance claim.

## Next action

Publish verified work to the existing PR without merging. Preserve reserved lane
owners and independent/human acceptance statuses. Genuine prospective protocol
approval and independently authored held-out labels are the next quality gate,
not more repeats of familiar fixtures. A future paid lifecycle experiment needs
a generation receipt matching its exact source. Prediction, production, release
and deployment remain unaccepted.
