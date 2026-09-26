# Plan Studio: guided amendments, not hidden state changes

The editor is part of 8BALL V0.2 and uses the same ENDSTATE contracts and planner as existing cases. It is not a second planning engine. Open **Plan Studio** from the navigation or the relationship view.

Select a condition, action or objective. Conditions have confirmation criteria, due dates and reported actor links. Actions expose nested AND/OR, explicit true/false prerequisites, guard restrictions, intended results, approval requirement, decision option, active/wait time, time windows, resource and actor links, reversibility, possible side effects and contingency triggers/follow-up references. Objectives expose mandatory/optional status, priority and explicit success/failure predicates. Advanced JSON remains available for compatibility.

Every amendment stays in a detached, case-scoped memory draft. Undo/redo history is bounded to 30 steps. Drafts are never saved in browser storage or exported as evidence. Discard removes the draft without touching the live case. A browser reload or workspace lock clears uncommitted material; a dirty reload warns first. Removing a referenced object requires explicitly resolving its references, not silently reconnecting its neighbours.

**Preview changes** validates against the exact live command path and recomputes routes on a copy. It returns changed fields, route differences, constraint warnings and invalidated-approval count. It neither records an audit event nor attests anything. A stale case revision rejects preview. Editing anything after preview invalidates the preview. **Review & commit** is a separate human choice and uses the original revision-checked `replace_graph` command. Concurrent changes produce a conflict rather than overwriting newer work.

Observed condition titles, meanings and confirmation rules cannot be rewritten; create a new ID for a different assertion. Completed actions remain immutable. Drafts may contain temporarily invalid empty rules while being edited, but cannot pass preview or commit. Empty success criteria cannot establish resolution. A verified prerequisite is not automatically produced by moving a visual node. Graph exploration remains read-only.

The UI uses black/graphite surfaces, a condition/action library, a central editor and an explicit impact panel. On narrow screens the panels stack. Labels, keyboard-focusable controls and preserved section expansion are part of the interaction tests. Local browser tests do not constitute a full screen-reader or cross-browser audit.
