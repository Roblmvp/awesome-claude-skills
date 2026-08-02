#!/usr/bin/env python3
"""Independent cross-check of AUDIT.md claims via raw XML parsing (no openpyxl for
structure claims) + a full formula-reference tokenizer for the dead-column claim.
Methodologically independent from tools/audit.py."""
import re
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

SRC = Path(__file__).resolve().parent.parent / "source" / "July_2026_Ford_Deal_Log_Master.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
z = zipfile.ZipFile(SRC)

# map sheet name -> sheetN.xml via workbook.xml + rels
wbx = ET.fromstring(z.read("xl/workbook.xml"))
rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
rid2tgt = {r.get("Id"): r.get("Target") for r in rels}
name2file, name2state = {}, {}
for sh in wbx.find("m:sheets", NS):
    rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    tgt = rid2tgt[rid]
    name2file[sh.get("name")] = "xl/" + tgt.lstrip("/")
    name2state[sh.get("name")] = sh.get("state", "visible")

shared = [t.findtext("m:t", default="", namespaces=NS) if t.find("m:t", NS) is not None
          else "".join(r.findtext("m:t", default="", namespaces=NS) for r in t.findall("m:r", NS))
          for t in ET.fromstring(z.read("xl/sharedStrings.xml"))] if "xl/sharedStrings.xml" in z.namelist() else []

DAY = [f"Jul {d}" for d in range(1, 32)]
COL = re.compile(r"([A-Z]{1,3})(\d+)$")

def cidx(c):
    v = 0
    for ch in c:
        v = v * 26 + ord(ch) - 64
    return v
AP = cidx("AP")

def cells(sheetname):
    root = ET.fromstring(z.read(name2file[sheetname]))
    for c in root.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"):
        ref = c.get("r"); m = COL.match(ref)
        col, row = m.group(1), int(m.group(2))
        f = c.find("m:f", NS); v = c.find("m:v", NS)
        # shared formulas: master carries text; slaves are <f t="shared" si=N/> with no text.
        # is_formula must be True for both, else cached <v> masquerades as a literal.
        yield col, row, ref, (f.text if f is not None else None), \
              (v.text if v is not None else None), c.get("t"), c.get("s"), (f is not None)

print("== CHECK 1: grid emptiness + formula-column identity (XML pass) ==")
bad = []
frm_count = defaultdict(int)
lit_count = defaultdict(int)
for tab in DAY:
    for col, row, ref, f, v, t, s, is_f in cells(tab):
        if 8 <= row <= 42 and cidx(col) <= AP:
            if is_f:
                frm_count[col] += 1
            elif v is not None:
                lit_count[col] += 1
                bad.append(f"{tab}!{ref}={v!r}")
print("  formula cells/col:", dict(sorted(frm_count.items())))
print("  literal cells in grid:", len(bad), bad[:5] or "→ EMPTY TEMPLATE CONFIRMED")
assert set(frm_count) == {"M", "S", "AI", "AJ", "AK", "AL", "AP"} and all(n == 1085 for n in frm_count.values()), "formula column set/count mismatch"

print("\n== CHECK 2: full-reference tokenizer — dead columns ==")
# collect every formula + DV formula in the workbook, tokenize ALL cell/range refs
ref_re = re.compile(r"(?:'(?P<q>[^']+)'|(?P<u>\b[A-Za-z][A-Za-z0-9_. ]*?))?!?\$?(?P<c1>[A-Z]{1,2})\$?(?P<r1>\d+)(?::\$?(?P<c2>[A-Z]{1,2})\$?(?P<r2>\d+))?")
def colspan(c1, c2):
    def n(c):
        v = 0
        for ch in c: v = v * 26 + ord(ch) - 64
        return v
    a, b = n(c1), n(c2 or c1)
    out = []
    for i in range(min(a, b), max(a, b) + 1):
        s, x = "", i
        while x: x, r = divmod(x - 1, 26); s = chr(65 + r) + s
        out.append(s)
    return out

consumed = defaultdict(set)   # day-grid col -> consumer descriptions
def scan_formula(fstr, home_sheet, home_row):
    for m in ref_re.finditer(fstr):
        tgt = m.group("q") or m.group("u")
        # determine target sheet: explicit or same-sheet
        if tgt is not None and "!" not in fstr[m.start():m.end()]:
            # tokenizer may grab function names as 'u'; require ! right after name
            pass
        seg = fstr[m.start():m.end()]
        sheet = tgt if (tgt and "!" in seg) else home_sheet
        if sheet not in DAY:
            continue
        r1, r2 = int(m.group("r1")), int(m.group("r2") or m.group("r1"))
        # overlap grid rows 8..42?
        if r2 < 8 or r1 > 42:
            continue
        for cc in colspan(m.group("c1"), m.group("c2")):
            if cidx(cc) <= AP:
                consumed[cc].add(f"{home_sheet}")

