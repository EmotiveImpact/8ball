# GitHub component research for ENDSTATE and 8BALL

16 October 2026. Read with the [full proposed evolution plan](../strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md). This is a bounded source, manifest and licence inspection, not an installed-system benchmark, security audit or independent predictive evaluation. No upstream runtime dependencies, model weights or services were installed; no inference was performed.

## Search and evidence

Public GitHub repository searches covered swarm intelligence, multi-agent social simulation, scenario simulation, temporal memory, causal decision tools, authorisation and model evaluation. Exact additional query URLs and returned candidates are retained in [search results](github-2026-10-16/github-search-results.json); earlier swarm queries are in [the MiroFish receipt](github-2026-10-16/mirofish-assessment.json). Search results are discovery leads, not endorsements. We also followed upstream dependencies and deliberately inspected established alternatives relevant to the existing product requirements.

GitHub API access returned Forbidden during the preceding research; public GitHub HTML, raw pinned files and native Git worked. No ranking, star-count or exhaustive ecosystem coverage claim is made. Remote HEADs identify inspected source, not stable releases selected for installation. [The machine-readable source manifest](github-2026-10-16/source-manifest.json) preserves full revisions.

## Findings by capability

| Research ID | Project / scope | Role and disposition |
| --- | --- | --- |
| RS-14 | [MiroFish](https://github.com/666ghj/MiroFish) | Source-to-social-simulation/report application; AGPL-3.0. Shortlist an isolated social-response experiment; not a generic ENDSTATE replacement. |
| RS-15 | [OASIS](https://github.com/camel-ai/oasis) | MiroFish's social simulation substrate; Apache-2.0. Compare lower-level adaptation with full MiroFish rather than stack both independently. |
| RS-16 | [AgentSociety](https://github.com/tsinghua-fib-lab/AgentSociety) | Broader distributed agent environments; AS2 Apache-2.0 with noted legacy commercial-directory exception. Later alternative where it earns complexity. |
| RS-17 | [LangGraph Swarm](https://github.com/langchain-ai/langgraph-swarm-py) | MIT conversational agent handoffs. Reference for coordination, not population prediction. |
| RS-18 | [AutoGen](https://github.com/microsoft/autogen) | MIT code / CC-BY-4.0 docs; current README says maintenance mode. Preserve patterns; not preferred new dependency. |
| RS-19 | [Graphiti](https://github.com/getzep/graphiti) | Apache-2.0 temporal graph memory; requires graph infrastructure and model providers. Optional derived retrieval adapter. |
| RS-20 | [Zep](https://github.com/getzep/zep) and [Python SDK](https://github.com/getzep/zep-python) | Public Apache-2.0 examples/client code for hosted Zep; not the hosted server. Managed alternative; service terms/costs separate. |
| RS-21 | [Mem0](https://github.com/mem0ai/mem0) | Apache-2.0 conversational memory alternative; no reason to stack beside Graphiti without a separate demonstrated need. |
| RS-22 | [OR-Tools](https://github.com/google/or-tools) | Apache-2.0 mathematical constraints/scheduling. Optional adapter for demonstrated limits in current planner. |
| RS-23 | [Mesa](https://github.com/mesa/mesa) | Apache-2.0 rule-based agent simulation. General operational baseline candidate; inspected HEAD is a 4.0 alpha with API changes. |
| RS-24 | [pymoo](https://github.com/anyoptimization/pymoo) | Apache-2.0 multiobjective search. Defer until direct comparison of existing routes is insufficient. |
| RS-25 | [DoWhy](https://github.com/py-why/dowhy) and [EconML](https://github.com/py-why/EconML) | MIT causal modelling/estimation. Later real-data work, dependent on identification assumptions. |
| RS-26 | [SALib](https://github.com/SALib/SALib) | MIT numeric sensitivity analysis. Later parameter investigations with explicit assumptions and run budgets. |
| RS-27 | [Promptfoo](https://github.com/promptfoo/promptfoo) | MIT model/prompt comparison. Optional developer tool; retain existing fixture and receipt authority. |
| RS-28 | [Phoenix](https://github.com/Arize-ai/phoenix) | Elastic License 2.0 trace/dataset/annotation tooling. Optional internal evaluation service; review hosted-feature restriction. |
| RS-29 | [LangGraph](https://github.com/langchain-ai/langgraph) | MIT stateful workflow/checkpoint library. Defer until measured need beyond current staged jobs. |
| RS-30 | [Temporal Python SDK](https://github.com/temporalio/sdk-python) | MIT durable workflow SDK; operated server/workers still needed. Later event-driven operations candidate. |
| RS-31 | [Docling](https://github.com/docling-project/docling) | MIT document extraction; models have separate licences. Strong later isolated source-ingestion candidate. |
| RS-32 | [Keycloak](https://github.com/keycloak/keycloak) | Apache-2.0 OIDC/MFA identity. Secure-pilot candidate or use an approved existing identity provider. |
| RS-33 | [OpenFGA](https://github.com/openfga/openfga) | Apache-2.0 relationship permissions. Optional when object/client/specialist sharing warrants a service. |
| RS-34 | [OPA](https://github.com/open-policy-agent/opa) | Apache-2.0 general policy decisions. Retain as later alternative; avoid overlapping policy stores. |
| RS-35 | [PostgreSQL](https://github.com/postgres/postgres) | PostgreSQL License; transactional production storage candidate. Row-security, roles and recovery require correct implementation. |
| RS-02 / RS-03 refresh | [Simulatrex engine](https://github.com/simulatrex/simulatrex-engine) / [possible-worlds](https://github.com/simulatrex/possible-worlds) | Apache-2.0. Preserve earlier research and event/agent patterns; current source still needs adaptation and validation. |

## Detailed inspection records

- [Complete product capability map](github-2026-10-16/capability-map.md): 25 families from original PRD through future vision, current code, gaps and exact task homes.
- [MiroFish and simulation alternatives](github-2026-10-16/mirofish.md): implemented Twitter/Reddit action sets, limited event controls, model/report loops and Cloud dependency.
- [Memory and Zep](github-2026-10-16/memory.md): pinned ingestion/search/deletion paths, defaults, source lineage and why Graphiti is not a Cloud endpoint swap.
- [Decision, optimisation and simulation](github-2026-10-16/decision.md): solver status, explicit unknowns, Pareto comparison, scenario seeds, causal assumptions and numeric sensitivity.
- [Evaluation, ingestion and workflow](github-2026-10-16/evaluation-workflow.md): raw experiments/annotations, cost limitations, Docling provenance and workflow restart semantics.
- [Agency identity, access and operations](github-2026-10-16/agency-components.md): minimal secure foundation and application responsibilities.

These records preserve the read-only research subprocesses' scope. Their “no application changes/tests” statements refer to upstream inspection, not the subsequent documentation-validation commands recorded in the [session handoff](../delivery/sessions/2026-10-16-evolution-research.md). Scratch clone locations are historical capture locations, not required runtime paths.

## Refresh of the earlier Simulatrex candidates

The engine's current remote HEAD is still `4e4fa06d7f527480b66ceb224a5d37bcfa2f9150`, matching the earlier research pin. Its README and Apache-2.0 licence were refreshed; the earlier bounded implementation findings are retained, not claimed as a fresh exhaustive audit.

`possible-worlds` was inspected at `08837a790f6ca0d98f7468935e9139292ea7cb78`. Its [event engine](https://github.com/simulatrex/possible-worlds/blob/08837a790f6ca0d98f7468935e9139292ea7cb78/src/simulatrex/event.py#L83) implements a scheduled-time trigger with an explicit placeholder for broader conditions. Its [evaluation engine](https://github.com/simulatrex/possible-worlds/blob/08837a790f6ca0d98f7468935e9139292ea7cb78/src/simulatrex/evaluation.py#L29) asks model-driven agent evaluations and a GPT-4-configured summarising evaluator, with a retry on exception. That is a useful reference for model orchestration, not an independent human judgement or calibrated outcome forecast. [The package](https://github.com/simulatrex/possible-worlds/blob/08837a790f6ca0d98f7468935e9139292ea7cb78/setup.py) declares version 0.0.4.1 and broad unpinned dependencies. An adapter must supply current dependency validation, explicit budgets, allowed action/event types and retained source-bound results.

## What changed our recommendation

1. Swarm systems have specific environment/action vocabularies. A Twitter/Reddit simulator cannot be treated as a supplier/venue/authority model without a tested mapping.
2. Memory adds extraction/embedding costs, temporal interpretation and retraction obligations. Graphiti library/server deletion paths differ; a case cannot rely on index deletion alone.
3. Per-response limits and cost assertions do not bound a whole multi-agent experiment. Provider calls multiply through roles, rounds, scenarios, repeats, embeddings and reports.
4. Familiar projects have material current licence/API differences: Mesa alpha APIs, Phoenix ELv2, MiroFish AGPL and differing Python/dependency ranges. A credible design needs isolated adapters and stable release selection.
5. Numerical outputs need status semantics. OR-Tools timeout/unknown is not impossibility; pymoo may retain a least-infeasible candidate; sensitivity analysis is not causal identification.

These discoveries are retained as EM-075 through EM-079 alongside refinements to earlier insights. They are candidate integration requirements and source observations, not newly accepted runtime features or rewritten V0.2 gates.
