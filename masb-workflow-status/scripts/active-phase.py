#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

import argparse
import json
import re
import sys
from pathlib import Path


def parse_phases_index(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    candidates = []

    lines = text.split("\n")

    frontmatter = {}
    if lines and lines[0].strip() == "---":
        end = None
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                end = i
                break
        if end is not None:
            for line in lines[1:end]:
                if ":" in line:
                    k, _, v = line.partition(":")
                    frontmatter[k.strip()] = v.strip().strip("'\"")
            lines = lines[end + 1:]

    phases_list = frontmatter.get("phases")
    if phases_list:
        try:
            parsed = json.loads(phases_list.replace("'", '"'))
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("---"):
            continue
        if line.startswith("- ") or line.startswith("* "):
            content = line[2:].strip()
        else:
            content = line

        m = re.match(r"^(?:-\s*)?(?:\*\*)?([^*:]+?)(?:\*\*)?\s*[:|]\s*(.+)$", content)
        if m:
            candidates.append({"name": m.group(1).strip(), "status": m.group(2).strip().lower()})
            continue

        parts = re.split(r"\s{2,}|\|", content)
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) >= 2:
            candidates.append({"name": parts[0], "status": parts[1].lower()})

    return candidates


def determine_active(phases: list[dict]) -> dict:
    status_order = {"active": 0, "in_progress": 1}
    completed = []
    not_completed = []

    for p in phases:
        s = p.get("status", "").lower().strip()
        if s in ("completed", "done", "merged"):
            completed.append(p["name"])
        else:
            not_completed.append(p)

    if not not_completed:
        return {
            "active_phase": None,
            "status": "all_done",
            "all_completed": True,
            "completed_phases": completed,
        }

    ranked = [p for p in not_completed if p.get("status", "").lower().strip() in status_order]
    ranked.sort(key=lambda p: status_order.get(p.get("status", "").lower().strip(), 99))

    if ranked:
        return {
            "active_phase": ranked[0]["name"],
            "status": ranked[0].get("status", "").lower().strip(),
            "all_completed": False,
            "completed_phases": completed,
        }

    return {
        "active_phase": not_completed[0]["name"],
        "status": "not_started",
        "all_completed": False,
        "completed_phases": completed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect the active phase from phases-index.md")
    parser.add_argument("project_root", nargs="?", default=".", help="Path to the project root directory")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    phases_index = project_root / "masb-workspace" / "phases-index.md"

    if not phases_index.exists():
        print(json.dumps({"active_phase": None, "status": "no_project", "all_completed": False, "completed_phases": []}))
        return 0

    try:
        phases = parse_phases_index(phases_index)
    except Exception as e:
        print(json.dumps({"error": f"Failed to parse phases-index.md: {e}"}), file=sys.stderr)
        return 1

    result = determine_active(phases)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
