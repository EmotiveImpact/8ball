# ENDSTATE: research decision register

Date: 24 September 2026
Status: Research proposals only. Not an approved roadmap amendment, implementation, installation, dependency approval or release.
Scope: ENDSTATE reusable engine and its first application, 8BALL. External sources: Simulatrex, The People Machine, Matt Pocock skills, Wayfinder, Wayfinder Maps and chartr.

## Decision summary

Preserve the existing evidence-supported, deterministic outcome kernel. Evaluate external ideas at three separate levels: development practice, engine semantics and optional experimental adapters. Do not replace the kernel with a behavioural simulator or treat a coding-agent skill as an enforceable runtime policy.

The strongest proposed extension is to make the dependency between evidence, assumptions, decisions and routes easier to inspect and invalidate. A second extension is to expose two distinct frontiers: the investigations that are ready to undertake and the operational actions that are authorised and eligible. A third is isolated scenario rehearsal, initially with explicit deterministic assumptions and later with evaluated model-generated hypotheses.

## Inspection boundaries

All four public repositories returned for the Simulatrex organisation were considered. Documentation was reviewed across the supplied projects, with selective source inspection of Simulatrex's API, parser, playground simulation entities, model wrapper, agent module and subpopulation experiment runner, plus the Wayfinder skill and local tracker contract and chartr plugin documentation.

This was not an exhaustive line-by-line audit or installed runtime evaluation. Container Git clones failed because network name resolution was unavailable; repository content was retrieved through GitHub and web tools. No package or model was installed and no external inference benchmark was run. No client data was sent to these projects. No repository changes or merges were performed.

Inspected Simulatrex engine develop tree: 4e4fa06d7f527480b66ceb224a5d37bcfa2f9150. Inspected subpopulation tree: deb67cfccb7df20b468987fd7ba6cc2a53adb9cc. Mutable external references must be refreshed and pinned before any adoption.

The live 8BALL PR #2 remained open and draft at head 824ca6421ff3100e1af596347f2d1247dde8f8dc. The recovered 24 September local delivery snapshot records ENDSTATE core 4/5 scoped subparts verified and 8BALL V0.2 9/20, neither accepted. These are not completion percentages and the local snapshot is not proof that its cumulative changes are published.

## Proposed dispositions

| Item | Proposed disposition | Boundary |
| --- | --- | --- |
| Matt Pocock engineering skills | Selectively adapt for development | Preserve existing PRD, ledger, human decisions and acceptance gates |
| Wayfinder method | Use for bounded unresolved design questions | Do not introduce a second authoritative delivery tracker |
| Wayfinder Maps | Study derived views, invalidation and graph linting | Do not use its serial Markdown adapter for concurrent case state |
| chartr | Optional developer workbench experiment | Not a kernel or customer-data dependency |
| Simulatrex engine | Architectural reference; isolated experiment only | No direct adoption as ENDSTATE's truth or planning layer |
| possible-worlds | Historical scenario/event reference | Do not count a fork as independent behavioural validation |
| llm-subpopulation-research | Experimental design reference | Model-response variation is not measured human behaviour |
| AlpacaDataCleaned | Exclude from commercial training by default | Dataset documentation states non-commercial restrictions |

## Evidence and hypothesis register

The following are proposed improvements, not claims that the current engine lacks every related mechanism. The existing PRD already includes question impact, isolated scenarios, revision semantics and stale-approval invalidation. Implementation begins by inspecting and extending those mechanisms, not duplicating them.

### R01: Premise-linked decision validity

Hypothesis: Explicit links from a decision's rationale to evidence, assumptions and constraints make changed circumstances easier to handle correctly.

Prototype: Add or reuse references to the base revision, supporting evidence IDs, unresolved assumptions, approver, scope and invalidation conditions. Derive a stale or review-required projection when a referenced premise changes. Preserve both the historical decision and the reason it was reopened.

Test: Retract a supporting source, alter an action prerequisite, resolve a contradiction and revoke an approval in separate fixtures. Compare affected decisions/routes with expert-labelled expectations. Verify that irrelevant changes do not indiscriminately invalidate all work.

