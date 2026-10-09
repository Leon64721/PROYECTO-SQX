#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige los Retest tasks para que HEREDEN la configuracion MTF del Build.
Copia la estructura de Data (2 charts) del Build-Task1 a cada Retest task.
"""

import os
import xml.etree.ElementTree as ET
import zipfile
import shutil
from pathlib import Path

PROJECT_CFX = r"C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ\project.cfx"
WORK_DIR = Path(r"C:\Users\LEON6\AppData\Local\Temp\ndxm_fix_mtf")

print("="*70)
print("CORRECTOR: Retest tasks con MTF")
print("="*70)
print()

# Limpiar y extraer
if WORK_DIR.exists():
    shutil.rmtree(WORK_DIR)
WORK_DIR.mkdir(parents=True)

with zipfile.ZipFile(PROJECT_CFX) as z:
    z.extractall(WORK_DIR)

print("Paso 1: Leyendo configuracion MTF del Build-Task1...")

# Parsear Build-Task1 para obtener la estructura de Data
build_path = WORK_DIR / "Build-Task1.xml"
build_tree = ET.parse(build_path)
build_root = build_tree.getroot()

# Encontrar elemento <Data> en Build
build_data = build_root.find(".//Data")
if build_data is None:
    print("ERROR: No se encontro <Data> en Build-Task1")
    sys.exit(1)

print("  OK Build-Task1 tiene estructura MTF")
print(f"  Numero de <Chart>: {len(build_data.findall('Charts/Chart'))}")
print()

# Copiar la estructura Data a cada Retest task
print("Paso 2: Copiando estructura MTF a Retest tasks...")

for i in range(1, 8):
    retest_path = WORK_DIR / f"Retest-Task{i}.xml"
    if not retest_path.exists():
        print(f"  WARN Retest-Task{i}.xml no encontrado, saltando")
        continue

    retest_tree = ET.parse(retest_path)
    retest_root = retest_tree.getroot()

    # Encontrar o crear elemento <Data> en Retest
    retest_data = retest_root.find(".//Data")
    if retest_data is None:
        print(f"  WARN Retest-Task{i} sin <Data>, saltando")
        continue

    # Copiar la estructura de Charts del Build al Retest
    # Primero, remover los Charts viejos
    charts_elem = retest_data.find("Charts")
    if charts_elem is not None:
        retest_data.remove(charts_elem)

    # Copiar Charts desde Build
    build_charts = build_data.find("Charts")
    if build_charts is not None:
        # Deep copy de Charts
        charts_copy = ET.fromstring(ET.tostring(build_charts))
        retest_data.append(charts_copy)
        print(f"  OK Retest-Task{i} - MTF heredado")

    # Guardar
    retest_tree.write(retest_path, encoding="utf-8", xml_declaration=True)

print()

# Reempaquetar
print("Paso 3: Reempaquetando proyecto...")

# Backup del original
import shutil
backup = PROJECT_CFX + ".backup"
shutil.copy2(PROJECT_CFX, backup)
print(f"  Backup creado: {backup}")

# Crear nuevo .cfx
os.remove(PROJECT_CFX)
with zipfile.ZipFile(PROJECT_CFX, "w", zipfile.ZIP_DEFLATED) as z:
    for file in WORK_DIR.glob("*"):
        z.write(file, arcname=file.name)

print(f"  OK Proyecto actualizado")
print()

print("="*70)
print("LISTO: Retest tasks ahora tienen MTF")
print("="*70)
print()
print("PROXIMO PASO:")
print(f"  1. Cierra SQX completamente")
print(f"  2. Reabre el proyecto NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ")
print(f"  3. Verifica que TODOS los Retest tasks muestren 2 charts en Data")
print(f"  4. Build > Run")
print()

# Limpiar
shutil.rmtree(WORK_DIR)