for name in name2file:
    for col, row, ref, f, v, t, s, is_f in cells(name):
        if f:
            scan_formula(f, name, row)
# data validation formulas (from XML)
for tab in DAY:
    root = ET.fromstring(z.read(name2file[tab]))
    for dv in root.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}dataValidation"):
        for f in dv:
            if f.text:
                scan_formula(f.text, tab, 8)
                consumed_by_dv = True
# conditional formatting formulas
cf_refs = defaultdict(set)
for tab in DAY[:1]:
    root = ET.fromstring(z.read(name2file[tab]))
    for cf in root.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}conditionalFormatting"):
        for rule in cf:
            for f in rule.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}formula"):
                if f.text:
                    for m in ref_re.finditer(f.text):
                        r1 = int(m.group("r1"))
                        if 8 <= r1 <= 42:
                            for cc in colspan(m.group("c1"), m.group("c2")):
                                cf_refs[cc].add(f.text[:40])

all_cols = colspan("A", "AP")
dead = [c for c in all_cols if c not in consumed]
print("  consumed by formulas/DV:", sorted(consumed, key=lambda c: (len(c), c)))
print("  DEAD (no formula/DV consumer):", dead)
print("  of the dead, referenced by CF only:", {c: sorted(cf_refs[c]) for c in dead if c in cf_refs})

print("\n== CHECK 3: M-column lock state via styles XML ==")
styles = ET.fromstring(z.read("xl/styles.xml"))
xfs = styles.find("m:cellXfs", NS)
def locked_of_style(s):
    if s is None: return True
    xf = xfs[int(s)]
    prot = xf.find("m:protection", NS)
    if prot is not None and prot.get("locked") is not None:
        return prot.get("locked") != "0"
    return True  # default locked
for tab in ["Jul 1", "Jul 15", "Jul 31"]:
    states = {}
    for col, row, ref, f, v, t, s, is_f in cells(tab):
        if row == 8 and col in ("A", "M", "S", "Q", "AI", "AJ", "AK", "AL", "AP", "AM"):
            states[col] = locked_of_style(s)
    print(f"  {tab} row8 locked-state: {states}")

print("\n== CHECK 4: sheet protection + freeze panes + autofilter + tables (XML) ==")
for name in ["Deal Explorer", "Jul 1", "Dashboard", "Commissions", "Nightly Text", "Pay Plan"]:
    root = ET.fromstring(z.read(name2file[name]))
    prot = root.find("m:sheetProtection", NS)
    pane = root.find("m:sheetViews/m:sheetView/m:pane", NS)
    af = root.find("m:autoFilter", NS)
    tparts = root.find("m:tableParts", NS)
    print(f"  {name}: protection={'yes' if prot is not None else 'NO'} pwd={'yes' if prot is not None and (prot.get('password') or prot.get('hashValue')) else 'no'} "
          f"pane={pane.get('topLeftCell') if pane is not None else None} state={name2state[name]} "
          f"autofilter={af.get('ref') if af is not None else None} tables={'yes' if tparts is not None else 'no'}")

print("\n== CHECK 5: delivered-definition divergence (string scan of all formulas) ==")
comm_delivered = day_ai = 0
for name in name2file:
    for col, row, ref, f, v, t, s, is_f in cells(name):
        if f and '="Delivered"' in f.replace("'", ""):
            comm_delivered += 1
        if f and 'Pending"' in f and 'Unwind"' in f:
            day_ai += 1
print(f"  formulas requiring Status=\"Delivered\": {comm_delivered} (expect 1488+ on Commissions + Explorer criteria area)")
print(f"  formulas using Pending/Unwind exclusion (AI family): {day_ai} (expect 1085)")
# where are the ="Delivered" ones?
locs = defaultdict(int)
for name in name2file:
    for col, row, ref, f, v, t, s, is_f in cells(name):
        if f and '"Delivered"' in f:
            locs[name] += 1
print("  by sheet:", dict(locs))

print("\n== CHECK 6: 'Dead' status absent ==")
hits = 0
for name in name2file:
    for col, row, ref, f, v, t, s, is_f in cells(name):
        for payload in (f, shared[int(v)] if (t == "s" and v is not None) else v):
            if payload and isinstance(payload, str) and re.search(r'\bDead\b', payload):
                hits += 1
                print("   HIT:", name, ref, payload[:80])
print("  'Dead' occurrences:", hits)

print("\nALL CROSS-CHECKS COMPLETE")
