import unittest
from support import *
from career_intelligence.classify import classify_job
class Tests(unittest.TestCase):
 def test_rationale(self): self.assertIn("dealer performance",classify_job(jobs()[0])["classification_signals"])
 def test_ambiguous_manual(self):
  j=jobs()[0]; j["responsibilities"]=["Dealer performance and revenue operations"]
  self.assertEqual(classify_job(j)["classification_status"],"manual_review")
 def test_does_not_set_fit(self): self.assertNotIn("qualification_fit_score",classify_job(jobs()[0]))
