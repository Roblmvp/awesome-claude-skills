# Repository Governance

This is a public collection of reusable skills. Apply these rules to every file in the repository.

## Public-data boundary

- Commit only reusable code, schemas, documentation, and synthetic fixtures. Never place private candidate data in this repository.
- Keep real resumes, contact details, compensation criteria, references, performance data, application records, interview notes, and career evidence outside the checkout in an ignored private location.
- Sanitize source evidence before a public commit. Use invented people and organizations in examples and tests.
- Never place credentials in prompts, source files, fixtures, logs, documentation, commits, or pull-request content. Never reuse a previously exposed Firecrawl credential.

## Evidence and resume integrity

- Never invent candidate experience, metrics, skills, titles, credentials, technical proficiency, regulatory or compliance knowledge, authority, leadership scope, financial authority, or results.
- Treat missing facts as unknown. Require a cited source, explicit candidate confirmation, or an explicit evidence status for every candidate claim.
- Keep job requirements separate from candidate qualifications. Never turn a requirement or keyword into candidate history.
- Describe adjacent experience only as **transferable experience**, not direct experience or mastery.
- Preserve official employers, titles, dates, education, and credentials exactly. Do not alter them for keyword matching.
- Use only eligible evidence in employer-facing content and keep each claim traceable to its evidence record. Surface gaps as questions or development opportunities.

## Agent and external-action safety

- Use synthetic candidate data in tests, examples, demonstrations, and fixtures.
- Obtain explicit human approval before submitting an application, sending outreach, creating a recurring monitor, or performing any other external write.
- Treat research and draft generation as read-only by default.
- For interactive Firecrawl access, use hosted MCP OAuth without embedding credentials in URLs. Future unattended code may read `FIRECRAWL_API_KEY` only from a protected environment; never print, persist, or commit it. Keyless operation is a limited fallback, not an authentication substitute.

## Code Review Rules

Require reviewers to flag unsupported candidate claims, requirements represented as experience, fabricated metrics, and altered titles, dates, education, or credentials. Also flag real candidate information in synthetic fixtures, credentials or tokens, unapproved external writes, and Firecrawl configuration outside supported non-secret patterns.
