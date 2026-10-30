# Local-workspace security fixes, 30 October 2026

Session ID / environment: Codex, Cloudroom cloud thread.

Task IDs / objective: B01-02, B02-15 and ES01-03. Close the three reviewed findings: Windows static UNC resolution, eager provider-response buffering, and mismatched legacy-import lineage. B02-18 remains blocked on its original acceptance requirements.

Branch / base commit: `room/check-repo-with-three-sub-agents-pj2t`, from `1038291bf219d04e7fe4a6a01c332d1ac277fdba`. Remote main matched that commit when inspected. No pre-existing worktree changes or open PR for this branch were found.

Files changed: `eightball/api.py`, `eightball/providers.py`, `eightball/v2/intelligence.py`, `eightball/v2/services.py`, the local generation recorder, focused regression tests, and the mandatory delivery/changelog/emergence records.

Implementation commits: `4c943c640442af32aaf45e359748a73c8b333b2d` (three security fixes and regression tests), then `bb881f278eb24b97732382a83a6084a22d7e1983` (bounded installed-suite watchdog and retained failed evidence). Final receipt-only commit identity is recorded in PR8 rather than invented inside its own contents.

## Patch boundaries and compatibility

Both static mounts use one `LocalStaticFiles` guard. It rejects decoded URL backslashes and drive-qualified path components before Windows path normalization or filesystem resolution. It retains symlink containment, GET/HEAD, ordinary nested assets, index handling and existing security headers. No FastAPI/Starlette upgrade was forced. This application mitigation addresses the exposed HTTP path; the pinned Starlette version itself remains upstream-affected. [Upstream advisory](https://github.com/Kludex/starlette/security/advisories/GHSA-wqp7-x3pw-xc5r).

Jev and both Ollama adapters share a bounded HTTP streaming read. Existing 200,000/200,000/500,000-byte limits, JSON request payloads, timeouts, permissions and sanitized errors remain. The adapters explicitly negotiate `Accept-Encoding: identity`; an encoded response is rejected before any decompression or body read. Error bodies are rejected without reading them. Supplied clients still carry job cancellation checkpoints. The local evaluation recorder and replay test now support streaming, retaining bounded complete responses and an explicit unreadable marker for incomplete/oversized reads. There is no eager fallback.

HTTPX ordinarily decompresses an incoming chunk before an application sees it. The three affected adapters therefore request identity encoding and reject non-identity responses before reading them, including stacked encodings. This closes the compressed-expansion bypass without adding a custom decoder. Providers that ignore identity negotiation fail closed with the existing sanitized unavailable response. No new total response deadline or provider quota was introduced. The separately bounded hosted transports are unchanged by this patch; their compressed-chunk behavior is a separate review candidate (EM-103), not a verified fix here.

Migration reconstructs the legacy `Situation` from the verified export snapshot and stores that exact export as lineage. A concurrent later edit remains in the legacy case; it cannot silently change the imported snapshot. Existing graph conversion, evidence/completion history, cleared approvals and idempotency remain.

## Tests and exact results / evidence

Before the patch, the first three new Windows-path regression cases reached the filesystem-resolution sentinel and failed. Earlier independent controlled reproductions also showed all three adapters buffering an entire 2 MiB body and an imported budget of 123 paired with lineage budget 7000.

Initial focused verification: 190 tests passed. Expanded focused verification before encoding hardening: 240 tests passed; final focused verification: 250 tests passed, one existing Starlette/AnyIO test-library deprecation warning. Python compilation passed. These counts overlap; they are not cumulative unique totals. The independent final patch reviewer found no concrete bypass/regression in the three fixes and passed 57 focused checks plus evaluator Recorder probes. The first full native run at `4c943c640442af32aaf45e359748a73c8b333b2d` passed 1,324 source tests and all 391 checks across eleven browser suites, but package building failed because this uv-created environment lacked pip. Its inspected report is `artifacts/acceptance/20261030T091939Z-f8811f70/report.json` (`valid=true`, `run_status=failed`). After installing pip, a separate installed regression retry hit its fixed 120-second subprocess deadline. Only that regression deadline is increased to 240 seconds, below the existing outer 300-second step; the complete tests and short build-command deadlines remain. The fresh complete native run `20261030T092917Z-265de974` at `bb881f278eb24b97732382a83a6084a22d7e1983` passed: **1,324 source tests, 1,324 installed-ENDSTATE regressions and 391 checks across all eleven native browser suites**, with zero failures/errors/skips in either code suite. All 21 acceptance steps passed, including compilation, JavaScript syntax, structural fixtures and canonical document guards. Source stayed unchanged during the run; `--inspect` returned `valid=true`, `run_status=passed` before these final receipt-only edits. Full retained report: `artifacts/acceptance/20261030T092917Z-265de974/report.json`; source SHA-256: `aae8d051a83ca999c4fd2fad2a2572ac892300465ec82b880b05bfc3f145e042`. The final receipt preserves report/wheel hashes and every failure. The completed receipt will supersede this paragraph with actual source-bound results.

Real models called? None. All provider traffic in verification is mocked; test stores are disposable fictional SQLite files. No private cases, credentials, model weights or live provider requests were used.

What remains unverified or failed: native Windows/SMB exploitation is not performed; Windows path operations are simulated and resolution is intercepted. Actual-model, independent professional, human accessibility/platform and V0.2 release acceptance remain open. The separately reported nine-prerequisite Chosen Course read failure is retained as EM-102 and deferred from these three security fixes.

Task status changes: no original required flag, acceptance criterion or task status is promoted. Current sprint ownership and evidence are updated in `progress.json` only.

Receipt-head CI `41035068063` at `5040812` passed both 1,324-test code suites and ten browser suites, but Studio failed on a stale `local unreleased` expectation after the record correctly became `pushed_unreleased`. Downloaded failed evidence is retained under `/tmp/8ball-ci-41035068063`; the failure reproduced locally under `/tmp/8ball-studio-before-fix`. The corrected assertion verifies the exact canonical badge, version/title and visible limits; the full native Studio journey passed **44 checks** under `/tmp/8ball-studio-after-fix`. Application runtime code is unchanged. PR8 is the authoritative final-head cumulative CI record.

## Emergence Review

What did this sprint reveal that we had not properly seen, specified or understood before we built it?

- **EM-099, supported_by_tests, existing_task:** checking a static path after filesystem resolution is too late on Windows. Guard the decoded URL before OS normalization while retaining ordinary Windows separators after normalization. This is an application boundary fix, not an ENDSTATE redesign.
- **EM-100, supported_by_tests, existing_task:** checking response length after eager HTTP buffering does not protect memory. Streaming must also preserve cancellation and evaluation recording; transport-level streaming does not change the model's `stream=False` output contract.
- **EM-101, supported_by_tests, existing_task:** two individually valid audit snapshots need not describe the same migration. Construct imported data from its verified source snapshot rather than a later read.
- **EM-102, observed_in_build, new_candidate/deferred:** a valid nested Chosen Course prerequisite tree can fail when reassessment flattens more than eight children. The earlier domain review reproduced this through authenticated API calls. Preserve it for a separate bounded correction; do not quietly extend this patch or claim it resolved.

ER-01: runtime changes address the actual recorded failures; no case state is inferred from a model result. ER-02: provenance and intended outcomes remain separate graphs. ER-03: the migration source revision, rather than the latest independent read, defines lineage. ER-04: no watcher, automatic send or external execution was added. ER-05: the fixes add no operator review burden or new UI flow.

ER-06: no outcome envelope or probability was invented. ER-07: models remain replaceable proposal providers with unchanged schemas and permissions. ER-08: the original fixer workflow and product identity remain. ER-09: OS paths and HTTP buffering expose engineering risks without proving production agency security. ER-10: the nested-course defect remains visible instead of being lost after the security review.

ER-11: no course selection, reconsideration or action authority semantics were changed. ER-12: conclusions cover these three paths, not all vulnerabilities or all deployment configurations. ER-13: failed experiments and bounded response omission remain explicit; no paid retry or invented inference occurred. ER-14: native evidence must identify the tested source and artifact hashes before final receipt-only edits. ER-15: the expected benefit is avoiding credential disclosure, memory exhaustion and misleading lineage; no independent operator-value measurement is claimed.

- **EM-103, operator_hypothesis, new_candidate/deferred:** unchanged hosted transports require a separate compressed-expansion review. This sprint closes that representation path only in the three affected legacy/local adapters.

- **EM-104, observed_in_build, existing_task:** the installed suite watchdog was shorter than the measured complete source suite runtime; align bounded nested test budgets while preserving all checks.

- **EM-105, supported_by_tests, existing_task:** the native delivery assertion must follow canonical pushed/released state instead of demanding a local-only label. Preserve the real browser journey and strengthen its exact-state check.

Emergence evidence level / roadmap disposition: EM-099–101 refine existing B01-02/B02-15/ES01-03 work; EM-102 is a deferred candidate within B03-07/ES02-06. No new required scope or release gate was added. Owner review remains pending.

Last pushed code checkpoint / PR: `bb881f278eb24b97732382a83a6084a22d7e1983`, [draft PR8](https://github.com/EmotiveImpact/8ball/pull/8). Both checkpoint GitHub workflows passed (41033947448 and 41033947388). Final receipt-head identity and CI are reported in the PR handoff comment.

Publication: the complete source and records are on the PR branch. Final handoff reports the resulting receipt commit and clean/dirty worktree; this document does not fabricate its own final hash.

Next task and exact next command/test: `gh pr checks 8`, then obtain explicit owner authorization to merge this reviewed development patch. After integration, follow `docs/delivery/NEXT-BUILD.md` for the unchanged actual-provider and independent/human gates. To reconstruct local acceptance evidence, check out tested commit `bb881f2` and run the documented native command; the final receipt-only source naturally has a different overall fingerprint.

Merge/deployment state: pushed development branch, draft PR8, unmerged and unreleased; no production deployment. A concrete reviewed patch and final verification precede the merge decision.
