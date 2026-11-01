"""Explicit bounded JSON only: no paths, discovery, imports, hooks or connectors."""
import hashlib
import json

from .contracts import DomainPack, MAX_PACK_BYTES, MigrationReport, PackReference


class PackError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PackError('duplicate_json_key')
        result[key] = value
    return result


def _nonfinite(_value):
    raise PackError('nonfinite_json')


def load_pack_json(payload: str | bytes) -> DomainPack:
    if not isinstance(payload, (str, bytes)):
        raise PackError('json_text_required')
    try:
        raw = payload.encode('utf-8') if isinstance(payload, str) else payload
        if len(raw) > MAX_PACK_BYTES:
            raise PackError('pack_size_limit')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_object, parse_constant=_nonfinite)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise PackError('invalid_json') from exc
    if not isinstance(data, dict):
        raise PackError('pack_object_required')
    # Bound otherwise-ignored or malformed JSON depth before Pydantic traverses it.
    pending = [(data, 0)]
    while pending:
        item, depth = pending.pop()
        if depth > 32:
            raise PackError('pack_depth_limit')
        if isinstance(item, dict):
            pending.extend((x, depth + 1) for x in item.values())
        elif isinstance(item, list):
            pending.extend((x, depth + 1) for x in item)
        elif isinstance(item, str):
            try:
                item.encode('utf-8')
            except UnicodeError as exc:
                raise PackError('invalid_unicode') from exc
    return DomainPack.model_validate(data)


def checked_pack(pack: DomainPack) -> DomainPack:
    if not isinstance(pack, DomainPack):
        raise PackError('domain_pack_required')
    # Revalidate nested mutable instances; never trust a prior parse or model_copy.
    return load_pack_json(pack.model_dump_json())


def pack_reference(pack: DomainPack) -> PackReference:
    parsed = checked_pack(pack)
    canonical = json.dumps(parsed.model_dump(mode='json'), sort_keys=True,
                           ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')
    return PackReference(pack_id=parsed.pack_id, pack_version=parsed.pack_version,
                         sha256=hashlib.sha256(canonical).hexdigest())


def require_reference(pack: DomainPack, expected: PackReference) -> None:
    expected = PackReference.model_validate(expected.model_dump(mode='python'))
    if pack_reference(pack) != expected:
        raise PackError('pack_reference_mismatch')


def compare_packs(before: DomainPack, after: DomainPack) -> MigrationReport:
    old, new = checked_pack(before), checked_pack(after)
    old_ref, new_ref = pack_reference(old), pack_reference(new)
    if old.pack_id != new.pack_id:
        raise PackError('different_pack_identity')
    if old_ref == new_ref:
        return MigrationReport(before=old_ref, after=new_ref, disposition='identical', changed_sections=[])
    old_version = tuple(map(int, old.pack_version.split('.')))
    new_version = tuple(map(int, new.pack_version.split('.')))
    if new_version <= old_version:
        raise PackError('changed_content_requires_newer_version')
    old_data, new_data = old.model_dump(mode='json'), new.model_dump(mode='json')
    changed = sorted(key for key in old_data if old_data[key] != new_data[key])
    return MigrationReport(before=old_ref, after=new_ref, disposition='explicit_review_required',
                           changed_sections=changed)
