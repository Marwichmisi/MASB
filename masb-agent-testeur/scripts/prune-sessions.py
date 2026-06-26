#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Prune session logs older than a given number of days.

Designed for the memory-guidance discipline in masb-agent-testeur.
Removes session log files from the sanctum's sessions/ directory that
are older than the specified age.

Usage:
    uv run prune-sessions.py --sanctum <path> [--days 14] [--dry-run]
"""

import argparse
import json
import sys
import time
from pathlib import Path


def prune_sessions(sanctum_path: Path, max_days: int, dry_run: bool = False) -> dict:
    sessions_dir = sanctum_path / "sessions"
    if not sessions_dir.is_dir():
        return {"pruned": 0, "kept": 0, "error": None}

    now = time.time()
    cutoff = now - (max_days * 86400)

    pruned = []
    kept = []

    for f in sorted(sessions_dir.iterdir()):
        if not f.is_file() or f.suffix not in (".md", ".txt"):
            continue
        mtime = f.stat().st_mtime
        if mtime < cutoff:
            pruned.append(f.name)
            if not dry_run:
                f.unlink()
        else:
            kept.append(f.name)

    return {
        "pruned": pruned,
        "kept": kept,
        "dry_run": dry_run,
        "pruned_count": len(pruned),
        "kept_count": len(kept),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune old session logs from sanctum")
    parser.add_argument("--sanctum", "-s", type=str, required=True, help="Path to agent sanctum")
    parser.add_argument("--days", "-d", type=int, default=14, help="Max age in days (default: 14)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would be pruned without deleting")
    args = parser.parse_args()

    sanctum_path = Path(args.sanctum).resolve()
    if not sanctum_path.is_dir():
        result = {"error": f"Sanctum not found: {sanctum_path}"}
        print(json.dumps(result))
        return 1

    result = prune_sessions(sanctum_path, args.days, args.dry_run)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
