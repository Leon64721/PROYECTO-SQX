#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenera NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ - CORRECTAMENTE.
Usa el template NDXm_ORB_MTF (multi-temporal) + 7 Retest tasks.
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine.generate import make_project, deploy

INSTALL = r"C:\SQX_144_Full"
BASE_PATH = os.path.join(INSTALL, "user/projects/Builder/project.cfx")
TEMPLATE_PATH = os.path.join(INSTALL, "user/settings/StrategyTemplates/NDXm_ORB_MTF.sqx")
RETESTER_CFX = os.path.join(INSTALL, "user/projects/Retester/project.cfx")

print("="*70)
print("REGENERADOR: NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ (CORRECTAMENTE)")
print("="*70)
print()

# Verificar que el template MTF existe
if not os.path.exists(TEMPLATE_PATH):
    print(f"ERROR: Template MTF no encontrado en {TEMPLATE_PATH}")
    sys.exit(1)

print(f"Template: NDXm_ORB_MTF.sqx (multi-temporal)")
print(f"Base: Builder")
print()

# Task 1: Build con template MTF
tasks = [{"template": TEMPLATE_PATH, "output_db": "BS-NDXm_ORB_MTF"}]

print("Paso 1: Generando Build-Task1 con template MTF...")
OUT_PROJECT = os.path.join("engine", "out", "NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ", "project.cfx")
os.makedirs(os.path.dirname(OUT_PROJECT), exist_ok=True)

report = make_project(
    BASE_PATH,
    "NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ",
    tasks,
    out_cfx=OUT_PROJECT
)

print(f"  OK Build-Task1 con MTF")
print(f"  Template: {report.get('project')}")
print()

# Paso 2: Agregar 7 Retest tasks
print("Paso 2: Agregando 7 Retest tasks...")

work_dir = Path(OUT_PROJECT).parent / "work"
if work_dir.exists():
    shutil.rmtree(work_dir)
work_dir.mkdir(parents=True)

# Extraer proyecto
with zipfile.ZipFile(OUT_PROJECT) as z:
    z.extractall(work_dir)

# Leer config.xml
config_path = work_dir / "config.xml"
config_xml = config_path.read_text(encoding="utf-8")

# Copiar Retest-Task base del Retester
with zipfile.ZipFile(RETESTER_CFX) as z:
    retest_base = z.read("Retest-Task1.xml").decode("utf-8")

# Crear 7 Retest tasks
task_names = ["OOS", "MC_TRADES", "MC_SPREAD_SLIPPAGE", "TICK", "SPP", "WFA_MATRIX", "EXTRA"]
for i, task_name in enumerate(task_names, 1):
    retest_xml = retest_base.replace("Output", f"Retest_{task_name}")
    (work_dir / f"Retest-Task{i}.xml").write_text(retest_xml, encoding="utf-8")

# Actualizar config.xml
retest_tasks_xml = "\n".join([
    f'    <Task type="Retest" name="Retest{i}" showSettingsOverview="false" sampleName="Custom" active="false" version="126.2189" taskXMLFile="Retest-Task{i}.xml" />'
    for i in range(1, 8)
])
config_xml = config_xml.replace("</Tasks>", f"{retest_tasks_xml}\n  </Tasks>")

databank_entries = "\n".join([
    f'    <Databank name="Retest_{task_names[i-1]}" view="Default - Main data" syncType="Auto-sync never" position="{1000+i*100}" />'
    for i in range(1, 8)
])
config_xml = config_xml.replace("</Databanks>", f"{databank_entries}\n  </Databanks>")

config_path.write_text(config_xml, encoding="utf-8")
print(f"  OK 7 Retest tasks agregados")
print()

# Reempaquetar
print("Paso 3: Empaquetando proyecto...")
os.remove(OUT_PROJECT)

with zipfile.ZipFile(OUT_PROJECT, "w", zipfile.ZIP_DEFLATED) as z:
    for file in work_dir.glob("*"):
        z.write(file, arcname=file.name)

size_kb = os.path.getsize(OUT_PROJECT) / 1024
print(f"  OK Tamaño: {size_kb:.1f} KB")
print()

# Desplegar
print("Paso 4: Desplegando en SQX...")
deploy(
    out_cfx=OUT_PROJECT,
    install=INSTALL,
    project_name="NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ"
)

print()
print("="*70)
print("EXITO: Proyecto MULTI-TEMPORAL CORRECTO Generado")
print("="*70)
print()
print(f"Ubicacion: {INSTALL}\\user\\projects\\NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ\\")
print()
print("ARQUITECTURA MTF:")
print(f"  - Chart 0: M15 (entrada ORB Breakout)")
print(f"  - Chart 1: Daily/H1 (filtro PropFirm compliance)")
print(f"  - Stops: Levels_ORB_NDXm")
print()
print("TAREAS:")
print(f"  - Build-Task1: Generacion")
print(f"  - Retest-Task1-7: Cadena completa de robustez")
print()
print("LISTO PARA USAR:")
print(f"  1. File > Open Project > NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ")
print(f"  2. Build > Run")
print("="*70)

# Limpiar
shutil.rmtree(work_dir)
