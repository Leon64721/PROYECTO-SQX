# Skill 4 V1.9 — Custodia de Base Limpia Custom Projects SQX con Symbol Resource Exact, OOS 20–30 y Smoke Test

## Propósito

Mantener una base custodiada limpia para generar Custom Projects de StrategyQuant X sin depender de que el usuario exporte una base nueva en cada activo, evitando residuos y errores de recursos internos.

Esta Skill reemplaza:

```text
SKILL_4_CUSTODIA_BASE_CUSTOM_PROJECTS_LIMPIOS_SQX.md
SKILL_4_CUSTODIA_BASE_CUSTOM_PROJECTS_LIMPIOS_SQX_V1_1_BASE_CUSTODIADA.md
SKILL_4_CUSTODIA_BASE_CUSTOM_PROJECTS_LIMPIOS_SQX_V1_2_RESOURCE_SAFE.md
```

## Fuente base custodiada

Archivo recomendado:

```text
BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx
```

Esta base se usa como **fuente de patching**, no como Custom Project operativo directo.

---

## Uso correcto

```text
La base custodiada no se entrega ni se importa directamente como proyecto operativo.
Primero debe copiarse, parchearse completamente para el activo real y auditarse.
```

Preferir siempre esta base custodiada sobre `.cfx` derivados de activos anteriores.

No usar como base principal:

```text
EURUSD_EDGE...
GBPUSD_EDGE...
AUDCAD_EDGE...
V3.3...
V4...
V1.2...
```

salvo orden explícita y auditoría completa.

---

## Estructura mínima obligatoria de la base

La base debe contener:

```text
config.xml
Build-Task1.xml
Retest-Task1.xml = OOS
Retest-Task2.xml = MC_TRADES
Retest-Task3.xml = MC_SPREAD_SLIPPAGE
Retest-Task5.xml = TICK
Retest-Task4.xml = SPP
Retest-Task6.xml = GESTION MONETARIA - DESACTIVADA
Retest-Task7.xml = WFA_MATRIX
```

`config.xml` debe contener `<Databanks>` con, como mínimo:

```text
Results
Existing portfolio
Last generation
Initial population
Strategies to improve
OOS
MC_TRADES
MC_SPREAD_SLIPPAGE
TICK
SPP
WFA MATRIX
GESTION MONETARIA - DESACTIVADA
```

---

## Placeholders permitidos en la base

La base puede contener placeholders porque no es operativa directa:

```text
__ASSET__
__NORMAL_SYMBOL__
__TICK_SYMBOL__
__INSTRUMENT__
__BROKER_PROFILE__
__BROKER_NAME__
__SESSION__
__BUILDER_START__
__OOS_START__
__OOS_START_PLUS1__
__NORMAL_END__
__TICK_START__
__TICK_END__
__DATE_REPLACE__
__STRATEGY_FILE__
```

También bloquear en finales placeholders tipo:

```text
[[ASSET]]
[[SYMBOL]]
[[AUDCAD]]
[[EURUSD]]
[[GBPUSD]]
[[USDJPY]]
```

---

## Regla bloqueante para archivos finales

Un `.cfx` final generado desde la base custodiada queda inválido si conserva cualquier placeholder.

Custom Project final:

```text
No puede contener placeholders.
Debe tener símbolos reales.
Debe tener fechas reales.
Debe tener instrumento real.
Debe tener source/precision/broker/uSymbol/uSymbolName alineados con Data Manager.
Debe pasar auditoría anti-residuos.
Debe pasar auditoría OOS Split.
Debe pasar auditoría DataBank chain.
Debe pasar auditoría Symbol Resource exact.
Debe pasar auditoría de ranking hardness.
Debe pasar auditoría de nodos protegidos.
Debe incluir reporte minucioso.
Debe incluir prueba de humo manual.
```

---

## Flujo obligatorio para nuevo activo

1. Copiar `BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx`.
2. Reemplazar placeholders por valores reales.
3. Configurar símbolo normal y tick.
4. Configurar `source`, `precision`, `uSymbol`, `uSymbolName`, `broker`, `instrument` y `broker profile` según Data Manager.
5. Configurar broker, instrumento y costos solo si el usuario los autoriza o confirma.
6. Configurar Builder, OOS, MC_TRADES, MC_SPREAD_SLIPPAGE, TICK, SPP y WFA_MATRIX.
7. Configurar OOS con Global Period completo normal y OOS1 como Data range part.
8. Configurar TICK solo con símbolo tick.
9. Reconstruir edge, timeframe, dirección, SL/TP, bloques, ranking y filtros según Skill 1.
10. Configurar robustez según Skill 2.
11. Auditar todo según Skill 3.
12. Generar reporte minucioso, matriz esperado vs detectado y auditoría de cambios.
13. Entregar instrucciones de prueba de humo.

