import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SKILL=ROOT/"career-opportunity-intelligence"; FIX=SKILL/"tests"/"fixtures"; sys.path.insert(0,str(SKILL/"scripts"))
def load(name): return json.loads((FIX/name).read_text())
def jobs():
 from career_intelligence.normalize import normalize_jobs
 return normalize_jobs(load("synthetic-jobs.json"))
