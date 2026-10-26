# Seven-lane integration — 26 October 2026

Branch: `devin/1792969169-roadmap-integrated`. Assigned base: `56c9b79428a612dff11e2fae0219640d156032ff`. Runtime comparison baseline: `baca8ad9efa531e5f172058845852963d7d5234a`. The containing source commit is the recoverable functional checkpoint; fresh acceptance will identify its exact commit, source manifest and artifact paths in a separate receipt.

## Source reconciliation

Integrated exact lane heads in dependency order: identity `5f7060c498b56ba48a5d1dcdd58b1efa6548071c`; events `e1465d58310fcd4865b5cf46e60c57f732c2ed37`; vault `b95f33568856861823468e09f7a8b56c16a4732f`; collaboration `5879903caad062aac4d6c8981ac4a4ffef3569c7`; operations `96f695d0cb9c28d6bf891513e39e9ca1496dd12a`; domain packs `1ec913806dd84e0577f35f2fcb49ef4ee4f15dd1`; intelligence `47c355a79eae0f6a989080c4b0323713db7c5649`.

Later agency documentation/evidence `2b1b465ebfa1b433c8f128b0478f6806dce9e2e7` is reconciled additively: retain its original changelog entry, complete-result session and exact source-bound receipt. It is baseline evidence, not an integrated-tree pass. All lane changelog/emergence fragments are merged by ID. No original discovery, failed experiment, acceptance requirement or blocker is removed.

## Functional integration

See [AGENCY-HOST](../../v2/AGENCY-HOST.md). Added explicit optional host/router/configuration and transaction-local identity, scope, vault-source, disclosure, event-worker, operations, knowledge and read-only pack adapters. Added usable isolated desk, client-only access and session-mode event-review controls without weakening CSP or local workflows. Missing production scanner/source/deletion/processor/probe adapters deny. Upload limit is at most 400000 bytes only on the exact vault upload route; the advertised 262144-byte original fits. Package registration and recursive wheel-content checks include pure nested ENDSTATE packages.

## Actual verification and preserved failures

- Initial integrated full unit run: **1778 passed**, one upstream Starlette/AnyIO deprecation warning, 81.70s. This predates the final four worker-invalidation regressions and session-review UI change; it is not the final acceptance total.
- Initial 258 focused lane/current-identity tests passed. Initial nine new host tests passed, including current-client disclosure, long-scan logout and actual/misdeclared/oversized body limits.
- Initial native agency run reached upload/quarantine/scan/download/packs/knowledge/operations, then an ambiguous locator failed. A subsequent run exposed long SHA text overflow at390px; wrapping fixed it. Another run demonstrated a real host UI lifecycle mismatch: vault mount returns an object, not a disposal function; the adapter now explicitly calls its dispose method. The corrected isolated agency run passed **14 native TLS checks**, including390/768/1440px and revocation clearing. Artifacts remain under `artifacts/agency` locally until fresh acceptance retains a source-bound run.
- Initial package regression collection exposed `test_vault_api` importing another test by top-level name under importlib mode; its import is now package-qualified. Initial worker-logout fixture exposed identity exceptions not normalised to the service permission contract; host current-principal resolution now normalises only authentication denials, preserving other failures.
- Final focused host/vault importlib run: **19 passed**, including cancellation, logout, review revocation and changed source policy after worker claim, with no repeat controlled call. Expanded native agency suite: **16 checks passed**, adding cookie-session source/result review and lock clearing. The first expanded run failed because the fixture lookup named a nonexistent table; corrected to the actual schema before rerun.
- Commands naming nonexistent test globs ran zero tests; they are setup mistakes, not passing or failing test evidence.
- Full final native acceptance, installed-wheel regressions and exact `--inspect` are pending at this checkpoint. No failed run is relabelled as passing.

## Emergence Review — ER-01 through ER-15

What did this sprint reveal that we had not properly seen, specified or understood before we built it?

