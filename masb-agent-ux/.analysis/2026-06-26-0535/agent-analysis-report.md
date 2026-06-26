# Analysis Report: masb-agent-ux

Generated: 2026-06-26 · Schema: 2

**Grade: Good**

> Solid memory agent with rich persona, but capability prompts read as checklists rather than the warm designer character First Breath builds

masb-agent-ux has a well-defined UI/UX Designer persona with four capabilities covering the full design workflow from global design system through per-phase UI to validation. The sanctum is complete, scripts are correct, and First Breath territories are domain-adapted. The main opportunities are infusing persona voice into the capability prompts (they read as dry checklists), fixing two sanctum wiring defects (placeholder mismatch, memlog leaking into runtime), and clarifying accessibility layering across three capabilities.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 4 |
| Medium | 20 |
| Low | 13 |

## Themes

### 1. Capability prompts are checklists, not the persona

- Root cause: First Breath builds a warm, creative designer who 'raconte pourquoi ces couleurs fonctionnent', but all 4 capability prompts are dry bullet lists — the persona voice disappears during execution. The leanness lens identifies the checklist pattern (format templating, yellow-flag NEVER constructions), and the enhancement lens confirms the remedy: open each capability with 1-2 lines of persona stance.
- Fix: Open each capability prompt with persona stance ('Tu es designer, pas un générateur de checklist'), collapse bullet lists to goal sentences, and replace NEVER constructions with positive framing.
- Findings:
  - `leanness-1` Design-system DOIT list is format templating — `references/design-system.md:15-22`
  - `leanness-2` UI-spec DOIT list is format templating — `references/ui-spec.md:15-23`
  - `leanness-3` Accessibility-check checklist is format templating — `references/accessibility-check.md:15-23`
  - `leanness-4` Theme-validate comparison list is format templating — `references/theme-validate.md:15-22`
  - `leanness-5` Theme-validate deviation process is numbered sequence — `references/theme-validate.md:24-27`
  - `leanness-6` Accessibility-check reporting format prescriptive — `references/accessibility-check.md:27`
  - `leanness-7` NEVER construction in design-system — `references/design-system.md:26`
  - `leanness-8` NEVER construction in ui-spec — `references/ui-spec.md:27`
  - `enhancement-1` ADD — Infuse persona voice into capability prompts — `references/*.md`

### 2. Sanctum wiring: dead references, placeholder mismatch, memlog leak

- Root cause: Three glitches in the sanctum lifecycle: (1) CREED instructs the agent to load prompt-quality-canon.md but it's in SKILL_ONLY_FILES and never copied, (2) CREED-template uses {project-root} (hyphen) but init-sanctum.py provides project_root (underscore) so Dominion paths render as literal placeholders, (3) .memlog.md in references/ leaks into the agent's runtime sanctum via copy_references. The canon pull-in order is additionally inert since EVOLVABLE=False.
- Fix: Add .memlog.md to SKILL_ONLY_FILES, fix placeholder to use matching token, and remove the canon pull-in standing order from CREED-template since the agent is not evolvable.
- Findings:
  - `architecture-1` CREED standing order references canon excluded from sanctum — `assets/CREED-template.md:48`
  - `sanctum-1` {project-root} placeholder mismatch in CREED Dominion — `assets/CREED-template.md:65-78`
  - `sanctum-2` .memlog.md leaks into sanctum runtime — `references/.memlog.md`

### 3. Pulse and stateless vestiges on non-autonomous memory agent

- Root cause: INDEX-template, MEMORY-template, and memory-guidance.md reference 'during Pulse' for curation, but Pulse is not enabled for this agent. Simultaneously, memory-guidance.md opens with 'You are stateless', contradicting the Sacred Truth's continuity framing. SKILL.md also mentions --pulse in step 1.
- Fix: Replace 'during Pulse' with 'at natural breaks' or 'at session end', remove the --pulse clause from SKILL.md step 1, and replace 'You are stateless' with 'Your working memory resets between sessions'.
- Findings:
  - `architecture-2` Pulse curation trigger on non-autonomous agent — `assets/INDEX-template.md:11`
  - `enhancement-6` REMOVE — Vestigial --pulse reference — `SKILL.md:49`
  - `enhancement-7` REMOVE — Contradictory 'stateless' language — `references/memory-guidance.md:10`

### 4. Accessibility and iteration gaps in design workflow

