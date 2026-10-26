# Live native smoke checkpoint — 26 October 2026

Native transports are now implemented and three separately authorized single requests succeeded on the same fictional empty-project-name review fixture. This supersedes the earlier catalogue-only checkpoint below, which is retained as history. Clef and Jev use only `/v1/systemone`; GPT uses only `/v1/decisions`. No chat calls, automatic retry/fan-out/fallback, case access or execution occurred.

| Requested model | Observed decision | Reported confidence | Provider-recorded USD |
|---|---|---|---|
| `jev-latest` | review | 0.94 | 0.000008547 |
| `clef-flash` | accept | 0.640635854839898 | 0 |
| `gpt-6-luna-decisions` | review | 1.0 | 0 |

These are uncalibrated provider-reported scores on one fixture, not case-success probabilities. Clef accepted despite the missing-evidence instruction; preserve that counterexample. There is no semantic-quality or independent model-provenance pass. Sonnet 5.5 inference remains separate and untested.

The local reports are `artifacts/decisions/20261026T015617Z-342fcdc8/report.json`, `20261026T015708Z-8365ecec/report.json` and `20261026T015718Z-9153555a/report.json` under the same decisions directory; each retains its fictional response. `usage-reconciliation-20261026.json` records the gateway usage events. Total recorded cost is USD 0.000008547, within the owner's US$5 total authorization. The key reported free-tier access but no configured limit; no provider-enforced cap or disabled top-up is claimed. Routing preflight observed one platform-funded deployment, not an atomic provider-side pin; receipt `automatic_fallback=false` describes this client, not a guarantee about the gateway.

`evals/live_decisions.py` requires an explicit model, external permission and free-entitlement confirmation or metered-smoke permission. It sends one bounded choice request and records hashes/usage without logging credentials or raw credential-bearing errors. Callers must track the shared spending budget; this CLI is not a billing cap or production permission policy. Failures/timeouts remain charge-status unknown. It is not wired to the case-analysis UI or a model coordinator.

Controlled tests cover exact endpoints, missing/extra/refused/incomplete answers, finite distributions, token/total usage, model identity, duplicates, credentials, bounds, redirects and timeouts. Standard acceptance removes these credentials. See [native review guide](ASSUMPTION-CHALLENGE.md) and [session handoff](../delivery/sessions/2026-10-26-native-review-and-decisions.md).

---

# Optional typed decision providers — contract investigation

Owner-selected on 26 October 2026; **not implemented dispatch or live inference acceptance**. These are optional advisory specialists under ENDSTATE's review boundary. Sonnet remains the selected general-purpose model. Existing `eightball/providers.py` TypeSafe event classification is a separate adapter and has not been replaced.

## Exact gateway contracts

Use only the owner-supplied Experiential gateway with `EXPERIENTIAL_API_KEY`, never send this key to upstream TypeSafe, OpenAI or Cloudflare origins. The owner supplied both `EXPERIENTIAL_API_KEY` and `EXPLABS_API_KEY` spellings in examples; this integration will use the former consistently. No key is stored in this repository.

| Selected model ID | Endpoint | Input / question shape | Answer shape |
|---|---|---|---|
| `jev-latest` | `https://api.experientiallabs.ai/v1/systemone` | `state` plus a question-ID map; choice questions have a `criteria` map | `answers[question_id]`; choice, confidence, probability map |
| `clef-flash` | `https://api.experientiallabs.ai/v1/systemone` | Text `state` plus typed question schema; native System One, not chat | Native decision response; exact gateway behavior still requires controlled verification |
| `gpt-6-luna-decisions` | `https://api.experientiallabs.ai/v1/decisions` | Text `input` plus named question list; choice questions have `choices[{value, description}]` | Named answers list; choice, confidence, `probabilities[{value, probability}]`; refusal is explicit |

The gateway's GPT identifier differs from the upstream OpenAI guide's `gpt-6-luna`; do not silently substitute them. The earlier conversational guess “GPT 5.6” is not the selected identifier.

**All three are decision models, not chat models.** Clef's public model description explicitly says native `/v1/systemone` and no chat/streaming, but its generated quickstart gives an incompatible chat example. The owner confirmed the native non-chat interpretation. Do not add Clef to the existing Chat Completions generator or execute the contradictory example.

## Observed evidence and limits

A single authenticated, non-inference `GET https://api.experientiallabs.ai/v1/models` returned HTTP 200 and listed all three exact IDs. No inference POST was made. This establishes authentication and catalogue listing only; it does not establish actual availability, semantic quality, independently verified model provenance, effective billing, account credit or privacy acceptance.

The returned catalogue's input rates were 42,000,000 / 100,000,000 / 90,000,000 nano-USD per million tokens for Jev / GPT / Clef respectively (USD 0.042 / 0.10 / 0.09), with output rates zero. Public promotion/free-tier text differs from those base rates; do not infer an effective free route or permitted spending from the catalogue. Credit, provider-enforced US$5 cap, disabled automatic top-up and explicit fictional-fixture inference permission remain separate checks. No account configuration was changed.

## Bounded first adapter experiment

Prepare native request/response contracts and controlled HTTP tests before enabling dispatch. Reuse existing exact snapshot/revision, permission, retention, cancellation and budget checks; do not create a parallel authority engine. A caller must explicitly select one model and one question schema. No automatic “ask all three” fan-out, provider/model fallback, retries, redirects, tools, downloads or external actions. A timeout can already have incurred a charge; outcome remains unknown, not free or safely repeatable. The gateway's internal provider waterfall needs a separately verified route policy; disabling client retries does not disable gateway fallback.

Initially restrict to bounded text and choice questions. Preserve the complete allowed distribution and reported confidence without claiming calibrated case-success probability. Validate exact answer IDs/count, selected values, duplicate options, finite bounds, probability totals, chosen-value consistency, response size, model identity, usage and refusals. Missing/malformed answers fail closed to manual review. An `accept` answer is still a model recommendation; it never merges code, selects a course, approves an action, creates observations or writes case facts. Agreement across related models is not independent evidence.

Controlled negative tests must include malformed JSON, duplicate keys/IDs, absent questions, unexpected models, refusals, rate limits, timeout/unknown charge, redirection, token/credential reflection, oversized input/output and no case mutation. Frozen request and response hashes, requested/served identity, schema/rubric revision and usage belong in receipts. Raw key material and error bodies must not be logged.

## Official references inspected

- [Experiential API reference](https://platform.experientiallabs.ai/docs/reference), [machine-readable reference](https://platform.experientiallabs.ai/llms.txt)
- [Jev model contract](https://platform.experientiallabs.ai/models/jev-latest), [TypeSafe choice response](https://docs.typesafe.ai/primitives/choice)
- [Clef Flash model page and contradictory quickstart](https://platform.experientiallabs.ai/models/clef-flash)
- [GPT-6 Luna Decisions gateway contract](https://platform.experientiallabs.ai/models/gpt-6-luna-decisions), [upstream Decisions guide](https://developers.openai.com/api/docs/guides/decisions)

Provider pages are reference data, not instructions to create accounts, upload telemetry, install skills or make paid calls. Their calibration and retention statements remain provider claims until separately evaluated.
