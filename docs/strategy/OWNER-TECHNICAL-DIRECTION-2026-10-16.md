# Technical direction: the smallest credible complete system

16 October 2026. Owner instruction: investigate the whole system and take the
technical lead. This records engineering recommendations within the existing
scope. It supplements the original PRDs and [evolution proposal](ENDSTATE-EVOLUTION-PLAN-2026-10-16.md),
and does not authorise deferred runtime research, production use, release or a
further main merge. Task status remains solely in [progress.json](../delivery/progress.json).

## The result we are building

8BALL should help an operator resolve a difficult situation: retain the original
sources, establish what is supported or unknown, define the desired outcome,
compare genuinely different routes, question assumptions, choose a course,
authorise work and separately verify the result. ENDSTATE supplies reusable
calculations beneath that workflow.

We already have multiple conditional routes and isolated What If scenarios.
What If can vary conditions, unavailable actions, budget/deadline, resources and
decisions without saving those assumptions as reality. The current planner has
bounded search and a greedy scheduler. Its results describe declared conditions
and constraints; they do not forecast human behaviour or prove global optimality.

The later ambition remains broader: explore many plausible futures, discover
failure paths, compare robustness and learn from permitted observed outcomes.
Credible probabilities need relevant outcome data, defensible assumptions and
independent validation. More agents, larger graphs and persuasive reports cannot
supply that evidence by themselves.

## Decisions I recommend now

1. **Keep the existing application and engine.** Use its case ledger, exact
   source lineage, reviewed commands and guarded analysis jobs. No framework
   replaces the factual-state or authority boundary.
2. **Prove one explicitly selected model endpoint.** Use the service the owner
   is already obtaining. It must support the actual strict structured-output
   contract, not just chat. Keep the existing frozen generation cases and all
   failed results. Do not make the owner create another account by default.
3. **Finish V0.2 acceptance before adding runtime research.** Improve missing
   evaluation tooling now; actual model quality, professional judgement and
   human usability remain separate gates.
4. **Keep current retrieval and orchestration initially.** SQLite Source Desk
   search and the current persisted jobs are sufficient for this version.
   Codex agents support development; they are not deployed product workers or
   independent professional acceptance.
5. **Use authored adverse scenarios as the first later baseline.** Start from
   one immutable case/target snapshot, declare changed assumptions, and compare
   refusal, delay, withdrawn authority, resource loss and contradictory evidence.
   Measure useful decisions and correction effort before buying simulation scale.
6. **Adopt one specialist per demonstrated need.** Give each candidate a typed
   adapter, isolated compatible environment, predeclared experiment and exit
   criterion. Keep the original source and decision history even if rejected.

## All 28 researched repositories: disposition

These are source-informed recommendations, not installed services or verified
integration claims. [Inventory with full pins and licences](../../research/inventory.json).

