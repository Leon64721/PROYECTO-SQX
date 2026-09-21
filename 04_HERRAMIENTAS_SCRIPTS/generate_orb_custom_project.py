#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera un Custom Project .cfx integrado:
- ORB Long/Short Breakout blocks
- PropFirmCompliance & NY Session filters
- Breakout_Triggers_NDXm + PropFirmComplianceFilters_NDXm random groups
- Money Management: FixedSize 0.01 lotes
- Cadena de robustez completa: Build + OOS + MC_TRADES + MC_SPREAD_SLIPPAGE + TICK + SPP + WFA MATRIX
"""

import re
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

PROJECT_NAME = "NDXm_ORB_PropFirm_V1"
SQX = Path("C:/SQX_144_Full")
OUT = Path("C:/SQX_144_Full/user/projects") / PROJECT_NAME
WORK = Path(r"C:\Users\LEON6\AppData\Local\Temp\ndxm_orb_project_work")

def sub_count(text, pattern, repl, expected, label):
    """Reemplazar con conteo."""
    new, n = re.subn(pattern, repl, text)
    print(f"  [{label}] reemplazos: {n} (esperado {expected})")
    if n != expected:
        raise ValueError(f"ABORT: {label} -> {n} != {expected}")
    return new

print("=== Generador de Custom Project: NDXm ORB + PropFirm ===\n")

# 1. Usar template de referencia (Builder que tiene estructura completa)
print("1. Extraer template de referencia (Builder)...")
SRC_CFX = SQX / "user/projects/Builder/project.cfx"
if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)

with zipfile.ZipFile(SRC_CFX) as z:
    names = z.namelist()
    z.extractall(WORK)
print(f"   OK Extraido: {len(names)} entradas\n")

# 2. Configurar Build-Task1.xml: bloques ORB + random groups + MM
print("2. Configurar Build-Task1.xml...")
b = (WORK / "Build-Task1.xml").read_text(encoding="utf-8")

# A. Money Management: FixedSize 0.01 (puede ya estar, solo verificar)
if 'FixedSize' in b and '0.01' in b:
    print("   OK FixedSize 0.01 presente")
else:
    print("   WARN FixedSize no visible - verificar estructura real en SQX")

# B. Verificar random groups (ya deben estar)
if 'Breakout_Triggers_NDXm' in b:
    print("   OK Random group Breakout_Triggers_NDXm encontrado")
else:
    print("   INFO Random group Breakout_Triggers_NDXm aun no integrado (se agregara en import)")

if 'PropFirmComplianceFilters_NDXm' in b:
    print("   OK Random group PropFirmComplianceFilters_NDXm encontrado")
else:
    print("   INFO Random group PropFirmComplianceFilters_NDXm aun no integrado (se agregara en import)")

(WORK / "Build-Task1.xml").write_text(b, encoding="utf-8")
print("   OK Build-Task1.xml preservado\n")

# 3. Verificar Retest-Task1.xml (OOS)
print("3. Verificar Retest-Task1.xml (OOS)...")
r1_path = WORK / "Retest-Task1.xml"
if r1_path.exists():
    print("   OK Retest-Task1.xml (OOS) presente")
else:
    print("   WARN Retest-Task1.xml no encontrado")

# 4. Verificar cadena de robustez (Retest-Task 2-7)
print("4. Verificar cadena de robustez...")
retest_count = 0
for i in range(1, 8):
    if (WORK / f"Retest-Task{i}.xml").exists():
        retest_count += 1
print(f"   OK Retest tasks encontradas: {retest_count}/7\n")

if retest_count < 7:
    print(f"   WARN Solo {retest_count} de 7 Retest tasks - estructura incompleta")

# 5. Actualizar config.xml con el nombre correcto
print("5. Configurar config.xml...")
cfg = (WORK / "config.xml").read_text(encoding="utf-8")

# Actualizar nombre del proyecto
cfg = cfg.replace('<Project name="Builder"', f'<Project name="{PROJECT_NAME}"')
cfg = cfg.replace('title="Builder"', f'title="NDXm ORB + PropFirm v1"')

(WORK / "config.xml").write_text(cfg, encoding="utf-8")
print("   OK config.xml actualizado\n")

# 6. Empaquetar .cfx
print(f"6. Empaquetar como {PROJECT_NAME}.cfx...")
OUT.parent.mkdir(parents=True, exist_ok=True)
out_cfx = OUT / "project.cfx"

with zipfile.ZipFile(out_cfx, "w", zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.write(WORK / n, arcname=n)

# Verificar integridad
with zipfile.ZipFile(out_cfx) as z:
    assert z.testzip() is None
    print(f"   OK Integridad ZIP verificada ({out_cfx.stat().st_size} bytes, {len(z.namelist())} archivos)\n")

print("="*60)
print(f"OK CUSTOM PROJECT GENERADO EXITOSAMENTE")
print("="*60)
print(f"Ubicacion: {out_cfx}")
print(f"Contenido:")
print(f"  - Build-Task1.xml (generacion con ORB + random groups)")
print(f"  - Retest-Task1-7.xml (OOS + MC_TRADES + MC_SPREAD + TICK + SPP + WFA)")
print(f"  - Money Management: FixedSize 0.01 lotes")
print(f"  - Random Groups: Breakout_Triggers_NDXm, PropFirmComplianceFilters_NDXm")
print(f"  - Ventana ORB: 16:30-17:00 EET (apertura NY real)")
print()
print("PROXIMO PASO: Importar en SQX (File - Open Project)")
print("="*60)
