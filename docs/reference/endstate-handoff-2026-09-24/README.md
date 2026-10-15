# 8BALL + ENDSTATE complete builder handoff

**Date:** 24 September 2026  
**Repository:** `EmotiveImpact/8ball`  
**Purpose:** durable continuation pack for the next coding/build session.

This pack exists because the live GitHub branch and the newest preserved local development checkpoint are not the same thing. A new builder must not rely only on chat memory or only on the remote branch.

## The short version

- **8BALL** is the fixer-facing product.
- **ENDSTATE** is the reusable outcome engine underneath it.
- The active product milestone is **8BALL V0.2: Reviewed Situation Intelligence**.
- The active engine extraction milestone is **ENDSTATE V0.1: Reusable Core**.
- V0.2 is **not accepted yet**.
- ENDSTATE V0.1 is **not accepted yet**.
- Do **not** jump to V0.3, a Sales app, autonomous outreach, or a prediction platform before finishing the present acceptance/integration work.
- Preserve the newly accepted long-term direction: prediction, simulation, possible worlds, decision dependencies, ENDSTATE Lab and an eventual Sales/SDR product lane.
- Those new ideas expand the ceiling of ENDSTATE. They do not erase or weaken the current V0.2 gates.

## Read in this order

1. `00-START-HERE.md`
2. `01-CURRENT-STATE.md`
3. `06-DECISIONS-AND-NON-NEGOTIABLES.md`
4. `07-ROADMAP-STRATEGY.md`
5. `02-ENDSTATE-EVOLUTION-RESEARCH.md`
6. `03-ENDSTATE-LAB.md`
7. `04-SALES-SDR-LANE.md`
8. `05-BUILDER-PROMPT.md`
9. `09-RESEARCH-SOURCES.md`

Then read the preserved source-of-truth material under `source-of-truth/`.

## Source-of-truth snapshots included

- `source-of-truth/MASTER-8BALL-ENDSTATE-PRD.md`
- `source-of-truth/ORIGINAL-8BALL-V0.2-ASTRA-PRD.md`
- `source-of-truth/CURRENT-INTEGRATED-BUILD-CHECKLIST.md`
- `source-of-truth/SOURCE-CLARITY-HANDOFF.md`

The GitHub repository itself remains authoritative for whatever has actually been pushed. The local checklist and handoffs preserve later unpublished work and must be reconciled with the current remote rather than assumed to be on it.

## Continuity rule

A future session must leave the project in a state where the next session can recover:

- exact branch and commit
- exact local/unpushed state
- task IDs
- files changed
- tests run and exact results
- model/provider used, if any
- what remains failed or unverified
- next command/action
- merge/deployment state
- emergence review
- new architecture decisions

Do not allow important product thinking to exist only in chat.
