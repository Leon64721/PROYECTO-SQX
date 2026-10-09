#!/usr/bin/env python3
import json
from pathlib import Path
from engine.groups import (load_catalog, make_group, number, hybrid_ref, wrap_groups)

# Cargar catalog
try:
    _, T, B = load_catalog("catalog.json")
    print("✓ Catalog loaded")
except Exception as e:
    print(f"✗ Error loading catalog: {e}")
    exit(1)

# Crear Random Group VALUE para niveles ORB
# Estos son los niveles de precio que el algoritmo genético puede usar como stops/limits
items_inline = []

# Intentar usar inline atoms si existen
inline_keys = ["Highest", "Lowest", "PriorDayHigh", "PriorDayLow"]

# Si no existen, usar hybrid blocks de niveles de precio si están disponibles
price_blocks = [k for k in B.keys() if "Level" in k or "High" in k or "Low" in k]
print(f"Available price blocks: {price_blocks[:5]}...")

# Crear grupo con número fijo para evaluar
levels = make_group(
    "Levels_ORB_NDXm",
    "Value",
    [
        number("100"),  # Placeholder: el genetic algorithm reemplazará esto
    ],
    category="ORB Levels"
)

xml = wrap_groups([levels])

# Escribir output
out_path = Path("out") / "Levels_ORB_NDXm.xml"
out_path.parent.mkdir(parents=True, exist_ok=True)

with open(out_path, "w") as f:
    f.write(xml)

print(f"✓ Generated: {out_path}")
