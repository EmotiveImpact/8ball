# Domain-packs lane handoff — 25 October 2026

## Scope and recoverable source

8BALL is the fixer product; ENDSTATE remains its reusable read-only engine. This is
an internal **source-only engineering preview**, not complete roadmap/product acceptance.

- Assigned branch: `devin/1792969169-roadmap-domain-packs`.
- Actual required starting/partition commit: `56c9b79428a612dff11e2fae0219640d156032ff`.
- Parent implementation baseline: `baca8ad9efa531e5f172058845852963d7d5234a`.
- Implemented/tested runtime and first receipt commit:
  `aa54fde9cb5ee43972399f1c2752d80bd9378c3c`, pushed to the assigned branch and
  independently matched with `git ls-remote --heads origin` after push. Subsequent
  handoff-only edits record that observed shipping state; no runtime/test bytes change.
- No merge/PR/release/deployment, source archive execution, actual inference, model download,
  real-client record or external send. Python 3.12.13 / Node 24.19.0; fictional data only.
- This receipt is committed with its code. The exact containing commit is returned on push;
  `git log -1 --format=%H -- docs/delivery/lane-reports/domain-packs.md` recovers it.
- Canonical trackers/shared files are frozen by ROADMAP-LANES; fragments below are proposals,
  not an alternate task-status ledger. Original task statuses/gates were not edited.
- Later agency `2b1b465...` documentation/evidence is for additive parent reconciliation;
  neither that report nor parent baseline native evidence proves these new/integrated bytes.

## Delivered behavior and bounded task evidence

| Task | Demonstrated engineering | Unfinished boundary |
| --- | --- | --- |
| ES04-01 | Strict bounded JSON packs supply native graph/actions/policies, vocabulary, mappings, confirmation metadata, inert prompts and integration declarations; exact all-section content pins and reject tests. | Host prompt/connector registration, real domain validation and integrated distribution are not implied. |
| ES04-02 | Exact existing supplier graph/open questions exported into fictional fixer pack and asserted equal; product still owns all actual playbooks and routes. Core imports no 8BALL and existing source/wire/audit regressions pass. | No shared app/playbook rewiring or intelligence adapter registration; integration owns any adoption. |
| ES04-03 | Neutral/sales/support/fixer all call the same native calculate; sales opt-out and support reviewed-policy/observed-authority negatives preserve separate permission/evidence semantics. | No second application, live sends, actual-model/professional quality, industry launch approval or production assurance. |
| ES04-04 | In-process consumer contract pins version/content/scope/revision; mandatory current grants and fresh bound snapshots. HTTP/MCP/SDK choices and future auth/version/error boundaries documented. | No public HTTP/MCP or published SDK. Real transactional current-authority adapter remains host-owned. |
| ES10-01 | Source-isolated Python consumer, conservative migration report, no automatic live changes; limits/owner/licence/support responsibilities documented. | Internal wheel manifest omits subpackage; actual installed regression fails. Distribution/licence/support promises remain gated. |
| ES10-02 | Recoverable test/code hashes and distinct reuse/quality/support boundaries; independent approval explicitly **not granted/recorded**. | No independent release approval, compatibility/SLO/support commitment or broad ES10 acceptance. |

## Integration contract (no router or UI mount)

1. Add `endstate.domain_packs` to the integration-owned root setuptools package list (or
   reviewed equivalent discovery). The current manifest contains only `endstate` and the
   built wheel omits the new directory. Rerun `scripts/build_endstate.py --regressions`;
   source-isolated tests are not a substitute. No dependency or database migration is needed.
2. Product-owned adapters may explicitly export reviewed pack inputs; preserve the existing
   supplier/playbook selection, prompt/source contracts, case routes and alpha audit lineage.
   There is no automatic fixture/product registration or executable plugin loading.
3. If adopting `PackConsumer`, the authenticated server constructs `Principal(subject)`;
   never accept it as a caller credential. Supply `authorise(principal, scope, 'plan_read')`
   querying CURRENT tenant/matter/snapshot authority, exactly boolean True, plus
   `read_snapshot(scope) -> BoundSnapshot(scope, snapshot)` from fresh scoped reads.
   Keep trusted grant state independent of request object aliases. Unknown/local-bearer
   subjects and cross-scope requests must deny before reads; no adapter means no bypass.
4. Consumer pins `endstate.domain-consumer.v1`, `endstate.domain-pack.v1`, pack ID/version/hash,
   expected revision and aware planning clock. It accepts only matching graph/resources/
   policies; host-owned `Constraint.confirmed` may differ without changing policy content.
   It checks current grants around calculation/final read and rejects stale/misbound results.
