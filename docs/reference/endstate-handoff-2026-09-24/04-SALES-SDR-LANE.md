# ENDSTATE Sales / SDR future product lane

## Status

Accepted future product direction.

**Not a current production application.**  
**Not permission to send autonomous outreach now.**

## Product model

One brain, multiple products.

```text
                    ENDSTATE
                       │
          ┌────────────┴────────────┐
          │                         │
       8BALL                  SALES PRODUCT
       Fixers                   Revenue teams
          │                         │
     Fixer pack                  Sales pack
          └────────────┬────────────┘
                       │
                 ENDSTATE kernel
```

ENDSTATE is the reusable technology.

8BALL is the first flagship product.

The eventual Sales/SDR product should be a different customer experience using the same core.

## What the Sales product does

An SDR, AE, account manager or authorised AI operator defines the desired revenue outcome.

Examples:

- identify relevant prospects
- qualify an opportunity
- book a meeting
- revive a dormant opportunity
- reach the economic buyer
- progress to proposal
- resolve an objection
- retain or expand an account
- close a verified sale

ENDSTATE then maintains the changing account world.

## Sales world model

Possible domain entities:

- account
- prospect
- buyer
- stakeholder
- champion
- blocker
- economic buyer
- opportunity
- product
- competitor
- meeting
- message
- call
- objection
- proposal
- budget
- deadline
- CRM record

Underneath, these map to generic ENDSTATE primitives.

## Domain mapping example

| ENDSTATE | Fixer / 8BALL | Sales |
|---|---|---|
| entity / actor | person / organisation | buyer / stakeholder / account |
| objective | desired resolution | revenue outcome |
| condition | required situation state | qualification / buying condition |
| constraint | case restriction | opt-out / channel / price / legal / policy restriction |
| action | case action | outreach / discovery / proposal / follow-up |
| evidence | source / observation | CRM / email / call / meeting / purchase evidence |
| route | resolution path | deal path |
| question | investigation | discovery question |
| decision | operator/client decision | commercial decision |
| verification | outcome proof | contract / payment / purchase / customer confirmation |

## Modes

### SDR Copilot

Human remains the sender/operator.

ENDSTATE provides who to contact, why, likely objective, research, likely objections, suggested message, next question, next action and alternative route.

### AI-assisted SDR

AI handles research, drafting, classification and proposed next steps.

Human approves external actions.

### Authorised AI SDR

A later, tightly governed mode where the AI may perform approved outreach within explicit recipient/content/channel/scope/expiry limits.

This requires separate production/security/abuse acceptance.

### Account Navigator

Maps multi-stakeholder B2B buying committees and finds routes through them.

### Pipeline Rescue

Takes a stalled deal and finds what changed, what is missing and what alternative path may exist.

### Conversation Intelligence

Converts calls/emails/meetings into reviewable state updates.

### B2C conversion

Uses the same engine but with different scale, consent, segmentation, action policy and prediction models.

## Why Sales is a strong second-domain proof

Sales produces measurable outcomes.

ENDSTATE can compare:

- predicted reply vs actual reply
- predicted objection vs actual objection
- predicted timing vs actual timing
- predicted meeting vs actual meeting
- predicted deal path vs actual deal path
- predicted route failure vs won/lost/stalled outcome

This makes it a strong place to calibrate prediction.

## Development rule

Sales must not import 8BALL-specific application code.

Target direction:

```text
sales application
    ↓
sales domain pack
    ↓
ENDSTATE contracts / kernel

8BALL application
    ↓
fixer domain pack
    ↓
ENDSTATE contracts / kernel
```

If a Sales proof requires forking the planner, that exposes a weakness in ENDSTATE's abstraction.

## What should remain shared

- state/evidence model
- actor/entity graph
- objective model
- constraints
- action prerequisites
- route generation
- decision model
- scenario isolation
- prediction interfaces
- What Changed
- event ingestion/replanning
- revision/audit semantics
- evaluation infrastructure

## What should be domain-specific

- terminology
- approved actions
- policy
- outreach restrictions
- opt-outs/consent
- CRM connectors
- success confirmation
- presentation/UI
- domain predictors
- evaluation data
- commercial workflow

## Commercial product naming

The Sales product does not need to be called 8BALL or even ENDSTATE.

The family can be:

- 8BALL, powered by ENDSTATE
- future Sales product, powered by ENDSTATE
- future Customer Ops product, powered by ENDSTATE

ENDSTATE remains the shared intellectual/engineering asset.

## Timing

Do not build the Sales application during the present V0.2 acceptance push.

Use the existing fictional Sales fixture as a reuse test.

After the current core is accepted, Sales can become the first serious second-domain proof.
