#!/usr/bin/env python3
"""Run the Sprint Skill installation bootstrap and create Sprint.html."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    generator = skill_root / "scripts" / "create_artifact.py"
    parser = argparse.ArgumentParser(
        description="Install Sprint by generating its ready-to-use HTML artifact."
    )
    parser.add_argument(
        "--output",
        default=str(Path.cwd() / "Sprint.html"),
        help="Destination for the generated artifact (default: ./Sprint.html)",
    )
    args = parser.parse_args()
    destination = Path(args.output).expanduser().resolve()
    if not generator.is_file():
        parser.error(f"Sprint generator not found: {generator}")
    subprocess.run(
        [sys.executable, str(generator), "--output", str(destination)],
        check=True,
    )
    if not destination.is_file() or destination.stat().st_size == 0:
        raise SystemExit("Sprint installation failed: artifact is missing or empty.")
    print(f"Sprint instalada. Artefato criado em: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
