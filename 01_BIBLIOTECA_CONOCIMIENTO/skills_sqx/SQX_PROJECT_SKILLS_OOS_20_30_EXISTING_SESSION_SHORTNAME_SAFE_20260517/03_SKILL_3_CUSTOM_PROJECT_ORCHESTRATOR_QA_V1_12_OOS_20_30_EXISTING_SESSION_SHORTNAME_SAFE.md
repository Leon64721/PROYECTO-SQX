# Skill 3 Final Operativa V1.11 — Custom Project Orchestrator QA, Resource Safe, DataBank Chain, Symbol Resource Exact e Import Smoke Test SQX

**Proyecto:** StrategyQuant X / Custom Project `.cfx`  
**Versión:** V1.10 Consolidada con Multi-Timeframe Quality Gate y OOS 20–30  
**Estado:** reemplaza la Skill 3 V1.6, V1.5, V1.4, V1.3, V1.2, V1.1 y todos los patches separados de Skill 3.  
**Función:** orquestar, generar, corregir, auditar y entregar Custom Projects `.cfx` completos para SQX, integrando diseño Builder, robustez por etapas, OOS Split correcto, ranking hardness, recursos internos compatibles, cadena real de Data Banks, auditoría de símbolos contra Data Manager y prueba de humo manual de importación.

---

## 0. Qué archivo reemplaza esta Skill

Esta Skill reemplaza y absorbe:

```text
SKILL_3_FINAL_CUSTOM_PROJECT_ORCHESTRATOR_QA_REPORTE_SQX.md
SKILL_3_FINAL_CUSTOM_PROJECT_ORCHESTRATOR_QA_REPORTE_SQX_V1_1_AUDITORIA_ESTRICTA.md
SKILL_3_FINAL_CUSTOM_PROJECT_ORCHESTRATOR_QA_REPORTE_SQX_V1_2_OOS_SPLIT_AUDITORIA_ESTRICTA.md
SKILL_3_FINAL_CUSTOM_PROJECT_ORCHESTRATOR_QA_REPORTE_SQX_V1_3_OOS_SPLIT_AUDITORIA_RANKING_HARDNESS.md
SKILL_3_FINAL_CUSTOM_PROJECT_ORCHESTRATOR_QA_REPORTE_SQX_V1_4_RESOURCE_DATABANK_SAFE.md
PATCH_SKILL_3_CONFIGURACION_TOTAL_CUSTOM_PROJECT.md
PATCH_SKILL_3_QA_PRE_ENTREGA_Y_DATA_OBLIGATORIA.md
PATCH_SKILL_REPORTE_MINUCIOSO_CUSTOM_PROJECT_SQX.md
PATCH_SKILL_3_AUDITORIA_ESTRICTA_ANTI_RESIDUOS_SQX.md
```

No cargar esos archivos por separado si esta Skill V1.6 está cargada.

---

## 1. Principio rector

Un Custom Project `.cfx` no es entregable operativo si solo se modifica una etapa aislada, una fecha, un símbolo, un filtro o la pantalla principal visible en SQX.

Todo Custom Project debe quedar configurado, auditado y reportado de punta a punta:

```text
Builder
→ OOS
→ MC_TRADES
→ MC_SPREAD_SLIPPAGE
→ TICK
→ SPP
→ WFA MATRIX
→ Auditoría global anti-residuos
→ Auditoría de cadena real de Data Banks
→ Auditoría de símbolos contra Data Manager
→ Auditoría de recursos internos SQX
→ Prueba de humo de importación
→ Reporte minucioso
→ Entrega final
```

Regla crítica:

```text
Archivo sin auditoría global = archivo no entregable.
Archivo con residuos = archivo no entregable.
Archivo sin matriz esperado vs detectado = archivo no entregable.
Archivo sin reporte de cambios = archivo no entregable.
Archivo con OOS Global Period limitado solo a la ventana OOS sin orden explícita = archivo no entregable.
Archivo con Data Bank chain incorrecta = archivo no entregable.
Archivo con símbolo/source/precision/broker inconsistente con Data Manager = archivo no entregable.
Archivo con recursos internos incompatibles = archivo no entregable.
```

---

## 2. Jerarquía de decisión

Cuando existan conflictos entre reglas:

```text
1. Orden explícita actual del usuario.
2. Restricciones y nodos protegidos.
3. Reglas de bloqueo técnico / QA.
4. Diagnóstico de data y régimen.
5. Skill 1 Builder.
6. Skill 2 Robustez.
7. Presets o defaults del sistema.
```

Prohibido justificar una configuración con:

```text
porque la skill lo dice
porque venía por defecto
porque estaba en la plantilla
```

Cada decisión debe tener argumento técnico.

---

## 3. Inputs obligatorios para Custom Project final

```text
1. Base custodiada o .cfx base autorizado.
2. Data diaria D1 del activo.
3. Nombre exacto del símbolo normal interno en SQX.
4. Nombre exacto del símbolo tick interno en SQX, si habrá TICK.
5. Rango disponible de data normal.
6. Rango disponible de data tick.
7. Source real del símbolo normal según Data Manager.
8. Source real del símbolo tick según Data Manager.
9. Precision real del símbolo normal: M1, H1, etc.
10. Precision real del símbolo tick: TICK.
11. Broker id / broker profile / instrumento.
12. Underlying symbol real: uSymbol / uSymbolName.
13. Broker.
14. Tipo de cuenta.
15. Objetivo operativo.
16. Número de edges / Custom Projects.
17. Restricciones explícitas.
18. Confirmación de CrossChecks solicitados o prohibidos.
19. Configuración de instrumento/costos si el usuario autoriza modificar nodos protegidos.
```

Si falta un input crítico:

```text
REQUIERE CONFIRMACIÓN
```

---

## 4. Data diaria y diagnóstico de régimen

No crear edges definitivos sin data diaria.

```text
SIN DATA DIARIA DEL ACTIVO → NO HAY EDGES DEFINITIVOS.
SIN DIAGNÓSTICO DE RÉGIMEN → NO HAY CUSTOM PROJECT FINAL.
```

La data diaria se usa para:

```text
- Diagnóstico de régimen.
- Selección de timeframe.
- Selección de ventanas Builder/IS y OOS.
- Selección de edges.
- Dirección: long, short o both.
- Justificación del diseño.
```

---

## 5. Configuración total obligatoria

Antes de entregar, revisar, configurar o validar explícitamente:

```text
Builder
What to build
Strategy Type
Market Sides / Direction
Full Settings
Genetic Options
Initial Population / Genetic Prefilters
Data Settings
Trading Options
Realistic Gaps
Building Blocks
Signals
Indicators
Comparators
Number of Conditions
Rule Complexity
Order Types
Exit Types
Stop Loss
Profit Target
Break Even
Trailing Stop
Exit After Bars
Exit Rule
Ranking Builder / Fitness
Ranking filters
Strategy Filtering Conditions
Max Strategies
Dismiss Similar Strategies
CrossChecks del Builder
Retest on Additional Markets del Builder
Higher Precision del Builder si aplica
Data Bank output del Builder
OOS
MC_TRADES
MC_SPREAD_SLIPPAGE
TICK
SPP
WFA MATRIX
Fechas de cada tarea
OOS Global Period
OOS Data range parts / OOS1
Símbolos de cada tarea
Source/precision/broker/uSymbol/uSymbolName de cada símbolo
Timeframe de cada tarea
Nombres de tareas
Data Banks visibles
Data Banks reales por Retest-Task*.xml
Gestión Monetaria extra
DeleteFailedStrategies
Nodos protegidos
Recursos internos SQX
Prueba de humo de importación
Reporte minucioso
Auditoría JSON/CSV de diferencias
```

