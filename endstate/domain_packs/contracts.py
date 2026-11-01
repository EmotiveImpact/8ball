"""Data-only catalogue inputs. Packs contain hypotheses, never case authority."""
from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import Field, model_validator

from ..contracts import Actor, Constraint, Graph, PlanningSnapshot, Question, Resource
from ..primitives import Identifier, Strict, Text, Title

PACK_CONTRACT = 'endstate.domain-pack.v1'
CONSUMER_CONTRACT = 'endstate.domain-consumer.v1'
MAX_PACK_BYTES = 262144
Version = Annotated[str, Field(pattern=r'^(0|[1-9][0-9]{0,5})\.(0|[1-9][0-9]{0,5})\.(0|[1-9][0-9]{0,5})$')]
Digest = Annotated[str, Field(pattern=r'^[a-f0-9]{64}$')]
Concept = Literal['snapshot', 'actor', 'condition', 'action', 'objective', 'constraint',
                  'evidence', 'observation', 'question', 'course', 'review']


class Vocabulary(Strict):
    concept: Concept
    singular: Title
    plural: Title


class ObjectMapping(Strict):
    product_object: Identifier
    engine_object: Concept
    description: Title


class ConfirmationRule(Strict):
    condition_id: Identifier
    evidence_requirement: Title
    reviewer_role: Title
    mode: Literal['explicit_reviewed_observation'] = 'explicit_reviewed_observation'


class Prompt(Strict):
    id: Identifier
    purpose: Literal['extract', 'graph', 'questions']
    text: Text
    output_contract: Title
    disposition: Literal['proposal_only'] = 'proposal_only'


class IntegrationDeclaration(Strict):
    id: Identifier
    adapter_key: Identifier
    contract_version: Version
    operations: list[Literal['source_ingest', 'proposal', 'notification']] = Field(min_length=1, max_length=3)
    required_permissions: list[Identifier] = Field(min_length=1, max_length=12)
    activation: Literal['host_registration_required'] = 'host_registration_required'
    external_permission: Literal['explicit_per_operation'] = 'explicit_per_operation'

    @model_validator(mode='after')
    def unique_operations(self):
        if len(set(self.operations)) != len(self.operations):
            raise ValueError('Repeated integration operation')
        if len(set(self.required_permissions)) != len(self.required_permissions):
            raise ValueError('Repeated integration permission')
        return self


class Catalogue(Strict):
    graph: Graph
    constraints: list[Constraint] = Field(default_factory=list, max_length=40)
    resources: list[Resource] = Field(default_factory=list, max_length=24)
    actors: list[Actor] = Field(default_factory=list, max_length=80)
    questions: list[Question] = Field(default_factory=list, max_length=80)

    @model_validator(mode='before')
    @classmethod
    def explicit_ids(cls, data):
        if isinstance(data, dict):
            graph = data.get('graph')
            groups = [data.get(k, []) for k in ('constraints', 'resources', 'actors', 'questions')]
            if isinstance(graph, dict):
                groups.extend(graph.get(k, []) for k in ('conditions', 'actions', 'objectives'))
            for group in groups:
                if isinstance(group, list):
                    for item in group:
                        if isinstance(item, dict) and 'id' not in item:
                            raise ValueError('Pack object IDs must be explicit and stable')
        return data

    @model_validator(mode='after')
    def hypothesis_only(self):
        if not self.graph.conditions or not self.graph.actions or not self.graph.objectives:
            raise ValueError('A catalogue needs conditions, actions and objectives')
        groups = [self.graph.conditions, self.graph.actions, self.graph.objectives,
                  self.constraints, self.actors, self.questions]
        for group in groups:
            for obj in group:
                if obj.provenance.origin != 'playbook' or obj.provenance.references or obj.provenance.run_id:
                    raise ValueError('Pack provenance must be an unsourced playbook hypothesis')
        if any(c.confirmed for c in self.constraints):
            raise ValueError('A pack cannot confirm a case policy')
        if any(q.status != 'open' or q.answer or q.evidence_ids for q in self.questions):
            raise ValueError('A pack cannot answer a case question')
        if any(a.last_contact for a in self.actors):
            raise ValueError('A pack cannot record an actual contact')
        if any(c.due_at for c in self.graph.conditions):
            raise ValueError('Case dates must be supplied by the host, not a reusable catalogue')
        if any(a.earliest_start or a.expires_at or any(c.due_at for c in a.contingencies)
               for a in self.graph.actions):
            raise ValueError('Case action dates do not belong in a reusable catalogue')
        if any(r.available_from or r.available_until for r in self.resources) or any(q.needed_by for q in self.questions):
            raise ValueError('Case scheduling dates do not belong in a reusable catalogue')
        # Native relations validate actors, policies, resources and all graph references.
        PlanningSnapshot(id='catalogue_validation', deadline=datetime.max.replace(tzinfo=timezone.utc),
                         **self.model_dump(mode='python'))
        return self


class DomainPack(Strict):
    schema_version: Literal['endstate.domain-pack.v1'] = PACK_CONTRACT
    pack_id: Identifier
    pack_version: Version
    engine_contract: Literal['endstate.plan.v1'] = 'endstate.plan.v1'
    owner: Title
    description: Text
    distribution: Literal['internal_review_required'] = 'internal_review_required'
    vocabulary: list[Vocabulary] = Field(min_length=1, max_length=11)
    object_mappings: list[ObjectMapping] = Field(min_length=1, max_length=40)
    catalogue: Catalogue
    confirmation_rules: list[ConfirmationRule] = Field(min_length=1, max_length=64)
    prompts: list[Prompt] = Field(min_length=1, max_length=8)
    integrations: list[IntegrationDeclaration] = Field(default_factory=list, max_length=12)

    @model_validator(mode='after')
    def coherent(self):
        for items, key in ((self.vocabulary, 'concept'), (self.object_mappings, 'product_object'),
                           (self.confirmation_rules, 'condition_id'), (self.prompts, 'id'),
                           (self.integrations, 'id')):
            values = [getattr(item, key) for item in items]
            if len(values) != len(set(values)):
                raise ValueError('Repeated domain-pack key: ' + key)
        concepts = {v.concept for v in self.vocabulary}
        if any(m.engine_object not in concepts for m in self.object_mappings):
            raise ValueError('Object mapping lacks vocabulary')
        confirmations = {r.condition_id: r.evidence_requirement for r in self.confirmation_rules}
        if confirmations != {c.id: c.confirmation for c in self.catalogue.graph.conditions}:
            raise ValueError('Every condition needs its exact explicit confirmation rule')
        return self


class PackReference(Strict):
    schema_version: Literal['endstate.domain-pack.v1'] = PACK_CONTRACT
    pack_id: Identifier
    pack_version: Version
    sha256: Digest


class MigrationReport(Strict):
    before: PackReference
    after: PackReference
    disposition: Literal['identical', 'explicit_review_required']
    changed_sections: list[str]
    automatic_case_migration: Literal[False] = False
