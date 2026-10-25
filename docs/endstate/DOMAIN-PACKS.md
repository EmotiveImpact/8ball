# Domain packs: internal data contract, not a product launch

8BALL owns the fixer experience. ENDSTATE remains its reusable, read-only planning
engine. `endstate.domain_packs` is an **internal source-only engineering preview**:
no new application, HTTP route, public SDK, MCP server, package release, connector
execution or runtime plugin system is introduced. Existing `/` and `/v2/` routes,
stored records, wire schemas and audit lineage are untouched.

## Contract and supported consumer

The supported preview consumer is a Python 3.12+ in-process host using the existing
`endstate.plan.v1` calculation contract and repository-pinned Pydantic. There is no
cross-version/platform support promise. The four fictional fixtures in
`tests/fixtures/domain_packs/` exercise the same native `calculate()` implementation.
The fixer fixture exports the existing **product-owned supplier playbook** unchanged;
it is not an ENDSTATE playbook or a replacement for product playbook selection.
The neutral/sales/support graphs reproduce the retained cross-domain kernel fixtures.

`DomainPack` (`endstate.domain-pack.v1`) supplies:

| Section | Meaning and boundary |
| --- | --- |
| ID/version/owner | Stable ID and numeric `major.minor.patch`, engine contract, internal-review distribution marker; owner is descriptive, not a signed credential. |
| vocabulary | Per-domain labels for shared concepts, not a renamed/forked calculation model. |
| object_mappings | Product object names mapped to declared engine concepts; no arbitrary field writes, imports or automatic entity identity. |
| catalogue | Native graph/action catalogue, policy constraints, resource templates, fictional actor templates and open verification questions. |
| confirmation_rules | Every condition's exact confirmation text and a named reviewer role. Metadata for host review, **not proof or a permission grant**. |
| prompts | Bounded text, purpose and product-selected output-contract declaration; proposal-only. No evaluation, interpolation, provider call or automatic prompt registration. |
| integrations | Opaque adapter keys, numeric adapter contract versions, supported operation labels and nonempty permission names. Host registration and explicit per-operation external permission are required. No URLs, executable paths, modules, credentials or automatic dispatch. |

Catalogue IDs must be explicit, unique within native object groups and valid under
the shared graph relations. Every sourced object has unsourced `playbook` provenance;
case references/run IDs, observations, evidence, approvals, completed actions,
answered questions, confirmed policies, actual contacts and absolute case schedules
are not reusable pack inputs. Decision-dependent catalogues are outside this v1
preview because decision records belong to case review. Template actions retain
native approval flags; a host may require stricter controls but a pack cannot grant
authority or erase an existing case's controls.

## Loading and pinning

```python
from pathlib import Path
from endstate.domain_packs import load_pack_json, pack_reference, instantiate, SnapshotSeed

# The host chooses an explicit reviewed file; the loader never discovers files.
pack = load_pack_json(Path('tests/fixtures/domain_packs/neutral.json').read_bytes())
reviewed_reference = pack_reference(pack)
snapshot = instantiate(pack, SnapshotSeed(
    snapshot_id='fictional_case', owner='Operator',
    deadline='2026-10-26T12:00:00Z', budget=10000,
))
```

Loading accepts UTF-8 JSON text/bytes only, at most 262144 bytes and depth 32.
Duplicate JSON keys, non-finite numbers, invalid Unicode, trailing data, unsupported
contract versions, unknown fields, invalid native references and unsupported pack
state fail visibly. Native graph/object count and text-length limits remain in force
(including 64 conditions/actions and eight objectives). No directory scans, YAML,
pickle, dynamic modules, network, persistent cache or on-import daemon exists.

The canonical SHA-256 reference includes **all validated fields**, including defaults,
prompt text, integration permissions and confirmation rules, not just the graph.
Object-key order/JSON whitespace do not affect identity; list order does. Boundary
functions revalidate detached nested data, including previously parsed mutable models.
A digest detects content drift; it is neither a signature nor a trusted publisher
identity, supply-chain attestation, malware scan or host approval. Store an approved
reference in host-owned review state, never accept a client-supplied hash as approval.

