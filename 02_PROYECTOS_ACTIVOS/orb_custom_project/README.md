# Proyecto activo: ORB Custom Project

Custom Project multi-temporal (Opening Range Breakout, M15 + H1) sobre `BASE_CP_MASTER_CLEAN_V1`.
Ver bitácora completa en
[user\PropFirm_Management\INDEX.md](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/INDEX.md)
ítems 23-25 (incidentes, causas raíz, fixes V2-V8) y
[24_ANALISIS_PROFUNDO_CORRIDA_FALLIDAS.md](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/02_PROYECTOS_ACTIVOS/orb_custom_project/24_ANALISIS_PROFUNDO_CORRIDA_FALLIDAS.md)
en esta misma carpeta.

## Estado (ver ítem 25 del INDEX)

Pipeline `V8` (`BASE_CP_MASTER_CLEAN_V1_ORB_V5_MAXTRADES2.cfx`) llegó a **541/1800** estrategias
pasando OOS tras corregir 3 causas raíz apiladas (bloque ORB sin cablear, precisión
Build≠OOS, umbral `AvgTrade` en $ vs lotes de 0.01). **Sigue abierto**: el freno "misma barra"
(732 estrategias descartadas, insensible al Stop Loss) — pendiente verificar contra `orders.bin`
antes de tocar nada más. Pipeline V8 quedó sin terminar de correr al cierre de esa sesión.

## Dónde aplican las skills `sqx-lab` en este frente

Este proyecto se construyó a mano (parcheando `.cfx` directamente con scripts Python
ad-hoc: `fix_orb_window_v2.py`, `fix_orb_oos_threshold_v4.py`, etc.) porque en ese momento no
existía todavía el toolkit oficial. Las 4 skills instaladas en `.claude\skills\` (ver
[ítem 29](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/29_sqx_lab_authoring_toolkit.md))
son relevantes para el trabajo que falta, no para rehacer lo ya corregido:

1. **`sqx-custom-block`** — si el freno "misma barra" resulta ser un problema de guard de
   re-entrada mal expresado (hipótesis abierta del ítem 25), se puede reautorizar el bloque ORB
   de entrada con un guard explícito (ej. "no reentrar si ya hay una orden abierta en esta
   sesión") como Condition block validado, en vez de parchear XML a mano.
2. **`sqx-strategy-template`** — si se decide iterar una v9/v10 del ORB, esta skill genera la
   plantilla desde un skeleton ya build-confirmado (en vez de seguir mutando el `.cfx` original
   con scripts uno-a-uno), reduciendo el riesgo de repetir el patrón de bugs apilados de V2-V7.
3. **`sqx-strategy-project`** — para clonar este proyecto como base de una v9 experimental sin
   arriesgar el `V8` que ya corrió parcialmente, wireando la plantilla corregida como nueva
   build task sobre uno de los proyectos donor detectados en el catálogo.

No se recomienda tocar los `.cfx` `_V4`...`_V8` existentes con las skills nuevas — son
artefactos ya validados en ejecución real; el toolkit aplica hacia adelante (v9+) o para el
freno "misma barra" si se confirma que es un problema de reglas, no de configuración.

## Historial de versiones

- 2026-09-16 — Creado README de proyecto activo (antes esta carpeta no tenía documentación
  propia), a pedido del usuario al pedir aplicar las skills `sqx-lab` a todo el proyecto.
