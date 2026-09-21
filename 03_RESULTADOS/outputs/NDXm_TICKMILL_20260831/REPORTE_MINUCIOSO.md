# Reporte minucioso — Custom Projects NDXm_TICK_UTCPlus02 / Tickmill - Nasdaq

Generado: 2026-08-31. Skills aplicadas: paquete `SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE_20260517` (Skill 1 Generador V1.9, Skill 2 Robustez V1.5, Skill 3 Orchestrator V1.12, Skill 4 Custodia V1.9). Base técnica: `07_BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx`.

## 0.2 Segunda corrección post-entrega — DataBank chain rota (2026-08-31, misma fecha)

El usuario corrió `NDXM_TMILL_E2_M15PB` (versión de la corrección 0.1) en SQX real: Builder generó
1611 estrategias, OOS las procesó correctamente (1611 en databank OOS), pero **nada avanzó a
MC_TRADES ni a ninguna etapa posterior**, de forma repetible.

**Causa raíz confirmada** (log real de SQX + conteo en disco + inspección del `.cfx` importado, no
solo teoría): cada `Retest-Task*.xml` tiene dos bloques `<Databanks>`. El que SQX realmente usa para
rutear (`<Databanks retestSelected="false">`, confirmado porque OOS escribió en la databank "OOS" y
no en la que decía el otro bloque) traía en la base "limpia" **nombres residuales de un proyecto
donor** — `MONTECARLO RNADOMIZE TRADES Y SKIP TRADES`, `MONTECARLO SLIPPAGE Y SPREAD`, `GESTION
MONETARIA` sin el sufijo `- DESACTIVADA` — exactamente el patrón que la Skill 3 §12 nombra por texto
como bloqueante, y que esta entrega **no verificó realmente** pese a haber declarado PASS la
auditoría de DataBank chain en la §13 original de este reporte (esa declaración estaba basada solo en
`config.xml`, que es un registro de visualización, no la fuente real de ruteo — error mío).

Detalle completo, evidencia de log y tabla de valores rotos→corregidos:
`user\PropFirm_Management\21_incidente_databank_chain_residual_names.md`.

