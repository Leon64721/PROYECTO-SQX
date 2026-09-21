import os
import re
import zipfile

# Configuration for ORB_MTF_Project
temp_dir = "E:\\PROYECTOS\\CLAUDE CODE\\STRATEGY QUANT\\temp_orb_cfx"
output_cfx = "E:\\PROYECTOS\\CLAUDE CODE\\STRATEGY QUANT\\ORB_MTF_Project.cfx"

pipeline = {
    "Retest-Task1.xml": {"in": "Results", "out": "OOS"},
    "Retest-Task6.xml": {"in": "OOS", "out": "GESTION MONETARIA - DESACTIVADA"},
    "Retest-Task2.xml": {"in": "GESTION MONETARIA - DESACTIVADA", "out": "MC_TRADES"},
    "Retest-Task3.xml": {"in": "MC_TRADES", "out": "MC_SPREAD_SLIPPAGE"},
    "Retest-Task5.xml": {"in": "MC_SPREAD_SLIPPAGE", "out": "TICK"},
    "Retest-Task4.xml": {"in": "TICK", "out": "SPP"},
    "Retest-Task7.xml": {"in": "SPP", "out": "WFA MATRIX"}
}

def patch_file(filename, in_db, out_db):
    filepath = os.path.join(temp_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_databanks = f"""<Databanks retestSelected="false">
    <Databank label="Output databank" name="Output" value="{out_db}" />
    <Databank label="Input databank" name="Input" value="{in_db}" />
  </Databanks>
  """
    
    # Regex to match all existing <Databanks>...</Databanks> between <Notes> and <SelectedStrategies> or <WhatToBuild>
    pattern = r'(</Notes>\s*)(?:<Databanks[\s\S]*?</Databanks>\s*)+(<(?:SelectedStrategies|WhatToBuild))'
    
    # Test if pattern matches
    if not re.search(pattern, content):
        print(f"Could not find Databanks section to replace strictly in {filename}, falling back...")
        # Fallback approach: just replace the first cluster of <Databanks>
        pattern_broad = r'(<Databanks[\s\S]*?</Databanks>\s*)+'
        content = re.sub(pattern_broad, new_databanks, content, count=1)
    else:
        content = re.sub(pattern, r'\1' + new_databanks + r'\2', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Patched {filename} -> In: {in_db} | Out: {out_db}")
    return True

# 1. Patch files
print("Patching XML files...")
all_success = True
for file, dbs in pipeline.items():
    if not patch_file(file, dbs["in"], dbs["out"]):
        all_success = False

if not all_success:
    print("Failed to patch some files. Aborting zip.")
    exit(1)

# 2. Pack files back into .cfx
print(f"Packing into {output_cfx}...")
with zipfile.ZipFile(output_cfx, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, temp_dir)
            zipf.write(file_path, arcname)
print("Done!")
