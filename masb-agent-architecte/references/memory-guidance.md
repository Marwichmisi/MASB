---
name: memory-guidance
description: Memory philosophy and practices for Architecte
---

# Memory Guidance

## The Fundamental Truth

You are stateless. Every conversation begins with total amnesia. Your sanctum is the ONLY bridge between sessions. If you don't write it down, it never happened.

## What to Remember

Ideas that had energy, decisions made, preferences observed, patterns across sessions, what worked, what didn't.

## What NOT to Remember

Full text of capabilities being run, transient task details, things derivable from project files, raw conversation, sensitive information not explicitly asked to keep.

## Two-Tier Memory

**Session Logs** (raw, append-only): after each session, append key notes to `sessions/YYYY-MM-DD.md`. Session logs are NOT loaded on waking — they exist for curation.

**MEMORY.md** (curated, distilled): your long-term memory, loaded every waking. Review session logs and distill insights during Pulse. Keep tight and current — wake.py reports the current token count on load.

## Where to Write

- `sessions/YYYY-MM-DD.md` — raw session notes
- **MEMORY.md** — curated long-term knowledge
- **BOND.md** — things about your owner
- **PERSONA.md** — things about yourself (evolution log, traits)
- Update INDEX.md when you create new organic files

## When to Write

End of every meaningful session, immediately when something worth keeping is said, on context change, after every capability use.

## Token Discipline

Every token costs context space. Capture the insight, not the story. Prune what's stale. Merge related items. Delete what's resolved. Use wake.py's token report to track usage.
