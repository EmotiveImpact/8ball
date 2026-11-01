# Verified checkpoint repair and publication

Owner request: “fix the issues”. Continue the existing unmerged branch `devin/1792969169-roadmap-integrated`, starting at `4f31c6b40141990d0863d9375f47a7ad51863dfc`. Preserve all preceding local research, native review and decision-provider work. No merge, deployment, release or further inference is authorized by this repair.

## Failures and corrections

The [installed-wheel CI failure](https://github.com/EmotiveImpact/8ball/actions/runs/40251660056/job/121344696444) is an OIDC test-clock mismatch, not an accepted authentication defect. The expiry test froze the service clock while the fixture signer kept wall time. Crossing a second boundary made a valid fixture token appear to have a future `iat`. Restore the original clock callable after the expiry assertion. Do not weaken signature, nonce, issuer, audience, expiry or current-authority checks. The corrected 29-test OIDC suite passes.

The first native review run `20261026T020659Z-5bbe5470` failed accessibility. Its retained screenshot showed an unintended original-title save. A zero-delay initial-focus timer could interrupt the first edit. Move initial focus synchronously after dialog insertion; the native regression deliberately releases delayed timers after selecting an input and verifies that focus remains there. The required blank-title/no-mutation assertions remain intact.

The old commit's separate automated review reported `errored`, not completed findings. This cannot be treated as code approval or a reason to weaken a gate. Recheck the review on the published head; retry only the failed service if needed.

## Exact verification

Before this documentation-only closeout, native run `20261026T021408Z-4e23f23f` passed on source SHA-256 `52e3af995e132ce9c70b9d98ff0aecf9c0a30388ab3695d0f424a1eb63d0b92e`: **1,945 source tests, 1,945 installed-wheel regressions and 13 native browser suites / 454 checks**. Compilation, all browser-module syntax, schemas, structural fixtures and delivery/changelog/emergence checks passed. `--inspect` confirmed exact source and evidence bytes before these documentation edits. Failed reports remain retained separately. The receipt is local engineering evidence, not an independent attestation, model-quality result or human accessibility certification.

Full native CI on the pushed head remains the final publication check. No new code or provider calls are needed just to repeat the successful transport smoke tests.

## Emergence Review

**What did this sprint reveal that we had not properly seen before?** EM-299: a security fixture using two different clocks can intermittently reject its own valid token; repair the fixture, not the security validator. EM-300: an errored review service supplies no correctness verdict. Both are existing-task/decision-record discoveries, not added product requirements. EM-298 retains the earlier focus/data-entry discovery.

- ER-01–03: preserve clock-domain and asynchronous-focus dependencies; distinguish a test failure, an application defect and absent review evidence.
- ER-04–06: the next decision-changing evidence is the published head's complete check result, not more model calls, retries of paid work or relaxed validation.
- ER-07–10: host authority and pure ENDSTATE boundaries stay unchanged; improve fixture scheduling and preserve failed receipts without promoting any acceptance status.
- ER-11–12: no selected course, evidence, approval, action or effect changes. This checkpoint covers controlled fictional software checks, not professional, model, production or real-client acceptance.
- ER-13–15: preserve both failing and passing artifacts; name the exact verified source; retain the local checkpoint rather than applying an older patch. Test counts do not establish operator value.

## Handoff

- Canonical task statuses: unchanged. B03-01 and B02-15 remain partial; B02-18 remains blocked.
- Branch/base: as above; the containing commit records the previously local implementation and repairs together.
- At preparation: local and unreleased. Verify the [PR head and checks](https://github.com/EmotiveImpact/8ball/pull/6) before claiming remote publication; the prepared patch must not be applied on top of this updated worktree.
- Next action: push this existing branch, settle CI and review without merging. Then return to bounded specialist coordination. Sonnet 5.5 inference and all independent/production gates remain separate.
