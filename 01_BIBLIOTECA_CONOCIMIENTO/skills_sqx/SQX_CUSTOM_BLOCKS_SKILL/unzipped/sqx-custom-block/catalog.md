# Atom catalog — discovered from this install

- config.xml: `C:\SQX_144_Full\internal\web\SQWIZARD\branding\global\config.xml`
- export: (none provided)
- registry: `C:\SQX_144_Full\internal\web\SQWIZARD\branding\global\UserCustomIndicators.xml`
- snippets: `C:\SQX_144_Full\user\extend`
- **171 native built-ins** + **3 YOUR custom indicators** (1 registered in config, 0 from exports, 0 from .java, 2 synthesized) = **174 total**

`bindable` = period/double params you can attach to an outer optimizer knob.
`mid` = midline for oscillators (the level a signal is measured against).
`⚠` = talib_* — UNUSABLE in single-symbol/FX builds (Stockpicker NPE); portfolio-only.
`◆` = multi-output — needs a #Line# pick (emit handles it; choose the output).
`✦` = your coded custom indicator (parsed from its Java snippet) — contract is read straight from @BuildingBlock/@Parameter/@Output; VERIFY on first import (seed via one block + export to promote to proven).
`✎` = synthesized from UserCustomIndicators.xml — best-effort schema, VERIFY on first import (or seed it: use it in one block, export, re-bootstrap → becomes proven).

## ⭐ YOUR custom indicators (3)

Indicators that are **yours** — imported or coded by you, identified by the `customSnippet` marker in your config plus any exported blocks / .java snippets / registry entries. Build blocks from any of these exactly like the native ones. `source` shows where each was read from.

| key | display | returnType | mid | source |
|---|---|---|---|---|
| `Adaptive_smoothing` | `Adaptive_smoothing(@Chart@#MaeDevLength#, #Price#)[#Shift#]` | price |  | registry |
| `Fractals` | `Fractals(@Chart@).#Line#[#Shift#]` | price |  | registry |
| `QlibSignal` | `QlibSignal(@Chart@)[#Shift#]` | number | 0 | config |

## config / indicator  (127)

