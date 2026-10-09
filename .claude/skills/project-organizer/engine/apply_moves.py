"""
apply_moves.py — Ejecuta movimientos de archivos/carpetas ya confirmados por el usuario, a partir
de un mapping.json con esta forma:

[
  {"src": "E:\\...\\STRATEGY QUANT\\algo_nuevo", "dest": "E:\\...\\STRATEGY QUANT\\01_BIBLIOTECA_CONOCIMIENTO\\academia_descargas\\algo_nuevo"},
  ...
]

Reglas de seguridad (no negociables):
  - Nunca mueve nada cuyo nombre este en taxonomy.json:never_touch (ej. "user").
  - Nunca sobreescribe un destino existente (falla en vez de pisar datos).
  - Nunca borra el origen tras mover a "05_ARCHIVO_DESCARTABLE" — solo lo reubica.
  - Si el repo git tiene commits, usa `git mv` (preserva historial); si no, usa un move normal.
  - Registra cada movimiento (exitoso o fallido) en logs/moves_<timestamp>.jsonl.

Uso:
    python engine/apply_moves.py mapping.json [--dry-run]
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = SKILL_DIR / "taxonomy.json"
LOGS_DIR = SKILL_DIR / "logs"


def load_taxonomy():
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def repo_has_commits(project_root: Path) -> bool:
    try:
        r = subprocess.run(
            ["git", "-C", str(project_root), "rev-parse", "HEAD"],
            capture_output=True, text=True,
        )
        return r.returncode == 0
    except FileNotFoundError:
        return False


def do_move(src: Path, dest: Path, use_git: bool, project_root: Path) -> tuple:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if use_git:
        r = subprocess.run(
            ["git", "-C", str(project_root), "mv", str(src), str(dest)],
            capture_output=True, text=True,
        )
        if r.returncode == 0:
            return True, "git mv"
        # fallback si git mv falla (ej. archivo no rastreado todavia por git)
    src.rename(dest)
    return True, ("move (fallback tras git mv fallido)" if use_git else "move")


def main():
    if len(sys.argv) < 2:
        print("Uso: python engine/apply_moves.py mapping.json [--dry-run]")
        sys.exit(1)

    mapping_path = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv

    with open(mapping_path, "r", encoding="utf-8-sig") as f:
        mapping = json.load(f)

    taxonomy = load_taxonomy()
    never_touch = set(taxonomy.get("never_touch", []))
    project_root = Path(taxonomy["project_root"])
    use_git = repo_has_commits(project_root) and not dry_run

    LOGS_DIR.mkdir(exist_ok=True)
    log_path = LOGS_DIR / f"moves_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

    results = []
    for item in mapping:
        src = Path(item["src"])
        dest = Path(item["dest"])
        entry = {"src": str(src), "dest": str(dest)}

        if src.name in never_touch:
            entry["status"] = "REFUSED_NEVER_TOUCH"
            results.append(entry)
            continue
        if not src.exists():
            entry["status"] = "REFUSED_SRC_NOT_FOUND"
            results.append(entry)
            continue
        if dest.exists():
            entry["status"] = "REFUSED_DEST_ALREADY_EXISTS"
            results.append(entry)
            continue

        if dry_run:
            entry["status"] = "DRY_RUN_OK"
            results.append(entry)
            continue

        try:
            ok, method = do_move(src, dest, use_git, project_root)
            entry["status"] = "MOVED"
            entry["method"] = method
        except Exception as e:
            entry["status"] = "ERROR"
            entry["error"] = str(e)
        results.append(entry)

    with open(log_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    ok_count = sum(1 for r in results if r["status"] in ("MOVED", "DRY_RUN_OK"))
    print(f"{'[DRY-RUN] ' if dry_run else ''}{ok_count}/{len(results)} movimiento(s) OK. Log: {log_path}")
    for r in results:
        if r["status"] not in ("MOVED", "DRY_RUN_OK"):
            print(f"  ATENCION [{r['status']}]: {r['src']} -> {r['dest']}")


if __name__ == "__main__":
    main()
