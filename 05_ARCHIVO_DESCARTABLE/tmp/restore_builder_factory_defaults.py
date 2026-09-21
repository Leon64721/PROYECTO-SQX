import zipfile, os, re

p = r'C:\SQX_144_Full\user\projects\Builder\project.cfx'
backup = p + '.bak'

if not os.path.exists(p):
    raise FileNotFoundError(p)

with zipfile.ZipFile(p, 'r') as z:
    names = z.namelist()
    if 'config.xml' not in names:
        raise ValueError(f'No config.xml in {p}')

    entries = {name: z.read(name) for name in names}
    xml = entries['config.xml'].decode('utf-8', 'replace')
    print('BEFORE_STRATEGYTYPE', re.search(r'<StrategyType[^>]*>', xml, re.I).group(0) if re.search(r'<StrategyType[^>]*>', xml, re.I) else 'MISSING')
    print('BEFORE_OUTPUT', 'Databank label="Output databank" name="Output" value="Results"' in xml)
    print('BEFORE_IMPROVE_FLAG', re.search(r'improveType="[^"]+"', xml, re.I).group(0) if re.search(r'improveType="[^"]+"', xml, re.I) else 'MISSING')

    # Force default Simple Strategy mode and disable improve-existing strategy.
    xml = re.sub(r'improveType="[^"]*"', 'improveType="none"', xml, count=1, flags=re.I)
    xml = re.sub(r'strategyFile="[^"]*"', 'strategyFile=""', xml, count=1, flags=re.I)
    xml = re.sub(r'improveDatabank="[^"]*"', 'improveDatabank=""', xml, count=1, flags=re.I)

    # Ensure a stock Results output databank remains selected without altering native stock sections.
    xml = re.sub(r'(<Databank label="Output databank" name="Output" value=")[^"]*("\s*/?>)', r'\1Results\2', xml, count=1, flags=re.I)
    if 'Databank label="Output databank" name="Output" value="Results"' not in xml:
        xml = xml.replace(
            '<Databank label="Output databank" name="Output" value="Last generation" />',
            '<Databank label="Output databank" name="Output" value="Results" />',
            1,
        )

    entries['config.xml'] = xml.encode('utf-8')

    if 'Build-Task1.xml' in entries:
        task_xml = entries['Build-Task1.xml'].decode('utf-8', 'replace')
        task_xml = re.sub(r'improveType="[^"]*"', 'improveType="none"', task_xml, count=1, flags=re.I)
        task_xml = re.sub(r'strategyFile="[^"]*"', 'strategyFile=""', task_xml, count=1, flags=re.I)
        task_xml = re.sub(r'improveDatabank="[^"]*"', 'improveDatabank=""', task_xml, count=1, flags=re.I)
        task_xml = re.sub(r'(<Databank label="Output databank" name="Output" value=")[^"]*("\s*/?>)', r'\1Results\2', task_xml, count=1, flags=re.I)
        entries['Build-Task1.xml'] = task_xml.encode('utf-8')

    with zipfile.ZipFile(backup, 'w', compression=zipfile.ZIP_DEFLATED) as zb:
        for name in names:
            zb.writestr(name, entries[name])

os.replace(backup, p)

with zipfile.ZipFile(p, 'r') as z:
    s = z.read('config.xml').decode('utf-8', 'replace')
    m = re.search(r'<StrategyType[^>]*>', s, re.I)
    print('AFTER_STRATEGYTYPE', m.group(0) if m else 'MISSING')
    print('AFTER_IMPROVE_FLAG', re.search(r'improveType="[^"]+"', s, re.I).group(0) if re.search(r'improveType="[^"]+"', s, re.I) else 'MISSING')
    print('AFTER_OUTPUT_RESULTS', 'Databank label="Output databank" name="Output" value="Results"' in s)
    print('AFTER_QLIB', 'QlibSignal' in s)
    print('AFTER_STOPLOSS', 'StopLoss' in s)
    print('AFTER_PROFITTARGET', 'ProfitTarget' in s)
    print('AFTER_ATR', 'ATR' in s)