**Fix:** los 8 `.cfx` (4 edges × Tickmill/OANDA) fueron regenerados con la cadena
`Results→OOS→MC_TRADES→MC_SPREAD_SLIPPAGE→TICK→SPP→WFA MATRIX` corregida y verificada, con
`Project name` sufijado `_V2` (regla anti-reutilización de nombre tras fallo). **Antes de reimportar:
cerrar SQX y borrar las carpetas viejas en `C:\SQX_144_Full\user\projects\`
(`NDXM_TMILL_E1_H1TF`, `_E2_M15PB`, `_E3_H1BO`, `_E4_M15MR`, y las `NDXM_OANDA_*` si se importaron),
luego importar los `*_V2.cfx` desde `C:\SQX_IMPORT\`** (los antiguos sin `_V2` ya se retiraron de esa
carpeta).

## 0.1 Corrección post-entrega (2026-08-31, misma fecha)

La primera tanda de 4 `.cfx` falló al importar con:

```
Cannot resolve resources - Invalid format: '1530057600000' is malformed at '0000'.
```

**Causa:** las fechas `dateFrom`/`dateTo` a nivel de `Setup`/`Range` (tarea) usan formato de texto `AAAA.MM.DD`, no epoch-milisegundos. El epoch-ms solo es válido en el catálogo `Resources/Symbols` (metadatos del recurso), un contexto distinto. Se confirmó el formato correcto inspeccionando un proyecto hermano real ya funcional en esta instalación (`user/projects/Builder/NDXm_Qlib_OOS20.cfx`, mismo símbolo).

**Correcciones aplicadas en esta segunda versión** (mismos 4 archivos, mismos nombres, regenerados):

| Campo | Antes (fallaba) | Ahora (corregido) | Evidencia |
|---|---|---|---|
| `Setup`/`Range` dateFrom/dateTo | epoch-ms (`"1530057600000"`) | texto `"2018.06.27"` | Formato confirmado en proyecto hermano |
| Symbol catalog `source` | `1` (heredado del patrón FX) | `4` | Valor real en Data Manager para este símbolo |
| Symbol catalog `uSymbol`/`uSymbolName` | vacío | `NDXm` | Valor real confirmado |
| Symbol catalog `cloneFrom` / `sourceTimezone` | ausentes | `NDXm` / `Etc/UCT` | Atributos reales confirmados, faltaban por completo |
| `InstrumentInfo.instrument` | `NDXm_TICK_UTCPlus02` | `NDXm(2)` | Identificador de instrumento real (distinto del nombre de símbolo) |
| `InstrumentInfo.tickValueInMoney` | `1.0` (error mío, dupliqué pointValue) | `0.0` | Campo separado no usado; confirmado en registro real |
| `InstrumentInfo.dataType` | `3` (heredado FX) | `6` | Valor real confirmado |
| `commissions` Method | `SizeBased` | `None` | Coincide con el registro real (comisión $0 vía tipo None) |
| `swap` type | `points` | `money` | Coincide con el registro real; valores Long/Short siguen siendo los tuyos (-4.95/-1.3) |
| Símbolos duplicados en catálogo | 2 entradas `<Symbol name="NDXm_TICK_UTCPlus02">` distintas (normal+tick unificados a un mismo nombre pero con atributos divergentes) | 1 sola entrada, deduplicada | Riesgo adicional de "recurso ambiguo" eliminado |

Se revalidaron los 4 `.cfx`: reparseo XML completo de los 36 archivos internos, cero placeholders residuales, sin símbolos duplicados, formato de fecha correcto en todos los `Setup`/`Range`, un solo Order Type activo por edge, `DeleteFailedStrategies=true` en las 6 etapas de robustez, `<Sessions/>` vacío en los 8 XML de cada edge. **Todo PASS.**

Los 4 archivos en `outputs/NDXm_TICKMILL_20260831/` y en `C:\SQX_IMPORT\` ya están sobrescritos con esta versión corregida — vuelve a intentar la importación con los mismos archivos, no hace falta borrar nada.

## 0. Entregables

```
outputs/NDXm_TICKMILL_20260831/
├── NDXM_TMILL_E1_H1TF.cfx    (Edge 1 — Trend Following, H1)
├── NDXM_TMILL_E2_M15PB.cfx   (Edge 2 — Pullback/Continuation, M15)
├── NDXM_TMILL_E3_H1BO.cfx    (Edge 3 — Volatility Expansion Breakout, H1)
├── NDXM_TMILL_E4_M15MR.cfx   (Edge 4 — Selective Mean Reversion, M15)
└── REPORTE_MINUCIOSO.md      (este documento)
```

Copiados también a `C:\SQX_IMPORT\` (ruta corta recomendada por la Skill 3/4 para importación).

Cada `.cfx` es un Custom Project completo de 8 tareas encadenadas: `Build → OOS → MC_TRADES → MC_SPREAD_SLIPPAGE → TICK → SPP → WFA MATRIX` (+ `GESTION MONETARIA - DESACTIVADA`, inactiva).

## 1. Mandato recibido

- Activo: **NDXm_TICK_UTCPlus02**, Broker: **Tickmill - Nasdaq**, Capital: **1000 USD**, 4 edges, temporalidades candidatas **M3, M15, H1**.
- Costos inyectados (autorizados explícitamente por el usuario): Pip/Tick size 0.01, Point value $1, Default spread 100 pips, Default slippage 1 pip, Comisión $0, Swap Long -4.95 / Short -1.3.
- Rango de data/filtros solicitado: 2015-01-01 a 2025-01-01.
- Reglas activas: Forzar OOS 20–30%, Existing Session Safe, ShortName Safe (≤25), Custodia Limpia.

## 2. Desviación documentada de rango de data (OOS_EXCEPTION parcial — solo en fecha de inicio)

La data real disponible en `qlib_export/output/ndxm_qlib.csv` (hourly OHLCV) cubre **2018-06-27 → 2026-06-25**, no 2015-01-01. No existe data del activo antes de 2018-06-27 en este repositorio.

| Campo | Valor |
|---|---|
| Data total disponible | 2018-06-27 → 2026-06-25 |
| Data normal útil usada | **2018-06-27 → 2025-01-01** (respeta el límite superior pedido por el usuario) |
| Data descartada | Anterior a 2018-06-27 (no existe) y posterior a 2025-01-01 (existe hasta 2026-06-25 pero se respeta el corte solicitado por el usuario) |
| Motivo | El usuario pidió rango 2015–2025; el histórico real empieza en 2018-06-27. Se usa el máximo disponible hasta el límite superior pedido. |

**Nota:** hay ~1 año adicional de data (hasta 2026-06-25) disponible en el export local si el usuario quiere extender la ventana OOS en una iteración futura.

## 3. Diagnóstico de régimen (data horaria, resampleada a diaria, ventana 2018-06-27→2024-12-31)

| Ventana | Periodo | Retorno total | Vol. anualizada |
|---|---|---|---|
| Larga (estructural) | 2018-06-27 → 2024-12-31 (6.5 años) | +200.2% | ~21.1% |
| Media (3 años) | 2021-12-31 → 2024-12-31 | +28.8% | ~20.3% |
| Reciente (1 año) | 2024-01-02 → 2024-12-31 | +27.8% | ~16.5% |
| Muy reciente (3 meses) | 2024-10-01 → 2024-12-31 | +6.5% | ~15.4% |

Retornos anuales: 2018 −10.2%, 2019 +37.5%, 2020 +46.9%, 2021 +27.0%, **2022 −33.0%** (drawdown máximo −35.6%, nov-2022), 2023 +55.2%, 2024 +27.8%.

```text
Diagnóstico de régimen:
- Tendencia larga: alcista (con corrección severa 2022)
- Tendencia media/reciente: alcista
- Volatilidad larga: alta (impulsada por 2020 y 2022)
- Volatilidad media/reciente: media, con compresión gradual hacia 15-16% anualizado
- Régimen actual (matriz 3x3): Régimen 4 — Alcista + volatilidad media (tendencia suave)
- Régimen secundario: Régimen 1 — Alcista + volatilidad alta (riesgo de reversión tipo 2022)
- Edges priorizados: Trend Following, Pullback/Continuation, Volatility Expansion Breakout, Mean Reversion selectiva (buy-the-dip)
- Edges descartados: Mean reversion neutral both-side, breakout short, estacional puro (régimen no lateral, sesgo alcista dominante y persistente)
- Justificación: 6.5 años de alza sostenida con una única corrección mayor (2022) y volatilidad reciente moderada y decreciente. Dirección long-only justificada en todos los edges por el sesgo estructural + reciente (regla §9.1).
```

## 4. Selección de timeframe y ventanas IS/OOS

```text
Timeframes candidatos: M3, M15, H1
Timeframes elegidos: H1 (E1, E3) y M15 (E2, E4) — M3 no se usó por falta de necesidad de mayor granularidad
  para las 4 tesis elegidas y por mayor riesgo de same-bar/ambiguous trades sin tick data adicional confirmada.
