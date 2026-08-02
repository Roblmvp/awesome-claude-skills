from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass
class CandidateEvidenceReference:
    evidence_id: str
    evidence_status: str
    evidence_category: str
    supported_text: str
    source_reference: str
    employer: str | None = None
    role: str | None = None
    date_range: str | None = None
    approximation_metadata: dict[str, Any] | None = None
    confidentiality_class: str = "private"
    allowed_uses: list[str] = field(default_factory=lambda: ["fit_analysis"])

@dataclass
class RequirementRecord:
    requirement_id: str
    source_job_id: str
    requirement_text: str
    requirement_type: str
    required_or_preferred: str
    criticality: str = "unknown"
    gating: bool = False
    years_required: float | None = None
    technologies: list[str] = field(default_factory=list)
    education: str | None = None
    leadership_scope: str | None = None
    source_reference: str = ""
    extraction_status: str = "explicit"
    confidence: float = 1.0
    human_review_required: bool = False

@dataclass
class FirecrawlOperationPlan:
    operation_id: str; operation_type: str; purpose: str; input: dict[str, Any]
    permitted_domains: list[str] = field(default_factory=list); excluded_domains: list[str] = field(default_factory=list)
    geography: dict[str, Any] = field(default_factory=dict); result_limit: int | None = None
    path_limits: list[str] = field(default_factory=list); max_depth: int | None = None; page_limit: int | None = None
    only_main_content: bool = True; output_formats: list[str] = field(default_factory=lambda: ["markdown"])
    structured_schema_reference: str | None = None; requires_authentication: bool = True
    requires_human_approval: bool = True; external_write: bool = False; recurring: bool = False
    enabled: bool = False; estimated_credit_category: str = "unknown"; safety_notes: list[str] = field(default_factory=list)
    command_preview: list[str] = field(default_factory=list); status: str = "planned"
    def to_dict(self): return asdict(self)
