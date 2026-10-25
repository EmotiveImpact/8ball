# 8BALL + ENDSTATE changelog

> Generated from `docs/delivery/changelog.json`. Update that source, then run `python scripts/changelog.py --write`. The in-app What’s new page reads the same entries.

This is product history, not the case decision trail. A build entry is not evidence of a merge, deployment or production-model approval.

## 0.2.0-alpha.8 · Review incoming changes through the browser

2026-10-25 · `local_unreleased`

Show original source/output, author a reviewed amendment in Plan Studio, preview effects and commit explicitly with recoverable session handling.

### Added

- Case-scoped review page and permission-checked preview endpoint.
- Twelfth native browser suite with original source, read-only, stale, lost acknowledgement and mobile checks.

### Changed

- Plan Studio can omit its separate live-review shortcut when embedded in event review.

### Verification

- 27 standalone native browser checks passed; full native validation pending.
- Initial incorrect fieldset assertion is preserved and replaced with actual disabled-control assertions.

### Limitations

- Development account-token flow only; real OIDC sign-in and genuine human acceptance remain unfinished.
- No authenticated worker dispatch, external send or production isolation.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Lost acknowledgement is an unknown outcome, not permission to retry.
- Discovery: Disabled-state tests must inspect actual interactive descendants.
- Risk: Late responses must not restore sensitive material after locking.
- Architecture: Session epochs, explicit refresh, existing editor semantics and a case-scoped transactional preview.
- Roadmap decision: existing_task: advance browser event review while retaining all production/model/human gates.
Registered discoveries: EM-108, EM-109.

Roadmap items: `B03-01`, `ES02-03`, `ES02-04`.

Evidence: [docs/delivery/sessions/2026-10-25-endstate-review-ui.md](docs/delivery/sessions/2026-10-25-endstate-review-ui.md), [docs/evidence/event-review-browser-first-failure-2026-10-25.json](docs/evidence/event-review-browser-first-failure-2026-10-25.json), [web/v2/event-review.js](web/v2/event-review.js).

## 0.2.0-alpha.8 · Verify authenticated event review and case-binding correction

2026-10-25 · `local_unreleased`

Record corrected full native evidence while retaining the separately demonstrated same-matter failure.

### Added

- Source-bound corrected native receipt.

### Changed

- Both product trackers, entry page and handoff now reference the verified API checkpoint.

### Verification

- 1345 source /1345 installed-engine /396 native browser checks passed; exact inspection and both checkpoint CI workflows passed.
- 65 focused API/event/review/lifecycle tests passed.

### Limitations

- No inferred historical ownership or automatic replay.
- Browser review, worker, production and original human/model gates remain unfinished.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Two cases may share a matter and revision. An attempt storing only matter scope and base revision can then be consumed by either case. The existing full native suite passed while an additional reproduction demonstrated this missing lineage constraint.
- Risk: Matching matter/revision alone can conceal wrong-case lineage.
- Architecture: Explicit case binding at enqueue; preserve unknown identity in historical rows.
- Roadmap decision: existing_task: correct demonstrated ES02 lineage gap.
Registered discoveries: EM-106, EM-107.

Roadmap items: `ES02-02`, `ES02-03`.

Evidence: [docs/evidence/endstate-event-api-native-2026-10-25.json](docs/evidence/endstate-event-api-native-2026-10-25.json), [docs/delivery/sessions/2026-10-25-endstate-event-api.md](docs/delivery/sessions/2026-10-25-endstate-event-api.md).

## 0.2.0-alpha.8 · Bind reviewed processing to its intended case

2026-10-25 · `local_unreleased`

Correct demonstrated cross-case consumption within one matter by binding new case attempts explicitly.

### Added

- Nullable historical case-binding migration and cross-case/migration regressions.

### Changed

- Unbound attempts remain retained but cannot create case changes.

### Fixed

- An unbound result could previously commit against a different same-matter case at a matching revision.

### Verification

- Preserved prior native pass and separate failing correctness reproduction; focused/full correction validation follows.

### Limitations

- No inferred historical ownership or automatic replay.
- Browser review, worker, production and original human/model gates remain unfinished.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Two cases may share a matter and revision. An attempt storing only matter scope and base revision can then be consumed by either case. The existing full native suite passed while an additional reproduction demonstrated this missing lineage constraint.
- Risk: Matching matter/revision alone can conceal wrong-case lineage.
- Architecture: Explicit case binding at enqueue; preserve unknown identity in historical rows.
- Roadmap decision: existing_task: correct demonstrated ES02 lineage gap.
Registered discoveries: EM-107.

Roadmap items: `ES02-02`, `ES02-03`.

Evidence: [docs/evidence/endstate-event-api-case-binding-gap-2026-10-25.json](docs/evidence/endstate-event-api-case-binding-gap-2026-10-25.json), [docs/delivery/sessions/2026-10-25-endstate-event-api.md](docs/delivery/sessions/2026-10-25-endstate-event-api.md).

## 0.2.0-alpha.8 · Connect reviewed ENDSTATE events to authenticated API

2026-10-25 · `local_unreleased`

Expose explicit source/result review and local notice delivery through signed identity and transactional permission checks.

### Added

- Event detail/review and notice pull/acknowledgement routes for shared-registry agency mode.
- Signed API regression coverage for identity spoofing, scope, stale/cancelled work and revoked permissions.

### Changed

- HTTP review explicitly requires current read and write permission.

### Verification

- Focused and cumulative native validation pending.

### Limitations

- No browser review screen, OIDC browser login, worker daemon, production isolation or external send.
- No actual-model or genuine independent/human acceptance.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: A route guard may pass before a grant is revoked, and a separate registry cannot participate in the case transaction. A write response containing source/result provenance also requires current read access, even when write permission is present.
- Risk: A successful route guard alone is not transaction-wide authority.
- Architecture: Shared registry/case database and read/write revalidation in review commit.
- Roadmap decision: existing_task: advance authenticated review without relaxing production gates.
Registered discoveries: EM-106.

Roadmap items: `B03-01`, `ES02-03`, `ES02-04`.

Evidence: [docs/delivery/sessions/2026-10-25-endstate-event-api.md](docs/delivery/sessions/2026-10-25-endstate-event-api.md), [eightball/v2/event_api.py](eightball/v2/event_api.py).

## 0.2.0-alpha.8 · Verify durable local delivery against full native suite

2026-10-25 · `local_unreleased`

Record exact-source native and checkpoint CI evidence for the local transactional outbox.

### Added

- Source-bound verification receipt.

### Changed

- Current handoff, tracker evidence and entry page now point to the verified outbox checkpoint.

### Verification

- 1331 source /1331 installed-engine /396 native browser checks passed; exact inspection and both checkpoint CI workflows passed.
- 40 focused event/review/outbox tests passed.

### Limitations

- No daemon, browser integration, external delivery, PostgreSQL isolation or historical backfill.
- No model or human acceptance.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: A committed graph review can be lost to downstream readers if notice creation occurs after its transaction. Atomic creation plus independent durable per-reader acknowledgement survives restarts, but repeats remain possible and acknowledgement cannot carry execution authority.
- Risk: Repeated delivery is expected until acknowledgement.
- Architecture: Case/review/outbox share one local transaction.
- Roadmap decision: existing_task: advance ES02 while preserving unfinished acceptance gates.
Registered discoveries: EM-105.

Roadmap items: `ES02-02`, `ES02-04`.

Evidence: [docs/evidence/endstate-outbox-native-2026-10-25.json](docs/evidence/endstate-outbox-native-2026-10-25.json), [docs/delivery/sessions/2026-10-25-endstate-outbox.md](docs/delivery/sessions/2026-10-25-endstate-outbox.md).

## 0.2.0-alpha.8 · Persist reviewed change notices with per-reader delivery

2026-10-25 · `local_unreleased`

Create local notices atomically with reviewed graph commits and retain ordered, permission-checked delivery acknowledgements.

### Added

- Transactional outbox and per-reader restart-safe delivery.
- Rollback, concurrency, ordering, revocation and tampering regressions.

### Verification

- Focused and cumulative native validation pending.

### Limitations

- No daemon, browser integration, external delivery, PostgreSQL isolation or historical backfill.
- No model or human acceptance.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: A committed graph review can be lost to downstream readers if notice creation occurs after its transaction. Atomic creation plus independent durable per-reader acknowledgement survives restarts, but repeats remain possible and acknowledgement cannot carry execution authority.
- Risk: Repeated delivery is expected until acknowledgement.
- Architecture: Case/review/outbox share one local transaction.
- Roadmap decision: existing_task: advance ES02 while preserving unfinished acceptance gates.
Registered discoveries: EM-105.

Roadmap items: `ES02-02`, `ES02-04`.

Evidence: [docs/delivery/sessions/2026-10-25-endstate-outbox.md](docs/delivery/sessions/2026-10-25-endstate-outbox.md), [eightball/v2/event_outbox.py](eightball/v2/event_outbox.py).

## 0.2.0-alpha.8 · Verify reviewed consumption and clarify the current entry point

2026-10-25 · `local_unreleased`

Record source-bound native evidence and preserve historical entry notes in an archive.

### Added

- Source-bound acceptance receipt.

### Changed

- START-HERE now links the standing goal, current tracker and original requirements; previous entry text preserved unchanged.

### Verification

- 1323 source /1323 installed-engine /396 native browser checks passed; exact inspection and checkpoint CI passed.

### Limitations

- Authenticated reviewer identity is supplied by trusted host; public agency writes remain disabled.
- No PostgreSQL tenant policies, automatic worker/outbox, live model or genuine human/independent acceptance.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Review provenance and permission must be bound to the actual transaction, not just the preceding processing attempt.
- Risk: A grant can expire during calculation; a rehashed receipt alone must not substitute original results or explanations.
- Architecture: Single local database transaction, explicit review request hash, conditional case-chain-linked export and a final expiry check.
- Roadmap decision: existing_task: advance ES02-03 without exposing incomplete agency write routes or claiming production acceptance.
Registered discoveries: EM-104.

Roadmap items: `ES02-02`, `ES02-03`, `ES02-04`.

Evidence: [docs/evidence/endstate-reviewed-consumption-native-2026-10-25.json](docs/evidence/endstate-reviewed-consumption-native-2026-10-25.json), [docs/delivery/sessions/2026-10-25-endstate-reviewed-consumption.md](docs/delivery/sessions/2026-10-25-endstate-reviewed-consumption.md).

## 0.2.0-alpha.8 · Commit reviewed event graph amendments atomically

2026-10-25 · `local_unreleased`

Bind explicit reviewed graph changes to original events/results and current case revision/permission in a single local transaction.

### Added

- Local reviewed-consumption service and conditional case export records.
- Tests for duplicate/concurrent consumption, stale revisions, scope/permission denial, rollback, expiry during calculation and provenance tampering.

### Changed

- ES02-03 now partial; existing graph validation, approval invalidation and change explanations are reused.

### Verification

- 32 focused event/review/lifecycle tests passed; cumulative native validation pending.

### Limitations

- Authenticated reviewer identity is supplied by trusted host; public agency writes remain disabled.
- No PostgreSQL tenant policies, automatic worker/outbox, live model or genuine human/independent acceptance.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Review provenance and permission must be bound to the actual transaction, not just the preceding processing attempt.
- Risk: A grant can expire during calculation; a rehashed receipt alone must not substitute original results or explanations.
- Architecture: Single local database transaction, explicit review request hash, conditional case-chain-linked export and a final expiry check.
- Roadmap decision: existing_task: advance ES02-03 without exposing incomplete agency write routes or claiming production acceptance.
Registered discoveries: EM-104.

Roadmap items: `ES02-02`, `ES02-03`, `ES02-04`.

Evidence: [docs/delivery/sessions/2026-10-25-endstate-reviewed-consumption.md](docs/delivery/sessions/2026-10-25-endstate-reviewed-consumption.md), [eightball/v2/event_reviews.py](eightball/v2/event_reviews.py).

## 0.2.0-alpha.8 · Verify durable processing and corrected review recovery

2026-10-25 · `local_unreleased`

Record passing cumulative software evidence after retaining and fixing the observed Plan Review race.

### Added

- Source-bound passing receipt linked to the original failed run.

### Changed

- Canonical tracker and handoff record the next reviewed case-transaction boundary.

### Verification

- 1309 source and1309 installed-engine tests passed.
- 396 native browser checks across11 suites passed.
- Exact source/artifact inspection valid before receipt edits; both checkpoint CI workflows passed.

### Limitations

- No independent review or model/human acceptance.
- Durable processing still requires actual transactional case integration.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Discarding stale data must also resolve pending user-interface states.
- Risk: Intermittent refresh ordering can leave an inaccessible review despite green CI elsewhere.
- Architecture: Bind completion/error handling to dialog ownership and revision; manual reopening only.
- Roadmap decision: existing_task: preserve demonstrated failure and add deterministic native coverage.
Registered discoveries: EM-102, EM-103.

Roadmap items: `ES02-02`, `ES02-04`, `B02-11`.

Evidence: [docs/evidence/endstate-processing-native-2026-10-25.json](docs/evidence/endstate-processing-native-2026-10-25.json), [docs/delivery/sessions/2026-10-25-endstate-processing.md](docs/delivery/sessions/2026-10-25-endstate-processing.md), [docs/evidence/endstate-processing-failed-2026-10-25.json](docs/evidence/endstate-processing-failed-2026-10-25.json).

## 0.2.0-alpha.8 · Resolve stale Plan Review loading after a case refresh

2026-10-25 · `local_unreleased`

Fix the race demonstrated during cumulative validation without publishing stale review results or automatically retrying.

### Added

- Deterministic native in-flight revision-change checks and retained failed-run receipt.

### Changed

- Context changes now show a manual reopen action instead of endless review loading.

### Verification

- First cumulative run failed in native Plan Review; exact inspection valid/failed.
- After correction all35 focused native Plan Review checks passed; cumulative rerun follows.

### Limitations

- No independent review or model/human acceptance.
- Durable processing still requires actual transactional case integration.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Discarding stale data must also resolve pending user-interface states.
- Risk: Intermittent refresh ordering can leave an inaccessible review despite green CI elsewhere.
- Architecture: Bind completion/error handling to dialog ownership and revision; manual reopening only.
- Roadmap decision: existing_task: preserve demonstrated failure and add deterministic native coverage.
Registered discoveries: EM-103.

