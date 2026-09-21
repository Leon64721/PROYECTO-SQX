# -*- coding: utf-8 -*-
"""
Extrae costos live de OANDA (MT5, cuenta 7044848, solo lectura) para los 9 pares JPY
disponibles y genera:
  - "Updated Instrument information.xml" en el formato oficial de SQX
    (custom_indicators/BrokerProfileInstrumentsSessionsScripts/Update_SQX_Instruments_information.mq5),
    listo para importar en Data Manager -> Broker profiles -> Import.
  - REPORTE_COSTOS_JPY.md / .csv / .json con el detalle y las formulas usadas.

Formulas (ya validadas en esta misma sesion contra Data Manager real, ver
user/PropFirm_Management/19_ndxm_custom_projects_multibroker_costos.md):
  - decimals        = SYMBOL_DIGITS
  - tickStep (raw)  = SYMBOL_TRADE_TICK_SIZE (fallback SYMBOL_POINT)
  - ticksPerPip     = 10 si decimals es 3 o 5 (broker de pip fraccionario), 1 si es 2 o 4
  - pipSize         = tickStep * ticksPerPip           (campo "Pip/Tick size" en SQX)
  - pointValue $    = trade_tick_value / trade_tick_size (campo "Point value in $")
  - spread (pips)   = (ask-bid) / pipSize               (campo "Default spread * pips")
  - swap_mode=INTEREST_CURRENT (confirmado para esta cuenta/todos los JPY) ->
        swap_usd_dia = (swap_%_anual/100) * precio_mid * pointValueUSD / 360
    (aproximacion documentada, no el monto exacto cobrado por el broker; para el
    valor exacto habria que ver el historial real de swaps de la cuenta)
  - dataType        = 3 (Forex). Codigos SQX: 1=Stock, 2=Futures, 3=Forex, 4=CFD,
    5=ETF, 6=Index, 7=Crypto (bug corregido 2026-09-16: se escribia "1"/Stock por error,
    causaba que el Data Manager clasificara los 9 pares como "Stock" en vez de "Forex").
"""
import MetaTrader5 as mt5
import json
import datetime
import os

SYMBOLS = ["AUDJPY", "CADJPY", "CHFJPY", "EURJPY", "GBPJPY.sml",
           "NZDJPY", "SGDJPY", "USDJPY.sml", "ZARJPY"]

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
XML_DIR = os.path.join(OUT_DIR, "StrategyQuantX")
os.makedirs(XML_DIR, exist_ok=True)


def strip_suffix(name: str) -> str:
    """Nombre de instrumento tal como existe en Data Manager (sin sufijo de broker)."""
    return name.split(".")[0]


