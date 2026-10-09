"""
validate.py — Revisa invariantes del proyecto tras aplicar movimientos:
  1. `user\\` sigue existiendo y no fue tocado (se compara solo su presencia, no su contenido interno).
  2. No quedan entradas sueltas en la raiz fuera de keep_in_root (llama a scan_root.py).
  3. No hay carpetas duplicadas (mismo nombre) entre las 5 categorias nuevas.
  4. Todas las categorias declaradas en taxonomy.json existen en disco.

Uso:
    python engine/validate.py
Codigo de salida: 0 si todo OK, 1 si hay problemas (se listan en stdout).
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = SKILL_DIR / "taxonomy.json"

sys.path.insert(0, str(SKILL_DIR / "engine"))
import scan_root  # noqa: E402


def load_taxonomy():
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    taxonomy = load_taxonomy()
    root = Path(taxonomy["project_root"])
    problems = []

    # 1) user\ existe
    user_dir = root / "user"
    if not user_dir.exists():
        problems.append("CRITICO: la carpeta 'user' no existe en la raiz — no deberia haberse movido nunca.")

    # 2) categorias existen en disco
    for cat in taxonomy.get("categories", []):
        cat_path = root / cat["id"]
        if not cat_path.exists():
            problems.append(f"Falta la carpeta de categoria declarada en taxonomy.json: {cat['id']}")

    # 3) sin duplicados de nombre entre categorias (comparando solo el primer nivel de cada categoria)
    name_locations = defaultdict(list)
    for cat in taxonomy.get("categories", []):
        cat_path = root / cat["id"]
        if not cat_path.exists():
            continue
        for entry in cat_path.iterdir():
            name_locations[entry.name].append(str(entry))
    for name, locations in name_locations.items():
        if len(locations) > 1:
            problems.append(f"Posible carpeta/archivo duplicado '{name}' en: {', '.join(locations)}")

    # 4) nada suelto en la raiz sin clasificar
    findings = scan_root.scan(taxonomy)
    unclassified = [f for f in findings if f["status"] == "UNCLASSIFIED"]
    matched_not_moved = [f for f in findings if f["status"] == "MATCHED_BUT_STILL_IN_ROOT"]
    out_of_project = [f for f in findings if f["status"] == "OUT_OF_PROJECT"]

    if unclassified:
        problems.append(f"{len(unclassified)} entrada(s) sin clasificar en la raiz: " +
                         ", ".join(f["name"] for f in unclassified))
    if matched_not_moved:
        problems.append(f"{len(matched_not_moved)} entrada(s) ya clasificables pero aun en la raiz: " +
                         ", ".join(f["name"] for f in matched_not_moved))
    if out_of_project:
        problems.append(f"{len(out_of_project)} entrada(s) fuera de proyecto aun en la raiz: " +
                         ", ".join(f["name"] for f in out_of_project))

    if problems:
        print(f"VALIDACION: {len(problems)} problema(s) encontrado(s):\n")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    print("VALIDACION OK: estructura del proyecto consistente con taxonomy.json, "
          "'user\\' intacto, raiz sin entradas sueltas.")
    sys.exit(0)


if __name__ == "__main__":
    main()
