# Analysis Report: masb-agent-developpeur

Generated: 2026-06-26 · Schema: 2

**Grade: Poor**

> Poor — critical TOML syntax error makes the sole config surface unparseable; bootloader leaks sanctum-bound content at 2.8x the guardrail; rich persona treated as investment, not waste.

L'agent a une base solide (persona cohérente, sanctum complet, capabilities fonctionnelles) mais souffre d'un défaut TOML critique et d'une fuite de contenu du bootloader vers le sanctum. Les capability prompts sont légèrement sur-prescriptives mais le cœur du contenu est utile.

| Severity | Count |
| --- | --- |
| Critical | 1 |
| High | 2 |
| Medium | 7 |
| Low | 6 |

## Themes

### 1. Bootloader overweight with sanctum-bound content

- Root cause: SKILL.md carries 1133 tokens (~2.8x the ~400 token guardrail for memory bootloaders) because persona voice, detailed Waking Mode behavioral guidance, and capability routing detail leaked into the bootloader instead of living in the sanctum (PERSONA.md, CAPABILITIES.md). This inflates every activation and duplicates content that should live in one place.
- Fix: Move persona voice/communication style to PERSONA-template.md. Trim Waking Mode to routing-only. Prune capability enumeration from frontmatter description. Target ~400 tokens.
- Findings:
  - `architecture-1` Sanctum-bound content leaked into overweight bootloader — `SKILL.md:6-8, SKILL.md:65-71`
  - `agent-cohesion-1` Bootloader SKILL.md leaks sanctum-bound content at 2.8x guardrail — `SKILL.md:6-8, SKILL.md:36-38`
  - `sanctum-1` Sanctum-bound communication style leaked into bootloader SKILL.md — `SKILL.md:6-8`

### 2. Capability prompts carry ceremony and defensive padding

- Root cause: All three capability prompts (implement, compile-check, auto-fix) have numbered steps that force sequential execution where the model would reach the same outcome without instruction, plus 'Express path' sections that describe what the model would do anyway. The CREED template also has a formatting defect (literal \n).
- Fix: Collapse numbered sequences to goal sentences. Remove Express path blocks from all three capabilities. Fix CREED-template.md \n formatting.
- Findings:
  - `leanness-1` implement.md numbered sequence over-prescriptive — `references/implement.md:17-33`
  - `leanness-2` Express path blocks in all 3 capability prompts are defensive padding — `references/implement.md:35, references/compile-check.md:22, references/auto-fix.md:26`
  - `leanness-4` compile-check.md full version barely beats its absence — `references/compile-check.md:9-24`
  - `leanness-5` auto-fix.md express path and process scaffolding are removable — `references/auto-fix.md:9-28`
  - `sanctum-2` Literal \n sequences in CREED-template.md instead of actual newlines — `CREED-template.md:17,23,35,40`

### 3. Developer workflow incomplete — missing dependency management and compile-fix pipeline

- Root cause: The implement → compile-check → auto-fix loop requires manual orchestration. Dependency management is explicitly excluded (escalated as 'complex error'). No single-shot pipeline chains the three capabilities end-to-end for expert users.
- Fix: Add a compile-fix pipeline capability (CFL) that chains implement → compile → auto-fix → recompile → report. Add a manage-dependency capability or expand auto-fix for dependency resolution.
- Findings:
  - `agent-cohesion-2` Dependency management is a gap in the developer workflow — `references/implement.md, references/auto-fix.md, assets/CREED-template.md`
  - `enhancement-2` No compile-fix pipeline capability for expert/automator flow — `references/implement.md, references/compile-check.md, references/auto-fix.md`

### 4. Sanctum self-containment broken for runtime dependencies

- Root cause: memory-guidance.md and prompt-quality-canon.md are in SKILL_ONLY_FILES and never copied to sanctum, yet the agent's CREED standing order and Persistent Memory directive reference them. After init, the agent depends on the skill bundle for normal operation.
- Fix: Remove memory-guidance.md and prompt-quality-canon.md from SKILL_ONLY_FILES so they're copied to sanctum/references/ during init.
- Findings:
  - `enhancement-1` Sanctum self-containment broken — runtime dependencies not copied — `scripts/init-sanctum.py:38`

## Strengths

