import hashlib, json, re
from copy import deepcopy
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from .constants import SCHEMA_VERSION, TRACKING_KEYS
from .source_policy import verify_source
from .validators import validate_job

def clean_text(value): return re.sub(r"\s+", " ", value).strip() if isinstance(value, str) else value

def canonical_url(url):
    parts=urlsplit(url); query=urlencode(sorted((k,v) for k,v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in TRACKING_KEYS))
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/") or "/", query, ""))

def normalize_name(value): return re.sub(r"[^a-z0-9]+", " ", clean_text(value).lower()).strip()
def normalize_date(value):
    if value is None: return None
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except (ValueError, AttributeError): raise ValueError(f"invalid date: {value!r}")

def canonical_content(job):
    keys=("normalized_company_name","normalized_title","requisition_id","job_status","city","state","country","work_model","summary","responsibilities","required_qualifications","preferred_qualifications")
    return {k:job.get(k) for k in keys}
def content_hash(job): return hashlib.sha256(json.dumps(canonical_content(job), sort_keys=True, separators=(",",":"), ensure_ascii=True).encode()).hexdigest()

def normalize_job(raw, now=None, employer_registry=None):
    job=deepcopy(raw); validate_job(job)
    job.setdefault("schema_version", SCHEMA_VERSION); job["source_url_original"]=job["source_url"]
    job["canonical_source_url"]=canonical_url(job.get("canonical_source_url") or job["source_url"])
    job["normalized_company_name"]=normalize_name(job["company_name"]); job["normalized_title"]=normalize_name(job["title"])
    for key in ("company_name","title","summary"): job[key]=clean_text(job.get(key))
    for key in ("posting_date","modified_date"): job[key]=normalize_date(job.get(key))
    job.setdefault("job_status","unknown"); job.setdefault("work_model","unknown"); job.setdefault("field_based",job["work_model"]=="field_based")
    job.setdefault("office_attendance",None); job.setdefault("travel_percent_min",None); job.setdefault("travel_percent_max",None); job.setdefault("overnight_expectation",None)
    for key in ("base_compensation_min","base_compensation_max","compensation_currency","compensation_period"): job.setdefault(key,None)
    job=verify_source(job,employer_registry)
    job.setdefault("provenance",[])
    if not job.get("source_sightings"):
        job["source_sightings"]=[{"source_url":job["source_url"],"source_type":job["source_type"]}]
    job.setdefault("conflicts",[]); job.setdefault("audit_events",[])
    job.setdefault("unknown_fields",sorted(k for k in ("office_attendance","travel_percent_min","travel_percent_max","overnight_expectation","base_compensation_min","base_compensation_max") if job.get(k) is None))
    job["content_hash"]=content_hash(job); return job

def normalize_jobs(records,employer_registry=None): return [normalize_job(r,employer_registry=employer_registry) for r in records]
