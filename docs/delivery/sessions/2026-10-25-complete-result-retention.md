# Complete bounded processing-result retention — 25 October 2026

Base `98ee073a1c5f25658aab915183c696c8b4099985`; branch feat/agency-authorisation-20261025, draft PR5.

GitHub access recovered. The previous local closeout 98ee073, including browser-review screenshots and exact-source evidence, was pushed and its remote branch head verified. Previous authentication-failure receipts remain historical evidence; publication is no longer blocked.

EventWork now accepts complete UTF-8 result text up to 500,000 bytes, matching the supported hosted response-envelope bound without importing a provider adapter into the queue. It does not truncate, repair or replace output. This corrects the demonstrated rejection of an ordinary 16,501-character fictional graph. Exact original text survives restart, reviewed consumption and audit export. Over-limit text is rejected without changing the running attempt; the trusted caller must preserve oversized transport failures separately, as the provider evidence contract requires.

36 focused work/review tests passed, including three new regressions: full graph restart retention, UTF-8 exact/over-bound handling, and full graph review/export identity. Full native verification follows. Actual model calls and authenticated background-worker dispatch remain unfinished; the larger bound alone does not complete those gates.

## Emergence Review

What did this reveal? The processing boundary should match the real provider envelope in bytes, while preserving original output identity (EM-110, EM-112).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | Continue the full existing 8BALL/ENDSTATE goal. |
| ER-02 | Keep provider-independent queue storage and existing model transport limits. |
| ER-03 | Preserve result text through work, explicit review and export. |
| ER-04 | Authenticated dispatch, production accounts/storage and real-model/human acceptance remain unfinished. |
| ER-05 | Retention success does not establish semantic quality or action authority. |
| ER-06 | Existing scope, token, cancellation and review permission checks are unchanged. |
| ER-07 | A UTF-8 byte boundary correctly handles multibyte text. |
| ER-08 | Reject over-limit output visibly; never truncate or automatically retry. |
| ER-09 | Assert exact raw result equality after restart and review export. |
| ER-10 | Keep the original oversized-result failure evidence. |
| ER-11 | No course, observation or approval changes without existing reviewed commands. |
| ER-12 | Test full graph, exact boundary and multibyte over-bound cases. |
| ER-13 | Oversized provider transport failures still require separate raw evidence retention. |
| ER-14 | Publish the previous closeout, then commit this correction and its actual verification. |
| ER-15 | Reviewers can now receive a complete ordinary graph result through the queue; operator/model usefulness remains unproven. |

Disposition: existing ES02-02/04 implementation correction. No new application, deferred research runtime, merge, deployment or paid inference.
