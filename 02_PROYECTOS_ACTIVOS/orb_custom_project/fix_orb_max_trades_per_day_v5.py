"""
Fix v5 for BASE_CP_MASTER_CLEAN_V1 (ORB Custom Project).

Root cause confirmed 2026-09-14: with v4 (DrawdownPct<35) the OOS 5th-run finally
completed (JVM restart fixed the Generation-0 freeze) but still gave 0 survivors.
Quantified sample of 60 OOS dismissals: 34/60 (57%) killed by the automatic filter
"too many trades closing at the same bar" -- now the dominant blocker (0 dismissals
by DrawdownPct, confirming that fix worked).

Confirmed in the live project.cfx:
- CBlock_ORBLongBreakout/ShortBreakout are a bare price-crossing condition with no
  re-entry guard (fires every time price re-crosses the range boundary).
- Trading Options MaxTradesPerDay="0" (unlimited).
- Exit-at-End-of-Day forces close at 22:30 EET for whatever is still open.

=> Unlimited intraday re-entries pile up and get force-closed together at the same
EOD bar, tripping SQX's built-in same-bar-close sanity filter on most candidates.

User's chosen fix (via AskUserQuestion 2026-09-14): try 2 trades/day first (not the
stricter 1/day) before going more restrictive, in case the edge needs the retry.

Operates on a FRESH copy of the live project.cfx (same pattern as v2/v3/v4) so any
manual UI edits made by the user are preserved.
"""
import shutil
import zipfile
import re
from pathlib import Path

LIVE_PROJECT = Path(r"C:\SQX_144_Full\user\projects\BASE_CP_MASTER_CLEAN_V1\project.cfx")
OUTPUT = Path(r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\BASE_CP_MASTER_CLEAN_V1_ORB_V5_MAXTRADES2.cfx")

OLD = '<Param key="MaxTradesPerDay" className="MaxTradesPerDay">0</Param>'
NEW = '<Param key="MaxTradesPerDay" className="MaxTradesPerDay">2</Param>'


def main():
    assert LIVE_PROJECT.exists(), f"Live project not found: {LIVE_PROJECT}"

    work_dir = Path(r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\_work_fix_orb_v5")
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)

    with zipfile.ZipFile(LIVE_PROJECT) as z:
        z.extractall(work_dir)

    build_task = work_dir / "Build-Task1.xml"
    txt = build_task.read_text(encoding="utf-8")

    count = txt.count(OLD)
    assert count == 1, f"Expected exactly 1 occurrence of MaxTradesPerDay=0, found {count}"

    new_txt = txt.replace(OLD, NEW)
    assert new_txt.count(NEW) == 1
    build_task.write_text(new_txt, encoding="utf-8")

    if OUTPUT.exists():
        OUTPUT.unlink()
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(work_dir.iterdir()):
            z.write(f, arcname=f.name)

    print(f"OK: MaxTradesPerDay 0 -> 2 (1/1 replacement)")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
