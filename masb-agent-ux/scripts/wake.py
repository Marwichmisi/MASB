#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

import sys
import json
import argparse
from pathlib import Path

SKILL_NAME = "masb-agent-ux"

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
        content = path.read_text(encoding="utf-8").rstrip()
        return {"file": path.name, "exists": True, "content": content}
    except FileNotFoundError:
        return {"file": path.name, "exists": False, "content": None}


def build_report(mode: str, sanctum: str, identity: list[dict]) -> dict:
    return {
        "mode": mode,
        "sanctum": sanctum,
        "identity": identity,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Waking — load masb-agent-ux sanctum in one pass, or route to First Breath",
    )
    parser.add_argument(
        "project_root",
        help="Root of the project (where _bmad/ lives)",
    )
    parser.add_argument(
        "--pulse",
        action="store_true",
        help="Run in Pulse Mode (autonomous wake)",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    sanctum = project_root / "_bmad" / "memory" / SKILL_NAME

    core_ok = (
        sanctum.is_dir()
        and (sanctum / "CREED.md").is_file()
        and (sanctum / "MEMORY.md").is_file()
    )
    if not core_ok:
        report = build_report("FIRST_BREATH", str(sanctum), [])
        print(json.dumps(report))
        return 0

    mode = "PULSE" if args.pulse else "WAKING"
    identity = []
    for name in IDENTITY_FILES:
        result = emit(sanctum / name)
        identity.append(result)
    if args.pulse:
        pulse = emit(sanctum / "PULSE.md")
        identity.append(pulse)

    report = build_report(mode, str(sanctum), identity)
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