Roadmap items: `B02-11`, `ES02-04`.

Evidence: [docs/evidence/endstate-processing-failed-2026-10-25.json](docs/evidence/endstate-processing-failed-2026-10-25.json), [docs/delivery/sessions/2026-10-25-endstate-processing.md](docs/delivery/sessions/2026-10-25-endstate-processing.md), [tests/browser_plan_review.py](tests/browser_plan_review.py).

## 0.2.0-alpha.8 · Add durable event-processing attempts and cancellation

2026-10-25 · `local_unreleased`

Persist explicit processing attempts with exclusive claims, bounded leases, cancellation and revision/permission disposition.

### Added

- Durable processing lifecycle bound to an existing scoped inbox record.
- Tests for restart, duplicate claims, cancellation, expiry, stale results and revoked permission.

### Changed

- ES02-04 now partial; all remaining acceptance and integration requirements stay open.

### Verification

- 18 focused inbox/lifecycle tests passed; cumulative validation pending.

### Limitations

- Trusted host must supply authenticated scope and current revision/permission observations; no public API is installed.
- No worker daemon/outbox, automatic model call, case mutation or production transactional isolation.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Expired processing leases cannot establish whether a remote request was executed.
- Risk: Silent reclamation can repeat paid or irreversible operations.
- Architecture: Explicit attempts and interruption; late results cannot publish after cancellation.
- Roadmap decision: existing_task: advance ES02-02/04 while preserving unfinished gates.
Registered discoveries: EM-102.

Roadmap items: `ES02-02`, `ES02-04`.

Evidence: [docs/delivery/sessions/2026-10-25-endstate-processing.md](docs/delivery/sessions/2026-10-25-endstate-processing.md), [eightball/event_work.py](eightball/event_work.py).

## 0.2.0-alpha.8 · Verify ENDSTATE inbox and shared build tracking

2026-10-25 · `local_unreleased`

Record cumulative native and checkpoint CI results for the durable inbox and written build goal.

### Added

- Source-bound event-inbox verification receipt.

### Changed

- Both product trackers link the verified increment and retain unfinished gates.

### Verification

- 1302 source tests and1302 installed-engine regressions passed.
- 394 native browser checks across11 suites passed.
- Exact source/artifact inspection valid before final receipt edits; both checkpoint CI workflows passed.

### Limitations

- No live connectors, durable worker/outbox, reviewed case commits or automatic replanning yet.
- 8BALL accounts, vault, collaboration, production and genuine model/human acceptance remain unfinished.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Occurrence time and receipt order are separate; retries must retain their original receipt.
- Risk: Automatic replay could wrongly reauthorise work if connected directly to commands.
- Architecture: Pure kernel contract; database remains in host. Scope asserted before append.
- Roadmap decision: existing_task: ES02-01/02 increment, no acceptance or deployment promotion.
Registered discoveries: EM-101.

Roadmap items: `ES02-01`, `ES02-02`, `DOC-06`.

Evidence: [docs/evidence/endstate-event-inbox-native-2026-10-25.json](docs/evidence/endstate-event-inbox-native-2026-10-25.json), [docs/delivery/sessions/2026-10-25-endstate-event-inbox.md](docs/delivery/sessions/2026-10-25-endstate-event-inbox.md), [docs/delivery/BUILD-GOAL.md](docs/delivery/BUILD-GOAL.md).

## 0.2.0-alpha.8 · Build the ENDSTATE event contract and durable host inbox

2026-10-25 · `local_unreleased`

Retain scoped incoming events with duplicate/conflict handling and durable arrival order; publish one explicit build goal and refresh both product trackers.

### Added

- Neutral pending-event/receipt contracts and SQLite host inbox.
- Eleven tests for restart, concurrent duplicates, changed retries, delayed events, scope and corruption.
- BUILD-GOAL.md with completion criteria and links to canonical status.

### Changed

- ES02-01/02 now partial; current branch/PR and next tasks refreshed without erasing prior inspections.

### Verification

- 11 focused event/inbox tests passed; cumulative native verification pending.

### Limitations

- No live connectors, durable worker/outbox, reviewed case commits or automatic replanning yet.
- 8BALL accounts, vault, collaboration, production and genuine model/human acceptance remain unfinished.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Occurrence time and receipt order are separate; retries must retain their original receipt.
- Risk: Automatic replay could wrongly reauthorise work if connected directly to commands.
- Architecture: Pure kernel contract; database remains in host. Scope asserted before append.
- Roadmap decision: existing_task: ES02-01/02 increment, no acceptance or deployment promotion.
Registered discoveries: EM-101.

Roadmap items: `ES02-01`, `ES02-02`, `DOC-06`.

Evidence: [docs/delivery/sessions/2026-10-25-endstate-event-inbox.md](docs/delivery/sessions/2026-10-25-endstate-event-inbox.md), [docs/endstate/EVENT-INBOX.md](docs/endstate/EVENT-INBOX.md), [docs/delivery/BUILD-GOAL.md](docs/delivery/BUILD-GOAL.md).

## 0.2.0-alpha.8 · Verify agency access and publish the clearer overview

2026-10-25 · `local_unreleased`

Record cumulative native verification, checkpoint CI and final uncertainty wording correction.

### Added

- Source-bound verification receipt and owner-accessible overview screenshot.

### Changed

- Display unknown and disputed counts separately.

### Verification

- 1291 source +1291 installed-engine +394 native browser checks passed on7fbb34a.
- Both checkpoint CI workflows passed; exact artifact/source inspection valid.
- Final wording passed node syntax and54 native workspace checks.

### Limitations

- No live OIDC browser login/MFA, PostgreSQL row enforcement, write/worker authorisation or production acceptance.
- Remaining roadmap steps and V0.2 actual-model/human gates remain open.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Authenticated identity alone cannot protect aggregate and asynchronous local routes.
- Risk: Grant revocation must span transaction/worker paths; in-flight responses cannot be recalled.
- Architecture: Explicit deny-by-default opt-in boundary, no client-created grants or silent migrations.
- Roadmap decision: existing_task: continue B03-01 and B02-19; no production deployment or gate promotion.
Registered discoveries: EM-100.

Roadmap items: `B03-01`, `B02-19`.

Evidence: [docs/evidence/agency-api-overview-native-2026-10-25.json](docs/evidence/agency-api-overview-native-2026-10-25.json), [docs/delivery/sessions/2026-10-25-agency-api-overview.md](docs/delivery/sessions/2026-10-25-agency-api-overview.md), [docs/screenshots/8ball-overview-2026-10-25.png](docs/screenshots/8ball-overview-2026-10-25.png).

## 0.2.0-alpha.8 · Add authenticated agency read access and a clearer Situation Room

2026-10-25 · `local_unreleased`

Persist scoped grants, validate signed issuer/audience-bound tokens and enforce an opt-in API read boundary; lead the workspace with a plain-language summary.

### Added

- Persistent registry, RS256 token validation and API denial tests.
- Situation summary, evidence/change links and keyboard-expandable graph.

### Changed

- Agency mode denies all unintegrated routes; local mode remains compatible.

### Verification

- 24 focused policy/API tests passed.
- Initial native workspace journey passed 51 checks; new disclosure checks and cumulative run follow.

### Limitations

- No live OIDC browser login/MFA, PostgreSQL row enforcement, write/worker authorisation or production acceptance.
- Remaining roadmap steps and V0.2 actual-model/human gates remain open.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Authenticated identity alone cannot protect aggregate and asynchronous local routes.
- Risk: Grant revocation must span transaction/worker paths; in-flight responses cannot be recalled.
- Architecture: Explicit deny-by-default opt-in boundary, no client-created grants or silent migrations.
- Roadmap decision: existing_task: continue B03-01 and B02-19; no production deployment or gate promotion.
Registered discoveries: EM-100.

Roadmap items: `B03-01`, `B02-19`.

Evidence: [docs/delivery/sessions/2026-10-25-agency-api-overview.md](docs/delivery/sessions/2026-10-25-agency-api-overview.md), [docs/v2/AGENCY-ACCESS.md](docs/v2/AGENCY-ACCESS.md).

## 0.2.0-alpha.8 · Publish the current workspace screenshot for owner review

2026-10-25 · `local_unreleased`

Make the actual local workspace screenshot accessible on GitHub at the owner request.

### Added

- docs/screenshots/8ball-situation-room-2026-10-25.png

### Verification

- Screenshot captured from native Chromium against the local application with fictional test data.
- The screenshot capture journey passed 51 workspace checks.

### Limitations

- Screenshot is not human acceptance, real-model evidence or a production deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: No new product finding; publish existing fictional workspace evidence for owner access.
- Risk: A screenshot must not imply production or model acceptance.
- Architecture: None; application source unchanged.
- Roadmap decision: no_action: evidence publication only; no task status changes.
Registered discoveries: EM-099.

Roadmap items: `B03-01`.

Evidence: [docs/screenshots/8ball-situation-room-2026-10-25.png](docs/screenshots/8ball-situation-room-2026-10-25.png), [docs/delivery/sessions/2026-10-25-agency-authorisation.md](docs/delivery/sessions/2026-10-25-agency-authorisation.md).

## 0.2.0-alpha.8 · Verify agency policy foundation against existing workflows

2026-10-25 · `local_unreleased`

Record cumulative native software verification without claiming production enforcement.

### Added

- Source-bound native verification receipt.

### Verification

- 1280 source tests and 1280 installed-engine regressions passed.
- 391 native browser checks across all eleven suites passed.
- Exact source/artifact inspection valid before receipt edits.

### Limitations

- Not connected to the local API. No OIDC, persistent membership, PostgreSQL row policy or production isolation claim.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Object grants must not expand into aggregate matter operations.
- Risk: Policy-only tests do not prove request or transaction enforcement.
- Architecture: Use verified identity and server-owned membership; enforce all consumed objects.
- Roadmap decision: Proceed with B03-01 under explicit full-product scope; no production deployment.
Registered discoveries: EM-099.

Roadmap items: `B03-01`.

Evidence: [docs/evidence/agency-authorisation-native-2026-10-25.json](docs/evidence/agency-authorisation-native-2026-10-25.json), [docs/delivery/sessions/2026-10-25-agency-authorisation.md](docs/delivery/sessions/2026-10-25-agency-authorisation.md).

## 0.2.0-alpha.8 · Begin the agency permission foundation

2026-10-25 · `local_unreleased`

Owner authorised the full product roadmap; add exact issuer/subject, tenant/matter/object and operation-scoped permission calculation.

### Added

- Immutable identity/resource/grant records and deny-by-default policy.
- 13 denial tests covering all six operations, foreign scopes, revocation, expiry and read-only object grants.

### Changed

- B03-01 is partial; existing V0.2 acceptance remains unchanged.

### Verification

- 13 policy tests passed; cumulative native verification follows.

### Limitations

- Not connected to the local API. No OIDC, persistent membership, PostgreSQL row policy or production isolation claim.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Object grants must not expand into aggregate matter operations.
- Risk: Policy-only tests do not prove request or transaction enforcement.
- Architecture: Use verified identity and server-owned membership; enforce all consumed objects.
- Roadmap decision: Proceed with B03-01 under explicit full-product scope; no production deployment.
Registered discoveries: EM-099.

Roadmap items: `B03-01`.

Evidence: [docs/delivery/sessions/2026-10-25-agency-authorisation.md](docs/delivery/sessions/2026-10-25-agency-authorisation.md), [tests/test_authorisation.py](tests/test_authorisation.py).

## 0.2.0-alpha.8 · Combined build passes native verification and checkpoint CI

2026-10-25 · `local_unreleased`

Record current cumulative software evidence and resolve already-integrated PR3; preserve all actual-model and human gates.

### Added

- Source-bound verification receipt with all eleven native browser suites and checkpoint CI results.

### Changed

- Canonical integration evidence now records completed software verification; final merge is tracked by PR4.

### Verification

- 1267 source tests and 1267 installed-engine regressions passed.
- 391 native browser checks across all eleven suites passed.
- Source/artifact inspection valid before documentation-only receipt edits.
- GitHub validation 40199806937 and documentation 40199807143 passed on a9254e6087ef606d581d626bfcda9d7e555c857e.

### Limitations

- No model generation, independent professional or human acceptance claimed.
- No deployment, release tag or research runtime adoption.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Existing source/evidence and secret-delivery findings apply; an open PR can already be integrated by ancestry.
- Risk: Stale PR targets, uncertain authentication causes and generic UI errors can mislead the next agent.
- Architecture: Preserve all source, frozen gates and case authority while consolidating delivery.
- Roadmap decision: Existing-task integration under ADR0007; no required task/status changes.
Registered discoveries: EM-051, EM-071, EM-098.

Roadmap items: `B02-09`, `B02-15`, `ES03-05`, `DOC-06`.

Evidence: [docs/evidence/build-consolidation-native-2026-10-25.json](docs/evidence/build-consolidation-native-2026-10-25.json), [docs/delivery/sessions/2026-10-25-build-consolidation.md](docs/delivery/sessions/2026-10-25-build-consolidation.md), [docs/delivery/NEXT-BUILD.md](docs/delivery/NEXT-BUILD.md).

## 0.2.0-alpha.8 · Owner-requested combined build and executable test handoff

2026-10-25 · `local_unreleased`

Consolidate completed development and resolve stale PR bookkeeping under explicit owner authority; retain all model and human gates.

### Added

- ADR0007 and NEXT-BUILD.md with exact software/provider/lifecycle commands and independent/human review boundaries.
- Preserved October25 authentication observation, without asserting an unproved root cause.

### Changed

- Integration branch contains all prior development; canonical next action is the prepared actual-provider test handoff.

### Verification

- Git ancestry confirms main is an ancestor of development and PR3 head already exists in main.
- Fresh cumulative native verification pending at this checkpoint.

### Limitations

- No model generation, independent professional or human acceptance claimed.
- No deployment, release tag or research runtime adoption.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Existing source/evidence and secret-delivery findings apply; an open PR can already be integrated by ancestry.
- Risk: Stale PR targets, uncertain authentication causes and generic UI errors can mislead the next agent.
- Architecture: Preserve all source, frozen gates and case authority while consolidating delivery.
- Roadmap decision: Existing-task integration under ADR0007; no required task/status changes.
Registered discoveries: EM-051, EM-071, EM-098.

