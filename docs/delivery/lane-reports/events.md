# Events lane source-bound handoff — 25 October 2026

## Scope and recoverable source

- Product: 8BALL fixer, using the reusable ENDSTATE engine; existing roadmap only.
- Lane/task IDs: events; ES02-01, ES02-02, ES02-03, ES02-04, B03-04.
- Assigned branch: `devin/1792969169-roadmap-events`.
- Actual starting partition: `56c9b79428a612dff11e2fae0219640d156032ff`.
- Inspected implementation baseline retained by partition: `baca8ad9efa531e5f172058845852963d7d5234a`.
- Tested functional checkpoint: `f749627f9f7456ddcc5744f22374c57f8c5e64be`.
- Final handoff adds only these lane-local records. Its resulting commit and
  remote-head equality are reported after push, not fabricated inside that commit.
- Initial source-plus-record push `ab93300657ad21965ba8fc54669f3d382a41a6ad`
  was verified identical locally and at the assigned remote head. This final
  records-only correction truthfully marks that checkpoint pushed/unreleased;
  its own final remote-head equality is reported separately after the last push.
- No main/other-lane merge, PR edit, release/tag, deployment or external send.
- Only fictional fixtures; no provider credentials, weights or real-client data.

The actual checkout was fetched/inspected, and the new assigned branch was made
from the requested partition. Required entry, PRD/roadmap/delivery/architecture,
event, engine-validation and retained failed model evidence were read before
implementation. Historical native/quality receipts are not evidence for this tree.
The later agency documentation checkpoint is integration's additive reconciliation
responsibility; this lane did not import it or another lane's code.

## Functional changes

- `eightball/event_inbox.py` and `eightball/event_work.py`: internal caller-owned
  transaction seams; existing standalone semantics remain. The host can now
  combine fresh authority checks, receipt/attempt persistence and rollback.
- `eightball/event_workers/service.py` and package initializer: explicit text
  connector, exact-receipt source-processing review/revocation, current matter
  grants and mandatory current source policy, idempotent enqueue, three explicit
  attempts maximum per case/receipt, one durable claim before one configured
  processor call, cancellation/expiry/stale/revoked dispositions, retained local
  output/failure codes and stage metrics. No background loop/retry/send exists.
- `eightball/v2/event_reviews.py`: dispatched consumption checks the source review
  and current policy at view/preview/commit, including immediately before commit;
  local latency fields join the existing atomic review/audit/outbox transaction.
  Historical/local attempts retain their original reviewed path. Unknown case
  binding cannot be inferred from matching matter/revision.
- `eightball/v2/event_api.py`: optional text-ingest/source-review/enqueue/cancel/
  status registration, and a source-policy argument to review registration.
  Verified host identity is mandatory; no HTTP provider-execution endpoint exists.
- `eightball/event_workers/replan.py`: bounded detached exact-clock calculation
  cache. Revision-only reuse is allowed only without revision-bound approvals;
  all graph/evidence/clock/sort/other changes fall back to complete ENDSTATE
  recomputation. It calculates derived data only, never case/course/action state.
- `tests/test_event_dispatch.py`, `tests/test_event_replan.py`: fictional negative
  security/lifecycle tests and exact typed full-recomputation parity.
- `docs/endstate/EVENT-INBOX.md`: current contracts, limitations and explicitly
  historical earlier checkpoint gaps. No shared router/navigation/store/command,
  manifest, acceptance runner, canonical ledger or generated canonical edit.

## Task-by-task evidence (not acceptance promotion)

