# Evaluation reliability and Anthropic protocol, 30 October 2026

Session ID / environment: Codex, Cloudroom cloud; Python 3.13.18 and native Chromium.
Task IDs / objective: B02-09, B02-12, B02-15, ES03-09, DOC-07. Bound this work to trustworthy evaluation receipts, source portability, a real process restart, explicit native Anthropic structured output and truthful provider configuration UI.
Branch / base commit: `room/review-last-commit-1038291-frrj` / `825ad6668c2c7d128da367476fe16cb8d214b837`. Fetched current source and fast-forwarded from the originally reviewed 1038291 to preserve merged PR8 security fixes. Open PR5/6/7 remain separate; no work from those branches is assumed.
Files changed: evaluation runners, acceptance/source manifests, compatible/native protocol transport, provider labels/setup, native Development journey, regression tests and canonical delivery/history documents. No ENDSTATE kernel, original PRD, fixture, approval, revision, CSP or case-effect semantics changed.
Implementation commits: pushed claim `d50d6d2`; the implementation commit is recorded by the final receipt/PR, not invented inside itself.

## Implementation and verification boundary

Fast failed jobs now fail the lifecycle experiment and stop subsequent trials. Fast successful jobs remain inconclusive with no automatic retry. Source checks bracket lifecycle trials and finalization. A source inspection or cleanup failure is retained separately, sanitized, and cannot erase interruption/abort status; final receipt saving still runs when storage is available. Disk failure cannot promise a saved checkpoint.

Research-bearing manifests retain full `sha256` with declared/observed commits and add version 2 `application_sha256` with source bytes/metadata and declared pins. Across machines, only pinned-checkout availability may differ. Start/finish source observations within one run must remain identical. Wrong populated commits, changed source/pins, malformed hashes and legacy mismatches remain blocked. `.cloudroom/` IDE attachments are excluded alongside generated output/virtual environments, with source and research metadata still bound.

The existing hosted provider gains explicit `EIGHTBALL_API_PROTOCOL=anthropic_messages`, requiring direct api.anthropic.com/v1 and provider anthropic. Unset protocol keeps generic completions; there is no silent switch. Native wire-schema translation records both schema hashes and retains all original local constraints. Native responses require one text block, complete end_turn, bounded identity-encoded data, safe model/usage metadata and strict JSON. No response repair, provider fallback, continuation, model download or new dependency. Protocol/stop evidence must match every generation stage before lifecycle admission.

The real restart regression uses an actual owned Popen application and real HTTP/SQLite with a delayed fictional local Ollama response. It waits for the local request to arrive, kills/restarts the application, releases the response, and verifies interrupted status, one call, no proposal, unchanged case and valid audit. This is local software evidence, not an actual hosted provider or remote cancellation guarantee.

Intelligence cards and analysis forms distinguish invalid configuration from absent settings. Native tests restart the actual server with invalid API/HF settings, verify both states and no implied processing permission. They tick the permission checkbox, close/reopen the dialog and verify it resets.

Tests and exact results / evidence:

- Before repairs: nine new reporting regressions failed as predicted; `artifacts/evaluation-reliability/eval-before-fix.log` retains the actual failure output.
- Initial focused run: 75 passed, one old expectation failed because failed lifecycle trials now stop after one submission. That expectation was corrected to preserve failure/no-retry semantics.
- Next focused run: 254 passed. Expanded run: 305 passed, one test-helper failure because the Hugging Face fixture lacked the new optional protocol property; fixed without modifying HF runtime behavior.
- A focused run overlapped our native browser process and failed the occupied-port guard: 305 passed, one failed. No process was reused/killed to bypass it. Subsequent suites are serialized; full failure log retained.
- Latest completed focused set before final cleanup edge tests: 306 passed, one pre-existing Starlette/AnyIO deprecation warning in 19.85s. New cleanup/HTTP failure cases require the cumulative run below.
- 24 controlled native-protocol/process tests passed in 2.75s. These counts overlap focused/full totals; do not add them.
- Native Development journey passed 30 checks, including the real invalid-configuration restart. Screenshot: `/tmp/8ball-development-eval/8BALL-Invalid-Provider-Configuration.png`.
- Python compilation of eightball/endstate/evals/scripts/research helper/tests and pip dependency check passed. All canonical validators passed at the preparation checkpoint.
- Final focused set including cleanup/HTTP failure cases: 311 passed, one existing warning, 20.46s.
- Missing-key CLI preflights: generation, lifecycle and native full journey each exited 2/blocked; zero model calls. Retained at artifacts/evaluation-reliability/blocked-preflight.json.
- Full integrated native acceptance and source/artifact inspection: pending at this implementation checkpoint. No historical totals are attached to this source.

