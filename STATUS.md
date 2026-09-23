# 8BALL + ENDSTATE: current delivery checkpoint

23 September 2026. **8BALL remains the fixer product. Its shared calculation kernel now lives in `endstate/`, called through compatibility adapters by 8BALL.** This is an embedded developer preview, not a standalone SDK or production service.

## Current code and evidence

Code commit **`0c4104a675600c20a290766909bca60088766b35`**, tree **`6259e4aa41bc948f560fd54e26025071a74c5867`**, on `feat/situation-intelligence-v2`. Native GitHub Actions run **35904869115** passed. Local results: **269 pytest tests**, including 36 extraction/compatibility checks. The downloaded native artifact records **51 V0.2 + 27 legacy browser checks**, real HTTP, SQLite, storage/reload and exports. See [ENDSTATE validation](docs/endstate/VALIDATION.md).

The separated core has no 8BALL, database, web-server or model-runtime import dependency. Neutral, sales and support fixtures use the same kernel. These are reuse tests, not three launched products. Existing wire schemas, plans, original database records and audit hashes are preserved by regression checks.

## Shared progress

The only editable task-status source is `docs/delivery/progress.json`. Regenerate [the checklist](docs/delivery/PROGRESS.md) with `python scripts/delivery.py --write`. The [roadmap](docs/ROADMAP.md), [contracts](docs/endstate/CONTRACTS.md) and [handoff](docs/delivery/HANDOFF.md) define the next work for both chat and Codex.

ES01-01 through ES01-04 have scoped verification. ES01-05 remains partial pending explicit embedded-package acceptance and result-contract compatibility review. Do not turn that partial gate into an implied public release.

## Still open

B02-09, reliable new-situation model graph proposals, remains blocked on the recorded actual Qwen failure. B02-18, the full V0.2 release gate, is not complete. GLiClass's initial evaluation was poor; Jev has no authorised live-test credential. [AI evaluation](docs/v2/AI-EVALUATION.md) retains those facts. This kernel extraction does not claim new model quality.

At this checkpoint PR #2 remains draft and unmerged; main remains at `08bc26ef397ec960d1b33b099c40888a8229eac0`. No merge, deployment or standalone ENDSTATE release. Real agency identities, expert/client access, confidential evidence storage and recovery controls remain production work. Use fictional/test information only.
