# Evolving emergence register: nothing silently discarded

> Generated from `docs/delivery/emergence.json`. Decision history lives there; delivery status comes only from `progress.json`. Run `python scripts/emergence.py --write`.

8BALL remains the fixer product. ENDSTATE supplies reusable calculations. This is the build-discovery register, not a client-case insight ledger.

Last review: 2026-10-26. **216 recorded discoveries.**

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

**Roadmap links:** `B04-03` (partial), `B04-04` (deferred).
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

**Roadmap links:** `B04-03` (partial), `ES03-02` (blocked).
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

**Roadmap links:** `B04-02` (partial).
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

**Roadmap links:** `B04-03` (partial), `B02-22` (not_started), `B04-04` (deferred).
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

**Roadmap links:** `B04-04` (deferred), `B04-02` (partial), `B02-11` (partial).
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

**Roadmap links:** `ES03-01` (partial), `ES04-01` (partial).
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

**Roadmap links:** `B03-02` (partial), `B04-02` (partial).
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

**Roadmap links:** `ES03-05` (partial), `B03-04` (partial).
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

**Roadmap links:** `ES04-04` (partial), `DOC-06` (verified).
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

**Roadmap links:** `B04-02` (partial), `ES03-05` (partial).
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

**Roadmap links:** `B02-14` (partial), `B03-02` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-16/whole-system-review.md`, `docs/evidence/whole-system-readiness-2026-10-16.json`, `docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md`.

**Decision history:**

- 2026-10-16 · candidate · Codex sprint review: new_candidate: preserve bounded engineering evidence or optional adapter requirement; no independent/model/human acceptance or new required research scope.

### [ ] EM-089: Local persistence can still have separate telemetry egress

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-16. **Origin:** Owner-delegated whole-system investigation and evaluation-readiness sprint.

Pinned Mem0 enables operation telemetry by default to us.i.posthog.com even when vector persistence is local. This source observation does not establish case-text leakage or a vulnerability.

**Product implication:** Record all data exits and telemetry configuration before an isolated future pilot; local storage alone cannot establish no external transmission.

**Roadmap links:** `B03-01` (partial), `B04-02` (partial).
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

### [ ] EM-253: Parallel task claims need explicit file and delivery-register ownership

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** roadmap-partition-2026-10-25.

Existing ledger task paths share routers, authorisation, worker and delivery registers; task-ID assignment alone does not partition implementation or prevent discovery-ID collisions. A reproducible seven-lane plan needs disjoint owned paths, a current-authority service/registration seam, reserved EM ranges and serial integration of lane-local evidence fragments.

**Product implication:** Parallel builders can preserve the fixer app and exact acceptance gates only if shared wiring, optional holds and external/professional decisions are not mistaken for lane-owned implementation or passed acceptance.

**Roadmap links:** `DOC-03` (verified), `DOC-06` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/ROADMAP-LANES.md`, `docs/delivery/progress.json`, `eightball/api.py`, `eightball/v2/api.py`, `eightball/v2/event_api.py`, `docs/delivery/sessions/2026-10-25-roadmap-partition.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin: decision_record: owner requested bounded coordination, not implementation or a new backlog. Reserve EM-113..252 for builders; this coordination decision uses EM-253 outside those ranges. Preserve original task gates and optional holds; later upstream documentation/evidence needs additive integration, not attribution to this baseline. No product acceptance gate is linked or claimed.

### [ ] EM-173: A disclosure review binds the recipient and exact grant, not only content

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Collaboration B03-03 implementation, session 7e526575ef714b7e8a85f6ef00ee7ca6.

An otherwise reviewed projection can be misdirected or silently revived if recipient, object and immutable client-grant digest are not checked with the exact content digest; replacing a revoked grant must not repair the old review.

**Product implication:** 8BALL disclosure review must preserve exact recipient/grant/content scope separately from evidence state and action authority; keep revoked and withdrawn records terminal and auditable.

**Roadmap links:** `B03-03` (partial).
**Completion scope:** `B03-03`.
**Evidence / source record:** `tests/test_projection.py`, `eightball/projections/service.py`, `docs/delivery/lane-reports/collaboration.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin engineering proposal: Existing-task B03-03 safety refinement demonstrated with controlled SQLite tests; no global acceptance or new required scope.

### [ ] EM-174: A safe source preview is not the final disclosure commit gate

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Collaboration/vault same-transaction seam discussion and implementation.

Standalone safe metadata or source handles cannot authorize a projection mutation: source access, release state, revision, integrity and retention may change between preview and commit. The source gate and mutation/audit must share the same active write transaction.

**Product implication:** Keep a fail-closed transaction-local vault gate in 8BALL integration; opaque handles are references, never bearer capabilities. Missing or different-database adapters deny rather than granting local bearer access.

**Roadmap links:** `B03-03` (partial).
**Completion scope:** `B03-03`.
**Evidence / source record:** `eightball/collaboration/contracts.py`, `tests/test_collaboration.py`, `docs/v2/COLLABORATION.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin engineering proposal: Existing-task refinement with explicitly confirmed vault contract and controlled wrapper tests; actual shared identity/vault/case combination remains an integration gate.

### [ ] EM-175: Client source readiness checks must not create internal source read access

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Projection client-read authority integration design.

Reusing a vault current-READ source gate under the client identity could require a broad internal grant merely to read curated projection content. Checking source lifecycle under the still-current independent reviewer, while separately checking the exact client projection grant, keeps those authorities distinct.

**Product implication:** Allow clients only the separately reviewed content allowlist; deny after reviewer or source access revocation without exposing source handles, metadata or internal objects. Host role/route mappings still require negative integration tests.

**Roadmap links:** `B03-03` (partial).
**Completion scope:** `B03-03`.
**Evidence / source record:** `tests/test_projection.py`, `eightball/projections/service.py`, `docs/v2/COLLABORATION.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin engineering proposal: Existing-task B03-03 distinction; controlled test denies client source authority while allowing only reviewed projection, not proof of production policy correctness.

### [ ] EM-176: Measure exact disclosure review and refresh recovery burden

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-25. **Origin:** Collaboration isolated UI and failure-recovery build review.

Exact recipient IDs, digests, separate review and explicit refresh after uncertain writes may prevent misdirected disclosure but also impose substantial manual review and recovery work; screen and passing-test counts do not show net operator benefit.

**Product implication:** Evaluate fictional-user disclosure tasks with wrong-recipient prevention, correction rate, review time and stale-refresh recovery measures before expanding the interface or claiming customer value.

**Roadmap links:** `B03-03` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `web/v2/collaboration-view.js`, `docs/delivery/lane-reports/collaboration.md`.

**Decision history:**

- 2026-10-25 · candidate · Devin engineering proposal: Retain for owner/usability review; no participant study, native new-flow review or new mandatory roadmap task is authorized or claimed.

### [ ] EM-177: Checkout tests alone do not prove installed-kernel test portability

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Collaboration isolated ENDSTATE wheel regression failure and repair.

1393 checkout tests passed while two collaboration tests could not collect under the installed-kernel runner's isolated importlib mode because sibling fixture imports were unqualified. Package-qualified test imports then passed 37 focused tests in both modes and 1393 installed-wheel regressions.

**Product implication:** Preserve installed-package verification alongside checkout tests for 8BALL/ENDSTATE work; distinguish a test portability repair from a kernel defect or broad acceptance. Keep the failed source-bound receipt rather than replacing it with later totals.

**Roadmap links:** `B03-03` (partial).
**Completion scope:** `B03-03`.
**Evidence / source record:** `tests/test_collaboration_api.py`, `tests/test_projection.py`, `docs/delivery/lane-reports/collaboration.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin engineering proposal: Existing-task verification refinement, corrected within owned tests and proven by final offline wheel/native runner; no new required scope, production/platform portability or B03 acceptance claim.

### [ ] EM-213: Pack content identity is not current case authority

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25-domain-packs-engineering.

A canonical all-section pack digest can detect changes to prompts, policies and adapter declarations, but neither a digest nor a caller subject authenticates a consumer. The read-only consumer needs independently host-authenticated identity, current scoped grants and a fresh revision-bound snapshot; local bearer identity, cross-scope requests and post-read revocation are rejected in focused tests.

**Product implication:** Keep pack review state host-owned and do not use a content pin or preview response as approval, publisher identity or a later commit/send/download ticket.

**Roadmap links:** `ES04-01` (partial), `ES04-04` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `endstate/domain_packs/loader.py`, `endstate/domain_packs/consumer.py`, `tests/test_domain_packs.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task / decision_record: bounded engineering and safe integration guidance under the linked existing tasks only. No new required scope, acceptance promotion, owner approval, public launch or release decision.

### [ ] EM-214: Reusable policy templates must not pre-confirm a case

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25-domain-packs-engineering.

The support reuse fixture originally had confirmed policy state. A reusable pack must reject that state, while a live host snapshot may independently record manual policy review. Focused tests show that review alone still cannot satisfy an unobserved authority predicate, and that unrelated catalogue changes fail review matching.

**Product implication:** Keep reusable hypotheses, human policy review, observed authority, action permission, completion and verified remedy outcome separate; never overlay a pack onto live state.

**Roadmap links:** `ES04-01` (partial), `ES04-03` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `tests/fixtures/domain_packs/support.json`, `endstate/domain_packs/contracts.py`, `endstate/domain_packs/consumer.py`, `tests/test_domain_packs.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task / decision_record: bounded engineering and safe integration guidance under the linked existing tasks only. No new required scope, acceptance promotion, owner approval, public launch or release decision.

### [ ] EM-215: Passing source consumers do not establish packaged distribution

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25-domain-packs-engineering.

The frozen setuptools manifest lists only endstate. The internal wheel smoke passes but omits endstate.domain_packs; the actual installed-wheel regression run fails test collection with ModuleNotFoundError. Source-isolated reuse and 1415 source tests therefore do not prove this preview ships. No top-level LICENSE/LICENCE file or independent release approval was found/created in this checkpoint.

**Product implication:** Integration must explicitly include the subpackage and rerun installed regressions, then separately settle licence/support/distribution and independent release approval; do not launch SDK/API/MCP from source-only evidence.

**Roadmap links:** `ES04-04` (partial), `ES10-01` (partial), `ES10-02` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `pyproject.toml`, `docs/endstate/DOMAIN-PACKS.md`, `tests/test_domain_packs.py`, `docs/delivery/lane-reports/domain-packs.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task / decision_record: bounded engineering and safe integration guidance under the linked existing tasks only. No new required scope, acceptance promotion, owner approval, public launch or release decision.

### [ ] EM-113: Source-processing review and current source policy are independent gates

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Events roadmap lane build at f749627f9f7456ddcc5744f22374c57f8c5e64be.

A whole-matter grant and an explicit review of incoming text do not establish current object quarantine, retention or processing/egress permission. Revocation between preview or claim and consumption must still deny; missing policy cannot default to a local test adapter.

**Product implication:** Keep explicit receipt/revision review separate from factual attestation and action authority. Wire current identity/vault/provider source policy transactionally before agency processing; make denial visible rather than weakening checks. Extra review/policy checks add integration and operator burden, but a permissive default would leak data.

