# Analysis Report: masb-agent-architecte

Generated: 2026-06-26 · Schema: 2

**Grade: Fair**

> Authentic, well-cohered no-code architecte persona with sound sanctum architecture — but a heavy bootloader (2.8x guardrail), scripted discovery that contradicts its own canon, and no fallback paths for users without a clear vision.

masb-agent-architecte is a well-constructed memory agent with a strong persona and clean capability chain from brainstorm to spec. The sanctum is complete and seeded, and the customization surface is correctly metadata-only. However, the bootloader SKILL.md carries duplicated sanctum-bound content at 2.8x the guardrail, the First Breath question bank contradicts the prompt-quality canon it ships, and there are no capability paths for expert users who want to skip planning or visionless users who need divergent exploration. 7 determinism leaks across memory guidance and First Breath ask the LLM to do counting and date arithmetic it cannot do reliably.

| Severity | Count |
| --- | --- |
| Critical | 2 |
| High | 8 |
| Medium | 13 |
| Low | 14 |

## Themes

### 1. Bootloader bloat and identity duplication

- Root cause: SKILL.md carries sanctum-bound content (full Three Laws, Sacred Truth, Stay in Character, Persistent Memory narrative) at 1131 tokens when ~400 is the guardrail for a memory bootloader. The Sacred Truth is duplicated verbatim across SKILL.md and CREED-template.md (~200 tokens of identical text loaded every session). The Three Laws exist only in the bootloader — they vanish from the agent's identity after First Breath when the sanctum becomes the primary identity source.
- Fix: Strip sanctum-bound content from SKILL.md: move Stay in Character and Persistent Memory narrative to PERSONA-template.md and CREED-template.md respectively. Keep only identity seed (2-3 sentences), short-form Three Laws, short-form Sacred Truth, and the activation spine. Add Three Laws section to CREED-template.md so they persist in sanctum. Deduplicate Sacred Truth — canonical copy in CREED-template.md, one-liner reference in SKILL.md.
- Findings:
  - `architecture-1` Bootloader exceeds guardrail by 2.8x with leaked identity content — `SKILL.md:1-60`
  - `architecture-2` Sacred Truth duplicated verbatim in bootloader and CREED template — `SKILL.md:19-23 / CREED-template.md:3-9`
  - `architecture-3` Three Laws defined in bootloader but absent from CREED template — `SKILL.md:9-17 vs CREED-template.md`
  - `sanctum-1` SKILL.md bootloader exceeds ~400 token guardrail at 1131 tokens — `SKILL.md:1-60`
  - `enhancement-4` remove: Sacred Truth duplicated verbatim across SKILL.md and CREED-template.md — `SKILL.md:20-23 and assets/CREED-template.md:3-9`
  - `enhancement-10` remove: The Three Laws framing adds ceremony without enforceable value — `SKILL.md:9-15`

### 2. Scripted discovery contradicts the agent's own canon

- Root cause: The agent ships prompt-quality-canon.md which teaches 'write the destination, not the route' and 'a script is your imagined transcript of one good session.' Yet first-breath.md contains 18+ questions in 4 rigid categories, decompose.md has a numbered list of independent rules, spec.md numbers 8 independent document sections, and prd.md templates standard PRD structure any model already knows. The canon's own tests would flag most of its agent's capability prompts as ceremony.
- Fix: Replace numbered lists and question banks with outcome-stated goals throughout. First-breath.md: replace 18 questions with 'discover naturally: their project, working style, phase preferences, expertise, name, and tools.' Decompose.md: replace numbered rules with one goal sentence. Spec.md: collapse 8-numbered sections. Prd.md: remove section template — the consumer definition alone does the work.
- Findings:
  - `leanness-1` first-breath.md: scripted interview replaces adaptive discovery — `references/first-breath.md:28-76`
  - `leanness-2` decompose.md: numbered list of independent rules masquerading as sequence — `references/decompose.md:17-23`
  - `leanness-3` spec.md: numbered section template disguises independent sections as sequence — `references/spec.md:17-25`
  - `leanness-4` prd.md: section template re-teaches standard PRD structure — `references/prd.md:17-24`
  - `leanness-7` memory-guidance.md: session log format template teaches markdown — `references/memory-guidance.md:41-53`
  - `enhancement-12` remove: discovery question list is over-structured per agent's own canon — `references/first-breath.md:36-60`

