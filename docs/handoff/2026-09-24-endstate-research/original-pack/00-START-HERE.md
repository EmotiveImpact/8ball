# START HERE - continuation strategy

## 1. What the next builder should do

The next builder should **continue and finish the current V0.2 / ENDSTATE V0.1 work**, not start a new product rewrite.

The immediate sequence is:

1. Refresh the real GitHub state.
2. Confirm the active PR, branch and remote head.
3. Locate the newest cumulative local source/patch checkpoint.
4. Reconcile it safely onto a fresh working branch from the current remote.
5. Run the full software, generated-document and browser regression gates.
6. Run native browser acceptance in an authorised environment.
7. Finish the real-model generation and full real-model journey gates.
8. Complete independent model-quality evaluation and accessibility review.
9. Complete `ES01-05` reusable-core acceptance.
10. Only then consider the V0.2 acceptance/release decision and movement into the next milestone.

Do **not** begin ENDSTATE 0.2 or an SDR product by abandoning unfinished V0.2 gates.

## 2. Current remote truth

At the last refresh in this handoff session:

- Repository: `EmotiveImpact/8ball`
- Pull request: `#2`
- PR title: `8BALL V0.2: reviewed situation intelligence and outcome engineering workspace`
- State: open
- Draft: true
- Merged: false
- Base: `main`
- Head branch: `feat/situation-intelligence-v2`
- Head SHA: `824ca6421ff3100e1af596347f2d1247dde8f8dc`
- Production deployment: not established
- Standalone ENDSTATE release: not established

A future session must refresh this before doing anything because it may have changed after 24 September 2026.

## 3. Newest preserved local truth

The later integrated checklist records a local/unpublished continuation based on the remote ancestor above.

It reports:

- Governance 1.1: 6/6 scoped items verified
- 8BALL V0.1: 3/3 scoped items verified
- 8BALL V0.2: 9/20 required subparts verified, milestone not accepted
- ENDSTATE V0.1: 4/5 required subparts verified, milestone not accepted
- ENDSTATE V0.2: not started as a required milestone
- later local integration branch metadata: `work/acceptance/integration-alpha7`
- 855 code tests passed in the local integration checkpoint
- the internal ENDSTATE wheel/source/schema compatibility rerun passed locally
- 344 browser checks across ten suites passed using an explicit ASGI bridge
- native loopback navigation remained environment/policy blocked
- actual-provider/model acceptance remained incomplete
- independent expert/model-quality acceptance remained incomplete

Those facts describe a preserved local checkpoint, **not code that is necessarily on GitHub**.

## 4. Very important remote/local discrepancy

The remote branch is behind several preserved local checkpoints.

The preserved local development history includes work described as:

- hosted/model-provider transport improvements
- black operator visual system
- relationship/Connections explorer
- Plan Studio
- controlled analysis jobs
- immutable product changelog
- Source Desk
- mandatory emergence review
- Emergent Insights
- Source Clarity
- Plan Review / quality-review infrastructure
- ENDSTATE package/result compatibility work
- broader integration/acceptance tooling

Do not rebuild these from memory if a cumulative source artifact exists.

Do not stack old cumulative patches on top of a newer cumulative patch.

Do not force-reset the remote branch.

## 5. Which version are we actually building?

**8BALL:** V0.2, Reviewed Situation Intelligence.  
**ENDSTATE:** V0.1, Reusable Core.

The application may carry alpha build labels internally, but those alpha labels do not mean V0.2 is accepted or released.

The next formal 8BALL milestone is V0.3, Secure Agency Pilot. Do not move there until V0.2's release/acceptance gate is honestly resolved.

The next formal ENDSTATE milestone is V0.2, Event-Driven Replanning. Do not describe it as built simply because some related local experiments exist.

## 6. Strategy for the new research

The Simulatrex / Wayfinder / skills / chartr research should **not interrupt the current build**.

It should do two things now:

1. become durable product/architecture context so it is not lost; and
2. establish an ENDSTATE Lab research lane that can run beside production development.

Production changes from that research should enter only through explicit decisions and version gates.

## 7. What the next builder must not do

- Do not rewrite the app from scratch.
- Do not weaken the real-model acceptance gate.
- Do not make synthetic simulation output equal to evidence.
- Do not mark a generated action complete merely because its intended effect sounds plausible.
- Do not merge `main`, mark PR #2 ready, or deploy unless explicitly authorised.
- Do not claim local bridge browser results are native acceptance.
- Do not claim a public ENDSTATE SDK exists.
- Do not start autonomous sales outreach.
- Do not bake `client`, `case`, `fixer` or sales-only semantics into the ENDSTATE kernel.
- Do not copy external research code into production without licence, security and fit review.

## 8. What success looks like for the next coding session

The next session should preferably produce one of these concrete outcomes:

**Best outcome:** safely integrate the preserved cumulative local V0.2 checkpoint, push an exact reproducible branch/commit, run authorised native CI, and update the canonical ledger.

**If integration already happened elsewhere:** refresh the repo, reconcile, then take the next unblocked required task from the canonical ledger.

**If provider/native environment blocks acceptance:** preserve the block honestly and complete the next bounded task that does not require pretending the blocked gate passed.
