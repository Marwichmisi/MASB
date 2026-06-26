# Analysis Report: /home/marwane/Documents/momono/skills/masb-workflow-status

Generated: 2026-06-26T04:42:00Z · Schema: 2

**Grade: Good**

> Skill solide et légère (389 tokens) avec deux axes d'amélioration : déplacer la logique déterministe dans un script et ajouter un mode JSON headless.

Le skill masb-workflow-status est remarquablement lean (389 tokens, 2 sections) et fait ce qu'il promet. Les deux findings haute sévérité portent sur la logique de détection de phase active (déterministe, devrait être un script) et l'absence de sortie JSON pour la composabilité headless. Quelques améliorations mineures de robustesse complètent le tableau.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 2 |
| Medium | 2 |
| Low | 2 |

## Themes

### 1. Logique déterministe dans le prompt

- Root cause: Le prompt demande au LLM de faire du parsing conditionnel (chercher un statut, appliquer des règles de fallback, détecter un état terminal) qui a une seule réponse correcte pour chaque entrée donnée. C'est du travail qu'un script fait gratuitement et exactement.
- Fix: Extraire la détection de phase active dans scripts/active-phase.py : lire phases-index.md, appliquer les règles (active > in_progress > première incomplète > all done), et retourner le résultat en JSON. Le prompt appelle le script et interprète seulement le résultat.
- Findings:
  - `determinism-1` Logique de détection de phase active dans le prompt — `SKILL.md:20`
  - `leanness-1` Résolution de `{project-root}` circulaire — `SKILL.md:14`
  - `leanness-2` Cas de plusieurs phases actives non spécifié — `SKILL.md:20`

### 2. Composabilité et sortie headless

- Root cause: Le skill ne produit qu'un texte formaté, sans alternative machine-parseable. Impossible pour un autre skill ou outil de consommer le résultat programmatiquement.
- Fix: Ajouter un mode --json qui émet un objet structuré (phase, statut, next_action, blockers, completed_phases) en plus du texte formaté. Fournir un template de sortie texte précis pour garantir la cohérence entre runs.
- Findings:
  - `enhancement-1` ADD: Mode sortie JSON headless — `SKILL.md:24-28`
  - `enhancement-2` ADD: Template de sortie texte précis — `SKILL.md:24-28`

## Strengths

- Lean : 389 tokens, bien sous le budget de 2000
- Graceful degradation : gère l'absence de fichiers et l'état terminal
- Architecture propre : simple-workflow, pas de ceremony inutile
- Frontmatter correct avec déclencheur en français

## Recommendations

1. Écrire scripts/active-phase.py pour la détection déterministe de la phase active, ce qui résout determinism-1 et clarifie le contrat de leanness-1/leanness-2 (resolves: determinism-1, leanness-1, leanness-2)
2. Ajouter le mode --json pour la sortie headless et un template de texte précis (resolves: enhancement-1, enhancement-2)
3. Ajouter un parse-guard pour les fichiers corrompus (enhancement-3) (resolves: enhancement-3)

## Experience

- **Première utilisation** — L'utilisateur tape 'masb status' → le skill lit les fichiers et affiche le statut. Clair et immédiat.
- **Projet non initialisé** — phases-index.md manquant → message 'aucun projet MASB initialisé'. Dégradation élégante.
- **Projet terminé** — Toutes les phases complétées → message 'projet terminé'. Dégradation élégante.
- **Phase avec blocage** — Le skill affiche blocked:review ou blocked:tests dans la section blocages. L'utilisateur sait quoi corriger.
- Headless: Pas encore headless-ready. L'ajout d'un flag --json (recommandation rank 2) le rendrait invocable par d'autres skills et scripts.

## Findings

### High (2)

#### determinism-1 — Logique de détection de phase active dans le prompt

- Lens: determinism
- Location: `SKILL.md:20`
- Evidence: Step 2 demande au LLM de parser phases-index.md, chercher un statut 'active' ou 'in_progress', appliquer un fallback, et détecter si toutes les phases sont complétées. C'est de la logique conditionnelle structurée, pas de l'interprétation qualitative.
- Recommendation: Ajouter un script scripts/active-phase.py qui lit phases-index.md, sélectionne la phase active via les règles décrites, et retourne le résultat. Le prompt appelle ce script au lieu de faire la logique elle-même.

#### enhancement-1 — ADD: Mode sortie JSON headless

- Lens: enhancement
- Location: `SKILL.md:24-28`
- Evidence: Produit seulement du texte non structuré, pas d'alternative machine-parseable. Casse le pattern de composabilité où les skills d'information devraient pouvoir alimenter d'autres skills en données structurées.
- Recommendation: Ajouter un flag --json qui émet un objet JSON structuré (phase name, status, next action, blockers, completed phases) à la place du texte formaté, pour que 'masb status --json' alimente d'autres skills BMad.

### Medium (2)

#### leanness-1 — Résolution de `{project-root}` circulaire

- Lens: leanness
- Location: `SKILL.md:14`
- Evidence: Règle de résolution : `{project-root}` → `le répertoire du projet`. C'est une tautologie — ne définit pas comment le modèle détermine ce répertoire.
- Recommendation: Remplacer par une règle actionnable : `{project-root}` → la racine du projet (par défaut le répertoire de travail courant).

#### enhancement-2 — ADD: Template de sortie texte précis

- Lens: enhancement
- Location: `SKILL.md:24-28`
- Evidence: Step 4 dit 'Produis un affichage structuré' avec des champs en bullet mais sans template précis. Différentes invocations LLM produiront des formats différents.
- Recommendation: Inclure un template de sortie exact dans un bloc de code pour que tous les agents émettent le même format visuel.

### Low (2)

#### leanness-2 — Cas de plusieurs phases actives non spécifié

- Lens: leanness
- Location: `SKILL.md:20`
- Evidence: Step 2: si deux phases ont le statut 'active', aucune règle de départage.
- Recommendation: Ajouter un départage : préférer 'active' avant 'in_progress', puis première dans l'ordre du document.

#### enhancement-3 — ADD: Dégradation pour entrée corrompue

- Lens: enhancement
- Location: `SKILL.md:18-22`
- Evidence: Steps 1 et 3 gèrent les fichiers manquants mais jamais le contenu corrompu ou non parseable.
- Recommendation: Ajouter un parse-guard : si le fichier existe mais ne peut pas être parsé, émettre un avertissement et continuer avec les données disponibles.