---

## 6. Nodos protegidos

Nunca modificar sin orden explícita:

```text
Spread base
Slippage base
Commission
Swap
Broker profile
Instrument settings
Point value
Tick size
Pip value
Symbol properties
Money Management
Initial Capital
Risked Money
Custom indicators
Custom blocks
Java snippets
Recursos internos del broker
Recursos internos del instrumento
```

Si se modifica un nodo protegido con autorización del usuario, el reporte debe declararlo como:

```text
MODIFICACIÓN AUTORIZADA POR EL USUARIO
```

---

## 7. Regla de data por etapa

Por defecto:

```text
Builder: data normal
OOS: data normal
MC_TRADES: data normal
MC_SPREAD_SLIPPAGE: data normal
TICK: data tick
SPP: data normal
WFA MATRIX: data normal
```

Solo TICK debe usar símbolo tick si el usuario no ordenó otra cosa.

---

## 8. OOS Split correcto

OOS no debe configurarse como Global Period = solo ventana OOS, salvo orden explícita de retest OOS puro.

Correcto:

```text
OOS Global Period = periodo normal completo autorizado.
OOS1 Data Range Part = Out of sample - Test desde corte IS/OOS hasta final normal.
Filtros OOS = calculados sobre OOS1, no sobre Global Period completo.
```

Bloquea entrega:

```text
OOS Global Period igual a OOS1 sin orden explícita.
OOS1 visual = 100% cuando se esperaba split.
OOS usa fecha final tick en vez de fecha final normal.
OOS1 no está marcado como Out of sample - Test.
Filtros OOS calculados sobre Global Period completo.
```

---

## 9. DeleteFailedStrategies obligatorio

En robustez activa:

```text
OOS: DeleteFailedStrategies=true
MC_TRADES: DeleteFailedStrategies=true
MC_SPREAD_SLIPPAGE: DeleteFailedStrategies=true
TICK: DeleteFailedStrategies=true
SPP: DeleteFailedStrategies=true
WFA MATRIX: DeleteFailedStrategies=true
```

---

## 10. Auditoría global anti-residuos

Escanear todos los archivos internos del `.cfx`, no solo `config.xml`.

Buscar:

```text
Símbolos no permitidos
Brokers no permitidos
Fuentes de data incorrectas
Fechas prohibidas
Timeframes incorrectos
MarketSides incorrectos
CrossChecks residuales
RetestOnAdditionalMarkets residuales
Data Banks residuales
SL/PT/BE/trailing residuales
Ranking/filtros residuales
Global Period incorrecto
Test precision incorrecto
Nodos protegidos modificados
Rutas locales C:\Users o D:\work, salvo campos técnicos strategyFile compatibles y justificados
Strategy 0.1.7, salvo strategyFile técnico requerido y justificado
Placeholders __...__
Placeholders [[...]]
```

---

## 11. Regla de fechas en todos los Setup

Bloquea entrega si en cualquier `Setup` de cualquier tarea:

```text
dateFrom == dateTo
dateFrom > dateTo
dateTo = 1970.01.01
dateTo = 0000.00.00
fecha normal posterior al final real de data normal
fecha tick fuera del rango tick disponible
```

---

## 12. Auditoría de cadena real de Data Banks

No basta con que existan las pestañas. Hay que auditar:

```text
1. Orden visible de Data Banks en config.xml.
2. Input/Output real en cada Retest-Task*.xml.
3. Bloque activo <Databanks retestSelected="false">.
```

Cadena esperada por defecto:

```text
Results → OOS → MC_TRADES → MC_SPREAD_SLIPPAGE → TICK → SPP → WFA MATRIX
```

Configuración esperada:

```text
OOS:
Input = Results
Output = OOS

MC_TRADES:
Input = OOS
Output = MC_TRADES

MC_SPREAD_SLIPPAGE:
Input = MC_TRADES
Output = MC_SPREAD_SLIPPAGE

TICK:
Input = MC_SPREAD_SLIPPAGE
Output = TICK

SPP:
Input = TICK
Output = SPP

WFA MATRIX:
Input = SPP
Output = WFA MATRIX
```

`GESTION MONETARIA - DESACTIVADA` debe quedar inactiva y fuera de la cadena principal, preferiblemente al final.

Bloquear si aparecen nombres residuales como:

```text
MONTECARLO RNADOMIZE TRADES Y SKIP TRADES
MONTECARLO SLIPPAGE Y SPREAD
GESTION MONETARIA
```

sin el estado explícito `- DESACTIVADA`.

---

## 13. Auditoría de Symbol Resource contra Data Manager

Antes de entregar, cada símbolo debe coincidir con Data Manager en:

```text
symbol name
instrument
broker profile
source
precision
uSymbol
uSymbolName
broker id
timeframe
date from
date to
data type
```

Reglas:

```text
No basta con que el nombre del símbolo coincida.
El source debe coincidir.
La precision debe coincidir.
El broker debe coincidir.
uSymbol/uSymbolName deben coincidir con el underlying symbol real.
```

Ejemplo validado AUDCAD DooPrime:

```text
AUDCADDOOPRIME_1M:
source="2"        # Dukascopy
precision="M1"
uSymbol="AUDCAD"
uSymbolName="AUDCAD"
broker="25"

AUDCAD_TICK_DOOPRIME:
source="1"        # File
precision="TICK"
broker="-1"
```

Bloquea entrega si:

```text
Símbolo normal M1 queda con precision="TICK".
Símbolo normal Dukascopy queda con source="1" File.
Símbolo tick queda con source Dukascopy.
SQX muestra Differences con una fila concreta de símbolo/source/precision incorrecto.
SQX propone usar otro símbolo distinto al esperado.
```

---

## 14. Recursos internos SQX: strategyFile/templateFile

No limpiar agresivamente `StrategyType/@strategyFile` ni `templateFile`.

Regla:

```text
Si un .cfx base o edge hermano abre correctamente, preservar la estructura compatible de templateFile y strategyFile de ese archivo, aunque contenga una ruta local histórica, salvo que una prueba demuestre que SQX lo resuelve con alternativa segura.
```

Motivo:

```text
SQX puede necesitar esos campos para resolver recursos internos. Limpiarlos o reemplazarlos por valores genéricos puede causar:
Cannot resolve custom resources / Failed to update zip content.
```

La limpieza anti-residuos debe distinguir entre:

```text
Residuos operativos prohibidos
vs
Campos técnicos requeridos por SQX para resolver recursos
```

---

## 15. Regla LimitTimeRange / filtros horarios nativos

Tras prueba AUDCAD E2 V14:

```text
LimitTimeRange=true provocó Cannot resolve custom resources / Failed to update zip content.
LimitTimeRange=false abrió correctamente.
```

Regla operativa:

```text
No activar LimitTimeRange nativo como configuración principal en Custom Projects generados desde la base custodiada hasta tener una base compatible que ya lo soporte.
```

Para edges de sesión:

```text
Versión principal: LimitTimeRange=false.
Versión experimental opcional: LimitTimeRange=true con etiqueta EXPERIMENTAL_SESSION_ON.
```

No bloquear el edge por esto. Si se requiere sesión, preferir:

```text
- Representarla con bloques/condiciones horarias compatibles si existen.
- O pedir/exportar una base SQX que ya tenga horario nativo funcionando.
```

---

## 16. Anti-colisión de Project Name

Cada `.cfx` final debe usar un `Project name` interno único por versión.

No reutilizar nombres ya importados en SQX, porque una carpeta previa en `user/projects` puede quedar corrupta y provocar:

```text
Cannot resolve custom resources
Failed to update zip content
```

Regla:

```text
Toda corrección debe usar nombre interno nuevo: V13, V14, V15, V16, V17, FIX, etc.
```

---

## 17. Prueba de humo de importación SQX

Ningún Custom Project queda aprobado hasta que pase prueba manual de humo:

```text
1. Cerrar SQX.
2. Borrar carpetas viejas del mismo Project name en user/projects.
3. Importar desde ruta corta, por ejemplo C:\SQX_IMPORT\.
4. Si aparece “Resolve project resources”, revisar si hay filas concretas.
5. Si no hay filas concretas erróneas, pulsar “Load config using these settings”.
6. Verificar que el proyecto abre.
7. Verificar que no queda “Project has unresolved resources”.
8. Verificar Data Banks:
   Results → OOS → MC_TRADES → MC_SPREAD_SLIPPAGE → TICK → SPP → WFA MATRIX.
9. Verificar símbolos:
   Builder/OOS/MC/SPP/WFA = símbolo normal.
   TICK = símbolo tick.
10. Presionar Start.
```

El cuadro “Resolve project resources” NO es fallo bloqueante si:

```text
- No muestra filas concretas de símbolos/sesiones incorrectas.
- Al pulsar “Load config using these settings”, el proyecto abre.
- El botón Start funciona.
- No queda Project has unresolved resources.
```

Sí es fallo bloqueante si:

```text
- Aparecen filas con símbolo/source/precision incorrectos.
- SQX propone usar otro símbolo.
- Queda Project has unresolved resources.
- Start falla.
```

---

## 18. Entregables obligatorios

Cada entrega final debe incluir:

```text
1. .cfx final importable.
2. Reporte ejecutivo.
3. Reporte minucioso Builder.
4. Reporte minucioso por etapa de robustez.
5. Auditoría técnica pre-entrega.
6. Manifiesto operativo congelado.
7. Diagnóstico de régimen basado en data diaria.
8. Fichas de edge.
9. Tabla de símbolos/data/timeframe/fechas por tarea.
10. Tabla de NumberOfTrades calculado por ventana.
11. Tabla de SL/TP por edge.
12. Tabla de ranking y filtros.
13. Tabla de nodos protegidos.
14. Auditoría global anti-residuos.
15. Auditoría DataBank chain.
16. Auditoría Symbol Resource exact.
17. AUDIT_CHANGES.json o AUDIT_CHANGES.csv.
18. Plan de diagnóstico si no genera candidatos.
19. Instrucciones de prueba de humo.
```

---

## 19. Regla final

La entrega válida termina cuando el usuario recibe:

```text
Archivo importable
Explicación completa de construcción
Justificación técnica de cada decisión
Auditoría de nodos protegidos
Matriz esperado vs detectado
Auditoría anti-residuos
Auditoría de DataBank chain
Auditoría de Symbol Resource exact
Prueba de humo de importación
Plan de diagnóstico si SQX no produce candidatos
```

Objetivo:

```text
Que el usuario entienda exactamente qué está minando, por qué lo está minando, qué cambió dentro del .cfx, cómo verificarlo en SQX y cómo ajustar sin romper el edge ni los recursos.
```


---

# Actualización V1.6 — Auditoría de Data Bank Quality Gate y Builder Anti-Basura

## 64. Propósito

Esta actualización conecta la Skill 3 con la Skill 1 V1.3. La Skill 3 no diseña el Quality Gate, pero debe auditar que el Custom Project final lo haya aplicado y que el reporte lo justifique.

Regla:

```text
Un Custom Project final no es entregable si el Builder no declara y reporta su modo de generación y su Quality Gate.
```

## 65. Campos obligatorios a auditar en Builder

Cada Custom Project debe incluir en reporte y auditoría:

```text
Modo de generación: DISCOVERY / BALANCEADO PRODUCTIVO / ESTRICTO / QUALITY FIRST
Meses_IS
Timeframe
Edge
Dirección
Costo operativo estimado
MinTradesFinal calculado
AvgTrade mínimo esperado
ProfitFactor mínimo
ReturnDDRatio mínimo
DrawdownPct máximo
StagnationPct máximo
Filtros de estabilidad
Filtros de concentración/outlier
Filtros de complejidad
Genetic Prefilters más suaves que Ranking Final
```

## 66. Auditoría de dureza del Builder

La matriz de ranking hardness debe ampliarse así:

```text
Edge | Modo | Meses_IS | TF | Dirección | MinTrades esperado | MinTrades detectado | PF esperado | PF detectado | Ret/DD esperado | Ret/DD detectado | DD% esperado | DD% detectado | Stagnation esperado | Stagnation detectado | AvgTrade esperado | AvgTrade detectado | Estado
```

Bloquear entrega si:

```text
- No se declara modo de generación.
- NumberOfTrades no está calculado por meses reales.
- AvgTrade no está evaluado frente a costos cuando el activo tiene costos relevantes.
- Ranking Final está vacío o es demasiado permisivo para el modo declarado.
- Genetic Prefilters son más duros que Ranking Final.
- Se usa Ret/DD como único criterio de calidad.
- No se reporta DrawdownPct o StagnationPct en modos Balanceado/Estricto.
- No se reporta riesgo de concentración/outliers cuando existen métricas disponibles.
```

## 67. Regla anti-Results basura

Si en una ejecución previa del mismo activo/edge ocurre:

```text
- Results se llena rápido y OOS < 2%.
- OOS = 0.
- MC_SPREAD_SLIPPAGE elimina 100%.
- TICK = 0 repetidamente.
```

la siguiente entrega debe marcar en el reporte:

```text
BUILDER HARDNESS UPGRADE APLICADO
```

Y debe demostrar cambios en:

```text
- Quality Gate del Ranking Final.
- AvgTrade vs costo.
- NumberOfTrades proporcional.
- PF / RetDD / DD / Stagnation.
- Complejidad y concentración si aplica.
```

Bloquear entrega si después de un fallo de este tipo se entrega otra versión sin endurecer el Builder o sin cambiar el edge.

## 68. Prohibición de rescatar lotes débiles relajando robustez

Si el problema ocurre antes de Tick/SPP/WFA, la solución no debe ser relajar retests finales.

Regla:

```text
No relajar OOS, MC_SPREAD_SLIPPAGE, TICK, SPP o WFA para compensar un Builder que llenó Results con estrategias débiles.
```

Acciones permitidas:

```text
- Endurecer Ranking Final del Builder.
- Exigir AvgTrade proporcional al costo.
- Recalcular NumberOfTrades.
- Controlar DD/Stagnation.
- Reducir complejidad.
- Cambiar edge/timeframe/ventana.
- Usar modo DISCOVERY explícito si solo se quiere explorar.
```