**Roadmap links:** `ES02-01` (partial), `ES02-02` (partial), `ES02-03` (partial), `B03-04` (partial).
**Completion scope:** `ES02-01`, `ES02-02`, `ES02-03`, `B03-04`.
**Evidence / source record:** `eightball/event_workers/service.py`, `eightball/v2/event_reviews.py`, `tests/test_event_dispatch.py`, `docs/delivery/lane-reports/events.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin / events engineering lane (not owner sign-off): Existing task refinement: mandatory fail-closed policy callback implemented and negatively tested; production adapter/native integration remains unaccepted, not a new required task.

### [ ] EM-114: Uncertain event processing must retain disposition without automatic provider replay

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Events roadmap lane build at f749627f9f7456ddcc5744f22374c57f8c5e64be.

A durable claim may outlive cancellation, worker revocation, lease expiry or a failed result-storage transaction. A repeated processing request after such a failure could duplicate a paid or non-recallable call even though no reviewable result was persisted.

**Product implication:** Claim and run-marker persistence precede one explicit call. Keep original bounded late output as inert trace where storage succeeds; do not publish stale/cancelled results, resume on restart or claim an external request was recalled. Storage failure can still prevent retaining raw output; operator inspection is preferable to invented success.

**Roadmap links:** `ES02-02` (partial), `ES02-04` (partial), `B03-04` (partial).
**Completion scope:** `ES02-02`, `ES02-04`, `B03-04`.
**Evidence / source record:** `eightball/event_workers/service.py`, `eightball/event_work.py`, `tests/test_event_dispatch.py`, `docs/delivery/lane-reports/events.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin / events engineering lane (not owner sign-off): Existing task refinement: explicit attempt lifecycle, retained safe failure codes and no automatic re-execution implemented; paid/live provider and production crash/recovery acceptance stay open.

### [ ] EM-115: Conservative replan reuse must retain explicit clocks and approval revisions

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Events roadmap lane build at f749627f9f7456ddcc5744f22374c57f8c5e64be.

Revision-only case changes can leave planning inputs unchanged, but action approvals depend on the exact revision and expiry. Reusing a result while omitting approval revision or as-of clock could revive expired or invalid authority.

**Product implication:** Use detached bounded exact-input/clock caching with revision-only reuse only when approvals are absent, and full ENDSTATE fallback for all other changes. This gives a narrowly testable optimization without inventing a broad partial-graph algorithm; conservative fallback may offer little speedup on changing cases.

**Roadmap links:** `ES02-04` (partial).
**Completion scope:** `ES02-04`.
**Evidence / source record:** `eightball/event_workers/replan.py`, `tests/test_event_replan.py`, `docs/delivery/lane-reports/events.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin / events engineering lane (not owner sign-off): Existing task refinement: conservative cache and exact full-response parity tested. General incremental-graph performance/production throughput remains an explicit limitation, not a passed gate.

### [ ] EM-116: A bounded retry ceiling needs an explicit operator recovery policy

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Events roadmap lane build at f749627f9f7456ddcc5744f22374c57f8c5e64be.

Three retained explicit attempts prevent silent retry loops, but exhausting that ceiling leaves no in-place reset. An operator may need to distinguish an invalid source or withdrawn consent from an infrastructure incident without erasing history or forging a new success.

**Product implication:** Evaluate a separately reviewed recovery workflow that preserves source, failure and billing/permission history, rather than adding unlimited resets or automatic retries. It could reduce operator friction, but may undermine budgets or encourage duplicate paid calls if policy is loose.

**Roadmap links:** `ES02-02` (partial), `B03-04` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `eightball/event_workers/service.py`, `tests/test_event_dispatch.py`, `docs/delivery/lane-reports/events.md`.

**Decision history:**

- 2026-10-25 · deferred · Devin / events engineering lane (not owner sign-off): Candidate recovery UX/policy requires owner/provider-budget decisions and observed operator need. Current bounded attempts remain; no reset bypass or extra required scope implemented.

### [ ] EM-117: Pre-commit local stage metrics are not combined provider or human latency evidence

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Events roadmap lane build at f749627f9f7456ddcc5744f22374c57f8c5e64be.

Local ingestion/processor/review timers can be retained on an atomic review record, but in-transaction durations stop before durability commit. Deterministic clocks in fixtures can verify instrumentation without measuring real inference or human review; mixed fixture and wall clocks yield incomparable waiting totals.

**Product implication:** Label metric scope, keep unknown historical durations null and retain the limitation instead of treating a fast scripted fixture as product performance. Integrated monotonic/UTC instrumentation and separately authorized real-provider/operator measurements are still needed.

**Roadmap links:** `ES02-04` (partial).
**Completion scope:** `ES02-04`.
**Evidence / source record:** `eightball/v2/event_reviews.py`, `eightball/event_workers/service.py`, `tests/test_event_dispatch.py`, `docs/delivery/lane-reports/events.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin / events engineering lane (not owner sign-off): Existing task refinement: local instrumentation and honest fictional timings retained; combined durability/provider/human and production latency gates remain open.

### [ ] EM-133: Object authority is not aggregate matter authority

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25 identity lane build and review; session d9478f50b2b844fcb292873f9d406d3d.

Object-only grants and a subset of operations cannot authorize whole-case access or another object; every requested operation must be checked against every consumed object.

**Product implication:** Keep aggregate projections explicit and require host object ownership/policy checks before any consumption.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** `B03-01`.
**Evidence / source record:** `docs/delivery/lane-reports/identity.md`, `docs/v2/AGENCY-ACCESS.md`, `tests/test_identity_authority.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin identity lane engineering proposal: existing_task: B03-01 bounded object/operation service implemented; no production integration claim.

### [ ] EM-134: A stale WAL snapshot can retain revoked grants

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25 identity lane build and review; session d9478f50b2b844fcb292873f9d406d3d.

An active SQLite read transaction can retain pre-revocation grants; obtaining a writer reservation before authority reads makes that stale snapshot fail closed.

**Product implication:** Do not let transaction-scoped authorization mean old snapshot authorization; accept contention denial rather than stale grant success.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** `B03-01`.
**Evidence / source record:** `docs/delivery/lane-reports/identity.md`, `docs/v2/AGENCY-ACCESS.md`, `tests/test_identity_authority.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin identity lane engineering proposal: existing_task: B03-01 same-database writer reservation and stale-WAL regression adopted; PostgreSQL remains separate.

### [ ] EM-135: Two permitted principals still cannot exchange identity mid-transaction

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25 identity lane build and review; session d9478f50b2b844fcb292873f9d406d3d.

Rechecking only that some current principal has grants can permit a transaction to begin as one actor and end as another equally permitted actor.

**Product implication:** Pin authenticated identity through the transaction so actor attribution survives reauthentication.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** `B03-01`.
**Evidence / source record:** `docs/delivery/lane-reports/identity.md`, `docs/v2/AGENCY-ACCESS.md`, `tests/test_identity_authority.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin identity lane engineering proposal: existing_task: B03-01 stable-principal transaction and rollback tests adopted.

### [ ] EM-136: Login exchange and session publication have separate cancellation boundaries

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25 identity lane build and review; session d9478f50b2b844fcb292873f9d406d3d.

A login attempt consumed before provider exchange still needs cancellation and expiry checks before publishing the returned identity session.

**Product implication:** Use one-use attempts, no uncertain exchange retry, and a post-exchange publication check; require a new explicit login after failure.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** `B03-01`.
**Evidence / source record:** `docs/delivery/lane-reports/identity.md`, `docs/v2/AGENCY-ACCESS.md`, `tests/test_oidc_login.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin identity lane engineering proposal: existing_task: B03-01 durable attempt states and post-exchange cancellation/expiry tests adopted.

### [ ] EM-137: Local logout is not provider termination or matter authority withdrawal

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25 identity lane build and review; session d9478f50b2b844fcb292873f9d406d3d.

Revoking a local opaque session neither terminates a provider account/session nor withdraws independently issued API tokens or future sign-ins.

**Product implication:** Keep local session, provider identity and current matter grants distinct in APIs and operator wording.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/identity.md`, `docs/v2/AGENCY-ACCESS.md`, `tests/test_identity_authority.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin identity lane engineering proposal: decision_record: B03-01 logout response explicitly reports provider_session_ended=false; host must separately withdraw grants/account access.

### [ ] EM-138: Offline identity fixtures cannot establish production provider or MFA trust

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25 identity lane build and review; session d9478f50b2b844fcb292873f9d406d3d.

Pinned signed-token fixtures exercise the local protocol but do not configure a real issuer, verify provider MFA/custody, establish distributed revocation or prove production row isolation.

**Product implication:** Retain explicit provider, production isolation and independent security gates even after local identity tests pass.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/identity.md`, `docs/v2/AGENCY-ACCESS.md`, `tests/test_identity_authority.py`.

**Decision history:**

- 2026-10-25 · deferred · Devin identity lane engineering proposal: existing_task: B03-01 production provider/MFA/PostgreSQL/key-custody/security-review acceptance remains external, not replaced by fixture results.

### [ ] EM-139: Expired unused login-attempt retention needs an explicit host policy

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25 identity lane build and review; session d9478f50b2b844fcb292873f9d406d3d.

Unused expired login attempts can retain their verifier until an explicit cancellation or host retention action; this lane deliberately adds no background cleanup scan.

**Product implication:** Review an explicit protected-store retention and account/session administration policy before deployment rather than silently running maintenance.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/identity.md`, `docs/v2/AGENCY-ACCESS.md`, `tests/test_identity_authority.py`.

**Decision history:**

- 2026-10-25 · candidate · Devin identity lane engineering proposal: new_candidate: retain bounded host cleanup/admin review under B03-01 without adding a daemon, new required task or production acceptance claim.

### [ ] EM-140: Frozen shipping-state fixtures can fail truthful native evidence

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** 2026-10-25 identity lane build and review; session d9478f50b2b844fcb292873f9d406d3d.

The partition changelog top entry is pushed_unreleased while native Studio hardcodes local unreleased; the builder cannot safely rewrite frozen shipping history or a shared test just to get green.

**Product implication:** Central integration must reconcile truthful shipping state and source-bound acceptance while preserving the failed experiment.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/identity.md`, `docs/v2/AGENCY-ACCESS.md`, `tests/test_identity_authority.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin identity lane engineering proposal: decision_record: record failed Studio evidence and central reconciliation request; no shared test/history edit or native pass is claimed.

### [ ] EM-233: Reference review must identify exact content without becoming fact or action authority

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** intelligence-lane-f3c5604865654b42ad08e573aa871c3e.

A new playbook or precedent version cannot inherit review of an earlier draft; a review binds the current version and digest, while author identity and factual/action approval remain separate. Controlled tests reject self-review, stale digests and review inheritance.

**Product implication:** Reusable patterns can be inspectable hypotheses without quietly approving case facts, selected courses or external actions.

**Roadmap links:** `B04-01` (partial), `B04-02` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/intelligence.md`, `tests/test_learning_knowledge.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: implement exact-version review infrastructure only. Specialist qualifications, professional approval, plan application and real outcomes still require separate evidence.

### [ ] EM-234: Withdrawal denial and terminal retirement need different source-access rules

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** intelligence-lane-f3c5604865654b42ad08e573aa871c3e.

Controlled source retraction/change/revocation tests deny reference retrieval, review and payload-idempotency replay, including historical quotes. Retirement remains available after source withdrawal so safety removal is not blocked by the source it must stop exposing. Draft quotes remain at rest; denial is not secure erasure.

**Product implication:** Current source eligibility belongs in a transaction-aware adapter. Managed retention and production deletion must not be claimed from local service filtering.

