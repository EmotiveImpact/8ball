"""Explicit hosted API run of the unchanged frozen generation fixtures.

Configure EIGHTBALL_API_* first; --allow-hosted is required. This wrapper uses
the same cases, compiler, unassisted-output checks and pass gate as the existing
hosted evaluation. It installs nothing and never retries or substitutes plans.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evals.live_huggingface import main

if __name__ == '__main__':
    raise SystemExit(main(default_provider='openai_compatible'))
