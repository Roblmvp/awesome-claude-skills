const pptxgen = require("pptxgenjs");

const NAVY = "202A44";
const SAPPH = "1D57A5";
const SKY = "41B6E6";
const CHART = "DBE442";
const GRAYBG = "F1F1F1";
const GRAYTX = "807B80";
const HEAD = "Myriad Bengali";
const BODY = "Lato";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "Gallatin Ford — We Auto Deck Template";

// ---------- 1. TITLE LAYOUT ----------
let s1 = pres.addSlide();
s1.background = { color: "FFFFFF" };
s1.addImage({ path: "ford_wheel_full.jpg", x: 0, y: 0, w: 4.6, h: 7.5, sizing: { type: "cover", w: 4.6, h: 7.5 } });
// Gallatin Ford lockup — Ford-governed, never recolored; JPG sits on white
s1.addImage({ path: "ford_logo.jpg", x: 5.15, y: 0.55, w: 2.1, h: 2.1 * 882 / 1600 });
s1.addText("KICKER LINE · MONTH YEAR", {
  x: 5.15, y: 2.55, w: 7.2, h: 0.32, margin: 0,
  fontFace: BODY, fontSize: 13, bold: true, color: SAPPH, charSpacing: 2,
});
s1.addText("Presentation Title Goes Here", {
  x: 5.15, y: 2.95, w: 7.4, h: 1.65, margin: 0, valign: "top",
  fontFace: HEAD, fontSize: 40, bold: true, color: NAVY, lineSpacing: 46,
});
s1.addText("Subtitle — the one-line commitment this deck makes", {
  x: 5.15, y: 4.6, w: 7.2, h: 0.85, margin: 0, valign: "top",
  fontFace: BODY, fontSize: 17, color: SAPPH,
});
s1.addImage({ path: "we_auto_logo.png", x: 5.15, y: 6.1, w: 0.95, h: 0.95 });
s1.addText([
  { text: "Prepared by We Auto for Gallatin Ford", options: { fontFace: BODY, fontSize: 12, bold: true, color: NAVY, breakLine: true } },
  { text: "1394 Nashville Pike, Gallatin, TN 37066", options: { fontFace: BODY, fontSize: 10, color: GRAYTX } },
], { x: 6.35, y: 6.28, w: 6.2, h: 0.65, margin: 0, valign: "middle" });
s1.addNotes("TEMPLATE — TITLE LAYOUT. Replace kicker, title, and subtitle. Logo positions are locked: Gallatin Ford lockup top right (never recolor, never place on non-white background), We Auto badge bottom with clear space equal to 50% of the height of the WE on all sides. Photo panel takes any portrait image.");

// ---------- 2. STRATEGY DIVIDER ----------
let s2 = pres.addSlide();
s2.background = { color: NAVY };
s2.addText("SECTION 0 · STRATEGY NAME", {
  x: 0.9, y: 4.45, w: 11.5, h: 0.35, margin: 0,
  fontFace: BODY, fontSize: 13, bold: true, color: SKY, charSpacing: 3,
});
s2.addText([
  { text: "WE ", options: { color: CHART } },
  { text: "SET THE STANDARD", options: { color: "FFFFFF" } },
], {
  x: 0.9, y: 4.85, w: 11.8, h: 1.7, margin: 0, valign: "top",
  fontFace: HEAD, fontSize: 54, bold: true,
});
s2.addNotes("TEMPLATE — STRATEGY DIVIDER. Navy full-bleed. Replace the section label and the WE-statement. The word WE stays chartreuse (brand signature from the We Auto guide and the 120-day plan); the rest stays white. No logos on dark backgrounds.");

// ---------- 3. BULLET SLIDE ----------
let s3 = pres.addSlide();
s3.background = { color: "FFFFFF" };
s3.addText("STRATEGY · SECTION LABEL", {
  x: 0.75, y: 0.5, w: 11.8, h: 0.3, margin: 0,
  fontFace: BODY, fontSize: 12, bold: true, color: SAPPH, charSpacing: 2,
});
s3.addText("Slide Headline Goes Here", {
  x: 0.75, y: 0.88, w: 11.8, h: 0.8, margin: 0, valign: "top",
  fontFace: HEAD, fontSize: 32, bold: true, color: NAVY,
});
s3.addText([
  { text: "First point — one idea, one line", options: { bullet: true, breakLine: true } },
  { text: "Second point — keep it speakable, not readable", options: { bullet: true, breakLine: true } },
  { text: "Third point — the detail lives on the backup sheet", options: { bullet: true, breakLine: true } },
  { text: "Fourth point — five bullets maximum on any slide", options: { bullet: true } },
], {
  x: 0.75, y: 2.05, w: 11.6, h: 4.3, margin: 0, valign: "top",
  fontFace: BODY, fontSize: 18, color: NAVY, paraSpaceAfter: 14,
});
s3.addShape(pres.ShapeType.rect, { x: 0, y: 6.95, w: 13.333, h: 0.55, fill: { color: GRAYBG } });
s3.addImage({ path: "gf_logo_official.png", x: 0.75, y: 7.06, w: 0.34 * 282 / 160, h: 0.34 });
s3.addText("Presentation Title · Prepared by We Auto", {
  x: 1.6, y: 6.95, w: 8, h: 0.55, margin: 0, valign: "middle",
  fontFace: BODY, fontSize: 9, color: GRAYTX,
});
s3.addText("03", {
  x: 12.3, y: 6.95, w: 0.7, h: 0.55, margin: 0, valign: "middle", align: "right",
  fontFace: BODY, fontSize: 9, color: GRAYTX,
});
s3.addNotes("TEMPLATE — BULLET SLIDE. Kicker names the strategy. One idea per slide, three to five bullets, no paragraphs. Footer is locked: transparent Gallatin Ford mark left, deck title center-left, page number right. Chartreuse never appears on this layout — it is reserved for the numbers.");

// ---------- 4. BIG NUMBER ----------
let s4 = pres.addSlide();
s4.background = { color: NAVY };
s4.addText("STRATEGY · THE NUMBER", {
  x: 0, y: 1.65, w: 13.333, h: 0.35, margin: 0, align: "center",
  fontFace: BODY, fontSize: 13, bold: true, color: SKY, charSpacing: 3,
});
s4.addText("00 → 00", {
  x: 0, y: 2.4, w: 13.333, h: 2.1, margin: 0, align: "center", valign: "middle",
  fontFace: HEAD, fontSize: 100, bold: true, color: CHART,
});
s4.addText("The number in one line — what it is", {
  x: 1.5, y: 4.85, w: 10.333, h: 0.6, margin: 0, align: "center",
  fontFace: BODY, fontSize: 20, color: "FFFFFF",
});
s4.addText("Why it matters — one supporting line", {
  x: 1.5, y: 5.55, w: 10.333, h: 0.5, margin: 0, align: "center",
  fontFace: BODY, fontSize: 14, color: SKY,
});
s4.addText("04", {
  x: 12.3, y: 6.95, w: 0.7, h: 0.4, margin: 0, valign: "middle", align: "right",
  fontFace: BODY, fontSize: 9, color: SKY,
});
s4.addNotes("TEMPLATE — BIG NUMBER. One number per deck section, chartreuse on navy — chartreuse is reserved for the five plan metrics and nothing else. Label in white, context in sky. No logos on dark backgrounds.");

pres.writeFile({ fileName: "gf_template_v1.pptx" }).then(() => console.log("written"));
