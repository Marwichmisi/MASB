#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
First Breath — Deterministic sanctum scaffolding.

This script runs BEFORE the conversational awakening. It creates the sanctum
folder structure, copies template files with config values substituted,
copies all capability files and their supporting references into the sanctum,
and auto-generates CAPABILITIES.md from capability prompt frontmatter.

After this script runs, the sanctum is fully self-contained — the agent does
not depend on the skill bundle location for normal operation.

Usage:
    uv run init-sanctum.py <project-root> <skill-path>
"""

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

SKILL_NAME = "masb-agent-research"
SANCTUM_DIR = SKILL_NAME

SKILL_ONLY_FILES = {"first-breath.md"}

TEMPLATE_FILES = [
    "INDEX-template.md",
    "PERSONA-template.md",
    "CREED-template.md",
    "BOND-template.md",
    "MEMORY-template.md",
    "CAPABILITIES-template.md",
]

EVOLVABLE = False


def parse_frontmatter(file_path: Path) -> dict:
    meta = {}
    content = file_path.read_text()
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return meta
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("'\"")
    return meta


def copy_references(source_dir: Path, dest_dir: Path) -> list[str]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for source_file in sorted(source_dir.iterdir()):
        if source_file.name in SKILL_ONLY_FILES:
            continue
        if source_file.is_file():
            shutil.copy2(source_file, dest_dir / source_file.name)
            copied.append(source_file.name)
    return copied


def copy_scripts(source_dir: Path, dest_dir: Path) -> list[str]:
    if not source_dir.exists():
        return []
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for source_file in sorted(source_dir.iterdir()):
        if source_file.is_file() and source_file.name != "init-sanctum.py":
            shutil.copy2(source_file, dest_dir / source_file.name)
            copied.append(source_file.name)
    return copied


def discover_capabilities(references_dir: Path, sanctum_refs_path: str) -> list[dict]:
    capabilities = []
    for md_file in sorted(references_dir.glob("*.md")):
        if md_file.name in SKILL_ONLY_FILES:
            continue
        meta = parse_frontmatter(md_file)
        if meta.get("name") and meta.get("code"):
            capabilities.append({
                "name": meta["name"],
                "description": meta.get("description", ""),
                "code": meta["code"],
                "source": f"{sanctum_refs_path}/{md_file.name}",
            })
    return capabilities


def generate_capabilities_md(capabilities: list[dict], evolvable: bool) -> str:
    lines = [
        "# Capabilities",
        "",
        "## Built-in",
        "",
        "| Code | Name | Description | Source |",
        "|------|------|-------------|--------|",
    ]
    for cap in capabilities:
        lines.append(
            f"| [{cap['code']}] | {cap['name']} | {cap['description']} | `{cap['source']}` |"
        )
    lines.extend([
        "",
        "## Tools",
        "",
        "Prefer crafting your own tools over depending on external ones.",
        "",
        "### User-Provided Tools",
        "",
        "_MCP servers, APIs, or services the owner has made available. Document them here._",
    ])
    return "\n".join(lines) + "\n"


def substitute_vars(content: str, variables: dict) -> str:
    for key, value in variables.items():
        content = content.replace(f"{{{key}}}", value)
    return content


def scan_placeholders(content: str) -> list[str]:
    return sorted(set(re.findall(r"\{[a-zA-Z_][a-zA-Z0-9_.-]*\}", content)))


def main():
    parser = argparse.ArgumentParser(description="Scaffold agent sanctum for First Breath")
    parser.add_argument("project_root", help="Path to the project root (where _bmad/ lives)")
    parser.add_argument("skill_path", help="Path to the skill directory (where SKILL.md lives)")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    skill_path = Path(args.skill_path).resolve()

    bmad_dir = project_root / "_bmad"
    memory_dir = bmad_dir / "memory"
    sanctum_path = memory_dir / SANCTUM_DIR
    assets_dir = skill_path / "assets"
    references_dir = skill_path / "references"
    scripts_dir = skill_path / "scripts"

    sanctum_refs = sanctum_path / "references"
    sanctum_scripts = sanctum_path / "scripts"
    sanctum_refs_path = "references"

    if sanctum_path.exists():
        print(json.dumps({"status": "exists", "sanctum": str(sanctum_path), "message": "Already born. Skipping."}))
        sys.exit(0)

    today = date.today().isoformat()
    variables = {
        "user_name": "friend",
        "communication_language": "English",
        "birth_date": today,
        "project_root": str(project_root),
        "sanctum_path": str(sanctum_path),
    }

    sanctum_path.mkdir(parents=True, exist_ok=True)
    (sanctum_path / "capabilities").mkdir(exist_ok=True)
    (sanctum_path / "sessions").mkdir(exist_ok=True)

    copied_refs = copy_references(references_dir, sanctum_refs)
    copied_scripts = copy_scripts(scripts_dir, sanctum_scripts)

    created_templates = []
    for template_name in TEMPLATE_FILES:
        template_path = assets_dir / template_name
        if not template_path.exists():
            continue
        output_name = template_name.replace("-template", "").upper()[:-3] + ".md"
        content = template_path.read_text()
        content = substitute_vars(content, variables)
        output_path = sanctum_path / output_name
        output_path.write_text(content)
        created_templates.append(output_name)

    # Post-process: scan and log remaining placeholders
    all_text = ""
    for output_name in created_templates:
        output_path = sanctum_path / output_name
        all_text += f"\n=== {output_name} ===\n" + output_path.read_text()
    remaining = scan_placeholders(all_text)
    if remaining:
        print(f"  Placeholders remaining: {', '.join(remaining)}")

    capabilities = discover_capabilities(references_dir, sanctum_refs_path)
    caps_content = generate_capabilities_md(capabilities, evolvable=EVOLVABLE)
    (sanctum_path / "CAPABILITIES.md").write_text(caps_content)

    result = {
        "status": "created",
        "sanctum": str(sanctum_path),
        "references_copied": copied_refs,
        "templates_created": created_templates,
        "capabilities_discovered": len(capabilities),
        "placeholders_remaining": remaining if remaining else [],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
