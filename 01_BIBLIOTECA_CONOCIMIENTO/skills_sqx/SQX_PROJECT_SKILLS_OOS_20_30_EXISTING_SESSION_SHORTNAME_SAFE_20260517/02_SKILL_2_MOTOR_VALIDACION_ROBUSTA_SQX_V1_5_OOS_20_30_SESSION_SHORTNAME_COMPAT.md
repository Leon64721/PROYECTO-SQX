# Skill Final Operativa V1.4 — Motor de Validación Robusta `.cfx` para StrategyQuant X

**Propósito:** validar de forma progresiva las estrategias generadas en StrategyQuant X Builder, usando un flujo operativo por etapas basado en `.cfx` de prueba, Data Banks sucesivos, filtros dinámicos y criterios binarios de aprobación o descarte.

**Estado:** Skill Final Operativa V1.4 consolidada como proceso ejecutivo reutilizable. Esta versión agrega proporcionalidad obligatoria por ventana real usada: los filtros de OOS, Tick, SPP y WFA se calibran sobre la data realmente evaluada, no sobre toda la data disponible.

---

## 1. Principio rector

La robustez no se evalúa en abstracto.

Una estrategia es robusta o no robusta según:

```text
- Objetivo para el que fue creada.
- Activo.
- Broker.
- Tipo de cuenta.
- Timeframe.
- Edge.
- Dirección.
- Data usada en Builder.
- CrossCheck usado en Builder.
- Data OOS disponible.
- Data tick disponible.
- Resultado de cada prueba previa.
```

Regla base:

> La Skill Builder crea estrategias. La Skill de Robustez valida si esas estrategias realmente sirven para el objetivo operativo declarado.

La IA no debe configurar una prueba de robustez sin entender primero qué se intentó crear en el Builder.

---

### 1.1 Regla de proporcionalidad por ventana real

La robustez se mide sobre la ventana realmente usada en cada etapa.

Regla obligatoria:

```text
La data disponible total no define automáticamente los filtros.
Los filtros se calibran por la duración real evaluada en esa etapa.
```

Por tanto, OOS, Tick, SPP y WFA deben calcular mínimos y umbrales según:

```text
- Meses reales evaluados.
- Timeframe real usado.
- Edge.
- Dirección.
- Objetivo operativo.
- Tipo de cuenta.
- Sensibilidad a costos y ejecución.
- Cantidad de trades esperada.
```

No se debe exigir a una ventana corta el mismo comportamiento estadístico que a 10 o 20 años de data.
Tampoco se debe relajar una ventana larga como si fuera una validación corta.


## 2. Relación con la Skill Builder

La Skill de Robustez hereda el contexto operativo de la Skill Builder.

La Skill Builder define:

```text
Activo:
Broker:
Tipo de cuenta:
Símbolo de construcción:
Símbolo de validación / broker:
Timeframe elegido por edge:
Justificación del timeframe:
Edge o familia de edge:
Dirección:
Objetivo:
Modo de generación:
Periodo Builder:
Periodo OOS:
Data total disponible:
Data usada realmente en Builder/IS:
Data descartada o no usada:
Justificación de uso/recorte de data:
Data broker/tick disponible:
Ranking usado en Builder:
CrossCheck usado en Builder:
```

La Skill de Robustez usa ese perfil para decidir:

```text
- Qué filtros aplicar en OOS.
- Qué intensidad usar en Monte Carlo Trades.
- Qué métodos activar en Monte Carlo Retest.
- Qué Ranking exigir en Tick Retest.
- Qué configuración usar en SPP.
- Qué ventanas y filtros usar en WFA Matrix.
- Qué estrategias merecen pasar a MT5.
- Qué estrategias merecen considerarse para portafolio.
```

Regla:

```text
Si el usuario ya tiene estrategias en Data Bank, debe enviar preferiblemente:

1. .cfx del Builder usado.
2. Data Bank generado por el Builder.
3. .cfx base de la siguiente prueba.
```

Si no se envía el `.cfx` del Builder, la Skill puede trabajar, pero con menor precisión porque pierde contexto del objetivo original.

---

## 3. Clasificación del objetivo heredado

La Skill de Robustez no inventa el objetivo. Lo hereda del Builder.

### 3.1 Incubación / trackrecord

Prioridades:

```text
- Robustez razonable.
- Bajo sobreajuste.
- Buen comportamiento OOS.
- Drawdown controlado.
- Stagnation moderada.
- Average Trade positivo.
- Compatibilidad con ejecución real.
```

Uso en robustez:

```text
OOS: balanceado.
MC Trades: balanceado.
MC Retest: spread/slippage realista.
Tick Retest: proporcional a data tick disponible.
SPP: balanceado.
WFA Matrix: balanceado.
```

### 3.2 Fondeo / prop firm

Prioridades:

```text
- Drawdown bajo.
- Baja exposición.
- Rachas negativas controladas.
- Estabilidad de curva.
- Baja probabilidad de romper límites de fondeo.
```

Uso en robustez:

```text
OOS: más exigente con DrawdownPct.
MC Trades: más estricto con expansión de DD.
MC Retest: spread/slippage realista-fuerte.
Tick Retest: fuerte control de deterioro.
SPP: balanceado/fuerte.
WFA Matrix: foco en DD por ventana y estabilidad.
```

### 3.3 Portafolio conservador

Prioridades:

```text
- Baja varianza.
- Drawdown bajo.
- Estabilidad.
- Baja stagnation.
- Curva suave.
```

Uso en robustez:

```text
OOS: balanceado/fuerte.
MC Trades: balanceado/fuerte.
MC Retest: puede activar métodos adicionales si tiene sentido.
Tick Retest: degradación limitada.
SPP: fuerte si hay suficientes trades.
WFA Matrix: exigente.
```

### 3.4 Portafolio agresivo

Prioridades:

```text
- Mayor retorno.
- Mayor tolerancia a variabilidad.
- Buen payout.
- Capacidad de recuperación.
```

Uso en robustez:

```text
OOS: no exigir curva perfecta.
MC Trades: no castigar demasiado profit concentrado.
MC Retest: spread/slippage realista.
Tick Retest: NetProfit positivo y AvgTrade positivo.
SPP/WFA: validar que el edge no sea accidental.
```

---

## 4. Archivos técnicos del sistema

### 4.1 `.cfx` del Builder

Uso:

```text
- Recuperar objetivo original.
- Ver activo, broker, timeframe, fechas, edge y dirección.
- Revisar Ranking usado.
- Revisar CrossCheck de broker.
- Entender qué filtros ya pasaron las estrategias.
```

### 4.2 Data Bank anterior

Cada etapa recibe un Data Bank de entrada.

Ejemplo:

```text
Builder Results → OOS
OOS → MC Trades
MC Trades → MC Retest
MC Retest → Tick
Tick → SPP
SPP → WFA Matrix
WFA Matrix → Evaluación MT5
```

### 4.3 `.cfx` base de cada prueba

Uso:

```text
- Contenedor técnico editable.
- Fuente de estructura XML compatible con SQX.
- Punto de partida para configurar Ranking, CrossChecks y Data Banks.
```

Regla:

```text
El .cfx base no se asume correcto.
Se analiza, se conserva lo coherente y se ajusta lo necesario.
```

---

## 5. Flujo oficial de validación

El flujo oficial queda así:

