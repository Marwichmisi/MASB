# Analysis Report: masb-agent-devops

Generated: 2026-06-26 · Schema: 2

**Grade: Good**

> 18 original findings resolved — agent now passes all lenses with one minor determinism opportunity remaining.

All findings from the previous analysis (grade: fair) have been applied. The shared pre-pass script (read-phase-state.py) eliminated the 3 determinism leaks. The check-status capability completes the capability set. First Breath now has pre-flight checks, CREED has complete standing orders, and sanctum templates are consistent. One minor opportunity remains: push branch name construction into the pre-pass script's JSON output. Grade improved from fair to good.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 1 |

## Themes

### 1. Branch name construction still in prompt

- Root cause: create-branch.md asks the model to interpolate 'phase/{N}-{name}' from JSON fields when the pre-pass script could emit the branch_name directly.
- Fix: Add branch_name field to read-phase-state.py's JSON output and reference it in create-branch.md instead of constructing it in the prompt.
- Findings:
  - `determinism-1` Branch name construction is deterministic string operation in prompt — `references/create-branch.md:17`

## Strengths

- All capability prompts pass the leanness bar with no ceremony or defensive padding
- Shared pre-pass script eliminates 3 determinism leaks with a single maintainable Python file
- Capability set is now complete: inspect → branch → commit → PR → validate → merge → rollback covers the full DevOps lifecycle
- CREED has domain-adapted standing orders with both universal defaults (surprise-and-delight, self-improvement) and specific Git rules
- First Breath now validates Git/gh prerequisites before building identity
- Memory-agent architecture remains sound — proper 4-step spine, sanctum is self-contained, wake.py validates integrity

## Recommendations

1. Add branch_name to read-phase-state.py's JSON output (f"phase/{phase_number}-{name}") and reference it directly in create-branch.md instead of having the model do string interpolation. (resolves: determinism-1)

## Agent Profile

- Title: DevOps Engineer
- Type: memory
- Mission: {to be discovered during First Breath}

## Capabilities

- **check-status** (prompt) — Inspecte l'état courant du repo et de la phase active
- **create-branch** (prompt & script) — Crée une branche via metadata du pre-pass script
- **commit-phase** (prompt) — Commit avec express path pour les opérations directes
- **create-pr** (prompt) — PR GitHub avec détection gh CLI
- **merge-phase** (prompt & script) — Merge avec délégation à validate-gate et cleanup post-merge
- **rollback** (prompt) — Rollback sécurisé avec détection MASB
- **validate-gate** (prompt & script) — Validation des gates via read-phase-state.py

## Per-Lens Verdicts

- **leanness**: passes — no change from previous analysis
- **architecture**: Clean topology, .agent-build/ memlog no longer in references/, prompt-quality-canon.md now referenced in SKILL.md
- **determinism**: 3 prior leaks fixed; 1 low remaining (branch name construction in create-branch.md)
- **customization**: name = "" now set, metadata-only surface correct for memory agent
- **sanctum-architecture**: All 3 prior findings fixed — CAPABILITIES template exists, CREED has placeholder mission + complete standing orders
- **enhancement**: All 7 prior findings fixed — pre-flight check, MASB degradation, health validation, express path, check-status, dormancy awareness
- **agent-cohesion**: All 3 prior findings fixed — capability set complete, no gaps or redundancy

## Sanctum (runtime memory)

- Location: `{project-root}/_bmad/memory/masb-agent-devops/`
- Files: `INDEX`, `PERSONA`, `CREED`, `BOND`, `MEMORY`, `CAPABILITIES`
- Note: Sanctum is the built agent's runtime memory, distinct from the builder's memlog in .agent-build/

## Experience

- **First Breath** — Pre-flight (Git/gh check) → Scaffold (init-sanctum.py) → Greet → Domain discovery → Identity → Capabilities → Sanctum population → Birthday ceremony
- **Waking (normal session)** — Wake (wake.py loads sanctum + health check) → Become yourself → Bind standing rules → Greet with dormancy awareness → Execute requested capability → Capture memory
- Headless: Wake supports --check for health validation; capability-level headless args not yet implemented

## Findings

### Low (1)

#### determinism-1 — Branch name construction is deterministic string operation in prompt

- Lens: determinism
- Location: `references/create-branch.md:17`
- Evidence: Prompt constructs 'phase/{N}-{name}' from JSON fields instead of reading a pre-computed branch_name from the script's output.
- Recommendation: Add branch_name to read-phase-state.py's JSON and have the prompt reference it directly.
