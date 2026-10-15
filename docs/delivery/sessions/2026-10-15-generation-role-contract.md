# V0.2 generation-role contract: completed software sprint

## Final validation receipt

The implementation checkpoint below is retained as written. Tested code commit: `8fad4118f07f91ac1884713530bac9479a7b51b7`. Cumulative native run `20261015T210711Z-b1e16249` passed: **951 code tests, 951 installed-kernel tests, 378 native Chromium checks across all eleven suites**, with zero failed/errored/skipped code tests. Compilation, all browser-module syntax checks, eight structural fixtures, offline internal wheel, schemas and all delivery/history checks passed. Inspection returned `valid=true`, `run_status=passed` against unchanged tested source. Source fingerprint: `cd783ba7e7c6d7507cb51fb751e3604f477bc362fbb3777a5675e3237959013e`.

[Committed receipt](../../evidence/generation-role-contract-2026-10-15.json) records counts, per-suite hashes and report SHA-256. Full raw evidence remains locally under `artifacts/acceptance/20261015T210711Z-b1e16249/`; it was inspected before these documentation-only receipt edits. Reconstruct the tested code commit before re-inspecting the report. The final documentation changes do not alter runtime code. Their 60 delivery/changelog/emergence tests passed, alongside generated/history guards and git diff --check.

Fallback public GitHub pages returned HTTP 200: PR #2 is Draft and its 23 visible body/comment blocks were read, including the most recent consolidation handoff. The earlier CI run `36219680306` publicly shows Success. API GraphQL/REST remain Forbidden, and the dynamic checks page could not supply a new run; no remote CI for this scoped branch is claimed. Application and documentation remote heads were re-fetched unchanged before finalisation.

Actual-provider preflight `evals/full_journey.py --provider ollama_staged --transport native` exited **2, blocked**, with zero model calls. No inference permission was inferred from silence. Local Ollama remains unreachable and hosted credentials/model/provider configuration absent. Fresh generation, actual-provider lifecycle/journey, independent expert and human acceptance remain outstanding. B02-09 remains blocked; B02 10/20 and ES01 5/5 internal stay unchanged.

EM-074 is preserved with evidence; EM-020/051/055/060 were revalidated. No further new discovery arose during native verification. All fifteen review passes below still apply. This sprint's implementation and documentation receipt are committed and pushed together to `fix/v02-generation-contract-20261015`; no unpushed implementation is intended at final handoff. The final response identifies the resulting receipt commit; a commit cannot contain its own hash. No PR comment could be posted through the forbidden API, and no private credential was requested to work around it.

**Next task:** select/authorise a real provider/model through supported server configuration, then run the unchanged four-case generation gate with `endstate.draft.prompts.v2`. If Ollama is deliberately configured, the exact next command is `EIGHTBALL_OLLAMA_MODEL=<selected-installed-model> EIGHTBALL_GRAPH_PROVIDER=ollama_staged .venv/bin/python evals/live_generation.py`; preserve the raw results. Follow with the separately opted-in full native provider journey and cancellation/staleness checks. Independent reviewers must freeze the protocol/held-out cases and provide genuine labels; human source, screen-reader/platform, visual and dense-graph reviews remain required. No merge or deployment is authorised.

---

## Preserved implementation checkpoint

