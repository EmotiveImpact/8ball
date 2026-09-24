# Recover the unpublished cumulative code

This handoff branch contains durable context and strategy. The newest unpublished code archive bytes remain preserved separately in the project Library and are not claimed to be on GitHub.

## Primary recovery artifacts

1. `8BALL-Integrated-Build-Developer-Pack.zip`
   - Library path: `/8Ball/8BALL-Integrated-Build-Developer-Pack.zip`
   - Project file ID observed 24 September 2026: `file_00000000d0e88246b8bfa2c71ad4a369`
   - Preferred complete developer handoff for the latest preserved integrated local checkpoint.

2. `8BALL-Integrated-Build-Source.zip`
   - Library path: `/8Ball/8BALL-Integrated-Build-Source.zip`
   - Project file ID observed 24 September 2026: `file_00000000e5208210932525e38c5be643`
   - Latest preserved cumulative source archive found during this handoff.

3. `8BALL-ENDSTATE-Vision-Strengthening-Pack.zip`
   - Library path: `/8Ball/8BALL-ENDSTATE-Vision-Strengthening-Pack.zip`
   - Project file ID observed 24 September 2026: `file_0000000027e4820ea5a693ca6f3eff03`
   - Historical strategic/vision material. The 24 September ENDSTATE research handoff supersedes it where they overlap.

Fallback earlier source: `8BALL-Source-Clarity-Source.zip`, Project file ID `file_00000000244882468a8c1fdb8d0e9e9e`.

## Integration rule

Refresh GitHub first. Prefer the newest cumulative integrated package. Inspect its internal handoff and hashes. Never stack cumulative packages, overwrite a dirty tree, force-reset another session's work, or claim an unpublished local commit exists remotely. Run the full regression and acceptance gates after integration.

The last remotely observed V0.2 head during creation of this handoff was `824ca6421ff3100e1af596347f2d1247dde8f8dc` on `feat/situation-intelligence-v2`, PR #2. Treat that as a dated checkpoint only.
