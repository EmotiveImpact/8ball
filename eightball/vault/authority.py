"""Adapter to existing server-owned agency grants; no provisioning endpoint."""
from collections.abc import Callable

from eightball.authorisation import Grant, Operation, Resource, permits
from .contracts import VaultPermission


class RegistryAuthority:
    """Registry tables must share the vault connection for serial revocation.

    Existing WRITE is not lawful-hold/deletion authority. The integrator must
    separately provide a current transactional control policy for those powers.
    """

    def __init__(self, control: Callable | None = None):
        self.control = control

    def require(self, db, *, identity, case_id, object_id, permission, now):
        row = db.execute('SELECT organisation_id,matter_id FROM agency_case_scope WHERE case_id=?',
                         (case_id,)).fetchone()
        if row is None:
            raise PermissionError('Access is not permitted')
        scope = Resource(organisation_id=row[0], matter_id=row[1], object_id=object_id)
        grants = tuple(Grant.model_validate_json(row[0]) for row in
                       db.execute('SELECT body FROM agency_grants WHERE revoked=0'))
        operations = {
            VaultPermission.UPLOAD: (Operation.READ, Operation.WRITE),
            VaultPermission.READ: (Operation.READ,),
            VaultPermission.DOWNLOAD: (Operation.READ, Operation.DOWNLOAD),
            VaultPermission.SCAN: (Operation.READ, Operation.WRITE),
            VaultPermission.HOLD: (Operation.READ, Operation.WRITE),
            VaultPermission.RETENTION: (Operation.READ, Operation.WRITE),
            VaultPermission.DELETE: (Operation.READ, Operation.WRITE),
            VaultPermission.AUDIT: (Operation.READ,),
        }[permission]
        if not all(permits(identity, scope, op, grants, now=now) for op in operations):
            raise PermissionError('Access is not permitted')
        if permission in {VaultPermission.SCAN, VaultPermission.HOLD, VaultPermission.RETENTION,
                          VaultPermission.DELETE, VaultPermission.AUDIT}:
            if self.control is None or self.control(db, identity, scope, permission, now) is not True:
                raise PermissionError('Separate vault control authority is required')
        return scope
