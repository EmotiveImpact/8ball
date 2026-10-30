# Current ENDSTATE work: atomic reviewed graph consumption

[Latest session](docs/delivery/sessions/2026-10-25-endstate-reviewed-consumption.md), [standing goal](docs/delivery/BUILD-GOAL.md), [both trackers](docs/delivery/PROGRESS.md). Continue feat/agency-authorisation-20261025. The local service now binds explicit graph review, source/result provenance and current permission/revision into one case transaction. Next integrate the review surface and worker/outbox; original model/human/production gates remain open.

# Current ENDSTATE work: durable processing attempts

[Latest session](docs/delivery/sessions/2026-10-25-endstate-processing.md), [standing goal](docs/delivery/BUILD-GOAL.md), [both product trackers](docs/delivery/PROGRESS.md). Continue feat/agency-authorisation-20261025, preserving newer work. EventWork adds exclusive claims, cancellation, interruption and stale/denied result handling. Reviewed case commits and worker/outbox integration remain next; no automatic external execution or production acceptance.

# Standing build goal and current execution

[Build goal](docs/delivery/BUILD-GOAL.md) defines the owner-authorised full product. [Canonical progress for 8BALL and ENDSTATE](docs/delivery/PROGRESS.md) shows actual task states, remaining work and next actions. [Latest sprint](docs/delivery/sessions/2026-10-25-endstate-event-inbox.md) implements the neutral event contract and durable host inbox. Continue current branch feat/agency-authorisation-20261025, preserving newer source. ES02-01/02 and B03-01 are partial; no production or actual-model/human acceptance is implied.

# Latest build: clearer overview and scoped agency API reads

Continue `feat/agency-authorisation-20261025`, preserving newer remote work. [Current handoff](docs/delivery/sessions/2026-10-25-agency-api-overview.md), [verification](docs/evidence/agency-api-overview-native-2026-10-25.json), [screenshot](docs/screenshots/8ball-overview-2026-10-25.png). Persistent grants and signed-token validation now protect an opt-in read/history/export API surface. Browser OIDC/MFA, writes/workers and production database enforcement remain unfinished. Full-product engineering is authorised; no deployment, production acceptance or deferred research adoption is implied.

# Current development: full-product roadmap

Owner explicitly authorised later product milestones on 25 October. B03-01 now has a tested permission-policy component; OIDC, durable grants, API/worker and database enforcement remain unfinished. Continue `feat/agency-authorisation-20261025`, preserving any newer remote work. See [session](docs/delivery/sessions/2026-10-25-agency-authorisation.md) and [receipt](docs/evidence/agency-authorisation-native-2026-10-25.json). The earlier V0.2 model/human gates remain open. No deployment or deferred research adoption.

# Current owner request: consolidate the completed build

