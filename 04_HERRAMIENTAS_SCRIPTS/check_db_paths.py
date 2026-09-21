import xml.etree.ElementTree as ET
import glob

tree = ET.parse('temp_cfx/Retest-Task1.xml')
root = tree.getroot()

# Create parent map
parent_map = {c: p for p in root.iter() for c in p}

for i, db in enumerate(root.findall('.//Databanks')):
    path = []
    curr = db
    while curr in parent_map:
        path.append(curr.tag)
        curr = parent_map[curr]
    path.append(root.tag) # Root
    print(f"Databanks {i}: Path: {' -> '.join(reversed(path))}")
