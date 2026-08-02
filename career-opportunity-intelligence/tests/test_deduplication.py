import unittest
from support import *
from career_intelligence.deduplicate import deduplicate_jobs,reason
class Tests(unittest.TestCase):
 def test_matching_req(self): self.assertEqual(len(deduplicate_jobs(jobs()[:2])),1)
 def test_conflicting_req_not_merge(self): self.assertIsNone(reason(jobs()[0],jobs()[2]))
 def test_canonical_official(self):
  a,b=jobs()[0],dict(jobs()[0],job_id="copy",requisition_id=None)
  a=dict(a,requisition_id=None); self.assertEqual(reason(a,b),"canonical_official_url")
 def test_dedup_reason(self): self.assertEqual(deduplicate_jobs(jobs()[:2])[0]["deduplication_reason"],"employer_and_requisition_id")