**Roadmap links:** `B04-02` (partial), `B02-14` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/intelligence.md`, `tests/test_learning_knowledge.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: keep source access fail-closed and preserve terminal retirement; defer managed retention/deletion and actual vault-policy integration to their authorised owners.
- 2026-10-25 · adopted · Devin: existing_task: final adapter/capacity checks require literal active=True, actual source text and a known nonnegative integer case revision, and permit terminal retirement beyond the normal journal cap. Truthy metadata and capacity limits must not bypass current policy or block safety removal. Controlled negative tests added; no broader source-policy/retention acceptance.

### [ ] EM-235: A model inventory listing is not a loaded or quality-approved model

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** intelligence-lane-f3c5604865654b42ad08e573aa871c3e.

Controlled runtime metadata tests distinguish exact configured weights and selected digest/size/detail fields from invalid or ambiguous inventory. Registry ports are not model tags. Invalid inventory remains unknown, and listed weights do not establish loaded state, inference or quality.

**Product implication:** The fixer needs separate readouts for connection/runtime version, verified inventory, selected weights and unperformed quality/inference checks.

**Roadmap links:** `B02-15` (partial), `ES03-04` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/intelligence.md`, `eightball/v2/runtime_status.py`, `tests/test_runtime_status.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: tighten read-only metadata contracts without model loading, silent downloads or actual-model acceptance; shared status-view wiring remains integration-owned.

### [ ] EM-236: Nested engine contracts require an explicit distribution declaration as well as source tests

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** intelligence-lane-f3c5604865654b42ad08e573aa871c3e.

The source-tree suite passes but the installed-wheel regression fails collection with ModuleNotFoundError for endstate.intelligence: the frozen root setuptools declaration includes only endstate. Source-tree success cannot prove distribution completeness.

**Product implication:** ENDSTATE's neutral contracts must be packaged and recursively fingerprinted before an integrated distribution can rely on them.

**Roadmap links:** `ES03-01` (partial), `B02-18` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/intelligence.md`, `pyproject.toml`.

**Decision history:**

- 2026-10-25 · adopted · Devin: decision_record: request integration-owned package allowlist/fingerprint changes and retain the failed wheel evidence. Do not edit a frozen manifest, skip the test or claim package acceptance.

### [ ] EM-237: Inspectable precedent can increase review burden without proving operator benefit

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-25. **Origin:** intelligence-lane-f3c5604865654b42ad08e573aa871c3e.

The implemented search is bounded lexical title/summary matching over scoped references; unreviewed precedent is excluded and empty results are scoped negatives. These deterministic checks do not show that more reference screens or reviews produce better decisions.

**Product implication:** Measure sound-decision time, missed constraints, inappropriate reuse and correction burden with qualified human judgement before claiming useful learning or success probabilities.

**Roadmap links:** `B04-03` (partial), `B04-01` (partial), `B04-02` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/intelligence.md`, `tests/test_learning_knowledge.py`.

**Decision history:**

- 2026-10-25 · deferred · Devin: existing_task: retain an owner-review hypothesis under B04-03, not a new required feature or optional B04-04 replay implementation. No human/pilot/value result is fabricated.

### [ ] EM-238: Native shipping-state assertions can fail independently of functional app preservation

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** intelligence-lane-f3c5604865654b42ad08e573aa871c3e.

The native Studio suite fails its current-build assertion at line 149 because it requires literal local unreleased while the frozen coordination changelog entry is pushed_unreleased. Eleven other native suites pass, but the complete native runner correctly remains failed.

**Product implication:** Truthful shipping state, generated changelog content and native fixture expectations must be reconciled centrally without changing state labels merely to obtain green checks.

**Roadmap links:** `B02-18` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/lane-reports/intelligence.md`, `tests/browser_studio.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin: decision_record: retain the failed Studio/native result and ask integration to reconcile exact version/shipping semantics and rerun the complete source-bound runner; no broad native acceptance.

### [ ] EM-193: Signed local audit bytes do not establish independent checkpoint custody

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** operations-2101512c.

Signing/verifying real Ed25519 checkpoints rejects altered digest, scope, revision and key, but the tool cannot verify that key or checkpoint custody is independent of the database administrator.

**Product implication:** Production audit claims require separately trusted key/checkpoint custody, rotation and external anchoring rather than an extra local hash.

**Roadmap links:** `B03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `tests/test_operations_recovery.py`, `docs/operations/2026-10-25-operations-2101512c.md`, `docs/delivery/lane-reports/operations.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: keep the signed engineering seam in B03-05 and preserve independent custody/production acceptance as explicit external gates.

### [ ] EM-194: A scoped audit checkpoint does not scope a whole-database restore

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** operations-2101512c.

The real SQLite backup/replay rehearsal verifies explicit case checkpoints including alpha import lineage, while copying every database byte; organisation/matter labels cannot turn that copy into a scoped export.

**Product implication:** Keep rehearsal host-only and fictional, require reviewed scope binding before signing, and never expose this implementation as a tenant-filtered recovery API.

**Roadmap links:** `B03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `tests/test_operations_recovery.py`, `docs/operations/2026-10-25-operations-2101512c.md`, `docs/delivery/lane-reports/operations.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: implement explicit new-file rehearsal only; managed/tenant-safe production backup and restore remain separate acceptance gates.

### [ ] EM-195: Current revocation observations are not remote revocation commands or atomicity

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** operations-2101512c.

Transactional tests show missing/unavailable surface probes cannot establish denial, close must rerun all six surfaces, and adapter failure or post-command revocation rolls back. A local transaction cannot guarantee atomic remote vault/search/worker state.

**Product implication:** Use fresh scoped probes and current authority, distinguish unavailable from denied, and require host-reviewed remote consistency rather than declaring a local journal entry globally revoked.

**Roadmap links:** `B03-05` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `tests/test_operations_journal.py`, `docs/operations/2026-10-25-operations-2101512c.md`, `docs/delivery/lane-reports/operations.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: retain fail-closed observations in B03-05 with explicit injection/remote-service gates; no cross-lane revocation command is invented.

### [ ] EM-196: Digest-matching release artifacts do not authenticate their claimed human decisions

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** operations-2101512c.

A complete source-bound artifact matrix in tests remains evidence_supplied_pending_authentication with human_decisions_authenticated and release/deploy/real-pilot authority false, even when every claimed evidence kind is present.

**Product implication:** Onboarding, legal, owner and customer acceptance require their actual authorised humans; software consistency tooling may expose gaps but cannot sign off those gates.

**Roadmap links:** `B10-01` (not_started), `B10-02` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `tests/test_operations_readiness.py`, `docs/operations/2026-10-25-operations-2101512c.md`, `docs/delivery/lane-reports/operations.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: apply consistency-only evidence handling to existing B10-01/B10-02, preserving all human/legal/customer and release gates.

### [ ] EM-197: A fictional resolution digest cannot erase the original failed pilot observation

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** operations-2101512c.

Fictional protocol tests preserve failed and unknown observations, missing dimensions and critical/high blockers. Supplying a resolution digest removes an unresolved-reference gap but does not turn the original failed observation into pass.

**Product implication:** Use an explicit later reviewed protocol/retest for closure rather than relabeling history; fictional complete observations never validate real qualified-fixer usefulness.

**Roadmap links:** `B03-06` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `tests/test_pilot_tooling.py`, `docs/operations/2026-10-25-operations-2101512c.md`, `docs/delivery/lane-reports/operations.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: build conservative fictional pilot tooling only, retaining real participants, protocol review and upstream acceptance prerequisites.

### [ ] EM-198: Confidential support metadata needs a separately controlled diagnostic narrative

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** operations-2101512c.

Strict operation schemas and sanitized probe-exception tests exclude arbitrary source text and adapter exception details while preserving opaque IDs, category, revision and evidence digests. That exclusion alone does not show that an incident can be diagnosed adequately.

**Product implication:** Keep detailed support reports in separately authorised evidence storage and measure triage/correction burden with authorised operators; do not restore sensitive free text to operational logs for convenience.

**Roadmap links:** `B10-01` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `tests/test_operations_journal.py`, `docs/operations/2026-10-25-operations-2101512c.md`, `docs/delivery/lane-reports/operations.md`.

**Decision history:**

- 2026-10-25 · adopted · Devin: existing_task: keep constrained metadata and document controlled support evidence handling. Diagnostic sufficiency remains an operator-evaluation hypothesis, not a new required product.

### [ ] EM-199: Native current-build checks conflate shipping state with runtime version

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** operations-2101512c.

The native Studio suite failed twice at current build and limits visible: the frozen partition changelog says pushed unreleased, but the existing test also demands local unreleased although the running version substring is present.

**Product implication:** Reconcile truthful branch shipping state with runtime-version assertions during shared integration; do not fake a local-only changelog state merely to obtain green native acceptance.

**Roadmap links:** `B10-02` (not_started).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/operations/verification-2101512c.json`, `docs/operations/2026-10-25-operations-2101512c.md`, `docs/delivery/lane-reports/operations.md`.

**Decision history:**

- 2026-10-25 · deferred · Devin: decision_record: preserve the exact shared-changelog native failure for integration, outside this builder's write ownership. No task acceptance or new required scope is promoted.
- 2026-10-25 · deferred · Devin: Exact committed-source native rerun reproduced the same assertion a third time. All 12 suites were attempted with provider settings stripped and runtime/canonical source unchanged; 11 passed, Studio alone failed. Preserve this failure for shared integration, not a fabricated success.

### [ ] EM-153: Vault controls need authority distinct from ordinary case WRITE

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Vault builder 2026-10-25 / session9c76974dc65748658ac94e333ea877fd.

The vault's existing WRITE grant cannot safely imply scan, lawful-hold, retention, local-deletion or audit powers. A separate current transactional control callback is required and missing control denies.

**Product implication:** Under existing B03-02, integrate explicit least-privilege control authority with current B03-01 identity/session policy rather than exposing privileged controls through the local operator token.

**Roadmap links:** `B03-02` (partial).
**Completion scope:** `B03-02`.
**Evidence / source record:** `docs/v2/VAULT.md`, `docs/delivery/lane-reports/vault.md`, `tests/test_vault.py`, `tests/test_vault_api.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin / roadmap-vault: existing_task: implemented fail-closed separate control seam and negative tests; no production role matrix, owner approval or broad gate is implied.

### [ ] EM-154: A clean scan verdict is publishable only for its exact live attempt and vault revision

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Vault builder 2026-10-25 / session9c76974dc65748658ac94e333ea877fd.

Revocation, scan cancellation and hold/retention revision changes during scanning invalidate publication even when a scanner later reports clean. Interrupted scans must not automatically resume or repeat on command replay.

**Product implication:** Keep scan claim, processing and release separate; recheck current authority and exact attempt/revision at publication, require explicit cancellation/restart and state that cancellation cannot recall bytes already supplied to a scanner.

**Roadmap links:** `B03-02` (partial).
**Completion scope:** `B03-02`.
**Evidence / source record:** `docs/v2/VAULT.md`, `docs/delivery/lane-reports/vault.md`, `tests/test_vault.py`, `tests/test_vault_api.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin / roadmap-vault: existing_task: implemented revision-bound scan publication/cancel/restart/idempotency tests within B03-02; real scanner isolation and bounded adapter execution remain integration gates.

### [ ] EM-155: Local ciphertext deletion is not proof of storage-wide or legal erasure

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Vault builder 2026-10-25 / session9c76974dc65748658ac94e333ea877fd.

Deleting a local encrypted blob can preserve an immutable descriptor and audited tombstone while leaving derived text, WAL/filesystem remnants, backups, replicas and provider retention outside its scope. Without current dependency clearance the vault must deny deletion.

