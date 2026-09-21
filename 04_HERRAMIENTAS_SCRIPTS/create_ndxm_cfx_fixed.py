#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crea Custom Project .cfx con estructura SQX correcta.
Basado en la estructura real de Builder (config.xml con Tasks/Resources/Databanks).
"""

import zipfile
from pathlib import Path
import shutil

PROJECT_NAME = "NDXm_ORB_PropFirm_V1"
SQX = Path("C:/SQX_144_Full")
OUT_DIR = SQX / "user/projects" / PROJECT_NAME
TEMP_DIR = Path(r"C:\Users\LEON6\AppData\Local\Temp\ndxm_cfx_temp2")

# Limpiar y crear directorio temporal
if TEMP_DIR.exists():
    shutil.rmtree(TEMP_DIR)
TEMP_DIR.mkdir(parents=True)

print(f"=== Creador de Custom Project: {PROJECT_NAME} (FIXED) ===\n")

# 1. config.xml con estructura SQX correcta
print("1. Generando config.xml con estructura SQX...")
config_xml = '''<Project name="NDXm_ORB_PropFirm_V1" version="144.2938">
  <Tasks>
    <Task type="Build" name="Build" showSettingsOverview="false" sampleName="Custom" active="true" version="126.2189" taskXMLFile="Build-Task1.xml" />
  </Tasks>
  <Resources>
    <Symbols />
    <Sessions />
    <CustomIndicators />
    <CustomBlocks />
  </Resources>
  <Databanks>
    <Databank name="Results" view="Default - Main data" syncType="Auto-sync every 1 hour" position="0" />
    <Databank name="Initial population" view="Default - Main data" syncType="Auto-sync never" position="1" />
    <Databank name="Last generation" view="Default - Main data" syncType="Auto-sync never" position="2" />
    <Databank name="Strategies to improve" view="Default - Main data" syncType="Auto-sync never" position="3" />
    <Databank name="Existing portfolio" view="Default" syncType="Auto-sync never" />
  </Databanks>
</Project>
'''
(TEMP_DIR / "config.xml").write_text(config_xml, encoding="utf-8")
print("   OK config.xml con estructura SQX")

# 2. Copiar Build-Task1.xml del Builder
print("2. Importando Build-Task1.xml del Builder...")
builder_cfx = SQX / "user/projects/Builder/project.cfx"
with zipfile.ZipFile(builder_cfx) as z:
    build_task_xml = z.read("Build-Task1.xml")
(TEMP_DIR / "Build-Task1.xml").write_bytes(build_task_xml)
print("   OK Build-Task1.xml importado")

# 3. Empaquetar como .cfx
print("3. Empaquetando como .cfx...")
if OUT_DIR.exists():
    shutil.rmtree(OUT_DIR)
OUT_DIR.mkdir(parents=True)
out_cfx = OUT_DIR / "project.cfx"

with zipfile.ZipFile(out_cfx, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(TEMP_DIR / "config.xml", arcname="config.xml")
    z.write(TEMP_DIR / "Build-Task1.xml", arcname="Build-Task1.xml")

# Verificar
with zipfile.ZipFile(out_cfx) as z:
    assert z.testzip() is None
    size_kb = out_cfx.stat().st_size / 1024
    print(f"   OK Integridad OK ({size_kb:.1f} KB, {len(z.namelist())} archivos)\n")

print("="*60)
print(f"PROYECTO REGENERADO: {PROJECT_NAME}")
print("="*60)
print(f"Ubicacion: {out_cfx}")
print(f"Estado: LISTO PARA IMPORTAR EN SQX")
print(f"\nProximos pasos:")
print(f"  1. Abre en SQX: File > Open Project > {PROJECT_NAME}")
print(f"  2. Ejecuta Build: Build > Run")
print(f"  3. Agrega Retest tasks desde UI")
print("="*60)

# Limpiar
shutil.rmtree(TEMP_DIR)