### 3. Deterministic work leaks into prompts

- Root cause: Three operations that only a script can do reliably are delegated to the LLM: token counting ('stay under 1500 tokens' across 3 locations), date-based file pruning ('delete sessions older than 14 days'), and regex pattern scanning ('find remaining {placeholder} tokens'). A fourth borderline case asks the LLM to validate folder naming conventions it just created. These cost tokens on every relevant invocation and produce unreliable results.
- Fix: Script token measurement into wake.py (output current MEMORY.md token count on load). Add a prune-sessions.py script that handles date comparison and stale-file removal. Script the placeholder scan into init-sanctum.py or a validate-sanctum.py post-pass. For folder-structure validation, add a validate-phases.py script called after decompose.
- Findings:
  - `determinism-1` Token counting delegated to LLM across memory guidance and templates — `references/memory-guidance.md:58,87 + assets/MEMORY-template.md:7`
  - `determinism-2` Date-based session log pruning asked of LLM — `references/memory-guidance.md:56`
  - `determinism-3` Placeholder pattern scanning assigned to LLM during First Breath — `references/first-breath.md:96`
  - `determinism-4` Structural validation rules embedded in decompose prompt — `references/decompose.md:17-23`

### 4. No fallback paths for divergent user archetypes

- Root cause: All five capabilities assume a linear, structured planning process starting from a concrete project idea. Three user archetypes have no path: the visionless user with only a vague desire (needs divergent ideation before structured questions), the expert who wants a rough plan fast (needs a quickplan exit ramp that skips PRD and full specs), and the returning user whose project has fully pivoted (needs rescope capability instead of piecemeal replan). A fourth gap is the user with existing Android code (needs audit capability).
- Fix: Add: ideate capability (divergent exploration → lightweight output), quickplan capability (3-5 phase outline, no PRD/spec overhead), rescope capability (archive current plan → fresh brainstorm), audit capability (read existing project → gap analysis), validate capability (cross-phase consistency check), and initialize-workspace as an explicit step in brainstorm.
- Findings:
  - `enhancement-1` add: divergent ideation mode for users with no clear vision — `SKILL.md:53-60 (On Activation)`
  - `enhancement-2` add: minimum-viable-plan exit ramp for expert users — `references/decompose.md:17-23`
  - `enhancement-5` add: rescope capability for full project pivots — `references/replan.md:1-28`
  - `enhancement-7` add: lightweight mode for trivial projects — `references/decompose.md:21`
  - `enhancement-8` add: existing-codebase analysis capability — `SKILL.md:60`
  - `agent-cohesion-2` Workspace initialization is implicit, not a capability — `references/brainstorm.md`
  - `enhancement-9` add: progress visibility and status summary capability — `references/decompose.md:13`
  - `agent-cohesion-1` No formal validation or consistency-check capability — `SKILL.md references/ and all capability files`

### 5. Prompt-quality-canon is the wrong reference for a spec-writing agent

- Root cause: The agent carries prompt-quality-canon.md and references it from CREED.md's 'Author to the standard' standing order. But the agent writes specs and plans, not prompts — its five capabilities are static .md files. The canon's advice on 'outcome vs prescription,' 'number-only-true-sequences,' and 'carve by relevance' is genuinely useful for spec writing, but the framing (prompts, models, invocations) confuses the genre. The 1652-token file loads every session even though the standing order fires 'only at the moment a capability is authored or refined.'
- Fix: Replace prompt-quality-canon.md with a spec-quality-canon.md that mirrors the same principles (outcome over process, consumer defines the bar, carve by relevance) framed for specification writing. Or remove the canon entirely — the CREED's 'Ne jamais deviner' and the 'le curseur' lines in each capability already set a clear bar. At minimum, stop loading it on every session: move the standing order to fire only on replan.
- Findings:
  - `enhancement-3` remove: Prompt Quality Canon is wrong-genre reference for a spec-writing agent — `references/prompt-quality-canon.md`
  - `agent-cohesion-4` prompt-quality-canon excluded from sanctum but referenced by CREED — `scripts/init-sanctum.py:12 and assets/CREED-template.md:36-37`