1. **ER-01:** Individually tested modules still need explicit identity, lifecycle, package and UI adapter contracts. Evidence: integrated host tests and native disposal failure. EM-254, existing_task.
2. **ER-02:** A green unit count did not disprove mobile/private-state problems. Counterevidence retained above; real IdP/security/human reviews remain missing.
3. **ER-03:** Vault sources connect apparently separate projection, reference and event routes; each consumes exact source state, not just matching identifiers.
4. **ER-04:** Independent production-policy/key/session review would most change confidence. A fixture scanner and local key wrapper are not that review.
5. **ER-05:** Keep the owner's fixer outcome central. A curated client update, selected course and source observation are different; none authorizes an action.
6. **ER-06:** Logout/revocation after claim/scan, changed source/case revisions and changed processing consent must trigger rechecking, not later publication from a stale preview.
7. **ER-07:** Current sessions, storage, source policy, disclosure and the narrowly scoped upload body cap belong in 8BALL; pure pack/reference contracts and nested wheel modules belong in ENDSTATE. EM-254/255 are existing_task integration findings; no optional research candidate becomes required scope.
8. **ER-08:** Production IdP/scanner/KMS/egress/deletion/probe infrastructure and external inference/pilots are not implemented by the fixture adapters. Missing adapters explicitly deny. EM-256 and the existing ledger blockers retain the choice for owner review.
9. **ER-09:** Actual focused/native passes and every material failed integration experiment are listed above. Full exact-source acceptance is pending at this checkpoint; real IdP, independent security, malware efficacy and human/semantic accessibility remain unverified.
10. **ER-10:** Cross-service policy drift, genuine multiuser behavior and unforeseen operator correction burden may remain. The owner can append a discovery/decision or explicit case review without replacing preserved observations. No automatic required-scope expansion follows.
11. **ER-11:** The owner selected completion of the current shared roadmap, not a replacement product. Existing case-selected courses are not switched by this integration or a changed ranking. Changed target, source, approval/case revision or consent requires explicit reconsideration, not automatic selection or action.
12. **ER-12:** No real clients, provider keys, optional upstream research code, professional operators or live model inputs were processed. Fixtures cover four pinned catalogues, not all possible plans. Limited text and source/object scope must not imply a global negative.
13. **ER-13:** The integrator corrected locator/mobile/disposal/import/session-exception and native fixture-query failures; original failures remain described above. Safe recovery is explicit refresh/reauthorisation and separately reviewed retry; no paid request repeats automatically and already-sent requests cannot be recalled.
14. **ER-14:** Exact seven lane heads and later baseline receipt are retained; the containing source commit is recoverable. Baseline1349/423 evidence must never cover this integrated tree. Full new-source acceptance/inspection must be recorded separately; unsupported production or reported-only model claims remain unaccepted.
15. **ER-15:** Client-only projections can now open without internal case access, and withheld stale sources distinguish safe absence from false certainty. These plausibly improve the next decision but are not measured operator-value evidence. Measure safe task completion, correction/recovery burden, inappropriate disclosure and outcome usefulness with qualified operators before claiming benefit; more controls/screens alone do not pass that gate.

Evidence level: supported_by_tests for the named unit/native behaviors; observed_in_build for integration/lifecycle discoveries; operator-value and production suitability remain unproven. No market hypothesis is promoted to implementation or accepted scope. EM-254..256 append these integration findings; all seven lane discoveries remain individually retained.

## Handoff and unfinished gates

At this functional checkpoint, changes are local/unreleased until an actual push is verified. No PR/main change, merge, release/deploy, live provider call, model download, real-client data/pilot or independent sign-off occurred. Fresh source-bound acceptance and publication status will be appended separately, never attached to the earlier baseline. Production identity/TLS/security/KMS/scanner/retention/egress/deletion/revocation adapters, PostgreSQL/managed operations, semantic/provider quality, human accessibility/legal/brand/customer/qualified-fixer/commercial acceptance remain unfinished.

Verified environment matches the existing repo blueprint: Python3.12.13 .venv, requirements-dev, setuptools82.0.1, cryptography, Node24.19.0 on PATH and installed Playwright Chromium. No extra blueprint commands are necessary. Keep all provider credentials stripped during ordinary acceptance.
