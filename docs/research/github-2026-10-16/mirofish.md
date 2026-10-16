# GitHub swarm intelligence research: MiroFish and ENDSTATE

Read-only source assessment, 16 October2026. No installation, inference, accuracy benchmark or application integration was performed. The application remains unchanged on main. These are research candidates, not newly accepted V0.2 scope.

## MiroFish

Inspected commit7657031ac01184afe2cb220f5ee3545573b5e843: https://github.com/666ghj/MiroFish/tree/7657031ac01184afe2cb220f5ee3545573b5e843

The implemented flow builds a source-derived graph, generates agent profiles/configuration, runs OASIS social-platform simulations, retains actions/logs, and generates reports with follow-up interviews. This matches the intended multi-agent rehearsal direction.

Its actual reviewed environments/actions centre on simulated Twitter and Reddit. The broad prediction slogan does not establish accuracy for fixer outcomes. The event configuration parser sets scheduled_events=[]; post-simulation IPC supports interview/batch_interview/close_env. I did not find a general replay/forked-world contract, ENDSTATE route adapter or held-out calibrated prediction evaluation in the inspected implementation. These are bounded source-review observations, not proof of absence from all upstream work.

A compatible LLM endpoint is still needed; the software coordinates model calls rather than supplying Qwen/DeepSeek weights. Current configuration requires Zep Cloud, and explicitly rejects a custom ZEP_API_URL. Report generation normally uses the same configured model and simulated graph/interviews; it is not independent model evaluation. Rounds/active agents/report calls can be bounded, but I found no project-wide money/token ledger/cap. README warns about consumption.

License: AGPL-3.0. This permits commercial activity subject to its conditions; assess covered-source/network obligations before embedding code. A separate service is an architectural boundary, not an automatic licensing exemption.

### Pinned evidence

- README workflow/dependencies/consumption: https://github.com/666ghj/MiroFish/blob/7657031ac01184afe2cb220f5ee3545573b5e843/README.md
- Licence: https://github.com/666ghj/MiroFish/blob/7657031ac01184afe2cb220f5ee3545573b5e843/LICENSE
- Required runtime/API configuration: https://github.com/666ghj/MiroFish/blob/7657031ac01184afe2cb220f5ee3545573b5e843/backend/app/config.py#L27-L72
- Actual action sets and execution/interview loop: https://github.com/666ghj/MiroFish/blob/7657031ac01184afe2cb220f5ee3545573b5e843/backend/scripts/run_parallel_simulation.py#L177-L214 and lines1253/1585/1595-1616.
- Scheduled event parsing: https://github.com/666ghj/MiroFish/blob/7657031ac01184afe2cb220f5ee3545573b5e843/backend/app/services/simulation_config_generator.py#L721-L728
- Report agent: https://github.com/666ghj/MiroFish/blob/7657031ac01184afe2cb220f5ee3545573b5e843/backend/app/services/report_agent.py

## Comparable repositories

| Repository | Verified role | ENDSTATE relevance |
| --- | --- | --- |
| https://github.com/camel-ai/oasis | Social simulation engine beneath MiroFish; Apache2.0. | Lower-level candidate for a bounded rehearsal adapter. |
| https://github.com/tsinghua-fib-lab/AgentSociety | AgentSociety2 modular environments, distributed execution/replay; substantial dependency stack. AS2 Apache2.0, with repository-noted legacy commercial-directory exception. | Broader possible-world research candidate requiring independent evaluation. |
| https://github.com/langchain-ai/langgraph-swarm-py | Agent handoff/state orchestration; MIT. | Coordination of proposal/critic/judge roles; not itself population forecasting. |
| https://github.com/microsoft/autogen | Team/handoff orchestration; current README says maintenance mode and recommends Microsoft Agent Framework. MIT code/CCBY4 documentation. | Reference patterns rather than first-choice new dependency. |

Pinned comparison revisions are retained in mirofish-assessment.json. Searches used GitHub repository HTML for swarm intelligence, multi agent social simulation and agent scenario simulation. Broad searches also return numerical optimisation libraries, which serve a different role.

## Fit to the existing vision

ENDSTATE supplies the explicit outcome, case snapshot, action dependencies, constraints and verification checks. A rehearsal adapter can supply isolated hypothetical events/reactions. A separately evaluated decision model can judge target alignment and compare route weaknesses; the current JEV classification adapter does not yet implement a full route judge. The 8BALL operator reviews the alternatives.

A sensible first evaluation compares the existing hand-authored What If baseline with a small fictional MiroFish/OASIS rehearsal under declared call/round/cost limits. Measure useful new failure discovery, false assumptions, goal coverage and review effort. Preserve case/revision and model provenance; synthetic events do not become observed facts or success probabilities. This assessment does not authorize paid calls, external case transmission, dependencies or deferred research integration.
