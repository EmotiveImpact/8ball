# Evolving emergence register: nothing silently discarded

> Generated from `docs/delivery/emergence.json`. Decision history lives there; delivery status comes only from `progress.json`. Run `python scripts/emergence.py --write`.

8BALL remains the fixer product. ENDSTATE supplies reusable calculations. This is the build-discovery register, not a client-case insight ledger.

Last review: 2026-10-25. **112 recorded discoveries.**

**Read the marks correctly:** `[x]` requires the linked acceptance scope to be verified. `[ ]` means open, partial, implemented-but-unaccepted, or a candidate. Strikethrough means declined or superseded, not deleted. An owner can reopen any decision with a new history entry.

## Mandatory questions at sprint close

- **ER-01 (both):** What did we discover that was not explicit before, and what exact evidence made it visible?
- **ER-02 (both):** What could disprove the finding, and what conflicting or missing evidence have we considered?
- **ER-03 (situation):** Which declared dependencies, actors, decisions or sources connect apparently separate candidate routes?
- **ER-04 (situation):** Which verification question or review could most change our available options?
- **ER-05 (situation):** Are we still working towards the client’s explicit target and success criteria?
- **ER-06 (situation):** What may be stale, what could follow from our actions, and what event should make us reconsider?
- **ER-07 (build):** Which findings belong in 8BALL, ENDSTATE, an existing task, or a retained future candidate?
- **ER-08 (build):** What are we not implementing, why, and where can the owner review or reopen that choice?
- **ER-09 (build):** What actually passed, what failed, and which claimed capabilities still need independent or native verification?
- **ER-10 (both):** What might we still have missed, and how can the operator or owner record their own hypothesis?
- **ER-11 (both):** What course has an authorised human selected, and what exactly would require reconsideration rather than an automatic switch?
- **ER-12 (both):** Which available inputs were not processed, what limits bound this conclusion, and what could exist outside the current catalogue?
- **ER-13 (both):** When analysis fails, what safe recovery is available, who contributed the correction, and is the original failure still recorded?
- **ER-14 (build):** Can the exact implementation and evidence for every delivery claim be recovered, or must that claim remain reported-only?
- **ER-15 (both):** Does this improve the operator’s next decision or merely increase reviews, alerts and screens? How would we measure the difference?

## Complete owner-review register

### [x] EM-001: Two linked graphs, not one ambiguous picture

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

The provenance/reality graph and the outcome/action graph answer different questions.

**Product implication:** Keep observations distinct from planned effects and expose their links without claiming causation.

**Roadmap links:** `B02-01` (verified), `B02-03` (verified), `ES01-02` (verified).
**Completion scope:** `B02-01`, `B02-03`, `ES01-02`.
**Evidence / source record:** `docs/v2/ARCHITECTURE.md`, `docs/delivery/EMERGENCE-REVIEW.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-002: Information acquisition is part of the plan

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Obtaining evidence can matter more than executing the next outward-facing action.

**Product implication:** Create reviewable verification questions from structural findings; explore a distinct knowledge-action type later.

**Roadmap links:** `B02-05` (verified), `B02-21` (implemented).
**Completion scope:** `B02-21`.
**Evidence / source record:** `docs/delivery/EMERGENCE-REVIEW.md`, `eightball/v2/insights.py`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-09-24 · adopted · ChatGPT vision refinement: Treat information-gathering work as a first-class next move in the case brief. Keep quantitative value-of-information optimisation a candidate.

### [ ] EM-003: Freshness is separate from factual support

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

An older supported observation can warrant another review without becoming false.

**Product implication:** Ship opt-in observation-age prompts; retain event-time and true expiry semantics for further work.

**Roadmap links:** `ES02-04` (partial), `ES02-05` (verified), `B02-21` (implemented), `ES02-06` (partial).
**Completion scope:** `ES02-04`.
**Evidence / source record:** `docs/delivery/EMERGENCE-REVIEW.md`, `endstate/insights.py`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-09-24 · adopted · ChatGPT vision refinement: Strengthen the clock/support distinction in ENDSTATE vision. No autonomous freshness or monitoring service is added.

### [ ] EM-004: Watch conditions should drive reconsideration

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Useful plans include what would make the operator change course, not just the next step.

**Product implication:** Define versioned watch triggers, event authority and durable ordered updates before claiming real-time insight monitoring.

**Roadmap links:** `ES02-01` (partial), `ES02-02` (partial), `ES02-03` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/EMERGENCE-REVIEW.md`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · deferred · ChatGPT development proposal: Keep the event-driven roadmap intact. Manual scans are not a live event service.
- 2026-09-24 · adopted · ChatGPT vision refinement: Promote to explicit reconsideration-contract design priority under optional ES02-06; the event-service and original release gates stay open.

### [ ] EM-005: Operator attention is a scarce resource

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Many reviews and context switches can make a nominally quick route operationally poor.

**Product implication:** Measure real operator load before introducing scoring or optimisation.

**Roadmap links:** `B04-03` (not_started), `B04-04` (deferred).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/EMERGENCE-REVIEW.md`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · candidate · ChatGPT development proposal: Preserved for owner review. No automatic scope or completion claim.
- 2026-09-24 · candidate · ChatGPT vision refinement: Carry forward as a measurable operator-workload hypothesis, not a new uncalibrated route score.

### [ ] EM-006: Outcomes may need an acceptable envelope

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A client may have an ideal result, minimum acceptable resolution and walk-away conditions.

**Product implication:** Evaluate the existing multi-objective/failure model before adding an Outcome Envelope contract.

**Roadmap links:** `B02-03` (verified), `B03-07` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/EMERGENCE-REVIEW.md`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · candidate · ChatGPT development proposal: Preserved for owner review. No automatic scope or completion claim.
- 2026-09-24 · adopted · ChatGPT vision refinement: Promote an explicitly authorised mandate/fallback design to optional B03-07. Existing objective/failure semantics remain; do not silently relax client intent.

### [ ] EM-007: Patterns across apparently separate requirements

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Two nominal alternatives can share the same unresolved prerequisite.

**Product implication:** Detect shared signed prerequisites in the selected bounded candidate set.

**Roadmap links:** `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `endstate/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-008: Truly hidden dependencies need more than graph counts

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A link absent from the graph cannot be reliably discovered by counting declared links.

**Product implication:** Add future evidence-grounded dependency hypotheses; do not claim that the first detector discovers unknown causality.

**Roadmap links:** `ES03-02` (blocked), `B02-09` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/EMERGENT-INSIGHTS.md`.

**Decision history:**

- 2026-09-24 · deferred · ChatGPT development proposal: Preserved for owner review. No automatic scope or completion claim.

### [ ] EM-009: One question can affect several routes

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A single missing observation may change multiple candidate paths.

**Product implication:** Offer a human-reviewed question rather than pretending to compute a causal leverage score.

**Roadmap links:** `B02-05` (verified), `B02-21` (implemented).
**Completion scope:** `B02-21`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-010: A peripheral actor can become structurally important

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Multiple current actions may converge on the same recorded actor.

**Product implication:** Show involvement as an inferred lead and ask who actually holds authority.

**Roadmap links:** `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `endstate/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-011: Contradictory sources must remain visible

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Opposing active observations require deliberate reconciliation.

**Product implication:** Detect recorded conflicts now; evaluate natural-language contradiction discovery separately.

**Roadmap links:** `B02-01` (verified), `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `endstate/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-012: Weakening support deserves a review prompt

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Retraction or concentrated evidence dependencies can weaken a plan’s evidential basis.

**Product implication:** Show one-record support clusters and invalidate earlier insight reviews when referenced content changes.

**Roadmap links:** `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-013: Route fragility needs explicit assumptions

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Unknown waits and third-party decisions can dominate the apparent schedule.

**Product implication:** Expose unbounded waits and shared decisions now; defer calibrated fragility scores.

**Roadmap links:** `ES02-05` (verified), `B02-21` (implemented), `ES02-06` (partial).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `endstate/insights.py`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-09-24 · adopted · ChatGPT vision refinement: Make declared support/assumptions visible in the selected-course design, without promising robustness outside the examined catalogue.

### [ ] EM-014: New information can reveal additional options

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A different candidate set can appear after evidence or constraints change.

**Product implication:** Compare named scans and distinguish new candidate IDs from genuinely new strategies.

**Roadmap links:** `B02-05` (verified), `B02-21` (implemented).
**Completion scope:** `B02-21`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-015: Objective drift needs a separate check

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A case can start solving a different problem from the requested outcome.

**Product implication:** Flag target wording edits without changed criteria now; semantic drift detection remains an evaluated future capability.

**Roadmap links:** `B02-09` (blocked), `B02-21` (implemented).
**Completion scope:** `B02-21`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-016: High-value questions are not just blocked tasks

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A question can distinguish competing explanations rather than immediately unlock an action.

**Product implication:** Investigate information-value models with explicit uncertainty and expert labels instead of a made-up score.

**Roadmap links:** `B04-03` (not_started), `ES03-02` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/prompts/EMERGENT-INSIGHTS.md`.

**Decision history:**

- 2026-09-24 · candidate · ChatGPT development proposal: Preserved for owner review. No automatic scope or completion claim.

### [ ] EM-017: Second-order consequences can change the problem

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

An action can help one objective while creating another difficulty.

**Product implication:** Surface declared possible side effects as hypotheses now; causal consequence prediction requires separate evidence.

**Roadmap links:** `B02-03` (verified), `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `endstate/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-018: Outcome discovery must not rewrite the client’s intent

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

New evidence may justify an acceptable fallback or clarify what success really means.

**Product implication:** Ask for an explicit client/operator decision when failure criteria are supported. Never change the objective autonomously.

**Roadmap links:** `B02-21` (implemented), `ES02-05` (verified), `B03-07` (partial).
**Completion scope:** `B02-21`, `ES02-05`.
**Evidence / source record:** `endstate/insights.py`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-09-24 · adopted · ChatGPT vision refinement: Link outcome clarification to explicit client-mandate authority; no automatic fallback adoption.

### [ ] EM-019: Exact text and lineage are part of operational intelligence

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A source excerpt needs its original position and version, not just a summary.

**Product implication:** Preserve Source Desk linkage and include original-source review in future corroboration checks.

**Roadmap links:** `B02-14` (partial).
**Completion scope:** `B02-14`.
**Evidence / source record:** `docs/v2/SOURCE-DESK.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-10-16 · adopted · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · adopted · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Docling derivative coordinates and source mapping require separate original/derived lineage. No deferred runtime or acceptance promotion.

### [ ] EM-020: Compiler validation is not semantic correctness

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Valid references and exact quotations can accompany an interpretation that misses the outcome.

**Product implication:** Preserve the failing real-model gates and independent semantic evaluation.

