---
name: validate
code: validate
description: Vérification de cohérence cross-phase
added: "2026-06-26"
type: capability
---

# validate

Vérifie la cohérence entre tous les artefacts du projet.

Lit `brainstorm.md`, `prd.md`, `phases-index.md`, et toutes les `spec.md` des phases. Produis un rapport listant :

- Features du PRD non couvertes par les specs de phase
- Phases sans spec rédigée mais marquées `ready`
- Dépendances entre phases qui pointent vers une phase inexistante
- Phases orphelines (sans dépendance et sans feature associée)
- Specs dont la définition de fait est absente ou trop vague

Le livrable est un résumé concis : soit "Tout est cohérent" soit la liste des incohérences.

Le curseur : ne propose pas de correctifs — signale seulement. L'utilisateur ou l'Architecte décide quoi faire.
