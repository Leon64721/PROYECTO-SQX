---
frente: GOBERNANZA
ia_ultima: Cursor
fecha: 2026-10-09
siguiente: Claude-Code
creditos_cursor_pct: 40
creditos_claude_pct: 0
creditos_baratos_pct: 10
bloqueo: false
---

# SESSION_HANDOFF — GOBERNANZA

Créditos de esta fase: **estimados** (no hay cupo numérico ni contador de producto).
Cursor ~40% (plan + artefactos). Baratos ~10% (agentes explore). Claude Code 0% hasta este brief.

## Brief para Claude Code (ejecutar solo esto)

Frente: GOBERNANZA
Objetivo: validar que el registry coincide con las skills en disco; no generar CFX ni tocar SQX vivo.
Skill principal: orchestrator + lectura de cada `SKILL.md` listado.
Skills excluidas: `sqx-strategy-project` en modo generar; cualquier Build/Retest.
Archivos a leer:
- `AGENTS.md`
- `SESSION_HANDOFF.md`
- `.claude/SKILLS_REGISTRY.md`
- `.claude/skills/*/SKILL.md` (las 6 filas del registry)
- `.claude/doctor.py` (existencia; no hace falta correrlo contra C: en este brief)
Archivos que se pueden modificar:
- este handoff
- `SESSION_HANDOFF.md` (índice)
Archivos que NO se tocan:
- `user/`
- `C:\SQX_144_Full`
- `.gitignore` (ya escrito en Cursor)
- cualquier `.cfx` / XML de bloques
Validación:
- Cada skill del registry tiene `SKILL.md` en la ruta dicha.
- No falta ninguna skill canónica conocida (project-organizer + 4 sqx-* + orchestrator).
- `catalog.json` no se commitea (sigue ignorado).
Resultado esperado: tabla skill / existe sí-no / nota. Luego cierre con métrica.
Siguiente IA: Cursor, solo si Claude Code encontró un hueco. Si todo OK, parar y esperar a Fabian (git commit pendiente de su OK).

## Hecho en Cursor (no repetir)

- `DECISION-LOG.md`, `AGENTS.md`, `IA_CREDITOS_Y_ROUTING.md`
- Handoffs maestro + 4 frentes
- `.cursor/rules/00-orchestrator.mdc`, `01-model-routing.mdc`
- `.claude/SKILLS_REGISTRY.md`, `.claude/skills/orchestrator/SKILL.md`
- `.gitignore` reforzado, informes FASE 0 movidos, `CFX_HASHES.md`
- Párrafo en `CLAUDE.md`, DECISIÓN-005, fila INDEX #38
- **No hay commit.** Fabian debe ver `git status` y autorizar.

## Cierre Claude Code (rellenar)

```
Cursor:      desconocido  — 40% (estimado, ya gastado en esta fase)
Claude Code: <n o desconocido>  — <pct>%
Baratos:     desconocido  — 10% (estimado, explore previo)
Notas:
```
