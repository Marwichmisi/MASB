#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Read the state of a MASB phase from the project workspace.

Reads phases-index.md and the phase's progress.md and emits compact JSON
so the agent can reason over structured data instead of parsing raw markdown.

Usage:
    uv run read-phase-state.py <project-root> [phase-name]
    uv run read-phase-state.py <project-root> --list

    project-root: The root of the project (where masb-workspace/ lives)
    phase-name:   Optional phase name (e.g. "01-setup"). If omitted, reads the
                  active/next incomplete phase.
    --list:       List all phases with their numbers and status.

Exit codes:
    0 — success
    1 — MASB workspace not found
    2 — phase not found or phase-index invalid
"""

import json
import re
import sys
from pathlib import Path


def read_phases_index(workspace: Path) -> list[dict] | None:
    """Parse phases-index.md and return a list of phase entries."""
    index_path = workspace / "phases-index.md"
    if not index_path.exists():
        return None

    text = index_path.read_text(encoding="utf-8")
    phases = []
    # Match markdown list items like: - 01-setup: description (status)
    # or table rows
    for line in text.splitlines():
        line = line.strip()
        # Match: - 01-name or - **01**-name
        m = re.match(r"^[-*]\s+\*{0,2}(\d+)\*{0,2}[-:\s]+([a-zA-Z0-9_-]+)", line)
        if m:
            phases.append({
                "number": int(m.group(1)),
                "name": m.group(2),
                "raw_line": line,
            })
    return phases if phases else None


def read_progress(workspace: Path, phase_name: str) -> dict:
    """Read progress.md for a phase and extract review/tests status."""
    progress_path = workspace / "phases" / phase_name / "progress.md"
    result = {
        "phase": phase_name,
        "review_passed": None,
        "tests_passed": None,
        "blockers": [],
    }

    if not progress_path.exists():
        result["status"] = "not_started"
        return result

    text = progress_path.read_text(encoding="utf-8")
    result["status"] = "in_progress"

    rp = re.search(r"review-passed\s*:\s*(true|false)", text, re.IGNORECASE)
    if rp:
        result["review_passed"] = rp.group(1).lower() == "true"

    tp = re.search(r"tests-passed\s*:\s*(true|false)", text, re.IGNORECASE)
    if tp:
        result["tests_passed"] = tp.group(1).lower() == "true"

    # Extract blockers
    for b in re.finditer(r"blocked\s*:\s*(\w+)", text, re.IGNORECASE):
        result["blockers"].append(b.group(1))

    return result


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    project_root = Path(args[0]).resolve()
    workspace = project_root / "masb-workspace"
    list_only = "--list" in args

    if not workspace.is_dir():
        print(json.dumps({"status": "no_project", "error": "No MASB workspace found"}))
        return 1

    phases = read_phases_index(workspace)
    if phases is None:
        print(json.dumps({"status": "no_phases", "error": "No phases-index.md found or empty"}))
        return 2

    if list_only:
        print(json.dumps({"status": "ok", "phases": phases}, indent=2))
        return 0

    # Determine target phase
    positional = [a for a in args if not a.startswith("--")][1:]
    if positional:
        target = positional[0]
    else:
        # Find the first incomplete phase
        target = None
        for p in phases:
            prog = read_progress(workspace, f"{p['number']:02d}-{p['name']}")
            if prog.get("review_passed") is not True or prog.get("tests_passed") is not True:
                target = f"{p['number']:02d}-{p['name']}"
                break
        if target is None:
            # All complete
            print(json.dumps({
                "status": "all_done",
                "phases": phases,
                "message": "All phases are complete"
            }, indent=2))
            return 0

    progress = read_progress(workspace, target)
    # Find the phase index entry
    phase_info = next((p for p in phases if f"{p['number']:02d}-{p['name']}" == target), None)

    output = {
        "status": "ok",
        "phase": target,
        "phase_number": phase_info["number"] if phase_info else None,
        "review_passed": progress.get("review_passed"),
        "tests_passed": progress.get("tests_passed"),
        "blockers": progress.get("blockers", []),
        "phase_status": progress.get("status", "unknown"),
    }

    if phase_info:
        # Determine predecessor for dependency checking
        if phase_info["number"] > 1:
            output["depends_on"] = f"{phase_info['number'] - 1:02d}-completed"
        else:
            output["depends_on"] = None

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
