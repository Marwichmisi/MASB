# Analysis Report: masb-agent-testeur

Generated: 2026-06-26 · Schema: 2

**Grade: Poor**

> An agent with a strong QA persona and coherent testing pipeline, burdened by template carry-over, missing environment hardening, and one critical pre-flight gap (uv dependency unverified) that would block every activation.

masb-agent-testeur embodies its 'rigoureux' QA persona well across 4 capabilities with a coherent compile→test→perf→report chain. Its primary weakness is template carry-over from the builder: dead Pulse references, a duplicated canon that an evolvable-only instruction pays for every waking, and sanctum-bound detail leaked into the bootloader. One critical finding (missing uv dependency check) would break every activation silently, and several high findings degrade its runtime economy and structural purity.

| Severity | Count |
| --- | --- |
| Critical | 1 |
| High | 5 |
| Medium | 13 |
| Low | 11 |

## Themes

### 1. Template carry-over from builder pattern

- Root cause: The agent inherited dead patterns from the builder's generic templates: Pulse curation workflow for a non-autonomous agent, prompt-quality-canon.md for a non-evolvable agent, and sanctum-bound detail (Stay in Character) leaked into the bootloader instead of CREED.
- Fix: Remove Pulse references from memory-guidance.md. Remove prompt-quality-canon.md from the refs copy set (agent is not evolvable). Move detailed Stay in Character guidance from SKILL.md into CREED-template.md. Strip the anti-patterns section from CREED-template.
- Findings:
  - `enhancement-2` remove: prompt-quality-canon.md from sanctum (dead reference) — `assets/CREED-template.md:35`
  - `enhancement-3` remove: Pulse curation workflow from memory-guidance.md — `references/memory-guidance.md:50-53`
  - `sanctum-architecture-1` Sanctum-bound communication style leaked in bootloader — `SKILL.md:26-28`
  - `leanness-1` CREED anti-patterns are ceremony — re-teach and padding — `assets/CREED-template.md:48-59`
  - `leanness-2` CREED Standing Orders duplicate Never directives from reference files — `assets/CREED-template.md:25-31`

### 2. Script opportunities in testing pipeline

- Root cause: Deterministic work — parsing test output, updating progress.md status fields, pruning session logs — lives in prompts when native Python scripts would be cheaper, more reliable, and token-free on every invocation.
- Fix: Create scripts/parse-test-results.py for structured test output parsing, and a shared progress.md update utility. Move session-log age-based pruning into a script.
- Findings:
  - `determinism-1` Test result parsing and extraction in prompt — `references/run-tests.md:16-20`
  - `determinism-2` Structured status writes to progress.md in prompts — `references/compile-verify.md:13,19 + references/run-tests.md:18,20`
  - `determinism-3` Session-log age-based pruning in prompt — `references/memory-guidance.md:50-51`

### 3. Pre-flight and environment hardening gaps

- Root cause: The agent's activation chain depends on uv and Python but the pre-flight check only verifies Android SDK, JDK, Gradle, and Git. Several runtime operations (Perfetto, ADB) also lack proactive verification.
- Fix: Add uv --version check to pre-flight. Add test-directory existence check before running tasks. Verify ADB device/emulator presence before instrumented tests. Add Perfetto availability check.
- Findings:
  - `enhancement-1` add: uv/Python dependency check to pre-flight — `references/first-breath.md:12-16`
  - `enhancement-6` add: empty/no-tests edge-case handling to run-tests — `references/run-tests.md:11-15`
  - `agent-cohesion-1` No test environment verification before running connected tests — `references/run-tests.md:14`
  - `agent-cohesion-6` Perfetto not checked during First Breath pre-flight — `references/first-breath.md:12-16`

### 4. Missing completeness for real-world Android QA

- Root cause: The agent covers compile→test→perf→report but omits standard QA concerns: test coverage analysis, lint verification, multi-module project heuristics, and structured success sign-off.
- Fix: Add coverage analysis (JaCoCo/Kover) after tests. Add lint/ktlint verification. Add structured success sign-off artifact. Add multi-module Gradle heuristic. Add re-verification protocol for post-fix cycles.
- Findings:
  - `agent-cohesion-2` Missing test coverage analysis — `references/run-tests.md`
  - `agent-cohesion-3` No lint or static analysis verification — `references/compile-verify.md`
  - `agent-cohesion-4` No structured success sign-off for all-green workflows — `references/failure-report.md`
  - `enhancement-4` add: multi-module Gradle project guidance to compile-verify — `references/compile-verify.md:11`
  - `enhancement-5` add: post-failure re-verification protocol — `references/compile-verify.md:19, references/run-tests.md:20`

