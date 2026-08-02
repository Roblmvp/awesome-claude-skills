# AUDIT.md — July 2026 Ford Deal Log Master (Phase 0)

Source: `July_2026_Ford_Deal_Log_Master.xlsx` (720,607 bytes).
Method: two-pass openpyxl load (formula pass + `data_only` pass, value pass never saved) + raw XML inspection.

---

## 0. Headline findings (read these first)

1. **The July file is a pristine, empty template.** Every input cell on every day tab
   (rows 8–42, all 31 tabs) is empty — 0 deals logged, 0 values anywhere in the input
   columns. Consequence: the "cut lowest-used columns, cite July usage counts" analysis
   is impossible from data. Actual usage count for **every** input column = **0**.
   Menu item 1 is re-scoped to a judgment call (see Menu).
2. **Much of the proposed menu already exists in July.** Dropdowns (16 validations/tab,
   incl. cascading Make→Model), sheet protection with unlocked inputs, freeze panes,
   status conditional formatting, banded rows, a daily summary + flags + pace block
   (at the *bottom* of each tab, rows 44–69), Sunday tab coloring, TODAY chip, and a
   duplicate-Deal# detector. The menu below marks each item **[EXISTS]**, **[PARTIAL]**
   or **[NEW]** so you only pay for what's actually new.
3. **Defect: formula column M ("Vehicle") is unlocked** on all 31 day tabs while the
   other six formula columns are locked. Protection is on, so users *can't* break
   S/AI/AJ/AK/AL/AP but *can* type over M's concat formula.
4. **Defect-adjacent: the rep roster is hardcoded in 3 places** — Staff & Lists A5:A20,
   Dashboard AD4:AD19, Commissions T4:T19 (16 identical literal names). Editing the
   roster on Staff & Lists does NOT propagate; the Dashboard/Commissions copies go stale.
5. **Performance: 24,475 formulas total; Deal Explorer alone is 11,936 (49%)** —
   but measured full recalc is only **11.4 s** in LibreOffice headless (see §8).
   The initial multi-minute timeouts were a build-container defect (missing
   libreoffice-calc package), not the workbook.
6. **Zero formula errors, zero pattern deviants, zero stray formulas** in the shipped
   July file. The six formula-column patterns are identical across all 31 tabs × 35 rows.

## 1. Sheet map (42 sheets)

| # | Sheet | State | Dims | Tab color | Freeze | Formulas | CF | DV | Protected |
|---|-------|-------|------|-----------|--------|----------|----|----|-----------|
| 1 | Guide | visible | A1:H15 | gold C9A227 | – | 2 | 0 | 0 | ✔ |
| 2 | Goals | visible | A1:H29 | gold | – | 6 | 2 | 0 | ✔ (goal cells unlocked + yellow FFF6BE) |
| 3 | Scoreboard | visible | A1:F39 | gold | – | 34 | 0 | 0 | ✔ |
| 4 | Deal Explorer | visible | A1:L1092 | gold | A44 | **11,936** | 0 | 3 | ✔ |
| 5 | Commissions | visible | A1:BH57 | gold | A4 | 1,781 | 12 | 0 | ✔ (Draw col N unlocked + yellow); col T hidden |
| 6 | Pay Plan | **hidden** | A1:L26 | gray A6A6A6 | – | 0 | 0 | 0 | ✔ ($ cells unlocked) |
| 7 | Dashboard | visible | A1:BT45 | gold | A4 | 1,621 | 3 | 0 | ✔; col T hidden |
| 8 | Nightly Text | visible | A1:V55 | gold | – | 203 | 2 | 0 | ✔; col P hidden |
| 9 | Leaderboard | visible | A1:F21 | gold | A6 | 81 | 0 | 0 | ✔ |
| 10–40 | Jul 1 … Jul 31 | visible | A1:AP69 | navy 0B1F4D; Sundays (5,12,19,26) slate B8C4DC | F8 | 278 each | 11 std + 1 x14 | 16 | ✔; cols AI, AL, AP hidden |
| 41 | Trade Report | visible | A1:H39 | green 1E7A34 | A9 | 193 | 1 | 0 | ✔ |
| 42 | Staff & Lists | visible | A1:BX204 | gray | – | 0 | 0 | 0 | ✔ (roster/list cells unlocked) |

Fonts: Arial throughout (headers 8pt bold, titles 16pt). Currency `$#,##0;[Red]($#,##0);"-"`.
Trade Report dates `ddd m/d`. No sheet has a protection password (protection = accident guard).

## 2. Named ranges (82)

- **Goals (11):** GoalUnitsNew/Used/Total (B12/B13/B14), GoalGrossNew/Used/Total (C12/C13/C14),
  GoalPVRFront/Back/Total (B18/B19/B20), GoalUnitsPerDay (B24), GoalGrossPerDay (B25), GoalSellingDays (C8).
