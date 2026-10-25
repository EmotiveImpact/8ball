# Ruflo: role in the ENDSTATE / 8BALL architecture

16 October 2026. Inspected source commit `1882006a02487590c8c66a7eec8d7504f6af33c3`. Bounded source/manifests/configuration review only: no installation, package scripts, model calls, upstream tests or integration.

## Recommendation

For the owner's plain-English explanation, free-Qwen clarification and checked
claims, read [Ruflo owner guide](ruflo-owner-guide.md).

Shortlist Ruflo as an optional developer/worker coordination harness. It surrounds Claude Code/Codex or configured model calls with tools, task/agent management, memory, hooks and workflow coordination. It is a different layer from MiroFish/OASIS social simulation and ENDSTATE conditional route calculation. Compare a bounded workflow against the current native agent/job approach before importing it into product runtime.

Source licence is MIT; root package is `claude-flow` 3.56.10 and declares Node >=20. Branding aliases and individual component versions differ. A compatible host/model configuration is still needed. Claude-specific console/mod functionality is not automatically portable to every MCP client. Optional AgentDB/RuVector packages bring their own dependency/runtime constraints.

## Where it could help

- Coordinate researcher, planner/proposer, critic and implementation/test workers with explicit task/result records.
- Reuse project context and retrieve relevant prior task patterns.
- Expose a worker pool through MCP or an explicit adapter while 8BALL retains reviewed commands and approvals.
- Provide developer operations and host-integration patterns; this cloud session already supports native subagents, so measured gain is required before adding another coordinator.

## What actual execution and evidence mean

The inspected execution core contains real configured-provider requests. Registration, task queue state and model execution must remain distinct. A provider response, agreement among agents or task status cannot establish source truth, professional quality, execution authority or an actual outcome. Source-level host tests explicitly separate keyless/stubbed CI from optional live provider legs. Historical verification marker presence attests source bytes/markers; it is not semantic evaluation of ENDSTATE plans.

The memory embedding policy permits deterministic hash fallback when a real embedder is unavailable unless its strict flag is enabled. Such vectors do not provide meaningful semantic similarity; adoption would need strict real-embedding configuration, a verified active backend and semantic retrieval fixtures. Optional trajectory/contrastive learning modules and rewards also do not establish that a configured foundation model has learned reliable fixer outcomes.

CLI postinstall code patches AgentDB dependency layout; its defined exports-augmentation helper is not called by the inspected main function. Initialisation and host hooks can alter project/host configuration. Any eventual evaluation should use isolated fictional projects, pinned packages and explicit tools/provider/budget choices, with no installation in the live 8BALL checkout as a side effect of source research. This is dependency/authority fit research, not a security audit.

## Proposed experiment

Use the same fictional research-and-plan task, source set, chosen provider/model and bounded call/time budget with (a) current simple/native workers and (b) Ruflo workers. Independently score missed constraints, unsupported claims, alternative usefulness, correction effort, latency and actual cost. Capture registration, provider dispatch, raw outputs, failures and completion evidence separately. Test stale revision publication and cancel/interruption boundaries. A simple passing host smoke test is insufficient.

No runtime adoption is proposed before this measured comparison. Current V0.2 requirements remain unchanged.

## Pinned starting sources

- [README and host distinctions](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/README.md)
- [MIT licence](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/LICENSE)
- [Root manifest](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/package.json)
- [Provider execution core](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/@claude-flow/cli/src/mcp-tools/agent-execute-core.ts)
- [Embedding fallback policy](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/@claude-flow/cli/src/memory/embedding-policy.ts)
- [Optional learning implementation](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/@claude-flow/cli/src/services/ruvector-training.ts)
- [AgentDB compatibility postinstall](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/v3/@claude-flow/cli/scripts/postinstall.cjs)
- [Host-matrix keyless/live distinction](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/scripts/e2e/host-matrix.mjs)
- [Historical marker-verification scope](https://github.com/ruvnet/ruflo/blob/1882006a02487590c8c66a7eec8d7504f6af33c3/verification/results.md)

Detailed source records: [actual execution/lifecycle](ruflo-execution.md), [memory, learning, runtime and evaluation evidence](ruflo-memory-runtime.md).
