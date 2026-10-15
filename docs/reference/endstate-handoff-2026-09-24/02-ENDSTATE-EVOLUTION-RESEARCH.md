# ENDSTATE evolution research - Simulatrex, Wayfinder, skills, chartr and the larger possibility

## Why this research matters

The research did **not** replace the original ENDSTATE idea.

It expanded the ceiling.

The original core remains:

```text
current evidenced state
+ desired state
+ permitted actions
+ constraints
→ conditional routes
→ human decisions
→ observed results
→ updated routes
```

The expanded long-term thesis is:

```text
UNDERSTAND THE WORLD
        ↓
DEFINE THE END STATE
        ↓
MODEL WHAT CAN CHANGE
        ↓
IDENTIFY WHAT MUST BE LEARNT
        ↓
PREDICT WHAT MAY HAPPEN
        ↓
SIMULATE POSSIBLE FUTURES
        ↓
STRESS-TEST ROUTES
        ↓
CHOOSE / APPROVE ACTIONS
        ↓
OBSERVE REALITY
        ↓
REPLAN
        ↓
LEARN FROM OUTCOMES
```

ENDSTATE should become a system for continuously steering a changing real-world situation towards a defined outcome.

## Prediction is part of the vision

The direction is **not** "do not predict people".

The direction is:

> Predict where there is a defensible basis to predict. Simulate where there are only assumptions. Never silently treat simulation as observed evidence.

Prediction can develop in layers.

### 1. Deterministic prediction

"If these conditions become true, this action becomes eligible."

Already close to current planning logic.

### 2. Operational forecasting

Examples:

- expected response time
- deadline risk
- probability of an approval taking longer than normal
- supplier reliability
- likely resource bottleneck

Can use historical data and statistical models.

### 3. Behavioural prediction

Examples:

- probability a prospect replies
- probable objection categories
- likely delay/refusal/counter-offer
- likely stakeholder escalation

Should be calibrated against real outcomes where possible.

### 4. Multi-actor prediction

Model chains of reaction across people and organisations.

### 5. Possible worlds

Generate many plausible future branches and identify routes that remain useful across a wide set of futures.

## The key semantic distinction

If 8 of 10 synthetic personas say "yes", that does **not** automatically mean an 80% real-world probability.

It means 8 of 10 simulations produced that response under a particular model and assumptions.

A real probability claim should eventually have calibration evidence such as:

- relevant historical interactions
- held-out evaluation
- model/version identity
- feature/source set
- calibration method
- confidence interval or uncertainty
- observed post-prediction outcomes

This distinction is a potential competitive advantage, not a limitation.

## Simulatrex

Research sources:

- https://github.com/simulatrex
- https://simulatrex.com/
- https://dominikscherm.substack.com/p/the-people-machine
- `simulatrex/simulatrex-engine`
- `simulatrex/possible-worlds`
- `simulatrex/llm-subpopulation-research`
- `simulatrex/AlpacaDataCleaned`

### Useful ideas

- generative agent-based modelling
- agents with persona/trait descriptions
- environments
- event-driven simulation
- repeated scenario experiments
- model-provider abstraction
- evaluation against objectives
- possible-world thinking
- behavioural experimentation

### Important implementation finding

The inspected public playground/runtime is much thinner than the full product proposition.

In one inspected path:

- DSL defines agents, environment and simulation
- environment loops through agents
- an agent asks an LLM to generate an action
- the inspected action prompt does not demonstrate rich evidence-grounded actor state being used as a calibrated predictive model
- named interactions are logged by the simple simulation entity path
- API state uses process-global simulation task/log structures

Therefore:

**Use Simulatrex as research material and inspiration. Do not treat the public repo as a production-grade human-prediction engine.**

### What ENDSTATE can do differently

ENDSTATE already has stronger requirements around:

- provenance
- observed vs disputed vs unknown
- revision-bound state
- action prerequisites
- authority
- human review
- completion vs effect
- scenario isolation
- audit
- replanning

The opportunity is to add behavioural/possible-world simulation **on top of** those semantics.

