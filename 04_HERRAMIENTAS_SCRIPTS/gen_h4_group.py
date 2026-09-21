import sys
from pathlib import Path
import json

sys.path.insert(0, r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-random-group')
from engine.groups import load_catalog, inline_item, is_greater, is_lower, number, hybrid_ref, make_group, wrap_groups

def build():
    catalog_path = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-random-group\catalog.json'
    _, T, B = load_catalog(catalog_path)
    groups = []
    
    # Let's create an MTF Condition Group that combines H4 Trend with Breakout blocks
    # Actually, random groups select ONE item.
    # If the user wants H4 Trend AND M15 entry, they can be two separate groups, or we use a block that combines them.
    # The sqx-strategy-template MTF shape usually has daily_filter + trigger. 
    # If we want a simple Trigger group, we can just put the existing Breakout blocks in it.
    
    # Let's just pool the user's custom blocks as the triggers
    triggers = ["CBlock_ORBLongBreakout", "CBlock_ORBLongBreakout_NYSession"]
    cond_items = [hybrid_ref(B[k]) for k in triggers if k in B]
    
    groups.append(make_group("Breakout_Triggers_NDXm", "Condition", cond_items, category="PropFirmCompliance_user"))

    # Let's create another group for MTF H4 Trend
    # Close > EMA on Chart 2
    if "Close" in T and "EMA" in T and "SMA" in T:
        h4_ema_up = is_greater(
            inline_item(T["Close"], optimize={"#Chart#": "2"}), 
            inline_item(T["EMA"], optimize={"#Chart#": "2", "#Period#": "10:100:10"})
        )
        h4_sma_up = is_greater(
            inline_item(T["Close"], optimize={"#Chart#": "2"}), 
            inline_item(T["SMA"], optimize={"#Chart#": "2", "#Period#": "10:100:10"})
        )
        groups.append(make_group("MTF_H4_Trend", "Condition", [h4_ema_up, h4_sma_up], category="PropFirmCompliance_user"))

    out = wrap_groups(groups)
    Path('h4_groups.xml').write_text(out, encoding='utf-8')
    print('Generated h4_groups.xml with', len(groups), 'groups.')

if __name__ == '__main__':
    build()
