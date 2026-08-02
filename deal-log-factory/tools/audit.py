#!/usr/bin/env python3
"""Phase 0 audit of July_2026_Ford_Deal_Log_Master.xlsx.

Two-pass load (formulas + data_only, the latter never saved).
Dumps everything needed for AUDIT.md into audit_out/.
"""
import json
import re
import sys
import warnings
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter

warnings.filterwarnings("ignore")

SRC = Path(__file__).resolve().parent.parent / "source" / "July_2026_Ford_Deal_Log_Master.xlsx"
OUT = Path(__file__).resolve().parent.parent / "audit_out"
OUT.mkdir(exist_ok=True)

wb = openpyxl.load_workbook(SRC, data_only=False)
wbv = openpyxl.load_workbook(SRC, data_only=True)  # NEVER SAVED

DAY_TABS = [f"Jul {d}" for d in range(1, 32)]
REPORT_TABS = [s for s in wb.sheetnames if s not in DAY_TABS]

# ---------------------------------------------------------------- helpers
def dump_sheet(name, max_row=None, max_col=None):
    """Full cell dump: coord | formula-or-value | cached value | number format."""
    ws, wsv = wb[name], wbv[name]
    lines = []
    mr = max_row or ws.max_row
    mc = max_col or ws.max_column
    for row in ws.iter_rows(min_row=1, max_row=mr, max_col=mc):
        for c in row:
            if c.value is None:
                continue
            v = wsv[c.coordinate].value
            lines.append(f"{c.coordinate}\t{c.value!r}\t| cached={v!r}\t| fmt={c.number_format}")
    return "\n".join(lines)

# ---------------------------------------------------------------- 1. sheet map
sheet_map = []
for name in wb.sheetnames:
    ws = wb[name]
    tc = ws.sheet_properties.tabColor
    hidden_cols = [d for d, dim in ws.column_dimensions.items() if dim.hidden]
    hidden_rows = [r for r, dim in ws.row_dimensions.items() if dim.hidden]
    fp = ws.freeze_panes
    prot = ws.protection.sheet
    sheet_map.append(dict(
        name=name, state=ws.sheet_state, max_row=ws.max_row, max_col=ws.max_column,
        tab_color=tc.rgb if tc else None, hidden_cols=hidden_cols,
        hidden_rows=hidden_rows[:10], freeze=fp, protected=prot,
        merged=len(ws.merged_cells.ranges),
        n_dv=len(ws.data_validations.dataValidation),
        n_cf=len(ws.conditional_formatting),
    ))
(OUT / "sheet_map.json").write_text(json.dumps(sheet_map, indent=1))

# ---------------------------------------------------------------- 2. day tab anatomy (Jul 1 as reference)
ref = "Jul 1"
ws = wb[ref]
anatomy = []
# header rows: find the row containing column headers
for r in range(1, 8):
    vals = [(get_column_letter(c.column), c.value) for c in ws[r] if c.value is not None]
    anatomy.append(f"ROW {r}: {vals}")
(OUT / "day_header_rows.txt").write_text("\n".join(anatomy))

# per-column: header, formula pattern (from first deal row), count formulas vs inputs
# first find deal rows: rows where column A area is the deal grid
day_dump = dump_sheet(ref)
(OUT / "day_jul1_full_dump.txt").write_text(day_dump)

# ---------------------------------------------------------------- 3. per-column usage census across all 31 day tabs
# Determine header row + deal row span dynamically from Jul 1 later; assume headers row and
# deal rows discovered from dump. We'll compute usage generically: for every column, count
# non-empty cells in rows >= DEAL_ROW_START across all day tabs, split formula vs literal.
# We detect deal-row span by finding the contiguous block of rows with data validation / borders.
# Simpler: report usage per column for rows 5..69 and let the analyst read it with the dump.
DEAL_ROW_START = None
# find first row where A-column value pattern suggests grid start (row after header row that
# contains 'Deal' style headers). We'll grep for the row containing 'Deal #' or similar.
header_row = None
for r in range(1, 10):
    rowvals = [str(c.value) for c in ws[r] if c.value is not None]
    joined = " | ".join(rowvals).lower()
    if "deal" in joined and ("customer" in joined or "stock" in joined):
        header_row = r
        break
