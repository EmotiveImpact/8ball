# 8BALL + ENDSTATE: current delivery checkpoint

Status review: 23 September 2026. **8BALL is the fixer product. ENDSTATE is the reusable engine underneath it.** The accepted naming does not mean a standalone kernel/package has already been extracted.

## Read the live progress record

[docs/delivery/PROGRESS.md](docs/delivery/PROGRESS.md) is the version-by-version and subpart-by-subpart checklist. Edit its source, `docs/delivery/progress.json`, then regenerate it with `python scripts/delivery.py --write`. The [roadmap](docs/ROADMAP.md) defines milestone scope and the [handoff](docs/delivery/HANDOFF.md) defines how chat and Codex continue the same work.

## Inspected application baseline

`f87f775cb883d6914cff9230731671851a3fc660` on `feat/situation-intelligence-v2`, draft PR #2. At inspection PRs #1 and #2 were unmerged and main remained at `08bc26ef397ec960d1b33b099c40888a8229eac0`. No hosted production deployment or standalone ENDSTATE release. Refresh this snapshot against GitHub before new work.

The baseline's recorded application results are 221 pytest checks, 51 V0.2 native browser checks and 27 legacy native checks, with their scopes in `docs/v2/VALIDATION.md`. Those are historical application results, not a claim that new engine extraction or model-quality work has passed.

The manual/reviewed local workflow is implemented and tested. The actual Qwen graph gate failed; the first GLiClass configuration performed poorly; Jev has no authorised live-test credential. See `docs/v2/AI-EVALUATION.md`. The full real-model V0.2 acceptance journey remains open.

## This planning update

ENDSTATE naming, fixer-first positioning, future reuse lanes, a coordinated version roadmap, the complete preserved original PRD, task/evidence tracking and the shared session protocol have been added. Application code and runtime behaviour are unchanged. Documentation/tooling checks are recorded in `docs/delivery/sessions/2026-09-23-endstate-naming.md`.

## Next work

`B02-09`: reproduce and fix reliable new-situation graph proposals without weakening the evidence/verification gate. `ES01-01`: define the incremental ENDSTATE contract and extraction boundary while preserving the working fixer product. The ledger records both tracks and their dependencies. Agency security, expert/client accounts, evidence vault and deployment remain unimplemented production work.

This update does not merge, deploy, install a model or declare V0.2 finished. Fictional/test case data only.
