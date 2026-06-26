# MASB — Marwane Android Spec Builder

Framework de développement guidé par l'IA pour la création d'applications mobiles Android.

MASB orchestre un workflow complet : de l'idéation d'une feature jusqu'à la construction du projet, l'écriture du code, la compilation, les tests et les commits versionnés. Le module s'appuie sur les [skills officiels Android](https://github.com/android/skills) de Google ainsi que des skills personnalisés.

## Installation

```bash
npx skills add github:Marwichmisi/MASB
```

Une fois installé, activez **masb-setup** dans opencode pour lancer la configuration interactive.

## Architecture

**Workflow centré sur les phases, agents spécialisés, dossier par phase.**

```
┌───────────────────────────────────────────────────────────┐
│ 1. Architecte  : spec.md (HITL — à l'activation de phase) │
│ 2. Research     : research/findings.md                     │
│ 3. Agent UI/UX  : ui-spec.md (décline le design-system)    │
│ 4. Développeur  : code/ (skills dédiés)                    │
│ 5. Reviewer     : review-report.md                         │
│ 6. Testeur      : test-report.md + compile check           │
│ 7. DevOps       : commit → branche → PR → merge HITL      │
└───────────────────────────────────────────────────────────┘
```

Chaque phase produit ses artefacts dans `masb-workspace/phases/NN-nom-phase/` :
- `spec.md` — Spécification de la phase
- `research/findings.md` — Patterns et documentation
- `ui-spec.md` — Déclinaison UI/UX
- `code/` — Implémentation
- `review-report.md` — Rapport de revue
- `test-report.md` — Rapport de tests
- `progress.md` — Statut et blocages

## Skills du module

### Agents MASB

| Skill | Type | Rôle | Capacités |
|-------|------|------|-----------|
| **masb-agent-architecte** | Agent (memory) | Découpage du projet en phases et rédaction de specs | `brainstorm`, `prd`, `decompose`, `spec`, `replan`, `ideate`, `quickplan`, `validate`, `rescope` |
| **masb-agent-research** | Agent (memory) | Recherche de patterns et bonnes pratiques Android | `research-patterns`, `enrich-spec`, `verify-approach` |
| **masb-agent-ux** | Agent (memory) | Design system Material 3 et déclinaison UI | `design-system`, `ui-spec`, `accessibility-check`, `theme-validate` |
| **masb-agent-developpeur** | Agent (memory) | Implémentation du code Android | `implement`, `compile-check`, `auto-fix` |
| **masb-agent-reviewer** | Agent (stateless) | Revue de code sécurité et performance | `security-review`, `perf-review`, `lint-report` |
| **masb-agent-testeur** | Agent (memory) | Tests, compilation et analyse de performance | `compile-verify`, `run-tests`, `perf-analyze`, `failure-report` |
| **masb-agent-devops** | Agent (memory) | Gestion Git, branches, PRs et merges | `create-branch`, `commit-phase`, `create-pr`, `merge-phase`, `rollback`, `check-status`, `validate-gate` |
| **masb-workflow-status** | Workflow | Suivi d'avancement du projet | `display_status` (commande: `masb status`) |

### Skills Android Google wrappés

Chaque agent MASB s'appuie sur les skills officiels Android pour garantir des implémentations conformes aux standards :

| Agent | Skills Android utilisés |
|-------|----------------------|
| **masb-agent-research** | `context7-cli`, `android-cli` |
| **masb-agent-developpeur** | `camera1-to-camerax`, `navigation-3`, `edge-to-edge`, `adaptive`, `styles`, `migrate-xml-views`, `appfunctions`, `verified-email`, `wear-compose-m3`, `display-glasses-glimmer`, `play-billing`, `engage-sdk`, `font-m3-cli`, `material-symbols-cli` |
| **masb-agent-reviewer** | `android-intent-security`, `r8-analyzer` |
| **masb-agent-testeur** | `testing-setup`, `perfetto-sql`, `perfetto-trace-analysis` |
| **masb-agent-devops** | `agp-9-upgrade`, `android-cli` |
| **masb-agent-ux** | `font-m3-cli`, `material-symbols-cli`, `adaptive`, `styles`, `edge-to-edge` |

### Dépendances système

| Dépendance | Agent concerné | Installation |
|-----------|----------------|--------------|
| Android SDK / CLI tools | Tous | `android-cli` ou `sdkmanager` |
| JDK 17+ | Développeur, Testeur | Vérifier présence |
| Git | DevOps | Vérifier présence |
| Skills Google Android | Tous | `android skills add --all` |
| `bun` | Research | Vérifier présence |
| `context7-cli` | Research | Installer via skill |
| `font-m3-cli` | Développeur, UX | Installer via skill |
| `material-symbols-cli` | Développeur, UX | Installer via skill |

## Configuration

Lors de l'installation, le setup skill collecte ces variables :

| Variable | Description |
|----------|-------------|
| `project_name` | Nom du projet Android |
| `package_name` | Package name (ex: com.example.app) |
| `github_repo` | URL du dépôt GitHub |
| `git_user_name` | Nom Git pour les commits |
| `git_user_email` | Email Git pour les commits |

## Commandes

- `masb status` — Affiche la phase courante, les étapes complétées et les prochaines actions
- `masb help` — Affiche l'aide du module et les commandes disponibles

## Workflow de développement

1. **L'Architecte** brainstome avec vous et décompose le projet en phases
2. **Phase 00** : l'UI/UX Designer produit le design system global (palette, typo, thème M3)
3. **Par phase** : Research → UI/UX → Développeur → Reviewer → Testeur → DevOps
4. **Validation HITL** à chaque transition de phase
5. **Boucle d'échec** : Review ou Test échoué → Dev patch → re-validation
6. **Gate DevOps** : bloque tant que review + tests ne sont pas verts
7. **Merge** : PR validée par l'utilisateur → merge dans main

## Cas d'utilisation créatifs

- **Mode audit** : Lancer Research + Reviewer sans Développeur pour auditer un projet existant
- **Mode apprentissage** : L'Architecte aide un débutant à décomposer un projet
- **CI/CD bridge** : DevOps utilisable indépendamment pour tout projet Git
- **Parallélisation massive** : Features indépendantes exécutées en parallèle

## Licence

MIT
