# Source clarity: identity and deadline review

Developer checkpoint `0.2.0-alpha.5`, inside unfinished 8BALL V0.2. This is a bounded, source-grounded operator workflow for B02-10/B02-14, not autonomous entity resolution or a passed model-quality gate.

## The operator loop

Open **Identity & deadlines**. Select a source excerpt and highlight the exact name or date wording. The application stores the original Unicode code-point range, quotation and whole-excerpt SHA-256. It shows surrounding context so a short selection does not hide negation, attribution or qualifications. Longer originals remain in Source Desk; first capture a relevant evidence passage, then review it. Source origin remains available.

For an identity mention, inspect same-name or shared-token candidates. Choose an existing actor and record that the mention refers to them, is explicitly a different person, or remains unresolved. Candidate ordering is lexical and does not prove identity. Every decision includes the reviewer rationale and exact quote. Earlier decisions remain available. No actor records, relationships, authorities, action references or observations are merged, renamed or reassigned.

For a deadline, choose the specific case/condition/decision/question target. Enter a full calendar date, or an explicit source-reference date plus a calendar-day offset. The source date is not assumed from its import time or the current clock. Enter the local wall-clock time, an IANA timezone and the reason for choosing it. The system converts to UTC, shows old/new values and the route/approval impact, and requires an explicit apply operation. Reading and previewing do not change the case. Application changes one scheduling field, invalidates approvals and creates linked review/case journal entries in one transaction. It does not attest a factual condition.

## Civil time is not always a unique instant

`endstate/time_review.py` validates explicit operator input against the installed IANA timezone database. It round-trips each possible fold through UTC. A missing local time has no valid instant and cannot be applied. A repeated local time requires the operator to select the first or second occurrence. Normal times reject an irrelevant fold choice. Timezone abbreviations such as BST/EST are not accepted as a substitute for a location. UTC is allowed explicitly. Fractional offsets and non-London locations are tested.

The helper uses Python standard-library `datetime`, `re` and `zoneinfo`, plus existing Pydantic contracts. ENDSTATE still imports no application, HTTP, database or model runtime. The import-allowlist test now admits only those two additional standard-library modules; an isolated helper test rejects application/runtime-service imports. A platform without timezone data returns a configuration error rather than guessing. Windows deployments may require installing `tzdata`; no package is downloaded silently.

Primary design references:
- Python 3.13 zoneinfo documentation: https://docs.python.org/3.13/library/zoneinfo.html
- PEP 495, local time disambiguation: https://peps.python.org/pep-0495/

These explain civil-time ambiguity. They do not establish that the chosen date/zone correctly interprets the human source. That remains a reviewed judgement.

## Lifecycle and integrity

A separate `v2_grounding_events` table stores append-only, hash-linked review snapshots. All mutations require both the expected case revision and the expected review revision, plus an idempotency key. Stale, concurrent and duplicate requests are tested. An exact source mention has one record per review kind; later interpretation appends rather than creating invisible duplicates. The ledger is limited to 150 reviews and 600 events per local case.

Preview returns a digest bound to the request, current case, quoted review record and resolved UTC instant. Editing the request invalidates the browser preview. Applying rechecks the digest, current source status and current case/review revisions. Preview and application are separate; no preview has the authority to write by itself. The case amendment and its interpretation record commit atomically, and export validates their link. Source-free historical exports retain their exact shape.

Retracted or changed source support flags the interpretation for reconsideration. A changed actor record similarly flags an earlier identity judgement. A later edited deadline marks the earlier adoption as historical. Retraction does **not** silently erase an adopted deadline: a requirement may remain operationally binding even if its supporting source is withdrawn. The operator must explicitly reconsider it. Dismissal/reopening never deletes history or reverses a previously applied schedule change.

## Limits

No model runs on this screen. There is no automatic pronoun resolution, fuzzy identity proof, global alias merging, jurisdiction-specific business-day arithmetic, free-form date parsing, or implicit conversion of a claim into an obligation. Natural-language relevance and identity correctness still require professional review. The underlying source-to-plan, independent evaluation, native-browser and production security gates remain open.

The journal is application-level integrity checking, not administrator-proof storage or independently anchored forensic custody. The local app remains for fictional/test cases and a trusted single operator. Original sources, working copies and source context remain sensitive outside those fixtures.

## APIs and tests

Authenticated `/api/v2/cases/{id}/grounding` read plus `/create`, `/identity`, `/disposition`, `/deadline-preview`, `/deadline-apply` POST operations. Extra privilege fields are rejected. The generic case-command endpoint cannot execute the special apply operation.

Run `tests/test_time_review.py`, `tests/test_grounding.py` and `tests/browser_grounding.py` alongside all existing tests. Native navigation was attempted and blocked in this environment; recorded browser results use the explicit ASGI bridge. The workflow includes the new native journey for later authorised integration. No browser security control was weakened.
