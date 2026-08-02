# Public Data, Evidence, and Secret Governance

## Repository boundary

Public repository files may contain reusable code, schemas, synthetic fixtures, and documentation only. Real resumes, compensation criteria, references, contact information, performance data, job applications, interview notes, and candidate evidence must remain outside this repository. Live output locations are ignored by Git. Sanitize and minimize any source evidence before considering a public commit.

Do not paste private data into an agent prompt associated with this checkout. Store approved live data in an access-controlled system outside the repository, apply retention and deletion controls there, and pass only the minimum necessary data to an authorized workflow.

## Evidence rules

Record the source and status of each candidate assertion before drafting employer-facing prose. Missing evidence stays unknown. A job posting describes employer requirements; it is not evidence about a candidate. Adjacent experience may be presented only as explicitly labeled transferable experience. Never modify official employer names, titles, dates, education, or credentials.

Unsupported metrics, query counts, tools, regulatory knowledge, industry expertise, leadership scope, financial authority, and performance results are prohibited. Ask the candidate for material missing evidence, and otherwise report the item as a gap or development opportunity.

## Secrets and Firecrawl

Never commit or log tokens, API keys, bearer headers, client secrets, credential-bearing URLs, or copied environment values. Rotate any credential that has been exposed; specifically, never reuse a previously exposed Firecrawl credential.

Interactive Codex sessions may authenticate to the hosted Firecrawl MCP endpoint using OAuth:

`https://mcp.firecrawl.dev/v2/mcp-oauth`

The project-scoped `.codex/config.toml` is considered only when Codex trusts the project. The URL contains no credential, and interactive OAuth authentication is completed separately rather than stored in that file. Future unattended software may obtain a newly rotated `FIRECRAWL_API_KEY` from a protected runtime environment only. Keyless mode is a limited fallback with reduced capability and must not be assumed suitable for production. Live Firecrawl collection and Detroit career-intelligence implementation are intentionally deferred to a subsequent change.

## Human approval boundary

Research and drafting are read-only. Applications, messages, outreach, recurring monitors, and all external writes require explicit human approval at the time of the action.
