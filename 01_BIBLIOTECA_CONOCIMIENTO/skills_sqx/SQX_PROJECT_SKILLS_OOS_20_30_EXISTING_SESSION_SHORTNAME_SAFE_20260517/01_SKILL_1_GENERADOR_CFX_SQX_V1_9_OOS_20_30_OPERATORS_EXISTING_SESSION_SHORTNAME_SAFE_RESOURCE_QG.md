# Skill Final Operativa V1.8 — Generador de Templates `.cfx` para StrategyQuant X Builder con Control Anti-Permisividad y Data Bank Quality Gate Multi-Timeframe

**Propósito:** crear templates `.cfx` importables en StrategyQuant X Builder a partir de una data diaria del activo, un `.cfx` base, un diccionario de rutas/nodos, un diccionario de métricas de ranking y las preferencias operativas del usuario.

**Estado:** Skill Final Operativa V1.7 con Operators Safe, Resource Safe, Quality Gate, Session Resource Safe y OOS 20–30. Reemplaza V1.3 y agrega Quality Gate multi-timeframe para M15/M30/H1/H4/D1. Mantiene la lógica de generación de edges, selección crítica de timeframe y ventanas de data, y agrega una regla obligatoria de control anti-permisividad del Builder para evitar que ventanas largas acepten estrategias débiles por filtros demasiado blandos.

---

## 1. Principio rector

La IA no debe modificar libremente el `.cfx`. El flujo obligatorio es:

1. Recibir inputs del usuario.
2. Validar archivos técnicos.
3. Analizar la data diaria.
4. Diagnosticar régimen/ciclo del activo.
5. Elegir timeframe por edge, régimen, objetivo, frecuencia esperada, sensibilidad a costos y robustez.
6. Seleccionar el periodo Builder/IS y OOS con criterio; la data disponible es universo máximo, no periodo obligatorio.
7. Seleccionar edge o familia de edges.
8. Traducir cada edge a configuración Builder.
9. Construir Ranking Final y Genetic Options desde cero.
10. Activar Cross Checks solo si el usuario los solicita o si el preset lo exige explícitamente.
11. Modificar únicamente nodos autorizados.
12. Validar que no se tocaron nodos protegidos.
13. Entregar `.cfx` final y reporte ejecutivo.

Regla base: **la IA propone la configuración; el patcher modifica nodos permitidos; el validador confirma que el `.cfx` final sigue siendo coherente e importable.**

---

## 2. Archivos técnicos del sistema

### 2.1 `.cfx` base

Uso correcto:

- Contenedor técnico editable.
- Fuente de estructura XML compatible con SQX.
- Punto de partida para generar el archivo final.

Uso prohibido:

- No tomarlo como configuración correcta.
- No heredar ranking sin criterio.
- No heredar edge sin criterio.
- No tomar sus costos como modificables.
- No asumir que sus Cross Checks son adecuados.

Regla: todo lo reutilizado del `.cfx` base debe justificarse. Si no está justificado, se reconstruye desde el objetivo, activo, broker, data, edge y restricciones del usuario.

### 2.2 Archivo de rutas del Builder

Se usa como diccionario técnico para:

- Building Blocks.
- Signals.
- Indicators.
- Comparadores funcionales.
- StopLimitBlocks.
- Order Types.
- Exit Types.
- Break Even.
- Trailing Stop.
- Stop Loss.
- Profit Target.
- Exit After Bars.

Regla: el archivo de rutas sirve como diccionario técnico, pero cada `.cfx` cargado debe validarse directamente antes de modificarlo.

### 2.3 `ranking.cfx`

Se usa como diccionario técnico de métricas de ranking. No es template operativo.

Métricas confirmadas para usar si existen en el mapa:

- `NetProfit`
- `ProfitFactor`
- `ReturnDDRatio`
- `DrawdownPct`
- `NumberOfTrades`
- `AvgTrade`
- `AvgTradesPerDay`
- `AvgTradesPerYear`
- `SharpeRatio`
- `RSquared`
- `WinningPct`
- `Expectancy`
- `RExpectancy`
- `SQN`
- `SQNScore`
- `Stability`
- `StabilitySQ3`
- `Stagnation`
- `StagnationPct`
- `PayoutRatio`
- `WinLossRatio`
- `ProfitableMonthsPct`
- `CalmarRatio`
- `CAGR`
- `RecoveryFactor`
- `UlcerIndex`
- `UlcerPerformanceIndex`
- `WorstYearProfit`
- `ZScore`
- `ZProbability`

Regla: el Ranking Final se construye desde cero según edge, objetivo, timeframe, periodo de datos y preferencias del usuario.

---

## 3. Inputs obligatorios

El usuario debe proporcionar o confirmar:

- `.cfx` base.
- Archivo de rutas/nodos del Builder.
- `ranking.cfx` o mapa de métricas ya extraído.
- Data diaria del activo.
- Rango total de data disponible.
- Restricción explícita sobre usar toda la data, si existe.
- Activo principal.
- Broker.
- Tipo de cuenta.
- Símbolo de construcción.
- Objetivo del template.
- Temporalidades permitidas o candidatas.
- Timeframe elegido por la IA, si el usuario autoriza decidirlo por edge.
- Número de edges deseados.
- Restricciones explícitas: qué NO se debe tocar.

Formato recomendado de mandato:

```text
Activo:
Broker:
Tipo de cuenta:
Símbolo de construcción:
Símbolo de validación:
Objetivo:
Temporalidades permitidas/candidatas:
¿La IA puede elegir timeframe por edge?:
Número de edges:
Dirección preferida, si aplica:
Cross Checks solicitados:
Restricciones / nodos que NO se deben tocar:
Data disponible:
¿Usar toda la data o seleccionar ventana con criterio?:
Periodo IS/OOS deseado:
```

Ejemplo:

```text
Activo: EURUSD
Broker: DooPrime
Cuenta: Cent
Símbolo de construcción: EURUSD normal
Símbolo de validación: EURUSD.c tick data
Objetivo: incubación para trackrecord
Temporalidades: H1, H4
Edges: 3
Dirección: definir según análisis
Cross Checks: additional market retest y tick retest
Restricciones: no tocar spread, slippage ni money management
Data diaria: adjunta
Periodo IS: 2012-2022
OOS: 2023-2026
```

---

## 4. Protección de nodos sensibles

Estos nodos quedan protegidos por defecto:

- Spread.
- Slippage.
- Commission.
- Swap.
- Point value.
- Tick size.
- Pip value.
- Broker profile.
- Instrument info.
- Money Management.
- Initial Capital.
- Risked Money.
- Recursos internos del broker.
- Recursos internos del instrumento.
- Custom indicators.
- Custom blocks.
- Java snippets.

Regla: no modificar costos operativos, propiedades económicas del activo ni money management salvo orden explícita del usuario.

Ejemplos de órdenes explícitas válidas:

```text
Cambia el spread a 0.7.
Cambia el slippage a 1.
Usa EURUSD.c como símbolo de validación.
Cambia el timeframe a H1.
Configura test precision en tick.
```

Si el usuario no da permiso, esos valores permanecen como estén en el `.cfx` base.

---

## 5. Nodos editables

### 5.1 Editables bajo orden del usuario

- Símbolo principal de construcción.
- Símbolo de validación.
- Timeframe.
- Fecha inicial.
- Fecha final.
- Test precision.
- Retest on Additional Markets.
- Higher Precision Retest.
- Monte Carlo Retest.
- Monte Carlo Manipulation.
- SPP.
- WFA.
- WFA Matrix.
- What If.

### 5.2 Editables según edge/objetivo

- `StrategyType`.
- `MarketSides`.
- `RulesComplexity`.
- `SLPTOptions`.
- `BuildMode`.
- Genetic Options.
- Genetic prefilters.
- Ranking Final.
- Final filters.
- Max Strategies.
- Stop Condition.
- Dismiss Similar Strategies.
- Building Blocks.
- Signals.
- Indicators.
- Comparadores funcionales.
- StopLimitBlocks.
- Order Types.
- Exit Types.
- Break Even.
- Trailing.
- Exit After Bars.

Regla: estos nodos no se copian mecánicamente de la base; se reconstruyen según objetivo, edge, régimen, timeframe y restricciones del usuario.

---

## 6. Clasificación del objetivo

### 6.1 Incubación / trackrecord

Prioridades:

- Robustez.
- Bajo sobreajuste.
- Buen comportamiento OOS.
- Drawdown controlado.
- Stagnation razonable.
- Average Trade suficiente.
- Compatibilidad con ejecución real.
- No perseguir rentabilidad exagerada.

Ranking recomendado:

- Fitness principal: `ReturnDDRatio`.
- Filtros secundarios: `ProfitFactor`, `DrawdownPct`, `StagnationPct`, `NumberOfTrades`, `AvgTrade`.
- Opcionales: `SharpeRatio`, `RSquared`, `Stability`, `ProfitableMonthsPct`.

### 6.2 Prop firm / fondeo

Prioridades:

- Drawdown bajo.
- Baja exposición.
- Control de rachas negativas.
- Estabilidad de curva.
- Riesgo operativo moderado.

Ranking recomendado:

- Fitness principal: `ReturnDDRatio`, `SharpeRatio` o `RecoveryFactor`.
- Filtros: `DrawdownPct`, `StagnationPct`, `ProfitFactor`, `AvgTrade`, `NumberOfTrades`.
- Opcionales: `Stability`, `RSquared`, `UlcerIndex`, `UlcerPerformanceIndex`.

### 6.3 Portafolio conservador

Prioridades:

- Baja varianza.
- Drawdown bajo.
- Estabilidad.
- Baja stagnation.
- Curva suave.

Ranking recomendado:

- Fitness: `ReturnDDRatio` o `SharpeRatio`.
- Filtros: `ProfitFactor`, `DrawdownPct`, `StagnationPct`, `Stability`, `RSquared`, `AvgTrade`.

### 6.4 Portafolio agresivo

Prioridades:

- Mayor retorno.
- Mayor tolerancia a variabilidad.
- Buen payout.
- Capacidad de recuperación.

Ranking recomendado:

- Fitness: `ReturnDDRatio`, `RecoveryFactor` o métrica equivalente disponible.
- Filtros: `ProfitFactor` suave, `DrawdownPct` más amplio, `PayoutRatio`, `AvgTrade`, `StagnationPct` más tolerante.

---

## 7. Análisis de data diaria y diagnóstico de régimen

Antes de elegir edges, la skill debe clasificar el activo según:

```text
Régimen = Tendencia × Volatilidad
```

### 7.1 Ejes del régimen

Tendencia:

- Alcista.
- Lateral.
- Bajista.

Puede estimarse con pendiente de medias, retorno acumulado, estructura de máximos/mínimos, regresión lineal, ADX si está disponible y persistencia del retorno.

Volatilidad:

- Alta.
- Media.
- Baja.

Puede estimarse con ATR relativo, rango diario promedio, desviación estándar de retornos, percentiles históricos y comparación de volatilidad reciente contra histórica.

### 7.2 Ventanas de análisis

Usar varias ventanas:

- Ventana larga: 5 a 10 años, si hay data.
- Ventana media: 1 a 3 años.
- Ventana reciente: 3 a 12 meses.

La ventana larga define contexto estructural, la media define fase dominante y la reciente define régimen actual.

### 7.2.1 Selección crítica de timeframe y ventanas de data

Regla principal:

```text
La temporalidad no debe heredarse del `.cfx` base.
La data disponible no debe usarse completa por defecto.
```

El `.cfx` base es un contenedor técnico. Sus fechas y timeframe solo se conservan si coinciden con el diagnóstico del activo, el edge, el objetivo y la calidad de la data.

### 7.2.2 Criterios para elegir timeframe

Para cada edge se debe decidir el timeframe de forma explícita, usando:

```text
- Régimen actual y régimen secundario.
- Sesgo estructural y reciente.
- Familia de edge.
- Objetivo operativo: incubación, fondeo, portafolio conservador o agresivo.
- Cantidad esperada de trades.
- Sensibilidad a spread, slippage y comisión.
- Tipo de entrada: Market, Stop o Limit.
- Compatibilidad con robustez posterior: OOS, Tick, SPP y WFA.
- Ruido operativo del activo.
```

Guía operativa:

```text
H1:
- Más útil para expansión de volatilidad, breakout, sesión, momentum intradía y edges que necesitan frecuencia.
- Mayor sensibilidad a spread/slippage.
- Requiere filtros de ejecución más cuidadosos.

H4:
- Más útil para mean reversion selectiva, pullback, continuation y trend suave.
- Reduce ruido y sensibilidad a costos.
- Puede producir menos trades; los mínimos deben calibrarse con prudencia.

D1:
- Solo usar si el edge es estructural, trend/pullback de largo plazo o calendario.
- Riesgo de muestra pobre si hay pocos trades.
- No forzar D1 solo por tener mucha data histórica.
```

Si se trabajan varios edges, pueden existir varios timeframes. No se debe forzar un único timeframe para todos los edges salvo que exista una razón operativa.

### 7.2.3 Criterios para seleccionar periodo Builder/IS y OOS

La data disponible es el universo máximo, no el periodo obligatorio de minería.

El periodo Builder/IS debe seleccionarse según:

```text
- Relevancia del régimen histórico frente al régimen actual.
- Similitud de ciclos de volatilidad y tendencia.
- Calidad, continuidad y limpieza de la data.
- Representatividad del ciclo reciente.
- Suficiencia de muestra para el timeframe y edge.
- Necesidad de evitar ciclos demasiado antiguos que ya no representen el comportamiento operativo actual.
- Riesgo de sobreajuste por ventana demasiado corta.
```

El OOS debe elegirse para validar generalización y actualidad, no como residuo automático. Debe ser lo bastante reciente para representar el mercado actual y lo bastante largo para que sus filtros sean estadísticamente proporcionales.

### 7.2.4 Cuándo usar toda la data

Usar toda la data solo cuando:

```text
- La calidad es consistente en todo el histórico.
- El edge es estructural y no depende de microestructura reciente.
- El régimen histórico contiene ciclos relevantes y comparables al actual.
- La muestra completa no introduce periodos obsoletos que distorsionen la minería.
- La cantidad de trades esperada necesita una ventana larga.
```

No usar toda la data cuando:

```text
- Hay cambios claros de régimen, liquidez, broker, spread o comportamiento del activo.
- La data antigua genera edges que no sobreviven al ciclo reciente.
- El timeframe es bajo y la sensibilidad a costos cambió con el tiempo.
- El objetivo es fondeo/incubación actual y la validación reciente pesa más que la historia vieja.
```

Salida obligatoria adicional del diagnóstico:

```text
Selección de timeframe y data:
- Timeframes candidatos:
- Timeframe elegido por edge:
- Data total disponible:
- Periodo Builder/IS elegido:
- Periodo OOS elegido:
- Data descartada o no usada:
- Motivo de usar toda la data o recortar ventana:
- Riesgo principal de la selección:
```


