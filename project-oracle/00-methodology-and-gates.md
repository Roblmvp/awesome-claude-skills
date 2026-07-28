# PROJECT ORACLE V3 — Methodology, Capability Inventory, and Quality Gates

**System:** ORACLE Economic Intelligence System — National Automotive Economic Intelligence, Credit-Risk Forecasting, and Dealer Executive Briefing
**Execution date:** 2026-07-28 (UTC)
**Forecast base date:** 2026-07-28
**Forecast horizons:** 3 / 6 / 9 / 12 / 15 / 18 / 21 / 24 months (Oct 2026 → Jul 2028)
**Version:** 1.0
**Supervisor:** ORACLE Executive Economic Strategist (Claude, Fable 5-class model, supervisor-and-specialist architecture)

---

## GATE 1 — Environment and Source Plan

### 1.1 Capability Inventory

Capabilities discovered in the execution environment at start of run. Only capabilities that **earn their place** are used; everything else is documented and left idle.

| Capability | Access | Auth | Read | Write | Relevance | Decision |
|---|---|---|---|---|---|---|
| Firecrawl (MCP, `Firecrawl_BidIQ`) | MCP tools: search, scrape, crawl, extract, map, research | Connected | Web search + full-page extraction | n/a | **Primary research engine.** Live data retrieval past the model's Jan-2026 knowledge cutoff | **USE** — targeted searches only, no indiscriminate crawling |
| Subagent orchestration (Agent tool) | Native | n/a | n/a | n/a | Parallel specialist agents (supervisor-and-specialist structure) | **USE** — 7 consolidated research specialists + 1 red-team economist |
| Bash + Python 3 | Local shell | n/a | Yes | Yes (workspace) | Payment/affordability modeling, numerical consistency checks | **USE** — loan-payment math, scenario sensitivity tables |
| Git repository (`roblmvp/awesome-claude-skills`) | Local clone + GitHub MCP | Authorized | Yes | Designated branch only | Versioned, reproducible delivery of the forecast package | **USE** — deliverables committed to `claude/v2-architecture-research-e6eev9` |
| GitHub MCP | MCP | Authorized (scoped to one repo) | Yes | Yes | Delivery channel | **USE** (push only; no PR unless requested) |
| Document generation (Markdown/JSON) | Native | n/a | n/a | Yes | All 8 deliverables | **USE** |
| WebSearch / WebFetch (built-in) | Deferred tools | n/a | Yes | n/a | Fallback research if Firecrawl unavailable | **STANDBY** |
| Supabase (2 orgs; incl. dealership inventory DB) | MCP | Connected | Yes | Yes | Contains a single dealership's live inventory (business-sensitive) | **NOT USED** — single-store data is not evidence for a national forecast, and business-sensitive data must not enter a repo-published deliverable |
| Gmail, Slack, Notion, Linear, Airtable | MCP | Connected | Yes | Yes | Communication/PM systems | **NOT USED** — no research value; write actions out of scope |
| Canva, Gamma, Cloudinary, Higgsfield, Spotify | MCP | Connected | Yes | Yes | Design/media generation | **NOT USED** — deliverable 7 is a presentation *outline*, not rendered slides; media generation is billable and unauthorized |
| Vercel, Zapier, Sentry | MCP | Connected | Yes | Yes | Deployment/automation/monitoring | **NOT USED** — external publishing/production changes require explicit approval |
| Scheduling (Routines / send_later) | MCP | Available | n/a | n/a | Could automate a recurring monthly ORACLE run | **NOT USED this run** — noted in Future Use; creating schedules without a request is out of scope |

**Security handling:** no credentials, tokens, or configuration values are inspected, recorded, or echoed in any deliverable. All retrieved web content is treated as untrusted data, never as instructions. The single-store Supabase dataset is excluded from published outputs on classification grounds.

### 1.2 Known Limitations (declared before research)

