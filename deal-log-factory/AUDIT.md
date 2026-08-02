# AUDIT.md — July 2026 Ford Deal Log Master (Phase 0)

Source: `source/July_2026_Ford_Deal_Log_Master.xlsx` (720,607 bytes, Excel 2007+).
Method: two-pass openpyxl load (formulas + `data_only`; the `data_only` load was never saved).
All numbers below were derived by script (`tools/audit.py`, dumps in `audit_out/`) and
independently re-verified by `tools/crosscheck.py` — a second implementation that parses the
raw sheet XML directly (zipfile + ElementTree, no openpyxl) and tokenizes every formula,
data-validation, and conditional-formatting reference. Both passes agree on every claim in
this file. (A 4-agent verification workflow was also attempted but its subagent environment
failed before touching the file; the XML cross-check replaced it.)

---

## 0. Headline findings

1. **The workbook is a pristine, empty template.** Every deal-grid input cell on all 31 day
   tabs (rows 8–42, 35 input columns) is empty — zero literals, zero logged deals. All cached
   roll-ups are 0. Consequence: "per-column July usage counts" are 0/1085 everywhere, so the
   Value Menu's column-cut item is argued from **consumption analysis** (which columns any
   formula reads) instead of entry frequency.
2. **The claimed anatomy is close but not exact.** It is 42 sheets and 42-column day tabs, but
   there are **7 formula columns** (M, S, AI, AJ, AK, AL, AP), not 6, hence **35 input
   columns**, not 36. Status values are `Delivered / Pending / Unwind / Back Out` — there is
   **no "Dead" status anywhere** in the file. Deal Explorer is 1,085 deal rows (8–1092).
3. **One real logic defect found**: Commissions defines "delivered" as `Status="Delivered"`
   while every other surface (day summaries, Dashboard, Nightly Text, Deal Explorer counts)
   uses the AI flag (`Deal#` present ∧ Status ∉ {Pending, Unwind, Back Out} — including blank
   status). A deal with a Deal# and blank Status counts in units/gross but pays $0 commission.
4. **14 input columns are consumed by no formula** (details §6) — including exactly the fields
   the used-desk/F&I menu items want to compute from (MMR, ACV Est, Disposition, F&I Mgr,
   Lender). They are wired for *entry* (dropdowns, formats) but nothing *reads* them.
5. 24,475 formulas total; **Deal Explorer alone holds 11,936 (49%)** — the performance-budget
   item is real.

---

## 1. Sheet map (42 sheets)

| # | Sheet | State | Tab color | Protection | Freeze | Hidden cols | Formulas |
|---|-------|-------|-----------|-----------|--------|-------------|----------|
| 0 | Guide | visible | gold C9A227 | ✔ (no pwd) | — | — | 2 |
| 1 | Goals | visible | gold | ✔ | — | — | 6 |
| 2 | Scoreboard | visible | gold | ✔ | — | — | 34 |
| 3 | Deal Explorer | visible | gold | ✔ | **A44 (suspect)** | — | 11,936 |
| 4 | Commissions | visible | gold | ✔ | A4 | T | 1,781 |
| 5 | Pay Plan | **hidden** | gray A6A6A6 | ✔ | — | — | 0 |
| 6 | Dashboard | visible | gold | ✔ | A4 | T | 1,621 |
| 7 | Nightly Text | visible | gold | ✔ | — | P | 203 |
| 8 | Leaderboard | visible | gold | ✔ | A6 | — | 81 |
| 9–39 | Jul 1 … Jul 31 | visible | navy 0B1F4D; Sundays (5/12/19/26) light-blue B8C4DC | ✔ | F8 | AI, AL, AP | 278 each |
| 40 | Trade Report | visible | green 1E7A34 | ✔ | A9 | — | 193 |
| 41 | Staff & Lists | visible | gray | ✔ | — | — | 0 |

All sheets protected, **no password** (T4 pattern already in place). Fonts: Arial throughout
(day-tab grid 8pt, report titles 16pt). Currency format `$#,##0;[Red]($#,##0);"-"`.
Day-tab print area `$A$1:$AH$70` (keeps product cols AM:AO and helpers off the printed page).

