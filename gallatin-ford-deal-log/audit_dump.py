#!/usr/bin/env python3
"""Phase 0 audit of July_2026_Ford_Deal_Log_Master.xlsx.

Two-pass load (formula pass + data_only pass; data_only NEVER saved).
Dumps everything needed for AUDIT.md into audit_data/.
"""
import json
import re
import warnings
from collections import Counter, defaultdict

import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string

warnings.filterwarnings("ignore")

SRC = "July_2026_Ford_Deal_Log_Master.xlsx"
wbf = openpyxl.load_workbook(SRC)                 # formula pass
wbv = openpyxl.load_workbook(SRC, data_only=True) # value pass — NEVER SAVED

DAY_TABS = [f"Jul {d}" for d in range(1, 32)]
DEAL_ROWS = range(8, 43)  # 35 deal rows
FORMULA_COLS = ["M", "S", "AI", "AJ", "AK", "AL", "AP"]
ALL_COLS = [get_column_letter(c) for c in range(1, 43)]
INPUT_COLS = [c for c in ALL_COLS if c not in FORMULA_COLS]

out = {}

# ---------- 1. Sheet map ----------
sheet_map = []
for ws in wbf.worksheets:
    tc = ws.sheet_properties.tabColor
    prot = ws.protection.sheet
    hidden_cols = [k for k, d in ws.column_dimensions.items() if d.hidden]
    hidden_rows = [r for r, d in ws.row_dimensions.items() if d.hidden]
    nf = sum(1 for row in ws.iter_rows() for c in row
             if isinstance(c.value, str) and c.value.startswith("="))
    ne = sum(1 for row in ws.iter_rows() for c in row if c.value is not None)
    sheet_map.append({
        "name": ws.title, "state": ws.sheet_state, "dims": ws.dimensions,
        "tab_color": tc.rgb if tc else None, "freeze": ws.freeze_panes,
        "protected": prot, "hidden_cols": hidden_cols, "hidden_rows": hidden_rows,
        "n_formulas": nf, "n_nonempty": ne,
        "n_merged": len(ws.merged_cells.ranges),
        "n_cf_rules": sum(len(cf.rules) for cf in ws.conditional_formatting),
        "n_dv": len(ws.data_validations.dataValidation),
    })
out["sheet_map"] = sheet_map

# ---------- 2. Named ranges ----------
out["named_ranges"] = {n: dn.value for n, dn in wbf.defined_names.items()}

# ---------- 3. Day-tab input-column usage census (values pass) ----------
usage = Counter()          # col -> non-empty count across all day tabs deal rows
usage_by_tab = defaultdict(Counter)
status_vals, type_vals, disp_vals, cpo_vals, ti_vals, rdr_vals = (Counter(),)*0 or (Counter(), Counter(), Counter(), Counter(), Counter(), Counter())
adsource_vals = Counter()
for t in DAY_TABS:
    ws = wbv[t]
    for r in DEAL_ROWS:
        for col in INPUT_COLS:
            v = ws[f"{col}{r}"].value
            if v is not None and v != "":
                usage[col] += 1
                usage_by_tab[t][col] += 1
        for col, ctr in (("AG", status_vals), ("A", type_vals), ("AA", disp_vals),
                         ("N", cpo_vals), ("Z", ti_vals), ("O", rdr_vals), ("AF", adsource_vals)):
            v = ws[f"{col}{r}"].value
            if v is not None and v != "":
                ctr[str(v)] += 1
hdr = {col: wbf["Jul 1"][f"{col}7"].value for col in ALL_COLS}
out["day_headers"] = hdr
out["usage_counts"] = {c: usage.get(c, 0) for c in INPUT_COLS}
out["value_censuses"] = {"Status_AG": dict(status_vals), "Type_A": dict(type_vals),
                         "Disposition_AA": dict(disp_vals), "CPO_N": dict(cpo_vals),
                         "TurnedIn_Z": dict(ti_vals), "RDR_O": dict(rdr_vals),
                         "AdSource_AF": dict(adsource_vals)}

# ---------- 4. Formula-pattern scan on day tabs ----------
def norm(f, row):
    """Normalize a formula by replacing the row number with @."""
    return re.sub(rf"(?<=[A-Z\$]){row}(?![0-9])", "@", f) if f else f

deviants = []
patterns = {}
for col in FORMULA_COLS:
    base = norm(wbf["Jul 1"][f"{col}8"].value or "", 8)
    patterns[col] = base
    for t in DAY_TABS:
        ws = wbf[t]
        for r in DEAL_ROWS:
            f = ws[f"{col}{r}"].value
            if not isinstance(f, str) or norm(f, r) != base:
                deviants.append(f"{t}!{col}{r} = {f!r}")
out["formula_patterns"] = patterns
out["pattern_deviants"] = deviants

# Also: input columns containing stray formulas
stray = []
for t in DAY_TABS:
    ws = wbf[t]
    for r in DEAL_ROWS:
        for col in INPUT_COLS:
            v = ws[f"{col}{r}"].value
            if isinstance(v, str) and v.startswith("="):
                stray.append(f"{t}!{col}{r} = {v[:80]!r}")
out["stray_formulas_in_input_cols"] = stray

# ---------- 5. Summary/footer block variance across day tabs ----------
foot = defaultdict(dict)
for t in DAY_TABS:
    ws = wbf[t]
    for addr in ("A1","D1","R1","A3","K3","A44","C62","C63","C64","C65","C66","C67","C68","C69","A61"):
        foot[addr][t] = ws[addr].value
