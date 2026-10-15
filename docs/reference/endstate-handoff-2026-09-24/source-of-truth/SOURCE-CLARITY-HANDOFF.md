# 8BALL Source clarity: ChatGPT / Codex handoff

24 September 2026. Developer checkpoint **0.2.0-alpha.5**. **8BALL is the fixer product; ENDSTATE is its reusable engine.**

## Delivery identity

This build is **local, not pushed, merged, deployed or released**.

- Local checkpoint commit: `f1bb3a81e947ac48a8e2113196b429f18cef57f3`. This commit does not exist on the remote merely because it is named here.
- Exact tracked source tree: `c057d35ff84c1480243208d9674f4e99f7bf74a6`.
- Source archive: `8BALL-Source-Clarity-Source.zip`, 191 tracked files, SHA-256 `0ad0d3fb1a8e5d180391bd21b314f66263c27a570623dccdcc49333835e97b14`.
- Inspected remote base: `824ca6421ff3100e1af596347f2d1247dde8f8dc`, tree `68ff7ac7b212fbdf67f77d051f69d13ed39485be`, `feat/situation-intelligence-v2`, draft PR #2.
- Preceding supplied Emergent Insights source tree: `a6cdfbf32e2b5d7a9803b9de94a3b729d847c1f6`.

The earlier source-write safety block has not been bypassed. Read the current remote and reconcile any newer work before authorised integration. Do not force-push, overwrite newer Codex work, assume this local Git history is the remote branch, or stack cumulative patches.

## Choose one integration route

**Complete source:** extract `8BALL-Source-Clarity-Source.zip`. It includes all prior unpublished work and this sprint. Use the normal run scripts from its `8ball` folder.

**Cumulative patch:** `8BALL-Source-Clarity-From-Remote.patch` applies only to the exact remote-base source tree above. It includes all preceding unpublished checkpoints. First check a clean working tree and run `git apply --check`, then apply on a working branch. Never use a patch check as permission to overwrite unrelated local work.

**Incremental patch:** `8BALL-Source-Clarity-From-Emergent-Insights.patch` applies only to the immediately preceding supplied alpha.4 source tree above. Do not apply it after the cumulative patch or complete source.

A clean copy of the remote-base source was patched and its resulting Git tree matched `c057d35ff84c1480243208d9674f4e99f7bf74a6` exactly. All **746 tests passed again** on that clean copy. Check the supplied hashes before integration.

## Read first

`AGENTS.md`, `docs/PRD.md`, `docs/ROADMAP.md`, `docs/delivery/PROGRESS.md`, `docs/delivery/HANDOFF.md`, `docs/v2/SOURCE-CLARITY.md`, `docs/delivery/sessions/2026-09-24-source-clarity-local.md`.

## New functionality

Source-grounded identity-mention review without actor merging; exact quote/context/hash retention; explicit deadline interpretation from a full date or source-reference date plus calendar days; IANA timezone and DST gap/fold review; read-only route impact preview; explicit atomic deadline application; source/actor/deadline changes flagged for reconsideration; linked interpretation and case histories.

No AI model is called on this screen. A reviewed interpretation is not proof of a source claim. Retraction flags an adopted deadline but does not silently remove it. No implied authority, free-form date parsing, business-day calendars, global alias merging or automatic deadline changes.

## Observed verification

746 code tests passed (74 new). 275 browser checks across eight suites passed using the explicit ASGI bridge with real Chromium, API and SQLite. New source-clarity journey: 26 checks. Python compilation, JavaScript syntax and generated-document/history guards passed.

Native browser navigation was attempted and blocked with `ERR_BLOCKED_BY_ADMINISTRATOR`. The bridge does not establish native networking, session storage, downloads or CSP enforcement. No new live Qwen, Hugging Face or JEV inference was run. Do not weaken browser security controls or substitute a bridge result for native acceptance.

## Integration gate

Run the complete test suite, compilation, syntax and generated-doc guards. Then run all eight native browser suites in an authorised environment:

```sh
python -m pytest -q
python -m compileall -q eightball endstate
node --check web/app.js
for file in web/v2/*.js; do node --check "$file"; done
python scripts/delivery.py --check
python scripts/emergence.py --check
python scripts/changelog.py --check
python -m playwright install chromium
python tests/browser_smoke.py
python tests/browser_v2.py
python tests/browser_development.py
python tests/browser_graph.py
python tests/browser_studio.py
python tests/browser_sources.py
python tests/browser_insights.py
python tests/browser_grounding.py
```

Record actual pushed commit and CI results only after observing them. Source-to-plan intelligence, independent semantic/identity/date evaluation, full native acceptance and production security remain incomplete. No merge or deployment is authorised.

## Shared status and emergence discipline

The task ledger remains `docs/delivery/progress.json`; regenerate its Markdown. B02-10 and B02-14 stay partial; do not turn this manual interpretation workflow into a claim that autonomous resolution is solved. B02-09 remains blocked on real-model acceptance.

The emergence register now retains **43 discoveries**, including EM-038 through EM-043 from this sprint. New work must append every identified discovery, including deferred/declined ideas, with rationale and user-review status. Update the immutable changelog and link its emergence review; use history guards against the actual starting commit. Business-day/end-of-day rules are deliberately retained as a deferred candidate, not guessed.
