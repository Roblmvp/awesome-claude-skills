# STATE.md — Deal Log Factory build state

- **Phase**: 0 — Ingest & Audit (COMPLETE, pending G1)
- **Last step**: AUDIT.md written and verified (4-agent adversarial pass on grid anatomy,
  dead columns, hardcodes, defects/protection). Gate 1 package posted in chat.
- **Next step**: WAIT for Rob's `APPROVED G1: <item numbers>` token. Then Phase 1 (SPEC.md).
- **Branch**: `claude/august-2026-gallatin-deal-log-0zba2o` in roblmvp/awesome-claude-skills,
  project dir `deal-log-factory/`.
- **Key facts a cold session must not rediscover**:
  - Source template is EMPTY (zero deals) — usage counts are consumption-based.
  - 7 formula columns (M,S,AI,AJ,AK,AL,AP), 35 inputs; grid rows 8–42; header row 7.
  - Statuses: Delivered/Pending/Unwind/Back Out (no "Dead").
  - Defects D1–D5 in AUDIT.md §7; hardcode inventory §8.
  - August: 31 days, first DOW Saturday, Sundays 2/9/16/23/30 closed, 26 selling days.
- **Artifacts**: AUDIT.md · tools/audit.py · audit_out/* (regenerable, git-ignored) ·
  source/July_2026_Ford_Deal_Log_Master.xlsx
