---
title: 'Marwane Android Spec Builder (MASB)'
status: 'complete'
module_name: 'Marwane Android Spec Builder'
module_code: 'MASB'
module_description: 'MASB est un framework de Développement guidé par l\'IA pour la création d\'application mobile'
architecture: ''
standalone: true
expands_module: ''
skills_planned:
  - masb-agent-architecte
  - masb-agent-research
  - masb-agent-ux
  - masb-agent-developpeur
  - masb-agent-reviewer
  - masb-agent-testeur
  - masb-agent-devops
  - masb-workflow-status
config_variables: []
created: '2026-06-26'
updated: '2026-06-26'
---

# Module Plan: Marwane Android Spec Builder (MASB)

## Vision

<!-- What this module does, who it's for, and why it matters -->

MASB est un framework complet de développement d'applications mobiles Android, guidé par l'IA.
Il orchestre un workflow complet : de l'idéation et brainstorming d'une feature, jusqu'à la construction du projet, l'écriture du code, la compilation, les tests, et les commits versionnés.
Le module s'appuie sur les skills officiels Android de Google (https://github.com/android/skills) ainsi que des skills personnalisés.
L'agent doit prioriser la consultation des skills pour les règles, la documentation, les patterns recommandés — afin d'éviter les hallucinations et de ne pas réinventer la roue.

## Architecture

**Patron : Workflow centré sur les phases, agents spécialisés, dossier par phase**

Pas d'agent orchestrateur dédié. Le workflow est piloté par un découpage en phases.
Chaque phase est un dossier autonome qui contient tout ce qui concerne son exécution.

### Déroulement global

1. **Architecte** → session brainstorming interactive avec l'utilisateur
   - Comprend le projet, les features, les attentes
   - Découpe l'idée en **phases** (ex: 01-setup, 02-auth, 03-ui-main...)
   - Pour chaque phase : écrit une spec dans son dossier dédié
   - Enregistre tout dans `masb-workspace/brainstorm.md` et `masb-workspace/phases-index.md`
   - Validation HITL avant de lancer la première phase

2. **Par phase** (ex: `masb-workspace/phases/01-setup/`) :
   - `spec.md` — spec de la phase (par Architecte)
   - `research/findings.md` — patterns, documentation (par Research)
   - `code/` — implémentation (par Développeur)
   - `review-report.md` — revue (par Reviewer)
   - `test-report.md` — tests (par Testeur)
   - `progress.md` — statut de la phase

3. À chaque nouvelle phase, on relance le workflow :
   - Research consulte à nouveau les skills adaptés à CETTE phase
   - Développeur implémente selon la spec de CETTE phase
   - Les recherches et implémentations varient selon la phase

### Phase 00 : Design System

Avant la première phase fonctionnelle, une phase dédiée :
1. **Agent UI/UX** → produit `design-system.md` (palette, typo, icônes, thème M3, accessibilité)
2. **HITL** → validation utilisateur du design system
3. Le design system est figé pour tout le projet

### Cycle de vie d'une phase standard

```
┌───────────────────────────────────────────────────────────┐
│ 1. Architecte  : spec.md (HITL — à l'activation de phase) │
│ 2. Research     : research/findings.md                     │
│ 3. Agent UI/UX  : ui-spec.md (décline le design-system)    │
│ 4. Développeur  : code/ (skills dédiés)                    │
│ 5. Reviewer     : review-report.md                         │
│    └── issues → blocked:review dans progress.md            │
│    └── Dev patch → re-review → review-passed              │
│ 6. Testeur      : test-report.md + compile check           │
│    └── failures → blocked:tests dans progress.md           │
│    └── Dev patch → re-test → tests-passed                 │
│ 7. DevOps       : commit → branche → PR → merge HITL      │
│    └── Bloqué tant que review-passed + tests-passed ≠ OK  │
└───────────────────────────────────────────────────────────┘
```