Roadmap items: `B02-09`, `B02-15`, `ES03-05`, `DOC-06`.

Evidence: [docs/delivery/sessions/2026-10-25-build-consolidation.md](docs/delivery/sessions/2026-10-25-build-consolidation.md), [docs/decisions/0007-owner-build-consolidation.md](docs/decisions/0007-owner-build-consolidation.md), [docs/delivery/NEXT-BUILD.md](docs/delivery/NEXT-BUILD.md), [docs/evidence/anthropic-authentication-2026-10-25.json](docs/evidence/anthropic-authentication-2026-10-25.json).

## 0.2.0-alpha.8 · Anthropic test configuration and secure key-entry instructions

2026-10-18 · `pushed_unreleased`

Prepared owner-selected Anthropic connection settings and exact existing-key destination instructions without claiming live compatibility or changing acceptance.

### Added

- Beginner Anthropic setup guide, source/configuration receipt and full Emergence Review.

### Changed

- Saved non-secret model/provider/URL suggestions and added api.anthropic.com to custom network destinations.
- Canonical next actions identify selected Anthropic and missing owner key/destination activation.

### Verification

- 142 existing controlled transport/CLI tests passed in 1.30s; isolated fictional-key format/status check used no DNS or HTTP.
- 60 continuity tests passed in 1.37s (one existing Starlette/AnyIO deprecation warning); append-only history and canonical generator checks passed.
- Official SDK source lists claude-sonnet-4-6; official compatibility-documentation access was blocked by the inherited proxy (HTTP403), without an origin response.
- No new native run is claimed. Independent agent source/guide review is engineering review, not independent professional acceptance.

### Limitations

- Existing EIGHTBALL_API_KEY secret is still destination-bound to the old Qwen service. Automatic retarget was rejected; owner must edit that row, enter key securely and Save/Publish. No duplicate secret was added.
- Actual Anthropic compatibility/schema enforcement, account model access/pricing and active settings remain unverified; zero live model calls.
- No application code, tests, dependencies, original PRD, frozen fixtures or task scope/statuses changed; independent/human acceptance remains open.
- No SDK/runtime installation, model download, spending, main merge, release or deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-098: visible provider settings and managed key destination must be changed separately.
- Risk: A valid setting format/SDK model listing can be mistaken for active access, remote structured-output enforcement or successful inference.
- Architecture: Keep server-owned explicit provider identity, secret destination restrictions and unchanged local compilation/approval gates.
- Roadmap decision: Refine existing provider/setup tasks; retain every original acceptance requirement/status and all earlier discoveries.
Registered discoveries: EM-098, EM-051, EM-085.

Roadmap items: `B02-09`, `B02-15`, `ES03-05`, `DOC-06`.

Evidence: [docs/delivery/sessions/2026-10-18-anthropic-configuration.md](docs/delivery/sessions/2026-10-18-anthropic-configuration.md), [docs/evidence/anthropic-setup-2026-10-18.json](docs/evidence/anthropic-setup-2026-10-18.json), [docs/v2/ANTHROPIC-SETUP.md](docs/v2/ANTHROPIC-SETUP.md).

## 0.2.0-alpha.8 · Verified source-stable evaluation and review-record checkpoint

2026-10-18 · `pushed_unreleased`

Cumulative native software verification passed for source-stable generation receipts, lifecycle prerequisites and optional prospective recording. Real-model and genuine independent/human acceptance remain open.

### Added

- Source-bound final receipt for tested code 25ca5e2dce4f28ec33d9b132cccabfa15b23683e, all eleven native suites and the actual unpopulated research checkout state.

### Changed

- Current canonical sprint evidence and next-agent handoff identify the verified development source while retaining every prior checkpoint and all 97 discoveries.

### Verification

- 1,267 source tests, 1,267 installed-kernel regressions and 391 native browser checks across all 11 suites passed; exact-source/artifact inspection valid before final documentation edits.
- 138 focused controlled tests passed; independent agent engineering review found no blocking issue. These overlap the cumulative tests and are not professional acceptance.
- Compilation, 17 JavaScript modules, eight structural fixture cases, internal package/schema export and append-only continuity guards passed.
- Original PRD, frozen generation bytes, compiler, semantic protocol, v1 review forms and every task scope/status remain unchanged.

### Limitations

- Exact service/model/active secure key, actual-model results, genuine independent study and human acceptance remain missing.
- Source checks bracket fixtures/final result, not every internal graph stage or every instant; source fingerprints do not prove loaded-code identity.
- Mechanical recording consistency does not authenticate declarations or establish held-out scientific adequacy. Existing manual v1 studies remain legitimate.
- Research source bodies are unpopulated in this restored checkout; no upstream runtime adoption, further main merge, release or deployment.
- Compatible receipts identify endpoint host, not different API base paths on that host (EM-097 candidate).

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-094: structural success and source-valid evidence need separate outcomes.
- Discovery: EM-095: summary flags alone cannot support returned-call evidence.
- Discovery: EM-096: mechanical study readiness and genuine prospective approval are separate.
- Discovery: EM-097: host-only endpoint identity cannot distinguish service paths; preserve as a candidate.
- Risk: Unauthenticated records, discrete source checks and declared coverage can be overinterpreted as continuous attestation or independent acceptance.
- Architecture: Keep offline evidence tools separate from case authority; retain original compiler, fixtures and semantic protocol.
- Roadmap decision: Refine existing tasks only; preserve every original status/acceptance requirement, prior form and discovery.
Registered discoveries: EM-094, EM-095, EM-096, EM-097.

Roadmap items: `B02-09`, `B02-11`, `B02-12`, `ES03-05`, `DOC-06`.

Evidence: [docs/evidence/review-evidence-native-2026-10-18.json](docs/evidence/review-evidence-native-2026-10-18.json), [docs/delivery/sessions/2026-10-18-review-evidence.md](docs/delivery/sessions/2026-10-18-review-evidence.md), [docs/delivery/review/PROSPECTIVE-RECORDING.md](docs/delivery/review/PROSPECTIVE-RECORDING.md).

## 0.2.0-alpha.8 · Source-stable model evidence and prospective review preparation

2026-10-18 · `local_unreleased`

Protect hosted fixture evidence from observed source drift and prepare optional private prospective study records without claiming model or human acceptance.

### Added

- Optional offline recording-v2 checker and unfilled protocol/dataset templates for the unchanged semantic protocol.

### Changed

- Lifecycle prerequisites require stable matching source and per-fixture returned-call consistency; receipts remain unsigned.
- Canonical progress and continuation records preserve all earlier work and unchanged acceptance statuses.

### Fixed

- Hosted fixtures could report success after their source changed during a controlled response. Observed drift or inspection failure now blocks later fixtures and final evidence success while preserving raw responses and structural results.

### Verification

- 138 focused controlled tests passed in 7.58s; final cumulative native verification pending.
- Independent agent engineering review found no blocking correctness defect; this is not independent professional acceptance.
- Pinned development environment restored; pip check passed. No live provider calls.

### Limitations

- Exact service/model/active secure key, actual-model results, genuine independent study and human acceptance remain missing.
- Source checks bracket fixtures/final result, not every internal graph stage or every instant; source fingerprints do not prove loaded-code identity.
- Mechanical recording consistency does not authenticate declarations or establish held-out scientific adequacy. Existing manual v1 studies remain legitimate.
- Research source bodies are unpopulated in this restored checkout; no upstream runtime adoption, further main merge, release or deployment.
- Compatible receipts identify endpoint host, not different API base paths on that host (EM-097 candidate).

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-094: structural success and source-valid evidence need separate outcomes.
- Discovery: EM-095: summary flags alone cannot support returned-call evidence.
- Discovery: EM-096: mechanical study readiness and genuine prospective approval are separate.
- Discovery: EM-097: host-only endpoint identity cannot distinguish service paths; preserve as a candidate.
- Risk: Unauthenticated records, discrete source checks and declared coverage can be overinterpreted as continuous attestation or independent acceptance.
- Architecture: Keep offline evidence tools separate from case authority; retain original compiler, fixtures and semantic protocol.
- Roadmap decision: Refine existing tasks only; preserve every original status/acceptance requirement, prior form and discovery.
Registered discoveries: EM-094, EM-095, EM-096, EM-097.

Roadmap items: `B02-09`, `B02-11`, `B02-12`, `ES03-05`, `DOC-06`.

Evidence: [docs/delivery/sessions/2026-10-18-review-evidence.md](docs/delivery/sessions/2026-10-18-review-evidence.md), [evals/review_readiness.py](evals/review_readiness.py), [docs/delivery/review/README.md](docs/delivery/review/README.md).

## 0.2.0-alpha.8 · Verified whole-system evaluation-readiness checkpoint

2026-10-16 · `pushed_unreleased`

Whole-system technical direction and bounded evaluation fixes passed cumulative native software verification; all original model and human acceptance gates remain.

### Added

- Exact-source final receipt for tested code 17a275c, 93 retained discoveries and all 28 research pins.

### Changed

- Current sprint metadata now points to the verified development branch; historical main integration and earlier native evidence are retained.

### Verification

- 1,171 source tests, 1,171 installed-kernel regressions and 391 native checks across all 11 suites passed; source/artifact inspection valid. No actual model or independent/human acceptance.
- Python compilation, 17 JavaScript modules, 8 structural cases, internal package/schema export and continuity guards passed.
- Original task scopes/statuses, frozen generation fixture bytes, compiler source and original PRD remained unchanged.

### Limitations

- Zero actual model calls; actual service access, independent study/labels and human reviews remain missing.
- Lifecycle admission timing and omitted discarded responses do not establish remote cancellation or complete provider evidence.
- No deferred runtime adoption, new remote CI claim, main merge, release or deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-085..087: fixed-model identity, durable experiment evidence and separate admission/remote observations.
- Discovery: EM-088..093: document coordinates, telemetry, actor failures, dependency environments, durability/retries and eval mode execution.
- Risk: Framework/model/service success can be mistaken for actual outcome correctness, scope isolation, free entitlement or genuine acceptance.
- Architecture: Keep existing host/engine authority; introduce optional isolated specialists only through measured source-aware contracts.
- Roadmap decision: Existing task engineering/documentation refinements; candidate adapter concerns retained without promoting deferred research into required scope.
Registered discoveries: EM-085, EM-086, EM-087, EM-088, EM-089, EM-090, EM-091, EM-092, EM-093.

Roadmap items: `DOC-06`, `B02-09`, `B02-11`, `B02-12`, `B02-15`, `ES03-05`, `ES03-09`.

Evidence: [docs/strategy/OWNER-TECHNICAL-DIRECTION-2026-10-16.md](docs/strategy/OWNER-TECHNICAL-DIRECTION-2026-10-16.md), [docs/research/github-2026-10-16/whole-system-review.md](docs/research/github-2026-10-16/whole-system-review.md), [docs/evidence/whole-system-readiness-2026-10-16.json](docs/evidence/whole-system-readiness-2026-10-16.json), [docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md](docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md), [docs/v2/ACTUAL-PROVIDER-EVIDENCE.md](docs/v2/ACTUAL-PROVIDER-EVIDENCE.md).

## 0.2.0-alpha.8 · Whole-system direction and retained model evaluation evidence

2026-10-16 · `local_unreleased`

Reviewed all 28 source candidates and chose a lean acceptance-first direction; fixed model-identity configuration and prepared retained generation/lifecycle evidence without model calls.

### Added

- Owner-readable complete disposition matrix, source findings and actual-provider evidence guide.
- Unique immutable generation checkpoints and opt-in cancel/stale/owned-process-restart observations.
- EM-085..093 plus additive history preserving every earlier discovery.

### Changed

- Exact successful assistant text retained only after existing validation; rejected/error/credential boundaries remain.
- Explicit OpenRouter :free catalog variants supported with pinned provider; random free router rejected.

### Fixed

- Repeated hosted runs no longer overwrite earlier experiment reports.
- Lifecycle cleanup terminates its owned process even if client close raises.

### Verification

- Focused controlled suites passed: 160 transport/integration, 68 retention/CLI/hosted-grounding, 89 lifecycle/CLI/integration/job tests including 30 new lifecycle cases; counts overlap.
- All 28 candidate pins reviewed by category; no upstream execution, install, model download or actual inference. Cumulative native verification pending at this code checkpoint.

### Limitations

- Zero actual model calls; endpoint/exact model/secure access remain missing. Existing fictional-only US$5 authorisation is preserved.
- Application admission is not remote delivery; lifecycle races/response loss remain explicit, with no automatic repeat.
- Current B02 remains 10/20 required verified and ES01 5/5 internal; independent professional and genuine human gates remain.
- No deferred runtime adoption, main merge, release or deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-085..087: fixed-model identity, durable experiment evidence and separate admission/remote observations.
- Discovery: EM-088..093: document coordinates, telemetry, actor failures, dependency environments, durability/retries and eval mode execution.
- Risk: Framework/model/service success can be mistaken for actual outcome correctness, scope isolation, free entitlement or genuine acceptance.
- Architecture: Keep existing host/engine authority; introduce optional isolated specialists only through measured source-aware contracts.
- Roadmap decision: Existing task engineering/documentation refinements; candidate adapter concerns retained without promoting deferred research into required scope.
Registered discoveries: EM-085, EM-086, EM-087, EM-088, EM-089, EM-090, EM-091, EM-092, EM-093.

Roadmap items: `DOC-06`, `B02-09`, `B02-11`, `B02-12`, `B02-15`, `ES03-05`, `ES03-09`.

Evidence: [docs/strategy/OWNER-TECHNICAL-DIRECTION-2026-10-16.md](docs/strategy/OWNER-TECHNICAL-DIRECTION-2026-10-16.md), [docs/research/github-2026-10-16/whole-system-review.md](docs/research/github-2026-10-16/whole-system-review.md), [docs/evidence/whole-system-readiness-2026-10-16.json](docs/evidence/whole-system-readiness-2026-10-16.json), [docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md](docs/delivery/sessions/2026-10-16-whole-system-evaluation-readiness.md), [docs/v2/ACTUAL-PROVIDER-EVIDENCE.md](docs/v2/ACTUAL-PROVIDER-EVIDENCE.md).

## 0.2.0-alpha.8 · Ruflo explained with current pinned-source evidence

