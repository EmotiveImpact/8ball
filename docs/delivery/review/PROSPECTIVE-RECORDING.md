# Optional offline prospective recording checks

The semantic requirements remain [plan-quality-protocol-v1](../../../evals/PLAN-QUALITY-GATE.md).
This helper checks an **optional recording format**, `v02-prospective-review.v2`.
The original [v1 form](protocol.template.json) and genuine manual studies remain
legitimate. No new mandatory acceptance gate, reviewer, numerical threshold or
approval has been selected by the building agent.

Copy [the unfilled protocol](protocol-v2.template.json) and
[dataset manifest](dataset-manifest.template.json) into a private directory
outside this public checkout. Obtain the actual owner and qualified independent
reviewer decisions before freezing the intended study. Use opaque reviewer and
qualification references; store their genuine supporting records privately.
Keep source permissions, retention, redaction and permitted transmission explicit.

Record independently authored cases, exact requested outcomes, historical
information cutoffs, specialist/risk scope, coverage and planned reviewers. Each
case references hashed source artifacts, separate exact model input and separate
expected labels. Public generation cases and the eight hinted development cases
are familiarisation material and cannot become the held-out acceptance set by
renaming them. Safety-critical cases need two distinct qualified independent
reviewers under the existing protocol. Declared qualifications and independence
still require real verification.

The arrays in the templates are intentionally empty. These entry skeletons show
the exact keys to fill; nulls/empty lists below are still blocked and are not
approved values. A configuration entry is:

```json
{
  "id": null, "provider": null, "inference_provider": null, "runtime": null,
  "model_id": null, "runtime_version": null, "prompt_version": null,
  "compiler_version": null, "schema_version": null, "parameters": {},
  "concurrency": null, "timeout_seconds": null, "ordering_policy": null,
  "permitted_data_scope": null,
  "authorized_budget": {"currency": null, "maximum_amount": null},
  "authorized_downloads": null
}
```

A dataset reviewer entry is
`{"ref": null, "qualifications_ref": null, "independence_ref": null}`.
A dataset case entry is:

```json
{
  "id": null,
  "source_artifacts": [{"ref": null, "sha256": null}],
  "model_input": {"ref": null, "sha256": null},
  "expected_labels": {"ref": null, "sha256": null},
  "exact_requested_outcome": null, "historical_information_cutoff": null,
  "risk_and_specialist_scope": null, "safety_critical": null,
  "coverage": [], "reviewer_refs": []
}
```

Use coverage names from the manifest's `required_coverage` array and reviewer
references from its roster. `case_count` is an integer matching the actual cases.
Each metric group's `thresholds` array contains supplied predicates shaped as:

```json
{"measure": null, "comparison": null, "value": null, "unit": null, "rationale": null}
```

`comparison` is one of `<`, `<=`, `==`, `>=`, `>` and `value` is a finite number,
never a boolean or a placeholder string. Fill every definition and denominator
with its intended measurement meaning, then have the genuine reviewers judge it.

The checker expects:

- A protocol referencing the final dataset manifest's bytes and SHA-256; that
  manifest references each source/input/label file's bytes and hash. All paths
  are relative to the private root and must be regular local files, without
  symlink or directory escape. No URLs are fetched.
- Explicit comparison configuration: exact requested model/provider/runtime,
  versions, parameters, concurrency, timeout, order, permitted data and authorised
  budget/downloads. No key belongs in these records. Source commit/hash fields
  are recorded identities; this helper does not attest a source checkout.
- Explicit definitions and units/denominators for all seven existing metric
  groups, with supplied finite numerical threshold predicates. Multiple
  predicates can describe a group. The owner and qualified reviewer must decide
  meaningful values for the intended use; this program invents none and cannot
  judge their scientific adequacy.
- All original zero-tolerance, denominator, no-substitution and review gates
  unchanged. Dataset/approval/freeze timestamps must be timezone aware and
  internally ordered. These timestamps are claims; the helper does not observe
  execution or prove that approval actually preceded it.

After filling and freezing the private protocol, calculate the SHA-256 of its
**final bytes** and record it externally. Do not put a self-hash into that file.
Then run (replace both placeholders with actual local values):

```sh
.venv/bin/python evals/review_readiness.py \
  --root /PRIVATE/STUDY-DIRECTORY \
  --protocol protocol.json \
  --protocol-sha256 FINAL_PROTOCOL_BYTES_SHA256
```

Output is a JSON report with JSON-pointer diagnostics. Exit 2 / `blocked` means
missing, inconsistent or unsupported recording data. Untouched templates are
blocked. Exit 0 / `mechanically_ready_for_prospective_study` means only that
these bounded recording checks passed. Every model/professional/human/model
selection/V0.2-completion flag remains false. Legacy v1 receives
`unsupported_recording_version` from this utility; that says nothing adverse
about a legitimate manual v1 study.

Limits are 2 MiB per file, 32 MiB total, 512 referenced files, 128 cases and
32 configurations. This is a local point-in-time, unsigned consistency check.
It cannot authenticate people, permission or independence, detect concealed
development exposure/paraphrased reuse, prove that labels were never supplied
to a model, or verify observed study execution/results. Exact shared input/label
bytes and known public source text can be detected; semantic label leakage
needs genuine review. A fictional complete test bundle is engineering evidence
for the checker only, never an approved study.

For actual inference use [the separate provider evidence procedure](../../v2/ACTUAL-PROVIDER-EVIDENCE.md).
Keep every failed/partial attempt and genuine reviewer judgement; record
corrections separately. Owner usability/visual review and qualified human
accessibility/platform checks remain [unperformed human work](HUMAN-ACCEPTANCE.template.md).