5. This read-only seam has no writes, async work, provider, persistent cache or retry. Host
   transactions must still recheck current grants/policy/review/revision for writes, source
   processing, download, publish and external sends. No preview is a commit ticket; no host
   cancellation/restart/paid-call guarantee can be inferred. Revocation cannot recall a
   returned response. The host should map errors without existence/validation-input leaks.
6. `compare_packs` lists sections requiring explicit review; same-version content mutation,
   downgrade, foreign identity and unsupported contracts fail. Never migrate snapshots,
   selected courses, evidence or approval state automatically. A host must retain old pins
   and use existing reviewed revision-bound commands/invalidation rules.
7. Merge this lane's EM-213..215 and changelog fragments by unique ID into canonical JSON,
   preserve all prior entries/gates and later agency evidence, then regenerate/check centrally.
   Newer canonical truthful shipping-state entries and Studio's hardcoded local-state test
   need integration reconciliation; do NOT change delivery state merely to make tests green.
8. No HTTP registration, worker loop, UI navigation or shared API permission mapping is
   requested. Do not broaden the manual token to agency access. Re-run combined native,
   installed-package and cross-lane negatives after approved host/manifests wiring.

## Exact verification and retained failures

All commands ran from repository root with local fictional/disposable data. Correct prefix:
`PATH="/home/ubuntu/repos/8ball/.venv/bin:/home/ubuntu/.nvm/versions/node/v24.19.0/bin:$PATH"`.
No configured linter/type-check command exists in the inspected project manifests; Python
compilation, strict runtime schema/negative tests, standalone import tests and JS syntax
were run. No JavaScript was changed. No active Git hooks were present (sample hooks only).

| Check | Actual result |
| --- | --- |
| `python -m pytest -q tests/test_domain_packs.py tests/test_endstate_kernel.py` | **95 passed** (59 new + 36 retained), 1.27s. |
| `python -m pytest -q` with corrected PATH | **1415 passed**, one upstream Starlette/AnyIO deprecation warning, 56.34s. |
| `python -m compileall -q eightball endstate scripts evals tests` | Passed. |
| `find web -name '*.js' -print0 ... node --check` | All **18** modules passed. |
| New module AST import guard and isolated source-only subprocess | Passed; no application/service imports. |
| `python scripts/build_endstate.py --output artifacts/domain-packs-package` | Existing internal-wheel smoke passed, roundtrip exact, no forbidden imports/network. **New subpackage absent.** |
| `python scripts/build_endstate.py --output artifacts/domain-packs-package-regressions --regressions` | **FAILED** one collection error: `ModuleNotFoundError: No module named 'endstate.domain_packs'`. Manifest is frozen and integration-owned. |
| `EIGHTBALL_BROWSER_BRIDGE=0 python tests/browser_smoke.py` | Native real Chromium/loopback HTTP/SQLite; **27** checks passed. |
| `EIGHTBALL_BROWSER_BRIDGE=0 python tests/browser_v2.py` | Native real Chromium/loopback HTTP/SQLite; **54** checks passed. |
| Native development / graph / sources / insights / grounding / plan_review / courses / accessibility | **22 / 42 / 39 / 40 / 26 / 35 / 31 / 36** checks passed. |
| Native Studio | **FAILED** at unchanged `tests/browser_studio.py:149`, `AssertionError: current build and limits visible`. No completed report/pass claimed. |
| Existing canonical delivery/changelog/emergence `--check` | Passed (71 tasks, 58 historical changelog entries, 113 historical discoveries); **not** a claim that these new fragments were integrated. No canonical writes. |
| Lane fragment validators / hypothetical additive merge history checks | Passed using existing schema validators and copied temporary evidence inputs; EM-213..215 are unique and all original entries/prompts are preserved. Canonical history is untouched. |

Ten of eleven original suites completed, totaling **352** native checks, not complete native
acceptance. Studio requires `'local unreleased'` in the newest changelog entry, but the
frozen partition entry is `pushed_unreleased`; the same first-entry/test bytes are present
at the starting commit, and the lane touches no browser/app/changelog runtime. No browser
bridge, altered CSP, fake inference, alternate fixture or state relabeling was used.
Native artifact transport fields identify loopback HTTP. The unchanged complete acceptance
runner was not rerun: known installed-wheel and Studio failures mean no integrated/native
acceptance claim is available; parent must perform exact integrated source-bound acceptance.

Retained setup/early failures and actual recovery:

