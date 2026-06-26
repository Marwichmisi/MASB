# Analysis Report: masb-agent-research

Generated: 2026-06-26 · Schema: 2

**Grade: Fair**

> Solid foundational agent with clear persona-capability alignment but multiple high-severity issues around missing headless mode, ceremony overhead, a broken reference, and activation behavior leaking from bootloader. One critical finding: CAPABILITIES template absent from assets/.

masb-agent-research is a well-structured memory agent with strong persona coherence: it knows exactly who it is (expert en veille technique Android) and what it does (research-patterns, enrich-spec, verify-approach). The primary opportunities are reducing activation ceremony for power users, adding a headless/fast-lookup path, resolving the broken capability-authoring.md reference, and trimming bootloader content back into the sanctum. The persona was treated as investment and was never flagged as waste.

| Severity | Count |
| --- | --- |
| Critical | 1 |
| High | 7 |
| Medium | 12 |
| Low | 7 |

## Themes

### 1. Missing headless and fast-lookup paths limit real-world utility

- Root cause: The agent was designed exclusively for the full MASB phase workflow with no shortcuts for returning experts or automators. All three capabilities require a phase context and produce phase-scoped files. Activation ceremony fires every session regardless of user expertise.
- Fix: Add a `quick-query` capability for inline sourced answers. Add `--headless` flag to wake.py. Introduce a stored preference in BOND.md for ceremony level.
- Findings:
  - `enhancement-1` No headless/automation mode — `SKILL.md:65-81, scripts/wake.py`
  - `enhancement-3` No fast-lookup/quick-query capability — `references/research-patterns.md, references/enrich-spec.md, references/verify-approach.md`
  - `enhancement-4` Daily waking ceremony over-applied — `SKILL.md:65-81`
  - `enhancement-5` First Breath too ceremonious for action-oriented user — `references/first-breath.md`

### 2. Bootloader carries sanctum-bound content

- Root cause: The SKILL.md On Activation section (lines 53-82) includes detailed mode-routing behavior, greeting scripts, and capability-style instructions that belong in sanctum templates per the bootloader-is-lean-by-design principle.
- Fix: Trim SKILL.md activation to the four-step routing skeleton only. Move greeting, pending-sparks handling, and capability-offer instructions into sanctum PERSONA or CAPABILITIES.
- Findings:
  - `sanctum-architecture-2` Activation behavior content leaking into bootloader — `SKILL.md:53-82`
  - `enhancement-4` Daily waking ceremony over-applied — `SKILL.md:65-81`
  - `enhancement-6` Script path resolution ambiguous — `SKILL.md`

### 3. Deterministic work delegated to LLM instead of scripts

- Root cause: Structural merge rules for config resolution and placeholder scanning in First Breath are described as prompt instructions when they are deterministic operations better served by scripts.
- Fix: Replace structural merge fallback in SKILL.md with a script call. Move placeholder scanning from First Breath into init-sanctum.py as a post-processing step.
- Findings:
  - `determinism-1` Structural merge rules delegated to LLM fallback — `SKILL.md:59-61`
  - `determinism-2` Template placeholder scanning delegated to LLM — `references/first-breath.md`
  - `customization-1` Secondary config mechanism reads config.yaml in init-sanctum.py — `scripts/init-sanctum.py`

### 4. Capability prompts contain role boundaries already in CREED

- Root cause: The curseur blocks and role meta-explanations in research-patterns.md, enrich-spec.md, and verify-approach.md restate principles already encoded in CREED (Vérité sourcée, Humilité technique, boundaries). The persona already governs these behaviors.
- Fix: Trim redundant role carving from capability prompts. Keep only the artifact specification, the consumer, and the non-obvious nuance. Resolve the CREED boundary contradiction with enrich-spec.
- Findings:
  - `leanness-1` Parenthetical restates sourcing principle from CREED — `references/research-patterns.md`
  - `leanness-2` Role meta-explanation redundant with CREED Boundaries — `references/enrich-spec.md`
  - `leanness-3` Curseur restates role boundary again — `references/enrich-spec.md`
  - `leanness-4` Curseur ceremony in two capability prompts restates persona principles — `references/research-patterns.md + references/verify-approach.md`
  - `leanness-5` Role preamble adds no dimension over CREED — `references/enrich-spec.md`
  - `agent-cohesion-1` Boundary contradiction between CREED and enrich-spec capability — `assets/CREED-template.md vs references/enrich-spec.md`

## Strengths