## Strengths

- Persona-capability alignment is excellent — the 'architecte qui ne code pas' is consistently enforced across all 5 capabilities, CREED boundaries, and the activation spine.
- Capability chain (brainstorm → prd → decompose → spec → replan) forms a clean linear journey with clear handoffs and HITL validation at each gate.
- Sanctum architecture is structurally complete: all 6 standard templates exist, carry meaningful domain-specific seeds, and init-sanctum.py's template list matches shipped assets.
- Customization surface is correctly lean for a memory agent — metadata-only customize.toml with empty name for First Breath naming, no override surface, no other config mechanism.
- Activation spine is sound: wake.py → become yourself → bind standing rules → proper mode. First Breath routes correctly to init-sanctum.py + conversational awakening.
- Domain-adapted CREED with concrete Android project values, standing orders, and anti-patterns. The 'zero code' boundary is a clear, enforced behavioral rule.
- The persona was treated as investment throughout build and analysis and was never flagged as waste — voice, warmth, and communication style are preserved.
- The 'le curseur' pattern in each capability prompt (a single line naming the failure mode to guard against) is an elegant application of the canon's scarred-rule principle.

## Recommendations

1. Trim SKILL.md bootloader: strip Stay in Character and Persistent Memory narrative to PERSONA/CREED templates; deduplicate Sacred Truth (canonical copy in CREED-template.md, one-liner in SKILL.md); add Three Laws to CREED-template.md. (resolves: architecture-1, architecture-2, architecture-3, sanctum-1, enhancement-4, enhancement-10, leanness-6)
2. Replace numbered lists and question banks with outcome-stated goals across first-breath.md, decompose.md, spec.md, prd.md, and brainstorm.md per the canon the agent already ships. (resolves: leanness-1, leanness-2, leanness-3, leanness-4, leanness-7, enhancement-12)
3. Script token counting, date-based pruning, and placeholder scanning into wake.py, prune-sessions.py, and validate-sanctum.py respectively. Add validate-phases.py for folder-structure validation after decompose. (resolves: determinism-1, determinism-2, determinism-3, determinism-4)
4. Add ideate, quickplan, rescope, and audit capabilities to cover divergent user archetypes. Add validate for cross-phase consistency checking. Make workspace initialization an explicit step. (resolves: enhancement-1, enhancement-2, enhancement-5, enhancement-7, enhancement-8, agent-cohesion-1, agent-cohesion-2, enhancement-9)
5. Replace prompt-quality-canon.md with spec-quality-canon.md framed for specification writing, or remove it entirely since CREED boundaries already set the bar. (resolves: enhancement-3, agent-cohesion-4)
6. Add non-Android guardrail to brainstorm and make phase-00 assignment configurable rather than hardcoded. (resolves: enhancement-11, agent-cohesion-5, enhancement-14)

## Agent Profile

- Title: Architecte Logiciel
- Type: memory
- Mission: Transformer une idée de projet Android en un plan d'exécution clair, découpé en phases autonomes que chaque agent peut implémenter — sans jamais écrire une ligne de code.

## Capabilities

- **brainstorm** (prompt) — Session interactive pour comprendre la vision du projet. Ouvre le dialogue, capture dans brainstorm.md.
- **prd** (prompt) — Consolide brainstorm.md en PRD structuré (vision, features, user stories, contraintes).
- **decompose** (prompt) — Découpe le projet en phases autonomes, crée dossiers et phases-index.md.
- **spec** (prompt) — Rédige la spec d'une phase au moment de son activation (jamais à l'avance).
- **replan** (prompt) — Re-découpe une phase existante quand le périmètre change ou qu'elle est trop grosse.

## Per-Lens Verdicts

