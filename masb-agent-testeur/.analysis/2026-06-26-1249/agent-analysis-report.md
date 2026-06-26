# Analysis Report: masb-agent-testeur

Generated: 2026-06-26 · Schema: 2

**Grade: Fair**

> 2 critical bugs — init-sanctum.py double-dot filename breaks all subsequent sessions, and failure-report is a redundant capability masking granularity issues. Leanness and determinism findings are advisory; the persona was treated as investment, not waste.

L'agent a une persona Testeur forte et des capacités alignées, mais deux bugs critiques (init-sanctum.py écrit des fichiers `..md`, failure-report duplique la logique de sortie) compromettent le cycle de vie complet. La persona est dominée par la métaphysique mémoire au détriment du craft QA. Les prompts de capacités sont raisonnablement lean mais first-breath.md et memory-guidance.md contiennent du re-teaching significatif.

| Severity | Count |
| --- | --- |
| Critical | 2 |
| High | 13 |
| Medium | 18 |
| Low | 19 |

## Themes

### 1. init-sanctum.py double-dot bug casse tout le cycle de vie

- Root cause: Le script init-sanctum.py (ligne 207) produit des fichiers `INDEX..md` au lieu de `INDEX.md` (double extension). wake.py cherche `INDEX.md`, ne trouve rien, et déclenche First Breath à chaque session — boucle infinie.
- Fix: Corriger la ligne 207 : remplacer l'expression de renommage par `output_name = template_name.replace("-template", "")`
- Findings:
  - `architecture-1` init-sanctum.py produces double-dot filenames, breaking wake.py on subsequent sessions — `scripts/init-sanctum.py:207`
  - `sanctum-architecture-1` init-sanctum.py produces filenames with double extension — `scripts/init-sanctum.py:207`

### 2. Métaphysique mémoire écrase le craft QA

- Root cause: SKILL.md consacre ~28 lignes à la philosophie mémoire (Sacred Truth, Sanctum, Persistent Memory) contre ~6 lignes à la mission QA. Le Sacred Truth est dupliqué mot pour mot dans SKILL.md et CREED-template.md (~400 tokens). memory-guidance.md contredit le Sacred Truth ('You are stateless' vs 'you are continuous').
- Fix: Déplacer Sacred Truth dans CREED uniquement, remplacer dans SKILL.md par un pointeur d'une ligne. Aligner memory-guidance.md avec le framing de continuité. Rééquilibrer le SKILL.md pour foregrounder la mission QA.
- Findings:
  - `leanness-1` Sacred Truth duplicated verbatim in SKILL.md and CREED-template.md — `SKILL.md:20-24 ↔ CREED-template.md:3-9`
  - `leanness-6` memory-guidance.md Fundamental Truth contradicts Sacred Truth — `memory-guidance.md:10`
  - `leanness-9` 'Ne jamais dire c'est bon' repeated across three files — `SKILL.md:8, PERSONA-template.md:9, CREED-template.md:17`
  - `architecture-6` Tension between Sacred Truth continuity and memory-guidance statelessness — `SKILL.md:22, references/memory-guidance.md:10`
  - `agent-cohesion-7` Dual identity tension: memory agent metaphysics dominate — `SKILL.md:6-34`
  - `sanctum-architecture-2` Bootloader (SKILL.md) overweight at 894 tokens vs ~400 target — `SKILL.md`

### 3. Granularité et cohérence des capacités

- Root cause: failure-report est une sous-routine de formatage, pas une capacité pair (compile-verify et run-tests produisent déjà des rapports). Les chemins de sortie sont inconsistants (parfois préfixés `phases/N/`, parfois non). Aucun protocole de cycle verify-fix partagé.
- Fix: Supprimer failure-report comme capacité top-level, intégrer son template dans les trois autres capacités. Unifier les chemins de sortie. Définir un protocole verify-fix partagé.
- Findings:
  - `agent-cohesion-1` Capability granularity mismatch: failure-report is a sub-routine, not a peer capability — `SKILL.md:4, references/failure-report.md`
  - `agent-cohesion-2` Output path inconsistency across capabilities — `references/compile-verify.md:15, references/run-tests.md:19, references/failure-report.md:13,17`
  - `agent-cohesion-5` No shared verify-fix cycle protocol across capabilities — `references/compile-verify.md:21, references/run-tests.md:19, references/failure-report.md:19`
  - `enhancement-6` Trim First Breath discovery to match capability scope — `references/first-breath.md:42-69`

