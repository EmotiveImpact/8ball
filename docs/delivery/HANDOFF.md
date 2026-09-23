# Shared handoff: this chat and Codex

## Start here

The product is **8BALL for fixers**, powered by the reusable **ENDSTATE** engine. Read `AGENTS.md`, `docs/PRD.md`, `docs/ROADMAP.md`, this file and `docs/delivery/PROGRESS.md`. The full original 37-section PRD is now in `docs/reference/8BALL-V0.2-ASTRA-PRD.md`; do not rely on a missing chat attachment. Current states belong only in `docs/delivery/progress.json`.

The latest verified application code checkpoint is `3a33866f375be355658d8e5d82addb25bcc7eed9`, branch `feat/situation-intelligence-v2`, draft PR #2. The staged drafting continuation, 306-test/native evidence and failed actual Qwen result are recorded in `docs/delivery/sessions/2026-09-23-staged-drafting.md` and `docs/endstate/COMPILATION.md`. ENDSTATE extraction evidence is in `docs/endstate/VALIDATION.md` and the contract is in `docs/endstate/CONTRACTS.md`. Refresh GitHub and local Git before starting: this is a checkpoint, not a promise that the remote head never changes. The ledger distinguishes this code baseline from later documentation commits.

## First session checks

1. Read the current PR/branch, latest commits and relevant CI. Verify the local remote URL and run `git status --short`, `git branch --show-current`, `git rev-parse HEAD` and `git fetch origin`.
2. Do not overwrite a dirty worktree, reset someone else's branch, force-push or assume `main` contains V0.2. Use the repository's current development branch from the ledger. Fast-forward only after reviewing local changes and divergence.
3. Read the specific task, its prerequisites and current implementation before changing code. Choose a bounded unit of work and create a working branch using `work/<task-id>/<session-name>` or the agreed active feature branch.
4. Record owner, working branch, base commit and next action in the task. Push a claim/handoff commit or coordinate on the PR before another session works on the same files. An unpushed local claim is not a distributed lock.

## Current next work, not a fresh rewrite

The first product blocker is `B02-09`: reliable reviewed graph proposals from genuinely new source material. The original captured Qwen graph named an absent verification action. A new explicit two-stage compiler now supplies IDs/wiring from complete model operations, but actual run 35911570117 still failed: readiness/goal duplication, invented existing-condition IDs and target confusion. Both failures are preserved; no template or synthetic verifier fixes the model response. Preserve and reproduce that failure. Do not manufacture the missing action, swap in a catalogue plan, weaken validation or shrink the test set to produce a green result. A typed multi-stage proposal/compiler or a different provider can be evaluated, but both must meet the same declared gate.

`ES01-01` through `ES01-04` now have scoped extraction evidence. 8BALL uses the embedded ENDSTATE kernel, and neutral/sales/support fixtures share that code without breaking old wire or audit records. Continue with `ES01-05`: review the embedded package and versioned result compatibility before accepting the package gate. This does not authorise a framework rewrite, public SDK launch or a new sales application.

`B02-18` stays blocked until the full V0.2 acceptance requirements pass. Optional `ES03-03` Jev live testing is blocked on an authorised key; never request a secret in a repository, PR comment, commit or public handoff.

## During implementation

Use stable task IDs in branch/commit/PR descriptions. Link a shared engine task from an 8BALL task rather than claiming it twice. Record new findings as blockers or explicit new tasks; do not silently rewrite an accepted objective. Keep model interpretation, evidence state and execution authority separate. Keep test fixtures fictional and avoid confidential information in logs/artifacts.

Before pushing, fetch again. If the source moved, inspect the diff and reconcile with normal merge/rebase on your own working branch. Re-run affected tests. Do not push a tree based on an old parent and assume it contains the other environment's changes.

## Status updates and checkboxes

Edit **only `docs/delivery/progress.json` for task states**, then run:

```sh
python scripts/delivery.py --write
python scripts/delivery.py --check
```

`PROGRESS.md` is generated. `[x]` means the named acceptance scope has evidence, not “someone wrote code”. Other states remain unchecked: `not_started`, `in_progress`, `implemented`, `partial`, `blocked`, `deferred`. Checked tasks need evidence references; failed gates need the failure and next action. Do not delete a task to improve completion figures. No percentage of total product readiness is inferred from the number of boxes.

Every substantive task records: ID, status, owner, branch/base commit, code paths, acceptance criterion, evidence IDs, blockers, next action and update date. Store exact code/CI/model artifact references under the ledger evidence registry. Redact secrets and sensitive source material. If a completed task regresses, reopen it and preserve its prior evidence/history in the session record.

## End every work session with a reproducible checkpoint

Use the template below in `docs/delivery/sessions/<date>-<session-id>.md`; add a brief PR comment pointing to it. Update affected tasks and regenerate the checklist in the same delivery. A documentation change may be verified using document/tool checks; application changes need the relevant existing and new tests.

```text
Session ID / environment: ChatGPT or Codex
Task IDs / objective:
Branch / base commit:
Files changed:
Implementation commits:
Tests and exact results / evidence:
Real models called? Runtime, model revision, data scope and result:
What remains unverified or failed:
Task status changes:
Last pushed commit / PR:
Unpushed work or patch/bundle location:
Next task and exact next command/test:
Merge/deployment state:
```

A commit cannot contain its own final hash: record its base/tested code revision inside the commit, then put the resulting commit ID in the PR handoff comment or the next checkpoint. Do not fabricate a self-referential hash or continually amend documentation to chase one.

When work cannot be pushed, provide an exact patch/bundle or source archive plus base commit and checksums. Clearly say it is not on the remote yet. The next environment cannot see an unpublished container directory or uncommitted local code.

## Test and release rules

Run the original and new backend tests, Python compilation, browser JavaScript syntax checks and appropriate native browser journeys for changed behaviour. Label bridge, mock, live model and native runs accurately. Read the actual CI result; starting a workflow is not a pass. Documentation tracking is checked by `scripts/delivery.py` and its dedicated workflow.

No automatic main merge, draft-to-ready conversion or deployment is authorised by this handoff. Re-evaluate current reviews and gates before asking for the release decision. Keep both product readiness and ENDSTATE packaging readiness distinct. A tested developer baseline can exist without claiming the full fixer platform is ready for customers.

## Copyable continuation instruction

Continue EmotiveImpact/8ball. Read AGENTS.md, docs/PRD.md, docs/ROADMAP.md, docs/delivery/PROGRESS.md and docs/delivery/HANDOFF.md. Confirm current GitHub and local branch/commit before changing anything. Keep 8BALL as the fixer product and ENDSTATE as its reusable engine. Select the next unblocked task from the ledger, preserve all evidence/approval/audit invariants, add and run tests, update task evidence and checkboxes, push a reproducible checkpoint and record unfinished work. Do not rewrite the application, silently change acceptance gates, merge or deploy without an explicit decision.
