"""
Gate (c) de la revisión CEO (/plan-ceo-review, 2026-08-12): compara los precios de
entrenamiento de Qlib contra un export real de la databank de SQX para el mismo
instrumento/rango de fechas -- ANTES de entrenar de verdad (hallazgo #8 de la revisión
"outside voice" de /plan-eng-review: entrenar sobre datos con mismatch de fuente invalida
el modelo sin importar qué tan correcto sea el resto del pipeline).

ESTADO: la función de comparación (compare_price_sources) es real y está auto-probada
con datos sintéticos abajo (self_test()). Ejecutarla contra datos REALES requiere:
  1. Un export de precios real de Qlib para el instrumento objetivo (pendiente: no hay
     instalación de Qlib conectada en este entorno todavía).
  2. Un export de precios real de SQX -- vía Data Manager -> Export, o leyendo el archivo
     de datos real del instrumento en C:\\SQX_144_Full\\user\\data\\ (no se hizo autónomamente
     en esta sesión: requiere confirmar qué instrumento/rango exacto usar, y leer datos
     reales de la instalación protegida es una acción que vale la pena confirmar primero).
Este script queda listo para correr en cuanto ambos exports existan -- no es un placeholder
sin lógica, es la lógica real, sin datos reales todavía para alimentarla.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd


def _normalize_sqx_tick_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    chunk = chunk.copy()
    ts_candidates = [c for c in ["DateTime", "timestamp", "datetime", "date_time", "time", "date"] if c in chunk.columns]
    if not ts_candidates:
        raise ValueError(f"No se encontró una columna de timestamp válida en el chunk. Columnas: {list(chunk.columns[:10])}")
    ts_col = ts_candidates[0]

    if {"Bid", "Ask"}.issubset(chunk.columns):
        chunk["close"] = (pd.to_numeric(chunk["Bid"], errors="coerce") + pd.to_numeric(chunk["Ask"], errors="coerce")) / 2.0
    elif "Close" in chunk.columns:
        chunk["close"] = pd.to_numeric(chunk["Close"], errors="coerce")
    elif "close" in chunk.columns:
        chunk["close"] = pd.to_numeric(chunk["close"], errors="coerce")
    else:
        raise ValueError(f"No se pudo derivar la columna 'close' para el chunk. Columnas: {list(chunk.columns)}")

    chunk[ts_col] = pd.to_datetime(chunk[ts_col], errors="coerce", utc=True)
    chunk = chunk[[ts_col, "close"]].dropna(subset=[ts_col, "close"]).drop_duplicates(subset=[ts_col])
    chunk = chunk.rename(columns={ts_col: "timestamp"})
    chunk = chunk.set_index("timestamp")
    return chunk


def _resample_sqx_to_hourly(csv_path: str | Path, chunksize: int = 1_000_000) -> pd.Series:
    path = Path(csv_path)
    frames = []
    for chunk in pd.read_csv(path, chunksize=chunksize, low_memory=False):
        frames.append(_normalize_sqx_tick_chunk(chunk))
    if not frames:
        raise ValueError(f"El CSV está vacío: {path}")

    merged = pd.concat(frames).sort_index()
    hourly = merged.resample("1h").agg({"close": "last"})
    return hourly["close"].dropna().rename("close")


def _load_close_series(csv_path: str | Path) -> pd.Series:
    if Path(csv_path).suffix.lower() == ".csv":
        return _resample_sqx_to_hourly(csv_path)
    raise ValueError(f"Formato no soportado para el CSV de SQX: {csv_path}")


def compare_price_sources(qlib_ohlcv: pd.DataFrame, sqx_export_csv_path: str,
                           tolerance: float = 1e-6) -> pd.DataFrame:
    """Retorna las filas donde los precios NO coinciden dentro de tolerance.
    DataFrame vacío = paridad confirmada.

    qlib_ohlcv: DataFrame indexado por timestamp, con columna 'close' (al menos).
    sqx_export_csv_path: CSV con columnas 'timestamp' (parseable) y 'close', exportado
    desde SQX (Data Manager -> Export, o lectura directa del archivo de datos real)."""
    sqx_ohlcv = _load_close_series(sqx_export_csv_path).to_frame()
    qlib_ohlcv = qlib_ohlcv.copy()

    if "timestamp" in qlib_ohlcv.columns:
        qlib_ohlcv = qlib_ohlcv.set_index(pd.to_datetime(qlib_ohlcv["timestamp"], utc=True))
    elif "datetime" in qlib_ohlcv.columns:
        qlib_ohlcv = qlib_ohlcv.set_index(pd.to_datetime(qlib_ohlcv["datetime"], utc=True))
    elif "DateTime" in qlib_ohlcv.columns:
        qlib_ohlcv = qlib_ohlcv.set_index(pd.to_datetime(qlib_ohlcv["DateTime"], utc=True))

    qlib_ohlcv = qlib_ohlcv[[c for c in ['close', 'Close'] if c in qlib_ohlcv.columns][:1]]
    if 'close' not in qlib_ohlcv.columns and 'Close' in qlib_ohlcv.columns:
        qlib_ohlcv = qlib_ohlcv.rename(columns={'Close': 'close'})

    qlib_ohlcv.index = pd.to_datetime(qlib_ohlcv.index, utc=True)
    sqx_ohlcv.index = pd.to_datetime(sqx_ohlcv.index, utc=True)
    merged = qlib_ohlcv.join(sqx_ohlcv, lsuffix="_qlib", rsuffix="_sqx", how="outer")

    # Filas presentes en un lado y no en el otro son, por definición, un mismatch --
    # ausencia total no cuenta como "dentro de tolerance", debe reportarse.
    missing_either_side = merged[merged["close_qlib"].isna() | merged["close_sqx"].isna()]

    both_present = merged.dropna(subset=["close_qlib", "close_sqx"])
    value_mismatches = both_present[
        (both_present["close_qlib"] - both_present["close_sqx"]).abs() > tolerance
    ]

    return pd.concat([missing_either_side, value_mismatches]).sort_index()


def self_test() -> None:
    """Prueba compare_price_sources con datos sintéticos -- NO valida datos reales de
    SQX/Qlib (esos no existen todavía en este entorno), valida que la LÓGICA de
    comparación detecta correctamente casos de match, mismatch de valor, y filas
    faltantes de un solo lado."""
    print("=== Self-test de compare_price_sources (datos sinteticos) ===")

    dates = pd.date_range("2024-01-01", periods=5, freq="D")

    # Caso 1: paridad exacta -> debe dar DataFrame vacio
    qlib_df = pd.DataFrame({"close": [100.0, 101.0, 102.0, 103.0, 104.0]}, index=dates)
    sqx_df = qlib_df.rename(columns={"close": "close"}).copy()
    sqx_csv = Path("_selftest_sqx_match.csv")
    sqx_df.reset_index().rename(columns={"index": "timestamp"}).to_csv(sqx_csv, index=False)
    result = compare_price_sources(qlib_df, str(sqx_csv))
    sqx_csv.unlink()
    assert result.empty, f"FALLO: se esperaba paridad exacta, se encontraron {len(result)} mismatches"
    print("OK: paridad exacta detectada correctamente (0 mismatches)")

    # Caso 2: un valor desviado mas alla de la tolerancia -> debe detectarlo
    sqx_df2 = qlib_df.copy()
    sqx_df2.iloc[2, sqx_df2.columns.get_loc("close")] = 102.0 + 0.01  # fuera de 1e-6
    sqx_csv2 = Path("_selftest_sqx_mismatch.csv")
    sqx_df2.reset_index().rename(columns={"index": "timestamp"}).to_csv(sqx_csv2, index=False)
    result2 = compare_price_sources(qlib_df, str(sqx_csv2))
    sqx_csv2.unlink()
    assert len(result2) == 1, f"FALLO: se esperaba 1 mismatch, se encontraron {len(result2)}"
    print(f"OK: mismatch de valor detectado correctamente (1 fila, fecha {result2.index[0].date()})")

    # Caso 3: SQX le falta una fecha que Qlib si tiene -> debe reportarse, no ignorarse
    sqx_df3 = qlib_df.drop(qlib_df.index[1]).copy()
    sqx_csv3 = Path("_selftest_sqx_missing.csv")
    sqx_df3.reset_index().rename(columns={"index": "timestamp"}).to_csv(sqx_csv3, index=False)
    result3 = compare_price_sources(qlib_df, str(sqx_csv3))
    sqx_csv3.unlink()
    assert len(result3) == 1, f"FALLO: se esperaba 1 fila faltante detectada, se encontraron {len(result3)}"
    print(f"OK: fecha faltante en un solo lado detectada correctamente (fecha {result3.index[0].date()})")

    print("\n=== Self-test COMPLETO: los 3 casos pasaron ===")
    print("NOTA: esto valida la logica de comparacion, no datos reales de SQX/Qlib --")
    print("      correr con --qlib-csv y --sqx-csv reales cuando existan esos exports.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                         help="Corre la auto-prueba con datos sinteticos (sin datos reales)")
    parser.add_argument("--qlib-csv", help="CSV con precios de entrenamiento reales de Qlib")
    parser.add_argument("--sqx-csv", help="CSV exportado desde la databank real de SQX")
    parser.add_argument("--tolerance", type=float, default=1e-6)
    args = parser.parse_args()

    if args.self_test or not (args.qlib_csv and args.sqx_csv):
        self_test()
        if not (args.qlib_csv and args.sqx_csv):
            print("\nSin --qlib-csv/--sqx-csv reales todavia -- self-test corrido por defecto.")
        return

    qlib_df = pd.read_csv(args.qlib_csv, low_memory=False)
    if "timestamp" in qlib_df.columns:
        qlib_df = qlib_df.set_index(pd.to_datetime(qlib_df["timestamp"], utc=True))
    elif "datetime" in qlib_df.columns:
        qlib_df = qlib_df.set_index(pd.to_datetime(qlib_df["datetime"], utc=True))
    elif "DateTime" in qlib_df.columns:
        qlib_df = qlib_df.set_index(pd.to_datetime(qlib_df["DateTime"], utc=True))
    mismatches = compare_price_sources(qlib_df, args.sqx_csv, tolerance=args.tolerance)
    if mismatches.empty:
        print("PARIDAD CONFIRMADA: 0 discrepancias entre Qlib y la databank real de SQX.")
    else:
        print(f"PARIDAD FALLIDA: {len(mismatches)} discrepancias encontradas:")
        print(mismatches)
        sys.exit(1)


if __name__ == "__main__":
    main()