- **leanness**: Capability prompts largely goal-oriented but first-breath.md carries a heavy scripted question bank (18+ questions in 4 categories); three prompts use numbered lists for independent items; CREED template repeats constraints across 4 sections.
- **architecture**: Bootloader exceeds ~400t guardrail (1131t) with leaked sanctum content; Sacred Truth duplicated verbatim in bootloader and CREED template; Three Laws absent from CREED; empty capabilities/ directory.
- **determinism**: 3 determinism leaks (token counting asked of LLM in 3 places, date-based session log pruning, placeholder regex scanning); 0 intelligence leaks in scripts.
- **customization**: Memory agent — about right. Metadata-only customize.toml with empty name (First-Breath-named). No override surface. No other config mechanism.
- **enhancement**: Missing critical paths: no divergent ideation for visionless users, no quickplan for experts, no rescope for full pivots, no existing-codebase audit. Sacred Truth duplicated (200t waste). Prompt-quality-canon is wrong-genre for a spec-writing agent.
- **agent-cohesion**: Tight persona-capability alignment. Gaps: no formal validation capability for cross-phase consistency, no workspace initialization as a distinct step. Decompose/replan boundary could blur over time.
- **sanctum-architecture**: Structurally complete — all 6 templates exist and seeded. First Breath question count (15+) exceeds configuration-style guidance (3-7). Bootloader carries persona-level directives that belong in sanctum.

## Sanctum (runtime memory)

- Location: `{project-root}/_bmad/memory/masb-agent-architecte/`
- Files: `INDEX.md`, `PERSONA.md`, `CREED.md`, `BOND.md`, `MEMORY.md`, `CAPABILITIES.md`
- Note: Sanctum is the built agent's runtime memory, distinct from the builder's .memlog.md in references/. All 6 standard templates exist and carry meaningful seeds. init-sanctum.py's template list matches shipped assets.

## Experience

- **First Breath (birth)** — init-sanctum.py scaffolds → warm greeting → 4-category discovery (projet, style, phases, expertise) → name selection → capability intro → tools → save-all → birthday ceremony
- **Brainstorm → PRD → Decompose → Spec** — User with project idea → brainstorm (open floor) → prd (consolidation → validation HITL) → decompose (phases-index + directories → validation HITL) → activate phase → spec (HITL) → handoff to Research
- **Replan (mid-phase pivot)** — User says phase scope changed → replan reads current spec + progress → proposes re-cut → validates HITL → updates spec.md + phases-index.md
- **Waking (returning user)** — wake.py loads sanctum → Become yourself → Bind standing rules → Waking Mode: callback from MEMORY → offer capabilities
- Headless: No headless mode. All capabilities require HITL validation per CREED boundaries. This is correct for the architecte's design — the persona is interactive by nature.

## Findings

### Critical (2)

#### enhancement-1 — add: divergent ideation mode for users with no clear vision

- Lens: enhancement
- Location: `SKILL.md:53-60 (On Activation)`
- Evidence: All four capabilities assume a concrete project exists. A user with only a vague desire gets forced into structured questions. First-timer archetype: overwhelming.
- Recommendation: Add an `ideate` capability parallel to `brainstorm` that opens with open-floor divergent exploration before any structured output. Route to it when the user's input shows no concrete project.

#### enhancement-2 — add: minimum-viable-plan exit ramp for expert users

- Lens: enhancement
- Location: `references/decompose.md:17-23`
- Evidence: The full decompose flow (brainstorm -> PRD -> phases -> specs) is mandatory per CREED boundaries. An expert who wants a rough plan fast has no path.
- Recommendation: Add a `quickplan` capability that produces a single-page outline (3-5 phases, no PRD, no per-phase spec) when the user explicitly requests speed. Full flow stays default.

### High (8)

#### leanness-1 — first-breath.md: scripted interview replaces adaptive discovery

- Lens: leanness
- Location: `references/first-breath.md:28-76`
- Evidence: 23 questions organized into 4 themed groups with exact French phrasing. A model told 'by the end you need to discover X, Y, Z' will ask the right questions conversationally.
- Recommendation: Replace question bank with an outcome: 'By the end you must know their project, working style, phase relationship, technical level, name, and available tools — discover these naturally.'

#### architecture-1 — Bootloader exceeds guardrail by 2.8x with leaked identity content

