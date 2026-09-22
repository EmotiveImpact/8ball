# AI implementation and small-model strategy

Research checked 22 September 2026. Provider pages and tags can change. No live model inference, latency, peak memory or end-to-end accuracy was measured for this release.

## Jev: bounded judgement, not the whole planner

TypeSafe describes Jev as a System One model returning typed Choice, Score and Noul answers. It does not generate prose/code or run the application's workflow. Use it to classify incoming evidence, flag a potential deadline change or route a question for review. Do not ask it to own the evidence graph, exact scheduling arithmetic or authority to act.

The implemented adapter calls `POST https://api.typesafe.ai/v1/systemone`, requests `choice` over five fixed labels and defaults to the explicit model `jev-1.13.0`. It validates the response type, labels, finite probability distribution and provider confidence. A reported classification probability is not the chance of successfully resolving a situation. We have not established that Jev is open source or self-hostable.

Set `TYPESAFE_API_KEY` in the server environment, not browser code. An operator must explicitly approve transmitting the selected source to TypeSafe on each request. Only an excerpt of at most 6,000 characters is allowed. Do not enable external processing for real confidential material without an appropriate privacy/security assessment and authorisation. Missing credentials and failed calls return a manual-review error; there is no simulated success response.

Primary sources:
- https://docs.typesafe.ai/introduction/coding-agents
- https://docs.typesafe.ai/api
- https://docs.typesafe.ai/models
- https://docs.typesafe.ai/model-jaggedness/jev-1.13

## Small local alternative: GLiClass Edge v3.0

The publisher lists `knowledgator/gliclass-edge-v3.0` as a 32.7-million-parameter zero-shot classifier, with 131 MB listed model size and Apache-2.0 licence. That file-size figure is NOT the runtime memory requirement. Frameworks, tokenisation, activations and concurrency add overhead. It is a credible small-model candidate for event classification, not a verified equivalent to Jev's calibration or an autonomous fixer.

The adapter uses the official GLiClass model/tokeniser/pipeline pattern on CPU with a multi-label output. Its scores are explicitly uncalibrated. Provisional score/margin thresholds trigger abstention; every result still requires human review. No performance parity, reliability or CPU speed claim is made.

Optional setup, separate from the core install:

```sh
python -m pip install gliclass 'transformers>=4.48.0'
python - <<'PY'
from gliclass import GLiClassModel
from transformers import AutoTokenizer
name = 'knowledgator/gliclass-edge-v3.0'
# Explicit setup-time download. Review publisher files before installing.
GLiClassModel.from_pretrained(name)
AutoTokenizer.from_pretrained(name, add_prefix_space=True, trust_remote_code=False)
PY
```

This optional dependency set is not locked or installed in the verified release environment. Run it in a disposable environment first and record a compatible lock and exact model revision before production evaluation. Case requests require locally cached weights; the application does not deliberately download weights while handling a case. Model-library internals and their network behaviour require separate live validation. No model weights are included in the repository.

Primary sources:
- https://huggingface.co/knowledgator/gliclass-edge-v3.0
- https://github.com/Knowledgator/GLiClass
- https://arxiv.org/abs/2508.07662

## Optional local extraction: Qwen through Ollama

A small generative model can propose which existing conditions a source explicitly discusses. The implemented local adapter uses Ollama's JSON-schema structured-output API, defaults to the available `qwen3.5:4b` tag and sends requests only to `http://127.0.0.1:11434/api/chat`. The Ollama model page lists an Apache-2.0 licence. This is a candidate configuration, not a tested live-inference deployment.

```sh
ollama pull qwen3.5:4b
# Run Ollama locally using its platform-specific service/serve instructions.
# EIGHTBALL_OLLAMA_MODEL can select another compatible local model.
```

The response may only propose existing condition IDs, exact booleans and verbatim spans found in the source. Unsupported spans, extra fields, invalid labels and malformed JSON fail closed. Exact text matching prevents fabricated citations but does not prove semantic support: a quoted rejection must not be mistaken for acceptance. An operator must inspect the source and make a separate attestation. Requests do not alter the case. Model thinking/token behaviour, truncation and schema adherence still need real-model evaluation.

Primary sources:
- https://ollama.com/library/qwen3.5:4b
- https://huggingface.co/Qwen/Qwen3.5-4B
- https://docs.ollama.com/capabilities/structured-outputs

## Why not an agent swarm first?

The hard requirement is reliable state and accountable decisions, not the number of agents. Multiple models agreeing on an unsupported claim would still not make it evidence. Start with one classification adapter, one optional extraction adapter and a deterministic planner. Permit abstention and unavailable-provider states without losing manual functionality. Add a larger model only where measured review effort or recall justifies it.

## Evaluation before selecting a production model

Create a human-labelled, consented or fictional test set covering each domain and event class: deadline changes, corrections, refusals, routine updates, ambiguous messages, negation, quoted instructions, conflicting sources and missing context. Keep development and held-out cases separate. Record exact provider version or model revision, dependency lock, prompt, labels and test date.

Measure per-class precision/recall, unsupported-claim rate, abstention coverage, source-span validity, semantic support, review time, latency and peak memory on the target machine. Evaluate calibration on held-out data before using probability thresholds. Compare Jev and GLiClass on the same inputs rather than comparing unrelated public benchmarks. Use a higher-capability local model only if results justify it. No model-quality acceptance threshold has been validated yet.

This release tests request contracts and failure handling with mocked responses. It does not persist model traces or automatically learn from prior cases. A production trace must record source IDs, case revision, model/version, output, reviewer and disposition without leaking confidential source data into application logs.
