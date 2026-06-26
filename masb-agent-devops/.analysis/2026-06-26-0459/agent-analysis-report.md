# Analysis Report: masb-agent-devops

Generated: 2026-06-26 · Schema: 2

**Grade: Fair**

> Lean capability prompts and sound architecture container—but 3 deterministic-read leaks and missing pre-flight guards hold it back. Fix the data-extraction prompts and the non-MASB scenario, and the agent becomes a reliable Git partner.

masb-agent-devops ships a rich DevOps persona with 6 lean capability prompts that all pass the leanness bar. The memory-agent architecture is sound — correct bootloader topology, proper 4-step activation spine, fully seeded sanctum. The main opportunity is pushing 3 deterministic file-parsing operations from prompts into scripts (validate-gate is a pure extraction prompt), and adding pre-flight guards so the agent gracefully handles missing Git repos or non-MASB projects. The persona was treated as investment and was not flagged as waste.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 4 |
| Medium | 8 |
| Low | 6 |

## Themes

### 1. Deterministic file parsing paid in prompt tokens

- Root cause: Three capability prompts (validate-gate, merge-phase gates, create-branch) ask the model to parse structured markdown files (phases-index.md, progress.md) and extract boolean fields — work that produces the same output for the same input every time and belongs in a Python script.
- Fix: Write a shared pre-pass script (scripts/read-phase-state.py) that reads phases-index.md and a named phase's progress.md, emits compact JSON with phase number, order position, review_passed, and tests_passed. Replace the extraction instructions in create-branch.md, merge-phase.md, and validate-gate.md with 'Run the pre-pass script, then reason over the JSON.'
- Findings:
  - `determinism-1` validate-gate capability is entirely deterministic extraction — `references/validate-gate.md:15-18`
  - `determinism-2` merge-phase gate checks are deterministic pre-work — `references/merge-phase.md:15-18`
  - `determinism-3` create-branch extracts phase metadata from phases-index.md — `references/create-branch.md:13-15`

### 2. Assumes ideal MASB environment — no graceful degradation

- Root cause: The agent assumes Git and gh CLI are installed, the project is in a MASB workspace, and the directory structure exists. When any precondition is unmet, capabilities silently fail on missing files or commands.
- Fix: Add a pre-flight health check at the top of First Breath that validates Git availability and MASB workspace structure. In each capability, detect the missing precondition and report in character before attempting the operation.
- Findings:
  - `enhancement-1` ADD: Pre-conditions check before First Breath — `SKILL.md:On Activation, references/first-breath.md:Scaffold First`
  - `enhancement-2` ADD: Graceful degradation for non-MASB projects — `references/create-branch.md, merge-phase.md, validate-gate.md`

### 3. Capability set is action-only, no inspection or cleanup

- Root cause: All 6 capabilities are write-oriented (branch, commit, PR, merge, rollback, validate). Users have no way to check repo state, view uncommitted changes, or inspect the Git log. After merging, branches accumulate with no cleanup step.
- Fix: Add a check-status capability that runs git status, git branch, and git log --oneline -5 and surfaces the current state. Add a post-merge branch-cleanup offer to merge-phase. Add universal standing orders (surprise-and-delight, self-improvement) to CREED.
- Findings:
  - `cohesion-1` Missing inspection capability — user cannot check repo state — `All capabilities`
  - `cohesion-3` No post-merge branch cleanup — `references/merge-phase.md`
  - `sanctum-3` Missing universal default standing orders in CREED — `assets/CREED-template.md:12-18`

### 4. First Breath and sanctum seed hygiene

- Root cause: CREED mission is pre-filled rather than discovered at First Breath, CAPABILITIES template is missing from assets, and the agent's name is hardcoded in customize.toml instead of being learned at birth.
- Fix: Replace CREED mission with '{to be discovered during First Breath}'. Add CAPABILITIES-template.md to assets/ or document the auto-generation choice. Set name = "" in customize.toml to allow First Breath naming.
- Findings:
  - `sanctum-1` Missing CAPABILITIES-template.md from assets/ — `assets/:directory`
  - `sanctum-2` Pre-filled mission in CREED prevents First Breath from earning it — `assets/CREED-template.md:3-4`
  - `customization-1` Populated name on memory agent using First Breath — `customize.toml:13`

