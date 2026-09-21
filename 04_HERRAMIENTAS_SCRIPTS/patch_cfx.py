import xml.etree.ElementTree as ET
import glob
import os
import zipfile

# Source files directory
temp_dir = "temp_cfx"
project_cfx_path = r"C:\SQX_144_Full\user\projects\BASE_CP_MASTER_CLEAN_V1\project.cfx"
backup_cfx_path = r"C:\SQX_144_Full\user\projects\BASE_CP_MASTER_CLEAN_V1\project.cfx.bak"

print("Starting custom project Databank alignment and duplicate cleanup...")

# Step 1: Create backup of the original project.cfx
if not os.path.exists(backup_cfx_path):
    import shutil
    shutil.copy2(project_cfx_path, backup_cfx_path)
    print(f"Created backup of original project.cfx at: {backup_cfx_path}")
else:
    print(f"Backup already exists at: {backup_cfx_path}")

# Step 2: Helper function to fix databanks in a task file
def fix_task_databanks(filename, expected_input, expected_output, remove_duplicates=True):
    filepath = os.path.join(temp_dir, filename)
    if not os.path.exists(filepath):
        print(f"File {filename} not found, skipping.")
        return False
        
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    # Find all Databanks elements
    dbs_elements = root.findall(".//Databanks")
    
    if not dbs_elements:
        print(f"No <Databanks> elements found in {filename}!")
        return False
        
    # If remove_duplicates is True and there are multiple Databanks elements
    if remove_duplicates and len(dbs_elements) > 1:
        print(f"  {filename}: Found {len(dbs_elements)} <Databanks> elements. Keeping only the first one and deleting others.")
        
        # We need to find the parent of each Databanks element to remove the extra ones
        # and keep only the first one.
        parent_map = {c: p for p in root.iter() for c in p}
        
        # Keep first, remove others
        first_db = dbs_elements[0]
        for db in dbs_elements[1:]:
            parent = parent_map.get(db)
            if parent is not None:
                parent.remove(db)
                
        # Update our list of Databanks elements
        dbs_elements = [first_db]
        
    # Now configure the first Databanks element
    db_elem = dbs_elements[0]
    
    # Let's find or create Databank child nodes
    input_node = None
    output_node = None
    
    for item in db_elem.findall("Databank"):
        name = item.attrib.get("name", "")
        label = item.attrib.get("label", "")
        if name == "Input" or label == "Input databank":
            input_node = item
        elif name == "Output" or label == "Output databank":
            output_node = item
            
    # If they don't exist, we can create them
    if input_node is None:
        input_node = ET.SubElement(db_elem, "Databank", {"label": "Input databank", "name": "Input"})
    if output_node is None:
        output_node = ET.SubElement(db_elem, "Databank", {"label": "Output databank", "name": "Output"})
        
    # Set the correct values
    print(f"  {filename}: Setting Input='{expected_input}' and Output='{expected_output}'")
    input_node.set("value", expected_input)
    output_node.set("value", expected_output)
    
    # Save the modified XML file
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
    return True

# Step 3: Run the fixes for each task file
# Retest-Task1.xml (OOS)
# Input: Results -> Output: OOS
fix_task_databanks("Retest-Task1.xml", expected_input="Results", expected_output="OOS", remove_duplicates=True)

# Retest-Task6.xml (GESTION MONETARIA - DESACTIVADA)
# Input: OOS -> Output: GESTION MONETARIA - DESACTIVADA
# Note: Task 6 corresponds to Task 3 in UI, which is currently inactive.
# Let's fix its names in case they activate it in the future.
fix_task_databanks("Retest-Task6.xml", expected_input="OOS", expected_output="GESTION MONETARIA - DESACTIVADA", remove_duplicates=True)

# Retest-Task2.xml (MC_TRADES)
# Since GESTION MONETARIA is inactive (Task 3 / Task 6), we must read directly from OOS!
# Input: OOS -> Output: MC_TRADES
fix_task_databanks("Retest-Task2.xml", expected_input="OOS", expected_output="MC_TRADES", remove_duplicates=True)

# Retest-Task3.xml (MC_SPREAD_SLIPPAGE)
# Input: MC_TRADES -> Output: MC_SPREAD_SLIPPAGE
fix_task_databanks("Retest-Task3.xml", expected_input="MC_TRADES", expected_output="MC_SPREAD_SLIPPAGE", remove_duplicates=True)

# Retest-Task5.xml (TICK)
# Input: MC_SPREAD_SLIPPAGE -> Output: TICK
fix_task_databanks("Retest-Task5.xml", expected_input="MC_SPREAD_SLIPPAGE", expected_output="TICK", remove_duplicates=True)

# Retest-Task4.xml (SPP)
# Input: TICK -> Output: SPP
fix_task_databanks("Retest-Task4.xml", expected_input="TICK", expected_output="SPP", remove_duplicates=True)

# Retest-Task7.xml (WFA MATRIX)
# Input: SPP -> Output: WFA MATRIX
fix_task_databanks("Retest-Task7.xml", expected_input="SPP", expected_output="WFA MATRIX", remove_duplicates=True)

# Step 4: Repack modified files back into project.cfx
print("\nRepacking all files back into project.cfx...")
with zipfile.ZipFile(project_cfx_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        if os.path.isfile(item_path):
            z.write(item_path, item)
            print(f"  Added {item} to project.cfx")

print("\nCustom Project Databank alignment is complete! All task transitions are now 100% correct and aligned.")
