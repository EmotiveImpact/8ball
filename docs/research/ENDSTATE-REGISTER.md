# ENDSTATE research register and source map

Consolidated 15 October 2026 from the supplied 24 September handoff. **This is archival synthesis, not a fresh upstream audit or installed benchmark.** Preserve reported findings with their original dates; refresh current commits, licences and API behaviour before code adoption.

Read the full [original decision register](../reference/endstate-handoff-2026-09-24/08-RESEARCH-DECISION-REGISTER.md), [evolution research](../reference/endstate-handoff-2026-09-24/02-ENDSTATE-EVOLUTION-RESEARCH.md) and [source list](../reference/endstate-handoff-2026-09-24/09-RESEARCH-SOURCES.md). No full upstream clone is claimed.

## Sources, findings, limitations and disposition

| ID | Source | Preserved finding / value | Limitation and next action |
| --- | --- | --- | --- |
| RS-01 | [Simulatrex organisation](https://github.com/simulatrex), [website](https://simulatrex.com/), [The People Machine](https://dominikscherm.substack.com/p/the-people-machine) | Agent/environment/possible-world research direction. | Product claims and conceptual articles are not independent accuracy evidence. Reference only. |
| RS-02 | [simulatrex-engine](https://github.com/simulatrex/simulatrex-engine) | Historical selective review found DSL/parser, agent loops, provider abstraction and a thin playground/API implementation. | Reported inspected develop tree `4e4fa06d7f527480b66ceb224a5d37bcfa2f9150`; not an audited calibrated predictor or production truth store. Reproduce only in Lab. |
| RS-03 | [possible-worlds](https://github.com/simulatrex/possible-worlds) | Scenario/event branching reference. | A fork or synthetic dialogue is not independent human-behaviour validation. Compare explicit branch contracts and deterministic baselines. |
| RS-04 | [llm-subpopulation-research](https://github.com/simulatrex/llm-subpopulation-research) | Experimental design and subpopulation variation. | Reported inspected tree `deb67cfccb7df20b468987fd7ba6cc2a53adb9cc`; model-response variation is not measured behaviour. Preserve evaluation assumptions. |
| RS-05 | [AlpacaDataCleaned](https://github.com/simulatrex/AlpacaDataCleaned) | Dataset provenance/licensing reference. | Original register reports non-commercial restrictions. Exclude commercial training by default pending a fresh rights review; this handoff is not a licence opinion. |
| RS-06 | [Wayfinder method](https://www.aihero.dev/skills-wayfinder), [Wayfinder skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md) | Distinguish what must be learnt from what can be executed; make decision premises visible. | Adapt the reasoning pattern, not documentation conventions as real-world truth or permission. R01/R02. |
| RS-07 | [Wayfinder Maps](https://github.com/rengwu/wayfinder-maps), [tracker contract](https://github.com/rengwu/wayfinder-maps/blob/main/skills/wayfinder-maps/TRACKER-MARKDOWN.md) | Derived decision views, invalidation and graph linting. | Do not substitute a serial Markdown tracker for concurrent case state or `progress.json`. |
| RS-08 | [Matt Pocock skills](https://github.com/mattpocock/skills), [distribution listing](https://skills.sh/mattpocock/skills) | Selective research/specification/domain modelling/TDD/review discipline. | Not installed by this consolidation. External skill instructions cannot override project scope, authority or acceptance. |
| RS-09 | [chartr](https://chartr.dev/), [source](https://github.com/rengwu/chartr), [plugins](https://github.com/rengwu/chartr/blob/main/docs/plugins.md) | Optional developer workbench for terminals, agents and planning. | Not an ENDSTATE dependency. Plugin/native execution requires explicit trust and licence/security review. |
| RS-10 | [Generative Agent Simulations of 1,000 People](https://arxiv.org/abs/2411.10109) | Interview-conditioned simulation research trail. | Source-specific methods/populations do not validate ENDSTATE's cases or personal forecasts. Re-read design and limits before using conclusions. |
| RS-11 | [Validating LLM simulations as behavioral evidence](https://arxiv.org/html/2602.15785v1) | Validation and interpretation of simulated behavioural evidence. | Preserve distinction between simulation outputs and real observations; apply to protocol design, not a quality certificate. |
| RS-12 | [Persona-prompted reactions study](https://www.nature.com/articles/s41598-026-66277-8) | The handoff cites modest, task-specific predictive results in social-media reactions. | Historical reported finding only; not a general human-prediction claim, not revalidated in this sprint. |
| RS-13 | [8BALL actual Qwen baseline](../evidence/qwen-baseline-2026-09-27.json) | Real extraction/graph experiment on this project's published source. | 3/4 schema-valid; graph rejected; no independent semantic evaluation. Drives current B02 closeout, not a future Lab success. |

## Preserve the original experiment IDs

R01 premise-linked decision validity; R02 investigation/execution frontiers; R03 competing world assumptions; R04 rehearsal provider contract; R05 robustness without invented probabilities; R06 expertise-to-domain packs; R07 decision-centred research memory.

The Lab's A-F experiment labels are mapped to these and to [future milestones](../strategy/ROADMAP-INTEGRATION.md) in [ENDSTATE-EXPERIMENTS.md](ENDSTATE-EXPERIMENTS.md). Do not rename the old IDs away or count a plan as an experiment run.

## Status vocabulary

Accepted direction means the owner wants the capability in the long-term vision. Proposed design means a candidate architecture/interface. Deferred implementation means it is deliberately outside the present build. Tested/verified requires named results and the actual tested scope. Declined means the rationale remains visible and can be reviewed again.

The research documents contain both an earlier proposals-only register and a later accepted-direction handoff. They are reconciled as **accepted long-term ambition, proposed implementation, deferred current adoption**. Neither document grants package-installation, model-training, autonomous-outreach or rewrite permission.

## Before importing any external code

Record repository URL, immutable commit/tree, capture date, licence and dependency rights, intended use, local modifications, security review, reproduction command, exact inputs, model/provider/version, resource costs, results, failures and adoption/rejection decision. A public repository is not permission for unrestricted commercial use.

Do not add the projects to runtime requirements simply to make them look included. This consolidation makes the research available to the next agent; it does not install or clone the upstream code.

## Completeness and provenance

The uploaded ZIP variant has 19 files, 18 payload hashes in its manifest. All files are preserved unchanged in `docs/reference/endstate-handoff-2026-09-24/`; [context-manifest.json](../delivery/context-manifest.json) records every payload, archive checksum and preservation check. The earlier published 18-file variant remains on its own branch and in the existing master backup. A different file count is documented rather than silently called identical.

Keep [all build discoveries](../delivery/EMERGENCE-REGISTER.md) separately from this external-research register. Product Emergent Insights is a third, case-scoped concept. Do not mix client-case hypotheses with developer research or software completion.
