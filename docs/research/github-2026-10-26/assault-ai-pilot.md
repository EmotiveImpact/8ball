<!-- Source inspection only; upstream code was not executed. -->

# Bounded source-mining result

**Verdict:** useful reference ideas for truthful inspection and evaluation provenance; not a candidate runtime dependency. Four focused native adaptations are worth considering, one boundary design is a negative example, and the learned hierarchy should be deferred/rejected for this product. No benefit has been experimentally established.

Upstream source is pinned to **0284a559d8bc3c7a15dfb0bf4fa42278242d60e9**. ENDSTATE comparisons use **4f31c6b40141990d0863d9375f47a7ad51863dfc**, not the parent's unpublished Assumption Challenge Brief. Existing inspect_plan, simulate, Insights, Plan Review and Chosen Course are the baseline—not missing capabilities. Recommendations below are proposals, not implementation or accepted roadmap scope. All experiments below are proposed and were **not run**.

## 1. Observation/view separation: an important negative example

**Observed evidence:** The [README service table](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/README.md#L46-L53) advertises fog of war. However, the [observation adapter](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/agents/efficientzero_v2/core/adapter_voec.py#L70-L110) copies every snapshot unit, including identity, side, coordinates, health and alive state; the [simulator snapshot](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/voec_sim/core/simulator.py#L297-L350) is built from the state units. No observer-specific visibility or redaction is apparent at these boundaries. This does not prove that every UI exposes everything; it does mean this adapter is not evidence of an enforced partial-observation boundary.

**Existing overlap:** ENDSTATE already derives unknown/disputed/true/false from reviewed observations in [condition_states](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/endstate/state.py#L7-L18). The application already has a substantially stronger client projection boundary: recipient/review/grant checks and a deliberate output allowlist in [client_read](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/eightball/projections/service.py#L164-L188).

**Transferable benefit:** use the observation object as a reminder to specify exactly which information a reviewer or future model may receive. Epistemic uncertainty and authorization redaction are different controls; hidden data must not merely be painted over in a UI.

**Limits/rights:** a full-state simulation observation is not a suitable confidential-case projection. No proof of learned partial-observation handling or privacy is supplied by the inspected tests. Upstream code-copy permission is unresolved.

**Recommendation: reject** this observation mapping as a knowledge/access boundary; adapt native, allowlisted view tests around existing ENDSTATE/application contracts instead.

**Acceptance experiment:** twelve synthetic paired views differing only in restricted records or their identifiers; assert zero restricted-field/identifier leakage in serialized payloads and equality of permitted outputs under hidden-data perturbations. Preserve unknown versus explicitly false in all twelve, and perform no live case write.

## 2. Replay: separate stored playback from deterministic recalculation

**Observed evidence:** The simple [Replay container](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_sim/debug/replay.py#L1-L27) separates metadata, initial state and turns; [ReplayObserver](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_sim/debug/replay_observer.py#L5-L63) groups different event types per turn. The [benchmark serialization test](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_bench/tests/test_benchmark_replay_serialization.py#L12-L29) covers a payload containing schema version, episode index, seed and transitions—not deterministic re-execution.

**Working-contract caveats:** [replay_writer](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_sim/debug/replay_writer.py#L4-L33) permits fallback string serialization. [storage_v2](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/storage_v2.py#L11-L21) writes plain bytes under a .zst extension when compression fails. Its [manifest and row index](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/storage_v2.py#L60-L112) provide useful navigability, but those functions do not establish an immutable evidence chain or reproduction guarantee.

**Existing overlap:** Chosen Course already preserves a detached snapshot, explicit clock and exact route; [verify_anchor](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/endstate/course.py#L90-L112) recalculates and rejects a route that does not reproduce. Plan Review [binds assessment to case revision and SHA-256](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/eightball/v2/plan_review.py#L68-L76).

**Transferable benefit:** an event-grouped review timeline or evidence bundle over existing immutable records, clearly distinguishing recorded observations, proposed changes, hypothetical calculations, review decisions and execution events.

**Limits/rights:** a seed and JSON round trip do not prove deterministic reproduction; display replay must not replay commands against live state. Lossy serializers and misleading file extensions are unsuitable evidence behavior. Rights are unresolved; do not copy the writer.

**Recommendation: adapt native**, leveraging existing snapshot/hash/course verification rather than importing replay infrastructure.

**Acceptance experiment:** ten small neutral fixtures exported and re-read at a fixed as_of and schema version must reproduce canonical calculation outputs; five corruption cases (changed snapshot, clock, event order, schema and missing row) must fail visibly. Database/evidence/approval digests must remain unchanged.

## 3. Inspector UX: navigate relevant events, not every repeated snapshot

**Observed evidence:** The typed [HexInspectorData](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_ai_ui/src/components/hex/HexInspectorPopup.tsx#L5-L32) and [conditional, viewport-bounded popup rendering](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_ai_ui/src/components/hex/HexInspectorPopup.tsx#L89-L115) show a concrete contextual inspector. More transferable than its domain content is the test-specified distinction between activity and mere object presence: [replay-filter helper](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_reporting_viewer_replay_filter.py#L4-L78) intentionally excludes board-state units from activity, while [navigation tests](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_reporting_viewer_replay_filter.py#L122-L174) specify previous/next, filtered navigation and keyboard/playback reuse.

**Evidence level:** the navigation helper is test-local and several tests assert generated HTML strings. This is an intended contract/example, not observed working UI behavior or accessibility validation; the active React viewer was not run.

**Existing overlap:** 8BALL already previews referenced records and evidence and shows snapshot-bound historical review state in [Plan Review UI](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/web/v2/plan-review-view.js#L20-L30), which preserves the key separation: review cannot verify facts or approve actions. Existing graph/Insights/What Changed surfaces should be extended, not replaced.

**Transferable benefit:** a bounded “previous/next relevant change” control for an action, condition or source, exposing exact typed references, revision and whether the row is observed, inferred, hypothetical or merely reviewed.

**Limits/rights:** substring matching in action IDs and compatibility aliases are not suitable as ENDSTATE's authoritative typed links. Source excerpts may be sensitive. Tactical data, maps and art are outside scope and have unresolved rights; keep only the nonmilitary UX idea.

**Recommendation: adapt native** in the current 8BALL inspector/history surfaces, not a new simulator interface.

**Acceptance experiment:** a twenty-event synthetic timeline with three referenced objects and repeated unchanged snapshots must return exactly the expected relevant event indexes per object, with identical keyboard and button navigation. Inspection must cause zero writes or approval changes; no filter may suppress contradictory evidence belonging to that object.

## 4. Per-field availability and provenance are more useful than a synthetic score

**Observed evidence:** [trace-row construction](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_bench/episode_trace_row_builder.py#L202-L214) carries value/source/available information and preserves some missing values as None rather than zero. The [reporting contract](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/contracts_v2.py#L20-L61) recognizes nullable selected-value/source/availability fields. [Tests](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_contracts_v2.py#L12-L46) cover a nullable value, wrong schema and a missing required field. The viewer tests explicitly expect [N/A distinct from false](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_reporting_viewer_replay_filter.py#L95-L102).

**Existing overlap:** ENDSTATE already has explicit four-state condition status and source/observation IDs in [state derivation](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/endstate/state.py#L7-L18); [Plan Review output](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/endstate/plan_review.py#L154-L159) refuses semantic verification or execution authority.

**Transferable benefit:** consistent diagnostic envelopes/UI labels for unavailable versus zero, source-derived versus inferred, stale versus current, and checked versus not checked. Useful for truthful provider/evaluation status and incomplete plan diagnostics without introducing probabilities.

**Limits/rights:** the inspected validator checks presence/nullability but does not enforce all field types or consistency of value/source/available. Its score semantics are not transferable quality or success probabilities. Code rights unresolved; use native types and existing factual states.

**Recommendation: adapt native**, as a contract-consistency improvement only; do not add a universal plan score.

**Acceptance experiment:** a fixed matrix covering absent, null, false, numeric zero, disputed, stale and unavailable data must round-trip without conflation. Contradictory availability/source combinations must be rejected. All displays and exports must agree, with zero inference-success or semantic-acceptance flags created from metadata alone.

## 5. Hierarchical decomposition is only a typed-interface analogy here

**Observed evidence:** The [hierarchical self-play test](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/agents/efficientzero_v2/tests/test_hierarchical_ezm_selfplay.py#L13-L74) uses a DummyAdapter; [its assertions](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/agents/efficientzero_v2/tests/test_hierarchical_ezm_selfplay.py#L80-L131) check manager/worker sample emission and target_map/mode_vector shape. This is not evidence of independent agents, useful human task decomposition or performance. The generic [plan-state normalizer](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_sim/contracts/training_contracts.py#L31-L80) carries step IDs and budgets, but also defaults missing budget state to UNBOUNDED and coerces/clamps malformed numeric input.

**Existing overlap:** ENDSTATE already expresses owner, purpose, requirements, guards, effects, resources, decisions and approvals in [Action](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/endstate/contracts.py#L135-L168). Existing [simulate](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/eightball/v2/services.py#L15-L54) enforces explicit hypothetical booleans, checks revision and references, strips approvals and returns persisted=false. A worker hierarchy is not needed to obtain bounded what-if comparison.

**Transferable benefit:** only the narrow interface discipline—explicit parent/child intent, resource limits, progress ownership and typed references—for a future operator-reviewed decomposition. Human commitments remain separate from proposed contributions.

**Limits/rights:** learned control and self-play are not an appropriate route to ENDSTATE's human authority model. Permissive UNBOUNDED/zero defaults could hide missing constraints. No tactical/combat optimization was evaluated. Model assets/code licensing is unresolved.

**Recommendation: defer** new hierarchical runtime/dependencies; reject combat/RL components. If owner later wants native decomposition metadata, extend current contracts and the separately unvalidated parent brief rather than creating a second planner or an agent swarm.

**Acceptance experiment:** offline fixtures at the parent's stated 4-perspective/12-contribution/3-overlay bounds, plus one over-limit fixture for each bound; require exact revision/hash matching and complete parent/reference attribution, reject stale/orphan/over-limit input, preserve dissent and produce zero live evidence/approval/action changes. This would validate only a proposed native contract, not model intelligence.

## 6. Evaluation provenance: retain per-case failures and lineage, but never call it quality acceptance

**Observed evidence:** The [evaluation manifest writer](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/storage_v2.py#L89-L112) records schema, evaluation/model/run/scenario IDs and episode indexes. The catalogue uses a [12-character SHA-1 configuration fingerprint](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/reporting/build_catalog.py#L24-L26) and attaches [parent-lineage roots and Git commit labels to histories](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/reporting/build_catalog.py#L524-L578). [Seed-level finalization](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_bench/benchmark_finalize.py#L59-L106) rejects missing per-seed/side records. Only the completeness pattern, not the military metrics, is relevant. [Catalogue tests](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_reporting_catalog.py#L6-L58) fabricate checkpoint text, manifests and a deadbeef commit tag; the [storage test](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/mlops/tests/test_storage_v2.py#L10-L33) asserts file/row structure. Neither is quality evidence.

**Existing overlap:** 8BALL's [acceptance inspection](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/scripts/acceptance.py#L210-L257) already validates source/artifact hashes, suite completeness, statuses and transport while returning model_quality_approved=false and released=false. [PRD acceptance requirements](https://github.com/EmotiveImpact/8ball/blob/4f31c6b40141990d0863d9375f47a7ad51863dfc/docs/PRD.md#L145-L151) already require held-out professional evaluation and preservation of failures. No replacement harness is needed.

**Transferable benefit:** extend native evidence navigation with explicit lineage of assessment inputs and per-case failure/missing-data drill-down; associate a provider/model/prompt only after exact identity is verified. Preserve independent reviewer provenance separately from shared-model ancestry.

**Limits/rights:** a source-commit string is not verification against bytes; truncated SHA-1 is a grouping fingerprint, not an integrity mechanism. A complete run, a synthetic PASS field, agreement between related runs or a model lineage is not independent corroboration. No live endpoints or unverified model aliases were researched. Code-copy permission unresolved.

**Recommendation: adapt native**, reusing the existing acceptance and review architecture. Defer any MLOps component/dependency selection until measured need and rights review.

**Acceptance experiment:** two offline synthetic evaluation bundles, one complete and one failed/incomplete, with five tamper/missing-artifact variants. Require complete per-case traceability and rejection/explicit incompleteness for all variants; retain failed rows and require exact snapshot/source/rubric/prompt identities. No code-only or related-model fixture may yield inference-success, independent-quality, release or execution authorization.

## Licence and copy limits

At the exact pinned tree, a filename inventory of all 5,250 entries found no conventionally named LICENSE, LICENCE, NOTICE, COPYING or COPYRIGHT file. The [README:214–217](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/README.md#L214-L217) advertises MIT via a LICENSE link that has no corresponding file in this tree, and separately says original game trademarks/card layouts/counter art belong to their creators. This is an unresolved permission gap, not a finding that MIT has been established. GitHub's no-license metadata was supplied in the task; I did not independently query it.

The [asset section](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/README.md#L116-L126) claims digitized official physical-game assets. The tree includes [rulebook chunks](https://github.com/richardcc/assault-ai-pilot/blob/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_rag/data/rulebook/chunks/rulebook_chunks.json), [compiled UI art](https://github.com/richardcc/assault-ai-pilot/tree/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/assault_ai_ui/dist/assets), and [legacy checkpoints](https://github.com/richardcc/assault-ai-pilot/tree/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9/legacy_archive/checkpoints). Ownership attribution is not a redistribution, RAG-use, training or derivative-content license. Exact rights for rulebook text, extracted rules/data, cards, counters, dice, maps, third-party bundled distribution assets and checkpoint weights/training material were not established. Dependency and bundled-asset license compatibility was not exhaustively audited.

Three tracked checkpoint entries were identified by Git metadata only: ppo_US.pt (24,383 bytes), ppo_US_phase01.pt (39,919), and ppo_US_phase01_HRL.pt (24,615). They were not materialized, read, loaded or run. Preserve these exclusions explicitly in any parent archive; do not assume a Git-only copy excludes tracked binary blobs.

No upstream code, assets, weights or rulebook material should be incorporated into application code or redistributed as licensed software on this evidence. Parent's authorized research-only preservation is not a licensing opinion or dependency approval. Prefer independently authored native implementations of the general ideas; obtain owner/legal clarification of exact software license, notices and content/weight rights before any code-copy or component proposal.

## Integration recommendations

Priority 1: low-risk native truthfulness improvements—consistent availability/provenance labels and reference-specific history navigation over existing Plan Review/Insights/Source Desk/Chosen Course data. Priority 2: a small read-only evidence/replay bundle that reuses existing exact snapshots, explicit clocks, SHA-256 digests and fail-closed verification; do not build a second audit system. Priority 3: per-case evaluation lineage and failed-case navigation within the existing acceptance/evaluation boundary, not a new MLOps stack.

Reject the full-state adapter as a confidential or partial-knowledge boundary; preserve native allowlisted projections and unknown/disputed semantics. Defer new hierarchical execution and all imported services, RL/models/weights, simulation engines, tactical components and UI assets. None of the inspected code is recommended as a directly adoptable component while permission and fit remain unresolved. No new app, agent swarm, autonomous execution or provider migration is proposed.

8BALL remains the flagship fixer UI; ENDSTATE remains the deterministic, reusable calculation/contracts layer. Models may propose; humans commit; review, chosen course, approval, completion and evidenced effects remain separate. The parent's <=4 perspectives / <=12 contributions / <=3 overlays Assumption Challenge Brief is reported WIP outside the baseline and has not been inspected or validated here. These findings should be considered against it without claiming it already satisfies them. All implementation, canonical EM/task assignment and scope decisions remain with the parent/owner.

## Emergence findings

Recommended parent dispositions (not canonical ledger entries):
1. decision_record — README fog-of-war language is not proof of an information boundary. Inspected full-state observation code and existing ENDSTATE client projection code make the mismatch concrete. Keep permissions/redaction distinct from epistemic unknowns; reject direct mapping adoption.
2. new_candidate — Event-focused history navigation can reduce reviewer effort without changing planner semantics. Evidence is a typed popup plus test-local navigation contracts/static HTML assertions, not a successful browser experiment.
3. new_candidate — Truthful value/source/availability labeling is a better immediate transfer than any score. Upstream's 'strict' contract checks presence/nullability but does not establish all type/consistency invariants; native validation should remain stronger.
4. decision_record — Playback, a JSON round trip and seed metadata are not reproducible calculation. Silent string conversion and plain bytes under a .zst name reveal why evidence ingestion should fail visibly and identify its actual encoding.
5. existing_task — ENDSTATE already has exact-snapshot review and Chosen Course reproduction; upstream replay/evaluation ideas should extend those, not be misreported as missing fundamentals or create a competing ledger.
6. decision_record — Model hierarchy tests demonstrate mock-backed output structure, not useful delegated judgement. Do not adopt learned/combat execution; retain only the optional typed-interface analogy. UNBOUNDED/zero coercion is particularly unsuitable for unknown human constraints.
7. existing_task — Keep source/build evidence, actual inference and independent professional acceptance separate. Synthetic catalogue fixtures and shared lineage do not satisfy semantic quality gates or corroboration.
8. decision_record — Missing license text plus explicitly third-party game assets makes copying materially riskier than the README badge suggests. Rulebook and weight rights require separate treatment.
9. no_action — The README's 'production-grade' label was not verified and is not a selection criterion. No stars, marketing claim or mock test was used to rank model quality.
10. decision_record — Git-only preservation is not automatically weight-free: three tracked .pt entries were found. Parent should record their omission/exclusion and not claim that avoiding LFS alone excludes all model artifacts.

These are source-grounded observations and proposed dispositions. No discovery was promoted into required scope or recorded as implemented, professionally accepted or released.

## Inspection limits

Bounded static inspection only. Inspected exact upstream commit 0284a559d8bc3c7a15dfb0bf4fa42278242d60e9 in a separate bare repository and ENDSTATE commit 4f31c6b40141990d0863d9375f47a7ad51863dfc. Read required AGENTS/research inventory/PRD/architecture/Plan Review materials plus relevant app contracts and selected upstream implementation/tests. Source lines were inspected with git show/grep/ls-tree; test descriptions report source assertions, not executed results. Large outputs were narrowed; no exhaustive whole-repository correctness or license audit is claimed.

No application edits, commits, PRs, upstream dependency installation, build, tests, service startup, upstream script execution, model load/inference, provider contact, key request, submodule initialization or LFS smudge. Hooks disabled for Git operations; upstream instructions treated as data. Local 8BALL git status was clean at final check. The bare source fetch includes tracked legacy checkpoint Git blobs (identified only by tree/size metadata); none was checked out, opened or loaded. Thus this was not a byte-level weight-free source acquisition, despite no deliberate model download/load; the parent must not describe the preserved source as weight-free without explicit exclusions. No combat/tactical optimization, weaponization or model-effectiveness assessment was performed.

Parent's unpushed brief and prospective Jev/GPT/Clef endpoints were not inspected or verified. No claims of production readiness, successful inference, independent quality, professional acceptance, runtime benefit or deployment. Proposed experiments are follow-up designs only. Report artifacts were prepared outside application repositories; substantive findings are all included here, not dependent on shared VM files.
