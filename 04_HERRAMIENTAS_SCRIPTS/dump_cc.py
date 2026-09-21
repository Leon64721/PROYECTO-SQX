import zipfile
import xml.etree.ElementTree as ET
with zipfile.ZipFile(r'C:\SQX_144_Full\user\projects\GBPJPY_nico66fxPRO_V2\project.cfx') as z:
    with z.open('Build-Task1.xml') as f:
        root = ET.parse(f).getroot()
        cc = root.find('.//CrossChecks')
        ET.dump(cc)
