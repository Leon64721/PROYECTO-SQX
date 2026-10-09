"""
render_catalog.py -- Genera 01_BIBLIOTECA_CONOCIMIENTO\\CATALOGO_PROYECTO.md a partir de
content_catalog.json (fuente de verdad) + taxonomy.json:content_catalog (definiciones de
kind/strategy_type/status). Es un archivo regenerado -- no editar CATALOGO_PROYECTO.md a mano,
editar content_catalog.json via classify_content.py y volver a correr esto.

Uso:
    python engine/render_catalog.py
"""
import json
from collections import defaultdict
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


def render(taxonomy: dict, catalog: dict) -> str:
    kinds = taxonomy["content_catalog"]["kinds"]
    strategy_types = taxonomy["content_catalog"]["strategy_types"]
    statuses = taxonomy["content_catalog"]["status"]
    items = list(catalog.get("items", {}).values())

    lines = [
        "# Catálogo del proyecto — Custom Projects, estrategias, bloques e indicadores",
        "",
        "**Archivo generado automáticamente por `engine/render_catalog.py` — no editar a mano.**",
        "Para corregir una entrada: `python engine/classify_content.py \"<ruta>\" --strategy-type <tipo> --status <estado>`, "
        "luego volver a correr `render_catalog.py`. Fuente de verdad real: "
        "`.claude/skills/project-organizer/content_catalog.json`.",
        "",
        f"Total de items catalogados: **{len(items)}**",
        "",
    ]

    notes_keys = sorted(k for k in catalog.keys() if k.startswith("_note"))
    if notes_keys:
        lines.append("## Notas generales")
        lines.append("")
        for k in notes_keys:
            lines.append(f"- {catalog[k]}")
        lines.append("")

    missing = [i for i in items if i.get("path_missing")]
    pending = [i for i in items if i.get("status") == "pendiente_clasificar" and not i.get("path_missing")]
    if missing:
        lines.append(f"⚠️ **{len(missing)} item(s) ya no existen en disco** (`path_missing=true`) — revisar si se movieron o se borraron.")
    if pending:
        lines.append(f"📋 **{len(pending)} item(s) pendientes de clasificar** (recién detectados, sin tipo/estado asignado).")
    lines.append("")

    by_kind = defaultdict(list)
    for it in items:
        by_kind[it.get("kind", "?")].append(it)

    for kind_id, kind_label in kinds.items():
        group = by_kind.get(kind_id, [])
        lines.append(f"## {kind_label} (`{kind_id}`) — {len(group)} item(s)")
        lines.append("")
        if not group:
            lines.append("_Ninguno detectado todavía._")
            lines.append("")
            continue

        lines.append("| Nombre | Estado | Tipo de estrategia | Notas | Ruta |")
        lines.append("|---|---|---|---|---|")
        for it in sorted(group, key=lambda x: x.get("name", "")):
            status_id = it.get("status") or "pendiente_clasificar"
            status_label = statuses.get(status_id, status_id)
            type_id = it.get("strategy_type")
            type_label = strategy_types.get(type_id, "—") if type_id else "—"
            name = it.get("name", "")
            if it.get("path_missing"):
                name = f"⚠️ {name} (no existe en disco)"
            notes = it.get("notes", "") or ""
            path = it.get("path", "")
            lines.append(f"| {name} | {status_label} | {type_label} | {notes} | `{path}` |")
        lines.append("")

    lines.append("## Definiciones de referencia")
    lines.append("")
    lines.append("**Tipos de estrategia (`strategy_type`):**")
    for k, v in strategy_types.items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("**Estados (`status`):**")
    for k, v in statuses.items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")

    return "\n".join(lines)


def main():
    taxonomy = load_taxonomy()
    catalog = load_catalog()
    root = Path(taxonomy["project_root"])
    out_path = root / "01_BIBLIOTECA_CONOCIMIENTO" / "CATALOGO_PROYECTO.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(taxonomy, catalog), encoding="utf-8")
    print(f"escrito: {out_path}")


if __name__ == "__main__":
    main()