- Lens: architecture
- Location: `SKILL.md:1-60`
- Evidence: SKILL.md is 1131 tokens vs ~400 token guardrail for memory agent bootloaders. Three Laws, Sacred Truth, Stay in Character are sanctum-bound content.
- Recommendation: Strip the Three Laws, Sacred Truth, Stay in Character from SKILL.md. Keep only activation sequence and Conventions (~400 tokens).

#### determinism-1 — Token counting delegated to LLM across memory guidance and templates

- Lens: determinism
- Location: `references/memory-guidance.md:58,87 + assets/MEMORY-template.md:7`
- Evidence: "aiming to stay near or under roughly 1500 tokens" in 3 separate instances — LLMs cannot count tokens reliably.
- Recommendation: Add token measurement to wake.py that outputs current MEMORY.md token count on load so the LLM knows exact usage.

#### determinism-2 — Date-based session log pruning asked of LLM

- Lens: determinism
- Location: `references/memory-guidance.md:56`
- Evidence: "prune session logs older than 14 days" — asks the LLM to do date comparison, a deterministic operation.
- Recommendation: Add a prune-sessions.py script that handles date comparison and reports result to the LLM.

#### enhancement-3 — remove: Prompt Quality Canon is wrong-genre reference for a spec-writing agent

- Lens: enhancement
- Location: `references/prompt-quality-canon.md`
- Evidence: The canon teaches prompt authoring; this agent writes specs and plans. The 1652-token file loads every session via the CREED standing order.
- Recommendation: Replace with a spec-quality-canon.md or remove entirely. At minimum, move the standing order to fire only on replan, not every session.

#### enhancement-4 — remove: Sacred Truth duplicated verbatim across SKILL.md and CREED-template.md

- Lens: enhancement
- Location: `SKILL.md:20-23 and assets/CREED-template.md:3-9`
- Evidence: Near-verbatim ~200 token block appears in both files, loaded on every session.
- Recommendation: Keep shorter version in SKILL.md; replace CREED.md's copy with a one-line reference: 'See The Sacred Truth in SKILL.md.'

#### enhancement-5 — add: rescope capability for full project pivots

- Lens: enhancement
- Location: `references/replan.md:1-28`
- Evidence: replan handles re-cutting a phase but not a full pivot. A returning user who changed their project direction has no clean reset path.
- Recommendation: Add a `rescope` capability that archives the current plan, clears active phase statuses, and starts a fresh brainstorm cycle.

#### enhancement-6 — remove: empty capabilities/ directory causes confusion

- Lens: enhancement
- Location: `capabilities/`
- Evidence: Empty directory with no .gitkeep or README. All capabilities are in references/. Signals either bug or unimplemented feature.
- Recommendation: Remove the empty capabilities/ directory and route all discovery through references/ only.

### Medium (13)

#### architecture-2 — Sacred Truth duplicated verbatim in bootloader and CREED template

- Lens: architecture
- Location: `SKILL.md:19-23 / CREED-template.md:3-9`
- Evidence: 109-word Sacred Truth passage appears identically in both files with minor edits, already drifting out of sync.
- Recommendation: Keep Sacred Truth in CREED-template.md only. Replace in SKILL.md with one-liner reference.

#### architecture-3 — Three Laws defined in bootloader but absent from CREED template

- Lens: architecture
- Location: `SKILL.md:9-17 vs CREED-template.md`
- Evidence: Three Laws present only in bootloader — absent from CREED. After First Breath, sanctum becomes identity source and the Laws vanish.
- Recommendation: Add Three Laws to CREED-template.md. Keep short reference in SKILL.md.

#### architecture-4 — Empty capabilities/ directory

- Lens: architecture
- Location: `capabilities/`
- Evidence: Root-level capabilities/ directory exists but is empty. All capability logic is in references/.
- Recommendation: Remove the directory or add a .gitkeep with explanatory comment.

#### leanness-2 — decompose.md: numbered list of independent rules masquerading as sequence

- Lens: leanness
- Location: `references/decompose.md:17-23`
- Evidence: 7 rules in a numbered list. These are independent obligations, not sequential steps.
- Recommendation: Replace with a single goal sentence describing domain conventions.

