import unittest
from support import *
from career_intelligence.export import render
class Tests(unittest.TestCase):
 def test_json_deterministic(self): self.assertEqual(render(jobs(),"json"),render(jobs(),"json"))
 def test_csv_deterministic(self): self.assertEqual(render(jobs(),"csv"),render(jobs(),"csv"))
 def test_markdown_deterministic(self): self.assertEqual(render(jobs(),"markdown"),render(jobs(),"markdown"))
 def test_ids_and_urls(self):
  for f in ("json","csv","markdown"):
   x=render(jobs(),f); self.assertIn("job-1",x); self.assertIn("careers.example.com",x)
 def test_confidential_supported_text_redacted(self):
  record={"evidence_id":"private-1","confidentiality_class":"restricted","supported_text":"do not publish"}
  for fmt in ("json","csv","markdown"):
   output=render([record],fmt); self.assertNotIn("do not publish",output); self.assertIn("REDACTED",output)
