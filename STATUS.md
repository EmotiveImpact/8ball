# 8BALL + ENDSTATE: current delivery checkpoint

23 September 2026. **8BALL is the fixer product. ENDSTATE is its shared calculation and proposal-compilation engine.** This remains a local developer preview, not a production agency service or public SDK.

## Current code and verification

Code commit **`3a33866f375be355658d8e5d82addb25bcc7eed9`**, tree **`1d513b7addb9bd5fd89b106dbb9d447d103e2f3f`**, on `feat/situation-intelligence-v2`. **306 pytest tests passed**, including 37 new compiler checks. Native GitHub workflow **35911570084** passed, with retrieved reports for **51 V0.2 and 27 legacy native Chromium checks**. Original wire/audit compatibility remains tested. See [the session evidence](docs/delivery/sessions/2026-09-23-staged-drafting.md).

ENDSTATE already powers 8BALL's planning through compatibility adapters. The new shared staged compiler separately asks a provider for outcome/verification objects and complete alternative routes, then assigns IDs and declared wiring. Every semantic action has a pointer to its model draft. No missing action is invented. The explicit `ollama_staged` graph-proposal option is available; catalogue remains the default and the old model path is preserved.

## Actual model blocker remains

Real Qwen workflow **35911570117 failed**. Three extraction fixtures produced valid structures, but the staged supplier graph was rejected for repeated readiness/goal results. It also contained invented existing-condition references and confused the original problem with the target outcome. All live case states remained unchanged. The full response and manual inspection are retained in [the verification record](docs/evidence/staged-compilation-verification.json). This is not production model-quality approval.

The initial GLiClass configuration was also below its acceptance standard. No live JEV request was made without credentials. The new architecture is implemented and tested; arbitrary-situation intelligence is not declared solved.

## Shared roadmap and next work

The sole editable status source is `docs/delivery/progress.json`; regenerate [PROGRESS.md](docs/delivery/PROGRESS.md) with `python scripts/delivery.py --write`. **8BALL V0.2: 9/18 required subparts verified. ENDSTATE V0.1: 4/5.** Counts are not effort or readiness percentages. B02-09 remains blocked and ES03-01 remains partial, now with the new code and actual model evidence.

Next: target/reference-aware frame validation and evaluated provider improvements, without weakening the preserved gate. Complete ES01-05's embedded result/package contract review separately. The guided editor, robust source handling, accurate model status/cancellation, accessibility, independent quality evaluation and full real-model native journey are still outstanding V0.2 work.

PR #2 remains draft and unmerged; main has not been changed. Secure agency identities, expert/client permissions, confidential evidence storage, recovery and commercial readiness remain future milestones. Use fictional/test data only. No deployment, autonomous external action or cross-client learning is running.