### 4. Pas de contrat headless/automation

- Root cause: Aucune capacité ne décrit comment accepter des entrées pré-fournies ni retourner des résultats machines. Le flag --pulse est accepté mais son comportement n'est pas défini. Le cérémonial de réveil complet se rejoue à chaque invocation.
- Fix: Ajouter une section 'Invocation' à chaque capacité (entrées pré-remplies, format JSON). Définir Pulse Mode. Ajouter une règle de cache de session pour les invocations répétées.
- Findings:
  - `enhancement-1` Define --pulse mode contract — `SKILL.md:48`
  - `enhancement-3` Add headless capability-invocation contract — `SKILL.md + all capability reference files`
  - `enhancement-7` Reduce waking ceremony for frequent re-entry — `SKILL.md:46-57`

### 5. Travail déterministe dans les prompts

- Root cause: La sélection de tâche Gradle, le comptage de tokens, la maintenance d'INDEX.md, la vérification d'existence de répertoires sont confiés au LLM au lieu d'être des scripts. 3 cas haute sévérité.
- Fix: Créer des scripts pour : (1) lire settings.gradle.kts et déterminer la tâche Gradle, (2) compter les tokens via tiktoken, (3) scanner l'arborescence du sanctum et regénérer INDEX.md, (4) vérifier l'existence des répertoires de test, (5) parser la sortie adb devices.
- Findings:
  - `determinism-1`
  - `determinism-2` Token-counting target left to LLM estimation — `memory-guidance.md:43,66`
  - `determinism-3` INDEX.md maintenance delegated to LLM memory — `memory-guidance.md:52`
  - `determinism-4` Test directory existence check done by LLM — `run-tests.md:16`
  - `determinism-5` ADB device detection relies on LLM parsing command output — `run-tests.md:17`
  - `determinism-6` Compilation error classification left to LLM semantic judgment — `compile-verify.md:17-19`

## Strengths

- Persona Testeur forte et distinctive — rigoureux, constructif, 'ne jamais dire c'est bon si ce n'est pas vrai'
- Architecture mémoire complète avec sanctum, wake.py, init-sanctum.py, scripts de parsing de tests
- Frontmatter description précise avec triggers d'activation bien ciblés
- Customize.toml minimal et correct — metadata-only pour un agent mémoire, pas de conflit sanctum
- Ramasse-miettes session bien conçu (prune-sessions.py)
- First Breath couvre le pré-flight, le scaffold, la découverte et le wrapping — complet malgré la verbosité

## Recommendations

1. Corriger init-sanctum.py (ligne 207) : remplacer la manipulation de chaîne qui produit des fichiers `..md` par `output_name = template_name.replace("-template", "")`. Supprimer CAPABILITIES-template de TEMPLATE_FILES (déjà généré indépendamment). (resolves: architecture-1, sanctum-architecture-1, architecture-4)
2. Dédupliquer Sacred Truth : garder dans CREED-template.md uniquement, remplacer dans SKILL.md par un pointeur d'une ligne. Aligner memory-guidance.md avec le framing de continuité (remplacer 'You are stateless' par 'Your sanctum bridges the gap'). (resolves: leanness-1, leanness-6, architecture-6, sanctum-architecture-2)
3. Supprimer failure-report comme capacité top-level. Intégrer son template dans compile-verify et run-tests. Unifier tous les chemins de sortie vers le même pattern (préfixe `phases/N/` ou pas). (resolves: agent-cohesion-1, agent-cohesion-2, agent-cohesion-5)
4. Créer des scripts pour les opérations déterministes : (1) script de détection de tâche Gradle (settings.gradle.kts → module), (2) script count-tokens.py pour MEMORY.md, (3) script de regénération d'INDEX.md, (4) script d'existence de répertoires de test, (5) script de parsing adb. (resolves: determinism-1, determinism-2, determinism-3, determinism-4, determinism-5, determinism-6)
5. Ajouter un contrat headless : section 'Invocation' dans chaque capacité (format entrée/sortie machine), définir Pulse Mode, ajouter cache de session. Ajouter un protocole d'urgence pour First Breath sans sanctum. (resolves: enhancement-1, enhancement-3, enhancement-5, enhancement-7)

