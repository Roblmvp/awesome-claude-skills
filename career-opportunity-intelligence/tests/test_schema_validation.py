import unittest
from support import *
from career_intelligence.validators import ValidationError,validate_job,validate_evidence
class Tests(unittest.TestCase):
 def test_valid_job(self): self.assertEqual(validate_job(load("synthetic-jobs.json")[0])["job_id"],"job-1")
 def test_missing_required(self):
  with self.assertRaises(ValidationError): validate_job({})
 def test_unknown_enum_fails(self):
  x=load("synthetic-jobs.json")[0]; x["work_model"]="sometimes"
  with self.assertRaises(ValidationError): validate_job(x)
 def test_unknown_schema_version_fails(self):
  x=load("synthetic-jobs.json")[0]; x["schema_version"]="999"
  with self.assertRaises(ValidationError): validate_job(x)
 def test_malformed_evidence_fails(self):
  with self.assertRaises(ValidationError): validate_evidence({"evidence_status":"verified_candidate_fact"})
