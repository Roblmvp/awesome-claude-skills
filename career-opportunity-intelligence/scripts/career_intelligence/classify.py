RULES={
"oem_dealer_field_operations":["dealer performance","field operations","district manager"],
"automotive_finance_dealer_relationships":["dealer relationship","automotive finance","floorplan"],
"automotive_saas_customer_success":["customer success","implementation manager","automotive saas"],
"sales_enablement_dealer_training":["sales enablement","dealer training","training manager"],
"business_revenue_operations":["revenue operations","business operations","sales operations"],
"regional_dealer_group_operations":["regional operations","dealer group","fixed operations"],
"adjacent_multilocation_b2b_leadership":["multi location","b2b operations","regional director"]}

def classify_job(job,rules=None):
    rules=rules or RULES; text=" ".join([job.get("title","")]+job.get("responsibilities",[])).lower(); matches={k:[s for s in v if s in text] for k,v in rules.items()}; matches={k:v for k,v in matches.items() if v}
    out=dict(job)
    if len(matches)==1: family,signals=next(iter(matches.items())); out.update(role_family=family,role_subfamily=None,classification_confidence=min(1.0,.65+.1*len(signals)),classification_signals=signals,classification_status="classified")
    elif len(matches)>1: out.update(role_family="unknown",role_subfamily=None,classification_confidence=0.0,classification_signals=sorted({s for v in matches.values() for s in v}),classification_status="manual_review")
    else: out.update(role_family="unknown",role_subfamily=None,classification_confidence=0.0,classification_signals=[],classification_status="manual_review")
    return out

def classify_jobs(jobs): return [classify_job(j) for j in jobs]
