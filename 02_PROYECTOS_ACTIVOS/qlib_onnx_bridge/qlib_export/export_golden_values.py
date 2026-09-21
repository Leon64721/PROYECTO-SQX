"""
Gate (a)/(d) de la revisión CEO (/plan-ceo-review): corre el modelo .onnx ya
entrenado (qlib_export/output/model.onnx, Tarea T2) sobre 500 barras de
prueba y vuelca golden_values.csv -- la mitad Python del gate de paridad.
El lado Java corre en GoldenValueTest.java (Tarea T4), comparado por
compare_golden_values.py.

DETALLE DE VENTANEO (importante, evita un falso mismatch): las primeras
`lookback_bars` posiciones de CUALQUIER ventana de precios son warm-up (NaN),
sin importar si hay historial "real" antes de esa ventana o no -- así calcula
QlibSignalCore.computeSignal() en Java, sin contexto oculto. Para que Java
compare de verdad contra las mismas 500 predicciones reales que Python
exporta (no 500 predicciones de las cuales las primeras 5 son NaN por falta
de contexto), export_close_prices.csv incluye 5 barras de CONTEXTO extra
antes de las 500 comparadas -- ambos lados ven exactamente la misma ventana
de 505 precios, y las predicciones de las posiciones locales 5..504 (los
mismos índices en ambos lados) son las que se comparan.
"""
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort
import pandas as pd

from train_export import make_synthetic_ohlcv, compute_features

OUTPUT_DIR = Path(__file__).parent / "output"
N_COMPARE_BARS = 500


def main():
    model_path = OUTPUT_DIR / "model.onnx"
    spec_path = OUTPUT_DIR / "feature_spec.json"
    if not model_path.exists() or not spec_path.exists():
        raise FileNotFoundError(
            f"Falta {model_path} o {spec_path} -- correr train_export.py primero (Tarea T2)."
        )

    spec = json.loads(spec_path.read_text())
    lookback = spec["lookback_bars"]
    feature_names = [f["name"] for f in sorted(spec["features"], key=lambda f: f["order_index"])]

    print(f"=== 1. Regenerar la MISMA serie sintetica usada en train_export.py (seed=42) ===")
    # Mismo n_bars/seed que train_export.main() -- garantiza valores identicos
    # bit a bit, no solo "estadisticamente similares".
    close_full = make_synthetic_ohlcv(n_bars=1000, seed=42)
    print(f"OK: {len(close_full)} barras regeneradas")

    print(f"\n=== 2. Tomar ventana de {N_COMPARE_BARS + lookback} barras "
          f"({N_COMPARE_BARS} a comparar + {lookback} de contexto de warm-up) ===")
    window = close_full.tail(N_COMPARE_BARS + lookback)
    assert len(window) == N_COMPARE_BARS + lookback

    # Exportado para que Java (GoldenValueTest.java) reciba EXACTAMENTE la
    # misma ventana como input -- sin esto, Java trataria sus primeras
    # `lookback` barras como warm-up propio (NaN) aunque Python sí tuviera
    # contexto previo, generando un mismatch falso en las primeras filas.
    close_csv = OUTPUT_DIR / "close_prices.csv"
    window.reset_index().rename(columns={"index": "timestamp", "close": "close"}).to_csv(
        close_csv, index=False
    )
    print(f"OK: {close_csv} escrito ({len(window)} precios, sirve de input identico para Java)")

    print(f"\n=== 3. Calcular features + correr inferencia ONNX sobre las {N_COMPARE_BARS} barras ===")
    features_full = compute_features(window)
    # Las primeras `lookback` filas de esta ventana son warm-up (NaN) -- se
    # descartan aqui, quedan las N_COMPARE_BARS con features validas.
    features_valid = features_full.iloc[lookback:]
    assert len(features_valid) == N_COMPARE_BARS, (
        f"esperaba {N_COMPARE_BARS} filas validas, hay {len(features_valid)}"
    )

    session = ort.InferenceSession(str(model_path))
    input_name = session.get_inputs()[0].name
    X = features_valid[feature_names].values.astype(np.float32)
    predictions = session.run(None, {input_name: X})[0].flatten()

    print(f"OK: {len(predictions)} predicciones generadas")

    print(f"\n=== 4. Escribir golden_values.csv ===")
    out = features_valid.copy()
    out.insert(0, "local_index", range(lookback, lookback + N_COMPARE_BARS))
    out["prediction"] = predictions
    golden_csv = OUTPUT_DIR / "golden_values.csv"
    out.to_csv(golden_csv, index=True, index_label="timestamp")
    print(f"OK: {golden_csv} escrito ({len(out)} filas)")

    print(f"\n=== COMPLETADO === local_index va de {lookback} a {lookback + N_COMPARE_BARS - 1} "
          f"dentro de los {len(window)} precios de close_prices.csv")


if __name__ == "__main__":
    main()