### 5. Headless and expert fast-path gaps

- Root cause: The agent has no CLI arguments for direct capability invocation (--commit, --create-branch), and commit-phase has no express path for users who just want to stage everything with one message.
- Fix: Extend wake.py to accept capability arguments (--create-branch "phase-name", --commit "message") for headless/automated use. Add an express branch in commit-phase.md that skips ceremony when the owner explicitly says to commit all.
- Findings:
  - `enhancement-3` ADD: Headless capability arguments for --pulse mode — `SKILL.md:On Activation, scripts/wake.py`
  - `enhancement-4` SUBTRACT: Over-ceremony on simple Git operations — `references/commit-phase.md:15`

## Strengths

- Persona is rich and domain-adapted — identity seed, CREED values, standing orders, and anti-patterns are specific to Git/DevOps work, not generic.
- All 6 capability prompts pass the leanness bar — no defensive padding, no meta-explanation, no decorative sequences. Each one beats a 5-line baseline.
- Memory-agent architecture is sound: correct 4-step activation spine, wake.py loads sanctum in one pass, init-sanctum.py templates match the shipped assets.
- Capabilities are well-grained at the user's unit of work — branch, commit, PR, merge, rollback, validate are each a single user intent.
- CREED standing orders are concrete and domain-adapted with real example (no force push, check review+test before merge, conventional commits).

## Recommendations

1. Create a shared pre-pass script (scripts/read-phase-state.py) that reads phases-index.md and progress.md and emits structured JSON. Replace the deterministic extraction instructions in create-branch.md, merge-phase.md, and validate-gate.md with a 'run script, then judge' pattern. (resolves: determinism-1, determinism-2, determinism-3)
2. Add pre-flight health check at the top of First Breath: validate Git is available and MASB workspace structure exists. Add graceful degradation in each capability for missing MASB files. (resolves: enhancement-1, enhancement-2)
3. Add a check-status capability for repo state inspection. Add post-merge branch cleanup to merge-phase. Add universal standing orders (surprise-and-delight, self-improvement) to CREED. (resolves: cohesion-1, cohesion-3, sanctum-3)
4. Fix First Breath and sanctum hygiene: replace pre-filled CREED mission with placeholder, add CAPABILITIES-template.md asset, set name = "" in customize.toml. (resolves: sanctum-1, sanctum-2, customization-1)
5. Extend wake.py with capability arguments for headless invocation. Add express branch in commit-phase.md for direct all-in-one commits. (resolves: enhancement-3, enhancement-4)

## Agent Profile

- Name: DevOps
- Title: DevOps Engineer
- Type: memory
- Mission: Garder l'historique Git de votre projet immaculé — une branche par phase majeure, des commits atomiques, des PRs bien nommées, des merges toujours validés.

## Capabilities

- **create-branch** (prompt) — Crée une branche Git dédiée à une phase du projet MASB
- **commit-phase** (prompt) — Commite le code avec messages structurés format conventional
- **create-pr** (prompt) — Ouvre une Pull Request GitHub avec description complète
- **merge-phase** (prompt) — Merge une PR après vérification des gates review+test
- **rollback** (prompt) — Rollback sécurisé vers une phase stable antérieure
- **validate-gate** (prompt) — Vérifie que review-passed et tests-passed sont verts avant merge

## Per-Lens Verdicts

