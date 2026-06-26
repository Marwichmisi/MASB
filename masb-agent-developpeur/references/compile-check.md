---
name: compile-check
description: Vérifie que le code compile avec Gradle
code: CC
added: 2026-06-26
type: capability
---

# Compile Check

Run `./gradlew assembleDebug`. On success, update `progress.md`. On failure, capture the error logs.

Never claim it compiles without running the actual build.
