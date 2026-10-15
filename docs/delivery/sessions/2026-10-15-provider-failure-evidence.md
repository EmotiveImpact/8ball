# V0.2 provider-failure evidence and review preparation

Session: 15 October 2026. Base `45f8794733df9635d8daf5146a37fb94af9e8e90`; branch `fix/v02-provider-failure-evidence-20261015`. The clean starting checkout contains both earlier generation-contract and graph-keyboard fixes. All remote branches were fetched; application `290e310707cf8bef6caf2508c285312b091bd18b`, documentation `0ee5834c0745640369f5a538b770c346f234232a` and main `08bc26ef397ec960d1b33b099c40888a8229eac0` remain unchanged. No previous source was replaced.

## Work and evidence boundary

Recovered START-HERE, NEXT-AGENT-PROMPT, V02-CLOSEOUT and linked specification/architecture/research/decision context from the separate documentation branch, plus AGENTS, canonical ledger, current handoff, both earlier 15 October sprint records and their receipts. The research freeze, original PRDs and generation fixtures remain intact. No documentation-branch merge is required to read its records.

Current public GitHub checks for `45f8794` state there are no checks for this commit; branch Actions search has no runs. PR #2 remains Draft; the earlier native run `36219680306` shows Success. The scoped push is outside the configured CI branch allowlist. Historical CI and the previous local native receipts do not validate this sprint's changed source. No new remote CI pass is claimed.

The managed runtime has no secret, runtime-variable or outbound-identity bindings. Relevant provider/model environment variables are unset (presence only), no Ollama binary is installed, and loopback Ollama is unreachable. About 33 GiB RAM and 30 GiB free disk are present; no NVIDIA runtime was found. The copied provider configuration is still placeholders. The owner answered that they did not understand the provider question and will review the application at the end. Explained that 8BALL needs its own model connection and asked whether to install the existing free Ollama/Qwen test setup using only fictional repository data. Silence is not model-download or inference permission. This record must be supplemented with any actual subsequent authorization and execution.

Read-only diagnosis identified a concrete loss of failure evidence: Ollama extraction rejected for schema or source-span validation raised a plain ValueError. The async job retained its failure/count, but no rejected proposal/raw model output, so the full-journey report could not preserve it before deleting its disposable database. The structural rejection is correct; its missing evidence is the defect. Implementation is limited to bounded structured extraction-failure trace/persistence through the existing protected proposal path, plus controlled regressions. It must not convert failure into success, publish cancelled/stale results, include arbitrary transport bodies, retry inference or mutate live case state.

Prepared [the review pack](../review/README.md): blank prospective protocol and per-case reviewer forms, exact original twenty-step human journey, and actionable source/identity/date, provider lifecycle, accessibility/platform, owner visual/mobile and dense-case comprehension sheets. All approvals, labels and performed-review values remain unset. The eight public hinted engineering examples are familiarisation material, never a held-out set. Owner review at the end is recorded as the owner's preference; qualified independent review/approved thresholds remain required separately.

## Verification and handoff

Focused controlled regression batch: 207 passed across test_v2_intelligence, test_analysis_jobs, test_acceptance_runner, test_hosted_and_grounding and test_endstate_compilation (one existing upstream deprecation warning). The first expansion had four failing test expectations: audit intentionally gains a failed model_runs record and the demo already has observations. Assertions were corrected to compare unchanged factual/event state with the intended added failed model record, without weakening application validation. Cumulative native acceptance is pending at this implementation checkpoint. A final source-bound receipt must record actual counts/results, tested commit, source fingerprint, artifact/report hashes and inspection. No new native or actual-model pass is claimed here. Review-template checks passed: 20 original steps verbatim, 54 NOT_RUN rows, 38 existing local Markdown targets, matching six-part rubric/version, null approvals/thresholds and unchanged task statuses/acceptance/required values. The frozen generation hash is unchanged. The committed review-pack receipt records exact template hashes. Dependency check passed with no broken requirements. Reusable install_script/start_skill were saved as environment draft cecfgdraft_6ad15542fffc819c8c9fe1442a1d8a7f; requires_publish=true. This does not apply configuration or provide a model; future restoration requires review/save and Publish in environment settings. Complete generated/history checks against the base above before commit/push.

B02 remains 10/20 required verified; ES01 remains 5/5 internal scopes. B02-09/12 remain blocked; B02-10/11/14/15/16/19 remain partial; B02-20 remains implemented. Templates and controlled rejection tests cannot clear actual-model/professional/human gates. No main merge, draft-to-ready conversion, tag, deployment or other industry application is authorized.

## Emergence Review

What did this sprint reveal that we had not properly seen, specified or understood before we built it? A correctly rejected extraction can lose its diagnostic model output between provider validation, persisted analysis jobs and a disposable journey server. Preserving graph failures alone is insufficient. This refines EM-051/055 rather than creating a feature or loosening a gate. The review pack also makes the existing EM-054 distinction actionable: the original human twenty-step journey and the scripted runner's twenty engineering checks are different evidence. No new research candidate or accepted scope is introduced.

| Pass | Finding / disposition |
| --- | --- |
| ER-01 | Exact change is preserving rejected extraction evidence and preparing existing acceptance records. |
| ER-02 | Provider, job, proposal and exported report share one failure-provenance boundary; EM-051/055. |
| ER-03 | Correct rejection and a recorded call count can coexist with lost output; preserve the counterexample. |
| ER-04 | Controlled schema/span failures through persisted jobs discriminate the evidence fix; actual inference remains separate. |
| ER-05 | Bind outputs/receipts to exact source, model/prompt and time; do not attach older CI to changed code. |
| ER-06 | Retention must not leak arbitrary transport/credential errors or publish cancelled/stale results. |
| ER-07 | No new optional screen, provider, domain product or research runtime; no_action. |
| ER-08 | Keep original acceptance, target, frozen cases and six rubric dimensions unchanged. |
| ER-09 | Reconsider if a rejection cannot be reconstructed after the temporary database is removed. |
| ER-10 | Missing authorized model and independent reviewers remain explicit dependencies, not passing tests. |
| ER-11 | No chosen course, action authority, approval or factual state is changed by recording failure. |
| ER-12 | Cover parsed Ollama extraction validation failures; do not claim all transport bytes or universal provider fidelity. |
| ER-13 | Original rejection/raw output survives separately from any later human/model correction; no repaired-output pass. |
| ER-14 | Commit source, recording aids and scoped receipt; full local artifacts are not an external upload. |
| ER-15 | Retained failure evidence should aid diagnosis and reviewer effort; actual operator benefit is unmeasured. |

Next task after software verification: apply an explicit provider choice/authorization if supplied, configure its runtime securely, and run all four unchanged generation fixtures, then actual-provider native integration and cancellation/staleness/interruption checks. Obtain prospective independent protocol/labels and prepare the owner's end review. If permission remains absent, finish the concrete software/review-preparation work and report the precise dependency without inventing inference or human acceptance.
