# 8BALL

**Current local checkpoint: 0.2.0-alpha.8, Chosen Course.** Select a reviewed candidate from Ways Through; inspect its original basis and current reconsideration reasons in the Situation Room. See `docs/v2/CHOSEN-COURSE.md`. Source remains local until an authorised push is verified. This does not complete V0.2 or permit confidential agency data.

## Latest local checkpoint: integrated acceptance, alpha.7

This complete local build consolidates every earlier upgrade and strengthens ENDSTATE's typed result contract, its actual internal distribution, keyboard/dialog behaviour and the end-to-end verification workflow. It remains **unfinished V0.2**, not a production service, public SDK or remotely pushed release.

After the development dependencies and Chromium are installed, run:

```sh
python scripts/acceptance.py --mode native --base <starting-commit>
```

The runner records source fingerprints, real counts and separate pass/fail/blocked results. It never falls back to a test bridge or calls a model automatically. Read [the integrated acceptance guide](docs/v2/ACCEPTANCE-RUNNER.md), [internal ENDSTATE package](docs/endstate/PACKAGE.md), [current status](STATUS.md) and [shared handoff](docs/delivery/HANDOFF.md).

A clone of the still-older GitHub branch does not contain these unpublished changes. Use the complete source package or **one** matching cumulative patch, not a stack of older cumulative patches. Source-write, native-browser, actual-provider and expert-review gates are recorded independently. No missing credentials or policy restrictions have been bypassed.

## Preserved previous checkpoint: Plan Review, alpha.6

Open **Plan Studio → Review live plan** for target tracing, structural findings, independent scenarios and a recorded six-part human review. This is a local developer checkpoint within unfinished V0.2. Review does not attest facts or approve actions. See `docs/v2/PLAN-REVIEW.md`, `evals/PLAN-QUALITY-GATE.md` and `docs/evidence/plan-review-local-verification.json`. All prior local upgrades are included; this package is not a pushed or deployed release.


**Find a way through.** Situation intelligence and outcome engineering for human-led case teams.

### Preserved previous checkpoint: 0.2.0-alpha.5

**Identity & deadlines** adds source-grounded human interpretation. Select exact wording, distinguish same-name actors without merging records, or interpret a date with explicit source context and timezone. Preview the route impact before adopting a deadline. Retractions and changed records flag old interpretations for review without deleting history. No AI provider is called by this feature. See [Source clarity](docs/v2/SOURCE-CLARITY.md).

The complete cumulative source remains local and unpublished. Current verification, 43 retained build discoveries and next integration gates are recorded in `STATUS.md`, the shared handoff and task ledger. The original source-to-plan quality gate remains open.

### Preserved earlier checkpoint: 0.2.0-alpha.4

**Emergent Insights** adds explicit, evidence-linked scans of the situation and its candidate routes. Twelve ENDSTATE structural checks plus a recorded target-alignment check surface patterns without claiming factual verification. Review, dismiss, reopen, add a hypothesis and explicitly create a verification question. Each judgement stays in a separate case-scoped history. No model or external provider is needed. See [Emergent Insights](docs/v2/EMERGENT-INSIGHTS.md).

**Build discoveries** is a separate, evolving owner-review register. All recorded ideas remain visible, including adopted, deferred and declined suggestions. The complete [emergence register](docs/delivery/EMERGENCE-REGISTER.md) and [prompt suite](docs/prompts/EMERGENT-INSIGHTS.md) are linked into the PRD, roadmap, changelog and Chat/Codex instructions. Completion marks come from the canonical task ledger, not a second set of statuses.

This package includes every preceding unpublished checkpoint. It remains a local developer build, not a remote release. Read `STATUS.md` and the handoff before cloning or applying patches.

### Preserved earlier checkpoint: 0.2.0-alpha.3

**Source Desk** now sits inside Evidence & claims: preserve a longer UTF-8 text original, search it, select exact passages, review duplicates and trace evidence back to its original position. Full sources stay outside AI requests; only explicitly captured excerpts can later be analysed. Retraction preserves history and removes support from linked evidence. See [Source Desk](docs/v2/SOURCE-DESK.md).

This source includes all previous Plan Studio, job, changelog, Connections and hosted/black work. It remains local and unpushed. Current verification and handoff are in `STATUS.md` and `docs/delivery/HANDOFF.md`.

### Preserved earlier checkpoint: 0.2.0-alpha.2

**Plan Studio** adds guided conditions, nested AND/OR requirements, explicit false rules, guards, decisions and contingencies. Preview changes against real planning logic, then commit deliberately. **Analysis Monitor** shows queued/running/stage/cancelled states and suppresses stale or cancelled results. **What’s new** reads the same canonical changelog as [CHANGELOG.md](CHANGELOG.md).

