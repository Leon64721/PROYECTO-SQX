#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copia la seccion <Subcharts> del Build a cada Retest task.
Esto es lo que faltaba para la multitemporalidad en Retest.
"""

import os
import xml.etree.ElementTree as ET
import zipfile
import shutil
from pathlib import Path

PROJECT_CFX = r"C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ\project.cfx"
WORK_DIR = Path(r"C:\Users\LEON6\AppData\Local\Temp\ndxm_fix_subcharts")

print("="*70)
print("CORRECTOR: Copiar Subcharts a Retest tasks")
print("="*70)
print()

# Limpiar y extraer
if WORK_DIR.exists():
    shutil.rmtree(WORK_DIR)
WORK_DIR.mkdir(parents=True)

with zipfile.ZipFile(PROJECT_CFX) as z:
    z.extractall(WORK_DIR)

print("Paso 1: Extrayendo <Subcharts> del Build-Task1...")

# Parsear Build-Task1
ET.register_namespace('', 'http://www.strategyquant.com')
build_path = WORK_DIR / "Build-Task1.xml"
build_tree = ET.parse(build_path)
build_root = build_tree.getroot()

# Namespace
ns = {'': 'http://www.strategyquant.com'}

# Buscar Subcharts en Build (puede estar en diferentes niveles)
build_subcharts = None
for subcharts in build_root.iter():
    if 'Subcharts' in str(subcharts.tag):
        build_subcharts = subcharts
        break

if build_subcharts is None:
    print("  Buscando en BuildConfig...")
    for elem in build_root.iter():
        if 'BuildConfig' in str(elem.tag):
            build_subcharts = elem.find('.//Subcharts', ns) or elem.find('.//Subcharts')
            if build_subcharts is not None:
                break

if build_subcharts is None:
    print("  WARN: <Subcharts> no encontrado en Build")
else:
    print(f"  OK <Subcharts> encontrado: {ET.tostring(build_subcharts, encoding='unicode')[:100]}...")

    # Copiar a cada Retest task
    print()
    print("Paso 2: Copiando <Subcharts> a cada Retest task...")

    for i in range(1, 8):
        retest_path = WORK_DIR / f"Retest-Task{i}.xml"
        if not retest_path.exists():
            continue

        retest_tree = ET.parse(retest_path)
        retest_root = retest_tree.getroot()

        # Buscar donde poner Subcharts (en RetestConfig)
        retest_config = None
        for elem in retest_root.iter():
            if 'RetestConfig' in str(elem.tag) or 'Config' in str(elem.tag):
                retest_config = elem
                break

        if retest_config is None:
            print(f"  WARN Retest-Task{i}: no encontrado Config, saltando")
            continue

        # Remover Subcharts viejos si existen
        for old_sub in retest_config.findall('.//Subcharts'):
            retest_config.remove(old_sub)

        # Copiar Subcharts
        subcharts_copy = ET.fromstring(ET.tostring(build_subcharts))
        retest_config.append(subcharts_copy)

        retest_tree.write(retest_path, encoding="utf-8", xml_declaration=True)
        print(f"  OK Retest-Task{i} - <Subcharts> copiado")

print()

# Reempaquetar
print("Paso 3: Reempaquetando proyecto...")
os.remove(PROJECT_CFX)

with zipfile.ZipFile(PROJECT_CFX, "w", zipfile.ZIP_DEFLATED) as z:
    for file in WORK_DIR.glob("*"):
        z.write(file, arcname=file.name)

print(f"  OK Proyecto actualizado")
print()

print("="*70)
print("LISTO: Todos los Retest tasks tienen Subcharts")
print("="*70)
print()
print("PROXIMO:")
print("  1. Cierra SQX")
print("  2. Reabre NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ")
print("  3. Build > Run (ya debería tener MTF en todas partes)")
print()

# Limpiar
shutil.rmtree(WORK_DIR)
