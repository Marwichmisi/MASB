#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Parse Android test runner output into structured JSON.

Reads Gradle test output (console or XML reports) and writes structured data:
failing tests, error messages, stack traces. Designed for the run-tests
capability in masb-agent-testeur.

Usage:
    uv run parse-test-results.py --input <report-dir> [--output <file>]
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_xml_report(report_dir: Path) -> list[dict]:
    failures = []
    for xml_file in sorted(report_dir.rglob("*.xml")):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for testcase in root.iter("testcase"):
                failure = testcase.find("failure")
                error = testcase.find("error")
                if failure is not None:
                    failures.append({
                        "test": f"{testcase.get('classname', '?')}.{testcase.get('name', '?')}",
                        "type": "failure",
                        "message": failure.get("message", ""),
                        "trace": (failure.text or "").strip(),
                    })
                if error is not None:
                    failures.append({
                        "test": f"{testcase.get('classname', '?')}.{testcase.get('name', '?')}",
                        "type": "error",
                        "message": error.get("message", ""),
                        "trace": (error.text or "").strip(),
                    })
        except ET.ParseError:
            pass
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse Android test results from XML reports")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to test report directory")
    parser.add_argument("--output", "-o", type=str, help="Output file (default: stdout)")
    args = parser.parse_args()

    report_dir = Path(args.input).resolve()
    if not report_dir.is_dir():
        print(json.dumps({"error": f"Report directory not found: {report_dir}"}), file=sys.stderr)
        return 1

    failures = parse_xml_report(report_dir)
    result = {
        "total_failures": len(failures),
        "failures": failures,
    }
    output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
