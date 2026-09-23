# Session checkpoint: ENDSTATE embedded kernel

Session ID / environment: 2026-09-23-endstate-kernel / ChatGPT.

Task IDs / objective: ES01-01 to ES01-04. Separate the reusable calculation core without changing 8BALL behaviour. ES01-05 records remaining package acceptance, not a claimed SDK release.

Branch / base commit: `feat/situation-intelligence-v2`, starting `5e2098e9cb12251592eb3889ce7926798484699d` / tree `ce918eea4404101e6cbb502cf81a08c316e4dda9`.

Files changed: new `endstate/` primitives, contracts, state, planner and in-process API; compatibility imports/adapters in `eightball/models.py`, `eightball/engine.py`, `eightball/v2/contracts.py` and `eightball/v2/planner.py`; frozen pre-extraction fixture and `tests/test_endstate_kernel.py`; one tracking test no longer assumes an eternally unclaimed task; CI compilation includes ENDSTATE. Final documentation updates the canonical ledger/board, PRD current boundary, README, STATUS, handoff and retrieved evidence reports.

Implementation commit: **`0c4104a675600c20a290766909bca60088766b35`**, exact tree **`6259e4aa41bc948f560fd54e26025071a74c5867`**. Local staged source matched that tree. The final documentation commit's resulting ID is posted on PR #2, not invented self-referentially here.

Tests and evidence: 269 local pytest tests (36 new); JavaScript syntax and Python compilation passed. Native GitHub run **35904869115**, job **107329902516**, succeeded. Retrieved artifact **10770074122** checksum `37a3d03fc78ad2804ca8fdd71e004b3c73f0a98b4ee033f4e1782128fd628f90` contains 51 V0.2 + 27 legacy native browser checks. Both reports are checked in unchanged. The local explicit ASGI bridge also passed both suites; administrator browser policy was not bypassed.

Compatibility proof: ten original case plans/briefings/deltas and wire-schema hashes; exact original database rows/audit hashes; neutral, sales and support fixture plans; strict input copying and validation; isolated process without 8BALL/database/web/model imports. Old observations, approvals, route semantics and source lineage remain intact.

Real models called: none by the direct local tests or browser journeys in this slice. Existing separately triggered model workflows are not kernel acceptance evidence. No model credentials, prompts or runtime configuration changed. Prior Qwen/GLiClass failures remain preserved and B02-09 remains blocked.

What remains unverified: supported standalone distribution, nested output-contract stabilisation and explicit package acceptance; arbitrary-situation graph quality; continuous event/connector operation; professional effectiveness and production agency security.

Task changes: ES01-01/02/03/04 and B02-17 verified for the same linked scope; the 8BALL compatibility task reuses the evidence rather than inventing another test run. ES01-05 partial. No B02 model or release gate promoted. The ledger, not this session narrative, is the editable current status source.

Last pushed code: `0c4104a675600c20a290766909bca60088766b35`, draft PR #2. Final documentation checkpoint is identified by its PR comment. No unpushed application work is intended after that checkpoint; any future local modifications require their own handoff.

Next task and commands: refresh the branch, read `docs/endstate/CONTRACTS.md` and the ledger's ES01-05; run `python -m pytest -q tests/test_endstate_kernel.py` and `python scripts/delivery.py --check`. The independent product blocker B02-09 still requires genuine new-source graph proposals to pass the unchanged model gate; never replace it silently with a catalogue output.

Merge/deployment state: no merge, no draft-to-ready transition, no deployment and no public SDK release. 8BALL remains the fixer product first.
