# Operations lane handoff — 25 October 2026

Branch: `devin/1792969169-roadmap-operations`. Starting partition:
`56c9b79428a612dff11e2fae0219640d156032ff`; inspected runtime baseline:
`baca8ad9efa531e5f172058845852963d7d5234a`. Functional source:
`7c80f5ef30466eefbbaede6c9d33a3fc9207c21c`. The later transfer commit adds only
owned evidence/handoff fragments; obtain its exact SHA from the final branch receipt.

## Delivered engineering, not task acceptance

| Existing task | Demonstrated portion | Still open |
| --- | --- | --- |
| B03-05 | Transactional scoped incident/revocation records; exact revision/idempotency; six current surface probes; signed checkpoints; actual new-file SQLite restore/replay including alpha lineage | Agency adapters/migration; current remote-surface consistency; independent anchor/key custody; managed encrypted backup/restore; monitored operational service and accepted recovery targets |
| B03-06 | Offline fictional-participant protocol and four-dimension observations; missing/fail/unknown and unresolved critical/high findings remain blockers | All ledger prerequisites; qualified real users, consent, authorised pilot, independent confidentiality/usefulness/corrections review; no real pilot performed |
| B10-01 | Offline artifact matrix for onboarding/support/terms/licence/ownership and a usable engineering triage/onboarding runbook | Actual legal/brand/licence decisions, support/service terms, operating owner, customer onboarding acceptance and upstream pilot |
| B10-02 | Per-environment/source-commit/digest/freshness evidence consumption; software/human/legal/independent/owner evidence kinds cannot substitute | All advertised capability, human accessibility, model-policy, security/recovery/customer acceptance gates; B10-01/B04-03 and explicit release/deploy authority |

Canonical registers were frozen by the partition. **No statuses, required flags,
acceptance, dependencies, prior evidence or blockers were edited.** Recommend that
integration records bounded partial engineering and external blockers only, never
`verified` for any of these tasks from this lane. The absence of baseline blockers is
not evidence that an external decision exists.

## Recoverable evidence

- Full receipt with ER-01..15: `docs/operations/2026-10-25-operations-2101512c.md`.
- Source/artifact digests, eleven passing individual native report payloads and failed
  Studio traceback: `docs/operations/verification-2101512c.json`. All twelve suites were
  rerun on the exact functional commit with provider settings stripped and unchanged
  runtime/canonical source checked before and after; 11 passed and Studio alone failed.
- Exact adapter/migration/route operation map and runbooks: `docs/operations/README.md`.
- Canonical append proposals: `operations-emergence.json` (EM-193..199; unused reserved
  IDs are not findings) and `operations-changelog.json` in this directory.

Suggested unique evidence IDs for central addition, preserving all existing entries:

- `EV-OPS-JOURNAL-2101512C`: `tests/test_operations_journal.py`, 32 isolated transaction,
  revoke/expiry/tenant/matter/case denial, stale/idempotency/cancellation/tamper/error tests.
- `EV-OPS-RECOVERY-2101512C`: `tests/test_operations_recovery.py`; real Ed25519 checkpoint,
  backup/audit replay and original alpha import lineage. Part of the combined 82 tests.
- `EV-OPS-READINESS-2101512C`: `tests/test_operations_readiness.py` and
  `tests/test_pilot_tooling.py`; part of the combined 82 tests; consistency/fictional only.
- `EV-OPS-VALIDATION-2101512C`: `docs/operations/verification-2101512c.json`; 1438 source
  tests passed; 10/11 original native suites passed (352 checks), one Studio assertion
  failed; additional event-review 27 passed. Not a green integrated acceptance receipt.

## Integration instructions

1. Apply this lane's commits additively, without importing another lane or overwriting
   upstream `2b1b465ebfa1b433c8f128b0478f6806dce9e2e7` documentation/evidence. Its test
   receipt does not cover these changes or integrated code.
2. Review `eightball.operations.journal.SCHEMA`; approve the three proposed ops tables
   explicitly and use the same current-grants transaction/database. No shared migration
   was run. No new dependency is required (`cryptography` comes from existing crypto extra).
3. Inject operation-specific current agency authority and safe scoped probes exactly as
   documented in README. Unknown/absent adapters deny. No local-operator bearer fallback.
4. Register `register_operations_routes(router, service)` only on the verified agency
   router, add exact method/operation mappings, populate `request.state.agency_identity`,
   and retain CSP, validation redaction and host request/rate limits. No router self-mounts.
5. Recovery/manifest CLIs stay offline host-only. Whole-DB rehearsal is not a matter-scoped
   export or HTTP restore. Scope binding must be established before signing checkpoints.
6. Merge fragments by stable ID into canonical JSON; preserve immutable prior entries,
   add unique EV entries and update only actual task evidence/next-actions/blockers.
   Regenerate emergence, delivery and changelog Markdown centrally. Local prospective
   union validation does not mean those canonical files are already integrated.
7. Fix the **existing** `tests/browser_studio.py:149` assumption that the latest changelog
   must say `local unreleased`: the truthful frozen partition entry says `pushed unreleased`.
   Do not fabricate a local-only delivery state merely to get green checks. Rerun full
   source-bound native acceptance after all wiring and canonical changes.
8. Cross-lane negatives must cover unknown agency routes, bearer isolation, cross-scope
   target handles, expiry/revoke before/after probe or claim, missing vault policy,
   quarantine/scan/retention, cancelled workers and stale reviewed projections. Local
   probe callbacks here are fixture adapters, not real remote-surface guarantees.

## Verification and limits

1438 pytest tests passed after correcting initial Node PATH failures; 82 targeted tests
are included, not additive. Python compilation and all 18 browser-module syntax checks
passed. Native HTTP suites and exact limitations are retained in the receipt. Studio
failed three times at the same shared-changelog assertion and remains open. No mock/bridge
substitution, actual inference, paid call, model download, real client data, new runtime,
PR/main change, release, deployment or independent/human acceptance occurred.

## Emergence Review

New evidence confirms that checkpoint signing is not independent custody; scoped
checkpoints do not scope a whole-DB restore; cross-surface revocation observations are
not revocation commands or remote atomicity; files do not authenticate human decisions;
fictional resolution references cannot erase failed observations; constrained support
metadata needs a separately controlled narrative artifact; and shipping state is not
the running version. EM-193..198 refine existing tasks, EM-199 is a retained integration
decision. No new required roadmap scope or customer-value claim is made.

Next action: integrator connects real adapters and canonical fragments, resolves the
retained shared Studio assertion, then reruns source-bound combined native/security
acceptance. External gates require their actual authorised owners, not more fixtures.
