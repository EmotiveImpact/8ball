# Session: staged drafting, 23 September 2026

Environment: ChatGPT. Work items: B02-09 and ES03-01. Product remains 8BALL for fixers, powered by ENDSTATE.

## Baseline and checkpoint

Started from remote `af97506c37dbf14ded6208b36277dd3b87a11784`, tree `a3de7517606f19afa07e061c09939663a0b514c7`, recovered through its source-package artifact. The downloaded source reproduced that tree. The local workspace has a synthetic recovery baseline commit; that local commit is not represented as a remote GitHub commit. No other worktree was reset or overwritten.

Pushed code commit **`3a33866f375be355658d8e5d82addb25bcc7eed9`**, exact tree **`1d513b7addb9bd5fd89b106dbb9d447d103e2f3f`**, on `feat/situation-intelligence-v2`, draft PR #2. Remote and locally tested source trees match. The following evidence/documentation checkpoint does not change that application code.

## Actual implementation

Added `endstate/compilation.py`: provider-independent frame/route contracts, deterministic namespaced IDs and declared wiring, complete model-supplied action objects and final verification, duplicate/reference/privilege checks, and a per-node origin map. A two-call provider boundary records both successful and failed raw JSON stages. No model runtime, database or 8BALL dependency is added to ENDSTATE.

Integrated the explicitly experimental `ollama_staged` option through `eightball/v2/intelligence.py`, `api.py` and the graph-proposal form. Existing catalogue default, legacy model path, authority checks and original failed-output regression remain. No synthetic verifier or template substitution repairs the model's response. All proposed actions require human approval and use conservative risk/reversibility defaults pending review.

Added `tests/test_endstate_compilation.py` and a fictional fixture. Updated the real-model evaluation to select the staged provider while retaining all four original cases and existing gates. Added authority/outcome assertions rather than weakening acceptance.

## Verified software

Baseline: 269 pytest tests. New total: **306 passed**, including **37 new compiler tests**. Python compilation, JavaScript syntax and delivery-document validation passed. The local V0.2 browser harness passed 51 checks using its explicit ASGI bridge; this is not a native browser networking claim.

Native application workflow **35911570084** succeeded. Retrieved artifact **10773052381**, SHA-256 `813b149abef9497a90ac100f3d82b6a7dc5efafa7ef3fa2baf51423b4457784c`, records **51 V0.2 plus 27 legacy native Chromium checks**. Actual HTTP, SQLite, session reload and downloaded exports were used. The browser journeys exercise rules/catalogue proposals, not live model quality.

## Actual Qwen result: gate still failed

Real model workflow **35911570117**, job **107352420478**, ran Ollama **0.34.3** and `qwen3.5:4b`, digest `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd`, on a temporary GitHub runner. No model or credential was installed on the user's computer. JEV was not called.

The same three extraction cases returned valid structures (3, 3 and 0 proposals). The supplier graph reached the second stage and then failed compilation: an intermediate result repeated readiness/final-goal conditions. Local replay of the retrieved raw response reproduced that exact validation failure. Manual inspection also found that the model treated the original supplier failure as a success criterion, biased readiness towards on-site spares despite a hire alternative, invented existing-condition IDs, and mislabelled some external-response actions.

All four live case states remained unchanged. The actual run failed; no checkbox is earned by the passing code suite. The raw artifact **10772839284**, SHA-256 `0bcfe28a223b38c4da42941917c49eef5b2eab181fc904a0189d895ebd1afc35`, is preserved losslessly at `docs/evidence/staged-qwen-attempt1.json.xz`. Reproducible digest and inspection notes are in `docs/evidence/staged-compilation-verification.json`.

## Status and remaining work

B02-09 remains **blocked**, now with both the original and new failed evidence. ES03-01 remains **partial**: shared compilation is implemented, but source interpretation and semantic quality are not complete. B02-11 independent quality evaluation and B02-12 full real-model native journey remain unchecked. ENDSTATE core ES01-05 remains partial; no package gate was silently closed. Counts remain 9/18 for 8BALL V0.2 and 4/5 for ENDSTATE V0.1.

A detached two-success-criteria experiment also exposed redundant candidate combinations in the bounded planner: it can list a route doing both alternative preparations as well as the two lean alternatives. This does not alter evidence or prove incorrect final state, but it reinforces the documented non-optimality boundary. The existing kernel and frozen results were not changed during this task. Record a dedicated dominance/branch-consistency improvement before claiming minimal routes.

Next implementation: validate stage-one frame references before paying for route expansion; distinguish the target from evidence describing the problem; constrain model reference fields to supplied IDs; compare a stronger provider where authorised against the unchanged fixture gate and independent semantic cases. Do not optimise only for this single known example or invent missing semantic content. The other unblocked task is ES01-05's typed result/package compatibility acceptance.

Reproduce software checks with `python -m pytest -q`, `python scripts/delivery.py --check`, Python compilation and the two native browser scripts. Reproduce model evaluation only after explicitly installing the runtime/weights: `EIGHTBALL_GRAPH_PROVIDER=ollama_staged python evals/live_generation.py`. This invokes actual local inference; a code-contract mock is not a substitute.

## Delivery boundary

The ledger, generated checklist, architecture and this handoff are committed together after the tested code checkpoint. The resulting documentation commit is recorded in the PR comment, not fabricated inside its own content. No source change is being withheld from Codex. PR #2 stays draft and unmerged. No main merge, deployment, real-client-data use or public ENDSTATE SDK release is authorised or claimed.
