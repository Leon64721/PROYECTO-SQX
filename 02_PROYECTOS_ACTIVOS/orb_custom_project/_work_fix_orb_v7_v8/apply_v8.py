import re, shutil, zipfile, sys
from pathlib import Path

SQX = Path("C:/SQX_144_Full")
SRC = SQX / "user/projects/ORB_V7_FIXED/project.cfx"      # V7 vivo (ya con M5 y precision 2)
NEW = SQX / "user/projects/ORB_V8_AVGTRADE_SL/project.cfx"
WORK = Path(r"C:\Users\LEON6\AppData\Local\Temp\v8_work")

def sub_count(text, pattern, repl, expected, label, flags=0):
    new, n = re.subn(pattern, repl, text, flags=flags)
    print(f"  [{label}] reemplazos: {n} (esperado {expected})")
    if n != expected:
        sys.exit(f"ABORT: {label} -> {n} != {expected}")
    return new

if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)
with zipfile.ZipFile(SRC) as z:
    names = z.namelist()
    z.extractall(WORK)
print(f"cfx V7 extraido: {len(names)} entradas")

print("V8-a  Build-Task1.xml: SL minimo 1.0 -> 2.0 ATR, PT minimo 1.2 -> 2.0 ATR")
b = (WORK / "Build-Task1.xml").read_text(encoding="utf-8")
b = sub_count(b, r"<MinSLATRMultiple>1\.0</MinSLATRMultiple>", "<MinSLATRMultiple>2.0</MinSLATRMultiple>", 1, "MinSLATRMultiple")
b = sub_count(b, r"<MinPTATRMultiple>1\.2</MinPTATRMultiple>", "<MinPTATRMultiple>2.0</MinPTATRMultiple>", 1, "MinPTATRMultiple")
(WORK / "Build-Task1.xml").write_text(b, encoding="utf-8")

print("V8-b  Retest-Task1.xml (OOS): AvgTrade 0.15 -> 0.05")
r = (WORK / "Retest-Task1.xml").read_text(encoding="utf-8")
pat = r'(class="AvgTrade" />\s*</Left-Side>\s*<Comparator value="&gt;" />\s*<Right-Side valueType="numeric">\s*<Numeric-Value value=)"0\.15"'
r = sub_count(r, pat, r'\1"0.05"', 1, "AvgTrade OOS", flags=re.S)
(WORK / "Retest-Task1.xml").write_text(r, encoding="utf-8")

NEW.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(NEW, "w", zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.write(WORK / n, arcname=n)
with zipfile.ZipFile(NEW) as z:
    assert z.testzip() is None
    print(f"OK -> {NEW} ({NEW.stat().st_size} bytes, {len(z.namelist())} entradas)")
