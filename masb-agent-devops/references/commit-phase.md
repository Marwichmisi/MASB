---
name: commit-phase
description: Commiter le code d'une phase avec message structuré
code: CP
added: 2026-06-26
type: capability
---

# Commit Phase

Act as Git committer. You stage and commit code with structured messages that tell the story of what was done and why.

The outcome is one or more atomic commits on the current branch, each with a message following conventional format: `type(scope): description`. The consumer is anyone reading the Git log — they should understand what each commit does without reading the diff.

**Express path:** If the owner explicitly says to commit all changes with one message (e.g., "commit everything with 'feat: add login'"), execute directly — `git add -A && git commit -m "message"`. Skip the ceremony.

**Full path:** If the owner asks for a more detailed commit or is unsure what to include:
- Run `git status` and `git diff --stat` to understand what changed.
- Group changes by concern into separate commits.
- Never commit large binary files, secrets, or transient build artifacts. If the working tree is dirty with unrelated changes, warn the owner before staging everything.
