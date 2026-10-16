# Hosted API/Qwen and source-only research-copy sprint

16 October 2026. Base `c9fd38438ba52e9320bc55b96132086bfe57ce6a`; branch
`feat/v02-compatible-provider-20261016`. The owner requested copying all researched
repositories and continuing engineering while they arrange a Qwen API endpoint.

## Completed implementation

- Added a server-configured OpenAI-compatible transport with exact model/provider,
  HTTPS API base URL, explicit external permission, strict JSON-schema requests,
  no redirects/retries/fallbacks, bounded responses and managed proxy/CA support.
  OpenRouter requires a pinned allowed provider; exact Alibaba DashScope hosts
  disable thinking for this non-streaming structured-response contract.
- Integrated source extraction, two-stage target-bound graph drafting, questions,
  real persisted jobs, authenticated API and existing review flow. Cancellation,
  stale cases and restart still suppress publication; selecting a provider never
  attests a fact or authorises an action.
- Added Hosted API / Qwen status, provider selection and a key-free setup dialog.
  The browser never accepts a private key. [Beginner guide](../../v2/QWEN-SETUP.md).
- Extended the same frozen-fixture hosted runner and the actual-provider journey.
  No fixture, original PRD, compiler prompt, guard or acceptance threshold changed.
- Preserved 28 exact upstream source checkouts as Git submodules under
  `research/external/`, original licences/notices and explicit model/LFS/nested
  exceptions. [Inventory](../../../research/inventory.json) and Git-only helper
  preserve complete intended source presence. No upstream software was run.
- Pruned external sources before app fingerprint/test traversal while retaining
  metadata and declared/checked-out Gitlink identity. Normal acceptance strips
  all new provider settings. Upstream instructions are reference data.

## Configuration and actual-provider boundary

The saved environment draft suggests Alibaba international
`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`, provider
`alibaba-model-studio`, a blank exact model and user-supplied `EIGHTBALL_API_KEY`
secret scoped to `dashscope-intl.aliyuncs.com`. The save added this destination
and requires user Save/Publish. This does not activate/authenticate the current
task or itself grant spending. Other regions/providers need matching settings/secret
destination. No key value was requested in chat or committed.

Observed runtime has no ready provider secret/model. A manual configuration
preflight exited 2 before any request. Actual model calls in this sprint: **zero**.
The owner subsequently authorised the repository's fictional examples up to
US$5, while expecting the endpoint they supply to be free access. Confirm the
actual service limits after receiving its public URL/exact model and secure key;
no endpoint was supplied or actual call made during this sprint. The owner will review the
product at the end; independent professional/semantic judgement remains separate.

## Verification checkpoint

Focused checks passed: 109 transport cases, 22 real-SQLite/controlled-HTTP lifecycle
cases, 4 CLI/preflight/report cases, 36 acceptance-boundary cases. These overlap
within the full suite and are not an additional claimed total. The existing
hosted/job/acceptance focused combined run passed 251 before the final five
transport additions; do not attach that count to the final cumulative tree.

The native development suite passed 22 browser checks, including seven new API
status/setup/focus/selection/permission checks. Its proposal is a controlled
fictional fixture, never real Qwen output. The archive Git-only verifier and
population repeatability passed for all 28 pins and 128 original notice files.

The cumulative native run tested code commit
`ddfead7fe2e44a01ec202d2196384c5dc2596c5b` and passed **1,104 source tests,
1,104 installed-kernel regressions and 391 native browser checks across all
11 suites**. Python compilation, 17 JavaScript module checks, structural
fixtures, internal package/schema export and continuity guards passed.
Run `20261016T094827Z-13d47ae7` finished at 09:51:56 UTC. Source fingerprint:
`a67ae2482bd858a1d4cf2fa63e0c12624746ce3d9eac1c80f01fc9c9aef438e5`.
Report SHA256:
`6f9ead281050589d6d73d92006dc4e8e2071cce31305a33ff9cb538591ed90a6`.
Inspection was valid/passed before final documentation edits.
[Final receipt](../../evidence/compatible-native-2026-10-16.json) records all
counts, checks and 28 source pins. Raw software artifacts remain local under
ignored `artifacts/acceptance/20261016T094827Z-13d47ae7`; the receipt is not an
artifact upload. Reconstruct the tested code with all source pins populated to
re-inspect it. The previous model failures remain preserved.

The bounded optional ES03-09 controlled transport/software contract is verified.
Original B02 required statuses remain unchanged. GitHub Actions has no push
trigger for this development branch and no PR was opened; no new remote CI
result is claimed. Main remains `d7d36b842464d7ad0e974a59730a682f1739fccf`.
The final receipt/changelog/status commit changes documentation only; the
development branch is pushed without merging or deploying.

## Emergence Review

What did the sprint reveal that we had not properly seen? Source preservation
and application verification need explicit separation, and raw rejection traces
require both model-output attribution and credential/Unicode handling. These
are EM-082/083. Existing EM-019/020/031/051/054/055/072/073/077 gained additive
evidence. No deferred runtime feature was promoted.

| Pass | Finding / disposition |
| --- | --- |
| ER-01 | Owner-authorised source copy and bounded provider implementation; DOC-07 and optional ES03-09. |
| ER-02 | One existing compiler/review/job path serves the new endpoint; no second planner. |
| ER-03 | Clean pinned sparse checkouts may omit source; literal key redaction missed Unicode-escaped echoes in an initial controlled test. Fixed and retained as EM-082/083. |
| ER-04 | Exact endpoint/model and active credentials remain missing. Fictional tests are authorised up to US$5 with free access expected; verify service limits. |
| ER-05 | Pin exact upstream revisions and preserve actual model/prompt/schema identities; aliases are not immutable weights. |
| ER-06 | Research hooks/tests/model payloads must not execute; cancelled remote requests may still complete/be billed. |
| ER-07 | A generic hosted endpoint removes the need to install local weights for this test path; no provider is silently selected. |
| ER-08 | Preserve exact target, genuine alternatives and explicit final verification; no compiler/schema weakening. |
| ER-09 | Strict failure/status and cancellation/revision gates require real-provider follow-up. |
| ER-10 | JSON-schema support, actual quality, provider retention and real cost remain unverified. |
| ER-11 | Provider output proposes; human course selection and action authority remain separate. |
| ER-12 | 28 declared source pins, explicit two model omissions, 51 LFS pointers and two nested references; copied source is not every external dependency. |
| ER-13 | Retain attributed exact bounded assistant failures or explicit omission/hash; never repair measured outputs. |
| ER-14 | Stage/version the source pins and bind cumulative evidence to its exact code commit. |
| ER-15 | Evaluate meaningful alternatives, correction effort, latency/cost and human understanding with independent labels; controlled response success is not operator value. |

Evidence level: controlled tests/source checks and native software checks, with
actual provider/professional/human evidence explicitly absent. Architecture:
optional application-owned transport and external source trust boundary. UX:
one existing Intelligence/review workflow, secure keys on the server. Roadmap:
original V0.2 required gates unchanged; source preservation is a new explicit
documentation deliverable and compatible transport is a bounded optional scope.

## Remaining work and next task

B02 remains 10/20 required verified; ES01 remains 5/5 internal. Activate the owner's
selected free-access Qwen settings, confirm service limits within the authorised
fictional-fixture US$5 ceiling, run unchanged generation
fixtures and actual selected-provider cancellation/stale/interruption/journey,
then independently authored evaluation and genuine human acceptance. Keep the
owner's end review and independent professional review distinct. No main merge,
release, deployment or new industry application is authorised/performed here.
