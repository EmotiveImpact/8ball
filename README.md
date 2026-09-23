# 8BALL

**Find a way through.** Situation intelligence and outcome engineering for human-led case teams.

## 8BALL, powered by ENDSTATE

**8BALL is the fixer application we are building and selling first. ENDSTATE is the reusable outcome-engineering technology underneath it.** Other applications can later supply their own domain knowledge and workflows; this is not a plan to abandon fixers or build every industry at once.

The shared calculation kernel now lives in `endstate/`; 8BALL calls it through compatibility adapters. See [the embedded contract](docs/endstate/CONTRACTS.md) and [extraction verification](docs/endstate/VALIDATION.md). A standalone supported SDK, public engine service and additional production products are not yet released.

For work in this chat or Codex, start with:

- [Master PRD](docs/PRD.md) and [version roadmap](docs/ROADMAP.md).
- [Version/subpart checklist](docs/delivery/PROGRESS.md), generated from `docs/delivery/progress.json`.
- [Shared handoff](docs/delivery/HANDOFF.md) and [AGENTS.md](AGENTS.md).
- [Original full V0.2 PRD](docs/reference/8BALL-V0.2-ASTRA-PRD.md), preserved without reducing its requirements.

Update the ledger when a task changes, then run `python scripts/delivery.py --write` and `python scripts/delivery.py --check`. Built, verified, merged and released are separate states. The existing failed real-model graph gate remains open.

## V0.2 developer release

The `/v2/` workspace turns source material into reviewable case objects, maintains an evidence-linked situation model, compares conditional routes and explains what changes when new information arrives. It is a real local application with FastAPI, SQLite, a responsive browser client and testable planning logic, not a chatbot or a static image.

**Local, single-operator, fictional/test cases only. Not a production agency service.** This repository is public. Never commit client information, keys, exports or model weights.

### Start

Use Python 3.12 or 3.13:

```sh
git clone https://github.com/EmotiveImpact/8ball.git
cd 8ball
git checkout feat/situation-intelligence-v2
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m eightball
```

Open **http://127.0.0.1:8048/v2/** and paste the operator token printed in the terminal. Windows users can run `scripts/run-local.ps1`; macOS/Linux users can run `sh scripts/run-local.sh`. These convenience scripts install only core application dependencies. Models are separately configured, not silently downloaded.

The CLI binds to loopback. Database: `~/.eightball/cases.sqlite3`, unless `EIGHTBALL_DB` is exported. Set a secret `EIGHTBALL_TOKEN` of at least 32 characters to retain the same token across restarts. The `.env.example` file documents variables; it is not automatically loaded. No paid API key, Node build or model is needed for manual planning, source capture or the catalogue.

### Explore the actual loop

Open the fictional Northstar case. Inspect the live model, Now panel, open questions and four structural route alternatives. Add and review source text, then separately attest a condition and watch readiness change. Record a decision, approve a suitable action and record completed work: the intended result remains unverified until evidenced. Compare routes, test a refusal in What If, inspect What Changed and export the decision trail.

Open a blank situation for intake. Paste sources or load a small `.txt` excerpt. Choose rules-based capture, an explicitly selected playbook, or a configured local model. Review proposals individually: accept, edit or reject. No proposal creates a verified fact. Related items are validated together; stale proposals cannot overwrite newer case state.

### What is implemented

Seventeen navigation views plus focused intake/detail/review dialogs: agency command, situation room, intake review, situation map, route comparison, actions/approvals, open questions, decisions, people/organisations, evidence/claims, timeline, changes, simulation, audit, client brief preview, playbooks and intelligence settings.

The V0.2 domain supports signed AND/OR prerequisites, explicit guards, multiple objectives, failure criteria, scoped restrictions, resource windows, active/wait durations, decision gates, reversible/irreversible actions and disclosed side effects. Routes use bounded backward search and forward validation with greedy scheduling. Counts and estimates are structural/operator inputs, not success predictions. External responses remain contingent.

Transactional persistence includes revision checks, idempotency, expiring approvals, event snapshots with linked hashes, replay verification, model proposal/disposition history and case export. Legacy alpha cases can be imported into a separate V0.2 case without altering the original. The original `/` workspace and its tests remain available.

### AI reality

Ollama adapters propose source-linked objects, novel graph structures and open questions. Jev and GLiClass provide optional bounded classifications. Every generated action begins approval-required. All model output remains advisory. The core engine owns arithmetic, state and constraints.

The first real GLiClass CPU experiment completed but scored only 6/30 raw top-one matches with 100% abstention on our fictional challenge set. It is **not approved as a production classifier**. Results, exact model revision and environment are preserved. Do not confuse a completed model job with a good model. See `docs/v2/AI-EVALUATION.md` for model setup, actual generation evidence and limitations.

### Validation and specifications

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
node --check web/app.js
for file in web/v2/*.js; do node --check "$file"; done
python -m playwright install chromium
python tests/browser_smoke.py
python tests/browser_v2.py
```

See `docs/v2/VALIDATION.md` for exact observed local/native CI results. Local bridged browser checks are explicitly distinguished from native browser networking, storage and downloads. `evals/` contains separate actual-model experiments.

- `docs/PRD-V0.2.md`: accepted product requirements.
- `docs/v2/ACCEPTANCE.md`: requirement-to-code map and boundaries.
- `docs/v2/ARCHITECTURE.md`: implemented semantics and limitations.
- `docs/v2/AI-EVALUATION.md`: model evidence and setup.
- `docs/v2/PRODUCTION-SECURITY.md`: proposed agency infrastructure and release gate.
- `STATUS.md`: delivery state; `AGENTS.md`: continuation rules.

### What this does not claim

No hosted deployment, tenant accounts, secure client portal, confidential file vault, OCR, automatic email/phone/payment execution, independently anchored forensic audit or guaranteed outcomes. The client brief is an operator preview. Free-text restrictions do not establish machine-verified legal compliance. Model/schema tests and fictional playbooks do not prove professional effectiveness. Complete the production security and expert-review gate before real client information is introduced.
