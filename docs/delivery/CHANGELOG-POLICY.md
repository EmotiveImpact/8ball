# Changelog policy applies prospectively, without rewriting history

The five exact historical entries before the Emergent Insights sprint were authored before mandatory discovery-register links, and four before mandatory emergence reviews. A cumulative integration from the earlier remote base must not require rewriting their original content.

`scripts/changelog.py` pins the five original entry IDs and canonical content hashes. Only those exact contents are exempt from the new-entry review/link rule. No date or name prefix can grant an exemption. Existing history still cannot be changed or removed relative to a comparison base. Every genuinely new entry needs an emergence review and `insight_ids`, including an explicit empty list when no discovery was identified.

Regression tests cover integration from a pre-changelog base, historical rewriting, backdated entries, future missing links and the frozen exception set. Changing this policy requires an explicit reviewed decision, never silently adding entries to the exemption list.
