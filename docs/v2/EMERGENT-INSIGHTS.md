# Emergent Insights: first bounded product implementation

Version `0.2.0-alpha.4`, local developer checkpoint inside unfinished V0.2. This is **not** a production release or a general AI insight model.

## What is built

`endstate/insights.py` adds twelve deterministic detectors over a validated planning snapshot: shared unresolved signed prerequisites, conflicting active observations, completed actions without evidenced results, actor-link concentration, unspecified waits, one-source support clusters, opt-in age review, shared unresolved decisions, declared possible side effects, recorded objective failure conditions, unresolved deadline pressure and missing mandatory success criteria. `eightball/v2/insights.py` adds a thirteenth recorded-change check: requested outcome wording changed while objective records remain unchanged. The latter asks for alignment review, not an assertion of semantic drift.

The API and black Emergent Insights workspace support explicit scans, current/all/dismissed/historical views, explanations and typed record references, review reasons, operator-authored hypotheses, a separate review history, and deliberate creation of a verification question. The Build discoveries screen shows the complete development register, separately from client-case findings.

## What is not built

No unrestricted causal discovery, motive/authority inference, natural-language contradiction checker, autonomous opportunity search, automatic objective rewriting, probabilistic success ranking, new live-model integration, event listener or background scan runs. Freshness policies flag review of old observation records; they do not expire factual state. Outcome envelopes, quantitative information value and operator-load optimisation remain visible candidates in the build register.

## Core trust rules

- Derived means calculated from the recorded graph, not independently proven true. Actor concentration is only an inferred lead; it never establishes control or authority.
- Source-record counts do not establish independence. A copied email or two excerpts can have a common original. The single-source detector is conservative about a shared record and explicitly does not certify corroboration.
- Freshness is off until the operator chooses a threshold. The first implementation measures observation recording time, not source-event time. It never changes truth or approval semantics.
- Scans are explicit and record their `as_of`, case revision, detector version, policy, bounds and disabled rules. Comparisons are against the previous scan, not every intermediate event.
- The candidate pool is the bounded set with no hard breaches; it can still have evidence gaps, decision blockers and third-party dependencies. It is not all feasible real-world routes.
- An insight has a stable identity and content fingerprint. Relevant content changes invalidate its prior review. Disappearance is labelled not reproduced, not resolved. Disabled/capped scans label omitted findings not evaluated. Reappearance starts a fresh review occurrence, even if text matches an older dismissed finding.
- Review requires the current case and insight-ledger revisions, the current fingerprint and context less than 15 minutes old. Manual hypotheses never automatically refresh their supporting context; explicitly revisit the same hypothesis against current referenced records with a reason, or add a reviewed follow-up if those records were removed. Prior contexts remain in history.
- No scan/review/hypothesis changes case facts, objectives, approvals or plans. Explicit **Create verification question** runs the existing typed command path, increments the case revision, invalidates approvals and atomically links the created question to the insight event. It never creates an observation.
- Original scan output and review reasons remain in a separate append-only local hash chain. The case export includes it only when present, preserving the original source/insight-free export contract. This chain is not independently anchored or administrator-proof, and cannot establish factual truth.

## Local API

All endpoints use the existing operator authentication and origin boundary:

```text
GET  /api/v2/insight-rules
GET  /api/v2/build-discoveries
GET  /api/v2/cases/{case_id}/insights
POST /api/v2/cases/{case_id}/insights/scan
POST /api/v2/cases/{case_id}/insights/review
POST /api/v2/cases/{case_id}/insights/hypotheses
POST /api/v2/cases/{case_id}/insights/revisit
POST /api/v2/cases/{case_id}/insights/question
```

Mutation contracts carry `event_id`, `expected_revision` and `expected_insight_revision`. Review/question requests also require the displayed `insight_id` and `fingerprint`. A retry with the same content/event ID is idempotent; reused IDs with changed content are rejected. No endpoint accepts a model-authored approval or a `confirmed` factual state.

## Operator journey

Open a fictional case, select **Emergent insights**, and scan the current situation. Leave age review off or choose an explicit threshold. Inspect a finding's basis, caveat and affected records. Record useful/investigating/dismissed/review complete with a reason. Switch to Everything to inspect every recorded finding. Add a hypothesis the software missed. Explicitly create a verification question for an appropriate current finding. Check Questions and observe that no factual condition was attested. Add relevant evidence or change a recorded action, rescan, and examine changed/not-reproduced/reappeared findings. Export the case to preserve the separate insight history and original case audit.

## Delivery and tests

See `docs/evidence/emergent-insights-local-verification.json` for actual observed results. Native browser behaviour, all accessibility requirements, independent operator usefulness and broader model quality are separate gates. Never turn an unpushed local build or bridge result into a native CI claim.
