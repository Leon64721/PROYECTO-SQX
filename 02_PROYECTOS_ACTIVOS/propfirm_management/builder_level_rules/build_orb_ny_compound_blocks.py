"""build_orb_ny_compound_blocks.py — ORB entry signals compounded with the NY
session compliance gate, as new standalone blocks.

Why a NEW block (not editing the existing ORBLongBreakout/ORBShortBreakout):
`orb_custom_project\\README.md` explicitly warns not to touch the validated
V4-V8 `.cfx` files or the original ORB blocks in production use. This generates
a *separate*, clearly-named pair (`ORBLongBreakout_NYSession` /
`ORBShortBreakout_NYSession`) that ANDs the original ORB breakout logic
(reproduced identically from `gen_orb.py`, same #Int1#-#Int4# session-range
params) with the DST-aware NY compliance window from
`build_ny_session_block.py`. Drop these new blocks into a strategy/template in
place of (or alongside) the plain ORB blocks when you want the Builder to only
ever be able to generate/keep entries that also respect the legal NY session.

The original ORBLongBreakout/ORBShortBreakout pair and every already-built
`.cfx` are untouched by this script.

Run:
  python build_orb_ny_compound_blocks.py catalog.json out_orb_ny_compound.xml
"""

from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-custom-block")
sys.path.insert(0, str(SKILL_ROOT))

from engine.emit import Catalog
from engine.grammar import (
    and_op, crosses_above, crosses_below, make_block, int_param, esc, wrap_batch,
)
from build_ny_session_block import ny_session_contents  # same folder, shared formula


def build(cat: Catalog) -> list[str]:
    blocks = []
    long_key, short_key = (
        "CBlock_ORBLongBreakout_NYSession",
        "CBlock_ORBShortBreakout_NYSession",
    )

    # identical param convention to the original gen_orb.py (#Int1#-#Int4#) so
    # the ORB range-window stays user/optimizer-configurable exactly as before.
    start_h = int_param("#Int1#", "Range Start Hour", "9", "0", "23")
    start_m = int_param("#Int2#", "Range Start Minute", "30", "0", "59")
    end_h = int_param("#Int3#", "Range End Hour", "10", "0", "23")
    end_m = int_param("#Int4#", "Range End Minute", "0", "0", "59")
    time_params = start_h + start_m + end_h + end_m

    ny_gate = ny_session_contents(cat)

    blocks.append(make_block(
        key=long_key,
        name="ORBLongBreakout_NYSession",
        display=esc(
            "Close crosses above ORB High (#Int1#:#Int2# - #Int3#:#Int4#) "
            "AND bar is inside NY session (DST-aware)"
        ),
        category="PropFirmCompliance_user",
        help_text=esc(
            "Long ORB breakout, identical entry geometry to ORBLongBreakout, but ANDed "
            "with the DST-aware NY cash-session gate (PF_NYSessionWindow logic) so the "
            "Builder cannot generate/keep a variant that enters outside the legal "
            "09:30-16:00 America/New_York window. Built for NDXm (feed timezone EET)."
        ),
        opposite=short_key,
        params=time_params,
        contents=and_op(
            crosses_above(
                cat.atom("Close", shift="1"),
                cat.atom("SessionHigh", StartHours="#Int1#", StartMinutes="#Int2#",
                         EndHours="#Int3#", EndMinutes="#Int4#", shift="1"),
            ),
            ny_gate,
        ),
    ))

    blocks.append(make_block(
        key=short_key,
        name="ORBShortBreakout_NYSession",
        display=esc(
            "Close crosses below ORB Low (#Int1#:#Int2# - #Int3#:#Int4#) "
            "AND bar is inside NY session (DST-aware)"
        ),
        category="PropFirmCompliance_user",
        help_text=esc(
            "Short ORB breakout, identical entry geometry to ORBShortBreakout, but ANDed "
            "with the DST-aware NY cash-session gate (PF_NYSessionWindow logic) so the "
            "Builder cannot generate/keep a variant that enters outside the legal "
            "09:30-16:00 America/New_York window. Built for NDXm (feed timezone EET)."
        ),
        opposite=long_key,
        params=time_params,
        contents=and_op(
            crosses_below(
                cat.atom("Close", shift="1"),
                cat.atom("SessionLow", StartHours="#Int1#", StartMinutes="#Int2#",
                         EndHours="#Int3#", EndMinutes="#Int4#", shift="1"),
            ),
            ny_gate,
        ),
    ))

    return blocks


def main(argv):
    catalog_path = argv[0] if argv else str(SKILL_ROOT / "catalog.json")
    out_path = argv[1] if len(argv) > 1 else "out_orb_ny_compound.xml"
    cat = Catalog(catalog_path)
    xml = wrap_batch(build(cat))
    Path(out_path).write_text(xml, encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"validate with:\n  python {SKILL_ROOT}\\engine\\validate.py {out_path} --catalog {catalog_path}")


if __name__ == "__main__":
    main(sys.argv[1:])
