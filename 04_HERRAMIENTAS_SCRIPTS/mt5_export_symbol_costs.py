import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import MetaTrader5 as mt5


def export_symbol(symbol: str) -> dict:
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"Symbol not found in MT5: {symbol}")

    tick_value = float(info.trade_tick_value)
    tick_size = float(info.trade_tick_size)

    return {
        "symbol": symbol,
        "visible": bool(info.visible),
        "path": getattr(info, "path", ""),
        "description": getattr(info, "description", ""),
        "currency_base": getattr(info, "currency_base", ""),
        "currency_profit": getattr(info, "currency_profit", ""),
        "currency_margin": getattr(info, "currency_margin", ""),
        "digits": int(info.digits),
        "point": float(info.point),
        "trade_tick_size": tick_size,
        "trade_tick_value": tick_value,
        "point_value": (tick_value / tick_size) if tick_size else None,
        "spread": float(info.spread),
        "swap_long": float(info.swap_long),
        "swap_short": float(info.swap_short),
        "swap_mode": int(info.swap_mode),
        "trade_contract_size": float(info.trade_contract_size),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export MT5 live instrument costs (tick size/value, spread, swap, point value)."
    )
    parser.add_argument("symbols", nargs="+", help="One or more MT5 symbol names, e.g. NDXm")
    parser.add_argument("--outdir", default=None, help="Output directory for JSON/CSV files")
    args = parser.parse_args()

    if not mt5.initialize():
        raise RuntimeError(f"mt5.initialize() failed: {mt5.last_error()}")

    try:
        account = mt5.account_info()
        if account is None:
            raise RuntimeError(f"mt5.account_info() returned None: {mt5.last_error()}")

        rows = [export_symbol(sym) for sym in args.symbols]
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "account": {
                "login": account.login,
                "server": account.server,
                "currency": account.currency,
                "balance": account.balance,
                "equity": account.equity,
            },
            "symbols": rows,
        }

        outdir = Path(args.outdir) if args.outdir else Path("outputs") / ("mt5_costs_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        outdir.mkdir(parents=True, exist_ok=True)

        json_path = outdir / "mt5_symbol_costs.json"
        csv_path = outdir / "mt5_symbol_costs.csv"
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
            writer.writeheader()
            writer.writerows(rows)

        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"Wrote: {json_path}")
        print(f"Wrote: {csv_path}")
        return 0
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