This local source includes the prior unpublished provider/black and Connections upgrades. It is not on the remote branch yet. See [STATUS.md](STATUS.md), [Plan Studio](docs/v2/PLAN-STUDIO.md), [analysis jobs](docs/v2/ANALYSIS-JOBS.md) and [the latest handoff](docs/delivery/HANDOFF.md). New code is not automatically available from a clone until the cumulative patch is integrated through an authorised path.


## 8BALL, powered by ENDSTATE

**8BALL is the fixer application we are building and selling first. ENDSTATE is the reusable outcome-engineering technology underneath it.** Other applications can later supply their own domain knowledge and workflows; this is not a plan to abandon fixers or build every industry at once.

The shared calculation kernel now lives in `endstate/`; 8BALL calls it through compatibility adapters. See [the embedded contract](docs/endstate/CONTRACTS.md) and [extraction verification](docs/endstate/VALIDATION.md). A standalone supported SDK, public engine service and additional production products are not yet released.

For work in this chat or Codex, start with:

- [Master PRD](docs/PRD.md) and [version roadmap](docs/ROADMAP.md).
- [Version/subpart checklist](docs/delivery/PROGRESS.md), generated from `docs/delivery/progress.json`.
- [Shared handoff](docs/delivery/HANDOFF.md) and [AGENTS.md](AGENTS.md).
- [Original full V0.2 PRD](docs/reference/8BALL-V0.2-ASTRA-PRD.md), preserved without reducing its requirements.

Update the ledger when a task changes, then run `python scripts/delivery.py --write` and `python scripts/delivery.py --check`. Built, verified, merged and released are separate states. The existing failed real-model graph gate remains open.

## V0.2 developer build

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

Twenty-one navigation views plus focused intake/detail/review dialogs: agency command, situation room, intake review, situation map, route comparison, actions/approvals, open questions, decisions, people/organisations, evidence/claims, timeline, changes, simulation, audit, client brief preview, playbooks, intelligence settings, Plan Studio, What’s new, Emergent insights and Build discoveries.

The V0.2 domain supports signed AND/OR prerequisites, explicit guards, multiple objectives, failure criteria, scoped restrictions, resource windows, active/wait durations, decision gates, reversible/irreversible actions and disclosed side effects. Routes use bounded backward search and forward validation with greedy scheduling. Counts and estimates are structural/operator inputs, not success predictions. External responses remain contingent.

Transactional persistence includes revision checks, idempotency, expiring approvals, event snapshots with linked hashes, replay verification, model proposal/disposition history and case export. Legacy alpha cases can be imported into a separate V0.2 case without altering the original. The original `/` workspace and its tests remain available.

### AI reality

Ollama adapters propose source-linked objects, novel graph structures and open questions. Jev and GLiClass provide optional bounded classifications. Every generated action begins approval-required. All model output remains advisory. The core engine owns arithmetic, state and constraints.

The first real GLiClass CPU experiment completed but scored only 6/30 raw top-one matches with 100% abstention on our fictional challenge set. It is **not approved as a production classifier**. Results, exact model revision and environment are preserved. Do not confuse a completed model job with a good model. See `docs/v2/AI-EVALUATION.md` for model setup, actual generation evidence and limitations.

### Optional hosted development and black workspace

The current development patch adds a black/graphite interface, explicit local-runtime checks and optional Hugging Face extraction/staged-graph/question support. No hosted key is supplied or model selected by default. Read [HOSTED-DEVELOPMENT.md](docs/v2/HOSTED-DEVELOPMENT.md) before configuring `HF_TOKEN`, `EIGHTBALL_HF_MODEL` and `EIGHTBALL_HF_PROVIDER`. The manual/local application still works without them. Configuration presence is not a successful connection or quality test.

The same original four model fixtures can later be run using `python evals/live_huggingface.py --allow-hosted`. It is not an automatic CI step. Check `STATUS.md` for the exact unpushed/pushed state and validation boundary of this source package.

### Validation and specifications

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
node --check web/app.js
for file in web/v2/*.js; do node --check "$file"; done
python -m playwright install chromium
python tests/browser_smoke.py
python tests/browser_v2.py
python tests/browser_development.py
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

## Vision and source-status refinement

Read the [8BALL vision](docs/vision/8BALL.md) and [ENDSTATE vision](docs/vision/ENDSTATE.md). Their mandate, chosen-course and reconsideration additions are design direction, not newly shipped features. The existing required V0.2 gates remain open.

This documentation overlay is based on the recoverable alpha.7 source. A later Draft Repair handoff reports unrecovered source; do not claim its runtime or test count from this package. [ADR 0004](docs/decisions/0004-evidence-led-course-and-recovery.md) records the boundary and optional candidate tasks.