```text
1. Builder con data larga + CrossCheck broker obligatorio.
2. OOS estructural con Ranking dinámico.
3. Monte Carlo Trades Manipulation obligatorio.
4. Monte Carlo Retest Methods.
5. Retest Tick / Real Spread / Slowest.
6. SPP / Strategy Parameter Permutation.
7. WFA Matrix.
8. Confirmación final MT5.
9. Selección para portafolio.
```

La etapa de Gestión Monetaria / Higher Precision queda fuera por ahora.

---

## 6. Regla binaria de decisión

No existe categoría de observación.

Cada etapa solo produce dos resultados:

```text
APROBADA:
- Cumple todos los filtros obligatorios de la etapa.

DESCARTADA:
- Falla uno o más filtros obligatorios de la etapa.
```

Regla:

```text
Si una estrategia falla una etapa, no continúa en el flujo.
```

---

## 7. Etapa 1 — Builder con CrossCheck broker obligatorio

### 7.1 Propósito

Crear estrategias con data larga, pero filtrarlas desde el nacimiento contra la data del broker.

### 7.2 Regla operativa

El Builder debe usar:

```text
Main data:
- Data larga, ejemplo Dukascopy o data extendida.

Additional Market / CrossCheck broker:
- Data del broker o símbolo real/tick/cent.
```

### 7.3 Objetivo del CrossCheck broker en Builder

No es validar robustez final.

Es evitar que nazcan estrategias incompatibles con el broker.

### 7.4 Filtros sugeridos para CrossCheck broker en Builder

```text
NetProfit > 0
ProfitFactor > 1.00 a 1.03
NumberOfTrades > mínimo proporcional
DrawdownPct < 45 a 55
ReturnDDRatio > 0.50 a 1.00
```

No usar como filtro obligatorio temprano:

```text
RSquared alto
Sharpe alto
Stability alta
WinningPct alto
Stagnation demasiado estricta
```

### 7.5 Regla final de Builder

```text
El Builder usa data larga para descubrir estrategias, pero debe incluir CrossCheck obligatorio con data del broker para filtrar incompatibilidad operativa desde el inicio.
```

---

## 8. Etapa 2 — OOS estructural con Ranking dinámico

### 8.1 Propósito

Validar que las estrategias generadas en Builder sobreviven en un periodo de datos no vistos, usando la misma familia de data larga utilizada para la minería.

El OOS no valida ejecución real del broker ni estabilidad paramétrica extrema.

### 8.2 Input

```text
- .cfx base de OOS.
- Data Bank salido del Builder.
- Fechas OOS definidas por el usuario.
- Activo.
- Timeframe.
- Edge o tipo de estrategia.
- Objetivo heredado desde Builder.
- Duración real del OOS.
```

### 8.3 Output

```text
Data Bank OOS
```

### 8.4 Regla central

```text
Los filtros del OOS deben tener sentido para la cantidad de data OOS realmente usada.
No se copian filtros del Builder.
No se exige el OOS como si fuera toda la data histórica.
No se calculan mínimos usando la data total disponible si el OOS usa solo una ventana parcial.
```

### 8.4.1 Regla de calibración por muestra real

Cada filtro del OOS debe salir de la ventana real configurada:

```text
Meses_OOS_reales = meses entre inicio OOS y fin OOS configurados.
MinTradesOOS = Meses_OOS_reales × trades mínimos por mes esperados según timeframe y edge.
```

Si el activo tiene data desde 2003 pero el OOS configurado es 2022-2026, los filtros deben calibrarse sobre 2022-2026, no sobre 2003-2026.

La Skill debe reportar:

```text
- Data total disponible.
- Data usada en OOS.
- Meses reales de OOS.
- Mínimo de trades calculado.
- Umbrales ajustados por objetivo.
```


### 8.5 Fitness recomendado

```text
ReturnDDRatio
```

### 8.6 Filtros principales

```text
NetProfit > 0
ProfitFactor > 1.00 a 1.05
NumberOfTrades > mínimo dinámico
DrawdownPct < límite dinámico
ReturnDDRatio > umbral dinámico
AvgTrade > 0
```

### 8.7 Filtros secundarios opcionales

```text
StagnationPct
ProfitableMonthsPct
Stability
RSquared suave, solo si el edge lo justifica
WinningPct, solo en mean reversion o pullback
PayoutRatio, útil en breakout/trend
```

### 8.8 Cálculo de mínimo de trades

```text
Meses_OOS = meses entre inicio OOS y fin OOS
MinTradesOOS = Meses_OOS × trades mínimos por mes esperados
```

Guía inicial:

```text
H1:
- Mean Reversion / Pullback: 1.0 a 3.0 trades/mes
- Breakout / Trend: 0.8 a 2.0 trades/mes
- Session / Time-based: 1.5 a 4.0 trades/mes

H4:
- Mean Reversion / Pullback: 0.8 a 2.0 trades/mes
- Breakout / Trend: 0.4 a 1.5 trades/mes
- Volatility Expansion: 0.4 a 1.5 trades/mes

D1:
- Trend / Breakout: 0.2 a 1.0 trades/mes
- Pullback: 0.3 a 1.2 trades/mes
```

### 8.9 Preset OOS balanceado

```text
NetProfit > 0
ProfitFactor > 1.03 a 1.05
NumberOfTrades > mínimo dinámico
DrawdownPct < 40 a 50
ReturnDDRatio > 0.70 a 1.20
AvgTrade > 0
```

### 8.10 Regla sobre RSquared

```text
RSquared no debe usarse como filtro fuerte por defecto en OOS.
Puede usarse como observación o filtro suave entre 0.20 y 0.50.
No usar RSquared > 0.70 como regla estándar.
```

### 8.11 Decisión

```text
APROBADA:
- Cumple todos los filtros OOS obligatorios.

DESCARTADA:
- Falla uno o más filtros OOS obligatorios.
```

---

## 9. Etapa 3 — Monte Carlo Trades Manipulation

### 9.1 Propósito

Validar que la estrategia no dependa excesivamente del orden exacto de trades ni de que se ejecuten absolutamente todas las operaciones históricas.

### 9.2 Regla operativa

```text
Monte Carlo Trades Manipulation es obligatorio para todas las estrategias que pasan OOS.
```

### 9.3 Input

```text
- .cfx base de MC Trades.
- Data Bank salido del OOS.
- Objetivo heredado desde Builder.
- Tipo de estrategia / edge.
```

### 9.4 Output

```text
Data Bank MC Trades
```

### 9.5 Configuración base

```text
MonteCarloManipulation: ON

Methods:
- RandomizeTradesOrder: ON
  Method: exact

- RandomlySkipTrades: ON
  Probability: 10%

NumberOfSimulations:
- 1000

MCUseFullSample:
- true
```

### 9.6 Acceptance balanceado

```text
NetProfit MC 95% >= 50% a 60% del NetProfit original
DrawdownPct MC 95% <= 160% a 175% del DrawdownPct original
```

### 9.7 Default recomendado

```text
NetProfit MC 95% >= 60% del original
DrawdownPct MC 95% <= 160% a 175% del original
```

### 9.8 Fondeo / cuenta real

```text
NetProfit MC 95% >= 50% a 60%
DrawdownPct MC 95% <= 125% a 150%
```

### 9.9 Decisión

```text
APROBADA:
- Cumple NetProfit MC.
- Cumple DrawdownPct MC.

DESCARTADA:
- Falla cualquiera de los dos filtros.
```

---

## 10. Etapa 4 — Monte Carlo Retest Methods

### 10.1 Propósito

Validar que la estrategia sobrevive a condiciones de retest alteradas, especialmente ejecución imperfecta por spread y slippage.

### 10.2 Regla operativa

