# Ruflo explained for the 8BALL owner

16 October 2026. Source-only follow-up at upstream commit
`1882006a02487590c8c66a7eec8d7504f6af33c3`; an HTTPS Git remote inspection
confirmed that both HEAD and main still pointed to that revision. Root package:
`claude-flow` 3.56.10, MIT, Node >=20. No upstream installation, execution,
model call or benchmark reproduction was performed.

## What you are looking at

Ruflo manages teams of AI workers. Give a team a task and it can coordinate
roles, messages, shared memory and work. It wraps model services and coding
hosts such as Claude Code/Codex. A researcher could collect material, a planner
draft options, a critic challenge assumptions and a tester check implementation.
Those workers may use the same underlying model; more worker roles do not imply
more independent knowledge.

| Part | Its job in the proposed system |
| --- | --- |
| Qwen or another model | Produces language and proposed interpretations through a separately supplied runtime/API. |
| Ruflo | Optionally assigns work, coordinates workers and retrieves task-pattern memory. |
| ENDSTATE | Keeps the existing explicit conditions, constraints and conditional route calculation. |
| 8BALL | Gives the operator the case workspace, evidence, review and action-authority workflow. |
| A future simulator | Runs explicitly defined hypothetical worlds; requires its own model, assumptions and validation. |

Ruflo does **not supply our missing free Qwen endpoint**. Its MIT source can be
used without a software licence fee, while actual model access still depends on
the selected service or separately operated local runtime. We have no evidence
of a bundled free Qwen service or universal free model quota.

## What the code supports

- Actual provider execution exists. The inspected core makes Anthropic,
  OpenRouter or Ollama requests; a headless backend can launch an installed and
  authenticated Claude CLI. Individual integrations have different requirements.
- Agent registration and task bookkeeping are separate from actual execution.
  The keyless WASM path can deliberately return an **echo stub**, labelled as
  having no LLM. A working dashboard or registered team alone is insufficient.
- Memory and adaptive routing are substantive mechanisms. The Q-router learns
  which worker role to choose from roles such as coder, tester and researcher.
  Its confidence is calculated from worker Q-values. This is a different
  prediction target from the probability of achieving a client's outcome.
- Some execution feedback currently defines success as returning without an
  API error. Useful plans still require source checks, relevant acceptance tests
  and independent evaluation. Agreement among workers cannot attest a fact.

## What needs caution

**Learning:** retained patterns and feedback can influence future worker choices.
That mechanism does not establish improvement in business decisions or training
of the hosted foundation model's weights. Real evaluation labels matter.

**Performance evidence:** one included multi-agent benchmark generates synthetic
results; its real Ruflo backend explicitly reports that it is not yet wired.
Other real execution paths and retrieval benchmarks exist, so assess each claim
against its particular evidence. Upstream's own May audit identified overstated
historical numbers and records later corrections. Current Flash Attention
telemetry explicitly reports zero meaning *unmeasured*. We have not independently
replicated the published measurements; historical defects must not all be
presented as current defects.

**Memory quality:** the inspected embedding policy allows a hash fallback unless
real embeddings are required. Hash-shaped vectors do not establish meaningful
semantic retrieval. A future pilot must expose and test its actual backend.

**Cost and model identity:** eligible neural-routed failures can retry with a
different model. Multiple workers and retries can consume additional capacity.
Disable unintended routing/fallback for a frozen-model evaluation and preserve
every attempted call. A retry count is not a dollar spending cap.

**Case authority:** source review found lifecycle semantics different from 8BALL's
cancelled/stale-result publication rules. A future adapter would need to retain
8BALL's exact source snapshot, expected revision, cancellation and human review
checks. No harness result should directly change case facts or authorise action.

## Recommendation

Keep Ruflo as an optional worker-coordination candidate in research. Finish the
current V0.2 real-model and independent/human acceptance first. This development
environment already provides native subagents and persisted application jobs.

A later bounded comparison should give native workers and Ruflo the same
fictional task, source snapshot, exact provider/model and call/time budget. Score
missed constraints, unsupported claims, useful alternatives, correction effort,
latency and actual cost. Use independently authored judgements. Add the smallest
useful component only if it demonstrates a worthwhile improvement.

The owner can keep the goal of exploring multiple scenarios. Reliable scenario
comparison still needs explicit interventions, credible transition assumptions,
constraints, outcome measurements and review. Worker consensus or routing
confidence cannot supply those missing contracts by itself.

## Technical handoff notes

Provider URL conventions differ between Ruflo components. Its inspected core
OpenRouter/custom gateway path appends `/v1/chat/completions`; its separate
OpenAI adapter appends `/chat/completions`. 8BALL's existing adapter also appends
only `/chat/completions`. Do not copy one component's settings blindly into
another or assume that successful provider registration tests structured output.

Ruflo also contains distributed consensus implementations (Raft, Byzantine and
Gossip; the named Paxos choice falls back to Raft). These protocols coordinate
agreement about shared state. They do not establish whether a client's proposed
plan is true or likely to succeed. A pilot must identify the actual configured
transport and algorithm rather than infer them from a feature label.

## Checked source references

All links below are pinned to the inspected revision.

- [Project describes its model/harness distinction](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/README.md#L95).
- [Provider selection and actual calls](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/cli/src/mcp-tools/agent-execute-core.ts#L171).
- [Core gateway URL construction](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/cli/src/mcp-tools/agent-execute-core.ts#L438), [separate OpenAI adapter](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/providers/src/openai-provider.ts#L178) and [consensus factory](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/swarm/src/consensus/index.ts#L23).
- [Keyless echo path and billing note](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/cli/src/ruvector/agent-wasm.ts#L220).
- [Model-changing retry and API-success feedback](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/cli/src/mcp-tools/agent-execute-core.ts#L644).
- [Worker choices](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/cli/src/ruvector/q-learning-router.ts#L160) and [routing/confidence calculation](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/cli/src/ruvector/q-learning-router.ts#L343).
- [Embedding fallback policy](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/cli/src/memory/embedding-policy.ts#L1).
- [Synthetic benchmark and unfinished real backend](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/scripts/benchmark-multiagent.mjs#L184).
- [Upstream audit with remediation history](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/docs/reviews/intelligence-system-audit-2026-05-29.md#L93) and [current unmeasured telemetry](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/%40claude-flow/swarm/src/attention-coordinator.ts#L973).

For technical lifecycle and dependency details see [execution review](ruflo-execution.md)
and [memory/runtime review](ruflo-memory-runtime.md). Existing source review,
software checks and agent research are not independent professional acceptance.