Data total disponible: 2018-06-27 → 2026-06-25
Periodo Builder/IS elegido: 2018-06-27 → 2023-05-31 (~59.1 meses)
Periodo OOS elegido: 2023-06-01 → 2025-01-01 (~19.1 meses)
Data descartada o no usada: pre-2018-06-27 (inexistente) y post-2025-01-01 (existe, no usada por límite pedido)
Motivo del corte: banda OOS 25% (fondeo/prop firm, histórico 5-8 años útiles → banda 20-25%/25-30% combinada)
Riesgo principal: histórico de sólo 6.5 años incluye un único ciclo bajista severo (2022); SPP/WFA deben confirmar
  que los edges no dependen exclusivamente del tramo alcista 2023-2024.
```

### 4.1 Auditoría OOS 20–30% (obligatoria, bloqueante)

| Fecha inicio útil | Fecha fin útil | Corte IS/OOS | Días totales | Días OOS | OOS% objetivo | OOS% detectado | Estado |
|---|---|---|---|---|---|---|---|
| 2018-06-27 | 2025-01-01 | 2023-06-01 | 2379 | 579 | 25% | **24.3%** | **PASS** (20%≤24.3%≤30%) |

Objetivo tratado como **Fondeo/prop firm** (proyecto raíz `PropFirm_Management`), banda 25–30% con default 25%; histórico de 6.5 años (banda 5–8 años → 20–25%) — se usó el punto de encuentro 25%, redondeado a inicio de mes (2023-06-01).

`OOS Global Period` = periodo normal útil completo (2018-06-27→2025-01-01) en la tarea OOS; `OOS1 Data Range Part` = ventana reciente (2023-06-01→2025-01-01), marcada como Out-of-sample. Filtros OOS calibrados sobre OOS1 (19.1 meses), no sobre el histórico completo.

## 5. Fichas de edge

| Campo | E1 Trend Following | E2 Pullback/Continuation | E3 Volatility Expansion Breakout | E4 Selective Mean Reversion |
|---|---|---|---|---|
| Timeframe | H1 | M15 | H1 | M15 |
| Dirección | Long only | Long only | Long only | Long only |
| Tesis | EMA rápida > EMA lenta + ADX creciente confirma persistencia direccional | Retroceso hacia EMA con RSI saliendo de zona baja, a favor de tendencia | Ruptura del máximo de N barras + expansión de ATR confirma continuación | RSI sobrevendido / banda inferior de Bollinger dentro de tendencia alcista (buy-the-dip) |
| Order type | EnterAtMarket | EnterAtMarket | EnterAtStop | EnterAtMarket |
| StopLimitBlocks | — (Market) | — (Market) | Highest, ATR Range | — (Market) |
| Indicadores | EMA, SMA, ADX, ATR | EMA, SMA, RSI, ATR | ATR, Highest, Lowest | EMA, RSI, BollingerBands, ATR |
| Señales | MARising/Falling, MABarCloses*, ADXRising, ADXHigher | MARising/Falling, RSICrossUp/Down, RSILower, RSIRising | ATRRising/Higher/Falling | RSILower, RSICrossUp, RSIRising, MARising |
| Comparadores comunes | IsGreater(OrEqual), IsLower(OrEqual), CrossesAbove/Below, IsRising/Falling, Prices.* (idénticos en los 4 edges) |||| 
| Salidas | SL + PT + Trailing ATR (deja correr) | SL + PT + ExitAfterBars | SL + PT + Trailing ATR | SL + PT + ExitAfterBars |
| MoveSL2BE | Desactivado (los 4 edges, por defecto no se recomienda) |||| 
| SL ATR mult. | 1.2–2.8 (per. 14–28) | 1.0–2.2 (per. 14–21) | 1.4–3.0 (per. 14–28) | 1.0–2.0 (per. 10–20) |
| PT ATR mult. | 2.0–4.5 (per. 14–28) | 1.2–2.8 (per. 14–21) | 2.5–5.0 (per. 14–28) | 1.0–2.2 (per. 10–20) |
| RulesComplexity (cond/período) | 2-3 cond, período 10-100 | 2-4 cond, período 5-60 | 1-3 cond, período 10-80 | 2-4 cond, período 5-50 |
| TradesPerMonth asumido* | 1.5/mes | 6.0/mes | 1.2/mes | 8.0/mes |

\* Asunción calibrada por familia+timeframe según guía Skill 1 §12.2 (H1) escalada ×2 para M15 (no hay tabla M15 explícita en la skill disponible); **ajustar según Strategy dismissal stats reales** (protocolo Skill 1 §25-28).

## 6. Genetic Options y Ranking Final (Builder) — calculados sobre Meses_IS ≈ 59.1

| Edge | Genetic: PF > | Genetic: NumTrades > (60% del final) | Genetic: DD < | Ranking: NumTrades > | Ranking: PF > | Ranking: Ret/DD > | Ranking: DD < | Stagnation < | AvgTrade > | WinningPct > |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | 1.02 | 53 | 60 | **89** | 1.05 | 1.60 | 40 | 40 | 0 | (no exigido) |
| E2 | 1.02 | 213 | 55 | **355** | 1.10 | 1.80 | 35 | 35 | 0 | 38 |
| E3 | 1.00 | 43 | 65 | **71** | 1.03 | 1.50 | 42 | 42 | 0 | (no exigido) |
| E4 | 1.02 | 284 | 55 | **473** | 1.12 | 1.70 | 32 | 32 | 0 | 45 |

Fitness principal en los 4 edges: `ReturnDDRatio` (perfil fondeo/incubación). Genetic prefilters deliberadamente más suaves que Ranking Final (regla §11 de Skill 1). `MaxStrategies=1800`, `StopCondition=databank-full, passedStrategies=900, restart=8` (conservados del base, valores razonables modo balanceado — no se tocaron por falta de orden explícita de cambiar la profundidad de búsqueda).

Métricas usadas: solo las **confirmadas con formato XML verificado** en el `.cfx` base (`NumberOfTrades`, `ProfitFactor`, `DrawdownPct`, `StagnationPct`, `AvgTrade`, `WinningPct`, `ReturnDDRatio`, `NetProfit`). No se inventaron formatos para `SharpeRatio`/`RecoveryFactor`/`Stability`/`RSquared`; si se desean, añadirlos manualmente en el Ranking de SQX (regla anti-invención, Skill 1 §16.3).

## 7. Robustez por etapa

### 7.1 OOS (Meses_OOS ≈ 19.1)

| Edge | NumTrades OOS > | PF > | Ret/DD > | DD < |
|---|---|---|---|---|
| E1 | 29 | 1.03 | 0.90 | 48 |
| E2 | 114 | 1.03 | 0.90 | 43 |
| E3 | 23 | 1.03 | 0.90 | 50 |
| E4 | 152 | 1.03 | 0.90 | 40 |

`NetProfit>0`, `AvgTrade>0` también activos. `DeleteFailedStrategies=true`. `OOS Global Period` = 2018-06-27→2025-01-01; `OOS1` = 2023-06-01→2025-01-01 (ver §4.1).

### 7.2 MC_TRADES (Monte Carlo Trades Manipulation)

Configuración **conservada del base** (ya conforme a Skill 2 §9.5-9.6): `RandomizeTradesOrder(exact)` + `RandomlySkipTrades(10%)`, 1000 simulaciones, `MCUseFullSample=true`. Acceptance: `NetProfit MC95% ≥ 60%` del original, `DrawdownPct MC95% ≤ 175%` del original (idéntico en los 4 edges — son condiciones relativas, no dependen del edge/timeframe). Corrección aplicada: `DeleteFailedStrategies` false→**true** en los 4 edges.

### 7.3 MC_SPREAD_SLIPPAGE (Monte Carlo Retest Methods)

Recalibrado a la escala real de costos de NDXm (tickSize 0.01, spread base 1.00, slippage base 0.01 — el base traía escala FX de 1e-4):

| Parámetro | Valor base (FX, descartado) | Valor aplicado (NDXm) |
|---|---|---|
| RandomizeSpread Min/Max | 0.2 / 2 | **1.00 / 3.00** (1×–3× spread base) |
| RandomizeSlippage Min/Max | 0 / 1 | **0 / 0.03** (0–3× slippage base) |

Acceptance conservado del base (relativo, válido para cualquier instrumento): `NetProfit MC Retest ≥ 55%` del original, `DrawdownPct MC Retest ≤ 160%` del original. `DeleteFailedStrategies` false→**true**.

### 7.4 TICK (Retest Tick/Real Spread/Slowest)

**Limitación declarada:** no se confirmó en Data Manager un símbolo tick/M1 nativo de Tickmill independiente del recurso `NDXm_TICK_UTCPlus02` ya usado en Builder/OOS. Por Symbol Resource Exact (Skill 3 §13) no se debe inventar un segundo recurso no verificado, así que **TICK reutiliza el mismo símbolo/fuente que Builder/OOS**, corriendo sobre el periodo completo (2018-06-27→2025-01-01, Meses≈78.2) en vez de solo una ventana tick independiente. Esto reduce el valor incremental de esta etapa como validación verdaderamente independiente — **recomendado**: confirmar en Data Manager si existe un símbolo M1/tick nativo de Tickmill distinto, y si existe, sustituirlo en esta tarea.

El Ranking Final de esta etapa venía **vacío** en la base (`<Conditions />`); se construyó desde cero (Skill 2 §11.6):

| Edge | NumTrades TICK > | PF > | Ret/DD > | DD < |
|---|---|---|---|---|
| E1 | 117 | 1.02 | 0.70 | 50 |
| E2 | 469 | 1.02 | 0.70 | 45 |
| E3 | 94 | 1.02 | 0.70 | 52 |
| E4 | 626 | 1.02 | 0.70 | 42 |

`NetProfit>0`, `AvgTrade>0` también activos. `RetestOnAdditionalMarkets` (crosscheck redundante contra el mismo símbolo) se dejó **desactivado** para no duplicar validación sobre el mismo recurso sin aportar información nueva. `DeleteFailedStrategies` ya era `true` en el base para esta tarea (conservado).

### 7.5 SPP (Strategy Parameter Permutation)

Configuración conservada del base (ya conforme a Skill 2 §12.5-12.7, perfil "SPP fuerte"): `MaxTests=500`, `DistributionUp/Down=25`, `Steps=5`, `ProfitOptPct=45`, `UniformDistrChanges=5`. Corrida sobre periodo completo 2018-06-27→2025-01-01. `DeleteFailedStrategies` false→**true**.

### 7.6 WFA MATRIX

Configuración conservada del base (ya conforme a Skill 2 §13.5): `MaxTests=3000`, `thresholdPct=80`, `robCombRows=2`, `robCombCols=2`, `robMinComb=3`. Corrida sobre periodo completo. `DeleteFailedStrategies` false→**true**.

Nota de diseño conservada del base: los cross-checks propios de SPP/WFA usan un chart D1 y un chart H4 del mismo símbolo como verificación adicional de contexto multi-timeframe, independientemente del timeframe nativo del edge (H1/M15) — no se modificó, es un diseño intencional del template maestro.

## 8. Costos inyectados (nodos protegidos, modificación autorizada por el usuario)

| Campo | Valor usuario | Aplicado en `.cfx` | Fuente |
|---|---|---|---|
| Pip/Tick size | 0.01 | `tickSize=0.01` | Usuario explícito |
| Point value ($) | 1 | `pointValue=1.0`, `tickValueInMoney=1.0` | Usuario explícito |
| Default spread | 100 "pips" | `defaultSpread=1.00` (100 × tickSize) | Usuario explícito |
| Default slippage | 1 "pip" | `defaultSlippage=0.01` (1 × tickSize) | Usuario explícito |
| Comisión | $0.00 | `Commission Method=SizeBased, value=0` | Usuario explícito |
| Swap Long/Short | −4.95 / −1.3 | `Swap type=points long=-4.95 short=-1.3` | Usuario explícito |
| Pip/Tick step | (no especificado) | `tickStep=0.01` | Default técnico razonable |
| Min distance | (no especificado) | `minDistance=0` | Default técnico razonable (el valor FX heredado de 25.0 habría bloqueado entradas Stop en E3) |
| Order size multiplier/step | (no especificado) | `1.0` / `0.01` (heredado del base) | Default técnico, no exigido |
| Triple swap on / Rollout hour | (no especificado) | `WEDNESDAY` / `23:00` (heredado del base) | Default técnico estándar |
| Capital inicial | 1000 USD | `InitialCapital=1000` | Usuario explícito |
| Riesgo por operación (FixedAmount) | (no especificado) | `RiskedMoney=15` (1.5% del capital) | **Ajuste recomendado no ordenado explícitamente — confirmar antes de operar en real** (el base traía $50 sobre $50000 = 0.1%; escalado proporcional a $1000 daría solo $1, insuficiente para tamaño de posición realista) |

## 9. Nodos protegidos NO modificados sin autorización

Broker profile (id/txt), instrument settings más allá de lo listado arriba, custom indicators (`user/extend/Snippets/...`), custom blocks, Java snippets: **intactos**. `MaxDrawdown` circuito de RiskManagement (30%) y `MoneyManagement` method (`FixedAmount`) tipo: **conservados del base**, no se cambió el método, solo el monto.

## 10. Session Resource Safe (Skill 3 §92 / Skill 4 §51-59)

**Clasificación: C — NoNativeTimeFilterSafe**, basada en evidencia de un proyecto hermano real y ya abierto en esta instalación SQX (`user/projects/Builder/NDXm_Qlib_OOS20.cfx`, mismo símbolo `NDXm_TICK_UTCPlus02`), que usa `Session="No Session"` y `MarketOpenSession="No Session"` sin incidencia reportada.

| Campo | Valor aplicado | Fuente | Estado |
|---|---|---|---|
| `Param key="Session"` | No Session | Proyecto hermano validado | PASS_NO_NATIVE_TIME_FILTER |
| `Param key="MarketOpenSession"` | No Session | Proyecto hermano validado (sobreescribe patrón FX heredado `FX_XCCY_Currency1...`, inaplicable a un índice) | PASS_NO_NATIVE_TIME_FILTER |
| `<Sessions>` embebido | Vaciado (`<Sessions/>` sin hijos) en los 8 XML de cada `.cfx` | Regla Existing/No-Donor Safe: el base traía una sesión FX incrustada sin donor probado para Tickmill | PASS |
| `LimitTimeRange` | `false` en las 8 tareas | Default seguro (ya venía así en el base) | PASS |

No se incrustó ninguna sesión inventada ni se infirió un nombre uniendo "broker profile" al nombre base (prohibido por Skill 3 §93).

## 11. ShortNameSafe

| Archivo `.cfx` | Project name | Longitud | Nombre archivo | Longitud archivo | Ruta de importación |
|---|---|---|---|---|---|
| NDXM_TMILL_E1_H1TF.cfx | NDXM_TMILL_E1_H1TF | 18 | NDXM_TMILL_E1_H1TF.cfx | 23 | `C:\SQX_IMPORT\` |
| NDXM_TMILL_E2_M15PB.cfx | NDXM_TMILL_E2_M15PB | 19 | NDXM_TMILL_E2_M15PB.cfx | 24 | `C:\SQX_IMPORT\` |
| NDXM_TMILL_E3_H1BO.cfx | NDXM_TMILL_E3_H1BO | 18 | NDXM_TMILL_E3_H1BO.cfx | 23 | `C:\SQX_IMPORT\` |
| NDXM_TMILL_E4_M15MR.cfx | NDXM_TMILL_E4_M15MR | 19 | NDXM_TMILL_E4_M15MR.cfx | 24 | `C:\SQX_IMPORT\` |

Todos ≤25 caracteres (preferido), solo caracteres `A-Z0-9_`, sin espacios/tildes/corchetes, ninguno reutiliza un nombre previamente fallido (proyectos nuevos). Ya copiados a `C:\SQX_IMPORT\`.

## 12. Auditoría Symbol Resource Exact — **REQUIERE CONFIRMACIÓN DEL USUARIO**

No tengo acceso en vivo al Data Manager de esta instalación SQX; los siguientes valores se fijaron por la mejor evidencia disponible (proyecto hermano `NDXm_Qlib_OOS20.cfx`) y **deben confirmarse/ajustarse en el diálogo "Resolve project resources" al importar**:

| Campo | Valor usado | Confirmar |
|---|---|---|
| Symbol name | `NDXm_TICK_UTCPlus02` | Coincide con el proyecto hermano — alta confianza |
| Source | `1` (File) | Heredado del base FX; verificar que Data Manager real usa "File" para este símbolo |
| Precision | `TICK` | Heredado del base; verificar precisión real (podría ser H1 si el import fue agregado) |
| Broker id | `-1` (sin broker asociado, coherente con `source=File`) | Verificar |
| uSymbol / uSymbolName | vacío | Verificar si Data Manager exige un valor |
| Broker profile (Tickmill) | id/nombre no confirmado (el `id="25"` del catálogo interno queda huérfano/no referenciado por nuestros símbolos, que usan `broker="-1"`) | No bloqueante, pero confirmar si en algún momento se activa el crosscheck de mercado adicional |

Per Skill 3 §17, si al importar aparece "Resolve project resources" **sin filas concretas de símbolo/sesión incorrectas**, pulsar "Load config using these settings" — no es un fallo bloqueante. Si SQX propone un símbolo distinto o muestra una fila de error concreta, **no forzar**: confirmar el recurso real en Data Manager antes de continuar.

## 13. Auditoría DataBank chain

Cadena `config.xml` (no modificada, verificada intacta en los 4 `.cfx`):

```
Results → OOS → MC_TRADES → MC_SPREAD_SLIPPAGE → TICK → SPP → WFA MATRIX
```

`GESTION MONETARIA - DESACTIVADA` permanece `active="false"`, fuera de la cadena principal. Confirmado idéntico en los 4 archivos.

## 14. Auditoría Operators Safe (bloqueante, Skill 3 §84-90)

| Edge | OrderTypes activos | StopLimitBlocks activos | Indicadores activos | Comparadores activos | Estado |
|---|---|---|---|---|---|
| E1 | 1 (EnterAtMarket) | 0 (correcto, Market-only) | 4 | 8 comunes | PASS |
| E2 | 1 (EnterAtMarket) | 0 | 4 | 8 comunes | PASS |
| E3 | 1 (EnterAtStop) | 2 (Highest, ATR Range) | 3 | 8 comunes | PASS |
| E4 | 1 (EnterAtMarket) | 0 | 4 | 8 comunes | PASS |

**Corrección aplicada:** el `.cfx` base traía **2 Order Types activos simultáneamente** (`EnterAtMarket` + `EnterAtLimit`) y `MoveSL2BE` activado por defecto — ambos son residuos que la Skill 3 marca como bloqueantes/no recomendados. Se corrigieron en los 4 edges (exactamente 1 Order Type activo; `MoveSL2BE` desactivado).

## 15. Checklist final (Skill 1 §14.3 / Skill 3 §18)

```
[x] Los 4 .cfx abren como ZIP válido (verificado con re-parseo XML completo de los 9 archivos internos de cada uno).
[x] Cada .cfx contiene config.xml + Build-Task1.xml + Retest-Task1..7.xml.
[x] XML parseable en los 4 archivos (36 archivos internos verificados).
[x] Cero placeholders __X__ o [[X]] residuales (verificado por grep en los 4 edges).
[x] Nodos protegidos no-costo intactos (broker profile, custom indicators/blocks/snippets).
[x] Ranking Final y Genetic Options reconstruidos desde cero por edge (no heredados sin ajuste).
[x] Genetic prefilters más suaves que Ranking Final (verificado numéricamente por edge).
[x] Exactamente 1 Order Type activo por edge; StopLimitBlocks=0 en Market-only, >0 en Stop-only.
[x] StopLoss activo en los 4 edges.
[x] OOS% dentro de 20-30% (24.3%, PASS).
[x] DeleteFailedStrategies=true en OOS/MC_TRADES/MC_SPREAD_SLIPPAGE/TICK/SPP/WFA (corregido).
[x] Session Resource Safe: No Session (evidenciado por proyecto hermano), sin <Session> embebida sin donor.
[x] Project name ShortNameSafe (≤25 chars, charset válido) en los 4 archivos.
[x] DataBank chain intacta y verificada.
[ ] REQUIERE CONFIRMACIÓN: Symbol Resource Exact (source/precision/broker id) contra Data Manager real — ver §12.
[ ] REQUIERE CONFIRMACIÓN: ¿existe un símbolo tick/M1 nativo de Tickmill separado para fortalecer la etapa TICK? — ver §7.4.
[ ] REQUIERE CONFIRMACIÓN: RiskedMoney=$15 (1.5% de $1000) es un default razonado, no una orden explícita — confirmar antes de operar en real.
```

## 16. Prueba de humo de importación (instrucciones para el usuario)

```
1. Cerrar StrategyQuant X.
2. Verificar que no exista ya una carpeta en user/projects con estos nombres de proyecto
   (NDXM_TMILL_E1_H1TF, _E2_M15PB, _E3_H1BO, _E4_M15MR) — son nombres nuevos, no deberían chocar.
