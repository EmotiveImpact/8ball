# Selected Sonnet lifecycle checkpoint — 26 October 2026

- **Session / environment:** Devin, existing Linux development VM; [session](https://app.devin.ai/sessions/dba6fbb6c7fc4ec0ad09d1333b6ab159).
- **Task IDs / objective:** B02-15 actual-configured-provider local lifecycle; ES01-05 bounded CI allowance. No model-quality or release acceptance.
- **Branch / base commit:** `devin/1792969169-roadmap-integrated` / `a31283785f6ccc2a5c31b9b936a9da353dcfb3fe`.
- **Files changed:** retained evaluation reports/checkpoints and evidence index; canonical delivery/changelog/emergence records and generated views; this handoff; `.github/workflows/ci.yml` timeout only. No application, engine, adapter, prompt, fixture or test changes.
- **Implementation commits:** actual-provider experiments ran at the clean base above. Subsequent changes record the evidence and increase the bounded CI allowance; their hashes are discoverable from the PR. The final software receipt records its exact tested commit separately.

## Tests and evidence

[Retained index](../../evidence/sonnet55-lifecycle-2026-10-26.json) binds both fresh reports to source SHA256 `49eb0908664241b4b4150f49bff4a2a9dc9e18b3ea2f2f09004e17e83c73540d` and preserves all 29 lifecycle checkpoints. No earlier report is relabelled.

1. Five actual native Sonnet requests passed the unchanged four frozen generation fixtures. The successful report matched current source, fixed fixture identity, provider/model and protocol before lifecycle work began.
2. Each scenario intervened after the **first application call admission**: cancellation → `cancelled`; changed case → `superseded`; owned process restart → `interrupted`.
3. All eight checks passed in each scenario: expected terminal state, inactive worker, absent proposal ID, no published proposal, no unintended case mutation, only one admitted stage, no later admitted call and stable status. The restart stopped only the harness-owned process and did not resume work.
4. These are local HTTP/process observations under the actual provider configuration, not native-UI lifecycle acceptance. Admission does not establish that the remote endpoint received, completed or cancelled a request. Those facts and the three interrupted/discarded requests' billing remain **unknown**. No race was retried; no output was patched; no runtime defect was found.

**Models/data:** direct `api.anthropic.com/v1/messages`, `claude-sonnet-5-5`, `anthropic_messages`, fixed fictional repository inputs and disposable database. No customer records, fallback, automatic retry or provider substitution. The owner selected this model and authorised bounded fictional testing within US$5 total, accepting the uncapped credited account with top-up off. Fresh successful generation usage estimates US$0.035328; known Sonnet usage now estimates US$0.123828, plus previously reported decision cost US$0.000008547. These are not invoice totals. Rejected and discarded-request billing remains unknown. No provider-enforced cap is claimed.

**CI correction:** [the preceding verify attempt](https://github.com/EmotiveImpact/8ball/actions/runs/40294671373/job/121477697237) reached its 20-minute timeout after slow Ubuntu font/Chromium dependency installation. Acceptance had begun but not completed. Its unmodified log is retained. Allow 40 minutes for the same steps, native checks and always-uploaded evidence; no gate is removed, no retry or permission bypass is added. Current CI must still be observed, not inferred from this edit. The previous rerun API returned 403 and the automated review service errored without findings; neither is a pass.

**Focused verification:** the first run had 323 passes and one delivery failure: the new next-action text removed reserved coordination lineage. The full prior text was restored, with the lifecycle checkpoint appended instead. [Failed output](../../evidence/lifecycle-delivery-regression-2026-10-26.log.xz) is retained; the corrected run passed all 324 focused checks. No model call was repeated for this documentation correction.

## Remaining scope and delivery

- **Unverified:** actual-provider native-UI lifecycle/human review, remote completion/cancellation/billing, independent semantic quality, predictive accuracy, professional acceptance and production readiness.
- **Task status changes:** none. B02-15 stays partial with a more precise blocker; reserved lane owner/branch/base and all original acceptance requirements remain. Other quality/human/release gates remain open.
- **Last pushed commit / PR:** live experiments use the already-pushed base above; [PR #6](https://github.com/EmotiveImpact/8ball/pull/6) is the publication authority. The closeout records final software verification; the subsequent PR head identifies the publication commit.
- **Unpushed work:** evidence/documentation and CI timeout change are local until the checkpoint is pushed. No uncommitted functional change should remain after that push.
- **Next task / command:** complete `python scripts/acceptance.py --mode native --base a31283785f6ccc2a5c31b9b936a9da353dcfb3fe` and source/artifact inspection. Then prepare the owner's requested historical prediction diagnostic using a documented pre-outcome cutoff and masked identifiers. Freeze outcome, horizon, inputs and baseline before inference; distinguish familiar historical data from independent or prospective held-out evaluation. Do not claim renamed history defeats model memorisation.
- **Merge / deployment:** no merge, deployment, release, model-quality approval or human acceptance.

## Emergence Review

**EM-314 — observed_in_build; existing_task B02-15.** Local finality is not remote finality. We can verify that the application discards work and does not start another stage while remote execution and charges remain unknown. The operator should see that distinction rather than a false promise that a request was recalled. This belongs to the existing 8BALL analysis-job and provenance boundary, not a second ENDSTATE cancellation subsystem.

**EM-315 — observed_in_build; existing_task ES01-05.** Dependency installation can exhaust the CI allowance before verification finishes. Retain the incomplete run, allow bounded setup time, and keep every gate. This improves engineering execution, not model or customer-benefit evidence.

ER-1–5: new evidence concerns local publication safety and missing remote observability, not a forecast or causal real-world claim. ER-6–10: do not turn unknown receipt into zero cost, repeat calls automatically, publish late work or erase the failed CI attempt. ER-11–15: source-bound history and authority remain unchanged; no selected course, observation or permission changes follow from these results. Operator usefulness and human acceptance still need their own evidence. Both findings are adopted only within existing tasks and remain in the owner-review queue; no new required capability is silently introduced.

## Preserved full-run failures and test correction

Two inspected, source-stable runs at `440a199` failed. The first invocation omitted the Node path already documented in the environment blueprint: 96 source tests failed, 1,994 passed and six skipped; installed-package regression timed out, although all 474 native browser checks passed. The next invocation used the documented Node executable; 2,096 source and installed regressions passed, but source clarity matched a pre-existing “2 deadlines” value before the asynchronously refreshed reconsideration count arrived. Both raw reports and failed logs/screenshots are retained under `docs/evidence/sonnet55-lifecycle-software-*`.

The test now verifies the warning counter changes from 0 to 2 and waits for exactly two filtered records. No application runtime, response mocking, arbitrary sleeps, source/revision rules or assertions were weakened. The focused correction passed 74 Python checks and 27 native browser checks; full acceptance is rerunning. Use `PATH="/home/ubuntu/.nvm/versions/node/v24.19.0/bin:$PATH" .venv/bin/python scripts/acceptance.py --mode native --base a31283785f6ccc2a5c31b9b936a9da353dcfb3fe`. The existing blueprint already records this path; no new installation or blueprint change was necessary.

**Emergence Review follow-up — EM-316:** freshness requires the specific changed state, not a coincidental page value. This is an existing-task verification correction, not new product scope or independent acceptance.

### Installed-suite budget correction

The third inspected run at `7e213d0` passed 2,096 source tests (121.59 seconds) and all 475 native browser checks. Installed-wheel regression alone timed out at its inherited 120-second build-command cap. The failed report/logs are retained as `sonnet55-lifecycle-software-package-timeout-2026-10-26`. Only the full installed regression call now gets 600 seconds; wheel build/install/smoke retain 120 seconds. Four tests confirm bounded defaults/override and failure/timeout propagation with no retry. **EM-317** records this verification-budget distinction. Full native acceptance is rerunning; no model calls are repeated.

The first budget-correction run was deliberately stopped when review found its enclosing package step still inherited 180 seconds. The unmodified partial report is retained as `sonnet55-lifecycle-software-interrupted-2026-10-26.json.xz` and is not a pass. The enclosing package step now has 900 seconds for build/install/smoke plus the 600-second regression; short command limits remain unchanged.

## Verified closeout

Exact commit `e3c92f05db73627d0c368aad919d00142fc85819`, source `4a613451258b4ed0f621833714c8f1b3ff5fe5863eca292d88d95513da94bd8e`, passed **2,100 source tests, 2,100 installed-wheel regressions, compilation, 24 JavaScript modules and 475 checks across all 13 native browser suites**. Source/artifact inspection matched before this documentation-only closeout. [Receipt](../../evidence/sonnet55-lifecycle-software-2026-10-26.json) retains all failed and partial runs; a valid inspected record is not necessarily a successful run. The one pre-existing Starlette/AnyIO deprecation warning remains.

The actual-provider lifecycle result is bound to the earlier unchanged application/engine/provider/browser runtime; later edits only corrected the native test synchronization and offline verification time budgets. No new provider call was made for software repair. Known Sonnet usage estimate remains USD 0.123828, with lifecycle/rejected billing unknown; decision-provider reported total remains USD 0.000008547. No provider-side cancellation, independent quality, production, merge or release claim.

Publication: existing PR #6, `devin/1792969169-roadmap-integrated`. Next action: the owner-requested documented historical retrospective with masked identifiers, frozen pre-outcome information, sealed outcome, explicit baseline and recognition/selection/leakage limitations. This is not a prospective or independently held-out predictive-quality gate.
