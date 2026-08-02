import re

def normalized_requirement(x): return re.sub(r"\s+"," ",x.strip().lower())
def extract_requirements(job):
    out=[]
    for kind,key in (("required","required_qualifications"),("preferred","preferred_qualifications")):
        for i,text in enumerate(job.get(key,[]),1):
            out.append({"requirement_id":f"{job['job_id']}:{kind}:{i}","source_job_id":job["job_id"],"requirement_text":text,"normalized_requirement":normalized_requirement(text),"requirement_type":"qualification","required_or_preferred":kind,"criticality":"unknown","gating":False,"years_required":None,"technologies":[],"education":None,"leadership_scope":None,"source_reference":job["source_url"],"extraction_status":"explicit","confidence":1.0,"human_review_required":False})
    return out

def aggregate_requirements(jobs,aliases=None):
    aliases=aliases or {}; buckets={}
    for j in jobs:
        for r in extract_requirements(j):
            key=aliases.get(r["normalized_requirement"],r["normalized_requirement"]); bucket=buckets.setdefault(key,{"requirement":key,"count":0,"required_count":0,"preferred_count":0,"gating_count":0,"source_job_ids":[],"source_references":[],"role_families":{},"title_clusters":{}})
            bucket["count"]+=1; bucket[r["required_or_preferred"]+"_count"]+=1; bucket["gating_count"]+=int(r["gating"]); bucket["source_job_ids"].append(j["job_id"]); bucket["source_references"].append(r["source_reference"])
            for field,target in ((j.get("role_family","unknown"),"role_families"),(j.get("normalized_title",j.get("title","")),"title_clusters")): bucket[target][field]=bucket[target].get(field,0)+1
    return {"requirements":[{**v,"source_job_ids":sorted(set(v["source_job_ids"])),"source_references":sorted(set(v["source_references"]))} for k,v in sorted(buckets.items())],"work_model_distribution":_counts(jobs,"work_model"),"travel_distribution":{"known":sum(j.get("travel_percent_min") is not None for j in jobs),"unknown":sum(j.get("travel_percent_min") is None for j in jobs)},"dealer_facing_count":sum(j.get("dealer_facing") is True for j in jobs)}
def _counts(items,key):
    out={}
    for item in items: out[str(item.get(key,"unknown"))]=out.get(str(item.get(key,"unknown")),0)+1
    return dict(sorted(out.items()))
