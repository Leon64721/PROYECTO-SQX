import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_ROOT))

from engine.emit import Catalog
from engine.grammar import (
    crosses_above, crosses_below, make_block, int_param, double_param, esc, wrap_batch,
)

def build(cat: Catalog) -> list[str]:
    blocks = []

    # ORB Strategy - Opening Range Breakout
    # We parameterize the session times so the user can optimize them in SQX.
    long_key, short_key = "CBlock_ORBLongBreakout", "CBlock_ORBShortBreakout"
    
    start_h = int_param("#Int1#", "Range Start Hour", "9", "0", "23")
    start_m = int_param("#Int2#", "Range Start Minute", "30", "0", "59")
    end_h = int_param("#Int3#", "Range End Hour", "10", "0", "23")
    end_m = int_param("#Int4#", "Range End Minute", "0", "0", "59")
    
    time_params = start_h + start_m + end_h + end_m

    # Long rule: Close crosses above the Session High
    blocks.append(make_block(
        key=long_key,
        name="ORBLongBreakout",
        display=esc("Close crosses above ORB High (#Int1#:#Int2# - #Int3#:#Int4#)"),
        category="Breakout_user",
        help_text=esc("Long: Close crosses above the Opening Range High (Session High)."),
        opposite=short_key,
        params=time_params,
        contents=crosses_above(
            cat.atom("Close", shift="1"), 
            cat.atom("SessionHigh", StartHours="#Int1#", StartMinutes="#Int2#", EndHours="#Int3#", EndMinutes="#Int4#", shift="1")
        ),
    ))
    
    # Short rule: Close crosses below the Session Low
    blocks.append(make_block(
        key=short_key,
        name="ORBShortBreakout",
        display=esc("Close crosses below ORB Low (#Int1#:#Int2# - #Int3#:#Int4#)"),
        category="Breakout_user",
        help_text=esc("Short: Close crosses below the Opening Range Low (Session Low)."),
        opposite=long_key,
        params=time_params,
        contents=crosses_below(
            cat.atom("Close", shift="1"), 
            cat.atom("SessionLow", StartHours="#Int1#", StartMinutes="#Int2#", EndHours="#Int3#", EndMinutes="#Int4#", shift="1")
        ),
    ))

    return blocks

def main():
    catalog_path = "catalog.json"
    out_path = "ORB_Breakout_Rules.xml"
    cat = Catalog(catalog_path)
    xml = wrap_batch(build(cat))
    Path(out_path).write_text(xml, encoding="utf-8")
    print(f"wrote {out_path}")

if __name__ == "__main__":
    main()