- **Dynamic rosters/lists (5):** SalespeopleList (A), SalesManagerList (D), FinanceManagerList (G),
  AdSourceList (J), LenderList (M) — all `'Staff & Lists'!$X$5:INDEX(...,COUNTA(...))` self-sizing.
- **Static lists (4):** MakeList (R5:R61), VehicleYearList (P5:P36), YN_LIST (P40:P41), N_ONLY (P43).
- **Make→Model cascade (62):** ACURA … VOLVO, one named column range per make
  (used by `INDIRECT(SUBSTITUTE(...))` validation on Sold/Trade Model).

## 3. Day-tab anatomy (validated on all 31 tabs)

Grid: 42 columns (A:AP) × rows 1–69. Deal rows **8:42 (exactly 35)**.
Row 1: `A1='JUL n'`, `D1='GALLATIN FORD — JUL n · DAYNAME'`, `R1=IF(TODAY()=DATE(2026,7,n),"● TODAY","")`.
Row 3 nav: HYPERLINK chips — Prev Day / Dashboard / Trade Report / Nightly Text / Leaderboard / Next Day (Jul 1 prev→Jul 31; Jul 31 next→Jul 1). Rows 4–5: **empty** (free space).
Row 6 section band: DEAL | SOLD VEHICLE | TRADE | DESK. Row 7: headers.

**Column census — 35 input columns, 7 formula columns** (the brief said 36/6; actual is
35/7 because "x Cr SP1/SP2" is two columns, AJ and AK):

Inputs: A Type · B Stock# · C Age · D Deal# · E Customer · F SP1 · G SP2 · H Sales Mgr ·
I F&I Mgr · J Sold Yr · K Sold Make · L Sold Model · N CPO · O RDR · P Lender · Q Front
Gross · R Finance Gross · T Trade Stock# · U Trade Yr · V Trade Make · W Trade Model ·
X Trade Mileage · Y Trade VIN · Z Turned In · AA Disposition · AB ACV · AC MMR · AD ACV
Est · AE JD Power Clean · AF Ad Source · AG Status · AH We Owe · AM VSC(Y) · AN LoJack(Y) ·
AO Int/Ext(Y).

Formula columns (patterns verbatim, row 8; identical across all rows/tabs — 0 deviants):

| Col | Formula |
|-----|---------|
| M Vehicle | `=IF(AND($K8="",$L8=""),"",TRIM($J8&" "&$K8&" "&$L8))` |
| S Total Gross | `=IF(COUNT(Q8:R8)=0,"",SUM(Q8:R8))` |
| AI x Delivered | `=IF($D8="",0,IF(OR($AG8="Pending",$AG8="Unwind",$AG8="Back Out"),0,1))` |
| AJ x Cr SP1 | `=IF($AI8=0,0,IF($F8="",0,IF($G8="",1,0.5)))` |
| AK x Cr SP2 | `=IF($AI8=0,0,IF($G8="",0,IF($F8="",1,0.5)))` |
| AL x Channel | `=IF($AF8="","",IF(COUNTIF(AdSourceList,$AF8)=0,"Untagged",INDEX('Staff & Lists'!$K$5:$K$204,MATCH($AF8,AdSourceList,0))))` |
| AP x Gross Tier | `=IF($AI8=0,"",MATCH(MAX(N($S8),0),'Pay Plan'!$D$5:$K$5,1))` |

Correction to the brief: statuses are **Delivered / Pending / Unwind / Back Out** (no
"Dead"); AI excludes Pending + Unwind + Back Out. Hidden columns: AI, AL, AP (AJ/AK visible).

**Footer blocks (below deals — you scroll to see them):**
- Rows 44–50 DAILY SUMMARY: New/Used/Total units (COUNTIFS on A + AI=1), front/finance/total gross (SUMIFS), trades taken.
- Rows 53–59 FLAGS: Trades C54, ACV Total C55, Pending C56, CPO C57, Not Turned In C58, We Owes C59.
- Rows 61–69 PACE COMMAND: MTD units C62 = prev-tab C62 + today's G46 (daisy-chain across tabs; Jul 1 seeds the chain); MTD gross C63 same on C63/G49; goals via named ranges; **C68 hardcoded selling-days-left countdown (27,26,25,…, Sundays repeat the next workday's value)**; C69 verdict with **hardcoded `n/27` fraction per tab** (n = selling days elapsed; Sundays share n with the prior day).