---

## Symbol Resource exact

Antes de generar final, pedir o detectar desde Data Manager:

```text
Symbol Name
Instrument
Broker profile
Underlying Symbol
Timeframe / precision
Timezone
Date from
Date to
Source
Data type
Broker id si aplica
```

Ejemplo validado AUDCAD:

```text
AUDCADDOOPRIME_1M:
source="2"
precision="M1"
uSymbol="AUDCAD"
uSymbolName="AUDCAD"
broker="25"

AUDCAD_TICK_DOOPRIME:
source="1"
precision="TICK"
broker="-1"
```

Bloquear si:

```text
El símbolo normal queda como File cuando Data Manager dice Dukascopy.
El símbolo normal M1 queda con precision TICK.
El símbolo tick queda como Dukascopy cuando Data Manager dice File.
uSymbol/uSymbolName no coinciden con el underlying symbol.
```

---

## LimitTimeRange y sesión

No activar `LimitTimeRange=true` como versión principal desde la base custodiada hasta tener una base compatible que abra con ese recurso.

Para edges de sesión:

```text
Versión principal: LimitTimeRange=false.
Versión opcional: EXPERIMENTAL_SESSION_ON con LimitTimeRange=true.
```

---

## strategyFile/templateFile

No limpiar agresivamente `StrategyType/@strategyFile` ni `templateFile`.

Si una variante hermana abre correctamente, preservar su estructura compatible, aunque tenga ruta local histórica, salvo prueba contraria.

---

## DataBank chain

Todo final debe tener cadena real:

```text
Results → OOS → MC_TRADES → MC_SPREAD_SLIPPAGE → TICK → SPP → WFA MATRIX
```

Y cada tarea:

```text
OOS: Results → OOS
MC_TRADES: OOS → MC_TRADES
MC_SPREAD_SLIPPAGE: MC_TRADES → MC_SPREAD_SLIPPAGE
TICK: MC_SPREAD_SLIPPAGE → TICK
SPP: TICK → SPP
WFA MATRIX: SPP → WFA MATRIX
```

`GESTION MONETARIA - DESACTIVADA` queda inactiva y fuera de la cadena.

---

## Anti-colisión de Project Name

Cada final debe tener `Project name` interno único por versión. No reutilizar nombres importados anteriormente.

---

## Prueba de humo

El usuario debe probar:

```text
Importar desde ruta corta.
Si aparece Resolve project resources:
  - si no hay filas concretas erróneas, pulsar Load config using these settings.
Verificar que abre.
Verificar Data Banks.
Verificar símbolos.
Presionar Start.
```

El aviso “Resolve project resources” es aceptable solo si se resuelve con el botón azul y el proyecto abre sin recursos pendientes.

---

## Regla final

La base custodiada es un contenedor técnico maestro. El valor operativo está en el patch completo + auditoría + prueba de humo, no en la base por sí sola.


---

# Actualización V1.4 — Integración con Data Bank Quality Gate

## 29. Propósito

La base custodiada sigue siendo una fuente técnica de patching, no un Custom Project operativo. Esta actualización agrega que cualquier proyecto generado desde la base debe incluir la configuración y reporte del Data Bank Quality Gate definido por Skill 1 V1.3.

## 30. Regla de base custodiada + Quality Gate

Al copiar `BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx`, el patcher debe completar no solo símbolos, recursos, fechas y Data Banks, sino también:

```text
- Modo de generación.
- Quality Gate del Builder.
- MinTradesFinal proporcional.
- AvgTrade mínimo frente a costos.
- PF / RetDD / DD / Stagnation.
- Reglas de concentración/outlier si están disponibles.
- Complejidad máxima o control de reglas.
```

## 31. Placeholders y finales

Además de los placeholders técnicos existentes, queda prohibido entregar un final que conserve placeholders o notas sin resolver sobre Quality Gate:

