# V0.2 actual-model evaluation and release decision

## Decision

**The manual/reviewed software workflow is tested. Arbitrary-situation AI graph generation has not passed its acceptance gate.** Keep PR #2 as a draft and the generative planner as an experimental, human-reviewed feature. Do not call the whole V0.2 PRD complete on the basis of the application test suite.

A JSON response, a successful request or a green job is not a measure of semantic quality. These experiments are small fictional engineering fixtures, not an independently labelled professional benchmark. No case outcome was predicted or achieved by a model. Jev was not live-tested because credentials were not supplied.

## Latest actual Ollama experiment

Application commit: `117957d3ba4475c6644ff4833d036061d8be6d2c`.

Workflow run **35881916301**, job **107252235835**, finished with **failure** at the actual generation evaluation step. The runtime and model downloaded and started successfully. All four model requests ran; the application's structural validator rejected the graph response.

Run: https://github.com/EmotiveImpact/8ball/actions/runs/35881916301

Artifact **10760674557**, SHA-256 `37be95340a1cb7240e036f113664ae0f3c866591fc551f794d55a6edb4b2c3f6`, contains the actual response record, including the failed graph. The archive was downloaded and its checksum verified. A compact provenance/results record is in `docs/evidence/release-verification.json`; the rejected graph response is preserved separately in this repository.

Runtime: Ollama **0.34.3**. Model: **qwen3.5:4b**. Actual model digest: `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd`. The runtime was downloaded from a pinned release and verified using its expected archive checksum. The application sent requests only to the runner's loopback Ollama service.

| Fixture | Observed result | Approximate request time |
| --- | --- | --- |
| Negation and roles | Structurally valid extraction, three proposals | 56.1 seconds |
| Conflicting reports | Structurally valid extraction, three proposals | 48.2 seconds |
| Quoted instruction | Valid empty proposal; no invented case resolution | 26.0 seconds |
| Novel supplier recovery | Graph rejected by final verification validation | 138.4 seconds |

The graph named `act_006` as the final verification action but supplied only `act_001` through `act_005`. It also confused some condition meanings and did not represent the supplied alternatives cleanly. The system rejected that output, and **all four live case states remained unchanged**. Structural validation is doing useful work; the model's proposed plan is not yet sufficiently reliable.

The current evaluation explicitly requires all four fixtures to produce valid proposals and the alternative-supplier case to retain at least two candidate routes. The failed result was not converted into success by dropping those requirements, inventing a verification action or silently substituting a catalogue plan.

## Earlier generation experiments

Run **35799403892**, artifact **10725626644**, used the broader full graph schema. The first three extraction fixtures produced valid responses, but the graph request did not complete successfully. Artifact SHA-256: `d665fc8d474ace97a0232ceb8396efdb13a99434c1457da7d5b874b492d137c4`.

Run **35801067036**, artifact **10725734286**, used a smaller graph wire format. It produced a schema-valid graph but only **one candidate route**, despite the fixture providing alternatives. Its job completed under an earlier weaker gate. That is not evidence that the final acceptance journey passed. Artifact SHA-256: `ab51d158d7c05a0cba11c4a55d4a871296fb03113736788ecacc89eccc56be02`.

Those findings led to explicit prerequisite lists, a required final verification action, and stronger evaluation gates. The latest failed graph demonstrates why retaining these checks and human review is necessary.

## GLiClass CPU experiment

Run **35798129246**, artifact **10724722378**, evaluated the actual application classifier adapter on 30 fixed fictional examples. Model: `knowledgator/gliclass-edge-v3.0`, exact revision `df03993a2ed98e5e4a0d2dd7efbbd105abe874cf`. Dataset SHA-256: `12873b9cf726001a89eadd5d6e47727ed6ca738ccd3a33ffc833d7a692e8d5fc`.

Raw top-one matches: **6/30, or 20%**. Coverage after the existing abstention rules: **0%**. Every response therefore remained an abstention for operator review. This tested configuration is **not approved for production classification**. The numbers describe this model/pipeline/label configuration on this small set, not all GLiClass models or the general feasibility of local classification.

The recorded environment used CPU inference with two threads. Median observed request time was 14.235 ms and process peak RSS was approximately 612.5 MiB, including the Python process. Neither number is a guarantee for the user's hardware. The artifact includes the dependency environment and raw per-case scores. Artifact SHA-256: `753d1ae6b902142241ad9fc8868c955286acd3bc82c65a008facd8d5dad1868b`.

## Current provider responsibilities

Rules capture is deterministic sentence capture, not semantic AI. Catalogue graph proposals are explicitly selected, human-authored hypotheses. Ollama proposes source-linked objects, questions and compact graphs; schema/reference checks and a separate review transaction stand between generation and case state. Jev and GLiClass are bounded classification options, not the owner of the graph or authority to act.

Operator mistakes such as an unknown source, a retracted source, an unsupported provider operation or missing permission are rejected before inference and do not create a misleading model-failure record. Actual invalid output and unavailable providers remain separately recorded as failed runs.

## Local setup

Core 8BALL works without models. For an explicitly chosen local experiment, install Ollama, start its local service, then obtain the candidate model deliberately:

```sh
ollama pull qwen3.5:4b
# In the same environment used to launch the 8BALL server:
export EIGHTBALL_OLLAMA_MODEL=qwen3.5:4b
python -m eightball
```

Use only fictional sources. Select Ollama in the review flow and inspect every generated object. Model tags can change; record the actual digest and runtime before comparing results. The project's evaluation workflow records these values.

Jev requires `TYPESAFE_API_KEY` in the server environment and explicit permission to transmit selected excerpts. Do not put the key in browser code, source control or an exported case. No live Jev quality or latency result is claimed here.

GLiClass dependencies and public weights are installed only by the explicit evaluation/setup flow. The application expects cached model files and does not deliberately download weights while handling a case. The recorded pipeline configuration needs investigation and a fresh, separate test set before selection.

## Next intelligence milestone

Use the failed response to create reproducible regression cases. Compare a stronger configured model and a staged generator on the same structural contracts without weakening validation. A staged process should propose explicit success criteria, intermediate states, alternative action paths and a final verification step, then undergo deterministic validation and human review. A repair attempt must remain bounded, preserve the original output and never invent source evidence.

After structural validity improves, obtain independent operator/expert labels and measure semantic errors, missing dependencies, unsupported authority, negation, critical deadline recall, abstention and correction effort on cases not used to tune the prompts. Only then decide which local or external model belongs in a pilot.
