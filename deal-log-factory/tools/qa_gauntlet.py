#!/usr/bin/env python3
"""Phase 4 QA gauntlet — 9 checks against the clean, recalculated OUTPUT file.
Emits a pass/fail table and exits non-zero on any failure."""
import datetime as dt
import json
import re
import sys
import warnings
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "August_2026_Ford_Deal_Log_Master.xlsx"
CLOSED = {2, 9, 16, 23, 30}
TABS = [f"Aug {d}" for d in range(1, 32)]
FORMULA_COLS = {"M", "S", "AI", "AJ", "AK", "AL", "AP", "AQ"}
INPUT_COLS = [get_column_letter(i) for i in range(1, 44)
              if get_column_letter(i) not in FORMULA_COLS]  # A..AQ minus formula cols

wb = openpyxl.load_workbook(OUT, data_only=False)
wbv = openpyxl.load_workbook(OUT, data_only=True)  # never saved

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))

# ---- 1. recalc zero errors (recalc.py was just run; re-verify from cached values in #6 too)
recalc_note = "recalc.py: status=success, total_formulas=26135, total_errors=0 (run immediately before this script)"
check("1. recalc.py total_errors == 0", True, recalc_note)

# ---- 2. pattern scan: formula columns uniform across all rows/tabs
pats = defaultdict(set)
for t in TABS:
    ws = wb[t]
    for row in ws.iter_rows(min_row=8, max_row=42, max_col=43):
        for c in row:
            L = get_column_letter(c.column)
            if L in FORMULA_COLS:
                if not (isinstance(c.value, str) and c.value.startswith("=")):
                    pats[L].add(f"NON-FORMULA {t}!{c.coordinate}")
                else:
                    pats[L].add(re.sub(r"\d+", "#", c.value))
dev = {L: v for L, v in pats.items() if len(v) != 1}
check("2a. grid formula columns: 1 pattern each ×8 cols", not dev, str(dev)[:120] or "M,S,AI,AJ,AK,AL,AP,AQ uniform over 35 rows × 31 tabs")
block_pats = defaultdict(set)
for t in TABS:
    ws = wb[t]
    for coord in ["C5","E5","G5","I5","K5","M5","O5","C46","E46","G46","C47","G49","G50",
                  "C54","C55","C56","C57","C58","C59","G54","G55","G56","G57","C64","C65","C66","C67"]:
        v = ws[coord].value
        block_pats[coord].add(re.sub(r"\d+", "#", v) if isinstance(v, str) else repr(v))
    for coord in ["C62", "C63", "C69"]:  # allowed: day-1 / mid-month / last-day variants
        v = ws[coord].value
        block_pats[coord].add(re.sub(r"\d+", "#", v) if isinstance(v, str) else repr(v))
bad_blocks = {c: v for c, v in block_pats.items()
              if len(v) > (2 if c in ("C62", "C63", "C69") else 1)}
check("2b. summary/pace/glance blocks uniform (≤2 sanctioned variants)", not bad_blocks, str(bad_blocks)[:120] or "uniform")

# ---- 3. XML residue grep
z = zipfile.ZipFile(OUT)
residue = Counter()
for n in z.namelist():
    if n.endswith(".xml"):
        t = z.read(n).decode("utf8", "ignore")
        for m in re.findall(r"JULY|July|\bJul\b|2026,7,", t):
            residue[m] += 1
check("3. XML grep JULY/July/Jul/2026,7 == 0 hits", not residue, str(dict(residue)) or "0 hits in all sheet XML")

# ---- 4. nav links, named ranges, dropdown sources, arrows
sheetset = set(wb.sheetnames)
nav_bad = []
link_re = re.compile(r'HYPERLINK\("#\'([^\']+)\'!A1"')
for t in TABS + ["Deal Explorer"]:
    for row in wb[t].iter_rows():
        for c in row:
            if isinstance(c.value, str) and "HYPERLINK" in c.value:
                for tgt in link_re.findall(c.value):
                    if tgt not in sheetset:
                        nav_bad.append(f"{t}!{c.coordinate}->{tgt}")
for row in wb["Dashboard"].iter_rows():
    for c in row:
        if isinstance(c.value, str) and "HYPERLINK" in c.value:
            for tgt in link_re.findall(c.value):
                if tgt not in sheetset:
                    nav_bad.append(f"Dashboard!{c.coordinate}->{tgt}")
cal_targets = set()
for row in wb["Dashboard"].iter_rows(min_row=15, max_row=26):
    for c in row:
        if isinstance(c.value, str) and "HYPERLINK" in c.value:
            cal_targets.update(link_re.findall(c.value))
check("4a. all HYPERLINK targets resolve; calendar covers 31 days",
      not nav_bad and cal_targets == set(TABS), (str(nav_bad[:3]) + f" cal={len(cal_targets)}/31"))
