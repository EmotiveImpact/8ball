# Bounded specialist review

This is an opt-in **engineering host integration**, not a default running swarm, a forecast generator or a production deployment. It uses the existing event-processing attempt and review path; it does not add another queue. No new inference was run for this implementation. Mocked native HTTP tests establish contracts and controls, not model quality.

ENDSTATE's `ReviewSpec` declares one to three distinct decision models, the exact questions, a time budget and a reported-cost stopping threshold. `summarize` retains each answer/distribution, unprocessed models, missing answers and disagreement without voting, ranking or approving. Choice confidence is not a calibrated event probability. Source facts, human decisions, rehearsals and actual outcomes remain separate.

The host explicitly constructs `SpecialistReviewProcessor(spec, allow_external=True)` and supplies it to `AgencyHost(..., processor=processor)`. The default processor remains absent. Model/provider selection is trusted host configuration in this slice, **not a new operator model-selection screen**. Source processing still requires its existing explicit review, current source policy and READ/INFER authority. Select and verify provider/data-processing policy before any real use; ordinary acceptance removes credentials and uses fictional fixtures.

Only the reviewed incoming event's text is sent. The complete case snapshot, other sources, private graphs and other matters are not appended. Result provenance binds the receipt, input, configuration and case revision. The source-processing review binds the processor configuration digest; changing selected models, questions or budgets requires a fresh review before processing. Request bodies retain native `/v1/systemone` versus `/v1/decisions` shapes. No chat fallback is added.

Each selected model gets one single-use `DecisionSession`. There is no retry, replacement model, hidden cascade, automatic resume or automatic provider request on import. Errors stop later models; partial validated answers remain labelled partial by the missing-model list and stop reason. Invalid answers are not counted. Unknown/non-integer reported nano-USD costs stop further requests. The report separates known reported costs from unknown attempts. Neither that threshold nor a local timer enforces provider billing or recalls a request already sent. A running request may exceed the threshold, complete after cancellation or be charged; stopping prevents subsequent calls and publication, not remote computation.

`EventWorkerService` preserves ordinary two-argument processors and adds an explicit cooperative protocol. The host checkpoints current identity, scope, source policy, source review, configuration, revision, claim token, cancellation and lease before/after each request and at publication. Provider calls occur outside write transactions. The existing application inference slot is shared with local analysis; waiting attempts recheck authority and lease. Standalone event services default to one slot. This remains one-process engineering infrastructure, not a distributed scheduler.

Completed/partial advisory reports are retained for the existing event review/status reader. They are **not graph patches** and are never automatically converted into observations, operator-declared objections, dispositions, chosen courses or approvals. The existing graph preview and commit still require a separate explicit human command. Dedicated model-selection controls and evidence-based usefulness evaluation remain follow-up work.

The incoming-change review now shows a read-only specialist comparison beside the preserved original output: each selected model's choice, missing or failed answers, unresolved differences, reported-cost uncertainty and request/response hashes. The server reconstructs the comparison using ENDSTATE's contracts and verifies the retained summary and receipt/input/spec/case/revision bindings before presenting it. Unknown versions, inconsistent summaries and invalid bindings do not get a typed presentation; original output is still retained for inspection. This is local integrity checking, not independent provider attestation. Historical results name their base revision, not the current case. All content shares the existing read/source-policy gate and is cleared on lock or detected revocation. Inspection makes no provider calls, casts no vote and cannot apply model answers to the graph.

Tests cover exact reviewed-text isolation, differing model choices, invalid/missing answers, unknown costs, budget/time stops, no retry, source/grant/review/configuration/revision/cancellation/lease changes between calls, shared-slot waiting and final-transaction publication races. Legacy event-review behavior and old source-free exports remain under regression tests. Report hashes are local integrity references, not independent attestations or proof that a provider served a particular model.

## Opt-in coordinated planning

