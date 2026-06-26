#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Regenerate INDEX.md for the agent's sanctum.

Scans the sanctum directory tree and produces a deterministic INDEX.md
listing standard files, session logs, and any organic files found.

Usage:
    uv run scripts/generate-index.py <sanctum-path>
    uv run scripts/generate-index.py --help
"""

import argparse
import json
import sys
from pathlib import Path

STANDARD_FILES = [
    "PERSONA.md",
    "CREED.md",
    "BOND.md",
    "MEMORY.md",
    "CAPABILITIES.md",
]


def generate_index(sanctum_path: Path) -> str:
    discovered = []
    for f in sorted(sanctum_path.iterdir()):
        if f.is_file() and f.suffix == ".md" and f.name not in STANDARD_FILES and f.name != "INDEX.md":
            discovered.append(f.name)

    session_dir = sanctum_path / "sessions"
    sessions = sorted(f.name for f in session_dir.glob("*.md")) if session_dir.is_dir() else []

    lines = ["# Index", "", "## Standard Files"]
    for name in STANDARD_FILES:
        marker = "✓" if (sanctum_path / name).exists() else "?"
        lines.append(f"- `{name}` — {marker}")

    if sessions:
        lines.extend(["", "## Session Logs"])
        for s in sessions:
            lines.append(f"- `sessions/{s}`")
    else:
        lines.extend(["", "## Session Logs", "_No sessions yet._"])

    if discovered:
        lines.extend(["", "## My Files"])
        for f in discovered:
            lines.append(f"- `{f}`")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate INDEX.md for an agent sanctum")
    parser.add_argument("sanctum_path", type=str, help="Path to the agent's sanctum directory")
    parser.add_argument("-o", type=str, help="Output file (default: stdout)")
    parser.add_argument("--write", action="store_true", help="Write directly to INDEX.md in the sanctum")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print diagnostics to stderr")
    args = parser.parse_args()

    sanctum = Path(args.sanctum_path).resolve()
    if not sanctum.is_dir():
        result = {"error": f"Sanctum directory not found: {sanctum}"}
        print(json.dumps(result))
        return 1

    index_content = generate_index(sanctum)

    if args.write:
        output_path = sanctum / "INDEX.md"
        output_path.write_text(index_content)
        result = {"status": "written", "file": str(output_path)}
        if args.verbose:
            print(f"generate-index: written to {output_path}", file=sys.stderr)
        print(json.dumps(result))
    elif args.o:
        Path(args.o).write_text(index_content)
    else:
        print(index_content)

    return 0


if __name__ == "__main__":
    sys.exit(main())
