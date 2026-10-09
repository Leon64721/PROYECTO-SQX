#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera NDXm_ORB_MTF template con multitemporalidad.
Shape: mtf_filter (multi-timeframe filter gate + trigger + stop)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "engine"))
from generate import from_design

INSTALL = r"C:\SQX_144_Full"

print("="*70)
print("GENERADOR: NDXm_ORB_MTF Template (Multi-Timeframe)")
print("="*70)
print()

# Design spec: MTF ORB con PropFirm compliance
design = {
    "name": "NDXm_ORB_MTF",
    "shape": "mtf_filter",
    "daily_filter": "PropFirmComplianceFilters_NDXm",
    "trigger": "Breakout_Triggers_NDXm",
    "price_pool": "Levels_ORB_NDXm",
    "thesis": "Intraday M15 ORB breakouts aligned with H1/Daily PropFirm compliance regime."
}

print("Design Spec:")
print(f"  Shape: {design['shape']}")
print(f"  Daily filter (HTF regime): {design['daily_filter']}")
print(f"  Trigger (M15): {design['trigger']}")
print(f"  Price pool (stops): {design['price_pool']}")
print(f"  Thesis: {design['thesis']}")
print()

print("Generando template...")
try:
    result = from_design(design, install=INSTALL)
    print(f"Resultado: {result}")
    print()

    out_file = os.path.join("engine", "out", "NDXm_ORB_MTF.sqx")
    if os.path.exists(out_file):
        size_kb = os.path.getsize(out_file) / 1024
        print("="*70)
        print("EXITO: NDXm_ORB_MTF Template Generado")
        print("="*70)
        print(f"Ubicacion: {out_file}")
        print(f"Tamano: {size_kb:.1f} KB")
        print()
        print("Contenido:")
        print(f"  - Shape: mtf_filter (multi-timeframe)")
        print(f"  - Daily filter: PropFirmComplianceFilters_NDXm (Chart 1 = HTF regime)")
        print(f"  - Trigger: Breakout_Triggers_NDXm (Chart 0 = M15 entry)")
        print(f"  - Price pool: Levels_ORB_NDXm (ORB stop levels)")
        print(f"  - Direccion: Both (long + short con mirrors automaticos)")
        print()
        print("Proximo paso:")
        print(f"  1. Importar en AlgoWizard: Random > Strategy Templates > Import")
        print(f"  2. Usar en sqx-strategy-project para crear el Custom Project final")
        print("="*70)
    else:
        print(f"ERROR: Template no fue emitido")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