usage = defaultdict(lambda: Counter())
formula_pattern = defaultdict(lambda: defaultdict(set))  # col -> normalized formula -> set(tab:row)
if header_row:
    DEAL_ROW_START = header_row + 1
    for tab in DAY_TABS:
        w = wb[tab]
        for row in w.iter_rows(min_row=DEAL_ROW_START, max_row=w.max_row, max_col=w.max_column):
            for c in row:
                if c.value is None:
                    continue
                col = get_column_letter(c.column)
                if isinstance(c.value, str) and c.value.startswith("="):
                    usage[col]["formula"] += 1
                    norm = re.sub(r"\d+", "#", c.value)
                    formula_pattern[col][norm].add(f"{tab}!{c.coordinate}")
                else:
                    usage[col]["literal"] += 1
census = {}
hdrs = {get_column_letter(c.column): c.value for c in ws[header_row]} if header_row else {}
for col in [get_column_letter(i) for i in range(1, ws.max_column + 1)]:
    census[col] = dict(header=hdrs.get(col), literal=usage[col]["literal"], formula=usage[col]["formula"])
(OUT / "day_column_census.json").write_text(json.dumps(dict(header_row=header_row, deal_row_start=DEAL_ROW_START, census=census), indent=1))

# formula pattern deviants within day tabs
dev_lines = []
for col, pats in sorted(formula_pattern.items()):
    if len(pats) > 1:
        dev_lines.append(f"COLUMN {col}: {len(pats)} distinct normalized patterns")
        for p, locs in sorted(pats.items(), key=lambda kv: -len(kv[1])):
            sample = sorted(locs)[:5]
            dev_lines.append(f"  [{len(locs)} cells] {p!r}  e.g. {sample}")
(OUT / "day_formula_deviants.txt").write_text("\n".join(dev_lines) or "NONE - every formula column uniform across all 31 tabs")

# ---------------------------------------------------------------- 4. report sheet dumps
for name in REPORT_TABS:
    safe = name.replace(" & ", "_").replace(" ", "_").lower()
    if name == "Deal Explorer":
        # huge; dump rows 1..40 fully + one row per day block sample + formula pattern census
        ws2 = wb[name]
        txt = dump_sheet(name, max_row=45)
        pats = defaultdict(set)
        for row in ws2.iter_rows(min_row=1, max_row=ws2.max_row, max_col=ws2.max_column):
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    norm = re.sub(r"\d+", "#", c.value)
                    norm = re.sub(r"'Jul #'", "'Jul #'", norm)
                    pats[norm].add(c.coordinate)
        txt += "\n\n== FORMULA PATTERNS (normalized) ==\n"
        for p, locs in sorted(pats.items(), key=lambda kv: -len(kv[1])):
            txt += f"[{len(locs)}] {p!r}  e.g. {sorted(locs)[:3]}\n"
        (OUT / f"sheet_{safe}.txt").write_text(txt)
    elif name == "Staff & Lists":
        # wide; dump only cols A..Q (staff/lists/benchmark area) + row1 headers of the rest
        (OUT / f"sheet_{safe}.txt").write_text(dump_sheet(name, max_col=17))
    else:
        (OUT / f"sheet_{safe}.txt").write_text(dump_sheet(name))

