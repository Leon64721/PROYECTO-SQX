from pathlib import Path
import zipfile, shutil, subprocess

src = Path(r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\tests\tmp\fullBuilderConfig.xml')
ws = Path(r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\user\projects\Builder')
ws.mkdir(parents=True, exist_ok=True)
source_cfx = ws / 'NDXm_Qlib_OOS20.cfx'
project_cfx = ws / 'project.cfx'
live_cfx = Path(r'C:\SQX_144_Full\user\projects\Builder\project.cfx')
live_cfx.parent.mkdir(parents=True, exist_ok=True)

assert src.exists(), f'Missing source file: {src}'
xml = src.read_text(encoding='utf-8')
required = ['NDXm_TICK_UTCPlus02', 'H1', 'QlibSignal(lookback=5)', '2024.01.27', '2026.06.25']
missing = [token for token in required if token not in xml]
assert not missing, f'Missing required markers in XML: {missing}'

for f in [source_cfx, project_cfx, live_cfx]:
    if f.exists():
        f.unlink()

with zipfile.ZipFile(source_cfx, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr('config.xml', xml)

shutil.copy2(source_cfx, project_cfx)
shutil.copy2(source_cfx, live_cfx)

with zipfile.ZipFile(live_cfx, 'r') as z:
    names = z.namelist()
    print('ZIP_ENTRIES', names)
    assert names == ['config.xml'], f'Unexpected ZIP root: {names}'
    cfg = z.read('config.xml').decode('utf-8', 'replace')
    print('CONFIG_XML_OK', 'config.xml' in names, len(cfg))
    for token in required:
        print(f'TOKEN_{token}:', token in cfg)
    print('XML_START', cfg.strip()[:160])

print('LIVE_EXISTS', live_cfx.exists())

try:
    res = subprocess.run(
        ['gbrain', 'put', 'sqx-fase-5-builder-verified', 'Fase 5 Completada: Proyecto Builder (NDXm_Qlib_OOS20.cfx) verificado con config.xml y desplegado a SQX'],
        capture_output=True,
        text=True,
        check=False,
    )
    print('GBRAIN_RC', res.returncode)
    print('GBRAIN_STDOUT', (res.stdout or '').strip())
    print('GBRAIN_STDERR', (res.stderr or '').strip())
except FileNotFoundError:
    print('GBRAIN_UNAVAILABLE', 'gbrain not in PATH')