## 69. Auditoría de profundidad de búsqueda

El reporte debe distinguir entre:

```text
Tiempo de minería
Cantidad en Results
Calidad mínima exigida
Supervivencia esperada en OOS/MC/Tick
```

Regla:

```text
No declarar que un Builder es bueno porque llenó Results rápido.
No declarar que un Builder es malo solo porque tardó poco.
Evaluar la dureza del Quality Gate y la supervivencia posterior.
```

## 70. Nuevos bloqueos finales

No entregar como final si:

```text
[FAIL] No existe sección Builder Quality Gate.
[FAIL] No existe modo de generación.
[FAIL] No existe cálculo de MinTradesFinal.
[FAIL] No existe análisis AvgTrade vs costo o justificación de no aplicarlo.
[FAIL] Ranking Final usa solo Ret/DD o NetProfit.
[FAIL] Results se llenó rápido en versión anterior y la nueva no muestra Builder Hardness Upgrade.
[FAIL] Se relajó robustez para rescatar un Builder débil sin orden explícita del usuario.
```


---

# Actualización V1.7 — Auditoría Multi-Timeframe Quality Gate

## 71. Propósito

Esta actualización conecta la Skill 3 con la Skill 1 V1.4. La Skill 3 debe auditar que el Custom Project no aplique filtros genéricos de H1/H4 cuando el usuario pide M15, M30 o D1.

Regla:

```text
Un Custom Project final no es entregable si el Builder no declara un perfil de Quality Gate coherente con el timeframe real.
```

## 72. Campos obligatorios nuevos de auditoría

Además de los campos de V1.6, la auditoría debe incluir:

```text
Timeframe real del Builder
Perfil de timeframe aplicado: M15 / M30 / H1 / H4 / D1 / otro
TradesPorMesEsperados usado
MinTradesFinal calculado
MinTradesGenetic calculado
Multiplicador AvgTrade vs costo usado
Costo operativo base usado
Control de same-bar/ambiguous trades si M15/M30
Control de outlier/concentración si D1
Justificación si el timeframe no está en M15/M30/H1/H4/D1
```

## 73. Matriz de auditoría ampliada

La matriz de ranking hardness debe quedar como mínimo así:

```text
Edge | Modo | TF | Perfil TF | Meses_IS | Trades/mes esperado | MinTrades esperado | MinTrades detectado | AvgTrade mult esperado | AvgTrade detectado | PF esperado | PF detectado | Ret/DD esperado | Ret/DD detectado | DD% esperado | DD% detectado | Stagnation esperado | Stagnation detectado | Outlier/concentración | Complejidad | Estado
```

## 74. Bloqueos por timeframe

Bloquear entrega si:

```text
M15/M30 usa mínimos de trades propios de H4/D1 sin justificación.
M15/M30 no evalúa AvgTrade frente a costo.
M15/M30 ignora ambiguous trades o same-bar exits cuando aparecen en dismissal stats.
D1 usa mínimos de trades de H1/M15.
D1 no reporta riesgo de outlier/concentración cuando las métricas existen.
D1 se aprueba con pocos trades sin advertencia ni revisión de concentración.
H1/H4 heredan filtros de otra base sin cálculo por meses IS.
```

## 75. Interpretación de dismissal stats por timeframe

La respuesta al usuario debe distinguir el problema según temporalidad:

```text
M15/M30:
Si dominan no trades, too little trades, same-bar o ambiguous trades, revisar estructura de edge/entradas y no solo bajar PF/RetDD.
Si domina AvgTrade, revisar costo operativo y tipo de entrada.

H1/H4:
Si dominan PF, RetDD, AvgTrade o NumberOfTrades, calibrar Quality Gate manteniendo modo.
Si dominan no trades/too little trades, revisar edge/bloques/timeframe.

D1:
Si domina NumberOfTrades, revisar si el edge diario es demasiado selectivo.
Si hay outliers o profit concentrado, no salvar la estrategia por PF/RetDD alto.
```

## 76. Regla anti-copia de filtros entre timeframes

```text
No se permite copiar el Ranking Final de un Custom Project H4 a M15 o D1 sin recalcular:
- MinTradesFinal.
- AvgTradeMin.
- PF mínimo.
- Ret/DD mínimo.
- DD máximo.
- Stagnation máxima.
- filtros de concentración/outliers.
- controles de ejecución.
```

## 77. Prueba de humo ampliada

Además de la prueba de humo de recursos, el reporte debe pedir al usuario verificar visualmente:

```text
Timeframe correcto en Builder y retests.
Data range correcto.
Data Banks correctos.
Quality Gate corresponde al timeframe.
No hay filtros de otro timeframe.
```

## 78. Regla final V1.7

```text
Un Custom Project puede estar técnicamente importable y aun así estar mal configurado si usa filtros del timeframe equivocado.
La auditoría debe bloquear ese caso antes de entregar.
```


---

# Actualización V1.8 — StrategyFile Resource Safe Gate y bloqueo anti strategyFile genérico

## 75. Incidente real que origina la actualización

Durante la generación de tres Custom Projects GBPJPY DooPrime Cent, el primer archivo importado falló inmediatamente en SQX con:

```text
Cannot resolve custom resources.
Failed to update zip content
```

Diagnóstico aplicado:

```text
El final V1 reemplazó StrategyType/@strategyFile por SQ3StrategyTemplateExample.sq4.
La versión V2 RESOURCE_SAFE abrió al restaurar un strategyFile técnico compatible y usar Project Name nuevo.
```

## 76. Regla bloqueante de StrategyType

La auditoría pre-entrega debe inspeccionar cada nodo:

```text
<StrategyType ... templateFile="..." strategyFile="..." ... />
```

en todos los archivos internos del `.cfx`.

Bloquear entrega si cualquier `strategyFile` queda como:

```text
SQ3StrategyTemplateExample.sq4
__STRATEGY_FILE__
vacío
igual a templateFile por reemplazo genérico
placeholder
ruta inventada
```

Excepción muy limitada:

```text
Solo se permite strategyFile genérico si el usuario aporta una base exportada donde ese mismo valor ya abrió en esa instalación, y la prueba de humo queda documentada. Por defecto, se bloquea.
```

## 77. Diferencia obligatoria entre templateFile y strategyFile

Regla:

```text
templateFile = plantilla SQX que puede conservarse.
strategyFile = recurso interno de estrategia que SQX usa para resolver contenido.
```

No deben tratarse como equivalentes.

Acción correcta:

```text
Conservar templateFile si venía compatible.
Restaurar strategyFile desde base/sibling/diccionario validado.
No limpiar strategyFile por estética.
No reemplazar strategyFile por el nombre de templateFile.
```

## 78. StrategyFile esperado dinámico

El `strategyFile` esperado no es universal. Debe declararse en el reporte como:

```text
StrategyFile Resource Safe usado: <valor exacto>
Fuente del valor: base validada / edge hermano validado / diccionario de nodos / export usuario
```

Ejemplo de valor técnico válido usado en la corrección GBPJPY:

```text
D:\work\StrategyQuant4\work_directory\StrategyQuant\user\projects\Retester\databanks\Results\Strategy 0.1.7.sq4
```

Aunque parezca ruta local histórica, puede ser necesario para SQX. No es residuo operativo si se usa como `strategyFile` compatible documentado.

