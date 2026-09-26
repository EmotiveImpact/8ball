# Owner review: what should strengthen 8BALL and ENDSTATE next?

24 September 2026. PRD revision 1.3. **Vision and specification update, not implemented product features.**

## The central insight

The product should not stop at generating possible routes. It should help a fixer retain a defensible chosen course, see what that choice depends on, and recognise when new information calls for a different decision.

**8BALL:** a live situation room for understanding a case, agreeing the mandate, selecting a course and managing its resolution.

**ENDSTATE:** reusable evidence-linked planning and reconsideration calculations. It proposes and explains; it does not inherit authority to act.

## What receives design priority

**An explicit mandate.** Clarify the intended result, hard limits, authorised concessions, proof of resolution and any separate fallback. This develops the already-recorded Outcome Envelope idea; it is not permission for the model to lower the goal.

**A human-selected course.** Keep “what the engine found” separate from “what the fixer chose”. Preserve the exact target, snapshot, dependencies and rationale. Selection must not equal execution approval.

**Reasons to reconsider.** When a reviewed update affects a dependency, guard, authority record, resource or deadline, explain that impact. New rankings do not silently change strategy, and incomplete checks cannot reassure the operator that a course is unchanged.

**Visible coverage and blind spots.** Show what source material was actually considered, what remains unresolved and how the search was bounded. “No route found in this model” is not “no solution exists”. A high-value next step may be obtaining information rather than taking an outward-facing action.

**Safe recovery.** Preserve failed drafts and human corrections as distinct records. A useful manual recovery path can make the product usable even when a model fails, but it cannot be counted as reliable unassisted generation.

**Measured operator value.** Validate whether the fixer makes a better next decision with less avoidable effort. Keep graph size, insight count and screen count out of the success definition. Prefer improving the existing workspace to adding more dashboards.

## What remains an explicitly retained candidate

A broader commitments/obligations record; outcome confirmation over a defined duration when genuinely required; permissioned replay of human corrections; and quantitative operator-attention or information-value optimisation. They remain in the register for owner review, not hidden or discarded. No automatic model training, cross-client learning or extra industry product is authorised.

## What changed in the project files

The master PRD is now revision 1.3. Separate 8BALL and ENDSTATE vision documents, an architecture decision and proposed acceptance scenarios specify the new distinctions. The roadmap adds four optional unaccepted tasks, preserving the original required gates. The existing 55 discoveries retain their text/history and ten new findings bring the register to 65. The review procedure grows from ten to fifteen prompts, with append-only protection for earlier questions.

Read `docs/delivery/EMERGENCE-REGISTER.md` for every observation and disposition, and `docs/delivery/progress.json` for delivery states. The register is not a second progress tracker.

## A delivery fact that matters

The latest available Draft Repair handoff says its completed source was not recovered. This update uses the recovered alpha.7 archive whose exact tree was reproduced. Later reported features and 905-test totals are not claimed for this earlier source. Source recovery or an explicit rebuild must precede further claims about that repair implementation.

## Immediate build order

Recover and verify the exact cumulative source; publish through an authorised workflow without overwriting newer work; run native integration; evaluate actual provider outputs against the unchanged quality gate; obtain independent operator/accessibility review. Then implement the approved next scope. Optional chosen-course contracts can be specified now, but do not displace the existing release blockers or secure agency requirements.