**Product implication:** Label deletion local_vault_ciphertext_only, enforce hold/retention plus same-transaction dependency guard and preserve independent erasure/recovery evidence as an existing B03-02 production gate.

**Roadmap links:** `B03-02` (partial).
**Completion scope:** `B03-02`.
**Evidence / source record:** `docs/v2/VAULT.md`, `docs/delivery/lane-reports/vault.md`, `tests/test_vault.py`, `tests/test_vault_api.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin / roadmap-vault: existing_task: implemented guarded local deletion and exact scope labeling/tests, not a compliance-erasure or managed-backup claim; broader production proof remains open.

### [ ] EM-156: Reviewed source handles are references, not future publication authority

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-25. **Origin:** Vault builder 2026-10-25 / session9c76974dc65748658ac94e333ea877fd.

A source handle returned before projection publication can become stale, revoked or unavailable. The final source gate must run on the caller's same-database transaction and verify current scope, exact revision/hash, clean release and authenticated ciphertext, with audit rolled back alongside the mutation.

**Product implication:** Use Vault.require_source(db, identity=..., case_id=..., object_id=..., expected_revision=..., expected_sha256=...) immediately at final shared BEGIN IMMEDIATE commit/publish boundary; never authorize from a cached handle or separate connection.

**Roadmap links:** `B03-02` (partial).
**Completion scope:** `B03-02`.
**Evidence / source record:** `docs/v2/VAULT.md`, `docs/delivery/lane-reports/vault.md`, `tests/test_vault.py`, `tests/test_vault_api.py`.

**Decision history:**

- 2026-10-25 · adopted · Devin / roadmap-vault: existing_task: added safe metadata-only transaction gate and rollback/staleness/revocation/quarantine/ciphertext tests for B03-02 integration; collaboration wrapper agreement and cumulative integration tests remain separate.

### [ ] EM-157: Content-envelope encryption and a local audit chain do not solve metadata custody

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Vault builder 2026-10-25 / session9c76974dc65748658ac94e333ea877fd.

AES-GCM protects original bytes and authenticates their descriptor, but filenames, scope metadata and audit identifiers remain outside the content envelope. SQLite triggers/hash chains do not protect against an administrator rewriting or truncating the database and chain.

**Product implication:** Require explicit whole-storage protection, key custody, independent audit anchoring and recovery threat review before any production claim; do not relabel the local wrapper/audit chain as managed infrastructure.

**Roadmap links:** `B03-02` (partial).
**Completion scope:** `B03-02`.
**Evidence / source record:** `docs/v2/VAULT.md`, `docs/delivery/lane-reports/vault.md`, `eightball/vault/crypto.py`, `eightball/vault/schema.sql`.

**Decision history:**

- 2026-10-25 · deferred · Devin / roadmap-vault: existing_task: preserve B03-02 production security/custody/recovery gates. No external infrastructure or independent security decision was authorized; bounded local implementation states these limits rather than inventing evidence.

### [ ] EM-158: Uncertain vault command outcomes need an explicit refresh boundary

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-25. **Origin:** Vault builder 2026-10-25 / session9c76974dc65748658ac94e333ea877fd.

The isolated panel separates immutable original version from mutable vault revision and clears visible object data/disables mutations after an uncertain command outcome. Disposal/generation guards reject late responses; no automatic retry is performed. These are implemented safeguards, not browser or operator-value evidence.

**Product implication:** Integrate the panel only with host-current agency auth and dispose on session/case change; measure correction burden and safe publication/deletion decisions after native and operator testing rather than treating screen or test counts as value.

**Roadmap links:** `B03-02` (partial).
**Completion scope:** `B03-02`.
**Evidence / source record:** `docs/v2/VAULT.md`, `docs/delivery/lane-reports/vault.md`, `web/v2/vault-panel.js`.

**Decision history:**

- 2026-10-25 · adopted · Devin / roadmap-vault: existing_task: implemented a focused explicit-control UI seam under B03-02 without shared navigation changes; native/accessibility/real operator evidence remains unaccepted.

### [ ] EM-254: Module seams need current transactional identity and source policy, not only module-level green tests

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Roadmap integration / 2026-10-26.

Host integration exposed package omissions, UI lifecycle mismatch and post-claim identity exception mismatch. Corrected checks distinguish source, client disclosure, processing consent and current session.

**Product implication:** Preserve explicit server-owned adapters and negative native/transactional tests. Do not mistake engineering totals for production/operator benefit.

**Roadmap links:** `B03-01` (partial), `B03-03` (partial), `ES02-03` (partial).
**Completion scope:** `B03-01`, `B03-03`, `ES02-03`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-roadmap-integration.md`, `docs/v2/AGENCY-HOST.md`, `tests/test_agency_host.py`.

**Decision history:**

- 2026-10-26 · adopted · Devin / roadmap-integrated: existing_task: bounded shared-host engineering and explicit decision to keep missing policy external gates open; no required scope or acceptance promotion.

### [ ] EM-255: Transport envelopes are part of the supported original-size contract

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Roadmap integration / 2026-10-26.

262144 bytes encode to about349528 base64 bytes before JSON overhead; the default300000-byte middleware rejected the advertised vault maximum. Exact-path cap400000 and actual/misdeclared/oversized tests reconcile it.

**Product implication:** Keep narrowly scoped body limits and verify real transport bytes rather than only decoder limits.

**Roadmap links:** `B03-02` (partial).
**Completion scope:** `B03-02`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-roadmap-integration.md`, `docs/v2/AGENCY-HOST.md`, `tests/test_agency_host.py`.

**Decision history:**

- 2026-10-26 · adopted · Devin / roadmap-integrated: existing_task: bounded shared-host engineering and explicit decision to keep missing policy external gates open; no required scope or acceptance promotion.

### [ ] EM-256: Missing production adapters must remain unavailable across the integrated desk

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Roadmap integration / 2026-10-26.

The integrated host intentionally omits scanner, processing policy, dependent-copy deletion, processor and revocation probe implementations in JSON startup. Fictional seeded sessions/scanner/worker output exercise software controls only.

**Product implication:** Expose safe unavailable states; retain all IdP,security,professional,provider,human,pilot and commercial gates instead of treating UI controls as acceptance.

**Roadmap links:** `B03-02` (partial), `B03-05` (partial), `ES03-02` (blocked).
**Completion scope:** `B03-02`, `B03-05`, `ES03-02`.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-roadmap-integration.md`, `docs/v2/AGENCY-HOST.md`, `tests/test_agency_host.py`.

**Decision history:**

- 2026-10-26 · adopted · Devin / roadmap-integrated: existing_task: bounded shared-host engineering and explicit decision to keep missing policy external gates open; no required scope or acceptance promotion.

### [ ] EM-257: Full-source and installed-kernel regressions are independent verification contracts

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Roadmap integration / 2026-10-26.

First integrated native run passed 13 browser suites/439 checks,but source tracking failed reserved ownership and installed-wheel tests exposed three cwd-relative operations CLI paths. Corrected claims/paths then passed 1782 source and1782 installed regressions in a fresh full native run.

**Product implication:** Retain all failed exact-source runs; do not equate native browser success,focused totals or a later receipt with a complete source-bound whole-run pass. Preserve builder ownership separately from integration ownership.

**Roadmap links:** `ES01-03` (verified), `B03-05` (partial), `B10-01` (not_started), `B10-02` (not_started), `B03-06` (not_started).
**Completion scope:** `ES01-03`, `B03-05`, `B10-01`, `B10-02`, `B03-06`.
**Evidence / source record:** `docs/evidence/roadmap-integration-failed-2026-10-26.json`, `docs/evidence/roadmap-integration-native-2026-10-26.json`, `docs/delivery/sessions/2026-10-26-roadmap-integration.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / roadmap-integrated: existing_task: repair bounded integration verification contracts without weakening isolation,source manifests,production or human acceptance. No required scope or status promotion.

### [ ] EM-258: A selected model upgrade also changes request semantics and usable output budget

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Sonnet 5.5 provider follow-up / 2026-10-26.

Owner selected Sonnet 5.5 and the account catalogue lists it active. Official migration documentation rejects sampling controls and enables adaptive thinking by default; the existing transport sent temperature=0. The compatibility endpoint also documents response_format as ignored. Controlled tests now omit temperature only on direct Anthropic; there is no new-model inference evidence.

**Product implication:** Treat model selection, protocol compatibility, account entitlement, output validation and independent usefulness as separate claims. Keep the fixed token ceiling, local validation and no retry/fallback; vendor request policy belongs outside the pure ENDSTATE kernel.

**Roadmap links:** `B02-09` (blocked).
**Completion scope:** `B02-09`.
**Evidence / source record:** `docs/v2/ANTHROPIC-SETUP.md`, `docs/evidence/anthropic-selection-2026-10-26.json`, `tests/test_compatible_provider.py`, `docs/delivery/sessions/2026-10-26-sonnet-55.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / provider follow-up: existing_task: implement the owner's explicit Sonnet 5.5 selection and bounded request migration, without Opus substitution, native-adapter claim, new required scope or model acceptance.

### [ ] EM-259: A fictional fixture authorisation and token ceiling do not establish an enforced spend cap

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Anthropic failed-run preflight review / 2026-10-26.

Four Sonnet 4.6 requests were attempted before the repository-required provider-enforced US$5 cap and disabled automatic top-up were confirmed. All returned HTTP400; safe retained diagnostics omit the precise cause. A later model-catalogue HTTP200 does not establish credits, billing limits or successful inference. The omission was disclosed and further inference stopped.

**Product implication:** Make billing preflight a separate explicit gate from credentials and model selection. Preserve failed receipts without attributing an unknown error to newer model rules. No automatic retry or budget increase; a future enforceable application spend ledger remains separate engineering.

