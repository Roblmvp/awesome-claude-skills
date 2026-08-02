#!/usr/bin/env python3
"""Validate skill metadata and public-repository safety using stdlib only."""
import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SKILL=ROOT/"career-opportunity-intelligence"
FIRECRAWL_KEY=re.compile(r"fc-[A-Za-z0-9_-]{20,}")
PLACEHOLDERS={"fc-YOUR-API-KEY","fc-..."}
GENERAL_SECRETS=(
 re.compile(r"AKIA[0-9A-Z]{16}"),
 re.compile(r"sk-[A-Za-z0-9]{20,}"),
 re.compile(r"Bearer [A-Za-z0-9._-]{20,}"),
)
PRIVATE_FIXTURE_PATTERNS=(re.compile(r"\brob\b",re.I),re.compile(r"roblmvp",re.I),re.compile(r"[\w.+-]+@(?!example\.)[\w.-]+\.[A-Za-z]{2,}"))

def firecrawl_secrets(text): return [m.group(0) for m in FIRECRAWL_KEY.finditer(text) if m.group(0) not in PLACEHOLDERS]
def tracked_files(): return [ROOT/Path(raw.decode()) for raw in subprocess.check_output(["git","ls-files","-z"],cwd=ROOT).split(b"\0") if raw]
def validate_secrets(paths=None):
 hits=[]
 for path in paths or tracked_files():
  if path.is_file():
   text=path.read_text(errors="ignore")
   for value in firecrawl_secrets(text):
    display=path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    hits.append(f"{display}: prohibited Firecrawl credential ({len(value)} characters)")
   for pattern in GENERAL_SECRETS:
    if pattern.search(text):
     display=path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
     hits.append(f"{display}: prohibited general credential pattern")
 if hits: raise ValueError("\n".join(hits))
def validate_fixture_privacy():
 for path in (SKILL/"tests"/"fixtures").glob("*.json"):
  text=path.read_text()
  if any(pattern.search(text) for pattern in PRIVATE_FIXTURE_PATTERNS): raise ValueError(f"candidate-specific data in fixture: {path.relative_to(ROOT)}")
def parse_skill_frontmatter():
 text=(SKILL/"SKILL.md").read_text(); match=re.match(r"^---\n(.*?)\n---\n",text,re.S)
 if not match: raise ValueError("SKILL.md requires frontmatter")
 values={}
 for line in match.group(1).splitlines():
  key,sep,value=line.partition(":")
  if not sep or not value.strip(): raise ValueError("invalid SKILL.md frontmatter")
  values[key.strip()]=value.strip()
 if values.get("name")!=SKILL.name or not values.get("description"): raise ValueError("skill metadata mismatch")
 return values
def parse_openai_yaml():
 lines=(SKILL/"agents"/"openai.yaml").read_text().splitlines()
 if not lines or lines[0]!="interface:": raise ValueError("openai.yaml requires interface")
 values={}
 for line in lines[1:]:
  if not line.startswith("  "): raise ValueError("unsupported openai.yaml structure")
  key,sep,value=line.strip().partition(":")
  if not sep: raise ValueError("invalid openai.yaml")
  try: values[key]=json.loads(value.strip())
  except json.JSONDecodeError as exc: raise ValueError("openai.yaml values must be JSON strings") from exc
 required={"display_name","short_description","default_prompt"}
 if not required <= values.keys() or any(not isinstance(values[k],str) or not values[k] for k in required): raise ValueError("incomplete openai.yaml interface")
 return values
def validate_local_links():
 for path in SKILL.rglob("*.md"):
  for target in re.findall(r"\[[^]]+\]\(([^)]+)\)",path.read_text()):
   if "://" not in target and not (path.parent/target.split("#")[0]).exists(): raise ValueError(f"broken local link: {path}: {target}")
def main():
 parse_skill_frontmatter(); parse_openai_yaml(); validate_local_links(); validate_secrets(); validate_fixture_privacy(); print("metadata and repository controls: valid"); return 0
if __name__=="__main__":
 try: raise SystemExit(main())
 except ValueError as exc: print(f"error: {exc}",file=sys.stderr); raise SystemExit(1)
