# 8BALL: outcome engineering for situation teams

Version: 0.1.0-alpha.1. Owner: Emotive Impact. 22 September 2026.

## Product contract
A professional states the current situation, a legitimate desired outcome, and constraints. 8BALL identifies what must become true, constructs executable alternative routes, attaches evidence to claims, and updates the plan when the situation changes. It supports judgement; it cannot guarantee another person's response or a real-world outcome.

The system is not a chat wrapper and not a general-purpose autonomous fixer. Its primary object is a Situation with an Outcome Graph. Planning is deterministic code; models make bounded, reviewable suggestions. The first workflow is commercial service recovery, using fictional data only.

## First working release
- Multi-case command view and a case-level Situation Room.
- Explicit conditions, actions, goals and alternative routes, editable as structured data.
- Backward goal expansion over a bounded action catalogue, with shared dependency deduplication, cycle validation and honest search limits.
- Evidence-linked observations, unknown/false/true/disputed state and explicit supersession. No model can verify its own claim.
- Per-owner scheduling estimates, budget ceilings, deadline slack, approval gates and blocked actions.
- Record action completion separately from proof that its intended result occurred.
- Scenario sandbox for deadline/budget/condition changes, without changing live state.
- An append-only application event ledger with revisions, hash linking and idempotency keys.
- Local persisted SQLite cases, JSON export, a simple client brief and a real browser interface.
- Disabled-by-default model adapters for Jev, GLiClass and Ollama. Advice only, not autonomous execution.

## Acceptance journey
Open the fictional Northstar retention case. Inspect routes. Add a source. Review that source and attest that the root cause is verified. Observe task readiness change. Tighten the deadline, see deadline pressure and route changes. Approve an eligible external-contact action. Completing a task must not mark the client retained. Simulate the client's refusal without mutating the case. Reload and retain the changes. Export the case including audit history.

## Not in this release
Multi-user identity, production tenant separation, real confidential evidence, file attachments/OCR, messaging connectors, autonomous external actions, proven model accuracy, causal outcome predictions, full resource optimisation, continuous background monitoring, certified evidence custody or a hosted deployment.

## Safety and trust requirements
Treat imported text as data, not instructions. Real client consent and approved data processing precede external model use. A task approval is revision-scoped and cannot survive a substantive case update. Models cannot alter case state, approve actions, send messages, suppress evidence or hide audit events. A reviewed document is not necessarily true: a human observation names exactly which condition it supports or contradicts. Conflicting active observations are disputed rather than silently overwritten. Withheld information and evidence destruction are not product capabilities.

## Production roadmap
1. Validate the local workflow with fictional and permissioned, de-identified cases; add an evaluation set reviewed by experienced operators.
2. Replace the local-token boundary with OIDC, organisation/matter membership, database row-level isolation and two-person approvals where required.
3. Add encrypted object storage, malware scanning, evidence source spans, retention/legal-hold policies and audited expert sharing.
4. Build a durable event/job pipeline with an outbox, retry limits, idempotent connectors and explicit send approvals.
5. Add model-assisted graph drafting and source-grounded extraction only after evaluation; never translate model certainty into outcome likelihood.
6. Pilot with qualified agencies. Measure missing-dependency rate, incorrect verification, unsafe readiness, replan usefulness and operator effort, not claims of guaranteed resolution.
