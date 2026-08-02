import tempfile,unittest
from pathlib import Path
from support import *
from validate_repository_controls import firecrawl_secrets,parse_openai_yaml,parse_skill_frontmatter,tracked_files,validate_fixture_privacy,validate_local_links,validate_secrets

class Tests(unittest.TestCase):
 def test_realistic_synthetic_firecrawl_key_rejected(self):
  value="fc-"+("SyntheticValue_"*2)
  self.assertEqual(firecrawl_secrets(value),[value])
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/"input.txt"; path.write_text(value)
   with self.assertRaises(ValueError): validate_secrets([path])
 def test_documentation_placeholders_allowed(self):
  self.assertEqual(firecrawl_secrets("fc-YOUR-API-KEY and fc-..."),[])
 def test_committed_files_have_no_firecrawl_credential(self): validate_secrets()
 def test_skill_metadata(self):
  self.assertEqual(parse_skill_frontmatter()["name"],"career-opportunity-intelligence"); self.assertTrue(parse_openai_yaml()["description"] if "description" in parse_openai_yaml() else parse_openai_yaml()["short_description"])
 def test_local_references(self): validate_local_links()
 def test_tracked_file_discovery(self): self.assertIn(ROOT/"AGENTS.md",tracked_files())
 def test_fixture_privacy(self): validate_fixture_privacy()
