---
name: decompose
code: decompose
description: Découpage du projet en phases autonomes
added: "2026-06-26"
type: capability
---

# decompose

À partir de `brainstorm.md` et `prd.md`, produis la structure complète du projet.

Le livrable principal est `{project-root}/masb-workspace/phases-index.md` qui liste toutes les phases avec nom, statut et ordre. Crée les dossiers `{project-root}/masb-workspace/phases/NN-nom-de-phase/`.

Conventions de décomposition : chaque phase produit un livrable concret, les phases sont ordonnées par dépendance (les indépendantes sont marquées `parallel: true`), la phase 00 est toujours le design system (sauf projet simple — dans ce cas, une phase unique sans PRD ni design system), chaque dossier de phase suit la structure `spec.md` + `research/` + `code/` + `review-report.md` + `test-report.md` + `progress.md`, et le nom des dossiers suit `NN-description-courte`.

Jauge la taille du projet : une phase qui dure plus d'une session est trop grosse. Recoupe. Une phase qui chevauche une autre est mal délimitée. Redessine.

Présente la décomposition à ton propriétaire avant d'écrire le moindre fichier. Valide chaque phase : nom, objectif, dépendances, ordre.
