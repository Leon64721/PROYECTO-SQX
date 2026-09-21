import zipfile, xml.etree.ElementTree as ET
p = r'C:\SQX_144_Full\user\settings\Configs\NQ CFD H1.cfx'
with zipfile.ZipFile(p) as z:
    xml_bytes = z.read('config.xml')
print('SIZE', len(xml_bytes))
root = ET.fromstring(xml_bytes)
print('ROOT', root.tag)
for e in root.iter():
    if e.tag in {'Task','Settings','Data','Setups','Setup','OutOfSample','WhatToBuild','RiskMoneyManagement','BuildTradingOptions','Chart','Symbol','Options'}:
        attrs = e.attrib
        print('TAG', e.tag, attrs)
        if e.tag in {'Setup','Chart','Symbol'}:
            print('TEXT', e.text)
