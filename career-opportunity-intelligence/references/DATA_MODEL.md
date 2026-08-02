# Data Model

`JobRecord` stores market facts, original and canonical URLs, provenance, sightings, conflicts, unknown fields, and audit events. `RequirementRecord` stores explicit posting requirements without semantic invention. `CandidateEvidenceReference` is a private-runtime interface. `FitRecord` stores evidence-linked judgments separately from preferences. `FirecrawlOperationPlan` is an inert, reviewable acquisition contract. Schemas use version `1.0`; null means unstated, while `unknown` is an explicit enum state.

A job content hash is SHA-256 over sorted compact JSON containing normalized employer/title, requisition, status, location, work model, summary, responsibilities, and qualifications.
