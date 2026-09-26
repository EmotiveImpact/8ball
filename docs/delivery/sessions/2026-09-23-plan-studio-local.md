# Plan Studio, analysis jobs and mandatory product history

## Scope and source

This local build extends the supplied Graph Explorer source tree `827f0ba92ffcdf0c74fe89fbf2ca41e3b2d81302`. Its remote ancestor remains `824ca6421ff3100e1af596347f2d1247dde8f8dc` at inspection. The reconstructed local Git parent exists only to generate exact-base patches; it is not a pushed commit or an alternative remote history.

The owner requested a continuously updated changelog, a permanent instruction for ChatGPT and Codex, and a substantial build towards the next version. This implements B02-13's guided authoring and the local B02-15 job lifecycle. It does not bypass B02-09's failing actual-model source-to-plan gate.

## Implemented

Plan Studio edits a detached graph with nested AND/OR, explicit false requirements, guards, effects, objectives, confirmation criteria, decision gates, named resources, durations/waits and explicit contingencies. Undo/redo and discard affect only the draft. The preview service applies the exact existing command validator to an in-memory candidate and computes route/delta differences without persistence. A separate human commit uses the existing optimistic revision and audit transaction. Observed meanings and completed actions remain protected. The black relationship explorer is preserved and remains read-only.

Local analysis jobs record request identity, status, stage counts and completion/cancellation. Jobs use one shared inference slot with a bounded queue. Context validation precedes admission. Cancelled or superseded jobs cannot publish a proposal, even if a late response arrives. No automatic retry or restart resume occurs. Interrupted work is marked as such on server restart. A provider call already sent may still finish or be billed; cancellation does not promise otherwise. Stage checkpoints prevent further requests and discard results. This is a single-process local service, not production agency orchestration.

`docs/delivery/changelog.json` is the canonical product history. The app's What’s new view and generated `CHANGELOG.md` read it. Task statuses still belong exclusively in `progress.json`. `scripts/changelog.py --check --base <sha>` requires an added entry for a changed build and rejects deletion or rewriting of historical entries. AGENTS and the shared handoff require this for every future build.

## Verification boundary

484 automated code tests passed. All five browser suites passed through the bridge, totalling 174 checks: 27 legacy, 51 V0.2, 15 provider/black, 38 Connections and 43 Plan Studio/job/changelog. Exact results and report contents are recorded in `docs/evidence/plan-studio-local-verification.json`. Native navigation was attempted and returned `ERR_BLOCKED_BY_ADMINISTRATOR`. The policy was not changed. The explicit existing ASGI browser bridge is used for local interaction checks; it does not establish native browser networking, CSP enforcement, session storage or actual downloads for this checkpoint.

Provider tests use controlled functions and HTTP responses, not real Hugging Face, Qwen or JEV inference. Cancellation races are tested against the real job/store state machine with controlled blocking responses. No secret or model download is included.

## Release boundary

`0.2.0-alpha.2` names this developer build, not acceptance of all V0.2 requirements. Nothing is merged, deployed or released. The previous GitHub source-write block is not bypassed. A cumulative patch/source pack preserves every preceding local HF, black-design and graph-explorer change. Native CI and authorised integration remain required.


## Integration and next actions

Apply the cumulative patch to a clean checkout of the inspected remote base, or reconcile it with newer authorised commits. It already includes both earlier unpublished checkpoints. Run all five native browser scripts and code/governance checks. Do not weaken a gate to obtain green CI. The source package manifest holds the actual resulting tree and archive checksums; this document does not attempt to embed its own hash.

B02-13 remains implemented, B02-15 partial, and DOC-04 verified within its explicitly local documentation/API/browser scope. V0.2 remains 9/18 required subparts verified, not an effort percentage. A real-provider comparison and independent semantic review remain separate work. Use the source-handling tasks for further development without inventing model credentials or marking Qwen's previous failure solved.


## Regression-test changes

The existing V0.2 browser test now waits for a published rules-capture proposal after asynchronous queue admission instead of treating navigation as completion. Assertions and evidence semantics were retained. The new changelog test waits for entry content and accounts for the rendered uppercase version label. No application policy, source validation or model acceptance threshold was weakened.