## 79. Auditoría StrategyFile Resource Safe

Agregar matriz obligatoria:

```text
Archivo | Nodo | templateFile detectado | strategyFile detectado | strategyFile esperado | Fuente del esperado | Estado
```

Estado PASS si:

```text
- Todos los StrategyType tienen strategyFile no genérico.
- Todos los StrategyType usan el mismo recurso esperado o un recurso compatible justificado.
- No hay placeholders.
- No hay valores vacíos.
- No hay reemplazo automático por SQ3StrategyTemplateExample.sq4.
```

Estado FAIL si:

```text
- Solo Build-Task está corregido pero Retest-Task no.
- Existe diferencia no justificada entre tareas.
- strategyFile contiene `SQ3StrategyTemplateExample.sq4` sin smoke test real.
- strategyFile contiene placeholder.
```

## 80. Acción correctiva cuando aparece Cannot resolve custom resources

Si el usuario reporta el error:

```text
Cannot resolve custom resources / Failed to update zip content
```

proceder en este orden:

```text
1. No tocar símbolos, costos ni filtros primero.
2. Comparar V fallida contra última V que abre o contra base compatible.
3. Revisar StrategyType/@strategyFile y templateFile en todos los XML.
4. Restaurar strategyFile compatible.
5. Verificar No Session / Sessions vacío si aplica.
6. Crear Project Name nuevo con sufijo RESOURCE_SAFE o Vx_RS.
7. Reempaquetar.
8. Entregar instrucciones para borrar carpeta vieja user/projects/<ProjectName fallido>.
9. Pedir importar desde ruta corta y presionar Start como smoke test.
```

## 81. Anti-residuos refinado

La auditoría anti-residuos no debe marcar automáticamente como error una ruta histórica en `StrategyType/@strategyFile` si:

```text
- Es el recurso exacto documentado como StrategyFile Resource Safe.
- Viene de una base o edge hermano validado.
- Está presente solo como valor de strategyFile.
```

Sí se bloquea si esa ruta aparece en:

```text
símbolos
brokers
sesiones
rutas de data
nombres de proyecto
crosschecks
campos operativos no relacionados con StrategyType
```

## 82. Bloqueo final añadido

```text
Archivo sin auditoría StrategyFile Resource Safe = archivo no entregable.
Archivo con strategyFile genérico = archivo no entregable.
Archivo que falla con Cannot resolve custom resources y se corrige sin Project Name nuevo = archivo no entregable.
```


---

# Actualización V1.9 — Operators Safe Gate, Comparators y Operand Audit

## 83. Incidente real que origina la actualización

Después de corregir `strategyFile` en GBPJPY, se detectó otro fallo: el Builder no inicia correctamente si se activan indicadores pero se dejan desactivados los comparadores/operadores funcionales.

Regla nueva:

```text
Archivo técnicamente importable + Builder sin operadores = archivo no entregable.
```

## 84. Auditoría bloqueante Operators Safe

Antes de entregar cualquier `.cfx`, la Skill 3 debe inspeccionar todos los XML internos y, como mínimo, `Build-Task1.xml`.

Matriz obligatoria:

```text
Archivo | ActiveIndicators | ActiveComparators | ActiveOperands | ActiveSignals | ActiveOrderTypes | ActiveStopLimitBlocks | Estado
```

Bloquear si:

```text
ActiveIndicators > 0 y ActiveComparators = 0.
ActiveComparators = 0.
ActiveOperands = 0.
ActiveOrderTypes != 1.
OrderType = EnterAtStop o EnterAtLimit y ActiveStopLimitBlocks = 0.
OrderType = EnterAtMarket y ActiveStopLimitBlocks heredados activos sin justificación.
```

## 85. Comparators/Operators whitelist

Buscar y auditar estos bloques cuando existan:

```text
IsGreater
IsLower
IsGreaterOrEqual
IsLowerOrEqual
Equals
NotEquals
CrossesAbove
CrossesBelow
IsRising
IsFalling
IsGreaterCount
IsLowerCount
IsGreaterPercentil
IsLowerPercentil
IndicatorCrossesAboveMA
IndicatorCrossesBelowMA
```

## 86. Operand/value whitelist

Buscar y auditar estos operandos cuando existan:

```text
Prices.Close
Prices.High
Prices.Low
Prices.Open
Prices.Bid
Prices.Ask
Indicators.Number
```

## 87. Anti-error de patch por categoría

La auditoría debe detectar si el patcher apagó operadores por hacer limpieza global de `category="indicators"`.

Patrón prohibido:

```text
Activar indicadores usando solo una whitelist de Indicators.* y poner en false todo lo demás en category="indicators".
```

Motivo:

```text
En SQX los comparadores también pueden estar bajo category="indicators".
```

## 88. Auditoría de OrderTypes y StopLimitBlocks

Regla final:

```text
OrderTypes activos = 1.
StopLimitBlocks > 0 si el OrderType activo es EnterAtStop o EnterAtLimit.
StopLimitBlocks = 0 si el proyecto es Market-only, salvo que exista justificación explícita.
```

Bloquear si:

```text
Market + Stop + Limit activos al tiempo en versión base.
Stop-only o Limit-only con 0 StopLimitBlocks.
Market-only con bloques StopLimit heredados y sin uso real.
```

## 89. Reporte obligatorio de corrección

Si una versión falló por operadores/comparadores, la corrección debe:

```text
1. Crear Project Name nuevo con sufijo V*_OPS u OPERATORS_SAFE.
2. Mantener strategyFile resource-safe validado.
3. Activar comparadores/operadores funcionales.
4. Activar operandos mínimos.
5. Auditar exact one order type.
6. Auditar StopLimitBlocks según OrderType.
7. Pedir borrar carpetas previas en user/projects antes de importar.
```

## 90. Regla final V1.9

```text
StrategyFile Resource Safe evita el fallo de recursos.
Operators Safe evita el fallo del Builder sin condiciones construibles.
Ambas auditorías son obligatorias y bloqueantes.
```

---

# Actualización Session Resource Safe — Incidente GBPUSD DooPrime Cent 2026-05-17

## Motivo operativo

Durante la importación de los Custom Projects GBPUSD DooPrime Cent `OPS_V1`, SQX mostró el error:

```text
Cannot check XML config resources - Cannot check session: Failed to convert session 'No Session' to xml.
```

El archivo E1 funcionó después de generar la versión `OPS_V2_SESSION_SAFE`, reemplazando el literal operativo `No Session` por el recurso de sesión real del proyecto:

```text
FX_XCCY_Currency1[DOOPRIME]
```

## Regla central Session Resource Safe

En Custom Projects finales no se debe escribir el texto humano `No Session` como recurso de sesión si SQX puede intentar convertirlo a XML.

```text
Session textual "No Session" en XML operativo final = NO ENTREGABLE,
salvo que venga de una exportación real probada y documentada en esa instalación.
```

Regla principal:

```text
LimitTimeRange=false no basta para desactivar sesión.
También debe existir un recurso de sesión resoluble por SQX en los campos internos que SQX valide.
```

## Fuente válida del recurso de sesión

El valor de sesión debe salir de una fuente real y verificable:

```text
1. Data Manager / nombre de sesión asociado al símbolo/instrumento.
2. Recurso de sesión detectado en una base o proyecto hermano que ya abrió en SQX.
3. Recurso de sesión exportado desde la instalación del usuario.
4. Recurso de sesión confirmado explícitamente por el usuario.
```

Ejemplo validado:

```text
Símbolo: GBPUSDDOOPRIME_1M
Instrumento: GBPUSD.cDOOPRIME
Broker profile: [DOOPRIME]
Sesión segura detectada/usada: FX_XCCY_Currency1[DOOPRIME]
LimitTimeRange=false
```

## Valores prohibidos en finales

Bloquear entrega si en cualquier XML interno del `.cfx` final aparece como sesión operativa:

```text
No Session
__SESSION__
[[SESSION]]
NONE
NULL
vacío cuando SQX exige recurso
recurso inventado no detectado en Data Manager/base/proyecto hermano
```

La palabra `No Session` puede aparecer únicamente en el reporte explicativo, no como valor funcional de sesión dentro de los XML del `.cfx` final.

## Auditoría obligatoria de sesiones

Antes de entregar cualquier `.cfx`, escanear todos los XML internos y reportar:

```text
Archivo | Campo/nodo sesión | Valor detectado | Valor esperado | LimitTimeRange | Estado
```

Campos o patrones a revisar globalmente:

```text
Session
Sessions
SessionOption
MarketOpenSession
TradingSession
session
sessionName
sessionId
LimitTimeRange
UseSession
TimeRange
```

Bloquear si:

```text
- Se detecta `No Session` como valor funcional.
- Se detecta placeholder de sesión.
- El recurso de sesión no coincide con el símbolo/instrumento/broker.
- `LimitTimeRange=true` aparece sin orden explícita y base compatible.
- SQX devuelve `Failed to convert session ... to xml`.
```

## Política para desactivar filtros horarios

Para versión principal segura:

```text
LimitTimeRange=false
Sin filtro horario nativo activo
Sin ventanas horarias nativas obligatorias
Sesión XML resoluble por SQX = recurso real del instrumento/broker
```

No usar `No Session` como sustituto de recurso. Si se quiere no limitar por horario, se desactiva el filtro horario con `LimitTimeRange=false`, pero se conserva/asigna una sesión válida que SQX pueda resolver.

## Edges de sesión

Hasta tener una base exportada compatible con horario nativo:

```text
Versión principal: LimitTimeRange=false + sesión real resoluble.
Versión experimental: LimitTimeRange=true solo si el usuario la pide y la base ya demostró abrir con ese recurso.
```

Para edges de sesión o time-of-day, preferir condiciones/bloques compatibles dentro del Builder antes que activar filtros horarios nativos que puedan romper recursos.

## Smoke test actualizado

La prueba de humo debe incluir:

```text
1. Importar desde ruta corta.
2. Verificar que no aparece: Failed to convert session 'No Session' to xml.
3. Si aparece Resolve project resources, revisar filas concretas.
4. Cargar con los recursos detectados solo si no cambia símbolo/source/precision/sesión.
5. Verificar Data Banks.
6. Verificar símbolos por etapa.
7. Verificar que la sesión visible corresponde al instrumento/broker o no genera error.
8. Presionar Start.
```

## Regla de aprendizaje permanente

Si un Custom Project falla por sesión, la corrección no debe hacerse solo en el archivo afectado. Deben actualizarse:

```text
- Generador / Skill 1 si diseña sesiones o Trading Options.
- Orquestador / Skill 3 para bloquear auditoría fallida.
- Custodia / Skill 4 para no convertir placeholders a `No Session`.
- Manifest y checksums del paquete de fuentes.
```


## Impacto específico en Skill 3 / QA pre-entrega

La auditoría anti-residuos queda ampliada con `SESSION RESOURCE SAFE GATE`.

### Matriz esperada vs detectada obligatoria

```text
Tarea | XML | Símbolo esperado | Sesión esperada | Sesión detectada | LimitTimeRange esperado | LimitTimeRange detectado | Estado
```

Por defecto:

```text
Builder/OOS/MC/SPP/WFA = símbolo normal + sesión real resoluble del instrumento.
TICK = símbolo tick + sesión real resoluble compatible, si SQX la exige.
LimitTimeRange=false en todas las tareas salvo orden explícita.
```

### Bloqueos nuevos

Bloquear entrega si aparece cualquiera de estos casos:

```text
[FAIL] Session literal No Session detectada en XML funcional.
[FAIL] Placeholder de sesión sin resolver.
[FAIL] Recurso de sesión no documentado.
[FAIL] No existe auditoría de sesión por tarea.
[FAIL] LimitTimeRange=true sin orden explícita/base compatible.
[FAIL] El reporte no incluye prueba de humo de sesión.
```

### Corrección automática permitida

Si se detecta `No Session` y existe una sesión real confirmada por Data Manager/proyecto hermano:

```text
Reemplazar No Session → recurso real confirmado.
Mantener LimitTimeRange=false.
Reauditar todos los XML.
Cambiar Project Name interno a nueva versión SESSION_SAFE.
```

Si no existe recurso confirmado:

```text
BLOQUEAR ENTREGA → pedir captura/export/base compatible.
```

### Nota sobre `Resolve project resources`

El cuadro de recursos puede ser aceptable, pero el error de conversión de sesión no lo es. La prueba de humo debe verificar explícitamente que no aparece:

```text
Cannot check session
Failed to convert session
Failed to convert session 'No Session' to xml
```

---

# Actualización OOS 20–30% — Regla Operativa Bloqueante para Custom Projects SQX

## Motivo operativo

En una entrega GBPUSD DooPrime Cent para objetivo TRACK se detectó un OOS aproximado de 16%, generado por un corte IS/OOS demasiado reciente respecto al histórico normal útil. Aunque la etapa OOS estaba técnicamente configurada como `OOS Global Period = periodo normal completo` y `OOS1 = ventana reciente`, el porcentaje reservado quedó por debajo del rango operativo deseado para validación fuera de muestra.

## Regla central

Todo Custom Project final con Builder + OOS debe reservar por defecto una ventana OOS cronológica reciente entre:

```text
OOS mínimo permitido por defecto: 20% del periodo normal útil.
OOS máximo permitido por defecto: 30% del periodo normal útil.
Rango recomendado general: 20%–30%.
Objetivo TRACK / incubación: 22%–27%, con default operativo 25%.
Fondeo / prop firm: 25%–30%, con default operativo 30% si hay suficiente data.
Portafolio conservador: 25%–30%, con default operativo 25%–28%.
Discovery / exploración: 20%–25%, con etiqueta DISCOVERY.
```

Regla bloqueante:

```text
Custom Project final con OOS < 20% = NO ENTREGABLE,
salvo orden explícita del usuario o imposibilidad estadística documentada.

Custom Project final con OOS > 30% = NO ENTREGABLE,
salvo orden explícita del usuario o justificación técnica documentada.
```

## Definición de periodo normal útil

El porcentaje se calcula sobre el periodo normal útil autorizado para Builder/OOS, no necesariamente sobre todo el histórico bruto disponible.

```text
Periodo normal útil = fecha normal inicial seleccionada → fecha normal final disponible/autorizada.
OOS% = duración OOS1 / duración periodo normal útil.
IS% = duración Builder/IS / duración periodo normal útil.
```