2026-10-16 · `pushed_unreleased`

Added an owner-readable source investigation of Ruflo worker coordination, model access, confidence and evidence limits. Application behavior and acceptance gates are unchanged.

### Added

- Plain-English owner guide, pinned-source receipt and complete ER-01–15 handoff.
- EM-084 preserves the prediction target behind worker-routing confidence; prior findings receive additive evidence.

### Changed

- Clarified that Ruflo still needs a separately supplied model service and provides no selected free Qwen endpoint for 8BALL.
- Preserved upstream historical audit/remediation dates alongside current unmeasured telemetry and synthetic/live benchmark distinctions.

### Verification

- Read-only source inspection; HTTPS Git remote HEAD/main matched copied commit 1882006a02487590c8c66a7eec8d7504f6af33c3.
- Canonical delivery/emergence/changelog regeneration and base-history checks passed; local documentation links, original scopes/statuses and whitespace checked.

### Limitations

- No installation, upstream execution, model calls or independent benchmark reproduction.
- Previous 1,104/1,104/391 software results belong to tested ddfead7; this documentation review does not rerun or extend those results.
- Ruflo remains optional research; V0.2 real-model and independent/human requirements remain open. No merge or deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-084: confidence/success metrics require an explicit prediction target; worker routing is separate from client-outcome probability.
- Discovery: Additive EM-020/055/077/081 source evidence: actual access/execution, exact model/retry accounting, semantic memory and dated remediation scope.
- Risk: A keyless demo, API-success reward or persuasive swarm dashboard may be mistaken for working free inference or correct scenario decisions.
- Architecture: Keep model access, optional worker coordination, hypothetical simulation and reviewed case authority separate.
- Roadmap decision: Existing DOC-06 documentation refinement and candidate ES03-02/05 evaluation concern; no new required task or runtime adoption.
Registered discoveries: EM-020, EM-055, EM-077, EM-081, EM-084.

Roadmap items: `DOC-06`, `ES03-02`, `ES03-05`.

Evidence: [docs/research/github-2026-10-16/ruflo-owner-guide.md](docs/research/github-2026-10-16/ruflo-owner-guide.md), [docs/evidence/ruflo-owner-review-2026-10-16.json](docs/evidence/ruflo-owner-review-2026-10-16.json), [docs/delivery/sessions/2026-10-16-ruflo-owner-review.md](docs/delivery/sessions/2026-10-16-ruflo-owner-review.md).

## 0.2.0-alpha.8 · Verified hosted transport and pinned research-copy checkpoint

2026-10-16 · `pushed_unreleased`

Source-only copies and the optional hosted API transport passed cumulative native software verification on the development branch. All original V0.2 model and human gates remain open.

### Added

- Source-bound final receipt for tested commit ddfead7 and all 28 declared/checked-out research pins.

### Changed

- ES03-09 is verified only for its explicit controlled transport/software scope. Original B02 remains 10/20 required verified; ENDSTATE V0.1 remains 5/5 internally.
- Owner authorises fictional model tests up to US$5 and expects their supplied endpoint to be free; exact endpoint/model, active secret and actual service limits remain pending.

### Verification

- 1,104 source tests and 1,104 installed-kernel regression tests passed.
- 391 native browser checks passed across all 11 suites; source/evidence inspection valid and run passed.
- All 28 research source checkouts and 128 notice files verified; Git-only population repeatability passed. No upstream software was executed.

### Limitations

- Zero actual model calls; real-model, independent professional and human acceptance remain open.
- Pushed development source is not a main merge, deployment or release. New remote CI is not claimed; branch push is outside configured CI triggers.
- Raw software artifacts remain local; committed receipt preserves hashes/counts. The earlier local checkpoint entry is retained as history.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-082: research source copies require explicit trust/discovery/fingerprint and completeness boundaries.
- Discovery: EM-083: rejection traces need attributed, byte-safe raw evidence and escaped-credential protection.
- Risk: Configuration or controlled HTTP success may be mistaken for actual-model/human acceptance; a captured source tree may be mistaken for an adopted dependency.
- Architecture: Keep optional provider transport in the application host; ENDSTATE compiler/authority semantics unchanged. External source pins are provenance inputs, not runtime imports.
- Roadmap decision: Owner-authorized DOC-07 and optional ES03-09 plus existing gate refinements; all original required acceptance remains.
Registered discoveries: EM-019, EM-020, EM-031, EM-051, EM-054, EM-055, EM-072, EM-073, EM-077, EM-082, EM-083.

Roadmap items: `DOC-07`, `ES03-09`, `B02-09`, `B02-12`, `B02-15`.

Evidence: [docs/evidence/compatible-native-2026-10-16.json](docs/evidence/compatible-native-2026-10-16.json), [docs/evidence/research-copy-2026-10-16.json](docs/evidence/research-copy-2026-10-16.json), [docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md](docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md), [docs/v2/QWEN-SETUP.md](docs/v2/QWEN-SETUP.md).

## 0.2.0-alpha.8 · Hosted Qwen API connection and preserved research sources

2026-10-16 · `local_unreleased`

Added explicit hosted OpenAI-compatible generation through existing review/compilation, and populated all28 inspected repositories as pinned source-only research checkouts.

### Added

- Server-configured hosted API/Qwen transport, UI/setup guide, unchanged-fixture wrapper and actual-journey provider option.
- Pinned research Gitlinks, original notice inventory, Git-only restoration/verification and external-source test/fingerprint boundary.

### Changed

- Actual provider settings use secure environment fields; normal acceptance strips them and never infers. Existing HF/local routes and frozen generation requirements remain.

### Fixed

- Controlled rejected responses retain attributed bounded assistant text with byte-safe credential omission; unsupported output is never silently repaired.

### Verification

- 109 controlled transport,22 SQLite/HTTP lifecycle,4 CLI and36 acceptance-boundary tests passed in focused runs.
- 22 native development browser checks passed; all28 source pins/notices/exceptions verified. Cumulative native acceptance is pending at this code checkpoint.

### Limitations

- Zero actual model calls; selected provider, spending/data scope, independent semantic evaluation and human acceptance remain open.
- Model files/LFS payloads/nested dependencies are explicitly unmaterialized research exceptions; no upstream dependencies or software were run.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-082: research source copies require explicit trust/discovery/fingerprint and completeness boundaries.
- Discovery: EM-083: rejection traces need attributed, byte-safe raw evidence and escaped-credential protection.
- Risk: Configuration or controlled HTTP success may be mistaken for actual-model/human acceptance; a captured source tree may be mistaken for an adopted dependency.
- Architecture: Keep optional provider transport in the application host; ENDSTATE compiler/authority semantics unchanged. External source pins are provenance inputs, not runtime imports.
- Roadmap decision: Owner-authorized DOC-07 and optional ES03-09 plus existing gate refinements; all original required acceptance remains.
Registered discoveries: EM-019, EM-020, EM-031, EM-051, EM-054, EM-055, EM-072, EM-073, EM-077, EM-082, EM-083.

Roadmap items: `DOC-07`, `ES03-09`, `B02-09`, `B02-12`, `B02-15`, `ES03-05`.

Evidence: [docs/evidence/compatible-native-2026-10-16.json](docs/evidence/compatible-native-2026-10-16.json), [docs/evidence/research-copy-2026-10-16.json](docs/evidence/research-copy-2026-10-16.json), [docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md](docs/delivery/sessions/2026-10-16-compatible-provider-research-copy.md), [docs/v2/QWEN-SETUP.md](docs/v2/QWEN-SETUP.md), [research/inventory.json](research/inventory.json).

## 0.2.0-alpha.8 · Ruflo worker-harness assessment and architecture placement

2026-10-16 · `pushed_unreleased`

Assessed the owner-supplied Ruflo project as an optional coordination harness, preserving ENDSTATE outcome/evidence boundaries and identifying semantic-backend validation needs.

### Added

- Pinned source findings/manifest and candidate EM-081; worker-coordinator role in the proposed combined design.

### Changed

- Research register, canonical documentation-task evidence, handoff and emergence history updated additively.

### Verification

- Actual documentation/history/preservation check results are in the source-bound follow-up receipt.

### Limitations

- Source inspection only: no upstream tests, install, provider/model calls or predictive/professional/human acceptance.
- No runtime task requirements/statuses, original PRDs/fixtures or application code changed.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: A vector-shaped hash fallback does not establish semantic retrieval; actual agent execution remains separate from registration and task correctness.
- Risk: A second coordinator can duplicate state and imply completed/validated work from status or consensus alone.
- Architecture: Optional typed worker adapter; case revisions, source facts and human approvals remain authoritative in 8BALL.
- Roadmap decision: candidate and existing_task refinements only; no runtime adoption or required scope promotion.
Registered discoveries: EM-020, EM-031, EM-046, EM-051, EM-054, EM-055, EM-061, EM-075, EM-077, EM-078, EM-081.

Roadmap items: `DOC-02`, `DOC-03`, `DOC-04`, `DOC-05`, `DOC-06`.

Evidence: [docs/evidence/ruflo-research-2026-10-16.json](docs/evidence/ruflo-research-2026-10-16.json), [docs/research/github-2026-10-16/ruflo.md](docs/research/github-2026-10-16/ruflo.md), [docs/delivery/sessions/2026-10-16-evolution-research.md](docs/delivery/sessions/2026-10-16-evolution-research.md).

## 0.2.0-alpha.8 · Tencent memory assessment and combined reference-case strategy

2026-10-16 · `pushed_unreleased`

Assessed the owner-supplied Tencent memory project and sharpened the combined design around one complete case, optional procedural memory and explicit scenario/decision contracts.

### Added

- Pinned Tencent source, contract/operations findings, candidate EM-080 and a six-responsibility architecture proposal.

### Changed

- Research register, plan, canonical documentation-task evidence and handoff updated additively.

### Verification

- Bounded source/configuration/licence inspection; current documentation/history/preservation checks recorded in the follow-up receipt.

### Limitations

- No upstream install/runtime test, inference, benchmark reproduction or independent/human acceptance.
- All runtime task acceptance/status fields remain unchanged. Tencent is a candidate, not an imported feature.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: L2 scenario is a memory narrative; generated procedures, citation ancestry and profile scopes need host-owned review and invalidation contracts.
- Risk: Memory consolidation or model choice confidence may be mistaken for factual proof, validated expertise or route authority.
- Architecture: Keep canonical evidence/approval state in 8BALL and use optional scoped API adapters for derived memory.
- Roadmap decision: new_candidate and existing_task refinements only; no required runtime promotion.
Registered discoveries: EM-019, EM-020, EM-027, EM-046, EM-055, EM-061, EM-063, EM-075, EM-076, EM-077, EM-078, EM-080.

Roadmap items: `DOC-02`, `DOC-03`, `DOC-04`, `DOC-05`, `DOC-06`.

Evidence: [docs/evidence/tencent-memory-research-2026-10-16.json](docs/evidence/tencent-memory-research-2026-10-16.json), [docs/research/github-2026-10-16/tencent-memory.md](docs/research/github-2026-10-16/tencent-memory.md), [docs/delivery/sessions/2026-10-16-evolution-research.md](docs/delivery/sessions/2026-10-16-evolution-research.md).

## 0.2.0-alpha.8 · Source-pinned evolution plan for scenarios, memory and decision support

2026-10-16 · `pushed_unreleased`

Owner-requested GitHub research maps 26 pinned repositories and 25 product capability families into a staged ENDSTATE/8BALL proposal, with a plain Zep explanation and bounded adoption experiments.

### Added

- Full evolution plan; pinned component register and six source/capability reports; query/source manifests; five candidate discoveries EM-075 through EM-079.

### Changed

- Linked the proposal into current entry points, handoff and existing roadmap/research registers; canonical runtime task requirements and statuses remain unchanged.

### Verification

- Documentation/history/ledger checks, focused documentation tests and source/requirement preservation are recorded with actual results in the session receipt.
- Upstream source/manifests/licences inspected; no candidate installation, inference, interoperability, predictive or human acceptance test.

### Limitations

- Recommendations are proposals, not imported features. B02 stays 10/20 required verified; ES01 stays 5/5 internal.
- Hosted model/provider identity, authorised test spending/transmission and independent/human review remain unresolved inputs for current V0.2 acceptance.
- Research branch is unmerged; application runtime and original fixtures are unchanged. No release or deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Domain action mappings, memory retraction contracts, aggregate experiment budgets, upstream licence/API differences and optimiser-status semantics need explicit adapter evaluation.
- Risk: Combining frameworks can duplicate state and multiply cost while concealing absent calibration or independent acceptance.
- Architecture: Keep ENDSTATE contracts and reviewed case records authoritative; compare optional source/memory/simulation/decision adapters against simpler baselines.
- Roadmap decision: new_candidate and existing_task refinements only; proposed sequencing maps to existing milestones/Lab IDs without new required runtime scope.
Registered discoveries: EM-020, EM-027, EM-046, EM-047, EM-051, EM-054, EM-061, EM-072, EM-075, EM-076, EM-077, EM-078, EM-079.

Roadmap items: `DOC-02`, `DOC-03`, `DOC-04`, `DOC-05`, `DOC-06`.

Evidence: [docs/evidence/evolution-research-2026-10-16.json](docs/evidence/evolution-research-2026-10-16.json), [docs/delivery/sessions/2026-10-16-evolution-research.md](docs/delivery/sessions/2026-10-16-evolution-research.md), [docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md](docs/strategy/ENDSTATE-EVOLUTION-PLAN-2026-10-16.md), [docs/research/GITHUB-COMPONENTS-2026-10-16.md](docs/research/GITHUB-COMPONENTS-2026-10-16.md).

## 0.2.0-alpha.8 · Current 8BALL build consolidated and verified on main

2026-10-15 · `pushed_unreleased`

Owner-authorized application/documentation integration is confirmed on main, with PRs1/2/3 showing Merged and a complete current build overview. This remains a development alpha.

### Added

- Source-bound consolidated native receipt and full-picture overview with current publication status.

### Changed

- Main now contains latest fixes, linked specifications, both original research variants and all74 discoveries. Canonical repository metadata records observed integration; acceptance remains unchanged.

### Verification

- At merge6b57a45,964 source tests,964 installed-kernel tests and384 native checks across eleven suites passed; source/artifact inspection valid/passed.
- Parent/history/archive/PRD/fixture checks passed. Public PRs1/2/3 show Merged; remote main and integration refs verified at tested merge before documentation receipt.

