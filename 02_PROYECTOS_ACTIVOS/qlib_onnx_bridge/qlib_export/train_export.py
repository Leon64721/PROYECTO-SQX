"""
Backend de entrenamiento y exportación Qlib->ONNX (Tarea T2 de Qlib_ONNX_Bridge_Design.md).

ESTADO DE ESTA CORRIDA: modelo de PRUEBA sobre datos sintéticos, para probar la mecánica
completa (features -> LightGBM -> ONNX -> feature_spec.json con hash) de punta a punta.
NO usa el workflow real de Qlib todavía (no hay instalación de Qlib en este entorno ni
datos reales de mercado conectados) -- eso es un paso posterior, explícito, cuando haya un
proyecto Qlib real para entrenar contra el instrumento/ventana de datos reales de SQX.

Salida: qlib_export/output/ (sandbox del proyecto). Desplegar a la instalación viva de SQX
(C:\\SQX_144_Full\\user\\extend\\CustomAnalysis\\models\\) es un paso aparte, no automático --
ver Qlib_ONNX_Bridge_Design.md, gate CEO (c): paridad de fuente de datos.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path

import numpy as np
import onnx
import pandas as pd

OUTPUT_DIR = Path(__file__).parent / "output"


# ---------------------------------------------------------------------------
# Features -- formulas simples, estilo Alpha158 (retornos/medias/std móviles),
# documentadas explícitamente para que feature_spec.json sea la fuente de verdad
# que el port Java debe replicar exacto.
# ---------------------------------------------------------------------------
FEATURE_DEFS = [
    {"name": "return_1", "lookback": 1,
     "formula": "close[t] / close[t-1] - 1"},
    {"name": "return_5", "lookback": 5,
     "formula": "close[t] / close[t-5] - 1"},
    {"name": "ma_5", "lookback": 5,
     "formula": "mean(close[t-4:t+1])"},
    {"name": "std_5", "lookback": 5,
     "formula": "std(close[t-4:t+1])"},
]


def compute_features(close: pd.Series) -> pd.DataFrame:
    """Calcula las features de FEATURE_DEFS sobre una serie de precios de cierre.
    Implementación de referencia -- el port Java (assembleFeatureBatch en
    QlibSignal.java) debe producir EXACTAMENTE estos mismos valores; esto es lo
    que valida el gate de valores dorados (export_golden_values.py)."""
    df = pd.DataFrame(index=close.index)
    df["return_1"] = close / close.shift(1) - 1
    df["return_5"] = close / close.shift(5) - 1
    df["ma_5"] = close.rolling(5).mean()
    df["std_5"] = close.rolling(5).std()
    return df


def make_synthetic_ohlcv(n_bars: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Genera una serie de precios sintética (random walk) SOLO para probar la
    mecánica de este pipeline. NO representa datos de mercado reales -- cuando
    se conecte Qlib de verdad, esta función se reemplaza por el data loader real
    (qlib.data.D.features() o equivalente) contra el instrumento real de SQX."""
    rng = np.random.default_rng(seed)
    returns = rng.normal(loc=0.0002, scale=0.01, size=n_bars)
    close = 100.0 * np.cumprod(1 + returns)
    dates = pd.date_range("2020-01-01", periods=n_bars, freq="D")
    return pd.Series(close, index=dates, name="close")


def train_or_load_model(feature_frame: pd.DataFrame, target: pd.Series):
    """Entrena un LightGBM real sobre las features + target ya alineados
    (NaN de warm-up ya descartados por el caller).

    TODO (conexión con Qlib real): reemplazar por qlib.workflow.R / qrun con un
    config YAML real, usando el LightGBM/PyTorch entrenado por Qlib sobre datos
    de mercado reales -- NO reinventar el loop de entrenamiento aquí. Esta
    función solo prueba que el resto del pipeline (export/hash/spec) funciona."""
    import lightgbm as lgb

    model = lgb.LGBMRegressor(n_estimators=50, max_depth=4, verbose=-1)
    model.fit(feature_frame.values, target.values)
    return model


def assert_no_temporal_leakage(train_end_date: str, sqx_oos_start_date: str) -> None:
    """Gate (b) de la revisión CEO: la ventana de entrenamiento de Qlib NO debe
    solaparse con las ventanas walk-forward que SQX tratará como out-of-sample.
    sqx_oos_start_date debe venir de la configuración real del proyecto SQX
    (Task de Walk-Forward / Retest), no asumirse."""
    train_end = datetime.date.fromisoformat(train_end_date)
    oos_start = datetime.date.fromisoformat(sqx_oos_start_date)
    if train_end >= oos_start:
        raise ValueError(
            f"FUGA TEMPORAL: el modelo se entrenó hasta {train_end}, pero SQX trata "
            f"{oos_start} en adelante como out-of-sample. Recortar el training set "
            f"o mover la ventana OOS de SQX."
        )


