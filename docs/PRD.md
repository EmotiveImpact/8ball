# 8BALL + ENDSTATE: master product requirements

Document revision: 1.3, 24 September 2026. Product owner: Emotive Impact.

**8BALL is the fixer product. ENDSTATE is the reusable outcome engine powering it.**

**Vision refinement:** 8BALL is the fixer’s live situation room for understanding, selecting and reconsidering a defensible course. ENDSTATE is the reusable evidence-linked planning and reconsideration engine. The expanded capabilities below are design direction, not implemented by this documentation revision.

Read the [8BALL vision](vision/8BALL.md), [ENDSTATE vision](vision/ENDSTATE.md) and [ADR 0004](decisions/0004-evidence-led-course-and-recovery.md). The recovered runtime baseline is alpha.7; this update does not claim the later reported Draft Repair source is present.

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

The result is a conditional plan, not a promise to control people or guarantee an outcome. When no supported path is found within the supplied catalogue, current evidence and declared search bounds, report those limits, missing information, conflicting constraints and decisions needed to reconsider the options. Do not claim global impossibility or invent a successful route.

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


## Development amendment: hosted inference and black visual identity

Decision [0002](decisions/0002-hosted-development-black-ui.md) records the owner's latest direction. Add optional Hugging Face Inference Providers support, retaining Ollama/manual operation. Credentials remain server-side, routing is explicit and case transmission requires per-analysis permission. The provider is not considered connected or evaluated merely because an adapter exists. Reuse the unchanged fictional regression set and record hosted results separately when a key is supplied.

Staged source-to-plan work must validate target quotations and existing references before route expansion. A coverage check does not prove semantic correctness. Reviewers must compare the requested outcome with proposed success criteria; neither successful transport nor a compiler pass can attest a fact.

Adopt the black/graphite visual system in [BLACK-VISUAL-SYSTEM.md](v2/BLACK-VISUAL-SYSTEM.md), keeping 8BALL's working fixer controls. Record the transport-only and visual subparts separately in the shared ledger. Current-model quality, source reconciliation, guided graph editing, complete accessibility and secure agency operation remain explicit requirements.

## Visual amendment: relationship exploration within the fixer product

The owner requested an Obsidian-style graph as an upgrade to 8BALL's black interface. Decision [0003](decisions/0003-relationship-explorer.md) adds a read-only relationship explorer, not a substitute for the outcome planner. Three views share the same case records: Connections, directed Outcome flow, and a keyboard-accessible Records list. Whole-case and selected-neighbourhood scopes expose recorded relations with labelled source status.

Dragging, pinning, zooming and filtering must not write to the case or audit. Positions and connection counts cannot imply authority, confidence or causal influence. Source assertions, intended action effects and active observations remain separate. Preserve exact AND/OR expressions in the inspector and require the existing human-reviewed controls for amendments. Track this as B02-20, independently of B02-13's still-unfinished guided authoring. The application remains a V0.2 developer preview; a visual upgrade is not a model-quality or production release.


## Source-handling implementation amendment

Source Desk implements part of B02-14 inside the Evidence workspace. It preserves bounded UTF-8 originals outside planning/model context, exact passage/quote offsets, explicit duplicate and version review, and source-linked retraction. This is not a relaxation of the original source/entity/date requirements. Semantic deduplication, identity reconciliation, timezone/deadline review, binary ingestion, independent professional validation and secure storage remain separate unfinished gates. See [SOURCE-DESK.md](v2/SOURCE-DESK.md) and the canonical task ledger.
## 17. Build-sprint emergence discipline

Implementation is allowed to teach us something the PRD did not anticipate. At the end of every substantive build sprint, ask: **“What did this sprint reveal that we had not properly seen, specified or understood before we built it?”** Capture the answer using [the emergence review](delivery/EMERGENCE-REVIEW.md).

Separate observed discoveries from hypotheses. Identify whether each finding belongs to the 8BALL product, the reusable ENDSTATE engine, both, or neither. Record new failure modes and operator/UX implications as well as opportunities. Do not silently convert an interesting insight into required scope: classify it against an existing task, retain it as a candidate, create a required task only by explicit product decision, create a decision record when architecture changes, or record no action.

This discipline is intended to prevent two opposite failures: blindly following an old roadmap after the product has taught us something important, and allowing every new idea to explode the roadmap. Changelog history, the session handoff and the canonical delivery ledger remain the source of truth for what was discovered and what was actually promoted.


## Accepted addition: case-level emergence and complete build-discovery retention

The owner explicitly requested that valuable build insights inform the product while **every identified insight, including deferred or declined ideas, remains listed for their review**. The canonical register is `docs/delivery/emergence.json`; its evolving readable view is `docs/delivery/EMERGENCE-REGISTER.md`. Original entries are retained and decisions append, with strikethrough rather than deletion for declined/superseded approaches. Delivery completion comes only from scoped `progress.json` tasks. The mandatory prompt sequence is in `docs/prompts/EMERGENT-INSIGHTS.md`.