# ---------------------------------------------------------------- 5. cross-sheet dependency graph
dep = defaultdict(Counter)
sheet_ref_re = re.compile(r"'([^']+)'!|(?<![A-Za-z0-9_'])([A-Za-z][A-Za-z0-9_. ]*?)!")
for name in wb.sheetnames:
    for row in wb[name].iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                for m in sheet_ref_re.finditer(c.value):
                    tgt = m.group(1) or m.group(2)
                    if tgt and tgt in wb.sheetnames and tgt != name:
                        dep[name][tgt] += 1
dep_lines = []
for src in wb.sheetnames:
    if dep[src]:
        tg = ", ".join(f"{t}×{n}" for t, n in dep[src].most_common())
        dep_lines.append(f"{src} -> {tg}")
(OUT / "dependency_graph.txt").write_text("\n".join(dep_lines))

# ---------------------------------------------------------------- 6. defect hunt
defects = []
# 6a. cached error values
for name in wbv.sheetnames:
    for row in wbv[name].iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("#"):
                defects.append(f"ERRORVAL {name}!{c.coordinate} = {c.value}")
# 6b. lowercased formulas (LibreOffice parse-failure tell)
for name in wb.sheetnames:
    for row in wb[name].iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                body = re.sub(r'"[^"]*"', "", c.value)
                funcs = re.findall(r"([a-z_]{3,})\(", body)
                funcs = [f for f in funcs if f.lower() == f and f not in ("_xlfn",)]
                if funcs:
                    defects.append(f"LOWERCASE {name}!{c.coordinate}: {funcs} in {c.value[:90]!r}")
# 6c. external refs
for name in wb.sheetnames:
    for row in wb[name].iter_rows():
        for c in row:
            if isinstance(c.value, str) and "[1]" in c.value:
                defects.append(f"EXTREF {name}!{c.coordinate}: {c.value[:90]!r}")
# 6d. modern functions
BAD = re.compile(r"\b(XLOOKUP|XMATCH|FILTER|SORT|UNIQUE|SEQUENCE)\(")
for name in wb.sheetnames:
    for row in wb[name].iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("=") and BAD.search(c.value):
                defects.append(f"MODERNFN {name}!{c.coordinate}: {c.value[:90]!r}")
(OUT / "defects.txt").write_text("\n".join(defects) or "NONE")

# ---------------------------------------------------------------- 7. hyperlinks + data validation inventory (Jul 1 + Jul 5 + reports)
lines = []
for name in ["Jul 1", "Jul 5", "Jul 31", "Deal Explorer", "Guide"]:
    ws3 = wb[name]
    for hl in ws3._hyperlinks:
        lines.append(f"HYPERLINK {name}!{hl.ref} -> location={hl.location!r} target={hl.target!r}")
    for dv in ws3.data_validations.dataValidation:
        lines.append(f"DV {name} {dv.sqref} type={dv.type} formula1={str(dv.formula1)[:80]!r} showDropDown={dv.showDropDown}")
(OUT / "links_and_dv.txt").write_text("\n".join(lines))

# ---------------------------------------------------------------- 8. formula count totals
tot = Counter()
for name in wb.sheetnames:
    n = sum(1 for row in wb[name].iter_rows() for c in row
            if isinstance(c.value, str) and c.value.startswith("="))
    tot[name] = n
(OUT / "formula_counts.json").write_text(json.dumps(dict(total=sum(tot.values()), per_sheet=dict(tot.most_common())), indent=1))

# ---------------------------------------------------------------- 9. conditional formatting inventory
cf_lines = []
for name in wb.sheetnames:
    for rng in wb[name].conditional_formatting:
        for rule in rng.rules:
            cf_lines.append(f"{name} {rng.sqref} | type={rule.type} op={getattr(rule,'operator',None)} formula={getattr(rule,'formula',None)}")
(OUT / "conditional_formatting.txt").write_text("\n".join(cf_lines) or "NONE")

print("AUDIT DUMPS COMPLETE")
print("total formulas:", sum(tot.values()))
print("defect lines:", len(defects))
print("header_row:", header_row, "deal_row_start:", DEAL_ROW_START)
