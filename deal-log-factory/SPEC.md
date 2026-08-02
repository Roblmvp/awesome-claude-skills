# SPEC.md — August 2026 Gallatin Ford Deal Log (FROZEN AT GATE 2)

The build contract for `build_deal_log.py`. Cold-session buildable: everything the generator
emits is specified here or copied verbatim from `source/July_2026_Ford_Deal_Log_Master.xlsx`
(exact July formulas quoted in `spec_refs/exact_formulas.txt`). Mid-build deviations stop the
build and go back to Rob.

## 0. Gate 1 approval record

Rob's token was `APPROVED CONTINUE` (blanket, no item numbers). Interpreted as: **all 14 menu
items in their recommended form + defect fixes D1–D5**, with the conservative reading on
item 1: **no input columns are cut** (a blanket approval is not read as permission to delete
fields). Concretely:

| Decision | Choice |
|---|---|
| Item 1 (column cuts) | **None.** All 42 July columns kept; AP kept for parity. New computed AQ appended. |
| D1 (delivered definition) | **AI flag wins.** Commissions consumes AJ/AK credits; `Status="Delivered"` gates removed everywhere. |
| Item 6 (Sundays) | Full clones (July convention) + existing CLOSED subtitle; new Saturday tab color. |
| Item 13 denominator | Penetration % = product Y ÷ **all delivered units** (labeled assumption; no financed flag exists). |
| Item 14 (Explorer) | Keep 35 rows/day + add native table; ✓ filter machinery kept; freeze fixed to A8. |

Any of these are one-line reversals at Gate 2.

## 1. BUILD CONFIG (authoritative)

```
MONTH=August  YEAR=2026  DAYS=31  FIRST_DOW=Saturday
CLOSED_DAYS=[2,9,16,23,30]  SELLING_DAYS=26  STORE=Gallatin Ford
OUTPUT_FILE=August_2026_Ford_Deal_Log_Master.xlsx
```

Derived (generator computes, never hand-edits):
- Tab names `Aug 1`…`Aug 31`. DOW: Aug 1=Sat, Aug 31=Mon.
- Excel serials: Aug 1 = 46235 (= verified Jul 1 serial 46204 + 31) … Aug 31 = 46265.
  Selling-day serials (26): 46235–46265 minus {46236, 46243, 46250, 46257, 46264}.
- Per-day `elapsed(d)` = selling days ≤ d: 1,1,2,3,4,5,6,7,7,8,9,10,11,12,13,13,14,15,16,17,18,19,19,20,21,22,23,24,25,25,26.
- Per-day `left(d)` = selling days ≥ d (C68 literals): 26,25,25,24,23,22,21,20,19,19,18,17,16,15,14,13,13,12,11,10,9,8,7,7,6,5,4,3,2,1,1.
- Calendar: **6 week rows** (July had 5) — week 1 holds Aug 1 only.

## 2. Workbook standards

- Fonts/formats/fills: copy July's exactly. Style constants (column widths, row heights,
  fills, fonts, number formats per region) are extracted once from the July file into
  `spec_refs/styles.json` at build time by the generator's `extract_styles()` step and applied
  verbatim; Arial throughout; currency `$#,##0;[Red]($#,##0);"-"`.
- Tab colors: reports gold `C9A227`; weekday navy `0B1F4D`; **Saturday steel `2E4A8F` (new)**;
  Sunday light-blue `B8C4DC`; Trade Report green `1E7A34`; Pay Plan/Staff gray `A6A6A6`.
- Protection: every sheet `sheet=True`, no password. Day tabs: all 35 input columns rows 8–42
  unlocked; **M locked (fixes D2)**; S/AI/AJ/AK/AL/AP/AQ locked. Report inputs unlocked as in
  July (Goals yellow cells, Commissions Draw N7:N22, Nightly live inputs + K10, Explorer
  criteria B5/D5/E5/G5/H5/I5, Pay Plan dollar cells, Staff & Lists list columns, Benchmarks).
- Dialect: T7 only (IF, SUMIFS, COUNTIF(S), SUMPRODUCT, INDEX/MATCH, LOOKUP, IFERROR, REPT,
  TRIM, TEXT, HYPERLINK, RANK, N, TODAY, DATE, DAY, SEARCH, ISNUMBER, COUNT/COUNTA/COUNTBLANK,
  MIN/MAX, SUM, ABS, ROUND, CHAR). No XLOOKUP/FILTER/SORT/UNIQUE/SEQUENCE/TEXTJOIN/IFS/SWITCH.
