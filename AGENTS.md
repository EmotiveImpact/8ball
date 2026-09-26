# 8BALL + ENDSTATE continuation rules

Read `README.md`, `docs/PRD.md`, `docs/ROADMAP.md`, `docs/delivery/PROGRESS.md`, `docs/delivery/HANDOFF.md`, `STATUS.md`, `docs/PRD-V0.2.md` and relevant architecture/validation evidence before editing. The source branch is not evidence of a merge or deployment. Keep the original alpha import path and audit lineage intact.

State, planning and authority are separate. Models propose; operators review; source-backed observations determine evidenced conditions. Completing work must never apply its intended effects to reality. Unknown is not false. Disputes require explicit reconciliation. Do not remove approval/revision checks, weaken CSP or replace native-browser tests with a mock just to obtain green CI.

Run `python -m pytest -q`, Python compilation, `node --check` for all browser modules and the native `tests/browser_smoke.py` plus `tests/browser_v2.py`. A bridge run must be labelled as such. Do not represent model contract tests as actual inference, or a successful evaluation job as model accuracy. Preserve failed experiments. The first GLiClass configuration was not acceptable on the synthetic test set.

Do not put real client records, exports, tokens, model weights or secrets in this public repository. No automatic external actions, cross-client learning or production deployment are authorised by the V0.2 architecture. Agency production work must pass `docs/v2/PRODUCTION-SECURITY.md` first.

## Product identity and shared progress

8BALL stays the flagship fixer product. ENDSTATE names the reusable engine under it, not a model or a new app replacing 8BALL. Keep fixer workflows and commercial priorities central; prove later reuse with small domain fixtures before claiming other products exist. Extraction is tracked work, not accomplished by this naming decision.

`docs/delivery/progress.json` is the only editable source of task statuses. Use stable task IDs, scope and evidence. Set owner, branch and base commit for active work, update blockers/next action and preserve earlier failed evidence. Run `python scripts/delivery.py --write` and `python scripts/delivery.py --check`; commit the ledger and generated checklist together. Do not manually maintain competing checklists in chat or Codex.

At session start, inspect the actual PR/head and local worktree. Never assume an unpushed change or an unmerged branch is available elsewhere. Claim a bounded task and coordinate overlapping file edits with a pushed checkpoint/PR comment. End the session with the template from `docs/delivery/HANDOFF.md`, exact test results, branch/commit, unpushed changes and the next action. Do not force-push, discard local work or invent completion. No main merge, draft-to-ready conversion or deployment is authorised by the documentation/roadmap update.

The complete original V0.2 PRD is `docs/reference/8BALL-V0.2-ASTRA-PRD.md` (Git blob `cdaa878bcfdee65a62e2096eae085af64a5377c6`). Keep it immutable; new decisions go in the master PRD and decision log. A historical document is not a current status dashboard.


Hosted development: read `docs/v2/HOSTED-DEVELOPMENT.md`. Never commit, request in chat, or return a Hugging Face token. No live hosted inference runs without explicit permission and a selected model/provider. Preserve `evals/generation-cases.json` and its canonical fixture hash. Run `tests/browser_development.py` in addition to the original browser journeys after provider/visual changes. Read the latest session record: a packaged local patch is not a remote commit.

Graph exploration: read `docs/v2/GRAPH-EXPLORER.md` and run `tests/browser_graph.py` alongside all existing browser suites. Its canvas is read-only; never convert moving nodes into case amendments or use visual proximity as evidence of authority or causation. Preserve exact AND/OR semantics in the inspector and the existing reviewed editor. The newest source package includes the preceding unpublished HF/black patch. Do not apply that older patch twice.

## Mandatory changelog rule for every build

For every code, interface, model, architecture or delivery change, add a dated entry to `docs/delivery/changelog.json` before handing off. Include stable roadmap IDs, what changed, actual verification, limitations, and the truthful local/pushed/released state. Never delete or rewrite an entry already present at the compared base; add a correction or integration entry instead. Do not include credentials or client records.

Run `python scripts/changelog.py --write` and `python scripts/changelog.py --check --base <your-starting-commit>` alongside the existing delivery checks. `CHANGELOG.md` is generated. The in-app **What’s new** page uses the same canonical entries, not another manually maintained history. The product changelog is separate from the case-specific **What Changed** and audit trail. A new version label must never hide unfinished acceptance gates.

Plan Studio and analysis jobs: read `docs/v2/PLAN-STUDIO.md` and `docs/v2/ANALYSIS-JOBS.md`. Run `tests/browser_studio.py` in addition to all existing browser journeys. A graph preview is read-only; committing still requires the expected revision. Do not turn browser drag events into case commands. Cancelling analysis forbids publication and further stages, but must not claim to recall a request already sent to a hosted provider. Do not resume interrupted jobs automatically or silently repeat paid requests. This local implementation supports one server process only.


Source Desk: read `docs/v2/SOURCE-DESK.md` and run `tests/browser_sources.py` with every previous browser suite. Retain original text and exact Unicode code-point offsets, even when browser display normalises newlines. Import/search/selection never implies AI processing or verified truth. Source/excerpt/quote lineage and transactional retraction must stay intact; never merge duplicates or entities automatically. Preserve exact old source-free audit exports. Original files are local test text, not a production vault.

## Mandatory emergence review at the end of every build sprint

Before a substantive sprint is handed off, read `docs/delivery/EMERGENCE-REVIEW.md` and answer: **“What did this sprint reveal that we had not properly seen, specified or understood before we built it?”** Record discoveries, risks, architecture implications, UX implications, evidence level and a roadmap disposition. Do not silently convert an interesting discovery into required scope.

