# Recover the unpublished cumulative code

This handoff ZIP contains the durable context, strategy and source-of-truth documents. It does **not** contain the newest unpublished code archive bytes.

The actual cumulative code packages are preserved separately in the project Library. Use the newest cumulative package first and do not stack earlier cumulative patches/packages on top of it.

## Primary code recovery artifacts

### 1. Integrated developer pack

- Name: `8BALL-Integrated-Build-Developer-Pack.zip`
- Library path: `/8Ball/8BALL-Integrated-Build-Developer-Pack.zip`
- Project file ID observed 24 September 2026: `file_00000000d0e88246b8bfa2c71ad4a369`
- Library file ID: `libfile_31f7ae9671888191ab96bd627cb9d882`
- Size observed: 11,445,419 bytes
- Modified: 24 September 2026 13:07 UTC
- Purpose: preferred full developer handoff for the latest preserved integrated local checkpoint.

### 2. Integrated source archive

- Name: `8BALL-Integrated-Build-Source.zip`
- Library path: `/8Ball/8BALL-Integrated-Build-Source.zip`
- Project file ID observed 24 September 2026: `file_00000000e5208210932525e38c5be643`
- Library file ID: `libfile_111bab4d307481918f63bd93af6c21b5`
- Size observed: 736,259 bytes
- Modified: 24 September 2026 05:52 UTC
- Purpose: latest preserved cumulative source archive found during this handoff.

### 3. Vision strengthening pack

- Name: `8BALL-ENDSTATE-Vision-Strengthening-Pack.zip`
- Library path: `/8Ball/8BALL-ENDSTATE-Vision-Strengthening-Pack.zip`
- Project file ID observed 24 September 2026: `file_0000000027e4820ea5a693ca6f3eff03`
- Library file ID: `libfile_667ff74a43048191bb135c090e2fdf76`
- Size observed: 574,780 bytes
- Modified: 24 September 2026 16:05 UTC
- Purpose: prior strategic/vision strengthening material. This new handoff supersedes it where the two overlap, but preserve it as historical context.

## Earlier fallback checkpoint

If the integrated packages cannot be accessed, the preceding Source Clarity source archive is:

- `8BALL-Source-Clarity-Source.zip`
- Library path: `/8BALL-Source-Clarity-Source.zip`
- Project file ID: `file_00000000244882468a8c1fdb8d0e9e9e`
- Size observed: 630,111 bytes

Its exact handoff is included in `source-of-truth/SOURCE-CLARITY-HANDOFF.md`.

## Integration rule

1. Refresh GitHub first.
2. Check the current remote head and whether another coding session has pushed newer work.
3. Prefer the newest cumulative integrated source/developer pack.
4. Inspect its internal handoff and hashes before application.
5. Never apply two cumulative packages to the same tree.
6. Preserve dirty/uncommitted work and reconcile normally.
7. Run the full regression and acceptance gates after integration.
8. Only record a pushed commit after observing that the push succeeded.

The last remotely observed V0.2 head during creation of this pack was `824ca6421ff3100e1af596347f2d1247dde8f8dc` on `feat/situation-intelligence-v2`, PR #2. Treat that as a dated checkpoint, not a permanent truth.
