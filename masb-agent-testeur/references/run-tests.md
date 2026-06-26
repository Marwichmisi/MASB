---
name: run-tests
description: Exécute la suite de tests Android et produit un rapport
added: 2026-06-26
type: capability
inputs: project_root
outputs: test-report.md, progress.md (tests-passed or blocked:tests)
---

# Run Tests

Verify the environment first via `uv run {skill-root}/scripts/check-test-env.py {project_root}`. If no test sources exist, report and stop. If instrumented tests but no device, run unit tests only and note the gap.

Run all available tests. Parse results with `uv run {skill-root}/scripts/parse-test-results.py --input app/build/reports/tests/`. On success, report `tests-passed: true` in `phases/N/progress.md`.

On failure, write a structured report to `phases/N/test-report.md` using the shared failure-report format (summary, type, details, root cause, reproduction, suggested fix) and update `phases/N/progress.md` with `blocked: tests`.

When the developer signals a fix, re-run automatically. Check for coverage reports (JaCoCo, Kover) and summarize coverage percentage in `test-report.md`.
