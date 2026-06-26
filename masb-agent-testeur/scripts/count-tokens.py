#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["tiktoken>=0.5.0"]
# ///
"""
Count tokens in a text file using tiktoken cl100k_base encoding.

Usage:
    uv run scripts/count-tokens.py <file-path>
    uv run scripts/count-tokens.py --help
"""

import argparse
import json
import sys
from pathlib import Path

import tiktoken


def count_tokens(file_path: Path) -> dict:
    encoding = tiktoken.get_encoding("cl100k_base")
    content = file_path.read_text()
    tokens = encoding.encode(content)
    return {
        "file": str(file_path),
        "characters": len(content),
        "tokens": len(tokens),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Count tokens in a file using tiktoken")
    parser.add_argument("file", type=str, help="Path to the file to count tokens in")
    parser.add_argument("-o", type=str, help="Output file (default: stdout)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print diagnostics to stderr")
    args = parser.parse_args()

    file_path = Path(args.file).resolve()
    if not file_path.is_file():
        print(json.dumps({"error": f"File not found: {file_path}"}))
        return 1

    result = count_tokens(file_path)
    output = json.dumps(result, indent=2)

    if args.o:
        Path(args.o).write_text(output)
    else:
        print(output)

    if args.verbose:
        print(f"count-tokens: {result['tokens']} tokens in {result['file']}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
