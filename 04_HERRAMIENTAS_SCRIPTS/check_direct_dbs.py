import xml.etree.ElementTree as ET

tree = ET.parse('temp_cfx/Retest-Task1.xml')
root = tree.getroot()

dbs_elements = root.findall('Databanks')
print(f"Number of direct <Databanks> children in Settings: {len(dbs_elements)}")

for i, db in enumerate(dbs_elements):
    print(f"\nDatabanks element {i}:")
    print(ET.tostring(db, encoding='utf-8').decode('utf-8'))
