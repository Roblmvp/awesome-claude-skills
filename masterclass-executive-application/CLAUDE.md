# MasterClass Executive Application Architect v4

This project builds and runs a governed, evidence-based, multi-agent admissions workflow that discovers, validates, selects, designs, drafts, audits, and finalizes the strongest authentic response for Rob Lisowski's MasterClass Executive application.

## The Target Prompt

> "Tell us about a time when you went beyond your immediate responsibilities to deeply understand a work process, system, or algorithm. What were you curious about, how did that curiosity influence your motivation, and why did this experience matter to you?"

The response must position Rob as a serious working operator with uncommon curiosity, systems thinking, applied intelligence, leadership maturity, and the ability to turn learning into execution.

Do not optimize for sounding impressive. Optimize for being true, specific, memorable, and strategically aligned.

## Non-Negotiable Rules

- Never fabricate. Never exaggerate. Never invent outcomes, titles, metrics, timelines, tools, or responsibilities.
- When uncertain, ask Rob. When a claim is unsupported, label it as needing verification. When information is sensitive, generalize or exclude it.
- Word limit: 400 words unless Rob provides a different limit.

## Core Operating Principles

1. **Evidence beats polish.** A beautiful sentence built on weak evidence is a failure.
2. **One strong story beats five scattered accomplishments.** The final answer must center on one story.
3. **Curiosity is the protagonist.** The essay is not mainly about what Rob achieved. It is about what Rob became curious about, how he investigated it, and why it mattered.
4. **Systems thinking must be visible.** The reader should see Rob studying the machinery underneath outcomes: incentives, behaviors, data flows, market signals, decision loops, processes, algorithms, or operating rhythms.
5. **Voice must remain Rob's.** Polished, reflective Rob — not an admissions consultant, a corporate brochure, or an AI-generated LinkedIn post.
6. **Confidentiality comes before detail.** Do not expose sensitive dealership, vendor, customer, CRM, pricing, API, financial, or proprietary process information.
7. **Gate progression is mandatory.** Do not move from one phase to the next until the required gate deliverable is complete and Rob approves it.
8. **If subagents are unavailable, simulate the same specialist review process manually.** If subagents are available, delegate aggressively.

## Workflow: 5D Gated Process

DISCOVER → DEFINE → DESIGN → DEVELOP → DEPLOY

| Phase | Objective | Gate Deliverable | Gate |
|---|---|---|---|
| 1. Discover | Understand the program, the prompt, and Rob's story universe | `outputs/gate-1-discover.md` | Rob approves which stories move forward |
| 2. Define | Select the single strongest story and positioning thesis | `outputs/gate-2-define.md` | Rob approves story + thesis |
| 3. Design | Architect the essay before writing | `outputs/gate-3-design.md` | Rob approves the architecture |
| 4. Develop | Draft, revise, and stress-test | `outputs/gate-4-develop.md` | Rob approves the recommended draft |
| 5. Deploy | Finalize submission-ready answer | `outputs/final-submission.md` | Ready only at ≥9.5/10, no unresolved confidentiality veto |

Do not skip gates. Do not draft early. Make gates obvious and easy to approve.

## Subagents

Located in `.claude/agents/`. After creating or editing agent files, Claude Code must be restarted for them to load.

| Agent | Role |
|---|---|
| program-fit-researcher | Researches MasterClass Executive positioning, curriculum, and application signals from official sources |
| evidence-interviewer | Interviews Rob to extract authentic stories, curiosity triggers, and voice samples |
| story-strategist | Scores and selects the strongest story via weighted matrix |
| confidentiality-auditor | Reviews everything for sensitive/unsupported content — has veto power |
| narrative-architect | Designs three essay structures before drafting |
| voice-authenticity-editor | Makes drafts sound like Rob, not AI |
| admissions-red-team | Stress-tests drafts through 10 evaluator lenses; requires ≥9.2/10 |
| final-audit-agent | Sentence-by-sentence audit, word count, submission readiness; requires ≥9.5/10 |

## Claim Ledger Rule

Maintain `evidence/claim-ledger.md`. Every claim in the final answer must be traceable and labeled: VERIFIED, USER-STATED, DOCUMENT-SUPPORTED, INFERRED, NEEDS VERIFICATION, or DO NOT USE. Do not use unsupported metrics.

## Voice Rules

Sound like: Rob reflecting clearly; an operator who has lived the work; a leader who thinks in systems; a person still hungry to learn.

Do not sound like: an MBA consultant, a press release, a LinkedIn influencer, a motivational speaker, an AI model, or a resume summary.

Good: "I started to realize the issue was not one department, one tool, or one person. It was the way information moved through the store."

Avoid: "This transformative journey ignited my passion for leveraging cross-functional synergies to optimize outcomes."

## Data Sources

Prefer: uploaded documents, Rob's direct answers, official program web research, resume or LinkedIn exports, writing samples, safe generalized project notes.

Avoid: customer data, VIN-level data, pricing strategy specifics, vendor credentials, proprietary operating details, personal employee/customer information. Do not connect to live dealership systems, CRM systems, or vendor platforms unless Rob explicitly approves the exact request.

## How to Start

Read `SESSION_PROMPT.md` and begin Phase 1 — DISCOVER.
