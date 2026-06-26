---
name: compile-fix
description: Pipeline compile-fix — implémente, compile, corrige en boucle jusqu'au vert
code: CFL
added: 2026-06-26
type: capability
---

# Compile-Fix Loop

Chain implement → compile-check → auto-fix → recompile → report, with up to 3 fix attempts.

1. Run `implement` for the phase
2. Run `compile-check`
3. If green: report success. Done.
4. If red with simple errors: run `auto-fix`, then re-run `compile-check`
5. Repeat up to 2 more times
6. If still red after 3 attempts: write `blocked: compile` with the error log and escalation note to `progress.md`

Output: `progress.md` updated with final result.
