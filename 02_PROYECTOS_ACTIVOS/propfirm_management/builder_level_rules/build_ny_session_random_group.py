"""build_ny_session_random_group.py — Random Group wrapping PF_NYSessionWindow
as a pool the Builder can genetically combine with ANY future entry signal
(not just ORB), using the sqx-random-group skill's HYBRID reference mode.

Why this is separate from the ORB-compound blocks (build_orb_ny_compound_blocks.py):
those are drop-in replacements for the ORB entry pair specifically. This Random
Group is the general mechanism described in
`02_PROYECTOS_ACTIVOS\\propfirm_management\\README.md`: a "Same condition" pool of
prop-firm compliance filters that ANY strategy template can pull from and AND
into its entry chain. Today the pool has one member (PF_NYSessionWindow); as
more compliance blocks are built (news restriction, trades-per-day) they get
added to this same group with no other changes needed downstream.

hybrid_ref() re-exports a block BY REFERENCE (bare CBlock_* pointer, no
<Contents> — AlgoWizard re-resolves the rule body at import from the already-
imported Custom Block). It needs the actual <Item> XML element of the block,
which we already generated ourselves in build_ny_session_block.py — no need to
re-bootstrap the random-group catalog against the live install first.

Prereq: PF_NYSessionWindow must already be imported into AlgoWizard's Custom
Blocks (Editor > Custom blocks > Import out_ny_session.xml) BEFORE importing
this group's XML, otherwise AlgoWizard has no CBlock_PF_NYSessionWindow to
resolve the reference against.

Run:
  python build_ny_session_random_group.py out_ny_session.xml out_ny_session_group.xml
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RG_ROOT = Path(r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-random-group")
sys.path.insert(0, str(RG_ROOT))

from engine.groups import hybrid_ref, make_group, wrap_groups  # noqa: E402


def build(blocks_xml_path: str) -> list[str]:
    tree = ET.parse(blocks_xml_path)
    items = {item.get("key"): item for item in tree.getroot().findall("Item")}

    target_key = "CBlock_PF_NYSessionWindow"
    if target_key not in items:
        raise SystemExit(f"{target_key} not found in {blocks_xml_path}")

    group = make_group(
        "PropFirmComplianceFilters_NDXm",
        "Condition",
        [hybrid_ref(items[target_key])],
        category="PropFirmCompliance_user",
    )
    return [group]


def main(argv):
    blocks_xml = argv[0] if argv else "out_ny_session.xml"
    out_path = argv[1] if len(argv) > 1 else "out_ny_session_group.xml"
    groups = build(blocks_xml)
    Path(out_path).write_text(wrap_groups(groups), encoding="utf-8")
    print(f"wrote {out_path}  ({len(groups)} group)")
    print(f"validate with:\n  python {RG_ROOT}\\engine\\validate.py {out_path} --catalog {RG_ROOT}\\catalog.json")


if __name__ == "__main__":
    main(sys.argv[1:])
