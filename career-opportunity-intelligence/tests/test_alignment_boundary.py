import unittest
from support import *
from career_intelligence.alignment import build_alignment
from career_intelligence.fit import match_job
class Tests(unittest.TestCase):
 def test_no_resume_prose(self): self.assertIsNone(build_alignment(jobs()[0],match_job(jobs()[0],[]))["employer_facing_content"])
 def test_blocked_claims(self): self.assertTrue(build_alignment(jobs()[0],match_job(jobs()[0],[]))["blocked_claims"])
 def test_resume_permitted_verified_evidence(self):
  evidence=load("synthetic-candidate-evidence.json"); evidence[0]["allowed_uses"].append("resume_alignment")
  fit=match_job(jobs()[0],evidence,load("synthetic-evidence-mappings.json"))
  self.assertEqual(build_alignment(jobs()[0],fit,evidence)["eligible_candidate_evidence_ids"],["ev-1"])
 def test_interview_only_evidence_blocked(self):
  evidence=load("synthetic-candidate-evidence.json"); evidence[0]["allowed_uses"]=["fit_analysis","interview_preparation"]
  fit=match_job(jobs()[0],evidence,load("synthetic-evidence-mappings.json"))
  self.assertEqual(build_alignment(jobs()[0],fit,evidence)["eligible_candidate_evidence_ids"],[])
 def test_restricted_evidence_blocked(self):
  evidence=load("synthetic-candidate-evidence.json"); evidence[0]["allowed_uses"].append("resume_alignment"); evidence[0]["confidentiality_class"]="restricted"
  fit=match_job(jobs()[0],evidence,load("synthetic-evidence-mappings.json"))
  self.assertEqual(build_alignment(jobs()[0],fit,evidence)["eligible_candidate_evidence_ids"],[])
