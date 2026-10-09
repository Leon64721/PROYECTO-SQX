# AGENTS.md — fuente única de orquestación

**Este archivo es la fuente de verdad** para Cursor y Claude Code.
Cambios aquí primero. Después se propagan a:

- `.cursor/rules/00-orchestrator.mdc`
- `.cursor/rules/01-model-routing.mdc`
- `.claude/skills/orchestrator/SKILL.md`

No pegar el Plan Maestro ni el INDEX completo en un chat. Leer este archivo + el handoff del frente activo + **un** archivo de verdad (INDEX o README del frente).

## Pregunta 0 (obligatoria)

Si el usuario no deja claro el frente, preguntar **uno**:

1. `CUSTOM_PROJECTS` — Custom Projects clásicos / ORB / NDXm / cadena de robustez
2. `QLIB_ONNX` — Qlib → ONNX → `QlibSignal`
3. `PROPFIRM` — compliance Java/Vue, noticias, dashboards
4. `GOBERNANZA` — orquestador, créditos, git, catálogo, skills

`MULTI_FRENTE` o "los dos a la vez" → **bloquear**. Pedir que elija uno. Un frente por sesión.

Esta sesión (2026-10-09) está en **GOBERNANZA** hasta que el usuario cambie.

## Roles

| Rol | Puede | No puede |
|---|---|---|
| **Router** | Clasificar frente, elegir skill, pedir 1 dato, bloquear mezcla | Crear bloques, `.cfx`, editar código de negocio |
| **Orquestador** | Brief de 15–25 líneas (objetivo, archivos, skill, validación, qué no tocar) | Implementar el brief |
| **Ejecutor** | Aplicar el brief | Cambiar el alcance |
| **Auditor** | Verificar contra el brief | Rediseñar |

El modelo capaz de la sesión hace Router + Orquestador + Auditor (corto).
La ejecución cara de SQX va a **Claude Code**. Grep/edits mecánicos van a **subagentes baratos**.

## Brief (formato)

```
Frente:
Objetivo:
Skill principal:
Skills excluidas:
Archivos a leer:
Archivos que se pueden modificar:
Archivos que NO se tocan:
Validación:
Resultado esperado:
Siguiente IA:
```

## Handoffs

- `SESSION_HANDOFF.md` — índice de frentes
- `SESSION_HANDOFF-GOBERNANZA.md`
- `SESSION_HANDOFF-CUSTOM_PROJECTS.md`
- `SESSION_HANDOFF-QLIB_ONNX.md`
- `SESSION_HANDOFF-PROPFIRM.md`

Al abrir: leer el maestro, luego **solo** el archivo del frente de hoy.
Al cerrar: actualizar maestro + frente + métrica de créditos (ver `01_BIBLIOTECA_CONOCIMIENTO/00_GOBERNANZA_SKILLS/IA_CREDITOS_Y_ROUTING.md`).

Cada handoff de frente empieza con YAML (campos: `frente`, `ia_ultima`, `fecha`, `siguiente`, `creditos_cursor_pct`, `creditos_claude_pct`, `creditos_baratos_pct`, `bloqueo`).

## Qué no tocar sin orden explícita

- `user/` (espejo SQX; `project-organizer` nunca lo mueve)
- `C:\SQX_144_Full` (instalación viva)
- `user/data`, `user/log`, `user/projects` masivos
- Bases limpias de Custom Project (DECISIÓN-004)
- Mezclar un frente de negocio con otro

## Git (repo público)

Remoto: https://github.com/Leon64721/PROYECTO-SQX
Antes de `git add`: leer `.gitignore`. **Prohibido** `git add .`.
No commit ni push sin confirmación de Fabian.
No force push / filter-repo (DECISIÓN P3).

## Skills canónicas

Lista humana: `.claude/SKILLS_REGISTRY.md`
Código: `.claude/skills/*/SKILL.md` + `engine/`
`catalog.json` es de esta máquina; no se commitea.

## Créditos

Cursor 40% (plan / brief / auditoría) · Claude Code 40% (ejecución + skills SQX) · subagentes baratos 20% (grep / editar / validar).
Detalle: `IA_CREDITOS_Y_ROUTING.md`.
