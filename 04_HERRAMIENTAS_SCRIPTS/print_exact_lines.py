import glob
import re

db_names = [
    'MONTECARLO RNADOMIZE TRADES Y SKIP TRADES',
    'MONTECARLO SLIPPAGE Y SPREAD',
    'GESTION MONETARIA',
    'GESTION MONETARIA - DESACTIVADA',
    'MC_TRADES',
    'MC_SPREAD_SLIPPAGE',
    'OOS',
    'TICK',
    'SPP',
    'WFA MATRIX'
]

print("Printing exact lines containing the databank names:")
for fn in sorted(glob.glob('temp_cfx/*.xml')):
    if 'config' in fn:
        continue
    with open(fn, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    found = False
    for i, line in enumerate(lines):
        for name in db_names:
            if name in line:
                if not found:
                    print(f"\n=== {fn} ===")
                    found = True
                print(f"  Line {i+1}: {line.strip()}")
