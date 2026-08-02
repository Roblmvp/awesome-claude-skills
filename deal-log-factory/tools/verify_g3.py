#!/usr/bin/env python3
"""Gate 3 verification: expected-vs-actual over the recalculated DRAFT workbook.
Reads cached values (data_only) — file must have been through recalc.py first."""
import sys
import warnings
from pathlib import Path

import openpyxl

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent.parent
wb = openpyxl.load_workbook(HERE / "August_2026_Ford_Deal_Log_Master.xlsx", data_only=True)  # never saved

d1, db, cm, sb, tr, nt, de, gl = (wb[s] for s in
    ["Aug 1", "Dashboard", "Commissions", "Scoreboard", "Trade Report", "Nightly Text", "Deal Explorer", "Goals"])

CHECKS = [
    # (label, actual, expected)
    ("Aug1 grid: ① AI/AJ/AK",        (d1["AI8"].value, d1["AJ8"].value, d1["AK8"].value), (1, 1, 0)),
    ("Aug1 grid: ① AL channel",      d1["AL8"].value, "Internet"),
    ("Aug1 grid: ① AP tier ($3,500)", d1["AP8"].value, 4),
    ("Aug1 grid: ① AQ ACV−MMR",      d1["AQ8"].value, 800),
    ("Aug1 grid: ② split AJ/AK",     (d1["AJ9"].value, d1["AK9"].value), (0.5, 0.5)),
    ("Aug1 grid: ③ delivered, water", (d1["AI10"].value, d1["G57"].value), (1, 1)),
    ("Aug1 grid: ④ pending AI=0",    d1["AI11"].value, 0),
    ("Aug1 grid: ⑤ unwind AI=0",     d1["AI12"].value, 0),
    ("Aug1 grid: ⑥ cash S=front",    d1["S13"].value, 1800),
    ("Aug1 grid: ⑦ AP tier ($9,000)", d1["AP14"].value, 8),
    ("Aug1 summary: units N/U/T",    (d1["C46"].value, d1["E46"].value, d1["G46"].value), (2, 3, 5)),
    ("Aug1 summary: front/fin/total", (d1["G47"].value, d1["G48"].value, d1["G49"].value), (10500, 6200, 16700)),
    ("Aug1 summary: trades/pending/CPO/kept", (d1["G50"].value, d1["C56"].value, d1["C57"].value, d1["C58"].value), (1, 1, 1, 0)),
    ("Aug1 FLAGS+: whlsl/ΣAQ/n/water", (d1["G54"].value, d1["G55"].value, d1["G56"].value, d1["G57"].value), (0, 800, 1, 1)),
    ("Aug1 glance strip C5/I5/M5/O5", (d1["C5"].value, d1["I5"].value, d1["M5"].value, d1["O5"].value), (5, 16700, 1, 1)),
    ("Aug1 pace: MTD/left/verdict",  (d1["C62"].value, d1["C68"].value, d1["C69"].value), (5, 26, "-")),
    ("Dash tiles: units/gross",      (db["B7"].value, db["D7"].value), (5, 16700)),
    ("Dash tiles: front/fin/trades/CPO", (db["G7"].value, db["I7"].value, db["K7"].value, db["L7"].value), (10500, 6200, 1, 1)),
    ("Dash BT4/BT5 (recalc 8/2)",    (db["BT4"].value, db["BT5"].value), (1, 25)),
    ("Dash pace: units/gross (×26)", (db["C12"].value, db["G12"].value), (130, 434200)),
    ("Dash intel: used:new / flag",  (db["C48"].value, db["D48"].value), (1.5, "▲ at/above 1.00")),
    ("Dash intel: water/whlsl%/cap", (db["G48"].value, db["J48"].value, db["K48"].value), (1, 0, "✓ under cap")),
    ("Dash intel: VSC pen / verdict", (db["C50"].value, db["D50"].value), (0.4, "⚠ vs 50%")),
    ("Dash intel: PVR f/b/t",        (db["C52"].value, db["F52"].value, db["I52"].value), (2100, 1240, 3340)),
    ("Dash F&I: MCCAN deals/VSC",    (db["B55"].value, db["D55"].value, db["E55"].value), ("JOHN MCCAN", 2, 0.5)),
    ("Dash F&I: MAGED deals/VSC",    (db["B56"].value, db["D56"].value, db["E56"].value), ("JACOB MAGED", 2, 0.5)),
    ("Dash leaderboard #1",          (db["B30"].value, db["H30"].value, db["J30"].value), ("FEDY ALI", 2, 12500)),
    ("Comm FEDY: units/gross/PVR",   (cm["C7"].value, cm["D7"].value, cm["E7"].value), (2, 12500, 6250)),
    ("Comm FEDY: tier/flat/prod/earn", (cm["F7"].value, cm["G7"].value, cm["J7"].value, cm["K7"].value), ("0–7", 900, 50, 950)),
    ("Comm CHAD (deal ② SP1): units/gross/flat/earn", (cm["C8"].value, cm["D8"].value, cm["G8"].value, cm["K8"].value), (0.5, 1000, 125, 125)),
    ("Comm RICH (deal ② SP2): units/flat", (cm["C9"].value, cm["G9"].value), (0.5, 125)),
    ("Comm audits 1–6 all ✓",        tuple(str(cm[f"I{r}"].value)[:1] for r in range(26, 32)), tuple("✓" * 6)),
    ("Scoreboard MTD N/U/T",         (sb["D8"].value, sb["D9"].value, sb["D10"].value), (2, 3, 5)),
    ("Scoreboard bars blank (no goals)", tuple(sb[f"G{r}"].value for r in (8, 10, 16)), (None, None, None)),
    ("Scoreboard pace units/gross",  (sb["C25"].value, sb["C26"].value), (130, 434200)),
    ("Trade recap: trades/turned/kept/ACV", (tr["B7"].value, tr["C7"].value, tr["D7"].value, tr["F7"].value), (1, 1, 0, 15000)),
    ("Trade recap: capture/whlsl/spread/aged", (tr["H7"].value, tr["I7"].value, tr["J7"].value, tr["K7"].value), (0.2, 0, 800, 0)),
    # L9 evaluates to "" which openpyxl's data_only pass reads back as None
    ("Trade Aug1 row: I/J/K/L",      (tr["I9"].value, tr["J9"].value, tr["K9"].value, tr["L9"].value), (0, 800, 1, None)),
    ("Nightly: MTD New/Used (thru 8/2)", (nt["E12"].value, nt["H12"].value), (2, 3)),
    ("Nightly: gross pace / unit pace", (nt["E13"].value, nt["H13"].value), (434200, 130)),
    ("Explorer: counter line",       de["B6"].value, "Showing 7 of 7 deals booked this month"),
    ("Explorer: row1 = deal ① ✓/deal#/gross", (de["A8"].value, de["C8"].value, de["J8"].value), ("✓", 5001, 3500)),
    ("Goals: consistency check idle", str(gl["A29"].value), "-"),
    ("Empty-sheet grace: Aug 2 summary", (wb["Aug 2"]["G46"].value, wb["Aug 2"]["C69"].value), (0, "-")),
]

fails = 0
print(f"{'CHECK':52s} | {'EXPECTED':34s} | {'ACTUAL':34s} | PASS")
print("-" * 140)
for label, actual, expected in CHECKS:
    ok = actual == expected
    fails += (not ok)
    print(f"{label:52s} | {str(expected):34s} | {str(actual):34s} | {'✅' if ok else '❌'}")
print("-" * 140)
print(f"RESULT: {len(CHECKS) - fails}/{len(CHECKS)} passed")
sys.exit(1 if fails else 0)
