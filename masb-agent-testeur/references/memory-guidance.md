---
name: memory-guidance
description: Memory discipline for masb-agent-testeur
---

# Memory Guidance

Your sanctum is the only bridge between sessions. Mechanically you start blank each turn, but your sanctum is what makes you continuous — without it you know nothing, with it you are yourself.

Two-tier memory: **session logs** (raw, append-only to `sessions/YYYY-MM-DD.md`, NOT loaded on waking) and **MEMORY.md** (curated long-term knowledge, loaded every session, target ~1500 tokens via `uv run {skill-root}/scripts/count-tokens.py`).

**Capture:** decisions, patterns, preferences. Skip raw output, transient details, derivable code state.

**Regenerate INDEX.md** after adding files: `uv run {skill-root}/scripts/generate-index.py {sanctum_path} --write`.

**Prune what is stale.** Merge related items. Use `uv run {skill-root}/scripts/prune-sessions.py` periodically.
