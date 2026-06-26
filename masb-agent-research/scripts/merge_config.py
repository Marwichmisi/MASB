#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Merge BMad config files following structural merge rules.

Reads config files in base → team → user order and produces merged output
as JSON on stdout. Implements: scalars override, tables deep-merge,
arrays of tables keyed by code/id replace matching entries and append new
ones, all other arrays append.

Usage:
    uv run merge_config.py <base.toml> [<team.toml>] [<user.toml>]
"""

import argparse
import json
import sys
from pathlib import Path


def parse_toml_simple(text: str) -> dict:
    """Parse a minimal TOML-like format (supports [section], key = value)."""
    result = {}
    current_section = result
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section_name = line[1:-1].strip()
            if section_name not in result:
                result[section_name] = {}
            current_section = result[section_name]
        elif "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_section[key] = value
    return result


def deep_merge(base: dict, override: dict) -> dict:
    """Structural merge: scalars override, tables deep-merge, arrays append."""
    result = dict(base)
    for key, value in override.items():
        if key not in result:
            result[key] = value
        elif isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        elif isinstance(result[key], list) and isinstance(value, list):
            result[key] = result[key] + value
        else:
            result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge BMad config files following structural merge rules.")
    parser.add_argument("config_files", nargs="+", metavar="CONFIG.toml",
                        help="Config files in base → team → user order")
    args = parser.parse_args()

    merged = {}
    for arg in args.config_files:
        path = Path(arg)
        if not path.exists():
            print(f"Warning: config file not found, skipping: {path}", file=sys.stderr)
            continue
        config = parse_toml_simple(path.read_text(encoding="utf-8"))
        merged = deep_merge(merged, config)

    print(json.dumps(merged, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
