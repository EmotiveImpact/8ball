# Decision 0003: a relationship explorer alongside the outcome planner

Date: 23 September 2026. Owner direction: build an Obsidian-like graph and continue the black visual refinement within 8BALL.

## Decision

Use three views of one case: **Connections** for exploration, **Outcome flow** for directed dependency membership and **Records** for search, keyboard use and an alternative to the canvas. The existing Situation Room, route calculation, evidence review, approvals, scenario isolation and command boundary stay intact. This is product UI, not a change to ENDSTATE state semantics.

The design borrows an interaction idea, not Obsidian code: select a record, highlight its immediate links and restrict to a one-, two- or three-link neighbourhood. Obsidian's official graph documentation describes global/local graphs and neighbour depth: https://obsidian.md/help/plugins/graph . No Obsidian plugin, account or service is integrated.

## Authority boundary

Only explicit case references create connections. A source quotation is a recorded assertion; an intended action effect is not an observation. Historical support is labelled and hidden by default. Layout proximity and node size do not express authority, causal strength or success probability. Moving a node only changes an in-memory coordinate. There are no graph-generated commands or inference requests.

## Validation scope

B02-20 covers projection, exploration, filtering, camera controls, pinning, source-aware inspection and read-only behaviour. B02-13 remains the separate guided nested editor task. B02-16 still requires full screen-reader and supported-platform review. Native CI, a real-model journey and production release are not implied by local browser rendering.