Monte Carlo Retest Methods es obligatorio, pero su configuración no es fija.

### 10.3 Métodos disponibles

```text
RandomizeHistoryData
RandomizeMinDistance
RandomizeSlippage
RandomizeSpread
RandomizeStartingBar
RandomizeStrategyParameters
```

### 10.4 Base mínima

```text
RandomizeSpread: ON
RandomizeSlippage: ON
```

### 10.5 Métodos adicionales

La IA puede activar métodos adicionales si tiene sentido según:

```text
- Broker.
- Activo.
- Tipo de cuenta.
- Timeframe.
- AvgTrade.
- Tipo de entrada: Market, Stop o Limit.
- Edge.
- Cantidad de trades.
- Objetivo final.
```

### 10.6 RandomizeSpread

Regla:

```text
No usar rangos fijos universales.
Configurar según spread promedio y spread extremo razonable del broker/activo.
```

Guía:

```text
Forex majors H1/H4:
- Min: spread promedio
- Max: 2x a 4x spread promedio

Forex crosses:
- Min: spread promedio
- Max: 3x a 5x spread promedio

Índices / XAUUSD:
- Configuración específica por broker.
```

### 10.7 RandomizeSlippage

Guía:

```text
Forex majors H1/H4:
- Suave: 0 a 1
- Balanceado: 0 a 2
- Fuerte: 0 a 3

Forex crosses:
- Balanceado: 0 a 3
- Fuerte: 0 a 5
```

### 10.8 RandomizeMinDistance

Activar si:

```text
- La estrategia usa Stop Orders.
- La estrategia usa Limit Orders.
- El broker tiene restricciones de distancia mínima relevantes.
- El activo es sensible a ejecución.
```

No activar si:

```text
- La estrategia usa principalmente Market Orders.
```

### 10.9 RandomizeStartingBar

Activar si:

```text
- Hay suficiente histórico.
- La estrategia puede depender de la alineación inicial de barras.
- Usa indicadores con lookback largo.
- Objetivo es cuenta real o portafolio conservador.
```

Guía:

```text
Suave: MaxChange 20 a 50
Balanceado: MaxChange 50
Fuerte: MaxChange 100
```

### 10.10 RandomizeStrategyParameters

Activar si:

```text
- La estrategia tiene parámetros optimizables relevantes.
- Queremos medir sensibilidad paramétrica antes de SPP.
- Objetivo es cuenta real, fondeo o portafolio conservador.
```

Guía:

```text
Suave:
- Probability: 5
- MaxChange: 10

Balanceado:
- Probability: 10
- MaxChange: 10 a 15

Fuerte:
- Probability: 10
- MaxChange: 20
```

### 10.11 RandomizeHistoryData

No activarlo por defecto.

Activar solo si:

```text
- Se busca estrés fuerte.
- Hay suficientes trades.
- El objetivo es cuenta real o portafolio conservador.
- La estrategia pasó muy bien etapas anteriores.
```

### 10.12 NumberOfSimulations

```text
Suave: 30 a 50
Balanceado: 50
Fuerte: 100
```

### 10.13 Acceptance balanceado

```text
NetProfit MC Retest >= 50% a 60% del original
DrawdownPct MC Retest <= 160% a 180% del original
```

### 10.14 Fondeo / cuenta real

```text
NetProfit MC Retest >= 50% a 60%
DrawdownPct MC Retest <= 130% a 150%
```

### 10.15 Decisión

```text
APROBADA:
- Cumple todos los filtros MC Retest configurados.

DESCARTADA:
- Falla uno o más filtros obligatorios.
```

---

## 11. Etapa 5 — Retest Tick / Real Spread / Slowest

### 11.1 Propósito

Validar si la estrategia sobrevive en la data tick del broker, con real spread y modo slowest.

### 11.2 Regla operativa

Esta etapa es un Retester independiente con data tick del broker ya configurada.

La IA no debe modificar data, símbolo ni costos salvo orden explícita.

La IA debe configurar principalmente el Ranking.

### 11.3 Input

```text
- .cfx base del Tick Retest.
- Data Bank salido de MC Retest.
- Data tick del broker ya configurada.
- Fecha inicio y fecha fin disponibles.
- Timeframe.
- Edge.
- Objetivo heredado.
```

### 11.4 Output

```text
Data Bank TICK
```

### 11.5 Qué no se modifica sin orden explícita

```text
Símbolo
Fuente de data
Test precision
Real spread
Spread/slippage base
Comisión
Swap
Broker profile
Instrument settings
Money Management
```

### 11.6 Ranking principal

```text
Fitness:
- ReturnDDRatio

Filtros principales:
- NetProfit
- ProfitFactor
- NumberOfTrades
- DrawdownPct
- ReturnDDRatio
- AvgTrade
```

### 11.7 Cálculo dinámico según data tick

```text
Meses_Tick = meses entre inicio tick y fin tick
MinTradesTick = Meses_Tick × trades mínimos por mes esperados
```

Guía:

```text
H1:
- Mean Reversion / Pullback: 1.0 a 3.0 trades/mes
- Breakout / Trend: 0.8 a 2.0 trades/mes

H4:
- Mean Reversion / Pullback: 0.6 a 1.8 trades/mes
- Breakout / Trend: 0.3 a 1.2 trades/mes

D1:
- Trend / Breakout: 0.15 a 0.8 trades/mes
- Pullback: 0.2 a 1.0 trades/mes
```

### 11.7.1 Regla sobre data tick disponible vs data tick usada

La data tick disponible es el universo máximo de validación, no una obligación automática.

Usar toda la data tick solo si:

```text
- La calidad es consistente.
- El histórico cubre varios regímenes útiles.
- El volumen de trades esperado es suficiente.
- No introduce tramos anómalos incompatibles con el broker/cuenta actual.
```

Si se usa una ventana parcial de tick, los filtros deben calibrarse sobre esa ventana parcial.
El reporte debe mostrar la diferencia entre data tick disponible y data tick usada.


### 11.8 Tick data corta

Menos de 24 meses:

```text
NetProfit > 0
ProfitFactor > 1.00
NumberOfTrades > mínimo dinámico bajo
DrawdownPct < 50 a 60
ReturnDDRatio > 0.40 a 0.80
AvgTrade > 0
```

### 11.9 Tick data media

24 a 60 meses:

```text
NetProfit > 0
ProfitFactor > 1.00 a 1.05
NumberOfTrades > mínimo dinámico normal
DrawdownPct < 40 a 55
ReturnDDRatio > 0.60 a 1.10
AvgTrade > 0
```

### 11.10 Tick data larga

Más de 60 meses:

```text
NetProfit > 0
ProfitFactor > 1.03 a 1.10
NumberOfTrades > mínimo dinámico normal/alto
DrawdownPct < 35 a 50
ReturnDDRatio > 0.80 a 1.50
AvgTrade > 0
StagnationPct < 40 a 55, opcional
ProfitableMonthsPct > 45 a 60, opcional
```

### 11.11 Decisión

```text
APROBADA:
- Cumple todos los filtros Tick.

DESCARTADA:
- Falla uno o más filtros Tick.
```

---

## 12. Etapa 6 — SPP / Strategy Parameter Permutation

### 12.1 Propósito

Validar que la estrategia no depende de una combinación exacta y frágil de parámetros.

### 12.2 Regla operativa

SPP se ejecuta después del Tick Retest.

### 12.3 Input

```text
- .cfx base de SPP.
- Data Bank salido del Tick Retest.
- Data larga o data configurada para SPP.
- Timeframe.
- Edge.
- Cantidad de trades.
- Objetivo heredado.
```