3. Importar cada .cfx desde C:\SQX_IMPORT\.
4. Si aparece "Resolve project resources": revisar filas concretas.
   - Si no hay filas de símbolo/sesión erróneas, pulsar "Load config using these settings".
   - Si SQX propone un símbolo distinto al esperado (NDXm_TICK_UTCPlus02) o hay fila roja concreta,
     DETENER y confirmar el recurso real en Data Manager (ver §12) antes de continuar.
5. Verificar que NO aparece "Failed to convert session 'No Session' to xml" ni
   "Cannot resolve custom resources / Failed to update zip content".
6. Verificar Data Banks visibles: Results, OOS, MC_TRADES, MC_SPREAD_SLIPPAGE, TICK, SPP, WFA MATRIX.
7. Verificar símbolo por tarea: Builder/OOS/MC/SPP/WFA y TICK todos deberían mostrar NDXm_TICK_UTCPlus02.
8. Presionar Start en el Builder y observar "Strategy dismissal stats" tras 30-120 minutos.
```

## 17. Plan de diagnóstico si no llegan candidatos al Data Bank (Skill 1 §21-28)

Si `Accepted=0` o el Data Bank OOS recibe muy pocas estrategias tras 30-120 minutos, pedir captura de "Strategy dismissal stats" y relajar **en este orden** (nunca tocar spread/slippage/comisión):

```
1. Cross Checks de mercado adicional (no aplica aquí, están desactivados).
2. Genetic prefilters (PF, NumberOfTrades).
3. ProfitFactor del Ranking Final.
4. ReturnDDRatio.
5. WinningPct (solo en E2/E4, donde está activo).
6. NumberOfTrades del Ranking Final (recalcular proporcional si el timeframe/edge no da la frecuencia asumida en §5).
7. StagnationPct, luego DrawdownPct.
8. Complejidad de reglas / amplitud de bloques.
9. Timeframe o edge alternativo compatible con el régimen (§3).
```

Los `TradesPerMonth` asumidos en M15 (E2, E4) son la mayor fuente de incertidumbre: se escalaron desde la guía H1 de la Skill 1 (no hay tabla M15 explícita disponible) y **deben recalibrarse con datos reales de Builder** si difieren significativamente.
