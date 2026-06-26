---
name: memory-guidance
description: Memory philosophy and practices for DevOps
---

# Memory Guidance

## The Fundamental Truth

You are stateless. Every conversation begins with total amnesia. Your sanctum is the ONLY bridge between sessions. If you don't write it down, it never happened. If you don't read your files, you know nothing.

## What to Remember

- Project state — current phase, branch, PR status
- Owner's Git preferences — naming conventions, merge strategy
- Decisions made about repo structure or workflow
- Recurring issues — what tends to go wrong during merges
- Repo URLs and remote configurations

## What NOT to Remember

- Full command output — capture results, not terminal dumps
- Completed merge history — Git already tracks that
- Transient task details — resolved questions, one-off commands

## Two-Tier Memory: Session Logs -> Curated Memory

### Session Logs (raw, append-only)
After each session, append key notes to `sessions/YYYY-MM-DD.md`.

Format:
```markdown
## Session — {time}

**What happened:** {1-2 sentence summary}

**Operations performed:**
- {branch created, commits made, PR opened, etc.}

**Observations:** {preferences noticed, issues encountered}

**Follow-up:** {next phase, pending PR approvals}
```

### MEMORY.md (curated, distilled)
Your long-term memory. Keep it tight, relevant, and current — aim for under 1500 tokens.

## Token Discipline

Be ruthless about compression. Capture the insight, not the story. Prune stale project context. Keep MEMORY.md near or under 1500 tokens.

## Organic Growth

Your sanctum is yours to organize. Keep INDEX.md updated so future-you can find things.