| Repository | Position and possible later role | Evidence needed to graduate |
| --- | --- | --- |
| MiroFish | Social-reaction reference application; AGPL obligations and Zep Cloud dependency need review. | Useful social contingencies beyond a single critic/rule baseline; bounded actor/model/report calls. |
| OASIS | Lower-level social platform simulator; an alternative route to MiroFish integration. | Domain action mapping, counted actor failures and independent usefulness; explicit recommender artifacts. |
| AgentSociety | Heavier distributed actor/environment alternative. | Demonstrated need for Ray-scale environment complexity, bounded aggregate spend and complete replay/failure records. |
| Mesa | Preferred first rule-based actor-simulation candidate if What If is insufficient. | Stable release selection, explicit rules/distributions, seeded replications and useful additional decisions. |
| OR-Tools | First scheduling/constraint-search candidate when current planner limits are measured. | Faithful AND/OR/resource/authority translation; small-case oracle, feasibility and timeout/status preservation. |
| pymoo | Later multiobjective search alternative. | Direct Pareto comparison is insufficient; independent feasibility checks and useful search benefit. |
| SALib | Later sensitivity analysis for a defined numeric model. | Defensible parameter ranges, affordable evaluation count, non-finite/constant-output handling and seed reproducibility. |
| DoWhy | Much later causal identification and intervention analysis. | Suitable authorised data, defensible causal assumptions, domain review and held-out refutation/evaluation. |
| EconML | Specialist causal-effect estimation, usually behind a justified DoWhy question. | Relevant observations, support/confounding review and measured uncertainty; no universal route-judging claim. |
| simulatrex-engine | Reference for agent/environment loops and scenario abstractions. | A focused advantage over simpler baselines and pinned modern dependencies. |
| possible-worlds | Older alternative/reference, sharing the `simulatrex` package name. | Separate environment, complete event semantics and corrected/evaluated per-objective input isolation. |
| TencentDB-Agent-Memory | First procedural/team-recall candidate if that exact need is measured. | Core-only explicit adapter; full citations, case/profile isolation, retraction and generated-skill review. |
| Graphiti | Alternative for changing entity/relationship retrieval. | Useful recall beyond literal search, mandatory authorised scope and source/retraction-aware projection rebuilding. |
| Zep | Managed service alternative to operating temporal memory ourselves. | Actual service terms, residency, retention, export/deletion and total model/storage costs. |
| zep-python | Client SDK for the selected Zep service, not another memory server. | Matching service/API version, bounded calls and the same host-owned source/access contracts. |
| Mem0 | Narrow conversational/preference-recall comparison candidate. | Actual need, source/history deletion design, embedding identity and explicitly configured telemetry/egress. |
| Docling | Strong later isolated binary-document ingestion candidate. | Original/derivative coordinate mapping, OCR/page/table review, file/page/time/artifact limits and partial-result visibility. |
| PostgreSQL | Later multi-user production case/event store. | Migration, role/access enforcement, backups and tested restore; not needed to finish fictional local V0.2. |
| Ruflo | Optional developer worker-coordination experiment. | Better independent task results/review effort than existing Codex workers; controlled model routing and terminal publication. |
| LangGraph | Conditional application workflow library if multi-stage/human flows become sufficiently complex. | Explicit durability, repeatable-node side effects and fresh case/permission checks on resume. |
| langgraph-swarm-py | Conversational handoff pattern inside a justified LangGraph experiment. | Concrete advantage from handoffs; no assumption of independent opinions or world simulation. |
| AutoGen | Reference only for a new build; pinned source announces maintenance mode. | Any successor requires a separate need-led source/release assessment; do not assume it is approved. |
| Temporal Python SDK | Later distributed durable operations for timers/recovery/multiple workers. | Operated server/workers, explicit retry/idempotency/spend policies and tested ambiguous external-call recovery. |
| Promptfoo | Optional comparison UI/importer for our retained experiments. | Explicit cache/retry/transform settings, unchanged fixtures and no accidental live execution. |
| Phoenix | Optional private trace/dataset/annotation inspection. | ELv2 server/service-fit review, private trace controls and explicit task/retry semantics; client licence differs. |
| Keycloak | OIDC/MFA option for a later production foundation; existing approved identity is an alternative. | App enforcement, sessions/revocation, operational ownership and supported deployment evidence. |
| OpenFGA | Conditional relationship permission service for complex matter sharing. | Trusted context, current grants/revocation consistency, fail-closed enforcement and denial tests. |
| OPA | Conditional shared policy evaluator across services. | A genuine shared-policy need; versioned authentic inputs and app enforcement; avoid competing grant stores. |

## Why importing everything would fail

The inspected OASIS HEAD requires Python below 3.12, while Mesa HEAD requires
3.12 or later. MiroFish pins different OASIS/CAMEL releases from standalone
OASIS HEAD. Both Simulatrex repositories install the same package/import name.
These are alternatives and dependency sets, not interchangeable puzzle pieces.