`instantiate()` creates a **new detached snapshot** with unknown conditions and empty
evidence, observations, approvals and completion. It cannot amend a live case, supply
a target on behalf of a client, carry approvals over or apply intended effects.
Policies begin unconfirmed; the host records their case review separately. Product
source adapters must continue to validate source spans and reviewed evidence normally.

## Read-only consumer and authority adapters

`PackConsumer(pack, authorise=..., read_snapshot=...)` is deliberately narrower than
an application service. It calculates against a frozen catalogue already present in
a host snapshot, with separately supplied live evidence and review state. It neither
loads a case from caller JSON nor overlays a pack on it. `ConsumerRequest` pins:

- `endstate.domain-consumer.v1`, the exact pack reference;
- tenant, matter and snapshot IDs;
- exact expected case revision, aware `as_of` time and native sort order.

The authenticated host, **not request JSON**, constructs `Principal(subject=...)`.
That class is a subject identifier, not an authentication mechanism. The mandatory
`authorise(principal, scope, 'plan_read')` callback must return exactly `True` based
on current object-scoped grants. It must keep its trusted grant state independent of
mutable request objects. Do not map the local/manual bearer token to agency authority.
Missing adapters and truthy non-boolean grants do not get a fallback. The mandatory
`read_snapshot(scope)` callback returns `BoundSnapshot(scope, snapshot)` from a scoped,
fresh host read, never a hidden scan or fallback matter. Scope, object ID and revision
must all match. Graph, constraints and resources must match the pinned catalogue;
only case-owned `Constraint.confirmed` may differ in constraints. This confirmation
alone does not establish the predicate's truth; source-backed authority is separate.

Authority is checked before reads/calculation and after calculation/final read. A fresh
second read detects revision changes and same-revision content changes; adapter failures
propagate, with no retry, cache publication, database writes or provider calls. Tests
cover cross-tenant/matter/object misbinding, unknown/local subject, revocation at each
read/grant phase, stale requests/results and partial read failure. A repeated explicit
read is deterministic and cannot create a duplicate action or paid request.

**This is not transactional agency isolation.** Revocation after the last check cannot
recall data already returned. The host must authorize reads in its database transaction
and recheck current permission, review/policy and exact revision in any later write,
download, publish or external send transaction. Do not turn this preview response into
a write ticket. For async work the host owns cancellation/restart fencing; this module
has no work queue, durable jobs, automatic resumes or side effects to cancel. A worker
must not publish or repeat paid calls based on a pack preview. `as_of` is a hypothetical
planning clock, not an authority clock; the grant callback must use current authority.
No HTTP exposure is requested for integration.

`PackError.code` has stable coarse failures (`permission_denied`,
`pack_reference_mismatch`, `stale_revision`, `catalogue_review_required`,
`snapshot_scope_mismatch`, `snapshot_changed_without_revision`, and JSON/version errors).
Schema failures raise native Pydantic `ValidationError`; adapter failures remain visible.
A future transport must map these to non-enumerating messages and avoid returning raw
validation inputs, pack prompts, host exceptions or existence details across scopes.

## Domain-specific evaluation and permissions

- **Fixer:** exact supplier starter/playbook and open questions; the fixture is a
  fictional hypothesis. Existing product adapters/routes keep ownership. Prompt and
  integration declarations are not wired to intelligence or ingestion automatically.
- **Neutral:** two alternatives and separate verification; actions require the native
  review/approval rules and completion never proves an intended outcome.
- **Sales:** unknown opt-out does not count as permission. An explicit reviewed false
  opt-out observation clears that guard; a later true opt-out blocks it again. Human
  action approval is still required, and an intended/accepted meeting is not a send.
