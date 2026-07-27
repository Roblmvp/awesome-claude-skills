const pptxgen = require("pptxgenjs");

const NAVY = "202A44";
const SAPPH = "1D57A5";
const SKY = "41B6E6";
const CHART = "DBE442";
const GRAYBG = "F1F1F1";
const GRAYTX = "807B80";
const HEAD = "Myriad Bengali";
const BODY = "Lato";
const FOOTER = "120-Day Used Vehicle Action Plan · Prepared by We Auto";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "120-Day Used Vehicle Action Plan";

let pageNum = 0;

// headlineRuns: array of {text, hl} — hl true renders navy-on-chartreuse highlight
function bulletSlide(kicker, headlineRuns, bullets, notes) {
  pageNum++;
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText(kicker, {
    x: 0.75, y: 0.5, w: 11.8, h: 0.3, margin: 0,
    fontFace: BODY, fontSize: 12, bold: true, color: SAPPH, charSpacing: 2,
  });
  const runs = headlineRuns.map((r, i) => ({
    text: r.text,
    options: r.hl ? { color: NAVY, highlight: CHART } : { color: NAVY },
  }));
  s.addText(runs, {
    x: 0.75, y: 0.88, w: 11.8, h: 0.8, margin: 0, valign: "top",
    fontFace: HEAD, fontSize: 32, bold: true,
  });
  const items = bullets.map((b, i) => ({
    text: b,
    options: { bullet: true, breakLine: i < bullets.length - 1 },
  }));
  s.addText(items, {
    x: 0.75, y: 2.05, w: 11.6, h: 4.3, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 18, color: NAVY, paraSpaceAfter: 14,
  });
  s.addShape(pres.ShapeType.rect, { x: 0, y: 6.95, w: 13.333, h: 0.55, fill: { color: GRAYBG } });
  s.addImage({ path: "gf_logo_official.png", x: 0.75, y: 7.06, w: 0.34 * 282 / 160, h: 0.34 });
  s.addText(FOOTER, {
    x: 1.6, y: 6.95, w: 8, h: 0.55, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 9, color: GRAYTX,
  });
  s.addText(String(pageNum).padStart(2, "0"), {
    x: 12.3, y: 6.95, w: 0.7, h: 0.55, margin: 0, valign: "middle", align: "right",
    fontFace: BODY, fontSize: 9, color: GRAYTX,
  });
  s.addNotes(notes);
  return s;
}

// ---------- COVER ----------
pageNum++;
let cover = pres.addSlide();
cover.background = { color: "FFFFFF" };
cover.addImage({ path: "ford_wheel_full.jpg", x: 0, y: 0, w: 4.6, h: 7.5, sizing: { type: "cover", w: 4.6, h: 7.5 } });
cover.addImage({ path: "ford_logo.jpg", x: 5.15, y: 0.55, w: 2.1, h: 2.1 * 882 / 1600 });
cover.addText("PREPARED FOR JOE BARBA · AUGUST 2026", {
  x: 5.15, y: 2.55, w: 7.2, h: 0.32, margin: 0,
  fontFace: BODY, fontSize: 13, bold: true, color: SAPPH, charSpacing: 2,
});
cover.addText("120-Day Used Vehicle Action Plan", {
  x: 5.15, y: 2.95, w: 7.4, h: 1.65, margin: 0, valign: "top",
  fontFace: HEAD, fontSize: 40, bold: true, color: NAVY, lineSpacing: 46,
});
cover.addText("Presented by Rob Lisowski & John McCann", {
  x: 5.15, y: 4.6, w: 7.2, h: 0.85, margin: 0, valign: "top",
  fontFace: BODY, fontSize: 17, color: SAPPH,
});
cover.addImage({ path: "we_auto_logo.png", x: 5.15, y: 6.1, w: 0.95, h: 0.95 });
cover.addText([
  { text: "Prepared by We Auto for Gallatin Ford", options: { fontFace: BODY, fontSize: 12, bold: true, color: NAVY, breakLine: true } },
  { text: "1394 Nashville Pike, Gallatin, TN 37066", options: { fontFace: BODY, fontSize: 10, color: GRAYTX } },
], { x: 6.35, y: 6.28, w: 6.2, h: 0.65, margin: 0, valign: "middle" });
cover.addNotes("SPEAKER: ROB — Open the laptop, let the cover sit while people settle. One line before advancing: \"Joe, this is the used-car plan. Twelve slides, four strategies, and John and I split the talking. Everything detailed is on one page we'll leave with you.\"");

