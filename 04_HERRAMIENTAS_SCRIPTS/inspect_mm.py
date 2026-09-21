import xml.etree.ElementTree as ET
import zipfile

def inspect():
    with zipfile.ZipFile(r'C:\SQX_144_Full\user\projects\Builder\project.cfx') as z:
        with z.open('Build-Task1.xml') as f:
            root = ET.parse(f).getroot()
            for mm in root.findall('.//MoneyManagement'):
                print("MoneyManagement:", ET.tostring(mm).decode('utf-8')[:500])

if __name__ == '__main__':
    inspect()