# 0006: Consolidate the current development build into main

Date: 15 October 2026. Status: owner-authorized integration decision, not V0.2 acceptance or deployment.

## Decision and authority

The owner instructed: “When are you going to merge everything so we get a fully picture of what we have built do it”. This supersedes the earlier no-main-merge instruction for this one consolidation. Prepare and verify the combined current application and documentation, then update main without rewriting remote history. Preserve the existing acceptance requirements and unfinished task statuses.

Integrate the latest application checkpoint `486c85ec07a05c7af8b30b142d2ad19faf402e25` (which contains all preceding active feature/fix branches) and documentation `0ee5834c0745640369f5a538b770c346f234232a`. Restore the separate historical research directory from `a8ecd9c833e1d929d6b2152cd80b51ac173967e8` byte-for-byte. Retain archival/operations refs; their older runtime trees and publication wrappers are not additional current application features.

Resolve canonical history by stable ID, preserving all entries and append-only discovery decisions. Keep the current application task scopes/statuses/evidence. Provide one current entry point and build overview. Do not replace the newer fixes with the older application or documentation snapshot.

## Boundaries

- Main will contain a consolidated **development alpha**, version `0.2.0-alpha.8`, with ENDSTATE internal `0.1.0a2`.
- B02 remains 10/20 required scopes verified and ES01 remains 5/5 internal scopes. Branch integration does not pass real-model, independent professional or human acceptance.
- No deployment, release tag, model download, paid inference, deferred research implementation or another industry application is authorized by this decision.
- Push the integration branch and main only. Their configured validation is model-free. Updating the older feature branch would trigger automatic model experiments, so that branch is retained unchanged.
- No force push, branch deletion or rewriting of original PRDs, frozen generation fixtures, historical evidence or discovery observations.

## Verification and recovery

Check runtime bytes against the latest application parent, original PRD/fixture hashes, both research variants, both parents' changelog/discovery histories and canonical task scope/status preservation. Run the model-free cumulative native acceptance and inspect its source/artifact report before publishing. Preserve the integration branch and previous parents for recovery.

The historical documentation-only `verify_consolidation.py` and `context-manifest.json` remain unchanged. Their frozen older application/progress assumptions do not describe this newer integrated build. A separate integration receipt records actual current-source checks and native evidence.
