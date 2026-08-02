import unittest
from support import *
from career_intelligence.firecrawl_contract import DisabledLiveFirecrawlAdapter,LiveExecutionDisabled
from career_intelligence.firecrawl_plan import FirecrawlPlanBuilder
class Tests(unittest.TestCase):
 def test_monitor_inactive(self):
  p=FirecrawlPlanBuilder().build("monitor","test",{})
  self.assertFalse(p["enabled"]); self.assertTrue(p["recurring"]); self.assertTrue(p["requires_human_approval"])
 def test_interact_approval(self): self.assertTrue(FirecrawlPlanBuilder().build("interact","test",{})["requires_human_approval"])
 def test_no_credential_preview(self):
  text=" ".join(FirecrawlPlanBuilder().build("search","test",{})["command_preview"]).lower()
  self.assertNotRegex(text,r"api.?key|bearer|oauth.?token|client.?secret")
 def test_live_disabled(self):
  with self.assertRaises(LiveExecutionDisabled): DisabledLiveFirecrawlAdapter().execute("search",{})
 def test_all_operations_planned(self): self.assertEqual(len(FirecrawlPlanBuilder().sequence(load("synthetic-search-profile.json"))),9)