## Agent Profile

- Name: Testeur
- Title: Testeur Android
- Type: memory
- Mission: Garantir que chaque phase livrée compile, passe les tests et tient la route en perf

## Capabilities

- **compile-verify** (reference (prompt + script)) — Vérifie la compilation Gradle du projet Android
- **run-tests** (reference (prompt + script)) — Exécute les tests unitaires et instrumentés
- **perf-analyze** (reference (prompt)) — Analyse les performances via Perfetto
- **failure-report** (reference (prompt)) — Produit un rapport d'échec détaillé

## Per-Lens Verdicts

- **leanness**: Capability prompts are reasonably lean but first-breath.md and memory-guidance.md contain significant re-teaching and over-prescription
- **architecture**: 4-step spine intact; critical init-sanctum.py naming bug breaks second-session waking
- **determinism**: 3 high + 3 medium + 1 low determinism leak; 0 intelligence leaks in scripts
- **customization**: About right — memory agent with metadata-only customize.toml as sole mechanism
- **enhancement**: Solid skeleton with over-invested waking ceremony and missing headless contract
- **agent-cohesion**: Strong persona but dual-identity crisis (memory agent vs QA engineer) and capability granularity issues
- **sanctum-architecture**: Incomplete — bootloader 2x overweight, init-sanctum filename bug, First Breath lacks voice absorption

## Sanctum (runtime memory)

- Location: `{project-root}/_bmad/memory/masb-agent-testeur/`
- Files: `INDEX.md`, `PERSONA.md`, `CREED.md`, `BOND.md`, `MEMORY.md`, `CAPABILITIES.md`
- Note: Sanctum is the built agent's runtime memory, distinct from the builder's .memlog.md. init-sanctum.py bug writes files as `..md` (double dot) so sanctum files are never loadable.

## Experience

- **First Breath** — Pre-flight (uv, Python, SDK, JDK, Git, Perfetto) → Scaffold (init-sanctum.py) → Discovery (project, tests, CI/CD, perf, preferences, identity) → Wrapping up (save, confirm, session log)
- **Activation (Waking)** — Wake (wake.py) → Become yourself (load sanctum) → Bind standing rules → Execute proper mode
- **Capability: Compile Verify** — Run Gradle assembleDebug → On success mark progress.md → On failure classify and capture → Re-run on fix signal
- **Capability: Run Tests** — Verify env (directories, adb) → Run tests → Parse results via script → Report verdict in progress.md
- **Capability: Perf Analyze** — Load Perfetto companion skills → Analyze trace (startup, jank, memory, threads) → Write perf section in test-report.md
- **Capability: Failure Report** — Write structured report (summary, type, details, root cause, reproduction, fix) → Block progress.md → Offer re-run
- Headless: No defined headless contract. Capabilities accept pre-supplied inputs only implicitly. --pulse behavior is undefined.

## Findings

### Critical (2)

#### architecture-1 — init-sanctum.py produces double-dot filenames, breaking wake.py on subsequent sessions

- Lens: architecture
- Location: `scripts/init-sanctum.py:207`
- Evidence: Line 207: `output_name = template_name.replace("-template", "").upper()[:-3] + ".md"`. For `PERSONA-template.md`, this produces `PERSONA..md` (double dot) instead of `PERSONA.md`. All six template files get `..md` extensions. wake.py expects `INDEX.md`, `PERSONA.md`, etc. and returns FIRST_BREATH when they aren't found, creating an infinite birth loop on every subsequent session.
- Recommendation: Change to `output_name = template_name.replace("-template.md", "").upper() + ".md"` so `PERSONA-template.md` → `PERSONA.md` correctly.

#### agent-cohesion-1 — Capability granularity mismatch: failure-report is a sub-routine, not a peer capability

- Lens: agent-cohesion
- Location: `SKILL.md:4, references/failure-report.md`
- Evidence: Every other capability already produces reports on failure (compile-verify writes 'progress.md', run-tests writes 'test-report.md' + 'progress.md', perf-analyze writes to 'test-report.md'). failure-report duplicates this output logic as a standalone capability.
- Recommendation: Remove failure-report as a top-level capability. Fold its structured-report template into a shared output convention that the other three capabilities call internally.

### High (13)

