# Validation record

Date: 22 September 2026. Release: `0.1.0-alpha.1`.

## Local results

`python -m pytest -q`: **86 passed**. Covers deterministic graph expansion, alternative routes, shared dependencies, owner scheduling, evidence review/conflicts/retraction/supersession, completion versus outcome, current-revision approvals, graph validation, input bounds, transactional persistence, stale/concurrent commands, idempotency, scenario non-persistence, authentication/origin/host checks, chain/snapshot tampering, and AI adapter request/response validation.

`node --check web/app.js`: passed. `python -m compileall -q eightball`: passed.

`EIGHTBALL_BROWSER_BRIDGE=1 python tests/browser_smoke.py`: **27 checks passed**. Real Chromium rendered the actual application JavaScript/CSS. Sixteen checks covered eight views at 1512px and 390px widths. The remaining checks exercised intake, escaped evidence, source review, observation-driven readiness, approval/completion, reopening persisted server state, scenario comparison, audit verification and export-payload generation. There were no page runtime errors in those journeys.

## Browser limitation

The local Chromium instance has an administrator URL block that prevented navigation even to loopback. That policy was not changed or bypassed. The fallback loaded our own document in memory and forwarded browser fetch calls through an explicit test harness to the real FastAPI application and real SQLite database. It is not a static fake interface, but it is also **not a native browser-network test**.

Consequently native browser HTTP, CSP enforcement, sessionStorage persistence, native downloads, real Origin-header behaviour and full cross-browser accessibility remain unverified locally. HTTP boundary rules were separately exercised with the API client. The browser harness also launches the real CLI and checks its loopback health response. The supplied GitHub Actions workflow requests the normal native-browser journey; writing a workflow is not evidence that it passed. Check the pull request's actual CI run.

## Model limitation

Jev and Ollama tests use HTTPX MockTransport. GLiClass tests inject a test pipeline. They verify contracts, finite scores, source-span checks, consent gates and unavailable-provider behaviour. They do not measure real model inference, latency, memory, calibration, accuracy, prompt-injection resistance or production dependencies. No secret, paid request or model weights were required for tests.

## Environment

Python 3.13.5; FastAPI 0.128.2; Pydantic 2.13.4; Uvicorn 0.48.0; HTTPX 0.28.1; pytest 9.0.2; Playwright 1.57.0; Node 22.16.0. Core direct dependencies are pinned. This is not a full transitive supply-chain lock or vulnerability audit. Optional GLiClass/Transformers dependencies were not installed.

## Scope of evidence

The fictional recovery and retention playbooks demonstrate state transitions and scheduling, not that these routes solve a real contractual dispute. Costs and durations are illustrative inputs. A passed test suite is not a security certification or proof of business outcomes. Multi-tenancy, confidential evidence handling, legal privilege, hosted availability, backup restoration and real-world operator effectiveness have not been established.
