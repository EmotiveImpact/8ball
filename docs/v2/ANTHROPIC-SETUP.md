# Test Anthropic from the cloud environment

The owner selected Anthropic on 18 October 2026 and **Sonnet 5.5, not Opus** on
26 October. Direct Anthropic now uses **native `/v1/messages`**, through the
existing `openai_compatible` application provider slot. Other hosts retain their
previous wire protocol; there is no model or protocol fallback.

## Current live checkpoint — 26 October 2026

The owner explicitly authorised bounded fictional testing despite the absence
of an account spending cap, confirmed sufficient credit and automatic top-up
off. US$5 is a test budget, **not** a verified provider-enforced limit. No account
setting, persistent secret or deployment configuration was changed.

One compatibility request returned HTTP 400; its exact cause remains unknown.
A separate native probe succeeded. Native transport uses `x-api-key`,
`anthropic-version: 2023-06-01`, medium effort and the unchanged 4096 output-token
ceiling. Sampling controls are omitted. Text is validated locally; thinking and
signatures are not proposal content. Tool calls, refusals, truncation, unexpected
served models and invalid source/graph bindings fail closed. Remote JSON-schema
enforcement is **not** claimed; the schema travels as prompt instructions.

Three extraction fixtures passed. The first graph frame was rejected because
its target quotes omitted `and`, even though both success criteria were present.
Prompt v3 clarifies exact lexical coverage; no validator was weakened and no
output was repaired. A fresh unchanged four-fixture run passed, including three
conditional routes, followed by all 20 steps of the actual-provider application
journey with native reload/download.

Retained successful responses imply **US$0.088500** at the checked public rates
of US$2/M input and US$10/M output tokens. This is a usage-based estimate, not an
invoice; rejected-request billing is unknown, not assumed zero. No automatic
retries. All examples are fictional; scripted reviews and observations occur in
disposable test cases, not real cases.

See [current handoff](../delivery/sessions/2026-10-26-sonnet-native.md) and
[evidence index](../evidence/sonnet-native-2026-10-26.json). Independent semantic
quality, prediction, human acceptance and production remain open. Historical
observations below retain what was known before this checkpoint.

## What goes where