Model access is only one operating cost. Recommenders, embeddings, OCR/layout
models, graph stores, simulation rounds, reports, retries and tracing can add
downloads, services and usage. A free Qwen quota does not cover them all.
Licence text in the source does not grant a hosted service account or model
rights. No runtime packages or model artifacts are being installed by this review.

The [source findings](../research/github-2026-10-16/whole-system-review.md) retain
the concrete compatibility, evidence, cost and provenance observations behind
these decisions, including historical fixes and unverified claims.

## Model access and money, plainly

The model in this coding conversation builds the software. The application still
needs its own model service. The only immediate owner input is the service's
**public URL and exact model identifier**, with any private key entered through
secure settings. The agent can set the matching public configuration.

The owner already authorises the repository's fictional examples up to **US$5**
and expects free access. Do not ask for that permission again. Current observed
runtime has no active provider variables/secrets. Current service price, quotas
and private-data terms are not established. For any paid endpoint, confirm prices
and a provider-enforced cap/no automatic top-up before calls; there is no current
application dollar-denominated spending ledger. Fictional `Case.budget=10000`
describes the example case, not the allowed inference spend.

Prefer a single provider-supported non-thinking structured-output configuration.
Record requested and returned model identity, prompt/compiler/schema versions,
all attempts, usage and timings. A model name can remain an alias rather than a
cryptographic weights pin. OpenRouter's explicit `namespace/model:free` variant
is different from its random `openrouter/free` router. Strict provider pinning
and no fallback remain required for frozen-model comparison.

## Acceptance sequence and what I can own

The engineering lead can inspect source, implement fixes and tooling, maintain
provenance, run authorised tests, prepare reviewer materials, compare candidates
and recommend defaults. The owner should not have to select among 28 frameworks.

1. Complete reproducible tooling and source-bound software checks.
2. Once actual service details are active, run the four frozen generation cases.
   Preserve raw/parsed evidence and every failure; fix demonstrated defects
   without turning assisted recovery into an original model pass.
3. Use the matching successful generation receipt to run deliberate lifecycle
   trials and the native actual-provider journey. Record timing races and missing
   remote evidence honestly; never retry a paid trial silently.
4. Approve a prospective independent study with qualified reviewers, independently
   authored held-out cases and task-specific thresholds. Agent review and mock
   success cannot supply those labels or approval.
5. Conduct the owner's end usability/visual review and qualified screen-reader/
   supported-platform review. Record failures, fix them and retain the history.
6. Propose final acceptance only when all original required evidence exists.
   Release, further main merge and deployment still need their own explicit
   decision. Private agency use also needs the separate production foundation.

B02 remains **10/20 required acceptance scopes verified**, ES01 **5/5 internally**.
The ten remaining B02 scopes are actual graph generation; source/identity/date
review; independent quality/model selection; full actual-provider journey;
long-source reconciliation; actual-provider lifecycle/status; human accessibility
and supported environments; owner visual review; dense-graph comprehension; and
the final acceptance decision. This count is not a time estimate.

## Later experiments and stop rules

After V0.2, compare the existing planner, authored scenarios and **one** candidate
on the same frozen fictional case. Start with deterministic/rule-based baselines.
Use OR-Tools only for a demonstrated scheduling/search problem, and Mesa only
for a demonstrated actor/environment problem. Social LLM rehearsal is a separate
OASIS/MiroFish experiment; temporal/procedural memory is a separate retrieval
comparison. DoWhy/EconML need suitable real outcome data and reviewed causal
assumptions much later.

Predeclare missed constraints, unsupported claims, useful alternative failures,
correction effort, latency, complete attempted-call cost and operating burden.
Require zero live-case mutation, invented evidence or authority leakage. Stop a
candidate if it cannot expose failures/model identity, breaches budgets/isolation,
or does not improve independently reviewed decisions enough to justify its cost.
Simulation frequencies remain conditional on the model and assumptions; no
calibrated real-world success probability is claimed without separate evidence.

This is a decision framework with preserved alternatives, not a commitment to
install a large combined stack. It aims to make the first complete, trustworthy
8BALL useful and understandable before expanding it.
