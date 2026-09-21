import sys
from pathlib import Path
import json

sys.path.insert(0, r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-random-group')
from engine.groups import load_catalog, hybrid_ref, make_group, wrap_groups

def build():
    catalog_path = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-random-group\catalog.json'
    _, T, B = load_catalog(catalog_path)
    groups = []
    
    # 1. MTF Trigger group using user's existing blocks (Breakout)
    triggers = ["CBlock_ORBLongBreakout", "CBlock_ORBLongBreakout_NYSession"]
    cond_items = []
    for t in triggers:
        if t in B:
            cond_items.append(hybrid_ref(B[t]))
    
    if cond_items:
        groups.append(make_group("Breakout_Triggers_NDXm", "Condition", cond_items, category="PropFirmCompliance_user"))

    out = wrap_groups(groups)
    out_path = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-random-group\breakout_triggers.xml'
    Path(out_path).write_text(out, encoding='utf-8')
    print('Generated', out_path, 'with', len(groups), 'groups.')

if __name__ == '__main__':
    build()
