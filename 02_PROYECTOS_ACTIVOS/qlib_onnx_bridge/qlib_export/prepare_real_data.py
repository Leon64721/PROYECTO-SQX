"""Preparación de una serie de precios reales de SQX para Qlib.

Objetivo:
- tomar un export real de SQX (o un CSV de la databank) con OHLCV,
- normalizar timestamps, columnas y resolución,
- escribir un dataset Qlib-compatible listo para entrenamiento o validación.

Uso típico:
    python qlib_export/prepare_real_data.py --input "C:/SQX_144_Full/.../NDXm.csv" \
        --symbol NDXm_TICK_UTCPlus02 --freq H1 --output qlib_export/output/ndxm_real.csv

Si no hay export real todavía, la misma herramienta puede ejecutarse en modo
--self-test con datos sintéticos para verificar la lógica de normalización.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Sequence

import pandas as pd

DEFAULT_OUTPUT = Path(__file__).resolve().parent / "output" / "ndxm_real_ohlcv.csv"


def _candidate_timestamp_columns() -> List[str]:
    return [
        "DateTime", "timestamp", "datetime", "date_time", "time", "date",
        "open_time", "close_time",
    ]


def _candidate_ohlc_columns() -> List[str]:
    return ["open", "high", "low", "close", "volume"]


def _normalize_numeric_series(series: pd.Series, column_name: str) -> pd.Series:
    out = pd.to_numeric(series, errors="coerce")
    if out.isna().all():
        raise ValueError(f"La columna '{column_name}' no contiene valores numéricos válidos.")
    return out


def _combine_date_and_time(frame: pd.DataFrame) -> pd.DataFrame:
    if {"date", "time"}.issubset(frame.columns):
        dt = pd.to_datetime(frame["date"].astype(str) + " " + frame["time"].astype(str), errors="coerce")
        frame = frame.copy()
        frame["timestamp"] = dt
    return frame


def _resolve_timestamp_column(frame: pd.DataFrame) -> str:
    ts_candidates = [c for c in _candidate_timestamp_columns() if c in frame.columns]
    if not ts_candidates:
        raise ValueError(
            "No se encontró una columna de timestamp válida. Columnas disponibles: "
            + ", ".join(frame.columns[:25])
        )
    return ts_candidates[0]


def _ensure_ohlcv_columns(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()

    if "Volume" in frame.columns and "volume" not in frame.columns:
        frame["volume"] = frame["Volume"]
    if "Close" in frame.columns and "close" not in frame.columns:
        frame["close"] = frame["Close"]
    if {"Bid", "Ask"}.issubset(frame.columns) and "close" not in frame.columns:
        if "Bid" in frame.columns and "Ask" in frame.columns:
            frame["close"] = (pd.to_numeric(frame["Bid"], errors="coerce") + pd.to_numeric(frame["Ask"], errors="coerce")) / 2.0

    if "close" not in frame.columns and "Close" in frame.columns:
        frame["close"] = frame["Close"]

    if not {"open", "high", "low", "close"}.issubset(frame.columns):
        if "close" not in frame.columns:
            raise ValueError("Se requiere al menos la columna 'close' (o Bid/Ask) para preparar un dataset Qlib.")
        for col in ["open", "high", "low"]:
            if col not in frame.columns:
                frame[col] = frame["close"]

    for col in ["open", "high", "low", "close"]:
        if col in frame.columns:
            frame[col] = _normalize_numeric_series(frame[col], col)

    if "volume" not in frame.columns:
        frame["volume"] = 0.0
    frame["volume"] = _normalize_numeric_series(frame["volume"], "volume")

    return frame


def _prepare_frame_from_csv(df: pd.DataFrame) -> pd.DataFrame:
    df = _combine_date_and_time(df)
    ts_col = _resolve_timestamp_column(df)
    df = df.rename(columns={ts_col: "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
    df = _ensure_ohlcv_columns(df)
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df = df.drop_duplicates(subset=["timestamp"]).set_index("timestamp")
    return df


def read_sqx_export(csv_path: str | Path) -> pd.DataFrame:
    """Lee un CSV exportado desde SQX o una databank legacy y devuelve un DataFrame listo."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de exportación de SQX: {path}")

    if path.stat().st_size > 256 * 1024 * 1024:
        chunks = []
        for chunk in pd.read_csv(path, chunksize=250_000, low_memory=False):
            chunks.append(_prepare_frame_from_csv(chunk))
        if not chunks:
            raise ValueError(f"El CSV está vacío: {path}")
        return pd.concat(chunks).sort_index()

    df = pd.read_csv(path, low_memory=False)
    return _prepare_frame_from_csv(df)


