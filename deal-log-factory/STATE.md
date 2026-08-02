# STATE.md — Deal Log Factory build state

- **Phase**: 2 — Prototype/Build (COMPLETE, pending G3)
- **G2**: approved; tags gate-1/2-approved local (remote rejects tag pushes, 403).
- **Architecture**: build_deal_log.py = config-driven TRANSFORM of the committed July donor
  (styles/structure verbatim) + SPEC deltas. Full 31-tab wiring done in one pass (transform
  makes phased cloning moot — flagged in G3 package). `--test-deals` seeds the 7-deal matrix.
- **Environment note**: container shipped LibreOffice WITHOUT the Calc component — any xlsx
  recalc hung. Fixed via `apt-get install libreoffice-calc`. recalc now ~11s.
- **Last step**: recalc clean (26,135 formulas, 0 errors); tools/verify_g3.py 44/44 passed;
  EX-fix deviation (Explorer empty-row ✓ semantics) applied + flagged for G3 approval.
- **Next step**: WAIT for `APPROVED G3`. Then Phase 3 residue purge is just a clean rebuild
  (no --test-deals) + Phase 4 QA gauntlet.
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