**Roadmap links:** `B02-09` (blocked), `B02-11` (partial), `ES03-02` (blocked).
**Completion scope:** `B02-11`.
**Evidence / source record:** `docs/evidence/staged-compilation-verification.json`, `docs/delivery/sessions/2026-10-15-generation-role-contract.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`, `docs/research/github-2026-10-16/ruflo-owner-guide.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-10-15 · adopted · Codex sprint review: Historical Qwen replay revalidates the distinction between exact compiler checks, prompt provenance, semantic quality and assisted recovery. Prompt version now survives success and rejection; fresh inference and human judgement remain outstanding.
- 2026-10-16 · adopted · Codex research review: existing_task: component research preserves semantic/professional evaluation, source/case boundaries, shared scenario baselines, exact evidence and measured operator value. Research proposal changes no acceptance requirement.
- 2026-10-16 · adopted · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · adopted · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · adopted · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.
- 2026-10-16 · adopted · Codex Ruflo owner source review: existing_task/candidate refinement: preserve separate model-access, bookkeeping, API-success, worker-routing and business-outcome targets; record synthetic/live benchmark scope and historical audit remediations. Optional coordinator remains unadopted.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Jev labels, worker consensus, model critiques and causal estimators each need task-specific independent correctness evidence. No deferred runtime or acceptance promotion.

### [ ] EM-021: Review state and evidence character must be separate

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A human can find an inference useful without establishing it as true.

**Product implication:** Use derived/inferred/hypothesis independently of review dispositions. Do not offer a misleading confirmed toggle.

**Roadmap links:** `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-022: A dismissal is not deletion or permanent suppression

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

An initially unhelpful finding can become relevant when the case changes.

**Product implication:** Retain dismissal reasons and reopen review when content changes or a finding recurs.

**Roadmap links:** `B02-21` (implemented).
**Completion scope:** `B02-21`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [x] EM-023: The owner must see ideas the builder did not select

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A development judgement can miss commercial or operational value visible to the owner.

**Product implication:** Keep all discoveries in an evolving register, including deferred/declined suggestions and decision history.

**Roadmap links:** `DOC-06` (verified).
**Completion scope:** `DOC-06`.
**Evidence / source record:** `scripts/emergence.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-024: A graph can falsely imply causation or control

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Position, line density and repeated mentions can look more authoritative than they are.

**Product implication:** Keep visual exploration read-only and state what every relationship actually represents.

**Roadmap links:** `B02-20` (implemented), `B02-21` (implemented).
**Completion scope:** `B02-20`, `B02-21`.
**Evidence / source record:** `docs/v2/GRAPH-EXPLORER.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-025: Bounded search makes universal claims unsafe

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Several calculated routes can overlap and are not all the routes reality permits.

**Product implication:** Label the candidate pool, truncation and caps. Avoid “every viable route” and unsupported success percentages.

**Roadmap links:** `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `endstate/insights.py`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Bounded planning and solver/optimiser/sensitivity statuses must retain coverage, infeasibility, unknown/nonfinite and reproducibility semantics. No deferred runtime or acceptance promotion.

### [ ] EM-026: No finding is also a result

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Forcing a model to produce insights encourages invented patterns.

**Product implication:** Permit an empty scan/proposal and show disabled or capped rules rather than imply exhaustive understanding.

**Roadmap links:** `B02-21` (implemented), `ES02-05` (verified).
**Completion scope:** `B02-21`, `ES02-05`.
**Evidence / source record:** `endstate/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-027: Cross-client learning is a separate permission boundary

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Reusable technology does not make confidential client histories reusable by default.

**Product implication:** Keep all case findings scoped; require an explicit governance and permission decision for precedent learning.

**Roadmap links:** `B04-02` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/PRODUCTION-SECURITY.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · deferred · ChatGPT development proposal: Preserved for owner review. No automatic scope or completion claim.
- 2026-10-16 · deferred · Codex research review: existing_task: component research preserves semantic/professional evaluation, source/case boundaries, shared scenario baselines, exact evidence and measured operator value. Research proposal changes no acceptance requirement.
- 2026-10-16 · deferred · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · deferred · Codex whole-system investigation: existing_task/candidate refinement: Optional memory namespaces, telemetry and permission caches need explicit trusted access/data-exit policies; no shared-case learning is authorised. No deferred runtime or acceptance promotion.

### [ ] EM-028: An insight and its supporting observation have different clocks

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A current scan can inspect an old observation; an old scan can be outdated after a fresh case edit.

**Product implication:** Separate as-of time, observation-age policy, case revision and review-context expiry.

**Roadmap links:** `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`, `B02-21`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-029: ~~Automatic promotion of insights would corrupt the authority boundary~~

**Disposition:** declined. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Calling a pattern confirmed or acting on it could silently turn inference into fact.

**Product implication:** Do not ship automatic attestation, approval, objective rewriting or external action from insights.

**Roadmap links:** `B02-06` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/prompts/EMERGENT-INSIGHTS.md`.

**Decision history:**

- 2026-09-24 · declined · ChatGPT development proposal: Declined implementation approach, retained for owner review. It conflicts with the established evidence and authority boundary.

### [ ] EM-030: Recurring scans can create noise instead of intelligence

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Duplicate or low-impact signals could consume the attention they were meant to save.

**Product implication:** Use stable identities and recurrence-aware review, then evaluate noise and missed findings with operators.

**Roadmap links:** `B02-21` (implemented), `B02-22` (not_started).
**Completion scope:** `B02-22`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-031: Provider cancellation cannot recall a request already sent

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

A cancelled UI request can still complete or incur provider charges.

**Product implication:** Preserve current job cancellation/publication boundaries and honest progress language.

**Roadmap links:** `B02-15` (partial).
**Completion scope:** `B02-15`.
**Evidence / source record:** `docs/v2/ANALYSIS-JOBS.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-10-16 · adopted · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · adopted · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Local admission is before HTTP, cancellation cannot recall provider compute; cleanup must stop the owned process even if client.close fails. No deferred runtime or acceptance promotion.

### [x] EM-032: Local source and remote repository can diverge

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Several valid local checkpoints are not present on the integration branch after a blocked source write.

**Product implication:** Ship reproducible cumulative patches, explicit handoffs and separate native/bridge claims; do not imply a clone contains unpublished work.

**Roadmap links:** `DOC-03` (verified), `DOC-04` (verified), `ES03-08` (blocked).
**Completion scope:** `DOC-03`, `DOC-04`.
**Evidence / source record:** `docs/delivery/HANDOFF.md`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-09-24 · adopted · ChatGPT vision refinement: Extend the recovery check: missing later source is reported-only, distinct from a verified earlier archive. See EM-062.

### [ ] EM-033: User-supplied hypotheses complement automatic detection

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

The fixer may notice a meaningful connection that no current rule detects.

**Product implication:** Keep a manually authored, record-linked hypothesis in the same case review history without promoting its truth.

**Roadmap links:** `B02-21` (implemented).
**Completion scope:** `B02-21`.
**Evidence / source record:** `eightball/v2/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-034: Evidence record counts do not establish source independence

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Several excerpts or copies may trace back to one original source.

**Product implication:** Explicitly qualify source-cluster detection; a future corroboration model must follow original-source lineage.

**Roadmap links:** `B02-14` (partial), `B02-21` (implemented).
**Completion scope:** `B02-14`.
**Evidence / source record:** `docs/v2/SOURCE-DESK.md`, `endstate/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-035: Async case switching can expose the wrong context

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

An old response must not populate the newly selected client’s insight panel.

**Product implication:** Guard responses by case ID and session epoch, clear state on switching/locking, and test it.

**Roadmap links:** `B02-21` (implemented).
**Completion scope:** `B02-21`.
**Evidence / source record:** `web/v2/insights-view.js`, `tests/test_insight_ui.py`, `docs/delivery/sessions/2026-10-15-provider-failure-evidence.md`, `docs/evidence/provider-failure-native-failed-2026-10-15.json`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.
- 2026-10-15 · adopted · Codex native acceptance follow-up: Cumulative native failure exposes same-case refresh overwriting a later explicit navigation. Preserve original failure and order presentation requests without changing case facts or authority; deterministic native regression required.

### [x] EM-036: Already-satisfied OR outcomes must not create artificial blockers

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Emergent Insights regression test during this sprint.

The preserved planner can list alternative branches after an OR objective is already evidenced. Treating every listed alternative as still required creates false deadline pressure.

**Product implication:** Suppress active-route-based emergence claims once mandatory outcomes are evidenced, while retaining true conflicts and review history. Preserve the planner compatibility contract.

**Roadmap links:** `ES02-05` (verified), `B02-21` (implemented).
**Completion scope:** `ES02-05`.
**Evidence / source record:** `tests/test_insight_engine.py`, `endstate/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development finding: A failing independent OR-goal fixture exposed a false-positive warning. Correct the detector boundary rather than relabel the test or alter the preserved planner.

### [x] EM-037: Governance upgrades must not rewrite pre-policy history

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-24. **Origin:** Cumulative integration inspection in Emergent Insights sprint.

Comparing the cumulative local build with its old remote base treated historical changelog entries as new and required fields that did not exist when those entries were written.

**Product implication:** Apply stricter rules to future entries while pinning exact historical exceptions. Preserve old wording and refuse blanket date-based exemptions.

**Roadmap links:** `DOC-04` (verified), `DOC-06` (verified).
**Completion scope:** `DOC-06`.
**Evidence / source record:** `scripts/changelog.py`, `tests/test_changelog.py`, `docs/delivery/CHANGELOG-POLICY.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Five exact content-bound historical exceptions preserve original records; future entries still require review and registry links. Cumulative integration tests make the boundary explicit.

### [ ] EM-038: Identity belongs to a source mention, not a shared name

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-24. **Origin:** Source clarity sprint and its explicit limitations.

A same-name fixture has two distinct actors. Selecting one source mention can establish a reviewer link without merging either actor or assigning authority.

**Product implication:** Keep source-scoped identity judgements, negative identifications and rationale. Leave global alias merging to a separately reviewed mechanism.

**Roadmap links:** `B02-10` (partial).
**Completion scope:** `B02-10`.
**Evidence / source record:** `docs/v2/SOURCE-CLARITY.md`, `tests/test_grounding.py`, `docs/delivery/sessions/2026-09-24-source-clarity-local.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Implement the bounded operator review within existing source-handling tasks; broad model/native acceptance stays open.

### [ ] EM-039: Interpreting a date and adopting a deadline are separate acts

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-24. **Origin:** Source clarity sprint and its explicit limitations.

A correctly converted date still does not establish that it should constrain the whole case rather than one report, decision or question.

**Product implication:** Preview the intended target and schedule impact, then explicitly commit one field with source and reviewer provenance.

**Roadmap links:** `B02-10` (partial).
**Completion scope:** `B02-10`.
**Evidence / source record:** `docs/v2/SOURCE-CLARITY.md`, `tests/test_grounding.py`, `docs/delivery/sessions/2026-09-24-source-clarity-local.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Implement the bounded operator review within existing source-handling tasks; broad model/native acceptance stays open.

### [ ] EM-040: A wall-clock time can mean zero, one or two instants

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-24. **Origin:** Source clarity sprint and its explicit limitations.

Timezone round-trip tests produce no real instant in a spring clock gap and two in an autumn fold. Source-relative dates also require a reference date independent of import time.

**Product implication:** Demand explicit timezone/reference input, block nonexistent times and require a choice for repeated ones; preserve local and UTC forms.

