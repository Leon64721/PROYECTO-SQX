import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

live = Path(r'C:\SQX_144_Full\user\projects\Builder\project.cfx')
mirror = Path(r'E:\CLASE OPTION STRATEGY QUANT\PROGRAMA\SQX_144_Full\SQX_144_Full\user\projects\Builder\project.cfx')
backup = live.with_name(live.name + '.bak_20260815')

if not backup.exists():
    shutil.copy2(live, backup)

with zipfile.ZipFile(mirror) as zref, zipfile.ZipFile(live) as zlive:
    ref_xml = zref.read('config.xml').decode('utf-8', 'replace')
    live_task_xml = zlive.read('Build-Task1.xml').decode('utf-8', 'replace')

ref_root = ET.fromstring(ref_xml)
lt_root = ET.fromstring(live_task_xml)
live_settings = lt_root if lt_root.tag == 'Settings' else lt_root.find('Settings')
if live_settings is None:
    raise RuntimeError('No <Settings> found in Build-Task1.xml')

build_task = ref_root.find("./Tasks/Task[@type='Build']")
if build_task is None:
    build_task = ref_root.find('./Tasks/Task')
if build_task is None:
    raise RuntimeError('No Build Task found in reference project')

old_settings = build_task.find('Settings')
if old_settings is not None:
    build_task.remove(old_settings)

settings_copy = ET.fromstring(ET.tostring(live_settings, encoding='utf-8', method='xml'))
build_task.insert(1, settings_copy)

xml_out = ET.tostring(ref_root, encoding='utf-8', method='xml').decode('utf-8')
repair_tmp = live.with_name(live.name + '.repair_tmp')
with zipfile.ZipFile(repair_tmp, 'w', compression=zipfile.ZIP_DEFLATED) as out:
    out.writestr('config.xml', xml_out)
    out.writestr('Build-Task1.xml', live_task_xml)

os.replace(repair_tmp, live)
print('Builder project repaired at:', live)
print('Backup created at:', backup)
