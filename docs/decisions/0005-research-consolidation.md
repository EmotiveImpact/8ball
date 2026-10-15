# ADR 0005: consolidate direction without interrupting V0.2

Date: 15 October 2026. Status: **accepted documentation decision under the owner's explicit request**. Implementation choices below remain proposed/deferred. Related: [ADR 0001](0001-endstate.md), [ADR 0004](0004-evidence-led-course-and-recovery.md), [START-HERE](../../START-HERE.md).

## Context and authority

The owner first asked to preserve the other chat's research until the current sprint/version was complete. They subsequently explicitly requested that the full research/strategy be integrated into permanent linked documentation on a separate branch, without replacing the original PRD, changing version gates, merging or deploying. The final request is to leave a discoverable handoff for the next agent.

This decision allows documentation consolidation now. It does not lift the runtime scope freeze, approve upstream code/data adoption or override existing production boundaries.

## Decisions

| ID | Disposition | Decision / remaining condition |
| --- | --- | --- |
| D01 | Accepted | 8BALL remains the flagship fixer application; ENDSTATE the shared outcome engine. |
| D02 | Accepted long-term vision | Include decision intelligence, operational/behavioural prediction, possible worlds, stress testing and learning. Not implemented by this ADR. |
| D03 | Accepted architectural direction | Future apps depend through reusable domain packs; Sales must not depend on 8BALL application code or fork the planner. Formal pack contracts remain future ES04 work. |
| D04 | Accepted sequencing | Finish current B02 acceptance and retain verified ES01 internal compatibility. Keep required flags, criteria, thresholds and current statuses unchanged. |
| D05 | Accepted documentation | Keep original PRDs and research byte-for-byte. Add linked supplements, current-state precedence and a single next-agent entry point. |
| D06 | Proposed design | Premise dependencies, dual frontiers, forecast/rehearsal envelopes, scenario families, client mandates and calibration records. Evaluate against existing mechanisms before implementation. |
| D07 | Deferred implementation | Simulatrex/possible-worlds adapters, multi-agent runtime, statistical/behavioural forecasting, training and a Sales/SDR production app. Require experiment and adoption gates. |
| D08 | Proposed development practice | Selectively adapt Matt Pocock/Wayfinder practices and optionally test chartr. No external skill collection/plugin installed and no competing tracker. |
| D09 | Excluded by default pending rights review | Commercial use of AlpacaDataCleaned and any code/data with unresolved licensing. The archive reports restrictions; a fresh rights check is required. |
| D10 | Not permitted | Treat synthetic outcomes as observations, simulation frequencies as calibrated probabilities, course selection as approval, or action completion as proven effect. |
| D11 | Not recovered / not implemented claim | Previously narrated Draft Repair source. Keep its report and recovery gap; do not count its old totals or silently rebuild it during scope freeze. |
| D12 | Deferred owner decision | Broader outcome envelopes, commitments, operator-attention optimisation, value of information, sustained confirmation and correction learning remain reviewable ideas, not mandatory new B02 work. |

## Reconciliation of historical ambiguity

The research register initially describes proposals; later handoff text describes accepted direction. Acceptance of ambition does not mean acceptance of a particular external implementation, benchmark or release. This distinction preserves both records without manufacturing agreement.

Old 9/20 B02 and 4/5 ES01 snapshots are historical. At the inspected current application, the sole tracker records 10/20 and 5/5 respectively. No task is advanced by this consolidation. No unsuccessful model run is hidden: the preserved 27 September baseline failed its graph step.

The uploaded research ZIP contains 19 files and its own manifest, whereas earlier archival notes refer to an 18-file variant. Preserve both provenance paths and verify the supplied variant rather than deleting a file to match an old count.

## Consequences

The next agent reads `START-HERE.md`, uses the current closeout queue for coding and the future map for architectural context. Existing PRD/roadmap text is not rewritten; append-only links direct readers to the supplements. The application and current build branch remain unchanged. There is no new product version, release, merge or deployment.

Future adoption needs an explicit decision that names the experiment/evidence, exact changed scope, new or existing task IDs, risks and acceptance requirements. A decision can be revisited, but the original finding and rationale remain visible.
