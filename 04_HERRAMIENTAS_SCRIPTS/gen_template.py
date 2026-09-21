import sys
import os

sys.path.insert(0, r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-strategy-template\engine')
from generate import from_design

designs = [
    {
        "name": "NDXm_NY_Session_Template", 
        "shape": "market",
        "filter": "PropFirmComplianceFilters_NDXm", 
        "trigger": "Breakout_Triggers_NDXm",
        "thesis": "Compliance filter restricts entries to NY Session, and breakout triggers catch the momentum during the session."
    }
]

def build():
    install = r"C:\SQX_144_Full"
    for d in designs:
        print(f"Generating {d['name']}...")
        from_design(d, install, outdir=".")
    print("Done generating template.")

if __name__ == '__main__':
    build()