- Root cause: Three capabilities (DS, AC, TV) touch WCAG without clear layering — DS defines, AC audits, TV monitors — but the boundary is undocumented. No capability validates designs against official Material Design 3 guidelines (elevation semantics, dynamic color, motion). The workflow terminates at TV (deviation report) with no path to revise the DS or US.
- Fix: Document the layering explicitly in each capability's scope, add M3 compliance validation to TV, and add revise-design-system / update-ui-spec capabilities for the iteration loop.
- Findings:
  - `agent-cohesion-1` Accessibility spread across 3 capabilities with unclear layering — `references/design-system.md, references/accessibility-check.md, references/theme-validate.md`
  - `agent-cohesion-2` No M3 compliance validation capability — `references/theme-validate.md`
  - `agent-cohesion-3` No iteration capability after validation — `references/design-system.md:28, references/theme-validate.md`

## Strengths

- Rich, domain-specific First Breath with calibration territories tailored to a UI/UX designer relationship
- Solid memory agent scaffolding: correct wake.py/init-sanctum.py, all 6 sanctum templates present with domain-specific seeds
- Persona voice in SKILL.md, CREED, and PERSONA template is warm, creative, and distinctive — the character feels real
- Four capabilities cover the full design workflow end-to-end: global DS → per-phase US → AC → TV cross-phase validation
- External skill dependencies (font-m3-cli, material-symbols-cli, adaptive, styles, edge-to-edge) are appropriate for the domain

## Recommendations

1. Infuse persona voice into all 4 capability prompts — open each with 1-2 lines of stance (collapses checklist findings) and replace numbered bullet sections with goal sentences (resolves: leanness-1, leanness-2, leanness-3, leanness-4, leanness-5, leanness-6, leanness-7, leanness-8, enhancement-1)
2. Fix sanctum wiring: add .memlog.md to SKILL_ONLY_FILES (sanctum-2), change {project-root} to {project_root} in CREED Dominion paths (sanctum-1), remove canon pull-in from CREED-template since EVOLVABLE=False (architecture-1), replace Pulse refs (architecture-2) (resolves: architecture-1, sanctum-1, sanctum-2, architecture-2, enhancement-6, enhancement-7)
3. Clarify accessibility layering: DS defines target level, AC audits, TV monitors across phases. Add M3 compliance validation to TV's scope. Add revise-design-system and update-ui-spec capabilities for iteration. (resolves: agent-cohesion-1, agent-cohesion-2, agent-cohesion-3)
4. Add graceful fallback for missing workspace files: if brainstorm.md/prd.md don't exist, surface in character and offer to backfill context conversationally (resolves: enhancement-2)
5. Pre-pass the deterministic comparison work in theme-validate into a script (scripts/extract-design-tokens.py) so the prompt reasons over structured JSON diffs instead of raw files (resolves: determinism-1)

## Agent Profile

- Name: agent-ux
- Title: UI/UX Designer
- Type: memory
- Mission: Transformer chaque projet Android en une experience visuelle cohérente, accessible et fidèle au Material Design 3

## Capabilities

- **design-system** (prompt) — Produit le design system global (palette, typo, icônes, thème M3, accessibilité)
- **ui-spec** (prompt) — Décline le design system pour une phase spécifique
- **accessibility-check** (prompt) — Vérifie l'accessibilité du design (WCAG, contrastes, cibles)
- **theme-validate** (prompt) — Valide la cohérence entre toutes les phases

## Per-Lens Verdicts

- **leanness**: Four capability prompts carry format-templating checklists; sanctum templates lean with minor redundant content
- **architecture**: Sound memory archetype, but CREED carries dead pointer and Pulse refs on non-autonomous agent
- **determinism**: One script candidate: theme-validate diff work should be a pre-pass script
- **customization**: Metadata-only memory agent, about right, sole mechanism
- **enhancement**: Strong persona foundations but capabilities lose the character; fallback handling missing
- **agent-cohesion**: Authentic persona with well-aligned capabilities; accessibility layering unclear, no iteration loop
- **sanctum-architecture**: Complete and seeded; placeholder mismatch and memlog leak in sanctum

## Sanctum (runtime memory)

- Location: `{project-root}/_bmad/memory/masb-agent-ux/`
- Files: `INDEX.md`, `PERSONA.md`, `CREED.md`, `BOND.md`, `MEMORY.md`, `CAPABILITIES.md`
- Note: All 6 standard templates present with meaningful domain-specific seeds. Two wiring issues: project-root/project_root placeholder mismatch in CREED Dominion paths, and .memlog.md leaks into sanctum via copy_references.

## Experience

- **First Breath** — Scaffold sanctum → warm calibration conversation → name, vibe, design preferences, mission, capabilities → birthday ceremony
- **Waking** — Wake via wake.py → become yourself (load sanctum) → bind standing rules → continuity callback or capabilities offer
- Headless: All 4 capabilities hardcode MASB workspace paths and assume pre-existing files. No path for pre-supplied inputs or automated invocation.

