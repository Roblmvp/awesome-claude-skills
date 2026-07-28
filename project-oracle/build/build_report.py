#!/usr/bin/env python3
"""Assemble the ORACLE visual report: compute SVG charts from forecast data,
inline fonts, emit artifact version (no wrapper) + standalone print version."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
def read(p): return open(os.path.join(HERE, p)).read()

# ---------------- chart helpers ----------------
def fnum(x): return f"{x:g}"

def rounded_bar_h(x, y, w, h, r, round_left, round_right, fill, opacity=1.0, tip=""):
    """Horizontal-run rect with selective end rounding via overlay patches."""
    s = f'<rect x="{fnum(x)}" y="{fnum(y)}" width="{fnum(w)}" height="{fnum(h)}" rx="{r}" fill="{fill}" opacity="{opacity}"/>'
    if not round_left:
        s += f'<rect x="{fnum(x)}" y="{fnum(y)}" width="{fnum(min(r, w/2))}" height="{fnum(h)}" fill="{fill}" opacity="{opacity}"/>'
    if not round_right:
        s += f'<rect x="{fnum(x + w - min(r, w/2))}" y="{fnum(y)}" width="{fnum(min(r, w/2))}" height="{fnum(h)}" fill="{fill}" opacity="{opacity}"/>'
    if tip:
        s += (f'<rect x="{fnum(x)}" y="{fnum(y-4)}" width="{fnum(w)}" height="{fnum(h+8)}" fill="transparent" '
              f'data-tip="{tip}" tabindex="0" role="img" aria-label="{tip}"/>')
    return s

def rounded_bar_v(x, y, w, h, r, fill, opacity=1.0, tip=""):
    """Vertical bar: rounded top, square baseline."""
    s = f'<rect x="{fnum(x)}" y="{fnum(y)}" width="{fnum(w)}" height="{fnum(h)}" rx="{r}" fill="{fill}" opacity="{opacity}"/>'
    s += f'<rect x="{fnum(x)}" y="{fnum(y + h - min(r, h/2))}" width="{fnum(w)}" height="{fnum(min(r, h/2))}" fill="{fill}" opacity="{opacity}"/>'
    if tip:
        s += (f'<rect x="{fnum(x-4)}" y="{fnum(y-8)}" width="{fnum(w+8)}" height="{fnum(h+8)}" fill="transparent" '
              f'data-tip="{tip}" tabindex="0" role="img" aria-label="{tip}"/>')
    return s

# ---------------- 1. scenario spectrum ----------------
def chart_spectrum():
    W, BAR_H, GAP = 1000, 46, 2
    segs = [  # display order: benign -> adverse (diverging arms)
        ("E", "Upside", 8,  "var(--sc-E)", "#fff",     "E — Upside Reacceleration: 8%"),
        ("A", "Soft landing", 28, "var(--sc-A)", "#131c2b", "A — Grinding Soft Landing: 28%"),
        ("B", "Rolling slowdown", 19, "var(--sc-B)", "#131c2b", "B — Rolling Slowdown: 19%"),
        ("D", "Sticky inflation", 20, "var(--sc-D)", "#131c2b", "D — Sticky Inflation / Hawkish Fed: 20%"),
        ("C", "Recession", 25, "var(--sc-C)", "#fff",  "C — Conventional Recession (24-mo window): 25%"),
    ]
    total_gap = GAP * (len(segs) - 1)
    usable = W - total_gap
    out, x = [], 0.0
    H = BAR_H + 44
    for i, (ltr, name, pct, fill, inkc, tip) in enumerate(segs):
        w = usable * pct / 100.0
        out.append(rounded_bar_h(x, 0, w, BAR_H, 4, i == 0, i == len(segs) - 1, fill, tip=tip))
        cx = x + w / 2
        out.append(f'<text x="{fnum(cx)}" y="{BAR_H/2+5}" text-anchor="middle" font-size="15" font-weight="500" fill="{inkc}">{ltr}&#8201;{pct}%</text>')
        # under-labels: name (muted)
        anchor = "middle"; tx = cx
        if i == 0: anchor, tx = "start", x
        if i == len(segs) - 1: anchor, tx = "end", x + w
        out.append(f'<text x="{fnum(tx)}" y="{BAR_H+22}" text-anchor="{anchor}" font-size="11.5" fill="var(--muted)">{name}</text>')
        x += w + GAP
    # polarity axis under labels
    out.append(f'<text x="0" y="{BAR_H+40}" font-size="10" letter-spacing="1.5" fill="var(--muted)">&#9668; MORE BENIGN</text>')
    out.append(f'<text x="{W}" y="{BAR_H+40}" text-anchor="end" font-size="10" letter-spacing="1.5" fill="var(--muted)">MORE ADVERSE &#9658;</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Scenario probabilities: E 8, A 28, B 19, D 20, C 25 percent">' + "".join(out) + "</svg>"

# ---------------- 2. SAAR line ----------------
def chart_saar():
    W, H = 470, 240
    ML, MR, MT, MB = 40, 46, 16, 34
    pw, ph = W - ML - MR, H - MT - MB
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
    vals   = [14.8, 15.8, 16.1, 16.1, 16.1, 16.5, 16.7]
    y0, y1 = 14.0, 17.0
    def X(i): return ML + pw * i / (len(vals) - 1)
    def Y(v): return MT + ph * (1 - (v - y0) / (y1 - y0))
    out = []
    for g in [14, 15, 16, 17]:
        out.append(f'<line x1="{ML}" y1="{fnum(Y(g))}" x2="{W-MR}" y2="{fnum(Y(g))}" stroke="var(--grid)" stroke-width="1"/>')
        out.append(f'<text x="{ML-8}" y="{fnum(Y(g)+4)}" text-anchor="end" font-size="11" fill="var(--muted)">{g}</text>')
    out.append(f'<line x1="{ML}" y1="{fnum(Y(y0))}" x2="{W-MR}" y2="{fnum(Y(y0))}" stroke="var(--baseline)" stroke-width="1"/>')
    solid = " ".join(f"{fnum(X(i))},{fnum(Y(v))}" for i, v in enumerate(vals[:6]))
    out.append(f'<polyline points="{solid}" fill="none" stroke="var(--series)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    out.append(f'<line x1="{fnum(X(5))}" y1="{fnum(Y(vals[5]))}" x2="{fnum(X(6))}" y2="{fnum(Y(vals[6]))}" stroke="var(--series)" stroke-width="2" stroke-dasharray="5 4" stroke-linecap="round"/>')
    for i, v in enumerate(vals):
        m = months[i]; f = " (forecast)" if i == 6 else ""
        tip = f"{m} 2026: {v}M SAAR{f}"
        if i == 6:
            out.append(f'<circle cx="{fnum(X(i))}" cy="{fnum(Y(v))}" r="4.5" fill="var(--surface)" stroke="var(--series)" stroke-width="2"/>')
        else:
            out.append(f'<circle cx="{fnum(X(i))}" cy="{fnum(Y(v))}" r="4" fill="var(--series)"/>')
        out.append(f'<circle cx="{fnum(X(i))}" cy="{fnum(Y(v))}" r="12" fill="transparent" data-tip="{tip}" tabindex="0" role="img" aria-label="{tip}"/>')
        out.append(f'<text x="{fnum(X(i))}" y="{H-12}" text-anchor="middle" font-size="10.5" fill="var(--muted)">{m}</text>')
    out.append(f'<text x="{fnum(X(5))}" y="{fnum(Y(16.5)-12)}" text-anchor="middle" font-size="11.5" font-weight="500" fill="var(--ink)">16.5</text>')
    out.append(f'<text x="{fnum(X(6)+8)}" y="{fnum(Y(16.7)+4)}" font-size="11.5" font-weight="500" fill="var(--ink)">16.7F</text>')
    out.append(f'<text x="{fnum(X(0))}" y="{fnum(Y(14.8)-12)}" text-anchor="middle" font-size="11" fill="var(--muted)">14.8</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="SAAR by month 2026, rising from 14.8 million in January to 16.5 in June, 16.7 forecast for July">' + "".join(out) + "</svg>"

# ---------------- 3. recession cumulative ----------------
def chart_recession():
    W, H = 470, 240
    ML, MR, MT, MB = 40, 52, 16, 34
    pw, ph = W - ML - MR, H - MT - MB
    hor = [3, 6, 9, 12, 15, 18, 21, 24]
    vals = [5, 9, 13, 16, 19, 21, 23, 25]
    y0, y1 = 0, 32
    def X(i): return ML + pw * i / (len(vals) - 1)
    def Y(v): return MT + ph * (1 - (v - y0) / (y1 - y0))
    out = []
    for g in [0, 10, 20, 30]:
        out.append(f'<line x1="{ML}" y1="{fnum(Y(g))}" x2="{W-MR}" y2="{fnum(Y(g))}" stroke="var(--grid)" stroke-width="1"/>')
        out.append(f'<text x="{ML-8}" y="{fnum(Y(g)+4)}" text-anchor="end" font-size="11" fill="var(--muted)">{g}%</text>')
    # base-rate reference
    out.append(f'<line x1="{ML}" y1="{fnum(Y(30))}" x2="{W-MR}" y2="{fnum(Y(30))}" stroke="var(--muted)" stroke-width="1" stroke-dasharray="3 4"/>')
    out.append(f'<text x="{W-MR+6}" y="{fnum(Y(30)+4)}" font-size="9.5" fill="var(--muted)">base</text>')
    out.append(f'<text x="{W-MR+6}" y="{fnum(Y(30)+15)}" font-size="9.5" fill="var(--muted)">rate</text>')
    pts = " ".join(f"{fnum(X(i))},{fnum(Y(v))}" for i, v in enumerate(vals))
    area = f"{ML},{fnum(Y(0))} " + pts + f" {fnum(X(len(vals)-1))},{fnum(Y(0))}"
    out.append(f'<polygon points="{area}" fill="var(--risk)" opacity="0.12"/>')
    out.append(f'<polyline points="{pts}" fill="none" stroke="var(--risk)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    out.append(f'<line x1="{ML}" y1="{fnum(Y(0))}" x2="{W-MR}" y2="{fnum(Y(0))}" stroke="var(--baseline)" stroke-width="1"/>')
    for i, v in enumerate(vals):
        tip = f"By month {hor[i]}: {v}% cumulative chance a recession has begun"
        r = 4.5 if i == len(vals) - 1 else 3
        out.append(f'<circle cx="{fnum(X(i))}" cy="{fnum(Y(v))}" r="{r}" fill="var(--risk)"/>')
        out.append(f'<circle cx="{fnum(X(i))}" cy="{fnum(Y(v))}" r="12" fill="transparent" data-tip="{tip}" tabindex="0" role="img" aria-label="{tip}"/>')
        out.append(f'<text x="{fnum(X(i))}" y="{H-12}" text-anchor="middle" font-size="10.5" fill="var(--muted)">{hor[i]}</text>')
    out.append(f'<text x="{fnum(X(7)+9)}" y="{fnum(Y(25)+4)}" font-size="12" font-weight="500" fill="var(--ink)">25%</text>')
    out.append(f'<text x="{fnum((ML+W-MR)/2)}" y="{H-1}" text-anchor="middle" font-size="9.5" letter-spacing="1" fill="var(--muted)">MONTHS AHEAD</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Cumulative recession probability rising from 5 percent at 3 months to 25 percent at 24 months, below the roughly 30 percent base rate">' + "".join(out) + "</svg>"

# ---------------- 4. tier payments ----------------
def chart_tiers():
    W = 470
    rows = [
        ("Prime-weighted avg", "6.39% APR", 740, "var(--seq-1)"),
        ("All-credit market", "9.58% APR", 809, "var(--seq-2)"),
        ("Subprime", "13.44% APR", 897, "var(--seq-3)"),
    ]
    BAR_H, GAP, TOP, LBL_H = 34, 26, 8, 16
    ML, MR = 8, 66
    pw = W - ML - MR
    vmax = 1000.0
    out = []
    y = TOP
    H = TOP + len(rows) * (BAR_H + LBL_H + GAP) - GAP + 14
    for name, apr, pay, fill in rows:
        out.append(f'<text x="{ML}" y="{y+11}" font-size="11.5" fill="var(--ink-2)">{name} &#183; <tspan fill="var(--muted)">{apr}</tspan></text>')
        by = y + LBL_H
        w = pw * pay / vmax
        tip = f"{name} at {apr}: ${pay}/mo on $44,156 over 72 months"
        s = f'<rect x="{ML}" y="{by}" width="{fnum(w)}" height="{BAR_H}" rx="4" fill="{fill}"/>'
        s += f'<rect x="{ML}" y="{by}" width="4" height="{BAR_H}" fill="{fill}"/>'
        s += f'<rect x="{ML-2}" y="{by-3}" width="{fnum(w+6)}" height="{BAR_H+6}" fill="transparent" data-tip="{tip}" tabindex="0" role="img" aria-label="{tip}"/>'
        out.append(s)
        out.append(f'<text x="{fnum(ML+w+10)}" y="{by+BAR_H/2+5}" font-size="14" font-weight="500" fill="var(--ink)">${pay}</text>')
        y = by + BAR_H + GAP
    out.append(f'<line x1="{ML}" y1="{fnum(y-GAP+8)}" x2="{ML}" y2="{TOP+LBL_H-4}" stroke="var(--baseline)" stroke-width="1"/>')
    return f'<svg viewBox="0 0 {W} {fnum(H)}" width="100%" role="img" aria-label="Monthly payment on the same 44,156 dollar 72-month note: prime 740, all-credit 809, subprime 897 dollars">' + "".join(out) + "</svg>"

# ---------------- 5. off-lease wave ----------------
def chart_offlease():
    W, H = 470, 250
    ML, MR, MT, MB = 40, 16, 26, 36
    pw, ph = W - ML - MR, H - MT - MB
    data = [("2025", 1.9, False), ("2026", 2.4, True), ("2027", 2.8, True)]
    y0, y1 = 0.0, 4.6
    def Y(v): return MT + ph * (1 - (v - y0) / (y1 - y0))
    out = []
    for g in [0, 1, 2, 3, 4]:
        out.append(f'<line x1="{ML}" y1="{fnum(Y(g))}" x2="{W-MR}" y2="{fnum(Y(g))}" stroke="var(--grid)" stroke-width="1"/>')
        out.append(f'<text x="{ML-8}" y="{fnum(Y(g)+4)}" text-anchor="end" font-size="11" fill="var(--muted)">{g}M</text>')
    slot = pw / len(data)
    bw = slot * 0.52
    for i, (yr, v, est) in enumerate(data):
        x = ML + slot * i + (slot - bw) / 2
        top = Y(v)
        lab = f"{yr}{'E' if est else ''}"
        tip = f"{lab}: ~{v}M lease returns" + (" (estimate)" if est else "")
        out.append(rounded_bar_v(x, top, bw, Y(0) - top, 4, "var(--series)", 0.8 if est else 1.0, tip))
        out.append(f'<text x="{fnum(x+bw/2)}" y="{fnum(top-8)}" text-anchor="middle" font-size="12.5" font-weight="500" fill="var(--ink)">{v}M</text>')
        out.append(f'<text x="{fnum(x+bw/2)}" y="{H-16}" text-anchor="middle" font-size="11" fill="var(--muted)">{lab}</text>')
    out.append(f'<line x1="{ML}" y1="{fnum(Y(4.0))}" x2="{W-MR}" y2="{fnum(Y(4.0))}" stroke="var(--muted)" stroke-width="1.2" stroke-dasharray="4 4"/>')
    out.append(f'<text x="{W-MR}" y="{fnum(Y(4.0)-7)}" text-anchor="end" font-size="10.5" fill="var(--muted)">pre-2020 norm ~4M</text>')
    out.append(f'<line x1="{ML}" y1="{fnum(Y(0))}" x2="{W-MR}" y2="{fnum(Y(0))}" stroke="var(--baseline)" stroke-width="1"/>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Off-lease returns: 1.9 million 2025, 2.4 estimated 2026, 2.8 estimated 2027, versus a pre-2020 norm near 4 million">' + "".join(out) + "</svg>"

# ---------------- assemble ----------------
tpl = read("report-template.html")
tpl = tpl.replace("{{BARLOW600}}", read("fonts/BarlowSemiCondensed-600.woff2.b64"))
tpl = tpl.replace("{{BARLOW700}}", read("fonts/BarlowSemiCondensed-700.woff2.b64"))
tpl = tpl.replace("{{PLEX400}}",  read("fonts/IBMPlexMono-400.woff2.b64"))
tpl = tpl.replace("{{PLEX500}}",  read("fonts/IBMPlexMono-500.woff2.b64"))
tpl = tpl.replace("{{CHART_SPECTRUM}}", chart_spectrum())
tpl = tpl.replace("{{CHART_SAAR}}", chart_saar())
tpl = tpl.replace("{{CHART_RECESSION}}", chart_recession())
tpl = tpl.replace("{{CHART_TIERS}}", chart_tiers())
tpl = tpl.replace("{{CHART_OFFLEASE}}", chart_offlease())

assert "{{" not in tpl, "unreplaced placeholder remains"

open(os.path.join(HERE, "report-content.html"), "w").write(tpl)
standalone = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width, initial-scale=1">'
              "</head><body>" + tpl + "</body></html>")
open(os.path.join(HERE, "report.html"), "w").write(standalone)
print("built: report-content.html (artifact) + report.html (standalone)")
print("sizes:", os.path.getsize(os.path.join(HERE, "report-content.html")), "bytes")