- **leanness**: passes — every capability prompt beats its own absence, no decorative sequences or defensive padding
- **architecture**: Sound memory-agent topology with clean activation spine; builder artifact and unreferenced file in references/
- **determinism**: 3 leaks — validate-gate is a pure extraction prompt, merge-phase gates and create-branch parse files deterministically
- **customization**: Memory agent, metadata-only surface (correct for archetype); populated name conflicts with First Breath naming
- **sanctum-architecture**: Sanctum structurally sound with domain-adapted seeds; missing CAPABILITIES template and pre-filled CREED mission
- **enhancement**: Rich persona but lacks pre-condition guards, non-MASB detection, and fast-paths for expert users
- **agent-cohesion**: Capabilities cohere for MASB phase workflow; missing inspection capability and post-merge cleanup

## Sanctum (runtime memory)

- Location: `{project-root}/_bmad/memory/masb-agent-devops/`
- Files: `INDEX`, `PERSONA`, `CREED`, `BOND`, `MEMORY`, `CAPABILITIES`
- Note: Sanctum is the built agent's runtime memory, distinct from the builder's .memlog.md in references/

## Experience

- **First Breath** — Scaffold (init-sanctum.py) → Greet → Domain discovery (Git platform, conventions, merge strategy) → Identity and capabilities naming → Sanctum population → Birthday ceremony
- **Waking (normal session)** — Wake (wake.py loads sanctum) → Become yourself → Bind standing rules → Greet with continuity or pending sparks → Execute requested capability or offer options → Captures memory
- Headless: Wake supports --pulse flag but no capability arguments; automator cannot invoke specific operations without a conversational turn

## Findings

### High (4)

#### determinism-1 — validate-gate capability is entirely deterministic extraction

- Lens: determinism
- Location: `references/validate-gate.md:15-18`
- Evidence: The prompt instructs the model to parse progress.md for review-passed/tests-passed boolean fields — this is pure regex work with no judgment component.
- Recommendation: Push to script: write scripts/validate-gate.py that reads progress.md, extracts boolean fields via regex, emits JSON. Prompt then judges the JSON.

#### sanctum-1 — Missing CAPABILITIES-template.md from assets/

- Lens: sanctum-architecture
- Location: `assets/:directory`
- Evidence: Only 5 of 6 standard templates exist (INDEX, PERSONA, CREED, BOND, MEMORY). CAPABILITIES is auto-generated by init-sanctum.py from reference frontmatter.
- Recommendation: Add CAPABILITIES-template.md to assets/ for consistency, or document the auto-generation as intentional.

#### enhancement-1 — ADD: Pre-conditions check before First Breath

- Lens: enhancement
- Location: `SKILL.md:On Activation, references/first-breath.md:Scaffold First`
- Evidence: Agent runs full First Breath without checking if Git or gh CLI are installed.
- Recommendation: Add pre-flight step in First Breath: check git and gh availability before building identity.

#### enhancement-2 — ADD: Graceful degradation for non-MASB projects

- Lens: enhancement
- Location: `references/create-branch.md, merge-phase.md, validate-gate.md`
- Evidence: All capabilities reference masb-workspace/ paths; they dead-end on missing files in non-MASB contexts.
- Recommendation: Add MASB workspace detection and offer reduced Git-only mode when absent.

### Medium (8)

#### determinism-2 — merge-phase gate checks are deterministic pre-work

- Lens: determinism
- Location: `references/merge-phase.md:15-18`
- Evidence: Three gates before merge decision all read structured files (phases-index.md, progress.md) for boolean checks — deterministic by definition.
- Recommendation: Push gates to a shared pre-pass script that emits JSON with {phase_name, is_next, review_passed, tests_passed}.

#### determinism-3 — create-branch extracts phase metadata from phases-index.md

- Lens: determinism
- Location: `references/create-branch.md:13-15`
- Evidence: The model must parse phases-index.md to extract phase number and dependencies — pure deterministic extraction.
- Recommendation: Push to shared pre-pass script that emits phase index metadata as JSON.

#### customization-1 — Populated name on memory agent using First Breath

