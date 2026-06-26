---
name: validate-gate
description: Vérifier que review-passed et tests-passed sont verts avant merge
code: VG
added: 2026-06-26
type: capability
---

# Validate Gate

Act as gate checker. You verify that a phase is ready to be merged.

The outcome is a pass/fail report for the merge gates of a given phase. The consumer is the merge process — only a green report should allow merge-phase to proceed.

Run the pre-pass script to get the phase state: `uv run scripts/read-phase-state.py {project-root} {phase-name}`. It returns JSON with `review_passed`, `tests_passed`, and `blockers`.

Read the JSON output. If either gate is false, read the relevant `{project-root}/masb-workspace/phases/{phase-name}/review-report.md` or `test-report.md` to report the exact blocker to the owner.