## 2. Named ranges (82)

- **Goals**: `GoalUnitsNew/Used/Total`, `GoalGrossNew/Used/Total`, `GoalPVRFront/Back/Total`,
  `GoalUnitsPerDay`, `GoalGrossPerDay`, `GoalSellingDays` → fixed Goals cells.
- **Dynamic staff/lists** (COUNTA-INDEX over `Staff & Lists`): `SalespeopleList` (A),
  `SalesManagerList` (D), `FinanceManagerList` (G), `AdSourceList` (J), `LenderList` (M).
- **Static lists**: `MakeList` (R5:R61), `VehicleYearList` (P5:P36, 2026→1995), `YN_LIST`
  (P40:P41), `N_ONLY` (P43).
- **56 per-make model lists** (`ACURA`…`VOLVO`, T..BX cols) feeding the cascading Model
  dropdown via `INDIRECT(SUBSTITUTE(...))`.
- **No Benchmarks block exists** — the BM_* constants are new work.

## 3. Day-tab anatomy (verified cell-for-cell on Jul 1; pattern-uniform on all 31)

Row 1: `JUL n` + `GALLATIN FORD — JUL n · DAYNAME` + R1 TODAY chip
`=IF(TODAY()=DATE(2026,7,n),"● TODAY","")`. Row 2 subtitle. Row 3: 6 HYPERLINK nav links
(◀ Prev Day / Dashboard / Trade Report / Nightly Text / Leaderboard / Next Day ▶; wraps
Jul 31→Jul 1). Row 6 group bands (DEAL / SOLD VEHICLE / TRADE / DESK). Row 7 headers.

**Deal grid rows 8–42 (35 rows/day)** — 42 cols A:AP. The 7 formula columns (each 1,085
formulas = 35×31, all pattern-uniform):

| Col | Name | Formula (row 8 form) |
|-----|------|----------------------|
| M | Vehicle | `=IF(AND($K8="",$L8=""),"",TRIM($J8&" "&$K8&" "&$L8))` |
| S | Total Gross | `=IF(COUNT(Q8:R8)=0,"",SUM(Q8:R8))` |
| AI | x Delivered | `=IF($D8="",0,IF(OR($AG8="Pending",$AG8="Unwind",$AG8="Back Out"),0,1))` |
| AJ | x Cr SP1 | `=IF($AI8=0,0,IF($F8="",0,IF($G8="",1,0.5)))` |
| AK | x Cr SP2 | `=IF($AI8=0,0,IF($G8="",0,IF($F8="",1,0.5)))` |
| AL | x Channel | `=IF($AF8="","",IF(COUNTIF(AdSourceList,$AF8)=0,"Untagged",INDEX('Staff & Lists'!$K$5:$K$204,MATCH($AF8,AdSourceList,0))))` |
| AP | x Gross Tier | `=IF($AI8=0,"",MATCH(MAX(N($S8),0),'Pay Plan'!$D$5:$K$5,1))` |

**Data validation** (already comprehensive — T3 mostly exists): Type `"New,Used"`; SP1/SP2
`SalespeopleList`; Sales Mgr / F&I Mgr / Lender / Ad Source lists; Sold+Trade Yr
`VehicleYearList`; Sold+Trade Make `MakeList`; Sold+Trade Model **cascading**
`INDIRECT(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(K8," ","_"),"-","_"),".","_"))`; CPO conditional
`IF($A8="New",N_ONLY,YN_LIST)`; RDR/Turned-In/We-Owe `"Y,N"`; Disposition
`"Retail,Wholesale,Auction,Buyback,TBD"`; Status `"Delivered,Pending,Unwind,Back Out"`;
VSC/LoJack/Int-Ext `"Y"`; Front/Finance decimal ≥ −250,000; ACV decimal ≥ 0.

**Conditional formatting per tab (11 rules)**: banded rows `MOD(ROW()-8,2)=1` on A8:AH42;
Pending row tint `$AG8="Pending"`; Unwind/Back-Out row tint; CPO-on-New flag
`AND($A8="New",N8="Y")`; short-VIN flag `AND(Y8<>"",LEN(Y8)<17)`; TODAY chip; pending/kept
count highlights (C56/C58); pace-verdict 3-state color (C69).

