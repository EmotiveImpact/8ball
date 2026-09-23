# 8BALL + ENDSTATE: master product requirements

Document revision: 1.1, 23 September 2026. Product owner: Emotive Impact.

**8BALL is the fixer product. ENDSTATE is the reusable outcome engine powering it.**

Preferred wording: **“8BALL, powered by ENDSTATE”** and **“using our ENDSTATE engine”**.

## 1. Authority and how to read this PRD

This master incorporates the accepted ENDSTATE naming and multi-application direction without replacing the fixer mission or reducing the original V0.2 requirements. It is the entry point for both this chat and Codex.

Read alongside:
- [Original V0.2 PRD, all 37 sections](reference/8BALL-V0.2-ASTRA-PRD.md), preserved byte-for-byte.
- [V0.2 implementation requirements](PRD-V0.2.md), including existing evidence, review and safety invariants.
- [Version roadmap](ROADMAP.md) for milestone scope, order and exit criteria.
- [Live delivery checklist](delivery/PROGRESS.md) for completed and outstanding subparts. Its sole editable status source is `delivery/progress.json`.
- [Shared development handoff](delivery/HANDOFF.md) and root `AGENTS.md` for the session protocol.

The original V0.1 PRD is archived at [reference/8BALL-V0.1-PRD.md](reference/8BALL-V0.1-PRD.md). Historical documents retain their original names and dates. New naming and reusable-engine direction take precedence where those documents describe the brand; their uncompleted functional and acceptance requirements remain in force. Any scope reduction requires an explicit recorded decision, not changing a checkbox to make a version look complete.

## 2. Product mission and first customer

Build a professional application that helps a fixer or situation-handling agency understand a difficult case, define an acceptable outcome, construct alternative lawful routes, coordinate decisions and evidence, and adapt when information changes.

The first commercial product is **8BALL for fixers**, with closely related crisis teams, private offices and client-management agencies as potential users. A sellable release requires a useful operator experience, professional validation, confidential-data controls, specialist/client permissions and dependable operations. A runnable developer alpha does not satisfy those requirements.

ENDSTATE is the shared engineering asset created in delivering that product. Reuse is an architectural requirement, not a reason to split attention across multiple unvalidated products.

## 3. What outcome engineering means

Given the current evidenced state, a human-defined desired outcome, permitted actions and constraints, work backwards to identify necessary conditions and candidate paths. Then check those paths forwards for dependencies, conflicting effects, authority, time, resources and verification requirements.

The result is a conditional plan, not a promise to control people or guarantee an outcome. When no supported path exists, return the missing information, conflicting constraints and decisions needed to reconsider the objective. Do not invent a successful route.

The user can start with an outcome, but an outcome alone does not supply knowledge of the world, legal authority, resources, actions or causal effects. The system must ask for or propose those missing inputs and label assumptions. Human review establishes which proposed structure the case will use.

## 4. Product boundary: 8BALL and ENDSTATE

| Responsibility | 8BALL product | ENDSTATE engine |
| --- | --- | --- |
| User language | Situations, clients, fixers, specialists, agency command | States, entities, evidence, objectives, actions, constraints |
| Experience | Intake, situation room, maps, routes, decisions, expert/client views | Typed contracts, validated commands, calculation and explanations |
| Specialist knowledge | Professional playbooks and case-specific restrictions | Accept and enforce explicit domain-supplied constraints |
| Integrations | Case-authorised source ingestion and collaboration | Normalised events, permissions and action interfaces |
| Business model | Product sold to fixers and agencies first | Reusable internal technology; possible later licensing/API/SDK |

ENDSTATE must be able to serve a second domain without duplicating its planner or leaking one client's records into another. It need not become a separately deployed service immediately. Keep one repository until a concrete packaging or ownership requirement justifies a split.

**Implemented boundary, 23 September 2026:** shared calculation code now lives in `endstate/`, with 8BALL compatibility adapters retaining its case, command and storage contracts. Separate distribution and supported public SDK acceptance remain unfinished. See [the embedded contract](endstate/CONTRACTS.md) and [verification record](endstate/VALIDATION.md). No data migration or model installation is implied.

## 5. Core outcome contract

Inputs must include a versioned state/evidence snapshot, explicit success and failure criteria, an action catalogue with prerequisites and intended effects, actor/authority references, constraints and known/unknown estimates. Each model proposal is traceable to its model, schema, source set and base revision.

Outputs must include candidate routes, shared and alternative work, evidence gaps, decisions, next eligible actions, restriction failures, time/cost/resource estimates, external dependencies, possible side effects, verification requirements and the changes from the preceding plan. Expose search limitations, unsupported assumptions and unknown waiting times.

The exact public ENDSTATE contract will be designed and tested during extraction. Proposed operations are `observe`, `set_outcome`, `plan`, `compare`, `simulate`, `explain_changes` and `next_actions`; these are target interfaces, not a claim that a standalone SDK currently exports them.