Real models called? None. All provider traffic in tests is controlled fictional output. Cloud and paired-Mac login environments expose no EIGHTBALL_API_* settings. A Cloudroom secure request for EIGHTBALL_API_KEY is pending; its private destination is /tmp/8ball-evaluation.env, outside source. No key value is read/printed or committed. Actual model testing requires usable secure access and confirmed pricing within the existing fictional-only US$5 ceiling. No independent professional/human acceptance is inferred.
What remains unverified or failed: actual Anthropic authentication/availability/inference; the original B02-09/B02-11/B02-12/B02-15 and independent human/accessibility/owner acceptance. Generic model-name/URL restrictions and distinct HF proxy policy are documented, not expanded. EM-102 course defect and EM-103 broader hosted compression candidate remain deferred from the prior sprint.
Task status changes: ownership/evidence/next action only in progress.json; no original acceptance criterion, required flag or status promotion. V0.2 remains 10/20 required scopes verified; ES01 remains 5/5 internal scopes.

## Emergence Review

What did this sprint reveal that we had not properly seen, specified or understood before we built it?

- EM-106 — execution outcome and evidence integrity are separate axes. Final source/cleanup errors must not rewrite an interruption. A quick provider failure is still a failure. Existing-task repair; supported by failing-before/passing-after controlled tests.
- EM-107 — declared research pins and observed checkout availability need separate identities. Portable acceptance must not remove provenance or tolerate wrong populated commits. Existing-task repair; real Git fixture and prerequisite/inspection tests.
- EM-108 — a provider identity does not specify API protocol or enforce a schema. Official Anthropic docs and controlled native tests support an explicit protocol and wire/local schema separation. Existing task; actual model behavior remains unverified.
- EM-109 — manager recreation alone does not test a process boundary. Real Popen/HTTP/SQLite recovery adds that evidence; a fixed test port also requires serialized suites. Existing-task repair; controlled process test, no hosted claim.
- EM-110 — absent and invalid settings need distinct operator states. Native tests confirm actual invalid configuration is visible before submission and permissions reset after use. Existing task; no independent usability study.
- EM-111 — IDE conversation attachments were accidentally part of source identity. Exclude IDE metadata while retaining actual source/metadata. Existing-task repair; source scan and exclusion regression.

ER-01: classify observed job/receipt changes before interpreting quality. ER-02: source/checkout/protocol provenance stays separate from planning/evidence/authority. ER-03: failed and interrupted evidence stays visible; no source state is attested. ER-04: no watcher, automatic send or paid retry; real late-response tests only show local discard. ER-05: clearer configuration reduces one avoidable submission error; operator benefit remains unmeasured.
ER-06: no outcome envelope, probability or new objective model. ER-07: explicit transport protocol preserves replaceable models; all original compiler checks remain. ER-08: fixer product and ENDSTATE kernel stay central with no new application/runtime. ER-09: source-check and protocol boundaries exposed evidence-tool risks; original actual-model gates remain. ER-10: deferred proxy/name-support/compression/course choices remain visible, without turning them into this sprint's scope.
ER-11: no chosen-course switch, action permission or approval rule change. ER-12: coverage is controlled HTTP/process and native Chromium; no universal remote cancellation/platform/model-quality conclusion. ER-13: retain failing tests, temporary port-collision failure and all future rejected actual outputs; never repair an output to claim unassisted success. ER-14: final receipt must bind the implementation commit, source manifest and artifacts before receipt-only edits; code checkpoint and pushed state remain distinct. ER-15: expected benefit is accurate failure diagnosis, reproducible evidence and fewer configuration mistakes; no professional/operator-value metric is invented.

Emergence evidence level / roadmap disposition: EM-106–111 refine existing B02-09/B02-12/B02-15/ES03-09/DOC-07 scope. Original observations remain immutable and decisions append. All deferred choices and previous 105 discoveries are retained; no new required scope or task acceptance.
Last pushed commit / PR: claim d50d6d2; implementation unpushed at this checkpoint, no new PR yet.
Unpushed work: implementation, tests and delivery records listed by Git; no private env file in the repository.
Next task and exact next command/test: `EIGHTBALL_BROWSER=/usr/bin/chromium .venv/bin/python scripts/acceptance.py --mode native --base 825ad6668c2c7d128da367476fe16cb8d214b837`, then `--inspect` the printed report before receipt-only edits. Actual fixtures run only after secure access/pricing; matching generation precedes lifecycle/full journey.
Merge/deployment state: development branch only; no merge, release/tag or deployment. Internal wheel is built locally by acceptance, never published.
