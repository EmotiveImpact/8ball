# 8BALL V0.2: relationship explorer

## Implemented in the local developer checkpoint

The existing Situation Map now offers Connections, Outcome flow and Records. It reads the current case snapshot and calculated plan. A node maps to a real typed object; an edge maps to a declared relationship, prerequisite, guard, intended effect, objective criterion, provenance quotation, observation, decision, question, restriction or resource reference. No text similarity or visual proximity invents a relationship.

`web/v2/graph-model.js` provides pure projection, filtering and bounded layout. `graph-view.js` provides the read-only interface. Neither module calls the API, imports the store or issues commands. The application mounts the explorer after rendering and clears its memory on workspace lock. Graph state is scoped by case ID and is not persisted into local storage or exported evidence.

## Interaction

Connections uses a bounded force-style layout with label separation. It settles immediately rather than running a perpetual animated simulation. Select a node to highlight immediate links and inspect its record. Focus neighbourhood narrows the graph; the depth selector expands up to three links. Search filters actual labels and recorded descriptions. Type controls show or hide categories without creating shortcut edges through hidden nodes.

Drag the background to pan. Drag a node in Connections to pin its display position. Unpin, reset layout, zoom buttons, plus/minus, arrow keys and Home are supported. Modified mouse-wheel zoom avoids trapping ordinary page scrolling. The directed flow uses component-aware layering so cycles do not recurse indefinitely. It begins at a readable scale; Fit can show the full layout. Arrow connections show dependency membership, not an invented all-of requirement: exact signed AND/OR expressions remain visible in the inspector and full action record.

Records is a full alternative to the canvas with labelled, focusable buttons. The inspector links to existing condition, actor, action and evidence detail controls. Any subsequent change still uses the original reviewed command mechanism. A read-only, single-file fictional preview can be generated with `python scripts/design_preview.py`.

## History, uncertainty and safety

Active support is distinguished from superseded or retracted evidence. Historical links can be explicitly enabled; they are dashed and labelled as historical in connection lists. Referenced unreviewed source quotations are not treated as attestations. Recorded decisions or answers whose supporting source has been retracted are labelled as needing review. Unknown conditions remain unknown and intended action effects remain labelled as intended.

The view displays the case revision, not a claim to live inbox synchronisation. It does not create, alter or remove prerequisites. It does not prove actor authority, source truth, influence or causal effects. All labels and excerpts are escaped before rendering. Pinned coordinates are display-only. Switching cases and locking the workspace cannot expose the preceding case's rendered records.

## Scale and limitations

The force-style layout is bounded to 120 visible nodes. Larger sets use a disclosed spaced grid with the same graph links; filtering, neighbourhoods and the Records list remain available. This is not a validated 10,000-node WebGL graph. Dense cases should be narrowed rather than implying that a giant hairball is useful. Touch uses pointer events; multi-touch pinch zoom and a full mobile usability study remain future work. Keyboard interaction and reduced-motion behaviour are covered locally, not a complete screen-reader audit.

## Tests

Run `python -m pytest -q`, `node --check` for all browser modules and all four browser suites: `browser_smoke.py`, `browser_v2.py`, `browser_development.py`, and `browser_graph.py`. The graph tests inspect projection integrity, namespaces, explicit signed links, history, type/search/local scopes, cycle safety, deterministic positions, pins, bounded fallback, input immutability and safe labels. Browser tests cover selection, focus depth, camera controls, pinning, exact logic, old record detail, isolated cases, history, keyboard focus, mobile widths, escaping and unchanged audit state.

Local native navigation returned `ERR_BLOCKED_BY_ADMINISTRATOR`; that policy was not changed. The explicitly named ASGI bridge renders the actual application code against the real API and SQLite, but does not verify native browser HTTP, CSP enforcement, native file navigation or downloads. No live model was invoked. Keep the current code unpublished until a normal authorised integration and native CI succeed.
