"""
classify.py — Sugiere una categoria/destino para UNA entrada dada (archivo o carpeta), usando
la taxonomia (patrones de nombre) y, si no matchea nada, inspeccionando el contenido superficial
(extensiones dominantes, presencia de SKILL.md/README, etc.) para dar una pista adicional.

NUNCA decide solo por contenido cuando no hay patron de nombre — siempre marca esos casos como
"REQUIERE_CONFIRMACION_USUARIO" en vez de adivinar en silencio (mismo principio que sqx-custom-block:
no asumir, preguntar).

Uso:
    python engine/classify.py "<ruta_absoluta_a_la_entrada>"
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = SKILL_DIR / "taxonomy.json"


def load_taxonomy():
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def match_category(name: str, taxonomy: dict):
    for cat in taxonomy.get("categories", []):
        for pattern in cat.get("name_patterns", []):
            if re.search(pattern, name):
                return cat
    return None


def match_out_of_project(name: str, taxonomy: dict) -> bool:
    patterns = taxonomy.get("out_of_project", {}).get("name_patterns", [])
    return any(re.search(p, name) for p in patterns)


def content_hint(entry: Path) -> str:
    """Pista superficial de contenido, solo informativa — no decide la clasificacion."""
    if not entry.is_dir():
        ext = entry.suffix.lower()
        size_kb = entry.stat().st_size / 1024
        return f"archivo suelto, extension={ext or '(sin extension)'}, {size_kb:.1f} KB"

    try:
        children = list(entry.iterdir())
    except PermissionError:
        return "carpeta (sin permiso de lectura)"

    if any(c.name.upper() in ("SKILL.MD",) for c in children):
        return "carpeta con SKILL.md -> probable material de biblioteca/skill"
    if any(c.name.lower() == "readme.md" for c in children):
        return "carpeta con README.md -> revisar de que trata antes de clasificar"

    exts = Counter(c.suffix.lower() for c in children if c.is_file())
    top_ext = exts.most_common(3)
    n_files = sum(1 for c in children if c.is_file())
    n_dirs = sum(1 for c in children if c.is_dir())
    return f"carpeta con {n_files} archivo(s) / {n_dirs} subcarpeta(s); extensiones dominantes: {top_ext or 'ninguna'}"


def classify(path_str: str, taxonomy: dict) -> dict:
    entry = Path(path_str)
    if not entry.exists():
        return {"error": f"no existe: {path_str}"}

    name = entry.name
    result = {
        "name": name,
        "path": str(entry),
        "is_dir": entry.is_dir(),
        "content_hint": content_hint(entry),
    }

    if name in taxonomy.get("never_touch", []):
        result["decision"] = "NEVER_TOUCH"
        result["reason"] = "Esta en la lista never_touch de la taxonomia (ej. user\\)."
        return result

    if name in taxonomy.get("keep_in_root", []):
        result["decision"] = "KEEP_IN_ROOT"
        result["reason"] = "Ya es parte de la estructura fija de la raiz."
        return result

    if match_out_of_project(name, taxonomy):
        result["decision"] = "OUT_OF_PROJECT"
        result["suggested_destination"] = taxonomy["out_of_project"]["destination"]
        result["reason"] = "El nombre coincide con un patron de contenido no relacionado al proyecto (ver taxonomy.json:out_of_project)."
        return result

    cat = match_category(name, taxonomy)
    if cat:
        result["decision"] = "CLASSIFIED"
        result["category_id"] = cat["id"]
        result["category_label"] = cat["label"]
        result["reason"] = f"El nombre coincide con un patron de la categoria {cat['id']}."
        return result

    result["decision"] = "REQUIERE_CONFIRMACION_USUARIO"
    result["reason"] = "Ningun patron de nombre coincide. Revisar content_hint y preguntar al usuario antes de mover."
    return result


def main():
    if len(sys.argv) < 2:
        print("Uso: python engine/classify.py \"<ruta_absoluta>\"")
        sys.exit(1)

    taxonomy = load_taxonomy()
    result = classify(sys.argv[1], taxonomy)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