**Roadmap links:** `B02-10` (partial).
**Completion scope:** `B02-10`.
**Evidence / source record:** `docs/v2/SOURCE-CLARITY.md`, `tests/test_time_review.py`, `docs/delivery/sessions/2026-09-24-source-clarity-local.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Implement the bounded operator review within existing source-handling tasks; broad model/native acceptance stays open.

### [ ] EM-041: Retracting a source does not necessarily cancel an adopted constraint

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-24. **Origin:** Source clarity sprint and its explicit limitations.

An operator-adopted deadline can remain important after its source is withdrawn. Automatically erasing it would silently change operational commitments.

**Product implication:** Flag the interpretation for reconsideration, preserve the existing deadline and require an explicit later amendment.

**Roadmap links:** `B02-10` (partial).
**Completion scope:** `B02-10`.
**Evidence / source record:** `docs/v2/SOURCE-CLARITY.md`, `tests/test_grounding.py`, `docs/delivery/sessions/2026-09-24-source-clarity-local.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Implement the bounded operator review within existing source-handling tasks; broad model/native acceptance stays open.

### [ ] EM-042: Exact quotation alone can still hide necessary context

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Source clarity sprint and its explicit limitations.

The selected name or date phrase omits nearby attribution, qualifications and negation. Exact offsets prove location, not a correct interpretation.

**Product implication:** Keep surrounding source wording visible beside the exact selection and retain a route back to the original.

**Roadmap links:** `B02-14` (partial).
**Completion scope:** `B02-14`.
**Evidence / source record:** `docs/v2/SOURCE-CLARITY.md`, `tests/test_grounding.py`, `docs/delivery/sessions/2026-09-24-source-clarity-local.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Implement the bounded operator review within existing source-handling tasks; broad model/native acceptance stays open.

### [ ] EM-043: Business days and end-of-day need explicit operational calendars

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Source clarity sprint and its explicit limitations.

The bounded calendar-day interpreter deliberately cannot decide what next business day or end of day means for every organisation, location or agreement.

**Product implication:** Consider versioned calendars and explicit working-hour policies, but do not invent them or silently expand the current date-review scope.

**Roadmap links:** `B02-10` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/SOURCE-CLARITY.md`, `tests/test_grounding.py`, `docs/delivery/sessions/2026-09-24-source-clarity-local.md`.

**Decision history:**

- 2026-09-24 · deferred · ChatGPT build review: Retain for owner review. Jurisdiction and organisation calendars need explicit policy and independent tests before implementation.

### [x] EM-044: Route identity must distinguish dependency order

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Plan Review sprint and reproducible structural fixtures.

Two returned routes used the same actions but different producer ordering and constraint results, yet shared an ID. A dictionary-based comparison could silently replace one.

**Product implication:** Disambiguate colliding routes by their declared dependency path while preserving non-colliding legacy IDs.

**Roadmap links:** `B02-03` (verified).
**Completion scope:** `B02-03`.
**Evidence / source record:** `docs/v2/PLAN-REVIEW.md`, `tests/test_plan_review.py`, `docs/evidence/route-identity-regression.json`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: An executable regression reproduced the old collision and confirms unique, stable IDs after the fix.

### [ ] EM-045: A structurally clean graph may target the wrong outcome

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Plan Review sprint and reproducible structural fixtures.

A deliberately valid fixture targets sending an offer although the desired outcome requires customer acceptance. Graph validation alone raises no structural flag.

**Product implication:** Require explicit human comparison of the requested target and actual success criteria; never claim semantic correctness from a clean structure.

**Roadmap links:** `B02-11` (partial), `B02-09` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/PLAN-REVIEW.md`, `tests/test_plan_review.py`, `docs/evidence/route-identity-regression.json`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Plan Review exposes target criteria beside the requested outcome; independent quality evaluation remains open.
- 2026-09-24 · adopted · ChatGPT vision refinement: Retain the semantic-target gate in both vision documents. A valid graph is not evidence the client intent was preserved.

### [ ] EM-046: Plan judgement is not factual truth or permission to act

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Plan Review sprint and reproducible structural fixtures.

A reviewer can mark all rubric dimensions supported while the plan still contains unresolved waits and external dependencies. That judgement must not erase the warnings or approve work.

**Product implication:** Store case-scoped reviews separately and bind them to exact context; evidence and execution approval remain their own processes.

**Roadmap links:** `B02-11` (partial), `B02-13` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/PLAN-REVIEW.md`, `tests/test_plan_review.py`, `docs/evidence/route-identity-regression.json`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/ruflo.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: The separate journal and tests preserve all case facts, revisions and approvals.
- 2026-10-16 · adopted · Codex research review: existing_task: component research preserves semantic/professional evaluation, source/case boundaries, shared scenario baselines, exact evidence and measured operator value. Research proposal changes no acceptance requirement.
- 2026-10-16 · adopted · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · adopted · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.

### [ ] EM-047: Independent scenario comparisons must share one baseline

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Plan Review sprint and reproducible structural fixtures.

A zero-budget scenario followed by a restored-budget scenario must not retain disabled actions or assumptions from the preceding experiment.

**Product implication:** Copy the same input for each explicit scenario and label independent versus combined experiments.

**Roadmap links:** `B02-05` (verified), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/PLAN-REVIEW.md`, `tests/test_plan_review.py`, `docs/evidence/route-identity-regression.json`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Read-only copies and regression tests prevent accumulating hypothetical changes.
- 2026-10-16 · adopted · Codex research review: existing_task: component research preserves semantic/professional evaluation, source/case boundaries, shared scenario baselines, exact evidence and measured operator value. Research proposal changes no acceptance requirement.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Later simulator comparisons require one immutable case/target baseline, assumptions and independent operator-value measures. No deferred runtime or acceptance promotion.

### [ ] EM-048: Review detail can become an operator burden

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Plan Review sprint and reproducible structural fixtures.

Six explicit rubric judgements add accountability but can also create repetitive work across frequent revisions.

**Product implication:** Measure review burden and determine which changes merit renewed attention before adding automated approval shortcuts.

**Roadmap links:** `B02-22` (not_started), `B04-04` (deferred).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/PLAN-REVIEW.md`, `tests/test_plan_review.py`, `docs/evidence/route-identity-regression.json`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · deferred · ChatGPT build review: Retained for owner review. No evidence yet supports removing criteria or silently carrying judgements to changed cases.
- 2026-09-24 · candidate · ChatGPT vision refinement: Prioritise decision usefulness and progressive disclosure; keep the existing critical review gates intact pending evidence.

### [ ] EM-049: An apparent failure can have a legitimate later recovery path

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Plan Review sprint and reproducible structural fixtures.

A destructive-effect fixture also allowed a different later action to restore a required condition. Declaring every such sequence impossible would have been an incorrect expected result.

**Product implication:** Test final state and declared order, not a simplistic rule that every negative effect invalidates a route. Preserve the distinction between recovery possibilities and guarantees.

**Roadmap links:** `B02-03` (verified), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/PLAN-REVIEW.md`, `tests/test_plan_review.py`, `docs/evidence/route-identity-regression.json`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: The regression retains both the valid recovery ordering and failing ordering; the constrained fixture states its budget restriction explicitly.

### [ ] EM-050: Nested output contracts need structural validation too

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Integration and acceptance sprint.

PlanResponse previously guaranteed its outer envelope but not the complete nested result structure.

**Product implication:** Validate route, clock, schedule, condition and briefing references without changing old wire records.

**Roadmap links:** `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `endstate/results.py`, `tests/test_endstate_results.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.

### [ ] EM-051: Verification belongs to exact source and evidence bytes

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Integration and acceptance sprint.

Separate successful test reports could be retained while the working source continued changing.

**Product implication:** Record per-run source and artifact manifests and reject stale or mixed-mode evidence.

**Roadmap links:** `B02-12` (blocked), `B02-16` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `scripts/acceptance.py`, `tests/test_acceptance_runner.py`, `docs/delivery/sessions/2026-10-15-generation-role-contract.md`, `docs/evidence/generation-role-contract-2026-10-15.json`, `docs/delivery/sessions/2026-10-15-provider-failure-evidence.md`, `docs/delivery/sessions/2026-10-15-main-consolidation.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`, `docs/research/github-2026-10-16/whole-system-review.md`, `docs/delivery/sessions/2026-10-18-review-evidence.md`, `docs/delivery/sessions/2026-10-18-anthropic-configuration.md`, `docs/delivery/sessions/2026-10-25-build-consolidation.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.
- 2026-10-15 · adopted · Codex sprint review: Historical Qwen replay revalidates the distinction between exact compiler checks, prompt provenance, semantic quality and assisted recovery. Prompt version now survives success and rejection; fresh inference and human judgement remain outstanding.
- 2026-10-15 · adopted · Codex provider evidence sprint: Retain bounded rejected-extraction output through async jobs and disposable journey evidence. Concrete unperformed review records preserve the distinction between scripted integration, owner end review and independent professional evaluation; no gate is promoted.
- 2026-10-15 · adopted · Codex integration review: Unify latest source and separate documentation without replacing newer runtime/acceptance evidence. Preserve both archive variants and histories; owner authorizes this main integration, not release/model/human acceptance.
- 2026-10-16 · adopted · Codex research review: existing_task: component research preserves semantic/professional evaluation, source/case boundaries, shared scenario baselines, exact evidence and measured operator value. Research proposal changes no acceptance requirement.
- 2026-10-16 · adopted · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · adopted · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Unique model-run checkpoints and exact assistant text improve source/evidence recovery; partial and hard-kill gaps remain explicit. No deferred runtime or acceptance promotion.
- 2026-10-18 · adopted · Codex sprint review: existing_task refinement: recovered newer pushed source from an older restored checkout; preserve source-bound run evidence and additive optional recording compatibility. Saved setup is not an active published environment. No acceptance promotion.
- 2026-10-18 · adopted · Codex Anthropic preparation: existing_task refinement: SDK-listed model identity, compatibility request formatting, allowed secret destination, active authentication and actual model quality remain separate. Official compatibility docs read was403; prepared configuration is not an inference result.
- 2026-10-25 · adopted · Codex integration review: existing_task: preserve source and uncertain auth evidence, resolve already-integrated PR ancestry, prepare exact next-agent tests. A generic save rejection did not establish the earlier claimed field-specific cause. No acceptance promotion.

### [ ] EM-052: A built distribution is not an installed-product test

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Integration and acceptance sprint.

The kernel could pass inside the application checkout without proving that the actual wheel contained and loaded the right files.

**Product implication:** Test the installed artifact outside the repository and rerun the original application suite against that kernel.

**Roadmap links:** `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `scripts/build_endstate.py`, `docs/endstate/PACKAGE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.

### [ ] EM-053: Operator orientation must survive replacement dialogs

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Integration and acceptance sprint.

Navigation and replaced dialogs could leave keyboard focus on the body or on a removed control.

**Product implication:** Preserve the root invoker, focus the visible dialog title and focus destination headings without changing authority.

