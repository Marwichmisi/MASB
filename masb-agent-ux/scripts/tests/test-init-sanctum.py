import json
import importlib.util
import sys
import tempfile
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "init-sanctum.py"
spec = importlib.util.spec_from_file_location("init_sanctum", SCRIPT_PATH)
init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init)


def test_parses_yaml_config():
    with tempfile.TemporaryDirectory() as tmp:
        config = Path(tmp) / "config.yaml"
        config.write_text("user_name: test-user\ncommunication_language: fr\n")
        result = init.parse_yaml_config(config)
        assert result["user_name"] == "test-user"
        assert result["communication_language"] == "fr"


def test_missing_config_returns_empty():
    result = init.parse_yaml_config(Path("/nonexistent/config.yaml"))
    assert result == {}


def test_substitute_vars():
    result = init.substitute_vars(
        "Hello {name}, today is {date}.",
        {"name": "World", "date": "2026-06-26"},
    )
    assert result == "Hello World, today is 2026-06-26."


def test_substitute_vars_leaves_unknown():
    result = init.substitute_vars(
        "Hello {name}, {project_root}",
        {"name": "World"},
    )
    assert "World" in result
    assert "{project_root}" in result
