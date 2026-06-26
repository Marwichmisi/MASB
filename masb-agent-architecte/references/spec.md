---
name: spec
code: spec
description: Rédaction de la spec d'une phase à son activation
added: "2026-06-26"
type: capability
---

# spec

Rédige la spec d'une phase UNIQUEMENT au moment de son activation. N'écris jamais les specs de toutes les phases d'un coup.

Le livrable est `{project-root}/masb-workspace/phases/NN-nom/spec.md`.

Le consommateur est Research, UI/UX et le Développeur — aucun n'était dans la conversation. La spec doit être autonome.

Couvre : objectif (une phrase), contexte (pourquoi cette phase existe), entrées disponibles, livrables attendus, définition de fait (comment on sait que c'est fini), dépendances, notes techniques, et questions ouvertes.

Le curseur : une spec qui laisse de l'ambiguïté sur le "fini" est une spec ratée. Si le Développeur n'a pas assez de contexte pour coder sans recrosser l'utilisateur, la spec est trop vague.

Ajoute la spec validée dans `phases-index.md` (statut: `ready`).
