"""Attributed hypothetical contributions, not a simulator or authority engine."""
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .primitives import Identifier, Strict, Title

VERSION = 'endstate.assumption-challenge.v1'
Reference = Annotated[str, Field(pattern=r'^(case|objective|condition|action|source|actor|constraint|decision):[a-zA-Z0-9_-]{1,80}$')]
StatementText = Annotated[str, Field(min_length=1, max_length=1500, pattern=r'\S')]


class Perspective(Strict):
    id: Identifier
    label: Title
    kind: Literal['fictional', 'archetype']
    objective: StatementText
    information_boundary: StatementText
    permitted_references: list[Reference] = Field(min_length=1, max_length=12)


class Contribution(Strict):
    id: Identifier
    role_id: Identifier
    kind: Literal['assumption', 'objection', 'question']
    text: StatementText
    references: list[Reference] = Field(min_length=1, max_length=12)
    counters: list[Identifier] = Field(default_factory=list, max_length=12)
    verification_needed: StatementText
    origin: Literal['operator_declared', 'deterministic_fixture'] = 'operator_declared'


class Branch(Strict):
    id: Identifier
    title: Title
    rationale: StatementText
    assumption_ids: list[Identifier] = Field(min_length=1, max_length=12)


class Disposition(Strict):
    contribution_id: Identifier
    status: Literal['open', 'addressed_in_review', 'retained_concern', 'deferred']
    rationale: StatementText


class OperatorDecision(Strict):
    outcome: Literal['continue_review', 'seek_information', 'reconsider', 'defer']
    rationale: StatementText
    contribution_ids: list[Identifier] = Field(default_factory=list, max_length=12)


class Draft(Strict):
    run_id: Identifier
    perspectives: list[Perspective] = Field(default_factory=list, max_length=4)
    contributions: list[Contribution] = Field(default_factory=list, max_length=12)
    branches: list[Branch] = Field(default_factory=list, max_length=3)
    dispositions: list[Disposition] = Field(default_factory=list, max_length=12)
    operator_decision: OperatorDecision | None = None
    perspectives_not_applicable_reason: StatementText | None = None

    @model_validator(mode='after')
    def linked(self):
        for objects in (self.perspectives, self.contributions, self.branches):
            if len({obj.id for obj in objects}) != len(objects):
                raise ValueError('Repeated challenge identifier')
        roles = {role.id: role for role in self.perspectives}
        claims = {claim.id: claim for claim in self.contributions}
        if self.perspectives and self.perspectives_not_applicable_reason is not None:
            raise ValueError('Declared perspectives cannot also be not applicable')
        if any(not obj.label.strip() for obj in self.perspectives) or any(not obj.title.strip() for obj in self.branches):
            raise ValueError('Challenge labels cannot be blank')
        for role in self.perspectives:
            if len(set(role.permitted_references)) != len(role.permitted_references):
                raise ValueError('Repeated perspective reference')
        for claim in self.contributions:
            if claim.role_id not in roles:
                raise ValueError('Contribution has no declared perspective')
            if not set(claim.references) <= set(roles[claim.role_id].permitted_references):
                raise ValueError('Contribution exceeds its declared information boundary')
            if (len(set(claim.references)) != len(claim.references)
                    or len(set(claim.counters)) != len(claim.counters)
                    or claim.id in claim.counters or not set(claim.counters) <= claims.keys()):
                raise ValueError('Invalid contribution references or counter-position')
        assumptions = {c.id for c in self.contributions if c.kind == 'assumption'}
        for branch in self.branches:
            if (len(set(branch.assumption_ids)) != len(branch.assumption_ids)
                    or not set(branch.assumption_ids) <= assumptions):
                raise ValueError('Each branch must link distinct declared assumptions')
        dispositions = {d.contribution_id: d for d in self.dispositions}
        if len(dispositions) != len(self.dispositions) or not dispositions.keys() <= claims.keys():
            raise ValueError('Each disposition must identify one distinct contribution')
        if self.operator_decision is not None:
            decision = self.operator_decision
            if (len(set(decision.contribution_ids)) != len(decision.contribution_ids)
                    or not set(decision.contribution_ids) <= claims.keys()):
                raise ValueError('Operator decision references unknown or repeated contributions')
            unresolved = {c.id for c in self.contributions if c.kind == 'objection'
                          and (c.id not in dispositions or dispositions[c.id].status != 'addressed_in_review')}
            if decision.outcome == 'continue_review' and not unresolved <= set(decision.contribution_ids):
                raise ValueError('Continuing review must explicitly acknowledge every unresolved objection')
        return self


