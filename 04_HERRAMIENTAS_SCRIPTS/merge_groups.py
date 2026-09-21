import xml.etree.ElementTree as ET
from pathlib import Path

def merge():
    target = r'C:\SQX_144_Full\user\settings\blockGroups.xml'
    source = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-random-group\breakout_triggers.xml'
    
    target_tree = ET.parse(target)
    target_root = target_tree.getroot()
    
    source_tree = ET.parse(source)
    source_root = source_tree.getroot()
    
    for group in source_root.findall('Group'):
        # Check if already exists by name
        name = group.get('name')
        existing = [g for g in target_root.findall('Group') if g.get('name') == name]
        if existing:
            target_root.remove(existing[0])
        target_root.append(group)
        
    target_tree.write(target, encoding='utf-8', xml_declaration=False)
    print("Merged groups into blockGroups.xml")

if __name__ == '__main__':
    merge()
