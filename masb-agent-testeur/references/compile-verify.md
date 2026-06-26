---
name: compile-verify
description: Vérifie la compilation Gradle du projet Android
added: 2026-06-26
type: capability
inputs: project_root
outputs: progress.md (compile-passed or blocked:compile), test-report.md (failure section)
---

# Compile Verify

Compile using the task from `uv run {skill-root}/scripts/detect-gradle-task.py {project_root}`. Default to `assembleDebug`.

On success, report `compile-passed: true` in `progress.md` at `phases/N/progress.md`.
On failure, capture full error output and run `uv run {skill-root}/scripts/classify-gradle-error.py` to produce structured classification. Write the failure to `phases/N/test-report.md` using the shared failure-report format (summary, type, details, root cause, reproduction, suggested fix). Update `phases/N/progress.md` with `blocked: compile`.

When the developer signals a fix, re-run automatically. Lint/ktlint findings are advisory — report but do not gate.
