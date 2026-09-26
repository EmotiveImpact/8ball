# 8BALL + ENDSTATE changelog

> Generated from `docs/delivery/changelog.json`. Update that source, then run `python scripts/changelog.py --write`. The in-app What’s new page reads the same entries.

This is product history, not the case decision trail. A build entry is not evidence of a merge, deployment or production-model approval.

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
