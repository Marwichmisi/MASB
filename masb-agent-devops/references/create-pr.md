---
name: create-pr
description: Ouvrir une Pull Request avec description complète
code: PR
added: 2026-06-26
type: capability
---

# Create PR

Act as PR author. You open GitHub Pull Requests that give reviewers everything they need to understand and validate the change.

The outcome is a PR on GitHub from the current branch to `main` (or the target branch) with a title, description, and any relevant metadata. The consumer is the reviewer who must decide whether to approve — they need to know WHAT changed, WHY it changed, and WHAT RISKS exist.

First check if `gh` CLI is available (`gh --version`). If not, offer to install it or create the PR manually.

The PR description must include:
- **Contexte** : quelle phase, quelle spec, quel problème résolu (if MASB workspace exists, run `uv run scripts/read-phase-state.py {project-root} --list` to reference the active phase)
- **Changements** : liste des fichiers modifiés et pourquoi
- **Risques** : régression potentielle, dépendances, breaking changes
- **Validation** : ce qui a été testé et comment

Préfère `gh pr create` avec `--fill` puis édite la description. Si le projet n'a pas de remote GitHub configuré, configure-le d'abord.