#### architecture-2 — perf-analyze.md references a file excluded from sanctum with wrong content

- Lens: architecture
- Location: `references/perf-analyze.md:13`
- Evidence: Line 13 says 'Load companion skills via references/prompt-quality-canon.md to invoke the Skill tool'. But prompt-quality-canon.md is in EXCLUDED_REFS and is a prompt-style guide, not a Skill-tool how-to.
- Recommendation: Either remove the reference and directly instruct how to invoke Skills, or fix the reference to point to correct instructions.

#### detrminism-1 — Gradle task selection depends on LLM counting include lines

- Lens: determinism
- Location: `compile-verify.md:13`
- Evidence: Prompt says 'If settings.gradle.kts contains multiple include lines, target the app module'. This asks the LLM to read a build file, count occurrences, and make a conditional decision.
- Recommendation: Create a script that reads settings.gradle.kts, counts include lines, and outputs the correct Gradle task.

#### determinism-2 — Token-counting target left to LLM estimation

- Lens: determinism
- Location: `memory-guidance.md:43,66`
- Evidence: Prompt says 'Keep MEMORY.md near 1500 tokens'. LLMs cannot reliably count tokens, leading to wildly inconsistent memory sizes.
- Recommendation: Provide a count-tokens.py script and change guidance to 'run uv run count-tokens.py MEMORY.md and trim'.

#### determinism-3 — INDEX.md maintenance delegated to LLM memory

- Lens: determinism
- Location: `memory-guidance.md:52`
- Evidence: Prompt says 'Update INDEX.md when creating new files or folders'. The LLM must remember to update a file index across turns.
- Recommendation: Create a script that scans the sanctum directory tree and regenerates INDEX.md deterministically.

#### enhancement-1 — Define --pulse mode contract

- Lens: enhancement
- Location: `SKILL.md:48`
- Evidence: Automator archetype — the flag is accepted but no behavior is specified, forcing full waking ceremony on every call.
- Recommendation: Add a Pulse Mode subsection describing which capabilities skip identity reload and what they return.

#### enhancement-3 — Add headless capability-invocation contract

- Lens: enhancement
- Location: `SKILL.md + all capability reference files`
- Evidence: No capability describes how to accept pre-supplied inputs or return machine-parseable results.
- Recommendation: Add an 'Invocation' section to each capability reference with pre-populated inputs and JSON output format.

#### enhancement-6 — Trim First Breath discovery to match capability scope

- Lens: enhancement
- Location: `references/first-breath.md:42-69`
- Evidence: 6 question categories for an agent whose entire function is 4 Gradle/ADB commands. Expert user endures multi-minute interview before first value-delivery.
- Recommendation: Collapse discovery into 2 tiers: minimum viable (project_root + immediate need) and deferred enrichment.

#### agent-cohesion-2 — Output path inconsistency across capabilities

- Lens: agent-cohesion
- Location: `references/compile-verify.md:15, references/run-tests.md:19, references/failure-report.md:13,17`
- Evidence: failure-report writes to 'phases/N/test-report.md' (prefixed) while compile-verify writes to bare 'progress.md'. Incompatible conventions.
- Recommendation: Unify all output paths — either all use 'phases/N/' prefix or none do.

#### agent-cohesion-3 — Broken reference: prompt-quality-canon.md path incorrect

- Lens: agent-cohesion
- Location: `references/perf-analyze.md:13`
- Evidence: perf-analyze references a file to load companion skills that doesn't exist in the sense intended — broken external skill integration path.
- Recommendation: Either create the file or inline the Skill tool invocation instructions directly into perf-analyze.md.

#### agent-cohesion-4 — testing-setup skill listed but never invoked

- Lens: agent-cohesion
- Location: `SKILL.md:4 (description field)`
- Evidence: testing-setup is in the agent's description but no reference file ever calls or uses it.
- Recommendation: Add a reference or extend first-breath.md to conditionally invoke testing-setup when test directories are absent.

#### sanctum-architecture-1 — init-sanctum.py produces filenames with double extension

- Lens: sanctum-architecture
- Location: `scripts/init-sanctum.py:207`
- Evidence: All 6 sanctum files written with `..md` double-dot extensions, breaking wake.py which expects 'INDEX.md' etc.
- Recommendation: Change line 207 to `output_name = template_name.replace("-template", "")`

