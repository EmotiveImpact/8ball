# Session: hosted development, target framing and black workspace

Environment: ChatGPT, 23 September 2026.

## Delivery boundary

Base remote commit: `824ca6421ff3100e1af596347f2d1247dde8f8dc` on `feat/situation-intelligence-v2`, draft PR #2. The source archive was checked against the exact base Git tree `68ff7ac7b212fbdf67f77d051f69d13ed39485be` before editing. This is a **local, unpushed checkpoint**. The GitHub write tool blocked the attempted write; no alternative write path was used. No commit, merge or deployment on GitHub is claimed.

Local working branch: `work/hf-black-drafting`. Its bootstrap Git commit is a local reconstruction of the base tree, not the remote commit. Apply the delivered patch to the exact remote base instead of merging this reconstructed history.

## Implemented scope

B02-09 / ES03-01: frame references now validate before route generation. Dynamic schemas restrict IDs to the supplied snapshot. The runtime staged path requires quotations covering the full human outcome and maps them to success criteria; the review room shows the target and each proposed criterion. This is structural coverage, not semantic truth. The captured Qwen failure is still preserved and now rejected earlier. Legacy compiler callers retain their wire contract.

ES03-06: optional Hugging Face transport, explicit model/provider, server-only credentials, per-analysis permission, bounded requests/responses, no redirects/retries/automatic routing, strict JSON failure handling and receipt metadata. A manual hosted test runner consumes the unchanged original four fictional cases. Missing configuration exits before requests. No HF key, paid call or real hosted inference was used.

B02-15 / ES03-04: a user-triggered local-runtime/weight inventory check and accurate configuration readouts. It never downloads or runs a model. Cancellation and durable progress jobs remain unfinished.

B02-19: black/graphite visual system, white primary controls, semantic evidence/status colours, ENDSTATE identity, explicit provider cards, target review and a mobile workspace lock. No new industry product or unrelated screen system.

## Verification

362 pytest checks passed, including 56 new hosted/target/probe checks. Python compilation and browser JavaScript syntax passed. Existing V0.2 (51 checks), legacy (27) and new development (15) browser suites run through the explicitly labelled ASGI bridge against the real application and SQLite. Native URL navigation was administrator-blocked; that policy was not changed. No current native browser or hosted-model result is inferred from these checks. See `docs/evidence/hf-black-local-verification.json` and the delivered browser reports.

## Still open

B02-09 remains blocked: no new real Qwen or HF generation has passed the actual fixture gate. B02-10/11/12 still need source reconciliation, independent quality labels and the full native real-model workflow. B02-13/14 guided editing/long sources and B02-15/16 job handling/accessibility remain unfinished. B02-19 is implemented but awaits native verification on the published source.

## Codex continuation

Fetch the remote and confirm it is still the base above. Use a clean working tree. Apply `8BALL-ENDSTATE-HF-Black.patch` with `git apply --check` followed by `git apply`. If the remote has advanced, review and reconcile the patch rather than resetting or force-pushing.

Run `python scripts/delivery.py --check`, `python -m pytest -q`, Python compilation, JavaScript syntax, then native `tests/browser_smoke.py`, `tests/browser_v2.py` and `tests/browser_development.py`. With an explicitly configured local Ollama installation, rerun `evals/live_generation.py` with `EIGHTBALL_GRAPH_PROVIDER=ollama_staged`. Preserve all four cases and failed evidence. Only after a real HF token/model/provider is supplied and processing authorised, run `python evals/live_huggingface.py --allow-hosted` on the same fictional fixtures. Do not paste the key into the repo or chat.

Push a normal reviewed checkpoint, record the actual commit/CI/model results, and replace the local/unpublished delivery annotation in the single ledger. Do not mark model quality, a release, main merge or a deployment complete merely because the transport tests pass.