## 6. The living plan and real-time behaviour

Required future sequence:

```text
Authorised source event
  -> preserve original source and provenance
  -> propose interpretation, including any goal/dependency change
  -> validate and review according to the action's authority policy
  -> commit accepted evidence/graph change at an explicit revision
  -> invalidate stale approvals
  -> recompute affected routes, blockers and questions
  -> show what changed and why
  -> human-approved work
  -> observe its actual result separately
```

“Real time” means event-driven, bounded-delay updates once authorised data reaches the system. It does not mean 8BALL knows events it has not received, that an LLM call is instantaneous, or that every incoming message is trusted.

A new email can change a fact, but changing the plan's action catalogue or removing a prerequisite requires a reviewed graph amendment. For example, a customer's willingness to meet before receiving the final report must not silently erase a restriction. Until approved, show the proposed alternative and keep the live restriction.

The current local application recalculates after committed updates and explicit plan requests. Continuous inbox/CRM ingestion, durable jobs, notifications and measured end-to-end freshness are separate unfinished delivery items. Event duplication, out-of-order arrival, retries, cancelled jobs, source retraction and concurrent reviewers must be tested before those connectors are trusted.

## 7. Evidence, authority and quality invariants

Source existence, a reported claim and an evidenced condition are different things. Unknown is not false. Contradictory active observations are disputed. Retraction removes active support without erasing history. An actor's motives or authority are not facts because a model guessed them.

Completing an action never proves its intended effect. Sending a proposal is not acceptance; an email open is not buying intent; replacing a product is not proof the complaint is resolved. Final outcomes need explicit evidence and an appropriate confirmation rule.

Models propose structure and interpretation. Operators commit observations, decisions and approvals. Proposals must be source-scoped and revision-bound; partial acceptance must preserve references atomically. Recorded answers and decisions cannot be wiped through generic editing. Simulations remain isolated from live state.

No fabricated success probabilities, guaranteed-resolution claims, silent cross-client learning or automatic external execution. High-impact/irreversible actions need appropriate authority and professional review. Structured policy checks do not establish universal legal compliance.

## 8. 8BALL functional scope

Retain the full V0.2 requirements: typed actors/relationships/events/claims/conditions/objectives/constraints/actions/resources/decisions/questions; attributed intake; reviewable extraction and graph proposals; source spans; nested AND/OR and explicit false requirements; guards and signed effects; known/unknown waits; multiple goals; alternatives; reversibility and side effects; decisions and approvals; route comparison; structural question prioritisation; What Changed; isolated What If; versioned playbooks; case-local retrieval; audit/replay/export; and legacy compatibility.

The interface must make four answers immediately accessible: **What is true? Where are we going? What blocks us? What do we do next?** Find a Way Through returns Now, Next, Decisions, Questions, Routes and Watch. Client views deliberately omit internal allegations, assumptions and strategy unless specifically approved for publication.

An effective professional product also needs guided graph editing, deadline/timezone review, safe duplicate/entity reconciliation, source chunking with preserved offsets, progress/cancellation for model work and accessibility. These are tracked separately from the existing JSON-editor and excerpt-based developer workflow.

## 9. ENDSTATE reusable architecture

Extract only real shared responsibilities: evidence-supported state, graph/objective contracts, planner and scheduler, restrictions and authority gates, question impact, scenario isolation, change explanations, revision semantics and model-provider interfaces. Keep 8BALL templates, language, UI and agency workflows in its domain/application layer.

Use compatibility adapters to protect existing imports, persistence and legacy audits. Migration must not rewrite historical facts, mark hypotheses as observed or change route semantics merely because a module moved. A neutral fixture, a sales fixture and a support fixture must use the same kernel with different domain inputs. This is proof of reuse, not three finished products.

Target dependency direction: `8BALL application -> 8BALL domain pack -> ENDSTATE contracts/kernel`. ENDSTATE must not import the 8BALL UI, hard-coded case names or client playbooks. Whether packaging uses a Python package or later service must follow measured needs. Do not introduce an agent swarm or microservices solely for branding.

## 10. Models are replaceable assistants

ENDSTATE is not Qwen, Ollama, Jev or GLiClass. Deterministic code owns state, constraints, route arithmetic and approval gates. Models may extract, classify, propose a graph, suggest questions or draft language.

A local model needs weights and a running service on the intended host; a temporary CI installation is not a customer installation. Jev's current adapter needs an authorised TypeSafe API credential, not a local “Jev installation”. Show actual runtime/provider status. Never put secrets or case data in this public repository.

Keep manual/rules/catalogue paths honest and usable without AI. Distinguish contract tests, actual inference and independent quality evaluation. Do not select a production model merely because its download is small. A larger model is an option only after licensing, processing policy, latency, costs and performance are evaluated. A few successful examples do not prove reliable arbitrary-situation planning.

## 11. Domain packs and future applications

