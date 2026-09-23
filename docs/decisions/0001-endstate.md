# Decision 0001: ENDSTATE powers 8BALL

Date: 23 September 2026. Status: accepted product direction, not a completed code extraction.

## The decision

**8BALL remains the flagship fixer application and the first product to sell. ENDSTATE is the name of the reusable outcome-engineering technology underneath it.** Preferred language: “8BALL, powered by ENDSTATE” and “using our ENDSTATE engine”. ENDSTATE is not a renamed Qwen model, Jev installation, agent persona or replacement for 8BALL.

The user's intent is a top-quality fixer product whose underlying work can also power sales, customer service/success, crisis management, social-media/client management and public-office operational applications. Do not turn that intent into a plan to abandon fixers, build every vertical at once or delay the fixer product until an abstract platform is finished.

Outcome engineering is the core concept from the beginning: current evidenced state + desired state + available actions + constraints -> conditional routes, unknowns and human decisions -> observed results -> updated routes. It is not a capability that appears only at a distant V1 milestone.

## Consequences

Keep 8BALL terminology, specialist workflows, case experience and commercial focus in the product layer. Make state, provenance, goals, graph validation, planning, constraints, questions, simulations, change explanations and provider contracts reusable in ENDSTATE as the code matures. No default percentage of reuse is promised. Prove reuse with small sales/support fixtures and contract tests before claiming another product exists.

A future domain pack supplies vocabulary, schemas/mappings, approved action catalogues, policies, success evidence, prompts, integrations and presentation. The core must not hard-code a customer's sales process or a fixer's playbook. Domain-specific authority, quality evaluation and safeguards remain necessary.

The current implementation is still under `eightball/v2/`. Calling its underlying technology ENDSTATE does not claim that a standalone library, SDK, public API, persistent model runtime or cloud service already exists. Keep import paths and database semantics unchanged during this documentation change. Extract incrementally with compatibility tests; do not perform a directory-only rebrand and call it an engine release.

## Scope and authority

This decision updates product naming and future reuse architecture. It does not erase the original V0.2 PRD, excuse its failed AI-planning acceptance gate, approve main merges, authorise deployment or make confidential client data safe to use. Name choice is not trademark/domain clearance; perform commercial clearance before public launch.

The master PRD is `docs/PRD.md`. Detailed execution status belongs in `docs/delivery/progress.json` and its generated checklist. The original PRDs are preserved under `docs/reference/`.
