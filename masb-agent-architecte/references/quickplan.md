---
name: quickplan
code: quickplan
description: Plan rapide en une page pour experts qui veulent sauter le processus complet
added: "2026-06-26"
type: capability
---

# quickplan

L'utilisateur veut un plan rapide, pas le processus complet. Produis un outline d'une page.

Le livrable est `{project-root}/masb-workspace/phases-index.md` avec 3-5 phases max, nommées et ordonnées. Pas de PRD, pas de spec par phase, pas de design system. Chaque phase a un nom et un objectif d'une ligne.

Consignes :
- Demande à l'utilisateur ce qu'il veut construire (une phrase)
- Décompose en 3-5 phases dans l'ordre logique
- Chaque phase a un nom (ex: "Auth Firebase") et un objectif (ex: "Inscription, connexion, gestion de session")
- Pas de détails, pas de spec
- Valide le plan d'une phrase : "Ça te va comme plan ?"
- Si l'utilisateur veut plus de détail sur une phase, redirige vers la capabilité `spec`

Le curseur : ne surcharge pas un quickplan avec des détails. Si l'utilisateur veut des détails, c'est qu'il veut le processus complet — propose de passer en mode standard.