// ---------- SLIDE 1 · THE GOAL (big number, ROB) ----------
pageNum++;
let g = pres.addSlide();
g.background = { color: NAVY };
g.addText("THE GOAL", {
  x: 0, y: 1.35, w: 13.333, h: 0.35, margin: 0, align: "center",
  fontFace: BODY, fontSize: 13, bold: true, color: SKY, charSpacing: 3,
});
g.addText("−$266 → $0", {
  x: 0, y: 2.1, w: 13.333, h: 2.1, margin: 0, align: "center", valign: "middle",
  fontFace: HEAD, fontSize: 100, bold: true, color: CHART,
});
g.addText("Front-end gross per unit — on the true basis: pack, net adds, and CPO money included", {
  x: 1.2, y: 4.55, w: 10.933, h: 0.6, margin: 0, align: "center",
  fontFace: BODY, fontSize: 20, color: "FFFFFF",
});
g.addText("120 units a month by November", {
  x: 1.5, y: 5.35, w: 10.333, h: 0.55, margin: 0, align: "center",
  fontFace: BODY, fontSize: 22, bold: true, color: CHART,
});
g.addText("02", {
  x: 12.3, y: 6.95, w: 0.7, h: 0.4, margin: 0, valign: "middle", align: "right",
  fontFace: BODY, fontSize: 9, color: SKY,
});
g.addNotes("SPEAKER: ROB — The Goal.\n• Open with the reporting basis and don't rush it: this −$266 includes pack, net adds, and CPO incentive money. The Daily Operating Report front-gross number is struck before those credits — it understates us, and it's not the number we manage.\n• Every used car we sell today is profitable in TOTAL — F&I is carrying the front end. That's the good news and the problem in one sentence. Fixing the front is pure margin.\n• Volume is flat-to-declining while the lot holds. This is a velocity problem, not a supply problem.\n• Say it plainly: we're not asking for money. We're asking for process, and for you to hold us to it. Four strategies, all process, none of it hope.\nJOE WILL ASK: \"That's not the number I see on the DOR.\" → Right — the DOR excludes pack, net adds, and CPO money. On the store's true basis it's −$266, and that's the number this whole plan manages to zero.");

// ---------- SLIDE 2 · FOUR STRATEGIES (divider, ROB) ----------
pageNum++;
let f = pres.addSlide();
f.background = { color: NAVY };
f.addText("THE PLAN", {
  x: 0.9, y: 3.85, w: 11.5, h: 0.35, margin: 0,
  fontFace: BODY, fontSize: 13, bold: true, color: SKY, charSpacing: 3,
});
f.addText("ACQUISITION. APPRAISAL.\nRECON. LEADS.", {
  x: 0.9, y: 4.25, w: 11.8, h: 2.0, margin: 0, valign: "top",
  fontFace: HEAD, fontSize: 54, bold: true, color: "FFFFFF", lineSpacing: 62,
});
f.addText("The first three fix supply. The fourth sells it.", {
  x: 0.9, y: 6.45, w: 11.8, h: 0.45, margin: 0,
  fontFace: BODY, fontSize: 16, color: SKY,
});
f.addNotes("SPEAKER: ROB — Four Strategies.\n• This slide is the whole presentation. Everything after this is detail on these four lines.\n• Acquisition — the right cars, from four channels, with a goal on each. Appraisal — one number on the car, no bumping. Recon — relationship and evidence; stop spending on cars we won't retail. Leads & CRM — the same daily discipline in the CRM that we have in the shop.\n• Execute the first three perfectly and skip the fourth, and we still miss 120.\n• Ownership out loud: I own all four. John co-drives acquisition and the daily trade walk. Tony and Nata hold the appraisal line with me. Austin and Brad are partners on recon.\nJOE WILL ASK: \"Where's pricing in this?\" → Inside two of them: appraisal sets the cost basis right, and the recon exit-strategy walk prices the disposition before we spend. Lifecycle repricing runs underneath as standing discipline.");