- Clear, well-defined persona (expert en veille technique, documentation-oriented) — the identity seed, CREED values, and communication style are coherent and specific to the research domain
- Capabilities have clear artifacts, consumers, and quality gates (curseur pattern) — each one produces a distinct output consumed by a named downstream agent
- First Breath uses config style with domain-specific discovery questions tailored to Android research preferences
- Scripts are syntactically valid, wake.py correctly routes Waking vs First Breath mode, init-sanctum.py auto-discovers capabilities from frontmatter
- customize.toml correctly identifies sanctum as primary customization surface for a memory agent
- Sanctum templates include meaningful CREED values, standing orders, and dominion boundaries

## Recommendations

1. Create CAPABILITIES-template.md in assets/ to satisfy the standard 6-template contract and fix the critical sanctum architecture finding (resolves: sanctum-architecture-1)
2. Add a `quick-query` capability for inline Android pattern lookups without phase context, and add `--headless` support to wake.py (resolves: enhancement-1, enhancement-3, enhancement-4)
3. Trim SKILL.md On Activation to the four-step routing skeleton only; move greeting, pending-sparks, and capability-offer behavior into sanctum templates (resolves: sanctum-architecture-2, enhancement-4)
4. Create references/capability-authoring.md or remove the dead reference from init-sanctum.py's generate_capabilities_md template (resolves: architecture-1)
5. Replace the structural merge fallback prompt in SKILL.md with a script call (scripts/merge_config.py) (resolves: determinism-1)
6. Document wake.py failure fallback analogous to the customization resolver fallback (resolves: enhancement-2)
7. Trim redundant curseur blocks and role meta-explanations from capability prompts; add seed examples to BOND-template.md (resolves: leanness-1, leanness-2, leanness-3, leanness-4, leanness-5, sanctum-architecture-3)

## Agent Profile

- Title: Expert en Veille Technique
- Type: memory
- Mission: Trouver les patterns, APIs et bonnes pratiques officiels qui rendent chaque phase Android implémentable -- sans jamais inventer ce que la documentation ne dit pas.

## Capabilities

- **research-patterns** (prompt) — Recherche patterns/APIs/bonnes pratiques pour une phase, produit findings.md
- **enrich-spec** (prompt) — Enrichit la spec avec recommandations sourcées via enrichment-proposal.md
- **verify-approach** (prompt) — Vérifie conformité d'une approche selon skills officiels, produit conformity-report.md

## Per-Lens Verdicts

- **leanness**: Lean overall; three curseur blocks and one role meta-explanation repeat principles already in CREED but none constitute whole-capability ceremony.
- **architecture**: Solid memory agent topology and activation spine. One high finding: capability-authoring.md reference does not exist.
- **determinism**: 2 determinism leaks found: structural merge rules in prompt (high), template placeholder scanning in prompt (low). No intelligence leaks.
- **customization**: customize.toml well-structured for memory agent. One medium finding: secondary config mechanism in init-sanctum.py.
- **enhancement**: Strong domain framing. High findings: no headless mode, no wake.py failure recovery, no fast-lookup path, over-ceremonied daily waking.
- **agent-cohesion**: Persona and capabilities align well. Medium tension between CREED boundary and enrich-spec's pattern recommendations.
- **sanctum-architecture**: Three Laws and Sacred Truth present. Critical: CAPABILITIES template missing from assets/. High: activation behavior leaking from bootloader.

## Sanctum (runtime memory)

- Location: `{project-root}/_bmad/memory/masb-agent-research/`
- Files: `INDEX`, `PERSONA`, `CREED`, `BOND`, `MEMORY`, `CAPABILITIES`
- Note: Sanctum is the built agent's runtime memory, distinct from the builder's .memlog.md

## Experience

- **First Breath** — Scaffold sanctum via init-sanctum.py, discovery questions (working style, research preferences), identity naming, capability introduction, tool setup. Configuration-style with 5 domain questions + urgency detection.
- **Waking (expert)** — wake.py loads sanctum → become yourself → bind standing rules → Waking Mode with greeting. No fast path for returning experts.
- **Phase research** — Architecte activates phase → research-patterns consumes spec.md → produces findings.md → enrich-spec proposes enhancements → verify-approach checks compliance.
- Headless: No headless mode available. All three capabilities require full conversational activation cycle.

## Findings

### Critical (1)

#### sanctum-architecture-1 — CAPABILITIES template missing from assets

