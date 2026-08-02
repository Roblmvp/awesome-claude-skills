# QA_REPORT.md — August_2026_Ford_Deal_Log_Master.xlsx (Gate 4)

Pipeline: `python3 build_deal_log.py --finalize` (clean build → LibreOffice recalc →
tab-color re-injection) → `python3 tools/qa_gauntlet.py`. Gate-3 functional verification
(7-deal matrix, 44/44 incl. hand-computed commissions line) ran on the same generator with
`--test-deals`; the shipped file is the clean build.

## Gauntlet results — 15/15 PASS

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `recalc.py` → `total_errors: 0` | ✅ | status=success, **26,135 formulas, 0 errors** |
| 2a | Formula-column pattern scan | ✅ | M, S, AI, AJ, AK, AL, AP, AQ: exactly 1 normalized pattern each across 35 rows × 31 tabs; zero deviants |
| 2b | Summary/pace/glance block uniformity | ✅ | uniform; only sanctioned variants (C62/C63 day-1 chain head; C69 last-day GOAL-HIT) |
| 3 | XML grep `JULY`/`July`/`Jul`/`2026,7` | ✅ | **0 hits** across all workbook XML (donor had 28,994) |
| 4a | Nav links resolve | ✅ | every HYPERLINK target exists; prev/next wraps Aug 31↔Aug 1; calendar covers 31/31 days |
| 4b | Named ranges | ✅ | 84 = donor 78 + 6 `BM_*`; all resolve; benchmark values live (0.50/0.50/0.33/1.00/500/3) |
| 4c | Dropdown sources + arrows | ✅ | all list DVs valid (incl. cascading Make→Model, conditional CPO, new Explorer B5); `showDropDown` unset everywhere ⇒ arrows render |
| 5 | DOW audit | ✅ | Aug 1=SATURDAY … Aug 31=MONDAY; Sundays 2/9/16/23/30: light-blue tab + CLOSED subtitle; Saturdays steel; weekdays navy — 31/31 |
| 6 | No `#REF!`/`#NAME?`/etc.; no lowercased formulas | ✅ | zero error values cached; zero parse-failed formulas ('#' glyphs at Commissions!A6, Dashboard!A29 only) |
| 7 | Empty-sheet grace | ✅ | zero deals: day summaries 0, verdicts "-", pace "—"/0, penetration "—", REPT bars blank, Nightly message renders, Explorer "Showing 0 of 0" — no `#DIV/0!` anywhere |
| 8 | Protection | ✅ | 42/42 sheets protected, **zero passwords** (donor's Staff & Lists legacy password removed); inputs unlocked (grid, Goals, Draw, Nightly, Explorer criteria, Pay Plan dollars, lists, Benchmarks); all 8 formula columns locked (M-col defect fixed) |
| 9 | Test residue | ✅ | 0 non-formula cells in all 31 deal grids; 0 test-marker strings in XML |
| x1 | Deal Explorer extras | ✅ | native table `DealLedger` (banded + header filter), freeze A8, sheet autofilter removed |
| x2 | Selling-day serials | ✅ | BR4:BR29 = the 26 August selling days (46235–46265 minus 5 Sundays), BR30 cleared |
| x3 | Roster wiring | ✅ | Dashboard AD4:AD19 + Commissions T4:T19 = live refs to Staff & Lists |

**File open time:** full LibreOffice open+recalc+save cycle ≈ **10 s** (26,135 formulas);
openpyxl load < 3 s. File size 561 KB (donor 721 KB).

## Notes for the record

- **LibreOffice repairs**: LO's recalc rewrite drops every `tabColor` in this workbook —
  `--finalize` re-injects them at the zip level after recalc so cached values are preserved.
  Container initially shipped LO *without* the Calc component (`libreoffice-calc` installed
  during Phase 2 — any future rebuild environment needs it).
- **Gate-3 functional evidence** (test build): 44/44 expected-vs-actual checks — split credits
  ½/½, tier MATCH at $3,500→4 and $9,000→8, ACV−MMR flag at +$800 vs $500, water flag +
  count, Pending/Unwind exclusion, cash-deal blanks, VSC pen 40% ⚠ vs 50%, commissions line
  hand-computed and matched to the penny, all six internal audits ✓.
- Known behavior: channel-mix COUNTIFs include non-delivered rows (July semantics, preserved).
- September rebuild: edit BUILD CONFIG (month facts + closed days) in `build_deal_log.py`,
  run `python3 build_deal_log.py --finalize`, run `python3 tools/qa_gauntlet.py`
  (update its CLOSED/TABS constants or import them from the build module).