### Limitations

- B02 remains10/20 and ES01 remains5/5 internal. Actual-model, independent professional and human acceptance remain open.
- No deployment, release tag, model download/inference or deferred research runtime. Final receipt edits are documentation only; original archive whitespace is retained unchanged.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-051/055/072: consolidate current source/context but keep merged development distinct from model quality, human acceptance and release.
- Discovery: EM-073: both research variants and original manifests remain recoverable in the main tree.
- Risk: An integrated default branch can be mistaken for accepted V0.2; the ledger and overview retain every open gate.
- Architecture: No runtime/authority/dependency change;135 runtime/workflow bytes/modes match latest application.
- Roadmap decision: existing delivery task and explicitly authorized source integration only; no acceptance promotion or scope change.
Registered discoveries: EM-051, EM-055, EM-072, EM-073.

Roadmap items: `DOC-02`, `DOC-03`, `DOC-04`, `DOC-05`, `DOC-06`, `B02-18`.

Evidence: [docs/evidence/main-consolidation-native-2026-10-15.json](docs/evidence/main-consolidation-native-2026-10-15.json), [docs/evidence/main-consolidation-preservation-2026-10-15.json](docs/evidence/main-consolidation-preservation-2026-10-15.json), [docs/delivery/sessions/2026-10-15-main-consolidation.md](docs/delivery/sessions/2026-10-15-main-consolidation.md), [docs/delivery/BUILD-OVERVIEW.md](docs/delivery/BUILD-OVERVIEW.md).

## 0.2.0-alpha.8 · Consolidated development build for owner-authorized main integration

2026-10-15 · `local_unreleased`

Combine latest application fixes, specifications, research archives and all delivery/discovery history into one inspectable development source.

### Added

- Complete build overview, current entry points and explicit owner integration decision.
- Older18-file research variant and six wrappers preserved alongside supplied19-file variant.

### Changed

- Canonical history resolves by stable-ID union and append-only decisions, preserving all74 discoveries and original changelog entries.

### Verification

- Current integration preservation passed:135 runtime/workflow files match latest app; both histories, all74 discoveries, original PRD/frozen cases and both research archives preserved. Task scope/status/milestones unchanged;107 local links verified.
- Cumulative native validation pending at preparation checkpoint; final source-bound receipt records actual outcomes.

### Limitations

- Source integration does not pass actual-model, independent professional or human acceptance; B02 stays10/20 and ES01 stays5/5 internal.
- No deployment, release tag, model download, paid inference, deferred research runtime or other application.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-051/072: latest runtime and documentation must be combined without adopting older snapshot evidence.
- Discovery: EM-073: retain distinct original archive variants and manifests; all prior discoveries stay visible.
- Risk: Blind branch merges could restore old runtime or trigger unapproved model workflows; source consolidation could be confused with accepted V0.2.
- Architecture: No runtime/library/dependency change; unify source and context while preserving existing authority boundaries.
- Roadmap decision: existing_task delivery consolidation only; explicit owner authority for main, no acceptance or required-scope changes.
Registered discoveries: EM-051, EM-055, EM-072, EM-073.

Roadmap items: `DOC-02`, `DOC-03`, `DOC-04`, `DOC-05`, `DOC-06`.

Evidence: [docs/delivery/sessions/2026-10-15-main-consolidation.md](docs/delivery/sessions/2026-10-15-main-consolidation.md), [docs/decisions/0006-consolidated-development-main.md](docs/decisions/0006-consolidated-development-main.md), [docs/evidence/main-consolidation-preservation-2026-10-15.json](docs/evidence/main-consolidation-preservation-2026-10-15.json).

## 0.2.0-alpha.8 · Provider evidence and navigation fixes passed native software acceptance

2026-10-15 · `pushed_unreleased`

Source-bound final software receipt for bounded rejected extraction provenance, newer navigation preservation and unperformed review materials. Earlier failed evidence remains visible.

### Added

- Exact final source/report/per-suite hashes and private-copy review recording aids.

### Changed

- Canonical evidence and latest handoff record the final actual software result without promoting external acceptance gates.

### Verification

- At 294ff578, 964 source tests, 964 installed-kernel tests and 384 native checks across eleven suites passed; zero failed/errored/skipped code tests.
- Compilation, JavaScript syntax, eight structural fixtures, internal wheel, schemas and generated/history guards passed; inspection valid=true/run_status=passed before documentation receipt edits.
- Earlier c1defce native failure remains valid/failed and led to the refresh/navigation fix; no failed experiment was erased.

### Limitations

- Zero actual model calls or weights downloaded. Provider/download permission remains unanswered; owner review is deferred until the end as requested.
- Review sheets remain unperformed; B02 stays 10/20 and ES01 stays 5/5 internal. Independent semantic/professional and human acceptance remain open.
- Pushed source is not merged, released, deployed or remote-CI-verified; no research/industry scope expansion.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-051/055: preserve rejected extraction provenance through the disposable journey boundary.
- Discovery: EM-035/053: older refresh destination must not override a later explicit navigation.
- Discovery: EM-054: prepared human and independent review records remain distinct from scripted integration.
- Risk: Passing source/native software checks does not clear provider quality or human acceptance.
- Architecture: Failure retention and navigation sequencing preserve existing state, authority, source and session boundaries.
- Roadmap decision: existing_task only; no required task promotion or deferred research implementation.
Registered discoveries: EM-035, EM-051, EM-053, EM-054, EM-055.

Roadmap items: `B02-09`, `B02-10`, `B02-11`, `B02-12`, `B02-14`, `B02-15`, `B02-16`, `B02-19`, `B02-20`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/evidence/provider-failure-native-2026-10-15.json](docs/evidence/provider-failure-native-2026-10-15.json), [docs/evidence/provider-failure-native-failed-2026-10-15.json](docs/evidence/provider-failure-native-failed-2026-10-15.json), [docs/evidence/v02-review-pack-2026-10-15.json](docs/evidence/v02-review-pack-2026-10-15.json), [docs/delivery/sessions/2026-10-15-provider-failure-evidence.md](docs/delivery/sessions/2026-10-15-provider-failure-evidence.md).

## 0.2.0-alpha.8 · Preserve explicit navigation when an earlier refresh finishes

2026-10-15 · `local_unreleased`

Cumulative verification exposed an asynchronous refresh overwriting a newer Room navigation. Preserve the failed run and correct the presentation race within existing acceptance.

### Added

- Deterministic native delayed-response regression retaining the actual fictional server data.

### Changed

- Later explicit navigation stays authoritative while current-case refresh still applies its data.

### Fixed

- Refresh/sort completion could send the operator back to an older tab.

### Verification

- First native cumulative run at c1defce failed only browser-courses; 964 code tests and prior ten suites passed. Evidence inspection valid=true, run_status=failed.
- Unchanged c1defce deterministic native baseline reproduced the race; corrected native courses passed31 checks, retaining all29 previous assertions. Node syntax, Python compilation and diff checks passed. Cumulative rerun pending at correction checkpoint.

### Limitations

- No real model or human acceptance; B02 remains10/20 required scopes verified.
- A valid failed report is retained, not counted as a passing native run.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-035/053: an older same-case refresh can overwrite a newer explicit tab choice despite case-load sequence guards.
- Risk: A passing earlier timing-sensitive journey does not exclude a race; do not hide it with sleeps.
- Architecture: Keep async presentation navigation ordering separate from case facts, revisions and chosen-course authority.
- Roadmap decision: existing_task B02-16/B02-20; retain all acceptance and prior failed evidence.
Registered discoveries: EM-035, EM-053, EM-051.

Roadmap items: `B02-16`, `B02-20`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/delivery/sessions/2026-10-15-provider-failure-evidence.md](docs/delivery/sessions/2026-10-15-provider-failure-evidence.md), [docs/evidence/provider-failure-native-failed-2026-10-15.json](docs/evidence/provider-failure-native-failed-2026-10-15.json), [docs/evidence/refresh-navigation-baseline-2026-10-15.json](docs/evidence/refresh-navigation-baseline-2026-10-15.json), [docs/evidence/refresh-navigation-focused-2026-10-15.json](docs/evidence/refresh-navigation-focused-2026-10-15.json).

## 0.2.0-alpha.8 · Preserve rejected extraction evidence and prepare V0.2 human review

2026-10-15 · `local_unreleased`

Bounded failure provenance through provider/jobs/proposals, with unperformed prospective protocol, independent case review and original twenty-step human walkthrough.

### Added

- Unperformed review pack with source, lifecycle, accessibility/platform, visual/mobile and dense-graph task sheets.

### Changed

- Recording aids keep prospective approval, independent labels, owner review and scripted integration separate.

### Fixed

- Ollama extraction schema/span rejection previously lost parsed model output before async journey export; structural rejection and live-state guards remain.

### Verification

- 207 controlled provider/job/journey/hosted/compiler regressions passed. Original rejection/state/cancel/stale boundaries remain.
- Review-pack verification passed: original 20 steps, 54 NOT_RUN rows, 38 local links, rubric/version/null defaults, unchanged task scope/status and frozen generation hash. Dependency check passed.
- Cumulative native verification pending at implementation checkpoint; the final source-bound receipt records the actual result.

### Limitations

- No actual inference/model download or independent human acceptance at this preparation checkpoint. Provider choice/permission is pending; owner review is requested at the end.
- B02 remains 10/20 and ES01 remains 5/5 internal; no release/merge/deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-051/055: a correct extraction rejection can lose its raw model output through the async disposable journey evidence path.
- Discovery: EM-054: scripted twenty checks and original human twenty steps need separate unperformed recording aids.
- Risk: Retaining provider failure must not expose arbitrary transport/credential errors or publish cancelled/stale output.
- Architecture: Use the existing protected failed-proposal path; no kernel, truth or authority change.
- Roadmap decision: existing_task B02-09/B02-11/B02-12/B02-15 plus existing human review scopes; no new required scope.
Registered discoveries: EM-051, EM-054, EM-055.

Roadmap items: `B02-09`, `B02-10`, `B02-11`, `B02-12`, `B02-14`, `B02-15`, `B02-16`, `B02-19`, `B02-20`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/delivery/sessions/2026-10-15-provider-failure-evidence.md](docs/delivery/sessions/2026-10-15-provider-failure-evidence.md), [docs/delivery/review/README.md](docs/delivery/review/README.md), [docs/evidence/v02-review-pack-2026-10-15.json](docs/evidence/v02-review-pack-2026-10-15.json).

## 0.2.0-alpha.8 · Graph keyboard fix passed cumulative native acceptance

2026-10-15 · `pushed_unreleased`

Native software regression passed at 5312c6c2f9ef39a68c320b2e1684897c6ac33265. The implementation and this documentation receipt are published on the scoped graph-keyboard branch.

### Added

- Source-bound cumulative receipt and preserved baseline/fixed native graph evidence.

### Changed

- Canonical evidence and handoff record completed keyboard regression verification; remaining human/provider gates stay unchanged.

### Verification

- 951 source code tests and 951 installed-kernel tests passed with zero failures, errors or skips.
- All 382 native Chromium checks passed across eleven suites, including 42 graph checks. Compilation, JavaScript syntax, schemas, eight structural fixtures and generated/history checks passed.
- Source/artifact inspection returned valid=true, run_status=passed at the tested code commit.

### Limitations

- No actual model, independent semantic, human screen-reader/platform, visual or dense-case operator acceptance.
- B02 remains 10/20; ES01 remains 5/5 internally. No main merge, release or deployment. Subsequent receipt edits are documentation only.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-053 orientation continuity applies to replaced in-page graph controls, not only dialogs. Native baseline and corrected evidence preserve the distinction.
- Risk: Passing automated focus checks is not professional, screen-reader or supported-platform acceptance.
- Architecture: Keep presentation focus state outside case commands, approvals and factual state; no graph semantics changed.
- Roadmap decision: existing_task B02-16/B02-20; keep external acceptance blockers and deferred research unchanged.
Registered discoveries: EM-053, EM-051.

Roadmap items: `B02-16`, `B02-20`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/evidence/graph-keyboard-native-2026-10-15.json](docs/evidence/graph-keyboard-native-2026-10-15.json), [docs/delivery/sessions/2026-10-15-graph-keyboard-focus.md](docs/delivery/sessions/2026-10-15-graph-keyboard-focus.md).

## 0.2.0-alpha.8 · Preserve keyboard orientation through graph control redraws

2026-10-15 · `local_unreleased`

Correct the graph control focus-loss regression within existing accessibility scope. Human screen-reader, platform and operator acceptance remain outstanding.

### Added

- Preserved native baseline evidence: four keyboard actions left focus on BODY while case audit remained unchanged.

### Changed

- Graph control redraw focus restoration and native keyboard regression checks.

### Fixed

- Keep focus on logical neighbourhood/reset controls, or the labelled scope selector when a disappearing control has no replacement.

### Verification

- Native baseline at 821d9f512a70aaa602587caa4ef604021719b01f reproduced four failed focus assertions, zero runtime errors and unchanged case audit.
- Corrected native graph suite passed 42 checks (38 preserved plus four keyboard regressions); syntax, Python compilation and git diff --check passed. Cumulative acceptance is pending at this implementation checkpoint.

### Limitations

- No real inference, independent semantic judgement, human screen-reader, broad platform or dense-case operator acceptance.
- B02 remains 10/20 required verified scopes; no application version change, main merge, release or deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Revalidate EM-053: replacing visually equivalent graph controls still discards their DOM focus identity; disappearing controls need a deliberate destination.
- Risk: Mouse-driven checks can pass while keyboard navigation drops to BODY; restoration must not create a focus trap.
- Architecture: Focus continuity is presentation state only and must not modify case evidence, authority or graph semantics.
- Roadmap decision: existing_task B02-16/B02-20. Preserve required human/provider gates and deferred research; no additional discovery ID or new feature required.
Registered discoveries: EM-053, EM-051.

Roadmap items: `B02-16`, `B02-20`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/delivery/sessions/2026-10-15-graph-keyboard-focus.md](docs/delivery/sessions/2026-10-15-graph-keyboard-focus.md), [docs/evidence/graph-keyboard-baseline-2026-10-15.json](docs/evidence/graph-keyboard-baseline-2026-10-15.json), [docs/evidence/graph-keyboard-focused-2026-10-15.json](docs/evidence/graph-keyboard-focused-2026-10-15.json).

