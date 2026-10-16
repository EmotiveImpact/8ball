# Connect a hosted Qwen model: beginner setup

A hosted service runs Qwen and gives 8BALL an API connection. You do not need
to install Qwen or Ollama on your computer or this environment. This optional
connection uses the existing source, outcome, validation and human-review flow.

## 1. Get the connection details

If someone is already giving you an endpoint, skip creating another account.
Get its public API base URL, exact model identifier and private API key through
their secure process. Share only the public URL/model in chat, then follow
section 2. If the service uses no key, tell the agent so it can check compatibility.

The suggested starting service is **Alibaba Cloud Model Studio**, Qwen's
official hosted service. Start at [Alibaba Cloud](https://www.alibabacloud.com/)
and find Model Studio, or use a provider you already have.

1. Create an account and open Model Studio. Select your service region.
2. Open API-key management and create a key. Keep it private.
3. Choose an available Qwen chat model; copy its **exact API model identifier**.
4. Copy the **OpenAI-compatible API base URL** for that same region and key.

The international example is
`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`. Other regions have
different URLs. Use your provider's URL; omit `/chat/completions`, which 8BALL
appends. This build accepts hosted HTTPS DNS endpoints on port 443.

The model must support JSON-schema structured responses. Availability and
compatibility need an actual test. You can share the exact model name and public
API URL in chat. **Never paste the private API key into chat.**

Check billing settings; there is no assumed free quota. A token limit does not
guarantee a money ceiling. Agree a small test budget before any billed call.
Only the repository's fictional fixtures are intended for the initial test.

## 2. Enter the settings securely

Open this Codex cloud environment's settings and review the prepared draft.
It suggests Alibaba's international endpoint; edit it if your region/provider
differs.

| Setting | What to enter |
| --- | --- |
| Secret **Qwen API key** / `EIGHTBALL_API_KEY` | The private key from your model service |
| `EIGHTBALL_API_BASE_URL` | The HTTPS API base URL |
| `EIGHTBALL_API_MODEL` | The exact model identifier |
| `EIGHTBALL_API_PROVIDER` | Provider identity, e.g. `alibaba-model-studio` |

The secret's allowed destination must match the API hostname. The proposed
draft uses `dashscope-intl.aliyuncs.com`. Tell the agent the public URL if it
differs so it can adjust the destination/network settings; keep the key private.

**Save and Publish** the configuration. This persists settings; it neither calls
a model nor proves that the running task has received them. The agent checks
observed readiness and restarts the application when settings are active.
Keep keys out of source files, command arguments, browser storage and exports.
A separately operated server can use its own secret manager/environment with
the same setting names.

## 3. What the agent will verify

The [actual-provider evidence guide](ACTUAL-PROVIDER-EVIDENCE.md) describes unique
retained generation runs, deliberate lifecycle trials and their limits.

Configuration checks send no request. The Intelligence page shows **Hosted API /
Qwen**, model, host and configured/not-tested status. The browser receives no
private key. Select this provider for source analysis or graph drafting; each
hosted analysis requires explicit permission to send the selected information.

Once settings are active and the fictional test budget/transmission is agreed:

```sh
.venv/bin/python evals/live_compatible.py --allow-hosted
.venv/bin/python evals/full_journey.py --provider openai_compatible --allow-inference --allow-external --transport native
```

These deliberate model calls may be billed. They do not run on import, status
checks or ordinary acceptance. The first uses the unchanged four generation
fixtures/compiler/pass gate and writes
`artifacts/compatible/<unique-run>/compatible-report.json`. The second runs a disposable
fictional journey and retains its own report. Cancellation, stale results and
interruptions also need selected-provider checks.

The transport makes no automatic retries, provider switches, downloads, JSON
repair or catalogue substitutions. It retains model identity, prompt/schema/input
hashes, timings, usage and bounded rejection evidence. Unsupported structured
output, refusal, truncation and invalid JSON remain failures. For exact Alibaba
DashScope hosts it explicitly disables thinking mode for the non-streaming
structured-response contract.

Engineering success is separate from independent semantic evaluation and human
acceptance. The owner still reviews usability/visuals at the end. Model suggestions
do not establish facts, change the target or authorise actions.

## OpenRouter or another service

Other hosted OpenAI-compatible services use the same base URL/model/key settings.
OpenRouter additionally needs `EIGHTBALL_API_PROVIDER=openrouter` and one explicit
`EIGHTBALL_API_ROUTING_PROVIDER` from its provider list. The request pins that
provider and disables fallbacks. Strict JSON-schema support must be tested.
An explicit catalog model ending `:free` is accepted on the exact OpenRouter
endpoint; the random `openrouter/free` router is rejected. This is syntax and
identity support, not a claim that a model is currently free or available.

The existing Hugging Face connection retains its own `HF_TOKEN`,
`EIGHTBALL_HF_MODEL` and `EIGHTBALL_HF_PROVIDER` settings.

Official API reference:
[Qwen through the OpenAI-compatible API](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions).
UI labels, availability, terms and prices may change; this guide does not claim
that an account, subscription or connection has already been tested.
