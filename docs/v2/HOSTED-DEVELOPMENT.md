# Hugging Face development provider

Developer adapter, not production-model approval. The current session did not have a Hugging Face key and did not make any hosted inference requests.

## Configuration later

Set these on the server, not in source control or the browser:

```sh
export HF_TOKEN='<private token>'
export EIGHTBALL_HF_MODEL='<namespace/model>'
export EIGHTBALL_HF_PROVIDER='<explicit provider>'
python -m eightball
```

Use a fine-grained token with permission to make calls to Inference Providers. Choose a currently supported model/provider combination that supports JSON-schema responses. There is intentionally no default hosted model and no automatic provider selection. Model availability and structured-output support need to be checked when credentials are configured; presence of settings is not a successful connection test.

The adapter uses the fixed Hugging Face router chat-completions endpoint. Requests explicitly name one model/provider, require JSON-schema output and cap completion tokens. No redirects, automatic retries, automatic provider/model fallback, model downloads or background paid calls are enabled. A single analysis can make two stage requests; each authorised request may incur provider charges. The application does not promise a monetary cost ceiling from the token cap.

## Data and permission

Every hosted analysis requires the operator's explicit `allow_external` choice. Extraction sends only selected source snippets. Graph generation also sends the human outcome, case brief and existing condition names/IDs; its second stage includes the proposed frame. Question generation sends minimised graph/question context, excluding embedded provenance quotations and recorded answers from unselected sources. These are still potentially sensitive case data. A checkbox is not a substitute for organisational data-processing authorisation.

Hugging Face routes to the named inference provider. That provider's own privacy, retention and security terms must be considered. Only fictional development cases are authorised in this build. Do not paste tokens into chat, a repository, a PR, an evidence record or an exported case. The status endpoint reports presence/format only; no token or token fragment is returned.

## What is validated

HTTP errors, refusals, tool-call responses, truncation, malformed/non-finite/duplicate-key JSON, oversized output and unexpected model changes fail closed. Original Pydantic contracts and exact source quotations are validated after transport processing. Receipt metadata records requested/routed model, served model identifier, input/schema/instruction hashes, usage when available, elapsed time and status. A served model ID is not necessarily an immutable weight revision; do not claim reproducibility that the provider does not expose.

The same ENDSTATE staged compiler serves local and hosted drafting. Runtime staged frames bind every proposed success criterion to an exact human-outcome quotation. Quotations must collectively cover the full target. This checks coverage/provenance, not that the criterion actually entails the outcome. Reviewers see each quotation next to its proposed criterion. Frame references are checked before the route request, and dynamic schemas allow only existing IDs. No absent operation is fabricated and no catalogue plan silently substitutes for a failed model response.

## Run the original development gate

The original four fictional fixture texts and targets are in `evals/generation-cases.json`. Their canonical hash remains `6758c54a9e873bf2f67ced368555b871d9cf890b55b4df33762a035be1deaeb3`. Local and hosted scripts consume the same file. This is a familiar engineering regression set, not an independent held-out quality benchmark.

After configuration, deliberately authorise the hosted experiment:

```sh
python evals/live_huggingface.py --allow-hosted
```

Without the flag or configuration it exits before requesting inference. The script opens no private case database. It preserves every fixture result, keeps the unchanged two-route/final-verification/state-isolation gate and writes `artifacts/huggingface/huggingface-report.json`. No hosted experiment is added to automatic CI.

A structurally valid response is not proof of a good plan. Next, independent reviewers must label target coverage, omitted conditions, unsupported authority, real alternatives, source support and review effort before selecting a production model. The failed historical Qwen and GLiClass results remain preserved.

## Local runtime checks

The Intelligence page has an explicit local-runtime check. It reads `/api/version` and `/api/tags` on loopback, with short timeouts and response bounds. It does not pull, load or run weights. An unreachable service is labelled “may be stopped or not installed”; it is not declared uninstalled. Listed weights are not proof of successful inference or model quality. Cancellation/progress jobs and broader installer support remain separate work.

## Primary API references

Documentation consulted 23 September 2026:

- Hugging Face Inference Providers, authentication, router and explicit provider suffix: https://huggingface.co/docs/inference-providers/index
- Structured outputs and provider-specific support: https://huggingface.co/docs/huggingface_hub/en/guides/inference
- Data/security boundary and downstream provider policies: https://huggingface.co/docs/inference-providers/security

These describe the provider interface, not an observed live integration in this session.
