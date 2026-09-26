# Pre-extraction compatibility fixture

`pre_extraction.json.xz` is an XZ-compressed UTF-8 JSON record captured from the unmodified source at remote commit `5e2098e9cb12251592eb3889ce7926798484699d`, tree `ce918eea4404101e6cbb502cf81a08c316e4dda9`, before extracting ENDSTATE. The local source was compared with that Git tree before capture. All input material is fictional.

Archive SHA-256: `9f28c27566811ab94a5e5388f9936b199cbc7d130845e2d93473ae9bd8cd6ad5`.

The fixed calculation time is `2026-09-23T18:00:00+00:00`. The record contains ten V0.2 cases, original wire-schema hashes, expected plan/briefing/budget-change hashes, a legacy case and original database rows plus expected audit hashes. Generated IDs and timestamps in those records are frozen as captured.

Only explicitly set-derived arrays (`ready`, `approvals`, `changed_routes`) are sorted when comparing result hashes. Route order, selected dependencies, schedule order, costs, state and timing remain significant. Database rows must remain byte-for-byte unchanged after reading them.

To inspect the data without another dependency:

```sh
python -c "import json,lzma,pathlib; p=pathlib.Path('tests/fixtures/endstate/pre_extraction.json.xz'); print(json.dumps(json.loads(lzma.decompress(p.read_bytes())), indent=2))"
```

This is baseline evidence, not output to regenerate automatically until tests pass. A deliberate semantics change requires a separate reviewed decision and new evidence; retain this pre-extraction record.