Hard boundary: A changed premise must not silently turn into a new human decision. No deletion of historical rationale.

### R02: Investigation and execution frontiers

Hypothesis: Operators benefit from seeing the next answerable questions separately from the next executable actions.

Prototype: Derive an investigation frontier from unresolved, unblocked, case-authorised inquiries. Derive an execution frontier from action prerequisites, resources, timing, authority and current approvals. Reuse the existing question-impact and next-action interfaces where available.

Test: Create cases with an action blocked by unknown authority, an unrelated unresolved question, conflicting evidence and time-sensitive prerequisites. Verify that the right investigation becomes eligible without prematurely authorising the action.

Hard boundary: An answered question is not automatically a verified condition; a resolved planning ticket is not a completed real-world outcome.

### R03: Explicit alternative world assumptions

Hypothesis: Maintaining a small set of competing explanations reduces the risk of planning around one unsupported interpretation.

Prototype: Represent alternatives such as unknown stock availability, uncertain decision authority or disputed delivery dates as labelled assumptions in isolated branches. Compute route feasibility under each branch using the same kernel.

Test: Compare results with hand-authored reference branches. Report which prerequisite changes feasibility and which evidence would distinguish the alternatives.

Hard boundary: Do not infer hidden motives or assign probabilities merely because a language model produces a plausible story.

### R04: Rehearsal provider contract

Hypothesis: A provider-neutral rehearsal interface can add useful failure cases without compromising evidence integrity.

Proposed input fields: case-scoped snapshot reference, base revision, objective IDs, candidate route IDs, explicit assumptions, permitted scenario perturbations, provider configuration, maximum calls, elapsed-time limit and cost budget.

Proposed output fields: provider/model version, prompt/schema version, source set, synthetic branch IDs, perturbed assumptions, simulated events, kernel validation results, limitations, errors, cost and latency. A seed can be recorded where supported; it is not a universal reproducibility guarantee. Preserve returned outputs for replay.

Test: Begin with deterministic scripted branches. Only then compare an LLM-generated branch provider against the baseline using independently reviewed cases.

Hard boundary: Synthetic events can enter a scenario branch only. They cannot satisfy live outcome verification, manufacture actor authority or bypass an approval.

### R05: Robustness without invented probabilities

Hypothesis: A route comparison that explains fragile dependencies, fallback coverage and reversal costs is useful before calibrated behavioural forecasting exists.

Prototype: For each route report supported prerequisites, unresolved prerequisites, scenarios in which it remains feasible, binding constraints, fallback options and reversible versus irreversible commitments. Label scenario counts as coverage of the chosen test set, not frequencies of real events.

Test: Change the scenario set deliberately and check whether rankings depend on arbitrary scenario sampling. Expose that dependence to the operator rather than presenting a universal score.

Hard boundary: Ten favourable synthetic reactions out of twelve do not establish an 83% chance of real success.

### R06: Expert practice to evaluated domain packs

Hypothesis: Human-authored expertise can become reusable domain inputs without becoming an unconstrained prompt library.

Prototype: Compile an approved playbook into proposed typed actors, evidence requirements, action preconditions, effects, resources, approval policies and outcome-verification rules. Require review and versioned tests before acceptance.

Test: Use the same engine with a neutral fixture and two adjacent domain fixtures. Evaluate whether vocabulary and policy vary without planner duplication or information leakage.

Hard boundary: A skill file is neither professional qualification nor legal authority. Updating one cannot silently change an active case's policy.

### R07: Decision-centred research memory

Hypothesis: Research remains more useful when each finding names the decision it informs, its evidence level and its adoption condition.

Prototype: Store concise findings, direct sources, inspected versions, counterevidence, proposed disposition and remaining uncertainty. Generate an index rather than duplicate full records in multiple places.

Test: A fresh session should recover the accepted scope and next unresolved research question without treating an experiment as a shipped capability.

Hard boundary: Preserve existing delivery and emergence-review rules. New research becomes mandatory build scope only through an explicit decision.

