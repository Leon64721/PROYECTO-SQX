r"""discover.py — find the user's StrategyQuant X installation and its catalog files.

This is the one-time "identify your SQX folder" step. An SQX install keeps the three
files the skill needs at fixed sub-paths under the install root, so the user never has
to hunt for them — point at the install root (or let discovery find it) and the rest is
derived:

  <install>/internal/web/SQWIZARD/branding/global/config.xml              (native vocab)
  <install>/internal/web/SQWIZARD/branding/global/UserCustomIndicators.xml (custom registry)
  <install>/user/settings/customBlocks.xml                                 (their custom blocks)

Usage:
  python engine/discover.py                 # search common locations, print what's found
  python engine/discover.py --json          # machine-readable (for the skill to consume)
  python engine/discover.py --install C:\StrategyQuantX144   # resolve a known root
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# files the skill needs, relative to the install root
SUBPATHS = {
    "config": Path("internal/web/SQWIZARD/branding/global/config.xml"),
    "user_indicators": Path("internal/web/SQWIZARD/branding/global/UserCustomIndicators.xml"),
    "export": Path("user/settings/customBlocks.xml"),
    # the user's OWN coded/imported custom indicators live as .java sources somewhere under
    # user/extend (typically Snippets/SQ/Blocks/Indicators/<Name>/<Name>.java, but the package
    # path varies and imported packs land in their own folders). We point at the WHOLE
    # user/extend tree and let bootstrap search it recursively, keeping every .java that has a
    # @BuildingBlock and is not a ConditionBlock/FunctionBlock — so custom indicators are found
    # no matter which subfolder they sit in.
    "snippets": Path("user/extend"),
}


def resolve_install(root: Path) -> dict:
    """Given an install root, resolve the three files (those that exist)."""
    info: dict = {"root": str(root)}
    for name, sub in SUBPATHS.items():
        p = root / sub
        info[name] = str(p) if p.exists() else None
    info["is_sqx_install"] = info["config"] is not None
    return info


def count_config_customs(config_path: str | None) -> int:
    """How many of the user's OWN custom indicators are registered in config.xml.

    The robust, machine-independent signal: SQX stamps every imported/coded indicator the
    user has registered with customSnippet="true". We count the value-indicator Items that
    carry it (categoryType="indicator"). This number does NOT depend on the .java source
    being present on disk — so a machine that has the indicators registered but not their
    source still reports them, instead of a misleading "0". (bootstrap.py reports the exact
    same set, plus anything from exports / .java / registry.)"""
    if not config_path:
        return 0
    try:
        text = Path(config_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    n = 0
    for tag in re.findall(r"<Item\b[^>]*?>", text):
        if 'customSnippet="true"' in tag and 'categoryType="indicator"' in tag:
            n += 1
    return n


def count_java_snippets(snippets_dir: str | None) -> int:
    """How many coded custom-indicator .java VALUE files sit under user/extend (a secondary,
    source-present-only signal). ConditionBlock/FunctionBlock companions are excluded."""
    if not snippets_dir:
        return 0
    n = 0
    try:
        for j in Path(snippets_dir).rglob("*.java"):
            t = j.read_text(encoding="utf-8", errors="replace")
            if ("@BuildingBlock" in t
                    and "extends ConditionBlock" not in t
                    and "extends FunctionBlock" not in t):
                n += 1
    except OSError:
        return 0
    return n


def _candidate_parents() -> list[Path]:
    home = os.environ.get("USERPROFILE") or os.environ.get("HOME") or ""
    raw = [
        home, os.path.join(home, "Documents"), os.path.join(home, "Applications"),
        "C:/", "C:/Program Files", "C:/Program Files (x86)",
        "D:/", "/Applications", "/opt",
        os.environ.get("LOCALAPPDATA", ""), os.environ.get("APPDATA", ""),
    ]
    seen, out = set(), []
    for r in raw:
        if r and r not in seen:
            seen.add(r)
            p = Path(r)
            if p.exists():
                out.append(p)
    return out


def find_installs(extra_roots: list[str] | None = None) -> list[dict]:
    """Search common locations for SQX installs (folders named StrategyQuant* that resolve
    to a real install). Returns one info dict per install found."""
    installs, seen = [], set()
    parents = _candidate_parents()
    for parent in parents:
        try:
            matches = list(parent.glob("StrategyQuant*")) + list(parent.glob("strategyquant*"))
        except OSError:
            continue
        for d in matches:
            if d.is_dir():
                info = resolve_install(d)
                if info["is_sqx_install"] and info["root"] not in seen:
                    seen.add(info["root"])
                    installs.append(info)
    for r in (extra_roots or []):
        info = resolve_install(Path(r))
        if info["is_sqx_install"] and info["root"] not in seen:
            seen.add(info["root"])
            installs.append(info)
    return installs


def main(argv) -> int:
    try:                                    # never crash on a non-UTF-8 console codepage
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Find the SQX install and its catalog files.")
    ap.add_argument("--install", help="resolve a known install root instead of searching")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    installs = [resolve_install(Path(args.install))] if args.install else find_installs()

    if args.json:
        print(json.dumps(installs, indent=1))
        return 0 if installs and installs[0]["is_sqx_install"] else 1

    if not installs or not any(i["is_sqx_install"] for i in installs):
        print("No StrategyQuant X install found in the usual places.")
        print("Ask the user for their install folder, then re-run:")
        print("  python engine/discover.py --install <folder>")
        return 1

    print(f"Found {len(installs)} StrategyQuant install(s):\n")
    for i in installs:
        n_cfg = count_config_customs(i.get("config"))
        n_snip = count_java_snippets(i.get("snippets"))
        print(f"  {i['root']}")
        print(f"    config.xml              : {'OK' if i['config'] else 'missing'}")
        print(f"    UserCustomIndicators.xml: {'OK' if i['user_indicators'] else 'missing'}")
        print(f"    customBlocks.xml (export): {'OK' if i['export'] else 'missing (no custom blocks yet)'}")
        print(f"    YOUR custom indicators  : {n_cfg} registered in config"
              + (f" (+ {n_snip} coded .java source file(s) on disk)" if n_snip else ""))
    print("\nYour custom indicators are recognised from config.xml's customSnippet marker —")
    print("they are found whether or not the .java source is present on this machine.")
    print("\nThese are SUGGESTIONS only — CONFIRM the correct folder WITH THE USER before")
    print("building (do not auto-adopt). Then build the catalog from the confirmed folder:")
    print(f"  python engine/bootstrap.py --install \"{installs[0]['root']}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