### 7.3 Matriz de 9 regímenes

| Régimen | Clasificación | Interpretación | Edges prioritarios |
|---|---|---|---|
| 1 | Alcista + volatilidad alta | Breakouts / momentum fuerte | Breakout, momentum, volatility expansion, trend rápido |
| 2 | Lateral + volatilidad alta | Whipsaw / falsas rupturas | Mean reversion selectiva, post-impulse reversion, session reversion |
| 3 | Bajista + volatilidad alta | Caídas rápidas / pánico | Breakout short, momentum short, trend short |
| 4 | Alcista + volatilidad media | Tendencia suave | Trend following, pullback, continuation |
| 5 | Lateral + volatilidad media | Rango medio | Mean reversion, range trading, session reversion |
| 6 | Bajista + volatilidad media | Desgaste bajista | Trend short, pullback short, continuation short |
| 7 | Alcista + volatilidad baja | Rally silencioso | Pullback, trend suave, low-vol momentum |
| 8 | Lateral + volatilidad baja | Compresión pre-ruptura | Volatility compression breakout, session breakout, mean reversion selectiva |
| 9 | Bajista + volatilidad baja | Goteo bajista | Trend short suave, pullback short, continuation short |

Salida obligatoria del diagnóstico:

```text
Diagnóstico de régimen:
- Tendencia larga:
- Tendencia media:
- Tendencia reciente:
- Volatilidad larga:
- Volatilidad media:
- Volatilidad reciente:
- Régimen actual según matriz 3x3:
- Régimen secundario:
- Edges priorizados:
- Edges descartados:
- Justificación:
```

Regla: no generar `.cfx` sin diagnóstico previo, salvo que el usuario pida explícitamente omitir el análisis.

---

## 8. Edge Registry ampliado

La skill no debe limitarse a edges clásicos. Puede proponer edges estacionales, de sesión, horario, volatilidad, híbridos o raros siempre que sean simples, programables y validables.

Familias de edge:

1. Mean Reversion.
2. Breakout.
3. Trend Following.
4. Pullback / Continuation.
5. Seasonal / Calendar.
6. Session-Based.
7. Day-of-Week.
8. Time-of-Day.
9. Volatility Expansion.
10. Volatility Compression.
11. Post-Impulse Reversion.
12. Session Momentum.
13. Gap Fill / Gap Continuation.
14. Hybrid Edges.
15. Experimental / Rare Edges.

Cada edge seleccionado debe tener ficha:

```text
Nombre del edge:
Tesis estructural:
Régimen en el que aplica:
Régimen en el que no aplica:
Timeframes sugeridos:
Dirección preferente:
Building Blocks:
Comparadores:
Order Types:
Exit Types:
Ranking recomendado:
Filtros prohibidos:
Cross Checks recomendados:
Riesgos de sobreajuste:
```

Si un edge no puede traducirse con los bloques disponibles, declarar que no es implementable directamente en Builder, proponer una aproximación o marcarlo como candidato para Custom Block / AlgoWizard.

---

## 9. Dirección operativa: long, short o both

La dirección no debe heredarse del `.cfx` base ni dejarse en `both` por comodidad. Debe definirse a partir de la data, el régimen, el edge y el objetivo.

Regla fundamental: **MarketSides debe ser una decisión explícita basada en data + régimen + edge.**

### 9.1 Cuándo usar long-only

Usar `long` cuando:

```text
- El régimen principal es alcista.
- El sesgo estructural y reciente favorece compras.
- El edge es trend following alcista.
- El edge es pullback/continuation en tendencia alcista.
- El edge es buy-the-dip o post-impulse reversion a favor de tendencia.
- El objetivo es incubación/trackrecord y se quiere evitar operar contra el sesgo dominante.
```

Ejemplo validado:

```text
USDJPY con sesgo alcista estructural + volatilidad media:
- Trend/Pullback Continuation = long-only.
- Volatility Expansion Breakout = long-only en la primera versión alineada al régimen.
- Post-Impulse Reversion = long-only tipo buy-the-dip.
```

### 9.2 Cuándo usar short-only

Usar `short` cuando:

```text
- El régimen principal es bajista.
- El sesgo estructural y reciente favorece ventas.
- El edge es trend following bajista.
- El edge es pullback/continuation short.
- El edge es breakdown / volatility expansion bajista.
- El edge es sell-the-rally en tendencia bajista.
```

### 9.3 Cuándo usar both

Usar `both` solo cuando:

```text
- La tesis del edge es simétrica.
- El régimen es lateral sin sesgo direccional claro.
- El objetivo es exploración controlada.
- El edge es mean reversion neutral en rango.
- El usuario pide explícitamente long y short.
- Se busca descubrir familias en ambas direcciones y luego filtrar.
```

Ejemplo validado:

```text
EURUSD lateral + volatilidad baja:
- Mean Reversion Selectiva = both puede tener sentido.
- Volatility Compression Breakout = both puede tener sentido si la ruptura puede darse en cualquier dirección.
```

### 9.4 Dirección por edge

```text
Trend Following:
- Usar dirección del régimen dominante.
- No usar both si la data muestra sesgo fuerte.

Pullback / Continuation:
- Usar dirección del sesgo dominante.
- En régimen alcista: long-only.
- En régimen bajista: short-only.

Breakout / Volatility Expansion:
- Usar both solo si el régimen es lateral/neutral.
- Usar long-only en régimen alcista.
- Usar short-only en régimen bajista.

Mean Reversion:
- Both si el mercado es lateral y simétrico.
- Long-only si el edge es buy-the-dip en régimen alcista.
- Short-only si el edge es sell-the-rally en régimen bajista.

Session / Time-of-Day:
- Definir según sesgo horario detectado.
- No asumir both.
```

### 9.5 Variantes direccionales

Si existe duda, no mezclar todo en un solo template. Crear variantes separadas:

```text
EDGE_LONG.cfx
EDGE_SHORT.cfx
EDGE_BOTH_EXPLORATORY.cfx
```

Regla: **para usuario final, si la data muestra sesgo claro, entregar primero la versión direccional alineada al régimen. Las versiones contrarias deben ser opcionales y justificadas.**

---

## 10. Building Blocks, entradas, salidas y trade management

Regla fundamental: no activar bloques al azar ni activar todos los bloques disponibles. Cada template debe representar una hipótesis clara.

Lógica obligatoria:

```text
Edge → tesis → régimen → timeframe → señales → indicadores → comparadores → entradas → salidas → ranking
```

### 10.1 Order Types disponibles

- `EnterAtMarket`.
- `EnterReverseAtMarket`.
- `EnterAtStop`.
- `EnterAtLimit`.

Uso recomendado:

- Mean Reversion: `EnterAtMarket`, `EnterAtLimit` opcional.
- Breakout: `EnterAtStop`, `EnterAtMarket` opcional.
- Trend Following: `EnterAtMarket`, `EnterAtStop` opcional.
- Pullback: `EnterAtMarket`, `EnterAtLimit` opcional, `EnterAtStop` si se busca confirmación.
- Session Momentum: `EnterAtMarket`, `EnterAtStop`.
- Gap Fill: `EnterAtMarket`, `EnterAtLimit`.
- Gap Continuation: `EnterAtMarket`, `EnterAtStop`.

`EnterReverseAtMarket` no debe activarse por defecto. Requiere justificación explícita.

### 10.2 Exit Types disponibles

- `ExitAfterBars.ExitAfterBars`.
- `MoveSL2BE.MoveSL2BE`.
- `MoveSL2BE.SL2BEAddPips`.
- `ProfitTarget.ProfitTarget`.
- `StopLoss.StopLoss`.
- `TrailingStop.TrailingStop`.
- `TrailingStop.TrailingActivation`.
- `_ExitRule_`.

Reglas:

- `StopLoss` debe estar activo salvo excepción explícita.
- `ProfitTarget` encaja mejor con reversión, pullback y sesión.
- `TrailingStop` encaja mejor con trend, breakout, momentum y volatility expansion.
- `ExitAfterBars` ayuda en mean reversion, pullback, sesión y post-impulse reversion.
- `MoveSL2BE` no se activa por defecto; puede destruir expectancy si corta ganadores.
- `TrailingActivation` debe evaluarse si se activa trailing.
- `ExitRule` debe ser simple y coherente con la entrada.

### 9.3 Comparadores funcionales

Comparadores disponibles:

- `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`.
- `Equals`, `NotEquals`.
- `CrossesAbove`, `CrossesBelow`.
- `IsRising`, `IsFalling`.
- `IsGreaterCount`, `IsLowerCount`.
- `IsGreaterPercentil`, `IsLowerPercentil`.
- `IndicatorCrossesAboveMA`, `IndicatorCrossesBelowMA`.

Ejemplos válidos:

```text
RSI + IsLower
RSI + IsGreater
RSI + CrossesAbove
RSI + CrossesBelow
MA + IsRising
MA + IsFalling
Close + CrossesAbove + MA
ATR + IsGreater
High/Low + CrossesAbove/CrossesBelow
```

---

## 10. Perfiles operativos por edge

### 10.1 Mean Reversion

Tesis: el precio corrige después de una sobreextensión relativa.

Bloques: RSI, Keltner/Bollinger si disponibles, ATR, Close, High, Low.

Comparadores: `IsGreater`, `IsLower`, `CrossesAbove`, `CrossesBelow`, `IsRising`, `IsFalling`.

Entradas: `EnterAtMarket`, `EnterAtLimit` opcional. Evitar `EnterAtStop`.

Salidas: `StopLoss`, `ProfitTarget`, `ExitAfterBars`, `MoveSL2BE` opcional. Evitar trailing agresivo.

Ranking: `ProfitFactor`, `WinningPct`, `ReturnDDRatio`, `AvgTrade`, `DrawdownPct`, `StagnationPct`, `NumberOfTrades`.

### 10.2 Breakout

Tesis: la ruptura de rangos o niveles genera continuación por expansión.

Bloques: ATR, High, Low, Close, Highest/Lowest si disponibles, canales, StopLimitBlocks.

Entradas: `EnterAtStop`, `EnterAtMarket` opcional con confirmación.

Salidas: `StopLoss`, `ProfitTarget` opcional, `TrailingStop` opcional, `TrailingActivation` opcional, `ExitAfterBars` opcional.

Ranking: `ReturnDDRatio`, `AvgTrade`, `PayoutRatio`, `DrawdownPct`, `StagnationPct`, `ProfitFactor` suave, `NumberOfTrades`. No exigir `WinningPct` alto.

### 10.3 Trend Following

Tesis: la persistencia direccional permite capturar movimientos extendidos.

Bloques: Moving Average, EMA, ATR, ADX si disponible, Close, High, Low.

Entradas: `EnterAtMarket`, `EnterAtStop` opcional.

Salidas: `StopLoss`, `TrailingStop` opcional, `TrailingActivation` opcional, `ProfitTarget` opcional, `ExitAfterBars` opcional no demasiado corto, `ExitRule` opcional por señal contraria.

Ranking: `ReturnDDRatio`, `SharpeRatio` opcional, `AvgTrade`, `PayoutRatio`, `RecoveryFactor`, `DrawdownPct`, `StagnationPct`, `ProfitFactor` suave. No exigir winrate alto.

### 10.4 Pullback / Continuation

Tesis: el mercado retrocede dentro de una estructura direccional y luego continúa.

Bloques: Moving Average, EMA, RSI, ATR, Close, High, Low.

Entradas: `EnterAtMarket`, `EnterAtLimit` opcional, `EnterAtStop` si se busca confirmación.

Salidas: `StopLoss`, `ProfitTarget`, `ExitAfterBars`, `MoveSL2BE` opcional, `TrailingStop` suave opcional.

Ranking: `ReturnDDRatio`, `ProfitFactor`, `WinningPct` moderado, `AvgTrade`, `DrawdownPct`, `StagnationPct`, `NumberOfTrades`.

### 10.5 Session-Based / Time-of-Day

Tesis: el comportamiento cambia según sesión u hora.

Aplicaciones: Asia, Londres, Nueva York, solapamientos, aperturas, cierres, horas de baja liquidez o expansión.

Entradas:

- Reversión de sesión: `EnterAtMarket`, `EnterAtLimit` opcional.
- Momentum de sesión: `EnterAtMarket`, `EnterAtStop`.
- Ruptura de sesión: `EnterAtStop`.

Salidas: `StopLoss`, `ProfitTarget`, `ExitAfterBars`, cierre horario si existe, trailing opcional para momentum.

Regla: no mezclar demasiadas sesiones en un mismo template.

### 10.6 Seasonal / Calendar

Tesis: ciertos periodos del calendario presentan sesgos repetitivos.

Aplicaciones: mes del año, semana del mes, inicio/fin de mes, día de semana, fin de trimestre.

Regla: no aceptar edge estacional con pocos trades. Alto riesgo de sobreajuste por calendario.

Ranking: `ProfitFactor`, `ReturnDDRatio`, `NumberOfTrades`, `AvgTrade`, `DrawdownPct`, `StagnationPct`, `ProfitableMonthsPct`.

### 10.7 Volatility Expansion / Compression

Tesis: cambios de volatilidad generan oportunidades de ruptura, continuación o reversión.

Bloques: ATR, High, Low, Close, rango, Keltner/Bollinger si disponibles.

Entradas:

- Expansión: `EnterAtStop`, `EnterAtMarket` con confirmación.
- Reversión tras volatilidad: `EnterAtMarket`, `EnterAtLimit` opcional.

Salidas: `StopLoss`, `ProfitTarget` opcional, `TrailingStop` opcional para expansión, `ExitAfterBars` opcional.

Ranking: `ReturnDDRatio`, `AvgTrade`, `ProfitFactor`, `DrawdownPct`, `StagnationPct`, `PayoutRatio` si es expansión/breakout.

### 10.8 Hybrid / Rare Edges

Un edge raro solo se acepta si es:

1. Simple.
2. Programable en SQX.
3. Basado en comportamiento de mercado.
4. Con suficientes trades.
5. Validable en OOS/retest.
6. No dependiente de una combinación absurda de reglas.

Evitar combinar BE + trailing + exit rule + demasiados filtros sin justificación.

---

## 11. Genetic Options

Genetic Options es la capa de evolución, no el filtro final.

Regla fundamental: **Genetic Options debe ser más flexible que Ranking Final.**

### 11.1 Genetic prefilters permitidos

- `NumberOfTrades` mínimo dinámico suave.
- `NetProfit > 0`, opcional.
- `ProfitFactor > 1.00` a `1.03`.
- `DrawdownPct` amplio, solo si el Builder genera demasiada basura.
- `AvgTrade > 0`, si no ahoga la búsqueda.

### 11.2 Genetic prefilters no recomendados

No usar al inicio:

- `ReturnDDRatio` alto.
- `SharpeRatio` alto.
- `WinningPct` alto.
- `RSquared` alto.
- `Stability` alto.
- `StagnationPct` estricta.
- `ProfitFactor > 1.15`.
- `DrawdownPct` demasiado estricto.
- `PayoutRatio` exigente.

### 11.3 Cálculo de MinTradesGenetic

```text
Meses_IS = meses entre dateFrom y dateTo
MinTradesFinal = Meses_IS × AvgTradesPerMonthFinal
MinTradesGenetic = MinTradesFinal × 0.40 a 0.70
```

Guía:

- H1: 50% a 70% del mínimo final.
- H4: 40% a 60% del mínimo final.
- D1: 35% a 50% del mínimo final.

Si el Builder no genera población, reducir primero filtros genéticos antes de tocar ranking final, bloques o costos.

### 11.4 Population Size y Max Generations

Búsqueda enfocada:

```text
Population Size: 150 a 300
Max Generations: 80 a 150
```

Búsqueda amplia/controlada:

```text
Population Size: 250 a 500
Max Generations: 100 a 250
```

Búsqueda exploratoria pesada:

```text
Population Size: 500+
Max Generations: 200+
```

No aumentar Population Size para compensar una mala selección de bloques.

---

## 12. Ranking Final

El Ranking Final decide qué estrategias pasan al Data Bank. No se hereda del `.cfx` base.

Capas obligatorias:

1. Fitness principal.
2. Filtros mínimos de supervivencia.
3. Filtros específicos del edge.
4. Filtros específicos del objetivo.
5. Filtros dinámicos según periodo de datos.
6. Filtros opcionales según métricas disponibles.

### 12.1 Fitness recomendado por objetivo

- Incubación / trackrecord: `ReturnDDRatio`; alternativas `ProfitFactor`, `SharpeRatio`, `RecoveryFactor`.
- Fondeo: `ReturnDDRatio`, `SharpeRatio`, `RecoveryFactor`; evitar `NetProfit` como criterio único.
- Portafolio conservador: `ReturnDDRatio`, `SharpeRatio`; secundarios `Stability`, `RSquared`, `UlcerPerformanceIndex`.
- Portafolio agresivo: `ReturnDDRatio`, `RecoveryFactor`; secundarios `NetProfit`, `PayoutRatio`, `CAGR`.

### 12.2 Cálculo dinámico de NumberOfTrades

```text
Meses_IS = meses entre dateFrom y dateTo
MinTradesFinal = Meses_IS × AvgTradesPerMonthFinal
```

Guía por timeframe:

```text
H1:
- Mean Reversion / Pullback: 1.5 a 5 trades/mes
- Breakout / Trend: 1 a 3 trades/mes
- Sesión / horario: 1.5 a 6 trades/mes

H4:
- Mean Reversion / Pullback: 0.8 a 3 trades/mes
- Breakout / Trend: 0.5 a 2 trades/mes
- Volatilidad / compresión: 0.5 a 2 trades/mes

D1:
- Trend / Breakout: 0.2 a 1.2 trades/mes
- Estacional / calendario: depende del evento, pero debe mantener muestra suficiente
```

### 12.3 Ranking base para incubación

```text
Fitness:
- ReturnDDRatio

Filtros base:
- NumberOfTrades > MinTradesFinal
- ProfitFactor > 1.08 a 1.20
- ReturnDDRatio > 2.0 a 3.5
- DrawdownPct < 25 a 35
- StagnationPct < 20 a 35
- AvgTrade > 0, o mayor a umbral mínimo si está disponible
```

Opcionales: `SharpeRatio`, `RSquared`, `Stability`, `ProfitableMonthsPct` con umbrales suaves.

### 12.4 Ranking por edge

Mean Reversion:

- Priorizar `ProfitFactor`, `WinningPct`, `ReturnDDRatio`, `AvgTrade`, `DrawdownPct`, `StagnationPct`, `NumberOfTrades`.
- Evitar `PayoutRatio` alto y `RSquared` demasiado alto.

Breakout:

- Priorizar `ReturnDDRatio`, `AvgTrade`, `PayoutRatio`, `DrawdownPct`, `StagnationPct`, `ProfitFactor` suave, `NumberOfTrades`.
- Evitar `WinningPct > 50%` como filtro obligatorio.

Trend Following:

- Priorizar `ReturnDDRatio`, `SharpeRatio`, `AvgTrade`, `PayoutRatio`, `RecoveryFactor`, `DrawdownPct`, `StagnationPct`.
- Evitar winrate alto.

Pullback / Continuation:

- Priorizar `ReturnDDRatio`, `ProfitFactor`, `WinningPct` moderado, `AvgTrade`, `DrawdownPct`, `StagnationPct`, `NumberOfTrades`.

Seasonal / Calendar:

- Priorizar `ProfitFactor`, `ReturnDDRatio`, `NumberOfTrades`, `AvgTrade`, `DrawdownPct`, `StagnationPct`, `ProfitableMonthsPct`.
- No aceptar pocos trades.

Session-Based / Time-of-Day:

- Priorizar `AvgTrade`, `ProfitFactor`, `ReturnDDRatio`, `NumberOfTrades`, `DrawdownPct`, `StagnationPct`, `SharpeRatio` opcional.

Volatility Expansion / Compression:

- Priorizar `ReturnDDRatio`, `AvgTrade`, `ProfitFactor`, `DrawdownPct`, `StagnationPct`, `PayoutRatio` si es expansión.

### 12.5 Métricas especiales

- `SharpeRatio`: filtro secundario, útil con frecuencia suficiente.
- `RSquared`: filtro suave; no exigir demasiado alto.
- `WinningPct`: útil para reversión/pullback; evitar alto en breakout/trend.
- `AvgTrade`: siempre importante, especialmente en H1 y sesión.
- `PayoutRatio`: útil en breakout, trend, momentum y gap continuation.
- `ProfitableMonthsPct`: útil para trackrecord, fondeo y estacionales.
- `Stability` / `StabilitySQ3`: útiles para conservador/fondeo, con umbral suave.
- `SQN` / `SQNScore`: secundario y solo con suficientes trades.

---

## 13. Cross Checks y validaciones opcionales

Regla fundamental: los Cross Checks no se activan automáticamente. Solo se activan si el usuario los solicita, si el preset lo exige explícitamente o si el objetivo declarado lo requiere.

Diferenciar:

1. Cross Checks dentro del Builder.
2. Validaciones posteriores en Retester / Custom Projects.
3. Validaciones externas en MT5, Quant Analyzer, Myfxbook o FX Blue.

### 13.1 Retest on Additional Markets

Uso:

- Crear con un símbolo y validar con otro.
- Ejemplo: construir con `EURUSD` y validar con `EURUSD.c`.
- Validar robustez entre data normal y data tick/cent.

Editable bajo orden: activar/desactivar, símbolo de validación, timeframe, fechas, test precision, acceptance criteria.

Protegido salvo orden: spread, slippage, commission, swap, point value, tick size.

### 13.2 Higher Precision / Tick Retest

Uso:

- Validar con precisión superior.
- Confirmar que no depende de modelado débil.
- Evaluar comportamiento con tick data.

Criterios sugeridos: NetProfit positivo, PF no colapsa, DD no se deteriora extremo, trades razonablemente similares, equity no cambia radicalmente.

### 13.3 Monte Carlo

Uso:

- Randomize trades order.
- Skip trades.
- Randomize spread/slippage si el usuario autorizó.
- Sensibilidad estadística.

Regla: no inventar rangos de spread/slippage si el usuario prohibió tocar costos o no proporcionó rangos.

### 13.4 SPP

Preferible como validación posterior o Custom Project, salvo que el usuario lo pida en Builder.

### 13.5 WFA / WFA Matrix

WFA se usa como validación de estabilidad, no como justificación automática para adoptar parámetros recomendados. WFA Matrix es para finalistas.

### 13.6 What If

Útil para sesión, día de semana, horario, calendario y exclusiones operativas. No usar para sobreoptimizar horarios sin justificación.

### 13.7 Cross Checks por objetivo

Incubación / trackrecord:

1. OOS.
2. Tick / Higher Precision Retest.
3. Additional Market/Symbol validation.
4. Monte Carlo.
5. SPP / WFA para finalistas.

Fondeo:

- Higher Precision Retest.
- Monte Carlo.
- What If para evitar horarios/días problemáticos.
- SPP en finalistas.

Portafolio conservador:

- Higher Precision Retest.
- Monte Carlo.
- SPP.
- WFA Matrix para finalistas.
- What If por estabilidad de periodos.

### 13.8 Si el Builder queda lento o no genera estrategias

Orden de diagnóstico:

1. Revisar Genetic prefilters.
2. Revisar Ranking Final.
3. Revisar exceso de Cross Checks.
4. Revisar demasiados bloques activos.
5. Revisar complejidad excesiva.
6. Revisar periodo de datos corto.
7. Revisar si costos ahogan el edge, pero no modificarlos sin permiso.

---

## 14. Proceso técnico de modificación segura del `.cfx`

Flujo técnico obligatorio:

```text
1. Recibir `.cfx` base.
2. Crear copia de trabajo.
3. Verificar que el `.cfx` es un ZIP válido.
4. Descomprimir en carpeta temporal.
5. Confirmar existencia de `config.xml`.
6. Leer y parsear `config.xml`.
7. Crear snapshot de nodos protegidos.
8. Crear plan de cambios.
9. Validar plan contra whitelist.
10. Aplicar cambios autorizados.
11. Validar XML resultante.
12. Comparar nodos protegidos antes/después.
13. Reempaquetar `.cfx`.
14. Validar que el nuevo `.cfx` contiene `config.xml`.
15. Generar reporte.
16. Entregar `.cfx` final.
```

Nunca modificar el `.cfx` original.

### 14.1 Plan de cambios antes del patch

Formato:

```text
Cambio:
- Sección:
- Nodo/ruta:
- Valor anterior:
- Valor nuevo:
- Motivo:
- Permiso requerido:
- Estado: autorizado / bloqueado / requiere confirmación
```

Si un cambio requiere permiso y el usuario no lo dio, no se aplica.

### 14.2 Validación semántica

Validar:

- StrategyType definido.
- MarketSides definido.
- Timeframe definido.
- Al menos un Order Type activo.
- StopLoss activo salvo excepción explícita.
- Al menos una salida coherente.
- Building Blocks coherentes con edge.
- Ranking tiene fitness principal.
- Ranking tiene filtros mínimos.
- Genetic prefilters no son más estrictos que Ranking Final.
- Cross Checks solo los solicitados.
- Nodos protegidos intactos.

Errores críticos:

- No hay entrada activa.
- No hay StopLoss sin justificación.
- Ranking final vacío.
- Todos los bloques activos sin tesis.
- Cross Checks pesados activados sin permiso.
- Spread/slippage modificados sin permiso.

### 14.3 Checklist final antes de entregar

```text
[ ] El `.cfx` final abre como ZIP.
[ ] Contiene `config.xml`.
[ ] XML parseable.
[ ] Nodos protegidos intactos.
[ ] Ranking construido desde cero.
[ ] Genetic Options más suaves que Ranking Final.
[ ] Building Blocks coherentes con edge.
[ ] Al menos un Order Type activo.
[ ] StopLoss activo salvo excepción explícita.
[ ] Exit Types coherentes.
[ ] Cross Checks solo los solicitados.
[ ] Nombre del archivo claro.
[ ] Reporte generado.
```

---

## 15. Reporte obligatorio

Cada `.cfx` generado debe ir acompañado de reporte:

```text
Template generado:
- Archivo:
- Activo:
- Broker:
- Cuenta:
- Símbolo de construcción:
- Símbolo de validación:
- Timeframe:
- Justificación del timeframe:
- Data total disponible:
- Periodo Builder/IS usado:
- Periodo OOS usado:
- Data descartada o no usada:
- Justificación de uso/recorte de data:
- Edge:
- Tesis del edge:
- Régimen usado:
- Dirección:
- Strategy Type:
- Building Blocks activados:
- Order Types:
- Exit Types:
- BE / Trailing:
- Genetic Options:
- Ranking final:
- Cross Checks activados:
- Nodos protegidos no modificados:
- Advertencias:
```

También incluir:

```text
Sección | Nodo | Valor anterior | Valor nuevo | Motivo
```

---

## 16. Errores prohibidos

La skill nunca debe:

1. Tratar el `.cfx` base como configuración correcta.
2. Copiar ranking del `.cfx` base sin reconstruirlo.
3. Inventar nombres internos de métricas, bloques o nodos.
4. Cambiar spread, slippage, commission o broker sin permiso.
5. Activar Cross Checks no solicitados.
6. Configurar `both` por comodidad sin justificarlo.
7. Activar todos los bloques indiscriminadamente.
8. Usar `WinningPct` alto para breakout/trend.
9. Usar filtros fijos sin considerar periodo de datos.
10. Ahogar la genética con filtros finales demasiado estrictos.
11. Usar WFA para adoptar parámetros automáticamente sin orden del usuario.
12. Entregar un `.cfx` sin reporte de cambios.
13. Entregar un `.cfx` sin validar nodos protegidos.
14. Prometer robustez sin OOS/retest/validación posterior.
15. Heredar timeframe del `.cfx` base sin justificarlo.
16. Usar toda la data disponible por defecto.
17. Recortar data sin justificar régimen, calidad, muestra y representatividad reciente.

---

## 17. Estructura final de ejecución

Cuando el usuario solicite generar un template real, ejecutar este orden exacto:

```text
1. Confirmar inputs.
2. Leer `.cfx` base.
3. Leer rutas/diccionario de bloques.
4. Leer diccionario de ranking.
5. Leer data diaria.
6. Analizar régimen de mercado.
7. Elegir timeframe por edge.
8. Elegir periodo Builder/IS y OOS con criterio.
9. Seleccionar edge o edges.
10. Crear ficha de cada edge.
11. Traducir cada edge a configuración Builder.
12. Construir Genetic Options.
13. Construir Ranking Final.
14. Configurar Cross Checks solicitados.
15. Crear plan de cambios.
16. Validar whitelist/blacklist.
17. Aplicar patch al `.cfx` copiado.
18. Validar XML.
19. Validar nodos protegidos.
20. Reempaquetar `.cfx`.
21. Generar reporte.
22. Entregar archivo final.
```

---

## 18. Formato de salida esperado

Para N edges:

```text
outputs/
├── ACTIVO_BROKER_EDGE1_NOMBRE.cfx
├── ACTIVO_BROKER_EDGE2_NOMBRE.cfx
├── ACTIVO_BROKER_EDGE3_NOMBRE.cfx
└── reporte_templates.txt
```

Ejemplo:

```text
EURUSD_DOOPRIME_CENT_H1_EDGE1_PULLBACK_CONTINUATION.cfx
EURUSD_DOOPRIME_CENT_H1_EDGE2_SESSION_MEAN_REVERSION.cfx
EURUSD_DOOPRIME_CENT_H4_EDGE3_VOLATILITY_COMPRESSION_BREAKOUT.cfx
```

