#!/usr/bin/env python3
"""Build the V4 NDXm MTF + SP500 retest candidate from proven donors.

The existing V2 Build is retained as the source of truth for the custom template,
MTF charts, exits, and fixed 0.01 position size. Retest tasks come from the
build-confirmed GBPJPY project because the previous V2 retests were placeholders
with incorrect input/output databank wiring. V4 also enables the four global
stop/limit price levels required by the EnterAtStop price pool.
"""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path


INSTALL = Path(r"C:\SQX_144_Full")
SOURCE = INSTALL / r"user\projects\NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ\project.cfx"
RETEST_DONOR = INSTALL / r"user\projects\GBPJPY_nico66fxPRO_V2\project.cfx"
OUT = Path(__file__).parent / "out" / "NDXm_ORB_PropFirm_V4_SP500_MTF_ROBUSTEZ" / "project.cfx"

MAIN = "NDXm_TICK_UTCPlus02"
CROSS = "SP500_TICK_UTCPlus02"
MAIN_CHARTS = (
    '<Chart symbol="NDXm_TICK_UTCPlus02" timeframe="M15" spread="80" />'
    '<Chart symbol="NDXm_TICK_UTCPlus02" timeframe="D1" spread="80" />'
)
CROSS_CHARTS = (
    '<Chart symbol="SP500_TICK_UTCPlus02" timeframe="M15" spread="0" />'
    '<Chart symbol="SP500_TICK_UTCPlus02" timeframe="D1" spread="0" />'
)
PRICE_LEVEL_BLOCKS = (
    "Stop/Limit Price Levels.Highest",
    "Stop/Limit Price Levels.Lowest",
    "Stop/Limit Price Levels.HighD",
    "Stop/Limit Price Levels.LowD",
)


