# Operator walkthrough: the local V0.2 build

Use fictional data only. This walkthrough does not describe a deployed agency service.

## 1. Start the workspace

From the source folder run `sh scripts/run-local.sh` on macOS/Linux, or `scripts/run-local.ps1` in PowerShell on Windows. Python 3.12 or 3.13 must be installed. The script creates a virtual environment, installs pinned direct application dependencies and starts the server. It does not install AI models.

Open `http://127.0.0.1:8048/v2/` and paste the operator token printed in your terminal. Keep the terminal running. The server binds only to the local machine. Cases persist in `~/.eightball/cases.sqlite3`. A new random token is generated on restart unless a secret `EIGHTBALL_TOKEN` has been deliberately configured.

## 2. Explore the fictional Northstar case

Select **Open fictional case**. The target is an accepted customer recovery agreement. The case contains labelled fictional sources and a few demonstration attestations. Inspect the target, map, Now panel, questions and candidate routes. These route durations and costs are playbook estimates, not forecasts.

Open **Ways through**, choose an explicit ordering and compare two routes. Inspect a route to see its sequence, prerequisites, waits, restrictions and contingency records. No outcome probability is shown. An action requiring customer agreement is conditional even when it has no unmatched graph inputs.

## 3. Observe how evidence changes readiness

In **Evidence & claims**, add a fictional source titled `Reviewed external wording`, attributed to `Fictional legal adviser`, with this text:

> External language has been approved by the fictional reviewer.

Review the source, then separately record an observation for **External language approved**, supported as true. Supply a rationale. Reviewing the source alone is not enough.

Open **Actions & approvals** and inspect **Confirm customer requirements**. Its prerequisites are now supported, but it still needs approval. Approve that specific action, then record its completion. This records work performed outside 8BALL; it does not contact the customer. **Customer requirements confirmed** must remain unknown until separately supported by evidence.

Open **What changed?** to inspect the resulting state and readiness differences.

## 4. Test a refusal without changing reality

Open **What if?**, select the condition **Standstill refused**, assume true, and select the hypothetical decision to seek mediation. Compare the resulting routes. The scenario is labelled as a simulation and is not committed to the live case. The absence of a response cannot be silently equated with refusal.

## 5. Build a case from messy sources

Create a new situation with **Blank case** selected. Describe what is happening and the desired outcome. Add several separately attributed source excerpts. Choose **Analyse sources**.

**Rules-based sentence capture** requires no model and records candidate claims/questions. It does not understand the case or infer people and deadlines. **Local Ollama** requires an installed/running model and can propose richer structured objects. **Jev** is an optional external judgement provider that needs server-side credentials and explicit transmission permission.

In **Intake review**, compare each proposal with its quotation. Accept one, edit another and reject another. Choose the edited disposition when committing edited JSON. The default is rejection. Accepting a claim does not verify it. Related graph items must be reviewed together; dangling references fail atomically.

Use **Propose outcome graph** to select a human-authored catalogue template or request a local-model draft. Inspect the desired success conditions, dependencies, authority, estimates and final verification action before acceptance. A valid schema is not proof that the proposed route would work in reality.

## 6. Inspect the people and preserve the record

Use **People & organisations** and the people map to inspect reported roles and relationships. Use **Decisions** to record direction, source evidence and rationale. Use **Open questions** to see which unresolved conditions affect routes and blocked actions. Use the explicit answer command to revise an answer; generic editing cannot erase a recorded answer.

Export the complete case from **Decision trail**. It includes snapshots, source data and model-review history and should be treated as sensitive even when the examples are fictional. The client brief export is a reviewed operator projection, not a secure client portal.

## Boundaries to remember

No message, phone call, payment or external action is sent. No client/expert account exists yet. A local token is not a multi-tenant authorisation system. Keep real confidential case material out until the production gate is implemented and reviewed.
