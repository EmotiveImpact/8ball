# ENDSTATE kernel extraction: verification record

23 September 2026. Scoped work: ES01-01, ES01-02, ES01-03 and ES01-04. Embedded preview only; no merge, deployment or standalone SDK release.

## Exact revisions

Starting source: `5e2098e9cb12251592eb3889ce7926798484699d`, tree `ce918eea4404101e6cbb502cf81a08c316e4dda9`.

Extracted application code: **`0c4104a675600c20a290766909bca60088766b35`**, tree **`6259e4aa41bc948f560fd54e26025071a74c5867`**. The staged local source tree was compared byte-for-byte with that Git tree before publication. The following documentation checkpoint changes no application algorithm.

Native GitHub Actions run **35904869115**, job **107329902516**, completed successfully on the extracted code. All steps passed: clean dependency installation, pytest, browser JavaScript syntax, Python compilation and both native browser journeys.

Run: https://github.com/EmotiveImpact/8ball/actions/runs/35904869115

Downloaded artifact **10770074122**, SHA-256 **`37a3d03fc78ad2804ca8fdd71e004b3c73f0a98b4ee033f4e1782128fd628f90`**. The archive checksum was verified. Its reports are preserved unchanged as `docs/evidence/endstate-kernel-browser-report.json` and `docs/evidence/endstate-kernel-browser-v2-report.json`.

## Observed software results

**269 local pytest tests passed**, including all 233 starting tests and 36 new ENDSTATE extraction checks. Native CI also passed the complete pytest step. JavaScript syntax and `python -m compileall -q eightball endstate` passed.

The retrieved native reports contain **51 V0.2 + 27 legacy Chromium checks**, 78 total. They exercise real loopback HTTP, SQLite, session storage, reload and actual downloaded exports. The existing content security policy was not weakened. Both desktop/mobile V0.2 layouts and the original application journeys continue to work.

Local browser navigation remained blocked by administrator policy. The policy was not changed. The explicitly labelled local ASGI bridge separately passed 51 V0.2 and 27 legacy checks; that is not the source of the native networking/storage/download claims above.

## What the new tests establish

Ten fictional pre-extraction cases preserve their complete plan, briefing, budget-constrained plan and change output hashes. Only set-derived arrays are normalised; route order, dependencies, schedules, costs and states remain significant. The original V1 and V2 wire-schema hashes also match.

Frozen pre-extraction SQLite rows can be read by the new code, their original audit chains and snapshot replay still verify, and reading them does not rewrite the records. Import aliases point to one shared source/graph implementation.

8BALL's adapter passes a detached `PlanningSnapshot` without fixer-specific client/title/summary fields to the kernel. Changing a returned hypothetical result cannot mutate the application state. The versioned calculation boundary rejects unknown versions, naive clocks, invalid costs, dangling references and nested mutated models.

Neutral, sales and support fixtures use the same calculation code. Sales opt-out and support remedy-authority predicates require explicit evidence; planned effects never become observed success. An isolated subprocess runs with only ENDSTATE source and Pydantic while explicitly blocking 8BALL, HTTPX, FastAPI, SQLite and Ollama imports.

## What this does not establish

This extraction does not solve arbitrary-situation AI graph generation, authenticate a supplied observation, validate professional effectiveness, create a sales/support application, implement live connectors or establish production confidentiality. It runs the existing planner through a separated dependency boundary. Its route limits and non-optimal greedy schedule remain unchanged.

The direct local tests and browser journeys did not call real models. Any separately triggered model workflow is independent evidence and must be inspected as such; no model-quality gate is marked complete by this record. Earlier failed Qwen and GLiClass evidence remains in the ledger.

The calculation envelope is versioned but nested plan mappings retain the existing V0.2 shape. Complete the embedded-package acceptance/compatibility review before marking ES01-05 verified or describing ENDSTATE as a supported public SDK. Built, verified, merged, distributed and commercially released remain different states.

## Reproduce

```sh
python -m pytest -q
python -m pytest -q tests/test_endstate_kernel.py
python scripts/delivery.py --check
python -m compileall -q eightball endstate
node --check web/app.js
for file in web/v2/*.js; do node --check "$file"; done
python tests/browser_smoke.py
python tests/browser_v2.py
```
