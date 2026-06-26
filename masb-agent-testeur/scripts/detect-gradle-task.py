#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Detect the correct Gradle assemble task for an Android project.

Reads settings.gradle.kts, counts include() declarations, and outputs
which module task to use: `assembleDebug` for single-module,
`:app:assembleDebug` for multi-module (when :app is present).

Usage:
    uv run scripts/detect-gradle-task.py <project-root>
    uv run scripts/detect-gradle-task.py --help
"""

import argparse
import json
import re
import sys
from pathlib import Path


def find_settings_dir(root: Path) -> Path | None:
    for candidate in [root, root / "app"]:
        if (candidate / "settings.gradle.kts").exists():
            return candidate
    return None


def detect_gradle_task(project_root: Path) -> dict:
    settings_dir = find_settings_dir(project_root)
    if not settings_dir:
        return {
            "task": "assembleDebug",
            "module": None,
            "multi_module": False,
            "warning": "No settings.gradle.kts found; defaulting to assembleDebug",
        }

    content = (settings_dir / "settings.gradle.kts").read_text()
    includes = re.findall(r'include\(\s*["\'](:[^"\']+)["\']\s*\)', content)
    includes += re.findall(r'include\s+["\'](:[^"\']+)["\']', content)
    includes += re.findall(r'include\s+\(\s*["\'](:[^"\']+)["\']\s*\)', content)

    modules = [inc for inc in includes if inc.startswith(":")]
    module_count = len(modules)

    if module_count <= 1:
        return {"task": "assembleDebug", "module": None, "multi_module": False}

    app_present = any(m.endswith(":app") for m in modules)
    if app_present:
        return {"task": ":app:assembleDebug", "module": ":app", "multi_module": True}

    return {
        "task": f"{modules[0]}:assembleDebug",
        "module": modules[0],
        "multi_module": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect Gradle assemble task for an Android project")
    parser.add_argument("project_root", type=str, help="Path to project root")
    parser.add_argument("-o", type=str, help="Output file (default: stdout)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print diagnostics to stderr")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(json.dumps({"error": f"Directory not found: {project_root}"}))
        return 1

    result = detect_gradle_task(project_root)
    output = json.dumps(result)

    if args.o:
        Path(args.o).write_text(output)
    else:
        print(output)

    if args.verbose:
        print(f"detect-gradle-task: {result['task']}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
