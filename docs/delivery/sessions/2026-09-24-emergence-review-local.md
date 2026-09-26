# Session: mandatory emergence review

Date: 24 September 2026. Environment: ChatGPT local continuation.

## Objective

Make end-of-build product discovery explicit and enforceable across this chat and Codex without silently expanding the accepted roadmap.

## Changes

- Added `docs/delivery/EMERGENCE-REVIEW.md` with the mandatory question, classification scheme and first observed/candidate findings.
- Added the rule to `AGENTS.md`, `docs/delivery/HANDOFF.md`, `docs/PRD.md` and `docs/ROADMAP.md`.
- Extended changelog validation so each newly added build entry must contain an evidence-labelled emergence review.
- Added regression tests for the rule and rendered emergence findings in generated / in-app product history when present.

## Emergence Review

**What did this sprint reveal that we had not properly seen, specified or understood before we built it?**

The act of formalising emergence itself exposed that product discovery needs a governed promotion path. Without one, either the roadmap freezes too early or every interesting observation becomes scope. We now treat discovery as evidence that must be classified before it can alter a version gate.

Current product findings captured in the dedicated review include: the two-graph distinction (reality/provenance vs outcome/action), information-acquisition actions, freshness and supersession, machine-readable watch/replan triggers, operator attention as a possible resource, and the possibility of outcome envelopes.

Evidence level: process observation plus implementation-grounded product hypotheses.

Roadmap disposition: governance rule is required (`DOC-05`); the product findings remain linked to existing work or explicit candidates until separately promoted.

## Verification

- 568 automated tests passed.
- 44 Plan Studio/changelog browser checks passed using the explicit ASGI bridge.
- Python compilation, browser JavaScript syntax, changelog generation and delivery-ledger checks passed.
- Native browser networking/storage/CSP and model inference were not tested by this process-only checkpoint.

## Release boundary

Documentation/process build only. No runtime planning semantics, model-quality gate, merge, deployment or production-readiness claim changes.