| Task | Demonstrated local engineering increment | Remaining gate |
| --- | --- | --- |
| ES02-01 | Existing strict versioned source/matter/occurrence/receipt/pending contract, explicit authenticated text-intake seam; text never becomes authority. | Integrated protected host and production source/identity policy acceptance. |
| ES02-02 | Atomic dedupe/ordering retained; current checks on idempotent retries; exclusive claims, explicit bounded retry, stale/revoked/cancelled result disposition, restart and rollback regressions. | Integrated identity/vault/provider storage transaction design and source-bound combined acceptance. |
| ES02-03 | Exact receipt/revision source-processing review plus separate explicit graph preview/review/commit; policy revocation after preview rolls back case/audit/notice. | Integrated identity/provider/vault route wiring and native reviewed journey. No professional/model acceptance implied. |
| ES02-04 | Local ingestion/processor/review metrics; conservative unchanged-input reuse and complete fallback exactly match full typed responses; cancelled/stale/revoked work cannot commit. | Real combined provider/human/durability latency and broader partial-graph performance acceptance; no general incremental speed guarantee. |
| B03-04 | Working explicit manual-text connector/service/HTTP seam; durable work updates; existing current-authority local transactional notices remain independent of actions. | Actual external connector/delivery, egress consent, production identity/vault and integrated retry/ordering acceptance. No network connector or external notification claimed. |

All assigned task gates remain **partial/unaccepted**; the canonical B03-04 status
is still `not_started` until the integrator applies an additive partial update.
The other four remain canonical `partial`. No canonical status was changed here.
Existing evidence/failures/dependencies/required flags and external blockers must
be preserved. Proposed evidence/task additions are in `events-changelog.json`;
they are integration instructions, not a second status ledger.

## Actual verification

Environment: Python 3.12.13 (`.venv` from the preinstalled pyenv interpreter),
development requirements installed; Node 24.19.0 from nvm on PATH. No browser,
model or external project was installed/run. No active Git hook/config was found
in the standard hooks directory; normal commits execute any configured hooks.
No repository lint/typechecker is configured separately; typed contract tests,
Python compilation, JS syntax and whitespace checks were used.

1. With nvm Node on PATH, `.venv/bin/python -m pytest -q`:
   **1,410 passed**, one upstream Starlette/AnyIO deprecation warning, 61.70s.
   Earlier full run before two route-wiring tests: **1,408 passed**, 63.45s.
2. `.venv/bin/python -m pytest -q tests/test_event_replan.py
   tests/test_event_dispatch.py tests/test_event_inbox.py tests/test_event_work.py
   tests/test_event_reviews.py`: **101 passed**, same warning, 4.98s.
3. `.venv/bin/python -m compileall -q eightball endstate tests scripts`: passed.
4. `find web -name '*.js' -not -path '*/node_modules/*' -print0 | xargs -0 -n1
   node --check`: all **18** browser modules passed; none was changed here.
5. `git diff --check`: passed. All changed tracked paths are lane-owned.
6. `scripts/delivery.py --check`, `scripts/changelog.py --check`,
   `scripts/emergence.py --check --base 56c9b79428a612dff11e2fae0219640d156032ff`:
   existing frozen sources/generated files pass (71 tasks/11 milestones,
   58 changelog entries, 113 previously recorded discoveries).
7. `scripts/changelog.py --check --base 56c9b79428a612dff11e2fae0219640d156032ff`
   deliberately reports **Changed build needs a new changelog entry** because the
   partition prohibits changing canonical changelog/emergence/tracking. This is
   retained failure evidence, not a gate bypass. Lane-local fragments provide the
   new entry/findings for the integrator to merge and regenerate centrally.
8. Additive fragment validation/regeneration is performed in a disposable mirror,
   using the existing validators/renderers and baseline-preservation checks;
   **passed**: 71 tasks, 59 changelog entries, 118 discoveries; all three generated
   render/write/read equality checks, baseline preservation, unique EV/EM IDs,
   unchanged unassigned tasks and retained blockers/evidence passed. The canonical
   worktree files remain byte-identical to the partition. This is fragment
   consistency, not runtime integration or broad acceptance.
9. Final focused event plus delivery/changelog/emergence pytest run after adding
   the lane records: **168 passed**, one upstream warning, 6.76s. Compilation,
   all-browser JS syntax, whitespace and the three unchanged canonical checks
   passed again. No runtime source changed after the full 1,410-test checkpoint.

Security coverage includes missing/expired/revoked/read-only/object-only/cross-
tenant/cross-matter authority; same-matter wrong-case IDs; source-review/policy
revocation before enqueue/claim/during processing/after preview/before commit;
unknown identities/routes; concurrent enqueue/claim; no repeated provider call;
invalid UTF-8/blank/oversized results; bounded attempts; cancellation/lease expiry;
stale revision; rollback after receipt/attempt/review writes; result-storage
failure; corrupt review; restart; local notice/audit linkage and detached parity.

