#!/usr/bin/env python3
"""Local offline report generation. No external calls or release decisions."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from eightball.operations.readiness import (FictionalPilot, ReadinessManifest,
                                            evaluate_readiness, summarize_pilot)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('readiness', 'pilot'))
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        if args.manifest.stat().st_size > 2_000_000:
            raise ValueError
        content = args.manifest.read_text()
        if args.mode == 'readiness':
            report = evaluate_readiness(ReadinessManifest.model_validate_json(content),
                                        root=args.root, now=datetime.now(timezone.utc))
        else:
            report = summarize_pilot(FictionalPilot.model_validate_json(content))
    except Exception:
        print(json.dumps({'status': 'invalid_input', 'release_authorized': False}))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report['status'] == 'blocked' else 0


if __name__ == '__main__':
    raise SystemExit(main())