### 12.4 Output

```text
Data Bank SPP
```

### 12.5 Configuración base

```text
OptProfileSysParamPermutation: ON

MaxTests: 500 a 1000
DistributionUp: 20
DistributionDown: 20
Steps: 4

WhatToParametrize:
Recommended: true
Periods: false
Shifts: false
Constants: false
OtherParams: false
EntryParams: false
EntryLogic: false
ExitParamsUsed: false
ExitParamsUnused: false
BooleanParams: false
```

### 12.6 Acceptance base

```text
ProfitOptPct: 35 a 40
AvgProfit: 0
UniformDistrChanges: 5
StdevAvgProfit: 1
EvalProfitOptCheck: true
EvalAvgProfitCheck: true
EvalUniformDistrCheck: true
EvalTopProfitCheck: false
```

### 12.7 SPP fuerte

Para fondeo, cuenta real o portafolio conservador:

```text
MaxTests: 1000 a 1500
DistributionUp: 20 a 30
DistributionDown: 20 a 30
Steps: 4 a 5
ProfitOptPct: 40 a 50
UniformDistrChanges: 3 a 5
EvalTopProfitCheck: true o false según dureza
```

### 12.8 Regla por cantidad de trades

```text
Menos de 80 trades:
- SPP suave o balanceado ligero.

80 a 200 trades:
- SPP balanceado.

Más de 200 trades:
- SPP balanceado/fuerte.
```

### 12.9 Decisión

```text
APROBADA:
- Cumple todos los checks activos del SPP.
- Cumple condiciones adicionales si existen.

DESCARTADA:
- Falla cualquier check obligatorio.
```

---

## 13. Etapa 7 — WFA Matrix

### 13.1 Propósito

Validar estabilidad temporal de la estrategia en diferentes combinaciones de ventanas de optimización y prueba.

### 13.2 Regla operativa

WFA Matrix se ejecuta después de SPP.

### 13.3 Input

```text
- .cfx base de WFA Matrix.
- Data Bank salido de SPP.
- Data larga disponible.
- Timeframe.
- Edge.
- Objetivo heredado.
```

### 13.4 Output

```text
Data Bank WFA MATRIX
```

### 13.5 Configuración base

```text
WalkForwardMatrix: ON

MaxTests: 3000

WhatToParametrize:
Recommended: true
Todo lo demás: false

Acceptance:
thresholdPct: 80
robCombRows: 2
robCombCols: 2
robMinComb: 3
```

### 13.5.1 Regla de ventanas WFA proporcionales

Las combinaciones de WFA Matrix deben ser coherentes con la data realmente asignada a WFA, el timeframe y el edge.

No se debe construir una matriz demasiado exigente para una muestra corta ni demasiado débil para una muestra larga.

Antes de configurar WFA Matrix, definir:

```text
- Data total disponible.
- Data realmente usada para WFA.
- Número esperado de trades por ventana.
- Tamaño mínimo aceptable de IS.
- Tamaño mínimo aceptable de OOS por ventana.
- Riesgo de ventanas con pocos trades.
```


### 13.6 Filtros base

```text
NetProfit WFA Matrix > 0
NetProfit WF/OOS > 55
WF % profitable runs > 65
Max profit in one run as % of total < 55
Max % Drawdown in one run <= 25
StagnationPct < 35
```

### 13.7 Ajuste por objetivo

#### Incubación / trackrecord

```text
NetProfit WFA Matrix > 0
NetProfit WF/OOS > 50 a 55
WF % profitable runs > 60 a 65
Max profit in one run < 55 a 60
Max DD in one run <= 25 a 30
StagnationPct < 35 a 45
```

#### Portafolio conservador

```text
NetProfit WFA Matrix > 0
NetProfit WF/OOS > 55 a 65
WF % profitable runs > 65 a 75
Max profit in one run < 45 a 55
Max DD in one run <= 20 a 25
StagnationPct < 30 a 40
```

#### Fondeo / The5ers

```text
NetProfit WFA Matrix > 0
NetProfit WF/OOS > 50 a 60
WF % profitable runs > 65 a 70
Max profit in one run < 50 a 55
Max DD in one run <= 20 a 25
StagnationPct < 30 a 40
```

### 13.8 Checklist obligatorio antes de WFA

```text
[ ] Símbolo correcto.
[ ] Timeframe correcto.
[ ] Fechas correctas.
[ ] Fecha final no es 1970.
[ ] Sesión correcta.
[ ] Input Data Bank = SPP.
[ ] Output Data Bank = WFA MATRIX.
[ ] Solo WalkForwardMatrix activo.
[ ] DeleteFailedStrategies = true.
[ ] Filtros proporcionales a data y timeframe.
```

### 13.9 Decisión

```text
APROBADA:
- Cumple todos los filtros WFA Matrix.

DESCARTADA:
- Falla cualquier filtro obligatorio.
```

---

## 14. Confirmación final MT5

### 14.1 Propósito

Validar externamente que las estrategias que pasaron WFA se comportan de forma razonable en MetaTrader 5.

### 14.2 Input

```text
- Data Bank WFA.
- Estrategias exportadas.
- Reportes individuales de SQX.
- Retests MT5.
- Configuración de broker/cuenta.
```

### 14.3 Evaluación

La IA debe revisar:

```text
- Resultado WFA.
- Resultado SPP.
- Resultado Tick.
- Degradación SQX vs MT5.
- NetProfit.
- ProfitFactor.
- Drawdown.
- ReturnDDRatio.
- AvgTrade.
- NumberOfTrades.
- Stagnation.
- Calidad de curva.
- Riesgo operativo.
```

### 14.4 Resultado

```text
APTA PARA PORTAFOLIO
DESCARTADA
```

---

## 15. Evaluación final para portafolio

Una estrategia no entra a portafolio solo por pasar WFA.

Debe evaluarse su aporte al conjunto:

```text
- Robustez individual.
- Drawdown.
- Stagnation.
- Correlación con otras estrategias.
- Diversificación por activo.
- Diversificación por timeframe.
- Diversificación por edge.
- Comportamiento reciente.
- Riesgo para fondeo o cuenta real.
```

Clasificación final:

```text
APTA PARA PORTAFOLIO
DESCARTADA
```

---

## 16. Protección de nodos sensibles

Nunca modificar sin orden explícita:

```text
Spread
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
```

Regla:

```text
La IA puede configurar filtros y pruebas, pero no debe alterar costos ni propiedades económicas del instrumento sin autorización.
```

---

## 17. Reporte obligatorio por etapa

Cada configuración debe entregar un reporte:

```text
Etapa:
Archivo .cfx base:
Data Bank input:
Data Bank output:
Activo:
Broker:
Timeframe:
Objetivo heredado:
Data usada:
Duración de data:
CrossChecks activos:
CrossChecks apagados:
Ranking configurado:
Filtros obligatorios:
Nodos protegidos no modificados:
Cambios recomendados:
Motivo de cada cambio:
Resultado esperado:
APROBADA / DESCARTADA:
```

---

## 18. Formato práctico de uso

### 18.1 Para iniciar robustez desde Builder

El usuario debe enviar:

```text
1. .cfx del Builder usado.
2. Data Bank generado por Builder.
3. .cfx base del OOS.
```

La IA debe responder:

```text
1. Perfil heredado del Builder.
2. Diagnóstico del Data Bank.
3. Configuración recomendada del OOS.
4. Ranking dinámico OOS.
5. Filtros APROBADA / DESCARTADA.
```

