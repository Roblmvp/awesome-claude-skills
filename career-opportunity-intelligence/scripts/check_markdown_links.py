#!/usr/bin/env python3
import re,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]; failures=[]
for path in (root/"career-opportunity-intelligence").rglob("*.md"):
 for target in re.findall(r"\[[^]]+\]\(([^)]+)\)",path.read_text()):
  if "://" not in target and not (path.parent/target.split("#")[0]).exists(): failures.append(f"{path.relative_to(root)}: {target}")
if failures: print("\n".join(failures),file=sys.stderr); raise SystemExit(1)
