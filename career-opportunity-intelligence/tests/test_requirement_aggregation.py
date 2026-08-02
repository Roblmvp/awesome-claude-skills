import unittest
from support import *
from career_intelligence.requirements import aggregate_requirements,extract_requirements
class Tests(unittest.TestCase):
 def test_source_ids(self): self.assertTrue(aggregate_requirements(jobs())["requirements"][0]["source_job_ids"])
 def test_exact_not_vague(self): self.assertGreaterEqual(len(aggregate_requirements(jobs())["requirements"]),3)
 def test_explicit_status(self): self.assertEqual(extract_requirements(jobs()[0])[0]["extraction_status"],"explicit")
