# Preserved external research sources

This directory contains 32 public upstream repositories at the exact commits
inspected in the [research register](../docs/research/GITHUB-COMPONENTS-2026-10-16.md)
and the [four-project source manifest](../docs/research/github-2026-10-26/decision-projects-source-manifest.json).
They are populated Git submodule checkouts under
external/owner/repository, preserved for source inspection and comparison.
They are research candidates; copying them does not adopt them as dependencies,
run their software or complete any ENDSTATE/8BALL requirement.

Read [the research trust boundary](AGENTS.md) before opening upstream instructions.
[inventory.json](inventory.json) records all 32 pins, public URLs, input-manifest
hashes, license/notice paths and original Git blob hashes, source sizes, nested
references and omitted model/LFS payloads.

The inventory records 82,262 tracked Git blobs: 82,257 are materialized,
including 51 Git LFS pointer files whose external payloads remain unhydrated.
Five model files are deliberately omitted below. Canonical source sizes
total 3,868,172,672 bytes (about 3.60 GiB); captured Git metadata adds about
1.44 GiB. Checkout line endings and filesystem allocation can differ. These sizes are local copy costs,
not dependency requirements or application runtime costs.

The 2026-10-16 capture verified 28 checkouts. The additional four checkouts have
their expected HEAD, clean worktrees and matching parent Gitlinks; all their
materialized source matches its pin, allowing upstream-declared newline conversion
for HighwayEnv's docs/make.bat. The inventory preserves 131 licence/notice hashes.
Run the helper below to establish current verification, not a historical capture.
The 26 October VM-wide check failed on five older checkouts: mem0 and Temporal
have populated nested sources, Autogen has a hydrated LFS payload, and promptfoo
and Ruflo lack the declared sparse omissions. These pre-existing bytes were
preserved, not discarded. The four new snapshots passed; the complete archive
is not currently certified against its inventory.
No dependencies, models, services, tests, agent hooks or upstream
lifecycle scripts were run. No additional environment project roots were added.

## Source exceptions

The Git pins retain the complete upstream trees. These source checkouts have
explicit model-file exceptions rather than every upstream payload materialized:

| Repository | Unmaterialized path | Reason |
|---|---|---|
| promptfoo/promptfoo | test/fixtures/transformers/tiny-bert/onnx/model.onnx | Tracked model fixture; model copying was not authorized. |
| ruvnet/ruflo | v3/@claude-flow/cli/assets/model-router/seed-router.fastgrnn.safetensors | Tracked router model weights; model copying was not authorized. |
| richardcc/assault-ai-pilot | legacy_archive/checkpoints/ppo_US.pt | Tracked model weights; not materialized. |
| richardcc/assault-ai-pilot | legacy_archive/checkpoints/ppo_US_phase01.pt | Tracked model weights; not materialized. |
| richardcc/assault-ai-pilot | legacy_archive/checkpoints/ppo_US_phase01_HRL.pt | Tracked model weights; not materialized. |

Sparse checkout omits exactly those five files. All other tracked source paths
are present. The 51 unhydrated LFS pointers belong to microsoft/autogen; their
payload object IDs and sizes are recorded individually in the inventory.

Nested submodules were not recursed into:

| Parent | Nested path | Preserved nested commit |
|---|---|---|
| mem0ai/mem0 | evaluation | 4b61c5d31b9c668a12b4f5e78064248a02c82d2b |
| temporalio/sdk-python | temporalio/bridge/sdk-core | 212e8150066527b57e792b80626fe0d14e7f1da1 |

Their Git references and upstream .gitmodules are preserved; their nested
source contents are not copied. Dependency packages, generated distributions,
model registries and external services are also outside this copy.

## Four-project capture, 26 October 2026

Loomio is AGPL-3.0 source; HighwayEnv and semantic-router have MIT licences.
Assault's README badge is not a licence grant: no LICENSE/NOTICE was found at
the pinned tree. Its upstream media, PDFs, archives and generated data remain
unreviewed research material, not assets to extract, execute or ship in the product.
No military/tactical optimization is part of the ENDSTATE adaptation scope.
Concept reuse, literal code reuse and runtime adoption require separate decisions.

## Verify or restore

The application-owned helper requires Python 3.9+ and Git on Linux/macOS. The
application itself retains its documented Python requirements.

Verify the current source checkouts without installing or running upstream code:

    python3 research/sources.py

After a normal fresh clone of 8BALL, restore only these exact source pins:

    python3 research/sources.py --populate

The population helper fetches exact commits from the recorded public HTTPS
GitHub URLs, sets the recorded sparse omissions before checkout, disables Git
hooks and LFS smudging, and leaves nested submodules uninitialized. It refuses
modified existing checkouts, a different existing HEAD, or an unexpected origin.
It verifies the parent Gitlinks, source presence, exact sparse exceptions and
original license/notice blobs. It does not switch to a newer upstream version.