#### leanness-3 — spec.md: numbered section template disguises independent sections as sequence

- Lens: leanness
- Location: `references/spec.md:17-25`
- Evidence: 8 section headings numbered. These are independent document sections, not sequential steps.
- Recommendation: Collapse to one sentence describing what to cover.

#### leanness-6 — CREED-template: same constraints repeated across four sections

- Lens: leanness
- Location: `assets/CREED-template.md:15-63`
- Evidence: "no code" appears in Core Values and Boundaries. "User validates" appears in Core Values, Standing Orders, Boundaries, and Anti-Patterns. Four sections covering same 5-6 rules.
- Recommendation: Merge Standing Orders and Boundaries. Fold Anti-Patterns Behavioral into a short note. Remove Anti-Patterns Operational.

#### determinism-3 — Placeholder pattern scanning assigned to LLM during First Breath

- Lens: determinism
- Location: `references/first-breath.md:96`
- Evidence: "scan sanctum files for remaining {...} placeholder instructions" — regex pattern matching asked of the LLM.
- Recommendation: Script the placeholder scan into init-sanctum.py or a validate-sanctum.py post-pass.

#### agent-cohesion-1 — No formal validation or consistency-check capability

- Lens: agent-cohesion
- Location: `SKILL.md references/ and all capability files`
- Evidence: No capability to systematically check cross-phase consistency: do dependencies resolve? Are all PRD features mapped?
- Recommendation: Add a `validate` capability that scans all project artifacts for consistency gaps.

#### agent-cohesion-2 — Workspace initialization is implicit, not a capability

- Lens: agent-cohesion
- Location: `references/brainstorm.md`
- Evidence: Init responsibility 'Créer masb-workspace/' is not handled by any capability. brainstorm.md doesn't ensure workspace exists.
- Recommendation: Add workspace scaffolding to brainstorm or introduce a lightweight init capability.

#### sanctum-1 — SKILL.md bootloader exceeds ~400 token guardrail at 1131 tokens

- Lens: sanctum-architecture
- Location: `SKILL.md:1-60`
- Evidence: 1131 tokens vs ~400 guardrail. Includes persona-level directives (Stay in Character) that belong in sanctum.
- Recommendation: Move Stay in Character and Persistent Memory narrative into PERSONA and CREED templates.

#### enhancement-7 — add: lightweight mode for trivial projects

- Lens: enhancement
- Location: `references/decompose.md:21`
- Evidence: A single-screen utility does not need design system phase or multi-phase decomposition. Rules calibrated for medium-to-large apps.
- Recommendation: Add a project-size classifier in brainstorm. Route to lightweight (single phase) or standard flow.

#### enhancement-8 — add: existing-codebase analysis capability

- Lens: enhancement
- Location: `SKILL.md:60`
- Evidence: No capability for users with an existing Android project. Assumes greenfield.
- Recommendation: Add an `audit` capability that reads existing project structure and produces gap analysis.

#### enhancement-9 — add: progress visibility and status summary capability

- Lens: enhancement
- Location: `references/decompose.md:13`
- Evidence: Only status artifact is phases-index.md. No capability summarizes what's done, blocked, or next.
- Recommendation: Add a `status` capability that reads phases-index.md + all progress.md files and produces a concise project dashboard.

### Low (14)

#### sanctum-2 — First Breath discovery question count exceeds 3-7 recommendation

- Lens: sanctum-architecture
- Location: `references/first-breath.md:38-60`
- Evidence: ~15 individual discovery questions across 4 categories, exceeding the 3-7 guidance for configuration-style First Breath.
- Recommendation: Consolidate to 5-7 highest-value questions. Keep category headers as guidance, reduce explicit question list.

#### architecture-5 — Frontmatter description mixes French and English

- Lens: architecture
- Location: `SKILL.md:3`
- Evidence: Role description is French, trigger phrase is English. Inconsistent with entirely French capability descriptions.
- Recommendation: Normalize to all-French or match the agent's predominant language.

#### determinism-4 — Structural validation rules embedded in decompose prompt

