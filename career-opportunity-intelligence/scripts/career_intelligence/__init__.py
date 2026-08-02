"""Offline, deterministic career opportunity intelligence core."""
from .normalize import normalize_job, normalize_jobs
from .deduplicate import deduplicate_jobs
from .classify import classify_job, classify_jobs