Every new changelog entry must include an `emergence_review` object, and the session handoff must contain an **Emergence Review** section. Classify findings as `existing_task`, `new_candidate`, `new_required_task`, `decision_record` or `no_action`. If a finding changes accepted scope, update `docs/delivery/progress.json` or add a decision record explicitly; otherwise preserve it as a hypothesis. Run the changelog and delivery checks before handoff.

## Preserve every discovery, not only selected features

At every sprint close run the question set in `docs/prompts/EMERGENT-INSIGHTS.md`. Enter **every identified build insight** in `docs/delivery/emergence.json`, including candidates you recommend deferring or declining. Use stable `EM-nnn` IDs, preserve original wording and prior evidence, and append decisions with a reason. The generated `docs/delivery/EMERGENCE-REGISTER.md` is the owner's evolving review document. Declined/superseded items are struck through, never deleted; a checked item derives only from its linked acceptance tasks in `progress.json`. An idea's adoption is not implementation or acceptance.

Prefer high-value, bounded improvements to 8BALL first. Translate adopted findings into explicit existing/new task IDs, not an uncontrolled automatic feature backlog. Leave every deferred choice visible for owner review. New changelog `emergence_review` objects must link their `insight_ids`. Run `python scripts/emergence.py --write` and `python scripts/emergence.py --check --base <starting-sha>`, then regenerate/check delivery and changelog artefacts. Correct older interpretations by a new linked item or appended decision, not erasure.

Product Emergent Insights are **not this build register**. Read `docs/v2/EMERGENT-INSIGHTS.md`; run `tests/browser_insights.py` and all prior suites. Scan findings are derived/inferred/hypothetical, and human review status is separate from factual evidence state. No detector, dismissal or review completion may attest a fact, alter a target, approve an action or trigger an external send. Explicit question creation must use the case command transaction, retain the finding link and invalidate approvals. Preserve dismissed/reappearing/history states, exact as-of revision, typed references, policy limits and source boundaries.


Source clarity: read `docs/v2/SOURCE-CLARITY.md`, run `tests/test_time_review.py`, `tests/test_grounding.py` and `tests/browser_grounding.py` alongside all previous suites. Never interpret a same-name match as global identity, merge actors from lexical similarity, use import/current time as an unstated date anchor, guess timezone abbreviations, or silently cancel an adopted deadline on source retraction. Deadline preview is read-only; application requires an exact reviewed digest and current case/review revision in one transaction. Review history and actor/date evidence states are separate. Preserve source-free export compatibility and the kernel’s no-service-import boundary.

## Plan Review and quality-evaluation boundary

Read `docs/v2/PLAN-REVIEW.md` and `evals/PLAN-QUALITY-GATE.md`. Run `tests/test_plan_review.py`, `evals/plan_review_bench.py` and `tests/browser_plan_review.py` alongside every earlier suite. Plan Review assesses the LIVE snapshot, not unsaved Studio edits. Never convert supported reviewer labels into factual state, action approval or an independent quality pass. Keep the immutable six-part review record and explicit scenario assumptions. Preserve noncolliding legacy route IDs and keep semantically different dependency paths distinct. Synthetic fixtures and unfilled reviewer sheets must not be represented as independent professional validation.

## Integrated acceptance and internal package (alpha.7)

Read `docs/v2/ACCEPTANCE-RUNNER.md`, `docs/v2/ACCESSIBILITY.md` and `docs/endstate/PACKAGE.md`. Prefer `python scripts/acceptance.py --mode native --base <starting-sha>` to isolated test totals. It retains **all eleven** browser suites, including Chosen Course. Never substitute `bridge` or `code` results for a blocked native run; report the mode, source hash and individual failures. Verify retained reports against their source and artifacts with `--inspect`. A valid evidence record can describe a failed or blocked run.

Actual inference requires the separate `evals/full_journey.py` opt-in procedure and configured providers. Standard acceptance strips provider tokens and operator database settings. No silent downloads, paid retries, substitute catalogue plans or invented model outputs. Scripted integration judgements are not independent semantic evaluation. Keep B02-09/B02-11/B02-12/B02-16/B02-18 gates explicit. Build the internal wheel locally; never publish it or merge/deploy without an explicit authorised decision. Continue the mandatory changelog and complete emergence register on every sprint.

## Vision and recoverable-source discipline

Read `docs/vision/8BALL.md`, `docs/vision/ENDSTATE.md` and ADR 0004. Candidate routes, a human-selected course, evidence, reviews and permissions are distinct. Do not implement a plan-selection click as authorisation or silently switch courses after ranking changes. Keep all existing approval-invalidating rules until a separately authorised change passes its own tests.

At sprint start reconcile every claimed latest feature with recoverable source bytes and matching evidence. A later handoff or screenshot without its source is reported-only; do not attach its test total to an earlier archive. Recover it or state an explicit rebuild. Do not replace a newer worktree with an older cumulative package.

Answer the expanded ER-11 through ER-15 prompts as well as the original ten. Preserve all discovered candidates, keep original observations immutable and append reasons when priorities change. Adopted vision is not implemented scope. B03-07/ES02-06/ES03-08/B04-04 remain optional and unaccepted in this documentation checkpoint; moving them into required scope needs an explicit decision and ledger update.

## Chosen Course preservation

Read `docs/v2/CHOSEN-COURSE.md`. Run `tests/test_courses.py` and the native-default `tests/browser_courses.py` with all prior suites. A selected route is a human intention, not an action permission or a fact. Never silently switch it when sorting or replanning. Preserve target, snapshot, exact prerequisite branch, sequence and rationale. Watches and review clocks remain explicit; reviewing does not clear warnings. Local pause/retirement must not be presented as external cancellation. Export/read must preserve old source-free formats and fail visibly on corrupt case/course history. Broader optional B03-07/ES02-06 prerequisites remain unfinished.
