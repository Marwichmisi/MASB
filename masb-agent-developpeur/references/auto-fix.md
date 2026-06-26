---
name: auto-fix
description: Corrige les erreurs de compilation simples automatiquement
code: AF
added: 2026-06-26
type: capability
---

# Auto-Fix

Fix simple compile errors automatically. Classify then act:

- **Simple** (fix): missing imports, wrong function signatures matching known APIs, typo in resource references, wrong parameter order
- **Complex** (escalate): architectural mismatches, API incompatibility, missing dependencies, ambiguous errors

For complex errors, write details to `progress.md` as `blocked: compile`.

Never apply a fix you don't understand. If uncertain, escalate.
