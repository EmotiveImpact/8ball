# ENDSTATE decision, optimisation and simulation candidates

Read-only source research, 16 October 2026. No dependencies were installed, model weights downloaded, provider calls made, or repository application files changed. HEADs below were fetched from native Git and inspected with source-only sparse clones under `/tmp/8ball-swarm-search/`. This is an adoption proposal, not runtime verification or an accuracy claim.

## Recommendation in one paragraph

Keep ENDSTATE as the evidence, authority and outcome-contract core. First finish its existing V0.2 real-provider and human gates. For subsequent scenario work, begin with the existing deterministic What If plus immutable scenario records and a simple transparent comparison table. Prototype OR-Tools only where existing route/schedule bounds create demonstrated difficulty. Use Mesa as a general repeatable simulation candidate and OASIS/MiroFish for the narrower social-reaction experiment. Reserve pymoo for genuinely large multiobjective search spaces. Reserve DoWhy/EconML for later measured-outcome datasets and explicitly reviewed causal assumptions. Installing all five gives no additional correctness by itself.

## What each layer answers

| Layer | Question it can help answer | What it cannot establish by itself |
| --- | --- | --- |
| ENDSTATE contracts | Does this action satisfy the recorded prerequisites, restrictions and human authority? | Whether the source or declared model captures all of reality. |
| OR-Tools | Which declared schedules/assignments satisfy constraints; what objective bound is achieved? | The likelihood that a person cooperates, whether a stated fact is true, or whether an action is authorised. |
| Transparent multi-criteria comparison / pymoo | Which feasible alternatives trade cost, delay, reversibility and other declared scores? | Which preferences are morally or commercially correct; whether estimated risk numbers are calibrated. |
| Mesa / OASIS | What happens within an explicitly specified simulated world as parameters and interactions change? | A real-world success probability without empirical calibration and validation. |
| DoWhy / EconML | Under a specified causal model and data assumptions, what effect might an intervention have, with robustness checks/intervals? | Identification from an arbitrary plan graph or causal truth from fluent text. |
| Human decision | Which evidenced, conditional course is acceptable and authorised? | An automatic guarantee of the future. |

Several different scenario routes can already be compared without a swarm. A swarm is useful when interaction among actors plausibly changes the result and that additional modelling earns its cost in an experiment.

## 1. Google OR-Tools — first optional optimisation candidate