// ---------- SLIDE 3 · ACQUISITION: THE CHANNELS (JOHN) ----------
bulletSlide(
  "STRATEGY 1 · ACQUISITION",
  [{ text: "Four channels. A goal on each." }],
  [
    "Trade-ins — the cheapest inventory we will ever own. Every trade we lose gets replaced at auction, at a premium",
    "Service drive — an appraisal lane on the drive; high-margin, growing",
    "Curb purchases — Facebook Marketplace and private party, bought one-on-one",
    "Auction — the fill, not the foundation. Buy list from turn data, max bids set before the sale, never in the lane",
    "Each channel carries a monthly unit goal and lives on the weekly scorecard",
  ],
  "SPEAKER: JOHN — Acquisition: The Channels.\n• The point of this slide: we stop depending on auction. Today auction is the default; in this plan it's the flex that covers whatever the other three don't produce.\n• Goals if asked (spoken, not on slide): at full pace roughly 58 from trades, 36 auction, 12 to 20 curb, 14 service drive and street — 120 acquisitions a month feeding 120 sales.\n• Manheim Nashville is the primary lane — local, minimal transport.\n• Trade capture gets tracked weekly, paired with appraisal discipline — those two dials move together or we're doing it wrong.\nJOE WILL ASK: \"What happens when trades don't show up?\" → Auction flexes up to cover — and every auction unit carries fees, transport, and inspection cost that a trade doesn't. That friction is exactly why trades are goal number one."
);

// ---------- SLIDE 4 · ACQUISITION: CURB PURCHASES (JOHN) ----------
bulletSlide(
  "STRATEGY 1 · ACQUISITION",
  [{ text: "$400 to anyone who finds us a car." }],
  [
    "Any employee — sales, BDC, service, office — earns $400 when the store buys a car they sourced",
    "We buy at the car, one-on-one: no auction fees, no transport, no sale-day bidding war",
    "The policy is not the strategy — the daily reminder is. This program dies quietly without daily communication",
    "Attorney-reviewed guardrails before launch; the dealership is the buyer of record on every deal",
  ],
  "SPEAKER: JOHN — Acquisition: Curb Purchases.\n• Sell the mindshare math: the spiff is deliberately rich so every department is scanning Marketplace on their lunch break. We're buying awareness, and awareness is the work.\n• Daily communication means it's in the morning huddle, every huddle. Not a memo in week one — a drumbeat.\n• Exclusive inventory angle: a curb car isn't sitting in a lane with forty dealers bidding on it.\nJOE WILL ASK: \"What's our exposure buying off the street?\" → Eight-point compliance list, attorney-reviewed before launch: store is buyer of record, ID must match title, history and flood check before any offer, dealership check or ACH only, no retail listing until title or lien release is in hand, all inspections at the store."
);

// ---------- SLIDE 5 · APPRAISAL: ONE NUMBER (ROB) ----------
bulletSlide(
  "STRATEGY 2 · APPRAISAL",
  [{ text: "The desking manager does not appraise." }],
  [
    "A manager off the deal puts one number on the car — the desk never sets it and never sees it set",
    "No bumping ACVs. A deal made by burying money in the trade doesn't disappear — it comes back as negative front gross",
    "The customer sees the car's condition with us, at the car — that's what makes a lower number defensible instead of insulting",
    "This is a structural control, not a policy request — it removes the mechanism, not just the habit",
  ],
  "SPEAKER: ROB — Appraisal: One Number.\n• This is the most-tested slide in the deck. Say so: somebody in the tower is going to want to bump a trade to save a deal in week two, and what happens in that moment decides whether this plan is real.\n• The blind desk is prevention; the over-allowance log is the reporting half — every over-allowance logged per deal, capped, reviewed weekly.\n• There's an escape valve, and it's controlled: on a committed buyer with a genuinely competitive trade, the desk can request a competitive-match review — GSM decides, logged with a reason code, capped as a small share of appraisals.\n• We watch capture and ACV discipline as paired metrics. If trade capture falls while we tighten, tightening pauses pending review — we're not going to win the appraisal and lose the lot.\nJOE WILL ASK: \"How many deals does this cost us?\" → We track exactly that — capture on the same scorecard line as ACV-to-market. If capture holds below industry average two weeks running, the tightening pauses. The dials move together or we stop."
);

// ---------- SLIDE 6 · APPRAISAL: THE PROCESS (ROB) ----------
bulletSlide(
  "STRATEGY 2 · APPRAISAL",
  [{ text: "Every trade. No exceptions." }],
  [
    "Trade-in questionnaire completed on every appraisal",
    "Trade walk with the customer, at the vehicle — they see what we see",
    "12 photos in VinCue, defects included — the record that prevents “nobody told me” at delivery",
    "OBD scan before the number is committed — it catches what the eye misses and prices it up front",
    "Tony, Nata, and I hold one standard. If one of the three of us lets it slide, the process is dead",
  ],
  "SPEAKER: ROB — Appraisal: The Process.\n• This runs as one sequence at the car, not three tasks: walk it with the customer, photograph it, scan it — then the number goes on. Lower ACVs the defensible way: the customer saw it, the record shows it, the scan priced it.\n• The three-manager line matters most: salespeople test the weakest gate. Tony, Nata, and I have agreed the answer is the same at all three desks.\n• Baselines get measured before this launches — bump rate, ACV-to-market, look-to-book — so ninety days from now the improvement is provable, not anecdotal.\nJOE WILL ASK: \"How do I know it's actually happening on every trade?\" → Every up with a trade gets logged and appraised, no exceptions — so look-to-book is measurable from day one. If the questionnaire, photos, and scan aren't in VinCue, the appraisal doesn't exist."
);

