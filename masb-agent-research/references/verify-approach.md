---
name: verify-approach
code: verify-approach
description: Vérifie la conformité d'une approche selon les skills officiels Android
added: "2026-06-26"
type: capability
---

# verify-approach

Tu peux être sollicité à tout moment pour vérifier qu'une approche technique est conforme aux recommandations officielles. Reçois une description de l'approche proposée. Consulte les skills Android concernés et vérifie :
- L'API ou le pattern existe bien dans la documentation officielle
- Il n'y a pas de dépréciation ou d'alternative plus récente
- Les bonnes pratiques du skill sont respectées
- Aucun anti-pattern connu n'est utilisé

Produis un rapport de conformité : `{project-root}/masb-workspace/phases/N/research/conformity-report.md` avec :
- ✅ Approche valide (si conforme)
- ⚠️ Alertes (si points d'attention)
- ❌ Non conforme (si l'approche viole les recommandations, avec la référence précise)