- Lens: sanctum-architecture
- Location: `assets/`
- Evidence: All 6 standard templates must exist - INDEX, PERSONA, CREED, BOND, MEMORY, CAPABILITIES. CAPABILITIES-template.md is absent (auto-generated from frontmatter). TEMPLATE_FILES list omits it.
- Recommendation: Add CAPABILITIES-template.md to assets/ or update to stub if auto-generation is the approved approach

### High (7)

#### architecture-1 — Referenced file references/capability-authoring.md does not exist

- Lens: architecture
- Location: `scripts/init-sanctum.py:161`
- Evidence: init-sanctum.py embeds 'Load references/capability-authoring.md' into generated CAPABILITIES.md. The file does not exist in references/ or anywhere in the skill bundle.
- Recommendation: Create references/capability-authoring.md or remove the dead reference from init-sanctum.py's generate_capabilities_md template

#### determinism-1 — Structural merge rules delegated to LLM fallback

- Lens: determinism
- Location: `SKILL.md:59-61`
- Evidence: Prompt instructs LLM to manually apply structural merge rules across config files. Precise deterministic data-structure work.
- Recommendation: Replace fallback with script call (uv run scripts/merge_config.py)

#### enhancement-1 — No headless/automation mode

- Lens: enhancement
- Location: `SKILL.md:65-81, scripts/wake.py`
- Evidence: All capabilities output files but activation always requires full persona cycle. wake.py has --pulse but no --headless flag.
- Recommendation: Add --headless flag to wake.py that outputs identity silently and skips greeting ceremony

#### enhancement-2 — No recovery path when wake.py fails

- Lens: enhancement
- Location: `SKILL.md:67`
- Evidence: SKILL.md mandates uv run scripts/wake.py with no fallback if uv unavailable or Python version missing.
- Recommendation: Document manual fallback for wake.py failure analogous to customization resolver fallback

#### enhancement-3 — No fast-lookup/quick-query capability

- Lens: enhancement
- Location: `references/research-patterns.md, references/enrich-spec.md, references/verify-approach.md`
- Evidence: All capabilities tied to phase workflow - require phase number N, spec file, produce output to masb-workspace/phases/N/.
- Recommendation: Add fourth capability quick-query that returns inline sourced answer without phase context

#### enhancement-4 — Daily waking ceremony over-applied

- Lens: enhancement
- Location: `SKILL.md:65-81`
- Evidence: Every session requires full ceremony - resolve customization, wake.py, become yourself, bind rules, execute Waking Mode with scripted greeting. No acceleration path for returning experts.
- Recommendation: Introduce --fast flag or stored preference in BOND.md that skips greeting ceremony

#### sanctum-architecture-2 — Activation behavior content leaking into bootloader

- Lens: sanctum-architecture
- Location: `SKILL.md:53-82`
- Evidence: On Activation section contains mode-routing behavior, greeting scripts, pending-sparks handling, capability instructions - belongs in sanctum.
- Recommendation: Move mode-specific behavior into sanctum templates, keep only routing skeleton in bootloader

### Medium (12)

#### leanness-4 — Curseur ceremony in two capability prompts restates persona principles

- Lens: leanness
- Location: `references/research-patterns.md + references/verify-approach.md`
- Evidence: Both files end with Le curseur paragraph re-teaching honesty/sourcing principles already in CREED.
- Recommendation: Replace with single terse line per file where non-obvious nuance exists, or remove entirely
- Proposed smallest: research-patterns.md: 'Marque comme hypothèse toute recommandation non sourcée depuis un skill officiel.' / verify-approach.md: remove - CREED already covers honesty.
- Predicted delta: None. CREED governs the same behaviors.

#### agent-cohesion-1 — Boundary contradiction between CREED and enrich-spec capability

- Lens: agent-cohesion
- Location: `assets/CREED-template.md vs references/enrich-spec.md`
- Evidence: CREED says do not propose architecture but enrich-spec instructs agent to propose 'Patterns d'implémentation recommandés'.
- Recommendation: Relax CREED boundary with carve-out for sourced technical recommendations, or narrow enrich-spec to catalog options only

#### agent-cohesion-2 — No handling for missing external skills

- Lens: agent-cohesion
- Location: `references/research-patterns.md`
- Evidence: research-patterns hardcodes context7-cli, android-cli, domain skills as sources but has no fallback when skills are not installed.
- Recommendation: Add skill-provisioning detection as activation step or capability

#### customization-1 — Secondary config mechanism reads config.yaml in init-sanctum.py

