import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_ROOT))

from engine.emit import Catalog

cat = Catalog("catalog.json")
print(cat.atom("SessionHigh"))
