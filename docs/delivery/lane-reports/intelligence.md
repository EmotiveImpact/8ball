# Intelligence lane — 25 October 2026

Session: `f3c5604865654b42ad08e573aa871c3e` ([recoverable session](https://app.devin.ai/sessions/f3c5604865654b42ad08e573aa871c3e)). Engineering handoff, not product acceptance.

## Branch, source and delivery

- Assigned branch: `devin/1792969169-roadmap-intelligence`.
- Actual branch starting commit: `56c9b79428a612dff11e2fae0219640d156032ff` (coordination partition); runtime baseline: `baca8ad9efa531e5f172058845852963d7d5234a`.
- The commit containing this receipt contains the implementation and proposed register fragments. A commit cannot contain its own hash: the exact resulting pushed SHA and remote-head verification are returned in the final session handoff, not fabricated here.
- No other lane, main, PR, release, deployment or real-client data was changed. Later agency documentation at `2b1b465ebfa1b433c8f128b0478f6806dce9e2e7` is not merged here and its evidence is not attributed to this code.
- Canonical JSON/generated ledgers are frozen by ROADMAP-LANES. No task status, original evidence, blocker, optional hold or acceptance text was changed. The two `intelligence-*.json` fragments are append-only proposals for central integration, not another status ledger. Proposed scoped evidence ID for the integrator: `EV-INTELLIGENCE-20261025-KNOWLEDGE`.

## Working changes

1. `endstate/intelligence/knowledge.py`: strict neutral scope, actor context, exact source support, versioned hypothesis and exact-version review contracts. Playbooks require an explicit graph; precedent requires source support. Assumptions, current authority, verification criteria and limitations are mandatory. Drafts are bounded to 250,000 encoded bytes; no database, HTTP, provider, model or 8BALL imports.
2. `eightball/intelligence/knowledge.py`: injected-transaction SQLite reference journal. Every row is organisation/matter/case scoped. Exact revision and current-authority checks, payload-bound request IDs, source revalidation, independent-author review, immutable kind, terminal retirement, read/history, deterministic bounded lexical search, explicit review-only notices. No daemon, connection or schema mutation on import.
3. `eightball/intelligence/api.py`: relative GET search/read and POST draft/review/retire registration with server-owned authenticated context. No shared router modifications. Generic permission/conflict/unavailable/invalid-request errors do not include source bodies.
4. `eightball/v2/playbooks.py`: `reviewable_playbook(id)` copies existing starters into explicitly unvalidated graph-only drafts. It does not approve, select, apply, import or generate a plan. Original starter files are unchanged.
5. `web/v2/intelligence-knowledge.js` and `.css`: separately mounted search/reference/review component. Exact versions and digests, source quotes/Unicode offsets, immutable graph/history, labelled controls, keyboard focus, loading/error/empty states, escaped text, scoped graphite styles and mobile wrapping. Review needs an explicit rationale/scope; no automatic retry after uncertain failure. Superseded/disposed responses cannot overwrite the view. This module is not mounted in navigation.
6. `eightball/v2/runtime_status.py`: exact configured-model metadata only; digest/size/detail allowlists, registry-port-aware tags, and ambiguous/invalid inventory remains unknown. Installation listing never means loaded, inferred, accurate or approved. Existing GET-only bounded local probe; no model download, loading or inference.
7. `tests/test_learning_knowledge.py`, `tests/test_learning_knowledge_ui.py`, `tests/test_runtime_status.py`: fictional contract, security, concurrency, persistence, runtime metadata and fake-DOM component checks. These are not independent professional labels or native coverage of the new module.

Evidence, proposals, references, human review, chosen course, permission, completion and observed effects remain separate. Returning `use_as_reference` does not verify a fact, attest an outcome or approve an action. No case graph, source, observation, course, approval or execution record is mutated by this service.

## Exact verification and retained failures

Environment: Python 3.12.13; Node 24.19.0; Playwright 1.57.0; Chromium 143.0.7499.4. Prefix `.venv/bin` and `/home/ubuntu/.nvm/versions/node/v24.19.0/bin` on PATH. Development requirements installed in a local venv. The offline wheel command first failed because setuptools was absent; installing the declared `setuptools>=82` build backend (84.2.1 resolved) allowed the real packaging failure below to be observed. Browser binaries were explicitly installed with `.venv/bin/python -m playwright install chromium`. No weights, model downloads, private credentials or paid/live inference.

Final code run:

```sh
PATH="$PWD/.venv/bin:/home/ubuntu/.nvm/versions/node/v24.19.0/bin:$PATH" \
  .venv/bin/python scripts/acceptance.py --mode native \
  --base 56c9b79428a612dff11e2fae0219640d156032ff \
  --output artifacts/intelligence-acceptance
```

Final run ID: `20261025T233752Z-c6a9eb2a`. **Overall FAILED**; `native_browser_verified=false`; no model-quality, expert or release acceptance. Source manifest SHA-256: `75f3bcec64c6dc76bd7b9de8b71ec19486188160148f6004f1c8715451b04f97`; source unchanged throughout the run. `--inspect` returned `valid=true`, `run_status=failed` immediately after the run: a valid record of failures, not a pass. This receipt and the register fragments existed before the final run and were subsequently updated with its results; their final documentary bytes are not in that historical source manifest. Runtime/test hashes below identify the exact unchanged tested implementation. Full runner logs/artifacts remain under the run ID in this session's ignored artifacts directory; the final native archive also retains the pre-update documentary bytes so this historical source snapshot can be reconstructed from the pushed implementation without pretending later record updates were tested. The earlier run `20261025T233006Z-c373a13d` failed on the same three gates before final adapter/capacity hardening. The integrator must run fresh exact-tree acceptance after wiring and fragment merge.

| Check | Observed result |
| --- | --- |
| Full pytest, within final native runner | **1427 passed**, 0 failures/errors/skips; one Starlette/AnyIO deprecation warning |
| Changed service/runtime/UI focus | **71 passed**, including six Node/fake-DOM checks and ten final policy/revision/capacity regression cases |
| Python compilation | passed (`eightball`, `endstate`; separate compileall also included `tests`) |
| All browser JavaScript syntax | passed, including new knowledge module |
| Structural plan-review bench | 8/8; model quality NOT ASSESSED |
| Schema export | passed |
| Delivery/emergence/generated changelog checks | passed against unchanged canonical registers |
| Base-aware changelog | **FAILED**: `Changed build needs a new changelog entry`; frozen canonical ledger awaits central fragment merge |
| Installed-wheel regressions | **FAILED** during collection: `ModuleNotFoundError: No module named 'endstate.intelligence'`; frozen explicit package list omits new nested package |
| Native transport probe | passed; no bridge substitution |
| Native legacy / workspace / provider / Connections | 27 / 54 / 22 / 42 checks passed |
| Native Studio | **FAILED** at `tests/browser_studio.py:149`: `current build and limits visible`; frozen top coordination entry is pushed-unreleased, while test requires literal `local unreleased`. No shared test or shipping state was changed to obtain green |
| Native Sources / Insights / Grounding | 39 / 40 / 26 checks passed |
| Native Plan Review / Accessibility / Chosen Course / Event Review | 35 / 36 / 31 / 27 checks passed |
| Native total | 379 checks in 11 passing suites; Studio failed, so no full native pass |
| `git diff --check` | passed before documentation handoff |

After writing the delivery records, the projected **central** merge of all six proposed emergence items and the changelog entry passed the existing validators, renderers and base/history checks in an isolated temporary validation root with copied evidence paths. No IDs collided and no frozen file was modified. This validates fragment shape/history only; the actual branch's base-aware changelog remains failed until integration appends the canonical entry. A native artifact archive is retained with the session handoff; it is not committed into product source.

The new component is absent from the shared navigation, so these native suites cover existing app preservation, **not native acceptance of the new knowledge workflow**. The six fake-DOM checks cannot supply browser, screen-reader, human accessibility or mobile visual acceptance. No testing agent was used; only the repository's authorised shell test commands.

Negative coverage includes exact negation-bearing Unicode quotes; stale/wrong hashes and offsets; duplicate source ranges; changed/retracted/unauthorised sources; organisation/matter/case isolation; item revocation; author self-review denial; revocation and case revision change during source validation; transaction rollback on commit failure; concurrent duplicate/stale writes; request-ID replay and payload conflict; persistence after restart; new-version review reset; inability to revive retirement; source-independent retirement after withdrawal; prompt-like source text staying data; API current-context mismatch; late/disposed UI responses and uncertain write failures without retries. All adapter tests are controlled SQLite fixtures, **not integrated agency/vault security approval**.

### Tested implementation SHA-256

| Path | SHA-256 |
| --- | --- |
| `eightball/intelligence/__init__.py` | `e048ead84a75a5662c0cb06c2be1fb99143fc921dd989e4ada2083c80af6a585` |
| `eightball/intelligence/api.py` | `ee1f9654df06ec9568c969bce936322e5b58108275f7cac006496ac2abf71994` |
| `eightball/intelligence/knowledge.py` | `2bd0fa8e4a1dc215fde669a2ed42dffad82a73e2b1942fc7a2cba90571a0ddf5` |
| `eightball/v2/playbooks.py` | `7baf2fccc73c35c07403cff830b01d72195231ac256d2a89d7d5a30c8fabf877` |
| `eightball/v2/runtime_status.py` | `2e6f3289b27f3a52a3374eb9ae7cae421e32a374328790702e7bb7e4f3b1da48` |
| `endstate/intelligence/__init__.py` | `7fd0695e2b32eeb97c58b1781d3e4f71bc610f5a08c718ad306a5e152cbcdcd4` |
| `endstate/intelligence/knowledge.py` | `a90e429777687956211d6980bdc2f25198830650ab4f21edc394b16c881426b3` |
| `tests/test_learning_knowledge.py` | `02572cb40c252fed94a77b659bc2b69b8144ee70efd7c0ea86256c340a21e998` |
| `tests/test_learning_knowledge_ui.py` | `42c9f6b4c290dd715bd0dabfb18ade9baf17d6b64014a970d7a781f014014163` |
| `tests/test_runtime_status.py` | `dd12b38b5853a825efdef577d3b646e4dc7a29e67f28f90da2c80872ea333d5b` |
| `web/v2/intelligence-knowledge.css` | `be42c101e59646e98d6c002ec59b70e0d7d2da7ea0514c67ec975fd32a6c4cd9` |
| `web/v2/intelligence-knowledge.js` | `50ecdc41ee8f711dafb270c3d354c8e24c84f3559ff9deba41eab7236db5d800` |

## Precise integration instructions

### Package and storage (integration-owned)

1. Add `endstate.intelligence` to the root setuptools package list (currently only `endstate`) without removing existing packages. Extend recursive kernel source fingerprints/coverage in packaging/acceptance code where needed; do not label the current wheel complete. Rerun `python scripts/build_endstate.py --regressions` offline after that change. No new runtime dependency is introduced by this lane.
2. Apply the explicit `SCHEMA` tuple from `eightball.intelligence.knowledge` as an integration-owned migration on a fictional sandbox first. The sole new table is `intelligence_knowledge_events`; no existing table/schema is changed here. Do not execute CREATE on an operator database at import or assume the table exists.
3. Supply `transaction() -> ContextManager[sqlite3.Connection]`: begin a write-serialising transaction, yield the connection, commit only after all checks succeed, rollback on every exception, close after completion. Tests use `BEGIN IMMEDIATE`. Case revision, object grants, source metadata/body eligibility and journal writes must be consistent in the same transaction. An independently changing external policy/body adapter without atomicity/version checking does not satisfy this contract.
4. Supply `authorise(conn, KnowledgeContext, operation, item_id) -> bool`. Only literal `True` authorises. **Exact operation strings are `knowledge.draft`, `knowledge.review`, `knowledge.retire`, `knowledge.read`, `knowledge.search`** (not `knowledge.write`). Writes and reads recheck current permission before return/commit. Search also checks per-item read access. Map all operations through identity's current role/matter/object policy, deny absent mappings. Search permission also exposes the case-scoped library revision; do not grant that metadata permission to a role allowed only one object's read endpoint. Author status or a local operator token never supplies agency authority.
5. Supply `resolve_source(conn, context, source_id) -> SourceSnapshot(text, active)` through current vault/source policy. Explicit ID lookup only: authenticate organisation/matter/case/object access, retention/scan/quarantine/processing policy eligibility and immutable body identity. A missing/denied adapter must reject, never fall back to global or local-bearer reads. The service checks exact UTF-8 SHA-256 and Unicode code-point offsets/quote. The adapter must not normalise text, merge entities or silently extend source selection. The tested adapter is not a managed vault.
6. Supply `case_revision(conn, context) -> int` from the current case snapshot and optionally a timezone-aware UTC `clock`. Draft/review/retire require exact expected case and library revisions. A queued/replayed request is not permission revival; cancellation, worker lifecycle and paid-provider replay remain event-lane concerns, not automatic functionality of this service.

### API and UI (integration-owned)

7. Construct `KnowledgeService(transaction, authorise=..., resolve_source=..., case_revision=...)` only when all adapters exist. Register `register_intelligence_routes(router, service, context_for_request=...)` under the existing authenticated `/api/v2` router only after identity supplies the current server-resolved actor/org/matter/case context. Reject wrong/missing/expired identities. Do not expose the seam on the legacy local bearer path. No client body supplies identity or scope.
8. Routes: `GET /cases/{case_id}/knowledge?q=&limit=20`; `GET /cases/{case_id}/knowledge/{item_id}?history=true`; `POST /cases/{case_id}/knowledge/{item_id}`. POST requires request ID and nonnegative expected library/case revisions plus exactly one of `draft`, `review`, `retire=true`. Draft version is generated by the service; review names exact `version` and `draft_sha256`. Errors: 403 permission, 409 changed case/reference/request, 404 unavailable source/reference, 400 invalid bounded service request; FastAPI body validation remains 422. No automatic retry on ambiguous server/commit failure: reload and inspect current history.
9. Import `mountKnowledge(root, api)` and load `intelligence-knowledge.css` explicitly through existing CSP-compliant asset loading. Inject case-bound `api.search(query)`, `api.read(item_id)` (request history), and `api.write(item_id, body)` returning parsed JSON and rejecting non-2xx responses. Use existing authenticated API handling. Dispose the module on case/navigation changes. Do not remount onto a different case while retaining old closures. No course selection, source attestation, graph application, external action or provider processing is wired by the component.
10. Add a governed draft-creation/import entry only after authority requirements are met. `reviewable_playbook(id)` is a plain draft factory; deliberately no starter is auto-seeded or selected. Existing complete starter case must still be inspected before any separate import. Expose new runtime `inventory_verified`/`selected_weights` fields alongside the existing status view if desired; never infer loaded/accurate from listed weights.
11. Merge fragment items/entries additively by ID, retain older failure/agency evidence, register scoped evidence only after checking source, and regenerate emergence/delivery/changelog Markdown. The base-aware changelog gate must then pass without historical erasure. Resolve the Studio fixture's hardcoded local-unreleased expectation with truthful shipping-state semantics; do not mislabel pushed code to satisfy it. Run all integrated security and native checks on the resulting exact tree, including unknown-route denial, local-token/agency isolation, cross-matter/object access and mid-operation revocation.

### Retention and deployment limitations

This is a bounded single-SQLite reference journal: normal writes stop at 500 scoped events, but one terminal retirement per existing item remains possible past that limit. Search is lexical title/summary matching (query <=300 characters, limit 1..50); there is no model learning/training or cross-client retrieval. It is not a production retrieval system, queue, remote vault, tenant database or backup service. Draft quotes and historical review text remain at rest in the journal after source withdrawal: service denial is **not secure erasure**. Managed retention/deletion, encrypted custody, scan results, reviewer qualification, tenant isolation, search permissions and production policy require their owning integrations and review before agency/client use. The source adapter must fail closed while those prerequisites are absent. Final negative tests require literal source `active=True`, an actual text body and a known nonnegative integer case revision; truthy strings/numbers and unknown revision metadata cannot authorise use.

## Task-by-task engineering boundary

| Assigned IDs | Evidence and remaining gate |
| --- | --- |
| B02-09, ES03-02 | No actual-model run. Retained Qwen failure remains a failure; no template substitution or synthetic completion. Actual-model valid/useful graph acceptance remains open. |
| B02-10 | Exact support/negation fixtures exercise reference copying only, not independent multi-source extraction semantics or scheduling acceptance. |
| B02-11 | No expert-labelled held-out dataset, reviewer threshold approval or independent semantic score invented. Existing protocol remains unfilled. |
| B02-12 | Existing native app regression attempted, overall failed; no new actual-model twenty-step journey, and new knowledge module unmounted. |
| B02-14 | Exact source digest/Unicode support, history/retraction/isolation checks added for references. Longer-source extraction, duplicate/entity semantics and integrated vault gates remain broader unfinished scope. |
| B02-15, ES03-04 | Read-only runtime metadata truthfulness improved and tested with controlled HTTP. No live runtime/weights/inference quality or real model cancellation acceptance claimed. |
| B02-16, B02-19 | New module uses labelled/keyboard-safe/scoped graphite controls and has six component tests. Existing native accessibility checks pass, but new-module native desktop/mobile/platform and independent human/screen-reader review remain open. |
| B02-18 | Full runner FAILED on three integration-owned gates; no integration/release approval. No acceptance status promoted. |
| B02-20 | Existing graph/native Connections regression passes; no graph explorer code changed and no broader scope claimed. |
| ES03-01 | Neutral typed knowledge contracts added outside product service. Source-tree passes; installed package currently fails until manifest integration. Existing compiler remains unchanged. |
| ES03-05 | Existing refusal/timeout/provider suites rerun; no new provider quality measurement, actual inference or lifecycle dispatch implementation claimed. |
| B04-01 | Versioned exact-digest starter review infrastructure implemented. No professional review, specialist qualification or successful outcome invented. |
| B04-02 | Source-linked, scoped reference service/negative tests implemented with injected adapters. Integrated agency identity/vault/retention and production leakage/security acceptance remain open. |
| B04-03 | No measured operator benefit, pilot, causal claim or success probability. Manual usefulness study remains necessary; tests do not measure customer value. |
| B02-21, B02-22, ES03-03, ES03-07, ES03-08, B04-04 | Optional no-implementation holds preserved. No live classifier/HF run, repair/research adoption, correction replay/training or independent insight-review sign-off. |

## Emergence Review — ER-01 through ER-15

What did this sprint reveal that we had not properly seen, specified or understood before we built it?

Reserved findings **EM-233..EM-238** are proposed in `intelligence-emergence.json`, all owner-review pending with no acceptance links. EM-239..252 are unused reservations, not discoveries. No new required task or optional-scope promotion.

| Prompt | Answer, evidence and disposition |
| --- | --- |
| ER-01 — New observation | A reviewed hypothesis needs immutable version/digest identity, not an item-level approved flag: new versions cannot inherit prior review. Implemented under B04-01/02; EM-233, supported by tests. |
| ER-02 — Disconfirmation | Exact quote support does not establish truth, causal relevance or specialist quality. Counterexample tests keep negation/prompt-like source text unchanged. Owner/professional reviews can reject these references. EM-233/237; no factual pass. |
| ER-03 — Connections | Identity, source eligibility and case revision all meet at one transaction. A review's source access can be withdrawn independently of draft identity; no hidden shared-source scan or cross-case retrieval. EM-234; existing B04-02. |
| ER-04 — Next useful question | Which references actually reduce correction work or time to a sound fixer decision? A predeclared human comparison, not more generated plans, can answer. EM-237, deferred measurement under B04-03. |
| ER-05 — Target | The module aids the fixer in inspecting hypotheses; it does not replace 8BALL with a generic learning product, change the client's goal, claim an industry app or select an outcome. Existing scope only. |
| ER-06 — Staleness/effects | Withdrawn/changed sources must deny retrieval/review and replay; an exact new draft needs a new review. Retirement must still be possible after source withdrawal. No watcher, factual reversal or external cancellation is inferred. EM-234. |
| ER-07 — Placement | Pure contracts belong in ENDSTATE; identity, SQLite, source and route policy stay in 8BALL. Installed-wheel regression proves package inclusion also needs explicit integration. EM-236, existing ES03-01. |
| ER-08 — Not implemented | No semantic embeddings, similarity-based identity merges, automatic training, inferred success scores, live model/provider run, research runtime or optional replay. Keep professional/human/platform/production gates open in the canonical ledger. EM-237 retained for owner review. |
| ER-09 — Actual result | 1427 source tests passed; 379 checks in 11 native suites passed; Studio, base changelog and installed package failed. New UI component is fake-DOM-only. Original failures retained; EM-236/238, no broad verified claim. |
| ER-10 — Blind spots | Same-source support can still be incomplete or misleading; global library revision is metadata; local append-only quotes are not secure deletion. Review burden and real eligibility adapters remain risks. Owners may append decisions/hypotheses; no invisible auto-backlog. EM-234/237. |
| ER-11 — Chosen course | No course is selected or reconsidered by reference review. Existing course records remain untouched; new evidence/authority changes need separate reviewed case commands. No automatic strategy switch. |
| ER-12 — Coverage | Search is lexical, scoped and bounded, not comprehensive/semantic. Unreviewed precedent is excluded; unreviewed starters are labelled hypotheses. Empty results are explicitly not global negatives. EM-237. |
| ER-13 — Recovery | Failed/ambiguous writes require reload, not automatic retries. Payload-bound request IDs and append-only history support safe diagnosis. Old Qwen model failures remain unmodified; no repair is counted as model success. EM-233/234. |
| ER-14 — Recoverability | Exact tested runtime/test hashes above, failed source-bound runner and lane-only commit/remote SHA make scope recoverable. Historical native evidence is not reattached to integrated code; wheel omission and shipping-state fixture mismatch are explicit. EM-236/238. |
| ER-15 — Operator value | Inspecting sources/limits before reusing a pattern may help, but extra review may be overhead. Measure sound-decision time, missed constraints, correction burden, abstention and inappropriate reuse before claiming benefit. EM-237; existing B04-03, not a new required feature. |

Owner-review queue: EM-233/234/235/236/238 refine existing task/decision boundaries; EM-237 retains an unperformed value study. New runtime inventory truthfulness (EM-235) is technical metadata only: running, installed, loaded and quality-approved are distinct.

## Next action / unpushed state / merge state

At receipt creation all functional work and this record are local; final session handoff supplies the subsequently committed/pushed SHA and confirms a clean worktree. No configured non-sample Git hooks were found in the inspected local hook directory or hook-path settings; normal `git commit` still invokes any configured hooks. No force push, reset, merge, PR change, release, deployment or upstream research execution.

Integrator next: reconcile this branch and later upstream documentation additively, fix the explicit nested-package declaration, wire only current-authority/eligible-source adapters, merge register fragments, resolve the shipping-state fixture truthfully, then run `python scripts/acceptance.py --mode native --base <integration-start>` and inspect the resulting report. B02 actual-model/expert/human and B04 professional/value/security gates remain separate and open.
