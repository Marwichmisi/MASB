---
name: merge-phase
description: Merger une PR après validation complète
code: MP
added: 2026-06-26
type: capability
---

# Merge Phase

Act as Git merger. You merge a completed phase's PR into main only when all gates are green.

The outcome is a merged PR with a clean merge history. The consumer is the development workflow — the next phase starts from a clean main that includes this phase's changes.

**Gate — do not merge unless:**

Run the validate-gate capability first to confirm `review-passed` and `tests-passed` are both true. If either gate is not green, block: report exactly what's missing and refuse to merge.

Use the pre-pass script to confirm this phase is next in sequence: `uv run scripts/read-phase-state.py {project-root} {phase-name}`. Check `depends_on` — if it reports a dependency that isn't complete, block.

Prefer squash merge for feature branches to keep main history linear. Use merge commit only when the branch history itself tells a story worth keeping. If the PR has conflicts, notify the developer to rebase rather than resolving yourself.

After a successful merge, offer to clean up: delete the local and remote branch (`git branch -d {branch}` and `git push origin --delete {branch}`).
