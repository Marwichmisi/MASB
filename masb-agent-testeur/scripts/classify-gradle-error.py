#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Classify Gradle compilation errors by pattern-matching known signatures.

Usage:
    uv run scripts/classify-gradle-error.py <error-file>
    uv run scripts/classify-gradle-error.py --help
"""

import argparse
import json
import re
import sys
from pathlib import Path

SIMPLE_PATTERNS = [
    r"unresolved reference",
    r"unresolved symbol",
    r"cannot find symbol",
    r"unclosed string literal",
    r"expecting",
    r"Type mismatch",
    r"None of the following functions",
    r"is not valid",
    r"Unresolved reference",
    r"unused.*import",
    r"must not be null",
    r"Only.*is allowed",
    r"doesn't match",
]

COMPLEX_PATTERNS = [
    r"Conflict[s]? with",
    r"dependency.*conflict",
    r"Failed to resolve",
    r"Could not determine.*dependencies",
    r"SDK.*version",
    r"compileSdk.*not found",
    r"targetSdk",
    r"AGP",
    r"gradle.*version",
    r"incompatible.*version",
    r"Plugin.*version",
    r"Unresolved dependency",
    r"Could not resolve all",
    r"Kotlin.*version.*incompatible",
    r"Unsupported class file major version",
    r"FAILURE: Build failed with an exception",
]


def classify_error(error_text: str) -> dict:
    for pattern in COMPLEX_PATTERNS:
        if re.search(pattern, error_text, re.IGNORECASE):
            return {
                "category": "complex",
                "matched_pattern": pattern,
                "suggestion": "Check dependency versions, AGP compatibility, and SDK configuration",
            }

    for pattern in SIMPLE_PATTERNS:
        if re.search(pattern, error_text, re.IGNORECASE):
            return {
                "category": "simple",
                "matched_pattern": pattern,
                "suggestion": "Fix the referenced symbol, import, or syntax issue",
            }

    return {
        "category": "unclassified",
        "matched_pattern": None,
        "suggestion": "Review the full error output",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify Gradle compilation errors")
    parser.add_argument("error_file", nargs="?", type=str, help="Path to file containing error output (reads from stdin if omitted)")
    parser.add_argument("-o", type=str, help="Output file (default: stdout)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print diagnostics to stderr")
    args = parser.parse_args()

    if args.error_file:
        path = Path(args.error_file)
        if not path.is_file():
            print(json.dumps({"error": f"File not found: {path}"}))
            return 1
        error_text = path.read_text()
    else:
        error_text = sys.stdin.read()

    result = classify_error(error_text)
    output = json.dumps(result, indent=2)

    if args.o:
        Path(args.o).write_text(output)
    else:
        print(output)

    if args.verbose:
        print(f"classify-gradle-error: {result['category']}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
