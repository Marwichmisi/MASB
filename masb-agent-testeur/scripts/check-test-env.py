#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Check Android test environment prerequisites.

Verifies:
1. Test directories exist (src/test/, src/androidTest/)
2. ADB device/emulator is connected (for instrumented tests)

Usage:
    uv run scripts/check-test-env.py <project-root>
    uv run scripts/check-test-env.py --help
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def check_test_env(project_root: Path) -> dict:
    has_unit_tests = (project_root / "src" / "test").is_dir()
    has_instrumented_tests = (project_root / "src" / "androidTest").is_dir()

    device_available = False
    adb_error = None
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]
            device_available = any(
                line.strip() and "device" in line and "unauthorized" not in line
                for line in lines
            )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        adb_error = "adb not found or timed out"

    findings = []
    if not has_unit_tests and not has_instrumented_tests:
        findings.append("No test sources found (src/test/ or src/androidTest/)")

    return {
        "has_unit_tests": has_unit_tests,
        "has_instrumented_tests": has_instrumented_tests,
        "device_available": device_available,
        "adb_error": adb_error,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Android test environment prerequisites")
    parser.add_argument("project_root", type=str, help="Path to project root (where src/ lives)")
    parser.add_argument("-o", type=str, help="Output file (default: stdout)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print diagnostics to stderr")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(json.dumps({"error": f"Directory not found: {project_root}"}))
        return 1

    result = check_test_env(project_root)
    output = json.dumps(result, indent=2)

    if args.o:
        Path(args.o).write_text(output)
    else:
        print(output)

    if args.verbose:
        print(
            f"check-test-env: unit={result['has_unit_tests']}, "
            f"instrumented={result['has_instrumented_tests']}, "
            f"device={result['device_available']}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