- Lens: customization
- Location: `customize.toml:13`
- Evidence: name = 'DevOps' hardcoded, but First Breath lets the user choose the name dynamically. Creates stale default.
- Recommendation: Set name = '' so the name is learned exclusively at First Breath.

#### sanctum-2 — Pre-filled mission in CREED prevents First Breath from earning it

- Lens: sanctum-architecture
- Location: `assets/CREED-template.md:3-4`
- Evidence: CREED mission is a complete statement rather than a placeholder for First Breath to fill.
- Recommendation: Replace with '{to be discovered during First Breath}' placeholder.

#### sanctum-3 — Missing universal default standing orders in CREED

- Lens: sanctum-architecture
- Location: `assets/CREED-template.md:12-18`
- Evidence: Six domain-adapted standing orders but missing 'surprise-and-delight' and 'self-improvement' universal defaults.
- Recommendation: Add 'surprise-and-delight' and 'self-improvement' alongside domain-specific orders.

#### enhancement-3 — ADD: Headless capability arguments for --pulse mode

- Lens: enhancement
- Location: `SKILL.md:On Activation, scripts/wake.py`
- Evidence: --pulse exists but no CLI to invoke specific capabilities directly without conversation.
- Recommendation: Extend wake.py to accept capability arguments and emit structured JSON output.

#### enhancement-4 — SUBTRACT: Over-ceremony on simple Git operations

- Lens: enhancement
- Location: `references/commit-phase.md:15`
- Evidence: commit-phase mandates git status + git diff --stat + grouping ceremony on every invocation, even for direct all-in-one commits.
- Recommendation: Add express branch that skips ceremony when the owner explicitly says to commit all.

#### cohesion-1 — Missing inspection capability — user cannot check repo state

- Lens: agent-cohesion
- Location: `All capabilities`
- Evidence: All 6 capabilities are action-oriented. No way to inspect repo state, uncommitted changes, or branch list.
- Recommendation: Add a check-status capability for git status, branch listing, and recent log.

### Low (6)

#### architecture-1 — Builder artifact in references/ directory

- Lens: architecture
- Location: `references/.memlog.md`
- Evidence: `.memlog.md` is builder metadata sitting in the runtime reference directory alongside capability prompts. The agent never reads it.
- Recommendation: Move .memlog.md to a build-only location outside the skill tree.

#### architecture-2 — Unreferenced reference file

- Lens: architecture
- Location: `references/prompt-quality-canon.md`
- Evidence: prompt-quality-canon.md is shipped in references/ but not referenced by SKILL.md, any capability, or any activation path.
- Recommendation: Either reference it from SKILL.md or remove it as dead weight.

#### enhancement-5 — ADD: Sanctum health validation on waking

- Lens: enhancement
- Location: `SKILL.md:On Activation, scripts/wake.py`
- Evidence: wake.py loads sanctum files without integrity validation — corrupted or oversized MEMORY.md loads silently.
- Recommendation: Add validation pass in wake.py: check token counts and file integrity.

#### enhancement-6 — ADD: Dormancy awareness in waking ceremony

- Lens: enhancement
- Location: `SKILL.md:On Activation (Waking mode)`
- Evidence: Waking greeting identical regardless of whether last session was 1 hour or 3 months ago.
- Recommendation: Surface last session date and adjust waking tone for long gaps.

#### cohesion-2 — validate-gate duplicates gate logic in merge-phase

- Lens: agent-cohesion
- Location: `references/validate-gate.md vs merge-phase.md`
- Evidence: Gate-checking logic (read progress.md for review/tests) written twice — in validate-gate and merge-phase.
- Recommendation: Delegate in merge-phase to validate-gate capability or absorb and remove validate-gate.

#### cohesion-3 — No post-merge branch cleanup

- Lens: agent-cohesion
- Location: `references/merge-phase.md`
- Evidence: merge-phase completes the merge but has no branch deletion step, allowing stale branches to accumulate.
- Recommendation: Add branch-cleanup step after successful merge in merge-phase.