**Roadmap links:** `B02-16` (partial), `B02-20` (implemented).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `web/v2/ui.js`, `tests/browser_accessibility.py`, `docs/delivery/sessions/2026-10-15-graph-keyboard-focus.md`, `docs/evidence/graph-keyboard-baseline-2026-10-15.json`, `docs/evidence/graph-keyboard-native-2026-10-15.json`, `docs/delivery/sessions/2026-10-15-provider-failure-evidence.md`, `docs/evidence/provider-failure-native-failed-2026-10-15.json`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.
- 2026-10-15 · adopted · Codex continuation review: existing_task B02-16/B02-20: graph redraw replaces inspector/filter controls just as dialog replacement can lose the invoker. Preserve logical control identity and an explicit destination when a control disappears. Record native reproduction and corrected behavior; automated focus does not replace human acceptance.
- 2026-10-15 · adopted · Codex native acceptance follow-up: Cumulative native failure exposes same-case refresh overwriting a later explicit navigation. Preserve original failure and order presentation requests without changing case facts or authority; deterministic native regression required.

### [ ] EM-054: Scripted real-model review is not independent judgement

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Integration and acceptance sprint.

An actual-inference integration script can exercise approvals and evidence mechanics while still using developer-authored reviewer choices.

**Product implication:** Label these choices and synthetic observations explicitly; do not use them to close independent quality or all-native human acceptance.

**Roadmap links:** `B02-11` (partial), `B02-12` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `evals/full_journey.py`, `docs/v2/ACCEPTANCE-RUNNER.md`, `docs/delivery/sessions/2026-10-15-provider-failure-evidence.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.
- 2026-10-15 · adopted · Codex provider evidence sprint: Retain bounded rejected-extraction output through async jobs and disposable journey evidence. Concrete unperformed review records preserve the distinction between scripted integration, owner end review and independent professional evaluation; no gate is promoted.
- 2026-10-16 · adopted · Codex research review: existing_task: component research preserves semantic/professional evaluation, source/case boundaries, shared scenario baselines, exact evidence and measured operator value. Research proposal changes no acceptance requirement.
- 2026-10-16 · adopted · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · adopted · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Prepared prospective templates, model judges and engineering agents cannot replace qualified independent or genuine human review. No deferred runtime or acceptance promotion.

### [ ] EM-055: Available, called, correct, integrated and released are separate gates

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Integration and acceptance sprint.

A configured provider can be unreachable; a valid model response can be semantically wrong; a passing local build can be unpushed and undeployed.

**Product implication:** Keep availability, invocation, model quality, browser transport and release status separate, including failures and zero-call preflights.

**Roadmap links:** `B02-12` (blocked), `B02-15` (partial), `B02-18` (blocked), `ES03-08` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `scripts/acceptance.py`, `evals/full_journey.py`, `docs/delivery/sessions/2026-09-24-integration-acceptance-local.md`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`, `docs/delivery/sessions/2026-10-15-generation-role-contract.md`, `docs/delivery/sessions/2026-10-15-provider-failure-evidence.md`, `docs/delivery/sessions/2026-10-15-main-consolidation.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`, `docs/research/github-2026-10-16/ruflo-owner-guide.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.
- 2026-09-24 · adopted · ChatGPT vision refinement: A narrated test total without its recoverable implementation is not current-source evidence. Preserve the missing-source caveat as well as native/model/publication states.
- 2026-10-15 · adopted · Codex sprint review: Historical Qwen replay revalidates the distinction between exact compiler checks, prompt provenance, semantic quality and assisted recovery. Prompt version now survives success and rejection; fresh inference and human judgement remain outstanding.
- 2026-10-15 · adopted · Codex provider evidence sprint: Retain bounded rejected-extraction output through async jobs and disposable journey evidence. Concrete unperformed review records preserve the distinction between scripted integration, owner end review and independent professional evaluation; no gate is promoted.
- 2026-10-15 · adopted · Codex integration review: Unify latest source and separate documentation without replacing newer runtime/acceptance evidence. Preserve both archive variants and histories; owner authorizes this main integration, not release/model/human acceptance.
- 2026-10-16 · adopted · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · adopted · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · adopted · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.
- 2026-10-16 · adopted · Codex Ruflo owner source review: existing_task/candidate refinement: preserve separate model-access, bookkeeping, API-success, worker-routing and business-outcome targets; record synthetic/live benchmark scope and historical audit remediations. Optional coordinator remains unadopted.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: OASIS driver completion, Phoenix dry-run, provider admission and absent cancelled proposals have distinct evidence meanings. No deferred runtime or acceptance promotion.

### [ ] EM-056: A candidate route is not a human-selected course

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

The recovered alpha.7 contracts represent candidate routes and individual decisions, but do not define a dedicated course-selection record tying an operator choice to a route, target and snapshot.

**Product implication:** Design a versioned selected-course record in 8BALL with a neutral ENDSTATE reference. Selection does not attest truth or authorise an action.

**Roadmap links:** `B03-07` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `endstate/contracts.py`, `endstate/results.py`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT documentation review: Adopt the bounded design direction, not runtime completion. Owner review and the listed acceptance work remain open.
- 2026-09-25 · adopted · ChatGPT local build: Local selected-course foundation implemented and focused-tested. Full mandate, secure team authority and continuous event handling remain outside this checkpoint.

### [ ] EM-057: Recalculation must not silently recommit the operator

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

Once a team has chosen a course, repeated ranking changes could confuse action and accountability if the interface treats the newest first route as the plan being followed.

**Product implication:** Separate refreshed alternatives from the chosen course. Present change reasons and request an explicit switch; preserve conservative approval invalidation.

**Roadmap links:** `ES02-06` (partial), `B03-07` (partial), `ES02-04` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`, `docs/vision/ACCEPTANCE-DESIGN.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT documentation review: Adopt the bounded design direction, not runtime completion. Owner review and the listed acceptance work remain open.
- 2026-09-25 · adopted · ChatGPT local build: Local selected-course foundation implemented and focused-tested. Full mandate, secure team authority and continuous event handling remain outside this checkpoint.

### [ ] EM-058: Negative conclusions need an explicit coverage boundary

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

The recovered source separates full originals, selected excerpts and bounded route search. A result about the processed subset cannot establish completeness of the whole situation.

**Product implication:** Expose supplied/selected/omitted inputs and catalogue/search limits alongside empty findings or no-route results. Do not collapse scope into a single confidence score.

**Roadmap links:** `B02-10` (partial), `B02-14` (partial), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `eightball/v2/source_desk.py`, `endstate/planner.py`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT documentation review: Adopt the bounded design direction, not runtime completion. Owner review and the listed acceptance work remain open.

### [ ] EM-059: Operational commitments may outlive the source that described them

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

Source Clarity already separates an adopted deadline from source retraction. The same distinction may be needed for promises, authorised concessions and other commitments made while handling a case.

**Product implication:** Evaluate an explicit commitments record with its own withdrawal authority and history; do not cancel commitments solely because source support changes.

**Roadmap links:** `B03-07` (partial), `B02-10` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/SOURCE-CLARITY.md`, `docs/vision/8BALL.md`.

**Decision history:**

- 2026-09-24 · candidate · ChatGPT documentation review: Retained for owner review; no new mandatory scope or implementation claim.

### [ ] EM-060: Recovering a plan is different from proving a model reliable

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

The supplied Draft Repair handoff reports a human-correction workflow but not a recovered implementation. If restored, a successful human repair would demonstrate recoverability rather than unassisted model quality.

**Product implication:** Recover and test the implementation, retain original failures and edits, and classify assisted success separately in evaluation. Do not change the frozen generation gate.

**Roadmap links:** `ES03-08` (blocked), `ES03-05` (partial), `B02-09` (blocked), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/reference/2026-09-24-draft-repair-delivery-record.md`, `docs/vision/ENDSTATE.md`, `docs/vision/ACCEPTANCE-DESIGN.md`, `docs/delivery/sessions/2026-10-15-generation-role-contract.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT documentation review: Adopt the bounded design direction, not runtime completion. Owner review and the listed acceptance work remain open.
- 2026-10-15 · adopted · Codex sprint review: Historical Qwen replay revalidates the distinction between exact compiler checks, prompt provenance, semantic quality and assisted recovery. Prompt version now survives success and rejection; fresh inference and human judgement remain outstanding.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: MiroFish retries/JSON repair remain assisted recovery, separate from original unassisted frozen generation results. No deferred runtime or acceptance promotion.

### [ ] EM-061: The primary value test is a better decision, not a larger graph

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

The cumulative workspace has more inspection and review surfaces. It is not yet independently established whether that makes a fixer faster, more accurate or simply busier.

**Product implication:** Measure correct next decisions, missed dependencies, false alarms and correction/review burden. Prefer progressive disclosure in the existing room over more dashboards.

**Roadmap links:** `B04-03` (not_started), `B02-22` (not_started), `B04-04` (deferred).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/vision/8BALL.md`, `evals/PLAN-QUALITY-GATE.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT documentation review: Adopt the bounded design direction, not runtime completion. Owner review and the listed acceptance work remain open.
- 2026-10-16 · adopted · Codex research review: existing_task: component research preserves semantic/professional evaluation, source/case boundaries, shared scenario baselines, exact evidence and measured operator value. Research proposal changes no acceptance requirement.
- 2026-10-16 · adopted · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · adopted · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Adopt one specialist only after independent quality/correction-effort and total operating-cost benefit over the native baseline. No deferred runtime or acceptance promotion.

### [ ] EM-062: A delivery claim requires a recoverable implementation

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

The latest supplied repair handoff states that its working tree was not recovered, while the alpha.7 ZIP can be reconstructed to its declared exact Git tree. Later reported test totals cannot be attached to that earlier source.

**Product implication:** Preserve a source inventory and mark later work reported-only until recovered or explicitly rebuilt. A handoff, screenshot or test-count statement is not a runnable package.

**Roadmap links:** `DOC-03` (verified), `DOC-04` (verified), `ES03-08` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/reference/2026-09-24-draft-repair-delivery-record.md`, `docs/delivery/sessions/2026-09-24-vision-strengthening.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT documentation review: Adopt the bounded design direction, not runtime completion. Owner review and the listed acceptance work remain open.

### [ ] EM-063: Human corrections can reveal failure classes without permitting training

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

A preserved correction could reveal a missing dependency, changed meaning or excessive review cost, but using that record for model training or another client is a separate decision.

**Product implication:** Explore permissioned, case-scoped correction replay for evaluation. Keep retention, confidentiality and dataset approval explicit; never silently train on client work.

**Roadmap links:** `B04-04` (deferred), `B04-02` (not_started), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/vision/ENDSTATE.md`, `docs/vision/8BALL.md`, `docs/research/github-2026-10-16/tencent-memory.md`.

**Decision history:**

- 2026-09-24 · candidate · ChatGPT documentation review: Retained for owner review; no new mandatory scope or implementation claim.
- 2026-10-16 · candidate · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.

### [ ] EM-064: Some outcomes need evidence over a declared confirmation window

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

A single successful check can satisfy a present-state condition without establishing a requested period of sustained recovery. Not every outcome requires such a period.

**Product implication:** Explore explicit outcome confirmation windows with the operator and preserve unknown timing. Do not add hidden universal stability periods or autonomous monitoring.

**Roadmap links:** `B03-07` (partial), `ES02-04` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`, `docs/vision/ACCEPTANCE-DESIGN.md`.

