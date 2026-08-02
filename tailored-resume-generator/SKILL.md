---
name: tailored-resume-generator
description: Tailors resumes to job descriptions while keeping every employer-facing claim traceable to candidate evidence and surfacing unsupported requirements as gaps.
---

# Tailored Resume Generator

Generate an ATS-readable resume without converting job-posting language into candidate history. Apply **evidence before prose**: inventory and classify candidate evidence first, map it to requirements second, and draft only after the map is complete.

## Required Inputs

Request:

- the full job description;
- the candidate's existing resume or work history, including official employer names, titles, and dates;
- education and credentials;
- candidate-provided skills, achievements, and metrics; and
- a source identifier for each fact or explicit candidate confirmation.

Treat omitted information as unknown. Ask focused questions when a missing fact is material; do not fill a blank using plausibility, industry norms, or job-description keywords.

## Evidence Gate

Read [the claim model](references/claim-model.md) before drafting. Classify every assertion as one of:

- `verified_candidate_fact`
- `candidate_confirmed_fact`
- `approximate_candidate_confirmed_fact`
- `transferable_experience`
- `job_requirement`
- `inferred_possibility`
- `unknown`
- `prohibited_unsupported_claim`

Optionally run the deterministic classifier:

```bash
python3 tailored-resume-generator/scripts/validate_claims.py claims.json
```

Use only verified facts, candidate-confirmed facts, explicitly approximate candidate-confirmed facts, and accurately labeled transferable experience in employer-facing output. Require an evidence identifier for each. Keep requirements, inferred possibilities, unknowns, and prohibited claims in the gap analysis.

## Integrity Rules

1. Preserve official employers, titles, dates, education, and credentials exactly.
2. Never invent or embellish metrics, percentages, counts, scale, results, tools, credentials, regulatory knowledge, industry knowledge, leadership scope, or financial authority.
3. Never infer mastery from adjacent experience.
4. Never convert a job requirement into candidate experience.
5. Never add keywords as candidate qualifications merely to improve ATS matching.
6. Label adjacent evidence as **transferable experience** and state what the evidence actually shows.
7. Retain unknown values as unknown; do not silently omit uncertainty from the analysis.
8. Trace every employer-facing statement to its source evidence.
9. Present material gaps as evidence questions or development opportunities.
10. Obtain explicit human approval before submitting a resume or application; this skill drafts only.

## Workflow

### 1. Separate sources

Create two inventories without merging them:

- **Candidate evidence:** exact supported facts and their evidence identifiers.
- **Job requirements:** employer language, priority, and whether matching evidence exists.

Extract must-have qualifications, preferred qualifications, responsibilities, tools, domain knowledge, and repeated terminology from the job description. Record each as a `job_requirement`; extraction does not make it candidate evidence.

### 2. Build an evidence matrix

For each requirement, record the requirement, matching evidence identifier, evidence status, eligibility, and gap/question. A semantic similarity is not proof of direct experience.

### 3. Resolve material uncertainty

Ask concise questions such as: “The posting requires SQL, but the supplied evidence does not mention it. Do you have specific SQL experience you want to confirm and source?” Until answered, keep the item out of the resume.

### 4. Draft from eligible rows only

Select the eligible accomplishments most relevant to the target role, then reorder supported bullets so the strongest matches appear first. Tailor emphasis by role without changing the underlying fact. Use exact job terminology only where the evidence supports the same meaning. For approximate candidate-confirmed values, use honest qualifiers such as “approximately” or “about.”

Build an ATS-conscious draft with standard headings such as Summary, Skills, Professional Experience, and Education. Keep layouts simple; avoid tables, graphics, and header/footer-dependent content. Include a skill or keyword only when an eligible evidence record supports it.

### 5. Audit every claim

For every summary phrase, skill, and bullet, identify its evidence record. Remove any claim without an eligible status and evidence identifier. Confirm that official identity, title, date, education, and credential fields are unchanged.

### 6. Return resume and gap report

Return:

1. the tailored draft;
2. a claim-to-evidence traceability table;
3. unmet or unknown requirements;
4. material evidence questions; and
5. accurately described development opportunities.

## Synthetic Regression Example

**Job requirements:** expert SQL, A/B testing, statistical analysis, communication, and healthcare/HIPAA familiarity; quantified impact preferred.

**Synthetic candidate evidence:**

- Data Analyst, Northstar Retail, 2019–2024 (`resume-role-1`)
- Built Python automation scripts (`candidate-note-2`)
- Created Tableau and Power BI dashboards (`resume-skill-3`)
- Worked with a marketing team on campaign analysis (`resume-role-1`)
- Business Analytics degree (`resume-education-1`)

**Evidence-safe result:**

```markdown
## Supported resume content

- Data Analyst | Northstar Retail | 2019–2024
- Built Python automation scripts.
- Created Tableau and Power BI dashboards.
- Transferable experience: collaborated with a marketing team on campaign analysis; this
  does not establish A/B testing experience.

## Gaps and questions (not resume claims)

- SQL — job requirement; candidate evidence not provided. Ask for specific, sourceable
  experience if applicable.
- A/B testing — job requirement; candidate evidence not provided.
- HIPAA knowledge — unknown; no regulatory evidence supplied.
- Query volume — unknown; do not manufacture a count.
- Percentage improvement — unknown; do not manufacture an impact metric.
```

The example intentionally does not add SQL, A/B testing, HIPAA knowledge, a query count, or a percentage improvement. Marketing analysis is adjacent evidence and is labeled transferable rather than presented as direct experimentation experience.

## Formatting

- Use standard headings, plain text or Markdown, and simple bullets.
- Prefer reverse chronological order and consistent dates.
- Avoid tables or graphics in the resume when ATS compatibility is important; the separate evidence matrix may use a table.
- Keep supported keywords natural and truthful.
