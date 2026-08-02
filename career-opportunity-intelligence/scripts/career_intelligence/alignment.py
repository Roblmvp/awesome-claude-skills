from .constants import ELIGIBLE_EVIDENCE
from .validators import validate_evidence

def build_alignment(job,fit,evidence=()):
    records={item["evidence_id"]:validate_evidence(item) for item in evidence}
    resume_ids=sorted(i for i in fit["eligible_evidence_ids"] if i in records and records[i]["evidence_status"] in ELIGIBLE_EVIDENCE and "resume_alignment" in records[i]["allowed_uses"] and records[i]["confidentiality_class"] in {"public","synthetic","private"})
    blocked=list(fit["blocked_candidate_claims"])
    blocked += [{"evidence_id":i,"reason":"not eligible for resume alignment"} for i in fit["eligible_evidence_ids"] if i not in resume_ids]
    return {"job_id":job["job_id"],"role_family":job.get("role_family","unknown"),"prioritized_requirements":[m["requirement_id"] for m in fit["requirement_matches"]],"eligible_candidate_evidence_ids":resume_ids,"transferable_evidence_ids":sorted({i for m in fit["requirement_matches"] if m["classification"]=="transferable" for i in m["evidence_ids"] if i in resume_ids}),"material_gaps":fit["material_gaps"],"clarification_questions":fit["clarification_questions"],"blocked_claims":blocked,"suggested_resume_family_identifier":job.get("role_family") if job.get("role_family") != "unknown" else None,"employer_facing_content":None}
