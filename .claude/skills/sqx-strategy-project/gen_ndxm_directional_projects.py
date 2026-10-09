#!/usr/bin/env python3
"""Create long-only and short-only NDXm MTF + SP500 project candidates.

The V4 project is structurally sound but its bilateral template asks SQX to
negate the symmetric PF_NYSessionWindow block. These candidates keep the V4
pipeline and price blocks while switching only the Build template and output
databank for each direction.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "out" / "NDXm_ORB_PropFirm_V4_SP500_MTF_ROBUSTEZ" / "project.cfx"
TEMPLATE_DIR = Path(r"C:\SQX_144_Full\user\settings\StrategyTemplates")
OUT_DIR = HERE / "out"

PROJECTS = [
    ("NDXm_ORB_PropFirm_V5_LONG_SP500_MTF", "NDXm_ORB_MTF_LONG.sqx"),
    ("NDXm_ORB_PropFirm_V5_SHORT_SP500_MTF", "NDXm_ORB_MTF_SHORT.sqx"),
]


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"V4 source project not found: {SOURCE}")
    with zipfile.ZipFile(SOURCE) as archive:
        source_members = {name: archive.read(name) for name in archive.namelist()}

    for project_name, template_name in PROJECTS:
        members = dict(source_members)
        build = members["Build-Task1.xml"].decode("utf-8")
        build, count = re.subn(
            r'(<StrategyType\b[^>]*templateFile=")[^"]+(")',
            lambda match: match.group(1) + str(TEMPLATE_DIR / template_name) + match.group(2),
            build,
            count=1,
        )
        if count != 1:
            raise ValueError("Build task does not contain exactly one StrategyType templateFile")
        build, count = re.subn(
            r'(<Databank label="Output databank" name="Output" value=")[^"]+(")',
            lambda match: match.group(1) + f"BS-{project_name}" + match.group(2),
            build,
            count=1,
        )
        if count != 1:
            raise ValueError("Build task does not contain exactly one output databank")
        members["Build-Task1.xml"] = build.encode("utf-8")

        config = members["config.xml"].decode("utf-8")
        config = config.replace("NDXm_ORB_PropFirm_V4_SP500_MTF_ROBUSTEZ", project_name)
        config = config.replace("BS-NDXm_ORB_MTF", f"BS-{project_name}")
        members["config.xml"] = config.encode("utf-8")

        output = OUT_DIR / project_name / "project.cfx"
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in members.items():
                archive.writestr(name, data)
        print(f"Created {output}")


if __name__ == "__main__":
    main()