## Strengths

- Strong QA rigoureux persona — consistently embodied across bootloader, capabilities, and sanctum templates
- Coherent compile→test→perf→report capability chain with clear handoffs
- Sound architecture: clean activation spine, proper bootloader pattern, correct file topology
- Customization surface is lean and correct — metadata-only with no sanctum conflict
- Capability prompts are outcome-focused and concise (average ~22 lines each)

## Recommendations

1. Add uv pre-flight check to first-breath.md and move detailed Stay in Character from SKILL.md to CREED — resolves the critical finding and one high in one edit. (resolves: enhancement-1, sanctum-architecture-1)
2. Strip dead template carry-over: remove Pulse sections from memory-guidance.md, exclude prompt-quality-canon.md from reference copy set (not evolvable), remove anti-patterns section from CREED. (resolves: enhancement-2, enhancement-3, leanness-1, leanness-2)
3. Create test-result parsing script and move deterministic progress.md writes and session pruning out of prompts. (resolves: determinism-1, determinism-2, determinism-3)
4. Add environment hardening: test-directory check, ADB verification, multi-module Gradle heuristic, and coverage analysis. (resolves: agent-cohesion-1, agent-cohesion-2, enhancement-4, enhancement-6, agent-cohesion-6)

## Agent Profile

- Name: masb-agent-testeur
- Title: Testeur Android
- Type: memory
- Mission: Garantir que chaque phase livrée compile, passe les tests et tient la route en perf

## Capabilities

- **compile-verify** (prompt) — Vérifie compilation Gradle, classe erreurs, met à jour progress.md
- **run-tests** (prompt) — Exécute tests unitaires + instrumentés, collecte résultats
- **perf-analyze** (prompt) — Analyse performances via Perfetto (skills wrappés)
- **failure-report** (prompt) — Produit rapport structuré avec root cause, reproduction, fix suggéré

## Per-Lens Verdicts

- **leanness**: 2 medium (duplicate CREED ceremony), 2 low (prescribed commands)
- **architecture**: Clean — all checks pass
- **determinism**: 1 high (test parsing), 1 medium (status writes), 1 low (session pruning)
- **customization**: Clean — about right, sole mechanism
- **enhancement**: 1 critical (uv check), 2 high (dead canon, dead Pulse), 3 medium, 2 low
- **agent-cohesion**: 2 medium (env check, coverage), 5 low (lint, signoff, overlap, Perfetto, skills load)
- **sanctum-architecture**: 1 high (communication style leaked into bootloader)

## Sanctum (runtime memory)

- Location: `{project-root}/_bmad/memory/masb-agent-testeur/`
- Files: `INDEX.md`, `PERSONA.md`, `CREED.md`, `BOND.md`, `MEMORY.md`, `CAPABILITIES.md`
- Note: The sanctum is the built agent's runtime memory, distinct from the builder's .memlog.md

## Experience

- **First Breath** — Pre-flight check → Scaffold sanctum → Discovery → Identity → Birthday ceremony
- **Waking** — Wake (wake.py) → Become yourself → Bind rules → Proper Mode → Greet
- **Testing workflow** — Compile verify → Run tests → Perf analyze → Failure report → Update progress.md
- Headless: Capabilities have code identifiers (CV, RT, PA, FR) and write structured artifacts — suitable for headless; no formal invocation contract documented.

## Findings

### Critical (1)

#### enhancement-1 — add: uv/Python dependency check to pre-flight

- Location: `references/first-breath.md:12-16`
- Evidence: Entire activation chain depends on `uv run scripts/wake.py` and `uv run scripts/init-sanctum.py`, but pre-flight only checks Android SDK, JDK, Gradle, Git. If uv or Python >=3.10 is absent, both First Breath and every Waking fail before the agent speaks.
- Recommendation: Add `uv --version` check to pre-flight steps. If missing, fail with an in-character message and install command.

### High (5)

#### lint-1 — Prompt file at skill root: .memlog.md

- Location: `/home/marwane/Documents/momono/skills/masb-agent-testeur/.memlog.md:0`
- Evidence: .memlog.md sits at skill root instead of references/
- Recommendation: Move .memlog.md to references/.memlog.md

#### determinism-1 — Test result parsing and extraction in prompt

- Location: `references/run-tests.md:16-20`
- Evidence: Prompt instructs the agent to 'capture failing test names, error messages, and stack traces' and collect results — deterministic extraction/parsing of structured data.
- Recommendation: Move test output parsing into a script (scripts/parse-test-results.py) that reads console output or XML reports and writes structured data.

