# 8BALL + ENDSTATE: start here

Consolidated handoff: **15 October 2026**. This is documentation integration, not a runtime release.

**8BALL is the fixer application. ENDSTATE is the reusable engine. Finish the current V0.2 acceptance work before implementing the expanded research.**

## 1. Which branch to use

| Purpose | Branch / observed revision | Instruction |
| --- | --- | --- |
| Active application | `feat/situation-intelligence-v2` at `290e310707cf8bef6caf2508c285312b091bd18b` | Continue current build here or on a scoped work branch from its refreshed head. |
| This consolidated documentation | `docs/endstate-consolidated-handoff-2026-10-15` | Read the whole plan here. Do not merge automatically. |
| Preserved research | `backup/research-recovered-2026-09-25` at `a8ecd9c833e1d929d6b2152cd80b51ac173967e8` | Historical source material, not current implementation instructions. |
| Main | `main` at `08bc26ef397ec960d1b33b099c40888a8229eac0` | Not the current application at this inspection. |
| Last model experiment | `ops/source-desk-closeout-20260926` at `b295758759e6cb1a3435ab45759ba3dc34d87efe` | Read-only Qwen experiment wrapper, not the application branch. |

These are inspected snapshots, not permanent branch-head guarantees. Fetch and compare before writing. PR #2 is draft and unmerged. It includes PR #1's foundation; the eight alpha labels are checkpoints, not eight competing applications. No production deployment or release tag is claimed.

## 2. What is built and what is still missing

Current runtime: **8BALL `0.2.0-alpha.8`**, ENDSTATE internal package **`0.1.0a2`**. Published application tree: `214c4835869dbe70f7c6ff6811977e5bb5a62841`, 252 tracked files before this documentation addition.

The black single-operator application contains the Situation Room, reviewed case/evidence model, source originals and excerpts, identity/deadline review, deterministic alternative routes, Connections graph, Plan Studio, Plan Review, Chosen Course, Emergent Insights, analysis jobs, approvals, scenarios and audit/export. Local/hosted model adapters exist; they are not themselves evidence of reliable generation.

Recorded native CI `36219680306` passed 938 code tests, the same 938 against installed ENDSTATE and 378 checks across eleven Chromium suites. Those are previous verified software results, not new model or human acceptance in this documentation session. See [native receipt](docs/evidence/native-closeout-2026-09-26.json).

**The canonical ledger says V0.2: 10/20 required scopes verified; ENDSTATE V0.1: 5/5 internal-core scopes verified.** These counts are acceptance items, not engineering-time or commercial-readiness percentages. [Current closeout](docs/delivery/V02-CLOSEOUT.md) identifies all ten remaining required scopes and who/evidence is needed.

**Critical newer evidence:** actual Qwen run `36340454120` on 27 September used the published application. Three extraction fixtures produced schema-valid proposals; the novel graph failed with `result_bypasses_verification` at `/routes`. All four live states remained unchanged. No semantic benchmark or production-model approval occurred. Read [the preserved raw report](docs/evidence/qwen-baseline-2026-09-27.json) before repeating the same experiment or claiming no actual model was run.

## 3. Read in this order

1. [Next-agent prompt](docs/delivery/NEXT-AGENT-PROMPT.md), [current closeout](docs/delivery/V02-CLOSEOUT.md), [AGENTS.md](AGENTS.md), and [canonical progress](docs/delivery/PROGRESS.md).
2. [Existing master PRD](docs/PRD.md) plus its [long-term addendum](docs/strategy/ENDSTATE-VISION-ADDENDUM.md). The original 37-section [Astra PRD](docs/reference/8BALL-V0.2-ASTRA-PRD.md) is unchanged.
3. [Current version roadmap](docs/ROADMAP.md) plus [future capability mapping](docs/strategy/ROADMAP-INTEGRATION.md).
4. [System architecture and operating loop](docs/architecture/ENDSTATE-SYSTEM.md), including application/domain-pack boundaries and model roles.
5. [Research register](docs/research/ENDSTATE-REGISTER.md), [experiment queue](docs/research/ENDSTATE-EXPERIMENTS.md), and [decision record](docs/decisions/0005-research-consolidation.md).
6. [Original research pack](docs/reference/endstate-handoff-2026-09-24/00-START-HERE.md), [build discoveries](docs/delivery/EMERGENCE-REGISTER.md) and [review prompt suite](docs/prompts/EMERGENT-INSIGHTS.md).

This index connects the records; it does not create a second editable progress tracker.

## 4. Authority when documents disagree

The latest explicit owner instruction controls scope: consolidate long-term direction in documentation now, preserve current build gates, use a separate documentation branch, and do not merge or deploy. The earlier hold still prohibits research-driven implementation during V0.2; it no longer prohibits this requested documentation consolidation.

Use live code plus its exact evidence for implementation claims; `docs/delivery/progress.json` alone controls task statuses. Historical snapshots, previous chat totals and archived prompts never overwrite newer records. Accepted vision, proposed design, implemented code, verified scope, merged code and released software are different states.

Older README/PRD/handoff paragraphs labelled local-only or alpha.7 describe previous checkpoints. Later source publication and native acceptance supersede those status statements, not their preserved history or requirements. ENDSTATE core acceptance is now complete for its internal scope; do not reopen it merely because a 24 September research document says 4/5.

## 5. What not to lose

All original research files from the newly supplied ZIP are retained unchanged under `docs/reference/endstate-handoff-2026-09-24/`. This supplied variant has **19 files**, including its manifest and README; historical delivery notes described an 18-file variant. [The context manifest](docs/delivery/context-manifest.json) records exact bytes and verifies the supplied manifest. Both the research branch and old backup are retained; neither is replaced.

All 71 earlier build discoveries remain. New consolidation findings are appended, not substituted for them. Dismissed, deferred and declined ideas remain reviewable. Every substantive sprint must continue the changelog, evidence, emergence review and explicit next-command handoff.

The narrated Draft Repair implementation was not recovered. Its [historical delivery record](docs/reference/2026-09-24-draft-repair-delivery-record.md) is not code or a valid claim of 905 tests in this checkpoint. Do not reintroduce it as implemented. Manual graph authoring exists; rejected-draft repair is separate, unverified work.

Full external-repository clones, model weights, private credentials and verbatim exports of all chats are not included or claimed. The preserved research contains source links and inspection findings, not installed upstream products. This consolidation preserves the available decisions and files, not inaccessible conversation turns.

## 6. Recovery and handoff

Use this documentation branch to recover the combined code base and linked specification. A companion recovery pack contains the source, incremental patch, Git bundle and checksums. Historical large screenshots and delivery ZIPs remain in `8BALL-Native-Closeout-Master-Backup-2026-09-26.zip`, previously stored in Library under `/8Ball/Backups/2026-09-26-Native-Closeout/`.

For an already-active coding session, send only the next-agent prompt and this branch, not a stack of cumulative patches. Do not overwrite a dirty worktree or force-push reconstructed history. The [session receipt](docs/delivery/sessions/2026-10-15-documentation-consolidation.md) describes exactly what this consolidation changed and what it did not.