**Roadmap links:** `B02-09` (blocked).
**Completion scope:** `B02-09`.
**Evidence / source record:** `docs/evidence/anthropic-selection-2026-10-26.json`, `docs/evidence/anthropic-compatible-2026-10-26.json.xz`, `docs/delivery/sessions/2026-10-26-sonnet-55.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / provider follow-up: decision_record within existing B02-09: retain the omission/failure, hold further inference until required billing checks, and do not promote catalogue access or a token cap into model or cost acceptance.

### [ ] EM-260: All three offered specialists are native typed decision models, not chat models

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Owner-supplied Jev and GPT examples use /v1/systemone and /v1/decisions. Clef public description says native non-chat /v1/systemone while its quickstart says chat. Owner confirmed all three are decision models. A read-only authenticated catalogue listed jev-latest, clef-flash and gpt-6-luna-decisions; no inference was made.

**Product implication:** Keep Sonnet as general-purpose model. Prepare separate native typed contracts, explicit abstention and advisory-only output. Catalogue, billing, gateway routing, actual inference and purpose-specific independent quality remain distinct gates. Do not silently substitute the upstream GPT slug, bypass spending preflight or auto-execute an accept label.

**Roadmap links:** `B02-09` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/DECISION-PROVIDERS.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / source synthesis: decision_record under existing provider work: preserve the owner-confirmed native protocol; not implemented inference or quality acceptance.

### [ ] EM-261: Pinned archival copying is not a licence grant or a weight-free Git history

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Four exact pins preserve 10,843 tracked blobs, 10,840 materialized blobs and three omitted Assault checkpoint worktree files. Loomio has AGPL-3.0; HighwayEnv and semantic-router MIT; Assault has no licence file despite its README badge. Git object acquisition can include omitted blobs without loading or materializing them.

**Product implication:** Keep source archives separate from application code/runtime. Original-expression native patterns are recommended; this source-informed process is not a certified clean room. Preserve MIT notices for any substantial copy; require scoped legal review for AGPL combinations and actual permission for unlicensed source, game/media/rulebook/data/model assets. No upstream execution or dependency adoption.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/decision-projects-source-manifest.json`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-262: loomio: Preserve distinct positions with reasons, not a single agreement score

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed source:** [Consent and consensus templates](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/config/poll_templates.yml#L236-L301) distinguish consent/objection from agree/abstain/disagree/block. [Reason validation](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/stance.rb#L245-L273) can require reasons specifically for disagreement/block; [Reason input](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/vue/src/components/poll/common/stance_reason.vue#L8-L38) selects a per-option prompt. Stances carry participant identity, poll association and versioned reasons: [stance model](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/stance.rb#L65-L88).

**Product implication:** **Transferable benefit (hypothesis):** add a bounded objection/contribution view attached to an exact assumption, review criterion or course reference. Preserve the contributor's original wording, an explicit question or proposed remedy, and a separate operator disposition. Distinguish uncertainty about a claim from disagreement with a proposed course and from no response. A majority summary must not replace the minority text. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/loomio.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-263: loomio: Separate tally, closing, authored disposition and actual outcome

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed source:** [Outcome fields/history](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/outcome.rb#L57-L81) has a separate author, statement, optional poll option, latest flag and review date. [Outcome creation](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/services/outcome_service.rb#L31-L79) explicitly creates an authored record and marks older outcomes non-latest. [Outcome authority](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/ability/outcome.rb#L9-L16) permits specified people to create/update only when the poll is not active; it does not require a favourable tally. [Closing work](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/services/poll_service.rb#L481-L519) closes the poll and handles results/timeline work, not evidence of real-world success. [Outcome panel](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/vue/src/components/poll/common/outcome_panel.vue#L44-L60) displays author, statement and review due date.

**Product implication:** **Transferable benefit (hypothesis):** a human disposition can explicitly state “proceed with unresolved objection”, “revise”, “ask for evidence” or “defer”, linking the unresolved contribution IDs and reasons. Keep the case's desired/evidenced outcome vocabulary separate from a deliberation's conclusion. A closure can remain historically visible without claiming that objections disappeared. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/loomio.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-264: loomio: Borrow visible change history, not Loomio's mutable-current-row semantics

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed source:** [Stance versioning/latest scopes](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/stance.rb#L71-L88) records selected fields through PaperTrail. [Stance update](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/services/stance_service.rb#L38-L83) creates a replacement only when option scores change and either comments exist or the previous update is older than 15 minutes; otherwise it updates the current stance. [Replacement construction](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/stance.rb#L129-L137) creates a new stance but does not itself establish a predecessor-hash chain. [Poll version fields](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/poll.rb#L252-L270) tracks selected poll fields; [Poll editing](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/services/poll_service.rb#L75-L104) mutates the poll under a lock. [Version retrieval](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/controllers/api/v1/versions_controller.rb#L1-L29) exposes authorised version lookup. These are useful history mechanisms, not the same guarantee as a case-bound immutable derived journal.

**Product implication:** **Transferable benefit (hypothesis):** display a position's evolution and who changed it, but append every accepted substantive change natively with predecessor, case/assessment hash and rationale. Keep history distinct from the current projection. A case/proposal revision should make an old stance historical rather than silently count it as support for new content. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/loomio.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-265: loomio: Keep participation, access rights and execution authority separate

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed source:** [Membership](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/membership.rb#L19-L39) distinguishes active/pending/accepted/revoked membership and tracks selected changes. [Vote/export permissions](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/ability/poll.rb#L5-L27) requires login, non-deactivation, active poll, visibility, current group participation and an eligible voter record. [Stance rights](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/ability/stance.rb#L9-L42) separately gates editing one's latest stance, changing vote weight and redaction. [Locked update](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/services/stance_service.rb#L59-L68) reloads and rechecks authority under a topic lock. [Member removal](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/services/poll_service.rb#L462-L471) revokes relevant active-poll stances, optionally preserving cast votes.

**Product implication:** **Transferable benefit (hypothesis):** if actual human collaboration is later authorised, model who was invited, who could contribute, who responded, whose grant later expired, and who can publish a disposition independently. Revocation can prevent new actions without erasing an attributed historical statement. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/loomio.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-266: loomio: Make participation denominators explicit; never convert them into confidence

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed source:** [Result calculation](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/services/poll_service.rb#L552-L601) separately computes score share and electorate share and evaluates option thresholds. [Quorum/weight calculations](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/poll.rb#L620-L676) distinguishes eligible voters or issued vote weight from votes cast. [Latest/decided/undecided scopes](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/stance.rb#L80-L91) separates no response from a cast response. Important edge: result calculation defines score percent as zero when total score is zero, so the consent template's “objections <= 0%” condition can be true with no votes; this is a threshold calculation, not evidence of human consent.

**Product implication:** **Transferable benefit (hypothesis):** display counts such as “2 of 4 invited humans responded; 1 unresolved objection”, with exact population and time/revision. If only operator-authored hypothetical perspectives exist, label them contributions/viewpoints, not people surveyed. Distinguish “no objection recorded” from “consent recorded”. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/loomio.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-267: loomio: Independent-input rounds require a real server boundary; anonymity conflicts with attributed reasons

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed source:** [Result availability/visibility](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/poll.rb#L679-L687) explicitly says “until_vote” may send results to the client and is presentation-controlled, whereas “until_closed” is backend-enforced. [Visibility/anonymity invariants](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/poll.rb#L823-L859) prevents early result revelation/reopening in the relevant mode and requires anonymous polls to disable reasons. [Anonymous participation masking](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/poll.rb#L553-L601) separates masked voter relations from intentional unmasked access and limits participation visibility. [Export/electorate visibility](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/ability/poll.rb#L23-L34) authorises exports based on result availability.

**Product implication:** **Transferable benefit (hypothesis):** a future separately authorised human-review round could collect reasons before revealing others' positions, reducing exposure to prior answers. It must remain distinct from evidence independence and preserve a reviewable identity/provenance policy. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/loomio.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · deferred · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-268: loomio: Export is a separate audit/privacy product, not just a convenient CSV

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed source:** [CSV exporter](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/extras/poll_exporter.rb#L42-L99) provides poll metadata, option results, current outcome, voter identifiers, membership title/delegate/weight, times and reasons. It exports `stances.latest`, not full stance/outcome version history. [Controller](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/controllers/polls_controller.rb#L8-L21) authorises the export before sending CSV/HTML/BLT. It is useful review material, not a self-contained immutable audit package.

**Concrete source-level discrepancy:** CSV rows directly read `stance.reason` at line 93; the [latest scope](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/models/stance.rb#L80-L89) excludes revoked records but not redacted ones. By contrast, [API serializer](https://github.com/loomio/loomio/blob/24380e2131c1e43594a241814f3f460a9b0065f6/app/serializers/stance_serializer.rb#L65-L81) suppresses redacted reasons and related attachments/previews. No redaction guard appears in the inspected CSV path. **This is a source-observed policy mismatch, not a runtime-confirmed exposure or a complete security audit.**

**Product implication:** **Transferable benefit (hypothesis):** offer a readable decision packet derived from the verified native journal: exact snapshot/version, original contributions, all dispositions and predecessors, missing participants, unresolved objections and authority/evidence disclaimers. Maintain an authorised complete audit and an explicitly labelled audience projection; neither should masquerade as the other. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/loomio.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-269: highwayenv: Explicit observation projections, separate from the full state and action contract

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence.** [define_spaces](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L156-L163) builds action and observation types separately. [ObservationType](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/observation.py#L31-L55) separates space declaration, observation generation and observer identity. [KinematicsObservation configuration and projection](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/observation.py#L175-L285) selects features, bounds vehicle count, normalizes/clips, orders/pads and optionally shuffles observations. These are simulator-owned projections, not truth acquisition.

**Product implication:** **Transferable benefit — inference.** A future assumption-critique view can explicitly declare which case references, epistemic labels and fields are visible, keeping the complete snapshot separate from the bounded report/proposal. This makes information loss inspectable. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/highwayenv.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-270: highwayenv: Reproducible reset/replay manifests rather than a seed-only claim

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence.** [reset](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L221-L251) accepts seed/options, delegates seeding to Gymnasium, optionally changes config, rebuilds the scene and resets time/steps. [step and simulation cadence](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L261-L319) distinguish policy decisions from simulation frames. [paired action tests](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/tests/envs/test_actions.py#L43-L67) reset variants with seed=0 and compare equivalent action trajectories.

**Product implication:** **Transferable benefit — inference.** For derived comparisons, retain a replay envelope: snapshot hash/revision, as_of, contract/rule version, ordered overlay specifications, input references and output hash. Record a seed only if randomness actually exists; do not add randomness to a deterministic core merely to imitate an environment. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/highwayenv.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-271: highwayenv: Isolate scenario branches AND verify the exact changed set

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence.** [deep-copy preprocessors](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L380-L452) transform copied environments; [custom deepcopy](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L457-L467) excludes viewer/video wrappers. However, [set_vehicle_field](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L431-L437) iterates cloned vehicles while comparing identity with the original self.vehicle. Static inference: that guard does not exclude the cloned ego vehicle as its shape suggests. [set_preferred_lane](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L414-L422) uses a truthiness guard, making lane 0 a no-op. These were not runtime-reproduced. The [preprocessor smoke test](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/tests/envs/test_env_preprocessors.py#L9-L26) resets after transformations, then checks observation/reward bounds; it does not assert transform targeting or persistence.

**Product implication:** **Transferable benefit — inference.** Strengthen exact-target assertions, not just deep-copy assertions: allowlisted changes by stable ID, explicit zero-versus-omitted handling, independent baselines and declared approval removal. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/highwayenv.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-272: highwayenv: Keep bounded computation distinct from evidenced outcomes

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence.** [step](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L261-L287) returns terminated and truncated separately. In [HighwayEnv](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/highway_env.py#L141-L151), termination is collision/optional off-road status; truncation is elapsed duration. Important counterexample: [finite_mdp conversion](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/finite_mdp.py#L85-L97) combines collision and end-of-horizon in a single terminal array. The distinction can be lost in an adapter even when the outer API has it.

**Product implication:** **Transferable benefit — inference.** Preserve separate fields for search exhaustion, hypothetical time cutoff, unresolved external waits and evidence-backed outcome state across every report/adapter. The UI must distinguish 'not found within this search' from 'false' and from 'verified complete'. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/highwayenv.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-273: highwayenv: Action catalogue, current eligibility and authority are different contracts

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence.** [ActionType](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/action.py#L23-L70) separates space declaration, execution and available actions. [DiscreteMetaAction.get_available_actions](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/action.py#L264-L300) filters lane changes by reachability and speed changes by speed index. This is a physical eligibility projection, not permission or legal authority.

**Product implication:** **Transferable benefit — inference.** Any scenario/action view should expose separate explanations for catalogue membership, structural eligibility, evidence sufficiency, human selection and authority. Reuse readiness and command validation rather than create a second eligibility engine. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/highwayenv.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-274: highwayenv: Preserve diagnostic dimensions; do not turn a reward into confidence

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence.** [HighwayEnv reward calculation](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/highway_env.py#L100-L139) derives component rewards, then weights/normalizes them. [reward documentation](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/docs/rewards/index.md#L3-L12) explicitly avoids specifying every desirable driving behavior. [finite_mdp's description](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/finite_mdp.py#L20-L42) calls TTC cells collision probabilities under constant-speed/no-other-lane-change assumptions, while [the implementation](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/finite_mdp.py#L125-L161) assigns hard-coded 1 and 0.5 collision-point costs. No empirical calibration evidence was established by this inspection.

**Product implication:** **Transferable benefit — inference.** Use dimension-level scenario deltas: hard breaches, evidence gaps, unknown waits, resources, costs and route membership, with exact assumptions and retained objections. Ranking is a preference presentation, not a factual or normative conclusion. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/highwayenv.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-275: highwayenv: Differential contract tests plus explicit fidelity labels

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence.** [Gym API tests](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/tests/envs/test_gym.py#L49-L106) check API shape, observation-space membership, reset config and terminated/truncated behavior. [action tests](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/tests/envs/test_actions.py#L43-L67) compare seeded equivalent action configurations; [observation regressions](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/tests/envs/test_observations.py#L23-L64) check declared shape/space behavior. [timing tests](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/tests/envs/test_time.py#L18-L39) measure throughput, not semantic quality. [HighwayEnvFast](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/highway_env.py#L154-L182) changes frequency, scene size and collision checking; [simplify](https://github.com/Farama-Foundation/HighwayEnv/blob/37c84a34cadcbfc17d61acf5196a89c380a56943/highway_env/envs/common/abstract.py#L380-L395) removes distant vehicles with a stated intent to preserve optimal actions, not a proof of equivalence.

**Product implication:** **Transferable benefit — inference.** Add focused differential tests across existing adapters/reports using the same snapshot, clock, sort order and engine version; record approximation/fidelity differences if any are later introduced. Preserve source-bound failure artifacts. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/highwayenv.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-276: semantic-router: Preserve a data-only advisory routing boundary; do not revive dynamic execution

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Recommendation: adapt native boundary; reject automatic tool/action execution.**

- **Observed upstream:** [Route](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/route.py#L6-L28) holds names, utterances, descriptions, thresholds and metadata; [RouteChoice](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/schema.py#L43-L50) returns an optional name/confidence/calibrated flag. The [v1 migration guide explicitly removes dynamic routes, function schemas, direct Route calls, RouteChoice.function_call, LLM wrappers and function-call helpers](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/docs/user-guide/guides/migration-to-v1.md#L323-L332). Its [replacement example puts subsequent invocation in application code](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/docs/user-guide/guides/migration-to-v1.md#L351-L373). [DecisionRouter forms a choice question from route descriptions or up to five utterances](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/decision.py#L43-L72).

**Product implication:** **Transferable benefit—inference:** a small task-label suggestion could help an operator choose an already supported analysis purpose or provider from an allowlisted catalogue. A native envelope could retain proposed purpose, alternatives, abstention reason, source IDs, snapshot hash/revision and router-policy version. Nothing should be imported into the deterministic kernel merely to obtain this envelope. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/semantic-router.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-277: semantic-router: Make abstention explicit, and retain stronger native response validation

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Recommendation: adapt native abstention semantics; do not replace the current adapter with the generic router unchecked.**

- **Observed upstream:** [BaseRouter defaults its threshold to None](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/base.py#L74-L84). [_choose preserves raw-score ranking, accepts everything when no bar is set, and returns name=None only when no candidate passes](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/base.py#L112-L143). Per-call thresholds override route/router thresholds. [DecisionRouter._route_scores only checks for a probability dictionary, converts values with float, and fills missing route names with 0.0](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/decision.py#L59-L63); that function does not establish finite/range/sum/expected-key validity. [The calibrated flag can mean merely model.probabilistic, without fitting](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/base.py#L100-L110), via [the model flag assigned by DecisionRouter](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/decision.py#L37-L41).

**Product implication:** **Transferable benefit—inference:** standardize an explicit no-match/manual-review result across optional providers, distinguishing raw similarity, provider-reported probability, empirical route-label calibration and unavailable/error. Policy should not let a caller silently lower safety thresholds. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/semantic-router.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-278: semantic-router: Borrow held-out routing evaluation, not “decision quality” probabilities

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Recommendation: adapt evaluation design natively; defer calibrated UI claims until domain-specific evidence exists.**

- **Observed upstream:** [afit learns from the top raw score and whether its label is correct, including None labels for out-of-scope queries; FitReport ECE is calculated on that same fitting data](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/base.py#L150-L173). [Calibrator requires both correct and incorrect examples and supports Platt/isotonic maps](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/calibration.py#L1-L35). The [benchmark specifies CLINC150 intent routing and separate validation/test data](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/benchmarks/accuracy.py#L1-L16). Its [measurement code fits on validation, evaluates held-out test, measures in-scope accuracy, out-of-scope recall, ECE and a threshold curve, and tunes a threshold on validation](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/benchmarks/accuracy.py#L238-L271).

**Product implication:** **Transferable benefit—inference:** evaluate a narrowly specified routing task using operator-labelled fictional examples, out-of-scope cases, ambiguity/negation and scenario-family-disjoint splits. Report accepted-route precision, coverage/abstention, OOS false acceptance, per-label errors, latency/cost and calibration provenance—not just aggregate accuracy. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/semantic-router.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-279: semantic-router: Adapt a budgeted cascade, but do not inherit composition's confidence semantics

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Recommendation: adapt a bounded native cascade only if useful; reject pooled scores as corroboration.**

- **Observed upstream:** [Chain sends only unresolved queries to later routers](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/compose.py#L39-L64). However, its final child returns scores regardless of that child's bar (line 55); the eventual outer choice uses [BaseRouter's threshold logic](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/base.py#L112-L143) and [the first child's route catalogue exposed by Chain](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/compose.py#L23-L34). Thus the last child's threshold is not automatically the final abstention rule. [Merge asks every child concurrently, averages scores with weights, and treats missing route scores as zero](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/compose.py#L67-L112). Its calibrated flag is simply all(child.calibrated).

**Product implication:** **Transferable benefit—inference:** deterministic eligibility checks first, an optional cheap local suggestion second, then at most an explicitly authorized bounded provider stage. The wrapper should impose one end-to-end call/cost/time budget, preserve each stage's provenance and dissent, and allow no result. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/semantic-router.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-280: semantic-router: Treat dense+sparse “hybrid” as retrieval scoring—not deterministic policy checking

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Recommendation: candidate component for bounded retrieval/triage experiments; reject it as an authority or evidence validator.**

- **Observed upstream:** [IndexedRouter exposes alpha, top_k and mean/max/sum aggregation](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/indexed.py#L87-L109); [_query scales dense and sparse query components and aggregates returned utterance scores by route](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/indexed.py#L215-L238). [HybridLocalIndex adds dense and sparse similarity scores; it explicitly rejects route_filter](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/index/hybrid_local.py#L104-L133). This is not an exact-rule/semantic guardrail conjunction.

**Product implication:** **Transferable benefit—inference:** sparse terms may complement semantic paraphrases when suggesting a bounded analysis category or retrieving relevant candidate excerpts. Exact current-revision, source-membership, identifier, permission and policy checks must remain separate native vetoes. Any future retrieval suggestion must retain original excerpt IDs and exact spans, not replace evidence with vectors. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/semantic-router.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · deferred · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-281: semantic-router: Make catalogue/calibrator changes explicit and snapshot-bound; avoid mutable shared-index policy

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Recommendation: adapt immutable provenance/invalidation; defer mutable remote route catalogues and automatic refitting.**

- **Observed upstream:** [the index is IndexedRouter's source of routes; refresh updates its cache, but newly written index hits can affect queries immediately](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/indexed.py#L126-L175). An uncached route uses the router-wide threshold rather than its not-yet-loaded route threshold. [Adding a route with a fitted sparse encoder refits vocabulary and deletes/rebuilds the index](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/indexed.py#L196-L206). [add/remove invokes _refit; saved fitting queries are rescored, or calibration is dropped when they are unavailable](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/base.py#L178-L227). In contrast, [_fill/refresh only changes the cache](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/indexed.py#L144-L161), not the fitted calibrator.

**Product implication:** **Transferable benefit—inference:** give a candidate router an immutable versioned manifest covering route labels/examples, encoder/model identity, index snapshot, scoring/threshold policy and calibrator plus labelled evaluation provenance. Bind every suggestion to this manifest and the live case hash/revision. Catalogue edits should produce a new reviewed version, not silently change existing outputs. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/semantic-router.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-282: semantic-router: Account for all egress and dependency surfaces—not only the final provider call

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Recommendation: adapt native egress receipts and explicit budgets; defer package/hosted-index adoption pending a demonstrated need and separate approvals.**

- **Observed upstream:** [OpenAIEncoder sends docs to embeddings.create and may truncate first](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/encoders/openai.py#L102-L126). [PineconeRecord includes the original utterance in metadata even though its ID hashes that utterance](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/index/pinecone.py#L80-L115), then [upserts records](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/index/pinecone.py#L521-L536). [SystemOne posts state, model and questions; defaults include three retries and concurrency eight](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/decision_models/systemone.py#L20-L104). These are distinct disclosure/cost surfaces.
- **Observed configuration/dependencies:** [from_config constructs encoders/indexes and supplies routes for upsert](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/config.py#L321-L355); [IndexedRouter construction builds and refreshes the index synchronously](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/routers/indexed.py#L117-L124). Thus loading is not merely reading inert settings. [FastEmbedEncoder constructs TextEmbedding](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/encoders/fastembed.py#L20-L53); actual model acquisition/offline behavior is in a dependency not audited here. [Core dependencies include several hosted-provider SDKs, with additional local/index/provider extras](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/pyproject.toml#L9-L74). API-key fields are excluded from [the SystemOne model representation/serialization](https://github.com/aurelio-labs/semantic-router/blob/1fa1937e390fe57fb85ee3bbb8b3db593a4145db/semantic_router/decision_models/systemone.py#L34-L53), which is useful but not consent or data minimization.

**Product implication:** **Transferable benefit—inference:** an application-owned egress manifest should cover encoding of exemplars and queries, remote-index writes, decision requests, calibration/refit/evaluation and retries. Allowlisted destination/model, exact source scope, purpose, byte/token limits, retention assumptions and cancellation semantics must be explicit before any transmission. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/semantic-router.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-283: assault-ai-pilot: Observation/view separation: an important negative example

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence:** The [README service table](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/README.md#L46-L53) advertises fog of war. However, the [observation adapter](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/agents/efficientzero_v2/core/adapter_voec.py#L70-L110) copies every snapshot unit, including identity, side, coordinates, health and alive state; the [simulator snapshot](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/voec_sim/core/simulator.py#L297-L350) is built from the state units. No observer-specific visibility or redaction is apparent at these boundaries. This does not prove that every UI exposes everything; it does mean this adapter is not evidence of an enforced partial-observation boundary.

**Product implication:** **Transferable benefit:** use the observation object as a reminder to specify exactly which information a reviewer or future model may receive. Epistemic uncertainty and authorization redaction are different controls; hidden data must not merely be painted over in a UI. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/assault-ai-pilot.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-284: assault-ai-pilot: Replay: separate stored playback from deterministic recalculation

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence:** The simple [Replay container](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_sim/debug/replay.py#L1-L27) separates metadata, initial state and turns; [ReplayObserver](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_sim/debug/replay_observer.py#L5-L63) groups different event types per turn. The [benchmark serialization test](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_bench/tests/test_benchmark_replay_serialization.py#L12-L29) covers a payload containing schema version, episode index, seed and transitions—not deterministic re-execution.

**Working-contract caveats:** [replay_writer](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_sim/debug/replay_writer.py#L4-L33) permits fallback string serialization. [storage_v2](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/storage_v2.py#L11-L21) writes plain bytes under a .zst extension when compression fails. Its [manifest and row index](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/storage_v2.py#L60-L112) provide useful navigability, but those functions do not establish an immutable evidence chain or reproduction guarantee.

**Product implication:** **Transferable benefit:** an event-grouped review timeline or evidence bundle over existing immutable records, clearly distinguishing recorded observations, proposed changes, hypothetical calculations, review decisions and execution events. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/assault-ai-pilot.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-285: assault-ai-pilot: Inspector UX: navigate relevant events, not every repeated snapshot

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence:** The typed [HexInspectorData](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_ai_ui/src/components/hex/HexInspectorPopup.tsx#L5-L32) and [conditional, viewport-bounded popup rendering](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_ai_ui/src/components/hex/HexInspectorPopup.tsx#L89-L115) show a concrete contextual inspector. More transferable than its domain content is the test-specified distinction between activity and mere object presence: [replay-filter helper](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_reporting_viewer_replay_filter.py#L4-L78) intentionally excludes board-state units from activity, while [navigation tests](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_reporting_viewer_replay_filter.py#L122-L174) specify previous/next, filtered navigation and keyboard/playback reuse.

**Evidence level:** the navigation helper is test-local and several tests assert generated HTML strings. This is an intended contract/example, not observed working UI behavior or accessibility validation; the active React viewer was not run.

**Product implication:** **Transferable benefit:** a bounded “previous/next relevant change” control for an action, condition or source, exposing exact typed references, revision and whether the row is observed, inferred, hypothetical or merely reviewed. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/assault-ai-pilot.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-286: assault-ai-pilot: Per-field availability and provenance are more useful than a synthetic score

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence:** [trace-row construction](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_bench/episode_trace_row_builder.py#L202-L214) carries value/source/available information and preserves some missing values as None rather than zero. The [reporting contract](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/contracts_v2.py#L20-L61) recognizes nullable selected-value/source/availability fields. [Tests](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_contracts_v2.py#L12-L46) cover a nullable value, wrong schema and a missing required field. The viewer tests explicitly expect [N/A distinct from false](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_reporting_viewer_replay_filter.py#L95-L102).

**Product implication:** **Transferable benefit:** consistent diagnostic envelopes/UI labels for unavailable versus zero, source-derived versus inferred, stale versus current, and checked versus not checked. Useful for truthful provider/evaluation status and incomplete plan diagnostics without introducing probabilities. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/assault-ai-pilot.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-287: assault-ai-pilot: Hierarchical decomposition is only a typed-interface analogy here

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence:** The [hierarchical self-play test](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/agents/efficientzero_v2/tests/test_hierarchical_ezm_selfplay.py#L13-L74) uses a DummyAdapter; [its assertions](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/agents/efficientzero_v2/tests/test_hierarchical_ezm_selfplay.py#L80-L131) check manager/worker sample emission and target_map/mode_vector shape. This is not evidence of independent agents, useful human task decomposition or performance. The generic [plan-state normalizer](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_sim/contracts/training_contracts.py#L31-L80) carries step IDs and budgets, but also defaults missing budget state to UNBOUNDED and coerces/clamps malformed numeric input.

**Product implication:** **Transferable benefit:** only the narrow interface discipline—explicit parent/child intent, resource limits, progress ownership and typed references—for a future operator-reviewed decomposition. Human commitments remain separate from proposed contributions. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/assault-ai-pilot.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · deferred · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-288: assault-ai-pilot: Evaluation provenance: retain per-case failures and lineage, but never call it quality acceptance

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Static pinned-source observation, not an executed test: **Observed evidence:** The [evaluation manifest writer](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/storage_v2.py#L89-L112) records schema, evaluation/model/run/scenario IDs and episode indexes. The catalogue uses a [12-character SHA-1 configuration fingerprint](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/reporting/build_catalog.py#L24-L26) and attaches [parent-lineage roots and Git commit labels to histories](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/reporting/build_catalog.py#L524-L578). [Seed-level finalization](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_bench/benchmark_finalize.py#L59-L106) rejects missing per-seed/side records. Only the completeness pattern, not the military metrics, is relevant. [Catalogue tests](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_reporting_catalog.py#L6-L58) fabricate checkpoint text, manifests and a deadbeef commit tag; the [storage test](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_storage_v2.py#L10-L33) asserts file/row structure. Neither is quality evidence.

**Product implication:** **Transferable benefit:** extend native evidence navigation with explicit lineage of assessment inputs and per-case failure/missing-data drill-down; associate a provider/model/prompt only after exact identity is verified. Preserve independent reviewer provenance separately from shared-model ancestry. Existing overlap, limits, rejected/deferred implementation alternatives and unrun measurable experiments remain in the source review. No new authority, factual attestation or automatic execution follows.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/research/github-2026-10-26/assault-ai-pilot.md`, `docs/research/github-2026-10-26/synthesis.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-289: A pre-populated VM can violate an otherwise intact research-source manifest

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Four-project pinned source / provider contract review, 2026-10-26.

Four new snapshots verify. Full 32-repository verification fails five older checkouts: mem0 and Temporal nested sources initialized, Autogen LFS payload hydrated, promptfoo and Ruflo sparse model omissions absent. Existing bytes predate this copy and were preserved, not discarded. Configured public Git origins also differ from globally rewritten proxy transport URLs.

**Product implication:** Verify actual checkout invariants on every restored VM; do not assert historical source-only conditions still hold. Check the configured origin and exact pin. Preserve pre-existing bytes while reconciling the environment separately. No full-archive certification, upstream execution or model acceptance is implied.

**Roadmap links:** Candidate only; no delivery commitment.
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `research/README.md`, `research/sources.py`, `tests/test_research_copy.py`.

**Decision history:**

- 2026-10-26 · candidate · Devin / source synthesis: new_candidate or existing-task refinement from static source inspection only. Detailed risks, declined alternatives and proposed experiments are retained in the linked review. No automatic required scope, dependency adoption, code reuse or acceptance promotion.

### [ ] EM-290: Opposing advisory answers survive successful native transports

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Native review and decision-provider implementation, 26 October 2026.

Jev and GPT requested review while Clef accepted the same fictional example with missing integration evidence. Valid native answers and provider scores do not establish semantic quality or independent corroboration.

**Product implication:** Preserve disagreements and evaluate on genuinely independent cases before assigning specialist authority; no majority-to-fact rule.

**Roadmap links:** `B02-11` (partial), `B02-15` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / integration: existing_task bounded engineering refinement only; no scope, required flag or acceptance promotion.

### [ ] EM-291: An event-route toggle is not an agency-mode security boundary

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Native review and decision-provider implementation, 26 October 2026.

The first packet API test found local challenge routes registered with AgencyHost because agency_events was false there. A separate agency_mode guard now omits routes and blocks local-history agency export in both configurations.

**Product implication:** Test every supported host configuration at the server boundary, not only UI visibility.

**Roadmap links:** `B02-11` (partial), `B02-15` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / integration: existing_task bounded engineering refinement only; no scope, required flag or acceptance promotion.

### [ ] EM-292: A mutable permission set can erase evidence of revocation

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Native review and decision-provider implementation, 26 October 2026.

Rechecking the same set object can miss a policy mutation. Packet scope is frozen before projection and compared again under a same-database immediate transaction.

**Product implication:** Serialize case/history/policy changes locally and retain the downloaded-copy revocation limitation; distributed enforcement is not established.

**Roadmap links:** `B02-11` (partial), `B02-15` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / integration: existing_task bounded engineering refinement only; no scope, required flag or acceptance promotion.

### [ ] EM-293: A saved brief pointer is not a complete decision audit

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Native review and decision-provider implementation, 26 October 2026.

An initial nested predecessor lookup failed; histories now verify before projection and missing/corrupt ancestry fails closed. Both packet modes explicitly omit source documents and predecessor contents.

**Product implication:** Retain lineage pointers and explicit omissions, never claim a latest or restricted view is a full audit.

**Roadmap links:** `B02-11` (partial), `B02-15` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / integration: existing_task bounded engineering refinement only; no scope, required flag or acceptance promotion.

### [ ] EM-294: Unpreviewed operator edits must not silently save an older review

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Native review and decision-provider implementation, 26 October 2026.

The UI could let a save serialize the previous prepared brief while newly typed disposition fields were ignored. Saving now requires previewing edits and tab changes preserve the unsubmitted values.

**Product implication:** Tie saved reasoning to exactly what the operator reviewed, without transforming review labels into approvals.

**Roadmap links:** `B02-11` (partial), `B02-15` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / integration: existing_task bounded engineering refinement only; no scope, required flag or acceptance promotion.

### [ ] EM-295: Nested reusable packages need the same import-boundary check

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Native review and decision-provider implementation, 26 October 2026.

The kernel guard only walked top-level modules. It now checks nested intelligence/domain packages too, allowing pure standard-library copy/math and ENDSTATE imports but no application/runtime services.

**Product implication:** Standalone wheel smoke exercises new primitives under blocked application/provider imports; packaging is not public SDK acceptance.

**Roadmap links:** `B02-11` (partial), `B02-15` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`.

**Decision history:**

- 2026-10-26 · adopted · Devin / integration: existing_task bounded engineering refinement only; no scope, required flag or acceptance promotion.

### [ ] EM-296: A narrative-free reference index is not anonymised public data

**Disposition:** deferred. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-10-26. **Origin:** Native review and decision-provider implementation, 26 October 2026.

Even after all free text is removed, selected IDs/hashes and case/history metadata may identify or correlate sensitive records.

**Product implication:** Keep the index internal and permission checked; public sharing or stronger de-identification requires separate design and review.

**Roadmap links:** `B02-11` (partial), `B02-15` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`.

**Decision history:**

- 2026-10-26 · deferred · Devin / integration: new_candidate or deferred concern, not an automatic required task or acceptance claim.

### [ ] EM-297: A free-tier flag does not guarantee zero recorded cost

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Native review and decision-provider implementation, 26 October 2026.

The key reported free tier while Jev recorded 8547 nano-USD. Clef/GPT recorded zero; the three-call total was USD 0.000008547. Gateway preflight did not atomically pin routing or verify a hard cap.

**Product implication:** Keep exact per-request receipts and shared-budget accounting; no automatic fan-out or retries. Future coordinator budget reservations remain separate work.

**Roadmap links:** `B02-11` (partial), `B02-15` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`.

**Decision history:**

- 2026-10-26 · candidate · Devin / integration: new_candidate or deferred concern, not an automatic required task or acceptance claim.

### [ ] EM-298: Deferred dialog focus can interrupt the first edit

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Native review full-acceptance failure, 26 October 2026.

The full native run failed its empty-title validity assertion and retained a screenshot of an unintended original-title save. Dialog opening used a deferred zero-delay heading focus. A controlled regression releases delayed timers after focusing the first input; synchronous initial focus keeps the active edit intact. The corrected focused native suite passes37 checks.

**Product implication:** Treat focus scheduling as data-entry behavior, not only an accessibility decoration. Preserve failed evidence and verify invalid input has actually been entered before asserting that a form rejects it. No human accessibility certification follows.

**Roadmap links:** `B02-15` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-review-and-decisions.md`, `tests/browser_accessibility.py`, `web/v2/ui.js`.

**Decision history:**

- 2026-10-26 · adopted · Devin / integration: existing_task correction to dialog focus; no acceptance gate or required scope changed.

### [ ] EM-299: Security fixtures must restore a shared clock domain

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Owner-directed checkpoint repair, 26 October 2026.

The installed-wheel OIDC expiry test froze the service clock after a simulated expiry while the token signer used wall time. Crossing a second boundary rejected its own valid token. Restoring the original clock callable fixes the fixture without weakening authentication.

**Product implication:** Keep simulated expiry and subsequent normal operations distinct; do not add validator leeway to hide a test-clock mismatch.

**Roadmap links:** `B03-01` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-checkpoint-repair.md`, `tests/test_oidc_login.py`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: restore the original test clock; retain strict token and authority validation.

### [ ] EM-300: An errored review service is not a review verdict

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Owner-directed checkpoint repair, 26 October 2026.

The automated review for the earlier PR head reported errored, and no findings were available. Passing local tests do not turn that missing review into an independent approval.

**Product implication:** Track service availability, software checks and independent review separately; retain the failure and recheck the published source.

**Roadmap links:** `B02-18` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-checkpoint-repair.md`, `tests/test_oidc_login.py`.

**Decision history:**

- 2026-10-26 · adopted · integration: decision_record: no review or release gate is promoted by a service failure.

### [ ] EM-301: Decision transport is not an event predictor

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Forecast readiness diagnostic.

Six conditional routes contained no outcome probabilities. Working decision transports do not configure an empirical event predictor.

**Product implication:** Keep measurement, missing capability and empirical acceptance separate.

**Roadmap links:** `B02-11` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-forecast-measurement.md`, `tests/test_forecasting.py`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task evaluation refinement and decision_record; no acceptance/status promotion.

### [ ] EM-302: Missing forecasts must not manufacture perfect scores

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Forecast readiness diagnostic.

Fully abstained evaluations need null scores. Missing outcomes are not false; same-subset baselines and coverage must be reported separately.

**Product implication:** Keep measurement, missing capability and empirical acceptance separate.

**Roadmap links:** `B02-11` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-forecast-measurement.md`, `tests/test_forecasting.py`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task evaluation refinement and decision_record; no acceptance/status promotion.

### [ ] EM-303: Separate labels do not prove independent blinding

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Forecast readiness diagnostic.

The diagnostic reads separately stored labels after freezing forecasts, but its author created both. Paired hypothetical worlds do not establish representative predictive skill.

**Product implication:** Keep measurement, missing capability and empirical acceptance separate.

**Roadmap links:** `B02-11` (partial), `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-forecast-measurement.md`, `tests/test_forecasting.py`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task evaluation refinement and decision_record; no acceptance/status promotion.

### [ ] EM-304: Authority checks must bracket every call and publication

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Bounded specialist worker integration.

A multi-model processor needs authority/revision/source/lease checks between calls and in the final transaction, not only around the entire pipeline.

**Product implication:** Preserve current authority, explicit scope and missing-result limitations; validate operator value separately.

**Roadmap links:** `B03-04` (partial), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-specialist-worker.md`, `tests/test_specialist_review.py`, `docs/v2/SPECIALIST-REVIEW.md`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: current authority and stale-result refinements.

### [ ] EM-305: Processing consent binds model configuration

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Bounded specialist worker integration.

Changing models, questions or budgets after source review must invalidate processing admission.

**Product implication:** Preserve current authority, explicit scope and missing-result limitations; validate operator value separately.

**Roadmap links:** `B03-04` (partial), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-specialist-worker.md`, `tests/test_specialist_review.py`, `docs/v2/SPECIALIST-REVIEW.md`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: bind the reviewed configuration digest.

### [ ] EM-306: Reported-cost stops are not billing caps

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Bounded specialist worker integration.

A provider response can omit costs or arrive after the budget is exceeded. Unknown cost must stop subsequent calls, never mean free.

**Product implication:** Preserve current authority, explicit scope and missing-result limitations; validate operator value separately.

**Roadmap links:** `B03-04` (partial), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-specialist-worker.md`, `tests/test_specialist_review.py`, `docs/v2/SPECIALIST-REVIEW.md`.

**Decision history:**

- 2026-10-26 · adopted · integration: decision_record: retain uncertainty and disclose provider-side limits.

### [ ] EM-307: Coordinators must share the existing inference slot

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Bounded specialist worker integration.

Independent event and local-analysis slots would permit extra parallel provider requests. The application now shares one slot.

**Product implication:** Preserve current authority, explicit scope and missing-result limitations; validate operator value separately.

**Roadmap links:** `B03-04` (partial), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-specialist-worker.md`, `tests/test_specialist_review.py`, `docs/v2/SPECIALIST-REVIEW.md`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: bounded single-process coordination, no second scheduler.

### [ ] EM-308: A typed report is not yet an operator comparison experience

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Bounded specialist worker integration.

The reviewed worker retains a typed specialist report but does not yet offer dedicated model selection and readable comparison controls or measured operator benefit.

**Product implication:** Preserve current authority, explicit scope and missing-result limitations; validate operator value separately.

**Roadmap links:** `B03-04` (partial), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-specialist-worker.md`, `tests/test_specialist_review.py`, `docs/v2/SPECIALIST-REVIEW.md`.

**Decision history:**

- 2026-10-26 · candidate · integration: new_candidate: operator controls and value evaluation; do not silently promote scope.
- 2026-10-26 · candidate · integration: existing_task: read-only retained comparison improves B03-04 without adding model-selection controls; the larger candidate and measured operator value remain unaccepted. See specialist-presentation session.

### [ ] EM-309: A polished comparison must not trust duplicated summary fields

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Retained specialist presentation.

A stored aggregate can contradict its own retained model answers or case/input binding. Formatting that aggregate without reconstruction could hide disagreement behind a credible-looking comparison.

**Product implication:** Reconstruct with ENDSTATE contracts and bind the exact retained source before projecting the comparison. Preserve original output and visibly withhold an invalid presentation; no new authority or inference.

**Roadmap links:** `B03-04` (partial), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-specialist-presentation.md`, `tests/test_specialist_review.py`, `tests/browser_event_review.py`, `eightball/v2/event_reviews.py`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: fail-closed read-only projection in the existing event review. No new required product scope, model selection or quality acceptance.

### [ ] EM-310: One information check needs stable lineage across repeated reconsideration

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Owner-directed check-observe-reconsider integration.

Rechecking an immutable brief can multiply the same unresolved question unless its root declaration is stable. An answer can also remain historically recorded after its evidence is retracted; neither review disposition nor answer status establishes a condition.

**Product implication:** Reuse the existing question/observation commands with a root-brief/contribution identity and a current, explicitly labelled projection. Keep review history immutable, preserve retracted support, and require separate operator reconsideration.

**Roadmap links:** `B02-05` (verified), `ES01-02` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-information-loop.md`, `tests/test_rehearsal.py`, `tests/browser_plan_review.py`, `docs/v2/ASSUMPTION-CHALLENGE.md`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: owner requested the information-to-reconsideration loop. Reuse native questions and review contracts; do not promote optional watchers, forecasts or production acceptance. Operator benefit remains unmeasured.

### [ ] EM-311: Transport success and generation acceptance are separate gates

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Sonnet native actual-provider integration.

Native Sonnet inference succeeded after a compatibility rejection, but the first graph still failed local validation. Catalogue access and a working wire protocol do not establish valid proposals or quality.

**Product implication:** Preserve exact protocol, prompt, source and output attribution. Local contract validity, independent semantic quality and human authority remain separate.

**Roadmap links:** `B02-09` (blocked), `B02-12` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-sonnet-native.md`, `docs/evidence/sonnet-native-2026-10-26.json`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: bounded provider/prompt correction; no new required scope or independent/human/production acceptance.

### [ ] EM-312: Lexical target coverage failure is not semantic omission

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Sonnet native actual-provider integration.

The live frame contained both requested success criteria but its quotes omitted the connector and. A lexical coverage diagnostic alone does not prove a missing semantic criterion; versioned prompt guidance corrected the contract without weakening validation.

**Product implication:** Preserve exact protocol, prompt, source and output attribution. Local contract validity, independent semantic quality and human authority remain separate.

**Roadmap links:** `B02-09` (blocked), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-sonnet-native.md`, `docs/evidence/sonnet-native-2026-10-26.json`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: bounded provider/prompt correction; no new required scope or independent/human/production acceptance.

### [ ] EM-313: Partial provider counters are not complete usage totals

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** supported_by_tests.
**First recorded:** 2026-10-26. **Origin:** Sonnet native actual-provider integration.

Controlled native receipts with missing output omitted known cache use; absent cache fields could be presented as complete prompt usage. Five counterexamples reproduced the normalization error.

**Product implication:** Unknown counts must remain unknown, and known input components must be aggregated independently of output completeness. This strengthens existing receipt honesty, not billing or quality acceptance.

**Roadmap links:** `B02-09` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-native-usage.md`, `docs/evidence/native-usage-regression-before-2026-10-26.log.xz`, `tests/test_compatible_provider.py`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task: B02-09 native adapter receipt correction; no scope expansion or customer-value claim.

### [ ] EM-314: Local lifecycle finality is not remote provider finality

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Selected Sonnet lifecycle experiment.

Source-matched Sonnet configuration discarded cancelled, superseded and interrupted work without a second stage or proposal. Local admission and terminal states did not provide remote receipt, completion, cancellation or billing evidence.

**Product implication:** Show the operator that local publication has stopped without saying the remote request or charge was recalled. Reuse the existing analysis-job/provenance contract; do not add a second cancellation system.

**Roadmap links:** `B02-15` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-provider-lifecycle.md`, `docs/evidence/sonnet55-lifecycle-2026-10-26.json`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task B02-15; sharpen evidence scope without changing its acceptance or the ENDSTATE authority model.

### [ ] EM-315: Environment installation time can exhaust verification time

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** PR6 source-bound verification timeout.

The 20-minute verify job spent most of its allowance installing Chromium OS dependencies and was cancelled after acceptance began. Completed checks are not a completed run.

**Product implication:** Keep the same native gates and artifacts with a bounded 40-minute CI allowance. This is engineering infrastructure, not product quality or production-readiness evidence.

**Roadmap links:** `ES01-05` (verified).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/delivery/sessions/2026-10-26-provider-lifecycle.md`, `.github/workflows/ci.yml`, `docs/evidence/ci-verify-timeout-2026-10-26.log.xz`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task ES01-05; preserve every gate and prior failure rather than bypassing checks or claiming the timeout was a pass.

### [ ] EM-316: Freshness needs the specific changed state, not a coincidental page value

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-10-26. **Origin:** Native source-retraction acceptance failure.

The grounding test accepted the digit 2 from an unchanged deadline counter before the asynchronous reconsideration counter changed from 0 to 2. Its premature attention-filter assertion failed with no browser runtime error.

**Product implication:** Wait for the exact warning-state transition and preserve the failed native report. A generic visible number is not a fresh-data receipt; no model, authority or release gate changes.

**Roadmap links:** `B02-15` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `tests/browser_grounding.py`, `docs/evidence/sonnet55-lifecycle-software-stale-counter-2026-10-26.json.xz`, `docs/delivery/sessions/2026-10-26-provider-lifecycle.md`.

**Decision history:**

- 2026-10-26 · adopted · integration: existing_task B02-15; repair synchronization against the real native API without sleeps, fabricated responses or weakened safety assertions.