**Decision history:**

- 2026-09-24 · candidate · ChatGPT documentation review: Retained for owner review; no new mandatory scope or implementation claim.

### [ ] EM-065: An evolving review protocol needs additive compatibility

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-24. **Origin:** Vision review regression run.

The initial full regression rejected five added review prompts because a test required exactly ten. The protocol must permit new passes without silently dropping, rewording or reordering the existing ones.

**Product implication:** Keep stable question IDs and append-only protocol history. Test both valid extensions and attempted loss of original review questions; do not weaken runtime safeguards to satisfy document tests.

**Roadmap links:** `DOC-05` (verified), `DOC-06` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `scripts/emergence.py`, `tests/test_emergence_register.py`, `docs/delivery/sessions/2026-09-24-vision-strengthening.md`, `docs/delivery/sessions/2026-10-18-review-evidence.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT regression review: Bounded documentation-tooling fix. Original ten passes remain mandatory and previously recorded protocol entries become append-only. No runtime or model-quality acceptance follows.
- 2026-10-18 · adopted · Codex sprint review: existing_task refinement: recovered newer pushed source from an older restored checkout; preserve source-bound run evidence and additive optional recording compatibility. Saved setup is not an active published environment. No acceptance promotion.

### [ ] EM-066: A chosen course must preserve its exact prerequisite branch

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-25. **Origin:** Chosen Course recovery and local implementation.

Recalculating only by the same action set can admit another OR branch or ordering. This implementation pins selected prerequisites and checks recorded order.

**Product implication:** Retain a reproducible anchor and label remaining candidates as conditional, not an automatic new course.

**Roadmap links:** `B03-07` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-09-25-chosen-course-recovery.md`, `tests/test_courses.py`.

**Decision history:**

- 2026-09-25 · adopted · ChatGPT build review: Adopt in the bounded local implementation and reproducible delivery; wider secure/native/operator acceptance remains unverified.

### [ ] EM-067: A review clock can change the judgement without changing case revision

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-25. **Origin:** Chosen Course recovery and local implementation.

A selected review time or deadline can be reached with no new source or state revision. Version-only checks would miss that reason to reconsider.

**Product implication:** Bind assessments to explicit clocks as well as snapshots; on-request review is not continuous monitoring.

**Roadmap links:** `B03-07` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-09-25-chosen-course-recovery.md`, `tests/test_courses.py`.

**Decision history:**

- 2026-09-25 · adopted · ChatGPT build review: Adopt in the bounded local implementation and reproducible delivery; wider secure/native/operator acceptance remains unverified.

### [ ] EM-068: Pausing the course record is not cancellation of work

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-25. **Origin:** Chosen Course recovery and local implementation.

Course lifecycle and action approval histories are separate. A local pause has no channel to cancel external activity or revoke separate approvals.

**Product implication:** State the exact effect of pause/resume/retirement and preserve action-authority boundaries.

**Roadmap links:** `B03-07` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-09-25-chosen-course-recovery.md`, `tests/test_courses.py`.

**Decision history:**

- 2026-09-25 · adopted · ChatGPT build review: Adopt in the bounded local implementation and reproducible delivery; wider secure/native/operator acceptance remains unverified.

### [ ] EM-069: Acknowledging a warning must not clear its factual cause

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-25. **Origin:** Chosen Course recovery and local implementation.

A human review record can be appended while a hard constraint or explicit watch is still triggered. Treating review as clearance would hide an unresolved issue.

**Product implication:** Show reviewed history and current diagnostics separately; require actual case changes or a new explicit course to change the basis.

**Roadmap links:** `B03-07` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-09-25-chosen-course-recovery.md`, `tests/test_courses.py`.

**Decision history:**

- 2026-09-25 · adopted · ChatGPT build review: Adopt in the bounded local implementation and reproducible delivery; wider secure/native/operator acceptance remains unverified.

### [ ] EM-070: Unavailable work and a verification-only remainder can coexist

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-09-25. **Origin:** Chosen Course recovery and local implementation.

Disabling a selected action may leave a candidate that asks for evidence of its intended result. That candidate is not proof the original work can proceed.

**Product implication:** Surface unavailable selected actions separately from evidence gaps and avoid global impossibility or unconditional viability claims.

**Roadmap links:** `B03-07` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-09-25-chosen-course-recovery.md`, `tests/test_courses.py`.

**Decision history:**

- 2026-09-25 · adopted · ChatGPT build review: Adopt in the bounded local implementation and reproducible delivery; wider secure/native/operator acceptance remains unverified.

### [ ] EM-071: An interrupted sprint needs reproducible source, not inherited result totals

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-25. **Origin:** Chosen Course recovery and local implementation.

The mounted alpha.7 archive and PRD overlay reproduced exactly; the interrupted Chosen Course narrative had no delivered implementation tree. New code and test results were rebuilt from the verified bytes.

**Product implication:** Checkpoint actual source and include a Git bundle, cumulative patch and byte-level manifest so the next environment can reproduce the work.

**Roadmap links:** `DOC-03` (verified), `DOC-04` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-09-25-chosen-course-recovery.md`, `docs/delivery/sessions/2026-10-18-review-evidence.md`, `docs/delivery/sessions/2026-10-25-build-consolidation.md`.

**Decision history:**

- 2026-09-25 · adopted · ChatGPT build review: Adopt in the bounded local implementation and reproducible delivery; wider secure/native/operator acceptance remains unverified.
- 2026-10-18 · adopted · Codex sprint review: existing_task refinement: recovered newer pushed source from an older restored checkout; preserve source-bound run evidence and additive optional recording compatibility. Saved setup is not an active published environment. No acceptance promotion.
- 2026-10-25 · adopted · Codex integration review: existing_task: preserve source and uncertain auth evidence, resolve already-integrated PR ancestry, prepare exact next-agent tests. A generic save rejection did not establish the earlier claimed field-specific cause. No acceptance promotion.

### [ ] EM-072: A handoff needs a current entry point and historical precedence

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-15. **Origin:** Documentation consolidation and recovery audit.

Repeated local-only paragraphs coexist with a later published source and native pass. Without an authoritative dated entry point, a new agent could reapply old packages or reopen already verified engine work.

**Product implication:** Keep a linked current closeout and immutable historical documents; read the canonical ledger before acting.

**Roadmap links:** `DOC-02` (verified), `DOC-03` (verified), `DOC-06` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-15-documentation-consolidation.md`, `docs/delivery/context-manifest.json`, `docs/delivery/sessions/2026-10-15-main-consolidation.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`.

**Decision history:**

- 2026-10-15 · adopted · ChatGPT documentation consolidation: Bounded documentation/recovery improvement only; no new required runtime scope or acceptance claim.
- 2026-10-15 · adopted · Codex integration review: Unify latest source and separate documentation without replacing newer runtime/acceptance evidence. Preserve both archive variants and histories; owner authorizes this main integration, not release/model/human acceptance.
- 2026-10-16 · adopted · Codex research review: existing_task: component research preserves semantic/professional evaluation, source/case boundaries, shared scenario baselines, exact evidence and measured operator value. Research proposal changes no acceptance requirement.
- 2026-10-16 · adopted · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.

### [ ] EM-073: Archive completeness must follow the supplied manifest, not an old file count

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-15. **Origin:** Documentation consolidation and recovery audit.

The newly supplied research ZIP contains 19 files, including README and its manifest, while previous delivery notes described an 18-file variant. Every payload must be verified and retained rather than reconciled by deleting the difference.

**Product implication:** Preserve variant provenance and checksums, and state explicit gaps instead of claiming every external clone or chat is included.

