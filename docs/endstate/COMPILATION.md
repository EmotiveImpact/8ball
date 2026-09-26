# ENDSTATE staged outcome compilation

Internal contract: `endstate.draft.v1`. Introduced for B02-09 and ES03-01. This is a review-only compiler, not an autonomous operator or a production-quality model endorsement.

## Why a separate draft contract

The previous single-response Qwen graph named a final verification action that it never supplied. The original invalid response and the original validator remain unchanged. The new path does not patch that response, invent a verification action or substitute a catalogue plan. Instead it asks the provider for smaller, complete semantic objects, then derives technical identifiers and wiring from an explicit restricted contract.

The 8BALL graph-proposal dialog exposes **Local Ollama · staged ENDSTATE draft** as a separate provider. Catalogue remains the default. **Local Ollama · legacy graph draft** retains the earlier implementation and its negative regression tests. No model is downloaded by selecting a form or importing ENDSTATE.

## Stages and authority

1. **Frame.** A provider proposes the readiness condition, all required success criteria, the complete final verification operation, and one to three approaches. A supplied outcome must retain all its parts, including any acceptance requirement. None of those propositions is treated as an accomplished fact.
2. **Routes.** The same provider supplies exactly one route for every declared approach: explicitly ordered steps, each with a complete action and a distinct evidence-verifiable result, followed by a complete operation that establishes the shared readiness condition. No free-form action IDs need to be invented by the model.
3. **Compile.** Pure Python validates the draft, assigns deterministic namespaced IDs, links the declared sequence, joins alternatives at readiness, and attaches the model-supplied final verification operation. That is the only action producing final target conditions. Every compiled action has a JSON pointer back to the exact draft operation supplying its semantic content.
4. **Review.** 8BALL validates the append-only delta against its current case, stores it as a pending proposal and uses the existing atomic accept/edit/reject transaction. Only a later, separate operator observation can establish an evidenced state.

Missing frame fields, missing operations, missing approaches, duplicates and references outside the supplied snapshot fail closed. There is no automatic retry, synthetic verifier or silent fallback. Failed stages preserve their raw JSON in the case-scoped model record, without printing sensitive source contents in API errors. Rejecting all items preserves the live case and revision.

## Engine/application boundary

`endstate.compilation` imports only the shared ENDSTATE contracts, the standard library and Pydantic. It has no dependency on 8BALL, FastAPI, a database, HTTPX or a model runtime. `draft_outcome` accepts an injected `(schema, instructions, context) -> (JSON, model_id)` provider function. Different providers can implement that contract without altering the deterministic planner.

`compile_outcome` can be used independently of model generation. It returns a validated `GraphDelta`, declared external-condition references, a node-origin map and review notices. It cannot return observations, selected decisions or approvals. The exact human outcome is preserved as the objective title. Source interpretation quality and the completeness of proposed success criteria still need human assessment.

8BALL owns selected-source authorisation, the loopback Ollama adapter, proposal storage and review. The new `ollama_staged` provider is graph-only. Existing extraction and judgement providers remain unchanged. Consequently ES03-01 is not automatically complete: all source interpretation, long-source handling and reconciliation interfaces are not yet extracted into the shared layer.

## Restricted scope, not a general planning shortcut

A route's intermediate steps are sequential by contract. Its readiness action requires all intermediate results. All alternative routes establish one readiness condition and share a final verifier. This is suitable for the first controlled drafting tests, not every crisis, parallel operation or nested contingent strategy. More expressive graphs remain available through reviewed 8BALL authoring; richer generation requires its own evaluated extension.

Generated actions start approval-required with conservative high-risk/difficult-to-reverse labels until reviewed. These are cautious defaults, not inferred risk measurements. External dependency and known/unknown wait fields come from the draft and must be reviewed too. Operator authority, budget, quantity, deadlines, omitted prerequisites and causal plausibility are not established by schema validity.

The compiler can reject exact duplicate routes under different names. It cannot prove that differently worded approaches are meaningfully different or effective. A pair of structurally valid routes is not evidence of business success.

## Regression and live-model evidence

`tests/test_endstate_compilation.py` and its fixed fictional fixture verify origin completeness, explicit final verification, deterministic and detached results, preserved alternatives, external references, strict errors, unchanged case state, reviewer disposition, completion/effect separation and failed-stage trace storage. These are controlled contract tests, not real model inference.

The separate `evals/live_generation.py` job preserves the same four original fictional inputs. Extraction still uses the existing local-model path; graph generation uses the explicit `EIGHTBALL_GRAPH_PROVIDER=ollama_staged` option. The gate still requires all four valid responses, at least two supplier routes and unchanged live state, and additionally checks approval and exact human-outcome preservation. No fixture was removed to make the job pass.

See `docs/evidence/staged-compilation-verification.json` and `docs/delivery/sessions/2026-09-23-staged-drafting.md` for the observed code revision, tests, actual model result and limitations. A successful small-fixture job does not complete the independent-quality or full native real-model acceptance milestones.
