# Costos live OANDA — pares JPY (2026-09-16)

Fuente: MT5 `OANDA Global Markets Limited`, cuenta 7044848, solo lectura (`symbol_info`).

| Instrumento (Data Manager) | Símbolo MT5 | Pip/Tick size | Pip/Tick step | Point value ($) | Spread (pips) | Swap Long ($/lote/día) | Swap Short ($/lote/día) | Order size step | Min distance |
|---|---|---|---|---|---|---|---|---|---|
| AUDJPY | AUDJPY | 0.010 | 0.001 | 640.62 | 1.50 | +28.47 | -52.69 | 0.01 | 0.005 |
| CADJPY | CADJPY | 0.010 | 0.001 | 640.62 | 1.40 | +2.86 | -27.64 | 0.01 | 0.005 |
| CHFJPY | CHFJPY | 0.010 | 0.001 | 640.62 | 3.00 | -43.47 | +1.82 | 0.01 | 0.005 |
| EURJPY | EURJPY | 0.010 | 0.001 | 640.62 | 1.80 | +11.09 | -49.72 | 0.01 | 0.005 |
| GBPJPY | GBPJPY.sml | 0.010 | 0.001 | 640.62 | 1.10 | +40.38 | -86.12 | 0.01 | 0.005 |
| NZDJPY | NZDJPY | 0.010 | 0.001 | 640.62 | 2.30 | +8.57 | -28.37 | 0.01 | 0.005 |
| SGDJPY | SGDJPY | 0.010 | 0.001 | 640.62 | 2.10 | -6.00 | -21.65 | 0.01 | 0.005 |
| USDJPY | USDJPY.sml | 0.010 | 0.001 | 640.62 | 1.20 | +33.50 | -67.16 | 0.01 | 0.005 |
| ZARJPY | ZARJPY | 0.010 | 0.001 | 640.62 | 1.20 | +3.29 | -8.94 | 0.01 | 0.000 |

## Notas
- `swap_mode` de todos estos símbolos en esta cuenta es `INTEREST_CURRENT` (tasa % anual, no puntos ni $ directos) — el swap en $/lote/día es una **aproximación** con `(swap_%/100) * precio_mid * pointValueUSD / 360`, no el monto exacto que cobra el broker cada noche (ver historial real de swaps de la cuenta para el valor exacto si se necesita precisión absoluta).
- Comisión: se asumió `None` (cuenta Standard con spread ya cargado, sin comisión explícita por lote) — verificar el tipo de cuenta real (Standard vs Raw/ECN) antes de mining/backtests que dependan mucho de este costo.
- El spread reportado es una foto **live** al momento de la consulta, no un promedio histórico — puede variar según sesión/liquidez.
- Archivo listo para importar: `StrategyQuantX/Updated Instrument information.xml`.