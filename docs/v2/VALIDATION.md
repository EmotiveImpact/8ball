# V0.2 verified engineering record

## Application revision

Code commit `117957d3ba4475c6644ff4833d036061d8be6d2c`, tree `378f21fad78a0c86be0cc2f06e3ef701b910d75c`, passed GitHub Actions run **35881920598** on 23 September 2026. The remote tree was compared byte-for-byte with the locally tested source tree before publication.

Run: https://github.com/EmotiveImpact/8ball/actions/runs/35881920598

## Results actually observed

**221 pytest tests passed locally**, including all 196 recovered tests and 25 additional release regressions. GitHub's clean-install validation run also passed its pytest step, JavaScript syntax checks, Python compilation and native browser journeys.

The downloaded browser artifact **10760793008** has SHA-256 `75e0b1ff0666d63d515dcfc19a9d7acc20d2862c42a53253ca798f38059cbc29`. It contains a **51-check V0.2 report** and a **27-check legacy report**: **78 native Chromium checks** in total. Both reports record real loopback HTTP, SQLite persistence and native storage/download journeys. No page runtime errors were recorded. The V0.2 UI was exercised at 1512 and 390 pixel widths.

Browser journeys cover source capture/review, supported observations, approval, completion distinct from outcome, change history, scenario isolation, route comparison, blank intake, accept/edit/reject, reviewed catalogue graphs, reload, snapshot replay and downloaded export. These UI journeys use explicitly labelled rules and catalogue providers. They do not establish real-model accuracy.

## Fixes added during release audit

The new regressions cover recorded answers being protected from generic replacement; invalid provider/purpose and source selections failing before inference or a failure trace; permission gates; visibility of older pending proposals; mutually exclusive decision requirements; projected guard and failure checks; signed evidence coverage; invalid resource windows; and transactional rejection without rewriting audit history.

## Local browser limitation

The local Chromium policy blocked URL navigation, including loopback. It was not disabled. Local interaction checks therefore used the existing explicit ASGI bridge against the actual application and SQLite store. All 51 V0.2 bridge checks passed, but that alone does not test browser HTTP, native session storage or native downloads. The separate native GitHub run above establishes the listed native journeys with the existing content security policy, not every browser, policy directive or accessibility case.

## Reproduce

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m compileall -q eightball
node --check web/app.js
for file in web/v2/*.js; do node --check "$file"; done
python -m playwright install chromium
python tests/browser_smoke.py
python tests/browser_v2.py
```

Models are deliberately not installed or invoked by these tests. Actual model runs are separate workflows under `evals/` and their results are discussed in `AI-EVALUATION.md`. Exact source packaging is provided by `.github/workflows/source-package.yml`, using tracked files, the commit/tree IDs and an archive checksum.

## Not established by this validation

Production tenant isolation, encrypted confidential evidence, independent audit anchoring, backup restoration, complete accessibility/cross-browser coverage, live Jev credentials, calibrated model accuracy, professional effectiveness or guaranteed case resolution. The local token is not an agency identity service. Existing code and tests are a developer release, not permission to introduce confidential client data.
