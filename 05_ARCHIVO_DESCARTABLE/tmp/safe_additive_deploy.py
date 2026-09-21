from __future__ import annotations
import hashlib
import shutil
from pathlib import Path

work = Path(r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT")
source_java_root = work / "user" / "extend" / "Snippets" / "SQ"
source_model_root = work / "qlib_export" / "output"
stock_projects_root = Path(r"C:\SQX_144_Full\user\projects")
stock_settings_root = Path(r"C:\SQX_144_Full\user\settings")
dest_java_root = Path(r"C:\SQX_144_Full\user\extend\Snippets\SQ")
dest_model_root = Path(r"C:\SQX_144_Full\user\extend\CustomAnalysis\models")

required_java = [
    "QlibSignal.java",
    "QlibSignalCore.java",
    "OnnxModelManager.java",
    "PropFirmComplianceLogic.java",
]
required_model = [
    "model.onnx",
    "feature_spec.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(root: Path):
    items = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            items[rel] = sha256_file(p)
    return items


def require_files():
    missing = []
    for name in required_java:
        p = source_java_root / name
        if not p.exists():
            missing.append(str(p))
    for name in required_model:
        p = source_model_root / name
        if not p.exists():
            missing.append(str(p))
    if missing:
        raise FileNotFoundError("Missing required source files:\n" + "\n".join(missing))


require_files()

before_projects = manifest(stock_projects_root)
before_settings = manifest(stock_settings_root)

print(f"BEFORE_PROJECTS={len(before_projects)} FILES")
print(f"BEFORE_SETTINGS={len(before_settings)} FILES")

# Create destination folders but do not touch native projects/settings.
dest_java_root.mkdir(parents=True, exist_ok=True)
dest_model_root.mkdir(parents=True, exist_ok=True)

for java_file in sorted(source_java_root.rglob("*.java")):
    relative = java_file.relative_to(source_java_root)
    destination = dest_java_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(java_file, destination)

for model_name in required_model:
    src = source_model_root / model_name
    shutil.copy2(src, dest_model_root / model_name)

after_projects = manifest(stock_projects_root)
after_settings = manifest(stock_settings_root)

projects_changed = (before_projects != after_projects)
settings_changed = (before_settings != after_settings)

print(f"PROJECTS_CHANGED={projects_changed}")
print(f"SETTINGS_CHANGED={settings_changed}")

if projects_changed:
    proj_keys = sorted(set(before_projects) | set(after_projects))
    diffs = [k for k in proj_keys if before_projects.get(k) != after_projects.get(k)]
    print(f"PROJECT_DIFFERENCES={diffs[:10]}")
if settings_changed:
    set_keys = sorted(set(before_settings) | set(after_settings))
    diffs = [k for k in set_keys if before_settings.get(k) != after_settings.get(k)]
    print(f"SETTINGS_DIFFERENCES={diffs[:10]}")

java_copied = [p.name for p in sorted(dest_java_root.rglob("*.java")) if p.name in required_java]
model_copied = sorted(p.name for p in dest_model_root.iterdir() if p.is_file())
print(f"JAVA_COPIED={java_copied}")
print(f"MODEL_COPIED={model_copied}")
print(f"JAVA_COUNT={len(list(dest_java_root.rglob('*.java')))}")
print(f"MODEL_COUNT={len(list(dest_model_root.iterdir()))}")

assert not projects_changed, "Native projects directory changed; deployment is not additive-safe."
assert not settings_changed, "Native settings directory changed; deployment is not additive-safe."
assert all((dest_java_root / name).exists() for name in required_java)
assert all((dest_model_root / name).exists() for name in required_model)
print("SAFE_ADDITIVE_DEPLOYMENT=OK")