### 18.2 Para continuar una etapa posterior

El usuario debe enviar:

```text
1. Data Bank de la etapa anterior.
2. .cfx base de la prueba siguiente.
3. Objetivo si cambió.
4. Información de data disponible si aplica.
```

La IA debe responder:

```text
1. Diagnóstico del .cfx.
2. Qué conservar.
3. Qué modificar.
4. Configuración recomendada.
5. Filtros obligatorios.
6. Resultado APROBADA / DESCARTADA.
```

---

## 19. Errores prohibidos

La Skill nunca debe:

1. Configurar pruebas sin heredar el objetivo del Builder.
2. Usar los mismos filtros para todos los activos/timeframes.
3. Exigir filtros desproporcionados para poca data.
4. Cambiar símbolo, spread, comisión, swap o money management sin permiso.
5. Activar todos los métodos de Monte Carlo Retest sin criterio.
6. Usar RSquared alto como filtro estándar de OOS.
7. Hacer SPP antes del Tick Retest.
8. Hacer WFA Matrix antes del SPP.
9. Dejar estrategias fallidas dentro del flujo si el usuario pidió decisión binaria.
10. Evaluar portafolio solo por NetProfit.
11. Pasar estrategias a MT5 sin revisar WFA/SPP/Tick.
12. Usar un `.cfx` con residuos de otro activo/timeframe sin validarlo.
13. Calibrar filtros con la data total disponible cuando la etapa usa una ventana parcial.
14. Exigir mínimos de trades desproporcionados para el timeframe y la duración real.
15. Usar toda la data tick por defecto sin revisar calidad, régimen y representatividad.

---

## 20. Checklist final de la Skill

```text
[ ] El objetivo fue heredado desde Builder.
[ ] El CrossCheck broker del Builder fue identificado.
[ ] El Data Bank anterior fue recibido.
[ ] El .cfx base de la etapa fue leído.
[ ] Los nodos protegidos fueron respetados.
[ ] Los filtros fueron configurados según la ventana real usada, timeframe, edge y objetivo.
[ ] La data total disponible no fue confundida con la data usada en la etapa.
[ ] Los mínimos de trades fueron calculados por meses reales evaluados.
[ ] La etapa produce solo APROBADA o DESCARTADA.
[ ] El Data Bank output está definido.
[ ] DeleteFailedStrategies debe estar alineado con la regla binaria.
[ ] Se generó reporte de configuración.
```

---

## 21. Estado de la Skill

Esta versión debe considerarse:

```text
Skill Final Operativa V1.3 — Motor de Validación Robusta .cfx para StrategyQuant X
```

Lista para prueba controlada end-to-end con:

```text
Builder.cfx
Data Bank Builder
OOS.cfx
MC Trades.cfx
MC Retest.cfx
Tick Retest.cfx
SPP.cfx
WFA.cfx
Resultados individuales
Retest MT5
```

Regla final:

```text
La Skill no promete que cualquier estrategia será robusta.
Promete un proceso ordenado, proporcional y binario para descartar estrategias débiles y conservar solo candidatas con mayor probabilidad de sobrevivir a validación real.
```


---

## 22. Regla operativa añadida — Base `.cfx` exacta por etapa y entrega obligatoria

Cada etapa de validación debe trabajar sobre el `.cfx` base exacto enviado por el usuario para esa prueba.

La IA no debe reutilizar un `.cfx` de una etapa anterior, de una prueba vieja o de otro activo/timeframe si el usuario no lo envió explícitamente como base actual.

Entrada mínima por etapa:

```text
1. Data Bank de la etapa anterior.
2. .cfx base exacto de la prueba actual.
3. Perfil heredado del Builder o .cfx del Builder si aún no se ha leído.
```

La IA solo puede modificar, según corresponda:

```text
- Input Data Bank.
- Output Data Bank.
- Ranking / filtros.
- CrossCheck de la prueba actual.
- Parámetros propios del test actual.
```

No debe modificar sin orden explícita:

```text
- Símbolo.
- Fechas.
- Data source.
- Timeframe.
- Broker.
- Spread base.
- Slippage base.
- Comisión.
- Swap.
- Money Management.
```

Salida obligatoria por etapa:

```text
1. .cfx final modificado/importable.
2. Reporte de configuración.
3. Resumen de cambios.
4. Filtros APROBADA / DESCARTADA.
```

Si el `.cfx` base enviado por el usuario ya contiene la configuración correcta, la IA debe validarlo, conservarlo, reexportarlo con nombre operativo claro y entregar el reporte indicando que no se tocaron nodos protegidos.


---

# Actualización V1.1 — Evaluación integral post-WFA y preparación para MT5

Esta actualización se agrega después de aplicar el flujo completo con lotes reales y detectar un punto operativo importante: **el ranking final de estrategias candidatas a MT5 no debe basarse solo en el WFA global ni solo en el WFA individual**.

La decisión pre-MT5 debe considerar todo el recorrido de la estrategia:

```text
OOS
→ Monte Carlo Trades
→ Monte Carlo Retest / Spread-Slippage
→ Retest Tick / Real Spread / Slowest
→ SPP
→ WFA Matrix global
→ WFA individual por estrategia
```

Regla central:

```text
Una estrategia que se ve excelente en WFA, pero se ve débil en Retest Tick, debe bajar de prioridad.
Una estrategia que combina buen Tick + buen SPP + buen WFA individual debe subir de prioridad.
```

---

## 22. Evaluación integral para seleccionar candidatas a MT5

### 22.1 Propósito

Después de WFA Matrix, la IA debe seleccionar cuáles estrategias merecen ser exportadas/retesteadas en MT5.

Esta selección no debe hacerse únicamente por:

```text
- NetProfit WFA.
- Ret/DD WFA.
- Profit Factor WFA.
```

Debe hacerse ponderando la calidad completa del camino de robustez.

### 22.2 Inputs recomendados

Para evaluar candidatas a MT5, el usuario debe enviar, idealmente:

```text
1. Data Bank del WFA Matrix.
2. Resultados individuales del WFA de cada estrategia candidata.
3. Resultado del Retest Tick previo.
4. Resultado del SPP previo.
5. Si es posible, resultado de MC Spread/Slippage y MC Trades.
```

Si el usuario envía solo WFA, la IA puede dar una preselección, pero debe advertir que falta ponderar Tick/SPP.

### 22.3 Regla de ponderación

La IA debe priorizar estrategias con equilibrio entre:

```text
1. Supervivencia en Tick Retest.
2. Estabilidad paramétrica en SPP.
3. WFA Matrix global aprobado.
4. WFA individual consistente.
5. Buen comportamiento WF/OOS.
6. Baja concentración de beneficio en una sola ventana.
7. Drawdown controlado.
8. AvgTrade suficiente para ejecución real.
```

Guía de ponderación operativa:

```text
Retest Tick / ejecución real: 30% a 35%
WFA individual: 25% a 30%
WFA global: 20% a 25%
SPP: 10% a 15%
OOS + MC previos: 5% a 10%
```

Esta ponderación no es matemática rígida; es una guía para evitar elegir estrategias solo por una métrica aislada.

---

## 23. Cómo ajustar el ranking si Tick contradice WFA

### 23.1 Si WFA es excelente pero Tick es débil

Bajar prioridad si en Tick aparece:

```text
- ProfitFactor cercano a 1.00.
- Ret/DD bajo frente al resto del lote.
- AvgTrade bajo.
- Drawdown relativamente alto.
- RSquared o Stability muy débil.
- NetProfit positivo pero pequeño.
```

