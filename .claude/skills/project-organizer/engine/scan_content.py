"""
scan_content.py -- Escanea las ubicaciones declaradas en taxonomy.json:content_catalog.
scan_locations y detecta items NUEVOS (Custom Projects .cfx, carpetas de portfolio bajo
user\\projects, Custom Blocks/Random Groups XML generados, indicadores). Los agrega a
content_catalog.json con status="pendiente_clasificar" y strategy_type=null -- NUNCA les
asigna un tipo/estado por su cuenta, eso lo hace classify_content.py con confirmacion del
usuario.

Tambien detecta items que YA estaban en el catalogo pero cuyo archivo/carpeta desaparecio
del disco (marca "path_missing": true, no los borra del catalogo -- historial).

Es de solo lectura sobre el proyecto (nunca mueve/borra nada); solo escribe/actualiza
content_catalog.json.

Uso:
    python engine/scan_content.py            # aplica los cambios a content_catalog.json
    python engine/scan_content.py --dry-run  # solo muestra que encontraria, no escribe
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = SKILL_DIR / "taxonomy.json"
CATALOG_PATH = SKILL_DIR / "content_catalog.json"


def load_taxonomy():
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_catalog():
    if not CATALOG_PATH.exists():
        return {"_comment": "Fuente de verdad del catalogo de contenido. Ver taxonomy.json:content_catalog para el esquema (kinds/strategy_types/status). Editar via engine/classify_content.py, no a mano salvo correccion puntual.",
                "items": {}}
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_catalog(catalog: dict):
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write("\n")


def discover(taxonomy: dict) -> list[dict]:
    root = Path(taxonomy["project_root"])
    found = []
    for loc in taxonomy["content_catalog"]["scan_locations"]:
        kind = loc["kind"]
        dirs_only = loc.get("dirs_only", False)
        exclude_names = set(loc.get("exclude_names", []))
        exclude_name_contains = [s.lower() for s in loc.get("exclude_name_contains", [])]
        for rel_root in loc["roots"]:
            base = root / rel_root
            if not base.exists():
                continue
            for entry in base.glob(loc["glob"]):
                if entry.name in exclude_names:
                    continue
                if exclude_name_contains and any(s in entry.name.lower() for s in exclude_name_contains):
                    continue
                if dirs_only and not entry.is_dir():
                    continue
                if not dirs_only and entry.is_dir():
                    continue
                found.append({"kind": kind, "path": str(entry)})
    return found


def main():
    dry_run = "--dry-run" in sys.argv
    taxonomy = load_taxonomy()
    catalog = load_catalog()
    items = catalog.setdefault("items", {})

    discovered = discover(taxonomy)
    discovered_paths = {d["path"] for d in discovered}

    new_count = 0
    for d in discovered:
        key = d["path"]
        if key not in items:
            new_count += 1
            entry = {
                "kind": d["kind"],
                "path": d["path"],
                "name": Path(d["path"]).name,
                "strategy_type": None,
                "status": "pendiente_clasificar",
                "notes": "",
            }
            if not dry_run:
                items[key] = entry

    missing_count = 0
    for key, entry in items.items():
        currently_missing = not Path(key).exists()
        was_missing = entry.get("path_missing", False)
        if currently_missing and not was_missing:
            missing_count += 1
            if not dry_run:
                entry["path_missing"] = True
        elif not currently_missing and was_missing:
            if not dry_run:
                entry["path_missing"] = False

    print(f"Escaneado: {len(discovered)} item(s) encontrados en las ubicaciones declaradas.")
    print(f"  Nuevos (agregados como pendiente_clasificar): {new_count}")
    print(f"  Ya existian en el catalogo: {len(discovered) - new_count}")
    print(f"  Marcados path_missing (estaban en catalogo, ya no existen en disco): {missing_count}")

    if dry_run:
        print("\n--dry-run: no se escribio content_catalog.json.")
        return

    save_catalog(catalog)
    print(f"\ncontent_catalog.json actualizado ({len(items)} item(s) totales).")

    pending = [i for i in items.values() if i.get("status") == "pendiente_clasificar"]
    if pending:
        print(f"\nSiguiente paso: {len(pending)} item(s) con status=pendiente_clasificar.")
        print("Usar engine/classify_content.py \"<ruta>\" --strategy-type <tipo> --status <estado>")
        print("(o dejar que el agente pregunte al usuario item por item antes de asignar).")


if __name__ == "__main__":
    main()
