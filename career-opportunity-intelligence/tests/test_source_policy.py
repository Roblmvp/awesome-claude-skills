import unittest
from support import *
from career_intelligence.normalize import normalize_job
from career_intelligence.source_policy import merge_authoritative
class Tests(unittest.TestCase):
 def setUp(self): self.a,self.b=jobs()[:2]
 def test_official_precedence(self): self.assertEqual(merge_authoritative(self.a,self.b)["source_type"],"official_employer")
 def test_aggregator_cannot_overwrite(self): self.assertEqual(merge_authoritative(self.a,self.b)["work_model"],"field_based")
 def test_conflict_preserved(self): self.assertIn("work_model",[x["field"] for x in merge_authoritative(self.a,self.b)["conflicts"]])
 def test_sightings_preserved(self): self.assertEqual(len(merge_authoritative(self.a,self.b)["source_sightings"]),2)
 def test_registry_linked_ats_is_verified(self):
  registry=load("synthetic-employer-registry.json"); ats=normalize_job(load("synthetic-jobs.json")[2],employer_registry=registry)
  self.assertTrue(ats["official_source"]); self.assertEqual(ats["source_verification"],"registry_verified")
 def test_unknown_ats_is_unverified(self):
  ats=normalize_job(load("synthetic-jobs.json")[2])
  self.assertFalse(ats["official_source"]); self.assertEqual(ats["source_authority"],6)
 def test_source_cannot_self_declare_official(self):
  raw=dict(load("synthetic-jobs.json")[2],official_source=True,source_authority=1)
  self.assertFalse(normalize_job(raw)["official_source"])
 def test_unverified_ats_cannot_overwrite_official(self):
  official=self.a; ats=normalize_job(dict(load("synthetic-jobs.json")[2],requisition_id=official["requisition_id"],work_model="remote"))
  self.assertEqual(merge_authoritative(official,ats)["work_model"],"field_based")
 def test_ownership_conflict_requires_review(self):
  raw=dict(load("synthetic-jobs.json")[2],company_name="Other Fictional Company")
  ats=normalize_job(raw,employer_registry=load("synthetic-employer-registry.json"))
  self.assertEqual(ats["source_review_status"],"manual_review"); self.assertEqual(ats["conflicts"][0]["field"],"ats_ownership")
