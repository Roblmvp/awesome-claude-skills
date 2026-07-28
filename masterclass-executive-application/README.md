# MasterClass Executive Application — Admissions Workflow

A gated, research-backed, subagent-driven workflow that produces Rob Lisowski's strongest authentic answer to the MasterClass Executive application prompt:

> "Tell us about a time when you went beyond your immediate responsibilities to deeply understand a work process, system, or algorithm. What were you curious about, how did that curiosity influence your motivation, and why did this experience matter to you?"

## How It Works

The project runs a 5D gated process — **DISCOVER → DEFINE → DESIGN → DEVELOP → DEPLOY** — where each phase produces a gate deliverable that Rob must approve before the next phase begins. Eight specialist subagents handle research, evidence intake, story selection, confidentiality review, narrative architecture, voice editing, red-team stress testing, and final audit.

## Project Layout

```
masterclass-executive-application/
├── CLAUDE.md                  # Operating principles, workflow rules, voice rules
├── SESSION_PROMPT.md          # Paste/run this to start Phase 1
├── .claude/
│   ├── settings.json          # Conservative permission defaults
│   └── agents/                # 8 specialist subagents
├── evidence/                  # Intake, story bank, claim ledger, voice samples
├── research/                  # Program fit brief, admissions signal analysis
├── outputs/                   # Gate deliverables 1–4 + final submission
└── scripts/
    └── word_count.py          # Word-limit enforcement
```

## Getting Started

1. Open Claude Code in this directory (restart if the agent files were just created, so subagents load).
2. Paste or reference `SESSION_PROMPT.md`.
3. Answer the evidence-intake questions honestly — evidence beats polish.
4. Approve or redirect at each gate.

## Guardrails

- No fabrication, no exaggeration, no unsupported metrics.
- Every claim is tracked in `evidence/claim-ledger.md` with a verification status.
- The confidentiality auditor has veto power over any draft containing sensitive dealership, vendor, customer, or proprietary information.
- Final answer must be under 400 words (unless Rob sets a different limit) and score ≥9.5/10 on the final audit.
