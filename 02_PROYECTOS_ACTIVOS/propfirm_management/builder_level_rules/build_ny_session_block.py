r"""build_ny_session_block.py — generates the NY cash-session compliance block
for NDXm (prop-firm item #2: session-time restriction, DST-aware).

Design (verified against real IANA tz data in verify_ny_session_formula.py —
2,557 days, 2024-2031, zero mismatches):

  NDXm's declared feed timezone is EET (Europe/Bucharest DST rule: last Sunday
  of March -> last Sunday of October). NY cash session is 09:30-16:00
  America/New_York (US DST rule: 2nd Sunday of March -> 1st Sunday of Nov).
  Because the two DST calendars don't switch on the same date, there are two
  short "mismatch" windows per year (~mid-March, ~late-Oct/early-Nov) where the
  EET-ET offset is 6h instead of the nominal 7h, which shifts the EET session
  window by exactly 1 hour:
    - nominal (both regions same DST state):  16:30 - 23:00 EET
    - mismatch (regions disagree on DST):      15:30 - 22:00 EET

  All calendar math is expressed with ONLY the primitives AlgoWizard actually
  has (no NOT, no direct equality) via BarMonth / BarDayOfMonth / BarDayOfWeek
  (Sunday=0) and the `recentSundayOfMonth = DayOfMonth - DayOfWeek` trick:
    - 2nd-Sunday-of-month boundary  <=>  recentSunday in [8, 14]-ish -> use >=8 / <8
    - last-Sunday-of-month boundary <=>  recentSunday in [25, 31]   -> use >=25 / <25
    - 1st-Sunday-of-month boundary  <=>  recentSunday in [1, 7]     -> use >=1  / <1

  mismatch = (Mar, recentSunday in [8,24]) OR (Oct, recentSunday>=25) OR (Nov, recentSunday<1)
  nominal  = (Jan|Feb|Dec) OR (Mar, recentSunday<8) OR (Mar, recentSunday>24)
             OR (Apr..Sep) OR (Oct, recentSunday<25) OR (Nov, recentSunday>=1)

  Every atom is read at shift=1 (this install's established convention for
  Bar&Time atoms, see examples/gen_complex_breakout.py — categoryType="other",
  exempt from the shift=0 look-ahead guard but consistently emitted at shift 1
  across the existing block set).

Run:
  python build_ny_session_block.py catalog.json out_ny_session.xml
  (catalog.json path: ..\..\..\.claude\skills\sqx-custom-block\catalog.json)
"""

from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-custom-block")
sys.path.insert(0, str(SKILL_ROOT))

from engine.emit import Catalog
from engine.grammar import (
    and_op, or_op, is_greater, is_lower, minus,
    make_block, esc, wrap_batch,
)

SHIFT = "1"


def eq(atom_expr: str, k: int) -> str:
    """x == k, built from IsGreater/IsLower since AlgoWizard has no equality op."""
    return and_op(is_greater(atom_expr, str(k - 1)), is_lower(atom_expr, str(k + 1)))


def between(atom_expr: str, lo: int, hi: int) -> str:
    """lo <= x <= hi, inclusive both ends (built from strict > lo-1 and < hi+1)."""
    return and_op(is_greater(atom_expr, str(lo - 1)), is_lower(atom_expr, str(hi + 1)))


def at_least(atom_expr: str, k: int) -> str:
    """x >= k"""
    return is_greater(atom_expr, str(k - 1))


def less_than(atom_expr: str, k: int) -> str:
    """x < k"""
    return is_lower(atom_expr, str(k))


def ny_session_contents(cat: Catalog) -> str:
    """Returns the DST-aware NY-session boolean tree (shared by the standalone
    compliance block and the ORB-compound blocks in build_orb_ny_compound_blocks.py)."""
    month = cat.atom("BarMonth", shift=SHIFT)
    day_of_month = cat.atom("BarDayOfMonth", shift=SHIFT)
    day_of_week = cat.atom("BarDayOfWeek", shift=SHIFT)
    hour = cat.atom("BarHour", shift=SHIFT)
    minute = cat.atom("BarMinute", shift=SHIFT)
    recent_sunday = minus(day_of_month, day_of_week)  # DayOfMonth - DayOfWeek(Sunday=0)

    # --- calendar branches (mutually exclusive, jointly exhaustive - proven in
    #     verify_ny_session_formula.py) ---------------------------------------
    mismatch_calendar = or_op(
        and_op(eq(month, 3), between(recent_sunday, 8, 24)),
        and_op(eq(month, 10), at_least(recent_sunday, 25)),
        and_op(eq(month, 11), less_than(recent_sunday, 1)),
    )
    nominal_calendar = or_op(
        eq(month, 1), eq(month, 2), eq(month, 12),
        and_op(eq(month, 3), less_than(recent_sunday, 8)),
        and_op(eq(month, 3), at_least(recent_sunday, 25)),
        between(month, 4, 9),
        and_op(eq(month, 10), less_than(recent_sunday, 25)),
        and_op(eq(month, 11), at_least(recent_sunday, 1)),
    )

    # --- hour:minute window tests (half-hour boundaries) --------------------
    def at_or_after(h: int, m: int) -> str:
        # Hour > h  OR  (Hour == h AND Minute >= m)
        return or_op(
            at_least(hour, h + 1),
            and_op(eq(hour, h), at_least(minute, m)),
        )

    def before(h: int) -> str:
        # session close is always on the hour -> simply Hour < h
        return less_than(hour, h)

    mismatch_window = and_op(at_or_after(15, 30), before(22))
    nominal_window = and_op(at_or_after(16, 30), before(23))

    return or_op(
        and_op(mismatch_calendar, mismatch_window),
        and_op(nominal_calendar, nominal_window),
    )


def build(cat: Catalog) -> list[str]:
    contents = ny_session_contents(cat)

    block = make_block(
        key="CBlock_PF_NYSessionWindow",
        name="PF_NYSessionWindow",
        display=esc(
            "Bar time is inside NYSE cash session (09:30-16:00 America/New_York), "
            "DST-aware, expressed in the chart's EET clock"
        ),
        category="PropFirmCompliance_user",
        help_text=esc(
            "Prop-firm compliance gate (symmetric, non-directional): true only when the "
            "current bar's EET clock time falls inside the real NYSE cash session "
            "(09:30-16:00 America/New_York), correctly adjusted for the fact that the US "
            "and EU switch DST on different calendar dates. Two mutually exclusive "
            "calendar branches: 'mismatch' (US/EU disagree on DST, ~mid-March and "
            "~late-Oct/early-Nov) uses 15:30-22:00 EET; 'nominal' (both regions same DST "
            "state) uses 16:30-23:00 EET. Verified against zoneinfo/IANA ground truth for "
            "2024-2030 (see verify_ny_session_formula.py) with zero mismatches. Built for "
            "NDXm (feed timezone EET). AND this block into an entry-rule chain so the "
            "Builder cannot generate/survive a variant that trades outside the legal "
            "session window."
        ),
        opposite="CBlock_null",  # symmetric: applies identically regardless of trade direction
        params="",
        contents=contents,
    )
    return [block]


def main(argv):
    catalog_path = argv[0] if argv else str(SKILL_ROOT / "catalog.json")
    out_path = argv[1] if len(argv) > 1 else "out_ny_session.xml"
    cat = Catalog(catalog_path)
    xml = wrap_batch(build(cat))
    Path(out_path).write_text(xml, encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"validate with:\n  python {SKILL_ROOT}\\engine\\validate.py {out_path} --catalog {catalog_path}")


if __name__ == "__main__":
    main(sys.argv[1:])
