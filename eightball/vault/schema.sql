-- Proposed lane-local schema. Vault construction is explicit; never run on import.
CREATE TABLE IF NOT EXISTS vault_originals (
    id TEXT PRIMARY KEY, case_id TEXT NOT NULL, organisation_id TEXT NOT NULL,
    matter_id TEXT NOT NULL, descriptor TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS vault_blobs (
    object_id TEXT PRIMARY KEY REFERENCES vault_originals(id),
    nonce BLOB NOT NULL, ciphertext BLOB NOT NULL, envelope TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS vault_state (
    object_id TEXT PRIMARY KEY REFERENCES vault_originals(id),
    revision INTEGER NOT NULL, status TEXT NOT NULL, retain_until TEXT NOT NULL,
    hold INTEGER NOT NULL DEFAULT 0, scan_attempt TEXT, scan_record TEXT
);
CREATE TABLE IF NOT EXISTS vault_commands (
    actor TEXT NOT NULL, case_id TEXT NOT NULL, command_id TEXT NOT NULL,
    request_hash TEXT NOT NULL, object_id TEXT NOT NULL REFERENCES vault_originals(id),
    PRIMARY KEY(actor, case_id, command_id)
);
CREATE TABLE IF NOT EXISTS vault_audit (
    sequence INTEGER PRIMARY KEY AUTOINCREMENT, record TEXT NOT NULL,
    previous_hash TEXT NOT NULL, record_hash TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS vault_original_no_update BEFORE UPDATE ON vault_originals
BEGIN SELECT RAISE(ABORT, 'Immutable original'); END;
CREATE TRIGGER IF NOT EXISTS vault_original_no_delete BEFORE DELETE ON vault_originals
BEGIN SELECT RAISE(ABORT, 'Preserve original descriptor'); END;
CREATE TRIGGER IF NOT EXISTS vault_blob_no_update BEFORE UPDATE ON vault_blobs
BEGIN SELECT RAISE(ABORT, 'Immutable encrypted original'); END;
CREATE TRIGGER IF NOT EXISTS vault_audit_no_update BEFORE UPDATE ON vault_audit
BEGIN SELECT RAISE(ABORT, 'Append-only audit'); END;
CREATE TRIGGER IF NOT EXISTS vault_audit_no_delete BEFORE DELETE ON vault_audit
BEGIN SELECT RAISE(ABORT, 'Append-only audit'); END;