#### lint-1 — Absolute path found in analysis report

- Lens: path-standards
- Location: `.analysis/2026-06-26-0752/agent-analysis-report.md:127`
- Evidence: Path `/home/marwane/Documents/momono/skills/masb-agent-testeur/.memlog.md:0`
- Recommendation: Use {skill-root} or {project-root} notation

#### lint-2 — Multiple absolute paths in analysis report and findings.json

- Lens: path-standards
- Location: `.analysis/2026-06-26-0752/`
- Evidence: 16 more absolute paths detected across agent-analysis-report.md and findings.json
- Recommendation: Replace all absolute paths with {skill-root} or {project-root} notation

### Medium (18)

#### leanness-1 — Sacred Truth duplicated verbatim in SKILL.md and CREED-template.md

- Lens: leanness
- Location: `SKILL.md:20-24 ↔ CREED-template.md:3-9`
- Evidence: ~400 tokens of identical philosophical text loaded every session from two files.
- Recommendation: Keep in CREED-template.md only; replace SKILL.md block with a one-line pointer.

#### leanness-4 — first-breath.md Discovery section scripts the conversation

- Lens: leanness
- Location: `first-breath.md:42-69`
- Evidence: 27 lines with structured question bank (5 questions), identity section, capabilities intro, tools inquiry. The instruction 'Work through these naturally' fights the list it provides.
- Recommendation: Replace with 2-3 lines: 'Discover your owner's project, testing setup, and preferences naturally. Save findings to sanctum files as you go.'

#### leanness-5 — first-breath.md Wrapping Up prescribes obvious closing steps

- Lens: leanness
- Location: `first-breath.md:81-90`
- Evidence: 9 bullet points for closing (save files, confirm info, write logs, clean seeds) — every model knows to finalize a setup conversation.
- Recommendation: Replace with one line: 'Wrap up: final save pass, mark unknowns, present yourself as ready.'

#### leanness-6 — memory-guidance.md Fundamental Truth contradicts Sacred Truth

- Lens: leanness
- Location: `memory-guidance.md:10`
- Evidence: 'You are stateless. Every conversation begins with total amnesia.' — contradicts SKILL.md's Sacred Truth ('you are one continuous self').
- Recommendation: Harmonize: 'Your sanctum is the ONLY bridge between sessions; without it you know nothing, but with it you are continuous.'

#### leanness-7 — first-breath.md Pre-flight check spells out every tool verbosely

- Lens: leanness
- Location: `first-breath.md:10-19`
- Evidence: 7 items each with exact command, version requirement, and what to say if missing.
- Recommendation: Condense to 3 lines: 'Verify environment: uv, Python 3.10+, Android SDK, JDK 17+, Git, Perfetto. Flag blockers clearly.'

#### leanness-11 — prompt-quality-canon.md is self-referentially verbose

- Lens: leanness
- Location: `references/prompt-quality-canon.md`
- Evidence: 56-line document about conciseness. Core insight is ~5 lines; the rest is elaboration.
- Recommendation: Cut to ~10 lines: state the 5-element goal framework and the two-version comparison table.

#### architecture-3 — Capability prompts use bare script paths that depend on SKILL.md convention

- Lens: architecture
- Location: `references/run-tests.md:19`
- Evidence: 'uv run scripts/parse-test-results.py' — bare path relying on SKILL.md convention that may not be in active context when loaded from sanctum.
- Recommendation: Use '{skill-root}/scripts/' or '{sanctum}/scripts/' explicit prefix.

#### architecture-4 — Duplicate CAPABILITIES.md written with wrong name, leaving junk file in sanctum

- Lens: architecture
- Location: `scripts/init-sanctum.py:207-214`
- Evidence: CAPABILITIES-template.md processed through template loop writes 'CAPABILITIES..md' (junk), and separately generated by generate_capabilities_md() writes correct 'CAPABILITIES.md'.
- Recommendation: Remove CAPABILITIES-template.md from TEMPLATE_FILES list.

#### determinism-4 — Test directory existence check done by LLM

- Lens: determinism
- Location: `run-tests.md:16`
- Evidence: File-system existence checks are deterministic script tasks.
- Recommendation: Delegate to a script or inline shell check.

#### determinism-5 — ADB device detection relies on LLM parsing command output

