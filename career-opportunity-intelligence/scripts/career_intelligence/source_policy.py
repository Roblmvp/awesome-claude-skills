from copy import deepcopy
from urllib.parse import urlsplit

from .constants import SOURCE_AUTHORITY

def verify_source(job, employer_registry=None):
    """Assign authority from controlled registry facts, never source assertions."""
    out=deepcopy(job); registry=employer_registry or {"employers":[]}
    domain=(urlsplit(out["source_url"]).hostname or "").lower()
    out["employer_domain"]=domain
    company=" ".join(out["company_name"].lower().split())
    matching=[e for e in registry.get("employers",[]) if " ".join(e.get("name","").lower().split())==company]
    ats_owners=[e.get("name") for e in registry.get("employers",[]) if domain in [d.lower() for d in e.get("verified_ats_domains",[])]]
    if out["source_type"] == "official_ats":
        verified=bool(matching and domain in [d.lower() for d in matching[0].get("verified_ats_domains",[])])
        out["source_verification"]="registry_verified" if verified else "unverified"
        out["source_authority"]=SOURCE_AUTHORITY["official_ats"] if verified else SOURCE_AUTHORITY["unknown"]
        out["official_source"]=verified
        if ats_owners and not verified:
            out["source_verification"]="ownership_conflict"; out["source_review_status"]="manual_review"
            out.setdefault("conflicts",[]).append({"field":"ats_ownership","claimed_company":out["company_name"],"registry_owners":sorted(ats_owners),"domain":domain})
    else:
        out["source_authority"]=SOURCE_AUTHORITY[out["source_type"]]
        out["official_source"]=out["source_authority"] <= SOURCE_AUTHORITY["official_corporate"]
        out["source_verification"]="source_type_policy"
    return out

def merge_authoritative(a,b):
    winner, other=(a,b) if a["source_authority"] <= b["source_authority"] else (b,a)
    out=deepcopy(winner); conflicts=list(a.get("conflicts",[]))+list(b.get("conflicts",[]))
    protected=("job_status","work_model","title","company_name","city","state","country","requisition_id")
    for key in protected:
        x,y=winner.get(key),other.get(key)
        if x not in (None,"","unknown") and y not in (None,"","unknown") and x != y:
            conflicts.append({"field":key,"authoritative_value":x,"conflicting_value":y,"authoritative_url":winner["source_url"],"other_url":other["source_url"]})
        elif x in (None,"","unknown") and y not in (None,"","unknown") and winner["source_authority"] == other["source_authority"]: out[key]=y
    out["conflicts"]=conflicts
    out["source_sightings"]=sorted(a.get("source_sightings",[])+b.get("source_sightings",[]),key=lambda x:x["source_url"])
    out.setdefault("audit_events",[]).append({"event":"source_selected","reason":"lowest source authority number","source_url":winner["source_url"]})
    return out