Session: Codex cloud, 15 October 2026. Scope: B02-09 / ES03-01, with DOC-03/04/05 continuity. Branch `fix/v02-generation-contract-20261015`, base `290e310707cf8bef6caf2508c285312b091bd18b` (refreshed PR #2 Git head). The initial working tree was clean; no prior work was replaced. All remote heads were fetched explicitly because the initial fetch refspec covered only main.

## Context and boundaries

Read the consolidated handoff at documentation commit `0ee5834c0745640369f5a538b770c346f234232a`, including START-HERE, NEXT-AGENT-PROMPT, V02-CLOSEOUT, master PRD, roadmap, architecture, decisions, research register, original research entrypoint and developer handoff. Its `progress.json` equals the application ledger. The separate documentation proposal remains unmerged. EM-072/073 and its consolidation changelog entry remain preserved on that branch; new discoveries start at EM-074 to avoid collisions. All 71 application discoveries remain, with append-only review history.

GitHub GraphQL and REST reads returned Forbidden. Remote Git access verified PR #2 head at the base above and PR #3 head at the documentation commit. Current CI/review comments could not be refreshed; retained native evidence is historical (938 code + 938 installed-kernel tests, 378 checks across eleven Chromium suites), not this sprint's validation.

## What changed and why

Recovered `docs/evidence/qwen-baseline-2026-09-27.json` byte-for-byte from the documentation branch (SHA-256 `4db80b5a17816f414cd09f1f27737ca12e3b3cc95f9fb2009854cc5154a82992`). It records actual historical inference, not a new run. The original fixture hash remains `6758c54a9e873bf2f67ced368555b871d9cf890b55b4df33762a035be1deaeb3`.

The graph copied readiness and both success titles into intermediate results; both route readiness actions copied the final verifier. Its readiness was also branch-specific, and its success confirmations cited a prior failure/possibility. Target-quote coverage did not detect those semantic defects. The compiler's `result_bypasses_verification` rejection is correct and unchanged.

`endstate/compilation.py` now explains distinct preparatory results, route-neutral shared readiness, future evidence requirements and the separately appended final verifier. Stage two receives explicit reserved titles. Schema changes are descriptions, not new mandatory fields or relaxed constraints. Compiler version stays `endstate.draft.v1`; prompt version is `endstate.draft.prompts.v2`. `evals/live_generation.py` retains both versions on success and rejection. No retries, repaired output, catalogue fallback, fabricated action or new approval/state authority was added.

Tests replay the three extraction responses and rejected graph through controlled transports, preserve exact raw JSON and live state, and cover readiness/each success title with case/whitespace variants. These are regressions, not new inference or semantic acceptance.

## Actual checks at this implementation checkpoint

- Baseline `.venv/bin/python -m pytest -q`: 938 passed, one upstream Starlette/AnyIO deprecation warning.
- `.venv/bin/python -m pytest tests/test_endstate_compilation.py -q`: 50 passed, same warning. First expansion attempt had three test fixture IndexErrors (one-criterion fixture indexed as two); corrected the synthetic test setup and reran. No application failure was hidden.
- Python 3.12.14; pinned development requirements and setuptools 82.0.1 installed in ignored `.venv`; Node 24.19.0; system Chromium 154.0.8037.57.
- Cumulative native acceptance is the next command below; no result is claimed here. A later receipt must record actual outcome and tested code revision.

No real model called. Ollama loopback returned ConnectError. HF_TOKEN, EIGHTBALL_HF_MODEL, EIGHTBALL_HF_PROVIDER and EIGHTBALL_OLLAMA_MODEL were unset (presence only checked). Provider/model choice and inference permission were requested while independent engineering continued. No weights downloaded, paid requests or secret values requested in chat.

## Emergence Review

What did this sprint reveal that we had not properly seen, specified or understood before we built it? Shared readiness can silently favour one alternative even when graph structure/target coverage appears valid (EM-074, observed_in_build, existing_task B02-09/ES03-01). The prompt correction is implemented; effectiveness on actual generation remains unverified. This is a reusable ENDSTATE drafting concern; 8BALL reviewers must still judge evidence relevance and genuine alternatives. No new screen or research feature is justified.

Every review pass was considered:

| Pass | Finding / disposition |
| --- | --- |
| ER-01 change | Prompt/schema guidance, context and trace/replay only; existing B02-09. |
| ER-02 connections | Branch-specific readiness masqueraded as shared OR state; EM-074 adopted within existing scope. |
| ER-03 disconfirmation | Failure/possibility cannot confirm success; revalidate EM-020/042/045. |
| ER-04 next information | Fresh authorised inference, then independent labels discriminate prompt usefulness; EM-054/055. |
| ER-05 freshness | Historical output and current instructions need separate dated/versioned lineage; EM-051/055. |
| ER-06 consequences | Paraphrased bypass or omitted preparation remains possible; semantic effectiveness unverified. |
| ER-07 options | No new runtime option or research promotion; no_action. |
| ER-08 target | Preserve both suitable chairs and written acceptance, exact human wording; EM-015/018/045. |
| ER-09 reconsideration | Retry when authorised provider/configuration changes meaningfully; no automatic paid retries; EM-031/055. |
| ER-10 blind spots | Four known development cases cannot establish unseen-case reliability; EM-020/054. |
| ER-11 chosen course | No selected course, fact or authority changes; EM-056/057, no_action. |
| ER-12 coverage | All four archived outputs replayed; zero current inference, independent or holdout judgements; EM-058. |
| ER-13 recovery | Preserve raw rejection; no repaired-output success; EM-060/063. |
| ER-14 delivery | Exact evidence bytes and recoverable code required; EM-051/062/071. Reserve remote EM-072/073. |
| ER-15 operator value | Fewer missed dependencies/corrections is an intended, unmeasured benefit; EM-048/061. |

Owner review queue: EM-074 and previously pending findings. Prompt provenance refines EM-051 rather than manufacturing a second discovery. No required scope changes. B02-09 stays blocked; B02 stays 10/20, ES01 stays 5/5 internal. Other required scopes and human reviews remain unchanged.

## Next command and continuity

Run from `/workspace/8ball`:

```sh
EIGHTBALL_BROWSER=/usr/bin/chromium .venv/bin/python scripts/acceptance.py --mode native --base 290e310707cf8bef6caf2508c285312b091bd18b
.venv/bin/python scripts/acceptance.py --inspect artifacts/acceptance/<this-run>/report.json
```

Then record the real result in a validation receipt, regenerate/check delivery/changelog/emergence, commit and push this scoped development branch. This document records the base; its containing commit cannot contain its own SHA. Before the final push, re-fetch application/docs heads and preserve any concurrent updates.

After selected provider/model and explicit inference authorisation, run the unchanged four-case generation gate and `evals/full_journey.py --provider ollama_staged --allow-inference --transport native` (or separately authorised hosted configuration). Test actual-provider cancellation/staleness too. Independent professionals must approve/freeze the protocol and holdout labels; humans must complete source, accessibility/platform, visual and dense-graph reviews. No agent sign-off substitutes for them.

The checkpoint branch was pushed at its base to reserve the scope. Implementation publication and cumulative validation are pending at this record; the final receipt will identify the tested code commit and publication result. No main merge, draft-to-ready conversion, release, deployment, new industry application or deferred research implementation.
