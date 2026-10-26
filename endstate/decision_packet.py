"""Disclosure projections of an already verified brief; never a truth store.

The host must supply current server-owned permissions and verified history.
Restricted indices exclude all narrative, including apparently allowed claims:
free text can disclose information beyond its declared reference links.
"""
from copy import deepcopy
from typing import Literal

from pydantic import Field, model_validator

from .primitives import Strict
from .rehearsal import Reference

VERSION = 'endstate.decision-packet.v1'


class DisclosureDenied(ValueError):
    pass


class Selection(Strict):
    mode: Literal['operator_review', 'reference_index'] = 'operator_review'
    references: list[Reference] = Field(default_factory=list, max_length=64)

    @model_validator(mode='after')
    def meaningful_selection(self):
        if len(set(self.references)) != len(self.references):
            raise ValueError('Repeated packet reference')
        if self.mode == 'reference_index' and not self.references:
            raise ValueError('Choose at least one reference for a restricted index')
        if self.mode == 'operator_review' and self.references:
            raise ValueError('A complete operator review cannot request a partial reference scope')
        return self


def project(brief: dict, selection: Selection, allowed_references: set[str]):
    selection = Selection.model_validate(selection.model_dump(mode='python'))
    known = set(brief['reference_hashes'])
    requested = set(selection.references) if selection.mode == 'reference_index' else known
    if not requested <= known & allowed_references:
        raise DisclosureDenied('Current disclosure policy does not permit this packet')
    index = [{'reference': ref, 'sha256': brief['reference_hashes'][ref]} for ref in sorted(requested)]
    if selection.mode == 'reference_index':
        return {'contract_version': VERSION, 'mode': selection.mode, 'complete_audit': False,
                'references': index, 'brief': None, 'predecessor_content': 'omitted',
                'omissions': ['All narrative, titles, stakeholder declarations and review reasons',
                              'All route calculations and hypothetical overlays',
                              'Unselected references, supporting records and predecessor contents'],
                'notice': 'Deliberately restricted reference index, not a complete decision or audit. Missing content must not be inferred.'}
    return {'contract_version': VERSION, 'mode': selection.mode, 'complete_audit': False,
            'references': index, 'brief': deepcopy(brief), 'predecessor_content': 'not_embedded',
            'omissions': ['Source document contents and unrelated case journals', 'Predecessor contents; lineage pointers are supplied separately'],
            'notice': 'Internal operator review, not a client-sharing permission or complete case audit. Recheck authority before sharing.'}