---

## 19. Criterio para pasar de V1 a Skill Final

La V1 puede convertirse en Skill Final cuando:

```text
[ ] Se prueba con un `.cfx` real.
[ ] Se genera al menos un template importable.
[ ] SQX lo abre sin error.
[ ] Los nodos protegidos no cambiaron.
[ ] Ranking, bloques y Cross Checks se modificaron correctamente.
[ ] El usuario aprueba el flujo operativo.
```

Hasta entonces, esta versión es:

```text
Skill Ejecutiva V1 consolidada, lista para prueba controlada.
```

No es todavía:

```text
Skill Final definitiva para automatización completa.
```

---

## 20. Próximo paso recomendado

Ejecutar una prueba controlada end-to-end con:

- `.cfx` base.
- Archivo de rutas.
- `ranking.cfx`.
- Data diaria del activo.
- Objetivo operativo real.
- Restricciones explícitas.

El primer entregable de la prueba debe ser el **diagnóstico de régimen y selección de edges**, antes de modificar cualquier `.cfx`.

---

# Actualización V1.2 — Modo usuario final, recalibración adaptativa y diagnóstico con rechazadas

Esta actualización se agrega después de la prueba real con EURUSD DooPrime. El objetivo es que la skill no solo genere `.cfx` importables, sino que también tenga un protocolo claro cuando un edge abre, llena población, pero no lleva suficientes estrategias al Data Bank.

## 21. Aprendizajes de la prueba real EURUSD

Durante la prueba controlada se validó:

```text
Edge 1 — Volatility Compression Breakout: funcionó correctamente.
Edge 2 — Pullback / Continuation: funcionó después de relajar filtros de forma quirúrgica.
Edge 3 — Selective Mean Reversion: funcionó después de simplificar la ejecución y relajar filtros.
```

Aprendizaje principal:

```text
Si el .cfx importa bien y la población se llena, el problema normalmente no es técnico, sino de productividad del edge, filtros, Cross Checks o estructura de entradas/salidas.
```

Regla nueva:

> No modificar el template a ciegas. Primero identificar por qué StrategyQuant está rechazando las estrategias.

---

## 22. Modo usuario final: generación adaptativa de candidatos

Para un usuario final, la experiencia ideal es que el sistema intente producir candidatos al Data Bank sin que el usuario tenga que rediseñar manualmente el Builder.

Pero hay una diferencia crítica:

```text
Se puede maximizar la probabilidad de generar candidatos.
No se puede garantizar que cualquier activo, cualquier data y cualquier configuración produzcan estrategias robustas.
```

El sistema debe prometer un proceso adaptativo, no una garantía falsa de robustez.

Mensaje correcto para usuario final:

```text
El sistema está diseñado para producir candidatos en Data Bank cuando existe una combinación razonable de activo, data, edge y filtros. Si no puede producir candidatos sin romper límites mínimos de calidad, marcará el edge como no viable y propondrá una alternativa.
```

---

## 23. Modos de generación

La skill debe permitir tres modos.

### 23.1 Modo estricto

Uso:

```text
- Usuario avanzado.
- Menos estrategias.
- Filtros iniciales más fuertes.
- Mayor riesgo de Data Bank vacío.
```

### 23.2 Modo balanceado

Uso recomendado por defecto.

```text
- Filtros razonables.
- Recalibración adaptativa si no llegan candidatos.
- Evita basura evidente.
- Permite generar material para Retester.
```

### 23.3 Modo descubrimiento

Uso:

```text
- Activos difíciles.
- Primera exploración.
- Búsqueda de familias prometedoras.
```

Advertencia:

```text
Este modo genera más candidatos, pero exige filtrado posterior fuerte.
No debe venderse como modo robusto.
```

---

## 24. Prueba de humo después de importar un `.cfx`

Cada template generado debe probarse en SQX antes de considerarlo aceptado.

### 24.1 Validaciones mínimas

```text
[ ] El .cfx importa sin error.
[ ] El Builder inicia correctamente.
[ ] La población se llena.
[ ] Empiezan a pasar estrategias al Data Bank.
[ ] No hay Cross Checks excesivamente pesados sin permiso.
[ ] Los filtros no bloquean el 100% de candidatos durante demasiado tiempo.
```

### 24.2 Criterio práctico de alerta

Solicitar revisión si después de 30 a 120 minutos:

```text
- Accepted = 0.
- No llegan estrategias al Data Bank.
- Llegan muy pocas estrategias.
- La población se llena pero todo queda rechazado.
```

Regla:

> Si un template abre y llena población, no se descarta inmediatamente el edge. Primero se analizan las estadísticas de rechazadas.

---

## 25. Protocolo de diagnóstico con capturas de rechazadas

Cuando un usuario diga que no salen estrategias, la skill debe pedir una captura del panel:

```text
Strategy dismissal stats
```

La captura debe mostrar, si es posible:

```text
- Reason to dismiss
- Count
- % of all
- Generated strategies
- Rejected strategies
- Accepted strategies
- In databank
- Genetic Evolution info
- Project running time
```

### 25.1 Cuándo pedir la captura

Pedir captura si:

```text
[ ] El .cfx importa bien, pero no llegan estrategias al Data Bank.
[ ] La población se llena, pero Accepted = 0.
[ ] El Data Bank recibe muy pocas estrategias después de 30 a 120 minutos.
[ ] El usuario reporta que “no salen estrategias”.
[ ] SQX muestra muchos rechazos y no está claro el cuello de botella.
[ ] Un edge funciona y otro no con la misma base.
```

---

## 26. Cómo interpretar las rechazadas

La skill debe clasificar los descartes en cuatro familias.

### 26.1 Filtros de Ranking Principal

Ejemplos:

```text
- Global filter: ProfitFactor [Main data]
- Global filter: ReturnDDRatio [Main data]
- Global filter: Winning Percent [Main data]
- Global filter: # of trades [Main data]
- Global filter: Stagnation [Main data]
- Global filter: DrawdownPct [Main data]
```

Interpretación:

```text
El edge genera candidatos, pero el ranking final está demasiado exigente para la fase de Builder.
```

### 26.2 Filtros de población inicial / genética

Ejemplos:

```text
- Initial population filter: Profit factor
- Initial population filter: # of trades
- Initial population filter: Drawdown
```

Interpretación:

```text
La genética está filtrando demasiado pronto y no permite evolución suficiente.
```

### 26.3 Filtros de Cross Check / Additional Markets

Ejemplos:

```text
- Cross Check filter in Backtests on additional markets: Net profit
- Cross Check filter in Backtests on additional markets: # of trades
- Cross Check filter in Backtests on additional markets: Profit factor
- Cross Check filter in Backtests on additional markets: Ret/DD Ratio
```

Interpretación:

```text
El mercado adicional está filtrando demasiado, especialmente si tiene menos histórico que el mercado principal.
```

Regla:

> El mercado adicional debe confirmar que la estrategia no colapsa; no debe exigir el mismo estándar que el mercado principal si tiene menos data.

### 26.4 Filtros automáticos técnicos

Ejemplos:

```text
- Automatic filter: no trades
- Automatic filter: too little trades
- Automatic filter: too many trades closing at the same bar
- Automatic filter: too many ambiguous trades
- Automatic filter: one exceptionally big trade
- Automatic filter: unfinished trades
```

Interpretación:

```text
El problema puede estar en estructura del edge, entradas, SL/TP, BE, trailing, precisión de test, timeframe o bloques demasiado restrictivos.
```

---

## 27. Decisiones según el filtro dominante

### 27.1 Si domina ProfitFactor

Acción:

```text
- Relajar PF gradualmente.
- No bajarlo por debajo del mínimo del modo seleccionado.
- Mantener filtro más fuerte para Retester.
```

Ejemplos:

```text
PF 1.12 → 1.07
PF 1.10 → 1.05
```

### 27.2 Si domina WinningPct

Acción:

```text
- Verificar si el edge necesita winrate alto.
- Mantenerlo en mean reversion si es coherente, pero reducir umbral.
- Quitar o suavizarlo en breakout, trend following o momentum.
```

Ejemplos:

```text
WinningPct 48 → 43
WinningPct 44 → 40
```

### 27.3 Si domina ReturnDDRatio

Acción:

```text
- Relajarlo en Builder inicial.
- Mantenerlo más fuerte para Retester.
```

Ejemplos:

```text
ReturnDDRatio 2.20 → 1.70
ReturnDDRatio 2.00 → 1.60
```

### 27.4 Si domina NumberOfTrades o too little trades

Acción:

```text
- Recalcular mínimo de trades según periodo real y timeframe.
- Revisar si el timeframe es demasiado alto.
- Revisar si entradas Limit/Stop reducen demasiado ejecuciones.
- Relajar el mínimo de trades sin aceptar muestras ridículas.
```

### 27.5 Si domina Additional Market

Acción:

```text
- Relajar filtros del mercado adicional.
- Mantener NetProfit > 0 como validación mínima.
- Usar PF > 1.00 o 1.01.
- Reducir trades mínimos proporcionalmente a la data disponible.
- Quitar o suavizar Ret/DD en mercado adicional si ahoga.
```

### 27.6 Si domina closing at same bar o ambiguous trades

Acción:

```text
- Simplificar entradas.
- Evitar mezclar Market + Limit + Stop en el primer template.
- Apagar BE en la versión inicial.
- Apagar trailing si no es esencial.
- Revisar si SL/TP está demasiado estrecho.
- Aumentar distancia mínima de SL/TP si aplica.
- Usar Market only para primera versión simple.
```

---

## 28. Orden adaptativo de relajación

Si no llegan candidatos al Data Bank, relajar en este orden:

```text
1. Cross Checks de Additional Markets, especialmente si tienen menos data.
2. Genetic prefilters.
3. ProfitFactor del ranking final.
4. ReturnDDRatio.
5. WinningPct, si el edge no depende fuertemente de winrate.
6. NumberOfTrades, calculado proporcionalmente al periodo.
7. StagnationPct.
8. DrawdownPct.
9. Complejidad de reglas.
10. Amplitud de Building Blocks.
11. Timeframe alternativo compatible.
12. Edge alternativo compatible con régimen.
```

No relajar primero:

```text
- Spread.
- Slippage.
- Commission.
- Swap.
- Money Management.
- Propiedades del instrumento.
```

---

## 29. Límites mínimos para no llenar el Data Bank con basura

La skill debe intentar generar candidatos, pero no romper la calidad mínima.

Límites guía para modo balanceado:

```text
ProfitFactor main:
- No bajar por debajo de 1.03 salvo modo descubrimiento.

ReturnDDRatio:
- No bajar por debajo de 1.20 salvo modo descubrimiento.

NumberOfTrades:
- No bajar por debajo de una muestra proporcional al periodo.

DrawdownPct:
- No abrir demasiado sin advertencia.

Additional Market:
- Puede ser suave, pero debe evitar colapso evidente.
```

Regla:

> Si para producir candidatos hay que romper todos los filtros mínimos, el edge debe marcarse como no viable bajo ese activo/data/configuración.

---

## 30. Regla de variantes para entradas, Limit y BE

Aprendizaje de la prueba EURUSD:

```text
Market + Limit + BE en el primer template puede ser conceptualmente válido, pero puede reducir productividad y aumentar ambigüedad.
```

Regla para usuario final:

> Para el primer template de un edge, usar la versión más simple que represente la tesis. Crear variantes separadas para Limit, Stop, BE o trailing.

Ejemplo Pullback / Continuation:

```text
Versión base:
- EnterAtMarket ON
- EnterAtLimit OFF
- BE OFF
- StopLoss ON
- ProfitTarget ON
- ExitAfterBars ON

Variante posterior:
- EnterAtLimit ON
- BE OFF

Variante posterior:
- EnterAtMarket ON
- BE ON
```

Ejemplo Mean Reversion:

```text
Versión base:
- EnterAtMarket ON
- EnterAtLimit OFF
- BE OFF
- Trailing OFF
- StopLoss ON
- ProfitTarget ON
- ExitAfterBars ON
```

Regla:

> Primero producir candidatos simples. Después probar variantes más sofisticadas.

---

## 31. Cuándo cambiar el edge completo

No cambiar el edge completo si:

```text
- El .cfx abre bien.
- La población se llena.
- Los rechazos dominantes son filtros de PF, Win%, Ret/DD o Additional Market.
```

Primero relajar filtros o simplificar ejecución.

Cambiar el edge si:

```text
- Tras relajación segura sigue sin producir candidatos.
- La mayoría de rechazos son no trades / too little trades.
- La tesis no produce suficiente muestra.
- La estructura genera mucha ambigüedad incluso simplificada.
- Hay que romper filtros mínimos para que pase algo.
```

Cuando se cambie edge:

```text
1. Mantener el régimen detectado.
2. Buscar un edge alternativo compatible.
3. Crear nuevo template.
4. Mantener nodos protegidos.
5. Reportar que el edge original fue descartado por baja productividad.
```

---

## 32. Respuesta estándar cuando el usuario envía una captura

La skill debe responder en este orden:

```text
1. Diagnóstico del cuello de botella principal.
2. Confirmar si el .cfx está técnicamente bien.
3. Indicar si el edge está muerto o solo demasiado filtrado.
4. Decir qué NO se debe tocar.
5. Proponer ajustes quirúrgicos.
6. Definir si corresponde V1.1, V1.2 o cambio de edge.
7. Entregar nueva configuración concreta.
```

Ejemplo:

```text
La población se llena, por lo tanto el .cfx no está roto. El problema no es técnico sino de filtros. El cuello de botella principal es ProfitFactor > 1.12, seguido de WinningPct y cierres en la misma barra. No cambiaría el edge todavía; haría una V1.1 con filtros proporcionales y ejecución Market only sin BE.
```

---

## 33. Registro de aprendizajes operativos

Si una versión ajustada funciona, la skill debe registrar:

```text
- Edge inicial.
- Problema observado.
- Filtros dominantes de rechazo.
- Cambios aplicados.
- Qué nodos protegidos no se tocaron.
- Resultado de la versión nueva.
```

Ejemplo registrado:

```text
Edge 3 Mean Reversion H1 no producía estrategias por PF, WinningPct, trades closing same bar y ambiguous trades. La versión simple Market only, sin Limit, sin BE, con filtros moderados, sí produjo candidatos. Aprendizaje: para usuario final, Mean Reversion inicial debe ser Market only + SL + TP + ExitAfterBars antes de probar variantes con Limit o BE.
```

---

## 34. Validación operativa final V1.0

La skill queda declarada como **Skill Final Operativa V1.0** porque fue probada en dos activos distintos y el flujo completo funcionó:

### 34.1 Caso validado 1: EURUSD / DooPrime Cent

Objetivo:

```text
Incubación para trackrecord, minería con más data y validación en símbolo adicional/tick/cent.
```

Resultado:

```text
Edge 1: Volatility Compression Breakout H4 → funcionó directo.
Edge 2: Pullback / Continuation H1 → funcionó después de ajuste V1.1 de filtros.
Edge 3: Selective Mean Reversion H1 → funcionó después de simplificar a Market only, sin Limit, sin BE, sin trailing.
```

Aprendizajes integrados:

```text
- Si la población se llena pero no llega al Data Bank, pedir Strategy dismissal stats.
- No cambiar el edge a ciegas.
- Relajar quirúrgicamente los filtros dominantes.
- Additional Market debe ser proporcional al histórico disponible.
- Mean Reversion inicial para usuario final funciona mejor simple: Market only + SL + TP + ExitAfterBars.
```

### 34.2 Caso validado 2: USDJPY / DooPrime Cent

Objetivo:

```text
Mismo objetivo que EURUSD: incubación para trackrecord, construcción con data principal y validación con el mismo activo en símbolo .c/tick/cent.
```

Diagnóstico del régimen:

```text
USDJPY mostró sesgo alcista estructural y reciente, con volatilidad media.
Régimen principal: alcista + volatilidad media.
```

Resultado:

```text
Edge 1: Trend / Pullback Continuation LONG → funcionó.
Edge 2: Volatility Expansion Breakout LONG → funcionó.
Edge 3: Post-Impulse / Buy-the-Dip Reversion LONG → funcionó.
```

Aprendizaje integrado:

```text
- No dejar MarketSides en both por defecto.
- Si la data muestra sesgo claro, la dirección debe alinearse con el régimen.
- En USDJPY alcista, los edges principales deben ser long-only salvo exploración explícita.
```

### 34.3 Criterio de validación alcanzado

```text
[OK] Se probaron .cfx reales.
[OK] Los templates importaron en SQX.
[OK] Los edges generaron minería funcional.
[OK] Se aplicó protocolo adaptativo con capturas de rechazadas.
[OK] Se corrigió dirección operativa usando análisis de data.
[OK] Se mantuvieron protegidos costos, spread, slippage, comisión, swap y money management.
[OK] Se integraron aprendizajes al documento final.
```

---

## 35. Estado final de la skill

Esta versión debe considerarse:

```text
Skill Final Operativa V1.0 — Generador de Templates .cfx para StrategyQuant X Builder.
```

Alcance validado:

```text
[OK] Generación de templates .cfx.
[OK] Análisis de régimen por data diaria.
[OK] Edge Registry ampliado.
[OK] Decisión explícita de MarketSides: long, short o both.
[OK] Ranking dinámico según objetivo, edge y periodo de datos.
[OK] Genetic Options más suaves que Ranking Final.
[OK] Cross Checks opcionales y proporcionales a la data disponible.
[OK] Modificación segura de .cfx.
[OK] Protocolo de prueba de humo.
[OK] Protocolo de capturas de rechazadas.
[OK] Recalibración adaptativa para usuario final.
[OK] Límites mínimos para no aceptar basura en Data Bank.
[OK] Validación práctica con EURUSD y USDJPY en DooPrime Cent.
```

Mejora continua recomendada:

```text
- Automatizar lectura de dismiss stats si SQX permite exportarla.
- Crear patcher Python estable con schema JSON/YAML.
- Crear presets por broker/activo/objetivo.
- Crear interfaz para usuario final.
- Probar con más activos, regímenes, brokers y timeframes.
```

Regla final:

```text
La skill está lista para entrega y uso operativo. No promete que cualquier activo produzca estrategias robustas, pero sí define un proceso adaptativo para generar candidatos, diagnosticar bloqueos, proteger nodos sensibles y recalibrar sin meter basura innecesaria al Data Bank.
```


---

## 36. Enmienda V1.1 — Timeframe y data con criterio

Esta enmienda formaliza dos reglas operativas obligatorias:

```text
1. El timeframe no se hereda del `.cfx` base.
2. La data disponible no se usa completa por defecto.
```

A partir de esta versión, cada generación debe justificar explícitamente:

```text
- Por qué se eligió H1, H4, D1 u otra temporalidad.
- Por qué un edge puede tener un timeframe distinto a otro edge.
- Qué parte de la data total se usa para Builder/IS.
- Qué parte queda como OOS.
- Qué data se descarta o se deja solo como referencia.
- Por qué usar más data mejora la muestra o por qué la empeora.
```

Regla final:

```text
Más data no significa mejor data.
Más timeframe no significa más robustez.
La decisión debe venir de edge + régimen + objetivo + calidad de data + costos + muestra esperada.
```


---

# Actualización V1.2 — Control anti-permisividad del Builder, ranking final mínimo por ventana larga y productividad con calidad

## 35. Problema que corrige esta actualización

En pruebas reales de Custom Project puede ocurrir que el Builder llene el Data Bank muy rápido, pero con estrategias de baja calidad. Esto no siempre significa que el edge esté mal; puede significar que el Ranking Final y los filtros de salida del Builder quedaron demasiado permisivos para la cantidad de histórico usada.

Regla central:

```text
Llenar rápido el Data Bank no es un éxito si el filtro final permite estrategias débiles.
Productividad sin umbral mínimo de calidad = modo descubrimiento, no modo balanceado ni entregable operativo final.
```

Esta actualización agrega pisos mínimos de dureza para evitar que, en ventanas largas como 2012→2022, filtros como `ReturnDDRatio > 1.00` pasen como Ranking Final balanceado.

---

## 36. Modo de generación obligatorio antes de configurar ranking

Cada Builder debe declarar explícitamente su modo:

```text
Modo descubrimiento
Modo balanceado
Modo estricto
```

### 36.1 Modo descubrimiento

Uso:

```text
- Primera exploración de un edge incierto.
- Objetivo: descubrir si existe alguna familia prometedora.
- Se permite mayor productividad y menor calidad inicial.
- No debe venderse como configuración robusta final.
```

Regla de naming:

```text
Si se usa modo descubrimiento, el archivo y el reporte deben decir DISCOVERY.
```

### 36.2 Modo balanceado

Uso por defecto para usuario final:

```text
- Generar candidatos suficientes.
- Evitar basura evidente.
- Preparar estrategias para OOS, MC, Tick, SPP y WFA.
```

### 36.3 Modo estricto

Uso:

```text
- Menos estrategias.
- Mayor calidad mínima.
- Mayor riesgo de Data Bank lento o vacío.
- Útil cuando el Builder está llenando demasiado rápido con estrategias débiles.
```

---

## 37. Regla anti-permisividad para ventanas largas de Builder/IS

Si el periodo Builder/IS tiene más de 8 años o más de 96 meses, el Ranking Final no puede usar umbrales de modo descubrimiento salvo orden explícita del usuario.

### 37.1 Bloqueo de Ret/DD demasiado bajo

Para Builder/IS > 96 meses:

```text
Modo balanceado:
- ReturnDDRatio final mínimo permitido: 1.80
- ReturnDDRatio recomendado: 2.00 a 3.00

Modo estricto:
- ReturnDDRatio final mínimo permitido: 2.30
- ReturnDDRatio recomendado: 2.50 a 3.50

Modo descubrimiento:
- ReturnDDRatio puede bajar a 1.20 a 1.70,
  pero el archivo debe marcarse como DISCOVERY y el reporte debe advertir que no es filtro final robusto.
```

Bloquea configuración final:

```text
Builder/IS > 96 meses + modo balanceado/estricto + ReturnDDRatio final < 1.80 = NO ENTREGABLE.
```

Ejemplo:

```text
EURUSD H4 LONG 2012.01.01 → 2022.12.31 ≈ 132 meses
ReturnDDRatio > 1.00 como filtro final = demasiado permisivo.
Uso aceptable: filtro genético suave o modo descubrimiento.
Uso no aceptable: Ranking Final balanceado.
```

---

## 38. Pisos mínimos de Ranking Final por ventana larga

Para Builder/IS mayor a 96 meses y objetivo incubación / trackrecord, usar como base:

```text
Modo balanceado:
NetProfit > 0
ProfitFactor >= 1.08 a 1.12
ReturnDDRatio >= 1.80 a 2.30
DrawdownPct <= 30 a 35
StagnationPct <= 30 a 40
AvgTrade > 0
NumberOfTrades >= mínimo dinámico por meses/timeframe/edge/dirección
```

```text
Modo estricto:
NetProfit > 0
ProfitFactor >= 1.12 a 1.20
ReturnDDRatio >= 2.30 a 3.50
DrawdownPct <= 25 a 30
StagnationPct <= 25 a 35
AvgTrade > 0
ProfitableMonthsPct >= 50 si hay suficiente muestra
NumberOfTrades >= mínimo dinámico más exigente
```

Regla:

```text
No usar ReturnDDRatio > 1.00 como Ranking Final en ventanas largas salvo modo descubrimiento explícito.
```

---

## 39. NumberOfTrades mínimo por ventana larga, timeframe, edge y dirección

El número de trades debe calcularse con:

```text
Meses_IS = meses entre fecha inicio Builder/IS y fecha fin Builder/IS
MinTradesFinal = Meses_IS × TradesPorMesEsperados × FactorDireccional
```

### 39.1 Factor direccional

```text
Both: 1.00
Long-only / Short-only con sesgo claro: 0.70 a 0.85
Long-only / Short-only contra sesgo o edge muy selectivo: 0.60 a 0.75, con advertencia
```

### 39.2 Guía para H4 en ventanas largas

Para H4 con más de 96 meses:

```text
Volatility Compression / Breakout:
- Balanceado long-only/short-only: 0.65 a 0.90 trades/mes
- Estricto long-only/short-only: 0.80 a 1.10 trades/mes

Trend / Pullback / Continuation:
- Balanceado long-only/short-only: 0.75 a 1.20 trades/mes
- Estricto long-only/short-only: 1.00 a 1.50 trades/mes

Mean Reversion H4:
- Balanceado long-only/short-only: 0.80 a 1.40 trades/mes
- Estricto long-only/short-only: 1.10 a 1.80 trades/mes
```

### 39.3 Guía para H1 en ventanas largas

Para H1 con más de 96 meses:

```text
Breakout / Trend:
- Balanceado long-only/short-only: 1.00 a 1.70 trades/mes
- Estricto long-only/short-only: 1.50 a 2.30 trades/mes

Pullback / Continuation:
- Balanceado long-only/short-only: 1.20 a 2.50 trades/mes
- Estricto long-only/short-only: 1.80 a 3.20 trades/mes

Mean Reversion:
- Balanceado long-only/short-only: 1.50 a 3.00 trades/mes
- Estricto long-only/short-only: 2.00 a 4.00 trades/mes
```

### 39.4 Ejemplo EURUSD Edge 1

```text
Edge: Volatility Compression Breakout
Timeframe: H4
Dirección: LONG
Builder/IS: 2012.01.01 → 2022.12.31
Meses aproximados: 132

Balanceado:
MinTradesFinal ≈ 90 a 120
MinTradesGenetic ≈ 45 a 70

Estricto:
MinTradesFinal ≈ 110 a 145
MinTradesGenetic ≈ 55 a 85
```

Regla:

```text
Si MinTradesFinal queda por debajo del rango proporcional sin justificación, el Builder está demasiado permisivo.
```

---

## 40. Genetic Options: productividad sin contaminar Ranking Final

Genetic Options puede ser más flexible, pero debe declararse como capa evolutiva, no como filtro final.

Para ventanas largas:

```text
MinTradesGenetic = 40% a 70% de MinTradesFinal
ProfitFactorGenetic = 1.00 a 1.03
NetProfit > 0 opcional o activo según productividad
DrawdownPct amplio: 45 a 55, según objetivo
AvgTrade > 0 solo si no ahoga la búsqueda
```

No usar en genética como filtro fuerte inicial:

```text
ReturnDDRatio alto
Sharpe alto
RSquared alto
WinningPct alto
Stability alta
Stagnation estricta
ProfitFactor > 1.10
```

Regla:

```text
Genetic Prefilters deben ser más suaves que Ranking Final.
Si la genética es igual o más dura que el Ranking Final, la configuración queda mal calibrada.
```

---

## 41. Control de Data Bank que se llena demasiado rápido

Si el Builder llena el Data Bank rápido pero con estrategias malas, diagnosticar antes de cambiar el edge.

### 41.1 Señales de ranking demasiado permisivo

```text
- Muchas estrategias con ReturnDDRatio entre 1.0 y 1.5.
- ProfitFactor apenas por encima de 1.00.
- DrawdownPct alto.
- StagnationPct alta.
- Pocos trades para una ventana larga.
- NetProfit concentrado en pocas operaciones.
- Curvas visualmente pobres aunque pasen filtros.
```

### 41.2 Acción recomendada

Endurecer en este orden:

```text
1. ReturnDDRatio final.
2. NumberOfTrades proporcional.
3. ProfitFactor.
4. DrawdownPct.
5. StagnationPct.
6. AvgTrade.
7. PayoutRatio en breakout/trend.
8. ProfitableMonthsPct si hay suficiente histórico.
```

No tocar primero:

```text
Spread
Slippage base
Commission
Swap
Money Management
Broker profile
Instrument settings
```

---

## 42. Ranking recomendado para Edge 1 EURUSD H4 LONG Breakout / Compression

Para el caso EURUSD DooPrime Cent, Edge 1 H4 LONG, Builder/IS 2012→2022:

### 42.1 Preset balanceado corregido

```text
Fitness:
ReturnDDRatio

Ranking Final:
NetProfit > 0
NumberOfTrades >= 100
ProfitFactor >= 1.10
ReturnDDRatio >= 2.00
DrawdownPct <= 30
StagnationPct <= 35
AvgTrade > 0
PayoutRatio >= 1.00
```

### 42.2 Preset estricto si sigue entrando basura

```text
Fitness:
ReturnDDRatio

Ranking Final:
NetProfit > 0
NumberOfTrades >= 120
ProfitFactor >= 1.12
ReturnDDRatio >= 2.30
DrawdownPct <= 28
StagnationPct <= 30
AvgTrade > 0
PayoutRatio >= 1.05
ProfitableMonthsPct >= 50
```

### 42.3 Genetic prefilter sugerido para ese caso

```text
NumberOfTrades >= 50 a 60
NetProfit > 0
ProfitFactor >= 1.00 a 1.03
DrawdownPct <= 45 a 50
AvgTrade > 0, solo si no ahoga productividad
```

Regla:

```text
WinningPct alto no debe ser filtro obligatorio para breakout/volatility expansion.
```

---

## 43. Reporte obligatorio adicional de dureza del Builder

Cada `.cfx` de Builder o Custom Project con Builder debe incluir:

```text
Modo de generación: descubrimiento / balanceado / estricto
Meses Builder/IS:
Timeframe:
Edge:
Dirección:
Trades/mes esperado:
Factor direccional:
MinTradesFinal calculado:
MinTradesGenetic calculado:
ReturnDDRatio Final:
ProfitFactor Final:
DrawdownPct Final:
StagnationPct Final:
AvgTrade:
Justificación de dureza:
Riesgo de Data Bank vacío:
Riesgo de Data Bank con basura:
Plan de ajuste si llena demasiado rápido:
Plan de ajuste si no llena:
```

Bloquea entrega como balanceada/estricta:

```text
- No declarar modo de generación.
- Builder/IS > 96 meses con ReturnDDRatio final < 1.80.
- NumberOfTrades sin cálculo proporcional.
- Genetic Prefilters más duros que Ranking Final.
- Reporte sin justificar por qué el ranking no es demasiado permisivo.
```

---

## 44. Regla final de esta actualización

```text
El Builder debe generar candidatos, pero no a cualquier costo.
Si el histórico es largo, el Ranking Final debe exigir calidad proporcional.
Si se quiere productividad extrema, se debe declarar modo DISCOVERY y no vender el archivo como balanceado ni robusto.
```


---

# Actualización V1.3 — Data Bank Quality Gate / Anti-Basura para Builder SQX

## 37. Propósito de esta actualización

Esta actualización corrige un problema detectado en pruebas reales con varios activos: algunos Custom Projects llenaban `Results` muy rápido, pero luego casi nada sobrevivía a OOS, MC Spread/Slippage, Tick, SPP o WFA. Esto indica que el Builder puede estar aceptando demasiadas estrategias débiles en el Data Bank inicial.

Regla central:

```text
El objetivo del Builder no es llenar rápido el Data Bank.
El objetivo del Builder es guardar candidatos que ya nazcan con calidad mínima operativa.
```

Esta actualización no reemplaza el análisis de edge, régimen, timeframe ni robustez. Agrega una puerta de calidad multidimensional antes de permitir que una estrategia entre al Data Bank `Results` en modo `BALANCEADO`, `BALANCEADO PRODUCTIVO`, `ESTRICTO` o `QUALITY FIRST`.

## 38. Principio Data Bank Quality Gate

En modo distinto de `DISCOVERY`, toda estrategia guardada en `Results` debe superar un Quality Gate compuesto por varias familias de calidad:

```text
1. Rentabilidad ajustada a riesgo.
2. Calidad de beneficio.
3. Muestra estadística suficiente.
4. Control de drawdown y stagnation.
5. Margen frente a costos.
6. Ausencia de concentración extrema.
7. Complejidad razonable.
8. Coherencia con el edge.
```

Regla:

```text
Una estrategia no debe entrar al Data Bank solo por Ret/DD, NetProfit o curva bonita.
Debe superar un conjunto mínimo de filtros coherentes con activo, broker, cuenta, edge, timeframe, dirección, ventana IS y objetivo.
```

## 39. Diferencia obligatoria entre Genetic Prefilters y Ranking Final

No endurecer la genética como si fuera el Ranking Final.

```text
Genetic Prefilters = entrada flexible para que la evolución trabaje.
Ranking Final / Strategy Filtering Conditions = puerta dura para entrar al Data Bank.
```

### 39.1 Genetic Prefilters recomendados

Mantener suaves:

```text
- NumberOfTrades proporcional suave.
- NetProfit > 0 opcional.
- ProfitFactor > 1.00 a 1.03.
- DrawdownPct amplio, solo si el Builder genera demasiada basura.
- AvgTrade > 0 solo si no ahoga la búsqueda.
```

Evitar en Genetic Prefilters salvo justificación:

```text
- ReturnDDRatio alto.
- ProfitFactor alto.
- SharpeRatio alto.
- RSquared alto.
- WinningPct alto.
- StagnationPct estricta.
- ProfitableMonthsPct estricta.
- AvgTrade como múltiplo fuerte del costo.
```

### 39.2 Ranking Final recomendado

El Ranking Final sí debe ser exigente y multidimensional. Debe incluir, según disponibilidad de métricas y edge:

```text
- ReturnDDRatio / RecoveryFactor / CalmarRatio.
- ProfitFactor.
- NumberOfTrades proporcional.
- AvgTrade o Expectancy.
- DrawdownPct.
- StagnationPct.
- ProfitableMonthsPct si la muestra lo permite.
- PayoutRatio si el edge es trend, breakout, momentum o volatility expansion.
- Stability / RSquared como filtros suaves si aplica.
- Complexity / DegreesOfFreedom si existe riesgo de sobreajuste.
- Outlier / concentración si la métrica está disponible.
```

## 40. Modos de generación actualizados

### 40.1 DISCOVERY

Uso:

```text
- Exploración inicial de un activo o edge desconocido.
- Buscar si existe alguna familia prometedora.
- No entregar como robusto.
- No usar para portafolio directo.
```

Pisos orientativos para Builder/IS largo:

```text
ProfitFactor >= 1.03 a 1.08
ReturnDDRatio >= 1.20 a 2.00
DrawdownPct <= 35 a 45
StagnationPct <= 40 a 50
AvgTrade > 0
NumberOfTrades proporcional bajo
```

### 40.2 BALANCEADO PRODUCTIVO

Uso recomendado por defecto cuando se quiere generar candidatos reales sin llenar basura.

Pisos orientativos para Builder/IS mayor a 96 meses:

```text
ProfitFactor >= 1.12 a 1.20
ReturnDDRatio >= 2.50 a 3.50
DrawdownPct <= 25 a 32
StagnationPct <= 28 a 38
AvgTrade >= múltiplo dinámico del costo
NumberOfTrades proporcional medio
ProfitableMonthsPct >= 45 a 55 si hay suficiente muestra
```

### 40.3 ESTRICTO / QUALITY FIRST

Uso:

```text
- Cuando Results se llena demasiado rápido.
- Cuando OOS queda por debajo de 2% de Results.
- Cuando OOS = 0.
- Cuando MC_SPREAD_SLIPPAGE elimina 100%.
- Cuando se busca menos cantidad y más calidad.
```

Pisos orientativos para Builder/IS mayor a 96 meses:

```text
ProfitFactor >= 1.18 a 1.30
ReturnDDRatio >= 3.50 a 5.00
DrawdownPct <= 18 a 28
StagnationPct <= 20 a 32
AvgTrade >= múltiplo fuerte del costo
NumberOfTrades proporcional alto
ProfitableMonthsPct >= 50 a 60 si hay suficiente muestra
Complexity controlada
```

Regla:

```text
Estos rangos no son universales fijos.
Deben ajustarse por activo, broker, cuenta, timeframe, edge, dirección, costos, ventana IS y objetivo.
```

## 41. Cálculo dinámico de NumberOfTrades reforzado

El mínimo de trades debe calcularse por meses reales de Builder/IS:

```text
Meses_IS = meses entre dateFrom y dateTo
MinTradesFinal = Meses_IS × AvgTradesPerMonthFinal
```

Guía reforzada por timeframe en Builder/IS largo:

```text
H1:
- Bajo/discovery: 1.5 trades/mes
- Balanceado: 2.0 a 3.0 trades/mes
- Estricto: 3.0 a 5.0 trades/mes

H4:
- Bajo/discovery: 0.8 trades/mes
- Balanceado: 1.2 a 1.8 trades/mes
- Estricto: 1.6 a 2.5 trades/mes

D1:
- Bajo/discovery: 0.2 a 0.4 trades/mes
- Balanceado: 0.4 a 0.8 trades/mes
- Estricto: 0.6 a 1.2 trades/mes
```

Ajustar según edge:

```text
Mean Reversion / Pullback: más trades esperados.
Trend / Breakout / Volatility Expansion: menos trades pero mayor AvgTrade/PayoutRatio.
Session / Time-of-Day: más trades si el horario es amplio; menos si la ventana es estrecha.
D1 / Seasonal: no exigir frecuencia absurda, pero evitar muestra ridícula.
```

## 42. AvgTrade vs costo operativo

Regla obligatoria:

```text
AvgTrade debe tener colchón frente al costo operativo esperado.
```

El costo operativo puede incluir:

```text
- Spread base.
- Slippage base o estrés esperado.
- Comisión.
- Min distance si afecta entradas Stop/Limit.
- Swap si el holding period es largo.
```

Guía inicial:

```text
H1: AvgTrade >= 2.5x a 4x costo base
H4: AvgTrade >= 3x a 5x costo base
D1: AvgTrade >= 4x a 6x costo base
```

Si la métrica `AvgTrade` está en dinero y el costo está en pips, el reporte debe explicar la conversión o marcarlo como:

```text
REQUIERE CONFIRMACIÓN DE UNIDADES
```

Bloqueo:

```text
Si MC_SPREAD_SLIPPAGE elimina el 100% de las estrategias, la siguiente versión debe exigir mayor AvgTrade/margen frente a costos antes de tocar OOS, MC o Tick.
```

## 43. Filtros por familia de calidad

### 43.1 Rentabilidad ajustada a riesgo

Usar una o varias:

```text
ReturnDDRatio
RecoveryFactor
CalmarRatio
SharpeRatio
SQN / SQNScore
```

Regla:

```text
Ret/DD no es suficiente por sí solo.
Debe combinarse con PF, AvgTrade, DD%, Stagnation y muestra suficiente.
```

### 43.2 Calidad de beneficio

Usar:

```text
ProfitFactor
AvgTrade
Expectancy
RExpectancy
PayoutRatio
NetProfit positivo
```

Evitar:

```text
NetProfit como criterio único.
ProfitFactor extremadamente alto sin suficientes trades.
AvgTrade bajo frente a costos.
```

### 43.3 Riesgo y estabilidad

Usar:

```text
DrawdownPct
StagnationPct
MaxConsecLosses si aplica
Exposure si aplica
OpenDrawdownPct si aplica
MaxIntradayDrawdown si aplica
```

Regla:

```text
Una estrategia rentable pero con DD, stagnation o exposición incompatibles con el objetivo no debe entrar limpia a Results.
```

### 43.4 Calidad de curva

Usar como filtros suaves o secundarios:

```text
RSquared
Stability
StabilitySQ3
EquitySlope
EquityAngle
ProfitableMonthsPct
```

No exigir `RSquared` alto en todos los edges. En trend, breakout o momentum puede eliminar estrategias válidas por curvas naturalmente irregulares.

### 43.5 Concentración y outliers

Si las métricas existen, filtrar o reportar:

```text
Outlier
Outlier2
MaxProfit
BiggestMAE
Max profit como % del NetProfit
Profit concentrado en 1 o pocas operaciones
```

Regla:

```text
No aceptar estrategias donde una operación o un tramo aislado explique una parte excesiva del resultado.
```

### 43.6 Complejidad

Controlar:

```text
Complexity
DegreesOfFreedom
Number of Conditions
RulesComplexity
Cantidad de indicadores y comparadores
```

Regla:

```text
A mayor complejidad, mayor exigencia de muestra, estabilidad y robustez.
```

## 44. Presets orientativos del Quality Gate

### 44.1 H1 Balanceado Productivo

```text
NumberOfTrades: proporcional medio
ProfitFactor: 1.12 a 1.18
ReturnDDRatio: 2.70 a 3.50
DrawdownPct: <= 25 a 30
StagnationPct: <= 30 a 35
AvgTrade: >= 2.5x a 4x costo base
ProfitableMonthsPct: >= 45 a 55 si hay histórico suficiente
Complexity: controlada
```

### 44.2 H1 Estricto / Quality First

```text
NumberOfTrades: proporcional alto
ProfitFactor: 1.18 a 1.25+
ReturnDDRatio: 3.50 a 4.50+
DrawdownPct: <= 20 a 25
StagnationPct: <= 25 a 30
AvgTrade: >= 3.5x a 5x costo base
ProfitableMonthsPct: >= 50 a 60 si hay histórico suficiente
Concentración/outliers: revisar o filtrar
```

### 44.3 H4 Balanceado Productivo

```text
NumberOfTrades: proporcional medio
ProfitFactor: 1.15 a 1.20
ReturnDDRatio: 2.80 a 3.50
DrawdownPct: <= 25 a 30
StagnationPct: <= 30 a 35
AvgTrade: >= 3x a 5x costo base
PayoutRatio: >= 1.00 si edge es trend/breakout/momentum
```

### 44.4 H4 Estricto / Quality First

```text
NumberOfTrades: proporcional alto
ProfitFactor: 1.18 a 1.30
ReturnDDRatio: 3.50 a 5.00
DrawdownPct: <= 18 a 25
StagnationPct: <= 20 a 30
AvgTrade: >= 4x a 6x costo base si el activo es caro
PayoutRatio: >= 1.00 a 1.10 si edge es trend/breakout/momentum
```

### 44.5 D1 Balanceado/Estricto

```text
NumberOfTrades: proporcional a baja frecuencia, sin muestra ridícula
ProfitFactor: 1.15 a 1.30
ReturnDDRatio: 2.50 a 5.00 según edge y duración
DrawdownPct: <= 20 a 30
StagnationPct: <= 25 a 40 según frecuencia
AvgTrade: >= 4x a 6x costo base
Outlier/concentración: obligatorio revisar
```

## 45. Diagnóstico automático de Builder permisivo

Activar alerta si ocurre cualquiera:

```text
- Results se llena muy rápido y OOS < 2% de Results.
- OOS = 0.
- MC_SPREAD_SLIPPAGE elimina 100%.
- TICK = 0 después de varios edges.
- SPP = 0 repetidamente.
- Results está lleno pero las estrategias tienen AvgTrade bajo frente a costos.
```

Acción obligatoria:

```text
No relajar OOS/MC/TICK para rescatar el lote.
No tocar costos, spread, slippage, comisión, swap ni money management.
Primero endurecer Ranking Final del Builder y/o cambiar edge.
```

Orden de corrección:

```text
1. Subir Quality Gate del Ranking Final.
2. Exigir AvgTrade proporcional al costo.
3. Recalcular NumberOfTrades por meses reales y timeframe.
4. Controlar DrawdownPct y StagnationPct.
5. Revisar concentración/outliers.
6. Reducir complejidad si hay sobreajuste.
7. Aumentar profundidad de búsqueda si sigue llenando fácil.
8. Cambiar edge si el problema persiste.
```

## 46. Profundidad de búsqueda y tiempo de minería

El tiempo no es métrica de calidad por sí solo.

Regla:

```text
1 hora no es automáticamente malo.
8 horas no es automáticamente bueno.
```

Pero si `Results` se llena rápido y luego OOS/MC/Tick colapsan, el sistema debe considerar:

```text
- Ranking Final demasiado flexible.
- Espacio de búsqueda demasiado amplio.
- Edge mal definido.
- Falta de filtro AvgTrade vs costo.
- Stop condition demasiado temprana.
```

Para modo `QUALITY FIRST`, considerar:

```text
- Permitir más generaciones/restarts.
- No detener solo porque Results se llenó fácil.
- Usar Dismiss Similar Strategies para evitar clones.
- Mantener Ranking Final duro.
- Evaluar calidad de mejora por generación, no solo cantidad almacenada.
```

## 47. Salida obligatoria del reporte Builder Quality Gate

Cada Custom Project debe reportar:

```text
Modo de generación: DISCOVERY / BALANCEADO PRODUCTIVO / ESTRICTO / QUALITY FIRST
Meses_IS:
Timeframe:
Edge:
Dirección:
Costo operativo estimado:
MinTradesFinal calculado:
AvgTrade mínimo esperado:
ProfitFactor mínimo:
ReturnDDRatio mínimo:
DrawdownPct máximo:
StagnationPct máximo:
Filtros de estabilidad:
Filtros de concentración/outlier:
Filtros de complejidad:
Motivo técnico de cada filtro:
Riesgo de Data Bank vacío:
Qué revisar si Results se llena demasiado rápido:
```

## 48. Regla final V1.3

```text
El Data Bank Results no debe ser una acumulación rápida de estrategias bonitas en IS.
Debe ser una primera selección de candidatos con calidad operativa suficiente para merecer OOS.
```

Si para que aparezcan estrategias hay que romper el Quality Gate mínimo del modo elegido, el sistema debe marcar:

```text
EDGE DÉBIL / NO VIABLE BAJO ESTA CONFIGURACIÓN
```

y proponer otro edge, otra ventana, otro timeframe o modo `DISCOVERY`, sin presentar los resultados como candidatos robustos.


---

# Actualización V1.4 — Multi-Timeframe Quality Gate / Calibrador M15, M30, H1, H4 y D1

## 49. Propósito de esta actualización

Esta actualización amplía el Data Bank Quality Gate para que el programa no quede sesgado a H1/H4. El sistema debe poder configurar Builder y Custom Projects para M15, M30, H1, H4 y D1 sin usar los mismos filtros de Ranking Final en todos los casos.

Regla central:

```text
El Quality Gate no se define solo por años de data.
Se define por timeframe + edge + costos + frecuencia esperada + meses IS + objetivo + modo de generación.
```

Bloqueo operativo:

```text
No usar los mismos umbrales de ProfitFactor, ReturnDDRatio, NumberOfTrades, AvgTrade, DrawdownPct, StagnationPct, outliers y complejidad para M15, M30, H1, H4 y D1.
```

## 50. Diferencia estructural por timeframe

### 50.1 Timeframes intradía bajos: M15 y M30

Características:

```text
- Mayor número esperado de operaciones.
- Mayor sensibilidad a spread, slippage, comisión y min distance.
- Mayor riesgo de ruido, same-bar exits, ambiguous trades y overfitting.
- Mayor necesidad de verificar AvgTrade frente a costo operativo.
- Mayor dependencia de Tick Retest/MT5 para validar ejecución real.
```

Regla:

```text
En M15/M30, una estrategia con AvgTrade bajo frente al costo no debe entrar limpia a Results en modo BALANCEADO o QUALITY FIRST.
```

### 50.2 Timeframes medios: H1 y H4

Características:

```text
- Balance entre frecuencia y ruido.
- H1 sigue siendo sensible a costos; H4 reduce ruido pero puede tener menos trades.
- Los filtros de trades deben calibrarse por edge y no por una cifra universal.
```

### 50.3 Timeframe diario: D1

Características:

```text
- Menor frecuencia esperada.
- Menor sensibilidad relativa al spread por operación.
- Mayor riesgo de muestra pequeña.
- Mayor riesgo de que 1 o 2 trades expliquen gran parte del resultado.
- Mayor riesgo de stagnation prolongada.
```

Regla:

```text
En D1 no se deben exigir trades mensuales de H1/H4, pero sí se debe revisar con mayor fuerza outliers, concentración, WorstYearProfit, ProfitableMonthsPct/ProfitableYears y stagnation absoluta.
```

## 51. Fórmula base universal

Para cualquier timeframe:

```text
Meses_IS = meses entre Builder dateFrom y Builder dateTo
MinTradesFinal = Meses_IS × TradesPorMesEsperados(timeframe, edge, dirección, modo)
MinTradesGenetic = MinTradesFinal × FactorGenetic(timeframe, modo)
```

Y para costos:

```text
CostoOperativoBase = spread base + slippage base esperado + comisión normalizada + ajuste por min distance si aplica
AvgTradeMin = CostoOperativoBase × Multiplicador(timeframe, modo, edge)
```

Si AvgTrade está en dinero y el costo está en pips:

```text
REQUIERE CONVERSIÓN DE UNIDADES
```

El reporte debe explicar la conversión o marcar que el umbral fue aplicado como aproximación conservadora.

## 52. Trades por mes esperados por timeframe y modo

Estos rangos son punto de partida, no reglas universales rígidas. Deben ajustarse por edge, dirección y activo.

### 52.1 M15

```text
DISCOVERY:
4 a 8 trades/mes

BALANCEADO PRODUCTIVO:
8 a 15 trades/mes

QUALITY FIRST / ESTRICTO:
12 a 25 trades/mes
```

Ajustes por edge:

```text
Mean Reversion / Session Reversion: zona alta del rango.
Breakout / Volatility Expansion: zona media.
Trend Following intradía: zona baja-media.
Edges de horario estrecho: reducir con justificación.
```

### 52.2 M30

```text
DISCOVERY:
2.5 a 5 trades/mes

BALANCEADO PRODUCTIVO:
5 a 10 trades/mes

QUALITY FIRST / ESTRICTO:
8 a 16 trades/mes
```

### 52.3 H1

```text
DISCOVERY:
1.5 a 2 trades/mes

BALANCEADO PRODUCTIVO:
2 a 3 trades/mes

QUALITY FIRST / ESTRICTO:
3 a 5 trades/mes
```

### 52.4 H4

```text
DISCOVERY:
0.8 a 1.0 trades/mes

BALANCEADO PRODUCTIVO:
1.2 a 1.8 trades/mes

QUALITY FIRST / ESTRICTO:
1.6 a 2.5 trades/mes
```

### 52.5 D1

```text
DISCOVERY:
0.2 a 0.4 trades/mes

BALANCEADO PRODUCTIVO:
0.4 a 0.8 trades/mes

QUALITY FIRST / ESTRICTO:
0.6 a 1.2 trades/mes
```

Regla D1:

```text
No aceptar muestra ridícula. Si el mínimo calculado queda muy bajo, revisar también trades por año, TotalTradingYears, WorstYearProfit y concentración del profit.
```

## 53. Multiplicadores de AvgTrade vs costo por timeframe

```text
M15:
BALANCEADO: 3x a 5x costo base
QUALITY FIRST: 4x a 6x costo base

M30:
BALANCEADO: 3x a 5x costo base
QUALITY FIRST: 4x a 6x costo base

H1:
BALANCEADO: 2.5x a 4x costo base
QUALITY FIRST: 3.5x a 5x costo base

H4:
BALANCEADO: 3x a 5x costo base
QUALITY FIRST: 4x a 6x costo base

D1:
BALANCEADO: 4x a 6x costo base
QUALITY FIRST: 5x a 8x costo base
```

Ajustes:

```text
Entradas Stop/Breakout: aumentar multiplicador si el activo es sensible a slippage.
Mean Reversion con TP pequeño: no permitir AvgTrade cerca del costo.
D1 con swaps relevantes: incluir costo de holding si aplica.
```

## 54. Rangos orientativos de Ranking Final por timeframe

### 54.1 M15 Balanceado Productivo

```text
NumberOfTrades: MinTradesFinal proporcional alto
ProfitFactor: 1.12 a 1.22
ReturnDDRatio: 3.00 a 4.00
DrawdownPct: <= 22 a 30
StagnationPct: <= 25 a 35
AvgTrade: >= 3x a 5x costo base
AmbiguousTrades: controlar
Same-bar exits: controlar
Complexity: baja-media
```

### 54.2 M15 Quality First

```text
ProfitFactor: 1.18 a 1.30+
ReturnDDRatio: 4.00 a 6.00
DrawdownPct: <= 18 a 25
StagnationPct: <= 20 a 30
AvgTrade: >= 4x a 6x costo base
NumberOfTrades: proporcional muy alto
Slippage/spread sensitivity: crítica
```

### 54.3 M30 Balanceado Productivo

```text
ProfitFactor: 1.12 a 1.20
ReturnDDRatio: 2.80 a 3.80
DrawdownPct: <= 22 a 30
StagnationPct: <= 25 a 35
AvgTrade: >= 3x a 5x costo base
NumberOfTrades: proporcional alto
```

### 54.4 M30 Quality First

```text
ProfitFactor: 1.18 a 1.28
ReturnDDRatio: 3.80 a 5.50
DrawdownPct: <= 18 a 25
StagnationPct: <= 20 a 30
AvgTrade: >= 4x a 6x costo base
```

### 54.5 H1 Balanceado Productivo

```text
ProfitFactor: 1.12 a 1.18
ReturnDDRatio: 2.70 a 3.50
DrawdownPct: <= 25 a 30
StagnationPct: <= 30 a 35
AvgTrade: >= 2.5x a 4x costo base
NumberOfTrades: proporcional medio
```

### 54.6 H1 Quality First

```text
ProfitFactor: 1.18 a 1.25+
ReturnDDRatio: 3.50 a 4.50+
DrawdownPct: <= 20 a 25
StagnationPct: <= 25 a 30
AvgTrade: >= 3.5x a 5x costo base
NumberOfTrades: proporcional alto
```

### 54.7 H4 Balanceado Productivo

```text
ProfitFactor: 1.15 a 1.20
ReturnDDRatio: 2.80 a 3.50
DrawdownPct: <= 25 a 30
StagnationPct: <= 30 a 35
AvgTrade: >= 3x a 5x costo base
PayoutRatio: >= 1.00 si edge es trend/breakout/momentum
```

### 54.8 H4 Quality First

```text
ProfitFactor: 1.18 a 1.30
ReturnDDRatio: 3.50 a 5.00
DrawdownPct: <= 18 a 25
StagnationPct: <= 20 a 30
AvgTrade: >= 4x a 6x costo base
PayoutRatio: >= 1.00 a 1.10 si aplica
```

### 54.9 D1 Balanceado Productivo

```text
ProfitFactor: 1.15 a 1.30
ReturnDDRatio: 2.80 a 4.00
DrawdownPct: <= 20 a 30
StagnationPct: <= 30 a 45
AvgTrade: >= 4x a 6x costo base
NumberOfTrades: proporcional bajo pero suficiente
Outlier/concentración: obligatorio revisar
WorstYearProfit: revisar si existe
```

### 54.10 D1 Quality First

```text
ProfitFactor: 1.25 a 1.50
ReturnDDRatio: 4.00 a 6.00
DrawdownPct: <= 15 a 25
StagnationPct: <= 25 a 40
AvgTrade: >= 5x a 8x costo base
Outlier/concentración: filtro o revisión obligatoria
ProfitableYears/WorstYearProfit: revisar si está disponible
```

## 55. Reglas especiales M15/M30

Bloquear o advertir si:

```text
AvgTrade está cerca del costo operativo.
Muchos rechazos por same-bar exits o ambiguous trades.
La estrategia depende de Stop/Limit con min distance relevante y no se evaluó slippage.
El Tick Retest no está disponible o es muy corto para validar ejecución.
NumberOfTrades es bajo para el timeframe.
```

Acciones preferidas:

```text
Simplificar entradas.
Evitar mezclar Market + Stop + Limit en la primera versión.
No activar BE/trailing complejo sin justificación.
Controlar AmbiguousTrades y trades closing same bar.
Usar Tick/real spread como validación prioritaria.
```

## 56. Reglas especiales D1

Bloquear o advertir si:

```text
NumberOfTrades total es demasiado bajo.
Una operación explica una parte excesiva del NetProfit.
Outlier/Outlier2 es alto.
MaxProfit como porcentaje de NetProfit es excesivo.
WorstYearProfit es muy negativo.
Stagnation absoluta es demasiado larga para el objetivo.
La estrategia solo gana en un tramo histórico aislado.
```

Acciones preferidas:

```text
Revisar concentración/outliers.
Revisar estabilidad por años.
No exigir trades de intradía.
No declarar robustez por PF/RetDD alto si hay pocos trades.
Usar WFA/SPP con cuidado proporcional a la muestra.
```

## 57. Diagnóstico de filtro dominante por timeframe

Si no salen estrategias:

```text
M15/M30:
- Si domina AvgTrade, spread/slippage o same-bar: revisar costos, entradas y estructura, no solo bajar filtros.
- Si domina too little trades, revisar edge/horario/bloques.
- Si domina PF/RetDD, bajar moderadamente sin romper el modo.

H1/H4:
- Si domina PF/RetDD, calibrar Ranking Final.
- Si domina no trades, revisar edge y bloques.
- Si domina MC Spread luego, subir AvgTrade en la siguiente versión.

D1:
- Si domina NumberOfTrades, no relajar automáticamente; revisar si el edge diario es demasiado selectivo.
- Si domina outlier/concentración, descartar o cambiar edge.
- Si domina stagnation, revisar si es tolerable para el objetivo.
```

## 58. Regla final V1.4

```text
El sistema debe calibrar el Quality Gate por timeframe.
M15/M30 requieren más muestra y más control de ejecución.
D1 requiere menos frecuencia, pero más control de outliers, concentración y stagnation.
H1/H4 quedan como perfiles intermedios, no como estándar universal.
```

No entregar un Custom Project como BALANCEADO o QUALITY FIRST si usa filtros de otro timeframe sin justificación explícita.


---

# Actualización V1.5 — StrategyFile Resource Safe Gate para Custom Projects

## 45. Problema corregido

En una prueba real con GBPJPY DooPrime Cent se detectó que un Custom Project podía abrir error al importar en SQX con:

```text
Cannot resolve custom resources.
Failed to update zip content
```

La causa operativa fue reemplazar el placeholder interno de StrategyQuant:

```text
StrategyType/@strategyFile = __STRATEGY_FILE__
```

por un valor genérico de plantilla:

```text
StrategyType/@strategyFile = SQ3StrategyTemplateExample.sq4
```

Ese valor puede ser válido como `templateFile`, pero no debe asumirse válido como `strategyFile`. En esta familia de Custom Projects, SQX necesita un recurso de estrategia compatible para resolver internamente el proyecto.

## 46. Regla bloqueante nueva

Queda prohibido entregar un `.cfx` final donde cualquier nodo:

```text
<StrategyType ... strategyFile="..." ... />
```

quede con alguno de estos valores, salvo prueba de humo explícita y documentada en esa misma instalación:

```text
strategyFile="SQ3StrategyTemplateExample.sq4"
strategyFile=""
strategyFile="__STRATEGY_FILE__"
strategyFile igual a templateFile por asignación genérica
strategyFile con placeholder o ruta inventada
```

