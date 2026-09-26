# Sprint: Chosen Course recovery and local implementation

Date: 2026-09-25. Owner: ChatGPT. Branch: `work/chosen-course-recovery`.
Starting local comparison commit: `ba0a84a54a0e115ac35b9590c8dc41c931f3e123`; exact tree `907dc4ba85507de1ba1050e69425b3f926d611ac`.

## Recovery and scope

Recovered the alpha.7 source ZIP to exact tree `5c49a40395e6d22510a8895a90ddd2f759378efa`, then reproduced the PRD 1.3 overlay exactly. Its 862 tests passed in this session. No completed Chosen Course or Draft Repair working tree was found among the mounted deliverables; the interrupted narrative and a delivery-note Git blob were not treated as code. This implementation was rebuilt, tested and checkpointed locally from those verified bytes.

Implement optional B03-07 / ES02-06 in bounded local form: one current course, immutable selections and rationale, explicit replacement, review/pause/resume/retirement, selected prerequisite branches and current reconsideration diagnostics. Keep all original required acceptance flags/statuses and model failures. The engine is read-only and product history is separate from the factual case. The full secure mandate/team/event service remains future work.

## Observed verification

Baseline: 862 passed. Focused new suite: 64 passed. Initial focused failure clarified the distinction between an unavailable chosen action and a verification-only hypothetical remainder; an explicit diagnostic and regression now preserve that distinction. The first browser run revealed a missing insertion point in the existing room template; corrected, and 29 chosen-course checks passed through the explicit local ASGI bridge. Aggregate acceptance is run separately and its source-bound report is included in the final pack.

Native navigation was attempted without policy changes and returned `ERR_BLOCKED_BY_ADMINISTRATOR`. No native pass, live model inference, independent operator review, release or deployment is claimed. The GitHub PR was refreshed: head `824ca6421ff3100e1af596347f2d1247dde8f8dc`, draft/unmerged. No source push was made. No alternative path around prior source-write restrictions was used.

## Emergence Review

All fifteen established review prompts were considered. Preserve every existing discovery and add EM-066 through EM-071: pin chosen prerequisite branches; reconsider on clock changes without new evidence; distinguish a paused record from external cancellation; keep review acknowledgement separate from clearing warnings; distinguish unavailable work from evidence-only remainders; bind recovery claims to reproduced source. These are evidence-backed implementation findings, not market validation.

Disposition: existing_task / decision_record. Keep full B03-07 and ES02-06 partial with their original prerequisites intact. No new required gate or additional industry product. Native integration, actual-model planning, independent usefulness and secure agency operation remain open. Dependency-scoped warnings and alert fatigue require operator validation before simplifying conservative review messages.

## Handoff

Use the complete new source, not an older clone. The final pack includes a cumulative patch from the last verified remote tree, an incremental patch from the verified PRD overlay, a self-contained local Git bundle, source manifest and test artefacts. A reconstructed local Git history is not remote ancestry. Do not force-push or overwrite newer Codex work. Publish only through the authorised workflow after comparing the exact current remote. No merge or deployment.