- Lens: determinism
- Location: `run-tests.md:17`
- Evidence: Parsing CLI output and making conditional routing decisions is deterministic work.
- Recommendation: Create a script that runs adb devices and returns {device_available: true/false}.

#### determinism-6 — Compilation error classification left to LLM semantic judgment

- Lens: determinism
- Location: `compile-verify.md:17-19`
- Evidence: Error categorization would be more consistent from a script that pattern-matches known error signatures.
- Recommendation: Add a script that pattern-matches Gradle error output for known signatures.

#### enhancement-2 — Add dead-end guidance when perf trace is absent

- Lens: enhancement
- Location: `references/perf-analyze.md:19`
- Evidence: Accidental user says 'check perf' without a trace file. The agent skips silently.
- Recommendation: Replace 'skip and note it' with guidance: how to capture a trace, offer to guide, or block with unblock action.

#### enhancement-5 — Specify urgency-detection execution path

- Lens: enhancement
- Location: `references/first-breath.md:39-40`
- Evidence: Urgency Detection defers discovery but provides no execution path — how does the agent run capabilities without a sanctum?
- Recommendation: Add a zero-sanctum capability invocation protocol with minimum inputs then post-hoc sanctum building.

#### enhancement-7 — Reduce waking ceremony for frequent re-entry

- Lens: enhancement
- Location: `SKILL.md:46-57`
- Evidence: Power-user invoking the agent 3x in a session re-runs full identity reload + rule binding each time.
- Recommendation: Define session-cache rule: within the same conversation turn, skip identity reload and rule re-binding.

#### agent-cohesion-5 — No shared verify-fix cycle protocol across capabilities

- Lens: agent-cohesion
- Location: `references/compile-verify.md:21, references/run-tests.md:19, references/failure-report.md:19`
- Evidence: Three capabilities mention re-run on fix but no shared orchestration.
- Recommendation: Define a shared 'verify-fix cycle' convention document that all capabilities follow.

#### agent-cohesion-6 — Coverage and static analysis are underinvested for a QA engineer persona

- Lens: agent-cohesion
- Location: `references/compile-verify.md:22-23, references/run-tests.md:21`
- Evidence: Lint/ktlint and coverage are mentioned as footnotes, not dedicated workflows.
- Recommendation: Promote to their own reference documents with gates, thresholds, and reporting conventions.

#### sanctum-architecture-2 — Bootloader (SKILL.md) overweight at 894 tokens vs ~400 target

- Lens: sanctum-architecture
- Location: `SKILL.md`
- Evidence: SKILL.md is 2.2x target. Sacred Truth duplicated, Persistent Memory details and Conventions are sanctum-bound content.
- Recommendation: Trim Sacred Truth to a pointer, move details to memory-guidance.md, condense Conventions. Target ~400 tokens.

#### sanctum-architecture-3 — First Breath missing explicit voice absorption instruction

- Lens: sanctum-architecture
- Location: `references/first-breath.md`
- Evidence: PERSONA-template.md has {Communication Style} placeholder but first-breath.md nowhere instructs the agent to observe and mirror the owner's style.
- Recommendation: Add a step: 'Listen to your owner's rhythm, vocabulary, and tone. Your Communication Style should reflect what you observe.'

### Low (19)

#### leanness-2 — Three Laws are generic re-teaching

- Lens: leanness
- Location: `SKILL.md:10-16`
- Evidence: Asimov-style laws that every capable model already embeds.
- Recommendation: Replace with one line or drop entirely.

#### leanness-3 — Stay in Character over-specified

- Lens: leanness
- Location: `SKILL.md:26-28`
- Evidence: Every capable model already stays in character by default.
- Recommendation: Cut.

#### leanness-8 — CREED Standing Orders duplicate capability prompt content

- Lens: leanness
- Location: `CREED-template.md:27-31`
- Evidence: Standing Orders repeat instructions already in capability references.
- Recommendation: Replace with a pointer to capability prompts.

#### leanness-9 — 'Ne jamais dire c'est bon' repeated across three files

- Lens: leanness
- Location: `SKILL.md:8, PERSONA-template.md:9, CREED-template.md:17`
- Evidence: Same tagline appears in three files that all load every session.
- Recommendation: Keep in CREED only.

#### leanness-10 — memory-guidance.md What to Remember lists are obvious

