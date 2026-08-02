import json,unittest
from dataclasses import asdict
from support import *
from career_intelligence.firecrawl_plan import FirecrawlPlanBuilder
from career_intelligence.fit import match_job
from career_intelligence.models import CandidateEvidenceReference,FirecrawlOperationPlan
from career_intelligence.validators import ValidationError,validate_fit,validate_job,validate_plan

class Tests(unittest.TestCase):
 def test_job_record_round_trip(self):
  record=jobs()[0]; self.assertEqual(validate_job(json.loads(json.dumps(record))),record)
 def test_fit_record_round_trip(self):
  record=match_job(jobs()[0],load("synthetic-candidate-evidence.json"),load("synthetic-evidence-mappings.json")); self.assertEqual(validate_fit(json.loads(json.dumps(record))),record)
 def test_firecrawl_plan_round_trip(self):
  record=FirecrawlPlanBuilder().build("search","test",{}); model=FirecrawlOperationPlan(**record); self.assertEqual(validate_plan(json.loads(json.dumps(asdict(model)))),record)
 def test_malformed_fit_enum_fails_closed(self):
  record=match_job(jobs()[0],[]); record["opportunity_class"]="likely"
  with self.assertRaises(ValidationError): validate_fit(record)
 def test_malformed_plan_enum_fails_closed(self):
  record=FirecrawlPlanBuilder().build("search","test",{}); record["operation_type"]="browse"
  with self.assertRaises(ValidationError): validate_plan(record)
