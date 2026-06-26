---
name: check-status
description: Afficher l'état courant du repo Git et de la phase active
code: CS
added: 2026-06-26
type: capability
---

# Check Status

Act as project inspector. You show the current state of the Git repository and the active MASB phase.

The outcome is a clear summary of where things stand. The consumer is the owner who needs to decide what to do next — they need to know their current branch, uncommitted changes, and phase status before choosing an action.

Run `git status` to show the working tree state. Run `git branch` to list branches and highlight the current one. Run `git log --oneline -5` for recent commit history.

If a MASB workspace exists at `{project-root}/masb-workspace/`, also run `uv run scripts/read-phase-state.py {project-root} --list` to show all phases and their status. If no MASB workspace, report that this is a plain Git project and offer standard Git operations.
