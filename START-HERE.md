# Start here: 8BALL powered by ENDSTATE

[Standing build goal](docs/delivery/BUILD-GOAL.md) · [Canonical progress for both products](docs/delivery/PROGRESS.md) · [Current handoff](docs/delivery/HANDOFF.md)

Continue `feat/agency-authorisation-20261025` ([draft PR5](https://github.com/EmotiveImpact/8ball/pull/5)). Fetch remote heads and inspect the worktree before editing; preserve any newer work. Main contains the earlier PR4 consolidation, not all subsequent development.

## Latest verified work

Reviewed graph changes now atomically retain a durable local change notice. Ordered per-reader delivery and acknowledgement recheck current read permission and survive restarts. [Session and emergence review](docs/delivery/sessions/2026-10-25-endstate-outbox.md); [exact-source verification receipt](docs/evidence/endstate-outbox-native-2026-10-25.json).

Next: explicit event review UI/API and authenticated host worker dispatch. The full product remains unfinished. Model evaluation, independent review, human acceptance and production readiness retain their original gates. Only [progress.json](docs/delivery/progress.json) carries editable task statuses.

## Requirements and continuity

- [Agent rules](AGENTS.md), [next-agent prompt](docs/delivery/NEXT-AGENT-PROMPT.md), [V0.2 closeout](docs/delivery/V02-CLOSEOUT.md).
- [Master PRD](docs/PRD.md), [original V0.2 PRD](docs/reference/8BALL-V0.2-ASTRA-PRD.md), [roadmap](docs/ROADMAP.md).
- [Architecture](docs/ARCHITECTURE.md), [ENDSTATE system](docs/architecture/ENDSTATE-SYSTEM.md), [decisions](docs/decisions/).
- [Research register](docs/research/ENDSTATE-REGISTER.md), [build discoveries](docs/delivery/EMERGENCE-REGISTER.md), [changelog](CHANGELOG.md).

The [previous entry page](docs/delivery/archive/START-HERE-through-reviewed-consumption-2026-10-25.md) is preserved byte-for-byte as historical evidence. Its relative links were originally rooted here, and old branch instructions and provider observations are not current state. Do not substitute research adoption, automated checks or stored review records for required acceptance.