## Findings

### High (4)

#### lint-9 — scripts/tests/ directory missing

- Lens: lint
- Location: `scripts/tests/`
- Evidence: No unit tests for any script
- Recommendation: Create scripts/tests/ with test files

#### enhancement-1 — ADD — Infuse persona voice into capability prompts

- Lens: enhancement
- Location: `references/*.md`
- Evidence: First Breath builds a warm persona; all 4 capability prompts are dry checklists
- Recommendation: Open each capability with 1-2 lines of persona framing

#### enhancement-2 — ADD — Graceful fallback when workspace files missing

- Lens: enhancement
- Location: `references/design-system.md:24`
- Evidence: Assumes brainstorm.md and prd.md exist; no guidance if absent
- Recommendation: Add soft-gate: offer to backfill context conversationally

#### agent-cohesion-1 — Accessibility spread across 3 capabilities with unclear layering

- Lens: agent-cohesion
- Location: `references/design-system.md, references/accessibility-check.md, references/theme-validate.md`
- Evidence: DS defines, AC audits, TV monitors — no documented boundary
- Recommendation: Document layering explicitly in each capability

### Medium (20)

#### lint-1 — init-sanctum.py No PEP 723 inline dependency block

- Lens: lint
- Location: `scripts/init-sanctum.py:1`
- Evidence: Script missing # /// script block with requires-python
- Recommendation: Add PEP 723 block

#### lint-2 — init-sanctum.py No argparse

- Lens: lint
- Location: `scripts/init-sanctum.py:1`
- Evidence: Script lacks --help self-documentation
- Recommendation: Add argparse

#### lint-3 — init-sanctum.py No json.dumps

- Lens: lint
- Location: `scripts/init-sanctum.py:1`
- Evidence: Output not structured JSON
- Recommendation: Use json.dumps

#### lint-4 — No unit test for init-sanctum.py

- Lens: lint
- Location: `scripts/init-sanctum.py`
- Evidence: No test file found
- Recommendation: Create unit test

#### lint-5 — wake.py No argparse

- Lens: lint
- Location: `scripts/wake.py:1`
- Evidence: Script lacks --help
- Recommendation: Add argparse

#### lint-6 — wake.py No json.dumps

- Lens: lint
- Location: `scripts/wake.py:1`
- Evidence: Output not structured JSON
- Recommendation: Use json.dumps

#### lint-8 — No unit test for wake.py

- Lens: lint
- Location: `scripts/wake.py`
- Evidence: No test file found
- Recommendation: Create unit test

#### leanness-1 — Design-system DOIT list is format templating

- Lens: leanness
- Location: `references/design-system.md:15-22`
- Evidence: Six bullets enumerating standard M3 design system sections the model already knows
- Recommendation: Replace with a single outcome sentence

#### leanness-2 — UI-spec DOIT list is format templating

- Lens: leanness
- Location: `references/ui-spec.md:15-23`
- Evidence: Seven bullets listing standard UI spec sections
- Recommendation: Collapse to one goal sentence

#### leanness-3 — Accessibility-check checklist is format templating

- Lens: leanness
- Location: `references/accessibility-check.md:15-23`
- Evidence: Seven WCAG checkpoints the expert already knows
- Recommendation: Replace checklist with a goal sentence

#### leanness-4 — Theme-validate comparison list is format templating

- Lens: leanness
- Location: `references/theme-validate.md:15-22`
- Evidence: Six comparison dimensions the role implies
- Recommendation: Replace with goal sentence

#### leanness-5 — Theme-validate deviation process is numbered sequence

- Lens: leanness
- Location: `references/theme-validate.md:24-27`
- Evidence: Three sub-bullets describing sequential process
- Recommendation: Collapse to one goal sentence

#### architecture-1 — CREED standing order references canon excluded from sanctum

- Lens: architecture
- Location: `assets/CREED-template.md:48`
- Evidence: prompt-quality-canon.md is in SKILL_ONLY_FILES, not copied to sanctum
- Recommendation: Remove canon pull-in from CREED since EVOLVABLE=False

#### determinism-1 — theme-validate does deterministic file comparison in a prompt

- Lens: determinism
- Location: `references/theme-validate.md`
- Evidence: Prompt instructs model to diff design docs — output is same for same inputs
- Recommendation: Write a pre-pass script to extract and diff design tokens as JSON

#### enhancement-3 — REMOVE — First Breath 10-step wrap-up ceremony

- Lens: enhancement
- Location: `references/first-breath.md:107-115`
- Evidence: 10 sequential procedural steps contradict the warm calibration tone
- Recommendation: Collapse to 1-2 goal sentences

#### enhancement-4 — ADD — Handle casual check-in in Waking mode