- Sheet order (42): Guide, Goals, Scoreboard, Deal Explorer, Commissions, Pay Plan(hidden),
  Dashboard, Nightly Text, Leaderboard, Aug 1…Aug 31, Trade Report, Staff & Lists.
- Hidden columns: day tabs AI/AL/AP (AQ **visible**); Dashboard T; Commissions T; Nightly P.
  Day-tab print area `$A$1:$AH$70`. Freeze: day tabs F8; Explorer **A8 (fixes D3)**;
  Dashboard A4; Commissions A4; Leaderboard A6; Trade Report A9.

## 3. Named ranges

All 82 July names re-created with identical definitions (Goal* → Goals cells; dynamic
COUNTA-INDEX staff/list ranges; MakeList/VehicleYearList/YN_LIST/N_ONLY; 56 make→model
lists). **New (6):**

```
BM_VSC_PEN         = 'Staff & Lists'!$F$25   = 0.50   (0%)
BM_APPR_TRADE      = 'Staff & Lists'!$F$26   = 0.50   (0%)
BM_IMMED_WHOLESALE = 'Staff & Lists'!$F$27   = 0.33   (0%)
BM_USED_TO_NEW     = 'Staff & Lists'!$F$28   = 1.00   (0.00)
BM_ACV_OVER_MMR    = 'Staff & Lists'!$F$29   = 500    ($#,##0)
BM_TURNIN_DAYS     = 'Staff & Lists'!$F$30   = 3      (0)
```

Yellow fill `FFF6BE`, unlocked, labels in E25:E30, header E24
`BENCHMARKS — tune targets here (yellow cells)`. Every new formula references these names;
no benchmark value is ever inlined.

## 4. Staff & Lists

July verbatim (rosters A/D/G, Ad Source→Channel J/K, Lenders M, Years P, MakeList R, model
lists T:BX) **plus**: Benchmarks block §3; the two note lines at A24/A25 move to C24/C25 so
`COUNTA` dynamic ranges count only real entries (cleanup; July's ranges carried 2 phantom
blanks).

## 5. Day tabs (template ×31; only labels/dates/nav/pace numbers vary)

Everything July has, cell-for-cell (rows 1–3 header+nav, row 6 bands, row 7 headers, grid
8–42, DAILY SUMMARY 44–59, PACE COMMAND 61–69, all DV, all CF, banded rows), with `Jul`→`Aug`,
`DATE(2026,7,n)`→`DATE(2026,8,n)`, DOW names per §1, Sunday subtitle `· CLOSED (SUNDAY)`
(July convention). The 7 formula columns keep July's exact formulas (AUDIT.md §3 table).

**New/changed cells:**

