#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

"""Validate phase folder structure and naming conventions after decompose."""

import sys
import re
from pathlib import Path


REQUIRED_FILES = {"spec.md", "progress.md"}
REQUIRED_DIRS = {"research", "code"}
PHASE_PATTERN = re.compile(r"^\d{2}-[a-z0-9-]+$")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("Usage: validate-phases.py <project-root>", file=sys.stderr)
        return 2

    project_root = Path(args[0]).resolve()
    phases_dir = project_root / "masb-workspace" / "phases"

    if not phases_dir.is_dir():
        print(f"No phases directory at {phases_dir}")
        return 0

    issues = []

    for phase_dir in sorted(phases_dir.iterdir()):
        if not phase_dir.is_dir():
            continue
        name = phase_dir.name

        if not PHASE_PATTERN.match(name):
            issues.append(f"  {name}: name does not follow NN-description-courte pattern")

        for req_file in REQUIRED_FILES:
            if not (phase_dir / req_file).is_file():
                issues.append(f"  {name}: missing required file: {req_file}")

        for req_dir in REQUIRED_DIRS:
            if not (phase_dir / req_dir).is_dir():
                issues.append(f"  {name}: missing required directory: {req_dir}/")

    if issues:
        print(f"Phase validation issues ({len(issues)}):")
        for issue in issues:
            print(issue)
        return 1
    else:
        print("All phases pass validation.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
