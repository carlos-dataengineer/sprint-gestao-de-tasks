#!/usr/bin/env python3
"""Generate the standalone Sprint HTML artifact from this Agent Skill package."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    source = skill_root / "assets" / "sprint.html"
    parser = argparse.ArgumentParser(description="Create the Sprint task-management HTML artifact.")
    parser.add_argument("--output", default="Sprint.html", help="Destination HTML path (default: ./Sprint.html)")
    args = parser.parse_args()
    destination = Path(args.output).expanduser().resolve()
    if not source.is_file():
        parser.error(f"Sprint source artifact not found: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if not destination.is_file() or destination.stat().st_size == 0:
        raise SystemExit("Artifact generation failed: output is missing or empty.")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
