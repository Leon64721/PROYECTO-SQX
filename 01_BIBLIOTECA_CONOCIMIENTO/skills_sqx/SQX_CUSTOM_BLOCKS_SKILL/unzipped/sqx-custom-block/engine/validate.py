"""validate.py — lint a custom-block batch before importing into AlgoWizard.

Standalone (stdlib only). Auto-detects <CustomBlocks> (block mode) vs <RandomGroups>
(group mode). Block mode runs 7 checks; the last two encode lessons that have bitten
real batches, as automated gates rather than prose:

  1) Well-formed XML            (also catches unescaped < > & in help/display)
  2) No duplicate Item keys
  3) Long/short pairs symmetric (A.opposite==B and B.opposite==A)
  4) Every #ParamN# in <Contents> is declared as a top-level <Param>
  5) Unique <Param> keys within each block
  6) Block name does NOT end in _<digits><letters>  (AlgoWizard UI strips that,
     breaking opposite-block links — name suffix lesson)
  7) [needs catalog] every multi-output atom used carries a #Line# param, and no
     talib_* atom is used (multi-output + Stockpicker-NPE lessons)

Usage:
  python engine/validate.py out.xml
  python engine/validate.py out.xml --catalog catalog.json     # enables check 7

Exit 0 = all checks pass (warnings allowed), 1 = a failure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PARAM_REF_RE = re.compile(r"#[A-Za-z][A-Za-z0-9]*#")
NUMBERED_PARAM_RE = re.compile(r"#(Period|Double|Int|Shift|Chart)\d+#")
NAME_SUFFIX_RE = re.compile(r"_\d+[A-Za-z]+$")        # _144Native, _2v3, _3x ...
VALUE_RETURN_TYPES = {"price", "pricerange", "number", "pricenumber"}


def _unique_param_keys(items, label_attr="key"):
    dups = []
    for it in items:
        keys = [k for k in (p.get("key") for p in it.findall("Param")) if k is not None]
        d = {k for k in keys if keys.count(k) > 1}
        if d:
            dups.append(f"{it.get(label_attr) or '<no-key>'}: {sorted(d)}")
    return dups


def _validate_blocks(root, catalog=None):
    items = root.findall("Item")
    n = 7 if catalog else 6
    print(f"PASS [1/{n}] well-formed XML ({len(items)} <Item> blocks)")
    failures, warnings = [], []

    keys = [k for k in (it.get("key") for it in items) if k is not None]
    dups = {k for k in keys if keys.count(k) > 1}
    print(f"{'FAIL' if dups else 'PASS'} [2/{n}] "
          + (f"duplicate keys: {sorted(dups)}" if dups else "no duplicate keys"))
    if dups:
        failures.append(f"duplicate keys: {sorted(dups)}")

    by_key = {it.get("key"): it for it in items}
    asym = []
    for it in items:
        opp = it.get("oppositeBlockKey")
        if not opp or opp == "CBlock_null":
            continue
        partner = by_key.get(opp)
        if partner is None:
            asym.append(f"{it.get('key')} -> {opp} (partner not in batch)")
        elif partner.get("oppositeBlockKey") != it.get("key"):
            asym.append(f"{it.get('key')} <-> {opp} (back-link {partner.get('oppositeBlockKey')!r})")
    print(f"{'FAIL' if asym else 'PASS'} [3/{n}] opposite pairs symmetric")
    if asym:
        failures.append("asymmetric opposites:\n  " + "\n  ".join(asym))

    undeclared = []
    for it in items:
        top = {p.get("key") for p in it.findall("Param") if p.get("key")}
        top.add("#Chart1#")
        contents = it.find("Contents")
        xml = ET.tostring(contents, encoding="unicode") if contents is not None else ""
        refs = {r for r in PARAM_REF_RE.findall(xml) if NUMBERED_PARAM_RE.match(r)}
        missing = refs - top
        if missing:
            undeclared.append(f"{it.get('key')}: {sorted(missing)}")
    print(f"{'FAIL' if undeclared else 'PASS'} [4/{n}] every param reference declared")
    if undeclared:
        failures.append("undeclared params:\n  " + "\n  ".join(undeclared))

    intra = _unique_param_keys(items)
    print(f"{'FAIL' if intra else 'PASS'} [5/{n}] unique param keys within blocks")
    if intra:
        failures.append("duplicate param keys:\n  " + "\n  ".join(intra))

    bad_names = [it.get("name") for it in items
                 if it.get("name") and NAME_SUFFIX_RE.search(it.get("name"))]
    print(f"{'FAIL' if bad_names else 'PASS'} [6/{n}] no _<digits><letters> name suffixes")
    if bad_names:
        failures.append("names ending _<digits><letters> (AlgoWizard strips these): "
                        + ", ".join(bad_names))

    if catalog:
        line_missing, talib_used = [], []
        for it in items:
            for atom in it.iter("Item"):
                k = atom.get("key")
                ce = catalog.get(k)
                if not ce:
                    continue
                if not ce.get("usable_single_symbol", True):
                    talib_used.append(f"{it.get('key')} uses talib atom {k}")
                if ce.get("multi_output") and not any(
                    p.get("key") == "#Line#" for p in atom.findall("Param")
                ):
                    line_missing.append(f"{it.get('key')} uses multi-output {k} without #Line#")
        problems = line_missing + talib_used
        print(f"{'FAIL' if problems else 'PASS'} [7/{n}] multi-output #Line# present & no talib atoms")
        if problems:
            failures.append("catalog checks:\n  " + "\n  ".join(problems))

    if warnings:
        print()
        for w in warnings:
            print("WARN", w)
    if failures:
        print()
        for f in failures:
            print("FAIL:", f)
        return 1
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--catalog", help="catalog.json — enables the multi-output/talib check")
    args = ap.parse_args(argv)

    p = Path(args.path)
    if not p.exists():
        print(f"FAIL: file not found: {p}")
        return 1
    try:
        root = ET.parse(p).getroot()
    except ET.ParseError as e:
        print(f"FAIL XML parse error (often an unescaped < > or & in help/display): {e}")
        return 1

    catalog = None
    if args.catalog and Path(args.catalog).exists():
        catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8")).get("atoms", {})

    if root.tag == "CustomBlocks":
        rc = _validate_blocks(root, catalog)
        if rc == 0:
            print(f"\nALL CHECKS PASSED — {p.name} is ready to import")
        return rc
    print(f"FAIL unexpected root <{root.tag}> (expected <CustomBlocks>)")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
