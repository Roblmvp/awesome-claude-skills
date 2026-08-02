import unittest
from support import *
from career_intelligence.fit import match_job
from career_intelligence.validators import ValidationError
class Tests(unittest.TestCase):
 def setUp(self): self.job=jobs()[0]; self.ev=load("synthetic-candidate-evidence.json")
 def test_proven_requires_evidence(self):
  with self.assertRaises(ValidationError): match_job(self.job,self.ev,{"job-1:required:1":{"classification":"proven","evidence_ids":[]}})
 def test_transferable_labeled(self):
  x=match_job(self.job,self.ev,{"job-1:required:1":{"classification":"transferable","evidence_ids":["ev-2"]}}); self.assertEqual(x["requirement_matches"][0]["classification"],"transferable")
 def test_developable_blocked(self):
  x=match_job(self.job,self.ev,{"job-1:required:1":{"classification":"developable"}}); self.assertEqual(x["blocked_candidate_claims"][0]["reason"],"developable")
 def test_unknown_not_proven_or_prohibitive(self): self.assertEqual(match_job(self.job,self.ev)["unknown_count"],1)
 def test_requirement_not_evidence(self): self.assertFalse(match_job(self.job,self.ev)["audit_events"][0]["job_description_used_as_evidence"])
 def test_missing_allowed_uses_fails_closed(self):
  evidence=[dict(self.ev[0])]; evidence[0].pop("allowed_uses")
  with self.assertRaises(ValidationError): match_job(self.job,evidence)
 def test_malformed_allowed_uses_fails_closed(self):
  evidence=[dict(self.ev[0],allowed_uses=["anything"])]
  with self.assertRaises(ValidationError): match_job(self.job,evidence)
