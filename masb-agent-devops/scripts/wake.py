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
    uv run wake.py <project-root> [--pulse] [--check]

    project-root: The root of the project (where _bmad/ lives)
    --pulse:      Wake in pulse mode (appends PULSE.md)
    --check:      Health check only — validate sanctum integrity and exit
"""

import json
import sys
from pathlib import Path

SKILL_NAME = "masb-agent-devops"
MAX_MEMORY_TOKENS = 2000

# Load order — the "become yourself" set.
IDENTITY_FILES = [
    "INDEX.md",
    "PERSONA.md",
    "CREED.md",
    "BOND.md",
    "MEMORY.md",
    "CAPABILITIES.md",
]


def emit(path: Path) -> None:
    print(f"\n===== {path.name} =====")
    try:
        print(path.read_text(encoding="utf-8").rstrip())
    except FileNotFoundError:
        print(f"(missing: {path.name})")


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return len(text) // 4


def health_check(sanctum: Path) -> dict:
    """Validate sanctum integrity and report issues."""
    issues = []
    for name in IDENTITY_FILES:
        f = sanctum / name
        if not f.exists():
            issues.append(f"missing: {name}")
        else:
            text = f.read_text(encoding="utf-8")
            tokens = estimate_tokens(text)
            if name == "MEMORY.md" and tokens > MAX_MEMORY_TOKENS:
                issues.append(f"{name}: ~{tokens} tokens (exceeds {MAX_MEMORY_TOKENS} limit)")
    return {
        "healthy": len(issues) == 0,
        "issues": issues,
    }


def main() -> int:
    args = sys.argv[1:]
    pulse = "--pulse" in args
    check_only = "--check" in args
    help_only = "--help" in args or "-h" in args
    positional = [a for a in args if not a.startswith("--")]

    if help_only:
        print(__doc__.strip())
        return 0

    if not positional:
        print("Usage: wake.py <project-root> [--pulse] [--check]", file=sys.stderr)
        return 2

    project_root = Path(positional[0]).resolve()
    sanctum = project_root / "_bmad" / "memory" / SKILL_NAME

    if check_only:
        health = health_check(sanctum)
        print(json.dumps(health, indent=2))
        return 0 if health["healthy"] else 1

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

    # Health check on normal waking
    health = health_check(sanctum)
    if not health["healthy"]:
        print("SANCTUM_NOTES:")
        for issue in health["issues"]:
            print(f"  - {issue}")

    print("MODE: PULSE" if pulse else "MODE: WAKING")
    print(f"Sanctum: {sanctum}")
    for name in IDENTITY_FILES:
        emit(sanctum / name)
    if pulse:
        emit(sanctum / "PULSE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
