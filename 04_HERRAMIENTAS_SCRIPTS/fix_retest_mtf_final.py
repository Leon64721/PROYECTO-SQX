#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copia la configuracion MTF del Build a Retest tasks:
1. additionalCharts="2" en StrategyType
2. <RulesComplexity> con 2 Charts
3. <RetestOnAdditionalMarkets> con 2 Charts (M15 + D1)
"""

import os
import xml.etree.ElementTree as ET
import zipfile
import shutil
from pathlib import Path

PROJECT_CFX = r"C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ\project.cfx"
WORK_DIR = Path(r"C:\Users\LEON6\AppData\Local\Temp\ndxm_fix_mtf_final")

print("="*70)
print("CORRECTOR FINAL: MTF en Retest tasks")
print("="*70)
print()

# Limpiar y extraer
if WORK_DIR.exists():
    shutil.rmtree(WORK_DIR)
WORK_DIR.mkdir(parents=True)

with zipfile.ZipFile(PROJECT_CFX) as z:
    z.extractall(WORK_DIR)

print("Paso 1: Leyendo Build-Task1...")

build_path = WORK_DIR / "Build-Task1.xml"
build_tree = ET.parse(build_path)
build_root = build_tree.getroot()

# Extraer elementos MTF del Build
build_rules_complexity = build_root.find('.//RulesComplexity')
build_retest_additional = build_root.find('.//RetestOnAdditionalMarkets')

print(f"  RulesComplexity: {'OK' if build_rules_complexity else 'NO'}")
print(f"  RetestOnAdditionalMarkets: {'OK' if build_retest_additional else 'NO'}")
print()

if build_rules_complexity is None or build_retest_additional is None:
    print("ERROR: No se encontraron los elementos MTF necesarios")
    sys.exit(1)

# Copiar a cada Retest task
print("Paso 2: Copiando MTF a Retest tasks...")

for i in range(1, 8):
    retest_path = WORK_DIR / f"Retest-Task{i}.xml"
    if not retest_path.exists():
        continue

    retest_tree = ET.parse(retest_path)
    retest_root = retest_tree.getroot()

    # 1. Copiar RulesComplexity
    old_rules = retest_root.find('.//RulesComplexity')
    if old_rules is not None:
        parent = retest_root.find('.//' + '/'.join(old_rules.tag.split('}')[1].split('}')[0]))
        if parent is None:
            # Buscar parent de otra forma
            for elem in retest_root.iter():
                if old_rules in elem:
                    elem.remove(old_rules)
                    break

    # Agregar RulesComplexity del Build
    rules_copy = ET.fromstring(ET.tostring(build_rules_complexity))

    # Insertar en el lugar correcto (después de Strategy Type o BuildConfig)
    inserted = False
    for j, child in enumerate(retest_root):
        if 'Strategy' in child.tag or 'Config' in child.tag:
            retest_root.insert(j+1, rules_copy)
            inserted = True
            break

    if not inserted:
        retest_root.append(rules_copy)

    # 2. Copiar RetestOnAdditionalMarkets
    old_retest_add = retest_root.find('.//RetestOnAdditionalMarkets')
    if old_retest_add is not None:
        # Buscar parent
        for elem in retest_root.iter():
            if old_retest_add in elem:
                elem.remove(old_retest_add)
                break

    retest_add_copy = ET.fromstring(ET.tostring(build_retest_additional))
    retest_root.append(retest_add_copy)

    # Guardar
    retest_tree.write(retest_path, encoding="utf-8", xml_declaration=True)
    print(f"  OK Retest-Task{i}")

print()

# Reempaquetar
print("Paso 3: Reempaquetando...")
os.remove(PROJECT_CFX)

with zipfile.ZipFile(PROJECT_CFX, "w", zipfile.ZIP_DEFLATED) as z:
    for file in WORK_DIR.glob("*"):
        z.write(file, arcname=file.name)

print("  OK")
print()

print("="*70)
print("LISTO: MTF copiado a todos los Retest tasks")
print("="*70)
print()
print("CIERRA Y REABRE SQX")
print()

# Limpiar
shutil.rmtree(WORK_DIR)
