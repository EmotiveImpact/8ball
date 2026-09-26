# Integration and acceptance sprint

24 September 2026. `0.2.0-alpha.7`, local and unreleased.

## Scope and input

The exact alpha.6 source tree is `cc821a2c5bfba0aa4027dcdc435d93a33ba5670c`; it was imported as local comparison commit `61ffde6b5b98165d376d0f88345c752d784b5659`. All 794 baseline tests were rerun successfully. The source package includes every previous black-interface, provider, graph, authoring, evidence, grounding, insight and review upgrade. Read-only GitHub inspection still shows `824ca6421ff3100e1af596347f2d1247dde8f8dc`, draft/unmerged PR #2. The earlier source-write restriction was not circumvented. This is not a pushed checkpoint or production deployment.

Work is bounded to existing ES01-05, B02-12 and B02-16 acceptance. No additional commercial vertical, automatic action, tenant service or unproved model-success claim is introduced.

## What changed

ENDSTATE now exposes fully typed nested results while retaining its old JSON/dictionary shape. Cross-field checks catch mismatched snapshots and references. An offline internal wheel build is tested from a temporary installation outside the checkout, and the complete application code suite runs again against that installed kernel. Original wire/audit and fictional cross-domain tests remain intact.

One consolidated runner records exact source hashes, logs, JUnit counts, browser evidence, wheel and schemas. It checks all ten browser suites, not a selected subset. Native, explicit bridge and code-only runs remain distinct. Artifact inspection rejects missing/changed evidence and reports a blocked run as blocked, not success. Ordinary acceptance strips provider credentials and operator database settings.

The actual-provider twenty-check integration path uses the frozen supplier fixture and real adapters only when explicitly authorised and configured. It contains no fallback graph or fabricated model output. Scripted mixed review tests API mechanics; its synthetic result observations are labelled as fixtures. Native mode adds genuine UI reload/download; HTTP mode is not native acceptance. Neither claims independent human judgement or a fully passed PRD.

Navigation now focuses the destination heading. Dialogs have visible-title labels, preserve the original return point across replacement, trap focus and restore it on Escape. Forced colours, clear focus rings, reduced motion and live-error announcements improve the existing black workspace without adding a screen.

## Observed evidence and limits

855 current code tests passed, including 61 new checks, and all 855 passed against the installed ENDSTATE wheel. All ten browser suites passed with 344 explicitly bridged checks, including 36 new accessibility interactions. Complete consolidated evidence is emitted by `scripts/acceptance.py` and carried in the developer pack. The in-repository summary is `docs/evidence/integration-acceptance-local-verification.json`.

Native navigation returned `ERR_BLOCKED_BY_ADMINISTRATOR`. The policy was unchanged. The local model runtime was unavailable, selected hosted configuration was absent, and official download-host probes failed DNS. No live inference or model installation occurred. Independent expert judgement, human screen-reader testing and supported-platform release validation are not completed.

## Emergence Review

What did this sprint reveal that we had not properly seen, specified or understood before we built it?

- EM-050: nested result contracts deserve the same structural discipline as input contracts; a typed envelope around opaque dictionaries is insufficient.
- EM-051: a test report must be bound to both source and evidence bytes, or old successes can be mistaken for a new build.
- EM-052: building a wheel is not testing it; the installed distribution must run separately from the checkout.
- EM-053: interrupted or replaced UI surfaces must preserve operator focus and orientation, not merely data.
- EM-054: actual inference plus scripted review is still not independent semantic judgement or a complete native-user acceptance.
- EM-055: configuration, runtime availability, inference, correctness, integration, deployment and release are distinct gates and must remain distinct in reports.

All six discoveries are retained with owner review pending. The first four are adopted in bounded existing work; the fifth and sixth are adopted reporting/acceptance rules, not claims that the remaining gates passed. No prior discovery is deleted or rewritten.

## Next handoff

Use one cumulative source/patch, verify the exact base and preserve newer Codex changes. Run native acceptance in an authorised environment, inspect its source-bound report, and run the unchanged actual-provider gate only after provider configuration is intentionally supplied. Collect independent operator labels under the existing quality protocol. Keep source-to-plan and release gates blocked until their evidence actually exists; do not replace them with the 855-test count or the new wheel artifact.