## 0.2.0-alpha.8 · Native regression verified for the generation-role correction

2026-10-15 · `pushed_unreleased`

Source-bound native software acceptance passed at 8fad4118f07f91ac1884713530bac9479a7b51b7. The same sprint publishes its code and this receipt on the scoped development branch; no V0.2 or model-quality acceptance follows.

### Added

- A source-bound validation receipt retaining exact counts, per-suite hashes, environment and actual-provider preflight status.

### Changed

- Canonical evidence and latest handoff now record completed native regression rather than the implementation checkpoint pending state.

### Verification

- 951 code tests passed with zero skipped, failed or errored tests; the same 951 passed against the installed ENDSTATE wheel.
- 378 native Chromium checks passed across all eleven suites. Python compilation, JavaScript syntax, schema export, eight structural fixtures and generated-document/history checks passed.
- Acceptance inspection valid=true and run_status=passed at tested code; source fingerprint cd783ba7e7c6d7507cb51fb751e3604f477bc362fbb3777a5675e3237959013e.
- Actual-provider preflight exited 2 (blocked), with zero calls; the public PR conversation and historical CI Success page were read after API reads were denied.
- Final documentation-only receipt: 60 delivery/changelog/emergence tests passed; generated/history guards and git diff --check passed.

### Limitations

- No fresh inference, independent semantic evaluation or human accessibility/operator acceptance; B02 remains 10/20, ES01 remains 5/5 internal.
- Native software evidence applies to the tested code revision. Final receipt edits are documentation only. No main merge, release or deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-074 remains an unverified semantic model-effectiveness concern after native software success; existing EM-020/051/055/060 remain applicable.
- Risk: Green contract/browser checks can be mistaken for successful inference or human acceptance.
- Architecture: Keep code, installed-package, native transport, actual-provider, semantic review and release evidence separate.
- Roadmap decision: existing_task: preserve B02-09 blocked until fresh selected-provider generation and independent judgement; no scope expansion.
Registered discoveries: EM-074, EM-020, EM-051, EM-055, EM-060.

Roadmap items: `B02-09`, `ES03-01`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/evidence/generation-role-contract-2026-10-15.json](docs/evidence/generation-role-contract-2026-10-15.json), [docs/delivery/sessions/2026-10-15-generation-role-contract.md](docs/delivery/sessions/2026-10-15-generation-role-contract.md).

## 0.2.0-alpha.8 · Clarify generated preparation, shared readiness and final verification

2026-10-15 · `local_unreleased`

Correct generation guidance for the preserved Qwen failure while retaining every deterministic compiler guard. This is a development correction, not evidence that real-model generation now passes.

### Added

- Exact historical 27 September Qwen evidence and controlled replay of all four original outputs.
- A separate prompt-version trace and explicit reserved readiness/success titles in second-stage context.

### Changed

- Schema descriptions and prompts distinguish preparatory results, branch-neutral readiness, future confirmation evidence and the single final verifier.
- Successful and rejected local generation receipts retain prompt/compiler versions.

### Fixed

- Generation instructions now explicitly prohibit repeating the shared verifier within a route or claiming reserved success conditions as intermediate results. The original failed output still rejects unchanged.

### Verification

- Unchanged baseline: 938 code tests passed.
- Focused compiler/replay checks: 50 passed. Initial test expansion exposed three fixture IndexErrors, corrected before this checkpoint.
- Historical report copied byte-for-byte from documentation commit 0ee5834c0745640369f5a538b770c346f234232a; SHA-256 4db80b5a17816f414cd09f1f27737ca12e3b3cc95f9fb2009854cc5154a82992. Cumulative native acceptance pending.

### Limitations

- No new model requests, model downloads, independent reviewer labels or human acceptance. B02 remains 10/20; ES01 remains 5/5 internal.
- Live GitHub API checks and review comments returned Forbidden; PR #2 Git head is verified. No merge, deployment, release or research feature adoption.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: EM-074: shared readiness must be achievable by either alternative. Existing EM-020/051/055/060 are revalidated.
- Risk: A model may paraphrase a forbidden result or supply irrelevant confirmation evidence; prompt/schema guidance is not semantic validation.
- Architecture: Keep compiler contracts stable and version generation guidance separately; all state/authority boundaries remain unchanged.
- Roadmap decision: existing_task: B02-09/ES03-01 only. Preserve every required model/human gate and defer research. EM-072/073 remain reserved on the pinned documentation branch.
Registered discoveries: EM-074, EM-020, EM-051, EM-055, EM-060.

Roadmap items: `B02-09`, `ES03-01`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/delivery/sessions/2026-10-15-generation-role-contract.md](docs/delivery/sessions/2026-10-15-generation-role-contract.md), [docs/evidence/qwen-baseline-2026-09-27.json](docs/evidence/qwen-baseline-2026-09-27.json), [tests/test_endstate_compilation.py](tests/test_endstate_compilation.py).

## 0.2.0-alpha.8 documentation · Consolidated research, future architecture and current closeout handoff

2026-10-15 · `local_unreleased`

Create one recoverable entry point linking the current published build to the full long-term research without changing runtime or current acceptance statuses. Publication is recorded separately after the exact documentation branch is verified.

### Added

- Root START-HERE and next-agent prompt; ten-scope V0.2 closeout; full ENDSTATE vision/roadmap/architecture supplements; source and experiment register; ADR 0005.
- All 19 files from the newly supplied handoff ZIP preserved unchanged, plus raw actual-model baseline evidence and a checksum context manifest.

### Changed

- Append-only navigation from the preserved master PRD, roadmap, AGENTS and handoff. README discovery banner.

### Fixed

- Resolve historical local-only/old-count confusion for the next agent without erasing prior records.

### Verification

- 60 existing delivery/changelog/emergence regression tests passed locally.
- Consolidation verifier passed: 19 original research files, all 18 manifest payload hashes, 52 relative links, five protected files, all 71 earlier discoveries and unchanged runtime/progress.
- Canonical delivery, emergence and changelog checks passed against exact application base 290e310707cf8bef6caf2508c285312b091bd18b.

### Limitations

- Documentation only: no runtime feature, future research experiment, new native/model/human acceptance, version release, merge or deployment.
- Existing 938/378 software results and 3/4 schema-valid failed Qwen baseline remain separately labelled historical evidence.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Current-state precedence is necessary when historical handoffs coexist with later publication.
- Discovery: The supplied archive variant must be preserved by its manifest rather than an old file count.
- Risk: A new agent might restart old work or treat accepted vision as permission to implement research during V0.2.
- Architecture: One canonical task ledger; separate evidence, decisions, application scope, research and publication records.
- Roadmap decision: existing_task: documentation consolidation and recoverability only; current required scopes and statuses unchanged.
Registered discoveries: EM-072, EM-073.

Roadmap items: `DOC-02`, `DOC-03`, `DOC-04`, `DOC-05`, `DOC-06`.

Evidence: [docs/delivery/sessions/2026-10-15-documentation-consolidation.md](docs/delivery/sessions/2026-10-15-documentation-consolidation.md), [docs/delivery/context-manifest.json](docs/delivery/context-manifest.json).

## 0.2.0-alpha.8 · Native software acceptance passed; internal core and guided authoring verified

2026-09-26 · `local_unreleased`

Record the published Source Desk correction and completed native evidence. This receipt begins locally and has its own publication record; runtime scope is unchanged.

### Added

- A source-bound native acceptance receipt and scoped checklist decisions.

### Changed

- B02-13 and ES01-05 are verified for their documented software/compatibility scope. Remaining tasks now name actual outstanding model or human review instead of an obsolete unpushed/native blocker.

### Fixed

- Current README/status/handoff distinguish published alpha.8 from preserved historical local-only checkpoints.

### Verification

- GitHub run 36219154611: 938 code tests and 938 tests against the installed internal ENDSTATE wheel passed.
- All eleven native browser suites passed: 378 checks including actual Source Desk original export.
- Downloaded artifact hash and all source/evidence hashes verified. No runtime/test change in this receipt.

### Limitations

- V0.2 is not accepted. Actual-model quality, professional source review, human accessibility/platform and operator checks remain.
- Research is separate; no main merge, release or deployment.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Native evidence closes transport-specific gaps but not human judgement; existing EM-035/EM-053/EM-051 remain applicable.
- Risk: Historical local-only status can mislead the next builder unless current evidence is prominent.
- Architecture: Keep source, verification, judgement and release states separate.
- Roadmap decision: existing_task: close supported software scopes only; preserve required model/human gates and scope freeze.
Registered discoveries: EM-035, EM-053, EM-051.

Roadmap items: `B02-13`, `B02-14`, `B02-16`, `ES01-05`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/evidence/native-closeout-2026-09-26.json](docs/evidence/native-closeout-2026-09-26.json), [docs/delivery/sessions/2026-09-26-native-acceptance-receipt.md](docs/delivery/sessions/2026-09-26-native-acceptance-receipt.md).

## 0.2.0-alpha.8 · Source Desk: preserve the operator query across delayed refreshes

2026-09-26 · `local_unreleased`

Correct the native Source Desk failure without weakening search, original-text preservation or case-isolation checks. Alpha.8 was published before this correction; a new native result is still required.

### Added

- Twelve deterministic response-order component regressions and three real-API browser assertions.

### Changed

- Query state is captured on input; same-document renders preserve keyboard position. Search and navigation use independent generations.

### Fixed

- Delayed refresh no longer erases a typed query. Superseded results and earlier document requests cannot replace a newer operator choice.

### Verification

- 938 local code tests passed; all 12 focused checks passed. Original source fails 8 of the new checks.
- 38 Source Desk browser checks passed through the explicit ASGI bridge. Native GitHub rerun must confirm the patched cumulative source.

### Limitations

- No new real model, independent expert or human accessibility review. No version acceptance, main merge or deployment.
- The local native attempt remains administrator-blocked. No workaround changes its policy. Deferred research remains separate.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Late rendering can lose a draft without a runtime error. This is new evidence for EM-035, EM-053 and EM-051, not an added feature lane.
- Risk: Fast test transports can hide response-order failures; obsolete search results can mislead operators.
- Architecture: Keep draft state outside replaceable DOM and scope request generations to the work they supersede.
- Roadmap decision: existing_task: resolve Source Desk/native acceptance only; maintain the owner scope freeze.
Registered discoveries: EM-035, EM-053, EM-051.

Roadmap items: `B02-14`, `B02-16`, `DOC-03`, `DOC-04`, `DOC-05`.

Evidence: [docs/delivery/sessions/2026-09-26-source-desk-native-closeout.md](docs/delivery/sessions/2026-09-26-source-desk-native-closeout.md), [docs/evidence/source-desk-native-closeout.json](docs/evidence/source-desk-native-closeout.json), [docs/evidence/source-desk-native-failure.txt](docs/evidence/source-desk-native-failure.txt), [tests/test_source_view_races.py](tests/test_source_view_races.py), [tests/browser_sources.py](tests/browser_sources.py).

## 0.2.0-alpha.8 · Chosen Course: retain the human choice and reasons to reconsider

2026-09-25 · `local_unreleased`

Recovered the exact alpha.7 + PRD 1.3 source and implemented a local Chosen Course workflow inside the existing Situation Room. This is not a secure agency release or an AI-generation quality improvement.

### Added

- Versioned read-only ENDSTATE course anchoring and reassessment, including selected prerequisite branches, explicit watches and clock checks.
- Transactional case-scoped choice history with explicit replacement, pause, resume, retirement and review, separate from facts and approvals.
- Black Situation Room course panel, route-selection preview, history/inspector, timeline/export integration and a dedicated browser suite.

### Changed

- Internal ENDSTATE distribution becomes 0.1.0a2, retaining endstate.plan.v1 and adding endstate.course.v1 contracts.
- Optional B03-07 / ES02-06 now partial for bounded local groundwork; original required tasks and dependencies remain intact.

### Fixed

- Prevented mistaken viability wording for disabled selected actions with verification-only remainders.
- Recovery no longer inherits unverified code or test totals from an interrupted narrative.

### Verification

- Reproduced both historical source trees exactly; baseline 862 tests passed.
- 64 focused code tests and 29 chosen-course browser checks passed through the explicit local bridge.
- Aggregate source-bound acceptance reports are packaged separately. Native probe was administrator-blocked; no policy changes.

### Limitations

- No source push, merge, deployment, secure multi-user authority or independent operator approval.
- Checks run on request, not as a continuous monitoring/notification service. Selection/pause/review never changes facts or action permissions.
- No live model inference and no recovered Draft Repair implementation. Existing real-model/native gates stay open.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Recalculating only by the same action set can admit another OR branch or ordering. This implementation pins selected prerequisites and checks recorded order.
- Discovery: A selected review time or deadline can be reached with no new source or state revision. Version-only checks would miss that reason to reconsider.
- Discovery: Course lifecycle and action approval histories are separate. A local pause has no channel to cancel external activity or revoke separate approvals.
- Discovery: A human review record can be appended while a hard constraint or explicit watch is still triggered. Treating review as clearance would hide an unresolved issue.
- Discovery: Disabling a selected action may leave a candidate that asks for evidence of its intended result. That candidate is not proof the original work can proceed.
- Discovery: The mounted alpha.7 archive and PRD overlay reproduced exactly; the interrupted Chosen Course narrative had no delivered implementation tree. New code and test results were rebuilt from the verified bytes.
- Risk: Choice history can be mistaken for authority unless the interface distinguishes it.
- Risk: Source-set and clock warnings can create review fatigue; independent operator testing is still required.
- Risk: Local history is hash-linked, not independently anchored or administrator-proof.
- Architecture: Pin the human-selected basis rather than tracking the newest top-ranked route.
- Architecture: Keep lifecycle judgements separate from factual case revisions, evidence and approvals.
- Architecture: Persist reproducible source before relying on narrated progress.
- Roadmap decision: existing_task / decision_record: deliver bounded local groundwork for optional B03-07 and ES02-06; preserve their original dependencies and all required V0.2 gates.
Registered discoveries: EM-066, EM-067, EM-068, EM-069, EM-070, EM-071.

Roadmap items: `B03-07`, `ES02-06`, `DOC-03`, `DOC-04`, `DOC-05`, `DOC-06`.

