# ORACLE Deliverable 5 — Dealer Early-Warning Dashboard

**Base date:** 2026-07-28 · **Recommended cadence:** weekly for Block 1 and store-level indicators; monthly for the rest, refreshed the week after the BLS jobs report.
**Current direction** is as of the base date, from the evidence ledger. **Type:** L = leading, C = coincident, G = lagging, S = structural, M = market-implied, X = sentiment, A = automotive-specific.

Reading rule: no single indicator triggers a strategy change. Act when **two or more Block-1 triggers fire together**, or when one fires and is confirmed by your own store-level block. Thresholds are decision aids derived from historical cycle behavior and this cycle's levels — they are judgment, not science.

---

## Block 1 — Kill-switch triggers (check weekly; these move strategy)

| Indicator | Type | Why it matters | Source / freq | Current (7/28/26) | Warning | Positive | If warning fires |
|---|---|---|---|---|---|---|---|
| Initial jobless claims (4-wk avg) | L | The single best real-time recession signal; the "low-fire" regime is the floor under demand | DOL, weekly | 187K — lowest since 1969 ↘ | >260K sustained 4+ wks (>300K = recession confirming) | <220K | Shift to defensive inventory posture (Scenario B/C playbook); shorten used aging limits to 45 days |
| Brent / national avg gas price | L | The oil shock is THE live macro variable: drives CPI, Fed, sentiment, mix | EIA/AAA, daily-weekly | Brent ~$88 after −9.2% on 7/27; gas $4.11 (+31% y/y) ⚠ | Brent >$100 for 30+ days or gas >$4.50 | Brent <$80 / gas <$3.50 | Rebalance lot mix toward hybrids/compacts/used EVs; re-forecast floor-traffic-sensitive spend |
| Fed policy direction (FOMC statements + FedWatch) | M | A Warsh HIKE flips the regime to Scenario D; a cut opens Scenario A/E | Fed/CME, 8×/yr + daily | 3.50–3.75%, hold expected 7/29; markets price hikes by mid-2027 ⚠ | Any 2026 hike, or 2-yr yield >4.75% | Cut delivered, or hike odds <10% for 2 mtgs | Lock floorplan hedges/rate expectations; accelerate aged-unit disposal before payment math worsens |
| S&P 500 drawdown from high | M | Top-decile spending (≈49% of consumption) is equity-underwritten — the "one-legged stool" | Market, daily | ~+9% YTD, at/near highs; AI-concentrated ⚠ | −15% sustained 30+ days (−20% = C-scenario confirming) | New highs w/ breadth improving | Expect luxury/high-ATP demand to crack first; tighten $60K+ inventory and specialty units |
| Auto credit availability (Dealertrack CAI) | A/L | Loosest since 2015 is holding up volume; a reversal chokes approvals fast | Cox, monthly | 104.6, 5th straight gain ↗ | 2 consecutive declines, or approval rate <71% | Continued gains | Expand lender bench NOW (before you need it); pre-position subprime alternatives; re-desk marginal deals early |
| USMCA / Section 338 status | S | A NA trade rupture = supply shock + price spike on ~half the parts bin and many models | USTR/news, event | Wind-down triggered 7/1; Canada 50% eff 8/19; Mexico talks live ⚠ | Talks collapse; Canada retaliation on autos/parts | Bilateral deal announced | Forward-buy fast-moving parts; pre-order affected-model inventory; re-quote body-shop parts contracts |

## Block 2 — Labor and income (monthly)