## Wayfinder / Wayfinder Maps

Research sources:

- https://www.aihero.dev/skills-wayfinder
- https://github.com/rengwu/wayfinder-maps
- https://www.skills.sh/mattpocock/skills
- https://github.com/mattpocock/skills

### Strongest idea to adapt

Separate:

- **what should we learn next?**
- **what can we execute next?**

ENDSTATE should eventually expose two frontiers.

### Investigation frontier

Questions that are now worth answering because their resolution will reduce route uncertainty or unlock a decision.

### Execution frontier

Actions whose conditions, authority, resources, timing and approvals are currently satisfied.

This is more powerful than a single task queue.

### Premise / decision dependency

Decisions should explicitly record what facts and assumptions support them.

A later fact, retraction or decision can undermine earlier reasoning.

Desired relationship:

```text
evidence
  ↓
premise / condition
  ↓
decision
  ↓
route
  ↓
approved action
```

When a supporting premise changes:

- identify affected decisions
- invalidate or mark them stale according to policy
- recompute affected routes
- explain exactly why the plan changed

This strengthens the existing What Changed and stale-approval model.

### What not to copy blindly

Development trackers can infer resolution from file/ticket conventions. ENDSTATE cannot infer real-world truth from documentation conventions.

Superseded reasoning should remain auditable.

Workflow notes never grant real-world authority.

## Matt Pocock skills

The value is primarily development discipline:

- primary-source research
- specification
- domain modelling
- TDD
- implementation review
- specification-compliance review
- Wayfinder decision mapping

Use selectively.

Do not install an entire external skill collection and let it become a competing source of truth.

Our PRD, task ledger, evidence and decisions remain authoritative.

## chartr

Sources:

- https://chartr.dev/
- https://github.com/rengwu/chartr

The useful idea is a developer workbench that can bring terminals, agents, planning and plugins into one environment.

This is optional development tooling.

It should not become an ENDSTATE dependency.

Any plugin/native extension research should happen in a controlled environment because developer plugins may execute with the user's authority.

## The larger ENDSTATE architecture

Long term, think in layers.

### WORLD

What is true?

- entities
- actors
- organisations
- relationships
- evidence
- claims
- events
- resources
- constraints
- authority
- time

### END STATE

What must become true?

- objectives
- success conditions
- failure conditions
- acceptable compromises
- deadlines
- boundaries

### CAUSAL / ACTION MODEL

What can change the world?

- actions
- prerequisites
- effects
- side effects
- resources
- restrictions
- actors
- verification

### WAYFINDER

What must be learnt or decided before action?

- questions
- investigations
- decisions
- premise dependencies
- invalidation

### PREDICTION ENGINE

What is likely to happen?

- operational timing
- failure likelihood
- actor behaviour
- organisational behaviour
- response distributions
- second-order effects

### POSSIBLE WORLDS

What could happen?

Branch many futures from an immutable base revision.

### RED TEAM / STRESS ENGINE

How does our plan fail?

Examples:

- actor refuses
- evidence is wrong
- approval disappears
- resource is unavailable
- event happens earlier/later
- competitor moves
- objective changes

### ROUTE ENGINE

Which route still works under the widest credible range of futures?

Be careful with language. Early "71% of scenario families survived" is not the same as "71% probability of success".

### LIVE REPLANNING

Observe → interpret → review → update → invalidate affected reasoning → recompute → explain.

### DOMAIN INTELLIGENCE

Domain packs supply:

- vocabulary/mappings
- action catalogue
- policies
- permissions
- success evidence
- prompts
- integrations
- domain-specific predictors
- evaluation sets

### LEARNING / CALIBRATION

Compare predictions to actual outcomes.

Prediction becomes better only when reality can correct it.

## Research conclusion

We are not trying to create another chatbot, another generic agent framework or another simulation toy.

The emerging category is closer to:

**Outcome intelligence infrastructure**

or:

**a system that understands a changing situation, models an end state, finds routes, predicts and stress-tests what may happen, and continuously adapts as reality changes.**