Retained failed experiments: the first expanded event run had **3 failures and
72 passes**: two tests expected `EventConflict` but the existing review service
correctly raised `eightball.store.Conflict`, and one called nonexistent
`Store.commit` instead of `Store.change`. Fixed the fixture assertions/call,
not production restrictions. Replan invalid-input fixture initially failed
before reaching the cache because assignment validation correctly rejected
negative budget (**1 failed/96 passed**, repeated once before correction);
the test now supplies an invalid request dictionary to the tested boundary.
Subsequent focused runs passed 75, 88, 99 and finally 101 tests as coverage grew.
An early Git config inspection was rejected by the environment; no configuration
was changed. The initial documentation patch context did not match, so it made
no edits; the corrected patch preserved historical notes explicitly.

### Honest local timing exercise

One additional fictional local processor/explicit-command exercise used actual
`perf_counter` and aware UTC clocks (not the deterministic test timer):
ingestion 0.001030809s; processor stage 0.001432762s; pre-commit review processing
0.013605885s; review wait 0.001793s; receipt-to-review start 0.015621s. Full local
replan 0.004820818s; unchanged-input reuse 0.002267558s; exact full parity true.
These single-run samples are **not** real inference, human review, transaction
durability, production load or independent performance evidence. An earlier
exploratory run mixed the fixture's fixed queue clock with real UTC; its wait
totals were not comparable and are excluded, not presented as a benchmark.

## Integration instructions

1. Integrate the functional checkpoint from the assigned branch; do not merge main
   or another lane here. Preserve later agency docs/evidence additively; earlier
   native reports cannot be attached to this changed source.
2. Use the same case/access/inbox/work/review/outbox SQLite database locally.
   Identity/vault lanes must supply current transactional policy adapters:
   `authority(db, Identity, Resource, tuple[Operation,...], aware_now) -> bool`
   and `source_policy(db, Identity, case_id, EventReceipt, aware_now) -> bool`.
   Source policy must resolve applicable access/quarantine/scan/retention/
   withdrawal/processing/egress permission. Missing policy must deny, never become
   a permissive local bearer or test callback in the agency application.
3. Construct `EventWorkerService(store, source_policy=policy, processor=processor,
   authority=authority)`; processor accepts `(receipt, detached_case_snapshot)`
   and returns original bounded proposal text. Identity/intelligence host wiring
   must enforce verified worker identity, selected provider, timeout, budget,
   explicit processing/egress consent and no automatic paid calls/retries.
4. After real agency authentication and safe operation mapping, register
   `register_event_worker_routes(router, service)` and
   `register_event_routes(router, store, source_policy=policy)`. Never expose
   them through local operator-token fallback. Router prefixes are host-owned;
   all paths are relative `/cases/...`. Source text/body cannot select identity.
5. Explicit sequence: ingest receipt; inspect/review source processing with its
   exact digest/current revision; enqueue with review ID/request ID; invoke one
   named `process(..., worker=verified_identity)` internally; inspect result;
   use the existing read-only preview and explicit graph review/rationale. Keep
   evidence, proposed graphs, graph review, selected courses, action permission,
   completion and observed effects distinct. Incoming source stays pending.
6. On cancellation, stale/denied/interrupted/failed/uncertain work, inspect the
   retained record. No automatic resume/retry, exception-message disclosure or
   claim of external recall is permitted. Existing bound-envelope revision
   checks stay intact; do not silently rebase old event text or permissions.
7. Optionally use `EventReplanner` for derived responses only. Never reuse across
   omitted clocks, different snapshots or approval revisions; leave full
   fallback intact. No case save/course switch happens in this seam.
8. Merge fragment `entries`/`items` by stable ID, append unique EV evidence/code
   paths and apply only the five task suggestions while retaining all prior
   evidence/blockers. No task is proposed verified. Regenerate/check emergence,
   delivery and changelog centrally against the actual integration base.
