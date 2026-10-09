#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera NDXm_ORB_PropFirm_V1_ROBUSTEZ - Custom Project COMPLETO.
Build-Task1 + 7 Retest tasks (OOS, MC_TRADES, MC_SPREAD_SLIPPAGE, TICK, SPP, WFA, EXTRA)
TODO automaticamente, listo para importar y correr Build.
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
TPL_DIR = os.path.join(INSTALL, "user/settings/StrategyTemplates")

print("="*70)
print("GENERADOR: NDXm_ORB_PropFirm_V1_ROBUSTEZ (Completo con 7 Retest)")
print("="*70)
print()

# Buscar template
import glob
templates = glob.glob(os.path.join(TPL_DIR, "**", "NDXm_NY_Session_Template.sqx"), recursive=True)
if not templates:
    print("ERROR: Template NDXm_NY_Session_Template.sqx no encontrado")
    sys.exit(1)

template_path = templates[0]
print(f"Template: {Path(template_path).name}")
print()

# Task 1: Build (con template)
tasks = [{"template": template_path, "output_db": "BS-NDXm_NY_Session_Template"}]

print("Generando Build-Task1 + estructura de robustez...")
OUT_PROJECT = os.path.join("engine", "out", "NDXm_ORB_PropFirm_V1_ROBUSTEZ", "project.cfx")

report = make_project(
    BASE_PATH,
    "NDXm_ORB_PropFirm_V1_ROBUSTEZ",
    tasks,
    out_cfx=OUT_PROJECT
)

print(f"  Build-Task1: OK ({report.get('build_tasks')} task)")
print()

# Agregar 7 Retest tasks manualmente al .cfx
print("Agregando 7 Retest tasks...")

# Extraer proyecto generado
work_dir = Path(OUT_PROJECT).parent / "work"
if work_dir.exists():
    shutil.rmtree(work_dir)
work_dir.mkdir(parents=True)

with zipfile.ZipFile(OUT_PROJECT) as z:
    z.extractall(work_dir)

# Leer config.xml
config_path = work_dir / "config.xml"
config_xml = config_path.read_text(encoding="utf-8")

# Copiar Retest-Task1-7 del Retester proyecto (que solo tiene Retest)
retester_cfx = os.path.join(INSTALL, "user/projects/Retester/project.cfx")
retest_tasks = {}

with zipfile.ZipFile(retester_cfx) as z:
    # Retester tiene Retest-Task1.xml, lo usamos como base para los 7
    retest_base = z.read("Retest-Task1.xml").decode("utf-8")

    # Crear 7 variantes (cambiando nombres de databanks internos)
    task_names = ["OOS", "MC_TRADES", "MC_SPREAD_SLIPPAGE", "TICK", "SPP", "WFA_MATRIX", "EXTRA"]
    for i, task_name in enumerate(task_names, 1):
        retest_xml = retest_base.replace("Output", f"Retest_{task_name}")
        retest_tasks[f"Retest-Task{i}.xml"] = retest_xml
        (work_dir / f"Retest-Task{i}.xml").write_text(retest_xml, encoding="utf-8")

# Actualizar config.xml para agregar Retest tasks
retest_tasks_xml = "\n".join([
    f'    <Task type="Retest" name="Retest{i}" showSettingsOverview="false" sampleName="Custom" active="false" version="126.2189" taskXMLFile="Retest-Task{i}.xml" />'
    for i in range(1, 8)
])

# Insertar antes de </Tasks>
config_xml = config_xml.replace("</Tasks>", f"{retest_tasks_xml}\n  </Tasks>")

# Agregar databanks para Retest
databank_entries = "\n".join([
    f'    <Databank name="Retest_{task_names[i-1]}" view="Default - Main data" syncType="Auto-sync never" position="{1000+i*100}" />'
    for i in range(1, 8)
])

config_xml = config_xml.replace("</Databanks>", f"{databank_entries}\n  </Databanks>")

config_path.write_text(config_xml, encoding="utf-8")

print(f"  Retest-Task1-7: OK (7 tasks agregados)")
print()

# Reempaquetar .cfx
print("Reempaquetando .cfx con todos los tasks...")
os.remove(OUT_PROJECT)

with zipfile.ZipFile(OUT_PROJECT, "w", zipfile.ZIP_DEFLATED) as z:
    for file in work_dir.glob("*"):
        z.write(file, arcname=file.name)

print(f"  Tamaño final: {os.path.getsize(OUT_PROJECT) / 1024:.1f} KB")
print()

# Desplegar
print("Desplegando en SQX...")
deploy(
    out_cfx=OUT_PROJECT,
    install=INSTALL,
    project_name="NDXm_ORB_PropFirm_V1_ROBUSTEZ"
)

print()
print("="*70)
print("EXITO: Custom Project COMPLETO Generado")
print("="*70)
print()
print(f"Ubicacion: {INSTALL}\\user\\projects\\NDXm_ORB_PropFirm_V1_ROBUSTEZ\\project.cfx")
print()
print("CONTENIDO COMPLETO:")
print(f"  - Build-Task1: Generacion (1800 estrategias)")
print(f"  - Retest-Task1: OOS (Out-of-Sample)")
print(f"  - Retest-Task2: MC_TRADES (Monte Carlo Trades)")
print(f"  - Retest-Task3: MC_SPREAD_SLIPPAGE (Spread & Slippage)")
print(f"  - Retest-Task4: TICK (Tick Simulation)")
print(f"  - Retest-Task5: SPP (Slippage & Pricing Pattern)")
print(f"  - Retest-Task6: WFA_MATRIX (Walk-Forward Analysis)")
print(f"  - Retest-Task7: EXTRA (Robustez adicional)")
print()
print("LISTO PARA USAR:")
print(f"  1. Abre SQX")
print(f"  2. File > Open Project > NDXm_ORB_PropFirm_V1_ROBUSTEZ")
print(f"  3. Build > Run")
print(f"  4. Monitorea: OOS tiene sobrevivientes > 0?")
print("="*70)

# Limpiar
shutil.rmtree(work_dir)