8BALL gains a case-level **Emergent Insights** workflow, separate from both What Changed (case deltas) and What's new / Build discoveries (software development). The first bounded detector set asks what becomes visible by considering the existing evidence model and calculated routes together. It records a basis, why it matters, typed references, what would verify/disprove it, uncertainty, current relevance and human disposition. The specification and truthful limits are in `docs/v2/EMERGENT-INSIGHTS.md`.

The initial implementation is deterministic, with no new AI dependency. It detects recorded patterns, not unknown causal relationships. It permits operator-authored hypotheses so the fixer can capture what the current detectors miss. Findings never become verified facts through review. Dismissed findings, changed content, inactive patterns and recurrence remain inspectable. Only an explicit separate command can create a linked verification question; no observation, target change, approval or external action follows automatically.

Broader semantic contradiction detection, genuinely hidden dependencies, causal leverage, outcome envelopes and quantitative attention/information models remain individually listed candidates. Their inclusion in the register is not silent expansion of the V0.2 acceptance gate, and this feature does not replace the failed real-model source-to-plan requirement.


## Source-clarity implementation inside existing V0.2 scope

`0.2.0-alpha.5` implements an explicit interpretation layer under B02-10/B02-14: source-linked name judgements, civil-time clarification and previewed deadline adoption. It does not replace arbitrary extraction, independent model evaluation or the remaining multi-source acceptance criteria. Details and boundaries are in [SOURCE-CLARITY.md](v2/SOURCE-CLARITY.md). The source record, the operator’s interpretation and an adopted operational constraint remain distinct. No guessed identity merge or implicit scheduling change is allowed.

## Plan Review checkpoint: existing V0.2 acceptance work

Within B02-11 and B02-13, expose exact requested outcome, success predicates, structural diagnostics, independent hypothetical checks and six explicit human quality judgements. Record the assessment separately from evidence/approvals, with snapshot and clock provenance. The ENDSTATE structural assessment and route-ID collision fix support B02-03; they do not complete arbitrary-source planning. The proposed quality protocol requires owner/expert agreement and actual independent reviews before a model can pass. See `docs/v2/PLAN-REVIEW.md` and `evals/PLAN-QUALITY-GATE.md`.


## Integrated verification checkpoint, alpha.7

The existing ES01-05/B02-12/B02-16 work now includes explicit nested result schemas, an internal wheel installation test, one source-bound acceptance runner, improved keyboard/dialog focus and a separately authorised actual-provider integration command. See `docs/v2/ACCEPTANCE-RUNNER.md` and the canonical ledger for actual status. Native policy restrictions and missing model prerequisites remain blockers, not reasons to substitute mock results. Scripted inference integration is not independent semantic evaluation or the complete native-user workflow. All prior scope and failed model evidence remain preserved. EM-050 through EM-055 record this sprint's discoveries without creating additional product lanes.

## Vision revision 1.3: course, mandate, coverage and recovery

This amendment strengthens the existing fixer-first promise without changing the original required version gates. The original PRDs remain immutable references.

1. **Mandate:** define the target, explicit limits, authority, evidence of completion and any separately authorised fallback or confirmation period. A hard-to-reach outcome is not permission to rewrite it.
2. **Chosen course:** distinguish candidate routes from a human-recorded course and its rationale. Choosing does not attest facts, approve actions or execute anything.
3. **Reconsideration:** explain whether reviewed changes affect that course; never silently switch it, hide incomplete checks or relax conservative approval invalidation.
4. **Coverage:** disclose selected versus unprocessed source material, source relationships and catalogue/search limits. No route found means no route found within that stated scope.
5. **Recovery:** preserve failures and human corrections as separate attributed records; manual usability and unassisted model quality are different acceptance outcomes.
6. **Operator value:** measure better decisions, missed dependencies, false positives and review cost rather than promising value from graph size or more screens.
7. **Reproducible delivery:** an unrecovered source cannot inherit a claimed feature or test pass. Preserve reported-only records and rebuild or recover explicitly.

Detailed behaviour and proposed test scenarios are in `vision/ACCEPTANCE-DESIGN.md`. New optional work is B03-07, ES02-06, ES03-08 and B04-04. All existing required statuses remain unchanged; candidate adoption is neither implementation nor acceptance. EM-056 through EM-065 are new register entries; earlier relevant findings retain their original wording with appended decisions.

Do not create separate engines, graph stores or additional top-level screens solely to implement this vocabulary. Keep neutral semantics in ENDSTATE and human identity, mandate, case storage, permissions and execution in 8BALL or another explicitly authorised host.

## Local implementation amendment: Chosen Course

25 September 2026: `0.2.0-alpha.8` implements a bounded local selected-course workflow described in [CHOSEN-COURSE.md](v2/CHOSEN-COURSE.md). The operator explicitly selects/replaces a course and records lifecycle judgements; ENDSTATE reassesses recorded dependencies and clocks without altering facts or approvals. This is groundwork, not completion of the full client mandate, secure team authority, continuous events or V0.3. Original required V0.2 gates and historical requirements remain unchanged.