out["footer_by_tab"] = foot

# ---------- 6. Error scan (values pass) ----------
ERRS = ("#REF!", "#NAME?", "#DIV/0!", "#VALUE!", "#N/A", "#NULL!", "#NUM!")
errors = []
for ws in wbv.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value in ERRS:
                errors.append(f"{ws.title}!{c.coordinate} = {c.value}")
out["value_errors"] = errors

# ---------- 7. Data validations ----------
dv_dump = {}
for ws in wbf.worksheets:
    lst = []
    for dv in ws.data_validations.dataValidation:
        lst.append({"type": dv.type, "formula1": dv.formula1,
                    "ranges": str(dv.sqref)})
    if lst:
        dv_dump[ws.title] = lst
out["data_validations_sample"] = {k: v for k, v in list(dv_dump.items())[:3]}
out["data_validation_sheets"] = {k: len(v) for k, v in dv_dump.items()}

# ---------- 8. Conditional formatting inventory (one day tab + others) ----------
cf_dump = {}
for name in ["Jul 1", "Dashboard", "Scoreboard", "Leaderboard", "Trade Report", "Commissions", "Deal Explorer", "Nightly Text"]:
    ws = wbf[name]
    lst = []
    for cf in ws.conditional_formatting:
        for rule in cf.rules:
            lst.append({"range": str(cf.sqref), "type": rule.type,
                        "operator": rule.operator, "formula": list(rule.formula) if rule.formula else None,
                        "text": rule.text})
    cf_dump[name] = lst
out["conditional_formatting"] = cf_dump

# ---------- 9. Cross-sheet dependency graph ----------
dep = defaultdict(Counter)
ref_re = re.compile(r"'([^']+)'!|(?<![A-Za-z0-9_'])([A-Za-z][A-Za-z0-9 &]*?)!")
for ws in wbf.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                for m in ref_re.finditer(c.value):
                    tgt = m.group(1) or m.group(2)
                    if tgt and tgt in wbf.sheetnames and tgt != ws.title:
                        dep[ws.title][tgt] += 1
out["dependency_graph"] = {k: dict(v) for k, v in dep.items()}

# ---------- 10. July totals sanity (values pass) ----------
tot_units = tot_front = tot_fin = tot_trades = 0
deals_logged = 0
neg_front_used = 0
acv_gt_mmr = 0
trades_with_both = 0
for t in DAY_TABS:
    ws = wbv[t]
    for r in DEAL_ROWS:
        if ws[f"D{r}"].value not in (None, ""):
            deals_logged += 1
        ai = ws[f"AI{r}"].value
        if ai == 1:
            tot_units += 1
            q = ws[f"Q{r}"].value or 0
            rr = ws[f"R{r}"].value or 0
            tot_front += q if isinstance(q, (int, float)) else 0
            tot_fin += rr if isinstance(rr, (int, float)) else 0
            if ws[f"T{r}"].value not in (None, ""):
                tot_trades += 1
            if ws[f"A{r}"].value == "Used" and isinstance(q, (int, float)) and q < 0:
                neg_front_used += 1
            acv, mmr = ws[f"AB{r}"].value, ws[f"AC{r}"].value
            if isinstance(acv, (int, float)) and isinstance(mmr, (int, float)):
                trades_with_both += 1
                if acv > mmr:
                    acv_gt_mmr += 1
out["july_totals"] = {"deals_logged_rows": deals_logged, "delivered_units": tot_units,
                      "front": tot_front, "finance": tot_fin, "total": tot_front + tot_fin,
                      "trades_on_delivered": tot_trades,
                      "used_neg_front": neg_front_used,
                      "trades_with_acv_and_mmr": trades_with_both,
                      "acv_over_mmr": acv_gt_mmr}

with open("audit_data.json", "w") as fh:
    json.dump(out, fh, indent=1, default=str)

# ---- console summary ----
print("== formula counts per sheet ==")
for s in sheet_map:
    print(f"  {s['name']:16} formulas={s['n_formulas']:6} nonempty={s['n_nonempty']:6} cf={s['n_cf_rules']:3} dv={s['n_dv']:3} prot={s['protected']} hiddencols={len(s['hidden_cols'])}")
print("TOTAL formulas:", sum(s["n_formulas"] for s in sheet_map))
print("\n== usage counts (input cols, all 31 tabs, rows 8-42) ==")
for c in INPUT_COLS:
    print(f"  {c:3} {str(hdr[c])[:22]:24} {usage.get(c,0)}")
print("\n== value censuses ==")
print(json.dumps(out["value_censuses"], indent=1))
print("\n== pattern deviants:", len(deviants), "==")
for d in deviants[:40]: print("  ", d)
print("\n== stray formulas in input cols:", len(stray), "==")
for s2 in stray[:20]: print("  ", s2)
print("\n== value errors:", len(errors), "==")
for e in errors[:40]: print("  ", e)
print("\n== data validation sheets ==", json.dumps(out["data_validation_sheets"]))
print("\n== july totals ==", json.dumps(out["july_totals"]))
print("\n== dependency graph ==")
for k, v in out["dependency_graph"].items():
    if k.startswith("Jul "): continue
    print(f"  {k:16} -> {dict(v)}")
daytab_deps = Counter()
for k, v in out["dependency_graph"].items():
    if k.startswith("Jul "):
        for tgt, n in v.items():
            daytab_deps[tgt] += n
print(f"  [day tabs agg]   -> {dict(daytab_deps)}")