Regla:

```text
WFA excelente no compensa completamente un Tick débil.
```

La estrategia puede seguir siendo apta para MT5, pero no debe ser primera prioridad.

### 23.2 Si Tick es fuerte y WFA es bueno

Subir prioridad si en Tick aparece:

```text
- NetProfit positivo y competitivo.
- ProfitFactor sólido.
- Ret/DD fuerte.
- Drawdown bajo o moderado.
- AvgTrade superior a la mediana del lote.
- Trades suficientes.
```

Y además el WFA individual tiene:

```text
- Mayoría de ventanas OOS positivas.
- WF/OOS ProfitFactor estable.
- WF/OOS Ret/DD aceptable.
- Sin concentración extrema del beneficio.
```

### 23.3 Si WFA individual tiene ventanas negativas

No descartar automáticamente si:

```text
- Solo hay 1 ventana negativa.
- La pérdida es pequeña.
- Las ventanas posteriores son consistentes.
- El resultado Tick fue fuerte.
```

Bajar prioridad o descartar si:

```text
- Hay varias ventanas OOS negativas.
- La pérdida negativa es grande.
- El profit depende de una sola ventana.
- La ventana más rentable explica una proporción excesiva del resultado total.
```

---

## 24. Reglas para Top 5 pre-MT5

Cuando el usuario pida un Top 5 para MT5, la IA debe:

```text
1. Revisar el resultado WFA global.
2. Revisar los WFA individuales.
3. Cruzar cada candidata contra su resultado Tick.
4. Considerar SPP si el resultado está disponible.
5. Priorizar equilibrio, no solo rentabilidad.
6. Entregar ranking justificado.
```

Formato recomendado:

```text
Prioridad | Estrategia | Veredicto | Motivo principal | Riesgo principal
```

Veredictos posibles:

```text
APTA MT5 — Alta prioridad
APTA MT5 — Media prioridad
APTA MT5 — Baja prioridad
DESCARTADA
```

Regla:

```text
Si una estrategia fue top por WFA pero tuvo Tick débil, debe indicarse explícitamente.
Si una estrategia tuvo Tick fuerte y WFA estable, debe subir de prioridad aunque no tenga el mayor NetProfit global.
```

---

## 25. Ejemplo operativo de ajuste de ranking

Caso observado:

```text
Una estrategia tenía WFA/OOS Ret/DD muy alto y WFA global excelente,
pero en Retest Tick tenía ProfitFactor menor, Ret/DD más bajo y AvgTrade inferior al resto.
```

Decisión correcta:

```text
Sigue siendo apta para MT5, pero baja de prioridad frente a estrategias con mejor equilibrio Tick + WFA.
```

Caso contrario:

```text
Una estrategia no era la número 1 por WFA global,
pero tenía Tick fuerte, buen AvgTrade, buen PF, buen Ret/DD y WFA individual consistente.
```

Decisión correcta:

```text
Sube en el Top final para MT5.
```

---

## 26. Confirmación final MT5 y comparación contra Retest Tick

La validación en MT5 es la última confirmación operativa antes de considerar una estrategia para portafolio.

### 26.1 Propósito

Comparar el comportamiento de la estrategia en MT5 contra lo observado en SQX, especialmente contra el **Retest Tick / Real Spread / Slowest**.

La comparación principal no debe hacerse solo contra WFA, sino contra el Tick Retest porque es la etapa SQX más cercana a ejecución real.

### 26.2 Inputs para evaluación MT5

El usuario debe enviar:

```text
1. Reporte MT5 de cada estrategia.
2. Resultado SQX Tick Retest de esa estrategia.
3. Resultado SPP.
4. Resultado WFA global.
5. Resultado WFA individual.
6. Configuración de broker/cuenta usada en MT5.
```

### 26.3 Métricas de comparación SQX Tick vs MT5

Comparar:

```text
NetProfit SQX Tick vs NetProfit MT5
ProfitFactor SQX Tick vs ProfitFactor MT5
Drawdown SQX Tick vs Drawdown MT5
NumberOfTrades SQX Tick vs NumberOfTrades MT5
AvgTrade SQX Tick vs AvgTrade MT5
Ret/DD SQX Tick vs Ret/DD MT5
Curva/equity visual
Fechas de operaciones si están disponibles
```

### 26.4 Degradación aceptable

Una estrategia puede degradarse en MT5 y seguir siendo válida si:

```text
- NetProfit sigue positivo.
- ProfitFactor no cae por debajo de 1.00.
- Drawdown no se expande de forma peligrosa.
- NumberOfTrades no cambia de forma absurda.
- AvgTrade sigue positivo.
- La curva conserva lógica general.
```

### 26.5 Señales de descarte en MT5

Descartar si:

```text
- NetProfit MT5 <= 0.
- ProfitFactor MT5 <= 1.00.
- Drawdown MT5 se dispara frente a SQX Tick.
- Trades MT5 caen demasiado o aumentan de forma anormal.
- AvgTrade se vuelve muy bajo o negativo.
- La curva cambia radicalmente.
- La estrategia depende de una sola operación o de un tramo aislado.
```

### 26.6 Veredicto después de MT5

La IA debe clasificar cada estrategia como:

```text
APTA PARA PRE-PORTAFOLIO
APTA SOLO PARA INCUBACIÓN
DESCARTADA
```

Definiciones:

```text
APTA PARA PRE-PORTAFOLIO:
- MT5 confirma comportamiento razonablemente alineado con SQX Tick.
- La estrategia ya pasó SPP/WFA.
- No presenta deterioro operativo crítico.

APTA SOLO PARA INCUBACIÓN:
- MT5 sigue positivo, pero muestra deterioro relevante.
- Requiere observación antes de entrar a portafolio.

DESCARTADA:
- MT5 invalida la ventaja observada en SQX.
```

---

## 27. Reglas para seleccionar portafolio después de MT5

Después de MT5, no se eligen estrategias solo por rendimiento individual.

La IA debe revisar:

```text
- Correlación entre estrategias.
- Diversificación por activo.
- Diversificación por timeframe.
- Diversificación por edge.
- Coincidencia de rachas de pérdida.
- Drawdown combinado.
- Exposición simultánea.
- Aporte marginal al portafolio.
```

Regla:

```text
La mejor estrategia individual no siempre es la mejor para el portafolio.
```

Para fondeo, además revisar:

```text
- Riesgo de pérdida diaria.
- Riesgo de pérdida total.
- Peor racha esperada.
- Stagnation.
- Estabilidad reciente.
```

---

## 28. Estado de avance de la Skill V1.3

Con esta actualización, la Skill queda preparada para la siguiente fase:

```text
Validación MT5 + comparación contra SQX Tick + decisión pre-portafolio.
```

El flujo completo queda:

```text
Builder
→ OOS
→ MC Trades
→ MC Retest / Spread-Slippage
→ Tick Retest
→ SPP
→ WFA Matrix
→ WFA individual
→ Ranking integral pre-MT5
→ Retest MT5
→ Comparación SQX Tick vs MT5
→ Pre-portafolio
→ Portafolio final
```

Regla final de esta actualización:

```text
El Top para MT5 debe considerar todo el historial de validación, con peso especial al Retest Tick y al WFA individual.
```

---

# Actualización V1.2 — Lectura cualitativa del edge por reglas internas

Esta actualización agrega la capa final de revisión lógica de cada estrategia candidata. Su propósito es evitar que una estrategia sea aceptada únicamente por métricas cuantitativas, sin entender qué ventaja intenta explotar y si esa ventaja aporta diversificación real al portafolio.