#### enhancement-2 — remove: prompt-quality-canon.md from sanctum (dead reference)

- Location: `assets/CREED-template.md:35`
- Evidence: EVOLVABLE=False, so this agent will never author or refine capabilities. Yet CREED instructs loading prompt-quality-canon.md at capability-authoring time, and the canon is copied into the sanctum — ~56 tokens paid every waking for a thing that can never happen.
- Recommendation: Remove the prompt-quality-canon.md reference from CREED Standing Orders and exclude it from the reference copy set.

#### enhancement-3 — remove: Pulse curation workflow from memory-guidance.md

- Location: `references/memory-guidance.md:50-53`
- Evidence: Agent is not autonomous (no PULSE), yet memory-guidance.md devotes paragraphs to 'During Pulse, review session logs and distill insights... Prune session logs older than 14 days.' Dead ceremony.
- Recommendation: Strip Pulse-specific sections from memory-guidance.md. Keep the Two-Tier structure but remove all Pulse-automation references.

#### sanctum-architecture-1 — Sanctum-bound communication style leaked in bootloader

- Location: `SKILL.md:26-28`
- Evidence: Stay in Character section contains detailed guidance ('Emote freely about waking', 'never describe the wiring') that belongs in CREED's Standing Orders or Philosophy, not in the bootloader.
- Recommendation: Replace detailed Stay in Character with a compact directive. Move full communication style into CREED-template.md.

### Medium (13)

#### lint-2 — No PEP 723 inline dependency block (# /// script)

- Location: `/home/marwane/Documents/momono/skills/masb-agent-testeur/scripts/init-sanctum.py:1`
- Evidence: Script lacks requires-python and dependency declarations
- Recommendation: Add PEP 723 block with requires-python and dependencies

#### lint-3 — No argparse found — script lacks --help self-documentation

- Location: `/home/marwane/Documents/momono/skills/masb-agent-testeur/scripts/init-sanctum.py:1`
- Evidence: Script handles argv manually without argparse
- Recommendation: Add argparse with description and argument help text

#### lint-4 — No json.dumps found — output may not be structured JSON

- Location: `/home/marwane/Documents/momono/skills/masb-agent-testeur/scripts/init-sanctum.py:1`
- Evidence: Script prints unstructured human-readable text
- Recommendation: Use json.dumps for structured output parseable by workflows

#### lint-5 — No argparse found — script lacks --help self-documentation

- Location: `/home/marwane/Documents/momono/skills/masb-agent-testeur/scripts/wake.py:1`
- Evidence: Script handles argv manually without argparse
- Recommendation: Add argparse with description and argument help text

#### lint-6 — No json.dumps found — output may not be structured JSON

- Location: `/home/marwane/Documents/momono/skills/masb-agent-testeur/scripts/wake.py:1`
- Evidence: Script prints unstructured human-readable text
- Recommendation: Use json.dumps for structured output parseable by workflows

#### leanness-1 — CREED anti-patterns are ceremony — re-teach and padding

- Location: `assets/CREED-template.md:48-59`
- Evidence: Operational anti-patterns ('Don't stand by passively', 'Don't repeat the same testing approach') are generic common-sense guidelines. Behavioral anti-patterns restate what Core Values and Standing Orders already cover.
- Recommendation: Remove the Anti-Patterns section entirely. Core Values + Standing Orders already encode the desired behaviors.

#### leanness-2 — CREED Standing Orders duplicate Never directives from reference files

- Location: `assets/CREED-template.md:25-31`
- Evidence: Standing Order #1 ('Always run the actual build or test suite before declaring success') is restated at the end of each reference file (compile-verify.md:21, run-tests.md:22, perf-analyze.md:21, failure-report.md:26).
- Recommendation: Remove the general 'always run actual checks' rule from CREED Standing Orders. Keep capability-specific Never directives in each reference.

#### determinism-2 — Structured status writes to progress.md in prompts

- Location: `references/compile-verify.md:13,19 + references/run-tests.md:18,20`
- Evidence: Both compile-verify and run-tests contain deterministic key-value formatting operations for progress.md fields.
- Recommendation: Have the output-producing script write progress.md fields directly, or use a shared progress.md update script.

#### enhancement-4 — add: multi-module Gradle project guidance to compile-verify

- Location: `references/compile-verify.md:11`
- Evidence: Capability works only for single-module projects. Many Android projects are multi-module.
- Recommendation: Add heuristic: inspect settings.gradle.kts for include lines; if multi-module, default to ./gradlew :app:assembleDebug.

#### enhancement-5 — add: post-failure re-verification protocol