| Indicator | Type | Why it matters | Source / freq | Current | Warning | Positive | Auto interpretation |
|---|---|---|---|---|---|---|---|
| Nonfarm payrolls (3-mo avg) | C | Income → purchase intent and approval quality | BLS, monthly | +92K/mo YTD, Jun +57K ⚠ | <0 for 2 of 3 months | >150K sustained | Each ~1pp unemployment rise historically costs ~10%+ of retail SAAR |
| Payroll revisions (net, trailing 3 releases) | L | Revisions lead the trend; 2025's −911K benchmark burned everyone | BLS, monthly | Negative bias | Cumulative −150K over 3 releases | Positive revisions | Treat headline beats skeptically when revisions run negative |
| Continuing claims | L | Re-hiring stops before firing starts; measures exit-difficulty | DOL, weekly | 1.80M stable | >2.0M | <1.75M | Rising = longer buyer job-search gaps = approval decay in near-prime |
| Challenger layoffs + tech/AI share | L | White-collar displacement is the new cycle's leading edge | Challenger, monthly | H1 443.6K, tech +83% y/y ⚠ | >100K/mo for 2 months | <40K/mo | White-collar metros (and $50K+ segments) weaken first — watch your zip-code mix |
| Labor-force participation | S | The 61.5% print flatters the unemployment rate | BLS, monthly | 61.5%, falling ⚠ | Further falls WITH rising unemployment | Recovery >62% | Falling participation + low claims = frozen market, not healthy one |
| Avg hourly earnings vs CPI (real wages) | C | Real income is what buys cars | BLS, monthly | Roughly flat; negative y/y in spring | Real wages negative 3+ months | Real +1%+ sustained | Negative real wages → payment objections rise before traffic falls |

## Block 3 — Inflation, rates, credit (monthly)

