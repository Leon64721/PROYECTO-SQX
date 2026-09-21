"""
Arnes de comparacion bar-a-bar del gate de valores dorados (Tarea T4 de
Qlib_ONNX_Bridge_Design.md, gate (a) de /plan-ceo-review): compara
golden_values.csv (predicciones de Python/onnxruntime) contra
java_predictions.csv (predicciones de GoldenValueTest.java, corriendo la
MISMA logica que usara QlibSignal.java real dentro de SQX), exigiendo
tolerancia estricta < 1e-6.

Nota de alineacion: golden_values.csv usa `local_index` (5..504) relativo a
los 505 precios de close_prices.csv; java_predictions.csv usa el mismo
`local_index` (0..504, de los cuales 0..4 son NaN de warm-up). Se comparan
solo los local_index presentes en AMBOS archivos con valor real (no NaN) --
las filas de warm-up (5 primeras) no estan en golden_values.csv en absoluto,
asi que la interseccion ya las excluye naturalmente.
"""
import sys
from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path(__file__).parent / "output"
TOLERANCE = 1e-6


def main():
    golden_path = OUTPUT_DIR / "golden_values.csv"
    java_path = OUTPUT_DIR / "java_predictions.csv"

    if not golden_path.exists():
        print(f"FALTA {golden_path} -- correr export_golden_values.py primero.")
        sys.exit(2)
    if not java_path.exists():
        print(f"FALTA {java_path} -- correr GoldenValueTest.java primero.")
        sys.exit(2)

    golden = pd.read_csv(golden_path)
    java = pd.read_csv(java_path)

    print(f"golden_values.csv: {len(golden)} filas (predicciones Python)")
    print(f"java_predictions.csv: {len(java)} filas (predicciones Java, incluye warm-up NaN)")

    merged = golden[["local_index", "prediction"]].merge(
        java, on="local_index", how="inner", suffixes=("_python", "")
    )
    if len(merged) != len(golden):
        print(f"ADVERTENCIA: solo {len(merged)}/{len(golden)} local_index coinciden entre "
              f"ambos archivos -- revisar que export_golden_values.py y GoldenValueTest.java "
              f"corrieron sobre la misma ventana.")

    merged["abs_diff"] = (merged["prediction"] - merged["java_prediction"]).abs()
    mismatches = merged[merged["abs_diff"] >= TOLERANCE]

    nan_in_java = merged["java_prediction"].isna()
    if nan_in_java.any():
        print(f"\nFALLO: {nan_in_java.sum()} filas tienen NaN en Java donde Python dio un "
              f"valor real -- indica que el warm-up de Java no calza con la ventana esperada.")
        print(merged[nan_in_java].head(10))
        sys.exit(1)

    print(f"\nComparadas {len(merged)} filas, tolerancia < {TOLERANCE}")
    print(f"  diff maxima:    {merged['abs_diff'].max():.3e}")
    print(f"  diff promedio:  {merged['abs_diff'].mean():.3e}")

    if mismatches.empty:
        print(f"\nGATE PASADO: 0 discrepancias >= {TOLERANCE} entre Java y Python. "
              f"Java replica el computo de Python bit-a-bit (dentro de tolerancia float32).")
    else:
        print(f"\nGATE FALLIDO: {len(mismatches)} discrepancias >= {TOLERANCE}:")
        print(mismatches[["local_index", "prediction", "java_prediction", "abs_diff"]]
              .sort_values("abs_diff", ascending=False).head(20))
        sys.exit(1)


if __name__ == "__main__":
    main()