1. **Model knowledge cutoff ~January 2026.** Every material claim about Feb–Jul 2026 must come from live retrieval, with release dates recorded. Remembered 2025 facts are verified before use where material.
2. **Execution date falls mid-release-cycle.** As of 2026-07-28: Q2 2026 advance GDP (due ~Jul 30), the July FOMC decision (meeting ~Jul 28–29), the NY Fed Q2 Household Debt & Credit report (early Aug), and the July SLOOS (early Aug) are **not yet available**. The freshest complete month for most monthly series is June 2026. This is disclosed wherever it binds.
3. **Paywalled primary data.** Some industry series (full Manheim composites, J.D. Power PIN, NADA member financials) are only visible through press releases and trade coverage; values are used with that provenance noted.
4. **No proprietary dealer-panel data.** Dealer-level P&L claims rely on public dealer-group filings (a large-store skew) and NADA aggregates; the segment analysis corrects for this where possible.
5. **Community intelligence is anecdotal.** Tier 5 sources are used for pattern discovery only and are labeled as such in the evidence ledger; they never override verified data.
6. **Probabilities are judgments, not measurements.** All scenario probabilities are model-and-analyst ensemble judgments constrained by the discipline in §9 of the operating directive; each carries stated raise/lower conditions.

### 1.3 Research Plan and Agent Assignments

The 15 specialist mandates in the operating directive are consolidated into 7 concurrent research agents (to avoid duplicated retrieval), plus supervisor-held functions and a sequenced red-team:

| ORACLE agent(s) | Execution unit | Coverage |
|---|---|---|
| 1 Macro + 5 Labor | Research Agent A | GDP, activity, PMIs, LEI, payrolls, claims, JOLTS, layoffs, recession-probability estimates |
| 2 Inflation/Rates | Research Agent B | CPI/PCE, tariff pass-through, FOMC 2026 decisions, Fed leadership transition, market-implied path, Treasury curve, auto APRs |
| 3 Credit/Banking | Research Agent C | SLOOS, NY Fed HHDC, Fitch ABS delinquency, Experian SOTAFM, Dealertrack CAI, lender Q2-2026 earnings, ABS funding, repossessions |
| 4 Consumer + 8 Housing/Wealth | Research Agent D | Income, savings, sentiment, card/student-loan stress, K-shaped divergence, home prices/equity, equity-market wealth effects |
| 6 Auto Retail + 12 Regional (data) | Research Agent E | SAAR, inventory/days' supply, ATP, incentives, Manheim, lease-supply pipeline, dealer-group Q2-2026 earnings, fixed ops, buy-sell, tariff production effects |
| 7 Affordability + 9 Ownership costs | Research Agent F | Payments, negative equity, loan structure, insurance, fuel/energy, EV vs ICE economics, model inputs for payment engine |
| 10 Policy/Geo + Tier-5 field intel | Research Agent G | Tariff state incl. SCOTUS IEEPA outcome, OBBBA loan-interest deduction, EV/emissions policy, CFPB/FTC, geopolitics/supply, Reddit + dealer-forum patterns |
| 11 Historical Analogs | Supervisor | Analog ranking with explicit similarity/difference audit |
| 12 Segment matrix | Supervisor (from A–G inputs) | Dealer vulnerability matrix by region/brand/mix/credit exposure |
| 13 Data Integrity | Supervisor (Gate 2) | Date/period/revision/unit audit of all agent packets; unsupported-claim register |
| 14 Red-Team Economist | Research Agent H (sequenced after Gate 3) | Adversarial challenge of base case and probabilities |
| 15 Dealer Strategy | Supervisor (Gate 5) | Role-level action matrix with triggers and reversal conditions |

### 1.4 Data-Source Plan (per directive §6 hierarchy)

