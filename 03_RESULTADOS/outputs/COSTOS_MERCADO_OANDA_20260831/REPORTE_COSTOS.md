# Costos de mercado — snapshot live OANDA (2026-08-31)

Fuente: consulta directa en vivo vía API Python `MetaTrader5` contra la terminal **OANDA Global MetaTrader 5**, cuenta real `7044848`, servidor `OANDA_Global-Live-1`, divisa de cuenta USD. Solo lectura (`symbol_info`, `account_info`) — no se ejecutó ninguna orden.

Archivos completos: `COSTOS_OANDA_snapshot.json` / `.csv` (25 instrumentos, todos los campos crudos de MT5 + valores derivados). `oanda_symbols_raw.json` tiene el volcado sin procesar de `symbol_info()` por si se necesita cualquier campo adicional.

## Metodología

- **Point value en $** = `trade_tick_value / trade_tick_size` (valor en USD de un movimiento de 1.0 unidad de precio, por lote estándar). MT5 ya entrega `trade_tick_value` convertido a la divisa de la cuenta (USD), sin importar la divisa de cotización del símbolo.
- **Spread** = snapshot del spread live en el momento de la consulta (en unidades de precio), no un promedio histórico. Puede variar según sesión/liquidez — considerarlo un punto de partida, no un valor fijo garantizado.
- **Swap** = todos los símbolos de esta cuenta usan `swap_mode=INTEREST_CURRENT` (tasa anual %, no puntos ni $ directos). Se estimó el swap diario en $/lote con: `(swap_%_anual/100) × precio_actual × pointValueUSD / 360`. Es una **aproximación razonable, no el monto exacto que cobra el broker** — para el valor exacto, confirmar con el historial de swaps reales de la cuenta o el panel "Especificación" (clic derecho símbolo → Especificación) en MT5.
- Instrumentos con "sin cotización" no tenían precio live en el momento de la consulta (mercado cerrado o símbolo sin suscripción activa) — no se pudo estimar el swap en $ para esos.

## Forex

| Símbolo | Descripción | Point value ($/lote) | Spread live | Swap Long ($/lote/día) | Swap Short ($/lote/día) |
|---|---|---|---|---|---|
| EURUSD.sml | Euro vs US Dollar | 100,000 | 0.00009 (0.9 pips) | -7.94 | +1.42 |
| GBPUSD.sml | GBP vs USD | 100,000 | 0.00011 (1.1 pips) | 0.00 | 0.00 |
| USDJPY.sml | USD vs JPY | 625.89 | 0.011 (1.1 pips) | +4.97 | -10.61 |
| USDCHF | USD vs CHF | 123,708.79 | 0.00012 (1.2 pips) | +7.89 | -13.92 |
| AUDUSD.sml | AUD vs USD | 100,000 | 0.00009 (0.9 pips) | -1.02 | -3.18 |
| USDCAD | USD vs CAD | 72,162.57 | 0.00015 (1.5 pips) | +1.61 | -7.47 |
| NZDUSD | NZD vs USD | 100,000 | 0.00016 (1.6 pips) | -3.45 | -0.12 |
| EURGBP.sml | EUR vs GBP | 135,473 | 0.0001 (1 pip) | 0.00 | 0.00 |
| EURJPY | EUR vs JPY | 625.89 | sin cotización | n/d | n/d |
| GBPJPY.sml | GBP vs JPY | 625.89 | 0.011 (1.1 pips) | 0.00 | 0.00 |

## Índices / Futuros

| Símbolo | Descripción | Point value ($/lote) | Spread live (puntos) | Swap Long ($/lote/día) | Swap Short ($/lote/día) |
|---|---|---|---|---|---|
| US100 | US Tech 100 (Nasdaq) | 1.00 | 2.2 | **-15.02** | **+2.79** |
| US500 | US SPX 500 | 1.00 | 0.6 | -3.93 | +0.73 |
| US30 | Wall Street 30 | 1.00 | 4.0 | -27.22 | +5.05 |
| DE40 | Germany 40 | 1.16 | 4.4 | -11.89 | -0.79 |
| UK100 | UK 100 | 1.35 | 2.3 | -7.61 | +1.50 |
| JP225 | Japan 225 | 0.006 | sin cotización | n/d | n/d |
| HK50 | Hong Kong 50 | 0.013 | sin cotización | n/d | n/d |
| CHINAH | China H Shares | 0.013 | sin cotización | n/d | n/d |

**US100 es el análogo directo de NDXm** en esta cuenta — estos son los valores que se inyectaron en los 4 `.cfx` de `outputs/NDXm_OANDA_20260831/`.

## Metales

| Símbolo | Descripción | Point value ($/lote) | Spread live | Swap Long/Short ($/lote/día) |
|---|---|---|---|---|
| XAUUSD.sml | Oro | 100.00 | 0.34 | 0.00 / 0.00 |
| XAGUSD | Plata | 5,000.00 | 0.032 | 0.00 / 0.00 |

## Energía

| Símbolo | Descripción | Point value ($/lote) | Spread live | Swap Long ($/lote/día) | Swap Short ($/lote/día) |
|---|---|---|---|---|---|
| USOIL.sml | WTI Crude | 1,000.00 | 0.03 | +22.60 | -34.63 |
| UKOIL.sml | Brent Crude | 1,000.00 | 0.04 | +69.38 | -82.27 |
| NATGAS | Gas Natural | 10,000.00 | sin cotización | n/d | n/d |

## Cripto

| Símbolo | Descripción | Point value ($/lote) | Swap Long/Short (%anual) |
|---|---|---|---|
| BTCUSD | Bitcoin | 1.00 | -85.92% / -64.08% (sin cotización live para $/día) |
| ETHUSD | Ethereum | 1.00 | -85.92% / -64.08% (sin cotización live para $/día) |

## Cómo reutilizar esto

El script que generó este snapshot está pensado para reutilizarse: apuntando `mt5.initialize(path=...)` a **cualquier terminal MT5 instalada y logueada** (Tickmill, Darwinex, etc.) en vez de la de OANDA, se puede repetir exactamente este mismo proceso para obtener los costos reales de otro broker, sin script MQL5 ni exportación/importación manual — solo con la terminal abierta y logueada. Avísame cuando tengas Tickmill (u otro broker) corriendo y repito la consulta.