Si se descarta data antigua por régimen, calidad, discontinuidad o irrelevancia, el reporte debe declarar:

```text
Data total disponible.
Data normal útil seleccionada.
Data descartada o no usada.
Motivo de descarte.
OOS% calculado sobre la data normal útil.
```

## Selección del corte IS/OOS

El OOS debe ser el bloque cronológico más reciente del periodo normal útil, salvo orden explícita distinta.

Proceso obligatorio:

```text
1. Detectar fecha inicial y final del periodo normal útil.
2. Calcular duración total en días/meses.
3. Elegir OOS target según objetivo, data y timeframe.
4. Calcular fecha de corte IS/OOS.
5. Redondear el corte al inicio de mes o inicio de semana operativo más cercano.
6. Recalcular OOS% real después del redondeo.
7. Confirmar que OOS% real queda entre 20% y 30%.
8. Si no queda, ajustar el corte hasta cumplir el rango.
```

## Guía por longitud de histórico normal útil

```text
Más de 12 años útiles:
- TRACK: 25% default.
- Fondeo/conservador: 25%–30%.
- No bajar de 22% sin justificación.

8 a 12 años útiles:
- TRACK: 22%–25%.
- Conservador/fondeo: 25%–28%.

5 a 8 años útiles:
- 20%–25%.
- Exigir revisión de meses OOS y trades esperados.

3 a 5 años útiles:
- 20% mínimo, pero marcar muestra limitada.
- Si el OOS queda con pocos trades esperados, complementar con WFA/forward/incubación.

Menos de 3 años útiles:
- No entregar como Custom Project final robusto salvo orden explícita.
- Marcar PRELIMINAR / DISCOVERY / REQUIERE MÁS DATA.
```

## Relación con filtros OOS

El porcentaje 20%–30% no reemplaza la calibración dinámica de filtros.

Regla:

```text
Primero se garantiza OOS% 20%–30%.
Después se calibran filtros OOS por meses reales, timeframe, edge, dirección, objetivo y trades esperados.
```

El mínimo de trades OOS debe seguir calculándose así:

```text
Meses_OOS_reales = meses entre corte IS/OOS y fecha final normal.
MinTradesOOS = Meses_OOS_reales × trades mínimos por mes esperados según timeframe y edge.
```

## OOS Split correcto dentro de SQX

La regla anterior de OOS Split se mantiene y queda reforzada:

```text
OOS Global Period = periodo normal útil completo.
OOS1 Data Range Part = bloque cronológico reciente equivalente a 20%–30%.
Filtros OOS = calculados sobre OOS1.
```

Bloquear si:

```text
OOS Global Period = solo la ventana OOS sin orden explícita.
OOS1 visual = 100% cuando se esperaba split.
OOS% detectado < 20%.
OOS% detectado > 30%.
No se reporta OOS%.
No se reporta fecha de corte IS/OOS.
No se reportan meses OOS reales.
```

## Excepciones permitidas

Solo se permite salir del rango 20%–30% si el reporte declara `OOS_EXCEPTION` y explica una de estas causas:

```text
1. Orden explícita del usuario.
2. Data útil demasiado corta para sostener 20% sin destruir muestra IS.
3. Necesidad de reproducir una prueba histórica exacta.
4. Investigación experimental marcada como DISCOVERY.
5. Edge estacional/calendario donde el corte estándar rompe la estructura de eventos.
```

Toda excepción debe incluir:

```text
OOS% solicitado o detectado.
Motivo.
Riesgo.
Plan compensatorio: WFA, forward/incubación, SPP más fuerte, o nueva minería con más data.
```

## Auditoría obligatoria OOS 20–30

Cada entrega debe incluir una matriz:

```text
Tarea | Fecha inicio normal útil | Fecha fin normal útil | Corte IS/OOS | Días/meses total | Días/meses OOS | OOS% esperado | OOS% detectado | Estado
```

Estado PASS si:

```text
20% <= OOS% detectado <= 30%.
OOS1 es bloque reciente.
OOS Global Period usa periodo normal útil completo.
Filtros se calibran por OOS1 real.
```

Estado FAIL si:

```text
OOS% fuera de 20%–30% sin OOS_EXCEPTION.
Corte IS/OOS no documentado.
OOS usa fecha final tick en vez de fecha final normal.
OOS1 no está marcado como Out of sample - Test.
```

## Regla final

```text
Para Custom Projects operativos, la validación OOS debe ser reciente, cronológica y suficientemente grande.
Por defecto, ningún final se entrega con OOS menor a 20% ni mayor a 30%.
```


## Aplicación específica en Skill 3 — QA bloqueante pre-entrega

La Skill 3 debe bloquear cualquier `.cfx` final cuyo OOS% detectado esté fuera del rango 20%–30% si no existe `OOS_EXCEPTION` autorizada.

Nueva auditoría obligatoria:

```text
OOS_20_30_AUDIT:
- normal_date_from
- normal_date_to
- useful_normal_days
- useful_normal_months
- is_date_from
- is_date_to
- oos_date_from
- oos_date_to
- oos_days
- oos_months
- oos_pct
- target_pct
- target_band
- rounded_cut_date
- oos_global_period_ok
- oos1_recent_block_ok
- filters_calibrated_on_oos1
- status
```

Bloqueos adicionales:

```text
[FAIL] OOS% < 20 sin OOS_EXCEPTION.
[FAIL] OOS% > 30 sin OOS_EXCEPTION.
[FAIL] OOS% no calculado.
[FAIL] Corte IS/OOS no reportado.
[FAIL] OOS target no declarado.
[FAIL] OOS Global Period no cubre periodo normal útil completo.
```

En la matriz esperado vs detectado, agregar columnas:

```text
OOS target % | OOS detectado % | Corte esperado | Corte detectado | Estado OOS 20-30
```


---

# Actualización V1.12 — Session Existing Resource Gate, Donor Session Gate y ShortNameSafe obligatorio

## 91. Incidente real que origina la actualización

En GBPUSD DooPrime Cent se generaron varias versiones de Custom Project hasta aislar los fallos:

```text
V3: uso de FX_XCCY_Currency1[DOOPRIME] como sesión funcional → Not found / resource error.
V4: uso de FX_XCCY_Currency1DOOPRIME incrustando sesión en el .cfx → Failed to update zip content.
V5: sesión core existente sin incrustar recurso → abrió.
V6: sesión broker existente sin bloque embebido → E1/E2 abrieron; E3 falló por nombre largo.
V7: sesión existente + <Sessions /> vacío + LimitTimeRange=false + Project name corto → funcionaron los 4 customs.
```

Conclusión:

```text
La auditoría anterior detectaba placeholders y sesiones inexistentes, pero no bloqueaba dos causas reales:
1. incrustar sesiones existentes como recursos nuevos sin donor probado;
2. Project name largo que rompe update del project.cfx interno.
```

## 92. Session Existing Resource Gate

Todo Custom Project final debe clasificar la sesión en una de estas categorías:

```text
A. ExistingSessionReferenceSafe
B. EmbeddedSessionFromDonorSafe
C. NoNativeTimeFilterSafe
D. SessionUnsupportedBlocked
```

### A. ExistingSessionReferenceSafe

Uso recomendado por defecto cuando la sesión ya existe en Data Manager.

Condiciones:

```text
Session Name confirmado por Data Manager o usuario.
Campos funcionales usan el nombre exacto.
<Sessions /> vacío.
LimitTimeRange=false salvo donor compatible.
No aparece bloque <Session name="..."> embebido.
No se usa Add new al importar.
```

### B. EmbeddedSessionFromDonorSafe

Permitido solo si el usuario entrega donor `.cfx` probado.

Condiciones:

```text
Donor exportado desde la misma instalación o instalación equivalente.
Donor reimportado con éxito.
Donor arrancó con Start.
Se copia bloque <Sessions> completo desde donor, no recreado manualmente.
LimitTimeRange=true solo si donor lo usaba y abrió bien.
```

### C. NoNativeTimeFilterSafe

Permitido cuando no se quiere filtrar por horario nativo.

Condiciones:

```text
LimitTimeRange=false.
No se incrustan sesiones nuevas.
Se usa sesión existente core o broker solo como referencia si SQX la exige.
```

### D. SessionUnsupportedBlocked

Bloquear entrega si:

```text
La sesión se inventa por texto.
La sesión se arma uniendo broker profile al nombre base.
Aparece No Session como valor funcional donde SQX valida sesión.
Aparece <Session> embebida sin donor probado.
LimitTimeRange=true sin donor probado.
SQX requiere Add new para resolver sesión.
```

## 93. Diferencia entre Session Name y Broker Profile

La auditoría debe distinguir columnas de Data Manager:

```text
Session Name = valor funcional de sesión.
Broker profile = perfil asociado, no parte automática del nombre.
```

Ejemplo validado por captura:

```text
Session Name: FX_XCCY_Currency1DOOPRIME
Broker profile: [DOOPRIME]
```

Error prohibido:

```text
Convertir lo anterior en FX_XCCY_Currency1[DOOPRIME]
```

Solo se permite un nombre con corchetes si esos corchetes aparecen literalmente en la columna Session Name.

## 94. Auditoría Session Existing Resource

Agregar matriz obligatoria:

```text
Archivo | Campo sesión | Valor detectado | Fuente del valor | ¿Existe en Data Manager? | ¿Embebido en <Sessions>? | LimitTimeRange | Donor probado | Estado
```

Estados:

```text
PASS_EXISTING_REFERENCE
PASS_DONOR_EMBEDDED
PASS_NO_NATIVE_TIME_FILTER
FAIL_SESSION_INFERRED
FAIL_EMBEDDED_WITHOUT_DONOR
FAIL_LIMIT_TIME_WITHOUT_DONOR
FAIL_NO_SESSION_FUNCTIONAL
```

## 95. Regla `Add new` / `Use existing`

En Resolve project resources:

```text
No usar Add new para sesiones de broker existentes.
Usar recurso existente si el nombre aparece en Data Manager.
Si SQX obliga a Add new, bloquear entrega y pedir donor .cfx.
```

El reporte debe instruir:

```text
Si aparece Resolve project resources y la sesión existe, elegir Use existing / Load config using these settings.
No crear sesión nueva desde el importador.
```

## 96. ShortNameSafe obligatorio

Todo final debe cumplir:

```text
Project name interno preferido <= 25 caracteres.
Project name interno máximo <= 30 caracteres.
Nombre de archivo preferido <= 35 caracteres.
Ruta de importación recomendada: C:\SQX_IMPORT\.
```

Caracteres permitidos:

```text
A-Z
0-9
_
```

Evitar:

```text
espacios
tildes
corchetes
paréntesis
puntos múltiples
sufijos largos
nombres descriptivos completos
```

Ejemplos PASS:

```text
GBPDP_E1_H4PB_V7
GBPDP_E2_H4BO_V7
GBPDP_E3_H1MR_V7
GBPDP_E4_H1MO_V7
```

Ejemplo FAIL:

```text
GBPUSD_DP_E3_H1_MEAN_REVERSION_BOTH_V6_BROKERSESSION_EXISTING
```

## 97. Auditoría ShortNameSafe

Agregar matriz obligatoria:

```text
Archivo .cfx | Project name | Longitud Project name | File name | Longitud file name | Ruta recomendada | Reutiliza nombre fallido | Estado
```

Bloquear entrega si:

```text
Project name > 30.
Project name reutiliza una versión que falló.
Project name contiene caracteres no permitidos.
Nombre de archivo excesivamente largo después de un error de recursos.
Reporte no pide borrar carpetas previas fallidas en user/projects.
```

## 98. Reglas de corrección después de fallo `Failed to update zip content`

Si el usuario reporta:

```text
Cannot resolve custom resources
Failed to update zip content
```

Proceder en este orden:

```text
1. Confirmar si otras variantes del mismo lote abrieron.
2. Si algunas abrieron, no cambiar edge/ranking/costos primero.
3. Revisar Project name y longitud.
4. Revisar si hay carpeta previa corrupta en user/projects.
5. Revisar <Sessions> embebido sin donor.
6. Revisar strategyFile.
7. Crear versión nueva con Project name corto.
8. Mantener sesión existente como referencia, no embebida.
9. Mantener <Sessions /> vacío salvo donor.
10. Pedir importar desde C:\SQX_IMPORT\.
```

## 99. Donor Session workflow obligatorio

Cuando el usuario quiera sesión nativa del broker sin errores:

```text
1. Usuario crea proyecto mínimo en SQX.
2. Selecciona símbolo/broker/sesión manualmente.
3. Activa horario nativo solo si lo necesita.
4. Exporta .cfx.
5. Reimporta el mismo .cfx.
6. Presiona Start.
7. Si abre y corre, ese .cfx queda como donor session validado.
8. El generador copia recursos de sesión desde donor, no los reconstruye.
```

Sin donor:

```text
No se incrusta <Session>.
No se activa LimitTimeRange=true.
```

## 100. Actualización del checklist pre-entrega

Además de las auditorías previas, todo Custom Project debe mostrar:

```text
[ ] Session classification definida.
[ ] Session Name tomado literal de Data Manager/donor.
[ ] Broker Profile no fue pegado al nombre de sesión por inferencia.
[ ] <Sessions /> vacío si se usa existing session.
[ ] <Sessions> embebido solo si donor probado.
[ ] LimitTimeRange=false salvo donor probado.
[ ] Project name <= 30 caracteres.
[ ] Project name no reutiliza versión fallida.
[ ] Nombre de archivo corto.
[ ] Instrucción de borrar carpetas viejas.
[ ] Ruta corta de importación indicada.
```

## 101. Bloqueos finales añadidos

No entregar si:

```text
[FAIL] Sesión inferida, no confirmada.
[FAIL] Sesión existente incrustada como <Session> sin donor probado.
[FAIL] LimitTimeRange=true sin donor probado.
[FAIL] Project name > 30 caracteres.
[FAIL] Nombre de versión fallida reutilizado.
[FAIL] Reporte no incluye ShortNameSafe.
[FAIL] Reporte no incluye Session Existing Resource Gate.
```

## 102. Regla final V1.12

```text
Un Custom Project correcto no solo debe tener símbolos, fechas, ranking y Data Banks correctos.
También debe importarse sin obligar a SQX a convertir sesiones problemáticas y sin nombres internos largos.
La forma segura por defecto es: sesión existente referenciada, <Sessions /> vacío, LimitTimeRange=false, Project name corto y Project name nuevo por versión.
```
