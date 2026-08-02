import unittest
from support import *
from career_intelligence.fit import match_job
from career_intelligence.scoring import score_fit
class Tests(unittest.TestCase):
 def setUp(self): self.fit=match_job(jobs()[0],load("synthetic-candidate-evidence.json"),load("synthetic-evidence-mappings.json"))
 def test_no_strategic_without_profile(self): self.assertIsNone(score_fit(self.fit)["strategic_value_score"])
 def test_reproducible(self): self.assertEqual(score_fit(self.fit),score_fit(self.fit))
 def test_components(self): self.assertIn("weights",score_fit(self.fit)["score_components"])
