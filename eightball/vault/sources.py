"""Read-only Source Desk integration seam, not an import or evidence attestation."""


def exact_text(vault, *, identity, case_id, object_id, expected_revision, expected_sha256):
    handle = vault.source_handle(identity=identity, case_id=case_id, object_id=object_id,
                                 expected_revision=expected_revision)
    content = vault.read_original(identity=identity, case_id=case_id, object_id=object_id,
                                  expected_revision=expected_revision, expected_sha256=expected_sha256)
    return {'source_handle': handle, 'text': content.decode('utf-8', errors='strict'),
            'representation': 'utf8-exact-v1', 'fact_verified': False}