| Indicator | Type | Why it matters | Source / freq | Current | Warning | Positive | Auto interpretation |
|---|---|---|---|---|---|---|---|
| CPI headline & core | C | Sets Fed path and real incomes | BLS, monthly | 3.5% / 2.6% ↘ off May 4.2% peak | Headline >4% again or core >3% | Headline <3% | Energy-driven inflation hits traffic (fuel budgets) before it hits rates |
| PCE (Fed's gauge) | C | The number Warsh answers to | BEA, monthly | 4.1% headline / 3.4% core (May) ⚠ | Core >3.5%持续 | Core <3.0% falling | Above-target PCE = no rescue cuts if demand weakens — plan without a Fed put |
| 5-yr inflation expectations (UMich) + breakevens | L/X | De-anchoring = Scenario D confirmation | UMich, monthly | 3.3% elevated ⚠ | >3.5% | <3.0% | De-anchoring → hikes → auto APRs 8%+ → payment-neutral pricing needs ~5% price cuts (engine §3) |
| 10-yr Treasury | M | Sets floorplan benchmarks (SOFR-linked) and mortgage/housing channel | Daily | 4.69–4.71% ⚠ | >5.0% | <4.25% | +100bp ≈ +$21/mo consumer payment, and roughly +$40-45/unit/month floorplan cost on a $50K unit |
| Average new-car APR (Edmunds/Cox) | A | The consumer's actual rate — has NOT followed Fed cuts | Quarterly/monthly | 7.0% (realized deals); 9.58% all-credit ⚠ | New >7.5% realized | <6.5% | Rate relief without subvention is not coming; subvention = $8K price-equivalent at 0% |
| SLOOS auto standards + Dealertrack approval rate | L/A | Lender willingness leads volume by ~2 quarters | Fed qtrly / Cox monthly | Easing; approvals 73.8% ↗ | Net tightening + approvals <71% | Approvals >75% | First tightening shows in near-prime LTV caps and doc stips — your F&I office sees it before the data does |
| Subprime auto ABS 60+ DPD (Fitch) | G/A | Severity cycle; drives lender pullback with a lag | Monthly | ~6.8–6.9% records (Feb latest) ⚠ | >7.5% new record trend | <6.0% | Rising DPD + record negative equity = eventual LTV caps → bigger cash-down requirements → conversion drop |
| Auto ABS spreads / issuance | M | Funding stress chokes non-bank lenders first | SIFMA/desk, monthly | Issuance +10.3% y/y, spreads tight ↗ | Subprime new-issue spreads widening >100bp | Tight and issuing | Widening = your subprime lenders raise buy rates / cut advances within weeks |

## Block 4 — Consumer capacity (monthly-quarterly)

| Indicator | Type | Why it matters | Source / freq | Current | Warning | Positive | Auto interpretation |
|---|---|---|---|---|---|---|---|
| Savings rate | S | The buffer is thin | BEA, monthly | 3.0% ⚠ | <2.5% | >4% | Thin savings = down payments fall further (already 11.6%, lowest since 2020) |
| Revolving credit growth (G.19) | L | Sharp swings signal exhaustion or retrenchment | Fed, monthly | May −4.7% annualized ⚠ | Negative 3 straight months | Moderate +2–5% | Contraction at the bottom = used-car demand softens at <$20K price points first |
| Card balances 90+ DPD (stock) | G | Bottom-cohort stress level | NY Fed, quarterly | >13%, 15-yr high ⚠ | >14% | <11% | Cross-default risk: card-stressed customers fail auto underwriting DTI screens |
| Student-loan default wave | S | Removes millions from financing eligibility (score −91 avg) | NY Fed/ED, quarterly | ~3.6M reported; flows crested ⚠ | Fall 2026 second wave materializes | Rehab/fresh-start uptake rises | Check your market's exposure: Sun Belt over-indexed; expect more co-signer deals and BHPH leakage |
| UMich sentiment + vehicle buying conditions | X | Sentiment leads discretionary timing at the margin | UMich, monthly | 54.4, 2-mo bounce, −12% y/y | <50 re-crater | >60 | Bounce is gas-price-driven — durable only if oil stays down |
| Consumer confidence (Conference Board) | X | Labor-differential subindex is a decent claims preview | CB, monthly | 91.2 (Jun) | <85 | >100 | Watch the jobs-plentiful-minus-hard-to-get spread more than the headline |
| Case-Shiller metro prices + EHS turnover | S | Housing wealth & the move-purchase channel; regional divergence | Monthly | National +0.8%; half of metros negative; EHS 4.09M depressed ⚠ | National negative y/y | Turnover >4.5M | Sun Belt stores: falling home prices = softer trade equity and down payments regionally |

## Block 5 — Automotive market (monthly)

| Indicator | Type | Why it matters | Source / freq | Current | Warning | Positive | Auto interpretation |
|---|---|---|---|---|---|---|---|
| SAAR (retail vs fleet split) | C/A | The headline is fleet-flattered — track retail | Cox/JDP, monthly | 16.5M Jun, best of yr; retail −4.1% H1 ⚠ | Retail SAAR-equivalent <15M | Retail growth positive y/y | Fleet strength ≠ your showroom; plan volume off retail trend |
| New days' supply — industry AND your brands | A | Aging = incentive escalation and floorplan drag | Cox vAuto, monthly | 80 days; Toyota 37 vs Jeep 160 | Your brand >100 | Your brand 45–75 | Fat-brand dealers: negotiate floorplan assistance, pre-empt with turn discipline now |
| Incentives % of ATP | A | The 13-month 7.0% discipline is the pricing regime's keystone | KBB, monthly | 7.0% steady | >8.5% and climbing = discipline broken | Stable 6.5–7.5% | If discipline breaks (Scenario B/C), front-end gross goes with it — get ahead with used mix |
| Manheim index (MoM, y/y) + auction conversion | A/L | Wholesale leads retail used pricing by 6–8 weeks | Manheim, bi-monthly | 211.5 mid-Jul, +2.0% y/y, orderly ↘ | y/y negative + conversion <50% | +2–5% y/y, conversion >55% | Conversion is the earliest tell — dealers stop raising hands before indexes fall |
| Off-lease return volume | S/A | Supply wave caps used values into 2027, then reverses post-2027 | Edmunds/Cox, quarterly | 2.4M 2026E (+25.7%), 2.8M 2027E ⚠ | Faster residual erosion (3-yr <64% MSRP) | Return rates fall (buyouts revive) | Buy 2-4-yr-old inventory cautiously into rising supply; the 2028+ scarcity flips it again |
| Used days' supply by price band | A | Sub-$15K at 33 days = the scarcity is at the bottom | Cox, monthly | 47 total; 33 sub-$15K | Sub-$15K >45 (scarcity easing = demand problem) | Tight but sourced via trades/service lane | Service-lane and street purchase programs are the moat for cheap-car supply |
| EV share + used-EV values | A | Post-credit reset done; fuel prices flipped used-EV economics | Cox/Manheim, monthly | New ~5.8%; used-EV values +12–13.6% y/y | Used-EV values roll over while EV lease returns +230% land | Gas stays >$4 (supports used-EV demand) | Used EVs = margin opportunity NOW, residual risk into 2027 — buy on turn, not on hope |
| Dealer-group GPUs / fixed-ops growth (public comps) | G/A | Your benchmark glide path | Quarterly filings | New GPU −4~7% y/y; fixed ops records | New GPU −15%+ y/y (acceleration) | GPU stabilization | If publics' GPU decline accelerates, the incentive war has started — protect used and F&I |
| Floorplan cost (your statement) | A | SOFR + spread × days' supply = controllable drag | Monthly | Industry interest declining (AN −10%) | Your floorplan interest/unit rising 2 straight months | Falling | Aging is the controllable half of floorplan expense — the rate half is not |

## Block 6 — Store-level confirmation set (your DMS/CRM, weekly)

These confirm or refute macro signals in YOUR market before national data does. No national thresholds — trend them against your trailing 13 weeks.

| Indicator | Watch for |
|---|---|
| Lead volume + cost per lead | Macro weakness shows in lead QUALITY (payment-shopping share) before volume |
| Appointment/show/close rates | Conversion decay with stable traffic = affordability/approval problem, not marketing problem |
| Approval rate by tier + stips/desk-rework rate | First-derivative of lender tightening — leads SLOOS by a quarter |
| Cash-down offered vs required | Falling offered cash-down = consumer buffer erosion in your market |
| Lost-sale reasons (payment vs rate vs approval vs trade value) | The mix tells you WHICH scenario is arriving locally |
| Trade-in negative-equity share and average | Your local read on C5; drives your desking and lender mix |
| Used cost-to-market vs Manheim segment trend | Are you buying above a falling market? Weekly repricing discipline |
| Aged inventory: % >45 and >60 days, $ in water | The liquidity kill-switch; act at 45 days, not 60 |
| Service RO count, customer-pay hours, declined-work backlog | Fixed-ops demand decay = late-cycle confirmation; declined-work list = recession-ready revenue reserve |
| Floorplan interest per unit sold | The all-in carrying-cost discipline metric |

---

## Calendar of scheduled catalysts (next 6 months)

| Date | Event | Why it matters |
|---|---|---|
| Jul 29, 2026 | FOMC decision (Warsh's 2nd meeting) | Hold vs hike = Scenario A/B vs D signal |
| Jul 30 | Q2 2026 advance GDP | Confirms/refutes 1.6% GDPNow muddle-through |
| Jul 31 | June PCE + UMich final | The Fed's number; tariff pass-through check |
| Jul 28–31 | ABG (7/28), LAD (7/29), GPI (7/30), AN (7/31) Q2 earnings | GPU glide path, fixed-ops carry, credit commentary |
| Early Aug | July SLOOS; NY Fed Q2 HHDC | Auto standards direction; delinquency flows |
| Aug 7 | July jobs report | Claims-vs-payrolls divergence resolution begins |
| Aug 19 | Section 338 Canada 50% effective | Retaliation risk on parts/vehicles |
| Sep–Oct | Fall student-loan default second wave (possible) | Further subprime buyer-pool erosion |
| ~Nov 1 | Rare-earth/Nexperia truce expiry | Chip/parts supply risk reprice |
| Nov 3 | Midterm elections | Tariff codification, dividend checks, CFPB posture, EV policy stakes |
| Oct–Dec | USMCA talk milestones; CA CARS Act effective (Oct) | Structural supply-chain and compliance triggers |