- Raw Python3.12 lacked Pydantic; created `.venv` and installed the documented dev requirements
  plus setuptools 82.0.1. The failed raw-interpreter import is not a kernel defect.
- Initial guessed `tests/test_endstate_package.py` path did not exist (pytest code 4); listed
  actual tests and ran the real retained kernel suite (36 pass), then the new focused suite.
- Initial focused run: **7 failed, 88 passed**. Tests guessed nonexistent native route fields
  `guard_gaps`/`approvals_required`, used forbidden dotted Identifier `os.system`, assigned a
  raw-dict `model_construct` test object through assignment validation, and shared the same
  mutable test scope with trusted fixture state. Corrected tests use native `evidence_gaps`/
  `approvals`, opaque adapter keys, intentionally constructed native child models and detached
  trusted fixture scope. Runtime grant/policy checks were not weakened; the corrected 95 pass.
- Initial full source run without Node on PATH: **96 failed, 1319 passed**, 58.11s; first exact
  failure `AssertionError: Node is required for graph module validation`; related subprocesses
  reported Node not found. Corrected documented Node24/.venv prefix gives 1415 pass.
- Chromium was not installed; explicitly installed Playwright Chromium (no model weights).
  Native scripts then ran without bridge mode. No browser-policy override was used.
- Attempt to read hooks via `git config` was rejected by tool policy. No Git configuration
  changed; inspected the directory/config as files and ran the ordinary commit path.
- Studio and installed-wheel failures remain unmodified and are integration follow-ups,
  not silently marked passed. Their exact error excerpts appear above and VM logs below.
- The first temporary merged-fragment validation used symlinks to repository evidence.
  The validator correctly rejected paths resolving outside that temporary root (`Missing
  changelog evidence: endstate/domain_packs/contracts.py`). Repeated with copied evidence
  bytes inside the temporary validation root; schema/additive-history checks passed without
  modifying the validator or any canonical file.

## Limitations, unpushed state and next action

No production isolation, auth launch, async restart fencing, paid inference, domain-expert
quality, legal suitability, human usability/accessibility sign-off, customer pilot, real
source vault/connector, public distribution, licence grant, support/SLO or independent
ENDSTATE release approval is demonstrated. No top-level LICENSE/LICENCE file was present;
this lane chooses none. Independent/human decisions stay outside engineering evidence.

Functional changes and lane-local records were committed and pushed only to the assigned
branch; remote equality was verified for `aa54fde9cb5ee43972399f1c2752d80bd9378c3c`.
No shared/canonical path is edited. Final handoff-only remote equality/commit is returned
after its push; that response, rather than a self-referential in-file hash, records the final head. Ignored
VM artifacts are not committed product data. Next action is integrator inclusion of the
subpackage + truthful changelog/Studio reconciliation + adapter review and combined exact
source-bound acceptance, preserving all unfinished gates and later upstream evidence.

## Emergence Review

**What did this sprint reveal that we had not properly seen, specified or understood before
we built it?** Reusable declarations need a full content pin but still do not provide
current authority; live reviewed policy state must remain separate from hypothetical
catalogues; and passing source consumers does not prove packaging or release readiness.
These are EM-213..215, existing-task/decision-record findings with owner review pending.
Reserved EM-216..232 remain unused reservations, not fabricated discoveries. No new required
scope or human acceptance is created. UX implication: no new screens; surface precise host
review/integration boundaries instead of proliferating implied permissions.

### ER-01: What did we discover that was not explicit before, and what exact evidence made it visible?

EM-213: all-section hashes do not confer current authority. EM-214: reusable policies cannot pre-confirm a case; manual review and observed authority are separate. EM-215: the fixed package manifest omits a valid source subpackage. Focused tests and the actual failed installed-wheel run make these concrete.

### ER-02: What could disprove the finding, and what conflicting or missing evidence have we considered?

A host with genuinely transactional grant-scoped reads/writes may supply stronger guarantees; none was integrated here. An amended manifest plus passing installed-wheel regressions would remove the packaging limitation. Existing source-only tests and old wheel successes cannot disprove the observed omission or grant production acceptance.

### ER-03: Which declared dependencies, actors, decisions or sources connect apparently separate candidate routes?

The same engine/native graph contract links all fictional candidate routes. Sales routes share the explicit opt-out guard; support routes share the remedy-authority policy. Fixer remains the product-owned supplier starter. No actor/entity merge, cross-client identity or new real-client relation was inferred.

### ER-04: Which verification question or review could most change our available options?

