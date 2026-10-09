#!/usr/bin/env python3
"""Create directional NDXm MTF templates that do not negate the NY-session gate.

The bilateral mtf_filter skeleton mirrors both condition groups. That is invalid
for PF_NYSessionWindow because it is symmetric and has no mathematical opposite.
The long/short skeletons keep the selected direction's signal as primary instead.
"""

from __future__ import annotations

import copy
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "engine" / "out"
INSTALL = r"C:\SQX_144_Full"
TRIGGER_GROUP = "Breakout_Triggers_NDXm"
LONG_BLOCK = "CBlock_ORBLongBreakout_NYSession"
SHORT_BLOCK = "CBlock_ORBShortBreakout_NYSession"

from engine.generate import from_design

_GROUPS_SPEC = importlib.util.spec_from_file_location(
    "sqx_random_group_engine",
    HERE / ".." / "sqx-random-group" / "engine" / "groups.py",
)
if _GROUPS_SPEC is None or _GROUPS_SPEC.loader is None:
    raise ImportError("Cannot load sqx-random-group engine")
_GROUPS = importlib.util.module_from_spec(_GROUPS_SPEC)
_GROUPS_SPEC.loader.exec_module(_GROUPS)
hybrid_ref = _GROUPS.hybrid_ref
load_blocks = _GROUPS.load_blocks


def restrict_trigger_group(
    template_path: Path,
    output_path: Path,
    block_key: str,
    name: str,
    install_blocks: dict[str, ET.Element],
) -> None:
    with zipfile.ZipFile(template_path) as archive:
        members = {member: archive.read(member) for member in archive.namelist()}
    root = ET.fromstring(members["strategy_Portfolio.xml"])
    group = next(
        group for group in root.iter("Group")
        if group.get("name") == TRIGGER_GROUP
    )
    items = list(group.findall("Item"))
    selected = [item for item in items if item.get("key") == block_key]
    if not selected and block_key in install_blocks:
        selected = [ET.fromstring(hybrid_ref(install_blocks[block_key]))]
    if len(selected) != 1:
        raise ValueError(f"Expected one {block_key} item in {TRIGGER_GROUP}, found {len(selected)}")
    for item in items:
        group.remove(item)
    group.append(copy.deepcopy(selected[0]))
    for element in root.iter("StrategyName"):
        element.text = name
    strategy = root.find("Strategy")
    if strategy is not None:
        strategy.set("name", name)
    ET.indent(root, space="  ")
    members["strategy_Portfolio.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for member, data in members.items():
            archive.writestr(member, data)


def main() -> None:
    designs = [
        ("mtf_filter_long", "NDXm_ORB_MTF_LONG_BASE", "NDXm_ORB_MTF_LONG.sqx", LONG_BLOCK),
        ("mtf_filter_short", "NDXm_ORB_MTF_SHORT_BASE", "NDXm_ORB_MTF_SHORT.sqx", SHORT_BLOCK),
    ]
    for shape, generated_name, output_name, block_key in designs:
        result = from_design(
            {
                "name": generated_name,
                "shape": shape,
                "daily_filter": "PropFirmComplianceFilters_NDXm",
                "trigger": TRIGGER_GROUP,
                "price_pool": "Levels_ORB_NDXm",
            },
            install=INSTALL,
            outdir=str(OUT_DIR),
        )
        base = Path(result)
        output = OUT_DIR / output_name
        blocks = load_blocks(Path(INSTALL) / "user" / "settings" / "customBlocks.xml")
        restrict_trigger_group(base, output, block_key, output.stem, blocks)
        print(f"wrote {output} with trigger {block_key}")


if __name__ == "__main__":
    main()
