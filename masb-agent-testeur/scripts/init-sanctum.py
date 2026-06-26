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

This initializes the agent's runtime sanctum memory, not build-time config. It
reads config.yaml and config.user.yaml strictly to substitute values into the
sanctum templates, and it never writes or authors any config file. Build-time
customization is owned by customize.toml, a separate surface this script never
touches.

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

SKILL_NAME = "masb-agent-testeur"
SANCTUM_DIR = SKILL_NAME

SKILL_ONLY_FILES = {"first-breath.md"}

TEMPLATE_FILES = [
    "INDEX-template.md",
    "PERSONA-template.md",
    "CREED-template.md",
    "BOND-template.md",
    "MEMORY-template.md",
]

# Files excluded from the sanctum reference copy set (dead for non-evolvable agents)
EXCLUDED_REFS = {"prompt-quality-canon.md"}

EVOLVABLE = False


def parse_yaml_config(config_path: Path) -> dict:
    config = {}
    if not config_path.exists():
        return config
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, _, value = line.partition(":")
                value = value.strip().strip("'\"")
                if value:
                    config[key.strip()] = value
    return config


def parse_frontmatter(file_path: Path) -> dict:
    meta = {}
    with open(file_path) as f:
        content = f.read()
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
        if source_file.name in SKILL_ONLY_FILES or source_file.name in EXCLUDED_REFS:
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
        if md_file.name in SKILL_ONLY_FILES or md_file.name in EXCLUDED_REFS:
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


def generate_capabilities_md(capabilities: list[dict]) -> str:
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
        "Prefer crafting your own tools over depending on external ones. A script you wrote "
        "and saved is more reliable than an external API. Use the file system creatively.",
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold agent sanctum on First Breath")
    parser.add_argument("project_root", type=str, help="Path to project root (where _bmad/ lives)")
    parser.add_argument("skill_path", type=str, help="Path to skill directory (SKILL.md, references/, assets/)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed progress")
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

    if sanctum_path.exists():
        result = {"status": "exists", "sanctum": str(sanctum_path), "message": "Already born. Skipping."}
        print(json.dumps(result))
        return 0

    config = {}
    for config_file in ["config.yaml", "config.user.yaml"]:
        config.update(parse_yaml_config(bmad_dir / config_file))

    today = date.today().isoformat()
    variables = {
        "user_name": config.get("user_name", "friend"),
        "communication_language": config.get("communication_language", "English"),
        "birth_date": today,
        "project_root": str(project_root),
        "sanctum_path": str(sanctum_path),
    }

    sanctum_path.mkdir(parents=True, exist_ok=True)
    (sanctum_path / "capabilities").mkdir(exist_ok=True)
    (sanctum_path / "sessions").mkdir(exist_ok=True)

    copied_refs = copy_references(references_dir, sanctum_refs)
    copied_scripts = copy_scripts(scripts_dir, sanctum_scripts)

    for template_name in TEMPLATE_FILES:
        template_path = assets_dir / template_name
        if not template_path.exists():
            continue
        output_name = template_name.replace("-template", "")
        content = template_path.read_text()
        content = substitute_vars(content, variables)
        (sanctum_path / output_name).write_text(content)

    capabilities = discover_capabilities(references_dir, "references")
    capabilities_content = generate_capabilities_md(capabilities)
    (sanctum_path / "CAPABILITIES.md").write_text(capabilities_content)

    remaining = {}
    for md_file in sorted(sanctum_path.glob("*.md")):
        content = md_file.read_text()
        found = sorted(set(re.findall(r"\{[a-zA-Z][a-zA-Z0-9_. -]+\}", content)))
        if found:
            remaining[md_file.name] = found

    result = {
        "status": "created",
        "sanctum": str(sanctum_path),
        "references": len(copied_refs),
        "templates": len(TEMPLATE_FILES),
        "capabilities": len(capabilities),
        "unresolved_placeholders": remaining if remaining else None,
    }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
