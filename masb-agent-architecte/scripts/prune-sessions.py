#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

"""Prune session logs older than N days. Reports what was removed."""

import sys
import re
from datetime import date, timedelta
from pathlib import Path


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("Usage: prune-sessions.py <project-root> [--days 14]", file=sys.stderr)
        return 2

    project_root = Path(args[0]).resolve()
    max_days = 14
    if "--days" in args:
        idx = args.index("--days")
        if idx + 1 < len(args):
            max_days = int(args[idx + 1])

    sessions_dir = project_root / "_bmad" / "memory" / "masb-agent-architecte" / "sessions"
    if not sessions_dir.is_dir():
        print(f"No sessions directory at {sessions_dir}")
        return 0

    cutoff = date.today() - timedelta(days=max_days)
    removed = []

    for f in sorted(sessions_dir.iterdir()):
        if not f.is_file() or f.suffix not in (".md", ".txt"):
            continue
        match = re.search(r"(\d{4})-(\d{2})-(\d{2})", f.name)
        if not match:
            continue
        try:
            file_date = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            if file_date < cutoff:
                f.unlink()
                removed.append(f.name)
        except (ValueError, OSError) as e:
            print(f"  Warning: could not process {f.name}: {e}", file=sys.stderr)

    if removed:
        print(f"Pruned {len(removed)} session logs older than {max_days} days:")
        for name in removed:
            print(f"  - {name}")
    else:
        print(f"No session logs older than {max_days} days found.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