- Lens: enhancement
- Location: `SKILL.md:56-59`
- Evidence: No path for social opening; agent forced to offer capabilities
- Recommendation: Add fork for casual openings before capabilities offer

#### enhancement-5 — ADD — Support headless capability invocation

- Lens: enhancement
- Location: `references/design-system.md:13`
- Evidence: All capabilities hardcode MASB workspace paths
- Recommendation: Add input contract: accept inline inputs vs file lookup

#### agent-cohesion-2 — No M3 compliance validation capability

- Lens: agent-cohesion
- Location: `references/theme-validate.md`
- Evidence: Persona is M3 specialist but no capability validates M3 guideline compliance
- Recommendation: Extend TV to include M3 spec validation

#### agent-cohesion-3 — No iteration capability after validation

- Lens: agent-cohesion
- Location: `references/design-system.md:28, references/theme-validate.md`
- Evidence: DS figé after HITL, TV reports deviations with no revision path
- Recommendation: Add revise-design-system / update-ui-spec capabilities

#### sanctum-1 — {project-root} placeholder mismatch in CREED Dominion

- Lens: sanctum-architecture
- Location: `assets/CREED-template.md:65-78`
- Evidence: Template uses hyphen but init-sanctum.py provides underscore
- Recommendation: Change template to use {project_root} or add hyphen variant

### Low (13)

#### lint-7 — wake.py No sys.exit calls

- Lens: lint
- Location: `scripts/wake.py:1`
- Evidence: May not return meaningful exit codes
- Recommendation: Add sys.exit()

#### leanness-6 — Accessibility-check reporting format prescriptive

- Lens: leanness
- Location: `references/accessibility-check.md:27`
- Evidence: Enumerates output fields instead of stating goal
- Recommendation: Replace with 'Produis un rapport structuré'

#### leanness-7 — NEVER construction in design-system

- Lens: leanness
- Location: `references/design-system.md:26`
- Evidence: 'Ne jamais inventer' — ALL-CAPS prescriptive tone
- Recommendation: Reword as positive standing order

#### leanness-8 — NEVER construction in ui-spec

- Lens: leanness
- Location: `references/ui-spec.md:27`
- Evidence: 'Ne jamais réinventer' — second instance of pattern
- Recommendation: Reword as positive

#### leanness-9 — Three redundant anti-patterns in CREED template

- Lens: leanness
- Location: `assets/CREED-template.md:55-57`
- Evidence: Anti-patterns 1-3 restate rules from Core Values and Standing Orders
- Recommendation: Drop or merge into relevant Core Value

#### leanness-10 — Meta-commentary before standing orders

- Lens: leanness
- Location: `assets/CREED-template.md:33`
- Evidence: 'These are always active' — meta-explanation the model infers
- Recommendation: Cut the line

#### leanness-11 — Verbose tool preference in CAPABILITIES template

- Lens: leanness
- Location: `assets/CAPABILITIES-template.md:11`
- Evidence: Three sentences saying the same directive
- Recommendation: Collapse to one sentence

#### architecture-2 — Pulse curation trigger on non-autonomous agent

- Lens: architecture
- Location: `assets/INDEX-template.md:11`
- Evidence: References 'during Pulse' but agent is memory-only
- Recommendation: Replace with 'at natural breaks'

#### architecture-3 — customize.toml name field empty

- Lens: architecture
- Location: `customize.toml:12`
- Evidence: name = "" while SKILL.md frontmatter has name: agent-ux
- Recommendation: Set name or leave empty for First Breath naming

#### enhancement-6 — REMOVE — Vestigial --pulse reference

- Lens: enhancement
- Location: `SKILL.md:49`
- Evidence: --pulse mentioned but agent has no Pulse mode
- Recommendation: Remove --pulse clause from SKILL.md step 1

#### enhancement-7 — REMOVE — Contradictory 'stateless' language

- Lens: enhancement
- Location: `references/memory-guidance.md:10`
- Evidence: 'You are stateless' contradicts Sacred Truth continuity
- Recommendation: Replace with 'Your working memory resets between sessions'

#### agent-cohesion-4 — Zero-code vs CLI skills ambiguity

- Lens: agent-cohesion
- Location: `assets/CREED-template.md:44`
- Evidence: CREED says 'ne jamais écrire de code' but references CLI tools
- Recommendation: Clarify if CLI tools imply code generation or just guidance

#### sanctum-2 — .memlog.md leaks into sanctum runtime

- Lens: sanctum-architecture
- Location: `references/.memlog.md`
- Evidence: Builder artifact copied by copy_references into agent's memory
- Recommendation: Add .memlog.md to SKILL_ONLY_FILES
