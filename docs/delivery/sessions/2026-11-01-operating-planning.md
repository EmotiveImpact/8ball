# Full operating-plan engineering checkpoint, 1 November 2026

Owner request: finish ENDSTATE, including the previously missing exact-goal,
complete operating-plan, written-review, arithmetic and SOP path. This is a
bounded refinement of ES03-01/05 and B02-09/11/12, not completion of the whole
roadmap or independent acceptance. Repository tracking is used; no Linear ticket
or replacement task authority is invented.

Branch: `devin/1792969169-roadmap-integrated`.
Starting commit: `2f910b947e4f3af348c3331482bf08fc693d7fbc`.
Existing PR: https://github.com/EmotiveImpact/8ball/pull/6 (open, not merged).
No main merge, deployment, release, publication, provider/model change or new
inference is authorised by this checkpoint. Existing failed experiments remain.

## Delivered software

See [the internal contract and boundaries](../../v2/OPERATING-PLANNING.md).
The new neutral contract, bounded independent-context written-role method,
authority-checked host adapter, offline reconstruction, read-only viewer and
package/schema exports preserve the old coordinated v1 path. Same-model role
challenges are labelled honestly; native decision-model explanations are not
invented. Arithmetic preserves unknown costs; original goals and requirements
remain bound to every candidate. No task is executed or effect observed.

## Verification in progress

98 new contract/method/host tests passed. 134 focused kernel/new-flow checks passed
after permitting only the pure standard-library `decimal` dependency in the
existing import allowlist; all application/service import bans remain.
The extended event-review suite passed 75 native browser checks with fictional
signed identities, including originals/reviews/revision, SOPs, arithmetic,
inert markup, mobile reflow, keyboard disclosure, reload/stale state, no writes,
corruption fallback, failed outputs, lock and revoked-read clearing.
Compilation, JavaScript syntax and the isolated internal-wheel smoke passed.

Initial full source run: 2,660 passed and one failed. The sole failure was the
kernel's explicit standard-library allowlist lacking `decimal`, not an inference
or model-quality failure. The initial browser fixture also rejected an
unexplained strategy change introduced by its own markup probe; preserving the
same strategy in both candidates fixed the fixture without weakening validation.
Raw local logs remain under `artifacts/operating-*`; these uncommitted runs are
not presented as exact-source final receipts. Full native/package acceptance and
exact-source/artifact inspection are pending; final evidence is additive below.

An initial complete native run also passed at source hash
`3c94ee674760a4d781a0905d7d147cffa9938d3448624d15a7ad09ab9003ad37`:
2,661 source and installed-wheel tests, 25 JS modules and 517 native checks in
13 suites. Its exact-source/artifact inspection was valid before the following
fix. It is retained under `artifacts/acceptance/20261101T155907Z-183b9b48` and is
superseded, not attached to the later arithmetic change.

Final inspection found a six-calculation tiny-value chain could expand a
fixed-point result into 1,000,050 characters and approach Decimal underflow.
Nonzero calculated magnitudes now have explicit symmetric 1e-30–1e30 bounds;
out-of-range is invalid, not zero. Three regressions cover that chain, exact
fractional zero and the retained lower boundary. EM-355 records this finding.

## Emergence Review

What did this sprint reveal that we had not properly specified before building?

| Pass | Finding and disposition |
| --- | --- |
| ER-01, changed | Goal/hash/coverage and deterministic arithmetic can now be reviewed together; existing ES03-01, EM-349. |
| ER-02, connects | SOP completion and intended effect remain separate; reuse existing human command/observation boundaries. |
| ER-03, challenges | Structurally complete can still be semantically useless; no B02-09/11 promotion, EM-349. |
| ER-04, information | Written role reviews need explicit evidence character, correction and next check; EM-350, existing B02-11. |
| ER-05, freshness | Result revision/source/permission remain time-bound; no inferred source truth or continuous watch. |
| ER-06, consequences | Unknown fees propagate through surplus; Decimal context must not silently change results, EM-352. |
| ER-07, options | Same-model independent contexts are available, not multi-model independence or native-model reasoning; EM-350. |
| ER-08, requested problem | Exact goal and original requirements are bound; links alone cannot prove faithful commercial coverage, EM-349. |
| ER-09, reconsideration | Proposed per-step reconsideration/evidence fields are retained; no automatic external action. |
| ER-10, blind spots | Strict provider schemas close arbitrary unit maps; bounded dimension lists avoid this mismatch, EM-351. |
| ER-11, chosen course | No route is selected and no selected course changes; viewing cannot authorise action. |
| ER-12, coverage | Five-call/4,096-token bounds may reject larger plans; explicit decomposition is deferred, EM-354. |
| ER-13, recovery | Every concern/change needs a corresponding retained reason; rejects unverifiable change claims, EM-353. |
| ER-14, recovery | Recoverable source plus native/wheel receipt required; previous receipts do not validate these new files. |
| ER-15, value | Reduced scope drift/correction burden is a hypothesis. Actual operator/independent comparison remains open. |

All identified findings EM-349–355 remain in the append-only register, including
the deferred bounded-decomposition candidate. No new required task, lane-owner
change or quality/release checkbox is created. Existing human, semantic,
prospective, actual-provider and production gates cannot be closed by these tests.

## Handoff

Next: finish full native/package acceptance and inspect exact source/artifacts;
publish functional changes plus the canonical changelog/register/ledger together,
settle remote software checks and keep the separate review service state explicit.
Nothing from this checkpoint is pushed yet. No claim that a real full commercial
plan has run through this new protocol, or that £100k is achievable, is made.