| key | display | returnType | mid | bindable | flags |
|---|---|---|---|---|---|
| `ADX` | `ADX(@Chart@#Period#, #Line#)[#Shift#]` | number |  | #Period# | ◆ |
| `AnchoredVWAP` | `AnchoredVWAP(@Chart@#SessionType#,#StdDevMult#)[#Shift#]` | price |  | #StdDevMult# |  |
| `Aroon` | `Aroon(@Chart@#Period#).#Line#[#Shift#]` | number | 50 | #Period# | ◆ |
| `AvgVolume` | `AV(@Chart@#Period#)[#Shift#]` | number |  | #Period# |  |
| `AwesomeOscillator` | `AwesomeOscillator(@Chart@)[#Shift#]` | number | 0 | — |  |
| `BearsPower` | `BearsPower(@Chart@#Period#, #ComputedFrom#)[#Shift#]` | number | 0 | #Period# |  |
| `BollingerBands` | `BollingerBands(@Chart@#Period#, #Deviation#).#Line#[#Shift#]` | price |  | #Period#, #Deviation# | ◆ |
| `BullsPower` | `BullsPower(@Chart@#Period#, #ComputedFrom#)[#Shift#]` | number | 0 | #Period# |  |
| `CCI` | `CCI(@Chart@#Period#)[#Shift#]` | number | 0 | #Period# |  |
| `DeMarker` | `DeMarker(@Chart@#Period#)[#Shift#]` | number | 0.5 | #Period# |  |
| `EMA` | `EMA(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `Fibo` | `Fibo(@Chart@)` | price |  | — |  |
| `Fractal` | `Fractal(@Chart@#Fractal#)[#Shift#]` | price |  | — | ◆ |
| `GannHiLo` | `GannHiLo(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `HeikenAshi` | `Heiken Ashi(@Chart@)[#Shift#]` | price |  | — | ◆ |
| `Highest` | `Highest(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `HighestInRange` | `HighestInRange(@Chart@#TimeFrom#, #TimeTo#)[#Shift#]` | price |  | — |  |
| `HighestIndex` | `HighestIndex(@Chart@#Period#)[#Shift#]` | number |  | #Period# |  |
| `HullMovingAverage` | `HMA(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `Ichimoku` | `Ichimoku(@Chart@#TenkanPeriod#,#KijunPeriod#,#SenkouPeriod#,#Line#)[#Shift#]` | price |  | #TenkanPeriod#, #KijunPeriod#, #SenkouPeriod# | ◆ |
| `KAMA` | `Kaufman's Adaptive Moving Average(@Chart@#ERPeriod#,#ShortPeriod#,#LongPeriod#)[#Shift#]` | price |  | #ERPeriod#, #ShortPeriod#, #LongPeriod# |  |
| `KaufmanEfficiencyRatio` | `Kaufman Efficiency Ratio(@Chart@#Period#)[#Shift#]` | number | 0.5 | #Period# |  |
| `KeltnerChannel` | `Keltner Channel(@Chart@#Period#, #Deviation#).#Line#[#Shift#]` | price |  | #Period#, #Deviation# | ◆ |
| `LWMA` | `LWMA(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `LaguerreRSI` | `Laguerre RSI(@Chart@#Gamma#)[#Shift#]` | number | 0.5 | #Gamma# |  |
| `LinearRegression` | `LinReg(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `Lowest` | `Lowest(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `LowestInRange` | `LowestInRange(@Chart@#TimeFrom#, #TimeTo#)[#Shift#]` | price |  | — |  |
| `LowestIndex` | `LowestIndex(@Chart@#Period#)[#Shift#]` | number |  | #Period# |  |
| `MACD` | `MACD(@Chart@#Fast#, #Slow#, #Smooth#).#Line#[#Shift#]` | number | 0 | #Fast#, #Slow#, #Smooth# | ◆ |
| `MTKeltnerChannel` | `MT Keltner Channel(@Chart@#Period#, #Deviation#).#Line#[#Shift#]` | price |  | #Period#, #Deviation# | ◆ |
| `Momentum` | `Momentum(@Chart@#Period#)[#Shift#]` | number | 100 | #Period# |  |
| `MovingAverage` | `MA(@Chart@#Period#, #MAMethod#)[#Shift#]` | price |  | #Period# |  |
| `OSMA` | `OSMA(@Chart@#FastEMA#, #SlowEMA#, #SignalPeriod#)[#Shift#]` | number | 0 | #FastEMA#, #SlowEMA#, #SignalPeriod# |  |
| `ParabolicSAR` | `ParabolicSAR(@Chart@#Step#, #Maximum#)[#Shift#]` | price |  | #Step#, #Maximum# |  |
| `Pivots` | `Pivots(@Chart@#StartHour#:#StartMinute#).#Line#[#Shift#]` | price |  | — | ◆ |
| `QQE` | `QQE(@Chart@#RSIPeriod#)[#Shift#]` | number | 50 | #RSIPeriod#, #sF#, #wF# | ◆ |
| `QlibSignal` | `QlibSignal(@Chart@)[#Shift#]` | number | 0 | — | ✦ |
| `ROC` | `ROC(@Chart@#Period#)[#Shift#]` | number |  | #Period# |  |
| `RSI` | `RSI(@Chart@#Period#)[#Shift#]` | number | 50 | #Period# |  |
| `Reflex` | `Reflex(@Chart@#Period#)[#Shift#]` | number |  | #Period# |  |
| `SMA` | `SMA(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `SMMA` | `SMMA(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `SRPercentRank` | `SRPercRank(@Chart@#Mode#,#Length#,#ATRPeriod#)[#Shift#]` | number | 50 | #Length#, #ATRPeriod# |  |
| `SchaffTrendCycle` | `Schaff Trend Cycle(@Chart@#StochPeriod#,#FastPeriod#,#SlowPeriod#)[#Shift#]` | number | 50 | #StochPeriod#, #FastPeriod#, #SlowPeriod# |  |
| `StdDev` | `StdDev(@Chart@#Period#)[#Shift#]` | number |  | #Period# |  |
| `Stochastic` | `Stoch(@Chart@#KPeriod#, #DPeriod#, #Slowing#).#Line#[#Shift#]` | number | 50 | #KPeriod#, #DPeriod#, #Slowing# | ◆ |
| `SuperTrend` | `SuperTrend(@Chart@#Mode#,#ATRPeriod#,#ATRMult#)[#Shift#]` | price |  | #ATRPeriod#, #ATRMult# |  |
| `TEMA` | `TEMA(@Chart@#Period#)[#Shift#]` | price |  | #Period# |  |
| `TPOProfile` | `TPO_Letters(#SessionType#,#ProfileRows#,#ValueAreaPct#).#Line#[#Shift#]` | price |  | #ValueAreaPct# | ◆ |
| `UlcerIndex` | `Ulcer Index(@Chart@#Mode#,#Period#)[#Shift#]` | number |  | #Period# |  |
| `VWAP` | `Volume Weighted Average Price - VWAP(@Chart@#VWAPPeriod#)[#Shift#]` | price |  | #VWAPPeriod# |  |
| `VolumeProfile` | `VolumeProfile(#SessionType#,#ProfileRows#,#ValueAreaPct#).#Line#[#Shift#]` | price |  | #ValueAreaPct#, #ClusterSpread#, #PivotPct#, #PivotATRMultiple#, #PivotATRPeriod# | ◆ |
| `VolumeProfileCustomHours` | `VolumeProfileCH(#SessionStartHours#:#SessionStartMinutes#-#SessionEndHours#:#SessionEndMinutes#,#ProfileRows#,#ValueAreaPct#).#Line#[#Shift#]` | price |  | #ValueAreaPct#, #ClusterSpread# | ◆ |
| `VolumeProfileCustomHoursMultiSession` | `VolumeProfileCHMulti(#ProfileRows#,#ValueAreaPct#).#Line#[#Shift#]` | price |  | #ValueAreaPct#, #ClusterSpread# | ◆ |
| `Vortex` | `Vortex(@Chart@#Period#)[#Shift#]` | number |  | #Period# | ◆ |
| `WaveTrend` | `WaveTrend(@Chart@#ChannelLength#,#AverageLength#).#Line#[#Shift#]` | number | 0 | #ChannelLength#, #AverageLength# | ◆ |
| `WilliamsPR` | `Williams %R(@Chart@#Period#)[#Shift#]` | number | -50 | #Period# |  |
| `talib_AD` | `AD(@Chart@)[#Shift#]` | number |  | — | ⚠ |
| `talib_ADOSC` | `ADOSC(@Chart@#FastPeriod#,#SlowPeriod#)[#Shift#]` | number |  | #FastPeriod#, #SlowPeriod# | ⚠ |
| `talib_ADX` | `ADX(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_ADXR` | `ADXR(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_APO` | `APO(@Chart@#FastPeriod#,#SlowPeriod#,#MAType#)[#Shift#]` | number |  | #FastPeriod#, #SlowPeriod# | ⚠ |
| `talib_AROON` | `AROON(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠◆ |
| `talib_AROONOSC` | `AROONOSC(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_ATR` | `ATR(@Chart@#TimePeriod#)[#Shift#]` | pricerange |  | #TimePeriod# | ⚠ |
| `talib_BBANDS` | `BBANDS(@Chart@#TimePeriod#,#NbDevUp#,#NbDevDn#,#MAType#)[#Shift#]` | price |  | #TimePeriod#, #NbDevUp#, #NbDevDn# | ⚠◆ |
| `talib_BETA` | `BETA(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_BOP` | `BOP(@Chart@)[#Shift#]` | number |  | — | ⚠ |
| `talib_CCI` | `CCI(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_CMO` | `CMO(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_CORREL` | `CORREL(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_DEMA` | `DEMA(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_DX` | `DX(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_EMA` | `EMA(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_HT_DCPERIOD` | `HT_DCPERIOD(@Chart@)[#Shift#]` | number |  | — | ⚠ |
| `talib_HT_DCPHASE` | `HT_DCPHASE(@Chart@)[#Shift#]` | number |  | — | ⚠ |
| `talib_HT_PHASOR` | `HT_PHASOR(@Chart@)[#Shift#]` | number |  | — | ⚠◆ |
| `talib_HT_SINE` | `HT_SINE(@Chart@)[#Shift#]` | number |  | — | ⚠◆ |
| `talib_HT_TRENDLINE` | `HT_TRENDLINE(@Chart@)[#Shift#]` | number |  | — | ⚠ |
| `talib_HT_TRENDMODE` | `HT_TRENDMODE(@Chart@)[#Shift#]` | number |  | — | ⚠ |
| `talib_KAMA` | `KAMA(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_LINEARREG` | `LINEARREG(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_LINEARREG_ANGLE` | `LINEARREG_ANGLE(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_LINEARREG_INTERCEPT` | `LINEARREG_INTERCEPT(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_LINEARREG_SLOPE` | `LINEARREG_SLOPE(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_MA` | `MA(@Chart@#TimePeriod#,#MAType#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_MACD` | `MACD(@Chart@#FastPeriod#,#SlowPeriod#,#SignalPeriod#)[#Shift#]` | number |  | #FastPeriod#, #SlowPeriod#, #SignalPeriod# | ⚠◆ |
| `talib_MACDEXT` | `MACDEXT(@Chart@#FastPeriod#,#FastMAType#,#SlowPeriod#,#SlowMAType#,#SignalPeriod#,#SignalMAType#)[#Shift#]` | number |  | #FastPeriod#, #SlowPeriod#, #SignalPeriod# | ⚠◆ |
| `talib_MACDFIX` | `MACDFIX(@Chart@#SignalPeriod#)[#Shift#]` | number |  | #SignalPeriod# | ⚠◆ |
| `talib_MAMA` | `MAMA(@Chart@#FastLimit#,#SlowLimit#)[#Shift#]` | price |  | #FastLimit#, #SlowLimit# | ⚠◆ |
| `talib_MAVP` | `MAVP(@Chart@#MinPeriod#,#MaxPeriod#,#MAType#)[#Shift#]` | number |  | #MinPeriod#, #MaxPeriod# | ⚠ |
| `talib_MAXINDEX` | `MAXINDEX(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_MFI` | `MFI(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_MIDPOINT` | `MIDPOINT(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_MIDPRICE` | `MIDPRICE(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_MININDEX` | `MININDEX(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_MINMAXINDEX` | `MINMAXINDEX(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠◆ |
| `talib_MINUS_DI` | `MINUS_DI(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_MINUS_DM` | `MINUS_DM(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_MOM` | `MOM(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_NATR` | `NATR(@Chart@#TimePeriod#)[#Shift#]` | pricerange |  | #TimePeriod# | ⚠ |
| `talib_OBV` | `OBV(@Chart@)[#Shift#]` | number |  | — | ⚠ |
| `talib_PLUS_DI` | `PLUS_DI(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_PLUS_DM` | `PLUS_DM(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_PPO` | `PPO(@Chart@#FastPeriod#,#SlowPeriod#,#MAType#)[#Shift#]` | number |  | #FastPeriod#, #SlowPeriod# | ⚠ |
| `talib_ROC` | `ROC(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_ROCP` | `ROCP(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_ROCR` | `ROCR(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_ROCR100` | `ROCR100(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_RSI` | `RSI(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_SAR` | `SAR(@Chart@#Acceleration#,#Maximum#)[#Shift#]` | price |  | #Acceleration#, #Maximum# | ⚠ |
| `talib_SAREXT` | `SAREXT(@Chart@#StartValue#,#OffsetOnReverse#,#AccelerationInitLong#,#AccelerationLong#,#AccelerationMaxLong#,#AccelerationInitShort#,#AccelerationShort#,#AccelerationMaxShort#)[#Shift#]` | price |  | #StartValue#, #OffsetOnReverse#, #AccelerationInitLong#, #AccelerationLong#, #AccelerationMaxLong#, #AccelerationInitShort#, #AccelerationShort#, #AccelerationMaxShort# | ⚠ |
| `talib_SMA` | `SMA(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_STDDEV` | `STDDEV(@Chart@#TimePeriod#,#NbDev#)[#Shift#]` | number |  | #TimePeriod#, #NbDev# | ⚠ |
| `talib_STOCH` | `STOCH(@Chart@#FastK_Period#,#SlowK_Period#,#SlowK_MAType#,#SlowD_Period#,#SlowD_MAType#)[#Shift#]` | number |  | #FastK_Period#, #SlowK_Period#, #SlowD_Period# | ⚠◆ |
| `talib_STOCHF` | `STOCHF(@Chart@#FastK_Period#,#FastD_Period#,#FastD_MAType#)[#Shift#]` | number |  | #FastK_Period#, #FastD_Period# | ⚠◆ |
| `talib_STOCHRSI` | `STOCHRSI(@Chart@#TimePeriod#,#FastK_Period#,#FastD_Period#,#FastD_MAType#)[#Shift#]` | number |  | #TimePeriod#, #FastK_Period#, #FastD_Period# | ⚠◆ |
| `talib_T3` | `T3(@Chart@#TimePeriod#,#VFactor#)[#Shift#]` | price |  | #TimePeriod#, #VFactor# | ⚠ |
| `talib_TEMA` | `TEMA(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_TRIMA` | `TRIMA(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_TRIX` | `TRIX(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |
| `talib_TSF` | `TSF(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_ULTOSC` | `ULTOSC(@Chart@#TimePeriod1#,#TimePeriod2#,#TimePeriod3#)[#Shift#]` | number |  | #TimePeriod1#, #TimePeriod2#, #TimePeriod3# | ⚠ |
| `talib_VAR` | `VAR(@Chart@#TimePeriod#,#NbDev#)[#Shift#]` | number |  | #TimePeriod#, #NbDev# | ⚠ |
| `talib_WILLR` | `WILLR(@Chart@#TimePeriod#)[#Shift#]` | number |  | #TimePeriod# | ⚠ |
| `talib_WMA` | `WMA(@Chart@#TimePeriod#)[#Shift#]` | price |  | #TimePeriod# | ⚠ |

## config / other  (10)

| key | display | returnType | mid | bindable | flags |
|---|---|---|---|---|---|
| `BarDate` | `` | number |  | — |  |
| `BarDayOfMonth` | `DayOfMonth[#Shift#]` | number |  | — |  |
| `BarDayOfWeek` | `DayOfWeek[#Shift#]` | number |  | — |  |
| `BarHour` | `Hour[#Shift#]` | number |  | — |  |
| `BarMinute` | `Minute[#Shift#]` | number |  | — |  |
| `BarMonth` | `Month[#Shift#]` | number |  | — |  |
| `BarTime` | `Time[#Shift#]` | number |  | — |  |
| `BarWeekOfMonth` | `WeekOfMonth[#Shift#]` | number |  | — |  |
| `CurrentBar` | `CurrentBar` | number |  | — |  |
| `FixedPips` | `FixedPips(#Value# pips)` | pricerange |  | #Value# |  |

## config / priceRange  (9)

| key | display | returnType | mid | bindable | flags |
|---|---|---|---|---|---|
| `ATR` | `ATR(@Chart@#Period#)[#Shift#]` | pricerange |  | #Period# |  |
| `BBRange` | `BB Range(@Chart@#Period#, #Deviation#)[#Shift#]` | pricerange |  | #Period#, #Deviation# |  |
| `BBWidthRatio` | `BB WR(@Chart@#Period#, #Deviation#)[#Shift#]` | pricerange |  | #Period#, #Deviation# |  |
| `BarRange` | `BarRange(@Chart@)[#Shift#]` | pricerange |  | — |  |
| `BiggestRange` | `BiggestRange(@Chart@#Period#)[#Shift#]` | pricerange |  | #Period# |  |
| `MTATR` | `MTATR(@Chart@#Period#)[#Shift#]` | pricerange |  | #Period# |  |
| `SmallestRange` | `SmallestRange(@Chart@#Period#)[#Shift#]` | pricerange |  | #Period# |  |
| `TrueRange` | `TrueRange[@Chart@#Shift#]` | pricerange |  | — |  |
| `talib_TRANGE` | `TRANGE(@Chart@)[#Shift#]` | pricerange |  | — | ⚠ |

## config / priceValue  (26)

| key | display | returnType | mid | bindable | flags |
|---|---|---|---|---|---|
| `Ask` | `Ask` | price |  | — |  |
| `Bid` | `Bid` | price |  | — |  |
| `Close` | `Close[@Chart@#Shift#]` | price |  | — |  |
| `CloseD` | `CloseD[@Chart@#Shift#]` | price |  | — |  |
| `CloseM` | `CloseM[@Chart@#Shift#]` | price |  | — |  |
| `CloseW` | `CloseW[@Chart@#Shift#]` | price |  | — |  |
| `HeikenAshiClose` | `Heiken Ashi Close[@Chart@#Shift#]` | price |  | — |  |
| `HeikenAshiHigh` | `Heiken Ashi High[@Chart@#Shift#]` | price |  | — |  |
| `HeikenAshiLow` | `Heiken Ashi Low[@Chart@#Shift#]` | price |  | — |  |
| `HeikenAshiOpen` | `Heiken Ashi Open[@Chart@#Shift#]` | price |  | — |  |
| `High` | `High[@Chart@#Shift#]` | price |  | — |  |
| `HighD` | `HighD[@Chart@#Shift#]` | price |  | — |  |
| `HighM` | `HighM[@Chart@#Shift#]` | price |  | — |  |
| `HighW` | `HighW[@Chart@#Shift#]` | price |  | — |  |
| `Low` | `Low[@Chart@#Shift#]` | price |  | — |  |
| `LowD` | `LowD[@Chart@#Shift#]` | price |  | — |  |
| `LowM` | `LowM[@Chart@#Shift#]` | price |  | — |  |
| `LowW` | `LowW[@Chart@#Shift#]` | price |  | — |  |
| `Open` | `Open[@Chart@#Shift#]` | price |  | — |  |
| `OpenD` | `OpenD[@Chart@#Shift#]` | price |  | — |  |
| `OpenM` | `OpenM[@Chart@#Shift#]` | price |  | — |  |
| `OpenW` | `OpenW[@Chart@#Shift#]` | price |  | — |  |
| `SessionClose` | `SessionClose(@Chart@#EndHours#:#EndMinutes#)[#Shift#]` | price |  | — |  |
| `SessionHigh` | `SessionHigh(@Chart@#StartHours#:#StartMinutes#-#EndHours#:#EndMinutes#)[#Shift#]` | price |  | — |  |
| `SessionLow` | `SessionLow(@Chart@#StartHours#:#StartMinutes#-#EndHours#:#EndMinutes#)[#Shift#]` | price |  | — |  |
| `SessionOpen` | `SessionOpen(@Chart@#StartHours#:#StartMinutes#)[#Shift#]` | price |  | — |  |

## registry / indicator  (2)

| key | display | returnType | mid | bindable | flags |
|---|---|---|---|---|---|
| `Adaptive_smoothing` | `Adaptive_smoothing(@Chart@#MaeDevLength#, #Price#)[#Shift#]` | price |  | #MaeDevLength#, #Price# | ✦✎ |
| `Fractals` | `Fractals(@Chart@).#Line#[#Shift#]` | price |  | — | ◆✦✎ |