| Where | Spec |
|---|---|
| Glance strip row 4 (labels, locked, 8pt gold-on-navy) | C4 `UNITS` E4 `FRONT` G4 `FINANCE` I4 `TOTAL` K4 `TRADES` M4 `PENDING` O4 `WATER` |
| Glance strip row 5 (values, locked) | C5 `=$G$46` · E5 `=$G$47` · G5 `=$G$48` · I5 `=$G$49` · K5 `=$G$50` · M5 `=$C$56` · O5 `=$G$57` |
| AQ7 header | `x ACV−MMR` (DESK band; visible; off print area) |
| AQ8:AQ42 (locked) | `=IF(OR($AB8="",$AC8=""),"",$AB8-$AC8)` fmt `$#,##0;[Red]($#,##0)` |
| FLAGS additions (labels E54:E57, values G54:G57, locked) | `Wholesaled` G54 `=COUNTIFS($T$8:$T$42,"<>",$AA$8:$AA$42,"Wholesale",$AI$8:$AI$42,1)+COUNTIFS($T$8:$T$42,"<>",$AA$8:$AA$42,"Auction",$AI$8:$AI$42,1)` · `ACV−MMR Σ` G55 `=SUMIFS($AQ$8:$AQ$42,$T$8:$T$42,"<>",$AI$8:$AI$42,1)` · `ACV−MMR n` G56 `=COUNTIFS($AB$8:$AB$42,"<>",$AC$8:$AC$42,"<>",$T$8:$T$42,"<>",$AI$8:$AI$42,1)` · `Water` G57 `=SUMPRODUCT(($A$8:$A$42="Used")*$AI$8:$AI$42*($Q$8:$Q$42<0))` |
| C68 | literal `left(d)` from §1 |
| C69 (days 1–30) | `=IF($C$64="","-",IF($C$62>=$C$64*{elapsed}/GoalSellingDays,"● AHEAD",IF($C$62>=0.9*$C$64*{elapsed}/GoalSellingDays,"● ON PACE","● BEHIND")))` — numerator literal, denominator now the named cell (July inlined /27) |
| C69 (Aug 31) | July's GOAL HIT/SHORT variant verbatim |
| New CF | water: Q8:Q42 `=AND($A8="Used",$AI8=1,N($Q8)<0)` red fill/white bold · missing-field amber on P, Q, AF: `=AND($AI8=1,$P8="")` (resp. `$Q8=""`, `$AF8="")` · over-allowance: AQ8:AQ42 `=AND($AQ8<>"",$AQ8>BM_ACV_OVER_MMR)` red bold |
| Nav row 3 | July pattern; prev/next wrap Aug 31↔Aug 1 |

MTD chain: Aug 1 `C62 =$G$46` / `C63 =$G$49`; Aug n≥2 `C62 ='Aug {n-1}'!$C$62+$G$46` etc. (July pattern).

## 6. Dashboard

July layout with these deltas:

- **Roster (fixes D4):** AD4:AD19 `='Staff & Lists'!A5` … `A20`. All helper SUMPRODUCTs (AE4:BI19 units via AJ/AK, AE23:BI38 gross, BK/BM/BN rank chain, AE41:BI45 channels vs BP41:45) — July patterns, Aug refs.
- **Per-day agg U4:AB34** → 31 rows: `U='Aug n'!$G$47` V=`$G$48` W=`$C$54` X=`$C$55` Y=`$C$57` Z/AA/AB=`COUNTIF('Aug n'!$AM|AN|AO$8:$AM|AN|AO$42,"Y")`. **New AC4:AC34** `='Aug n'!$C$46` (per-day New units).
- **Date block:** BR4:BR29 = the 26 serials; `BT4 =MIN(GoalSellingDays,COUNTIF($BR$4:$BR$29,"<="&TODAY()))` · `BT5 =MAX(0,COUNTIF($BR$4:$BR$29,">="&TODAY()))` · BT6/BT7 `='Aug 31'!$C$62/$C$63`. New intel chains (31-term, July-idiom): `BT10` water `='Aug 1'!$G$57+…+'Aug 31'!$G$57` · `BT11` new units `=SUM(AC4:AC34)` · `BT12` wholesaled `='Aug 1'!$G$54+…` · `BT13` spread Σ `='Aug 1'!$G$55+…` · `BT14` spread n `='Aug 1'!$G$56+…`.
- **M11 pace verdict:** July formula with `/27` → `/GoalSellingDays` (twice).
- **New pace row 12:** B12 `Units Pace` C12 `=IF(BT4=0,"—",ROUND(BT6/BT4*GoalSellingDays,1))` D12 `=IF(OR(GoalUnitsTotal="",BT4=0),"",IF(C12>=GoalUnitsTotal,"▲ +"&TEXT(C12-GoalUnitsTotal,"0.0"),"▼ "&TEXT(C12-GoalUnitsTotal,"0.0")))` · F12 `Gross Pace` G12 `=IF(BT4=0,"—",ROUND(BT7/BT4*GoalSellingDays,0))` I12 `=IF(OR(GoalGrossTotal="",BT4=0),"",IF(G12>=GoalGrossTotal,"▲ "&TEXT(G12-GoalGrossTotal,"$#,##0"),"▼ "&TEXT(G12-GoalGrossTotal,"$#,##0")))`.
- **Calendar rows 14–26 (6 week pairs)**; hyperlink chips + `nu · $x.xk` strips per July pattern; `closed` under each of the 5 Sundays. Visible blocks below shift +2 rows: leaderboard header A28, rows 29–45 (16 ranks; formulas = July row-28 family, `$BN$4:$BN$19` unchanged); CHANNEL MIX N28–N34; PRODUCTS (MTD) N36: VSC Q37 `=SUM(Z4:Z34)`, LoJack Q38, Int/Ext Q39.
- **New INTEL band rows 47–56 (cols A..Q):**
  - A47 `USED DESK & F&I INTEL — MTD`
  - B48 `Used:New` C48 `=IF(BT11=0,"—",ROUND((BT6-BT11)/BT11,2))` D48 `=IF(C48="—","",IF(C48>=BM_USED_TO_NEW,"▲ at/above "&TEXT(BM_USED_TO_NEW,"0.00"),"▼ below "&TEXT(BM_USED_TO_NEW,"0.00")))`
  - F48 `Water deals` G48 `=BT10` (CF red when >0) · I48 `Wholesaled %` J48 `=IF(W_total=0,"—",BT12/W_total)` where `W_total=SUM(W4:W34)`; verdict K48 `=IF(J48="—","",IF(J48<=BM_IMMED_WHOLESALE,"✓ under cap","⚠ over "&TEXT(BM_IMMED_WHOLESALE,"0%")))`
  - B50 `VSC pen` C50 `=IF(BT6=0,"—",SUM(Z4:Z34)/BT6)` D50 `=IF(C50="—","",IF(C50>=BM_VSC_PEN,"✓","⚠ vs "&TEXT(BM_VSC_PEN,"0%")))` · F50 `LoJack` G50 `=IF(BT6=0,"—",SUM(AA4:AA34)/BT6)` · I50 `Int/Ext` J50 `=IF(BT6=0,"—",SUM(AB4:AB34)/BT6)`
  - B52 `PVR front` C52 `=IF(BT6=0,"—",SUM(U4:U34)/BT6)` · E52 `back` F52 `=IF(BT6=0,"—",SUM(V4:V34)/BT6)` · H52 `total` I52 `=IF(BT6=0,"—",BT7/BT6)`
  - Rows 54–56 `F&I MANAGER SPLIT`: per manager m∈{`='Staff & Lists'!G5`,`G6`} (names in B55/B56): deals D, VSC E, LoJack F, Int/Ext G as 31-term SUMPRODUCT chains, e.g. deals `=SUMPRODUCT(('Aug 1'!$I$8:$I$42=$B55)*'Aug 1'!$AI$8:$AI$42)+…`; product % `=IF($D55=0,"—",SUMPRODUCT(('Aug 1'!$I$8:$I$42=$B55)*'Aug 1'!$AI$8:$AI$42*('Aug 1'!$AM$8:$AM$42="Y"))+… /$D55)` (per-product columns; AM→E, AN→F, AO→G).
- Appraisal-capture tile lives on Trade Report (§10), not duplicated here.

## 7. Scoreboard

July verbatim (chains → `'Aug 1'..'Aug 31'`, `'Jul 31'`→`'Aug 31'`) plus:
- **Bars col G** at G8:G10, G14:G16: `=IF(OR($C8="-",N($C8)=0),"",REPT("█",MIN(20,ROUND($D8/$C8*20,0)))&IF($D8>=$C8," ✔",""))` (T1; blank when no goal).
- **PACE block** rows 24–27: B24 `PACE — projected finish`; B25 `Units` C25 `=IF(Dashboard!$BT$4=0,"-",ROUND('Aug 31'!$C$62/Dashboard!$BT$4*GoalSellingDays,1))` D25 `=IF(OR(GoalUnitsTotal="",C25="-"),"-",IF(C25>=GoalUnitsTotal,"▲ +"&TEXT(C25-GoalUnitsTotal,"0.0"),"▼ "&TEXT(C25-GoalUnitsTotal,"0.0")))`; B26 `Gross` C26/D26 same shape with `$C$63`, GoalGrossTotal, `$#,##0`.

## 8. Commissions (D1+D4 fixes inside)

Layout/visible table/audits as July; rosters `T4:T19 ='Staff & Lists'!A5…A20`. Helper families
re-gated on credits (per-day, rep r, day tab D):

- Units (rows 4–19): `=SUMPRODUCT((D!$F$8:$F$42=$Tr)*D!$AJ$8:$AJ$42+(D!$G$8:$G$42=$Tr)*D!$AK$8:$AK$42)`
- Gross (rows 23–38): same credit expression `*(D!$Q$8:$Q$42+D!$R$8:$R$42)`
- Pay (rows 42–57): same credit expression `*LOOKUP(((D!$Q$8:$Q$42+D!$R$8:$R$42)*((D!$Q$8:$Q$42+D!$R$8:$R$42)>0)),'Pay Plan'!$D$5:$K$5,INDEX('Pay Plan'!$D$6:$K$12,$BBr,0))` (July's clamp+retro-tier LOOKUP, status gate replaced by credits)
- BA `=SUM(U:AD)` fast-start (days 1–10) · BB tier `=MATCH(BD,'Pay Plan'!$C$6:$C$12,1)` · BC products (SP1, per July assumption A4): `=SUMPRODUCT((D!$F$8:$F$42=$Tr)*D!$AI$8:$AI$42*((D!$AM$8:$AM$42="Y")+(D!$AN$8:$AN$42="Y")+(D!$AO$8:$AO$42="Y")))+…` · BD/BE/BF sums · BH4 delivered check `='Aug 1'!$G$46+'Aug 1'!$E$46+…` → use Σ per-tab `$G$46` (total units) 31-term chain · BH5 products chain AI-gated · BH6/BH7/BH8 July verbatim.
- Visible row/audit formulas July verbatim (they reference helpers). Draw N7:N22 yellow unlocked.

## 9. Nightly Text

July verbatim with Aug refs; ranges `Dashboard!$BR$4:$BR$29`; A2 `DATE(2026,8,1)`. New:
G13 `Unit pace` H13 `=IF($E$8=0,0,($E$12+$H$12)/$E$8*COUNT(Dashboard!$BR$4:$BR$29))` ·
F13 `=IF(OR(GoalGrossTotal="",$E$8=0),"",IF($E$13>=GoalGrossTotal,"▲","▼"))` ·
I13 `=IF(OR(GoalUnitsTotal="",$E$8=0),"",IF($H$13>=GoalUnitsTotal,"▲","▼"))`.
Message A23 / readiness A22 unchanged.

## 10. Trade Report

July structure (recap row 7, day rows 9–39 ← Aug refs) plus:
- Day-row cols: I9 `Wholesaled` `='Aug 1'!$G$54` · J9 `ΣACV−MMR` `='Aug 1'!$G$55` · K9 `n` `='Aug 1'!$G$56` (K narrow/gray) · L9 `Aged` `=IF(AND(E9>0,B9<=TODAY()-BM_TURNIN_DAYS),"⏰ AGED","")`.
- **D5 fix**: day-tab C58 becomes `=COUNTIFS($T$8:$T$42,"<>",$Z$8:$Z$42,"N",$AI$8:$AI$42,1)` so kept-counts are delivered-gated like trades.
- Recap additions (labels row 6, values row 7): H `Capture %` `=IF(Dashboard!$BT$6=0,"—",B7/Dashboard!$BT$6)` + verdict vs BM_APPR_TRADE · I `Whlsl %` `=IF(B7=0,"—",SUM(I9:I39)/B7)` + verdict vs BM_IMMED_WHOLESALE (⚠ when above) · J `Avg ACV−MMR` `=IF(SUM(K9:K39)=0,"—",SUM(J9:J39)/SUM(K9:K39))` + CF vs BM_ACV_OVER_MMR · K `Aged` `=COUNTIF(L9:L39,"⏰ AGED")`.

## 11. Deal Explorer

July machinery verbatim (criteria row 5, B6 counter, ✓ col A, 10 link cols, 35 rows × 31
days, B-col literal Aug dates fmt `ddd m/d`): links → `'Aug n'`. Changes: freeze A8; B5 gets
`DataValidation(list, SalespeopleList)`; **native table `DealLedger` over A7:L1092**
(TableStyleMedium2, banded rows, header filter) replacing the sheet-level autofilter.

## 12. Goals / Pay Plan / Leaderboard / Guide

- **Goals**: title AUGUST 2026; C5 `August 2026`, C6 31, **C7 5, C8 26**; formulas July verbatim; yellow inputs empty.
- **Pay Plan**: verbatim copy (values, labels, assumption note), hidden, dollar cells unlocked.
- **Leaderboard**: July formulas (Dashboard helpers unchanged rows) + bars restyled: `=IF(OR(MAX(Dashboard!$BK$4:$BK$19)=0,N(C6)=0),"",REPT("█",ROUND(20*C6/MAX(Dashboard!$BK$4:$BK$19),0)))`.
- **Guide**: rewritten plain-language (Phase 3) covering: daily flow, status semantics, glance strip, water/over-allowance flags, AQ column, Benchmarks tuning, pace tiles, Trade Report intel, Explorer table filtering, Commissions single delivered-definition. Live PVR line → `'Aug 31'`.

## 13. Build order, git, QA hooks

1. `extract_styles()` → `spec_refs/styles.json` (one-time July introspection, committed).
2. Phase 2 prototype: Staff & Lists+Benchmarks → Pay Plan → Goals → `Aug 1` template → Dashboard wired to Aug 1 only → 7-deal test matrix → `recalc.py` → G3 package.
3. Phase 3: clone template ×31 from CONFIG → all reports → Guide → purge test deals (scripted scan: non-empty grid input cells must be 0) → commit per sheet group.
4. Phase 4: 9-point QA gauntlet (prompt list) → G4.
- Commits per sheet group; tags `gate-2-approved` … `gate-4-shipped`; STATE.md updated every chunk.
- Empty-sheet grace: every new formula above already guards div-by-zero/blank goals (`IF(...=0,"—"...)`, `N()` guards); QA #7 verifies with zero deals.
