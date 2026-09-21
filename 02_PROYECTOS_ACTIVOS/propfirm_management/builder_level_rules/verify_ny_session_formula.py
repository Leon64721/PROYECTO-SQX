r"""verify_ny_session_formula.py

Ground-truth verification of the "NY session window, DST-aware" boolean formula
BEFORE it gets translated into AlgoWizard custom-block XML.

Why this exists: AlgoWizard's grammar has NO native "IsEqual"/"NOT" operator (only
IsGreater/IsLower + AND/OR), so the DST switch logic has to be expressed as a
hand-built arithmetic/comparison tree (see design notes in
`user\PropFirm_Management\31_ny_session_builder_block.md`). That kind of formula is
exactly the kind of thing that silently breaks on a boundary day. This script proves
the formula is correct by comparing it, day by day across many years, against the
REAL DST-aware conversion computed independently via Python's `zoneinfo` (the actual
IANA tz database — not hand-derived rules).

Symbol under test: NDXm (StrategyQuant declares its data feed timezone as EET).
Reference EU zone used for ground truth: Europe/Bucharest (follows the standard EU
DST rule: DST starts last Sunday of March, ends last Sunday of October — same rule
any real EET-zone city follows).
Session to protect: NYSE cash session, 09:30-16:00 America/New_York.

Run:  python verify_ny_session_formula.py
"""
from __future__ import annotations
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
EET = ZoneInfo("Europe/Bucharest")  # any real EU/EET-rule city works identically


def ground_truth_window_eet(d: date) -> tuple[time, time]:
    """The REAL NY 09:30-16:00 session window, expressed in EET local time for
    calendar day `d`, computed via the IANA tz database (independent of our formula)."""
    ny_open = datetime.combine(d, time(9, 30), tzinfo=NY)
    ny_close = datetime.combine(d, time(16, 0), tzinfo=NY)
    open_eet = ny_open.astimezone(EET)
    close_eet = ny_close.astimezone(EET)
    return open_eet.time(), close_eet.time()


# ---------------------------------------------------------------------------
# Our hand-built formula (1:1 translation of what will become the AlgoWizard
# boolean tree — see build_ny_session_block.py). Uses ONLY the primitives
# actually available in AlgoWizard: integer month/day-of-month/day-of-week of
# the bar (Sunday=0) plus greater-than/less-than/AND/OR (no equality, no NOT).
# ---------------------------------------------------------------------------

def recent_sunday_day(d: date) -> int:
    """Day-of-month of the most recent Sunday on/before `d` (may be <=0, meaning
    it falls in the previous month) — mirrors DayOfMonth - DayOfWeek(Sunday=0)."""
    dow_sunday0 = (d.weekday() + 1) % 7  # python: Monday=0 -> convert to Sunday=0
    return d.day - dow_sunday0


def formula_window_eet(d: date) -> tuple[time, time]:
    mo = d.month
    rs = recent_sunday_day(d)

    mismatch = (
        (mo == 3 and 8 <= rs <= 24) or       # US already DST, EU not yet (Mar 8-24 window)
        (mo == 10 and rs >= 25) or            # EU already back to standard, US still DST
        (mo == 11 and rs < 1)                 # Nov, before US 1st Sunday switch-back
    )
    nominal = (
        mo in (1, 2, 12) or
        (mo == 3 and rs < 8) or
        (mo == 3 and rs > 24) or
        (4 <= mo <= 9) or
        (mo == 10 and rs < 25) or
        (mo == 11 and rs > 0)
    )
    assert mismatch != nominal or (not mismatch and not nominal) is False, \
        f"formula gap on {d}: mismatch={mismatch} nominal={nominal}"
    assert mismatch or nominal, f"formula GAP (neither branch matched) on {d}"
    assert not (mismatch and nominal), f"formula OVERLAP on {d}"

    if mismatch:
        return time(15, 30), time(22, 0)
    return time(16, 30), time(23, 0)


def main():
    start = date(2024, 1, 1)
    end = date(2031, 1, 1)
    d = start
    mismatches_found = []
    total = 0
    while d < end:
        total += 1
        truth_open, truth_close = ground_truth_window_eet(d)
        # ground truth is exact to the minute; our formula is deliberately
        # hour:minute-quantized daily (DST flips happen at 2am local, so the
        # flip DAY itself may briefly disagree by an hour for ~2 hours after
        # midnight EET before the flip local time — acceptable, documented).
        formula_open, formula_close = formula_window_eet(d)
        if truth_open != formula_open or truth_close != formula_close:
            mismatches_found.append((d, truth_open, truth_close, formula_open, formula_close))
        d += timedelta(days=1)

    print(f"Checked {total} days ({start} .. {end}).")
    if not mismatches_found:
        print("OK: formula matches zoneinfo ground truth on EVERY calendar day tested.")
    else:
        print(f"MISMATCH on {len(mismatches_found)} day(s):")
        for d, to_, tc, fo, fc in mismatches_found[:30]:
            print(f"  {d}: truth=({to_},{tc})  formula=({fo},{fc})")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
