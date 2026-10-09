# SKILLS_REGISTRY

Índice humano. Claude Code descubre skills por `.claude/skills/*/SKILL.md`, no por `catalog.json`.
`catalog.json` / `catalog.md` son bootstrap contra `C:\SQX_144_Full` (por máquina; no commitear).

| Skill | Ruta | Qué hace | Cuándo usarla | No usar para |
|---|---|---|---|---|
| orchestrator | `.claude/skills/orchestrator/SKILL.md` | Resumen: leer AGENTS.md + handoff | Toda sesión Claude Code | Sustituir AGENTS.md |
| project-organizer | `.claude/skills/project-organizer/SKILL.md` | Taxonomía 01–05 + catálogo de contenido | Raíz sucia, clasificar artefactos, cierre de sesión | Mover `user/` |
| sqx-custom-block | `.claude/skills/sqx-custom-block/SKILL.md` | Condition / Price level → XML AlgoWizard | Nueva regla de trading validada | Custom Project `.cfx` completo |
| sqx-random-group | `.claude/skills/sqx-random-group/SKILL.md` | Pools / menús de bloques | Agrupar bloques ya validados | Inventar bloques |
| sqx-strategy-template | `.claude/skills/sqx-strategy-template/SKILL.md` | Plantilla `.sqx` (incl. MTF) | Tras grupos existentes | Saltar validación de bloques |
| sqx-strategy-project | `.claude/skills/sqx-strategy-project/SKILL.md` | Clonar / cablear `project.cfx` | Tras template validado | Parchear bases limpias in-place |

Utilidades (no son skills): `.claude/doctor.py`, `.claude/sqx_common.py`.

Legacy (no canónico): copias en `01_BIBLIOTECA_CONOCIMIENTO/skills_sqx/`. No ejecutar desde ahí.
