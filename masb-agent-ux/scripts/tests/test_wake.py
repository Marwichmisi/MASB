import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import wake


def test_first_breath_when_no_sanctum():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        result = wake.main(["wake.py", str(project)])
        assert result == 0


def test_waking_mode_with_sanctum():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        sanctum = project / "_bmad" / "memory" / "masb-agent-ux"
        sanctum.mkdir(parents=True)
        (sanctum / "CREED.md").write_text("# Creed")
        (sanctum / "MEMORY.md").write_text("# Memory")
        for f in ["INDEX.md", "PERSONA.md", "BOND.md", "CAPABILITIES.md"]:
            (sanctum / f).write_text(f"# {f}")

        result = wake.main(["wake.py", str(project)])
        assert result == 0


def test_waking_mode_returns_json():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        sanctum = project / "_bmad" / "memory" / "masb-agent-ux"
        sanctum.mkdir(parents=True)
        (sanctum / "CREED.md").write_text("# Creed")
        (sanctum / "MEMORY.md").write_text("# Memory")
        (sanctum / "INDEX.md").write_text("# Index")
        (sanctum / "PERSONA.md").write_text("# Persona")
        (sanctum / "BOND.md").write_text("# Bond")
        (sanctum / "CAPABILITIES.md").write_text("# Capabilities")

        result = wake.main(["wake.py", str(project)])
        assert result == 0


def test_pulse_flag():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        sanctum = project / "_bmad" / "memory" / "masb-agent-ux"
        sanctum.mkdir(parents=True)
        (sanctum / "CREED.md").write_text("# Creed")
        (sanctum / "MEMORY.md").write_text("# Memory")
        (sanctum / "INDEX.md").write_text("# Index")
        (sanctum / "PERSONA.md").write_text("# Persona")
        (sanctum / "BOND.md").write_text("# Bond")
        (sanctum / "CAPABILITIES.md").write_text("# Capabilities")

        result = wake.main(["wake.py", str(project), "--pulse"])
        assert result == 0