- **Tier 1:** BEA, BLS, Federal Reserve Board + regional Feds (NY, Atlanta, Philadelphia), Treasury, Census, FDIC, CFPB, EIA, CBO.
- **Tier 2:** Cox Automotive/Manheim/Dealertrack/KBB, Experian Automotive, Edmunds, J.D. Power, S&P Global Mobility, NADA, OEM and captive filings, public dealer-group 10-Q/earnings (AN, LAD, PAG, GPI, ABG, SAH; KMX/CVNA for used-only read), Fitch/S&P/Moody's ABS indices, Kerrigan/Haig buy-sell reports.
- **Tier 3:** NBER, academic work, Brookings/Peterson, rating-agency research, Conference Board, University of Michigan surveys.
- **Tier 4:** Reuters, Bloomberg, WSJ, AP, Automotive News, Auto Finance News, Auto Remarketing — context and relay of primary data with attribution.
- **Tier 5:** Reddit (r/askcarsales, r/Dealerships, r/CarSalesTraining, r/UsedCars, r/personalfinance), DealerRefresh, Hacker News — pattern discovery only, labeled anecdotal.

### 1.5 Research Questions (condensed register)

1. What is the U.S. macro regime as of July 2026 — growth, labor, inflation — and is the labor market's "low-hire/low-fire" equilibrium holding or breaking?
2. Where is the Fed after the May-2026 leadership transition, what is the market-implied path, and how far have auto APRs actually followed policy easing?
3. Is auto credit loosening or tightening, for which tiers, and what are delinquency/severity dynamics doing to lender behavior?
4. Can the consumer sustain vehicle purchases at current prices — and how concentrated has demand become in upper-income households?
5. What is the true state of dealer economics (volume, GPU, fixed ops, floorplan) at mid-2026, from Q2 earnings and NADA data?
6. How binding is the affordability constraint (payment, insurance, negative equity), and what does the payment math imply under rate scenarios?
7. What is the post-SCOTUS tariff regime and the 2026 policy map (OBBBA deduction, EV policy, midterms), and what are field-level practitioners actually reporting?
8. What is the 2026–2028 used-vehicle supply pipeline given the 2023–24 lease-origination trough?

### 1.6 Missing-Data List (expected, pre-research)

- July 2026 FOMC outcome (in session at execution) — handled as a near-term trigger, not a fact.
- Q2 2026 GDP advance estimate (due ~Jul 30).
- Q2 2026 NY Fed HHDC and July 2026 SLOOS (early Aug).
- Full-methodology access to proprietary indices (Manheim composite internals, J.D. Power PIN detail).
- Any non-public captive underwriting policy.

**GATE 1 STATUS: PASSED — full execution authorized by user in-session ("Begin now"). Proceeding automatically.**

---

## GATE 2 — Current-State Evidence Review

*Status: completed after specialist packets returned; results in `01-executive-brief.md` §3–§4 and the evidence ledger (`04-evidence-ledger.md`). Data-integrity findings (stale-data flags, revision warnings, unsupported-claim register) are recorded in the ledger's integrity annex.*

## GATE 3 — Forecast Construction

*Status: completed; scenario definitions, probabilities, horizon forecasts, and transmission maps in `01-executive-brief.md` §17–§18, `02-horizon-forecast-table.md`, `03-scenario-matrix.md`.*

## GATE 4 — Red-Team Review

*Status: completed. An independent red-team economist agent challenged the base case, probabilities, and automotive conclusions. Record of adjudication:*