// ---------- SLIDE 7 · RECON: THE RELATIONSHIP (ROB) ----------
bulletSlide(
  "STRATEGY 3 · RECON",
  [{ text: "We go to them." }],
  [
    "Austin, Brad, Barry, Shannon, and the techs — this strategy is showing up, not sending a memo",
    "The shop already performs. Our job is keeping it that way, together",
    "They help build the KPIs — they don't get handed them",
    "One short weekly review of specific cars, no-fault, one committed improvement each week",
  ],
  "SPEAKER: ROB — Recon: The Relationship.\n• Lead with the credit, in person: the recon team got dramatically faster over the last ninety days and now beats the industry's best-practice band. That's their win and they should hear it from us in their shop.\n• The honest framing for Joe: used recon competes with customer-pay work for the same techs and parts. That allocation is a human negotiation, and it goes better when we're up there every day instead of sending tickets.\n• Austin's seat at the table is load-bearing — he controls tech allocation and parts priority. If he stops showing up, we escalate; we don't quietly continue.\n• The weekly review is a system diagnosis, not a blame forum — stated ground rule, every meeting, including one correctly-handled car as the positive control.\nJOE WILL ASK: \"Why does 'relationship' get its own slide?\" → Because the biggest handoff in this building is between sales and service, and no KPI survives if the people measured by it weren't in the room when it was built."
);

// ---------- SLIDE 8 · RECON: THE KPIS (ROB) ----------
bulletSlide(
  "STRATEGY 3 · RECON",
  [{ text: "Time to line: " }, { text: "8.5 → 5.0 days", hl: true }, { text: "." }],
  [
    "The shop is not the bottleneck — the wait after the shop is",
    "KPI one: every vehicle gets a completed used vehicle inspection",
    "KPI two: tires recommended → a photo of the tread measurement goes in Rapid Recon",
    "An estimate argues; a photo decides. Evidence is what actually cuts recon spend",
  ],
  "SPEAKER: ROB — Recon: The KPIs.\n• The finding worth saying out loud: recon cycle time improved 25 percent in ninety days and now beats best practice. Meanwhile the finished-car wait — photos, pricing, listing — more than doubled. The constraint moved out of the shop and into merchandising. 8.5 to 5.0 is the whole-store number, and the shop's piece is already done.\n• The tire photo is measured once and used three times: it prices the ACV at appraisal, it backs the asking price online, and it's a CPO pass/fail line item anyway.\n• Getting to 5.0: photo SLA after recon, price on arrival, list during recon with interim photos. Merchandising moves; the shop holds.\n• Every day off time-to-line is holding cost we stop paying and a fresher price when the car hits the market.\nJOE WILL ASK: \"If the shop's already fast, why is recon a strategy?\" → Because keeping a shop at best practice is a daily act, and because the KPIs make spend evidence-based — that's where the recon dollars actually get saved."
);

// ---------- SLIDE 9 · RECON: EXIT STRATEGY UP FRONT (JOHN) ----------
bulletSlide(
  "STRATEGY 3 · RECON",
  [{ text: "203 on the ground", hl: true }, { text: ". Every one gets a decision." }],
  [
    "Daily trade walk: every unit gets a call before recon — retail, dispose, service-only, or decline",
    "Hard gate: no unit is authorized into recon without a logged disposition decision",
    "Recon on a car we were never going to retail is unrecoverable — it doesn't come back at disposal and it doesn't come back in F&I",
    "The walk happens every day. Rob primary, me named backup, on-duty desk manager covers if we're both out",
  ],
  "SPEAKER: JOHN — Recon: Exit Strategy Up Front.\n• The principle in one line: the walk decides the exit before the first dollar is spent. Otherwise the walk is just documenting sunk cost.\n• Time cost stated up front so it never becomes the excuse: at full volume this is thirty to forty-five minutes a day. That's the price of never writing a recon check on a wholesale car.\n• Coverage rule matters — a unit with no logged decision does not move to recon. Ever. Not \"waits for Rob\" — does not move.\nJOE WILL ASK: \"Are you going to starve the lot playing it safe?\" → No — a decision isn't a disposal. Most cars still retail. The gate just means we know the exit before the spend, instead of finding out after."
);