- **Support:** a manual policy review **and** observed remedy authority are required;
  either alone leaves remedies blocked. Approval and verified remedy outcome remain
  separate. No refund/replacement integration is executed.

These are synthetic permission/contract evaluations, not domain-expert assessment,
legal suitability, actual inference, a sales/support application or customer evidence.
External/professional quality and host authority integration remain separate gates.

## Versioning and migrations

Use `require_reference(pack, approved_reference)` at each use. `compare_packs(old, new)`
reports identical content or `explicit_review_required`, listing changed top-level
sections and both references. Changed content requires the same pack ID and a strictly
newer numeric version, including patch-only text/prompt/policy changes. Unsupported
schema/engine versions are rejected, not best-effort coerced. A new version is not
evidence of compatibility; the tool intentionally does not infer semver compatibility.

There is **no automatic case migration**. The report never transforms snapshots,
records selected courses, answers questions, changes facts, carries approvals or
applies effects. Existing case IDs must not be remapped or silently rebound to a new
catalogue. The host keeps the old pinned bytes, reviews a proposed graph amendment at
the exact case revision, applies existing approval/course invalidation rules in one
host transaction, reruns relevant evaluations and records the decision. Ordinary case
amendments outside the frozen-catalogue preview use existing product/native contracts;
they must not evade the strict match by swapping an unreviewed pack reference.

## Distribution options, licensing and operational ownership

| Option | Decision, contracts and gate |
| --- | --- |
| Internal Python module | Implemented and source-isolated consumer-tested here. Best fit for the existing app and fictional consumers. No independent release. |
| Published Python SDK/wheel | Deferred. Integrator must explicitly include `endstate.domain_packs` in the frozen root manifest and rerun installed-wheel regressions. Current wheel includes only `endstate`, so do not claim these preview modules ship in it. Public API stability, licence and support/release approvals remain unrecorded. |
| HTTP API | Not implemented. Needs a real authenticated host, tenant/matter/object isolation, non-enumerating errors, current-grant transaction semantics, transport limits and the explicit versioned request/response contracts before exposure. No new service is justified for this in-process preview. |
| MCP | Not implemented. Any later tool must use the same version/reference/revision and current-authority contracts; tool invocation is not action permission. Discovery/resources must not leak tenant data. There is no MCP product release. |

No top-level LICENSE/LICENCE file was present at this source checkpoint. This preview
does not choose a licence or grant third-party pack redistribution, proprietary-playbook,
commercial service or support rights. Fixture text is fictional in-repository engineering material. A real
pack owner must review source permissions and record licence/operational ownership
before distribution. The pack `owner` label cannot make that legal decision.

Operational responsibilities: 8BALL owns fixer vocabulary/playbooks, source provenance,
authentication, storage, policy review and all transactions; ENDSTATE maintainers own
read-only native schemas/calculation and these bounded data contracts. Any consumer
owns adapter security, clocks, scoped reads, retention and safe error mapping. No SLO,
on-call service, security certification, professional quality, multiple-platform support
or public compatibility promise is invented. Independent release approval is **not
granted/recorded** and remains an explicit external gate (ES10-02), not a passing test.

## Verification and integration

Focused: `python -m pytest -q tests/test_domain_packs.py tests/test_endstate_kernel.py`.
The lane receipt records actual full/native/package results and retained failures;
focused reuse does not establish ES04/ES10 milestone completion.

Integration must: add the subpackage to the internal manifest if source-only use is
insufficient; adapt product-owned playbook/prompt inputs explicitly; inject authenticated
current-authority/scoped-read adapters only for an approved consumer; retain existing
case command transactions and validation; add installed-wheel and cross-lane negatives;
then reconcile lane-local fragments into canonical tracking without removing historical
evidence. There are no database migrations, new dependencies, UI mounts or shared
router/auth changes in this lane. SDK/API/MCP launch, licence/support terms and
independent release approval require separate decisions.
