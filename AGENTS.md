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
