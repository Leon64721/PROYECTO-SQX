from __future__ import annotations
import hashlib
import os
import shutil
import subprocess
from pathlib import Path

src_projects = Path(r"E:\CLASE OPTION STRATEGY QUANT\PROGRAMA\SQX_144_Full\user\projects")
src_settings = Path(r"E:\CLASE OPTION STRATEGY QUANT\PROGRAMA\SQX_144_Full\user\settings")
dst_projects = Path(r"C:\SQX_144_Full\user\projects")
dst_settings = Path(r"C:\SQX_144_Full\user\settings")

workspace = Path(r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT")
java_src = workspace / "user" / "extend" / "Snippets" / "SQ"
model_src = workspace / "qlib_export" / "output"
dst_java = Path(r"C:\SQX_144_Full\user\extend\Snippets\SQ")
dst_model = Path(r"C:\SQX_144_Full\user\extend\CustomAnalysis\models")

required_java = [
    "QlibSignal.java",
    "QlibSignalCore.java",
    "OnnxModelManager.java",
    "PropFirmComplianceLogic.java",
]
required_model = ["model.onnx", "feature_spec.json"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(root: Path):
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            out[rel] = sha256_file(p)
    return out


def stop_processes():
    names = ["StrategyQuantX", "StrategyQuantX_ui", "java", "javaw"]
    for name in names:
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", f"Stop-Process -Name '{name}' -Force -ErrorAction SilentlyContinue"], check=False)
        except Exception as e:
            print(f"STOP_WARNING {name}: {e}")
    # Also use taskkill for a final fallback.
    for name in names:
        try:
            subprocess.run(["taskkill", "/F", "/IM", f"{name}.exe"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass


def ensure_source_paths():
    missing = []
    for p in [src_projects, src_settings, java_src, model_src]:
        if not p.exists():
            missing.append(str(p))
    for name in required_java:
        if not (java_src / name).exists():
            missing.append(str(java_src / name))
    for name in required_model:
        if not (model_src / name).exists():
            missing.append(str(model_src / name))
    if missing:
        raise FileNotFoundError("Missing required source paths:\n" + "\n".join(missing))


def restore_tree(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def deploy_ml():
    dst_java.mkdir(parents=True, exist_ok=True)
    dst_model.mkdir(parents=True, exist_ok=True)

    for java_file in sorted(java_src.rglob("*.java")):
        rel = java_file.relative_to(java_src)
        target = dst_java / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(java_file, target)

    for name in required_model:
        shutil.copy2(model_src / name, dst_model / name)


ensure_source_paths()
print(f"SOURCE_PROJECTS={src_projects.exists()}")
print(f"SOURCE_SETTINGS={src_settings.exists()}")
stop_processes()
restore_tree(src_projects, dst_projects)
restore_tree(src_settings, dst_settings)
deploy_ml()

projects_match = manifest(src_projects) == manifest(dst_projects)
settings_match = manifest(src_settings) == manifest(dst_settings)
print(f"PROJECTS_MATCH={projects_match}")
print(f"SETTINGS_MATCH={settings_match}")
print(f"JAVA_COUNT={len(list(dst_java.rglob('*.java')))}")
print(f"MODEL_FILES={sorted(p.name for p in dst_model.iterdir() if p.is_file())}")

if not projects_match or not settings_match:
    raise RuntimeError("Restore verification failed: project/settings manifests differ from stock source")

for name in required_java:
    assert (dst_java / name).exists(), f"Missing deployed Java file: {name}"
for name in required_model:
    assert (dst_model / name).exists(), f"Missing deployed model file: {name}"

print("RESTORE_AND_DEPLOY_OK")
