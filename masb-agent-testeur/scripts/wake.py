#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Waking — load the agent's sanctum in one pass, or route to First Breath.

Run on activation. Determines the mode from the filesystem (and the --pulse
flag) and, when the sanctum exists, prints the full identity in a single read
(INDEX, PERSONA, CREED, BOND, MEMORY, CAPABILITIES) so the agent becomes itself
in one shot instead of six. In --pulse mode it also appends PULSE.md. When no
sanctum exists, it prints a directive to run First Breath.

This loads runtime memory only. It never reads or writes config or customize.toml.

Usage:
    uv run wake.py <project-root> [--pulse]
"""

import argparse
import json
import sys
from pathlib import Path

SKILL_NAME = "masb-agent-testeur"

IDENTITY_FILES = [
    "INDEX.md",
    "PERSONA.md",
    "CREED.md",
    "BOND.md",
    "MEMORY.md",
    "CAPABILITIES.md",
]

def emit(path: Path) -> dict:
    try:
        return {"file": path.name, "content": path.read_text(encoding="utf-8").rstrip()}
    except FileNotFoundError:
        return {"file": path.name, "content": None}

def main() -> int:
    parser = argparse.ArgumentParser(description="Load agent sanctum on waking")
    parser.add_argument("project_root", type=str, help="Path to project root (where _bmad/ lives)")
    parser.add_argument("--pulse", action="store_true", help="Run in Pulse mode (autonomous wake)")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    sanctum = project_root / "_bmad" / "memory" / SKILL_NAME

    core_ok = (
        sanctum.is_dir()
        and (sanctum / "CREED.md").is_file()
        and (sanctum / "MEMORY.md").is_file()
    )
    if not core_ok:
        result = {
            "mode": "FIRST_BREATH",
            "sanctum": str(sanctum),
            "directive": "This is your one birth. Load references/first-breath.md and follow it.",
        }
        print(json.dumps(result))
        return 0

    identities = [emit(sanctum / name) for name in IDENTITY_FILES]
    result = {
        "mode": "PULSE" if args.pulse else "WAKING",
        "sanctum": str(sanctum),
        "identities": identities,
    }
    print(json.dumps(result))
    return 0

if __name__ == "__main__":
    sys.exit(main())