def export_to_onnx(model, n_features: int):
    """Convierte el LGBMRegressor entrenado a ONNX vía onnxmltools."""
    from onnxmltools import convert_lightgbm
    from onnxmltools.convert.common.data_types import FloatTensorType

    onnx_model = convert_lightgbm(
        model,
        initial_types=[("input", FloatTensorType([None, n_features]))],
        # Sin target_opset explicito: onnxmltools elige el opset maximo que su
        # convertidor y el paquete onnx instalado realmente soportan. Un valor
        # fijo (17) fallo en este entorno -- el maximo real es 15 (ver corrida
        # fallida). No hardcodear un numero que no se verifico contra el
        # entorno real.
    )
    return onnx_model


def write_feature_spec(feature_names: list, feature_defs: list, model_kind: str,
                        trained_at: str, train_start: str, train_end: str) -> tuple:
    """Escribe feature_spec.json y retorna (spec_dict, spec_hash)."""
    lookback_by_name = {f["name"]: f["lookback"] for f in feature_defs}
    formula_by_name = {f["name"]: f["formula"] for f in feature_defs}

    spec = {
        "version": 1,
        "model_kind": model_kind,
        "trained_at": trained_at,
        "train_window": {"start": train_start, "end": train_end},
        "lookback_bars": max(lookback_by_name.values()),
        "features": [
            {
                "name": name,
                "formula": formula_by_name[name],
                "lookback": lookback_by_name[name],
                "order_index": i,
            }
            for i, name in enumerate(feature_names)
        ],
    }
    spec_json = json.dumps(spec, indent=2, sort_keys=True)
    spec_hash = hashlib.sha256(spec_json.encode()).hexdigest()[:16]
    spec["spec_hash"] = spec_hash

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    spec_path = OUTPUT_DIR / "feature_spec.json"
    spec_path.write_text(json.dumps(spec, indent=2))
    return spec, spec_hash


def embed_spec_hash_in_onnx(onnx_model, spec_hash: str):
    """Embebe spec_hash como metadata custom del modelo ONNX, para que
    OnnxModelManager.java pueda verificar en tiempo de carga que model.onnx y
    feature_spec.json no se desincronizaron (hallazgo #7 de la revisión
    "outside voice" de /plan-eng-review)."""
    meta = onnx_model.metadata_props.add()
    meta.key = "spec_hash"
    meta.value = spec_hash
    return onnx_model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-end-date", default="2022-06-30")
    parser.add_argument("--sqx-oos-start-date", default="2022-07-01")
    args = parser.parse_args()

    print("=== 1. Gate (b): verificar que NO hay fuga temporal ===")
    assert_no_temporal_leakage(args.train_end_date, args.sqx_oos_start_date)
    print(f"OK: train_end={args.train_end_date} < sqx_oos_start={args.sqx_oos_start_date}")

    print("\n=== 2. Generar datos sintéticos (SOLO para probar el pipeline) ===")
    close = make_synthetic_ohlcv(n_bars=1000)
    print(f"OK: {len(close)} barras sintéticas generadas")

    print("\n=== 3. Calcular features (Alpha158-style, formulas en FEATURE_DEFS) ===")
    features = compute_features(close)
    target = (close.shift(-1) / close - 1).rename("target")  # retorno del siguiente bar
    combined = pd.concat([features, target], axis=1).dropna()
    feature_names = [f["name"] for f in FEATURE_DEFS]
    print(f"OK: {len(combined)} filas post warm-up (de {len(close)} barras totales)")

    print("\n=== 4. Entrenar LightGBM (modelo de PRUEBA, no Qlib real) ===")
    model = train_or_load_model(combined[feature_names], combined["target"])
    print(f"OK: modelo entrenado, {model.n_features_} features")

    print("\n=== 5. Exportar a ONNX ===")
    onnx_model = export_to_onnx(model, n_features=len(feature_names))
    print(f"OK: modelo ONNX generado (opset {onnx_model.opset_import[0].version})")

    print("\n=== 6. Escribir feature_spec.json con hash SHA-256 ===")
    spec, spec_hash = write_feature_spec(
        feature_names, FEATURE_DEFS, model_kind="lightgbm",
        trained_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        train_start=str(close.index[0].date()), train_end=args.train_end_date,
    )
    print(f"OK: feature_spec.json escrito, spec_hash={spec_hash}, "
          f"lookback_bars={spec['lookback_bars']}")

    print("\n=== 7. Embeber spec_hash en metadata del modelo ONNX ===")
    onnx_model = embed_spec_hash_in_onnx(onnx_model, spec_hash)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model_path = OUTPUT_DIR / "model.onnx"
    onnx.save(onnx_model, str(model_path))
    print(f"OK: model.onnx escrito en {model_path}")

    print("\n=== 8. Verificar acoplamiento model.onnx <-> feature_spec.json ===")
    reloaded = onnx.load(str(model_path))
    embedded_hash = next(
        (m.value for m in reloaded.metadata_props if m.key == "spec_hash"), None
    )
    assert embedded_hash == spec_hash, (
        f"MISMATCH: metadata del modelo trae {embedded_hash}, spec real es {spec_hash}"
    )
    print(f"OK: hash embebido en model.onnx ({embedded_hash}) coincide con "
          f"feature_spec.json ({spec_hash})")

    print(f"\n=== COMPLETADO === Outputs en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
