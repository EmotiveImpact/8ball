# 8BALL

**Find a way through.** Outcome-engineering software for a human-led situation room.

`0.1.0-alpha.1` is a working, local, single-operator developer release. It is **not a production agency service**. Use fictional data only. This repository is public; never commit case files, keys, exports or personal information.

## What works

An operator defines the situation, desired outcome, constraints and a human-authored action catalogue. The engine works backwards from the goal, produces alternative routes, checks prerequisites, schedules work by owner and recalculates when evidence changes. A polished, responsive browser workspace connects to a real FastAPI service and SQLite database.

There are eight views: agency command, situation room, outcome graph, ways through, evidence, actions and approvals, decision trail, and an operator-only client brief preview. The interface includes case intake, two editable playbooks, evidence review, disputed observations, revision-scoped approvals, completion recording, constraints, a non-persistent scenario sandbox and JSON audit export.

**Recording an action as completed never makes its intended result true.** Sending an offer is not proof that someone accepted it. A reviewed source plus a separate operator attestation establishes an evidenced condition. Conflicting attestations remain disputed until explicitly reconciled.

## Start locally

Use Python 3.12 or 3.13. The verified development environment is documented in `docs/VALIDATION.md`.

```sh
git clone https://github.com/EmotiveImpact/8ball.git
cd 8ball
git checkout feat/outcome-engine-alpha
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m eightball
```

On Windows activate with `.venv\Scripts\Activate.ps1` instead. Open `http://127.0.0.1:8048` and enter the operator token printed in the terminal. Select **Open fictional case**. The server intentionally binds to loopback only. It does not create a public website.

The default database is `~/.eightball/cases.sqlite3`. Stop the process with Ctrl+C. Data survives restarting; a new token is generated unless `EIGHTBALL_TOKEN` is explicitly set to a secret of at least 32 characters. Environment variables must be exported by your shell; `.env.example` is documentation, not an automatically loaded configuration file. Do not pass the token to a public service.

No Node installation, frontend build, model download or paid API key is needed for the core application. Optional models are disabled until deliberately configured and requested. The browser must use the local server, not open `web/index.html` directly.

## Try the outcome loop

Open the fictional Northstar case. Inspect its three candidate routes. Add an incident preservation log in Evidence, review the source, and attest the condition **Incident records preserved**. Root-cause investigation becomes ready. Record a task as completed and notice that its intended outcome remains unknown until evidenced. Use **What if?** to test a £1 budget; the routes fail that constraint without changing the case. Export the decision trail to inspect the stored event chain.

Estimated time and cost come from the editable playbook. They are illustrative, conditional inputs, not measured business benchmarks or success predictions. Third-party consent cannot be guaranteed.

## Optional AI

Jev is a bounded judgement service, not the planner. GLiClass Edge is a small, local, open-weight classification candidate. A local Ollama model can propose source-grounded observations. The adapters are implemented and their interfaces/failure handling are tested, but **no live model inference or model-quality benchmark was run for this release**. See `docs/AI.md` for verified sources, configuration and evaluation requirements.

AI can suggest; it cannot approve, attest, spend, send messages or modify a case. Free-text intake does not automatically generate a novel playbook in this alpha.

## Validation

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
node --check web/app.js
python -m playwright install chromium
python tests/browser_smoke.py
```

The local browser environment blocked URL navigation, so initial checks used an explicitly documented offline ASGI bridge. The subsequent native GitHub Actions run **35752284823** passed all 27 browser checks over real HTTP, including native session storage and downloads, with the existing CSP enabled. It also passed all 86 pytest tests. See `docs/VALIDATION.md` for the tested commit, retrieved report, earlier harness fixes and remaining limitations.

## Documentation and next milestone

- `docs/PRD.md`: product, acceptance journey and scope.
- `docs/ARCHITECTURE.md`: engine semantics, trust boundaries and production path.
- `docs/AI.md`: Jev, small local alternatives and evaluation plan.
- `docs/VALIDATION.md`: what was tested and what remains unverified.
- `STATUS.md`: delivery state and next implementation priorities.

Before real client use: authenticated identities, tenant isolation, role-scoped expert access, encrypted evidence storage, retention/deletion controls, independently anchored audits, operational monitoring, tested recovery and professional review. Neither this README nor the software establishes legal privilege or regulatory compliance.
