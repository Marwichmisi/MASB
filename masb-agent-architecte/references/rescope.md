---
name: rescope
code: rescope
description: Pivot complet du projet — archive le plan actuel et recommence le brainstorming
added: "2026-06-26"
type: capability
---

# rescope

L'utilisateur change complètement de direction. Archive le plan actuel et recommence.

Archive :
1. Renomme `{project-root}/masb-workspace/phases-index.md` en `phases-index.archive.YYYY-MM-DD.md`
2. Déplace les dossiers de phases dans `{project-root}/masb-workspace/archives/YYYY-MM-DD/`
3. Réinitialise les statuts de toutes les phases

Préserve le contexte de l'utilisateur dans MEMORY.md (préférences, style de travail, expertise).

Puis lance un nouveau cycle `brainstorm` → découverte fraîche.

Le curseur : ne confonds pas rescope (pivot complet) avec replan (re-découpage d'une phase). Demande confirmation avant d'archiver.
