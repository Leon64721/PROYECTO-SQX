import zipfile, re, os
paths = [r'C:\SQX_144_Full\user\projects\Builder\project.cfx', r'C:\SQX_144_Full\user\settings\Configs\NQ CFD H1.cfx']
for p in paths:
    print('FILE', p, 'EXISTS', os.path.exists(p))
    if not os.path.exists(p):
        continue
    with zipfile.ZipFile(p) as z:
        print('ZIP_ENTRIES', z.namelist()[:10])
        xml = z.read('config.xml').decode('utf-8', 'replace')
        m = re.search(r'<StrategyType[^>]*>', xml, re.I)
        print('STRATEGYTYPE', m.group(0)[:300] if m else 'MISSING')
        for pat in ['improveType=', 'improveDatabank=', 'strategyFile=', 'output databank', 'Results', 'Default', 'Simple']:
            q = re.search(pat, xml, re.I)
            print('PAT', pat, 'FOUND', bool(q), q.group(0)[:200] if q else None)
            if q:
                start = max(0, q.start()-180)
                end = min(len(xml), q.end()+500)
                print(xml[start:end])
                print('---')
        print('HAS_STOPLOSS', 'StopLoss' in xml)
        print('HAS_PROFITTARGET', 'ProfitTarget' in xml)
        print('HAS_ATR', 'ATR' in xml)
        print('HAS_QLIB', 'QlibSignal' in xml)
        print('== END ==\n')
