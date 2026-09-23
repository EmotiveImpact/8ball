# ENDSTATE embedded kernel: contract and dependency boundary

Status: internal preview, 23 September 2026. Work items ES01-01 through ES01-04. This is the first extraction from 8BALL, not a public SDK release or another application.

## What is actually shared

`endstate/primitives.py` owns source and observation types. `contracts.py` owns graph, objective, actor, restriction and resource records plus `PlanningSnapshot`. `state.py` derives evidence-supported truth. `planner.py` owns the existing V0.2 signed planner, scheduler, readiness, questions, briefing and structural changes. `api.py` exposes a versioned, validated in-process calculation request.

8BALL imports ENDSTATE. ENDSTATE imports only Python standard-library modules and Pydantic. It does not import 8BALL, FastAPI, SQLite, HTTPX, a model runtime or named playbooks. Import and calculation do not download models, open a database or send a message.

8BALL still owns the Situation/Case product record, client/title/summary/status, storage, commands, proposal review, model adapters, specialist playbooks, API routes and interface. The preserved `eightball.v2.planner` is an adapter, not a second copy of the algorithm. The original V0.1 planner remains for its legacy wire contract and uses the shared evidence-state evaluator.

## Calculation request

Use `endstate.api.calculate(PlanRequest(...))`, or supply an equivalent Python mapping. The required fields are `snapshot` and a timezone-aware `as_of`. The contract version is `endstate.plan.v1`; the default ordering is `fewest_unknowns`. Other current orderings are `fastest`, `lowest_cost`, `fewest_external`, `least_irreversible` and `operator_risk`.

The snapshot contains an ID, owner, revision, deadline, budget, graph, evidence, observations, actors, relationships, reported events, claims, restrictions, resources, decisions, questions, completed action IDs and recorded approvals. No client name, case title, free-text situation brief, product status or fixer template is required. This removes product metadata, not all sensitive content: evidence itself can be sensitive and stays subject to the calling application's access policy.

Money values retain the existing non-negative whole-unit convention. The caller must use one consistent accounting unit. No currency conversion is performed. Durations are minutes, timestamps are timezone-aware and unspecified waits remain lower bounds.

The input is serialised to plain values, validated and copied at the calculation boundary. Nested mutable model instances are revalidated as well. A caller cannot accidentally alter its live case by modifying a returned schedule.

## Response and errors

The response identifies `contract_version`, `snapshot_id`, `revision`, `plan` and `briefing`. Plans retain the existing V0.2 result shape: candidates, evidence gaps, constraints, selected prerequisites, schedules, readiness, question impact and visible search limits. The briefing provides Now, Next, Decisions, Questions, Routes and Watch.

Invalid schema versions, naive clocks, negative values, unknown fields and dangling references raise Pydantic `ValidationError`. A well-formed but unsupported or impossible objective returns evidence gaps or constraint failures, not an invented route or guaranteed outcome. Nested output mappings remain the tested V0.2 structure; a fully typed, stabilised public result schema and distribution package are separate package-gate work.

Only `calculate` is the validated external boundary in this slice. `endstate.planner` functions are internal kernel operations over an already validated snapshot. Compatibility callers may still use them through 8BALL's adapter.

## Authority boundary

ENDSTATE calculates over supplied records. It does not authenticate the identity or evidential authority of the caller. The application must authorise, review and transactionally commit evidence, approvals and decisions before providing an authoritative snapshot. A model response must not be passed off as approved observations.

A ready action is not an executed action. A simulated intended effect is not a fact. The kernel never grants an approval, contacts a stakeholder, changes the database or declares an unobserved real-world outcome. External connectors and a durable event service remain unimplemented here.

## Compatibility and tests

The original Case and Situation JSON schemas are unchanged. Original source IDs, observations, stored snapshots, audit hashes, proposal envelopes and API response shapes remain readable. Existing imports re-export the same generic class objects. Product-specific metadata changes are added by the 8BALL adapter after the kernel explains structural changes.

`tests/test_endstate_kernel.py` compares ten frozen pre-extraction inputs, their plans, briefings, constrained plans and changes. It restores original database rows and verifies their audit and replay hashes without rewriting the records. It also runs neutral, sales and support fixtures through the same kernel, including opt-out and remedy-authority restrictions, and launches an isolated Python process with only ENDSTATE source and Pydantic.

These are small fictional reuse fixtures, not finished sales/support applications, professional-effectiveness studies or proof that arbitrary natural-language situations can be solved. The recorded Qwen graph-generation failure remains a separate blocker.

## Next boundaries to stabilise

Complete the package acceptance review, nested result schemas and distribution/compatibility tests before declaring ENDSTATE V0.1 accepted as a reusable package. Keep eventual observation commands, normalised events, incremental planning and graph compilation separate from this read-only calculation boundary. Continue building the fixer product rather than splitting into multiple commercial apps.
