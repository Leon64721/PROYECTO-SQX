# Proyecto activo: Prop Firm / Cuentas de Fondeo

Este archivo es un **hub/índice** — no contiene el código en sí. El código funcional de este
frente de trabajo vive intencionalmente dentro de `user\` (espejo exacto de la instalación real
de SQX, nunca se toca ni se mueve, por regla de la taxonomía del proyecto — ver
[project-organizer](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/.claude/skills/project-organizer)).
Esta carpeta existe solo para que el tema tenga la misma visibilidad como "proyecto activo" que
ya tienen [orb_custom_project](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/02_PROYECTOS_ACTIVOS/orb_custom_project)
y [qlib_onnx_bridge](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/02_PROYECTOS_ACTIVOS/qlib_onnx_bridge).

## Qué es este proyecto

Todo lo relacionado con hacer que las estrategias generadas por SQX cumplan las reglas de
cuentas de fondeo (prop firm) — Apex, LucidPro, TPT PRO, etc. — y con visualizar/validar ese
cumplimiento desde dashboards propios dentro de SQX.

## Mapa de componentes (todo vive bajo `user\`, solo referenciado aquí)

### 1. Dashboards HTML/Vue — `user\extend\ResultsPlugins\`

Plugins de resultados custom (Vue 3 + HTML, cargados por SQX directamente en su UI):

| Carpeta | Título interno | Propósito |
|---|---|---|
| [ProjectHub](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/extend/ResultsPlugins/ProjectHub/index.html) | "StrategyQuant Project Hub" | Menú central de navegación del proyecto, embebido dentro de SQX |
| [Prop analytics](</E:/PROYECTOS/CLAUDE CODE/STRATEGY QUANT/user/extend/ResultsPlugins/Prop analytics/index.html>) | "PropAnalytics" | Dashboard de análisis de estrategias bajo métricas de prop firm (i18n con `locales\`) |
| [Prop Monte Carlo](</E:/PROYECTOS/CLAUDE CODE/STRATEGY QUANT/user/extend/ResultsPlugins/Prop Monte Carlo/index.html>) | "Prop Monte Carlo" | Visualización de resultados de Monte Carlo aplicados a reglas de fondeo |
| [PropFirmValidator](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/extend/ResultsPlugins/PropFirmValidator/index.html) | "Prop Firm Validator" | Validador visual de si una estrategia cumple las reglas de una prop firm específica |
| [CustomPlugin](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/extend/ResultsPlugins/CustomPlugin/index.html) | "Plugin Template" | Plantilla/guía genérica para crear nuevos ResultsPlugins (no es de prop firm, es la base que se usó para construir los otros) |

Nota: `PropFirmValidator\index.html.bak` es un backup previo, no borrar sin confirmar con el
usuario (regla de `project-organizer`: nunca borrar automáticamente).

### 2. Lógica de compliance (Java) — `user\extend\Snippets\SQ\`

Existe **duplicada** en dos paquetes (`Columns\Databanks\` y `Conditions\PropFirm\`, mismos 20
nombres de archivo en ambos) — pendiente de investigar si es intencional (dos puntos de
extensión distintos de la API de SQX que reusan la misma lógica) o redundancia real a limpiar:

- `PropFirmComplianceLogic.java`, `PropFirmScore.java`, `NewsCalendar.java` — motor genérico.
- Un par `_Eval_50k.java` / `_Funded_50k.java` (+ su `_Reason.java` explicativo) por cada prop
  firm soportada: **Apex**, **LucidPro**, **TPT PRO/Test**.
- `PropFirm_DEBUG_*.java` — columnas de diagnóstico (dump de orders, MC manipulation stats,
  news violations, worst daily DD/equity).

Config asociada: `user\extend\CustomAnalysis\PropFirmProfiles.json`,
`NewsCalendarProfiles.json`, `economic_events_calendar.NOTES.md`.

### 3. Bitácora / fuente de verdad — `user\PropFirm_Management\`

[INDEX.md](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/INDEX.md) — 29
ítems documentados (planes, hallazgos, incidentes). Sigue siendo la fuente de verdad de qué está
hecho/pendiente; este README no la reemplaza, solo la hace más fácil de encontrar.

## Pendientes activos ahora mismo (extraídos del INDEX.md, 2026-09-16)

| Ítem | Qué falta | Bloqueo |
|---|---|---|
| [#2](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/02_custom_project_builder_level.md) — Custom Project / Builder-level (reglas de firma desde generación) | **En progreso** — primer bloque generado y validado ([ítem 31](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/31_ny_session_builder_block.md): sesión NY DST-aware para NDXm); falta importar en AlgoWizard y probar en build real | Ninguno técnico |
| [#3](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/03_capa5_montecarlo_manipulation.md) — Capa 5 Monte Carlo Manipulation Pass Rate | Diseño listo, falta compilar y correr Retest con Cross Checks | Requiere acción del usuario en SQX real |
| [#11](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/11_capa2_restriccion_noticias.md) — Restricción de noticias (TPT PRO Funded) | Bug de rollover/zona horaria sin resolver (ver `TODOS.md`); bloquea activar `newsRestrictionActive=true` | Requiere decidir cómo modelar el rollover real por prop firm (falta parámetro de offset de sesión) |
| [#18](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/18_qlibsignal_registro_builder_2026_08_16.md) — QlibSignal en Builder | Validar contra precios SQX reales antes de GA | Comparte frente con `qlib_onnx_bridge` |
| [#19](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/19_ndxm_custom_projects_multibroker_costos.md) — Multi-broker costos | Repetir con Tickmill real | Requiere que el usuario tenga esa terminal MT5 logueada |

## Dónde aplican las skills `sqx-lab` en este frente

Las 4 skills instaladas en `.claude\skills\` ([ítem 29](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/29_sqx_lab_authoring_toolkit.md))
encajan directamente con el pendiente **#2** de arriba, que lleva desde 2026-08-02 sin iniciar
por falta de tiempo/API — es exactamente lo que el toolkit automatiza:

1. **`sqx-custom-block`** — convertir las restricciones de una prop firm (ej. "no operar 2
   minutos antes/después de noticias de alto impacto", "no abrir posición fuera de la sesión de
   Nueva York") en **Condition blocks** nativos de AlgoWizard, en vez de solo lógica Java de
   post-análisis. Esto movería el control de "antes de generar" (Builder-level) a diferencia del
   enfoque actual que solo mide cumplimiento *después* de generar (Columns/Conditions Java).
2. **`sqx-random-group`** — agrupar esos bloques en un pool ("reglas compatibles con fondeo")
   que el Builder pueda muestrear junto a las reglas normales de la estrategia.
3. **`sqx-strategy-template`** — generar plantillas que combinen una señal de entrada (por
   ejemplo `QlibSignal`, el bloque ML ya registrado en Builder) con esas reglas de fondeo como
   filtro obligatorio.
4. **`sqx-strategy-project`** — clonar uno de los 6 proyectos base ya detectados en el catálogo
   (`Builder`, `GBPJPY_nico66fxPRO_V2`, etc.) y wirear la plantilla anterior como build task,
   cerrando el ciclo: **regla de fondeo → grupo → plantilla → project.cfx ejecutable**.

Esto también conecta directamente con **qlib_onnx_bridge**: una plantilla de
`sqx-strategy-template` puede usar `QlibSignal` como trigger/filtro y las reglas de prop firm
como gate — unificando ambos frentes de trabajo en un solo project.cfx.

## Historial de versiones

- 2026-09-16 — Creado como hub índice, a pedido del usuario tras notar que el tema "prop firm /
  cuentas de fondeo" no aparecía como proyecto activo tras la reorganización estructural
  (ítem 27). No se movió ni copió ningún archivo de `user\` — solo se documentan y enlazan.
