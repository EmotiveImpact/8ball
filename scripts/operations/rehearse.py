#!/usr/bin/env python3
"""Restore one explicitly selected fictional SQLite backup into a NEW sandbox."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from eightball.operations.recovery import Checkpoint, rehearse_restore


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--sandbox', required=True, type=Path)
    parser.add_argument('--checkpoints', required=True, type=Path,
                        help='JSON array of signed checkpoints held separately from source')
    parser.add_argument('--trusted-public-key', required=True, type=Path)
    parser.add_argument('--maximum-age-seconds', required=True, type=int)
    parser.add_argument('--rto-seconds', required=True, type=float)
    parser.add_argument('--legacy', action='store_true')
    parser.add_argument('--fictional-only', required=True, action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.checkpoints.stat().st_size > 2_000_000 or args.trusted_public_key.stat().st_size > 8192:
            raise ValueError
        checkpoints = tuple(Checkpoint.model_validate_json(json.dumps(c))
                            for c in json.loads(args.checkpoints.read_text()))
        key = load_pem_public_key(args.trusted_public_key.read_bytes())
        if not isinstance(key, Ed25519PublicKey):
            raise ValueError
        report = rehearse_restore(args.source, args.sandbox, checkpoints=checkpoints,
                                  public_key=key, maximum_age_seconds=args.maximum_age_seconds,
                                  rto_seconds=args.rto_seconds, legacy=args.legacy)
    except Exception:
        print(json.dumps({'status': 'failed', 'scope': 'fictional_local_sqlite_rehearsal',
                          'production_recovery_accepted': False,
                          'reason': 'Rehearsal failed; preserve private inputs for inspection'}))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