For integration the highest-value check is actual installed-wheel reuse after the explicit manifest addition, plus tenant/matter/object authorization under the real host transaction. In the fixtures, reviewed opt-out and authority observations materially change route availability without authorizing a send.

### ER-05: Are we still working towards the client’s explicit target and success criteria?

Yes: this is the assigned existing roadmap slice toward a fixer-first 8BALL with reusable ENDSTATE. No replacement app, new sales/support product, research runtime adoption or assumed client target was introduced. Broad task/product gates remain open.

### ER-06: What may be stale, what could follow from our actions, and what event should make us reconsider?

Pack content, case revision and current grants can become stale independently. Any pin, catalogue, policy, evidence or grant change requires reconsideration; the service rejects detected stale/revoked reads and does not automatically switch courses or publish. Revocation after return cannot recall information.

### ER-07: Which findings belong in 8BALL, ENDSTATE, an existing task, or a retained future candidate?

Schemas, pins and read-only calculation belong in ENDSTATE under ES04/ES10; actual fixer vocabulary/playbooks, authenticated records and case transactions remain 8BALL-owned. EM-213..215 are existing-task/decision-record findings, not automatic scope or independently accepted requirements.

### ER-08: What are we not implementing, why, and where can the owner review or reopen that choice?

No HTTP/MCP surface, external connector, public SDK, live migration, durable worker or production auth is implemented because this data-only lane lacks shared wiring/transaction ownership and explicit launch approval. DOMAIN-PACKS.md and this receipt record manifest/auth/ownership integration gates for owner review.

### ER-09: What actually passed, what failed, and which claimed capabilities still need independent or native verification?

95 focused and 1415 full source tests, compilation/18 JS checks and ten native suites passed. Studio failed its unchanged frozen newest-changelog local-unreleased predicate. Actual installed-wheel regressions failed collection because the preview is omitted. These are not native acceptance, actual inference, expert/legal quality or independent release approval.

### ER-10: What might we still have missed, and how can the operator or owner record their own hypothesis?

A real domain may need decision-dependent templates, richer object-field mappings, prompt output-contract binding, signed publisher provenance, platform coverage or professional review. These are limits/hypotheses, not an invented backlog. The owner can append a reasoned decision to these immutable findings and reopen distribution choices.

### ER-11: What course has an authorised human selected, and what exactly would require reconsideration rather than an automatic switch?

No human selected a case course and no independent human release decision was supplied. The owner authorized routine engineering only. A new version, fresh ranking or fixture pass never authorizes a switch, external action or release.

### ER-12: Which available inputs were not processed, what limits bound this conclusion, and what could exist outside the current catalogue?

Only fictional catalogues and explicitly injected detached snapshots were processed. Real clients, live providers, external source archives, independent expert sheets, other operating systems and production grants/transactions were not processed. Loader limits are 262144 bytes, depth 32 and native object bounds; search limits remain the existing kernel limits.

### ER-13: When analysis fails, what safe recovery is available, who contributed the correction, and is the original failure still recorded?

Initial focused failures were test-contract/fixture mistakes (native route keys, opaque key syntax, constructed model test and shared mutable test scope). Corrected tests pass without weakening runtime grants. Initial full failures were Node missing from PATH and passed with documented Node24/.venv prefixes. Studio and installed-wheel failures remain unchanged and visible for integration; no retry of a provider, hidden source substitution or fabricated correction occurred.

### ER-14: Can the exact implementation and evidence for every delivery claim be recovered, or must that claim remain reported-only?

The receipt embeds code/fixture/test/document SHA256s, exact base, branch, commands and native report hashes. The final pushed commit identifies all committed bytes (self-hash is not embedded). VM artifact logs are not a published acceptance receipt; committed failure excerpts preserve diagnoses. Parent baseline evidence is not attributed to integrated code.

### ER-15: Does this improve the operator’s next decision or merely increase reviews, alerts and screens? How would we measure the difference?

A single explicit pack pin and unchanged kernel reduce hidden forks and unreviewed template drift without adding screens. A future host should measure time to review a changed pack and permission-failure clarity; no operator study or performance/SLO benefit was measured here.

## Implemented source manifest (SHA-256)

These unchanged runtime/fixture/test bytes were used for the recorded tests; delivery
records do not claim to self-hash. The final commit contains all source and this receipt.