**16 data validations** (A Type New,Used · F:G SalespeopleList · H SalesManagerList ·
I FinanceManagerList · J,U VehicleYearList · K,V MakeList · L,W INDIRECT cascade ·
N IF(New,N_ONLY,YN_LIST) · O,Z,AH Y,N · P LenderList · AA Retail,Wholesale,Auction,Buyback,TBD ·
AF AdSourceList · AG Delivered,Pending,Unwind,Back Out · AM:AO "Y" · Q:R decimal ≥ −250000 · AB decimal ≥ 0).

**12 CF rules**: banded rows; Pending → amber row; Unwind/Back Out → gray row; CPO=Y on
New → warning; short Trade VIN (<17 chars) warning; TODAY chip; pending/kept-trade count
highlights; pace verdict 3-state color; **+ 1 x14-extension rule: duplicate Deal# across
the whole month via `COUNTIF('Deal Explorer'!$C$8:$C$1092,D8)>1`** (openpyxl cannot write
x14 — the August generator must emit this rule as raw XML or as a standard cross-sheet CF; decision in SPEC).

## 4. Hub sheets

- **Dashboard** (BT45): visible zone A1:S45 = MTD tiles · goal/pace band + verdict ·
  clickable July calendar with per-day mini-stats ("3u · $12,400"), Sundays say "closed" ·
  16-row salesperson leaderboard · channel mix (Internet/Phone/Showroom/Campaign/Untagged)
  · products MTD (VSC/LoJack/Int-Ext). Helper block U3:BT45: U4:AB34 per-day pulls from
  each tab's G47/G48/C54/C55/C57 + 3 COUNTIFs; AD4:AD19 roster (hardcoded); AE4:BI19
  units rep×day (SUMPRODUCT ½/½ split); AE23:BI38 gross rep×day; AE41:BI45 channel×day;
  BK sums; BM/BN tie-broken RANK; **BR4:BR30 = 27 hardcoded selling-day date serials
  (Sundays absent)**; BT4 selling days elapsed `MIN(27,COUNTIF(BR,"<="&TODAY()))`;
  BT5 selling days left; BT6/BT7 MTD units/gross ← `'Jul 31'!C62/C63`.
- **Commissions** (BH57): visible A1:O31 — per-rep Units/Gross/PVR/Tier/Flat/Unit
  Bonus/Fast-Start/Product $/EARNINGS/Draw(input, yellow)/Balance + TOTALS + 6 self-audit
  rows (I26:I31 ✓/⚠). Helpers: T4:T19 roster (hardcoded); U4:AY19 credited units rep×day;
  U23:AY38 credited gross; U42:AY57 **retro flat $ rep×day** — SUMPRODUCT that LOOKUPs
  each deal's gross into the Pay Plan tier row selected by the rep's *final monthly* units
  (BB = MATCH(BD units, PayPlan C6:C12)); BA fast-start units (days ≤ 10th); BC delivered
  product count; BD/BE/BF sums; BH4:BH8 audit aggregates.
- **Pay Plan** (hidden, no formulas): D5:K5 tier breakpoints 0/1500/2500/3500/4000/5500/7000/8500;
  units rows B6:B12 (0–7/8–13/14–16/17–19/20–24/25–29/30+, C col lookup keys 0/8/14/17/20/25/30);
  flat matrix D6:K12; unit bonus B15:C20; fast start E15:F19; product $ H15:I17 ($25 each); weekly draw L15=500; year-end table B23:C26.
- **Scoreboard**: goal-vs-MTD Units/Gross (New/Used/Total), PVR, pace — reads named
  ranges + `'Jul 31'!C62/C63` + hidden B36:B39 = 31-term chains `SUM('Jul n'!C46...)`.
- **Leaderboard**: printable rank board, INDEX/MATCH into Dashboard helpers + REPT("=",…) bar chart.
- **Nightly Text**: helper P7:V37 (hidden P = day labels; Q..V = per-day New/Used units,
  front, back via SUMIFS into tabs); tiles indexed by `DAY(TODAY())` with K10 day-override;
  yellow live-input cells (calls/leads/etc.); A22 readiness check (✅/⚠); A23 giant
  CHAR(10) message string built for Teams copy-paste.
- **Trade Report**: month recap B7:G7 + per-day rows 9–39 pulling each tab's C54/C55/C58,
  turned-in %, avg ACV, ⚠ "n kept" flag.
- **Deal Explorer**: criteria row 5 (SP/Type/Status/Cert/Min-Gross/Search + 3 DVs);
  **1,085 live-link rows (31×35)**, 11 formulas each (A ✓-filter + C:L links to
  D/B/E/A/F/G/M/S/AG/N of each tab row); "Showing X of Y" counter.
- **Guide**: manager instructions + live PVR line reading `'Jul 31'!C62/C63`.
- **Staff & Lists**: rosters (16 SP / 4 SM / 2 F&I), Ad Source→Channel map (J/K cols),
  Lenders (M), years/makes/models reference columns (P–BX), inline notes.

