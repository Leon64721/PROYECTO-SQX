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

print("Searching for databank name occurrences across files...")
for fn in sorted(glob.glob('temp_cfx/*.xml')):
    with open(fn, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    found = []
    for name in db_names:
        count = len(re.findall(re.escape(name), content))
        if count > 0:
            found.append(f"'{name}': {count} times")
    if found:
        print(f"{fn}:")
        for item in found:
            print(f"  {item}")