Regla práctica:

```text
`templateFile` puede conservar `SQ3StrategyTemplateExample.sq4` si viene de una base compatible.
`strategyFile` debe conservar o restaurar el recurso strategyFile compatible de una base, edge hermano o diccionario de nodos que ya haya abierto correctamente en SQX.
```

## 47. Fuente permitida para StrategyType/@strategyFile

Al generar Custom Projects desde la base custodiada, el patcher debe resolver `__STRATEGY_FILE__` usando una de estas fuentes, en este orden:

```text
1. Valor exacto de `strategyFile` de una variante hermana del mismo árbol que ya abrió correctamente en SQX.
2. Valor exacto validado en el diccionario de rutas/nodos Builder.
3. Valor exacto de una base SQX exportada por el usuario que ya abra correctamente.
```

No se debe crear ni normalizar el valor manualmente.

## 48. Ejemplo validado en corrección GBPJPY

La corrección que permitió importar el proyecto fue restaurar un recurso técnico de StrategyQuant similar a:

```text
D:\work\StrategyQuant4\work_directory\StrategyQuant\user\projects\Retester\databanks\Results\Strategy 0.1.7.sq4
```

Este tipo de ruta histórica no debe tratarse automáticamente como residuo operativo. En este caso es un campo técnico usado por SQX para resolver recursos internos.

## 49. Auditoría obligatoria añadida al Builder/Custom Project

Antes de entregar cualquier `.cfx`, auditar en todos los XML internos:

```text
Build-Task*.xml
Retest-Task*.xml
config.xml si aplica
```

Y reportar:

```text
Archivo XML
StrategyType/@templateFile detectado
StrategyType/@strategyFile detectado
Fuente usada para strategyFile
Estado: PASS / FAIL
```

Bloquear entrega si:

```text
- strategyFile queda genérico.
- strategyFile queda igualado a templateFile sin prueba validada.
- strategyFile queda vacío.
- strategyFile conserva placeholder.
- solo se corrigió Build-Task y no los Retest-Task.
- la auditoría no lista todos los StrategyType encontrados.
```

## 50. Regla anti-cache después de error de recurso

Si SQX ya falló con un Project Name, la siguiente versión debe cambiar el Project Name interno y el archivo final debe llevar sufijo como:

```text
V2_RS
RESOURCE_SAFE
FIX_RS
```

Además, pedir borrar la carpeta vieja en:

```text
user/projects/<ProjectName anterior>
```

antes de importar la versión corregida.

## 51. Regla final V1.5

```text
No basta con que el `.cfx` pase auditoría XML.
Debe pasar auditoría StrategyFile Resource Safe.
Un final con strategyFile genérico no es entregable operativo.
```


---

# Actualización V1.6 — Operators Safe Gate para Builder SQX

## 80. Motivo

Se detectó un fallo operativo real en Custom Projects GBPJPY: el archivo podía abrir después de la corrección `strategyFile`, pero el Builder podía no iniciar cuando el patch activaba indicadores y apagaba por error los comparadores/operadores funcionales.

Causa técnica típica:

```text
El patcher manipula todos los bloques category="indicators" como si fueran solo indicadores.
En SQX, varios comparadores/operadores también aparecen bajo category="indicators".
Resultado: Indicators activos + Comparators/Operators en use="false".
```

Esto deja al Builder sin piezas suficientes para formar condiciones del tipo:

```text
Indicador/Precio/Valor + Comparador/Operador + Indicador/Precio/Valor
```

## 81. Regla bloqueante Indicators + Operators

Todo Builder final debe cumplir:

```text
Si ActiveIndicators > 0 entonces ActiveComparators > 0.
ActiveOperands > 0.
ActiveOrderTypes = 1.
StopLimitBlocks > 0 si OrderType activo es EnterAtStop o EnterAtLimit.
StopLimitBlocks = 0 permitido y recomendado si OrderType activo es EnterAtMarket.
```

Bloquear entrega si:

```text
Indicators activos y Comparators/Operators activos = 0.
Comparators activos pero sin operands/precios/valores mínimos.
OrderTypes activos = 0.
OrderTypes activos > 1, salvo variante experimental explícita.
Stop/Limit order activo con StopLimitBlocks activos = 0.
Market-only con StopLimitBlocks heredados activos sin justificación.
```

## 82. Comparadores/operadores core permitidos

La whitelist mínima de operadores funcionales es:

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

No todos deben estar activos siempre, pero cada template debe tener una selección coherente con el edge.

## 83. Operands mínimos recomendados

Activar al menos una familia válida de operandos:

```text
Prices.Close
Prices.High
Prices.Low
Prices.Open
Indicators.Number
```

Opcional según edge:

```text
Prices.Bid
Prices.Ask
Indicators.Highest
Indicators.Lowest
```

## 84. Regla crítica para patchers

Queda prohibido hacer esto de forma global:

```text
for block where category == "indicators":
    use = key in indicators_on
```

porque eso apaga comparadores que SQX guarda dentro de la misma categoría.

El patch correcto debe separar familias:

```text
1. Indicator blocks reales.
2. Comparator/operator blocks.
3. Operand/value/price blocks.
4. Signal blocks.
5. StopLimitBlocks.
6. OrderTypes.
7. ExitTypes.
```

## 85. Matriz obligatoria de reporte Builder Operators Safe

Todo `.cfx` final debe reportar:

```text
Archivo | ActiveIndicators | ActiveComparators | ActiveOperands | ActiveSignals | ActiveOrderTypes | ActiveStopLimitBlocks | Estado
```

Estado PASS solo si:

```text
ActiveComparators > 0.
ActiveOperands > 0.
ActiveOrderTypes = 1.
La familia de StopLimitBlocks coincide con el OrderType activo.
```

## 86. Reglas por tipo de entrada

Market-only:

```text
EnterAtMarket = true.
EnterAtStop = false.
EnterAtLimit = false.
StopLimitBlocks = 0 recomendado.
BE/trailing solo si la variante lo justifica.
```

Stop-only:

```text
EnterAtStop = true.
EnterAtMarket = false.
EnterAtLimit = false.
StopLimitBlocks > 0 obligatorio.
Ejemplos: ATR, Highest/Lowest, EMA/SMA, High/Low.
```

Limit-only:

```text
EnterAtLimit = true.
EnterAtMarket = false.
EnterAtStop = false.
StopLimitBlocks > 0 obligatorio.
Ejemplos: ATR, Bollinger/Keltner, EMA/SMA, High/Low.
```

## 87. Regla final V1.6

```text
Un Builder con indicadores pero sin operadores no es entregable, aunque el .cfx importe.
La auditoría debe bloquearlo antes de entregar.
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


## Impacto específico en Skill 1 / Builder

Al diseñar Trading Options para el Builder:

```text
No heredar sesión del .cfx base por comodidad.
No convertir ausencia de filtro horario en `No Session` textual.
No activar LimitTimeRange=true por defecto.
```

Para cada edge se debe declarar:

```text
SessionPolicy: SESSION_RESOURCE_SAFE
SessionResourceUsed: recurso real detectado, por ejemplo FX_XCCY_Currency1[DOOPRIME]
LimitTimeRange: false salvo orden explícita
SessionRationale: se usa recurso resoluble para evitar error XML, sin limitar horario
```

Si falta el recurso real de sesión:

```text
REQUIERE CONFIRMACIÓN O BASE HERMANA VALIDADA.
```

No entregar Builder final con sesión no resoluble aunque todo lo demás esté correcto.

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


## Aplicación específica en Skill 1 — Builder y selección de ventanas

Al elegir periodo Builder/IS y OOS, la Skill 1 debe calcular primero el rango normal útil y luego reservar 20%–30% como OOS reciente. La selección de edges, timeframe, ranking y Quality Gate se hace después de congelar ese corte.

Checklist adicional de Skill 1:

```text
[ ] Data normal útil definida.
[ ] OOS target elegido según objetivo.
[ ] OOS% calculado antes de patch.
[ ] Builder/IS no invade OOS.
[ ] Ranking Final calculado sobre Builder/IS.
[ ] OOS reservado como data no vista.
[ ] Reporte declara IS%, OOS%, corte y meses reales.
```

Si el usuario pide TRACK y no especifica porcentaje:

```text
Usar OOS target 25%, ajustable dentro de 22%–27% por redondeo y calidad de data.
```


---

# Actualización V1.9 — Session Existing Safe, Donor Session Gate y Short Project Names

## 45. Motivo operativo

Durante la generación real de Custom Projects GBPUSD DooPrime Cent se validó una cadena de fallos y correcciones:

```text
V3: sesión funcional incorrecta con corchetes: FX_XCCY_Currency1[DOOPRIME] → fallo de recurso.
V4: sesión exacta detectada, pero embebida/incrustada en el .cfx → fallo al actualizar ZIP interno.
V5: sin sesión embebida y LimitTimeRange=false → abrió.
V6: sesión existente referenciada sin bloque embebido → E1/E2 abrieron, E3 falló por nombre interno largo.
V7: sesión existente + <Sessions /> vacío + Project name corto → funcionaron los 4 Custom Projects.
```

Conclusión:

```text
El problema no era solamente la existencia de la sesión, sino cómo se empaquetaba y cómo SQX intentaba resolverla al importar el proyecto.
```

## 46. Regla Session Existing Safe

Cuando el usuario quiera operar con una sesión de broker existente en Data Manager, no se debe inventar ni incrustar una sesión nueva dentro del `.cfx`.

Regla por defecto:

```text
Usar el nombre exacto de la sesión existente en campos funcionales.
No agregar bloque <Session name="..."> salvo que venga de una base donadora exportada y reimportada con éxito.
Dejar <Sessions /> vacío si se usa una sesión ya existente en la instalación del usuario.
Mantener LimitTimeRange=false salvo prueba compatible.
No usar Add new en Resolve project resources.
Usar recurso existente / Use existing / Load config using these settings si no hay diferencias erróneas.
```

Campos funcionales donde puede referenciarse una sesión existente:

```text
SessionOption
MarketOpenSession
TradingSession
Setup/@session
session
sessionName
```

Pero el bloque de recursos debe quedar:

```xml
<Sessions />
```

salvo que exista **donor session** validado.

## 47. No sintetizar nombres de sesión

Nunca construir nombres de sesión combinando nombre base + broker profile por inferencia.

Prohibido:

```text
FX_XCCY_Currency1[DOOPRIME] si ese texto no aparece literalmente en la columna Session Name.
FX_XCCY_Currency1DOOPRIME si no fue visto o confirmado en Data Manager.
No Session como valor funcional en XML operativo.
NONE / NULL / vacío si SQX valida sesión.
```

Permitido:

```text
Nombre literal visto en Data Manager > Sessions > columna Session Name.
Nombre literal extraído de una base .cfx exportada por la misma instalación y probada.
Nombre literal de un proyecto hermano que ya abrió y corrió en SQX.
```

Si el nombre de sesión aparece con corchetes en la **columna Session Name**, se puede usar. Si los corchetes aparecen solo en **Broker profile**, no deben agregarse al nombre de sesión.

## 48. Donor Session Gate

Si el usuario quiere usar una sesión de broker con filtro horario nativo o `LimitTimeRange=true`, se requiere una base donadora.

Base donadora válida:

```text
1. Creada en la instalación SQX del usuario.
2. Mismo broker/instrumento/símbolo objetivo o equivalente validado.
3. Sesión seleccionada manualmente por el usuario.
4. Exportada como .cfx.
5. Reimportada desde ruta corta.
6. Probada con Start sin Cannot resolve custom resources.
```

Solo entonces se permite copiar:

```text
- bloque <Sessions> completo,
- campos Session/MarketOpenSession/Setup session,
- LimitTimeRange=true si ya abrió con ese recurso,
- estructura de Trading Options relacionada con horario.
```

Sin donor session validado:

```text
Versión principal = session existing reference + <Sessions /> vacío + LimitTimeRange=false.
```

## 49. Política para edges de sesión

Para edges tipo Londres, NY, Asia, apertura/cierre o time-of-day:

```text
Preferir condiciones/bloques horarios dentro de la lógica del Builder si existen.
No activar filtro horario nativo como versión principal si no hay donor session validado.
Crear variante EXP_SESSION solo cuando el usuario entregue donor .cfx probado.
```

## 50. Regla Short Project Names

SQX puede fallar al actualizar `project.cfx` interno si el `Project name` o la ruta del proyecto importado quedan largos o si existen carpetas previas corruptas.

Regla obligatoria:

```text
Project name interno preferido: <= 25 caracteres.
Project name interno máximo permitido: 30 caracteres.
Nombre de archivo preferido: <= 35 caracteres.
Ruta de importación recomendada: C:\SQX_IMPORT\.
No usar sufijos largos como BROKERSESSION_EXISTING, SESSION_EXACT, OOS25_SESSION_SAFE, RESOURCE_SAFE en el Project name final.
```

Formato recomendado:

```text
<ASSET_SHORT><BROKER_SHORT>_<EDGE>_<TF>_<VERSION>
```

Ejemplos:

```text
GBPDP_E1_H4PB_V7
GBPDP_E2_H4BO_V7
GBPDP_E3_H1MR_V7
GBPDP_E4_H1MO_V7
AUDDP_E2_H4BO_V3
UJDP_E1_H1TR_V2
```

Bloquear entrega si:

```text
Project name > 30 caracteres.
Project name contiene espacios, tildes, corchetes o caracteres no ASCII.
Project name reutiliza una versión que ya falló.
Nombre largo se usa para corrección después de error Cannot resolve custom resources.
```

## 51. Anti-colisión de carpetas `user/projects`

Cada corrección debe usar `Project name` nuevo y corto. Además, el reporte debe pedir al usuario borrar carpetas previas fallidas en:

```text
user/projects/<ProjectName anterior>
```

Especialmente cuando apareció:

```text
Cannot resolve custom resources
Failed to update zip content
```

## 52. Inputs obligatorios adicionales

Cuando se trabaje con broker/session:

```text
Nombre exacto de Session Name desde Data Manager.
Broker profile mostrado en la columna Broker profile.
Confirmación de si se quiere solo usar sesión existente o activar filtro horario nativo.
Si se quiere filtro horario nativo: donor .cfx exportado y probado.
```

## 53. Naming report obligatorio

Cada reporte debe incluir:

```text
Project name interno:
Longitud del Project name:
Nombre de archivo:
Longitud del nombre de archivo:
Ruta de importación recomendada:
Estado ShortNameSafe: PASS/FAIL
```

## 54. Regla final V1.9

```text
Una sesión existente en Data Manager no debe incrustarse automáticamente como recurso nuevo.
Primero se referencia como existente, con <Sessions /> vacío y LimitTimeRange=false.
Para incrustar sesión o usar horario nativo, se exige donor .cfx probado.
Todo final debe tener Project name corto para evitar fallos de importación por carpeta/ruta/nombre.
```