- Location: `references/compile-verify.md:19, references/run-tests.md:20`
- Evidence: After a failure is reported and the developer says 'I fixed it', there is no documented protocol for re-running. Dead-end experience gap.
- Recommendation: Add a re-verification section to failure-report.md: offer to re-run the capability when the developer signals readiness.

#### enhancement-6 — add: empty/no-tests edge-case handling to run-tests

- Location: `references/run-tests.md:11-15`
- Evidence: Capability unconditionally runs test tasks, but a project may have no tests. Agent will run Gradle tasks producing zero output or even fail.
- Recommendation: Add pre-step: check if test directories exist. If neither unit nor instrumented tests exist, report 'No test sources found.'

#### agent-cohesion-1 — No test environment verification before running connected tests

- Location: `references/run-tests.md:14`
- Evidence: Capability says 'if emulator or device available' but has no proactive ADB/device check.
- Recommendation: Add environment-check step: verify adb devices, confirm emulator/device status, or communicate when instrumented tests cannot run.

#### agent-cohesion-2 — Missing test coverage analysis

- Location: `references/run-tests.md`
- Evidence: Agent reports pass/fail but never examines coverage reports (JaCoCo, Kover).
- Recommendation: Add coverage-analysis step: locate coverage reports, report percentage, flag untested areas.

### Low (11)

#### lint-7 — No sys.exit() calls — may not return meaningful exit codes

- Location: `/home/marwane/Documents/momono/skills/masb-agent-testeur/scripts/wake.py:1`
- Evidence: Script returns integer from main() but uses raise SystemExit
- Recommendation: Return 0=success, 1=fail, 2=error via sys.exit()

#### leanness-3 — Numbered sequence in run-tests prescribes how instead of what

- Location: `references/run-tests.md:13-14`
- Evidence: Numbered sequence prescribing exact commands and order for unit/instrumented tests.
- Recommendation: Replace with outcome-oriented statement: 'Run all available tests (unit and instrumented, if device/emulator available).'

#### leanness-4 — compile-verify prescribes exact Gradle command

- Location: `references/compile-verify.md:11`
- Evidence: Exact Gradle commands re-teach a standard CLI the model already knows.
- Recommendation: Replace with 'Compile the project using the appropriate Gradle task.'

#### determinism-3 — Session-log age-based pruning in prompt

- Location: `references/memory-guidance.md:50-51`
- Evidence: 'Prune session logs older than 14 days' is a deterministic file-system operation with one correct answer per file.
- Recommendation: Create a script (scripts/prune-sessions.py) that handles session-log pruning deterministically.

#### enhancement-7 — add: success milestone delight moment

- Location: `references/compile-verify.md:13, references/run-tests.md:18`
- Evidence: Every capability is failure-oriented with no celebration when all gates pass.
- Recommendation: Add closing note: after all gates pass, produce a brief success verdict in character.

#### enhancement-8 — add: headless invocation contract for each capability

- Location: `references/compile-verify.md, references/run-tests.md, references/perf-analyze.md`
- Evidence: Capabilities use code identifiers and write structured output but define no required input parameters or output contract for headless use.
- Recommendation: Add frontmatter fields `inputs:` and `outputs:` to each capability reference.

#### agent-cohesion-3 — No lint or static analysis verification

- Location: `references/compile-verify.md`
- Evidence: Agent checks compilation but not Android lint, ktlint, or Spotless.
- Recommendation: Add lint verification as companion step to compile-verify or create a static-analysis capability.

#### agent-cohesion-4 — No structured success sign-off for all-green workflows

- Location: `references/failure-report.md`
- Evidence: Well-defined for red paths but no structured success deliverable when everything passes.
- Recommendation: Add validation-signoff capability producing a structured success report.

#### agent-cohesion-5 — `./gradlew build` may leak into test execution

- Location: `references/compile-verify.md:11`
- Evidence: Offering `build` may trigger test tasks, overlapping with run-tests domain.
- Recommendation: Default to assembleDebug for compile verification; reserve build for when tests are explicitly requested.

#### agent-cohesion-6 — Perfetto not checked during First Breath pre-flight

- Location: `references/first-breath.md:12-16`
- Evidence: Performance analysis is a core capability but Perfetto availability is not verified at birth.
- Recommendation: Add Perfetto availability check (which perfetto or trace_processor presence) to pre-flight.

#### agent-cohesion-7 — perf-analyze references external skills without loading mechanism

- Location: `references/perf-analyze.md:13-14`
- Evidence: Says 'Load the perfetto-sql skill' but gives no instruction on how to invoke the Skill tool.
- Recommendation: Document skill-loading mechanism explicitly or add companion-skill-loading instruction to On Activation.