**Roadmap links:** `DOC-02` (verified), `DOC-03` (verified), `DOC-06` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-15-documentation-consolidation.md`, `docs/delivery/context-manifest.json`, `docs/delivery/sessions/2026-10-15-main-consolidation.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`.

**Decision history:**

- 2026-10-15 · adopted · ChatGPT documentation consolidation: Bounded documentation/recovery improvement only; no new required runtime scope or acceptance claim.
- 2026-10-15 · adopted · Codex integration review: Unify latest source and separate documentation without replacing newer runtime/acceptance evidence. Preserve both archive variants and histories; owner authorizes this main integration, not release/model/human acceptance.
- 2026-10-16 · adopted · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.

### [ ] EM-074: Shared readiness must be reachable through either genuine alternative

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-15. **Origin:** V0.2 Qwen baseline recovery and generation-role contract correction.

The archived Qwen frame requires on-site spare-chair confirmation even for its external-hire alternative. Duplicate-title validation rejects this particular output, but cannot prove semantic branch neutrality in otherwise valid wording.

**Product implication:** Keep shared readiness separate from branch-specific preparation and from final success. Clarify generation guidance and include branch neutrality in independent review; do not weaken the validator or relabel a replay as model success.

**Roadmap links:** `B02-09` (blocked), `ES03-01` (partial).
**Completion scope:** `B02-09`.
**Evidence / source record:** `docs/evidence/qwen-baseline-2026-09-27.json`, `docs/delivery/sessions/2026-10-15-generation-role-contract.md`, `endstate/compilation.py`, `docs/evidence/generation-role-contract-2026-10-15.json`.

**Decision history:**

- 2026-10-15 · adopted · Codex sprint review: existing_task: clarify the existing generation contract now; fresh-model effectiveness and independent review remain required. No research feature or new release gate added.

### [ ] EM-075: A simulator needs a tested domain action and environment mapping

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-requested GitHub component/evolution research; source inspection, not runtime experiment.

MiroFish/OASIS source inspection shows Twitter/Reddit action spaces and simulation/report loops. Broader prediction language does not supply fixer-specific actors, legal actions, constraints or outcome verification.

**Product implication:** Evaluate domain mapping and incremental useful-failure discovery against authored scenarios before adopting a simulator. Preserve broader possible-world ambition as research.

**Roadmap links:** `ES03-01` (partial), `ES04-01` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/GITHUB-COMPONENTS-2026-10-16.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex research review: new_candidate: retain source-informed integration requirement for the proposed experiments; no required scope or runtime acceptance added.
- 2026-10-16 · candidate · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · candidate · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · candidate · Codex whole-system investigation: existing_task/candidate refinement: OASIS social action mappings, extra recommender artifacts and actor failures must be counted explicitly. No deferred runtime or acceptance promotion.

### [ ] EM-076: Memory deletion and retraction are projection contracts

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-requested GitHub component/evolution research; source inspection, not runtime experiment.

Graphiti library and companion server episode deletion follow different cleanup paths; multi-source support and generated simulation memory can outlive or be removed with one episode. Source-level inspection does not prove product retraction behavior.

**Product implication:** Keep canonical source retraction authoritative; test shared support, namespace separation, deletion/rebuild and case access before memory adoption.

**Roadmap links:** `B03-02` (not_started), `B04-02` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/GITHUB-COMPONENTS-2026-10-16.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex research review: new_candidate: retain source-informed integration requirement for the proposed experiments; no required scope or runtime acceptance added.
- 2026-10-16 · candidate · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · candidate · Codex whole-system investigation: existing_task/candidate refinement: Tencent merged ancestry/profile retraction, Graphiti optional scope/deletion and Mem0 retained history require complete projection/retention contracts. No deferred runtime or acceptance promotion.

### [ ] EM-077: A whole experiment needs a budget beyond each model call

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-requested GitHub component/evolution research; source inspection, not runtime experiment.

Model costs multiply across cases, branches, actors, rounds, repeats, embeddings and reports. Promptfoo cost assertions run after a response; per-call caps do not themselves bound total experiment spending.

**Product implication:** Require an aggregate experiment budget and stop accounting, provider caps where available, attempted-call receipts and explicit retry/cancellation policy.

**Roadmap links:** `ES03-05` (partial), `B03-04` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/GITHUB-COMPONENTS-2026-10-16.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md`, `docs/research/github-2026-10-16/ruflo-owner-guide.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex research review: new_candidate: retain source-informed integration requirement for the proposed experiments; no required scope or runtime acceptance added.
- 2026-10-16 · candidate · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · candidate · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · candidate · Codex compatible-provider sprint: existing_task refinement: preserve exact upstream pins/source exceptions, managed provider configuration, raw rejection evidence, stage/cancel/revision boundaries and actual-versus-controlled acceptance. Source copying adopts no upstream runtime.
- 2026-10-16 · candidate · Codex Ruflo owner source review: existing_task/candidate refinement: preserve separate model-access, bookkeeping, API-success, worker-routing and business-outcome targets; record synthetic/live benchmark scope and historical audit remediations. Optional coordinator remains unadopted.
- 2026-10-16 · candidate · Codex whole-system investigation: existing_task/candidate refinement: AgentSociety per-process retry/token stats, Temporal unlimited default retry, separate embedding/recommender/report calls and fictional case budgets do not enforce a USD experiment cap. No deferred runtime or acceptance promotion.

### [ ] EM-078: Upstream names hide materially different licence and API boundaries

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-requested GitHub component/evolution research; source inspection, not runtime experiment.

Pinned research found Mesa 4.0 alpha API changes, Phoenix Elastic License 2.0, MiroFish AGPL and multiple incompatible runtime/dependency ranges. Familiar project names alone do not identify an adoptable supported stack.

**Product implication:** Keep source pins, stable release selection and dependency/licence review with each optional adapter; compare alternatives before stacking frameworks.

**Roadmap links:** `ES04-04` (not_started), `DOC-06` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/GITHUB-COMPONENTS-2026-10-16.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/tencent-memory.md`, `docs/research/github-2026-10-16/ruflo.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex research review: new_candidate: retain source-informed integration requirement for the proposed experiments; no required scope or runtime acceptance added.
- 2026-10-16 · candidate · Codex Tencent source research: existing_task/candidate refinement: memory summaries and generated procedures need retained citations, scoped profiles, retraction/rebuild, actual-outcome evaluation and distinct bounded-choice failure states. MIT/beta source and model calls do not establish product acceptance.
- 2026-10-16 · candidate · Codex Ruflo source review: existing_task/candidate refinement: worker coordination and actual provider execution are different from hypothetical population simulation, correct plans, independent review and case authority. Preserve backend, version, budget and cancellation evidence.
- 2026-10-16 · candidate · Codex whole-system investigation: existing_task/candidate refinement: Incompatible Python/CAMEL ranges, shared Simulatrex package names, AutoGen maintenance and differing server/client/model licences require versioned isolated adoption decisions. No deferred runtime or acceptance promotion.

### [ ] EM-079: Optimisation candidates must retain feasibility and uncertainty status

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-requested GitHub component/evolution research; source inspection, not runtime experiment.

OR-Tools distinguishes feasible, optimal, unknown and infeasible under declared assumptions; pymoo may retain a least-infeasible candidate when none is feasible. Numeric sensitivity also depends on assumed input ranges.

**Product implication:** Preserve solver status and search bounds, revalidate returned routes, keep unknowns explicit and never promote a best-found candidate into execution authority or a calibrated forecast.

**Roadmap links:** `ES03-01` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/GITHUB-COMPONENTS-2026-10-16.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex research review: new_candidate: retain source-informed integration requirement for the proposed experiments; no required scope or runtime acceptance added.
- 2026-10-16 · candidate · Codex whole-system investigation: existing_task/candidate refinement: OR-Tools status/bounds and pymoo infeasible optima need host validation; SALib constant outputs, non-finite values and seed zero need explicit tests. No deferred runtime or acceptance promotion.

### [ ] EM-080: A memory scenario summary is distinct from a hypothetical world branch

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-supplied TencentDB Agent Memory source assessment.

Tencent L2 scenario means a model-maintained topic/scene narrative. Shared terminology does not implement ENDSTATE immutable case branches, explicit perturbations, simulated transitions or comparison/replay contracts.

**Product implication:** Use explicit adapter responsibility names and separate procedural recall from hypothetical-world experiments; verify each capability against its actual contract before counting it as available.

**Roadmap links:** `ES02-06` (partial), `ES03-01` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/tencent-memory.md`, `docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex source research: new_candidate: preserve terminology/contract distinction; no new required feature or runtime adoption.
- 2026-10-16 · candidate · Codex whole-system investigation: existing_task/candidate refinement: Topic/profile memory and shared-conversation handoff remain distinct from hypothetical world transitions. No deferred runtime or acceptance promotion.

### [ ] EM-081: A vector-shaped fallback does not establish semantic retrieval

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-supplied Ruflo source assessment.

The inspected Ruflo embedding policy permits a deterministic hash fallback when real embedders cannot load unless strict real-embedding policy is enabled. A correctly shaped vector or running search endpoint therefore does not establish meaningful semantic retrieval.

**Product implication:** Optional retrieval adapters must expose active backend/degraded mode and pass task-relevant semantic fixtures; configure fail-closed behavior where semantic output is required before adopting the provider.

**Roadmap links:** `B04-02` (not_started), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/ruflo.md`, `docs/research/github-2026-10-16/ruflo-owner-guide.md`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex bounded source review: new_candidate: retain an adapter validation requirement from source inspection; no runtime dependency or required scope promoted.
- 2026-10-16 · candidate · Codex Ruflo owner source review: existing_task/candidate refinement: preserve separate model-access, bookkeeping, API-success, worker-routing and business-outcome targets; record synthetic/live benchmark scope and historical audit remediations. Optional coordinator remains unadopted.
- 2026-10-16 · candidate · Codex whole-system investigation: existing_task/candidate refinement: A configured Qwen chat endpoint does not supply Graphiti embeddings/reranking or make hash fallback semantically meaningful. No deferred runtime or acceptance promotion.

### [ ] EM-082: External research copies need an application trust and test boundary

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-16. **Origin:** Qwen API transport and owner-authorized research-copy sprint.

Copying28 upstream repositories introduces more than71000 tracked files, upstream tests/configuration/instructions and model references. App verification must not traverse or execute them; sparse-clean Git status alone also does not establish every intended source path is materialized.

**Product implication:** Prune research/external before test/source traversal, fingerprint declared/checked-out pins and metadata, and verify every source path plus explicit sparse/model/LFS/nested exceptions and original notices.

**Roadmap links:** `DOC-07` (verified), `DOC-06` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `research/README.md`, `research/inventory.json`, `scripts/acceptance.py`, `tests/test_acceptance_runner.py`, `docs/evidence/compatible-native-2026-10-16.json`.

**Decision history:**

- 2026-10-16 · adopted · Codex build review: existing_task: implement bounded source/transport safeguards within the owner-authorized source-copy and provider work; no real-model or independent acceptance inferred.
- 2026-10-16 · adopted · Codex build review: existing_task: cumulative native run at ddfead7 passed 1,104 source/1,104 installed tests and 391 browser checks; inspection valid. This adds software evidence only, not live-provider or independent/human acceptance.

### [ ] EM-083: Rejected model evidence needs attributed and byte-safe retention

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-16. **Origin:** Qwen API transport and owner-authorized research-copy sprint.

A malformed HTTP200 body is not necessarily assistant output. Valid assistant text can contain malformed JSON, invalid Unicode or a credential encoded with Unicode escapes; literal-only redaction was insufficient in the first controlled transport review.

**Product implication:** Keep exact bounded assistant text only after envelope attribution, retain original hashes/omission reasons, reject reflected credentials including decoded forms, preserve HTTP-error redaction, and never repair evaluation output.

**Roadmap links:** `ES03-09` (verified), `B02-15` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `eightball/v2/compatible.py`, `tests/test_compatible_provider.py`, `docs/evidence/compatible-native-2026-10-16.json`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · adopted · Codex build review: existing_task: implement bounded source/transport safeguards within the owner-authorized source-copy and provider work; no real-model or independent acceptance inferred.
- 2026-10-16 · adopted · Codex build review: existing_task: cumulative native run at ddfead7 passed 1,104 source/1,104 installed tests and 391 browser checks; inspection valid. This adds software evidence only, not live-provider or independent/human acceptance.
- 2026-10-16 · adopted · Codex whole-system investigation: existing_task/candidate refinement: Validated compatible successes now retain exact bounded assistant text; HTTP envelopes/headers/error bodies remain excluded. No deferred runtime or acceptance promotion.

### [ ] EM-084: Confidence metrics need explicit prediction targets

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-requested plain-English Ruflo investigation.

The inspected Ruflo Q-router reports softmax confidence over learned worker-role Q-values; the inspected execution feedback uses return without API error as success. These metrics concern worker assignment and transport completion, while no calibrated business-outcome probability is established by those paths.

**Product implication:** Label the target and provenance of confidence/success metrics. Keep worker assignment, provider completion, independent plan quality and actual outcome measurement distinct; require held-out calibration before presenting a probability of achieving the client outcome.

**Roadmap links:** `ES03-02` (blocked), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/ruflo-owner-guide.md`, `docs/evidence/ruflo-owner-review-2026-10-16.json`, `docs/research/github-2026-10-16/whole-system-review.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex bounded source review: new_candidate: preserve a prediction-target/adapter evaluation requirement. No new required scope, runtime integration or independent acceptance follows from inspected source.
- 2026-10-16 · candidate · Codex whole-system investigation: existing_task/candidate refinement: Worker-routing confidence, API completion, causal effects and actual client-outcome probability keep separate prediction targets. No deferred runtime or acceptance promotion.

### [ ] EM-085: Fixed-model configuration must distinguish catalog variants and routers

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

The hosted model validator rejected an explicit OpenRouter :free catalog variant while admitting openrouter/free, which official documentation describes as a random model router. Controlled tests reproduced and now block that mismatch.

**Product implication:** Accept only the explicit selected catalog variant on its correct endpoint with pinned provider/no fallback; preserve requested/served identity and test known dynamic routers.

