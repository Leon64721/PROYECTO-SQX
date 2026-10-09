# DECISION-LOG — Orquestación IA y GitHub curado

Fecha: 2026-10-09
Frente: GOBERNANZA
Fuente: plan aprobado (v2) + confirmaciones de Fabian en sesión Cursor.

Este archivo registra decisiones. No sustituye a `AGENTS.md` (operativo) ni a `INDEX.md` (estado del proyecto SQX).

## P1–P5

| ID | Pregunta | Decisión | Quién / cuándo |
|---|---|---|---|
| P1 | Frente prioritario de esta fase | GOBERNANZA. No abrir CUSTOM_PROJECTS, QLIB_ONNX ni PROPFIRM en paralelo. | Fabian, 2026-10-09 (opción A previa = solo orquestador) |
| P2 | Sensibilidad de `.claude/skills/` | No hay credenciales, modelos ONNX ni datos de clientes. Publicable: `SKILL.md` + `engine/` + `doctor.py` / `sqx_common.py`. No publicar: `catalog.json` / `catalog.md` (bootstrap de máquina), `out/`, `.claude/settings.local.json`. | Auditoría solo lectura 2026-10-09 |
| P3 | Historial JAR / email ya público | B+C: no reescribir historial, no force push. Ignorar `*.jar` futuros. | Fabian, 2026-10-09 (respuesta "1") |
| P4 | Presupuesto de créditos | Política 40/40/20 sin cupo numérico fijo. Métrica obligatoria al cierre de turno. | Plan aprobado; Fabian no dio cupo X/Y/Z |
| P5 | Scope del repo público | Docs de gobernanza, skills (código), scripts `04_`, hubs MD de `02_`, `.cfx` chicos ya publicados. No: `user/` entero, databanks, logs, backtests masivos, catálogos de máquina, `settings.local.json`, `05_ARCHIVO` nuevo. | Fabian, repo público curado |

## Riesgos R1–R6

| ID | Decisión |
|---|---|
| R1 | Un frente por sesión. `MULTI_FRENTE` bloquea. |
| R2 | Cursor 40% / Claude Code 40% / subagentes baratos 20%. Si una capa se pasa, pausa y handoff. |
| R3 | Claude Code descubre skills por `SKILL.md`, no por `catalog.json`. Registry humano en `.claude/SKILLS_REGISTRY.md`. |
| R4 | Opción B: `user/` fuera de git. Historial de `.cfx` vigentes = `CFX_HASHES.md` (SHA256). No crear `user/.gitignore`. |
| R5 | `SESSION_HANDOFF.md` maestro + un archivo por frente. |
| R6 | `AGENTS.md` es la fuente de verdad. `.cursor/rules/*` y `.claude/skills/orchestrator/SKILL.md` son resúmenes. |

## Inventario `user/` (E:, no C:)

Recuperable vs crítico, sin inferir vigencia de estrategias más allá del catálogo del 2026-09-16.

| Qué | Clasificación | Acción GitHub |
|---|---|---|
| Gobernanza, skills, `04_`, hubs `02_` | Crítico y versionable fuera de `user/` | Sí (curado) |
| `user/extend/` (Java/Vue) | Crítico; vive también en `C:\SQX_144_Full` | No se sube (Opción B). No se copia a `02_` en esta fase. |
| `user/PropFirm_Management/INDEX.md` | Fuente de verdad operativa | No se dumpa `user/`. Se edita en local; el hub `02_PROYECTOS_ACTIVOS/propfirm_management/` ya está en el remoto. |
| `user/projects` (~17k `.sqx`) | Recuperable / output de minería | No se sube |
| `user/log`, staging, recovery | Regenerable / ruido | No se sube |
| `user/data` | En E: no existe. En C: ~25 GB | No mezclar |

## Historial de cambios de este log

- 2026-10-09 — creación. Decisiones de la sesión Cursor que aprobó el plan v2.
