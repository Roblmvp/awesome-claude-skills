from .models import FirecrawlOperationPlan
from .validators import validate_plan
class FirecrawlPlanBuilder:
    def build(self,operation,purpose,input_data,**overrides):
        approval=operation in {"crawl","interact","agent","extract","monitor"}; recurring=operation=="monitor"; external=recurring and bool(input_data.get("notification") or input_data.get("webhook"))
        defaults={"operation_id":f"plan-{operation}","operation_type":operation,"purpose":purpose,"input":input_data,"requires_human_approval":approval,"external_write":external,"recurring":recurring,"enabled":False,"only_main_content":operation in {"scrape","batch_scrape"},"result_limit":5 if operation=="search" else None,"max_depth":1 if operation=="crawl" else None,"page_limit":10 if operation in {"map","crawl"} else None,"safety_notes":["offline plan only","no credentials","no forms or applications"],"command_preview":["firecrawl",operation,"--input-json", "<approved-input>"]}
        defaults.update(overrides); plan=FirecrawlOperationPlan(**defaults).to_dict(); return validate_plan(plan)
    def sequence(self,profile):
        domains=profile.get("permitted_domains",[]); geo=profile.get("geography",{})
        specs=[("search","bounded broad discovery"),("map","official career URL discovery"),("scrape","known official job pages"),("batch_scrape","approved URL set"),("crawl","bounded career paths"),("interact","approved dynamic public ATS"),("agent","supplemental research"),("extract","approved structured extraction"),("monitor","future recurring observation")]
        return [self.build(op,purpose,{"query":profile.get("query"),"notification":None},permitted_domains=domains,geography=geo) for op,purpose in specs]
