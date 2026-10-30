# Test Anthropic from the cloud environment

The owner selected Anthropic on 18 October 2026. The current app has a generic
OpenAI-compatible hosted transport. These are **prepared compatibility-test
settings**, not a successful Anthropic call or a native Messages adapter.

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
| Environment variables | `EIGHTBALL_API_MODEL` | `claude-sonnet-4-6` |
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

## What has actually been checked

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

Consequently the first authorised actual response must establish compatibility.
Do not assume a strict-schema request means the service enforces that schema.
Keep every current local JSON, source, graph and final-verification gate. A
rejection, unsupported field, prose, refusal or invalid graph remains a failure;
no output repair, automatic retry, provider switch or catalogue substitution.
If the actual service demonstrates an incompatibility, retain the failure and
implement a separately verified native adapter without changing acceptance.
No Anthropic SDK dependency or upstream runtime has been installed.

## Documented compatibility limits, read 30 October 2026

The [official compatibility page](https://platform.claude.com/docs/en/api/openai-sdk)
was readable on 30 October 2026. It documents, without any actual call:

- `response_format` is **ignored**. Our strict JSON schema is therefore not
  enforced by the service; conformance relies only on the system instruction
  and the existing local JSON/schema/graph gates. Fenced or prose-wrapped JSON
  fails as `invalid_json` and is never repaired. Expect this risk before paying.
- `temperature` 0 is accepted for `claude-sonnet-4-6`. Claude 4.7 and later
  models return HTTP 400 for any value below 1, so switching the configured
  model to a newer Claude family fails before inference with the current
  transport. Do not change the transport's temperature to pass; that is a
  separate, verified change.
- Personal or service-account keys not scoped to a workspace need an
  `anthropic-workspace-id` header, which this transport does not send. Use a
  workspace-scoped key.
- Anthropic describes the layer as intended for testing, not production; native
  structured outputs require the Messages API. A native adapter remains a
  separately scoped task.

Documentation is not an Anthropic response. Only the first authorised actual
run establishes compatibility.

## After settings are active

Follow [actual-provider evidence](ACTUAL-PROVIDER-EVIDENCE.md), using the existing
`openai_compatible` transport and configured API-provider identity `anthropic`:

```sh
.venv/bin/python evals/live_compatible.py --allow-hosted
```

This is a deliberate real inference command, not a configuration check. Run it
only after observing active credentials/network settings and confirming service
limits within the existing fictional-only US$5 authorisation. Preserve all raw
failures, requested/served identities, source/prompt/compiler versions and times.
Generation makes up to five requests and never retries automatically.

Only after matching successful generation proceed to lifecycle and native
actual-provider journeys. Genuine independent professional and human acceptance
remain separate; the owner reviews usability/visuals at the agreed end.