- Repository: https://github.com/google/or-tools
- Inspected HEAD: `100f66e6242ab8bf8d32feb8f3bf086db66ae2b5`.
- Licence: Apache-2.0 (`LICENSE`).
- Actual capabilities: CP-SAT and linear solvers, scheduling/resource constraints, optional intervals, no-overlap and cumulative resource constraints, assumptions, solver bounds and statuses; Python wrapper over native C++.
- Code: [CP-SAT model/solver](https://github.com/google/or-tools/blob/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5/ortools/sat/python/cp_model.py), notably `add_no_overlap` (1411), `add_cumulative` (1448), `validate` (1624), `add_assumption` (1668), `solve` (1752), asynchronous `stop_search` (1781), `best_objective_bound` (1882).
- [Python package manifest template](https://github.com/google/or-tools/blob/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5/ortools/python/setup.py.in): Python >=3.9, NumPy >=2.0.2, pandas >=2, protobuf >=6.33.1,<6.34, absl-py, typing-extensions, immutabledict; native binary platform compatibility must be tested. No LLM or hosted service is required.
- Distinction: `OPTIMAL`, `FEASIBLE`, `INFEASIBLE`, `UNKNOWN`, `MODEL_INVALID` must survive into an explanation; a time limit is not impossibility. All-solution enumeration is available for satisfaction models without an objective; top-k diverse optimised routes require additional modelling, not a single magical switch.
- Fit: existing ENDSTATE `endstate/planner.py` already calculates bounded routes/schedules. An adapter can receive a frozen, fully declared scheduling problem, then return candidate assignments, bounds and reasons. ENDSTATE must revalidate returned routes and retain all unresolved waits and authority requirements. Do not encode unknown prerequisites as false/true just to make a binary solver accept them; either branch declared assumptions explicitly or leave them unresolved outside the solver.
- Experiment: finite fictional DAGs with mutually exclusive routes, precedence, shared resources, budgets, unavailable intervals, deadlines, cyclic/contradictory cases and genuinely unknown waits. Compare current planner, brute-force oracle on small cases and OR-Tools; predeclare runtime limits. Require zero constraint or authority violations; exact agreement with small finite oracle; honest incomplete/timeout reporting; improved useful scheduling coverage or latency on larger cases. No automatic replacement unless measured benefit is material.

## 2. pymoo — useful later for multiobjective alternatives

- Repository: https://github.com/anyoptimization/pymoo
- Inspected HEAD: `23110c155aa8f31b5f1b86928227fb3931ba7f00`.
- Licence: Apache-2.0.
- [Manifest](https://github.com/anyoptimization/pymoo/blob/23110c155aa8f31b5f1b86928227fb3931ba7f00/pyproject.toml): Python >=3.10; NumPy, SciPy, moocore, autograd, cma, matplotlib, alive_progress, Deprecated; optional parallel frameworks. No model endpoint required.
- Actual code: [NSGA-II](https://github.com/anyoptimization/pymoo/blob/23110c155aa8f31b5f1b86928227fb3931ba7f00/pymoo/algorithms/moo/nsga2.py) performs genetic candidate search and rank/crowding selection; [Problem](https://github.com/anyoptimization/pymoo/blob/23110c155aa8f31b5f1b86928227fb3931ba7f00/pymoo/core/problem.py) has objective, inequality and equality dimensions; [minimize](https://github.com/anyoptimization/pymoo/blob/23110c155aa8f31b5f1b86928227fb3931ba7f00/pymoo/optimize.py) accepts seed, termination, callbacks and history.
- Fit: a Pareto frontier shows alternatives where improving one declared measure worsens another, such as speed versus cost versus reversibility. Use actual measured/declared quantities; attach provenance to uncertain estimates. Human preferences and hard limits must remain visible. An LLM/JEV score cannot silently become a fact or permission.
- Limitation: evolutionary search does not generally prove global optimum/completeness. `NSGA2._set_optimum()` selects a lowest-constraint-violation candidate if none is feasible; an adapter must never publish it as eligible. [Repair operators](https://github.com/anyoptimization/pymoo/blob/23110c155aa8f31b5f1b86928227fb3931ba7f00/pymoo/core/repair.py) exist; any candidate transformation must be explicit and independently revalidated, not silent repair of frozen model-generation evaluation outputs.
- Recommendation: first implement direct Pareto filtering of the small route list already generated by ENDSTATE, with sensitivity to declared user preferences. Add pymoo only if large discrete/continuous search requires it. Benchmark against exact frontiers in small cases and repeated-seed quality/runtime on larger ones; retain diversity, feasibility and uncertainty. Do not add a heavy optimiser merely to calculate a weighted score over three routes.

## 3. Mesa — general controlled agent-based simulation candidate

- Repository: https://github.com/mesa/mesa (requested ProjectMesa/mesa redirects).
- Inspected HEAD: `5451086fe47ab78e9ba894aa1b4c3063f4c247f1`.
- Licence: Apache-2.0.
- Current source version is **4.0.0a0**, not a stable-release recommendation. [Manifest](https://github.com/mesa/mesa/blob/5451086fe47ab78e9ba894aa1b4c3063f4c247f1/pyproject.toml) requires Python >=3.12; core NumPy, pandas, tqdm, SciPy (pythran conditional on macOS). Optional graph and visualisation dependencies. No LLM or Zep service is required for rule-based simulation.
- Actual code: [Model](https://github.com/mesa/mesa/blob/5451086fe47ab78e9ba894aa1b4c3063f4c247f1/mesa/model.py) owns agents and RNG; [Scenario](https://github.com/mesa/mesa/blob/5451086fe47ab78e9ba894aa1b4c3063f4c247f1/mesa/experimental/scenarios/scenario.py) freezes parameters after construction and derives seeded replications; [run_scenarios](https://github.com/mesa/mesa/blob/5451086fe47ab78e9ba894aa1b4c3063f4c247f1/mesa/experimental/scenarios/runner.py) runs sequentially or through an executor and records success/failure/aborted runs in a Store. These are actual implementation seams, not only README claims.
- Important version boundary: [migration guide](https://github.com/mesa/mesa/blob/5451086fe47ab78e9ba894aa1b4c3063f4c247f1/docs/migration_guide.md) states 4.0 removes `batch_run`, `seed`, older simulators and other APIs. Scenario sweep code is under `experimental`. Select a stable pinned release and verify the relevant API before adoption; do not mix an old tutorial with this HEAD.
- Fit: operational actors with transparent rules (availability, response delay, workload, escalation, resource contention) can form a cheaper, inspectable baseline to compare against an LLM swarm. Domain behaviour still has to be specified and evaluated; Mesa does not ship an accurate model of fixers, clients or negotiations.
- Experiment: fixed scenario families such as delayed approval, refusal, unavailable specialist, changed deadline; explicit distributions/assumptions; repeat seeds, use paired/common seeds across intervention comparisons when valid, persist input snapshot and outcomes; verify no live case mutation. Compare known hand-authored expectations and simpler What If. Only then test whether LLM actors find independently useful extra contingencies. Simulation frequencies remain conditional simulation frequencies.

## 4. DoWhy — causal model and assumptions layer, after data exists

- Repository: https://github.com/py-why/dowhy
- Inspected HEAD: `10648f1a295cbb40fd9cdd7ce43521a6ef954078`.
- Licence: MIT.
- Actual API [causal_model.py](https://github.com/py-why/dowhy/blob/10648f1a295cbb40fd9cdd7ce43521a6ef954078/dowhy/causal_model.py): model assumptions, identify effect, estimate effect and refute estimate. Refuters include placebo treatment, random/unobserved common causes, data subsets and bootstrap. [gcm/whatif.py](https://github.com/py-why/dowhy/blob/10648f1a295cbb40fd9cdd7ce43521a6ef954078/dowhy/gcm/whatif.py) implements intervention and counterfactual sampling through a causal DAG and fitted mechanisms; observed-case counterfactual inference without noise data requires invertible structural models.
- [Manifest](https://github.com/py-why/dowhy/blob/10648f1a295cbb40fd9cdd7ce43521a6ef954078/pyproject.toml): Python >=3.9,<3.14; NumPy >2, pandas, SciPy, statsmodels, NetworkX, sympy, scikit-learn, causal-learn, numba, cvxpy and **EconML >=0.16 is a main dependency at this inspected HEAD**, despite an extras entry. This is a substantial scientific stack; package pins matter. README says Python 3.8+ but manifest is authoritative for this source snapshot.
- Fit: later questions like whether a type of intervention changes response time rather than merely correlating with it; identifying what additional data is required. ENDSTATE dependency graph is not automatically a causal DAG. A required approval followed by an action is an operational dependency, not statistical causal identification.
- Limitation: passing refutations does not prove all untestable assumptions. Some causal effects are not identifiable; abstention is required. One unique case and synthetic text cannot support population-level causal effect claims. Begin with synthetic known-ground-truth datasets only to validate the pipeline, then ethically authorised real longitudinal data with domain experts and temporal/case heldouts.

## 5. EconML — specialised learned intervention effects

- Repository: https://github.com/py-why/EconML
- Inspected HEAD: `d625dd696ea28c62e6e4d8baea6e4154b98c30b4`.
- Licence: MIT.
- [README](https://github.com/py-why/EconML/blob/d625dd696ea28c62e6e4d8baea6e4154b98c30b4/README.md) explicitly describes heterogeneous treatment effects, measured features/confounders and either no-unobserved-confounding or instrumental-variable assumptions. Source implements cross-fitted residualisation in [CausalForestDML](https://github.com/py-why/EconML/blob/d625dd696ea28c62e6e4d8baea6e4154b98c30b4/econml/dml/causal_forest.py), plus [effect_interval](https://github.com/py-why/EconML/blob/d625dd696ea28c62e6e4d8baea6e4154b98c30b4/econml/_cate_estimator.py).
- [Manifest](https://github.com/py-why/EconML/blob/d625dd696ea28c62e6e4d8baea6e4154b98c30b4/pyproject.toml): Python >=3.9, NumPy >=2.0.2, numba >=0.60, SciPy >=1.13.1, scikit-learn >=1.6,<1.10, sparse, joblib, statsmodels, pandas, SHAP, LightGBM, packaging. Optional DoWhy is constrained >=0.13,<0.15; runtime compatibility must be tested rather than combining arbitrary HEADs. Compiled extensions also matter.
- Fit: long-term outcome learning with sufficient repeated, authorised comparable observations. Useful for different intervention effects across observed contexts. It is not a universal decision judge, and confidence intervals are conditional on identification/model/data assumptions.
- Recommendation: no separate initial adoption; retain as an optional DoWhy-compatible estimator when the data/causal question justifies it. Prespecify identification, overlap, confounding, temporal split, interval coverage and baseline comparisons. Record limitations and abstain outside support.

## 6. SALib — numeric sensitivity once the scenario has measurable outputs

- Repository: https://github.com/SALib/SALib; inspected source at `748cf169e82227bcc56dcfc961fcfb03a1e0df45` supplied by parent and fetched at that exact raw SHA.
- Licence: [MIT](https://github.com/SALib/SALib/blob/748cf169e82227bcc56dcfc961fcfb03a1e0df45/LICENSE.md). [Manifest](https://github.com/SALib/SALib/blob/748cf169e82227bcc56dcfc961fcfb03a1e0df45/pyproject.toml): Python >=3.10, NumPy >=2, SciPy >=1.9.3, matplotlib, pandas >=2, multiprocess. No model endpoint required.
- Actual [Sobol sampler](https://github.com/SALib/SALib/blob/748cf169e82227bcc56dcfc961fcfb03a1e0df45/src/SALib/sample/sobol.py) creates a prescribed numeric experiment design; [Sobol analyser](https://github.com/SALib/SALib/blob/748cf169e82227bcc56dcfc961fcfb03a1e0df45/src/SALib/analyze/sobol.py) takes the numeric output vector Y and returns first-order/total-order sensitivity estimates with resampled intervals, plus second-order interactions optionally. [Morris analyser](https://github.com/SALib/SALib/blob/748cf169e82227bcc56dcfc961fcfb03a1e0df45/src/SALib/analyze/morris.py) offers screening of factor effects.
- Fit: once a scenario maps explicit bounded parameters to quantities such as completion delay or resource shortfall, identify which assumed ranges drive the result. This can help decide which uncertain input is worth investigating. Input range/distribution choices must be explicit, and dependence among inputs needs a suitable method/design. Sensitivity is not causal identification or an estimate that an action will succeed.
- Limit: freeform model narratives are not a numeric function merely because a judge assigns them a score. Begin with deterministic simulator outputs and known synthetic functions; control seeds/noise and repeated runs for stochastic models. Freeze the output measure and input distributions before analysis.
- Cost: the inspected Sobol sampler documents N*(D+2) evaluations without second-order terms and N*(2D+2) with them. Multiplying that by an LLM swarm can be expensive. Use transparent cheap baselines/screening first, then a separately capped expensive experiment if justified. Do not silently launch thousands of model calls.

## Minimal staged adoption

1. Complete unchanged 8BALL V0.2 generation, provider lifecycle and actual human/independent acceptance. Existing 964+964+384 software evidence does not close these gates.
2. Implement a future generic scenario contract around frozen ENDSTATE revisions, explicit changed assumptions, provenance, limits, output classification and no live mutation. Baseline: hand-authored What If and direct route comparisons.
3. Run an isolated OR-Tools experiment only on demonstrated scheduling/search shortcomings; add it as a replaceable adapter if it outperforms the current engine and preserves contracts.
4. Prototype one general simulation engine (Mesa candidate) and one social-reaction engine (OASIS/MiroFish candidate) against the same declared fictional challenge, with bounded runs and independently scored incremental usefulness. Avoid installing competing orchestrators merely because they have overlapping features.
5. Use a decision panel separating hard eligibility, observed quantities, uncertain forecasts and human priorities. JEV or another model may produce a labelled critique/recommendation only after task-fit testing; deterministic checks remain authoritative for constraints and humans remain authoritative for decisions.
6. Capture authorised real outcomes and prediction records; only then introduce forecasting calibration and later DoWhy/EconML causal learning. Add pymoo if candidate space growth proves direct Pareto filtering insufficient.

## Cross-cutting experimental acceptance

Before a candidate graduates, freeze the hypothesis, baseline, case split, metrics, thresholds, version/environment, licence obligations and resource budget. Retain raw inputs/outputs/failures. Require zero leakage between case/scenario/live state; zero invented evidence/approval; reproducible deterministic calculations; honest interrupted/incomplete results; separate synthetic conditional outcomes from calibrated probabilities; documented cancellation; measurable incremental value after correction burden, cost and latency. Human usefulness judgements require actual independent human reviewers, not agent votes. Reassess current release pins and licences at adoption time.

Source confidence: high for the inspected APIs, manifests, version boundaries and licence texts; moderate for fit recommendations; no runtime, integration, numerical accuracy, security or predictive validation was performed in this read-only pass.
