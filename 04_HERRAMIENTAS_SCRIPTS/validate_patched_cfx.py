import xml.etree.ElementTree as ET
import glob

print("Validating PATCHED task files...")
for fn in sorted(glob.glob("temp_cfx_patched/Retest-Task*.xml")):
    try:
        tree = ET.parse(fn)
        root = tree.getroot()
        dbs = root.findall(".//Databanks")
        print(f"\n{fn}: found {len(dbs)} <Databanks> elements")
        for i, db in enumerate(dbs):
            print(f"  [{i}] attribs: {db.attrib}")
            for item in db.findall("Databank"):
                name = item.attrib.get("name", "")
                label = item.attrib.get("label", "")
                val = item.attrib.get("value", "")
                print(f"    - Label: {label:<16} Name: {name:<10} Value: {val}")
    except Exception as e:
        print(f"Error parsing {fn}: {e}")
