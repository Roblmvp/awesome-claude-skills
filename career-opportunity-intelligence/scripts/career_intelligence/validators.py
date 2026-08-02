from .constants import *

class ValidationError(ValueError): pass

JOB_REQUIRED = {"schema_version", "job_id", "company_name", "title", "source_url", "source_type"}

def validate_job(job):
    missing = sorted(k for k in JOB_REQUIRED if not job.get(k))
    if missing: raise ValidationError(f"missing required job fields: {', '.join(missing)}")
    if job["schema_version"] != SCHEMA_VERSION: raise ValidationError("unsupported schema_version")
    if job.get("work_model", "unknown") not in WORK_MODELS: raise ValidationError("invalid work_model")
    if job.get("source_type") not in SOURCE_TYPES: raise ValidationError("invalid source_type")
    if job.get("job_status", "unknown") not in JOB_STATUSES: raise ValidationError("invalid job_status")
    return job

def validate_fit(fit):
    required = {"schema_version", "job_id", "requirement_matches", "opportunity_class", "eligible_evidence_ids"}
    missing = sorted(k for k in required if k not in fit)
    if missing: raise ValidationError(f"missing required fit fields: {', '.join(missing)}")
    if fit["schema_version"] != SCHEMA_VERSION: raise ValidationError("unsupported schema_version")
    if fit["opportunity_class"] not in OPPORTUNITY_CLASSES: raise ValidationError("invalid opportunity_class")
    for match in fit["requirement_matches"]:
        if match.get("classification") not in MATCH_CLASSES: raise ValidationError("invalid match classification")
    return fit

def validate_evidence(item):
    if item.get("evidence_status") not in EVIDENCE_STATUSES: raise ValidationError("invalid evidence_status")
    if not item.get("evidence_id") or not item.get("source_reference"): raise ValidationError("evidence requires identifiers")
    uses = item.get("allowed_uses")
    if not isinstance(uses, list) or not uses or any(use not in ALLOWED_EVIDENCE_USES for use in uses):
        raise ValidationError("evidence requires valid allowed_uses")
    if item.get("confidentiality_class") not in CONFIDENTIALITY_CLASSES:
        raise ValidationError("evidence requires valid confidentiality_class")
    if item.get("evidence_status") == "approximate_candidate_confirmed_fact" and not item.get("approximation_metadata"):
        raise ValidationError("approximate evidence requires metadata")
    return item

def validate_plan(plan):
    required = {"operation_id", "operation_type", "purpose", "input", "enabled", "command_preview"}
    missing = sorted(k for k in required if k not in plan)
    if missing: raise ValidationError(f"missing required plan fields: {', '.join(missing)}")
    if plan.get("operation_type") not in OPERATIONS: raise ValidationError("invalid operation_type")
    if plan["operation_type"] == "monitor" and (plan.get("enabled") or not plan.get("recurring") or not plan.get("requires_human_approval")):
        raise ValidationError("monitor must be disabled, recurring, and approved")
    if plan["operation_type"] in {"interact", "agent", "crawl"} and plan.get("enabled"): raise ValidationError("high-impact live plans must be disabled")
    return plan