| Potential application | Domain-specific requirement beyond the shared engine |
| --- | --- |
| Fixers / crisis managers | Evidence handling, lawful stabilisation, qualified specialists and client confidentiality |
| Sales / customer success | CRM state, legitimate outreach policy, opt-outs, economic authority and signed/verified business outcomes |
| Customer service | Order/issue verification, remedy authority, service deadlines and customer confirmation |
| Social-media / client managers | Client-approved goals, genuine campaign data, content approvals and platform-compliant actions; no invented causal guarantees |
| Public-office / political staff | Constituency casework, policy/service delivery, public-interest records and lawful coordination; no personal-data-based political persuasion |
| Other operational applications | Explicit action semantics, success evidence, permissions, domain evaluation and support ownership |

These are future reuse lanes, not products already built or permissions to launch all of them. Fixer validation remains the first commercial priority. Prove one or two adjacent domain packs using test data; pilot additional lanes only with an explicit decision. ENDSTATE licensing, public API, SDK and MCP are later distribution options, not current deliverables.

## 12. Versions and subparts

Keep two named tracks without inventing released tags:

- **8BALL:** V0.1 foundation; V0.2 reviewed situation intelligence; V0.3 secure agency pilot; V0.4 professionally reviewed resolution intelligence; V1 fixer production release.
- **ENDSTATE:** V0.1 reusable core; V0.2 event-driven replanning contracts; V0.3 evaluated intelligence compilation; V0.4 domain packs/integration interfaces; V1 supported reusable engine release.

Outcome engineering is present throughout. ENDSTATE version numbers measure engineering maturity, not a countdown before 8BALL becomes useful. A shared task may support both tracks; cross-reference it rather than marking duplicated work complete twice. Subpart IDs are stable work items, not package versions. Actual Git tags and application version constants change only through a release decision.

The [roadmap](ROADMAP.md) and [checklist](delivery/PROGRESS.md) define exact version gates. Software built, software verified, merged code, packaged artifacts, model quality and production deployment are separate states. A version cannot be called accepted while a required gate is partial, blocked or unstarted. Optional Jev testing does not replace the required generative-planning gate.

## 13. Acceptance and evaluation

Preserve the original twenty-step V0.2 end-to-end journey. Starting from a blank case, real model extraction and reviewed graph proposals must yield meaningful alternative routes; human edits and rejections must work; new evidence must alter route/question state; scenarios must stay isolated; completion must not imply success; reload and audit must preserve the whole process. Rules/catalogue browser journeys do not substitute for this real-model journey.

Use independently reviewed, separately held-out cases for negation, contradiction, actor authority, deadlines, missing dependencies, alternatives and verification. Agree quality/latency thresholds before the held-out run; record the dataset, model/runtime, schema/prompt version, corrections and failed cases. Do not weaken a gate after observing a failure without an explicit product decision and rationale.

Fixer pilots must measure time to a reviewable plan, correction effort, omitted dependencies, unsupported assertions, unsafe eligibility, change usefulness and operator effectiveness. Each new lane must pass its own professional evaluation even when the kernel is shared. The engine cannot assume success in one lane proves effectiveness in another.

## 14. Production release requirements

Before real agency data: authenticated identities and MFA where appropriate; organisation/matter access; cross-tenant denial tests; scoped experts and revocation; separately published client projections; encrypted evidence with immutable originals, malware scanning and hashes; retention/hold/deletion controls; authorised provider processing; independent audit checkpoints; recoverable backups; observability; and tested incident handling.

See [production security design](v2/PRODUCTION-SECURITY.md). Those requirements are not satisfied by the current local token, SQLite file, screenshot, source ZIP or green unit tests. External messaging/payment/call connectors require separately authorised recipient/content/scope, expiry, revision and idempotency controls; no such capability is implied by this update.

## 15. Shared delivery rules

Every session in this chat or Codex must read the actual current branch, this PRD, the delivery checklist and handoff before making changes. Claim a small task with a unique ID, record its base commit and owner, preserve uncommitted work, test the scoped change and update evidence/status in the same delivery.

Never mark work verified from intention, a screenshot alone or an old test run covering different code. Never claim an unpushed local change is available to the other environment. Push or export a reproducible patch/bundle and record the exact commit, tests and unfinished work. The next session refreshes repository state; the chat is not an alternative source of truth.

## 16. Current state and release authority

The naming/roadmap baseline was `f87f775cb883d6914cff9230731671851a3fc660`. The subsequent implemented kernel extraction is verified at **`0c4104a675600c20a290766909bca60088766b35`** on `feat/situation-intelligence-v2`, draft PR #2. 8BALL now uses shared ENDSTATE calculation code; the standalone package gate is not yet accepted. The arbitrary-situation AI graph gate remains open. See the ledger for task-by-task evidence rather than treating a document revision as a release.

No main merge, draft-to-ready change, public SDK release or production deployment is authorised by this checkpoint. Earlier merge suggestions remain recommendations, not completed operations. Refresh current GitHub state before further work and obtain a clear release instruction before merging.
