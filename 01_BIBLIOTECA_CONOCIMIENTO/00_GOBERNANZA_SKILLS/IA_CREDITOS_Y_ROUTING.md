# Política de créditos y routing

Fuente operativa de roles: `AGENTS.md`. Este archivo solo define **quién gasta** y **cuánto**.

No hay cupo numérico fijo (P4). Se mide en **porcentaje del turno de fase**, no en "turno impar/par ciego".

## Reparto objetivo

| Capa | Techo | Qué hace | Dónde |
|---|---|---|---|
| Cursor (orquestador) | 40% | Clasificar, brief, auditoría de alcance, commit/docs cuando toca | Esta sesión / modelo capaz |
| Claude Code | 40% | Ejecutar brief: skills `sqx-*`, `doctor.py`, `validate.py` | CLI Claude Code |
| Subagentes baratos | 20% | Grep, leer, tamaños, edits mecánicos, `git status` | `composer-2.5-fast` u homólogo |

Si una capa supera su techo: **pausa**, actualiza handoff, continúa la otra IA. No abrir otro turno del mismo lado "para terminar".

## Métrica de cierre (obligatoria)

Copiar al handoff del frente y al maestro:

```
Cursor:      <n> (estimación o "desconocido")  — <pct>%
Claude Code: <n>                               — <pct>%
Baratos:     <n>                               — <pct>%
Notas:
```

Si no hay número de créditos del producto, escribir `desconocido` y el porcentaje **estimado** del trabajo de la fase (no inventar un saldo). Decir que es estimado.

## Routing de tareas

Ver también `.cursor/rules/01-model-routing.mdc`.

| Tarea | Capa |
|---|---|
| Clasificar frente / brief / cambiar alcance | Cursor orquestador |
| Explorar repo / grep / tamaños | Barato |
| Editar docs / rules / gitignore | Barato o Cursor barato |
| Authoring SQX (block → group → template → project) | Claude Code |
| `doctor.py` / `validate.py` de skills | Claude Code |
| Análisis databank / scripts `04_` | Claude Code o barato según el brief |
| `git status` / catálogo `project-organizer` | Barato |
| Auditoría "¿se cumplió el brief?" | Cursor orquestador (corto) |
| Build / Retest en SQX real | Bloqueado en frente GOBERNANZA |

## Alternancia Cursor ↔ Claude Code

1. Cursor cierra con brief en `SESSION_HANDOFF-<FRENTE>.md`.
2. Claude Code abre **solo** AGENTS.md + maestro + ese frente. No re-estudia el repo.
3. Claude Code cierra actualizando el mismo handoff.
4. Si Cursor agotó >40% en la fase, Claude Code no le devuelve trabajo de orquestación; deja el siguiente paso escrito.
