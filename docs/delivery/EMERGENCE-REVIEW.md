# End-of-sprint emergence review

This review is mandatory at the end of every substantive 8BALL / ENDSTATE build sprint. It exists to catch capabilities, risks and product directions that only become visible after real implementation. It is **not** permission to expand scope automatically.

## The question we always ask

> **What did this sprint reveal that we had not properly seen, specified or understood before we built it?**

Answer it before the sprint handoff is considered complete.

## Required review

For each sprint, record:

1. **New capability or opportunity** — what became possible or strategically clearer because of the build?
2. **New risk or failure mode** — what did implementation expose that the PRD did not make explicit enough?
3. **Architecture implication** — does this reveal a reusable ENDSTATE primitive, a domain-specific 8BALL concern, or neither?
4. **UX / operator implication** — does the fixer need a new way to see, review, control or understand this?
5. **Roadmap decision** — classify each finding as one of:
   - `existing_task` — already covered; link the task ID and sharpen its next action if needed.
   - `new_candidate` — record as a hypothesis/candidate; do not silently promote it to required scope.
   - `new_required_task` — create a stable task only when the product decision is explicit.
   - `decision_record` — architectural/product choice that needs a decision note.
   - `no_action` — interesting, but not worth changing the roadmap.
6. **Evidence level** — say whether the finding is `observed_in_build`, `supported_by_tests`, `operator_hypothesis`, or `market_hypothesis`.

Every new changelog entry must include an `emergence_review` object. The build-history validator enforces this for entries added after this rule was introduced.

## Current discoveries from the V0.2 build

These are the first captured findings. They are not all new roadmap commitments.

### 1. We are really maintaining two linked graphs

**Observed in build.** Source Desk and Connections describe **what appears to be true and why**. Plan Studio and Find a Way Through describe **what must become true and how**. Treating these as one undifferentiated graph would make evidence, assumptions and intended effects easy to confuse.

**Implication:** preserve a clear boundary between the **reality / provenance graph** and the **outcome / action graph**, with explicit links between them. This reinforces existing B02 and ENDSTATE contracts rather than creating a new product.

### 2. Information acquisition is itself part of the plan

**Observed in build.** Many of the most valuable next moves are not external execution actions; they are actions to resolve uncertainty: obtain a document, confirm authority, verify a deadline, ask a stakeholder, or reconcile conflicting sources.

**Implication:** evaluate a future distinction between **knowledge actions** and **world-changing actions**. For now this belongs under question priority, source review and route planning; do not invent another subsystem yet.

### 3. Freshness matters almost as much as truth

**Observed in build.** In a changing situation, a statement may have been supported and still become operationally stale. Source versioning and What Changed make this visible.

**Implication:** ENDSTATE V0.2 event-driven replanning should explicitly consider observation time, supersession, expiry / freshness and trigger conditions. A condition should not remain operationally trusted merely because it was true once.

### 4. A plan needs watch conditions, not only next actions

**Observed in build.** The useful question is increasingly: “what new event would make us change this route?” The current Watch briefing hints at this, but machine-readable replan triggers are not yet a first-class contract.

**Implication:** treat this as an ENDSTATE V0.2 design candidate under event-driven replanning, not a V0.2 release blocker unless the roadmap is explicitly amended.

### 5. Operator attention is a constrained resource

**Operator hypothesis grounded in the UI build.** Route quality is affected by how many reviews, decisions and context switches a human must perform, not only time and cost.

**Implication:** investigate an **operator-load** measure later. Do not turn it into a fake optimisation score before pilot evidence exists.

### 6. Desired outcomes may need an acceptable envelope, not one perfect end state

**Product hypothesis.** Fixers often have an ideal state, a minimum acceptable resolution and explicit failure / walk-away conditions. Multi-objectives and failure criteria already give us some of this structure.

**Implication:** evaluate whether the existing objective model is sufficient before adding a separate “Outcome Envelope” concept. No roadmap expansion yet.

## Promotion rule

Emergent insight is valuable precisely because it can change the product, but every idea does **not** become scope. A finding only changes the accepted roadmap when it has an explicit owner/product decision and is entered in the canonical ledger. Until then it stays an evidence-labelled hypothesis in the sprint record.

## Evolving register and owner review (current rule)

The six discoveries above are the **first captured snapshot**, not the complete evolving list. All earlier product-insight ideas and current discoveries are consolidated in [EMERGENCE-REGISTER.md](EMERGENCE-REGISTER.md), generated from `emergence.json`. Preserve every identified idea, including recommendations not to build it. Do not remove entries to improve a completion count. The owner must be able to see what the developer deferred and why.

Use the full prompt sequence in `docs/prompts/EMERGENT-INSIGHTS.md`. For each discovery, record original wording, source/evidence level, 8BALL/ENDSTATE implication, adoption/candidate/defer/decline/supersede decision, rationale, roadmap links and owner-review state. Decision history is append-only. `[x]` is derived from verified acceptance tasks, not an idea being interesting; strikethrough retains declined or superseded entries for review. Every new changelog entry links the relevant `EM-nnn` IDs. If the sprint exposes no new insight, say so explicitly and link the existing findings reviewed; do not manufacture discoveries to fill the template.

The in-product Emergent Insights ledger concerns **client situations**, and is separate from this build register. The application can show both to the current local operator, but neither is part of a public client brief. Future role-based deployment must retain that separation.

## Additional review lenses, not new automatic runtime features

Read `docs/vision/8BALL.md` and `docs/vision/ENDSTATE.md`. The register now also asks about the human-selected course and its reconsideration trigger, unprocessed inputs and bounded conclusions, safe failure recovery, recoverable delivery evidence and measurable operator benefit (ER-11 through ER-15).

Record which findings refine existing entries before adding a new one. Preserve candidates and declined ideas; adoption as a design priority does not clear any runtime gate. A screenshot, an unrecovered archive or an unverified test-count statement cannot supply a feature-completion tick.