Create an API key in the [Claude developer platform](https://platform.claude.com/).
API usage needs API billing/credits; a Claude chat subscription does not itself
configure this application's API access. The existing authorisation remains
fictional repository examples only, at most US$5; confirm service pricing/limits
before actual calls. Do not paste a private key into chat or this public repo.

Open the cloud environment settings:

| Section | Name | Value |
| --- | --- | --- |
| Secrets | `EIGHTBALL_API_KEY` | Your private Anthropic API key |
| Environment variables | `EIGHTBALL_API_BASE_URL` | `https://api.anthropic.com/v1` |
| Environment variables | `EIGHTBALL_API_MODEL` | `claude-sonnet-5-5` |
| Environment variables | `EIGHTBALL_API_PROVIDER` | `anthropic` |

Edit the **existing** secret slot for `EIGHTBALL_API_KEY`, currently labelled
**Qwen API key**. Its label does not choose a model service. Change its
**Allowed destinations** from `dashscope-intl.aliyuncs.com` to
`api.anthropic.com` (hostname only), then supply the Anthropic key securely.
You may rename the label if the interface allows. Do not create another secret
targeting the same variable. Leave `EIGHTBALL_API_ROUTING_PROVIDER` unset.

The agent saved the three non-secret suggestions and added `api.anthropic.com`
to custom network destinations, preserving existing network settings. The
configuration service rejected changing the existing secret target automatically:
it requires that edit in environment settings. No draft changes were saved by
the rejected attempt; the subsequent non-secret/network save succeeded. No
secret value was read, copied or supplied by the agent.

**Save and Publish** after entering the key and changing its allowed destination.
A draft save alone does not activate settings. The agent checks observed runtime
readiness and restarts only its own application process when required. This
neither deploys the application nor proves successful model access.

## Historical pre-inference observations — 26 October 2026

The session-only key authenticated a read-only `GET /v1/models` request (HTTP
200, complete list, no inference). It lists `claude-sonnet-5-5` as active.
This establishes catalogue access, not inference entitlement, account credit,
provider-enforced spending limits or model quality. No global environment,
deployed application or saved secret was changed by this check. The example
configuration is opt-in and is not automatically loaded.

The official [Sonnet 5.5 migration guide](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)
requires omitting sampling controls. The direct `api.anthropic.com` transport
now omits `temperature`; other endpoints retain their existing parameters.
Thinking remains the provider default, which is adaptive on Sonnet 5.5. The
4096-token output ceiling is unchanged and includes thinking; truncation is a
failure, not a reason to retry or increase spend automatically. The
[published model page](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)
lists US$2/million input tokens and US$10/million output tokens when consulted;
confirm effective account pricing, credits, a provider-enforced US$5 cap and
disabled automatic top-up before sending inference. No application dollar
ledger currently enforces that cap.

The earlier Sonnet 4.6 fixture attempt returned four HTTP 400 rejections and
no accepted output. Its sanitized errors do not identify the cause. Do not
attribute that historical failure to Sonnet 5.5's rules. The run happened
before the required spending-cap confirmation; that was a preflight omission,
not evidence of a cap. Preserve the [failed receipt](../evidence/anthropic-compatible-2026-10-26.json.xz).
No further inference is authorised to proceed until that preflight is verified.

The now-readable [compatibility documentation](https://platform.claude.com/docs/en/api/openai-sdk)
describes this endpoint as a test/comparison layer, not the preferred production
integration, and says `response_format` is ignored. Requesting a strict schema
does not mean it is enforced remotely. Keep local validation and all existing
acceptance gates; a native Messages/structured-output adapter is separate work.

## Historical setup checks — 18 October 2026

The current app accepts these setting formats without DNS or HTTP and constructs
`https://api.anthropic.com/v1/chat/completions`. An isolated check used a fictional
key, reported `configured_not_tested`, and left authentication/inference false.
Existing controlled transport tests are software checks, not Anthropic responses.

The official [Python SDK at bcd55fe](https://github.com/anthropics/anthropic-sdk-python/tree/bcd55fe1d3f0f1240765f8cef04295b67337f55a)
lists [claude-sonnet-4-6](https://github.com/anthropics/anthropic-sdk-python/blob/bcd55fe1d3f0f1240765f8cef04295b67337f55a/src/anthropic/types/model.py#L21).
That does not prove account availability, entitlement or current pricing.
Its native API uses `/v1/messages`, `X-Api-Key`, `anthropic-version`, content
blocks and `output_config.format`; those differ from the existing generic
transport. The official [OpenAI-compatibility documentation](https://platform.claude.com/docs/en/api/openai-sdk)
was blocked by the inherited proxy with HTTP 403. This does not establish an
Anthropic-origin response. No bypass was attempted.
Readable SDK/cookbook source did not establish the compatibility endpoint's
Bearer authentication, accepted parameters or `response_format` enforcement.

At that checkpoint, the first authorised actual response still had to establish compatibility.
Do not assume a strict-schema request means the service enforces that schema.
Keep every current local JSON, source, graph and final-verification gate. A
rejection, unsupported field, prose, refusal or invalid graph remains a failure;
no output repair, automatic retry, provider switch or catalogue substitution.
If the actual service demonstrates an incompatibility, retain the failure and
implement a separately verified native adapter without changing acceptance.
No Anthropic SDK dependency or upstream runtime has been installed.

## After settings are active

Follow [actual-provider evidence](ACTUAL-PROVIDER-EVIDENCE.md), using the existing
`openai_compatible` application slot and configured API-provider identity
`anthropic` (native Messages on the exact direct Anthropic host):

```sh
.venv/bin/python evals/live_compatible.py --allow-hosted
```

This is a deliberate real inference command, not a configuration check. Run it
only after observing active credentials/network settings and confirming service
limits and disabled automatic top-up within the existing fictional-only
authorisation. The owner accepted the uncapped account for these bounded tests;
do not claim a provider-enforced US$5 limit. Preserve all raw
failures, requested/served identities, source/prompt/compiler versions and times.
Generation makes up to five requests and never retries automatically.

Only after matching successful generation proceed to lifecycle and native
actual-provider journeys. Genuine independent professional and human acceptance
remain separate; the owner reviews usability/visuals at the agreed end.