## Evaluation sequence

1. Complete or preserve the existing ES01-05 and B02-09/B02-11/B02-12 acceptance work. Do not count these proposals as satisfying it.
2. Evaluate R01 and R02 on fictional fixtures using existing kernel functions and established revision semantics.
3. Add deterministic R03/R04 branches and verify zero changes to live evidence, authority or completion state.
4. Compare three approaches on separate held-out cases: current kernel, kernel plus hand-authored scenarios, and kernel plus model-proposed scenarios.
5. Have reviewers judge missing dependencies found, unsupported assumptions introduced, useful fallback discovery, correction effort and decision usefulness. Record costs, latency, errors and abstentions.
6. Consider model-based rehearsal only where it adds material value over the cheaper baseline. Validate each new domain separately. Do not weaken thresholds after seeing a failed result.

Historical case evaluation must use only the evidence available at the chosen historical cut-off. Future outcomes and later documents must not leak into prompts, retrieval or case construction. Training, development and final evaluation cases must be separated at the case level. Real-person data requires the appropriate authorisation and processing controls.

## Focused source register

Project authority: 8BALL-ENDSTATE-Master-PRD.md, revision 1.1, 23 September 2026; 8BALL-Integrated-Build-Checklist.md, reviewed 24 September 2026. These were recovered from the user's Library, not replaced by public web material.

- Live project PR: https://github.com/EmotiveImpact/8ball/pull/2
- Simulatrex organisation: https://github.com/simulatrex
- Simulatrex website: https://simulatrex.com/
- The People Machine, 2 February 2024: https://dominikscherm.substack.com/p/the-people-machine
- Simulatrex engine: https://github.com/simulatrex/simulatrex-engine
- Inspected API: https://github.com/simulatrex/simulatrex-engine/blob/develop/api/server.py
- Inspected parser: https://github.com/simulatrex/simulatrex-engine/blob/develop/src/simulatrex/dsl_parser.py
- Inspected playground runtime: https://github.com/simulatrex/simulatrex-engine/blob/develop/src/simulatrex/simulation_entities.py
- Inspected model wrapper: https://github.com/simulatrex/simulatrex-engine/blob/develop/src/simulatrex/llms/models/models.py
- possible-worlds: https://github.com/simulatrex/possible-worlds
- Subpopulation research: https://github.com/simulatrex/llm-subpopulation-research
- Inspected experiment runner: https://github.com/simulatrex/llm-subpopulation-research/blob/main/experiment.py
- Alpaca data and licence notice: https://github.com/simulatrex/AlpacaDataCleaned
- Matt Pocock skills: https://github.com/mattpocock/skills
- skills.sh distribution listing: https://skills.sh/mattpocock/skills
- Wayfinder article: https://www.aihero.dev/skills-wayfinder
- Current Wayfinder skill: https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md
- Wayfinder Maps: https://github.com/rengwu/wayfinder-maps
- Local tracker contract: https://github.com/rengwu/wayfinder-maps/blob/main/skills/wayfinder-maps/TRACKER-MARKDOWN.md
- chartr: https://chartr.dev/
- chartr source and licence: https://github.com/rengwu/chartr
- chartr plugin trust model: https://github.com/rengwu/chartr/blob/main/docs/plugins.md
- Park et al., Generative Agent Simulations of 1,000 People: https://arxiv.org/abs/2411.10109
- Hullman et al., Validating LLM simulations as behavioral evidence: https://arxiv.org/html/2602.15785v1
- Bojic et al., Persona-prompted LLM agents achieve modest but genuine prediction of human social media reactions, Scientific Reports, 3 September 2026: https://www.nature.com/articles/s41598-026-66277-8

## Current research conclusion

Adopt selected development practices; adapt structural decision and uncertainty patterns; evaluate isolated rehearsal; decline unvalidated prediction claims and unsuitable data/dependencies. ENDSTATE's differentiating asset should remain the disciplined connection between evidence, constraints, alternatives, authorised action and verified outcomes. The experiments above are designed to test whether the new ideas strengthen that connection.
