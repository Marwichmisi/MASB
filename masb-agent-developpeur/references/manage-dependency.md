---
name: manage-dependency
description: Ajoute ou met à jour une dépendance Gradle dans le projet
code: DEP
added: 2026-06-26
type: capability
---

# Manage Dependency

Add or update a Gradle dependency. Works with the project's `build.gradle.kts` or `libs.versions.toml`.

1. Detect which dependency format the project uses (version catalog or direct)
2. Add the dependency with the appropriate version notation
3. Run `compile-check` to verify the dependency resolves
4. If resolution fails, rollback the change and report the error

Output: Dependency added or rollback report in `progress.md`.