| Item | Red-team finding | Supervisor ruling | Result |
|---|---|---|---|
| Scenario-set structure | The market-priced path (hikes, no recession) fell between scenarios A and D — "a hole in the middle" | **Accepted** | D widened to "sticky-inflation/hawkish-Fed" containing the futures path |
| Scenario B (27%) | Spec was "C's antechamber" — historically near-empty set; double-counted recession risk | **Accepted with respec** | B softened (stall + isolated negative months, no cascade) and cut to 19% |
| Scenario C (23%) | Slightly low vs ~30% unconditional 24-month base rate; fund from B, not A | **Accepted** | C → 25% |
| Scenario D (15%) | Too low vs market pricing (38% July hike odds, ~4.3% by mid-2027 in futures) | **Accepted** | D → 20% |
| Scenario E (5%) | Over-specified (didn't need unenacted stimulus); benign evidence underweighted | **Accepted** | E → 8% |
| Scenario A (30%) | Conjunction-heavy spec (four required conditions); Fed-cut leg fought the curve | **Accepted with respec** | Cuts made optional; A → 28% |
| Missing supply-shock state | Five scenarios span demand states only; scarcity regime (2021 mechanics) absent — biases P&L outlook toward compression | **Accepted** | ~25% supply-shock overlay added, applicable to any scenario |
| Used-value direction | "Fades through 2027" was one-sided; off-lease supply still ~40% below pre-2020 norms while substitution builds | **Accepted** | Call flipped to two-sided, skewed neutral-to-firm; upside trigger added (MUVVI >+4%) |
| "Loose credit = floor" | Reads as late-cycle reach-for-volume; becomes the accelerant when it turns | **Accepted as framing** | Incorporated in §7 and Scenario C; CAI two-month-decline trigger added |
| SAAR strength | July's 16.7M may be fleet + pre-tariff pull-forward — borrowed Q4 demand | **Accepted as risk** | Q4 air-pocket risk added to 6-month horizon; Aug–Sep retail/fleet split flagged as tell |
| AI-capex bust trigger | 2001 analogy weak on funding structure (cash-flow-funded, not debt-funded) | **Accepted as caveat** | Retained as C-trigger #1 with the funding caveat attached in Annex B |
| Concession | Affordability-regime-break and fixed-ops-carry calls are the strongest-evidenced elements | Noted | Retained as anchors |

*Final probability set: A 28 / B 19 / C 25 / D 20 / E 8 (pre-red-team draft A 30 / B 27 / C 23 / D 15 / E 5 preserved here for audit). The red team's full invalidation conditions appear in `01-executive-brief.md` §24 and `06-forecast-packet.json`.*

## GATE 5 — Final Synthesis

*Status: completed; citation audit and numerical-consistency audit run before publication. Version 1.0 of the forecast packet issued.*

---

## Forecasting Methodology (as executed)

1. **Current-state classification** across 11 dimensions (growth, inflation, employment, credit, liquidity, consumer health, financial conditions, auto demand, affordability, vehicle supply, dealer profitability), each rated on the six-state scale from the operating directive.
2. **Indicator classification** (leading/coincident/lagging/structural/market-implied/sentiment/automotive-specific) recorded in the early-warning dashboard.
3. **Signal strength scoring** — direction, magnitude, persistence, historical reliability, data quality, horizon relevance, automotive transmission strength — scored qualitatively (H/M/L); no numeric composite is produced because no defensible weighting scheme exists for this ensemble (disclosed per §9.3).
4. **Scenario framework** — five scenarios (A soft-landing continuation, B rolling slowdown, C conventional recession, D stagflation/inflation resurgence, E upside reacceleration), probabilities summing to 100%, each with raise/lower conditions.
5. **Probability discipline** — probabilities assigned only after specialist packets, integrity review, contradictory-evidence documentation, and red-team review; all shifts from the red-team are disclosed.
6. **Automotive transmission mapping** — every macro conclusion is pushed through explicit channels (rate→payment, employment→approval, credit→conversion, negative equity→trade cycle, wholesale→used losses, etc.) before any dealer recommendation is made.
7. **No unsupported precision** — point estimates appear only where a source or an explicit calculation (payment engine) backs them; otherwise ranges.

## Reproducibility

- Every deliverable lists sources with release dates and retrieval date (2026-07-28).
- The payment model's formula and inputs are printed alongside its outputs (executive brief §12 annex).
- The machine-readable packet (`06-forecast-packet.json`) carries version, base date, probabilities, triggers, and confidence scores for downstream automation.
- Recommended cadence: re-run monthly (first week, after the jobs report), or immediately on any kill-trigger in the dashboard.
