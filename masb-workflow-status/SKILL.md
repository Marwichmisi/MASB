---
name: masb-workflow-status
description: Affiche l'état d'avancement du projet MASB. Utilisez quand l'utilisateur dit 'masb status' ou demande où on en est dans le projet.
---

# masb-workflow-status

## Overview

Ce workflow affiche l'état d'avancement du projet Android MASB. Il lit `phases-index.md` et le `progress.md` de la phase active pour produire un résumé lisible. L'utilisateur sait exactement où on en est et quoi faire ensuite.

## Resolution rules

- `{project-root}` → la racine du projet (par défaut le répertoire de travail courant).
- `{skill-root}` → le répertoire d'installation de ce skill.

## On Activation

1. **Détecter la phase active.** Exécute `uv run {skill-root}/scripts/active-phase.py {project-root}`. Le script retourne un JSON avec la phase active, son statut, et la liste des phases complétées. Si `status` est `no_project`, affiche qu'aucun projet MASB n'est initialisé et termine. Si `status` est `all_done`, affiche que le projet est terminé.

2. **Charger le progress de la phase active.** Si une phase active est détectée, lis `{project-root}/masb-workspace/phases/{active_phase}/progress.md`. S'il n'existe pas ou si le contenu est invalide, la phase n'a pas encore commencé.

3. **Afficher le statut.** Si le flag `--json` est présent, émet un objet JSON structuré :
   ```json
   {
     "phase": "<nom>",
     "status": "<statut>",
     "next_action": "<prochaine action>",
     "blockers": ["review"|"tests"|null],
     "completed_phases": ["<phase1>", "<phase2>"]
   }
   ```

   Sinon, produit un affichage formaté selon ce gabarit :

   ```
   ── MASB Status ──────────────────────
    Phase courante : <nom> (<statut>)
    Prochaine action : <action>
    Blocages : <review|tests|aucun>
    Phases complétées : <liste>
   ────────────────────────────────────
   ```