| Path | SHA-256 |
| --- | --- |
| `docs/endstate/DOMAIN-PACKS.md` | `651469ce141aa534336b4099720751e8575bf00d6403b528b3951c732ce201e7` |
| `endstate/domain_packs/__init__.py` | `c4ec0211b3a75f062c11884825c2aa44fc2f00a4191bfe7abc6ee7475cb6ab76` |
| `endstate/domain_packs/consumer.py` | `949483547e9a97b1f1106214137d80929c53b84a0626ed59ba99599b2c919446` |
| `endstate/domain_packs/contracts.py` | `25e9404206403fe418f4d1646626854b9520b77d6d18541015ca8fc068d7fcf1` |
| `endstate/domain_packs/loader.py` | `0425929f00731ba32d6681d4562df97a0f590b6c233cd0e6fdf1bbbfd353e661` |
| `tests/fixtures/domain_packs/fixer.json` | `2c7ebd5301245917260d08edaede2727e96bd4b039fc8e1d3b08adb738edc471` |
| `tests/fixtures/domain_packs/neutral.json` | `9992694194e75326956913e4558ee1a6d0f93a29f506ac2ea6cf538b72314c49` |
| `tests/fixtures/domain_packs/sales.json` | `f6abf2481c0fadea4e654fec29e92f5fd2cec78b1a65692cf8432968990094e0` |
| `tests/fixtures/domain_packs/support.json` | `49924b6f9d4b2148d7ed28beaa6f392e9eaf76b25f3acac55b4b9a4394f66008` |
| `tests/test_domain_packs.py` | `a4f9a28346d346ed2a68eba2810459911da0f994a8121bc9bdf0f9341908bf55` |

## Local evidence inventory (not a passed consolidated acceptance report)

These are ignored VM artifact paths; hashes identify the actual local outputs, not an
external attestation or published artifact store. Committed result/error excerpts above
remain readable without those VM files.

| VM artifact | SHA-256 |
| --- | --- |
| `artifacts/domain-packs-full-pytest-corrected.log` | `1aaee711bf6126c3a7c9bd1fe62cbbdadb0b47c0b37c9e527d2c33c0ffe7c055` |
| `artifacts/domain-packs-full-pytest.log` | `9e30d83cd2e6b62c3d099cdd9309da60a1ab20c33f1fb2888ea3849f0da6e582` |
| `artifacts/domain-packs-native-smoke/browser-report.json` | `c553e60bb97ef58196ee5bee1f4fde22203273a6f5bade21c2d298c2faa549c6` |
| `artifacts/domain-packs-native-v2/browser-v2-report.json` | `369f8fed6e2f6d700d5fc0b785dbf623480eaf6003cb1c04b998a2807a56742a` |
| `artifacts/domain-packs-other-native/accessibility/accessibility-browser-report.json` | `1694bba70004e2b415b4a645d054f81605243be6dfce93d642b3fa47a1013e1d` |
| `artifacts/domain-packs-other-native/courses/browser-courses-report.json` | `3dac79f1093e5145895cff92481ea8ce62a0b1d530544fca15c319c226663226` |
| `artifacts/domain-packs-other-native/development/development-browser-report.json` | `6e40ca17878fdcbd8b2fd2b1ab5754ee92840a85a6a242cd93198b119d4c34b5` |
| `artifacts/domain-packs-other-native/graph/browser-graph-report.json` | `c0f21b9d6f57e53711802c0eeedae5647da1b4a0195eef504a797f16ce41f39c` |
| `artifacts/domain-packs-other-native/grounding/browser-grounding-report.json` | `4c0acde1ff3c693ac7714a556d7292a02bd4b8363b5c48091ee8ca5640153c35` |
| `artifacts/domain-packs-other-native/insights/insights-browser-report.json` | `05a47f8e44b3e856cc19ad85bc4f2154835e5c6fed34788232f11969f304a952` |
| `artifacts/domain-packs-other-native/plan_review/browser-plan-review-report.json` | `246a4c540eab74e1821aaba225917f8d799d7a021a1b75c0b0238a49a165ee27` |
| `artifacts/domain-packs-other-native/sources/source-browser-report.json` | `4abf02bc619f78c83f5133f848ceb2ef4cdb5b7810dbf8d8e9b8c93dcc93df27` |
| `artifacts/domain-packs-other-native/studio.log` | `7a1a2b639720566acef8842af2c83e9f8c7e15493fbd63ebbaef198da5b7cc9a` |
| `artifacts/domain-packs-package/package-verification.json` | `dd1aca1a57c87fffe402c66480ece36abf47f15c76dc179339f2441f3c66e991` |
| `artifacts/domain-packs-package-regressions.log` | `67ba53db2c7766f583733b91332866370b3a4e91832c442fad74261aa61e50b8` |