- Lens: determinism
- Location: `references/decompose.md:17-23`
- Evidence: Naming conventions and folder structure rules that the LLM must both create and validate — validation side is deterministic.
- Recommendation: After decompose creates structure, run a validate-phases.py that checks patterns and required files.

#### leanness-4 — prd.md: section template re-teaches standard PRD structure

- Lens: leanness
- Location: `references/prd.md:17-24`
- Evidence: 7-section PRD template. Any capable model knows PRD structure — the consumer definition alone does the work.
- Recommendation: Remove the section template. Let the consumer definition carry the bar.

#### leanness-5 — brainstorm.md: persona restated in capability prompt

- Lens: leanness
- Location: `references/brainstorm.md:9-10`
- Evidence: "Tu es l'architecte logiciel... Tu ne codes pas" — persona already inherited from bootloader and sanctum.
- Recommendation: Remove lines 9-10. Start at 'Ouvre le dialogue avec une invitation large.'

#### leanness-7 — memory-guidance.md: session log format template teaches markdown

- Lens: leanness
- Location: `references/memory-guidance.md:41-53`
- Evidence: Formatted markdown template for session log entries. Model already writes markdown fluently.
- Recommendation: Collapse format template to one line describing convention.

#### agent-cohesion-3 — decompose and replan share overlapping mechanics

- Lens: agent-cohesion
- Location: `references/decompose.md vs references/replan.md`
- Evidence: Both write to phases-index.md and create directories. Boundary could blur as agent evolves.
- Recommendation: Document the boundary more sharply or unify into a single decompose with initial/replan mode.

#### agent-cohesion-4 — prompt-quality-canon excluded from sanctum but referenced by CREED

- Lens: agent-cohesion
- Location: `scripts/init-sanctum.py:12 and assets/CREED-template.md:36-37`
- Evidence: init-sanctum.py lists canon in SKILL_ONLY_FILES (not copied to sanctum). CREED references it from skill root.
- Recommendation: Either copy canon to sanctum or add a check noting its path for non-standard invocations.

#### agent-cohesion-5 — Phase 00 hardcoded as 'always design system' limits modularity

- Lens: agent-cohesion
- Location: `references/decompose.md:21`
- Evidence: Hardcoded rule makes agent less reusable outside MASB. Projects without UI needs still get phase 00.
- Recommendation: Make phase-00 assignment configurable with MASB default.

#### enhancement-10 — remove: The Three Laws framing adds ceremony without enforceable value

- Lens: enhancement
- Location: `SKILL.md:9-15`
- Evidence: 6-line Asimov-style laws. 'Never cause harm' and 'Obey' already enforced by base model training. Only 'preserve yourself' (sanctum protection) is genuinely useful.
- Recommendation: Replace with single line: 'Your sanctum is your continuity. Protect it.' Move owner-obedience to CREED Boundaries.

#### enhancement-11 — add: non-Android guard or multi-platform extension point

- Lens: enhancement
- Location: `SKILL.md:1-4`
- Evidence: Branded Android-only. A user asking for iOS/web/Flutter gets no guardrail.
- Recommendation: Add a platform check in brainstorm, or generalize architecture principles.

#### enhancement-12 — remove: discovery question list is over-structured per agent's own canon

- Lens: enhancement
- Location: `references/first-breath.md:36-60`
- Evidence: 18+ questions in 5 categories IS the script the prompt-quality-canon warns against.
- Recommendation: Replace question categories with outcome-stated goals.

#### enhancement-13 — add: --dry-run or --just-status flag for wake.py

- Lens: enhancement
- Location: `scripts/wake.py:30-32`
- Evidence: No lightweight mode. Every waking loads all 6 identity files.
- Recommendation: Add a --status flag that prints only MEMORY.md + one-liner summary.

#### enhancement-14 — add: capture-don't-interrupt posture in brainstorm.md

- Lens: enhancement
- Location: `references/brainstorm.md:13`
- Evidence: Save-as-you-go could interrupt user's stream if agent saves mid-sentence.
- Recommendation: Add explicit guidance: save only at natural pauses, not mid-stream.