Regla central:

```text
Después de WFA, WFA individual, Retest Tick y MT5, la IA debe leer las reglas internas de cada estrategia candidata para identificar el edge real, el régimen esperado y su posible redundancia frente a otras estrategias aprobadas.
```

Esta etapa no reemplaza las pruebas cuantitativas. Las complementa.

---

## 29. Etapa final — Lectura cualitativa del edge por reglas

### 29.1 Propósito

Analizar la lógica interna de la estrategia para responder:

```text
¿Qué intenta explotar esta estrategia?
¿Por qué debería funcionar?
En qué régimen debería ganar?
En qué régimen debería sufrir?
Se parece demasiado a otras estrategias candidatas?
Aporta diversificación real al portafolio?
```

Una estrategia puede pasar WFA y MT5, pero aun así quedar en reserva si su lógica es redundante frente a estrategias mejores.

---

### 29.2 Cuándo se aplica

Esta lectura se aplica después de:

```text
1. OOS aprobado.
2. MC Trades aprobado.
3. MC Retest / Spread-Slippage aprobado.
4. Retest Tick aprobado.
5. SPP aprobado.
6. WFA Matrix aprobado.
7. WFA individual revisado.
8. MT5 comparado contra SQX Tick.
```

Uso operativo:

```text
No hacer lectura cualitativa profunda de estrategias que ya fallaron etapas anteriores.
Aplicarla solo sobre candidatas reales a MT5, pre-portafolio o portafolio.
```

---

### 29.3 Inputs requeridos

El usuario debe enviar capturas o exportación de reglas de SQX:

```text
- Trading signals.
- Long entry.
- Short entry.
- Long exit.
- Short exit.
- Tipo de orden: Market, Stop o Limit.
- Precio de entrada.
- Bars Valid.
- Replace Existing Order.
- Allow Duplicate Trades.
- Stop Loss.
- Profit Target.
- Break Even.
- Trailing Stop.
- Exit After Bars.
- Filtros horarios o sesiones si existen.
- Parámetros optimizables principales.
```

Si faltan capturas, la IA debe indicar qué parte de la lógica no se pudo confirmar.

---

### 29.4 Qué debe identificar la IA

La IA debe clasificar:

```text
1. Dirección:
   - Long only.
   - Short only.
   - Both.

2. Tipo de edge:
   - Trend following.
   - Pullback continuation.
   - Mean reversion.
   - Volatility compression.
   - Volatility expansion.
   - Breakout.
   - Momentum.
   - Reversal.
   - Session / time-based.
   - Mixto.

3. Régimen esperado:
   - Tendencia.
   - Rango.
   - Compresión.
   - Expansión.
   - Ruptura.
   - Continuación.
   - Reversión.
   - Alta volatilidad.
   - Baja volatilidad.

4. Estructura de entrada:
   - Condición previa.
   - Confirmación.
   - Tipo de orden.
   - Fórmula/precio de entrada.
   - Validez de orden.

5. Estructura de salida:
   - Stop Loss.
   - Profit Target.
   - Break Even.
   - Trailing Stop.
   - Salida por señal.
   - Salida por tiempo.

6. Vulnerabilidades:
   - Sensibilidad a spread/slippage.
   - Falsos breakouts.
   - Sobredependencia de un indicador.
   - Stops demasiado ajustados.
   - Targets demasiado ambiciosos.
   - Entradas tardías.
   - Exceso de exposición.
   - Dependencia de una sola dirección.

7. Aporte a portafolio:
   - Diversificación por edge.
   - Diversificación por timeframe.
   - Diversificación por tipo de entrada.
   - Diversificación por régimen.
   - Redundancia con otras candidatas.
```

---

### 29.5 Regla de lectura de señales

La IA debe separar entre:

```text
1. Señal habilitadora.
2. Condición realmente selectiva.
3. Precio de entrada.
4. Gestión de salida.
```

Regla importante:

```text
No asumir que la condición de Trading Signals es el edge principal.
A veces la condición es muy laxa o casi siempre verdadera; en esos casos, el edge puede estar en el tipo de orden, en el precio de entrada o en el modelo de salida.
```

Ejemplo:

```text
Highest(30)[1] > Low[1]
```

puede ser una condición casi siempre verdadera. En ese caso, la verdadera lógica puede estar en una orden Buy Stop ubicada sobre una banda de volatilidad o sobre un máximo relevante.

---

### 29.6 Evaluación de tipo de orden

La IA debe evaluar el tipo de orden porque cambia el tipo de edge:

```text
Market Order:
- Entrada inmediata.
- Más común en mean reversion, pullback o señales confirmadas.

Stop Order:
- Entrada por ruptura.
- Más común en breakout, momentum y volatility expansion.
- Más sensible a slippage en momentos rápidos.

Limit Order:
- Entrada por retroceso o precio mejorado.
- Más común en mean reversion o pullback.
- Riesgo de quedarse sin ejecución.
```

Regla:

```text
Las estrategias con Stop Orders deben revisarse con especial atención en MC Spread/Slippage, Tick Retest y MT5.
```

---

### 29.7 Evaluación de SL/PT

La IA debe revisar si la salida tiene lógica coherente con el edge.

Para breakout / momentum:

```text
- Profit Target normalmente debería permitir capturar expansión.
- Stop Loss no debería ser demasiado ajustado.
- TP/SL mayor a 1 puede tener sentido si el win rate no es alto.
```

Para mean reversion:

```text
- Profit Target puede ser más cercano.
- Stop Loss puede ser más amplio.
- El win rate suele ser más importante.
```

Para pullback continuation:

```text
- SL debe proteger si el pullback falla.
- PT debe capturar continuación sin exigir expansión extrema.
```

Regla:

```text
Si la gestión de salida contradice el edge, la estrategia baja de prioridad aunque haya pasado pruebas.
```

---

### 29.8 Resultado de la lectura cualitativa

Cada estrategia debe recibir un reporte con este formato:

```text
Estrategia:
Activo / Timeframe:
Dirección:
Edge identificado:
Régimen esperado:
Condición principal:
Tipo de orden:
Precio de entrada:
Bars Valid:
Gestión de salida:
Fortalezas lógicas:
Vulnerabilidades:
Redundancia con otras candidatas:
Aporte a portafolio:
Veredicto lógico:
```

Veredictos posibles:

```text
APTA PARA PORTAFOLIO
APTA PARA PRE-PORTAFOLIO
APTA SOLO PARA INCUBACIÓN
DESCARTADA POR REDUNDANCIA
DESCARTADA POR FRAGILIDAD LÓGICA
```

---

## 30. Ejemplo aplicado — Strategy 2.1.329

### 30.1 Reglas observadas

```text
LongEntrySignal:
BollingerBands(10, 2.0).Lower[1] > KeltnerChannel(20, 2.5).Lower[1]

ShortEntrySignal: false
LongExitSignal: false
ShortExitSignal: false
```

Entrada:

```text
EnterAtStop
Dirección: Long
Precio: Highest(10)[1]
Bars Valid: 3
Replace Existing Order: ON
```

Salida:

```text
Profit Target: 2.4 * ATR(24)
Stop Loss: 2.0 * ATR(18)
No usa trailing.
No usa break-even.
No usa salida por señal.
```

### 30.2 Edge identificado

```text
Volatility Compression / Breakout Long
```

Lectura:

```text
La estrategia detecta una estructura de volatilidad usando Bollinger Bands y Keltner Channel, pero no entra inmediatamente. Espera ruptura del máximo reciente de 10 barras mediante Buy Stop. Busca continuación alcista después de una condición de compresión o estructura de volatilidad.
```

