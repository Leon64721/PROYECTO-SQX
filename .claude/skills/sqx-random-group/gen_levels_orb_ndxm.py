#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera Levels_ORB_NDXm Value group.
Usa átomos inline para crear un pool de niveles ORB:
- Highest[1]: máximo del bar anterior
- Lowest[1]: mínimo del bar anterior
- HighD: High de ayer (prior day high)
- LowD: Low de ayer (prior day low)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine.groups import load_catalog, inline_item, make_group, wrap_groups

# Step 3: Key check contra catálogo
print("=== LEVELS_ORB_NDXM Value Group ===\n")
print("Step 3: Verificando átomos en catálogo...")
meta, T, B = load_catalog("catalog.json")

# Verificar que los átomos existen
required_atoms = ["Highest", "Lowest", "HighD", "LowD"]
for atom in required_atoms:
    if atom not in T:
        raise ValueError(f"Átomo {atom} no encontrado en catálogo")
    print(f"  OK {atom}: {T[atom].get('rule', 'value atom')}")

print()

# Step 4: Generar Value group con inline items
print("Step 4: Generando Value group...")
levels_orb = make_group(
    "Levels_ORB_NDXm",
    "Value",
    [
        inline_item(T["Highest"]),  # Highest[1] = máximo del bar anterior
        inline_item(T["Lowest"]),   # Lowest[1] = mínimo del bar anterior
        inline_item(T["HighD"]),    # Prior day high
        inline_item(T["LowD"]),     # Prior day low
    ],
    category="ORB_Levels"
)

xml_content = wrap_groups([levels_orb])
out_file = os.path.join("engine", "out", "Levels_ORB_NDXm.xml")
os.makedirs(os.path.dirname(out_file), exist_ok=True)

with open(out_file, "w", encoding="utf-8") as f:
    f.write(xml_content)

print(f"  Emitido: {out_file}")
print()

# Step 5: Validar
print("Step 5: Validando...")
os.system(f'python engine/validate.py "{out_file}"')

print()
print("="*60)
print("LEVELS_ORB_NDXM Value Group Generado")
print("="*60)
print(f"Ubicacion: {out_file}")
print(f"Contenido:")
print(f"  - Highest (máximo bar anterior)")
print(f"  - Lowest (mínimo bar anterior)")
print(f"  - HighD (prior day high)")
print(f"  - LowD (prior day low)")
print()
print("Proximo paso: importar en AlgoWizard")
print("  Random > Block groups > Import > {out_file}")
print("="*60)