```text
__QUALITY_MODE__
__MIN_TRADES_FINAL__
__AVG_TRADE_MIN__
__PF_MIN__
__RETDD_MIN__
__DD_MAX__
__STAGNATION_MAX__
__COST_MULTIPLIER__
```

## 32. Regla final V1.4

```text
La base custodiada produce estructura técnica.
La Skill 1 produce calidad del Builder.
La Skill 3 audita que ambas cosas quedaron aplicadas.
```

No entregar un Custom Project generado desde la base si el Builder queda sin Quality Gate reportado.


---

# Actualización V1.5 — Base Custodiada con Multi-Timeframe Quality Gate

## 33. Propósito

La base custodiada debe poder generar Custom Projects para M15, M30, H1, H4 y D1 sin heredar filtros de otro timeframe.

Regla:

```text
La base custodiada aporta estructura técnica.
El patcher debe reconstruir el Quality Gate según el timeframe real solicitado.
```

## 34. Placeholders adicionales prohibidos en finales

Un archivo final no puede conservar:

```text
__TIMEFRAME_PROFILE__
__TRADES_PER_MONTH_EXPECTED__
__MIN_TRADES_GENETIC__
__AVG_TRADE_COST_MULTIPLIER__
__OUTLIER_FILTER__
__AMBIGUOUS_TRADES_POLICY__
__SAME_BAR_POLICY__
```

## 35. Reglas por timeframe al parchear desde la base

```text
M15/M30:
- Recalcular trades mínimos altos.
- Recalcular AvgTrade vs costo con multiplicador intradía.
- Revisar ambiguous trades y same-bar exits.
- No entregar sin advertencia si no hay tick/retest suficiente.

H1/H4:
- Aplicar perfiles intermedios.
- Recalcular trades por meses IS y edge.
- No heredar filtros de una base anterior.

D1:
- Recalcular trades bajos pero suficientes.
- Activar reporte de outlier/concentración.
- Revisar stagnation absoluta, WorstYearProfit y profit concentrado si las métricas existen.
```

## 36. Regla final V1.5

```text
La base custodiada nunca define por sí sola el ranking final.
El ranking final siempre se reconstruye por Skill 1 según timeframe, edge, costos, meses IS y objetivo; Skill 3 audita que eso se cumplió.
```


---

# Actualización V1.6 — Custodia StrategyFile Resource Safe

## 37. Motivo

La base custodiada puede contener:

```text
strategyFile="__STRATEGY_FILE__"
```

porque es una fuente de patching, no un proyecto operativo. El error real en GBPJPY ocurrió cuando ese placeholder se reemplazó por:

```text
strategyFile="SQ3StrategyTemplateExample.sq4"
```

Ese reemplazo no es seguro en Custom Projects y puede causar:

```text
Cannot resolve custom resources
Failed to update zip content
```

## 38. Regla de custodia del placeholder __STRATEGY_FILE__

El placeholder `__STRATEGY_FILE__` solo puede reemplazarse por un recurso strategyFile compatible validado.

Fuentes aceptadas:

```text
1. StrategyFile exacto de un proyecto hermano que ya abrió en SQX.
2. StrategyFile exacto del diccionario de rutas/nodos confirmado.
3. StrategyFile exacto de una base exportada por el usuario y probada.
```

Fuentes prohibidas:

```text
SQ3StrategyTemplateExample.sq4
valor vacío
ruta inventada
normalización estética
copiar templateFile hacia strategyFile
```

## 39. Regla de conservación templateFile/strategyFile

```text
templateFile puede seguir como SQ3StrategyTemplateExample.sq4.
strategyFile no debe igualarse a templateFile por defecto.
```

Si el patcher no sabe qué strategyFile usar:

```text
BLOQUEAR ENTREGA → REQUIERE BASE O EDGE HERMANO VALIDADO.
```

No entregar finales con strategyFile dudoso.

## 40. Auditoría bloqueante desde base custodiada

Todo final generado desde la base debe incluir:

```text
StrategyFile Resource Safe usado
Fuente del strategyFile
Lista de archivos XML donde aparece StrategyType
Comparación templateFile vs strategyFile
Estado PASS/FAIL
```

Bloquear si:

```text
- El final conserva __STRATEGY_FILE__.
- El final usa SQ3StrategyTemplateExample.sq4 como strategyFile.
- El final tiene strategyFile vacío.
- El final corrige solo algunas tareas.
- El final no tiene Project Name nuevo después de una versión fallida.
```

## 41. Project Name después de fallo