**Roadmap links:** `ES03-09` (verified), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`, `docs/delivery/sessions/2026-10-18-anthropic-configuration.md`.

**Decision history:**

- 2026-10-16 · adopted · Codex sprint review: existing_task: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.
- 2026-10-16 · adopted · Codex native verification: existing_task: tested 17a275c passed 1,171 source tests, 1,171 installed-kernel regressions and 391 native checks across all 11 suites passed; source/artifact inspection valid. No actual model or independent/human acceptance. This is bounded software evidence only; no gate promotion.
- 2026-10-18 · adopted · Codex Anthropic preparation: existing_task refinement: SDK-listed model identity, compatibility request formatting, allowed secret destination, active authentication and actual model quality remain separate. Official compatibility docs read was403; prepared configuration is not an inference result.

### [ ] EM-086: Experiment evidence must survive successive runs and interruptions

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

The hosted frozen-fixture runner wrote to one reusable report path, so a later invocation could replace earlier failure/success evidence. Unique runs and exclusive numbered checkpoints now preserve results and partial attempts.

**Product implication:** Checkpoint before subsequent calls, record source/version/input identity, retain interruption/unknown-response states and do not manufacture evidence after hard kill.

**Roadmap links:** `ES03-05` (partial), `B02-09` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`, `docs/delivery/sessions/2026-10-18-review-evidence.md`.

**Decision history:**

- 2026-10-16 · adopted · Codex sprint review: existing_task: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.
- 2026-10-16 · adopted · Codex native verification: existing_task: tested 17a275c passed 1,171 source tests, 1,171 installed-kernel regressions and 391 native checks across all 11 suites passed; source/artifact inspection valid. No actual model or independent/human acceptance. This is bounded software evidence only; no gate promotion.
- 2026-10-18 · adopted · Codex sprint review: existing_task refinement: recovered newer pushed source from an older restored checkout; preserve source-bound run evidence and additive optional recording compatibility. Saved setup is not an active published environment. No acceptance promotion.

### [ ] EM-087: Call admission and remote delivery require separate observations

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

The application increments calls_started before HTTP. Cancelled/stale/interrupted jobs correctly publish no proposal, so remote response/model/billing evidence can be unavailable. Fast provider completion can win a lifecycle intervention race.

**Product implication:** Label admission-trigger trials, record explicit missing remote evidence and not_exercised/inconclusive coverage, avoid automatic paid retries, and guarantee cleanup of only the owned process.

**Roadmap links:** `B02-15` (partial), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`.

**Decision history:**

- 2026-10-16 · adopted · Codex sprint review: existing_task: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.
- 2026-10-16 · adopted · Codex native verification: existing_task: tested 17a275c passed 1,171 source tests, 1,171 installed-kernel regressions and 391 native checks across all 11 suites passed; source/artifact inspection valid. No actual model or independent/human acceptance. This is bounded software evidence only; no gate promotion.

### [ ] EM-088: Document provenance needs original and derivative coordinate systems

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

Pinned Docling reading-order code strips/joins/replaces cell text before assigning spans, and tables can have charspan=(0,0). These coordinates describe derivative structure rather than exact original-PDF Unicode text.

**Product implication:** Keep original-file hashes, derivative/version/page/bbox and exported-text mappings separate; require independent OCR/table/source review and visible partial results.

**Roadmap links:** `B02-14` (partial), `B03-02` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex sprint review: new_candidate: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.

### [ ] EM-089: Local persistence can still have separate telemetry egress

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

Pinned Mem0 enables operation telemetry by default to us.i.posthog.com even when vector persistence is local. This source observation does not establish case-text leakage or a vulnerability.

**Product implication:** Record all data exits and telemetry configuration before an isolated future pilot; local storage alone cannot establish no external transmission.

**Roadmap links:** `B03-01` (partial), `B04-02` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex sprint review: new_candidate: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.

### [ ] EM-090: Completed simulation drivers can conceal failed actors

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

Pinned OASIS catches actor exceptions and returns them while its environment step discards gather results. A normally completed driver therefore need not report every actor action as successful.

**Product implication:** Require explicit actor/step failure and omission accounting, classify partial runs and retain attempted-call costs before comparing simulated worlds.

**Roadmap links:** `ES03-05` (partial), `ES02-06` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex sprint review: new_candidate: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.

### [ ] EM-091: Preserved repository revisions need compatible isolated environments

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

Pinned OASIS requires Python below 3.12 while Mesa HEAD requires 3.12 or later; MiroFish pins different CAMEL/OASIS versions, and both Simulatrex repos publish the same package/import name.

**Product implication:** Treat alternatives as versioned adapter environments, select supported releases deliberately and test exact dependency/model artifacts rather than co-installing copied HEADs.

**Roadmap links:** `ES03-05` (partial), `DOC-07` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex sprint review: new_candidate: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.

### [ ] EM-092: Workflow recovery needs explicit durability and retry semantics

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

LangGraph defaults to async durability and resumes interrupted nodes from their beginning. Temporal retry maximum zero means no maximum. Persistence alone does not renew case authority or make paid external effects exactly once.

**Product implication:** Choose durability/attempt/time/idempotency policies explicitly, recheck source/case/permission on resume and reconcile ambiguous external outcomes before retry.

**Roadmap links:** `ES02-02` (partial), `ES02-04` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex sprint review: new_candidate: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.

### [ ] EM-093: Evaluation modes need explicit execution and freshness contracts

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

Pinned Phoenix dry_run still executes experiment tasks and defaults to three retries; Promptfoo caches by default and supports transforms/repeats/retries. A harmless-sounding mode or green result does not establish fresh unassisted inference.

**Product implication:** Prefer importing retained outputs initially, and declare live calls/cache/retry/transform settings and all failures for any later evaluation-tool adapter.

**Roadmap links:** `B02-11` (partial), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex sprint review: new_candidate: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.

### [ ] EM-094: Structural success can outlive valid source provenance

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-18. **Origin:** V0.2 source-stable evidence and prospective review sprint.

A controlled hosted-fixture response changed the source after the initial fingerprint. The old runner still evaluated all four fixtures and returned success. Bracketing source checks now fail the evidence gate and preserve structural results and raw responses independently.

**Product implication:** Bind each admitted fixture and final receipt to the same inspected source, keep observed drift sticky, and stop subsequent fixtures. These snapshots do not establish continuous source stability or loaded-code identity.

**Roadmap links:** `B02-09` (blocked), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `evals/live_huggingface.py`, `tests/test_hosted_eval_retention.py`, `docs/delivery/sessions/2026-10-18-review-evidence.md`, `docs/evidence/review-evidence-native-2026-10-18.json`.

**Decision history:**

- 2026-10-18 · adopted · Codex sprint review: existing_task: bounded evidence-tool refinement; no new required acceptance gate, research runtime or professional/human approval.
- 2026-10-18 · adopted · Codex native verification: existing_task software evidence: 1,267 source tests, 1,267 installed-kernel regressions and 391 native browser checks across all 11 suites passed; exact-source/artifact inspection valid before final documentation edits. No model/professional/human acceptance or required scope promotion.

### [ ] EM-095: A summary flag is weaker than returned-call evidence

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-18. **Origin:** V0.2 source-stable evidence and prospective review sprint.

Lifecycle prerequisites accepted representative schema-2 summaries without any proposal or returned-call records because the top-level actual-hosted-request flag was sufficient. Per-fixture identity, call records and stable final source must be checked separately.

**Product implication:** Treat receipts as unsigned engineering records. Reject inconsistent or missing generation prerequisites before admitting a new actual-provider lifecycle run; this does not authenticate remote execution.

**Roadmap links:** `B02-09` (blocked), `B02-12` (blocked), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `evals/provider_lifecycle.py`, `tests/test_provider_lifecycle.py`, `docs/delivery/sessions/2026-10-18-review-evidence.md`, `docs/evidence/review-evidence-native-2026-10-18.json`.

**Decision history:**

- 2026-10-18 · adopted · Codex sprint review: existing_task: bounded evidence-tool refinement; no new required acceptance gate, research runtime or professional/human approval.
- 2026-10-18 · adopted · Codex native verification: existing_task software evidence: 1,267 source tests, 1,267 installed-kernel regressions and 391 native browser checks across all 11 suites passed; exact-source/artifact inspection valid before final documentation edits. No model/professional/human acceptance or required scope promotion.

### [ ] EM-096: Mechanical study readiness is separate from genuine prospective approval

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-18. **Origin:** V0.2 source-stable evidence and prospective review sprint.

An optional strict recording format can identify missing prospective study details, numeric threshold decisions, changed gates, mismatched private artifacts and exact public fixture reuse. It cannot authenticate reviewer qualifications, independent authorship, permissions, approval or when execution actually occurred.

**Product implication:** Keep existing manual v1 studies legitimate, add recording v2 without revising the semantic protocol, and leave all independent/model/human acceptance flags false even when a fictional bundle is mechanically complete.

**Roadmap links:** `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `evals/review_readiness.py`, `tests/test_review_readiness.py`, `docs/delivery/sessions/2026-10-18-review-evidence.md`, `docs/evidence/review-evidence-native-2026-10-18.json`.

**Decision history:**

- 2026-10-18 · adopted · Codex sprint review: existing_task: bounded evidence-tool refinement; no new required acceptance gate, research runtime or professional/human approval.
- 2026-10-18 · adopted · Codex native verification: existing_task software evidence: 1,267 source tests, 1,267 installed-kernel regressions and 391 native browser checks across all 11 suites passed; exact-source/artifact inspection valid before final documentation edits. No model/professional/human acceptance or required scope promotion.

### [ ] EM-097: Endpoint host identity does not distinguish service paths

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-18. **Origin:** Independent engineering review of lifecycle prerequisites.

Compatible provider receipts bind the endpoint host but not the full configured API base path. Two service or tenant paths on the same host therefore cannot be distinguished by the current receipt configuration identity.

**Product implication:** Treat existing receipts as host-bound unsigned engineering records. Consider a separately scoped canonical base-URL fingerprint before reusing evidence across same-host path changes; never include keys or sensitive URL components.

**Roadmap links:** `B02-09` (blocked), `B02-12` (blocked), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `evals/provider_lifecycle.py`, `docs/v2/ACTUAL-PROVIDER-EVIDENCE.md`, `docs/delivery/sessions/2026-10-18-review-evidence.md`, `docs/evidence/review-evidence-native-2026-10-18.json`.

**Decision history:**

- 2026-10-18 · candidate · Codex engineering review: new_candidate: preserve the observed limitation explicitly rather than broadening this sprint into endpoint identity redesign. No model acceptance or configuration attestation is claimed.
- 2026-10-18 · candidate · Codex native verification: new_candidate retained: 1,267 source tests, 1,267 installed-kernel regressions and 391 native browser checks across all 11 suites passed; exact-source/artifact inspection valid before final documentation edits. No model/professional/human acceptance or required scope promotion.

### [ ] EM-098: Changing provider also requires changing the managed secret destination

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-18. **Origin:** Owner-selected Anthropic environment preparation.

The existing generic API-key requirement was labelled Qwen and allowed only its former service host. An automatic change to its allowed destination was rejected with no draft mutation; changing URL/model suggestions alone cannot rebind that managed key. Duplicate requirements are explicitly prohibited.

