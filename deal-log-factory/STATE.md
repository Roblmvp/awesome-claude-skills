# STATE.md — Deal Log Factory build state

- **Phase**: 1 — Spec Lock (SPEC.md written, pending G2)
- **G1 record**: Rob replied `APPROVED CONTINUE` (blanket). Interpreted per SPEC.md §0 —
  all 14 items in recommended form + D1–D5 fixes, NO column cuts.
- **Last step**: SPEC.md frozen draft committed; derived August facts verified by script
  (elapsed/left sequences, serials 46235–46265, DOW).
- **Next step**: WAIT for `APPROVED G2`. Then Phase 2 prototype per SPEC §13.
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
