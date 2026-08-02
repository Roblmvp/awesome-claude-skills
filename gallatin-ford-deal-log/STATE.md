# STATE.md — Deal Log Factory build state

## Build config (v2 FINAL)
MONTH=August YEAR=2026 DAYS=31 FIRST_DOW=Saturday
CLOSED_DAYS=[2,9,16,23,30] SELLING_DAYS=26 STORE=Gallatin Ford
SOURCE=July_2026_Ford_Deal_Log_Master.xlsx → OUTPUT=August_2026_Ford_Deal_Log_Master.xlsx

## Current phase
**Phase 0 — INGEST & AUDIT: complete. AWAITING: G1.**

## Last completed step
- Two-pass load + full audit done → `AUDIT.md`, raw data in `audit_data.json` (audit_dump.py reproduces it).
- Key facts for later phases:
  - July file is an EMPTY template (0 deals). Usage counts all 0 → menu item 1 re-scoped.
  - Day tabs: deal rows 8:42; 35 input cols; 7 formula cols M,S,AI,AJ,AK,AL,AP (AI/AL/AP hidden).
  - Statuses: Delivered/Pending/Unwind/Back Out (no "Dead").
  - Footer per tab: summary 44–50, flags 53–59, pace 61–69; C62/C63 MTD daisy-chain; C68/C69 hardcoded July pace (27 selling days → August = 26).
  - Defects: M column unlocked (D2); roster hardcoded ×3 (D3); dup-Deal# CF is x14 XML — openpyxl can't emit natively (D5).
  - Perf: 24,475 formulas; Deal Explorer 11,936 (49%); LibreOffice recalc >120s.
  - Dashboard helpers: AD4:AD19 roster, AE:BI unit/gross/channel matrices, BR4:BR30 selling-day serials, BT4:BT7 aggregates.
  - Commissions helpers: T roster, U:AY units/gross/flat matrices rows 4-19/23-38/42-57, BB tier via MATCH(BD,'Pay Plan'!C6:C12), audits I26:I31.

## Next step
Wait for Rob's `APPROVED G1: <numbers>` → Phase 1 write SPEC.md from July anatomy + approved items → Gate 2.

## Gates
- G1: posted, awaiting approval token.
- G2/G3/G4: not reached.

## Environment notes
- Repo: roblmvp/awesome-claude-skills, branch claude/gallatin-ford-deal-log-aug-uc4qry, project dir gallatin-ford-deal-log/.
- openpyxl 3.1.5 pip-installed; recalc via /root/.claude/skills/xlsx/scripts/recalc.py (LibreOffice).
- **TRAP: the container ships WITHOUT libreoffice-calc** — soffice starts but cannot load any
  spreadsheet, so recalc.py idles until its timeout and reports "LibreOffice timed out; formulas
  were NOT recalculated". Fix (do this FIRST in any new session):
  `apt-get update -q && DEBIAN_FRONTEND=noninteractive apt-get install -y -q libreoffice-calc`
  Verify with a trivial convert-to csv before trusting any recalc timing.
- Never save a data_only workbook. Quote 'Staff & Lists' in refs. No XLOOKUP/FILTER/SORT/UNIQUE/SEQUENCE; _xlfn. prefix for TEXTJOIN/IFS/SWITCH/etc.