**Product implication:** Show a novice one exact existing key variable and destination edit. Preserve saved bindings, require the owner to edit that row securely, and distinguish draft network/variable preparation from active credential delivery and actual inference.

**Roadmap links:** `B02-09` (blocked), `B02-15` (partial), `ES03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-18-anthropic-configuration.md`, `docs/evidence/anthropic-setup-2026-10-18.json`, `docs/v2/ANTHROPIC-SETUP.md`, `docs/delivery/sessions/2026-10-25-build-consolidation.md`.

**Decision history:**

- 2026-10-18 · adopted · Codex configuration review: existing_task: document the observed secret-rebinding restriction and exact owner step; no new required feature, model/professional/human acceptance or runtime research adoption.
- 2026-10-25 · adopted · Codex integration review: existing_task: preserve source and uncertain auth evidence, resolve already-integrated PR ancestry, prepare exact next-agent tests. A generic save rejection did not establish the earlier claimed field-specific cause. No acceptance promotion.

### [ ] EM-099: Object grants cannot authorise aggregate matter operations

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Agency authorisation foundation.

A grant to read one object cannot grant a matter listing, search, export or inference over other objects. Identity includes issuer as well as subject.

**Product implication:** Enforce server-owned scope on every consumed object and reload revoked grants; policy permits remain separate from action approval.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** `B03-01`.
**Evidence / source record:** `eightball/authorisation.py`, `tests/test_authorisation.py`, `docs/delivery/sessions/2026-10-25-agency-authorisation.md`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: implement fail-closed policy foundation under owner-authorised full-product roadmap; API enforcement remains unfinished.

### [ ] EM-100: Adding authenticated identity does not make every existing route safe

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Agency API and overview sprint.

The local API has aggregate listings, legacy imports and asynchronous jobs whose existing single-operator assumptions cannot inherit agency permissions from a sign-in check alone.

**Product implication:** Use an explicit opt-in allowlist and deny unintegrated routes until actor, transaction and worker enforcement exists. Present a readable situation overview before graph detail.

**Roadmap links:** `B03-01` (partial), `B02-19` (partial).
**Completion scope:** `B03-01`.
**Evidence / source record:** `docs/v2/AGENCY-ACCESS.md`, `docs/delivery/sessions/2026-10-25-agency-api-overview.md`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: preserve local compatibility and refuse unsafe agency operations while implementing the full product roadmap.

### [ ] EM-101: Arrival order and occurrence time must remain separate during replay

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** ENDSTATE durable inbox.

A delayed source event can arrive after a newer occurrence. Reordering by its claimed clock or replacing an earlier receipt on retry would change history. Identical deliveries need the same retained receipt; changed content under the same identity must conflict.

**Product implication:** Retain scoped arrival sequence, optional occurrence time and original receipt; ingestion remains pending and cannot execute commands.

**Roadmap links:** `ES02-01` (partial), `ES02-02` (partial).
**Completion scope:** `ES02-01`, `ES02-02`.
**Evidence / source record:** `docs/endstate/EVENT-INBOX.md`, `docs/delivery/sessions/2026-10-25-endstate-event-inbox.md`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: implement neutral event contract and durable host inbox without promoting incoming data into authority.

### [ ] EM-102: A durable lease is not permission to repeat external work

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** ENDSTATE event processing lifecycle.

A restarted process cannot infer whether a leased operation already reached an external service. Expired attempts must become interrupted rather than being silently claimed again. A new explicit attempt must preserve the previous record.

**Product implication:** Keep durable attempt identity, opaque claim ownership, original revision and terminal history. Stale or denied outputs remain separate from reviewable results.

**Roadmap links:** `ES02-02` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-02`, `ES02-04`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-25-endstate-processing.md`, `eightball/event_work.py`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: durable processing foundation without automatic paid replay or action authority.

### [ ] EM-103: Discarding stale review responses must resolve the loading state

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Native Plan Review race during ENDSTATE lifecycle verification.

Case refresh changed the review snapshot while assessment was in flight. The stale response was safely discarded, but its dialog remained on Inspecting indefinitely. Remote CI passing did not negate the local observed race.

**Product implication:** End stale loading with an explicit recovery state and deliberate reopening, while never allowing an older request to overwrite a newer dialog.

**Roadmap links:** `B02-11` (partial), `ES02-04` (partial).
**Completion scope:** `B02-11`.
**Evidence / source record:** `docs/evidence/endstate-processing-failed-2026-10-25.json`, `docs/delivery/sessions/2026-10-25-endstate-processing.md`, `tests/browser_plan_review.py`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: fix observed race, add deterministic native coverage and preserve the failed receipt.

### [ ] EM-104: Reviewed consumption must bind source, result, identity and case commit together

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** ENDSTATE reviewed graph transaction.

A durable processing result alone cannot authorise a graph update. The explicit review must bind the original receipt and result, reviewer, rationale, command and exact revision, with permission checked inside the same write transaction and again before commit if calculation can outlive a grant.

**Product implication:** Preserve source/result and explicit edits in a case-linked receipt. Reject stale, revoked, expired or cross-matter consumption; retain original export shape for cases without consumed events.

**Roadmap links:** `ES02-02` (partial), `ES02-03` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-03`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-25-endstate-reviewed-consumption.md`, `eightball/v2/event_reviews.py`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: atomic local reviewed consumption with provenance and unchanged semantic/human acceptance gates.

### [ ] EM-105: Delivery acknowledgement is separate from review and action approval

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** ENDSTATE transactional local outbox.

A committed graph review can be lost to downstream readers if notice creation occurs after its transaction. Atomic creation plus independent durable per-reader acknowledgement survives restarts, but repeats remain possible and acknowledgement cannot carry execution authority.

**Product implication:** Persist a small case/revision notice in the same transaction. Recheck current read permissions on pull and acknowledgement; keep delivered, reviewed and approved states distinct.

**Roadmap links:** `ES02-02` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-02`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-25-endstate-outbox.md`, `eightball/v2/event_outbox.py`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: local durable delivery foundation; external effects and production acceptance remain unimplemented.

### [ ] EM-106: Reviewed API writes must share the grant transaction and authorise returned source

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Authenticated event review API.

A route guard may pass before a grant is revoked, and a separate registry cannot participate in the case transaction. A write response containing source/result provenance also requires current read access, even when write permission is present.

**Product implication:** Register event routes only with a shared case/registry database, bind JWT identity server-side, and require READ plus WRITE inside the HTTP review transaction.

**Roadmap links:** `B03-01` (partial), `ES02-03` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-03`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-25-endstate-event-api.md`, `eightball/v2/event_api.py`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: verified local review API with unchanged production and human gates.

### [ ] EM-107: Matter scope and revision do not uniquely identify a processing case

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Same-matter event review reproduction.

Two cases may share a matter and revision. An attempt storing only matter scope and base revision can then be consumed by either case. The existing full native suite passed while an additional reproduction demonstrated this missing lineage constraint.

**Product implication:** Bind case processing explicitly at enqueue and reject unbound new consumption. Preserve historical unknown identity during migration; previously committed receipts remain records of what happened.

**Roadmap links:** `ES02-02` (partial), `ES02-03` (partial).
**Completion scope:** `ES02-02`, `ES02-03`.
**Evidence / source record:** `docs/evidence/endstate-event-api-case-binding-gap-2026-10-25.json`, `docs/delivery/sessions/2026-10-25-endstate-event-api.md`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: correct demonstrated lineage failure without inventing historical case ownership.

### [ ] EM-108: A lost save acknowledgement requires outcome recovery, not automatic replay

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Native browser event review.

The server can commit a reviewed amendment while the browser loses its acknowledgement. Retrying automatically would confuse mutation intent with network recovery. A controlled native test committed once, discarded the response and recovered the outcome through explicit refresh.

**Product implication:** Disable editing while outcome is uncertain; retain original source/result and use deliberate refresh without repeating the mutation.

**Roadmap links:** `ES02-03` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-03`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-25-endstate-review-ui.md`, `tests/browser_event_review.py`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: improve review recovery and native evidence without relaxing acceptance.

### [ ] EM-109: Disabled-state tests must inspect interactive controls

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Native browser event review.

The first native review run asserted Playwright disabled state on a fieldset. The DOM had the disabled attribute, but that assertion did not verify its controls. Inspecting the actual rationale input and preview button accurately exercised read-only access.

**Product implication:** Preserve the failed artifact and assert effective disabled state on real controls; do not remove permission checks to obtain a passing test.

**Roadmap links:** `ES02-03` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-03`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-25-endstate-review-ui.md`, `docs/evidence/event-review-browser-first-failure-2026-10-25.json`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: improve review recovery and native evidence without relaxing acceptance.

### [ ] EM-110: A structured plan already exceeds the provisional result-text cap

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Native browser event review.

The fictional demo graph serializes to 16,501 characters. EventWork accepts at most 12,000 characters, so preserving the complete graph through that path failed without truncation and left the attempt running.

**Product implication:** Before connecting the worker, retain complete provider output within justified bounds or immutable artifact references, and explicitly preserve oversized failure evidence.

**Roadmap links:** `ES02-02` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-02`, `ES02-04`.
**Evidence / source record:** `docs/evidence/event-result-size-boundary-2026-10-25.json`, `docs/delivery/sessions/2026-10-25-endstate-review-ui.md`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: retain demonstrated integration boundaries and fix test harness without weakening acceptance.
- 2026-10-25 · adopted · Codex: Existing output boundary corrected to supported 500000 UTF-8 bytes with exact retention tests; authenticated worker and actual-provider acceptance remain unfinished.

### [ ] EM-111: Native test waits must honour both CSP and application timing

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Native browser event review.

A screenshot wait using string evaluation failed under script-src self in both local native and GitHub CI runs. Its locator replacement first used a 5-second default despite a 6.5-second notification lifetime.

**Product implication:** Keep CSP intact, assert with browser locator APIs and use a bounded deadline matching the real notification lifetime; preserve failed runs.

**Roadmap links:** `ES02-03` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-03`, `ES02-04`.
**Evidence / source record:** `docs/evidence/event-review-native-csp-failure-2026-10-25.json`, `docs/delivery/sessions/2026-10-25-endstate-review-ui.md`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: retain demonstrated integration boundaries and fix test harness without weakening acceptance.

### [ ] EM-112: Result capacity should count encoded bytes across the provider and queue boundary

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Complete processing-result retention.

Character count and UTF-8 byte count differ for multilingual text. A character-only bound neither matches the provider envelope limit nor reliably bounds stored output. Exact and one-byte-over tests demonstrated the difference.

**Product implication:** Use a justified byte limit, preserve exact original text and reject oversized results without mutating or silently repairing the attempt.

**Roadmap links:** `ES02-02` (partial), `ES02-04` (partial).
**Completion scope:** `ES02-02`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-25-complete-result-retention.md`, `tests/test_event_work.py`.

**Decision history:**

- 2026-10-25 · adopted · Codex: existing_task: consistent bounded retention without provider or semantic acceptance claims.
