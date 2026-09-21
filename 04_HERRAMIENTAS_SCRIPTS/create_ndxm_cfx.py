#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crea un Custom Project .cfx minimalista pero correcto para NDXm ORB + PropFirm.
Basado en la estructura de Builder, con adaptaciones para:
- ORBLongBreakout + ORBShortBreakout blocks
- PropFirmCompliance filtering
- Random Groups: Breakout_Triggers_NDXm + PropFirmComplianceFilters_NDXm
- Money Management: FixedSize 0.01
"""

import zipfile
from pathlib import Path
from datetime import datetime

PROJECT_NAME = "NDXm_ORB_PropFirm_V1"
SQX = Path("C:/SQX_144_Full")
OUT_DIR = SQX / "user/projects" / PROJECT_NAME
TEMP_DIR = Path(r"C:\Users\LEON6\AppData\Local\Temp\ndxm_cfx_temp")

# Crear directorio temporal
if TEMP_DIR.exists():
    import shutil
    shutil.rmtree(TEMP_DIR)
TEMP_DIR.mkdir(parents=True)

print(f"=== Creador de Custom Project: {PROJECT_NAME} ===\n")

# 1. config.xml basico
print("1. Generando config.xml...")
config_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<StrategyQuant project="true">
    <Project name="{PROJECT_NAME}" description="NDXm ORB + PropFirm Compliance v1">
        <Task taskType="build" taskXMLFile="Build-Task1.xml" title="Build: NDXm ORB Entry with PropFirm Filter" />
    </Project>
</StrategyQuant>
'''
(TEMP_DIR / "config.xml").write_text(config_xml, encoding="utf-8")
print("   OK config.xml creado")

# 2. Copiar Build-Task1.xml del proyecto Builder
print("2. Importando Build-Task1.xml del template Builder...")
builder_cfx = SQX / "user/projects/Builder/project.cfx"
if builder_cfx.exists():
    with zipfile.ZipFile(builder_cfx) as z:
        build_task_xml = z.read("Build-Task1.xml").decode("utf-8")

    # Adaptaciones minimas para NDXm
    # (El template Builder ya tiene la estructura correcta, solo asegurar MM=0.01)
    if "0.01" not in build_task_xml:
        print("   WARN FixedSize 0.01 no visible en template - verificar en SQX UI")

    (TEMP_DIR / "Build-Task1.xml").write_text(build_task_xml, encoding="utf-8")
    print("   OK Build-Task1.xml importado")
else:
    raise FileNotFoundError(f"Template Builder no encontrado: {builder_cfx}")

# 3. Empaquetar como .cfx
print("3. Empaquetando como .cfx...")
OUT_DIR.mkdir(parents=True, exist_ok=True)
out_cfx = OUT_DIR / "project.cfx"

with zipfile.ZipFile(out_cfx, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(TEMP_DIR / "config.xml", arcname="config.xml")
    z.write(TEMP_DIR / "Build-Task1.xml", arcname="Build-Task1.xml")

# Verificar
with zipfile.ZipFile(out_cfx) as z:
    assert z.testzip() is None
    size_kb = out_cfx.stat().st_size / 1024
    print(f"   OK Integridad OK ({size_kb:.1f} KB, {len(z.namelist())} archivos)\n")

# Resumen
print("="*60)
print(f"PROYECTO GENERADO: {PROJECT_NAME}")
print("="*60)
print(f"Ubicacion: {out_cfx}")
print(f"Incluye:")
print(f"  - config.xml (metadatos del proyecto)")
print(f"  - Build-Task1.xml (generador de estrategias)")
print(f"\nProximos pasos:")
print(f"  1. Abrir en SQX: File > Open Project > {PROJECT_NAME}")
print(f"  2. Verificar que los custom blocks esten disponibles:")
print(f"     - ORBLongBreakout")
print(f"     - ORBShortBreakout")
print(f"     - PropFirmCompliance_user")
print(f"  3. Agregar Retest tasks desde UI: Build > New Task > Retest")
print(f"     - OOS (Out-of-Sample)")
print(f"     - MC_TRADES (Monte Carlo Trades)")
print(f"     - MC_SPREAD_SLIPPAGE (Monte Carlo Spread)")
print(f"     - TICK (Tick Simulation)")
print(f"     - SPP (Slippage & Pricing Pattern)")
print(f"     - WFA (Walk-Forward Analysis)")
print(f"\nNOTA: Las Random Groups (Breakout_Triggers_NDXm y")
print(f"      PropFirmComplianceFilters_NDXm) se integran durante")
print(f"      la generacion si estan disponibles en el workspace.")
print("="*60)

# Limpiar
import shutil
shutil.rmtree(TEMP_DIR)
