---
name: brainstorm
code: brainstorm
description: Session interactive pour comprendre la vision du projet
added: "2026-06-26"
type: capability
---

# brainstorm

Ouvre le dialogue avec une invitation large. Laisse ton propriétaire déverser tout ce qu'il a en tête avant de poser une question structurée. Ne l'interromps pas pour sauvegarder — capture en mémoire et écris dans `brainstorm.md` uniquement aux pauses naturelles (silence, changement de sujet, question de l'utilisateur).

Valide que le projet est Android avant d'aller plus loin. Si ce n'est pas le cas, préviens que l'agent est calibré pour Android.

Le livrable est `{project-root}/masb-workspace/brainstorm.md` : un document brut qui capture les idées, features souhaitées, contraintes techniques, et la vision globale. Le consommateur est tout agent MASB qui n'était pas dans la conversation — le document doit être autonome.

Si l'utilisateur n'a pas de vision claire ("je veux construire quelque chose pour les musiciens"), bascule en mode idéation divergente avant toute question structurée.

Le curseur : ne laisse aucune zone d'ombre. Une feature évoquée mais pas clarifiée est un risque.
