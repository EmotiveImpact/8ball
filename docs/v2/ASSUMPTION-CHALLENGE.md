# Assumption challenges, reproducible comparisons and decision packets

Local, unreleased integration on `devin/1792969169-roadmap-integrated`, based on `4f31c6b40141990d0863d9375f47a7ad51863dfc`. This extends Plan Review, not the action-authority system. It does not implement a model swarm, predict particular people or import an upstream runtime.

## Operator flow

Open **Plan Review → Assumption challenge**. Declare up to four fictional/archetype perspectives and their information boundaries, with up to twelve assumptions, objections and questions. Each statement names inspected case references and what would verify or challenge it. Omitted perspectives and contributions remain missing, never agreement or consent. Named-person psychological profiles are not supported.

Compare up to three explicit branches. The UI offers a hypothetical condition, unavailable action and budget; the shared engine also supports explicit deadlines, resource starts and decision selections. Each branch uses the same authoritative snapshot and calculation clock. Comparisons expose the exact changed fields, snapshot/overlay/result hashes, contract/planner version and search bounds. Unknown, false, absent, zero, disputed and search cutoff remain distinct. Synthetic observations and cleared approvals exist only in a discarded hypothetical copy. No real case changes or hypothetical approvals are applied.

Preview your disposition and next-review decision. `continue_review` must explicitly acknowledge every unresolved objection. Other outcomes are seek information, reconsider or defer—not approve or execute. Labels such as addressed in review cannot establish a fact. Original wording remains in the brief. Unpreviewed disposition edits block saving instead of silently saving an older result; unsubmitted review values survive tab switches.

Save a derived brief to its separate, immutable case-scoped journal. Saving binds case revision/hash, clock, content digest and history sequence, with a fifteen-minute write window. The limit is 100 briefs per case and 128 KiB per brief. Duplicate identical saves return the original; reused keys with altered content fail. Rechecks append a predecessor link while preserving original perspectives/contributions and clearing review dispositions for renewed consideration. Actual evidence enters only through existing source/observation workflows.

## Two packet modes, no automatic sharing

Generate a packet only from a verified saved brief. The server checks the current case revision, exact saved brief, expiry, history sequence/head hash and current disclosure policy. It verifies case and derived histories and replays saved comparisons; missing/corrupt/cyclic predecessor history fails rather than producing a misleading partial audit.

- **Internal operator review:** includes the saved brief, reference hashes and predecessor pointers, but not predecessor contents, original source documents or unrelated journals. Every reference must be permitted.
- **Restricted reference index:** includes only explicitly selected reference IDs/hashes and packet metadata. All narrative, titles, declarations, review reasons, calculations and predecessor contents are omitted, even if their declared references appear allowed. The API accepts up to 64 selected references; this first UI selects one.

Both modes explicitly set `complete_audit=false`, `persisted=false`, `facts_attested=false` and `execution_authorized=false`. Omissions are visible. A restricted index is neither an anonymised document nor proof of what omitted material says; hashes and case/history metadata can still be sensitive. These are internal local-operator tools, not a permission to share with a client. A downloaded copy cannot be remotely revoked.

The permission set is copied before projection and rechecked before returning. A SQLite immediate transaction serializes concurrent database policy/case/history changes. This is a local same-database boundary, not distributed-authority acceptance. The caller cannot supply an allowlist. Both agency-host and access-only agency configurations omit these routes; local challenge histories are refused by agency audit export until a separately authorized scoped projection exists. Existing source-free audit exports retain their exact old shape.

## Reusable engine versus host

- `endstate/rehearsal.py`: attributed declarations, objections, dispositions and exact JSON change detection.
- `endstate/scenarios.py`: neutral `PlanningSnapshot` projection, deterministic comparison and replay verification.
- `endstate/decision_packet.py`: disclosure projection of a host-verified brief; no storage or permission discovery.
- `eightball/v2/rehearsal.py`: verified snapshot/journal persistence and replay.
- `eightball/v2/decision_packet.py`: current authority, transactional checks and packet envelope.
- `endstate/intelligence/decisions.py` and `eightball/v2/decision_models.py`: separate optional typed decision contract and native transport, not invoked by this workflow. See [decision-provider evidence](DECISION-PROVIDERS.md).

No Loomio AGPL templates/code, HighwayEnv runtime, semantic-router runtime or unlicensed assault-ai-pilot assets were incorporated. Source inspection informed original native implementations. Independent operator benefit, model quality, social simulation and production acceptance remain unproved.

## Verification

Focused Python tests cover malformed/stale/cross-case submissions, exact projection changes, deterministic replay, bounds, no mutation, corruption, missing predecessors and current permissions. The native Plan Review journey covers retained dissent, explicit acknowledgement, preserved edits, separate saving, real packet downloads and stale-export denial. The package guard recursively inspects ENDSTATE imports and the offline wheel smoke exercises comparison/replay, restricted projection and typed choices without importing application/provider services.

Run `.venv/bin/python scripts/acceptance.py --mode native --base 4f31c6b40141990d0863d9375f47a7ad51863dfc` with the existing Python/Node tools on PATH. The runner strips hosted credentials, including the new decision-provider variables. Read the exact source-bound report, not an older test count. No live model calls are part of ordinary acceptance.
