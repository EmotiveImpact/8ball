# ENDSTATE event inbox — 25 October 2026

Base48e572e95be8b28d0b317d7bc8b3a18893a3ef76; branch feat/agency-authorisation-20261025. Owner explicitly requested implementation and clear status docs for both engines/product, plus a standing goal. BUILD-GOAL.md states the objective and completion criteria; progress.json remains the only editable task-status source. Refreshed actual branch/PR metadata while preserving prior inspections.

Built endstate.events incoming/receipt contracts and eightball.event_inbox durable host storage. Scope, source/version, optional occurrence/base revision and pending review are retained. Arrival sequence/receipt time are assigned by the host. Identical retries return the same receipt, conflicting retries fail and concurrent duplicates serialize. Restart preserves records. Incoming events never mutate a case or grant authority.

11 focused tests passed. Cumulative native validation follows. Current ES02-01/02 remain partial until proposal/review/commit and worker/outbox integration is complete. B03-01 remains partial; browser sign-in, PostgreSQL enforcement and actor-bound writes/workers are unfinished. See canonical PROGRESS.md for every remaining task in both tracks.

## Emergence Review

What did this reveal? Claimed occurrence time and durable receipt order are different; replay must preserve both (EM-101).

| Prompt | Finding / disposition |
| --- | --- |
| ER-01 | One written build goal, execution and both product statuses requested. |
| ER-02 | Neutral kernel contracts and host persistence have separate responsibilities. |
| ER-03 | Late arrivals must not silently reorder retained receipts. |
| ER-04 | Worker/outbox and reviewed commits remain prerequisites for live replanning. |
| ER-05 | Ingested text has no command authority. |
| ER-06 | Same event identity with changed content must fail, not overwrite. |
| ER-07 | Unknown occurrence time must stay unknown. |
| ER-08 | Durable ingestion is not automatic case processing or external execution. |
| ER-09 | Serialize duplicate races and preserve restart behaviour. |
| ER-10 | Keep one canonical ledger rather than competing completion lists. |
| ER-11 | No case evidence, target, chosen course or permission changed. |
| ER-12 | Test restart, concurrent delivery, delayed events, scope and corruption. |
| ER-13 | Preserve earlier100 discoveries and failed model/verification evidence. |
| ER-14 | Content hashes are not signed independent audit anchors. |
| ER-15 | Implement reviewed consumption and durable worker/outbox next, alongside agency access. |

Evidence: controlled tests. UX: show pending incoming information separately from accepted case changes. Architecture: no network/database dependency inside ENDSTATE. Disposition: existing tasks only; no production release/deployment or new research runtime.

## Verified source and next action

Tested 20400336bd5462733755001b42e991c05944e1d1: 1302 source tests, 1302 installed-engine regressions and394 native browser checks across11 suites passed. Exact source/artifact inspection valid before documentation-only receipt edits. Both checkpoint CI runs40204433283/40204433474 passed. One existing Starlette/AnyIO warning in each Python run. Receipt: ../../evidence/endstate-event-inbox-native-2026-10-25.json.

Next ENDSTATE work: reviewed consumption, worker/outbox, expected-revision and permission revalidation. Next8BALL work: browser sign-in/account administration and database/worker enforcement. All remaining requirements and blockers for both products remain in the generated canonical progress checklist. The standing goal is BUILD-GOAL.md. No original gate was weakened or marked complete by this increment.