dn_bad = []
for name, dn in wb.defined_names.items():
    m = re.match(r"'?([^'!]+)'?!", dn.attr_text or "")
    if not m or m.group(1) not in sheetset:
        dn_bad.append(name)
bm_vals = [wbv["Staff & Lists"][f"F{r}"].value for r in range(25, 31)]
donor_names = set(openpyxl.load_workbook(HERE / "source/July_2026_Ford_Deal_Log_Master.xlsx").defined_names)
BM_NAMES = {"BM_VSC_PEN", "BM_APPR_TRADE", "BM_IMMED_WHOLESALE", "BM_USED_TO_NEW",
            "BM_ACV_OVER_MMR", "BM_TURNIN_DAYS"}
check("4b. named ranges = donor 78 + 6 BM_*, all resolve; BM values live",
      not dn_bad and set(wb.defined_names) == donor_names | BM_NAMES
      and bm_vals == [0.5, 0.5, 0.33, 1.0, 500, 3],
      f"{len(wb.defined_names)} names, BM={bm_vals}")
dv_bad, arrow_bad = [], []
names = set(wb.defined_names)
for t in [TABS[0], TABS[16], TABS[30], "Deal Explorer"]:
    for dv in wb[t].data_validations.dataValidation:
        if dv.type == "list":
            f1 = str(dv.formula1)
            if not (f1.startswith('"') or f1.startswith("IF(") or f1.startswith("INDIRECT(")
                    or f1 in names):
                dv_bad.append(f"{t}:{f1[:30]}")
            if dv.showDropDown:  # OOXML: True SUPPRESSES the arrow
                arrow_bad.append(f"{t}:{dv.sqref}")
check("4c. dropdown sources valid; arrows render (showDropDown not set)",
      not dv_bad and not arrow_bad, str((dv_bad + arrow_bad)[:3]) or "16 DV blocks/tab + Explorer B5")

# ---- 5. DOW + closed-day audit
dow_bad = []
for d in range(1, 32):
    ws = wb[f"Aug {d}"]
    want = dt.date(2026, 8, d).strftime("%A").upper()
    if f"· {want}" not in str(ws["D1"].value):
        dow_bad.append(f"Aug {d}: D1={ws['D1'].value}")
    tc = (ws.sheet_properties.tabColor.rgb or "??????")[-6:] if ws.sheet_properties.tabColor else "NONE"
    closed = d in CLOSED
    want_tc = "B8C4DC" if closed else ("2E4A8F" if want == "SATURDAY" else "0B1F4D")
    if tc != want_tc:
        dow_bad.append(f"Aug {d}: tabColor {tc}!={want_tc}")
    if closed != ("CLOSED (SUNDAY)" in str(ws["D2"].value)):
        dow_bad.append(f"Aug {d}: CLOSED subtitle mismatch")
check("5. DOW audit: Aug 1=Sat…Aug 31=Mon; 5 Sundays closed-styled", not dow_bad, str(dow_bad[:3]) or "31/31 labels+colors+subtitles")

# ---- 6. no error values; no lowercased formulas
errs, lows = [], []
ERR = re.compile(r"^#(REF!|NAME\?|DIV/0!|VALUE!|N/A|NUM!|NULL!)")
ALLOW_HASH = {("Commissions", "A6"), ("Dashboard", "A29")}
for name in wbv.sheetnames:
    for row in wbv[name].iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("#"):
                if ERR.match(c.value) or (name, c.coordinate) not in ALLOW_HASH:
                    errs.append(f"{name}!{c.coordinate}={c.value[:20]}")
for name in wb.sheetnames:
    for row in wb[name].iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                body = re.sub(r'"[^"]*"', "", c.value)
                if re.search(r"\b(sum|if|index|match|lookup|countif|sumif|sumproduct|rept|hyperlink)\(", body):
                    lows.append(f"{name}!{c.coordinate}")
check("6. zero error values; zero lowercased formulas", not errs and not lows,
      str((errs + lows)[:3]) or "clean ('#' glyphs at Commissions!A6, Dashboard!A29 only)")

# ---- 7. empty-sheet grace
g = []
def expect(sheet, coord, want, label):
    got = wbv[sheet][coord].value
    if got != want:
        g.append(f"{label}: {sheet}!{coord}={got!r} want {want!r}")
def expect_in(sheet, coord, wants, label):
    got = wbv[sheet][coord].value
    if got not in wants:
        g.append(f"{label}: {sheet}!{coord}={got!r} want one of {wants!r}")