Evidence: [docs/delivery/sessions/2026-09-25-chosen-course-recovery.md](docs/delivery/sessions/2026-09-25-chosen-course-recovery.md), [docs/v2/CHOSEN-COURSE.md](docs/v2/CHOSEN-COURSE.md), [docs/evidence/chosen-course-focused-verification.json](docs/evidence/chosen-course-focused-verification.json), [tests/test_courses.py](tests/test_courses.py), [tests/browser_courses.py](tests/browser_courses.py).

## 0.2.0-alpha.7 / PRD 1.3 · Vision strengthened; recovered-source boundary made explicit

2026-09-24 · `local_unreleased`

Documentation-only refinement: 8BALL becomes the fixer’s live situation room around an explicit mandate and human-selected course; ENDSTATE remains a neutral planning and reconsideration engine. No runtime completion or new required scope is implied.

### Added

- Separate 8BALL and ENDSTATE vision documents, ADR 0004 and proposed course/coverage/recovery acceptance scenarios.
- Ten new discoveries retained alongside all 55 originals; five additional end-of-sprint review prompts.
- Four optional unaccepted candidate/recovery tasks with explicit acceptance and next steps.

### Changed

- Master PRD revision 1.3, roadmap, agent instructions and handoff link the refined vision without changing required flags or statuses.
- Earlier fallback/watch/attention/recoverability discoveries have appended dispositions rather than rewritten observations.

### Fixed

- The latest handoff’s missing Draft Repair source is explicitly separated from the recovered alpha.7 implementation; later narrated test totals are not attached to the earlier source.
- No-path wording now identifies the supplied catalogue and search bounds rather than implying global impossibility.
- The review protocol now permits additional passes while requiring the original ten and preserving recorded prompt text/order. Seven regression checks cover safe extension and denied rewrites.

### Verification

- Recovered alpha.7 source tree matches exactly. All 862 regression tests passed, including seven new additive-protocol checks; focused governance subset: 60 passed.
- Delivery, emergence and changelog validators passed against the reconstructed exact base. Required task statuses/flags, original discoveries and historical changelog entries are preserved.
- Initial fixed-ten-prompt regression failure is retained in the verification pack. No new native browser, runtime feature, actual inference or operator-quality acceptance.

### Limitations

- Documentation only; new course/mandate/recovery capabilities are not implemented by this review.
- No source push, merge, deployment, real inference, native browser or independent operator review.
- The later repair source was not recovered. Existing V0.2 and model-quality gates remain open.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: The recovered alpha.7 contracts represent candidate routes and individual decisions, but do not define a dedicated course-selection record tying an operator choice to a route, target and snapshot.
- Discovery: Once a team has chosen a course, repeated ranking changes could confuse action and accountability if the interface treats the newest first route as the plan being followed.
- Discovery: The recovered source separates full originals, selected excerpts and bounded route search. A result about the processed subset cannot establish completeness of the whole situation.
- Discovery: Source Clarity already separates an adopted deadline from source retraction. The same distinction may be needed for promises, authorised concessions and other commitments made while handling a case.
- Discovery: The supplied Draft Repair handoff reports a human-correction workflow but not a recovered implementation. If restored, a successful human repair would demonstrate recoverability rather than unassisted model quality.
- Discovery: The cumulative workspace has more inspection and review surfaces. It is not yet independently established whether that makes a fixer faster, more accurate or simply busier.
- Discovery: The latest supplied repair handoff states that its working tree was not recovered, while the alpha.7 ZIP can be reconstructed to its declared exact Git tree. Later reported test totals cannot be attached to that earlier source.
- Discovery: A preserved correction could reveal a missing dependency, changed meaning or excessive review cost, but using that record for model training or another client is a separate decision.
- Discovery: A single successful check can satisfy a present-state condition without establishing a requested period of sustained recovery. Not every outcome requires such a period.
- Discovery: The initial test suite hard-coded exactly ten prompts; additive compatibility needs stable identifiers and preserved history instead.
- Risk: More concepts can increase operator burden or silently expand release scope.
- Risk: Reviewing or selecting a plan must never become proof or authority to act.
- Risk: Using an earlier recovered source must not overwrite later code when recovered.
- Architecture: Keep candidate route, human-selected course and approval as distinct records.
- Architecture: Keep host identity/storage/execution outside the calculation kernel.
- Architecture: Expose scope and recoverability rather than unsupported confidence scores.
- Roadmap decision: existing_task / new_candidate / decision_record: strengthen existing vision and record four optional unaccepted candidates; no new_required_task or required completion change.
Registered discoveries: EM-056, EM-057, EM-058, EM-059, EM-060, EM-061, EM-062, EM-063, EM-064, EM-002, EM-003, EM-004, EM-005, EM-006, EM-013, EM-018, EM-032, EM-045, EM-048, EM-055, EM-065.

Roadmap items: `DOC-02`, `DOC-03`, `DOC-04`, `DOC-05`, `DOC-06`, `B03-07`, `ES02-06`, `ES03-08`, `B04-04`.

Evidence: [docs/delivery/sessions/2026-09-24-vision-strengthening.md](docs/delivery/sessions/2026-09-24-vision-strengthening.md), [docs/evidence/vision-review-source-inventory.json](docs/evidence/vision-review-source-inventory.json), [docs/decisions/0004-evidence-led-course-and-recovery.md](docs/decisions/0004-evidence-led-course-and-recovery.md), [docs/vision/8BALL.md](docs/vision/8BALL.md), [docs/vision/ENDSTATE.md](docs/vision/ENDSTATE.md), [docs/vision/ACCEPTANCE-DESIGN.md](docs/vision/ACCEPTANCE-DESIGN.md), [scripts/emergence.py](scripts/emergence.py), [tests/test_emergence_register.py](tests/test_emergence_register.py), [docs/vision/OWNER-REVIEW.md](docs/vision/OWNER-REVIEW.md).

## 0.2.0-alpha.7 · Consolidated acceptance, internal ENDSTATE package and keyboard continuity

2026-09-24 · `local_unreleased`

The complete black 8BALL workspace now has one source-bound verification path, strict reusable result schemas, a real internal wheel installation check and clearer keyboard/dialog behaviour. No new application lane or model-quality claim.

### Added

- Strict nested PlanResult/BriefingResult schemas with cross-field references and exact JSON compatibility.
- Offline ENDSTATE wheel creation, isolated installation, full code-suite rerun against the installed kernel and schema export.
- One acceptance runner with fresh per-run reports, exact source/artifact hashes, ten browser suites and distinct passed/failed/blocked modes.
- Explicit actual-provider twenty-check integration command and opt-in hosted workflow; no mock fallback or automatic download.
- Six emergence records EM-050 through EM-055 retained for owner review.

### Changed

- Checkpoint version is 0.2.0-alpha.7, still local and unfinished V0.2.
- CI is configured to use the same consolidated runner; this unpushed workflow has not executed.

### Fixed

- Navigation focuses the destination heading; replacement dialogs retain their original return target; alerts/focus/forced-colour/reduced-motion states are explicit.
- Verification rejects changed/missing evidence, source drift, omitted suites and bridge reports presented as native.
- A test fixture path is now relative to its test file, so installed-kernel regression testing does not depend on checkout working directory.

### Verification

- 855 code tests passed, preserving the 794-test baseline and adding 61 checks. All 855 also passed against the installed wheel.
- All 344 browser checks passed across ten suites through the explicit local ASGI bridge, including 36 new keyboard/reflow checks. Full source-bound reports are supplied in the developer pack.
- Native navigation was legitimately attempted and administrator-blocked. Local/hosted actual-provider preflights were blocked before inference.

### Limitations

- Local and unpushed. Previous source-write restriction was not bypassed.
- No new actual inference, independent expert labels, human screen-reader study, native acceptance or production/SDK release.
- The actual-provider script uses API integration and scripted reviewer actions, with additional native reload/download when available; it is not the full independent all-native user acceptance.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: PlanResponse previously guaranteed its outer envelope but not the complete nested result structure.
- Discovery: Separate successful test reports could be retained while the working source continued changing.
- Discovery: The kernel could pass inside the application checkout without proving that the actual wheel contained and loaded the right files.
- Discovery: Navigation and replaced dialogs could leave keyboard focus on the body or on a removed control.
- Discovery: An actual-inference integration script can exercise approvals and evidence mechanics while still using developer-authored reviewer choices.
- Discovery: A configured provider can be unreachable; a valid model response can be semantically wrong; a passing local build can be unpushed and undeployed.
- Risk: Many passing code tests cannot clear a model-quality, native-browser or production-security gate.
- Risk: Source/artifact hashes are local integrity checks, not independently signed evidence.
- Architecture: Keep ENDSTATE internal calculation and distribution separate from 8BALL identity, storage and execution authority.
- Architecture: Keep inference, scripted integration, independent human evaluation and commercial release as distinct records.
- Roadmap decision: Advance existing ES01-05/B02-12/B02-16 only. Preserve B02-09/B02-11/B02-12/B02-18 open gates and every earlier discovery.
Registered discoveries: EM-050, EM-051, EM-052, EM-053, EM-054, EM-055.

Roadmap items: `ES01-05`, `B02-12`, `B02-16`.

Evidence: [docs/v2/ACCEPTANCE-RUNNER.md](docs/v2/ACCEPTANCE-RUNNER.md), [docs/v2/ACCESSIBILITY.md](docs/v2/ACCESSIBILITY.md), [docs/endstate/PACKAGE.md](docs/endstate/PACKAGE.md), [docs/evidence/integration-acceptance-local-verification.json](docs/evidence/integration-acceptance-local-verification.json), [docs/delivery/sessions/2026-09-24-integration-acceptance-local.md](docs/delivery/sessions/2026-09-24-integration-acceptance-local.md).

## 0.2.0-alpha.6 · Plan Review, independent scenarios and distinct route identities

2026-09-24 · `local_unreleased`

Inspect the live outcome graph, compare explicit hypothetical changes and record human plan-quality judgements without changing evidence or action authority. Preserves all earlier local builds.

### Added

- Plan Review inside Plan Studio and Ways Through: exact outcome/confirmation tracing, inspectable source references, structural findings and a six-part human review.
- Independent removal, budget and elapsed-time checks, each reset to the same live case snapshot.
- Separate review journal with exact assessment digests, expiry, concurrency/idempotency, stale-history labels and audit export.
- Eight offline engineering fixtures, an unfilled expert-review worksheet and a proposed plan-quality protocol. Six more discoveries retained for owner review.

### Changed

- Application checkpoint is 0.2.0-alpha.6, still an unfinished local V0.2 preview.
- Native regression workflow includes Plan Review; local evidence remains explicitly bridged.

### Fixed

- Different producer orders no longer share a route ID and overwrite one another in comparisons. Noncolliding legacy IDs stay unchanged.
- A clean graph is not presented as semantic proof, and a favourable human review cannot approve an action or attest facts.

### Verification

- 794 automated tests passed, preserving all 746 input tests and adding 48 checks.
- 308 explicitly bridged browser checks passed across nine suites, including 33 Plan Review checks.
- Eight of eight offline synthetic structural fixtures passed. No model or independent reviewer was used.
- Python compilation, JavaScript syntax and immutable delivery/document guards passed. Native navigation was attempted and administrator-blocked; no new native CI or live inference.

### Limitations

- Local and unpushed; prior source-write safety restriction has not been bypassed.
- Plan Review assesses the live case, not unsaved Plan Studio drafts. Scenario checks are bounded arithmetic, not causal outcome forecasts.
- Independent expert review, robust arbitrary-situation model generation, secure agency operation and native integration acceptance remain open.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: Candidate routes with the same actions but different producer ordering can have different feasibility and need different identities.
- Discovery: A schema-valid route can still satisfy a weaker target than the user requested.
- Discovery: Human review and operational approval must remain separate records.
- Discovery: Independent stress comparisons must not inherit earlier hypothetical changes.
- Discovery: The human review burden may need usability measurement; it must not be reduced by automatic pass labels.
- Discovery: Negative effects can be followed by valid recovery; tests must reflect actual declared constraints.
- Risk: Structural checks do not establish truthful sources, correct motives, outcome alignment or success likelihood.
- Risk: An unfilled reviewer sheet is not independent evaluation.
- Architecture: Keep the pure assessment in ENDSTATE and human review records in the 8BALL application journal.
- Architecture: Disambiguate only colliding route IDs to preserve frozen legacy results.
- Roadmap decision: Advance existing B02-03/B02-11/B02-13. Keep semantic/model/native gates open and retain EM-048 as a deferred owner-review hypothesis.
Registered discoveries: EM-044, EM-045, EM-046, EM-047, EM-048, EM-049.

Roadmap items: `B02-03`, `B02-11`, `B02-13`.

Evidence: [docs/v2/PLAN-REVIEW.md](docs/v2/PLAN-REVIEW.md), [evals/PLAN-QUALITY-GATE.md](evals/PLAN-QUALITY-GATE.md), [docs/evidence/plan-review-local-verification.json](docs/evidence/plan-review-local-verification.json), [docs/evidence/route-identity-regression.json](docs/evidence/route-identity-regression.json), [docs/delivery/sessions/2026-09-24-plan-review-local.md](docs/delivery/sessions/2026-09-24-plan-review-local.md).

## 0.2.0-alpha.5 · Source-grounded identity and deadline review

2026-09-24 · `local_unreleased`

A black source-clarity workspace records human identity interpretations and explicitly previewed deadline amendments, without merging actors, guessing dates or attesting claims. All previous local upgrades remain included.

### Added

- Exact source-mention records, lexical name candidates, linked/distinct/unresolved judgements and preserved reviewer reasons.
- Reusable civil-time interpretation with explicit reference dates, IANA timezones, fold selection, gap rejection and UTC conversion.
- Preview then apply for case, condition, decision or question deadlines, with source-bound revision checks and paired audit entries.
- Retraction/actor-change/overridden-deadline attention states and six additional retained build discoveries.

### Changed

- The full regression workflow includes the new native source-clarity journey, while local evidence remains explicitly bridge-based.
- The ENDSTATE import boundary admits the standard-library re and zoneinfo modules; it still prohibits application/network/database services.

### Fixed

