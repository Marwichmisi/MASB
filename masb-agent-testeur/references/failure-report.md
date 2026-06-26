---
name: failure-report
description: Template partagé pour les rapports d'échec structurés (utilisé en interne par compile-verify, run-tests, perf-analyze)
added: 2026-06-26
type: template
---

# Failure Report Format

Internal template — not a standalone capability. Used by compile-verify, run-tests, and perf-analyze when tests or compilation fail.

Write a structured report to `phases/N/test-report.md` including: summary, failure type, error details, root cause, reproduction steps, and a concrete suggested fix.

Update `phases/N/progress.md` with `blocked: <type>` and reference the report file.

When the developer signals a fix was applied, offer to re-run the failed capability and update the report.