## 5. Dependency graph

```
Staff & Lists (rosters, lists, channel map)      Pay Plan (tiers, rates)
        │ AL channel INDEX/MATCH (35/tab)                │ AP tier MATCH (35/tab)
        ▼                                                ▼
Day tabs Jul 1…Jul 31  ──daisy-chain C62/C63 MTD──►  (each tab → prev tab)
   │            │            │              │                    │
   │ per-day    │ 350/tab    │ 374/tab      │ 5/tab              │ 16/tab
   ▼            ▼            ▼              ▼                    ▼
Dashboard   Deal Explorer  Commissions   Trade Report      Nightly Text
   │   ▲(also Pay Plan ×1107)                                 │(+Dashboard ×3)
   │   └── Commissions helpers                                │
   ├──► Leaderboard (×128)                                    │
   └──► Scoreboard (BT5; + direct 31-tab chains + 'Jul 31'!C62/C63 + Goals named ranges)
Guide ──► 'Jul 31'!C62/C63 (PVR line)
```

Aggregation contract every consumer relies on: per-tab cells G46/C46/E46 (units),
G47/G48/G49/C49/E49 (gross), C54–C59 (flags), C62/C63 (MTD chain), AI/AJ/AK/AL/AP columns.

## 6. Input-vs-formula census

| Zone | Input cells | Formula cells |
|---|---|---|
| Day tab (each) | 35 cols × 35 rows = 1,225 possible; plus 0 footer inputs | 278 (245 col-formulas + 33 footer/header) |
| Goals | 8 (B12,C12,B13,C13,B18,B19 + facts locked) | 6 |
| Pay Plan | 71 rate/breakpoint cells (all unlocked) | 0 |
| Commissions | 16 (Draw N7:N22) | 1,781 |
| Nightly Text | 12 live inputs + K10 override | 203 |
| Staff & Lists | ~1,329 roster/list values | 0 |
| Dashboard / Scoreboard / Leaderboard / Trade Report / Deal Explorer / Guide | 0 (DE: 6 criteria cells) | 1,621 / 34 / 81 / 193 / 11,936 / 2 |

## 7. Defect hunt results

| ID | Severity | Finding |
|----|----------|---------|
| D1 | info | File contains zero deal data — pristine template. All usage counts = 0. |
| D2 | **defect** | Formula col **M unlocked** on all 31 day tabs (typeable despite protection). Other 6 formula cols locked correctly. Fix in August build. |
| D3 | **defect** | Roster hardcoded ×3 (Staff & Lists / Dashboard AD / Commissions T). Stale-name risk. Menu item 11 links them by formula. |
| D4 | design smell | Pace numbers hardcoded per tab: C68 countdown literal, C69 `n/27` literal fraction. Regenerated from CONFIG each month, so acceptable — but they exist as data (BR serials → BT4/BT5) on Dashboard; could be formulas. Kept as-is unless Rob objects (script derives all of them from CONFIG either way). |
| D5 | watch | Duplicate-Deal# CF is an x14 extension; openpyxl drops it on save. August generator must re-emit it deliberately (raw XML post-injection, or standard CF + cross-sheet formula, or helper-column approach). Decision recorded in SPEC. |
| D6 | behavior note | A row with Status=Delivered but **no Deal#** counts 0 everywhere, silently. A Delivered row missing Lender/gross also passes silently. Menu item 5 adds the red flag. |
| D7 | none | 0 value errors, 0 broken links, 0 pattern deviants, 0 stray formulas, all named ranges + hyperlinks + DV sources resolve. |

## 8. Performance budget (measured)

- Total formulas: **24,475**. Deal Explorer: **11,936 (48.8%)** = 1,085 deal rows ×
  (1 filter formula + 10 live links) + 1 counter; Commissions 1,781; Dashboard 1,621;
  31 day tabs 8,618 (278 each); everything else ~520.
- **Measured LibreOffice headless full recalc + save: 11.4 s wall clock, 0 errors on
  all 24,475 formulas.** Excel desktop should be comparable or faster. The workbook is
  NOT slow as shipped.
- Investigation note: initial recalc attempts timed out at 5–9 minutes on *every* copy,
  including a 6-formula subset — root cause was the build container missing the
  `libreoffice-calc` package (soffice started but could not load any spreadsheet).
  Fixed via apt; trap recorded in STATE.md so later phases don't rediscover it.
- Volatile functions: `TODAY()` appears on every day tab (R1 chip) + 6 hub headers +
  Dashboard BT4/BT5 + Nightly Text — ~40 volatile cells force broad recalc on every
  edit, but the broad recalc itself is cheap (see measurement).
- File size 720 KB / 42 sheets.

## 9. Simplification Menu

See Gate 1 message (menu is the decision artifact; this file is the evidence).