Si una versión produjo error de recursos, no se debe reutilizar el mismo Project Name. Crear una variante nueva:

```text
<PROJECT>_V2_RS
<PROJECT>_RESOURCE_SAFE
<PROJECT>_FIX_RS
```

El reporte debe pedir borrar la carpeta previa en `user/projects`.

## 42. Regla final V1.6

```text
La base custodiada permite placeholders.
El final no permite placeholders ni strategyFile genérico.
El strategyFile es un recurso SQX protegido y debe tratarse como nodo técnico crítico.
```


---

# Actualización V1.7 — Custodia Operators Safe para Builder

## 43. Motivo

La base custodiada puede contener todos los bloques disponibles, pero el patch final puede romper el Builder si activa indicadores y desactiva comparadores/operadores por error.

El riesgo aparece cuando se manipula globalmente:

```text
category="indicators"
```

porque dentro de esa categoría SQX puede incluir tanto indicadores reales como comparadores/operadores.

## 44. Regla de patch desde base custodiada

Al generar un final desde la base, el patcher debe separar explícitamente:

```text
Indicators reales
Comparators/Operators
Operands/Prices/Values
Signals
OrderTypes
StopLimitBlocks
ExitTypes
```

No se permite apagar todo `category="indicators"` salvo la whitelist de indicadores, porque eso puede apagar `IsGreater`, `IsLower`, `CrossesAbove`, `CrossesBelow`, etc.

## 45. Placeholders lógicos prohibidos en finales

Además de los placeholders existentes, bloquear si el reporte conserva:

```text
__COMPARATORS__
__OPERATORS__
__OPERANDS__
__ACTIVE_ORDER_TYPES__
__STOP_LIMIT_BLOCKS__
```

## 46. Auditoría custodiada Operators Safe

Todo final debe incluir:

```text
Archivo | Indicadores activos | Comparadores activos | Operandos activos | OrderTypes activos | StopLimitBlocks activos | Estado
```

Bloquear si:

```text
Indicadores activos y comparadores activos = 0.
Comparadores activos = 0.
Operandos activos = 0.
OrderTypes activos != 1.
Stop/Limit activo sin StopLimitBlocks.
```

## 47. Regla final V1.7

```text
La base custodiada aporta estructura.
La entrega final debe demostrar que el Builder tiene condiciones construibles: indicador/precio/valor + operador + indicador/precio/valor.
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


## Impacto específico en Skill 4 / Base custodiada

La base custodiada puede conservar el placeholder:

```text
__SESSION__
```

porque la base no es operativa directa. Pero ningún final puede conservarlo ni reemplazarlo por `No Session` textual.

### Reemplazo correcto del placeholder

```text
__SESSION__ → recurso real detectado/confirmado, por ejemplo FX_XCCY_Currency1[DOOPRIME]
```

### Reemplazo prohibido

```text
__SESSION__ → No Session
__SESSION__ → vacío
__SESSION__ → NONE
__SESSION__ → sesión inventada
```

### Custodia de recursos de sesión

Agregar al manifiesto operativo congelado:

```text
Session resource usado:
Fuente del session resource:
Archivos XML donde aparece:
LimitTimeRange detectado:
Estado Session Resource Safe:
```

### Regla final V1.8

```text
La base custodiada puede no tener una sesión final.
El Custom Project final siempre debe tener una sesión resoluble si SQX la valida.
Desactivar horario no equivale a escribir No Session.
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


## Aplicación específica en Skill 4 — Base custodiada y placeholders

La base custodiada sigue siendo source-only y no define el porcentaje OOS por sí misma. Todo patch final debe completar el corte IS/OOS calculado por el motor operativo y auditar que el OOS final quede entre 20% y 30%.

Placeholders adicionales prohibidos en finales:

```text
__OOS_TARGET_PCT__
__OOS_DETECTED_PCT__
__OOS_CUT_DATE__
__OOS_EXCEPTION__
```

Bloquear entrega si un final conserva cualquiera de esos placeholders o si el reporte no incluye auditoría OOS 20–30.


---

# Actualización V1.10 — Custodia Existing Session Safe, Donor Session Safe y ShortNameSafe

## 50. Motivo

La base custodiada puede generar proyectos técnicamente válidos como XML, pero SQX puede fallar al importarlos si:

```text
- Se incrusta una sesión existente como recurso nuevo sin donor probado.
- Se usa un nombre de sesión inferido desde el broker profile.
- Se reemplaza __SESSION__ por No Session funcional.
- Se activa LimitTimeRange=true sin base compatible.
- El Project name es demasiado largo.
- Se reutiliza una carpeta corrupta en user/projects.
```

## 51. Custodia del placeholder `__SESSION__`

El placeholder `__SESSION__` de la base custodiada solo puede resolverse mediante una de estas fuentes:

```text
1. Session Name literal confirmado en Data Manager.
2. Session Name literal de donor .cfx probado.
3. Session Name literal de proyecto hermano que abrió y arrancó.
```

Prohibido resolverlo por inferencia:

```text
Nombre base + broker profile.
Nombre base + [BROKER].
No Session.
NONE / NULL / vacío.
```

## 52. Modo Existing Session Reference

Cuando la sesión ya existe en Data Manager:

```text
Reemplazar __SESSION__ en campos funcionales por el nombre exacto.
No insertar bloque <Session name="..."> en el .cfx.
Dejar <Sessions /> vacío.
Mantener LimitTimeRange=false salvo donor compatible.
```

Ejemplo validado:

```text
Session Name: FX_XCCY_Currency1DOOPRIME
Broker profile: [DOOPRIME]
Modo seguro: usar FX_XCCY_Currency1DOOPRIME como referencia funcional y dejar <Sessions /> vacío.
```

## 53. Modo Donor Session Embedded

Solo si el usuario aporta donor `.cfx` validado:

```text
Copiar bloque <Sessions> completo desde donor.
Copiar campos funcionales relacionados con sesión.
Copiar LimitTimeRange solo si el donor lo usa y abre.
No recrear la sesión manualmente.
```

El reporte debe indicar:

```text
Donor file:
Fecha de prueba:
¿Reimportó?: sí/no
¿Start funcionó?: sí/no
Campos copiados:
Estado DonorSessionSafe:
```

## 54. Custodia de `LimitTimeRange`

Por defecto:

```text
LimitTimeRange=false
```

Solo permitir:

```text
LimitTimeRange=true
```

si:

```text
- El usuario lo pide explícitamente.
- Existe donor .cfx probado.
- La auditoría confirma que el bloque <Sessions> viene del donor.
```

## 55. ShortNameSafe desde la base custodiada

Al generar finales desde la base:

```text
Project name interno preferido <= 25 caracteres.
Project name máximo <= 30 caracteres.
Nombre de archivo preferido <= 35 caracteres.
```

La base no debe generar nombres descriptivos largos. El reporte puede ser descriptivo, pero el Project name no.

Ejemplo:

```text
Reporte: GBPUSD DooPrime Cent Edge 3 H1 Mean Reversion Both V7
Project name: GBPDP_E3_H1MR_V7
File name: GBPDP_E3_H1MR_V7.cfx
```

## 56. Matriz obligatoria de custodia de sesión

Todo final debe incluir:

```text
Project | Session mode | Session functional value | Sessions block | LimitTimeRange | Donor used | Data Manager confirmed | Estado
```

Estados:

```text
PASS_EXISTING_SESSION_REFERENCE
PASS_DONOR_SESSION_EMBEDDED
PASS_NO_NATIVE_TIME_FILTER
FAIL_INFERRED_SESSION
FAIL_EMBEDDED_WITHOUT_DONOR
FAIL_LIMIT_TIME_WITHOUT_DONOR
FAIL_NO_SESSION_FUNCTIONAL
```

## 57. Matriz obligatoria ShortNameSafe

```text
Project | Project name | Length | File name | File length | Import path recommendation | Estado
```

Bloquear si:

```text
Length > 30.
File length excesiva tras fallo previo.
Nombre reutilizado tras Cannot resolve custom resources.
Caracteres no ASCII, espacios, corchetes o tildes.
```

## 58. Limpieza de carpetas previas

Todo reporte de corrección debe pedir:

```text
Cerrar SQX.
Borrar carpetas previas fallidas en user/projects.
Importar desde C:\SQX_IMPORT\.
```

No basta con generar Project name nuevo si SQX conserva carpeta corrupta de una versión anterior con el mismo nombre.

## 59. Regla final V1.10

```text
La base custodiada no debe incrustar sesiones existentes por defecto.
Debe referenciarlas como existentes y usar <Sessions /> vacío, salvo donor probado.
Todo final generado desde la base debe tener Project name corto y nuevo.
```