def read_zip(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def replace_setup_charts(xml: str, charts: str, detailed: bool = False) -> str:
    if detailed:
        container = re.search(r'<Setups detailed="true">', xml)
        start = re.search(r"<Setup\b", xml[container.end() :]) if container else None
        if start is not None and container is not None:
            offset = container.end()
            setup_start = offset + re.search(r"<Setup\b", xml[offset:]).start()
        else:
            setup_start = -1
    else:
        main = re.search(r"<Setup\b", xml)
        setup_start = main.start() if main else -1
    if setup_start < 0:
        raise ValueError("Retest task has no expected setup")
    setup_end = xml.find("</Setup>", setup_start)
    if setup_end < 0:
        raise ValueError("Retest setup is not closed")
    setup = xml[setup_start:setup_end]
    setup = re.sub(r"<Chart\b[^>]*/>", "", setup)
    setup = setup.replace(">", ">" + charts, 1)
    return xml[:setup_start] + setup + xml[setup_end:]


def replace_resources(xml: str, resources: str) -> str:
    return re.sub(r"<Resources>.*?</Resources>", resources, xml, count=1, flags=re.S)


def enable_price_level_blocks(xml: str) -> str:
    """Enable the exact Price blocks needed by the template's stop-order pool."""
    for key in PRICE_LEVEL_BLOCKS:
        pattern = rf'(<Block key="{re.escape(key)}"[^>]*\buse=")[^"]+(")'
        xml, replaced = re.subn(pattern, r"\g<1>true\2", xml, count=1)
        if replaced != 1:
            raise ValueError(f"Build donor has no configurable Price block {key!r}")
    return xml


def adapt_retest(xml: str, input_db: str, output_db: str, cross_market: bool) -> str:
    xml = xml.replace("\r\n", "\n")
    xml = re.sub(r'engine="[^"]+"', 'engine="MetaTrader5 (hedged)"', xml, count=2)
    xml = replace_setup_charts(xml, MAIN_CHARTS)
    if '<Setups detailed="true">' in xml:
        xml = replace_setup_charts(xml, CROSS_CHARTS, detailed=True)
    xml = xml.replace("EW_TICK_UTCPlus02", CROSS)
    xml = re.sub(
        r'<RetestOnAdditionalMarkets use="[^"]+">',
        f'<RetestOnAdditionalMarkets use="{"true" if cross_market else "false"}">',
        xml,
        count=1,
    )
    if output_db == "Spread_Slippage":
        xml = re.sub(
            r'<MonteCarloRetest use="[^"]+">',
            '<MonteCarloRetest use="true">',
            xml,
            count=1,
        )
    xml = re.sub(r'<StrategyType\b([^>]*)additionalCharts="[^"]+"', r'<StrategyType\1additionalCharts="2"', xml, count=1)
    if "additionalCharts=" not in xml:
        xml = re.sub(r"<StrategyType\b", '<StrategyType additionalCharts="2"', xml, count=1)
    xml = re.sub(r'(<Databank label="Output databank" name="Output" value=")[^"]+(")', rf"\g<1>{output_db}\g<2>", xml, count=1)
    xml = re.sub(r'(<Databank label="Input databank" name="Input" value=")[^"]+(")', rf"\g<1>{input_db}\g<2>", xml, count=1)
    return xml


def main() -> None:
    if not SOURCE.is_file() or not RETEST_DONOR.is_file():
        raise FileNotFoundError("Both the existing V2 project and GBPJPY donor are required")

    source = read_zip(SOURCE)
    donor = read_zip(RETEST_DONOR)
    build = source["Build-Task1.xml"].decode("utf-8").replace("\r\n", "\n")
    build = enable_price_level_blocks(build)

    # Replace the old inactive XAUUSD cross-market setup and resource with SP500.
    build = build.replace("XAUUSD", CROSS)
    build = build.replace('instrument="SP500_TICK_UTCPlus02"', 'instrument="SP500"')
    build = re.sub(
        r'(<RetestOnAdditionalMarkets use=")[^"]+(")',
        r"\1false\2",
        build,
        count=1,
    )
    resources_match = re.search(r"<Resources>.*?</Resources>", build, flags=re.S)
    if resources_match is None:
        raise ValueError("Build task has no Resources section")
    resources = resources_match.group(0)

    stage_sources = [
        ("OOS1", "Retest-Task2.xml", "Results", False),
        ("OOS2", "Retest-Task3.xml", "OOS1", False),
        ("SP500", "Retest-Task2.xml", "OOS2", True),
        ("Spread_Slippage", "Retest-Task6.xml", "SP500", False),
        ("Final_MC", "Retest-Task7.xml", "Spread_Slippage", False),
    ]
    members: dict[str, bytes] = {"Build-Task1.xml": build.encode("utf-8")}
    config = source["config.xml"].decode("utf-8").replace("\r\n", "\n")
    config = re.sub(r"<Tasks>.*?</Tasks>", "<Tasks></Tasks>", config, count=1, flags=re.S)
    config = re.sub(r"<Databanks>.*?</Databanks>", "<Databanks></Databanks>", config, count=1, flags=re.S)

    task_lines = [
        '    <Task type="Build" name="NDXm_ORB_MTF" showSettingsOverview="false" '
        'sampleName="Custom" active="true" taskXMLFile="Build-Task1.xml" '
        'title="BS-NDXm_ORB_MTF" />'
    ]
    databank_lines = [
        '    <Databank name="Results" view="Default - Main data" syncType="Auto-sync never" position="0" />',
        '    <Databank name="Last generation" view="Default - Main data" syncType="Auto-sync never" position="1" />',
        '    <Databank name="Initial population" view="Default - Main data" syncType="Auto-sync never" position="2" />',
        '    <Databank name="Strategies to improve" view="Default - Main data" syncType="Auto-sync never" position="3" />',
        '    <Databank name="Existing portfolio" view="Default - Main data" syncType="Auto-sync never" position="4" />',
        '    <Databank name="BS-NDXm_ORB_MTF" view="Default - Main data" syncType="Auto-sync every 10 minutes" position="1500" />',
    ]
    for index, (name, donor_name, input_db, cross_market) in enumerate(stage_sources, start=1):
        output_db = name
        xml = donor[donor_name].decode("utf-8")
        xml = adapt_retest(xml, input_db, output_db, cross_market)
        xml = replace_resources(xml, resources)
        member = f"Retest-Task{index}.xml"
        members[member] = xml.encode("utf-8")
        task_lines.append(
            f'    <Task type="Retest" name="{name}" showSettingsOverview="false" '
            f'sampleName="Custom" active="true" version="126.2189" title="{name}" '
            f'taskXMLFile="{member}" />'
        )
        databank_lines.append(
            f'    <Databank name="{output_db}" view="Default - Main data" '
                f'syncType="Auto-sync every 1 hour" position="{1500 - index * 100}" />'
        )

    clear = donor["ClearDatabanks-Task8.xml"].replace(
        b'<Databank name="EURJPY" />', b'<Databank name="SP500" />'
    ).replace(
        b'<Databank name="USDJPY" />', b'<Databank name="Spread_Slippage" />'
    ).replace(
        b'<Databank name="Skluz" />', b'<Databank name="Final_MC" />'
    )
    goto = donor["GoToTask-Task9.xml"]
    members["ClearDatabanks-Task6.xml"] = clear
    members["GoToTask-Task7.xml"] = goto.replace(
        b'task="Build strategies"', b'task="NDXm_ORB_MTF"'
    )
    task_lines.extend(
        [
            '    <Task name="Clear intermediate databanks" type="ClearDatabanks" active="false" taskXMLFile="ClearDatabanks-Task6.xml" />',
            '    <Task name="Go To Build" type="GoToTask" active="false" taskXMLFile="GoToTask-Task7.xml" />',
        ]
    )

    config = config.replace("<Tasks></Tasks>", "<Tasks>\n" + "\n".join(task_lines) + "\n  </Tasks>")
    config = config.replace("<Databanks></Databanks>", "<Databanks>\n" + "\n".join(databank_lines) + "\n  </Databanks>")
    config = config.replace("NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ", "NDXm_ORB_PropFirm_V4_SP500_MTF_ROBUSTEZ")
    members["config.xml"] = config.encode("utf-8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in members.items():
            archive.writestr(name, data)

    # Structural checks before any deployment.
    with zipfile.ZipFile(OUT) as archive:
        check = {name: archive.read(name).decode("utf-8", errors="strict") for name in archive.namelist() if name.endswith(".xml")}
    assert "NDXm_ORB_MTF.sqx" in check["Build-Task1.xml"]
    assert check["Build-Task1.xml"].count('Param key="Size" className="FixedSize">0.01') == 1
    for key in PRICE_LEVEL_BLOCKS:
        assert f'<Block key="{key}"' in check["Build-Task1.xml"]
        assert re.search(rf'<Block key="{re.escape(key)}"[^>]*\buse="true"', check["Build-Task1.xml"])
    for name, donor_name, input_db, _ in stage_sources:
        xml = check[f"Retest-Task{stage_sources.index((name, donor_name, input_db, _)) + 1}.xml"]
        assert f'value="{name}"' in xml
        assert f'value="{input_db}"' in xml
        assert "SP500_TICK_UTCPlus02" in xml
        assert "NDXm_TICK_UTCPlus02" in xml
    print(f"Created and verified: {OUT}")
    print("Stages: Results -> OOS1 -> OOS2 -> SP500 -> Spread_Slippage -> Final_MC")
    print("Deployment intentionally not performed; SQX must be closed and the candidate reviewed first.")


if __name__ == "__main__":
    main()
