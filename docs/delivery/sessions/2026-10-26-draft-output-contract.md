# Draft instructions v4 — stricter guidance, unchanged acceptance

## Scope and source

Existing B02-11 follow-up from pushed `52e5c0d`, on
`devin/1792969169-roadmap-integrated`. The original five-request diagnostic and
the second seven-request diagnostic remain permanently failed/partial. Neither
is resumed, repaired or recounted as a success.

`endstate.compilation.PROMPT_VERSION` becomes `endstate.draft.prompts.v4`.
Both frame and route prompts now explicitly require one bare JSON object without
Markdown fences/commentary, respect for every schema `maxLength` even after
review, and shorter generated prose without altering exact quotations or the
human target. The same instructions reach initial and revision calls.

The prompts also clarify an existing planning requirement: an operational
outcome needs its enabling work and reviewable records before verification.
Requests, filing locations or a recorded response must not stand in for the
work, consent or safety clearance. Unknown/refusal remains distinct from a
satisfied prerequisite. No operation completion attests an intended effect.

No schema, 180-character limit, strict JSON parser, source-coverage rule,
compiler wiring, retry/fallback policy, human authority or provider profile was
changed. This is stronger guidance, not a guarantee the model will obey or an
independent judgement that any generated route is sufficient.

## Verification

**477 focused checks passed**, covering compilation, coordination, frozen
evaluation and both compatible/native transports. Compilation and whitespace
checks passed. One existing Starlette/AnyIO deprecation warning, no skipped test.

New boundary tests preserve 180-character acceptance and 181-character rejection
for readiness and success confirmations at both initial and revision stages.
Controlled offline replay of the retained assistant outputs still rejects the
actual overlength Sonnet revision and fenced Opus frame, with no extra stage or
silent replacement. It is not another inference run. Original Sonnet proposal,
panel bindings and every answer survive the replay unchanged.

Full source-bound native and installed-wheel verification is next. No inference,
new price check or billing lookup has occurred in this change. No model-quality,
forecasting, operator-benefit, production, merge/deployment/release gate passes.
B02-11 stays partial and the dedicated coordinated-result UI remains outstanding.

## Emergence Review

EM-335/336/337 are refined, not replaced: complete challenges do not guarantee a
valid revision; prompt-only compliance is per-request; and positive choice
labels do not establish operational completeness. The engineering boundary is
tested, but better output rates and better plans remain unverified. A future
diagnostic needs a new source/protocol freeze and must retain every failure.

ER-01–15 reviewed: no additional scope promoted. Keep unprocessed/failed stages,
minority answers, provenance, human-selected course and recovery attribution
visible. More instructions can increase verbosity or compete for attention;
controlled prompt-presence checks cannot quantify that risk. The fixer still
needs source-linked review and cannot infer a safe action or achieved outcome
from either a polished route or this software verification.

## Handoff

Touched runtime: compilation prompts only; tests and canonical delivery records
alongside. Local uncommitted at this checkpoint; next commit, native/package
acceptance, source-bound archive and additive publication. No source edits during
acceptance or any later frozen inference run. No merge/deployment/release.
