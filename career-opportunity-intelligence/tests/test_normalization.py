import unittest
from support import *
from career_intelligence.normalize import canonical_url,content_hash,normalize_job
class Tests(unittest.TestCase):
 def setUp(self): self.raw=load("synthetic-jobs.json")[0]
 def test_nullable_market_fields(self): self.assertIsNone(normalize_job(self.raw)["base_compensation_min"])
 def test_compensation_not_inferred(self): self.assertIsNone(normalize_job(self.raw)["base_compensation_max"])
 def test_travel_not_inferred(self): self.assertIsNone(normalize_job(self.raw)["travel_percent_min"])
 def test_field_distinct(self): self.assertEqual(normalize_job(self.raw)["work_model"],"field_based")
 def test_tracking_removed(self): self.assertNotIn("utm_",canonical_url(self.raw["source_url"]))
 def test_original_preserved(self): self.assertIn("utm_source",normalize_job(self.raw)["source_url_original"])
 def test_hash_deterministic(self): self.assertEqual(content_hash(normalize_job(self.raw)),content_hash(normalize_job(self.raw)))
 def test_hash_changes(self):
  a=normalize_job(self.raw); b=dict(a,summary="Changed")
  self.assertNotEqual(content_hash(a),content_hash(b))