def _resample_to_freq(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    if df.empty:
        return df
    normalized_freq = freq.strip().lower()
    if normalized_freq in {"h1", "1h", "hourly", "60min", "1h"}:
        normalized_freq = "1h"
    elif normalized_freq in {"m15", "15min", "15t"}:
        normalized_freq = "15min"
    elif normalized_freq in {"m5", "5min", "5t"}:
        normalized_freq = "5min"

    out = df.resample(normalized_freq).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    })
    return out.dropna(subset=["close"]).sort_index()


def prepare_real_data(
    input_csv: str | Path,
    output_csv: str | Path = DEFAULT_OUTPUT,
    symbol: str | None = None,
    freq: str = "H1",
    timezone: str | None = None,
) -> pd.DataFrame:
    """Prepara un CSV Qlib-friendly a partir de un export real de SQX.

    La salida mantiene el índice temporal como timestamp UTC y escribe únicamente las
    columnas de soporte necesarias para Qlib: open/high/low/close/volume.
    """
    df = read_sqx_export(input_csv)
    df = _resample_to_freq(df, freq)

    if timezone:
        tz = str(timezone).strip()
        if tz.upper() == "UTC":
            df.index = df.index.tz_convert("UTC")
        else:
            # Acepta timezone strings de pandas como 'UTC', 'Europe/Berlin', etc.
            df.index = df.index.tz_localize(tz)
            df.index = df.index.tz_convert("UTC")

    if symbol:
        df = df.assign(symbol=str(symbol))

    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Export Qlib-friendly: timestamp + OHLCV, sin multiplicar columnas extra.
    if "symbol" in df.columns:
        out_df = df.reset_index().rename(columns={"timestamp": "datetime"})
        out_df = out_df[["datetime", "symbol", "open", "high", "low", "close", "volume"]]
    else:
        out_df = df.reset_index().rename(columns={"timestamp": "datetime"})
        out_df = out_df[["datetime", "open", "high", "low", "close", "volume"]]

    out_df.to_csv(output_path, index=False)
    return out_df


def _self_test() -> None:
    print("=== Self-test prepare_real_data ===")
    src = Path(__file__).resolve().parent / "output" / "_selftest_sqx_export.csv"
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=4, freq="D"),
            "time": ["00:00:00", "00:00:00", "00:00:00", "00:00:00"],
            "open": [100.0, 101.0, 102.0, 103.0],
            "high": [101.0, 102.0, 103.0, 104.0],
            "low": [99.0, 100.0, 101.0, 102.0],
            "close": [100.5, 101.5, 102.5, 103.5],
            "volume": [10, 11, 12, 13],
        }
    )
    df.to_csv(src, index=False)

    out_path = Path(__file__).resolve().parent / "output" / "_selftest_qlib_ready.csv"
    normalized = prepare_real_data(src, output_csv=out_path, symbol="NDXm_TICK_UTCPlus02", freq="H1")
    assert "datetime" in normalized.columns, normalized.columns
    assert normalized["close"].notna().all(), "Hay NaN en close tras normalización"
    assert normalized["datetime"].nunique() == len(normalized), "Hay timestamps duplicados"
    print("OK: preparación de datos real normalizada correctamente")
    for path in (src, out_path):
        if path.exists():
            path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", "--input-csv", dest="input", help="CSV de exportación real de SQX o databank")
    parser.add_argument("--output", "--output-csv", dest="output", default=str(DEFAULT_OUTPUT), help="Archivo CSV final Qlib-friendly")
    parser.add_argument("--symbol", default=None, help="Símbolo de mercado, ej. NDXm_TICK_UTCPlus02")
    parser.add_argument("--freq", default="H1", help="Resolución de datos: H1, M15, etc.")
    parser.add_argument("--timezone", default=None, help="Timezone de la serie antes de convertir a UTC")
    parser.add_argument("--self-test", action="store_true", help="Ejecuta prueba local sintética")
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        return

    if not args.input:
        raise SystemExit("Debes pasar --input o --self-test. Si aún no hay export real, solicita el CSV de SQX antes de continuar.")

    prepare_real_data(
        input_csv=args.input,
        output_csv=args.output,
        symbol=args.symbol,
        freq=args.freq,
        timezone=args.timezone,
    )
    print(f"Dataset Qlib listo: {args.output}")


if __name__ == "__main__":
    main()