Combined source `a9254e6087ef606d581d626bfcda9d7e555c857e` passed 1,267 source
tests, 1,267 installed-engine tests and 391 native browser checks, plus both
checkpoint GitHub CI workflows. [Verification receipt](docs/evidence/build-consolidation-native-2026-10-25.json).
[PR4](https://github.com/EmotiveImpact/8ball/pull/4) records final-head CI and the
owner-authorised merge. Start from current remote main once that PR is merged;
older branch instructions below are historical. PR3 was closed because its exact
head was already integrated. Actual-model and human acceptance remain open.

Read [NEXT-BUILD.md](docs/delivery/NEXT-BUILD.md) for the next agent's executable
software/model/lifecycle test procedure. [ADR0007](docs/decisions/0007-owner-build-consolidation.md)
records the new explicit integration authority; [current session](docs/delivery/sessions/2026-10-25-build-consolidation.md)
records actual verification and merge outcomes. All previous source and original
acceptance gates remain. Earlier provider observations below are historical;
do not repeat an unproved key-delivery diagnosis or treat coding-agent reviews
as independent professional acceptance.

# Historical provider preparation

The owner selected Anthropic. [Exact secure setup fields](docs/v2/ANTHROPIC-SETUP.md) and [configuration/source receipt](docs/evidence/anthropic-setup-2026-10-18.json) distinguish prepared settings from active access. The existing EIGHTBALL_API_KEY secret needs its destination changed to api.anthropic.com and the key entered securely, then Save/Publish. Claude Sonnet 4.6 compatibility is unverified until actual responses; keep every original local gate. [Full sprint/ER review](docs/delivery/sessions/2026-10-18-anthropic-configuration.md). Application code is unchanged; earlier native results below belong to their exact tested source. All 98 discoveries and original task statuses remain preserved.

---

# Current development: source-stable evidence and prospective study records

Verified code `25ca5e2dce4f28ec33d9b132cccabfa15b23683e` passed 1,267 source tests, 1,267 installed-kernel regressions and 391 native browser checks across all 11 suites; source/artifact inspection valid before documentation-only final receipts. [Exact receipt](docs/evidence/review-evidence-native-2026-10-18.json).

Continue `feat/v02-review-evidence-20261018` from `e513237f5b66c0689fa870e0d82873d8b71e4d8a`, preserving all earlier work. [Current sprint and full Emergence Review](docs/delivery/sessions/2026-10-18-review-evidence.md) records the restored environment, engineering changes and exact verification. [Optional private recording guide](docs/delivery/review/PROSPECTIVE-RECORDING.md) prepares genuine future studies without granting approval. The [canonical ledger](docs/delivery/progress.json) retains every required gate/status. Actual service/model/secure key are still missing; existing fictional-fixture US$5 permission does not need to be requested again. Owner review is at the end; independent qualified review remains distinct. No further main merge/release/deployment. Earlier source-bound results below remain historical.

---

## Current work: whole-system direction and evaluation readiness

Continue `feat/v02-evaluation-readiness-20261016` from `0fed04b`, preserving every earlier fix and research source. Read [the owner's technical direction](docs/strategy/OWNER-TECHNICAL-DIRECTION-2026-10-16.md), [all-category source findings](docs/research/github-2026-10-16/whole-system-review.md), [actual-provider evidence guide](docs/v2/ACTUAL-PROVIDER-EVIDENCE.md) and [current sprint](docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md). The sprint fixes explicit-model identity and retains generation/lifecycle evidence; tested code `17a275c` passed 1,171 source tests, 1,171 installed-kernel regressions and 391 native checks across all 11 suites. [Exact-source receipt](docs/evidence/whole-system-readiness-2026-10-16.json) records valid inspection and limits. B02 stays 10/20 and ES01 5/5 internally; no deferred runtime adoption or new model calls.

## Latest owner research: understand Ruflo

Read [the plain-English Ruflo investigation](docs/research/github-2026-10-16/ruflo-owner-guide.md) and [source-only handoff](docs/delivery/sessions/2026-10-16-ruflo-owner-review.md). This explains optional worker coordination, separately supplied model access and evidence limits. No runtime adoption or acceptance change; the verified development below is preserved.

## Latest development: Qwen API transport and research source copies

On `feat/v02-compatible-provider-20261016`, based on research checkpoint `c9fd384`, all 28 inspected source repositories are now populated under [research/external](research/README.md) at immutable pins. Tested code `ddfead7` passed 1,104 source tests, 1,104 installed-kernel tests and 391 native browser checks across 11 suites; [source-bound receipt](docs/evidence/compatible-native-2026-10-16.json). The [Qwen setup guide](docs/v2/QWEN-SETUP.md) explains secure hosted endpoint configuration. Read [the current sprint](docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md) and [handoff](docs/delivery/HANDOFF.md). This development branch includes all consolidated main/fixes and research proposals. Actual-model, independent/human V0.2 acceptance remains open; source copies adopt no deferred runtime. The owner authorises fictional model tests up to US$5 and expects their supplied endpoint to be free; confirm the service limits after receiving its public URL/model and secure key.

## Latest research proposal, 16 October 2026

For the owner's requested GitHub search and combined system plan, read [ENDSTATE evolution](docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md), [pinned component research](docs/research/GITHUB-COMPONENTS-2026-10-16.md) and [the session handoff](docs/delivery/sessions/2026-10-16-evolution-research.md). This is a documentation proposal on `docs/endstate-evolution-plan-20261016`, based on consolidated main `d7d36b8`; application behavior and acceptance gates are unchanged. The next engineering requirement remains actual-provider V0.2 evaluation.

# Current consolidated build: 8BALL powered by ENDSTATE

The latest application fixes and separate documentation are now consolidated in **main** under the owner's explicit instruction. GitHub PRs #1, #2 and #3 show Merged. The combined source passed 964 source tests, 964 installed-kernel tests and 384 native browser checks; see [the current receipt](docs/evidence/main-consolidation-native-2026-10-15.json). Read [the build overview](docs/delivery/BUILD-OVERVIEW.md), [current integration handoff](docs/delivery/HANDOFF.md), [ADR 0006](docs/decisions/0006-consolidated-development-main.md), and [the integration session](docs/delivery/sessions/2026-10-15-main-consolidation.md).

The application parent is `486c85ec07a05c7af8b30b142d2ad19faf402e25`; documentation parent `0ee5834c0745640369f5a538b770c346f234232a`. All earlier active application work is included in that application parent. The current tree combines both histories and preserves original research variants. Refresh actual main/HEAD and the latest receipt before development.

**V0.2 remains 10/20 required scopes verified; ENDSTATE V0.1 remains 5/5 internal scopes.** Main integration does not complete model, independent professional or human acceptance. No deployment, model download or deferred research implementation is part of this integration.

Use [NEXT-AGENT-PROMPT](docs/delivery/NEXT-AGENT-PROMPT.md), [V02-CLOSEOUT](docs/delivery/V02-CLOSEOUT.md), the [master PRD](docs/PRD.md), [roadmap](docs/ROADMAP.md), [architecture](docs/architecture/ENDSTATE-SYSTEM.md), [research register](docs/research/ENDSTATE-REGISTER.md), [decisions](docs/decisions/0006-consolidated-development-main.md), [review pack](docs/delivery/review/README.md) and sole editable [progress ledger](docs/delivery/progress.json).

Research archives: the supplied 19-file variant is at `docs/reference/endstate-handoff-2026-09-24/`; the older 18-file original pack and its six wrapper documents are retained unchanged at `docs/handoff/2026-09-24-endstate-research/`. Archive/ops branches remain preserved in Git. The historical documentation-only verifier/manifest describe their old frozen snapshot; use the new integration receipt for the combined source.

## Historical documentation-branch snapshot

The original index below is preserved. Its branch separation and next engineering task are historical; current source, current handoff and the explicit owner integration decision above take precedence.

---

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
