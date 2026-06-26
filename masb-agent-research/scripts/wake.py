#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Waking — load the agent's sanctum in one pass, or route to First Breath.

Run on activation. Determines the mode from the filesystem (and the --pulse
/ --headless flags) and, when the sanctum exists, prints the full identity
in a single read so the agent becomes itself in one shot.

Usage:
    uv run wake.py <project-root> [--pulse] [--headless]
"""

import argparse
import json
import sys
from pathlib import Path

SKILL_NAME = "masb-agent-research"

IDENTITY_FILES = [
    "INDEX.md",
    "PERSONA.md",
    "CREED.md",
    "BOND.md",
    "MEMORY.md",
    "CAPABILITIES.md",
]


def emit(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").rstrip()
    except FileNotFoundError:
        return f"(missing: {path.name})"


def main() -> int:
    parser = argparse.ArgumentParser(description="Load sanctum identity or route to First Breath")
    parser.add_argument("project_root", help="Path to the project root (where _bmad/ lives)")
    parser.add_argument("--pulse", action="store_true", help="Pulse mode (autonomous wake)")
    parser.add_argument("--headless", action="store_true", help="Headless mode (no greeting ceremony)")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    sanctum = project_root / "_bmad" / "memory" / SKILL_NAME

    core_ok = (
        sanctum.is_dir()
        and (sanctum / "CREED.md").is_file()
        and (sanctum / "MEMORY.md").is_file()
    )
    if not core_ok:
        print("MODE: FIRST_BREATH")
        print(f"NO SANCTUM at {sanctum}")
        print("This is your one birth. Load references/first-breath.md and follow it.")
        return 0

    mode = "PULSE" if args.pulse else "HEADLESS" if args.headless else "WAKING"
    identity = {name: emit(sanctum / name) for name in IDENTITY_FILES}
    if args.pulse:
        identity["PULSE.md"] = emit(sanctum / "PULSE.md")

    result = {
        "mode": mode,
        "sanctum": str(sanctum),
        "identity": identity,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
