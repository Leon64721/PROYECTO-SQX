#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera NDXm_ORB_PropFirm_V1 usando sqx-strategy-project.
- Base: Builder (NDXm_TICK_UTCPlus02 / M15)
- Template: NDXm_NY_Session_Template.sqx (diseñado para NDXm con NY Session Window)
- Resultado: 1 build task, listo para importar en SQX
"""

import os
import sys
import glob
from pathlib import Path

# Agregar engine al path
engine_dir = Path(__file__).parent / "engine"
sys.path.insert(0, str(engine_dir))

from generate import make_project, deploy

INSTALL = r"C:\SQX_144_Full"
BASE_PATH = Path(INSTALL) / "user/projects/Builder/project.cfx"
TPL_DIR = Path(INSTALL) / "user/settings/StrategyTemplates/NDXm_Fleet"
OUT_PROJECT = Path(__file__).parent / "out" / "NDXm_ORB_PropFirm_V1" / "project.cfx"

print("="*60)
print("GENERADOR: NDXm_ORB_PropFirm_V1")
print("="*60)
print(f"Base project: Builder (NDXm_TICK_UTCPlus02 / M15)")
print(f"Template: NDXm_NY_Session_Template.sqx")
print(f"Output: {OUT_PROJECT}\n")

# Recolectar templates
templates = sorted(glob.glob(os.path.join(TPL_DIR, "*.sqx")))
if not templates:
    raise FileNotFoundError(f"No templates found in {TPL_DIR}")

print(f"Templates encontrados: {len(templates)}")
for t in templates:
    print(f"  - {Path(t).name}")
print()

# Construir tareas (1 template = 1 build task)
tasks = []
for template_path in templates:
    stem = Path(template_path).stem
    tasks.append({
        "template": template_path,
        "output_db": f"BS-{stem}",
    })

print(f"Tasks a generar: {len(tasks)}")
print()

# STEP 2: Generar (emit + self-verify)
print("STEP 2: Generando proyecto...")
report = make_project(
    str(BASE_PATH),
    "NDXm_ORB_PropFirm_V1",
    tasks,
    out_cfx=str(OUT_PROJECT)
)

print("Reporte de generacion:")
print(f"  Reporte completo: {report}")
print()

# STEP 3: Validar
# El reporte es exitoso si NO tiene errores (no necesariamente tiene "status" key)
has_error = 'error' in report
if not has_error and report.get('ok') != False:
    print("STEP 3: Validacion OK - proyecto estructuralmente correcto")
    print()

    # STEP 4: Deploy
    print("STEP 4: Desplegando en la instalacion...")
    deploy(
        out_cfx=str(OUT_PROJECT),
        install=INSTALL,
        project_name="NDXm_ORB_PropFirm_V1"
    )
    print()

    print("="*60)
    print("EXITO: Proyecto generado y desplegado")
    print("="*60)
    print(f"Ubicacion: {INSTALL}\\user\\projects\\NDXm_ORB_PropFirm_V1\\project.cfx")
    print()
    print("PROXIMO PASO:")
    print("  1. Abre SQX")
    print("  2. File > Open Project > NDXm_ORB_PropFirm_V1")
    print("  3. Build > Run (genera estrategias)")
    print("  4. Agrega Retest tasks manualmente desde UI")
    print("="*60)
else:
    print(f"ERROR: {report.get('error', 'unknown')}")
    sys.exit(1)