- Persona cohérente et reconnaissable — 'Développeur Android expert' se retrouve dans les trois capabilities
- Sanctum structurellement complet — les 6 templates, wake.py et init-sanctum.py sont tous présents avec le bon SKILL_NAME et le bon flag EVOLVABLE
- Capabilities fonctionnelles avec frontmatter valide — auto-découvertes par init-sanctum.py
- First Breath de type configuration avec questions de découverte adaptées au domaine Android
- Standing orders pertinents avec le canon pull-in et les valeurs bien adaptées au domaine
- TOML corrigé et active — le fichier est maintenant parsable et valide
- Persona traitée comme investissement — aucune recommandation de l'aplatir

## Recommendations

1. Fix CREED-template.md literal \n formatting and restore TOML integrity (already done) (resolves: customization-1, leanness-3, sanctum-2)
2. Trim SKILL.md bootloader to ~400 tokens: move persona voice to PERSONA-template.md, reduce Waking Mode to routing-only, trim frontmatter description (resolves: architecture-1, agent-cohesion-1, sanctum-1)
3. Remove memory-guidance.md and prompt-quality-canon.md from SKILL_ONLY_FILES in init-sanctum.py so the sanctum is self-contained (already done) (resolves: enhancement-1)
4. Remove Express path blocks from all three capability prompts and collapse numbered sequences to goal sentences (resolves: leanness-1, leanness-2, leanness-4, leanness-5)
5. Add compile-fix pipeline capability and dependency management capability (resolves: agent-cohesion-2, enhancement-2)

## Findings

### Critical (1)

#### customization-1 — Invalid TOML syntax in name field — unclosed multi-line string

- Lens: customization
- Location: `customize.toml:13`
- Evidence: Field reads `name = """"` (four double quotes). TOML interprets `"""` as start of multi-line string; no closing `"""` exists. The entire customize.toml was unparseable. Now fixed to `name = ""`.
- Recommendation: Use `name = ""` for empty string. Already fixed.

### High (2)

#### architecture-1 — Sanctum-bound content leaked into overweight bootloader

- Lens: architecture
- Location: `SKILL.md:6-8, SKILL.md:65-71`
- Evidence: SKILL.md is 1133 tokens vs ~400-token guardrail. Persona voice block and detailed Waking Mode behavioral guidance belong in sanctum (PERSONA.md).
- Recommendation: Move persona voice to PERSONA-template.md. Trim Waking Mode section to routing-only. Target ~400 tokens.

#### enhancement-1 — Sanctum self-containment broken — runtime dependencies not copied

- Lens: enhancement
- Location: `scripts/init-sanctum.py:38`
- Evidence: memory-guidance.md and prompt-quality-canon.md in SKILL_ONLY_FILES are never copied to sanctum. Agent's CREED and Persistent Memory directive reference them at runtime.
- Recommendation: Remove from SKILL_ONLY_FILES. Already done.

### Medium (7)

#### sanctum-1 — Sanctum-bound communication style leaked into bootloader SKILL.md

- Lens: sanctum-architecture
- Location: `SKILL.md:6-8`
- Evidence: 1133 token bootloader carries full persona voice that belongs in sanctum.
- Recommendation: Move to PERSONA-template.md.

#### sanctum-2 — Literal \n sequences in CREED-template.md instead of actual newlines

- Lens: sanctum-architecture
- Location: `CREED-template.md:17,23,35,40`
- Evidence: Four sections use literal `\n` escape sequences — renders as visible `\n` in markdown.
- Recommendation: Replace \n with real newlines. Already done.

#### agent-cohesion-1 — Bootloader SKILL.md leaks sanctum-bound content at 2.8x guardrail

- Lens: agent-cohesion
- Location: `SKILL.md:6-8, SKILL.md:36-38`
- Evidence: 1133 tokens vs ~400. Stay in Character section duplicates persona communication style belonging in sanctum.
- Recommendation: Move Stay in Character detail to PERSONA.md.

#### agent-cohesion-2 — Dependency management is a gap in the developer workflow

- Lens: agent-cohesion
- Location: `references/implement.md, references/auto-fix.md, assets/CREED-template.md`
- Evidence: No capability to add/update dependencies. Auto-fix classifies 'missing dependencies' as complex errors to escalate.
- Recommendation: Add manage-dependency capability or expand auto-fix.

