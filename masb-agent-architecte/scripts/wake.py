#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

import sys
import os
from pathlib import Path

SKILL_NAME = "masb-agent-architecte"

IDENTITY_FILES = [
    "INDEX.md",
    "PERSONA.md",
    "CREED.md",
    "BOND.md",
    "MEMORY.md",
    "CAPABILITIES.md",
]


def count_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return len(text.split())


def emit(path: Path) -> None:
    print(f"\n===== {path.name} =====")
    try:
        content = path.read_text(encoding="utf-8").rstrip()
        print(content)
        tokens = count_tokens(content)
        print(f"\n--- {tokens} tokens ---")
    except FileNotFoundError:
        print(f"(missing: {path.name})")


def main() -> int:
    args = sys.argv[1:]
    pulse = "--pulse" in args
    status_only = "--status" in args
    positional = [a for a in args if not a.startswith("--")]
    if not positional:
        print("Usage: wake.py <project-root> [--pulse] [--status]", file=sys.stderr)
        return 2

    project_root = Path(positional[0]).resolve()
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

    print("MODE: PULSE" if pulse else "MODE: WAKING")
    print(f"Sanctum: {sanctum}")

    if status_only:
        mem_path = sanctum / "MEMORY.md"
        if mem_path.exists():
            content = mem_path.read_text(encoding="utf-8").rstrip()
            print(f"\n===== MEMORY.md (summary) =====")
            lines = content.split("\n")[:10]
            print("\n".join(lines))
            if len(content.split("\n")) > 10:
                print("...")
            print(f"\n--- {count_tokens(content)} tokens ---")
        return 0

    for name in IDENTITY_FILES:
        emit(sanctum / name)
    if pulse:
        emit(sanctum / "PULSE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
