import zipfile
import xml.etree.ElementTree as ET

def check_cc(p):
    try:
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.startswith('Build-Task'):
                    with z.open(n) as f:
                        root = ET.parse(f).getroot()
                        cc = root.find('.//CrossChecks')
                        if cc is not None:
                            print(f'{p} - {n}: CrossChecks found, count: {len(list(cc))}')
                            for c in cc:
                                print('  ', c.tag, c.attrib)
                        else:
                            print(f'{p} - {n}: No CrossChecks')
    except Exception as e:
        print(e)

check_cc(r'C:\SQX_144_Full\user\projects\Builder\project.cfx')
check_cc(r'C:\SQX_144_Full\user\projects\GBPJPY_nico66fxPRO_V2\project.cfx')
