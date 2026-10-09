"""
scan_root.py — Escanea la raiz del proyecto y reporta cada entrada (archivo o carpeta) que
NO esta ya dentro de la estructura de taxonomia conocida (keep_in_root / categorias).

No mueve nada. Es de solo lectura. Uso:
    python engine/scan_root.py [--json]

Salida por defecto: texto humano. Con --json: lista de dicts para consumo programatico.
"""
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = SKILL_DIR / "taxonomy.json"


def load_taxonomy():
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def is_kept(name: str, taxonomy: dict) -> bool:
    return name in taxonomy.get("keep_in_root", [])


def match_out_of_project(name: str, taxonomy: dict) -> bool:
    patterns = taxonomy.get("out_of_project", {}).get("name_patterns", [])
    return any(re.search(p, name) for p in patterns)


def match_category(name: str, taxonomy: dict):
    """Devuelve (category_id, label) de la primera categoria cuyo patron matchee, o None."""
    for cat in taxonomy.get("categories", []):
        for pattern in cat.get("name_patterns", []):
            if re.search(pattern, name):
                return cat["id"], cat["label"]
    return None


def scan(taxonomy: dict):
    root = Path(taxonomy["project_root"])
    if not root.exists():
        raise SystemExit(f"ERROR: project_root no existe: {root}")

    findings = []
    for entry in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        name = entry.name

        if name in taxonomy.get("never_touch", []):
            continue
        if is_kept(name, taxonomy):
            continue

        if match_out_of_project(name, taxonomy):
            findings.append({
                "name": name,
                "path": str(entry),
                "is_dir": entry.is_dir(),
                "status": "OUT_OF_PROJECT",
                "suggested_destination": taxonomy["out_of_project"]["destination"],
            })
            continue

        cat_match = match_category(name, taxonomy)
        if cat_match:
            cat_id, cat_label = cat_match
            findings.append({
                "name": name,
                "path": str(entry),
                "is_dir": entry.is_dir(),
                "status": "MATCHED_BUT_STILL_IN_ROOT",
                "suggested_destination": cat_id,
                "suggested_label": cat_label,
            })
            continue

        # No matchea nada conocido -> requiere clasificacion manual (ask_user)
        findings.append({
            "name": name,
            "path": str(entry),
            "is_dir": entry.is_dir(),
            "status": "UNCLASSIFIED",
            "suggested_destination": None,
        })

    return findings


def main():
    taxonomy = load_taxonomy()
    findings = scan(taxonomy)

    as_json = "--json" in sys.argv
    if as_json:
        print(json.dumps(findings, indent=2, ensure_ascii=False))
        return

    if not findings:
        print("OK: no hay entradas sueltas en la raiz — todo esta ya clasificado en su carpeta.")
        return

    print(f"Se encontraron {len(findings)} entrada(s) en la raiz que no estan en su lugar final:\n")
    for f in findings:
        kind = "carpeta" if f["is_dir"] else "archivo"
        if f["status"] == "OUT_OF_PROJECT":
            print(f"  [FUERA DE PROYECTO] {kind} '{f['name']}' -> sugerido mover a {f['suggested_destination']}")
        elif f["status"] == "MATCHED_BUT_STILL_IN_ROOT":
            print(f"  [CLASIFICABLE]      {kind} '{f['name']}' -> sugerido: {f['suggested_destination']} ({f['suggested_label']})")
        else:
            print(f"  [SIN CLASIFICAR]    {kind} '{f['name']}' -> ningun patron coincide, preguntar al usuario")

    print("\nSiguiente paso: usar engine/classify.py para revisar cada 'SIN CLASIFICAR' con mas detalle,")
    print("o engine/apply_moves.py con un mapping.json ya confirmado para ejecutar los movimientos.")


if __name__ == "__main__":
    main()
