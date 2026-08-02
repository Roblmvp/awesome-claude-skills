import json,re,subprocess,unittest
from support import *
class Tests(unittest.TestCase):
 def test_fixture_is_synthetic(self):
  text=" ".join(p.read_text().lower() for p in FIX.glob("*.json")); self.assertNotRegex(text,r"\brob\b|roblmvp"); self.assertNotRegex(text,r"[\w.+-]+@(?!example\.)[\w.-]+")
 def test_private_output_ignored(self):
  p=subprocess.run(["git","check-ignore",".career-intelligence/demo/out.json"],cwd=ROOT,capture_output=True,text=True); self.assertEqual(p.returncode,0,p.stderr)
 def test_no_network_imports(self):
  text=" ".join(p.read_text() for p in (SKILL/"scripts").rglob("*.py")); self.assertNotRegex(text,r"\b(requests|urllib\.request|httpx|socket)\b")
 def test_no_secret_like_values(self):
  patterns=[r"AKIA[0-9A-Z]{16}",r"sk-[A-Za-z0-9]{20,}",r"Bearer [A-Za-z0-9._-]{20,}"]
  for p in SKILL.rglob("*"):
   if p.is_file():
    for pattern in patterns: self.assertIsNone(re.search(pattern,p.read_text(errors="ignore")),str(p))
 def test_monitor_fixture_disabled(self): self.assertFalse(json.loads((SKILL/"assets"/"monitor-definition.example.json").read_text())["enabled"])
