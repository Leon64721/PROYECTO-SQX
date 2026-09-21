# SUPERSEDIDO — no usar este análisis

Este archivo se escribió el 2026-09-14 a media tarde y afirmaba que la causa raíz de los 0
sobrevivientes en OOS era `<EntryRules use="false">` en el proyecto heredado. **Esa conclusión era
incorrecta**: esa sección pertenece a "Parts to improve", no a la generación; el Build siempre
generó 1.800 estrategias cuando el `.cfx` era un zip válido.

Las causas raíz reales (bloque ORB sin cablear, precisión Build≠OOS, umbral `AvgTrade` en $ vs
0.01 lotes), la evidencia y los fixes están en:

- `user\PropFirm_Management\24_incidente_orb_custom_project_otra_ia.md` (cronología completa)
- `user\PropFirm_Management\25_cierre_sesion_2026_09_14_orb.md` (método y checklist)
