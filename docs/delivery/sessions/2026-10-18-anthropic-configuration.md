# Anthropic provider choice and secure environment preparation

18 October 2026. Branch `feat/v02-review-evidence-20261018`, base
`12ffdadb2f094e8f31fbd60486b5f775894b32ec`. The owner selected Anthropic for
testing and asked where to put the key and connection settings. This is a
configuration/documentation continuation; application code, tests, dependencies,
original PRDs, frozen fixtures and all acceptance requirements are unchanged.

## Completed work and evidence

- Fetched all remote branches and preserved the clean latest development HEAD.
- Inspected the actual generic transport and the official Anthropic Python SDK
  at `bcd55fe1d3f0f1240765f8cef04295b67337f55a`. The SDK lists the proposed
  `claude-sonnet-4-6`; account availability/pricing remain untested. Native
  Messages and generic completion protocols differ; neither compatibility nor
  the need for a native adapter was proved by SDK source inspection.
- Normal inherited-proxy access to the official compatibility documentation
  was blocked by the inherited proxy with HTTP 403. This does not establish an
  Anthropic-origin response. No policy was bypassed; no model request occurred.
- Saved non-secret draft suggestions for Anthropic base URL/model/provider and
  added `api.anthropic.com` to custom network destinations. Existing install,
  repositories and unrelated configuration remain preserved.
- The existing `EIGHTBALL_API_KEY` slot is labelled Qwen and destination-bound
  to its old host. The configuration service rejected an automatic target edit
  and explicitly prohibited duplicate requirements. No changes from that attempt
  were saved. The successful separate save preserves that secret; the owner must
  edit its allowed destination to `api.anthropic.com` and enter the private key
  in settings, then Save and Publish. The agent never received a secret value.
- [Beginner setup guide](../../v2/ANTHROPIC-SETUP.md) gives exact fields, the
  required secret edit, activation steps and explicit compatibility limits.
- Isolated format/status check with a fictional key, blocked DNS/HTTP, confirmed
  derived compatibility URL and `configured_not_tested`; no credential/model
  success was claimed. Focused existing transport/CLI and continuity results are
  recorded in the final configuration receipt: **142 transport/CLI tests passed
  in 1.30s; 60 continuity tests passed in 1.37s**, with one existing Starlette/AnyIO
  deprecation warning. Independent agent source/document review found no blocking
  issue; it is not independent professional acceptance.

[Configuration receipt](../../evidence/anthropic-setup-2026-10-18.json) records the
actual limits and evidence. No new native run is needed for this configuration/
documentation-only change. The earlier native result remains **historical for
tested code `25ca5e2dce4f28ec33d9b132cccabfa15b23683e`**: 1,267 source tests,
1,267 installed-kernel regressions and 391 checks across eleven native suites.
It is not an Anthropic, independent professional or human acceptance result.
No current remote CI is claimed; no live inference, spending, model download,
runtime adoption, main merge, release or deployment.

## Emergence Review

What did this reveal that we had not properly seen, specified or understood?
A provider change is also a secret-destination change; replacing visible URL
fields cannot rebind a managed key. EM-098 preserves the observed restriction
and necessary operator step. Existing source/identity findings gain evidence.

| Pass | Finding / disposition |
| --- | --- |
| ER-01 | Owner selected Anthropic; keep the existing V0.2 goal and fictional-only US$5 ceiling. |
| ER-02 | Prepare the existing generic transport rather than claiming an unimplemented native adapter. |
| ER-03 | Old secret destination prevents the new service from receiving its key; settings edit is required. |
| ER-04 | Active key, published destination/network variables, actual account/model access and genuine reviews remain missing. |
| ER-05 | Secret label, app variable, allowed hostname, requested model and wire protocol are separate identities. |
| ER-06 | No duplicate secret, bypass, credential copying, automatic paid retry or schema weakening. |
| ER-07 | Native Messages support is an engineering alternative only if actual compatibility demonstrates a need. |
| ER-08 | SDK model listings and configured status do not establish availability, price, strict output or inference. |
| ER-09 | Run unchanged fixtures first; preserve any rejection before deciding a bounded adapter correction. |
| ER-10 | Official compatibility docs were inaccessible; retain that source-evidence limitation. |
| ER-11 | No case state, target, course or action permission changes through configuration. |
| ER-12 | Bounded SDK/config inspection, not service certification or a live-provider benchmark. |
| ER-13 | Preserve the rejected draft mutation and distinguish it from the later successful non-secret save. |
| ER-14 | Commit/push exact setup/handoff records and save continuation at the pushed development HEAD. |
| ER-15 | Give a novice exact settings and one secure key-entry path; minimise setup confusion without inventing successful access. |

Evidence level: observed configuration-service behaviour and controlled format/
software checks. Architecture: preserve server-owned provider settings, credential
destination restrictions and the model-proposal/authority boundary. UX: the old
Qwen label must not imply that its destination automatically changes. Disposition:
existing B02-09/B02-15/ES03-05 refinement, no new required task or research scope.

## Remaining gates and next concrete task

Owner edits the existing key slot's allowed destination to `api.anthropic.com`,
enters the Anthropic key securely, and saves/publishes. Check active runtime
readiness and permitted network destination, confirm service limits, then run the
unchanged generation fixtures using the prepared compatibility route. Retain all
responses/failures before any correction; follow with matching lifecycle/native
journeys and genuinely independent/human reviews. B02 remains 10/20 and ES01 5/5
internally; all original statuses and required acceptance remain unchanged.
