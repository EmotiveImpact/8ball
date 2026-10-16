# Whole-system source investigation

16 October 2026; application starting point `0fed04b5e299f4a2e53050456559133c1231b088`.
All 28 candidate repository pins remain in [inventory](../../../research/inventory.json).
Category reviews inspected existing research and focused actual source/manifests.
No upstream installers, tests, services, hooks or models were run. This is bounded
architecture/component-fit research, not an exhaustive or security audit, legal
opinion, independent professional acceptance or replicated benchmark.

The [owner technical direction](../../strategy/OWNER-TECHNICAL-DIRECTION-2026-10-16.md)
records the complete disposition matrix and staged recommendation. Earlier
assessments remain preserved; source inspection does not adopt runtime features.

## Product and evidence

The application has real source originals/excerpts, reviewed proposals,
condition/evidence separation, alternatives, course tracking, approvals,
questions, isolated What If and audit/export. ENDSTATE is a separate internal
read-only calculation package. Planning is bounded to 64 routes/4,096 expansions
with greedy capacity-one scheduling; this is not global optimisation or a
calibrated behavioural forecast. Current Jev code classifies five event labels
and explicitly distinguishes confidence from outcome chance.

- [What If](../../../eightball/v2/services.py), [planner](../../../endstate/planner.py),
  [Jev](../../../eightball/providers.py), [internal contract](../../endstate/CONTRACTS.md).
- Historical Qwen graph failure remains in [the original report](../../evidence/qwen-baseline-2026-09-27.json).
- Previous software result is 1,104 source / 1,104 installed / 391 native at
  `ddfead7`; it is historical until a later source-bound run is recorded.

Three immediate engineering findings: the live fixture runner reused a fixed
report path; the happy-path journey lacked deliberate cancel/stale/process-restart
trials; and provider configuration rejected explicit OpenRouter `:free` variants
while admitting the dynamic free router. The sprint addresses those bounded
tooling/identity gaps without calling a model. Independent study templates remain
recording aids rather than an approved/machine-enforced acceptance study.

## Simulation, optimisation and causal tools

| Source finding | Consequence / disposition |
| --- | --- |
| OASIS HEAD requires Python <3.12; Mesa HEAD requires >=3.12. MiroFish pins CAMEL/OASIS versions different from standalone OASIS HEAD. | Separate versioned adapter environments; copying HEADs cannot establish compatible installation. EM-091. |
| Both Simulatrex repositories publish/import `simulatrex`, at different versions. | Treat as alternatives; do not co-install. Possible Worlds' broader natural-language event trigger remains a placeholder. |
| OASIS Twitter recommender can call Hugging Face `from_pretrained` for `Twitter/twhin-bert-base`; Reddit/random has a no-recommender-model path. | A hosted Qwen endpoint does not remove all possible local artifact downloads. Preapprove exact artifacts if a later pilot needs them. |
| OASIS actor method returns caught exception objects while environment step discards gather results. | Count failed/omitted actor actions explicitly; normal driver completion cannot establish complete success. EM-090. |
| MiroFish configuration retries three times, varies temperature, repairs invalid/truncated JSON and omits max_tokens on that path. | Preserve assisted/retried status; never substitute its success for unchanged unassisted generation acceptance. |
| AgentSociety2 records tokens but uses per-process AIMD with unbounded maximum and default four attempts. | Central experiment admission/cost control remains separate; Ray object-store setup adds operating requirements. |
| Mesa HEAD is 4.0.0a0 with experimental scenario API. | Select and recheck a stable release for a later rule-based pilot. |
| OR-Tools has typed feasibility/optimality/unknown statuses; pymoo can retain a least-infeasible candidate. | Independently validate every candidate and preserve status/bounds; present neither timeout nor a returned candidate as proof. |
| SALib Sobol runs scale as N(D+2) or N(2D+2); analyser normalises by output standard deviation and uses a truthy seed check. | Use cheap functions first; test constant outputs, non-finite results and seed 0 explicitly. |
| DoWhy/EconML require identification assumptions and suitable observations; ENDSTATE prerequisites are an operational graph. | Keep causal estimation deferred; do not interpret dependency links as an identified causal DAG. |
| Possible Worlds evaluation is GPT-4 narrative judgement and accumulates agent_results across objective iterations. | Source-observed cross-objective input risk; isolate/review objectives in any adaptation and retain independent evaluation. |

Pinned references:

- [OASIS manifest](https://github.com/camel-ai/oasis/blob/bc805a19978a620bb400f4c644ce9d772ccbfc70/pyproject.toml#L24), [recommenders](https://github.com/camel-ai/oasis/blob/bc805a19978a620bb400f4c644ce9d772ccbfc70/oasis/social_platform/recsys.py#L64), [actor failures](https://github.com/camel-ai/oasis/blob/bc805a19978a620bb400f4c644ce9d772ccbfc70/oasis/social_agent/agent.py#L126), [step](https://github.com/camel-ai/oasis/blob/bc805a19978a620bb400f4c644ce9d772ccbfc70/oasis/environment/env.py#L207).
- [MiroFish config retry/repair](https://github.com/666ghj/MiroFish/blob/7657031ac01184afe2cb220f5ee3545573b5e843/backend/app/services/simulation_config_generator.py#L435).
- [AgentSociety dispatcher](https://github.com/tsinghua-fib-lab/AgentSociety/blob/8cc5bb9a9c27d039ec5519375db9d73ccf508cba/packages/agentsociety2/agentsociety2/config/llm_dispatcher.py#L655).
- [Mesa scenario runner](https://github.com/mesa/mesa/blob/5451086fe47ab78e9ba894aa1b4c3063f4c247f1/mesa/experimental/scenarios/runner.py#L208), [OR-Tools solver](https://github.com/google/or-tools/blob/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5/ortools/sat/python/cp_model.py#L1733), [pymoo NSGA2](https://github.com/anyoptimization/pymoo/blob/23110c155aa8f31b5f1b86928227fb3931ba7f00/pymoo/algorithms/moo/nsga2.py#L95).
- [SALib sampler](https://github.com/SALib/SALib/blob/748cf169e82227bcc56dcfc961fcfb03a1e0df45/src/SALib/sample/sobol.py#L30), [analyser](https://github.com/SALib/SALib/blob/748cf169e82227bcc56dcfc961fcfb03a1e0df45/src/SALib/analyze/sobol.py#L115).
- [DoWhy counterfactuals](https://github.com/py-why/dowhy/blob/10648f1a295cbb40fd9cdd7ce43521a6ef954078/dowhy/gcm/whatif.py#L105), [EconML assumptions](https://github.com/py-why/EconML/blob/d625dd696ea28c62e6e4d8baea6e4154b98c30b4/README.md#L20).
- [Engine package](https://github.com/simulatrex/simulatrex-engine/blob/4e4fa06d7f527480b66ceb224a5d37bcfa2f9150/setup.py#L7), [Possible Worlds package](https://github.com/simulatrex/possible-worlds/blob/08837a790f6ca0d98f7468935e9139292ea7cb78/setup.py), [event placeholder](https://github.com/simulatrex/possible-worlds/blob/08837a790f6ca0d98f7468935e9139292ea7cb78/src/simulatrex/event.py#L94), [objective evaluation](https://github.com/simulatrex/possible-worlds/blob/08837a790f6ca0d98f7468935e9139292ea7cb78/src/simulatrex/evaluation.py#L45).

## Memory, ingestion and source authority

Keep current case-scoped literal source search initially. It is not an existing
BM25/vector service. If a later retrieval failure is demonstrated, compare one
candidate: Tencent Core for approved procedural recall, Graphiti for changing
relationships, Zep as a managed alternative or Mem0 for narrower conversation
recall. Do not create four competing authorities. Graphiti defaults separately
create extraction, embedding and reranking clients plus graph infrastructure;
a Qwen chat endpoint alone does not replace them.

| Source finding | Consequence / disposition |
| --- | --- |
| Tencent Core can use SQLite/FTS5 without embeddings, but model extraction remains. L2/L3 group across team+agent; session/user/task are not that partition. | Case/scenario isolation must be explicit. A topic summary is not a hypothetical world. |
| Tencent reader can return empty source_message_ids; merges use incoming ancestry; lower-record deletion does not establish profile/skill recomputation. | Preserve canonical ancestry externally and test full derivative invalidation. Existing EM-076/080 evidence refined. |
| Graphiti optional group_ids=None creates no partition filter, and library/server episode deletion differs. | Trusted mandatory scope and host-owned tombstone/rebuild are required; namespace metadata alone is not access control. |
| Zep public repo/SDK provides examples/client code, not the hosted product. | API licence, service account, residency/retention and costs remain separate. |
| Mem0 defaults to OpenAI extraction/embeddings and Qdrant; infer=False still embeds. Deletion preserves history by design. | Explicit actual backend/data-exit and complete retention/reset semantics before any pilot. |
| Mem0 telemetry defaults enabled and targets us.i.posthog.com for operation metadata. | Explicitly configure telemetry before import and inspect egress. This is not a demonstrated case-text leak or security vulnerability. EM-089. |
| Docling strips/joins cell text and replaces characters before assigning spans; tables may use charspan=(0,0). | Preserve original file hash plus derivative/version/page/bbox mappings. Those offsets cannot be called original-PDF Unicode offsets. EM-088. |
| Docling default limits can be effectively unbounded; timeout may yield PARTIAL_SUCCESS; pipeline artifacts can download on first use. | Isolated worker with explicit file/page/time/artifact limits and visible partial/rejected results. |
| PostgreSQL RLS has role/owner bypass semantics and must be configured. | Future multi-user storage needs app grants, migration, backup/restore and denial evidence; database choice alone cannot establish isolation. |

Pinned references:

- [Tencent source reader](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/e9a82935b52741e0c798c75326e90b7144eb4d5f/MemoryCore/src/core/record/l1-reader.ts#L80), [profile scope](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/e9a82935b52741e0c798c75326e90b7144eb4d5f/MemoryCore/src/core/profile/profile-scope.ts#L34), [merge ancestry](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/e9a82935b52741e0c798c75326e90b7144eb4d5f/MemoryCore/src/core/record/l1-writer.ts#L221).
- [Graphiti filter](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/search/search_utils.py#L95), [library deletion](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/graphiti.py#L2164), [server deletion](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/server/graph_service/zep_graphiti.py#L73).
- [Mem0 telemetry](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/memory/telemetry.py#L14), [deletion/history](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/memory/main.py#L1883).
- [Docling reading-order normalisation](https://github.com/docling-project/docling/blob/f690a5232c505c787a1e952216b431134b4d7c94/docling/models/stages/reading_order/readingorder_model.py#L109), [table provenance](https://github.com/docling-project/docling/blob/f690a5232c505c787a1e952216b431134b4d7c94/docling/models/stages/reading_order/readingorder_model.py#L149).
- [PostgreSQL RLS](https://github.com/postgres/postgres/blob/eb7cc1d09e742d369540016455d0f55c619106f2/doc/src/sgml/ddl.sgml#L2967).

## Orchestration, identity and enforcement

Native application jobs already preserve idempotency, case revision, terminal
states and guarded proposal publication; restart interrupts work and never retries
automatically. They support one server process. Codex delegation is development
tooling. Ruflo overlaps that tooling; LangGraph is a possible later application
workflow library; Temporal is a distinct operated durable-workflow service.

New/sharpened integration requirements:

- LangGraph defaults to async checkpoint durability; sync/exit modes differ.
  Interrupt resumes by re-executing the node. Repeated side effects and fresh
  identity/case/approval checks remain adapter responsibilities. EM-092.
- Temporal retry maximum defaults to zero meaning no maximum. Paid model
  activities need explicit attempts/time/idempotency and ambiguous-call accounting.
- Swarm handoff commonly means routing a shared conversation to one next worker.
  It does not implement world transitions. AutoGen maintenance mode was already
  recorded; default unbounded team turns and cancellation/state-save caveats add
  concrete requirements if its patterns are adapted.
- Ruflo registry termination, headless process completion and case publication
  are different contracts. Preserve the prior source-supported cancellation race
  and exact model-changing fallback limits; no runtime reproduction is claimed.
- OIDC/Keycloak identifies the user; OpenFGA can check relationship grants; OPA
  evaluates policy. The app still enforces current authority at the final write.
  Cached permission answers and logout propagation need explicit revocation timing.
  These are fit obligations, not security certification or validated vulnerabilities.

Pinned references:

- [LangGraph durability](https://github.com/langchain-ai/langgraph/blob/e77a5cb08c1f3ff306d997dd76fc7169afdab5ea/libs/langgraph/langgraph/pregel/main.py#L2798), [interrupt/re-execution](https://github.com/langchain-ai/langgraph/blob/e77a5cb08c1f3ff306d997dd76fc7169afdab5ea/libs/langgraph/langgraph/types.py#L903).
- [Temporal retries](https://github.com/temporalio/sdk-python/blob/346d4dcd0863657c3a33283c952a296762059339/temporalio/common.py#L36).
- [LangGraph Swarm handoff](https://github.com/langchain-ai/langgraph-swarm-py/blob/5442a15cdd0ed210589148900c9960c24c489d04/langgraph_swarm/handoff.py#L73), [AutoGen maintenance](https://github.com/microsoft/autogen/blob/027ecf0a379bcc1d09956d46d12d44a3ad9cee14/README.md#L14), [swarm defaults](https://github.com/microsoft/autogen/blob/027ecf0a379bcc1d09956d46d12d44a3ad9cee14/python/packages/autogen-agentchat/src/autogen_agentchat/teams/_group_chat/_swarm_group_chat.py#L126).
- [Ruflo findings](ruflo-execution.md), [OpenFGA consistency](https://github.com/openfga/openfga/blob/fb8e7df866742a0c947e3066919ee59ac9e70eea/cmd/run/run.go#L330), [Keycloak revocation](https://github.com/keycloak/keycloak/blob/eae20e964b2e23cfd8f4ed18b599343ebb056e8f/docs/documentation/server_admin/topics/sessions/revocation.adoc#L16), [OPA decision contract](https://github.com/open-policy-agent/opa/blob/fdf6011f57fdc25f01de1982e296bb402cf37625/v1/sdk/opa.go#L361).

## Evaluation and model-service evidence

Keep the project runners and prospective independent-review pack. Promptfoo and
Phoenix may inspect/compare retained experiments later; they do not supply
professional labels or waive the frozen gate. Promptfoo caching defaults on;
transformations/repeats/retries need explicit policy. Phoenix experiment retries
default to three, and dry_run still executes tasks. Prefer offline artifact import
first. ELv2 server and Apache-2.0 client licensing are different scopes. EM-093.

The current runtime observed no provider variables or secrets. Official Alibaba
and OpenRouter website fetches failed through the inherited proxy; no claim of
fresh pricing/free entitlement or private-data terms is made. Official GitHub
documentation was accessible at these additional **documentation references**
(not added runtime/research-submodule dependencies):

- OpenRouterTeam/docs `cf946639e64019ddad516b9536d9be766c45e10d`:
  [structured output](https://github.com/OpenRouterTeam/docs/blob/cf946639e64019ddad516b9536d9be766c45e10d/guides/features/structured-outputs.mdx),
  [explicit free variant](https://github.com/OpenRouterTeam/docs/blob/cf946639e64019ddad516b9536d9be766c45e10d/guides/routing/model-variants/free.mdx),
  [random free router](https://github.com/OpenRouterTeam/docs/blob/cf946639e64019ddad516b9536d9be766c45e10d/guides/routing/routers/free-router.mdx),
  [data collection](https://github.com/OpenRouterTeam/docs/blob/cf946639e64019ddad516b9536d9be766c45e10d/guides/privacy/data-collection.mdx),
  [downstream logging](https://github.com/OpenRouterTeam/docs/blob/cf946639e64019ddad516b9536d9be766c45e10d/guides/privacy/provider-logging.mdx).
- QwenLM/Qwen3 `7a2f61ffc7a20d47efcd2bf97f6f2bf52729042e`:
  [model/runtime modes](https://github.com/QwenLM/Qwen3/blob/7a2f61ffc7a20d47efcd2bf97f6f2bf52729042e/README.md).
- [Promptfoo cache](https://github.com/promptfoo/promptfoo/blob/132a2d38b1b0adc953b0db650f950d573bc113c4/src/cache.ts#L56),
  [Phoenix experiment semantics](https://github.com/Arize-ai/phoenix/blob/2be380f7a360b7a71f97fc510de5e9679e58f7c9/packages/phoenix-client/src/phoenix/client/resources/experiments/__init__.py#L780).

Our hosted transport still requires a nonempty private key and hosted HTTPS DNS
on port 443. A truly keyless or HTTP/IP service requires a separately tested
compatibility change; do not invent a dummy key or bypass the network proxy.
Strict schema support varies by endpoint. Thinking-only Qwen modes do not become
non-thinking because a client requests it; select a supported mode and test it.

The owner permits fictional examples up to US$5 and expects free access. The app
has no hard dollar ledger; a case budget, token cap or cost alert cannot replace
provider-enforced spend control. Free quotas, embeddings, downstream logging,
retention and regional processing need selected-service evidence. No client data
is authorised. Builder model access is separate from application inference.

The inspected OpenRouter documentation constants describe 20 requests/minute
and daily tiers of 50 or 1,000 free requests depending on purchased-credit
history. These are dated source values, not verified account entitlement or
current availability. The privacy mirror describes prompt/output product-use
opt-ins as off by default while metadata is retained; downstream providers have
separate policies. Verify the actual selected service before any private data.

## What this investigation cannot establish

It cannot produce the owner's private credentials, a guaranteed free model,
independent professional judgements, genuine human accessibility/visual acceptance,
or calibrated predictions without a valid model/data/evaluation process. These
remain explicit dependencies. Every identified source finding is retained here
and in the emergence register; no unresolved fact is silently converted to a
passing gate or a required runtime feature.
