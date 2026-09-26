# Source clarity sprint: local-only checkpoint

24 September 2026. `0.2.0-alpha.5`. Work branch: `work/B02-10/source-clarity`.

## Starting point and scope

Continued the supplied Emergent Insights alpha.4 archive, exact source tree `a6cdfbf32e2b5d7a9803b9de94a3b729d847c1f6`. The local comparison baseline is `7d6e144a8450cea090cc832ede44a2b3a5857ac0`; it is not a pushed commit. Its unchanged 672-test baseline passed before implementation. GitHub PR #2 was read through the connected tool and remained draft/unmerged at `824ca6421ff3100e1af596347f2d1247dde8f8dc`. Earlier local source-write denial was not bypassed.

This bounded sprint advances B02-10 and B02-14: exact source mentions, explicit identity judgement, civil-time interpretation, previewed schedule application and complete interpretation history. The black workspace is integrated with existing evidence, actor records, Source Desk origins and case changes. No extra product lane or AI provider was introduced.

## Implemented and tested

The new ENDSTATE civil-time helper has no application or model dependencies. It requires explicit timezone/reference-date input and tests gaps, folds, fractional offsets and invalid dates. The application review service retains quotes and decisions separately, never merges actors, and only applies a deadline through a paired journal/case transaction. Existing observed meanings and completed actions remain immutable. Negative identity decisions and later judgements retain their original reasons.

Preview isolation, rollback, idempotency, concurrency, stale context, source retraction, real approval invalidation, original-source lineage and review/case audit linking are covered. A same-name pair remains two actors. Changing text in the preview clears its apply control. A retracted source flags its interpretation without silently cancelling an adopted deadline.

Actual final counts are in `docs/evidence/source-clarity-local-verification.json`. Browser results come from the real application, API and SQLite through the explicit in-memory ASGI bridge. Native navigation was attempted and failed with `net::ERR_BLOCKED_BY_ADMINISTRATOR` at the local application URL. No alternate hostname, browser policy change or remote write route was used. No new native CI, actual model inference, paid API call, production security certification or merge is claimed.

## Emergence Review

**What did this sprint reveal that we had not properly seen before?**

- EM-038: an identity match belongs to a particular source mention, not an automatic equivalence between every same-name record. Adopted as bounded source-linked judgement under B02-10/B02-14.
- EM-039: interpreting date wording and adopting an operational deadline are separate decisions. Adopted as preview then explicit case amendment, not a new factual observation.
- EM-040: civil time may identify zero, one or two instants. Adopted as explicit timezone/anchor/fold handling in the reusable helper, not guessed parser behaviour.
- EM-041: withdrawing a source must trigger review of an adopted constraint, not necessarily erase it. Adopted as visible attention state and preserved scheduling history.
- EM-042: an exact selected phrase can still hide context. Adopted by displaying surrounding source wording and exact original offsets, retaining negation and attribution for human inspection.
- EM-043: business-day and end-of-day expressions need explicit calendars and organisational rules. Deferred and retained for owner review; no jurisdiction calendar is silently invented.

Existing EM-019, EM-020, EM-021, EM-022 and EM-035 remain applicable: source lineage, validation versus semantics, distinct review/evidence states, preserved history and case-switch isolation. Prior discoveries and declined items were not removed. The register grows from 37 to 43 entries. No broad model-quality or production gate is ticked off by this deterministic workflow.

## Next work

Integrate the cumulative source and run all eight native browser suites. Keep B02-10/B02-14 partial until multi-source professional interpretation and richer reconciliation meet their acceptance criteria. Resume the unchanged B02-09 source-to-plan and B02-11/B02-12 independent/full real-provider gates when an authorised provider is available. Review accessibility and operator usefulness before V0.2 acceptance; V0.3 remains the secure agency pilot, not a renamed alpha.