- A name-text candidate is never silently chosen as an identity or authority.
- Editing a deadline interpretation invalidates the preview; stale source/case/review context cannot apply.
- Selected phrases are shown with surrounding wording so negation and attribution remain available to the reviewer.

### Verification

- 746 automated tests passed, preserving the 672-test supplied baseline and adding 74 checks.
- 275 explicit ASGI-bridge browser checks passed across eight suites, including 26 new source-clarity checks.
- Python/JavaScript and generated-document checks passed. Native navigation was attempted and administrator-blocked; no new native CI or model inference.

### Limitations

- Local and unreleased. Earlier source-write denial was not bypassed.
- This is human source interpretation, not general entity extraction, global actor merging, natural-language calendar inference or semantic model-quality approval.
- B02-10/B02-14 and all broad source-to-plan, native, independent review and secure agency gates remain open.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: A same-name fixture has two distinct actors. Selecting one source mention can establish a reviewer link without merging either actor or assigning authority.
- Discovery: A correctly converted date still does not establish that it should constrain the whole case rather than one report, decision or question.
- Discovery: Timezone round-trip tests produce no real instant in a spring clock gap and two in an autumn fold. Source-relative dates also require a reference date independent of import time.
- Discovery: An operator-adopted deadline can remain important after its source is withdrawn. Automatically erasing it would silently change operational commitments.
- Discovery: The selected name or date phrase omits nearby attribution, qualifications and negation. Exact offsets prove location, not a correct interpretation.
- Discovery: The bounded calendar-day interpreter deliberately cannot decide what next business day or end of day means for every organisation, location or agreement.
- Risk: Shared names, exact quotations and schema validation do not prove identity, authority or the source’s intended date.
- Risk: Withdrawing evidence should prompt reconsideration, not silently remove adopted operational commitments.
- Architecture: Keep source interpretations in a separate journal; only explicit adoption of a deadline touches the planning snapshot.
- Architecture: Civil-time interpretation is reusable without an application, provider or network dependency.
- Roadmap decision: Advance existing B02-10/B02-14 with bounded deterministic/human review. Retain business-calendar handling as EM-043 for owner review; no new required lane or weakened model gate.
Registered discoveries: EM-038, EM-039, EM-040, EM-041, EM-042, EM-043, EM-019, EM-020, EM-021, EM-022, EM-035.

Roadmap items: `B02-10`, `B02-14`.

Evidence: [docs/v2/SOURCE-CLARITY.md](docs/v2/SOURCE-CLARITY.md), [docs/delivery/sessions/2026-09-24-source-clarity-local.md](docs/delivery/sessions/2026-09-24-source-clarity-local.md), [docs/evidence/source-clarity-local-verification.json](docs/evidence/source-clarity-local-verification.json).

## 0.2.0-alpha.4 · Emergent Insights and an evolving owner-review register

2026-09-24 · `local_unreleased`

A bounded situation-insight workflow joins the existing fixer application, while every recorded build discovery stays visible in a separate evolving register. Neither implies AI-quality or production acceptance.

### Added

- Twelve deterministic ENDSTATE detectors and a recorded target-alignment check, with typed references, explicit caveats, policy settings and candidate-set limits.
- Case-scoped scans, review reasons, manual hypotheses, deliberate revisiting, recurrence-aware dismissal and exact-context verification-question creation.
- Black Emergent Insights and Build discoveries screens, complete history export and a separate hash-linked insight ledger.
- An evolving 37-discovery register and ten review questions; candidates and declined ideas remain available for owner review.

### Changed

- New build reviews link stable EM-nnn discovery IDs and preserve original observation/decision history. Delivery completion is derived only from the canonical task ledger.

### Fixed

- Already-satisfied OR outcomes no longer cause this detector layer to treat unused alternatives as required blockers.
- A changed or reappearing finding cannot silently inherit an old dismissal; reviewing never marks factual conditions confirmed.
- Historical governance compatibility uses five exact content-bound exceptions, not backdating or rewriting prior changelog entries.
- Insight forms use secure random IDs with the existing fallback and recheck case identity after awaited detail responses.

### Verification

- 672 automated tests passed, including 104 added since the supplied 568-test baseline.
- 249 explicit ASGI-bridge browser checks passed across seven suites, including 39 new Emergent Insights checks.
- Python compilation, browser-module syntax and generated roadmap/register/changelog checks passed.
- Native browser navigation was attempted and blocked by administrator policy. No new native CI or actual-model inference is claimed.

### Limitations

- Local and unreleased; no new native CI, model inference, external ingestion, autonomous actions or production security acceptance is claimed.
- Current detection is structural, not arbitrary causal discovery, semantic contradiction detection or prediction. Owner/operator usefulness remains a separate gate.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: The review workflow needs a separate status axis from evidence character.
- Discovery: A dismissed finding must be reconsidered after changed content or recurrence.
- Discovery: Satisfied OR objectives can retain alternative candidate branches; these must not become false insight blockers.
- Discovery: Cumulative integration must preserve exact pre-policy changelog entries while enforcing review links on future entries.
- Risk: Source-record counts do not establish independence, graph concentration does not prove authority, and age is not falsity.
- Risk: A case response arriving after a user switches contexts must not populate the new case.
- Architecture: Keep read-only ENDSTATE detectors separate from 8BALL persistence, human review and factual attestations.
- Architecture: A versioned, append-only discovery register lets the owner reconsider what the builder did not select.
- Roadmap decision: Adopt DOC-06 and bounded ES02-05/B02-21 scope. Keep B02-22 usefulness/native acceptance open. Preserve all source/model and production gates.
Registered discoveries: EM-007, EM-009, EM-010, EM-011, EM-012, EM-013, EM-014, EM-015, EM-017, EM-018, EM-021, EM-022, EM-023, EM-024, EM-025, EM-026, EM-028, EM-030, EM-033, EM-034, EM-035, EM-036, EM-037.

Roadmap items: `DOC-06`, `ES02-05`, `B02-21`, `B02-22`.

Evidence: [docs/delivery/sessions/2026-09-24-emergent-insights-local.md](docs/delivery/sessions/2026-09-24-emergent-insights-local.md), [docs/v2/EMERGENT-INSIGHTS.md](docs/v2/EMERGENT-INSIGHTS.md), [docs/delivery/EMERGENCE-REGISTER.md](docs/delivery/EMERGENCE-REGISTER.md), [docs/evidence/emergent-insights-local-verification.json](docs/evidence/emergent-insights-local-verification.json), [docs/delivery/CHANGELOG-POLICY.md](docs/delivery/CHANGELOG-POLICY.md).

## 0.2.0-alpha.3 · Mandatory build-sprint emergence review

2026-09-24 · `local_unreleased`

Development governance now requires every build sprint to capture what the implementation revealed that the existing plan did not fully anticipate, without automatically expanding scope.

### Added

- A mandatory Emergence Review in AGENTS, the shared handoff, PRD and roadmap.
- A dedicated emergence-review guide with evidence levels and a controlled roadmap-promotion decision.
- Build-history support for recording discoveries, risks, architecture implications and roadmap disposition.

### Changed

- New build changelog entries must include an emergence review when checked against their starting base.

### Fixed

- Product discoveries can no longer disappear into chat-only context or silently become roadmap commitments without classification.

### Verification

- 568 automated tests passed after the governance/changelog changes.
- 44 Plan Studio/changelog browser checks passed through the explicitly labelled ASGI bridge; native browser networking/storage/CSP are not inferred.
- Python compilation, browser JavaScript syntax, generated changelog and delivery-ledger validation passed.

### Limitations

- Local documentation/process checkpoint only; not pushed, merged, deployed or a change to V0.2 acceptance gates.
- Current product discoveries include hypotheses that remain unpromoted until explicit roadmap decisions.

### Emergence review

**What did this sprint reveal that we had not properly seen before?**

- Discovery: 8BALL is converging on two explicitly linked graphs: reality/provenance and outcome/action.
- Discovery: Information acquisition, freshness and replan triggers are becoming first-class planning concerns.
- Discovery: Operator attention and acceptable outcome envelopes may deserve later modelling, but need pilot evidence first.
- Risk: Graph visualisation can imply causal confidence that the evidence does not support.
- Risk: Uncontrolled product discovery can either freeze the roadmap too early or cause scope explosion.
- Architecture: ENDSTATE event-driven replanning should account for freshness, supersession and machine-readable watch conditions.
- Architecture: Keep source/evidence semantics separate from intended action effects and route structure.
- Roadmap decision: Create DOC-05 as a required governance task. Keep the substantive product findings under existing tasks or as candidates until separately promoted.

Roadmap items: `DOC-05`, `DOC-04`.

Evidence: [docs/delivery/sessions/2026-09-24-emergence-review-local.md](docs/delivery/sessions/2026-09-24-emergence-review-local.md), [docs/delivery/EMERGENCE-REVIEW.md](docs/delivery/EMERGENCE-REVIEW.md).

## 0.2.0-alpha.3 · Source Desk: original text and traceable evidence

2026-09-24 · `local_unreleased`

A bounded source-handling upgrade inside V0.2. It does not claim a production evidence vault or completed AI planning.

### Added

- Black Source Desk inside Evidence, with full-text search, passage navigation, source selection and a deliberate evidence-capture review.
- Immutable UTF-8 originals up to 200,000 Unicode characters, exact excerpt/quote lineage, content hashes and source-aware audit exports.
- Explicit duplicate candidates, separate-provenance import decisions and linked versions that never silently overwrite earlier sources.
- Transactional original retraction that removes linked evidence support while preserving text, observations and history.

### Changed

- Only captured excerpts may be selected for analysis. Full originals remain outside provider requests and the existing 12,000-character model allowance stays unchanged.
- Body limits are checked against actual received bytes; only source import/preview receives a larger bounded allowance.

### Fixed

- Original offsets remain correct across UTF-16 browser selection, emoji, combining characters and CRLF display normalisation.
- Source-free historical case exports retain their exact old wire/audit representation.
- Invalid replacement files cannot silently reuse a previously loaded source.

### Verification

- 566 automated tests passed, including 82 new source, API and Unicode-mapping checks.
- 210 explicit ASGI-bridge browser checks passed across six suites, including 35 new Source Desk checks and the preserved workflows. No native browser or model-quality result is inferred.
- Python compilation, JavaScript syntax and single-ledger/changelog validation passed. Exact-base patch reproduction is documented in the delivered package manifest.

### Limitations

- Local only: not pushed, merged or deployed.
- UTF-8 .txt/.md and pasted text only. PDF/DOCX/OCR, semantic entity merging and independent source/model quality review are not implemented.
- No native browser or new live-model result. Production permissions, encrypted vault and independently anchored custody remain future work.

Roadmap items: `B02-14`, `B02-10`, `DOC-04`.

Evidence: [docs/evidence/source-desk-local-verification.json](docs/evidence/source-desk-local-verification.json), [docs/delivery/sessions/2026-09-24-source-desk-local.md](docs/delivery/sessions/2026-09-24-source-desk-local.md).

## 0.2.0-alpha.2 · Plan Studio, controlled analysis and a visible changelog

2026-09-23 · `local_unreleased`

An operator-focused authoring build inside V0.2. It does not claim V0.3 or production readiness.

### Added

- Guided nested AND/OR and explicit-false authoring, guards, intended effects, verification criteria, resources, decision gates and response contingencies.
- Read-only amendment preview with route differences, historical protections, undo/redo, discard and a separate revision-checked commit.
- Persistent local analysis status with bounded queue, stage counts, cancellation, stale-result rejection and restart interruption.
- In-app What’s new and a generated root CHANGELOG.md. Every future build must update the shared changelog and delivery ledger.
- Desktop authoring columns scroll independently; smaller screens keep a responsive stacked layout.

### Changed

- Source analysis runs through explicit jobs rather than a blocking browser request. Model output still requires human review.
- Plan Studio extends the black operator interface; the read-only relationship explorer remains separate.

### Fixed

- Cancellation or a case revision change prevents a late model response being published.
- A server restart never automatically retries inference or reuses old external-transmission permission.
- Uncommitted plan drafts are protected when switching to an existing, newly created or imported case.

### Verification

- 484 automated tests passed locally, including 85 added since the supplied Connections checkpoint.
- 174 Chromium checks passed through the explicit ASGI bridge: 27 legacy, 51 V0.2, 15 provider/black, 38 Connections and 43 Plan Studio/job/changelog.
- Python compilation, all browser JavaScript syntax checks, changelog generation/base comparison and shared-ledger validation passed.
- Native browser navigation returned ERR_BLOCKED_BY_ADMINISTRATOR. No native CI result or new real-model result is claimed.

### Limitations

- Not pushed, merged, deployed or commercially released.
- An in-flight provider call may finish or be billed after cancellation. Its result is discarded and further stages are stopped.
- No new real-model quality result; the source-to-plan gate remains open.
- Single local server process, not a distributed agency job service.

Roadmap items: `B02-13`, `B02-15`, `DOC-04`.

Evidence: [docs/delivery/sessions/2026-09-23-plan-studio-local.md](docs/delivery/sessions/2026-09-23-plan-studio-local.md), [docs/evidence/plan-studio-local-verification.json](docs/evidence/plan-studio-local-verification.json).

## 0.2 developer checkpoint · Connections explorer

2026-09-23 · `local_unreleased`

Read-only Connections, Outcome flow and Records views around the current case.

### Added

- Neighbourhood focus, search/type filters, pan/zoom, display-only pins and record inspector.

### Verification

- Previous checkpoint: 399 automated code checks and 131 explicitly bridged browser checks.

### Limitations

- Those results do not establish native browser CI or live model quality.

Roadmap items: `B02-20`.

Evidence: [docs/evidence/relationship-explorer-local-verification.json](docs/evidence/relationship-explorer-local-verification.json).

## 0.2 developer checkpoint · Hosted-provider preparation and black interface

2026-09-23 · `local_unreleased`

Optional Hugging Face transport, exact target-bound frame validation and black visual tokens.

### Added

- Explicit hosted model/provider configuration, runtime probes and target review.

### Verification

- Previous checkpoint: 362 automated code checks and 93 explicitly bridged browser checks.

### Limitations

- No Hugging Face credentials or live call. GitHub source write was blocked.

Roadmap items: `B02-09`, `B02-15`.

Evidence: [docs/evidence/hf-black-local-verification.json](docs/evidence/hf-black-local-verification.json).
