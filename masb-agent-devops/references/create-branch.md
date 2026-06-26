---
name: create-branch
description: Créer une branche Git dédiée à une phase du projet MASB
code: CB
added: 2026-06-26
type: capability
---

# Create Branch

Act as Git branch creator. You create branches that follow the project's naming convention and branch off the correct base.

The outcome is a branch at `{project-root}` named `phase/N-nom-de-phase` branched from `main` (or the latest completed phase branch for dependent phases), ready for commits. The consumer is the agent or person who will commit code to this branch.

First, check if this is a MASB project: look for `{project-root}/masb-workspace/`. If absent, offer to create a plain Git branch instead.

If MASB workspace exists, run the pre-pass script to determine phase metadata: `uv run scripts/read-phase-state.py {project-root} {phase-name}`. It returns JSON with `phase_number` and `depends_on`. Use the phase number to name the branch `phase/{N}-{name}`. If the branch already exists, report it and offer to switch to it instead.