- Lens: customization
- Location: `scripts/init-sanctum.py`
- Evidence: init-sanctum.py reads _bmad/config.yaml for user_name/communication_language, creating parallel surface outside customize.toml.
- Recommendation: Remove config.yaml codepath from init-sanctum.py; set defaults conversationally during First Breath

#### enhancement-5 — First Breath too ceremonious for action-oriented user

- Lens: enhancement
- Location: `references/first-breath.md`
- Evidence: 5 discovery questions + identity + personality + capabilities + tools before research help. Urgency detection vague.
- Recommendation: Define concrete urgency signals, add --minimal-setup flag

#### enhancement-6 — Script path resolution ambiguous

- Lens: enhancement
- Location: `SKILL.md`
- Evidence: Script calls use bare relative paths (uv run scripts/wake.py) with no {skill-root}/ prefix.
- Recommendation: Prefix all script references with {skill-root}/

#### sanctum-architecture-3 — BOND template seeds are empty placeholders

- Lens: sanctum-architecture
- Location: `assets/BOND-template.md`
- Evidence: Domain sections exist but all seed content is {à découvrir}. Things to Remember and Things to Avoid are empty.
- Recommendation: Add meaningful seed examples or default values to each BOND section

#### lint-1 — No PEP 723 inline dependency block in init-sanctum.py

- Lens: lint
- Location: `scripts/init-sanctum.py`
- Evidence: Script lacks # /// script metadata block.
- Recommendation: Add PEP 723 block with requires-python and dependencies

#### lint-2 — No argparse in init-sanctum.py

- Lens: lint
- Location: `scripts/init-sanctum.py`
- Evidence: Script lacks --help self-documentation.
- Recommendation: Add argparse with description and argument help text

#### lint-3 — No json.dumps in init-sanctum.py

- Lens: lint
- Location: `scripts/init-sanctum.py`
- Evidence: Output may not be structured JSON.
- Recommendation: Use json.dumps for structured output

#### lint-4 — No argparse in wake.py

- Lens: lint
- Location: `scripts/wake.py`
- Evidence: Script lacks --help self-documentation.
- Recommendation: Add argparse with description and argument help text

#### lint-5 — No json.dumps in wake.py

- Lens: lint
- Location: `scripts/wake.py`
- Evidence: Output may not be structured JSON.
- Recommendation: Use json.dumps for structured output

### Low (7)

#### determinism-2 — Template placeholder scanning delegated to LLM

- Lens: determinism
- Location: `references/first-breath.md`
- Evidence: Prompt instructs LLM to scan for remaining {placeholder} and replace.
- Recommendation: Move placeholder scan into init-sanctum.py as post-processing step

#### leanness-1 — Parenthetical restates sourcing principle from CREED

- Lens: leanness
- Location: `references/research-patterns.md`
- Evidence: '(sourcés depuis les skills)' appended to section header. CREED already enshrines Vérité sourcée.
- Recommendation: Drop the parenthetical

#### leanness-2 — Role meta-explanation redundant with CREED Boundaries

- Lens: leanness
- Location: `references/enrich-spec.md`
- Evidence: Role explanation duplicates CREED Boundaries.
- Recommendation: Drop role-explanatory sentence, keep consumer/artifact spec

#### leanness-3 — Curseur restates role boundary again

- Lens: leanness
- Location: `references/enrich-spec.md`
- Evidence: Curseur repeats same role carve-out already at line 11.
- Recommendation: Remove the curseur block

#### leanness-5 — Role preamble adds no dimension over CREED

- Lens: leanness
- Location: `references/enrich-spec.md`
- Evidence: Two role-clarification sentences are only content beyond I/O spec. Define boundary already in CREED.
- Recommendation: Cut both role clarifications. File reduces to 5 lines of pure I/O spec.
- Proposed smallest: Lis spec.md et findings.md. Propose dans enrichment-proposal.md des dépendances, contraintes techniques, patterns d'implémentation et points d'attention. L'Architecte valide et intègre.
- Predicted delta: Minimal. CREED Boundaries already prevent role encroachment.

#### agent-cohesion-3 — No proactive deprecated-pattern detection across phases

- Lens: agent-cohesion
- Location: `references/research-patterns.md vs references/verify-approach.md`
- Evidence: verify-approach spots deprecation reactively but research-patterns has no proactive cross-reference step.
- Recommendation: Add note to re-validate prior phase recommendations against current documentation

#### lint-6 — No sys.exit() calls in wake.py

- Lens: lint
- Location: `scripts/wake.py`
- Evidence: May not return meaningful exit codes.
- Recommendation: Return 0=success, 1=fail, 2=error via sys.exit()
