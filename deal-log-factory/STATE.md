# STATE.md — Deal Log Factory build state

- **Phase**: 4 — QA Gauntlet (COMPLETE, pending G4)
- **G2**: approved; tags gate-1/2-approved local (remote rejects tag pushes, 403).
- **Architecture**: build_deal_log.py = config-driven TRANSFORM of the committed July donor
  (styles/structure verbatim) + SPEC deltas. Full 31-tab wiring done in one pass (transform
  makes phased cloning moot — flagged in G3 package). `--test-deals` seeds the 7-deal matrix.
- **Environment note**: container shipped LibreOffice WITHOUT the Calc component — any xlsx
  recalc hung. Fixed via `apt-get install libreoffice-calc`. recalc now ~11s.
- **G3**: approved (incl. EX fix). Clean rebuild + `--finalize` (recalc + LO tab-color
  repair + password wipe). tools/qa_gauntlet.py: 15/15 PASS. QA_REPORT.md written.
- **Next step**: WAIT for `APPROVED G4`. On approval: tag gate-4-shipped, final delivery.
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