// ---------- SLIDE 10 · LEADS: THE LEAK (JOHN) ----------
bulletSlide(
  "STRATEGY 4 · LEADS & CRM",
  [{ text: "59%", hl: true }, { text: " of our appointments show up." }],
  [
    "The problem is not lead volume — it's what happens after the lead arrives",
    "Our biggest lead source converts the worst",
    "People told us they were coming in and didn't — about a showroom's worth of customers every month",
    "Of the customers who do show, roughly three in four buy. The leak is the door, not the close",
  ],
  "SPEAKER: JOHN — Leads: The Leak.\n• The clearest numbers in the whole plan, spoken: over ninety days we set 247 appointments and 145 showed. That's 59 percent — 102 people who told us they were coming and didn't, about 34 a month.\n• Scale of the prize: getting show rate from 59 to 75 percent is worth roughly ten units a month — nearly a third of the gap to 120 — with zero added ad spend and zero added inventory.\n• Context if pressed: our largest source is around 45 percent of all leads closing at 8 percent. And internet leads are only about a fifth of total deliveries — the rest is floor, phone, repeat, referral, service.\nJOE WILL ASK: \"So do we buy more leads?\" → No. More leads at a 59 percent show rate just wastes more of them. The fix is a confirmation process, and it's free."
);

// ---------- SLIDE 11 · LEADS: BEING IN THE CRM (JOHN) ----------
bulletSlide(
  "STRATEGY 4 · LEADS & CRM",
  [{ text: "Presence, not spend." }],
  [
    "Appointment confirmation process — this is the whole opportunity, and it costs nothing",
    "Verify response time: the CRM reports first-response with no unit stated. One question to the admin settles whether we answer leads in minutes or in hours",
    "Underperforming sources get a decision, not more effort — get the cost, make the keep-or-kill call",
    "Daily lead review, same discipline as the daily trade walk. The trade walk works because we show up every day. The CRM is no different",
  ],
  "SPEAKER: JOHN — Leads: Being In The CRM.\n• The response-time point deserves weight: if those first-response figures are minutes, we're answering leads in seven to eleven hours, and that alone is costing deals. If they're seconds, it's a non-issue. One question resolves it — it just has to be asked.\n• The keep-or-kill case, spoken: one source gave us well over a hundred leads and three deals — and even the customers who walked in mostly didn't buy. That's lead quality, not follow-up. We get the cost per delivered unit and decide.\n• Also worth saying: one source is doing the opposite — pre-approved shoppers where nearly every show delivered. Same review finds what to kill AND what to scale.\nJOE WILL ASK: \"Who owns the confirmation process?\" → BDC and the sales managers run it; Rob and I review it in the daily lead check. It's a checklist and a cadence, not new software and not new spend."
);

// ---------- SLIDE 12 · WHAT WE NEED (ROB) ----------
bulletSlide(
  "THE ASK",
  [{ text: "Five asks." }],
  [
    "Approve the one-time lot clean-up once the week-one analysis sizes it — that loss already happened; we're making it visible instead of letting it bleed through the results",
    "Back the one-number appraisal policy publicly the first time it gets tested",
    "Approve the curb-purchase spiff and the comp alignment, so pay pushes the same direction as the plan",
    "Give us the keep-or-kill call on the weak lead source once the cost data is in",
    "Fifteen minutes a day in the stand-up for the first month — your presence is what sets the standard",
  ],
  "SPEAKER: ROB — What We Need.\n• Frame it as decisions, not budget: almost nothing on this list is spend. It's authority, timing, and visible backing.\n• On the clean-up: the analysis gets done in week one and the number comes to you sized, with the aged units named. Approving it up front is what keeps the go-forward results honest — nobody gets surprised in month two.\n• On the appraisal backing: the policy will be tested by a real deal within weeks. One public \"the number is the number\" from you and it holds; one quiet exception and it's dead.\n• Close on the commitment: break-even front end, 120 a month, and every piece of it measured — baselines first, so in ninety days we're showing you befores and afters, not opinions.\nJOE WILL ASK: \"What does all this cost me?\" → The clean-up, which is a loss we've already taken economically, and the spiff money — which replaces auction fees we're paying today. Everything else on this list is discipline."
);

pres.writeFile({ fileName: "gf_deck_v1.pptx" }).then(() => console.log("written", pageNum, "pages"));