**Règle :** Une phase ne passe au DevOps que si `review-passed` et `tests-passed` sont verts dans `progress.md`.
```

### Memory Architecture

**Deux zones distinctes :**

```
masb-workspace/                           ← Dossier de travail du PROJET
├── brainstorm.md                         ← Idées brutes, vision globale (par Architecte)
├── prd.md                                ← Vision produit, features, user stories
├── design-system.md                      ← Palette, typo, icônes, thème M3 (par UI/UX — phase 00)
├── phases-index.md                       ← Liste toutes les phases, statut, ordre
└── phases/
    ├── 00-design-system/                 ← Phase design system (UI/UX)
    │   └── ui-spec.md
    └── 01-nom-de-la-phase/               ← Un dossier PAR phase
        ├── spec.md                       ← Spec (Architecte)
        ├── research/
        │   └── findings.md               ← Recherches (Research)
        ├── ui-spec.md                    ← Déclinaison UI/UX de la phase
        ├── code/                         ← Code (Développeur)
        ├── review-report.md              ← Revue (Reviewer) — contient issues: []
        ├── test-report.md                ← Tests (Testeur) — contient failures: []
        └── progress.md                   ← Statut (review-passed, tests-passed)

_bmad/memory/masb/
├── shared/
│   ├── index.md                          ← Projet, stack, architecture décidée
│   └── decisions.md                      ← Décisions globales
└── agents/
    ├── architecte/daily/                 ← Journal perso (raw, horodaté)
    ├── research/daily/
    ├── architecte/daily/
    ├── research/daily/
    ├── ux/daily/
    ├── developpeur/daily/
    ├── reviewer/daily/
    ├── testeur/daily/
    └── devops/daily/
