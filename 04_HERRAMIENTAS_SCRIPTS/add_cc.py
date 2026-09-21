import zipfile
import tempfile
import os
import xml.etree.ElementTree as ET

proj_path = r'C:\SQX_144_Full\user\projects\NDXm_NY_Session_Project\project.cfx'

# Template from standard GBPJPY setup or defaults
def inject_or_modify_mc(mc_node):
    mc_node.set('use', 'true')
    # If we really want to ensure the settings are standard, we'd normally parse and set specific children.
    # We will trust SQX has decent defaults if the block exists, or the user can verify in UI.

def enable_robustness(xml_content):
    root = ET.fromstring(xml_content)
    cc = root.find('.//CrossChecks')
    if cc is None:
        return xml_content
    
    # 1. Higher Precision
    hp = cc.find('RetestWithHigherPrecision')
    if hp is not None:
        hp.set('use', 'true')
        
    # 2. Monte Carlo Retest
    mc = cc.find('MonteCarloRetest')
    if mc is not None:
        mc.set('use', 'true')

    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def main():
    if not os.path.exists(proj_path):
        print(f"Project not found: {proj_path}")
        return

    temp_dir = tempfile.mkdtemp()
    temp_zip = os.path.join(temp_dir, 'new_proj.cfx')
    
    modified = False
    with zipfile.ZipFile(proj_path, 'r') as zin:
        with zipfile.ZipFile(temp_zip, 'w') as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                if item.filename.startswith('Build-Task'):
                    new_content = enable_robustness(content)
                    if new_content != content:
                        modified = True
                        print(f"Enabled CC in {item.filename}")
                    zout.writestr(item, new_content)
                else:
                    zout.writestr(item, content)
                    
    if modified:
        import shutil
        shutil.move(temp_zip, proj_path)
        print("Updated project with CrossChecks enabled.")
    else:
        print("No changes made.")

if __name__ == '__main__':
    main()