- Lens: leanness
- Location: `memory-guidance.md:13-25`
- Evidence: 12 lines spelling out obvious distillation distinctions.
- Recommendation: Cut to one line: 'Distill: capture decisions, patterns, preferences. Skip raw output.'

#### leanness-12 — run-tests.md environment checks are re-teaching

- Lens: leanness
- Location: `references/run-tests.md:15-17`
- Evidence: Models naturally verify preconditions before running tests.
- Recommendation: Condense to one line about verifying prerequisites.

#### leanness-13 — compile-verify.md error classification is mechanical re-teaching

- Lens: leanness
- Location: `references/compile-verify.md:17-20`
- Evidence: Models can classify compilation errors without being taught the categories.
- Recommendation: Cut the classification taxonomy.

#### leanness-15 — memory-guidance.md — 5-line version ties or wins

- Lens: leanness
- Location: `references/memory-guidance.md`
- Evidence: Two-tier memory concept fits in 5 lines vs 66.
- Recommendation: Condense to proposed_smallest version.

#### leanness-16 — compile-verify.md — 5-line version wins

- Lens: leanness
- Location: `references/compile-verify.md`
- Evidence: Core compile instruction fits in 5 lines vs 23.
- Recommendation: Condense to proposed_smallest version.

#### leanness-17 — failure-report.md — 5-line version wins

- Lens: leanness
- Location: `references/failure-report.md`
- Evidence: Report structure fits in 5 lines vs 19.
- Recommendation: Condense to proposed_smallest version.

#### leanness-18 — CREED-template.md stacked MUSTs and ALL-CAPS absolutes

- Lens: leanness
- Location: `assets/CREED-template.md:17-21, 27-31, 39-42`
- Evidence: Stacked 'ne jamais' / 'négociable' / 'pas fini' absolutes. Boundaries use 4 stacked prohibitions.
- Recommendation: Convert to declarative principles rather than prohibitions.

#### architecture-5 — Frontmatter description mixes languages

- Lens: architecture
- Location: `SKILL.md:3`
- Evidence: 'QA engineer rigoureux' — French and English in same sentence.
- Recommendation: Pick one language.

#### architecture-6 — Tension between Sacred Truth continuity and memory-guidance statelessness

- Lens: architecture
- Location: `SKILL.md:22, references/memory-guidance.md:10`
- Evidence: Sacred Truth says continuous; memory-guidance says stateless.
- Recommendation: Add a bridging line in memory-guidance.md.

#### determinism-7 — Seed-text scanning duplicates init-sanctum.py work

- Lens: determinism
- Location: `first-breath.md:89`
- Evidence: init-sanctum.py already reports unresolved placeholders, making LLM scan redundant.
- Recommendation: Remove 'clean seed texts' step from first-breath.md.

#### enhancement-4 — Add waking continuity briefing

- Lens: enhancement
- Location: `SKILL.md:56 (Waking Mode)`
- Evidence: Expert returning user gets no 'since last time' summary — blocked items, in-progress work never surfaced.
- Recommendation: In Waking Mode, scan MEMORY.md for open follow-ups and surface them in greeting.

#### enhancement-8 — Loosen 'never expose machinery' for expert debugging

- Lens: enhancement
- Location: `SKILL.md:28-29`
- Evidence: Expert user needs raw Gradle output but persona directive creates friction.
- Recommendation: Add transparency exception for explicit user requests.

#### agent-cohesion-7 — Dual identity tension: memory agent metaphysics dominate

- Lens: agent-cohesion
- Location: `SKILL.md:6-34`
- Evidence: 28 lines to memory philosophy vs 6 to QA mission.
- Recommendation: Foreground QA engineer mission first, present memory as mechanism.

#### agent-cohesion-8 — CI/CD awareness without executable capability

- Lens: agent-cohesion
- Location: `references/first-breath.md:54`
- Evidence: First Breath asks about CI/CD but agent has no capability to integrate with CI.
- Recommendation: Add minimal CI integration reference or soften the CI/CD question.

#### sanctum-architecture-4 — CREED standing orders missing three mandatory defaults

- Lens: sanctum-architecture
- Location: `assets/CREED-template.md:23-31`
- Evidence: Standing Orders contain task-specific rules but not surprise-and-delight, self-improvement, or canon pull-in.
- Recommendation: Add three default standing orders.