#### enhancement-2 — No compile-fix pipeline capability for expert/automator flow

- Lens: enhancement
- Location: `references/implement.md, references/compile-check.md, references/auto-fix.md`
- Evidence: Expert must manually loop: implement → compile-check → auto-fix → compile-check. No single-shot pipeline.
- Recommendation: Add pipeline capability CFL that chains implement → compile → auto-fix → recompile → report.

#### leanness-1 — implement.md numbered sequence over-prescriptive

- Lens: leanness
- Location: `references/implement.md:17-33`
- Evidence: 4 numbered steps force sequential execution. Steps 3-4 are persona knowledge or already in output spec.
- Recommendation: Collapse to goal sentences. Keep only the non-inferable skill-name mapping.
- Proposed smallest: Implement code from spec, findings, and UI spec. Output to phases/N/code/. Before writing, consult the relevant skill: navigation-3 | camera1-to-camerax | edge-to-edge | adaptive | styles | migrate-xml-views-to-jetpack-compose | appfunctions | verified-email | jetpack-compose-m3 | display-glasses-with-jetpack-compose-glimmer | play-billing-library-version-upgrade | engage-sdk-integration. Never invent an API.
- Predicted delta: Near-zero.

#### leanness-3 — CREED-template.md uses literal \n instead of actual line breaks

- Lens: leanness
- Location: `assets/CREED-template.md:17,23,35,40`
- Evidence: Four bullet-list sections contain literal \n characters.
- Recommendation: Replace with real newlines. Already done.

### Low (6)

#### enhancement-3 — {bond-domain-sections} placeholder leaks into generated BOND.md

- Lens: enhancement
- Location: `assets/BOND-template.md:8`
- Evidence: Placeholder not in substitute_vars map — survives as raw literal text in generated BOND.md.
- Recommendation: Replace with comment-style instruction. Already done.

#### determinism-1 — Prompt instructs model to scan for remaining {\u2026} placeholders

- Lens: determinism
- Location: `references/first-breath.md:73`
- Evidence: Instruction 'scanne les fichiers du sanctum pour les instructions {\u2026} restantes' is a deterministic text-pattern scan the model does once at generation cost.
- Recommendation: Add post-substitution validation to init-sanctum.py to flag remaining placeholders deterministically.

#### leanness-2 — Express path blocks in all 3 capability prompts are defensive padding

- Lens: leanness
- Location: `references/implement.md:35, references/compile-check.md:22, references/auto-fix.md:26`
- Evidence: Each capability carries an Express path describing default behavior the model would do anyway.
- Recommendation: Delete all three Express path sections.

#### leanness-4 — compile-check.md full version barely beats its absence

- Lens: leanness
- Location: `references/compile-check.md:9-24`
- Evidence: 24 lines / 174 tokens — only the build command and progress.md convention are non-inferable.
- Recommendation: Collapse to: 'Run ./gradlew assembleDebug. On success, update progress.md. On failure, capture logs. Never claim it compiles without running the build.'
- Proposed smallest: Run ./gradlew assembleDebug. On success, update progress.md. On failure, capture logs. Never claim it compiles without running the build.
- Predicted delta: Near-zero.

#### leanness-5 — auto-fix.md express path and process scaffolding are removable

- Lens: leanness
- Location: `references/auto-fix.md:9-28`
- Evidence: 5-step numbered process can collapse. Only non-inferable content is simple-vs-complex classification boundary and escalation format.
- Recommendation: Keep classification rule with examples, escalation path, non-negotiable. Drop numbered scaffolding and express path.
- Proposed smallest: Fix simple compile errors (missing imports, wrong signatures, typos, resource references, wrong parameters). Complex errors (architecture, API incompatibility, missing deps, ambiguous) write to progress.md as blocked: compile. Never apply a fix you don't understand.
- Predicted delta: Small.

#### customization-2 — name and title lack read-only-at-runtime comments

- Lens: customization
- Location: `customize.toml:13-14`
- Evidence: No comment noting these are install-time roster metadata, not runtime overrides.
- Recommendation: Add inline comments: `name = ""  # read-only at runtime` and `title = "...
