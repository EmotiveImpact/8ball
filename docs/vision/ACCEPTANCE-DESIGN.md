# Design acceptance examples for the stronger 8BALL / ENDSTATE vision

**Specification only. These are proposed acceptance scenarios, not executed runtime tests.**

## Course selection and revalidation

| ID | Scenario | Required result |
| --- | --- | --- |
| COURSE-01 | Operator selects Route A from snapshot 12 | Retain snapshot/target/route/dependency references and rationale. No observation, action approval or external execution follows. |
| COURSE-02 | A new ranking places Route B first | Route A remains the recorded choice. Explain the alternative; do not silently switch. |
| COURSE-03 | A reviewed source withdraws support for a prerequisite used by A | Preserve history, recompute from the committed revision and mark the course for review. Do not assert the world is false merely because support disappeared. |
| COURSE-04 | A purportedly unrelated change arrives | Preserve conservative approval invalidation. A future scoped explanation may say no affected dependency was found only within its recorded coverage. |
| COURSE-05 | A guard, policy, authority record or shared resource changes | Reconsideration must include these dependencies, not just visible prerequisite edges. |
| COURSE-06 | Two routes use the same actions in different orders | Preserve distinct identity, causal assumptions and constraint results; never merge them by action-set equality. |
| COURSE-07 | Some consulted record is unavailable, or recomputation fails | Report not established / review required. Do not return an old valid result without a stale label. |
| COURSE-08 | Only a clock deadline passes | Report elapsed review/deadline scope. Do not invent a third-party response or a factual observation. |

## Mandate, fallback and durable resolution

| ID | Scenario | Required result |
| --- | --- | --- |
| MANDATE-01 | The model proposes a narrower easier goal | Show target mismatch. Only an authorised explicit change can revise the objective. |
| MANDATE-02 | Ideal result is unavailable but an acceptable fallback exists | Present the fallback with its own authority, constraints and proof requirements. Do not mark the ideal outcome achieved. |
| MANDATE-03 | A source used to adopt a deadline is retracted | Retain the adopted operational commitment and flag reconsideration. Withdrawal is a separate authorised decision. |
| MANDATE-04 | Resolution requires seven days of demonstrated stability | One successful check does not fulfil the interval. The operator's declared window and evidence requirements control confirmation. |
| MANDATE-05 | No stability window was required | Do not invent one or delay closure using a universal policy hidden from the operator. |

## Coverage and recoverable failure

| ID | Scenario | Required result |
| --- | --- | --- |
| COVER-01 | Only three excerpts of a long source were selected | Record the selection and untouched scope. Do not describe the whole original as analysed. |
| COVER-02 | No route found after a bounded search | Report catalogue, snapshot, assumptions and truncation, plus missing information worth resolving. No universal impossibility claim. |
| COVER-03 | Three evidence records repeat one original assertion | Count records separately from independent sources; do not claim corroboration by count alone. |
| RECOVER-01 | A model returns an invalid draft | Preserve raw output/error and offer manual correction or an explicitly labelled alternative without auto-acceptance. |
| RECOVER-02 | Human edits the failed draft | Store a separate versioned repair/proposal with exact edits and contribution type. Do not rewrite the model result or grant factual/approval authority. |
| RECOVER-03 | Case changes while repair is being reviewed | Reject stale acceptance or require a new validated review. Retain all histories. |
| RECOVER-04 | Model unavailable but manually reviewed structure exists | Manual planning continues, labelled correctly. No silent hosted-provider switch. |
| RECOVER-05 | Handoff reports successful tests but the working source is absent | Keep the record as reported-only; reproduce from recovered exact bytes before claiming current implementation. |

## Operator evaluation, not fabricated KPIs

Test representative situations with a fixed baseline and a defined operator task. Measure decision correctness/completeness under an expert rubric, time to reach a reviewable course, time to respond correctly to a material update, correction burden, missed dependencies, false alarms and ability to explain source support. Include rejected suggestions and successful manual work. No measured benefit, study result or target percentage is supplied by this document.

Correction replay remains opt-in and case/matter-scoped; it is not permission to fine-tune a model or retrieve another client's information. A broader outcome contract or chosen-course feature must improve the existing workflow rather than require a new dashboard for each object.
