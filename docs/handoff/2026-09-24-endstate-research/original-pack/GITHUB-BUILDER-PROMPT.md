# Copy/paste this into the next builder coding session

Continue the `EmotiveImpact/8ball` project from its real current state.

Before changing code, read the repository's `AGENTS.md`, `docs/PRD.md`, `docs/ROADMAP.md`, `docs/delivery/PROGRESS.md`, `docs/delivery/HANDOFF.md`, current PR #2, current branch/HEAD, CI/evidence, and the full handoff pack I am giving you. Treat the repository and exact preserved artifacts as source of truth, not chat memory.

Important recovery fact: the live remote and the newest preserved local checkpoint are not the same thing. At the last refresh on 24 September 2026, PR #2 was still open/draft/unmerged on `feat/situation-intelligence-v2` at `824ca6421ff3100e1af596347f2d1247dde8f8dc`. Later local V0.2 work exists in preserved handoffs/checklists/artifacts and must be reconciled safely rather than rebuilt or assumed to be on GitHub. Locate the newest cumulative local source/patch artifact first. Do not stack older cumulative patches, force-reset, overwrite a dirty worktree, or invent that unpublished commits exist remotely.

We are currently finishing **8BALL V0.2: Reviewed Situation Intelligence** and **ENDSTATE V0.1: Reusable Core**. Do not jump to V0.3 or rewrite the application. The latest preserved status has 8BALL V0.2 at 9/20 required subparts verified and ENDSTATE V0.1 at 4/5, with later local integration work implemented but still missing important native/model/expert acceptance. Refresh those numbers from the exact source you integrate.

Priority order:
1. safely integrate/reconcile the newest cumulative local checkpoint;
2. run complete tests, generated-document guards and native browser/CI in an authorised environment;
3. finish `B02-09` reliable reviewed graph proposals with the unchanged actual-model quality gate;
4. finish `B02-10` source/entity/deadline quality;
5. finish `B02-11` independent held-out model evaluation;
6. finish `B02-12` the genuine full actual-provider twenty-step journey;
7. finish `B02-16` accessibility/supported-environment review;
8. finish `ES01-05` reusable core acceptance;
9. keep `B02-18` blocked until every required V0.2 acceptance gate genuinely passes;
10. do not merge, deploy or mark the PR ready without explicit authority.

Preserve these invariants: unknown is not false; disputed evidence is explicit; model output is a proposal; completing work never proves its intended effect; simulations never mutate live state; approval/revision checks remain intact; no confidential client data or secrets enter the public repository; no automatic external actions are authorised by the current milestone.

New accepted product direction from 24 September 2026, to preserve but NOT use as an excuse to interrupt the present build:

- 8BALL remains the fixer application.
- ENDSTATE is the reusable engine/platform.
- Prediction is part of ENDSTATE's long-term vision.
- ENDSTATE must distinguish calibrated prediction from synthetic simulation.
- Future architecture should support investigation frontier vs execution frontier, premise/decision dependencies, decision invalidation, possible-world branching, stress testing and learning from observed outcomes.
- Establish ENDSTATE Lab as a separate research lane for Simulatrex, Wayfinder, Matt Pocock skills, chartr and related experiments. External research code is not production until licence/security/evaluation gates pass.
- A Sales/SDR application is a strong candidate for the first serious second-domain proof, but do not build that product now. The Sales application should later use `Sales app -> Sales domain pack -> ENDSTATE`, never `Sales -> 8BALL application code`.
- Keep one repository while ENDSTATE extraction is stabilising. Split only when packaging/release/ownership needs justify it.

At the end of your session, update the canonical task ledger and changelog through their generators, preserve failed evidence, create the required emergence review, push a reproducible checkpoint if authorised, and report exact branch, base, commits, files, test results, model/provider results, blockers, unpushed work, next command and merge/deployment state.

Do not merely tell me what you would build. Continue the build from the next legitimate task, and finish as much of the current acceptance work as the environment allows without weakening any gate.
