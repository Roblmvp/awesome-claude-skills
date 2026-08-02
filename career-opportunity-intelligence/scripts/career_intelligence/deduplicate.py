from .source_policy import merge_authoritative

def reason(a,b):
    if a.get("requisition_id") and b.get("requisition_id") and a["requisition_id"] != b["requisition_id"]: return None
    if a["normalized_company_name"]==b["normalized_company_name"] and a.get("requisition_id") and a.get("requisition_id")==b.get("requisition_id"): return "employer_and_requisition_id"
    if a.get("official_source") and b.get("official_source") and a["canonical_source_url"]==b["canonical_source_url"]: return "canonical_official_url"
    loc=lambda x:(x.get("city"),x.get("state"),x.get("country"))
    if a["normalized_company_name"]==b["normalized_company_name"] and a["normalized_title"]==b["normalized_title"] and loc(a)==loc(b): return "fallback_fingerprint"
    return None

def deduplicate_jobs(jobs):
    output=[]
    for job in jobs:
        for i,current in enumerate(output):
            why=reason(current,job)
            if why:
                merged=merge_authoritative(current,job); merged["deduplication_reason"]=why
                if current.get("content_hash") != job.get("content_hash"): merged.setdefault("audit_events",[]).append({"event":"content_changed","previous_hash":current.get("content_hash"),"observed_hash":job.get("content_hash")})
                output[i]=merged; break
        else: output.append(job)
    return sorted(output,key=lambda x:x["job_id"])