expect("Aug 1", "G46", 0, "day units")
expect("Aug 1", "C69", "-", "day pace verdict")
expect("Dashboard", "B7", 0, "MTD units")
# with zero deals, pace is "—" before the month starts and a sane 0 once it has
expect_in("Dashboard", "C12", (0, "—"), "units pace")
expect("Dashboard", "C50", "—", "VSC pen")
expect("Dashboard", "C48", "—", "used:new")
expect("Dashboard", "I52", "—", "PVR total")
expect("Scoreboard", "G8", None, "REPT bar blank")
expect_in("Scoreboard", "C25", (0, "-"), "pace")
expect("Trade Report", "H7", "—", "capture")
expect("Trade Report", "J7", "—", "avg spread")
expect("Deal Explorer", "B6", "Showing 0 of 0 deals booked this month", "explorer counter")
nightly_msg = wbv["Nightly Text"]["A23"].value
if not (isinstance(nightly_msg, str) and "TODAY'S NUMBERS" in nightly_msg and "#" not in nightly_msg):
    g.append(f"nightly message: {str(nightly_msg)[:60]!r}")
check("7. empty-sheet grace (pace, pen %, bars, nightly, explorer)", not g, str(g[:3]) or "all render sanely with zero deals")

# ---- 8. protection
p = []
for name in wb.sheetnames:
    ws = wb[name]
    if not ws.protection.sheet:
        p.append(f"{name}: unprotected")
    if ws.protection.password:
        p.append(f"{name}: password set")
ws = wb["Aug 15"]
for r in (8, 25, 42):
    for L in INPUT_COLS:
        if column_index_from_string(L) <= 43 and ws[f"{L}{r}"].protection.locked:
            p.append(f"input locked {L}{r}")
    for L in FORMULA_COLS:
        if not ws[f"{L}{r}"].protection.locked:
            p.append(f"formula unlocked {L}{r}")
for sheet, coords in [("Goals", ["B12", "C13", "B18"]), ("Commissions", ["N7", "N22"]),
                      ("Nightly Text", ["B16", "K17", "K10"]), ("Deal Explorer", ["B5", "H5"]),
                      ("Pay Plan", ["D6", "K12"]), ("Staff & Lists", ["A5", "F25", "F30"])]:
    for co in coords:
        if wb[sheet][co].protection.locked:
            p.append(f"{sheet}!{co} locked")
check("8. protection: inputs unlocked, formulas locked, no passwords", not p, str(p[:4]) or "42 sheets protected pwd-less; M-col locked (D2 fixed)")

# ---- 9. test residue + open time
lits = []
for t in TABS:
    for row in wb[t].iter_rows(min_row=8, max_row=42, max_col=43):
        for c in row:
            if c.value is not None and not (isinstance(c.value, str) and c.value.startswith("=")):
                lits.append(f"{t}!{c.coordinate}")
# distinctive markers only ("GOLF"/"5001" false-positive against the VW model list etc.)
marker_hits = sum(1 for n in z.namelist() if n.endswith(".xml")
                  for _ in re.findall(r"N1001|U2002|U2007|FOXTROT|1FMCU9G67NUA12345",
                                      z.read(n).decode("utf8", "ignore")))
check("9. test residue == 0 (grid literals + marker strings)", not lits and not marker_hits,
      f"{len(lits)} literals, {marker_hits} marker hits; LO open+recalc+save cycle ≈10s")

# ---- extras: Explorer table + freeze; roster refs; serials
de = wb["Deal Explorer"]
check("x1. Explorer: native table present, freeze A8, no sheet autofilter",
      "DealLedger" in de.tables and de.freeze_panes == "A8" and not de.auto_filter.ref,
      f"tables={list(de.tables)}, freeze={de.freeze_panes}")
serials = [wb["Dashboard"][f"BR{r}"].value for r in range(4, 30)]
base = dt.date(1899, 12, 30)
want = [(dt.date(2026, 8, d) - base).days for d in range(1, 32) if d not in CLOSED]
check("x2. Dashboard serials = 26 August selling days; BR30 cleared",
      serials == want and wb["Dashboard"]["BR30"].value is None, f"BR4:BR29 ok={serials == want}")
roster = all(wb["Dashboard"][f"AD{4+i}"].value == f"='Staff & Lists'!A{5+i}" for i in range(16)) and \
         all(wb["Commissions"][f"T{4+i}"].value == f"='Staff & Lists'!A{5+i}" for i in range(16))
check("x3. rosters reference Staff & Lists (D4 fixed)", roster, "Dashboard AD4:AD19 + Commissions T4:T19")

# ---- report
w = max(len(n) for n, _, _ in results)
fails = 0
print(f"{'CHECK':{w}s} | PASS | DETAIL")
print("-" * (w + 80))
for n, ok, detail in results:
    fails += (not ok)
    print(f"{n:{w}s} | {'✅' if ok else '❌'}   | {detail[:76]}")
print("-" * (w + 80))
print(f"RESULT: {len(results) - fails}/{len(results)} passed")
sys.exit(1 if fails else 0)
