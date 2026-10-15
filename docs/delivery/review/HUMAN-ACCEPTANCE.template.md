# V0.2 human acceptance record — unperformed template

Template version: `human-acceptance-template-v1`. **No review, approval, inference or acceptance is recorded by this file.** Copy it for an actual review; every result below starts `NOT_RUN`. Preparation of a sheet does not change any task in [the canonical ledger](../progress.json).

Use fictional cases in the current single-operator application. Keep completed records, source excerpts, exports and reviewer identities in the review's designated protected location, outside this public repository. Public receipts may use reviewer aliases/roles and approved redacted evidence references. Never record credentials. Preserve failed observations and original outputs alongside later corrections.

## Session prerequisites and record

Complete these fields before the relevant review. Missing provider permission blocks actual-provider exercises; it does not prevent independent manual source, visual or accessibility review. Missing case or reviewer preparation is recorded as `BLOCKED`, not a pass.

| Field | Actual value / evidence reference |
| --- | --- |
| Record ID; template version | |
| Exact application branch, commit and source/tree hash | |
| Matching software acceptance receipt; its scope and limitations | |
| Reviewer alias/role; relevant experience; independence/conflicts | |
| Session start/end with timezone; task observation timestamps | |
| OS/version, browser/version, device/input, viewport and zoom | |
| Screen reader/version/settings where used | |
| Owner-selected supported configurations to review; untested configurations | |
| Fictional case IDs, starting revisions and export/snapshot hashes | |
| Source/dataset manifest, permissions, author and historical information cutoff | |
| Review-owned disposable database location; confirmation it contains no client data | |
| Selected provider and requested/served model; digest/revision if actually exposed | |
| Runtime, schema and prompt versions; actual configuration/runtime-check evidence | |
| Inference and any external-transmission permission; permitted operations/call exposure | |
| Applicable approved evaluation protocol/threshold record, or `NOT_APPROVED` | |
| Protected evidence location and redacted public receipt destination | |

