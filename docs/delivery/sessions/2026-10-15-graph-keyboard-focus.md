# V0.2 graph keyboard focus

Session: Codex cloud, 15 October 2026. Tasks B02-16 / B02-20 with DOC-03/04/05 continuity. Branch `fix/v02-graph-keyboard-20261015`, base `821d9f512a70aaa602587caa4ef604021719b01f`. This base includes the previous generation-role correction and its source-bound native evidence; it does not imply a main merge or model acceptance. A clean base checkpoint was pushed before shared-file work.

## Scope and current observations

The resumed goal grants no additional inference, model-download, release or industry-application authority. Two read-only agents audited the open V0.2 scopes. The provider/evaluation/journey machinery exists; its required actual-provider and independent/human evidence remains missing. Runtime configuration contains no credential/variable bindings, relevant hosted settings are unset, and Ollama loopback returns ConnectError. The cloud runtime skill was read, including supported networking guidance. Network enforcement readiness was unknown; no outbound-access readiness was inferred from configuration.

One concrete accepted engineering gap was identified: graph repaint replaces inspector and filter controls while restoring only node/list focus. Keyboard activation of neighbourhood/clear/reset controls can therefore strand focus on the document body. This is within existing keyboard accessibility, not permission for a new screen, graph semantics change or deferred research feature.

Only `web/v2/graph-view.js` and `tests/browser_graph.py` are assigned to the implementation agent. The root agent owns continuity files. Native baseline reproduction at exact base renderer SHA-256 `1696da788859f869e1b9b31dab55c3e45ad7d49dfb8b463f87b9088f73355c92` found all four named controls leave `activeElement` on BODY after keyboard Enter. The original assertions failed, audit state stayed unchanged, no runtime errors or model calls occurred. [The raw baseline receipt](../../evidence/graph-keyboard-baseline-2026-10-15.json) is retained unchanged. The initial probe expected graph fallback for disappearing controls; the final implementation deliberately uses the always-present labelled scope selector instead. The corrected native graph suite passed **42 checks**, including four new keyboard regressions, with unchanged case audit and no runtime errors/model calls. [Focused receipt](../../evidence/graph-keyboard-focused-2026-10-15.json). Node syntax, Python compilation and diff checks passed. Cumulative acceptance follows after source stops changing. No unchanged suite is rerun merely to increase totals.

## Acceptance and remaining blockers

Preserve logical focus on a replacement control, with a deliberate focusable fallback when an action removes its own control. Cover keyboard activation and both filter-reset locations, retain type/node/list focus and the view-only audit invariants. Graph controls cannot issue case commands or alter evidence, prerequisites, approvals, selected courses or the ledger.

B02-16 remains partial pending human screen-reader and supported-browser/OS review. B02-20 remains implemented pending representative dense-case operator comprehension and broader human usability/accessibility. The other required gates still need selected/authorised real-provider execution, independent approved protocols/labels, professional source review, owner visual review and the final release decision. B02 stays 10/20; ES01 stays 5/5 internal. No status promotion from automated focus checks.

## Emergence Review

What did this sprint reveal that we had not properly seen, specified or understood before we built it? A visually equivalent graph control can be a different DOM node after repaint; focus restoration must preserve its logical role, and disappearing controls need an explicit next destination. This refines EM-053 (operator orientation across replacement UI) and EM-051 (matching source/evidence); original observations remain unchanged and review history is appended. Evidence strength depends on the native baseline/fixed receipts, not static suspicion alone. Disposition: existing_task B02-16/B02-20, no new release gate or optional feature.

| Pass | Finding / disposition |
| --- | --- |
| ER-01 | Exact change is logical keyboard focus through graph redraw; existing tasks only. |
| ER-02 | Inspector/filter replacement shares the orientation boundary already captured by EM-053. |
| ER-03 | Existing mouse-click checks can pass while keyboard focus is lost; preserve the counterexample. |
| ER-04 | The discriminating evidence is actual keyboard activation plus active-element assertions. |
| ER-05 | Bind baseline/fixed observations to their exact source; old native evidence cannot validate this fix. |
| ER-06 | Restoration must not jump to another case, a removed control or body; avoid a focus trap. |
| ER-07 | No new route, product, optional screen or research capability; no_action. |
| ER-08 | Keep the human target, actual records and read-only graph semantics unchanged. |
| ER-09 | Reconsider if restoration destination disappears or filtering leaves no records. |
| ER-10 | Automated Chromium focus is not human screen-reader or all-platform conformance. |
| ER-11 | Selected course and action authority are untouched; no_action. |
| ER-12 | Check the named controls and existing cumulative suites, not universal accessibility. |
| ER-13 | Preserve baseline failure and corrected behavior without weakening assertions. |
| ER-14 | Commit recoverable source and record tested revision, counts, hashes and transport. |
| ER-15 | Maintaining keyboard position should reduce navigation recovery work; operator value is unmeasured. |

## Handoff requirements

Record the native reproduction, focused result and cumulative source-bound acceptance before push. Regenerate/check changelog, delivery and emergence against the actual base. Commit/push only this scoped development branch; no force push, main merge, deployment or release. The final response identifies the resulting commit; the containing commit cannot contain its own SHA.

After engineering verification, next external step remains selected/authorised provider configuration and unchanged four-case generation evaluation, followed by the real-provider native journey and independent/human reviews. No secret value belongs in chat, source or the receipt.