Fortalezas:

```text
- Lógica simple.
- Entrada stop coherente con breakout.
- SL/PT dinámicos por ATR.
- Solo entra si hay ruptura de máximo reciente.
```

Riesgos:

```text
- Puede sufrir falsos breakouts.
- Puede ser sensible a ejecución por usar Buy Stop.
- No tiene trailing ni break-even.
- Puede ser redundante con otras estrategias long breakout de USDJPY.
```

Veredicto lógico:

```text
APTA PARA PRE-PORTAFOLIO si no es redundante con estrategias breakout más fuertes.
```

---

## 31. Ejemplo aplicado — Strategy 4.9.322

### 31.1 Reglas observadas

```text
LongEntrySignal:
Highest(30)[1] > Low[1]

ShortEntrySignal: false
LongExitSignal: false
ShortExitSignal: false
```

Entrada:

```text
EnterAtStop
Dirección: Long
Precio: BollingerBands(10, 2.3).Upper[1] + 0.5 * ATR(40)[1]
Bars Valid: 4
Replace Existing Order: ON
```

Salida:

```text
Profit Target: 2.4 * ATR(16)
Stop Loss: 1.3 * ATR(14)
No usa trailing.
No usa break-even.
No usa salida por señal.
```

### 31.2 Edge identificado

```text
Volatility Expansion / Breakout Momentum Long
```

Lectura:

```text
La condición principal es poco restrictiva; la verdadera ventaja está en el precio de entrada. La estrategia coloca una Buy Stop por encima de la banda superior de Bollinger más un filtro adicional de 0.5 ATR. Solo entra si USDJPY rompe al alza con fuerza una zona de volatilidad superior.
```

Fortalezas:

```text
- Edge claro de expansión alcista.
- Entrada stop coherente con momentum/breakout.
- Filtro extra de volatilidad usando ATR.
- Relación aproximada TP/SL favorable: 2.4 / 1.3 ≈ 1.85.
- No está sobrecargada de condiciones.
- Fácil de explicar y auditar.
```

Riesgos:

```text
- Puede sufrir en rangos laterales con falsos breakouts.
- Es sensible a slippage por entrar en ruptura.
- No tiene trailing ni break-even.
- Solo opera long, por lo que depende de regímenes alcistas o expansiones bullish.
```

Veredicto lógico:

```text
APTA PARA PRE-PORTAFOLIO
Prioridad: Alta
```

Regla aprendida:

```text
Si una estrategia muestra buen desempeño cuantitativo y además su lógica es simple, coherente y explicable, sube de prioridad frente a estrategias con métricas similares pero lógica más ambigua o redundante.
```

---

## 32. Cierre de la Skill 2

Con esta actualización, la Skill 2 queda cerrada como motor de validación robusta individual.

Flujo final completo:

```text
Builder
→ OOS
→ MC Trades
→ MC Retest / Spread-Slippage
→ Retest Tick / Real Spread / Slowest
→ SPP
→ WFA Matrix
→ WFA individual
→ Ranking integral pre-MT5
→ Retest MT5
→ Comparación SQX Tick vs MT5
→ Lectura cualitativa del edge por reglas
→ Veredicto pre-portafolio / incubación / descarte
```

Regla final:

```text
Una estrategia candidata robusta no solo debe pasar pruebas cuantitativas. También debe tener una lógica de mercado coherente, comprensible, no excesivamente redundante y compatible con el objetivo de portafolio.
```



---

## 33. Enmienda V1.3 — Proporcionalidad por ventana usada

Esta enmienda agrega una regla transversal para todas las etapas de robustez:

```text
Los filtros se calculan con base en la data realmente usada por la etapa, no con base en toda la data disponible del activo.
```

Aplicación:

```text
- OOS: mínimos de trades y umbrales según meses reales de OOS.
- MC Trades: aceptación según el comportamiento original de la muestra evaluada.
- MC Spread/Slippage: intensidad según activo, broker, cuenta, timeframe, tipo de entrada y AvgTrade.
- Tick: filtros según data tick realmente usada.
- SPP: intensidad según cantidad real de trades.
- WFA Matrix: ventanas coherentes con muestra, timeframe y trades por ventana.
```

Regla final:

```text
No siempre más data significa mejor validación.
La robustez útil es proporcional, contextual y alineada con el régimen que se quiere operar.
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


## Aplicación específica en Skill 2 — Robustez OOS

La Skill 2 debe rechazar configuraciones donde la etapa OOS evalúe una muestra fuera de rango sin excepción documentada. Esto no significa endurecer arbitrariamente los filtros; significa que la ventana de validación debe ser lo bastante representativa antes de calibrar filtros.

Checklist adicional de Skill 2:

```text
[ ] Meses_OOS_reales calculados.
[ ] OOS% detectado entre 20% y 30%.
[ ] MinTradesOOS calculado por meses OOS reales.
[ ] PF, Ret/DD, DD%, AvgTrade y Stagnation calibrados por ventana real.
[ ] No se usan filtros de toda la historia para una ventana OOS parcial.
```


---

# Actualización V1.5 — Compatibilidad con Session Existing Safe y Short Project Names

## 27. Motivo

Las pruebas de robustez OOS, MC_TRADES, MC_SPREAD_SLIPPAGE, TICK, SPP y WFA MATRIX pueden fallar al importar aunque los filtros estén bien configurados si el `.cfx` hereda una sesión embebida incompatible o un Project name demasiado largo.

Esta actualización no cambia la lógica estadística de robustez. Agrega una regla de compatibilidad técnica para que cada etapa conserve la política de recursos definida por el Orchestrator.

## 28. Regla de sesión por etapa

Las etapas de robustez no deben corregir, inventar ni incrustar sesiones.

Por defecto deben conservar:

```text
Session existing reference validada por Skill 3/Skill 4.
<Sessions /> vacío si la sesión ya existe en Data Manager.
LimitTimeRange=false salvo donor session probado.
```

Bloquear una etapa si:

```text
Aparece No Session como sesión funcional XML.
Aparece una sesión con corchetes generada por inferencia y no por Data Manager.
La etapa incrusta un bloque <Session> que no viene de donor .cfx probado.
LimitTimeRange=true aparece sin donor compatible.
```

## 29. Regla de nombres cortos para etapas de robustez

Cada `.cfx` de etapa debe usar Project name corto:

```text
Preferido <= 25 caracteres.
Máximo permitido <= 30 caracteres.
```

Ejemplos:

```text
GBPDP_E3_H1MR_OOS_V1
GBPDP_E3_H1MR_TICK_V1
GBPDP_E3_H1MR_WFA_V1
```

Evitar:

```text
GBPUSD_DP_E3_H1_MEAN_REVERSION_BOTH_V6_BROKERSESSION_EXISTING
```

## 30. Smoke test técnico antes de evaluar robustez

Antes de interpretar resultados estadísticos, confirmar que la etapa:

```text
Importa desde ruta corta.
No falla con Cannot resolve custom resources.
No falla con Failed to update zip content.
Abre con Data Banks correctos.
Conserva sesión existente o no usa filtro horario nativo.
Presiona Start.
```

Si falla en importación, no es fallo de robustez; es fallo técnico de recursos.

## 31. Regla final V1.5

```text
La robustez se evalúa solo después de que el .cfx importó y arrancó.
Un fallo de sesión, ZIP interno o Project name no debe interpretarse como degradación de estrategia.
```
