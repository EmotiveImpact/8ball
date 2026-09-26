# Evolving emergence register: nothing silently discarded

> Generated from `docs/delivery/emergence.json`. Decision history lives there; delivery status comes only from `progress.json`. Run `python scripts/emergence.py --write`.

8BALL remains the fixer product. ENDSTATE supplies reusable calculations. This is the build-discovery register, not a client-case insight ledger.

Last review: 2026-09-25. **71 recorded discoveries.**

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

**Roadmap links:** `ES02-04` (not_started), `ES02-05` (verified), `B02-21` (implemented), `ES02-06` (partial).
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

**Roadmap links:** `ES02-01` (not_started), `ES02-02` (not_started), `ES02-03` (not_started), `ES02-06` (partial).
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
**Evidence / source record:** `docs/v2/SOURCE-DESK.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

### [ ] EM-020: Compiler validation is not semantic correctness

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Accepted product discussion and build review.

Valid references and exact quotations can accompany an interpretation that misses the outcome.

**Product implication:** Preserve the failing real-model gates and independent semantic evaluation.

**Roadmap links:** `B02-09` (blocked), `B02-11` (partial), `ES03-02` (blocked).
**Completion scope:** `B02-11`.
**Evidence / source record:** `docs/evidence/staged-compilation-verification.json`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

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
**Evidence / source record:** `endstate/insights.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

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
**Evidence / source record:** `docs/v2/PRODUCTION-SECURITY.md`.

**Decision history:**

- 2026-09-24 · deferred · ChatGPT development proposal: Preserved for owner review. No automatic scope or completion claim.

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
**Evidence / source record:** `docs/v2/ANALYSIS-JOBS.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

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
**Evidence / source record:** `web/v2/insights-view.js`, `tests/test_insight_ui.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT development proposal: Adopt bounded scope now; wider interpretation still needs owner and operator review.

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
**Evidence / source record:** `docs/v2/PLAN-REVIEW.md`, `tests/test_plan_review.py`, `docs/evidence/route-identity-regression.json`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: The separate journal and tests preserve all case facts, revisions and approvals.

### [ ] EM-047: Independent scenario comparisons must share one baseline

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Plan Review sprint and reproducible structural fixtures.

A zero-budget scenario followed by a restored-budget scenario must not retain disabled actions or assumptions from the preceding experiment.

**Product implication:** Copy the same input for each explicit scenario and label independent versus combined experiments.

**Roadmap links:** `B02-05` (verified), `B02-11` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/v2/PLAN-REVIEW.md`, `tests/test_plan_review.py`, `docs/evidence/route-identity-regression.json`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Read-only copies and regression tests prevent accumulating hypothetical changes.

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
**Evidence / source record:** `scripts/acceptance.py`, `tests/test_acceptance_runner.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.

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

**Roadmap links:** `B02-16` (partial).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `web/v2/ui.js`, `tests/browser_accessibility.py`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.

### [ ] EM-054: Scripted real-model review is not independent judgement

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Integration and acceptance sprint.

An actual-inference integration script can exercise approvals and evidence mechanics while still using developer-authored reviewer choices.

**Product implication:** Label these choices and synthetic observations explicitly; do not use them to close independent quality or all-native human acceptance.

**Roadmap links:** `B02-11` (partial), `B02-12` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `evals/full_journey.py`, `docs/v2/ACCEPTANCE-RUNNER.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.

### [ ] EM-055: Available, called, correct, integrated and released are separate gates

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** observed_in_build.
**First recorded:** 2026-09-24. **Origin:** Integration and acceptance sprint.

A configured provider can be unreachable; a valid model response can be semantically wrong; a passing local build can be unpushed and undeployed.

**Product implication:** Keep availability, invocation, model quality, browser transport and release status separate, including failures and zero-call preflights.

**Roadmap links:** `B02-12` (blocked), `B02-15` (partial), `B02-18` (blocked), `ES03-08` (blocked).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `scripts/acceptance.py`, `evals/full_journey.py`, `docs/delivery/sessions/2026-09-24-integration-acceptance-local.md`, `docs/decisions/0004-evidence-led-course-and-recovery.md`, `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT build review: Bounded existing-task improvement; implementation does not imply that wider model/native/release acceptance has passed.
- 2026-09-24 · adopted · ChatGPT vision refinement: A narrated test total without its recoverable implementation is not current-source evidence. Preserve the missing-source caveat as well as native/model/publication states.

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

**Roadmap links:** `ES02-06` (partial), `B03-07` (partial), `ES02-04` (not_started).
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
**Evidence / source record:** `docs/reference/2026-09-24-draft-repair-delivery-record.md`, `docs/vision/ENDSTATE.md`, `docs/vision/ACCEPTANCE-DESIGN.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT documentation review: Adopt the bounded design direction, not runtime completion. Owner review and the listed acceptance work remain open.

### [ ] EM-061: The primary value test is a better decision, not a larger graph

**Disposition:** adopted. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

The cumulative workspace has more inspection and review surfaces. It is not yet independently established whether that makes a fixer faster, more accurate or simply busier.

**Product implication:** Measure correct next decisions, missed dependencies, false alarms and correction/review burden. Prefer progressive disclosure in the existing room over more dashboards.

**Roadmap links:** `B04-03` (not_started), `B02-22` (not_started), `B04-04` (deferred).
**Completion scope:** No scoped completion gate yet; do not tick this idea off.
**Evidence / source record:** `docs/vision/8BALL.md`, `evals/PLAN-QUALITY-GATE.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT documentation review: Adopt the bounded design direction, not runtime completion. Owner review and the listed acceptance work remain open.

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
**Evidence / source record:** `docs/vision/ENDSTATE.md`, `docs/vision/8BALL.md`.

**Decision history:**

- 2026-09-24 · candidate · ChatGPT documentation review: Retained for owner review; no new mandatory scope or implementation claim.

### [ ] EM-064: Some outcomes need evidence over a declared confirmation window

**Disposition:** candidate. **Owner review:** pending. **Original evidence level:** operator_hypothesis.
**First recorded:** 2026-09-24. **Origin:** Vision/source-recovery review of the available alpha.7 checkpoint.

A single successful check can satisfy a present-state condition without establishing a requested period of sustained recovery. Not every outcome requires such a period.

**Product implication:** Explore explicit outcome confirmation windows with the operator and preserve unknown timing. Do not add hidden universal stability periods or autonomous monitoring.

**Roadmap links:** `B03-07` (partial), `ES02-04` (not_started), `ES02-06` (partial).
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
**Evidence / source record:** `scripts/emergence.py`, `tests/test_emergence_register.py`, `docs/delivery/sessions/2026-09-24-vision-strengthening.md`.

**Decision history:**

- 2026-09-24 · adopted · ChatGPT regression review: Bounded documentation-tooling fix. Original ten passes remain mandatory and previously recorded protocol entries become append-only. No runtime or model-quality acceptance follows.

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
**Evidence / source record:** `docs/delivery/sessions/2026-09-25-chosen-course-recovery.md`.

**Decision history:**

- 2026-09-25 · adopted · ChatGPT build review: Adopt in the bounded local implementation and reproducible delivery; wider secure/native/operator acceptance remains unverified.
