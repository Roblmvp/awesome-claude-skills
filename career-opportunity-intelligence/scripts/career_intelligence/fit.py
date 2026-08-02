from .constants import ELIGIBLE_EVIDENCE, MATCH_CLASSES, SCHEMA_VERSION
from .requirements import extract_requirements
from .validators import ValidationError, validate_evidence

def match_job(job,evidence,mappings=None,candidate_profile_reference="private-profile"):
    evidence={e["evidence_id"]:validate_evidence(e) for e in evidence}; mappings=mappings or {}; matches=[]; blocked=[]
    for requirement in extract_requirements(job):
        mapping=mappings.get(requirement["requirement_id"],{}); classification=mapping.get("classification","unknown"); ids=mapping.get("evidence_ids",[])
        if classification not in MATCH_CLASSES: raise ValidationError("invalid match classification")
        eligible=[i for i in ids if i in evidence and evidence[i]["evidence_status"] in ELIGIBLE_EVIDENCE and "fit_analysis" in evidence[i].get("allowed_uses",[])]
        if classification=="proven" and not eligible: raise ValidationError("proven match requires eligible evidence ID")
        if classification=="transferable" and not eligible: raise ValidationError("transferable match requires eligible evidence ID")
        if classification not in {"proven","transferable"}: eligible=[]
        match={"requirement_id":requirement["requirement_id"],"classification":classification,"evidence_ids":eligible,"requirement_text":requirement["requirement_text"],"gating":requirement["gating"]}
        matches.append(match)
        if classification not in {"proven","transferable"}: blocked.append({"requirement_id":requirement["requirement_id"],"text":requirement["requirement_text"],"reason":classification})
    counts={k:sum(m["classification"]==k for m in matches) for k in MATCH_CLASSES}; total=len(matches); supported=counts["proven"]+counts["transferable"]
    return {"schema_version":SCHEMA_VERSION,"job_id":job["job_id"],"candidate_profile_reference":candidate_profile_reference,"requirement_matches":matches,**{f"{k}_count":v for k,v in counts.items()},"evidence_coverage_score":round(100*supported/total,2) if total else 0.0,"qualification_fit_score":None,"strategic_value_score":None,"confidence_score":None,"opportunity_class":"manual_review","material_gaps":[m for m in matches if m["classification"] in {"developable","prohibitive","unproven"}],"clarification_questions":[f"What eligible evidence supports {m['requirement_id']}?" for m in matches if m["classification"]=="unknown"],"blocked_candidate_claims":blocked,"eligible_evidence_ids":sorted({i for m in matches for i in m["evidence_ids"]}),"scoring_profile_version":None,"audit_events":[{"event":"evidence_match","job_description_used_as_evidence":False}]}