def xml_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def build():
    ok = mt5.initialize()
    if not ok:
        raise RuntimeError(f"mt5.initialize() fallo: {mt5.last_error()}")

    acc = mt5.account_info()
    broker_name = acc.company if acc else "OANDA Global Markets Limited"

    for s in SYMBOLS:
        mt5.symbol_select(s, True)

    rows = []
    for sym in SYMBOLS:
        info = mt5.symbol_info(sym)
        if info is None:
            print("WARNING: sin symbol_info para", sym)
            continue

        digits = info.digits
        tick_step = info.trade_tick_size if info.trade_tick_size > 0 else info.point
        ticks_per_pip = 10 if digits in (3, 5) else 1
        pip_size = tick_step * ticks_per_pip

        tick_value = info.trade_tick_value
        point_value_usd = (tick_value / tick_step) if tick_step else 0.0

        bid, ask = info.bid, info.ask
        mid = (bid + ask) / 2 if (bid and ask) else 0.0
        spread_price = (ask - bid) if (bid and ask) else info.spread * info.point
        spread_pips = spread_price / pip_size if pip_size else 0.0

        swap_mode = info.swap_mode  # 5 = SYMBOL_SWAP_MODE_INTEREST_CURRENT (confirmado)
        swap_long_pct = info.swap_long
        swap_short_pct = info.swap_short
        if mid:
            swap_long_usd = (swap_long_pct / 100) * mid * point_value_usd / 360
            swap_short_usd = (swap_short_pct / 100) * mid * point_value_usd / 360
        else:
            swap_long_usd = swap_short_usd = 0.0

        instrument_name = strip_suffix(sym)

        rows.append(dict(
            mt5_symbol=sym,
            instrument=instrument_name,
            description=info.description,
            digits=digits,
            tick_step=tick_step,
            pip_size=pip_size,
            point_value_usd=round(point_value_usd, 6),
            contract_size=info.trade_contract_size,
            bid=bid, ask=ask, mid=mid,
            spread_price_units=round(spread_price, 6),
            spread_pips=round(spread_pips, 2),
            swap_mode=swap_mode,
            swap_long_pct_annual=swap_long_pct,
            swap_short_pct_annual=swap_short_pct,
            swap_long_usd_per_lot_day=round(swap_long_usd, 2),
            swap_short_usd_per_lot_day=round(swap_short_usd, 2),
            volume_step=info.volume_step,
            min_distance_points=info.trade_stops_level,
            min_distance_price=round(info.trade_stops_level * info.point, 6),
            path=info.path,
        ))

    mt5.shutdown()

    # ---- 1) XML formato oficial SQX (Data Manager -> Broker profiles -> Import) ----
    xml_lines = ["<Instruments>"]
    for r in rows:
        commissions_inner = (
            '&lt;Method type=&quot;None&quot; use=&quot;true&quot;&gt;'
            '&lt;Params/&gt;&lt;/Method&gt;'
        )
        swap_inner = (
            f'&lt;Swap use=&quot;true&quot; type=&quot;money&quot; '
            f'long=&quot;{r["swap_long_usd_per_lot_day"]:.2f}&quot; '
            f'short=&quot;{r["swap_short_usd_per_lot_day"]:.2f}&quot; '
            f'tripleSwapOn=&quot;WEDNESDAY&quot;/&gt;'
        )
        line = (
            f'  <InstrumentInfo instrument="{r["instrument"]}" '
            f'description="{xml_escape(r["description"])}" '
            f'tickSize="{r["pip_size"]:.{r["digits"]}f}" '
            f'tickStep="{r["tick_step"]:.{r["digits"]}f}" '
            f'tickValueInMoney="{r["point_value_usd"]:.6f}" '
            f'defaultSpread="{r["spread_pips"]:.2f}" '
            f'defaultSlippage="0" '
            f'decimals="{r["digits"]}" '
            f'commissions="{commissions_inner}" '
            f'pointValue="{r["point_value_usd"]:.6f}" '
            f'dataType="3" '
            f'recognizedFromOrders="false" '
            f'alias="{r["instrument"]}" '
            f'exchange="" country="" sector="" '
            f'swap="{swap_inner}" '
            f'orderSizeMultiplier="1.0" orderSizeStep="{r["volume_step"]}" '
            f'minDistance="{r["min_distance_price"]:.{r["digits"]}f}" />'
        )
        xml_lines.append(line)
    xml_lines.append("</Instruments>")

    xml_path = os.path.join(XML_DIR, "Updated Instrument information.xml")
    with open(xml_path, "w", encoding="ansi", errors="replace") as f:
        f.write("\n".join(xml_lines))

    # ---- 2) JSON / CSV / Markdown de respaldo ----
    generated = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(os.path.join(OUT_DIR, "COSTOS_OANDA_JPY.json"), "w", encoding="utf-8") as f:
        json.dump(dict(broker=broker_name, generated_utc=generated, symbols=rows), f,
                   indent=2, default=str)

    import csv
    with open(os.path.join(OUT_DIR, "COSTOS_OANDA_JPY.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    md = [f"# Costos live OANDA — pares JPY ({generated[:10]})", "",
          f"Fuente: MT5 `{broker_name}`, cuenta 7044848, solo lectura (`symbol_info`).", "",
          "| Instrumento (Data Manager) | Símbolo MT5 | Pip/Tick size | Pip/Tick step | "
          "Point value ($) | Spread (pips) | Swap Long ($/lote/día) | Swap Short ($/lote/día) | "
          "Order size step | Min distance |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(
            f"| {r['instrument']} | {r['mt5_symbol']} | {r['pip_size']:.{r['digits']}f} | "
            f"{r['tick_step']:.{r['digits']}f} | {r['point_value_usd']:.2f} | "
            f"{r['spread_pips']:.2f} | {r['swap_long_usd_per_lot_day']:+.2f} | "
            f"{r['swap_short_usd_per_lot_day']:+.2f} | {r['volume_step']} | "
            f"{r['min_distance_price']:.{r['digits']}f} |"
        )
    md.append("")
    md.append("## Notas")
    md.append("- `swap_mode` de todos estos símbolos en esta cuenta es "
              "`INTEREST_CURRENT` (tasa % anual, no puntos ni $ directos) — el swap en "
              "$/lote/día es una **aproximación** con "
              "`(swap_%/100) * precio_mid * pointValueUSD / 360`, no el monto exacto que "
              "cobra el broker cada noche (ver historial real de swaps de la cuenta para el "
              "valor exacto si se necesita precisión absoluta).")
    md.append("- Comisión: se asumió `None` (cuenta Standard con spread ya cargado, sin "
              "comisión explícita por lote) — verificar el tipo de cuenta real (Standard vs "
              "Raw/ECN) antes de mining/backtests que dependan mucho de este costo.")
    md.append("- El spread reportado es una foto **live** al momento de la consulta, no un "
              "promedio histórico — puede variar según sesión/liquidez.")
    md.append(f"- Archivo listo para importar: `StrategyQuantX/Updated Instrument information.xml`.")
    with open(os.path.join(OUT_DIR, "REPORTE_COSTOS_JPY.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"OK - {len(rows)} instrumentos procesados.")
    print("XML:", xml_path)
    return rows


if __name__ == "__main__":
    build()
