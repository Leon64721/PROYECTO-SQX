"""
classify_content.py -- Asigna strategy_type/status a UN item ya detectado por scan_content.py,
o consulta su estado actual. Da una pista de contenido superficial (para .cfx/.xml: intenta leer
metadatos reconocibles -- nombre de bloques Custom/AlgoWizard, simbolo, timeframe -- SIN interpretar
eso como una decision), pero la asignacion de strategy_type/status siempre viene de los flags
explicitos --strategy-type/--status (que en la practica el agente solo pasa despues de confirmar
con el usuario). Nunca adivina en silencio -- mismo principio que classify.py (capa de carpetas).

Uso:
    # ver el item + pista de contenido (no cambia nada)
    python engine/classify_content.py "<ruta_absoluta>"

    # asignar tipo/estado (una vez confirmado con el usuario)
    python engine/classify_content.py "<ruta_absoluta>" --strategy-type breakout_session --status vigente

    # agregar una nota libre
    python engine/classify_content.py "<ruta_absoluta>" --notes "Version activa del ORB, ver item 31"
"""
import json
import re
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
        raise SystemExit("content_catalog.json no existe todavia -- correr engine/scan_content.py primero.")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_catalog(catalog: dict):
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write("\n")


def content_hint(path_str: str, kind: str) -> str:
    """Pista superficial, solo informativa -- nunca decide strategy_type/status por su cuenta."""
    p = Path(path_str)
    if not p.exists():
        return "(archivo/carpeta ya no existe en disco -- ver path_missing)"

    if kind == "portfolio_project" and p.is_dir():
        n_sqx = sum(1 for _ in p.glob("*.sqx"))
        return f"carpeta de portfolio con {n_sqx} estrategia(s) .sqx"

    if kind in ("custom_block", "random_group") and p.suffix.lower() == ".xml":
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return "(no se pudo leer el archivo)"
        keys = re.findall(r'key="(CBlock_[A-Za-z0-9_]+)"', text)
        cats = re.findall(r'category="([A-Za-z0-9_]+)"', text)
        groups = re.findall(r'<Group[^>]*name="([^"]+)"', text)
        parts = []
        if keys:
            parts.append(f"bloques: {', '.join(sorted(set(keys)))}")
        if cats:
            parts.append(f"categorias: {', '.join(sorted(set(cats)))}")
        if groups:
            parts.append(f"grupos: {', '.join(sorted(set(groups)))}")
        return "; ".join(parts) if parts else "XML sin marcadores reconocidos"

    if kind == "custom_project" and p.suffix.lower() == ".cfx":
        size_kb = p.stat().st_size / 1024
        return f"Custom Project (.cfx), {size_kb:.1f} KB -- abrir en SQX para confirmar simbolo/broker/tipo"

    if p.is_dir():
        n_files = sum(1 for c in p.iterdir() if c.is_file())
        return f"carpeta con {n_files} archivo(s) directo(s)"

    return f"archivo suelto, {p.stat().st_size / 1024:.1f} KB"


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(1)

    path_arg = argv[0]
    strategy_type = None
    status = None
    notes = None
    i = 1
    while i < len(argv):
        if argv[i] == "--strategy-type" and i + 1 < len(argv):
            strategy_type = argv[i + 1]
            i += 2
        elif argv[i] == "--status" and i + 1 < len(argv):
            status = argv[i + 1]
            i += 2
        elif argv[i] == "--notes" and i + 1 < len(argv):
            notes = argv[i + 1]
            i += 2
        else:
            i += 1

    taxonomy = load_taxonomy()
    catalog = load_catalog()
    items = catalog.setdefault("items", {})

    # tolera que el usuario pase una ruta con distinta capitalizacion/slashes que la key guardada
    key = path_arg
    if key not in items:
        matches = [k for k in items if Path(k).resolve() == Path(path_arg).resolve()]
        if matches:
            key = matches[0]
        else:
            print(f"'{path_arg}' no esta en content_catalog.json todavia.")
            print("Correr engine/scan_content.py primero para detectarlo.")
            sys.exit(1)

    entry = items[key]
    valid_types = set(taxonomy["content_catalog"]["strategy_types"])
    valid_status = set(taxonomy["content_catalog"]["status"])

    if strategy_type is not None:
        if strategy_type not in valid_types:
            print(f"strategy_type invalido: {strategy_type!r}. Validos: {sorted(valid_types)}")
            sys.exit(1)
        entry["strategy_type"] = strategy_type
    if status is not None:
        if status not in valid_status:
            print(f"status invalido: {status!r}. Validos: {sorted(valid_status)}")
            sys.exit(1)
        entry["status"] = status
    if notes is not None:
        entry["notes"] = notes

    if strategy_type or status or notes:
        save_catalog(catalog)
        print(f"Actualizado: {key}")

    print(json.dumps({
        **entry,
        "content_hint": content_hint(key, entry["kind"]),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
