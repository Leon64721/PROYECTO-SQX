import re, shutil, zipfile, sys
from pathlib import Path
from datetime import datetime

SQX = Path("C:/SQX_144_Full")
SRC_CFX = SQX / "user/projects/ORB_SIMPLE_V1/project.cfx"
NEW_PROJ = SQX / "user/projects/ORB_V7_FIXED"
WORK = Path(r"C:\Users\LEON6\AppData\Local\Temp\v7_work")
BLOCKS = SQX / "user/settings/customBlocks.xml"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def sub_count(text, pattern, repl, expected, label, flags=0):
    new, n = re.subn(pattern, repl, text, flags=flags)
    print(f"  [{label}] reemplazos: {n} (esperado {expected})")
    if n != expected:
        sys.exit(f"ABORT: {label} -> {n} != {expected}")
    return new

# ---------- FIX 1: cablear #Int1#..#Int4# al SessionHigh/SessionLow interno ----------
print("FIX 1 - customBlocks.xml (cableado de parametros)")
bak = BLOCKS.with_name(f"customBlocks.xml.bak_{STAMP}")
shutil.copy2(BLOCKS, bak)
print(f"  backup: {bak}")
xml = BLOCKS.read_text(encoding="utf-8")
wire = {"#StartHours#": "#Int1#", "#StartMinutes#": "#Int2#", "#EndHours#": "#Int3#", "#EndMinutes#": "#Int4#"}
for inner, outer in wire.items():
    # <Param key="#StartHours#" ... builderStep="1">8</Param>  ->  ... builderStep="1" customParam="true" value="#Int1#">#Int1#</Param>
    pat = r'(<Param key="' + re.escape(inner) + r'"[^>]*?builderStep="1")>[0-9]+</Param>'
    xml = sub_count(xml, pat, r'\1 customParam="true" value="' + outer + '">' + outer + '</Param>', 2, f"{inner}->{outer}")
BLOCKS.write_text(xml, encoding="utf-8")
print(f"  verificacion: value=\"#Int1#\" aparece {xml.count('value=\"#Int1#\"')} veces (esperado 2)")

# ---------- Extraer .cfx ----------
if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)
with zipfile.ZipFile(SRC_CFX) as z:
    names = z.namelist()
    z.extractall(WORK)
print(f"\ncfx extraido: {len(names)} entradas")

# ---------- FIX 2: Build precision 1 -> 2, ventana ORB fija 16:30-17:00, senales desde 17:00, max 2 trades/dia ----------
print("FIX 2 - Build-Task1.xml")
b = (WORK / "Build-Task1.xml").read_text(encoding="utf-8")
b = sub_count(b, r'(<Setup dateFrom="2018\.06\.27" dateTo="2023\.01\.01" testPrecision=)"1"', r'\1"2"', 1, "testPrecision main 1->2")
b = sub_count(b, r'(<Param key="#Int2#" name="Range Start Minute"[^>]*minValue=)"0" maxValue="59"', r'\1"30" maxValue="30"', 2, "Int2 minuto inicio fijo 30")
b = sub_count(b, r'(<Param key="#Int3#" name="Range End Hour"[^>]*minValue=)"16" maxValue="17"', r'\1"17" maxValue="17"', 2, "Int3 hora fin fija 17")
b = sub_count(b, r'(<Param key="#Int4#" name="Range End Minute"[^>]*minValue=)"0" maxValue="59"', r'\1"0" maxValue="0"', 2, "Int4 minuto fin fijo 0")
b = sub_count(b, r'(<Param key="SignalTimeRangeFrom" className="LimitTimeRange">)59400<', r'\g<1>61200<', 1, "senales desde 17:00 (fin del rango)")
b = sub_count(b, r'(<Param key="MaxTradesPerDay" className="MaxTradesPerDay">)0<', r'\g<1>2<', 1, "MaxTradesPerDay 0->2")
(WORK / "Build-Task1.xml").write_text(b, encoding="utf-8")

# ---------- FIX 3: umbral OOS AvgTrade $1.50 -> $0.15 (0.01 lotes) ----------
print("FIX 3 - Retest-Task1.xml (OOS)")
r = (WORK / "Retest-Task1.xml").read_text(encoding="utf-8")
pat = r'(class="AvgTrade" />\s*</Left-Side>\s*<Comparator value="&gt;" />\s*<Right-Side valueType="numeric">\s*<Numeric-Value value=)"1\.5(0)?"'
r = sub_count(r, pat, r'\1"0.15"', 1, "AvgTrade OOS 1.5->0.15", flags=re.S)
(WORK / "Retest-Task1.xml").write_text(r, encoding="utf-8")

# ---------- Empaquetar proyecto nuevo ----------
NEW_PROJ.mkdir(parents=True, exist_ok=True)
out = NEW_PROJ / "project.cfx"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.write(WORK / n, arcname=n)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    print(f"\nOK -> {out}  ({out.stat().st_size} bytes, {len(z.namelist())} entradas)")