Use an existing checkout at the recorded commit. Start the installed application with `python -m eightball`, or use the documented [local launch scripts](../../v2/RUNBOOK.md#1-start-the-workspace) when installation is needed. Explicitly select a review-only `EIGHTBALL_DB` before starting; do not reuse an operator's working database. Open `http://127.0.0.1:8048/v2/` and enter the terminal's operator token locally. Record startup failures without changing browser security policy.

[Open fictional case / Northstar](../../v2/RUNBOOK.md#2-explore-the-fictional-northstar-case) supports familiarisation with the current controls. A blank case is required for the original journey below. Known public examples, the eight [engineering review cases](../../../evals/plan-review-cases.json), and their [unfilled familiarisation sheet](../../evidence/plan-review/human-review-sheet.json) are not an independent held-out dataset. This human workflow sheet does not supply independent labels or approve numerical thresholds; use [the existing proposed quality protocol](../../../evals/PLAN-QUALITY-GATE.md) and the separately approved study materials.

For each exercised row replace `NOT_RUN` with the human's actual `PASS`, `FAIL` or `BLOCKED`, retaining observations, evidence, reviewer and time. Explain any inapplicable case rather than counting an unexercised requirement as passed. Record correction effort and elapsed time where relevant; do not invent success percentages.

## Original V0.2 journey — exact definition of done

The step wording below is reproduced verbatim from [the immutable original PRD, section 34](../../reference/8BALL-V0.2-ASTRA-PRD.md#34-v02-definition-of-done). Complete it in the actual application with deliberately authorised real-model proposals and genuine human accept/edit/reject judgements. Preserve source/model responses, rejection and edits as distinct contributions. Stop and record failed or unavailable generation; do not insert a catalogue or repaired output and label it model success.

The separate [actual-provider integration runner](../../v2/ACCEPTANCE-RUNNER.md#actual-model-use-is-a-different-command) exercises software with scripted review and synthetic observations. Its twenty checks are supporting integration evidence, not this human review, independent semantic evaluation or real-world confirmation. Record engineering fixture observations explicitly as fictional; action completion cannot establish an intended effect.

| Step | Original wording | Result | Observed behaviour / correction | Evidence reference | Reviewer | Time + timezone |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Operator creates a situation. | NOT_RUN | | | | |
| 2 | Pastes several messy source snippets. | NOT_RUN | | | | |
| 3 | AI proposes actors, events, claims, deadlines and constraints. | NOT_RUN | | | | |
| 4 | Operator accepts some, edits some and rejects others. | NOT_RUN | | | | |
| 5 | Operator defines the desired outcome. | NOT_RUN | | | | |
| 6 | AI proposes the outcome conditions and candidate actions. | NOT_RUN | | | | |
| 7 | Operator accepts the graph. | NOT_RUN | | | | |
| 8 | 8BALL produces at least two materially different routes. | NOT_RUN | | | | |
| 9 | It identifies the most important unanswered questions. | NOT_RUN | | | | |
| 10 | Operator records evidence resolving one question. | NOT_RUN | | | | |
| 11 | One route changes. | NOT_RUN | | | | |
| 12 | “What Changed?” explains the delta. | NOT_RUN | | | | |
| 13 | Operator tests a hypothetical stakeholder refusal. | NOT_RUN | | | | |
| 14 | Simulation produces different routes without changing live state. | NOT_RUN | | | | |
| 15 | Operator approves an eligible action. | NOT_RUN | | | | |
| 16 | Operator records that action as completed. | NOT_RUN | | | | |
| 17 | The intended effect remains unknown until evidenced. | NOT_RUN | | | | |
| 18 | Case reload preserves everything. | NOT_RUN | | | | |
| 19 | Audit export reconstructs all important human decisions and model proposals. | NOT_RUN | | | | |
| 20 | Desktop and mobile browser tests pass. | NOT_RUN | | | | |

Journey case/revision and exact model-call receipts: __________

Human judgement, missing dependencies, unsupported statements, corrections and unresolved disagreements: __________

## Professional source, identity and deadline review

Relevant scopes: B02-10/B02-14. Follow [Source Desk](../../v2/SOURCE-DESK.md) and [Source Clarity](../../v2/SOURCE-CLARITY.md), using a reviewer-approved fictional multi-source set. Record the selected originals/excerpts, exact wording, Unicode ranges/hashes and untouched material. Judge whether the workflow preserves meaning and is usable professionally, alongside its mechanical integrity. No model is called by Source Desk or Identity & deadlines themselves.

| Review task in the existing UI | Boundary to inspect | Result | Observation / evidence / reviewer / time |
| --- | --- | --- | --- |
| Evidence & claims → Source Desk → import a longer UTF-8 text/Markdown original; preview before storing. | Exact original, attribution and partial-reader limits remain clear. Import does not attest claims or start inference. | NOT_RUN | |
| Select passages containing relevant negation, uncertainty and attribution; preview and capture; trace captured evidence to its original. | The selected wording and original offsets are preserved. Captured coverage is not full-source analysis or verified truth. | NOT_RUN | |
| Import exact/near-duplicate and version candidates; inspect the explicit keep/separate choice and its rationale. | No silent overwrite, independent-corroboration claim, entity merge or loss of provenance. | NOT_RUN | |
| Evidence & claims → Identity & deadlines → Select source wording; select an ambiguous name mention. | Surrounding context and same-name candidates are inspectable. Name similarity supplies neither identity nor authority. | NOT_RUN | |
| Review identity as unresolved, explicitly distinct or linked, with a reason; revise a judgement and inspect history. | One mention is interpreted; actor records, observations and authority are not merged or reassigned. | NOT_RUN | |
| Select deadline wording; deliberately choose its target, date/source anchor, wall time, IANA zone and reasons; preview. | Relative dates do not inherit import/current time. The exact target, UTC conversion, route impact and invalidated approvals are understandable before any write. | NOT_RUN | |
| Exercise an ambiguous or nonexistent civil time present in the review set, then edit a preview input. | Ambiguity needs an explicit occurrence; nonexistent time is not guessed. Edited details require another preview. | NOT_RUN | |
| Explicitly apply the reviewed deadline; inspect What changed? and the interpretation history/export. | Only the selected scheduling field changes; source/review/case lineage remains, approvals invalidate, and no factual condition is attested. | NOT_RUN | |
| Retract a review-owned original or supporting source and revisit linked interpretations. | History and source bytes remain. Lost support prompts reconsideration; an adopted deadline is not silently cancelled. | NOT_RUN | |

Independent source interpretation errors, omissions, duplicate handling, unresolved ambiguities, correction effort and professional usefulness: __________

## Selected-provider lifecycle review

Relevant scope: B02-15, supporting B02-09/B02-12. Read [Analysis jobs](../../v2/ANALYSIS-JOBS.md) and [hosted permission/runtime boundaries](../../v2/HOSTED-DEVELOPMENT.md). Use only the selected, authorised provider and a dedicated disposable fictional database/server session. Record actual job IDs, stages, base revisions, started/returned call counts, latency and retained failure/proposal records. Do not retry automatically or change provider/model to obtain a pass.

Cancellation is cooperative: an external request already sent can finish and incur charges. This review must never describe cancellation, workspace lock or local server shutdown as recalling such a request. Obtain permission for the actual request exposure before exercising in-flight cases; stop if it has not been authorised.

| Review task in the existing UI/session | Boundary to inspect | Result | Observation / evidence / reviewer / time |
| --- | --- | --- | --- |
| Intelligence → inspect configuration and explicitly Check local runtime where applicable. | Configured, reachable, weights listed, inference completed and quality approved are distinct. An unreachable service is not declared uninstalled. No implicit download or request occurs. | NOT_RUN | |
| Analyse sources / Propose outcome graph with selected inputs; inspect Intake review's analysis monitor and refresh. | Actual provider, purpose, base revision, stage and returned/started calls are accurate; refresh retains the job. No proposal creates case facts or approvals. | NOT_RUN | |
| Cancel a queued review-owned job before a provider request starts. | No inference starts for that cancelled job and no proposal is published. If this state cannot be reached, record it unexercised. | NOT_RUN | |
| Cancel a review-owned job while its actual provider request is in flight. | Further stages/publication stop; late output is discarded; draining and actual calls remain visible. Do not claim provider-side recall. | NOT_RUN | |
| During another authorised request, make an explicit substantive update to that same fictional case. | The old-revision result cannot publish as a current proposal or overwrite the update. Preserve the superseded/failed result evidence. | NOT_RUN | |
| Lock, reopen and inspect the outstanding review-owned job. | Lock clears rendered case content; it does not claim inference stopped. The actual job can be inspected or explicitly cancelled after reopening. | NOT_RUN | |
| In the dedicated session, deliberately stop only the review-owned local server with an unfinished job; restart it against the same disposable database. | The job is marked interrupted, retained and not resumed or retried automatically. Any new request needs a deliberate new choice and permission. | NOT_RUN | |

Provider failures/refusals/timeouts, request exposure, calls/costs actually returned, cancellation timing and unexercised states: __________

## Human accessibility and supported-environment review

Relevant scope: B02-16. Follow [Accessibility](../../v2/ACCESSIBILITY.md) in the actual local application. Use the recorded owner-selected OS/browser/screen-reader configurations. Copy this section for each configuration; never extrapolate Linux/Chromium automation to another platform or assistive technology. Record the expected announced text, what was heard, navigation effort and any recovery needed. No WCAG certification is implied.

| Human task | Boundary to inspect | Result | Observation / evidence / reviewer / time |
| --- | --- | --- | --- |
| Start, sign in and open a fictional/blank case using the intended platform startup path. | Startup errors and token instructions are understandable; no secret is copied into review evidence. | NOT_RUN | |
| Navigate the existing views with keyboard and screen reader. | Headings, landmarks, field labels, button names, current view and destination focus convey position and purpose. | NOT_RUN | |
| Open/replace/close dialogs; traverse forwards/backwards; activate Escape. | Dialog name and content are announced, focus stays usable inside it and returns to a valid logical control on closure. | NOT_RUN | |
| Exercise blank-case/empty-search states and required-field or other safely induced local errors. | Empty/error guidance is available without sight; errors are announced and recovery preserves entered context where supported. | NOT_RUN | |
| Observe authorised analysis loading, progress, failure and cancellation states when provider prerequisites are met. | Real status changes and available next controls are understandable. Record `BLOCKED` when no authorised provider is available. | NOT_RUN | |
| Use Situation map's Records alternative, neighbourhood, clear and both filter-reset locations by keyboard; inspect a record and exact logic. | Dynamic replacement preserves orientation and a valid focus destination; canvas position is not required to interpret records. | NOT_RUN | |
| Review recorded narrow/mobile widths, zoom and applicable reduced-motion/forced-colour settings. | Text and essential controls remain usable; meaning is not conveyed by colour alone; no required control becomes unreachable. | NOT_RUN | |

Configuration-specific barriers, exact reproduction steps, severity, workarounds and untested configurations: __________

## Owner visual and mobile review

Relevant scope: B02-19. Inspect the existing [black/graphite visual system](../../v2/BLACK-VISUAL-SYSTEM.md) and actual application, rather than treating a screenshot or [read-only design preview](../../../scripts/design_preview.py) as functional acceptance. Record the owner's judgement and rationale; an agent cannot provide owner sign-off.

| Owner task | Result | Observation / evidence / reviewer / time |
| --- | --- | --- |
| Review black/graphite hierarchy, typography, status-label legibility and focus visibility in Situation room, Evidence & claims and Ways through. | NOT_RUN | |
| Compare the exact requested target, assumptions, unknown/disputed conditions, approval requirements and completed work without mistaking a conditional plan for success. | NOT_RUN | |
| Inspect Intelligence/provider controls and their configured/available/verified distinctions; inspect source and plan-review explanations. | NOT_RUN | |
| On the recorded mobile device/viewport, navigate, inspect routes/sources and use the visible workspace lock; verify that case content clears. | NOT_RUN | |

Owner decision, rationale, required corrections and remaining review: __________

## Representative dense-case graph comprehension review

Relevant scope: B02-20, with B02-16 accessibility. Use [Situation map's current Connections, Outcome flow and Records](../../v2/GRAPH-EXPLORER.md). Agree a representative fictional case and operator questions before the session; record the case/export hash, actual record/link counts and why it represents the intended work. Northstar is useful familiarisation, not automatic proof of dense-case representativeness. If no representative case is selected, record `BLOCKED`; do not invent a universal density threshold.

The existing force layout is bounded to 120 visible nodes; larger sets use a disclosed grid. This is an implementation boundary, not a proposed usability pass score. Where the chosen case exercises it, inspect that boundary honestly. Do not claim graph size, node count or synthetic fixture success establishes operator value.

| Operator task | Result | Observation / evidence / reviewer / time |
| --- | --- | --- |
| Find a specified actor/condition/source, inspect its origin/history and explain whether its state is observed, unknown, disputed or historical. | NOT_RUN | |
| Narrow to a neighbourhood, vary depth/type/search filters and recover the whole case; explain which records remain hidden. | NOT_RUN | |
| In Outcome flow and the inspector, explain exact signed AND/OR prerequisites and distinguish intended effects from evidenced results. | NOT_RUN | |
| Use Records instead of the canvas to reach the same case record and its full details. | NOT_RUN | |
| Explain material route differences, a shared blocker and the evidence needed next, without inferring authority or causation from visual proximity. | NOT_RUN | |
| Exercise the chosen case's dense view/grid if applicable, keyboard/mobile navigation and historical links; identify overload, missed information and misleading presentation. | NOT_RUN | |
| Verify graph exploration, layout/pins and filtering leave case revision, evidence, approvals and audit unchanged. | NOT_RUN | |

Predeclared operator questions; correctness/completeness; time/correction effort; blind spots; alternative-view usefulness and remaining barriers: __________

## Close the review record

List every `FAIL`, `BLOCKED`, unexercised requirement, disagreement and required correction with its retained evidence. Link subsequent review records without replacing the initial observations. Identify which existing task scopes the evidence actually supports; the canonical ledger remains the only task-status source. Completing this record neither approves an action nor authorises a merge, release or deployment.

Reviewer conclusion and exact reviewed scope: __________

Required follow-up, responsible human role and next review prerequisite: __________
