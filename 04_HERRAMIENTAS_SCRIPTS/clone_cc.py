import zipfile
import tempfile
import os
import xml.etree.ElementTree as ET

gbpjpy_path = r'C:\SQX_144_Full\user\projects\GBPJPY_nico66fxPRO_V2\project.cfx'
ndxm_path = r'C:\SQX_144_Full\user\projects\NDXm_NY_Session_Project\project.cfx'

def get_donor_cc():
    with zipfile.ZipFile(gbpjpy_path, 'r') as z:
        with z.open('Build-Task1.xml') as f:
            root = ET.parse(f).getroot()
            cc = root.find('.//CrossChecks')
            return cc

def replace_cc(xml_content, donor_cc):
    root = ET.fromstring(xml_content)
    
    # Find existing CC node
    old_cc = root.find('.//CrossChecks')
    if old_cc is not None:
        parent_map = {c: p for p in root.iter() for c in p}
        parent = parent_map[old_cc]
        
        # We need to make a copy of the donor_cc so we don't mess up the original element tree mapping
        import copy
        new_cc = copy.deepcopy(donor_cc)
        
        # Additionally, let's enable Monte Carlo since GBPJPY might not have it enabled
        # The user requested to combine standard robust tests with GBPJPY's settings
        mc = new_cc.find('MonteCarloRetest')
        if mc is not None:
            mc.set('use', 'true')
        else:
            # Create a simple MC element if it completely didn't exist
            mc = ET.SubElement(new_cc, 'MonteCarloRetest', use='true')
            setup = ET.SubElement(mc, 'Setup')
            ET.SubElement(setup, 'Simulations').text = '100'
            ET.SubElement(setup, 'RandomizeTrades', type='RandomizeTradesOrder', probability='0.0', skipProbability='0.1')
        
        # Ensure RetestWithHigherPrecision is true
        hp = new_cc.find('RetestWithHigherPrecision')
        if hp is not None:
            hp.set('use', 'true')
            
        parent.remove(old_cc)
        parent.append(new_cc)
        
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def main():
    donor_cc = get_donor_cc()
    if donor_cc is None:
        print("Donor CC not found")
        return
        
    temp_dir = tempfile.mkdtemp()
    temp_zip = os.path.join(temp_dir, 'new_proj.cfx')
    
    modified = False
    with zipfile.ZipFile(ndxm_path, 'r') as zin:
        with zipfile.ZipFile(temp_zip, 'w') as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                if item.filename.startswith('Build-Task'):
                    new_content = replace_cc(content, donor_cc)
                    if new_content != content:
                        modified = True
                        print(f"Replaced CC in {item.filename} with GBPJPY's template + MC adjustments")
                    zout.writestr(item, new_content)
                else:
                    zout.writestr(item, content)
                    
    if modified:
        import shutil
        shutil.move(temp_zip, ndxm_path)
        print("Updated NDXm project with combined CrossChecks!")
    else:
        print("No changes made.")

if __name__ == '__main__':
    main()