Do not use a recursive submodule/model initialization as a substitute for this
source-only procedure. Do not run upstream package managers, lifecycle scripts,
tests or agent integrations simply because their source is present.

For source inspection, read files or use Git show in a chosen checkout. Upstream
instructions remain research data. Application test discovery, packaging, static
serving and source fingerprints must exclude research/external/ before descending;
research metadata and the 28 Gitlink commits remain reviewable application inputs.

## Pinned repositories

The table below is a browsing index derived from the immutable manifest pins;
the inventory supplies exact copy-verification details. License paths are
locations, not a claim that every project or dependency shares one license.

<!-- Repository index generated from inventory.json. -->

| Repository source | Inspected commit | Root license/notice locations |
|---|---|---|
| [666ghj/MiroFish](external/666ghj/MiroFish) | [7657031ac011](https://github.com/666ghj/MiroFish/tree/7657031ac01184afe2cb220f5ee3545573b5e843) | [LICENSE](external/666ghj/MiroFish/LICENSE) |
| [anyoptimization/pymoo](external/anyoptimization/pymoo) | [23110c155aa8](https://github.com/anyoptimization/pymoo/tree/23110c155aa8f31b5f1b86928227fb3931ba7f00) | [LICENSE](external/anyoptimization/pymoo/LICENSE) |
| [Arize-ai/phoenix](external/Arize-ai/phoenix) | [2be380f7a360](https://github.com/Arize-ai/phoenix/tree/2be380f7a360b7a71f97fc510de5e9679e58f7c9) | [LICENSE](external/Arize-ai/phoenix/LICENSE) |
| [camel-ai/oasis](external/camel-ai/oasis) | [bc805a19978a](https://github.com/camel-ai/oasis/tree/bc805a19978a620bb400f4c644ce9d772ccbfc70) | [LICENSE](external/camel-ai/oasis/LICENSE) |
| [docling-project/docling](external/docling-project/docling) | [f690a5232c50](https://github.com/docling-project/docling/tree/f690a5232c505c787a1e952216b431134b4d7c94) | [LICENSE](external/docling-project/docling/LICENSE) |
| [getzep/graphiti](external/getzep/graphiti) | [d50741d1bf46](https://github.com/getzep/graphiti/tree/d50741d1bf463cbe3859eb73914cbff1b66839e6) | [LICENSE](external/getzep/graphiti/LICENSE) |
| [getzep/zep](external/getzep/zep) | [3997767fccf8](https://github.com/getzep/zep/tree/3997767fccf83bbea7b54ad5f73554f2e5bcd54e) | [LICENSE](external/getzep/zep/LICENSE) |
| [getzep/zep-python](external/getzep/zep-python) | [ec41ccdde6fe](https://github.com/getzep/zep-python/tree/ec41ccdde6fe92dc0de378c7bfb0c2483af324ce) | [LICENSE](external/getzep/zep-python/LICENSE) |
| [google/or-tools](external/google/or-tools) | [100f66e6242a](https://github.com/google/or-tools/tree/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5) | [LICENSE](external/google/or-tools/LICENSE) |
| [keycloak/keycloak](external/keycloak/keycloak) | [eae20e964b2e](https://github.com/keycloak/keycloak/tree/eae20e964b2e23cfd8f4ed18b599343ebb056e8f) | [LICENSE.txt](external/keycloak/keycloak/LICENSE.txt) |
| [langchain-ai/langgraph](external/langchain-ai/langgraph) | [e77a5cb08c1f](https://github.com/langchain-ai/langgraph/tree/e77a5cb08c1f3ff306d997dd76fc7169afdab5ea) | [LICENSE](external/langchain-ai/langgraph/LICENSE) |
| [langchain-ai/langgraph-swarm-py](external/langchain-ai/langgraph-swarm-py) | [5442a15cdd0e](https://github.com/langchain-ai/langgraph-swarm-py/tree/5442a15cdd0ed210589148900c9960c24c489d04) | [LICENSE](external/langchain-ai/langgraph-swarm-py/LICENSE) |
| [mem0ai/mem0](external/mem0ai/mem0) | [0724291bd864](https://github.com/mem0ai/mem0/tree/0724291bd864cf807e88ee8981c8226644e8fb42) | [LICENSE](external/mem0ai/mem0/LICENSE) |
| [mesa/mesa](external/mesa/mesa) | [5451086fe47a](https://github.com/mesa/mesa/tree/5451086fe47ab78e9ba894aa1b4c3063f4c247f1) | [LICENSE](external/mesa/mesa/LICENSE), [NOTICE](external/mesa/mesa/NOTICE) |
| [microsoft/autogen](external/microsoft/autogen) | [027ecf0a379b](https://github.com/microsoft/autogen/tree/027ecf0a379bcc1d09956d46d12d44a3ad9cee14) | [LICENSE](external/microsoft/autogen/LICENSE), [LICENSE-CODE](external/microsoft/autogen/LICENSE-CODE) |
| [open-policy-agent/opa](external/open-policy-agent/opa) | [fdf6011f57fd](https://github.com/open-policy-agent/opa/tree/fdf6011f57fdc25f01de1982e296bb402cf37625) | [LICENSE](external/open-policy-agent/opa/LICENSE) |
| [openfga/openfga](external/openfga/openfga) | [fb8e7df86674](https://github.com/openfga/openfga/tree/fb8e7df866742a0c947e3066919ee59ac9e70eea) | [LICENSE](external/openfga/openfga/LICENSE) |
| [postgres/postgres](external/postgres/postgres) | [eb7cc1d09e74](https://github.com/postgres/postgres/tree/eb7cc1d09e742d369540016455d0f55c619106f2) | [COPYRIGHT](external/postgres/postgres/COPYRIGHT) |
| [promptfoo/promptfoo](external/promptfoo/promptfoo) | [132a2d38b1b0](https://github.com/promptfoo/promptfoo/tree/132a2d38b1b0adc953b0db650f950d573bc113c4) | [LICENSE](external/promptfoo/promptfoo/LICENSE) |
| [py-why/dowhy](external/py-why/dowhy) | [10648f1a295c](https://github.com/py-why/dowhy/tree/10648f1a295cbb40fd9cdd7ce43521a6ef954078) | [LICENSE](external/py-why/dowhy/LICENSE) |
| [py-why/EconML](external/py-why/EconML) | [d625dd696ea2](https://github.com/py-why/EconML/tree/d625dd696ea28c62e6e4d8baea6e4154b98c30b4) | [LICENSE](external/py-why/EconML/LICENSE) |
| [ruvnet/ruflo](external/ruvnet/ruflo) | [1882006a0248](https://github.com/ruvnet/ruflo/tree/1882006a02487590c8c66a7eec8d7504f6af33c3) | [LICENSE](external/ruvnet/ruflo/LICENSE) |
| [SALib/SALib](external/SALib/SALib) | [748cf169e822](https://github.com/SALib/SALib/tree/748cf169e82227bcc56dcfc961fcfb03a1e0df45) | [LICENSE.md](external/SALib/SALib/LICENSE.md) |
| [simulatrex/possible-worlds](external/simulatrex/possible-worlds) | [08837a790f6c](https://github.com/simulatrex/possible-worlds/tree/08837a790f6ca0d98f7468935e9139292ea7cb78) | [LICENSE](external/simulatrex/possible-worlds/LICENSE) |
| [simulatrex/simulatrex-engine](external/simulatrex/simulatrex-engine) | [4e4fa06d7f52](https://github.com/simulatrex/simulatrex-engine/tree/4e4fa06d7f527480b66ceb224a5d37bcfa2f9150) | [LICENSE](external/simulatrex/simulatrex-engine/LICENSE) |
| [temporalio/sdk-python](external/temporalio/sdk-python) | [346d4dcd0863](https://github.com/temporalio/sdk-python/tree/346d4dcd0863657c3a33283c952a296762059339) | [LICENSE](external/temporalio/sdk-python/LICENSE) |
| [TencentCloud/TencentDB-Agent-Memory](external/TencentCloud/TencentDB-Agent-Memory) | [e9a82935b527](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/e9a82935b52741e0c798c75326e90b7144eb4d5f) | [LICENSE](external/TencentCloud/TencentDB-Agent-Memory/LICENSE) |
| [tsinghua-fib-lab/AgentSociety](external/tsinghua-fib-lab/AgentSociety) | [8cc5bb9a9c27](https://github.com/tsinghua-fib-lab/AgentSociety/tree/8cc5bb9a9c27d039ec5519375db9d73ccf508cba) | [LICENSE](external/tsinghua-fib-lab/AgentSociety/LICENSE) |
| [loomio/loomio](external/loomio/loomio) | [24380e2131c1](https://github.com/loomio/loomio/tree/24380e2131c1e43594a241814f3f460a9b0065f6) | [LICENSE.txt](external/loomio/loomio/LICENSE.txt), AGPL-3.0 |
| [Farama-Foundation/HighwayEnv](external/Farama-Foundation/HighwayEnv) | [37c84a34cadc](https://github.com/Farama-Foundation/HighwayEnv/tree/37c84a34cadcbfc17d61acf5196a89c380a56943) | [LICENSE](external/Farama-Foundation/HighwayEnv/LICENSE), MIT |
| [aurelio-labs/semantic-router](external/aurelio-labs/semantic-router) | [1fa1937e390f](https://github.com/aurelio-labs/semantic-router/tree/1fa1937e390fe57fb85ee3bbb8b3db593a4145db) | [LICENSE](external/aurelio-labs/semantic-router/LICENSE), MIT |
| [richardcc/assault-ai-pilot](external/richardcc/assault-ai-pilot) | [0284a559d8bc](https://github.com/richardcc/assault-ai-pilot/tree/0284a559d8bc3c7a15dfb0bf4fa42278242d60e9) | No licence file at this pin; badge alone is insufficient. |