def validate_references(draft: Draft, allowed: set[str]):
    if any(not set(role.permitted_references) <= allowed for role in draft.perspectives):
        raise ValueError('Challenge references a missing case record')


def coverage(draft: Draft):
    addressed = {d.contribution_id for d in draft.dispositions if d.status == 'addressed_in_review'}
    return {'state': 'declared' if draft.perspectives else 'not_applicable' if draft.perspectives_not_applicable_reason else 'not_supplied',
            'not_applicable_reason': draft.perspectives_not_applicable_reason,
            'declared_perspectives': len(draft.perspectives),
            'contributing_perspectives': len({c.role_id for c in draft.contributions}),
            'missing_contributions': [p.id for p in draft.perspectives if not any(c.role_id == p.id for c in draft.contributions)],
            'all_objections': [c.id for c in draft.contributions if c.kind == 'objection'],
            'operator_addressed': sorted(addressed),
            'unresolved_objections': [c.id for c in draft.contributions if c.kind == 'objection' and c.id not in addressed],
            'unanswered_questions': [c.id for c in draft.contributions if c.kind == 'question' and c.id not in addressed],
            'notice': 'Operator-declared perspectives. Missing contributions are not agreement, refusal or consent. Addressed in review is not factual verification or action approval.'}


def changed_fields(before, after, path=()):
    """Exact JSON differences; object collections use identifiers, not positions."""
    if isinstance(before, list) and isinstance(after, list):
        if all(isinstance(x, dict) and isinstance(x.get('id'), str) for x in before + after):
            left, right = {x['id']: x for x in before}, {x['id']: x for x in after}
            if len(left) != len(before) or len(right) != len(after):
                raise ValueError('Repeated identifier in comparison')
            return changed_fields(left, right, path)
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(before.keys() | after.keys()):
            if key in before and key in after:
                result.extend(changed_fields(before[key], after[key], (*path, key)))
            else:
                result.append({'path': [*path, key], 'before_present': key in before, 'after_present': key in after,
                               'before': before.get(key), 'after': after.get(key)})
        return result
    if type(before) is not type(after) or before != after:
        return [{'path': list(path), 'before_present': True, 'after_present': True, 'before': before, 'after': after}]
    return []


def information_agenda(draft: Draft):
    """Declared structural links only, not expected value or predictive priority."""
    draft = Draft.model_validate(draft.model_dump(mode='python'))
    items = []
    for contribution in draft.contributions:
        counters = sorted({c.id for c in draft.contributions
                           if contribution.id in c.counters} | set(contribution.counters))
        related = {contribution.id, *counters}
        branches = sorted(b.id for b in draft.branches if related & set(b.assumption_ids))
        disposition = next((d.status for d in draft.dispositions
                            if d.contribution_id == contribution.id), 'not_reviewed')
        items.append({'contribution_id': contribution.id, 'kind': contribution.kind,
                      'statement': contribution.text, 'verification_needed': contribution.verification_needed,
                      'references': list(contribution.references), 'counter_ids': counters,
                      'branch_ids': branches, 'review_disposition': disposition,
                      'attention_basis': 'contested_branch' if branches and counters else
                                         'branch_linked' if branches else 'declared_check'})
    order = {'contested_branch': 0, 'branch_linked': 1, 'declared_check': 2}
    items.sort(key=lambda item: (order[item['attention_basis']], -len(item['branch_ids']), item['contribution_id']))
    return {'version': 'endstate.information-agenda.v1', 'items': items,
            'coverage': coverage(draft), 'facts_attested': False, 'execution_authorised': False,
            'notice': 'Declared counter-links and branch coverage determine display order, not value, urgency or probability. Every statement remains visible; addressed in review is not verified. No check is automatically selected or sent.'}
