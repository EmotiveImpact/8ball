# ENDSTATE embedded package preview

ENDSTATE is the read-only calculation kernel used by 8BALL. This internal alpha
can now be built as a wheel containing only `endstate/`, its metadata and type
marker. It does not contain 8BALL, client data, a database, web UI, HTTP service,
model weights, credentials or provider adapters. Do not upload it to PyPI.

Use `endstate.api.calculate(PlanRequest(...))`. Inputs remain versioned detached
snapshots. Outputs remain ordinary dictionaries and JSON, now with complete
nested result schemas in `endstate/results.py`, a timezone-aware clock and
cross-field validation. Invalid results fail rather than being relabelled as
working plans. A conditional calculation does not grant any authority to act.

The caller supplies its own reviewed action catalogue, observations, actors,
constraints and explicit goal conditions. ENDSTATE cannot know an unobserved
real-world event or guarantee a third party's response. Graph estimates are
assumptions; search and scheduling limits are explicit in every result.

Build and smoke-test with `python scripts/build_endstate.py`. Add `--regressions` to run the complete application code suite against the temporary installed kernel as well; the consolidated acceptance runner does this automatically. This requires the
installed core dependencies, pip and setuptools 82 or newer. The command uses
`--no-index --no-deps --no-build-isolation`, so it does not download dependencies.
It tests the actual wheel in a temporary installation outside the source tree.
Only `artifacts/endstate-package/` is written. Source/module hashes and wheel
contents are checked before a local package-verification report is emitted.

This is an internal distribution preview, not a commercial SDK commitment or
public release. The 8BALL UI remains the primary product and runs normally using
`python -m eightball`. The package does not change its existing storage/audit
wire formats. Input and output schemas can be exported using
`python scripts/export_endstate_schemas.py --output artifacts/endstate-schemas`.
