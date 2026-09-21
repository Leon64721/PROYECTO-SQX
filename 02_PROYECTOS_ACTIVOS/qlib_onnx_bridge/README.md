# Proyecto activo: Agente de Trading ML (Qlib → ONNX → SQX)

Puente entre un modelo de machine learning entrenado en Qlib (Python) y StrategyQuant X, vía
ONNX Runtime embebido como indicador nativo de Builder (`QlibSignal`). Ver el diseño completo en
[user\Qlib_ONNX_Bridge_Design.md](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/Qlib_ONNX_Bridge_Design.md)
y el estado en
[user\PropFirm_Management\INDEX.md](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/INDEX.md)
(ítems 15 y 18).

## Contenido de esta carpeta

- [qlib_export\](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/02_PROYECTOS_ACTIVOS/qlib_onnx_bridge/qlib_export) —
  lado Python: `train_export.py` (entrena y exporta a ONNX), `export_golden_values.py` /
  `compare_golden_values.py` (gate de paridad Java/Python), `export_sqx_price_parity.py`,
  `prepare_real_data.py`. Salidas en `qlib_export\output\` (`model.onnx`, `feature_spec.json`,
  `golden_values.csv`, `java_predictions.csv`, `ndxm_qlib.csv`).

El lado Java (`QlibSignal.java`, `OnnxModelManager.java`) vive en `user\extend\Snippets\SQ\` por
regla de taxonomía (código que SQX compila en vivo) — no se duplica aquí, solo se referencia
desde el diseño de arriba.

## Estado (ver ítem 18 del INDEX)

`(QS) Qlib Signal` ya aparece como bloque nativo en Builder → Building blocks → Indicators
(confirmado tras Compile All). Gate JNI en verde (500 outputs finitos, 0 centinelas, paridad
Java/Python exacta). **Pendiente**: validar contra precios SQX reales antes de pasar a búsqueda
genética (GA) real.

## Dónde aplican las skills `sqx-lab` en este frente

`QlibSignal` ya es un bloque nativo disponible — pero hoy nadie lo usa dentro de una estrategia
real de Builder. Las 4 skills instaladas en `.claude\skills\` (ver
[ítem 29](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/PropFirm_Management/29_sqx_lab_authoring_toolkit.md))
son el camino directo para cerrar ese ciclo "modelo entrenado → estrategia minable":

1. **`sqx-custom-block`** — envolver `QlibSignal` en Condition blocks útiles para el Builder
   (ej. "QlibSignal cruza por encima de un umbral", "QlibSignal está en su percentil superior")
   en vez de dejarlo como indicador crudo.
2. **`sqx-random-group`** — agrupar esos Condition blocks en un pool que el Builder pueda
   combinar genéticamente con reglas normales (mismo patrón que las 424 reglas / 162 atoms ya
   detectados en el catálogo bootstrapeado de este install).
3. **`sqx-strategy-template`** — diseñar una plantilla `.sqx` donde `QlibSignal` sea el
   filtro/trigger principal, con salida (stop/target) ligada a un grupo de Price-level.
4. **`sqx-strategy-project`** — clonar un proyecto donor real (el catálogo ya detectó 6:
   `Builder`, `GBPJPY_nico66fxPRO_V2`, `Optimizer`, `PortfolioComposer`, `PortfolioMaster`,
   `Retester`) y wirear la plantilla como build task, con la validación de precios reales del
   pendiente del ítem 18 como paso previo obligatorio antes de correr el build completo.

Este mismo flujo se cruza con el proyecto
[propfirm_management](/E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/02_PROYECTOS_ACTIVOS/propfirm_management/README.md):
una plantilla que combine `QlibSignal` + reglas de fondeo como gate obligatorio unifica ambos
frentes en un solo `project.cfx`.

## Historial de versiones

- 2026-09-16 — Creado README de proyecto activo (antes esta carpeta no tenía documentación
  propia), a pedido del usuario al pedir aplicar las skills `sqx-lab` a todo el proyecto, no
  solo a ORB.