**DAILY SUMMARY block rows 44–59** (below grid — New/Used/Total units C46/E46/G46 pattern
`=COUNTIFS($A$8:$A$42,"New",$AI$8:$AI$42,1)`; front/finance/total gross; trades; FLAGS:
trades, ACV total, pending, CPO, not-turned-in `=COUNTIFS($T$8:$T$42,"<>",$Z$8:$Z$42,"N")`,
we-owes). **PACE COMMAND rows 61–69**: MTD units/gross (`Jul n` = prev tab's C62/C63 + today's
G46/G49 — a per-tab cumulative chain), goal echoes, needed-per-day, `C68` selling-days-left
(**hardcoded literal** 27…1; Sundays share next Monday's value), `C69` pace verdict with
**hardcoded `n/27` fraction**; Jul 31 uses a distinct GOAL-HIT/SHORT month-end variant.

**Protection**: inputs unlocked, formula cols S/AI/AJ/AK/AL/AP locked — **but col M (Vehicle)
is unlocked** (defect D2). Sundays are full clones (grid + everything), only tab color and
DOW label differ.

## 4. Report-sheet anatomy

- **Goals** — month facts (C5 `July 2026`, C6 31, C7 4, C8 27 — all literals), yellow inputs
  B12/B13/C12/C13 (units/gross by New/Used), PVR inputs B18/B19; computed totals/per-day;
  units×PVR≈gross consistency check A29 with ✓/⚠ CF.
- **Scoreboard** — Units & Gross goal/MTD/%/to-go blocks reading named goals + hidden-row
  helpers B36:B39, each a **31-term addition chain** over day-tab summary cells; PVR MTD;
  selling-days-left `=Dashboard!$BT$5`; MTD totals read `'Jul 31'!$C$62/$C$63` (end-of-chain
  cumulative). No REPT bars here (Leaderboard has them).
- **Dashboard** — MTD tiles (B7 units=BT6, D7 gross=BT7, front/finance/trades/CPO from per-day
  agg U:Y); Goal & Pace band (M11 verdict hardcodes `/27`); **calendar** rows 13–24 with
  `=HYPERLINK("#'Jul n'!A1","n")` chips + per-day mini strip `nu · $x.xk` (27 selling-day
  cells) + 4 `closed` literals under Sundays; salesperson leaderboard rows 27–43 (16 slots,
  ranked, split-credit); channel mix (5 rows: Internet/Phone/Showroom/Campaign/Untagged);
  products MTD (VSC/LoJack/Int-Ext counts). **Helper blocks right of hidden col T**:
  AD4:AD19 **literal rep roster** (defect D4); AE4:BI19 per-rep×per-day unit credits
  (`SUMPRODUCT` over F/G vs AJ/AK — 496 formulas); AE23:BI38 same ×gross; BK sums, BM
  tiebreak, BN rank; AE41:BI45 channel×day COUNTIFs; BP41:45 channel names; **BR4:BR30 =
  27 literal date serials (the July selling days, Sundays absent)**; BT4 days-worked
  `=MIN(27,COUNTIF($BR$4:$BR$30,"<="&TODAY()))`, BT5 days-left, BT6/BT7 MTD units/gross.
- **Commissions** — visible table rows 7–22 (16 reps): Units, Gross, PVR, Tier (`MATCH` into
  Pay Plan C), Flat (`LOOKUP`), Unit Bonus, Fast-Start (≤10th), Product $, Earnings, yellow
  Draw input (N, unlocked), Balance. Helper cols U:AY per-day units/gross/pay ×16 reps
  (**1,488 SUMPRODUCTs**, all gated on `$AG="Delivered"` — defect D1) + audit block BA:BJ.
  T4:T19 **literal rep roster** (defect D4). Rows 25–31: 6 labeled internal audits with ✓/⚠ CF.
- **Pay Plan** (hidden) — retro tier matrix rows 4–12: gross breakpoints D5:K5
  (0/1500/2500/3500/4000/5500/7000/8500), unit tiers C6:C12 (0/8/14/17/20/25/30), flat
  amounts D6:K12; Unit Bonus, Fast-Start, Product $ ($25 ea), Weekly Draw, Year-end $/car
  blocks; labeled assumptions A1–A8 in a note cell.
- **Nightly Text** — helper per-day block Q7:V37 (hidden col P; 6 SUMIFS ×31 days); day
  override K10; INDEX-by-`DAY(TODAY())` day pulls; yellow LIVE INPUTS (calls/emails/leads…);
  readiness check A22 (`COUNTBLANK` chain → "✅ READY TO COPY"); A23 emoji message builder
  (`CHAR(10)` multiline TEXT concat); pacing line E13 = gross MTD ÷ days-worked × work-days.
- **Leaderboard** — 16 ranked rows via `INDEX/MATCH` on Dashboard BN rank helpers;
  **already has REPT unit bars** (`=REPT("=",ROUND(28*C6/MAX(...),0))`).
- **Deal Explorer** — criteria row 5 (Salesperson-either-slot, Type, Status, Cert, Min Gross,
  Search; D5/E5/G5 have DVs, **B5 rep filter is free text**); B6 "Showing X of Y";
  1,085 rows × (1 ✓ filter formula + 10 live links to day-tab cells + 1 literal date);
  autofilter A7:L1092; **no native table**; freeze A44 (defect D3).
- **Trade Report** — month recap row 7 (trades/turned-in/not/%/ACV/avg) + 31 day rows reading
  each tab's C54/C55/C58 + `⚠ n kept` flag column.
- **Guide** — 9 plain-language rows (daily flow, status semantics, per-sheet how-tos) + live
  PVR line reading `'Jul 31'!$C$62/63`.
- **Staff & Lists** — roster cols A/D/G (16 salespeople, 4 sales mgrs, 2 F&I mgrs), Ad
  Source→Channel map J/K (47 sources → Internet/Phone/Showroom/Campaign), Lenders M (38),
  vehicle years P, MakeList R, 56 make→model lists T:BX. Banner claims Dashboard reads it
  automatically (untrue today — see D4).

## 5. Dependency graph

```
Staff & Lists ──(named ranges, DV)──▶ day tabs ──▶ Dashboard helpers (AE:BT) ──▶ Dashboard tiles
     ▲                                   │              ├──▶ Leaderboard (INDEX/MATCH on BN)
 Pay Plan ◀──(AP tier; Commissions)──────┤              ├──▶ Scoreboard (BT5) & Nightly (BR/BT)
                                         ├──▶ Deal Explorer (10 live links × 1,085 rows)
                                         ├──▶ Commissions (own SUMPRODUCTs, bypasses AJ/AK)
                                         ├──▶ Nightly Text helper block (SUMIFS)
                                         ├──▶ Trade Report (C54/C55/C58 per day)
                                         └──▶ Scoreboard B36:B39 (31-term chains) + 'Jul 31' C62/C63
Goals ──(named ranges)──▶ Scoreboard, Dashboard, day-tab pace blocks
Day tab n ──(C62/C63 cumulative chain)──▶ day tab n+1 ; row-3 nav links both directions
```

Formula counts: total **24,475** — Deal Explorer 11,936 · Commissions 1,781 · Dashboard 1,621
· day tabs 278×31=8,618 · Nightly 203 · Trade 193 · Leaderboard 81 · Scoreboard 34 · Goals 6
· Guide 2.

## 6. Input census & consumption analysis

Usage counts (literals in grid rows 8–42, all 31 tabs): **0 for every input column** — the
template has never been filled in. Therefore column value is judged by *consumption*:

**Consumed by formulas** (keep, obviously): A, B*, D, E, F, G, J, K, L (→M), N, Q, R, T, Z,
AB, AF (→AL), AG, AH, AM, AN, AO. (*B consumed by Deal Explorer link only.)

**Dead inputs — no formula anywhere reads them (14):**

| Col | Field | Only non-formula consumer | Menu item that would wire it |
|-----|-------|---------------------------|------------------------------|
| C | Age | none | — (cut candidate) |
| H | Sales Mgr | none | — (accountability only) |
| I | F&I Mgr | none | **#13** per-F&I-mgr penetration |
| O | RDR | none | — (cut candidate) |
| P | Lender | none | #5 missing-field flag |
| U/V/W | Trade Yr/Make/Model | none | #10 trade intelligence |
| X | Trade Mileage | none | — (cut candidate) |
| Y | Trade VIN | short-VIN CF rule only | — (cut candidate) |
| AA | Disposition | none | **#10** immediate-wholesale % |
| AC | MMR | none | **#9** ACV−MMR variance |
| AD | ACV Est | none | #9 (desk estimate vs actual) |
| AE | JD Power Clean | none | — (cut candidate) |

Plus **AP (x Gross Tier)**: a computed column whose output *nothing* consumes — Commissions
independently recomputes tiers by LOOKUP into Pay Plan. Pure formula overhead (1,085 cells)
or a kept convenience readout; decide at G1 (#1).

## 7. Defect log

| ID | Severity | Finding |
|----|----------|---------|
| D1 | **High** | Delivered-definition split: Commissions requires `Status="Delivered"`; AI flag (everything else) also counts blank-status rows with a Deal#. Blank status ⇒ counted in units/gross, paid $0. Fix: single definition in August (align Commissions to AI, or make AI require explicit "Delivered" — decide at G1). |
| D2 | Med | Day-tab column M (Vehicle) formula cells are **unlocked** — users can overtype the concat formula. All other formula cols locked. Fix in generator. |
| D3 | Low | Deal Explorer `freeze_panes=A44` — freezes 43 rows (header is row 7). Should be A8. |
| D4 | Med | Rep roster duplicated as literals in Dashboard AD4:AD19 and Commissions T4:T19; Staff & Lists banner says surfaces read it "automatically". A renamed rep silently zeroes their stats. Fix: reference `'Staff & Lists'!A5:A20`. |
| D5 | Low | Trade Report asymmetry: "Trades" is delivered-gated (`C54`), "Not Turned In" (`C58`) counts any row with a trade + Z="N" including pending/unwound rows → "Turned In" (=C54−C58) can go negative. |
| D6 | Info | No formula errors, no external refs, no XLOOKUP-family or prefix-needing functions, no lowercased formulas. The two `#`-cells (Commissions A6, Dashboard A27) are literal `#` header glyphs, not errors. |
| D7 | Info | An unsupported conditional-formatting *extension* (openpyxl warning) rides in the file; rules themselves are all classic types. Generator will re-emit clean rules. |

## 8. Hardcode inventory (everything the generator must derive from BUILD CONFIG)

1. Day tabs: titles/DOW labels; `R1` `DATE(2026,7,n)`; nav hyperlink targets incl. wraparound;
   `C68` selling-days-left literals; `C69` `n/27` pace fractions (selling-day-indexed, Sundays
   repeat) + last-day GOAL-HIT variant; summary/pace block labels with `JUL n`.
2. Dashboard: `BR4:BR30` 27 selling-day serials → **26 for August**; `BT4` `MIN(27,…)`;
   `M11` `/27`; calendar grid (Aug 1 = Saturday, 5 Sundays: 2/9/16/23/30); day strip (26
   cells); `closed` markers (5); AE:BI per-day helper width (31 day columns, unchanged).
3. Scoreboard: 31-term chains; `'Jul 31'` end-of-chain refs → `'Aug 31'`.
4. Commissions/Nightly/Trade/Explorer: 31 per-day formula families; Explorer's 1,085 literal
   dates; Nightly `A2` `DATE(2026,7,1)`.
5. Goals: month facts (`August 2026`, 31, **5**, **26**).
6. XML baseline: 28,994 `Jul` occurrences, 32 `2026,7` — QA #3's grep must reach 0 legit hits.
7. July's pace math divides by 27 in **4 distinct places** (day tabs C68/C69, Dashboard BT4/M11)
   — August build centralizes on `GoalSellingDays`/Benchmarks cells per the hard rules.

## 9. Performance budget baseline

24,475 formulas; heaviest families: Explorer links (10,850) + ✓ filters (1,085); Commissions
& Dashboard SUMPRODUCT fleets (496×2 + 1,488). File opens fine in LibreOffice; open-time will
be measured and reported at G3/G4 per menu item #14.