9. Run source-bound full/native integrated acceptance, including original alpha,
   V2 and event-review journeys; add cross-lane negatives for local token/unknown
   agency routes, object leakage, missing policies and revoke-after-preview/
   claim/commit. Native/UI testing was not authorised/performed in this lane.

## Emergence Review — all ER-01 through ER-15

What did this sprint reveal that we had not properly seen, specified or understood
before we built it? Findings EM-113..117 are preserved with evidence, risks,
architecture/UX implications, counterarguments and dispositions in the fragment.
EM-118..132 remain unused reservations, not invented findings.

| Prompt | Answer for this bounded build |
| --- | --- |
| ER-01 — What changed? | Compared with the exact partition: dispatch/current-policy/source-review/timing and conservative reuse were added; no source observation, action authority or chosen course was asserted. |
| ER-02 — What connects? | Inbox/work/case/grants/review/outbox share one local transaction; source review and source policy are distinct dependencies. EM-113. |
| ER-03 — What challenges our picture? | A durable queue alone does not prevent permission revival; a cancelled or unpersisted result cannot justify replaying a paid call. Negative tests challenge those assumptions. EM-113/114. |
| ER-04 — What information matters next? | Concrete identity/vault/provider adapter and integrated native evidence, not invented provider output; operator recovery needs evaluation. EM-113/116. |
| ER-05 — What may become stale? | Receipt source version/time, case revision, current grants/policy, lease and exact plan clock are independent. Age is not falsity; cache must not revive approvals. EM-115. |
| ER-06 — What could follow from our action? | Local cancellation prevents publication but cannot recall provider work. Unknown provider/storage outcome remains uncertain; side effects are not observed success. EM-114. |
| ER-07 — What new option is visible? | Safe unchanged-input reuse avoids a kernel call for revision-only/no-approval changes. All other changes recompute fully; no new external strategy or send is introduced. EM-115. |
| ER-08 — Are we solving the requested problem? | Existing fixer event/review workflows are strengthened; ENDSTATE remains a neutral engine, not an industry app or automatic operator replacement. No scope gate is silently promoted. |
| ER-09 — What should make us reconsider? | Revocation, new revision, source withdrawal, lease expiry, failed persistence and changed clock/approval inputs require reinspection or full calculation, never automatic course switching. EM-113/114/115. |
| ER-10 — What have we missed? | Production policy transaction design, external connectors/notifications, combined latency/load and exception recovery UX remain unproven. EM-116/117; owner review pending. |
| ER-11 — Chosen course/reconsideration | No human-selected course is introduced or switched. Derived replanning is not authorisation, completion or truth. Existing review/approval invalidation remains. |
| ER-12 — Coverage/negative conclusions | Only explicit supplied fictional text/case snapshots were processed. No filesystem/vault crawling, omitted-input inference, global impossibility or independent corroboration is claimed. |
| ER-13 — Recovery/attribution | Scripted local processor and explicit command fixtures are deterministic contributions, not real model/human success. Retain failed disposition/base/source; no silent retry or assisted-success relabelling. EM-114/116. |
| ER-14 — Recoverable delivery | Functional checkpoint above contains the exact changed bytes; final lane records identify tests/base/limitations and the final push is verified separately. Parent baseline native receipt is not reused as this tree's evidence. |
| ER-15 — Operator value | This may prevent stale/revoked amendments and duplicate calls, but no reduced decision time/usefulness or professional quality has been measured. Review/retry burden is an owner-evaluation candidate. EM-116/117. |

## Remaining boundaries and next action

No native/browser/testing-agent run, real provider inference, production identity/
isolation/scanner/retention service, external send, pilot, independent semantic/
quality/human accessibility decision, release or deployment is claimed. No CSP,
approval/revision check, source truth or historical audit/import lineage was
weakened. Deferred research remains source-only/unexecuted.

Next owner: integration. Next exact checks after wiring/merging fragments:
`python scripts/emergence.py --write && python scripts/delivery.py --write &&
python scripts/changelog.py --write`, then all three `--check` commands with the
actual integration base and `python scripts/acceptance.py --mode native --base
<integration-start>` followed by its source/artifact `--inspect`. Retain failures
and broad external/human/model gates. Do not merge/deploy from this lane handoff.
