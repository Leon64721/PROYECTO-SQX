import zipfile
import tempfile
import os
import xml.etree.ElementTree as ET

proj_path = r'C:\SQX_144_Full\user\projects\NDXm_NY_Session_Project\project.cfx'

def add_mtf_setup(xml_content):
    root = ET.fromstring(xml_content)
    setups = root.find('.//Data/Setups')
    
    if setups is not None:
        # Check if already multiple setups
        if len(list(setups)) > 1:
            return xml_content  # Already has multiple setups
        
        # Clone the first setup
        first_setup = setups[0]
        import copy
        new_setup = copy.deepcopy(first_setup)
        
        # Change timeframe to H4
        chart = new_setup.find('Chart')
        if chart is not None:
            chart.set('timeframe', 'H4')
            
        setups.append(new_setup)
        print("Added H4 Data2 setup to project.")
        
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
                    new_content = add_mtf_setup(content)
                    if new_content != content:
                        modified = True
                        print(f"Added MTF to {item.filename}")
                    zout.writestr(item, new_content)
                else:
                    zout.writestr(item, content)

    if modified:
        import shutil
        shutil.move(temp_zip, proj_path)
        print("Updated NDXm project with Multiple Timeframes (H4) enabled.")
    else:
        print("No changes made.")

if __name__ == '__main__':
    main()
