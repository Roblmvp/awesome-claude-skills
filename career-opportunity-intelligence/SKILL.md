---
name: career-opportunity-intelligence
description: Deterministic, provider-neutral analysis of structured job-market records with source provenance, deduplication, role classification, evidence-safe candidate matching, transparent scoring, exports, and disabled-by-default Firecrawl plans. Use for offline opportunity intelligence, recurring-requirement analysis, fit audits, or preparing bounded live-acquisition plans without collecting jobs or drafting resumes.
---

# Career Opportunity Intelligence

Operate offline and keep market facts, candidate evidence, fit judgments, and preferences separate. Read [SOURCE_POLICY.md](references/SOURCE_POLICY.md), [DATA_MODEL.md](references/DATA_MODEL.md), and [FIT_AND_SCORING.md](references/FIT_AND_SCORING.md) before interpreting results.

## Workflow

1. Accept only structured input or synthetic Firecrawl-shaped fixtures.
2. Normalize while retaining original values, provenance, nulls, and conflicts.
3. Apply official-source precedence and deterministic deduplication.
4. Classify role families independently of candidate qualification.
5. Aggregate exact normalized requirements with source job IDs.
6. Match requirements only to eligible structured evidence. Never use a posting as candidate evidence.
7. Compute reproducible qualification scores. Compute strategic value only from an explicit profile.
8. Export auditable JSON, CSV, or Markdown.
9. Build but never execute Firecrawl plans. Read [FIRECRAWL_OPERATIONS.md](references/FIRECRAWL_OPERATIONS.md) and [LIVE_VALIDATION_GATE.md](references/LIVE_VALIDATION_GATE.md) before Phase 2B-2.

Run `python3 career-opportunity-intelligence/scripts/run_career_intelligence.py --help`. Keep live/private output under ignored `.career-intelligence/`; see [PRIVATE_RUNTIME_BOUNDARY.md](references/PRIVATE_RUNTIME_BOUNDARY.md).

## Hard boundaries

- Preserve missing values as null or `unknown`; never infer compensation, travel, or candidate metrics.
- Label adjacent evidence `transferable`; do not present `developable`, `unproven`, or `unknown` as experience.
- Do not generate resume prose, submit forms, contact anyone, authenticate, activate monitors, or execute network calls.
- Require human approval for later live acquisition, interaction, recurring monitors, applications, outreach, and every external write.