```

### Memory Contract

| Fichier | Agents | Contenu |
|---------|--------|---------|
| `masb-workspace/brainstorm.md` | Architecte → User | Idées brutes, vision, features souhaitées |
| `masb-workspace/prd.md` | Architecte → User → Tous | Vision produit, features, contraintes, user stories |
| `masb-workspace/design-system.md` | UI/UX → Tous | Palette, typo, icônes, thème M3, accessibilité (figé phase 00) |
| `masb-workspace/phases-index.md` | Tous | Liste des phases avec statut |
| `masb-workspace/phases/N/spec.md` | Architecte → Research, Dev, UI/UX | Spec détaillée de la phase (écrite à l'activation) |
| `masb-workspace/phases/N/research/findings.md` | Research → Dev, UI/UX | Patterns, doc consultée, recommandations |
| `masb-workspace/phases/N/ui-spec.md` | UI/UX → Dev, Reviewer | Déclinaison visuelle de la phase (réf. design-system.md) |
| `masb-workspace/phases/N/code/` | Dev → Reviewer, Testeur | Code implémenté |
| `masb-workspace/phases/N/review-report.md` | Reviewer → Dev | Résultat review avec `issues: []` |
| `masb-workspace/phases/N/test-report.md` | Testeur → Dev | Rapport test avec `failures: []` |
| `masb-workspace/phases/N/progress.md` | Agent actif | Statut, blocages, `review-passed`, `tests-passed` |
| `_bmad/memory/masb/shared/index.md` | Tous | Contexte global persistant du projet |
| `_bmad/memory/masb/shared/decisions.md` | Tous | Décisions clés avec rational |
| `_bmad/memory/masb/agents/X/daily/` | Agent X | Journal personnel brut |

### Cross-Agent Patterns

- **Router :** L'utilisateur via `masb status` + validation HITL aux transitions de phase
- **Parallélisation :** Phases indépendantes détectées par l'Architecte → exécutées en parallèle par sous-agents dans leurs dossiers respectifs
- **Handoff phase → phase :** Séquentiel — une phase doit être mergée avant que la suivante commence (sauf parallélisation)
- **Handoff interne phase :** Architecte → Research → UI/UX → Dev → Reviewer → Testeur → DevOps
- **Boucle échec Review :** Reviewer trouve `issues` → écrit dans `review-report.md` → marque `blocked: review` dans `progress.md` → Dev lit le rapport → patch → re-review → OK → `review-passed`
- **Boucle échec Test :** Testeur trouve `failures` → écrit dans `test-report.md` avec logs → marque `blocked: tests` dans `progress.md` → Dev lit le rapport → patch → re-test → OK → `tests-passed`
- **Gate DevOps :** Impossible de lancer DevOps tant que `review-passed` + `tests-passed` ≠ `true` dans `progress.md`
- **Re-décomposition :** À tout moment, l'Architecte peut être ré-invoqué → met à jour `phases-index.md` et peut créér de nouveaux dossiers de phase

## Skills

### masb-agent-architecte

**Type:** Agent

**Persona:** Architecte logiciel méthodique et pédagogue. Pose les bonnes questions pour comprendre la vision du projet avant de toucher au moindre code. Esprit de synthèse, capable de décomposer des idées complexes en phases claires.

**Core Outcome:** Le projet est découpé en phases autonomes, chaque phase a une spec claire validée par l'utilisateur — prêt à implémenter.

**The Non-Negotiable:** Rien n'est implémenté tant que l'utilisateur n'a pas validé le PRD, la décomposition et les specs.

**Capacités:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| `brainstorm` | Session interactive pour comprendre la vision, features, attentes | Idée du user (libre) | `masb-workspace/brainstorm.md` |
| `prd` | Rédaction du document PRD (vision produit, features, contraintes, user stories) | `brainstorm.md` | `masb-workspace/prd.md` |
| `decompose` | Découpage du projet en phases autonomes | `prd.md`, `brainstorm.md` | `masb-workspace/phases-index.md` + dossiers |
| `spec` | Rédaction de la spec d'une phase (à l'activation UNIQUEMENT) | Phase sélectionnée + `prd.md` | `masb-workspace/phases/N/spec.md` |
| `replan` | Re-découpage d'une phase existante | Phase à re-décomposer | `spec.md` mise à jour |

**Memory:** Écrit `brainstorm.md`, `phases-index.md`, `phases/N/spec.md`. Journal perso dans `architecte/daily/`.

**Init Responsibility:** Créer le dossier `masb-workspace/` et initialiser `brainstorm.md` et `phases-index.md`.

**Activation Modes:** Interactive (HITL obligatoire).

**Tool Dependencies:** Aucun — pas de skill technique direct.

**Design Notes:** L'Architecte ne touche pas au code. Son rôle s'arrête quand la spec est validée. L'utilisateur valide chaque phase avant son exécution.

---

### masb-agent-research

**Type:** Agent

**Persona:** Expert en veille technique, documentation-oriented. Consulte les skills Google Android, la doc SDK, les patterns recommandés avant la moindre ligne de code.

**Core Outcome:** Chaque phase a un rapport de recherche listant les patterns, APIs, et bonnes pratiques à suivre — sourcé depuis les skills officiels.

**The Non-Negotiable:** Ne jamais inventer une API ou un pattern. Tout doit être sourcé depuis les skills Google Android ou la documentation officielle.

**Capacités:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| `research-patterns` | Étude des skills Android pour trouver les patterns adaptés à la phase | `phases/N/spec.md` | `phases/N/research/findings.md` |
| `enrich-spec` | Enrichit la spec avec les patterns et recommandations trouvés | `spec.md` + `findings.md` | `spec.md` enrichie (proposition) |
| `verify-approach` | Vérifie que l'approche choisie est valide selon les skills | Approche proposée | Rapport de conformité / alertes |

**Memory:** Lit `spec.md`. Écrit `research/findings.md`. Journal perso dans `research/daily/`.

**Init Responsibility:** Aucune — attend qu'une phase ait une spec.

**Activation Modes:** Headless (par défaut) + interactif si blocage documentaire.

**Tool Dependencies:** `context7-cli`, `android-cli`, skills Google Android wrappés.

**Design Notes:** Les findings sont propres à chaque phase. Une phase "navigation" va chercher des patterns différents d'une phase "camera".

---

### masb-agent-developpeur

**Type:** Agent

**Persona:** Développeur Android expert. Suit les patterns sans dévier. Consulte toujours les skills Google avant d'écrire du code.

**Core Outcome:** Code fonctionnel, compilé, qui suit les patterns recommandés par les skills Android — pas de code inventé.

**The Non-Negotiable:** Consulter les skills Google AVANT d'écrire la première ligne. Vérifier la compilation avant de passer la main.

**Capacités:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| `implement` | Implémente le code selon la spec enrichie | `spec.md` + `findings.md` | `phases/N/code/` |
| `compile-check` | Vérifie que le code compile | Code | Résultat compilation |
| `auto-fix` | Corrige les erreurs de compilation simples | Logs d'erreur | Code patché |

**Memory:** Lit `spec.md`, `research/findings.md`. Écrit dans `phases/N/code/`. Journal perso dans `developpeur/daily/`.

**Init Responsibility:** Aucune — attend qu'une phase ait une spec + findings.

**Activation Modes:** Headless (par défaut) + interactif pour arbitrages techniques.

**Tool Dependencies (skills Google wrappés):** `camera1-to-camerax`, `navigation-3`, `edge-to-edge`, `adaptive`, `styles`, `migrate-xml-views`, `appfunctions`, `verified-email`, `wear-compose-m3`, `display-glasses-glimmer`, `play-billing`, `engage-sdk`, `font-m3-cli`, `material-symbols-cli`.

**Design Notes:** Le développeur utilise des sous-agents pour ne pas surcharger son contexte. Chaque fichier ou feature peut être délégué à un sous-agent.

---

### masb-agent-ux

**Type:** Agent

**Persona:** Designer UI/UX spécialiste Material Design. Sens de l'esthétique, de la cohérence et de l'accessibilité. Connaît les guidelines Material 3 sur le bout des doigts.

**Core Outcome:** Un design system cohérent (phase 00) + une déclinaison visuelle par phase qui respecte le design system. Cohérence garantie sur tout le projet.

**The Non-Negotiable:** Chaque phase UI DOIT décliner le `design-system.md` — jamais réinventer la palette ou la typo en cours de route.

**Capacités:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| `design-system` | Produit le design system global du projet (phase 00) | `prd.md`, `brainstorm.md` | `design-system.md` (palette, typo via font-m3, icônes via material-symbols, thème M3, accessibilité) |
| `ui-spec` | Décline le design system pour une phase spécifique | `phase/spec.md` + `design-system.md` | `phase/ui-spec.md` (écrans, flux, navigation, layout) |
| `accessibility-check` | Vérifie l'accessibilité du design | `ui-spec.md` | Rapport accessibilité |
| `theme-validate` | Valide la cohérence entre phases | `design-system.md` + toutes les `ui-spec.md` | Rapport de cohérence |

**Memory:** Lit `spec.md`, `design-system.md`, `research/findings.md`. Écrit `design-system.md` (phase 00) et `phases/N/ui-spec.md`. Journal perso dans `ux/daily/`.

**Init Responsibility:** Attend la phase 00 pour produire le design system.

**Activation Modes:** Headless + HITL (validation du design system phase 00).

**Tool Dependencies (skills wrappés):** `font-m3-cli`, `material-symbols-cli`, `adaptive`, `styles`, `edge-to-edge`.

**Design Notes:** Phase 00 = design system global. Ensuite, chaque phase UI lit `design-system.md` + `spec.md` de la phase et produit une déclinaison. Le Reviewer vérifie la conformité au design system.

---

### masb-agent-reviewer

**Type:** Agent

**Persona:** Pair reviewer exigeant. Sécurité-first, performance-aware. Ne laisse rien passer.

**Core Outcome:** Code audité — zéro vulnérabilité, patterns sécurisés, pas de régression perf.

**The Non-Negotiable:** Si un skill security/perf existe pour le pattern utilisé, il DOIT être consulté.

**Capacités:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| `security-review` | Audit sécurité du code via skills dédiés | `code/` | `review-report.md` (section security) |
| `perf-review` | Audit performance du code | `code/` | `review-report.md` (section perf) |
| `lint-report` | Rapport de linting et code style | `code/` | `review-report.md` (section lint) |

**Memory:** Lit `code/`, `spec.md`. Écrit `review-report.md`. Journal perso dans `reviewer/daily/`.

**Init Responsibility:** Aucune — attend que Dev ait écrit du code.

**Activation Modes:** Headless.

**Tool Dependencies (skills Google wrappés):** `android-intent-security`, `r8-analyzer`.

**Design Notes:** Le reviewer examine le code sans l'exécuter. Si des problèmes sont détectés, il les documente dans `review-report.md` et le développeur les corrige avant de passer au testeur.

---

### masb-agent-testeur

**Type:** Agent

**Persona:** QA engineer rigoureux. Tests, compilation, perf. Ne valide que quand tout est vert.

**Core Outcome:** Tests qui passent, code qui compile, rapport clair. Si échec : rapport détaillé pour le développeur.

**The Non-Negotiable:** Ne jamais dire "c'est bon" si les tests ne passent pas ou si la compilation échoue.

**Capacités:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| `compile-verify` | Vérifie compilation du projet complet | Projet | Résultat compilation |
| `run-tests` | Exécute la suite de tests | Projet + config test | Résultat des tests |
| `perf-analyze` | Analyse performance via Perfetto | Trace | Rapport perf |
| `failure-report` | Rapport d'échec détaillé | Logs d'échec | `test-report.md` + alerte dans `progress.md` |

**Memory:** Lit `code/`, `spec.md`. Écrit `test-report.md`. Met à jour `progress.md` avec blocages. Journal perso dans `testeur/daily/`.

**Init Responsibility:** Aucune — attend que Reviewer ait validé le code.

**Activation Modes:** Headless.

**Tool Dependencies (skills Google wrappés):** `testing-setup`, `perfetto-sql`, `perfetto-trace-analysis`.

**Design Notes:** En cas d'échec, écrit un rapport dans `test-report.md` et marque le blocage dans `progress.md`. Le développeur est notifié et patch. Boucle jusqu'à succès.

---

### masb-agent-devops

**Type:** Agent

**Persona:** DevOps engineer organisé, Git expert. Branches propres, messages structurés, PRs claires.

**Core Outcome:** Historique Git propre — branche par phase majeure, commits atomiques, PRs bien nommées, merges validés HITL.

**The Non-Negotiable:** Chaque phase majeure = une branche dédiée. Jamais de commit direct sur main. HITL obligatoire avant merge.

**Capacités:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| `create-branch` | Crée une branche dédiée à la phase | Phase | Branche Git |
| `commit-phase` | Commit le code de la phase avec message structuré | `code/` | Commit |
| `create-pr` | Ouvre une PR avec description | Branche | PR GitHub |
| `merge-phase` | Merge la PR après validation | PR | Merge |
| `rollback` | Retour arrière vers une phase stable | Phase cible | Code restauré |

**Memory:** Lit `phases-index.md`, `progress.md` des phases. Journal perso dans `devops/daily/`.

**Init Responsibility:** Cloner le repo, configurer le remote.

**Activation Modes:** Headless (exécution Git) + HITL (validation PR/merge).

**Tool Dependencies (skills Google wrappés):** `agp-9-upgrade`, `android-cli`.

**Design Notes:** Le DevOps suit le plan de phases — il sait quelles phases sont complétées et prêtes à être mergées.

---

### masb-workflow-status

**Type:** Workflow (pas un agent)

**Core Outcome:** L'utilisateur sait où on en est et quoi faire.

**Capacité unique :** Lit `phases-index.md` et `progress.md` de la phase active. Affiche :

- Phase courante et son statut
- Prochaine action attendue
- Blocages éventuels
- Résumé des phases complétées

**Commande :** `masb status`

## Configuration

### Variables de configuration

| Variable | Prompt | Default | Résultat | User Setting |
|----------|--------|---------|----------|-------------|
| `project_name` | Nom du projet Android ? | — | `{value}` | non |
| `package_name` | Package name (ex: com.example.app) ? | — | `{value}` | non |
| `github_repo` | URL du dépôt GitHub ? | — | `{value}` | non |
| `git_user_name` | Nom Git pour les commits | détection auto | `{value}` | non |
| `git_user_email` | Email Git pour les commits | détection auto | `{value}` | non |

**Note :** `min_sdk` / `target_sdk` / `compile_sdk` ne sont pas en config — ils sont déterminés par l'Architecte lors du discovery en fonction des dépendances du projet. Les skills wrapperont cette décision dans la spec.

### Commandes du module
- `masb status` — Affiche la phase courante, les étapes complétées et les prochaines actions (lit `shared/progress.md`)
- `masb help` — Affiche l'aide du module et les commandes disponibles

## External Dependencies

| Dépendance | Skills concernés | Action setup |
|-----------|-----------------|-------------|
| Android SDK / CLI tools | Tous | Installer si absent via `android-cli` ou `sdkmanager` |
| JDK 17+ | Développeur, Testeur | Vérifier présence, guider installation |
| Git | DevOps | Vérifier présence, configurer si besoin |
| Skills Google Android (tous) | Tous (wrappés) | Installer via `android skills add --all` |
| `bun` | Research (context7-cli) | Vérifier présence |
| `context7-cli` | Research | Installer via skill |
| `font-m3-cli` | Développeur | Installer via skill |
| `material-symbols-cli` | Développeur | Installer via skill |

## UI and Visualization

Pas de dashboard UI. L'état d'avancement est consultable via :
- `masb status` — affichage en console de la phase courante et des prochaines étapes
- `masb help` — aide du module

## Setup Extensions

1. **Wrapper les skills Android** : le setup installe tous les skills Google Android via `android skills add --all`, puis les mappe aux agents concernés
2. **Création du workspace** : initialise `masb-workspace/` avec `brainstorm.md` et `phases-index.md`
3. **Installation des skills customs** : `context7-cli`, `font-m3-cli`, `material-symbols-cli`
4. **Vérification des dépendances externes** : JDK, Git, Android SDK
5. **Git** : cloner ou init le repo, configurer remote

## Integration

Module autonome. Ne dépend d'aucun autre module BMad.
Tous les skills Google Android sont wrappés comme dépendances internes.
Les skills personnalisés sont inclus dans le module.

## Creative Use Cases

- **Mode audit** : lancer Research + Reviewer sans Développeur pour auditer un projet existant
- **Mode apprentissage** : l'Architecte peut aider un débutant à comprendre comment décomposer un projet
- **CI/CD bridge** : le DevOps peut être utilisé indépendamment pour gérer le workflow Git d'autres projets
- **Parallélisation massive** : sur un projet avec 5 features indépendantes, 5 phases peuvent tourner en parallèle

## Ideas Captured

### Session 1 — 2026-06-26

**Vision initiale :**
- Module de création d'apps mobiles Android — complet, pour tout type d'app, même projets d'envergure
- Workflow complet : idéation → brainstorming → décomposition en phases → specs → sous-phases → consultation des skills → code → compilation → tests → commit → PR → merge
- Basé sur les skills officiels Google Android (https://github.com/android/skills) + skills personnalisés

**Contraintes clés :**
- L'agent DOIT prioriser l'usage des skills pour connaître les règles, chercher la documentation — éviter de tourner en rond et d'inventer des choses
- L'agent doit vérifier la compilation et les tests avant de déclarer une implémentation terminée
- Commits à certains niveaux — une branche par phase majeure, PR distinctes, merge quand terminé
- Utilisation exclusive des skills officiels Android — pas de limitation, toute la suite disponible

**Architecture agents (validée) :**
- **Orchestrateur** — coordonne le workflow global, décide de la parallélisation
- **Architecte** — brainstorming, mode discovery, décomposition en phases/specs, human-in-the-loop
- **Research** — recherche des patterns Android avant implémentation, prépare les bases
- **Développeur** — implémentation du code
- **Reviewer** — revue de code
- **Testeur** — compilation + tests
- **DevOps** — branches, commits, PRs, merges

**Mapping skills → agents :**
- Architecte : *(aucun skill tech)*
- Research : context7-cli, android-cli
- Développeur : camera1-to-camerax, navigation-3, edge-to-edge, adaptive, styles, migrate-xml-views, appfunctions, verified-email, wear-compose-m3, display-glasses-glimmer, play-billing, engage-sdk, font-m3-cli, material-symbols-cli
- Reviewer : android-intent-security, r8-analyzer
- Testeur : testing-setup, perfetto-sql, perfetto-trace-analysis
- DevOps : agp-9-upgrade, android-cli
- Orchestrateur : tous (pour savoir qui appeler)
- UI/UX : font-m3-cli, material-symbols-cli, adaptive, styles, edge-to-edge

**Décisions clés :**
- Pas d'agent orchestrateur — workflow géré via les phases (Architecte décompose)
- Architecte : brainstorming complet → décomposition en phases → spec par phase (pas de PRD)
- Dossier par phase : `masb-workspace/phases/N-nom/` avec spec, research, code, reports
- Research et implémentation varient selon chaque phase (relance à chaque phase)
- Human-in-the-loop : validation utilisateur à chaque transition de phase
- Mémoire : deux zones — `masb-workspace/` (travail par phase) + `_bmad/memory/masb/` (persistant)
- Pas de `curated/` par agent — que des `daily/` pour les journaux perso
- Pas de dashboard UI, mais `masb status` en console
- Échec de test → rapport → boucle Dev patch
- Re-décomposition possible à tout moment
- Wrapper les skills Android en dépendances intégrées
- Parallélisation sur features indépendantes
- Agent UI/UX dédié avec design system global (phase 00) + déclinaison par phase
- PRD (`prd.md`) documenté par l'Architecte pendant le brainstorming
- Spec écrite UNIQUEMENT à l'activation de la phase (pas tout d'un coup)
- Boucle échec Review : blocked → Dev patch → re-review → review-passed
- Boucle échec Test : blocked → Dev patch → re-test → tests-passed
- Gate DevOps : review-passed + tests-passed obligatoires
- Sous-agents IA pour éviter la surcharge de contexte
- Branche par phase majeure, PR + merge HITL

## Build Roadmap

**Ordre de construction recommandé :**

1. **masb-agent-architecte** — Le cœur du module. Sans lui, rien n'est décomposé.
2. **masb-workflow-status** — Indispensable pour le suivi utilisateur.
3. **masb-agent-devops** — Git et branches. Nécessaire dès la première phase.
4. **masb-agent-research** — Précède les implémenteurs. Consultation des skills Google.
5. **masb-agent-ux** — Design system. Dépend de Research.
6. **masb-agent-developpeur** — Implémentation. Dépend de Research + UI/UX.
7. **masb-agent-reviewer** — Review. Dépend du Développeur.
8. **masb-agent-testeur** — Tests. Dépend du Développeur.

**Recommandation :** Construire 1 → 2 → 3 en séquence. Puis 4 + 5 en parallèle. Puis 6. Puis 7 + 8 en parallèle.

**Next steps:**

1. Build each skill using **Build an Agent (BA)** or **Build a Workflow (BW)** — share this plan document as context
2. When all skills are built, return to **Create Module (CM)** to scaffold the module infrastructure
