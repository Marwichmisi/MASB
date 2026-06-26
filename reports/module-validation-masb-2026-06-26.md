# Validation Report — masb (Marwane Android Spec Builder)

**Date:** 2026-06-26
**Module:** masb
**Path:** `/home/marwane/Documents/momono/skills`
**Status:** FAIL

---

## Structural Issues

### HIGH — Duplicate Menu Code `CP`

| Line | Skill | Display Name | Current Code | Suggested Fix |
|------|-------|-------------|-------------|---------------|
| 14 | masb-agent-developpeur | Compile Check | CP | keep CP |
| 25 | masb-agent-devops | Create PR | CP | change to **CR** |

### MEDIUM — Extra Commas in CSV (7 rows)

Rows where `preceded-by` and `followed-by` are both empty: pattern has `,,,,false` instead of `,,,false`.

| Row | Skill | Entry | Fix |
|-----|-------|-------|-----|
| 6 | masb-agent-architecte | Replan | `1-vision,,,,false` → `1-vision,,,false` |
| 9 | masb-agent-research | Vérifier Approche | `2-research,,,,false` → `2-research,,,false` |
| 12 | masb-agent-ux | Accessibilité | `3-design,,,,false` → `3-design,,,false` |
| 22 | masb-agent-testeur | Failure Report | `6-test,,,,false` → `6-test,,,false` |
| 27 | masb-agent-devops | Rollback | `7-devops,,,,false` → `7-devops,,,false` |
| 28 | masb-agent-devops | Validate Gate | `7-devops,,,,false` → `7-devops,,,false` |
| 29 | masb-workflow-status | Status | `0-status,,,,false` → `0-status,,,false` |

### MEDIUM — Unescaped Comma in Description (PRD)

Line 3: `Rédaction du document PRD (vision produit, features, user stories)` contains commas.
**Fix:** Wrap in quotes: `"Rédaction du document PRD (vision produit, features, user stories)"`

### MEDIUM — Broken Reference `followed-by`

Line 5 (Spec): `followed-by=research` but no entry has `action=research`.
**Fix:** Change to `research-patterns`.

---

## Quality Issues

### MEDIUM — Agent Roster Code Mismatch (masb-agent-reviewer)

`customize.toml` has `code = "masb-agent-reviewer"` but `module.yaml` has `code: agent-reviewer`.
All other 6 agents use short codes (`agent-architecte`, etc.) in both places.
**Fix:** Change customize.toml `code` to `"agent-reviewer"` for consistency.

### LOW — Agent Roster Icon Drift (masb-agent-reviewer)

`module.yaml` gives `icon: "🔍"` but `customize.toml` has `icon = ""` (empty).
**Fix:** Add `icon = "🔍"` to customize.toml.

### LOW — SKILL.md name ≠ Directory (masb-agent-ux)

`masb-agent-ux/SKILL.md` has `name: agent-ux` — all other skills use `masb-agent-*`.
**Fix:** Change to `name: masb-agent-ux`.

### LOW — CSV Orphan Entry: Failure Report

Entry `failure-report` (action) is registered in CSV but not documented in `masb-agent-testeur/SKILL.md` capabilities table.
**Fix:** Add to SKILL.md capabilities table or remove from CSV.

---

## Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical | 0 | — |
| High | 1 | Unfixed |
| Medium | 4 | Unfixed |
| Low | 3 | Unfixed |
| **Total** | **8** | **Needs fixes** |

## Re-validation

After fixes: run `python3 /home/marwane/Documents/momono/.agents/skills/bmad-module-builder/scripts/validate-module.py /home/marwane/Documents/momono/skills`