`endstate.intelligence.planning.coordinate` adds one bounded method, not an
unrestricted swarm: one proposer makes a two-stage original draft; the configured
decision specialists independently answer the same declared questions about that
original; the same proposer sees **every** retained answer and makes a separate
two-stage revision. Both drafts use the unchanged strict target-coverage checks,
frame/route validation and deterministic compiler. The original proposal, panel
and revision are separate records. `final_synthesis` points to the revised
candidate for human review; it neither chooses a route nor claims objections
resolved. An unchanged revision is permitted. There is no majority rule.

The independent `SpecialistReviewProcessor` remains available as its own baseline.
The new `CoordinatedPlanningProcessor` implements the same cooperative host
interface and shared inference slot. The host constructs a
`CoordinatedPlanningSpec` with an explicit human outcome, `ReviewSpec`, overall
deadline of at most 600 seconds and
`planning_cost_policy='explicit_unpriced_token_bound'`, then passes the processor
to the existing agency host with `allow_external=True`. There is no default
activation, new queue, client-supplied provider setting or model-selection UI.
Configure an appropriate event-work lease explicitly (at most 600 seconds); the
ordinary 60-second lease is **not** silently extended for a multistage attempt.

Only the reviewed event text, the explicitly configured outcome and derived
advisory proposal/answers are shared. Other snapshot content is never appended.
The processing review binds the method, spec, validated server-owned provider
settings (including credential rotation through an opaque digest), four maximum
generation attempts and 4,096 maximum output tokens per generation request.
The opaque digest also binds the specialist credential; rotation of either key
requires fresh review. Generation uses a single frozen compatible/native session. Each served planning
model ID must exactly equal the configured requested ID; no alias, substitution,
repair or fallback is introduced. GLM still requires explicitly selected
prompt-only mode; local draft validation is identical.

**Budget scope matters:** the decision API's reported-cost threshold does not
cover planning APIs, which report tokens but not verified charges. The unpriced
planning policy is required, without a default, so the host must explicitly
approve a finite call/token allowance before source-processing review. Reports
label planning cost unknown and billing unverified; this is not a dollar cap or
a claim that generation is free. Unknown decision cost, an exhausted decision
threshold, failure or a missing answer stops before any revision. Deadlines
prevent later calls, not remote processing or billing of an in-flight request.

Every provider call is bracketed by current-authority checkpoints. Cancellation,
changed permissions/source policy/configuration/revision or lease expiration
prevents later calls and publication. Other failed/partial advisory results retain
the original proposal, available traces and provider receipts; source-policy
revocation does not grant permission to publish those bytes. Planner receipts
include exact bounded raw assistant text and transport hashes where safe. A
200,000-byte cumulative planning-receipt limit stops further requests; raw text
that exceeds it is explicitly omitted, with hashes retained, not claimed recoverable.
Native specialist receipts and original validated answer shapes are separate from
the normalized panel. Unrequested envelope fields and unvalidated native payloads
are not copied into storage or revision; their omission and envelope hash remain
explicit. No private hidden reasoning is requested or retained. The existing
500,000-byte host result limit still applies. An overlong derived
specialist input fails without truncation; a valid original draft remains separate.

The new report kind is `coordinated_planning`. Its original JSON can be inspected
through the existing permission-gated event review, but **the readable specialist
card is not a coordinated-report card**. No new presentation, automatic graph
commit, observation, approval, action or course selection is included. The
specialists supply bounded choice/distribution answers, not free-form rebuttals;
question design limits what they can challenge. Controlled software checks do
not establish better plans, predictive accuracy or operator usefulness. A frozen
fictional single-model/panel/coordinated diagnostic and independent human-quality
review remain distinct follow-ups.

## Current read-only coordinated presentation

The preceding backend-only presentation limitation is superseded by the coordinated result card in authenticated incoming-change review. It separately shows the original proposal, every independent choice/distribution, incomplete or failed stages, revision and advisory synthesis. It never applies a graph or authorises action. The server recompiles retained drafts, reconstructs comparisons and validates stage/source bindings; invalid summaries remain raw-only. Current read/source-policy gates and historical revision labels apply to every stage. Canonical serialization is handled using hash-checked raw provider JSON where available, not output repair. See [implementation and limitations](../delivery/sessions/2026-10-26-coordinated-result-ui.md). Native scripted verification is not independent quality or human acceptance.
