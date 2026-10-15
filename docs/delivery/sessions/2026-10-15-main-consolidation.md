# Consolidated development build and owner-authorized main integration

15 October 2026. Working branch `integration/v02-consolidated-20261015`, application base `486c85ec07a05c7af8b30b142d2ad19faf402e25`, documentation parent `0ee5834c0745640369f5a538b770c346f234232a`. Main observed before work: `08bc26ef397ec960d1b33b099c40888a8229eac0`. Starting worktree clean; all remote branches fetched. [ADR 0006](../../decisions/0006-consolidated-development-main.md) records the new explicit owner merge instruction and its scope.

## Final verification and main publication

Merge commit `6b57a4503c9e88b4aa97f36b4a24d36ecd82d31f` has both exact parents 486c85e and 0ee5834. Cumulative native run `20261015T225319Z-62e2dcc4` passed **964 source tests, 964 installed-kernel tests and 384 native checks across all eleven suites**, with zero failed/errored/skipped code tests. Compilation, JavaScript syntax, eight structural fixtures, offline internal wheel, schemas and continuity checks passed. Inspection returned valid=true/run_status=passed/native_browser_verified=true before final documentation receipt edits. Source fingerprint `9980113a775bb08046a8fc14d55d99d5e784f022e340692f6da548863ac2dff2`; report SHA-256 `853f765f7675594b0e2e4e8d70deb1a1840521accd37224627e9d17524f5a133`. [Final native receipt](../../evidence/main-consolidation-native-2026-10-15.json).

Pushed the integration branch, re-fetched main and verified it still matched 08bc26e, then advanced remote main without force to the tested merge. Remote main and integration were advertised at the same full 6b57a45 hash. Public GitHub pages show PRs #1, #2 and #3 Merged. A final documentation-only commit records these observed outcomes and updates both refs; the final response identifies that receipt commit. No source, archive or fix branch was deleted or rewritten. No deployment/tag/model download/inference occurred; source integration does not clear any V0.2 gate.

Independent read-only preservation audit confirmed 135 runtime/workflow files match the latest application, both histories/all 74 discoveries and all task scopes/statuses/milestones remain intact, both archives match, original PRD/frozen fixtures match, and 128 local links across its broader 10-page set exist. The committed original preservation check covered 107 links in eight entrypoints. Original archive Markdown has existing trailing-space line breaks; full diff --check reports those exact imported bytes. They were deliberately retained to preserve the supplied checksums; current nonarchive edits receive separate whitespace checks.

Reconstruct the tested merge for raw report inspection; final receipt/status edits are documentation only and get generated/history checks. Full logs/JUnit/screenshots/schema/wheel remain in local artifacts/acceptance/20261015T225319Z-62e2dcc4/. All 15 Emergence Review passes below remain valid, with the actual preservation and verification results now recorded. The next work remains authorized real-model evaluation and genuine independent/human acceptance, not another source merge.

---

## Integration

The latest application already contains outcome-engine alpha, situation-intelligence V0.2, Source Desk, generation-contract, graph-keyboard, provider-failure evidence and refresh/navigation fixes. Merge the separate consolidated documentation history into this newer source. Four conflicts concern generated CHANGELOG/EMERGENCE and their canonical JSON. Resolve canonical changelog by stable-ID union (all 20 application entries plus the documentation entry), and discovery records by stable ID/history prefix (all 74 unique discoveries). Regenerate the derived documents; retain all current application histories and evidence. No runtime file is replaced.

Both research variants are present: the supplied 19-file archive at `docs/reference/endstate-handoff-2026-09-24/`, and the older 18-file original pack plus six wrapper documents restored unchanged under `docs/handoff/2026-09-24-endstate-research/` from the pinned recovery branch. Distinct original manifests remain intact. Other archive/ops refs remain retained; older runtime trees, transport wrappers and encoded patches are not blindly merged over the current application.

Current README, START-HERE, build overview, closeout and next-agent guidance take precedence over preserved historical snapshot paragraphs. The original PRDs, actual model failures, frozen cases, all changelog entries and original discovery wording remain unchanged. [Build overview](../BUILD-OVERVIEW.md) shows the complete existing operator loop and boundaries. Long-term research remains documentation, not runtime scope.

## Verification and publication checkpoint

Preservation checks passed: 135 runtime/workflow files match the application parent byte-for-byte and mode-for-mode; both parents' changelog entries and discovery observations/history/evidence survive; all 74 discoveries are retained; task scope/status/required/dependencies/milestones are unchanged; all19 supplied research payloads and24 older-archive directory files match; original PRD and frozen generation hashes match;107 local entrypoint links exist. [Preservation receipt](../../evidence/main-consolidation-preservation-2026-10-15.json). Cumulative native acceptance is pending at this integration preparation checkpoint. A subsequent source-bound receipt must record the exact tested merge commit, mode, source fingerprint, actual code/installed/browser totals, report/artifact hashes and inspection. Do not attach the earlier964/964/384 pass to a different source without new evidence. No model/service/credential or human acceptance is supplied by a merge.

After successful verification, push the integration and main refs without force. Do not update the feature branch: its push triggers model experiments, whereas integration/main are model-free and have no deployment workflow. Main integration is a development-source consolidation under the owner's explicit instruction. It is not a V0.2 acceptance, release tag, deployment or provider authorization. The final response supplies actual published commit and remote verification; a commit cannot contain its own SHA.

## Emergence Review

What did this sprint reveal that we had not properly seen, specified or understood before we built it? Current runtime fixes and current research documentation were on different descendants of an older application snapshot. Selecting either alone obscures part of the project, and blindly taking the documentation tracker or an old research tree would lose newer evidence. Stable-ID history union and one current entry point refine EM-051/055/072/073. There is no new required runtime feature or discovery ID.

| Pass | Finding / disposition |
| --- | --- |
| ER-01 | Exact delta is consolidated source/documentation and explicit main authority; existing delivery tasks. |
| ER-02 | Code, research, tracker and histories need a common inspectable entry point; EM-072. |
| ER-03 | A newer documentation date does not make its older code/tracker snapshot authoritative. |
| ER-04 | Parent-byte/history/hash checks distinguish lossless integration from apparent completeness. |
| ER-05 | Preserve prior receipts at their exact source; fresh verification covers this merge. |
| ER-06 | Do not overwrite current runtime or silently trigger model workflows on the old feature branch. |
| ER-07 | Research becomes visible without importing its proposed runtime; no new scope. |
| ER-08 | Original PRDs, frozen fixtures and required acceptance remain unchanged. |
| ER-09 | Reconsider integration if another remote head advances or preserved evidence differs. |
| ER-10 | Consolidation is not real-model quality, professional review or human accessibility acceptance. |
| ER-11 | Chosen course, evidence, approvals and action permissions remain distinct and unchanged. |
| ER-12 | All current application features are included; archive/ops refs are indexed, not claimed as extra shipped features. |
| ER-13 | Both failed experiments and later corrections remain recoverable; no repaired-model pass. |
| ER-14 | Preserve both merge parents, recovery refs, archive variants and exact source-bound receipts. |
| ER-15 | One coherent build should reduce owner/agent confusion; operator usefulness still needs the end review. |

Next task after integration: deliberate model/provider setup, unchanged real-generation gate and actual-provider lifecycle/journey, then genuine independent and owner acceptance using the prepared review pack. No permission to download Qwen or use a paid endpoint has yet been given.
