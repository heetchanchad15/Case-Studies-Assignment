/*
 * Individual Task 1, Part 2 - executive video presentation.
 *
 * Deliberately carries NO name or student number: the video and its slides are
 * shared with a peer for review.
 *
 *   node build_deck.js
 */

const pptxgen = require("pptxgenjs");
const path = require("path");

const OUT = path.join(__dirname, "Content-Moderation-Triage.pptx");

// ---------------------------------------------------------------- palette
// Content-informed: midnight navy for the platform at 3am, burnt coral used
// ONLY for the false-alarm numbers. Chart pair validated for colour-vision
// deficiency (worst adjacent dE 20.9 protan) against the light surface.
const NAVY = "0F1729";   // dominant background
const CARD = "1B2740";   // raised surface
const CARD2 = "223козы"; // (unused placeholder guard)
const INK = "E9EEF8";   // primary ink on dark
const MUTED = "93A9CC";   // secondary ink on dark
const CORAL = "FF6B5B";   // accent on dark - alarm only
const LIGHT = "F4F6FB";   // inverted slide surface
const DARKINK = "0F1729";   // ink on the light slide
const CHART_R = "C8452B";   // chart coral  (validated)
const CHART_B = "2A6FB8";   // chart blue   (validated)

const HEAD = "Cambria";  // safe-list serif, renders true-to-width
const BODY = "Calibri"; // safe-list sans

const W = 13.333, H = 7.5, M = 0.75;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";           // must be set before any slide
pres.title = "Who gets reviewed first?";
pres.author = " ";                       // no personal information - peer reviewed
pres.company = " ";
pres.subject = "Content moderation triage";

// --------------------------------------------------------------- helpers

/** The repeated motif: a short queue of items, a couple of them flagged. */
function queueMotif(slide, x, y, flagged = [1, 4], dim = "27395C") {
    for (let i = 0; i < 9; i++) {
        slide.addShape(pres.ShapeType.roundRect, {
            x: x + i * 0.26, y, w: 0.17, h: 0.17, rectRadius: 0.04,
            fill: { color: flagged.includes(i) ? CORAL : dim },
            line: { type: "none" },
        });
    }
}

function slideTitle(slide, text, color = INK) {
    slide.addText(text, {
        x: M, y: 0.62, w: W - 2 * M, h: 0.95,
        fontFace: HEAD, fontSize: 38, bold: true, color, margin: 0,
        valign: "top",
    });
}

function eyebrow(slide, text, color = CORAL) {
    slide.addText(text, {
        x: M, y: 0.3, w: W - 2 * M, h: 0.3,
        fontFace: BODY, fontSize: 12, bold: true, color,
        charSpacing: 2.2, margin: 0,
    });
}

function darkSlide() {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    return s;
}

// =====================================================================
// 1  Title
// =====================================================================
{
    const s = darkSlide();

    s.addText("CASE STUDIES IN DATA SCIENCE  ·  INDIVIDUAL TASK 1", {
        x: M, y: 1.85, w: W - 2 * M, h: 0.3,
        fontFace: BODY, fontSize: 13, bold: true, color: CORAL,
        charSpacing: 2.6, margin: 0,
    });

    s.addText("Who gets reviewed first?", {
        x: M, y: 2.4, w: 10.4, h: 1.4,
        fontFace: HEAD, fontSize: 62, bold: true, color: INK, margin: 0,
    });

    s.addText(
        "Machine learning for content moderation when you cannot read everything",
        {
            x: M, y: 3.95, w: 8.8, h: 0.9,
            fontFace: BODY, fontSize: 20, color: MUTED, margin: 0, lineSpacing: 28,
        });

    queueMotif(s, M, 5.35, [1, 4, 5]);

    s.addText("A 4-minute executive briefing", {
        x: M, y: 5.85, w: 6, h: 0.35,
        fontFace: BODY, fontSize: 13, italic: true, color: MUTED, margin: 0,
    });

    s.addNotes(
        "Every day, a social platform receives more posts than any team of humans " +
        "could ever read. This briefing is about which of those posts a person " +
        "should look at first, and what I found when I tested two ways of deciding.");
}

// =====================================================================
// 2  The problem
// =====================================================================
{
    const s = darkSlide();
    eyebrow(s, "THE PROBLEM");
    slideTitle(s, "The constraint isn't detection. It's capacity.");

    // Big stat block
    s.addShape(pres.ShapeType.roundRect, {
        x: M, y: 2.15, w: 4.55, h: 3.85, rectRadius: 0.12,
        fill: { color: CARD }, line: { type: "none" },
    });
    s.addText("~1%", {
        x: M + 0.45, y: 2.75, w: 3.7, h: 1.5,
        fontFace: HEAD, fontSize: 94, bold: true, color: CORAL, margin: 0,
    });
    s.addText("of the daily stream is all a fixed review team can realistically read.", {
        x: M + 0.45, y: 4.35, w: 3.7, h: 1.2,
        fontFace: BODY, fontSize: 17, color: MUTED, margin: 0, lineSpacing: 24,
    });

    // Three constraint lines
    const rows = [
        ["You can't review everything.", "The volume beats any headcount you can hire."],
        ["You can't delete automatically.", "Get it wrong and you have silenced ordinary people."],
        ["So the real question is triage.", "Of everything that arrived today, what does a human see first?"],
    ];
    rows.forEach((r, i) => {
        const y = 2.35 + i * 1.28;
        s.addShape(pres.ShapeType.ellipse, {
            x: 5.9, y: y + 0.06, w: 0.3, h: 0.3,
            fill: { color: i === 2 ? CORAL : "2E4166" }, line: { type: "none" },
        });
        s.addText(r[0], {
            x: 6.42, y, w: 6.0, h: 0.38,
            fontFace: BODY, fontSize: 18, bold: true, color: INK, margin: 0,
        });
        s.addText(r[1], {
            x: 6.42, y: y + 0.38, w: 6.0, h: 0.5,
            fontFace: BODY, fontSize: 14.5, color: MUTED, margin: 0,
        });
    });

    s.addNotes(
        "Here is the constraint. A fixed review team can realistically read about one " +
        "percent of what arrives. You can't review everything, and you can't just " +
        "delete automatically, because if you get that wrong you have silenced " +
        "ordinary people, and you will hear about it from them, from the press, and " +
        "from the regulator. So the question isn't whether a computer can spot harmful " +
        "content. It's this: given that we only ever get to look at a tiny slice, " +
        "which slice?");
}

// =====================================================================
// 3  What I did
// =====================================================================
{
    const s = darkSlide();
    eyebrow(s, "THE SETUP");
    slideTitle(s, "What I tested, and what I assumed");

    const items = [
        ["2", "Two public collections of real comments",
            "About 25,000 posts from one platform and 160,000 from another, each already judged harmful or not by people."],
        ["2", "Two automated sorting systems",
            "Built on different principles, both ranking content by how likely it is to break the rules."],
        ["5", "Five separate tests of each",
            "Run on different slices of the data, so a good result can't be a fluke of one lucky sample."],
    ];
    items.forEach((it, i) => {
        const y = 2.0 + i * 1.15;
        s.addShape(pres.ShapeType.ellipse, {
            x: M, y, w: 0.62, h: 0.62,
            fill: { color: CARD }, line: { color: "31456B", width: 1 },
        });
        s.addText(it[0], {
            x: M, y: y + 0.06, w: 0.62, h: 0.5,
            fontFace: HEAD, fontSize: 26, bold: true, color: CORAL,
            align: "center", margin: 0,
        });
        s.addText(it[1], {
            x: M + 0.95, y: y - 0.02, w: 7.2, h: 0.4,
            fontFace: BODY, fontSize: 19, bold: true, color: INK, margin: 0,
        });
        s.addText(it[2], {
            x: M + 0.95, y: y + 0.38, w: 8.3, h: 0.62,
            fontFace: BODY, fontSize: 14.5, color: MUTED, margin: 0, lineSpacing: 19,
        });
    });

    // Assumption callout
    s.addShape(pres.ShapeType.roundRect, {
        x: M, y: 5.62, w: W - 2 * M, h: 1.05, rectRadius: 0.1,
        fill: { color: CARD }, line: { type: "none" },
    });
    s.addText([
        { text: "Key assumption   ", options: { bold: true, color: CORAL, fontSize: 14 } },
        {
            text: "The machine's job is to rank, not to decide. A human still makes every call — " +
                "so the cost of a wrong ranking is a wasted review, not an unjust ban.",
            options: { color: INK, fontSize: 15 }
        },
    ], {
        x: M + 0.35, y: 5.78, w: W - 2 * M - 0.7, h: 0.75,
        fontFace: BODY, margin: 0, lineSpacing: 20,
    });

    s.addNotes(
        "Here's what I did. I took two public collections of online comments that " +
        "people had already judged as harmful or not — about twenty-five thousand " +
        "posts from one platform, and about a hundred and sixty thousand from " +
        "another. I built two different automated systems to sort content by how " +
        "likely it is to break the rules. And I tested each one five separate times, " +
        "on different slices of the data, so the numbers aren't a fluke. One " +
        "assumption runs through all of it: the machine's job is to rank, not to " +
        "decide. A human still makes the call.");
}

// =====================================================================
// 4  Finding 1
// =====================================================================
{
    const s = darkSlide();
    eyebrow(s, "FINDING 01");
    slideTitle(s, "The obvious scoreboard lies");

    const cols = [
        ["The 'better' system", "94.5%", "accurate overall", "13%", "of harmful posts caught", CORAL],
        ["The simpler system", "92.2%", "accurate overall", "41%", "of harmful posts caught", "6EA8FF"],
    ];
    cols.forEach((c, i) => {
        const x = M + i * 4.55;
        s.addShape(pres.ShapeType.roundRect, {
            x, y: 2.0, w: 4.15, h: 3.05, rectRadius: 0.12,
            fill: { color: CARD }, line: { type: "none" },
        });
        s.addText(c[0], {
            x: x + 0.35, y: 2.22, w: 3.45, h: 0.35,
            fontFace: BODY, fontSize: 15, bold: true, color: MUTED, margin: 0,
        });
        s.addText(c[1], {
            x: x + 0.35, y: 2.62, w: 3.45, h: 0.72,
            fontFace: HEAD, fontSize: 40, bold: true, color: INK, margin: 0,
        });
        s.addText(c[2], {
            x: x + 0.35, y: 3.32, w: 3.45, h: 0.3,
            fontFace: BODY, fontSize: 13.5, color: MUTED, margin: 0,
        });
        s.addText(c[3], {
            x: x + 0.35, y: 3.78, w: 3.45, h: 0.78,
            fontFace: HEAD, fontSize: 46, bold: true, color: c[5], margin: 0,
        });
        s.addText(c[4], {
            x: x + 0.35, y: 4.56, w: 3.45, h: 0.32,
            fontFace: BODY, fontSize: 13.5, color: MUTED, margin: 0,
        });
    });

    // Punchline
    s.addShape(pres.ShapeType.roundRect, {
        x: 9.5, y: 2.0, w: 3.08, h: 3.05, rectRadius: 0.12,
        fill: { color: CORAL }, line: { type: "none" },
    });
    s.addText("Flag nothing at all and you still score 94%.", {
        x: 9.82, y: 2.35, w: 2.45, h: 1.7,
        fontFace: HEAD, fontSize: 25, bold: true, color: "2A0D08", margin: 0, lineSpacing: 30,
    });
    s.addText("Harmful content is under 6% of the data.", {
        x: 9.82, y: 4.15, w: 2.45, h: 0.75,
        fontFace: BODY, fontSize: 13.5, color: "4A1A10", margin: 0, lineSpacing: 18,
    });

    s.addText("Accuracy rewards a system for being quiet. We need one that is right when it speaks.", {
        x: M, y: 5.5, w: W - 2 * M, h: 0.5,
        fontFace: BODY, fontSize: 17, italic: true, color: MUTED, margin: 0,
    });

    s.addNotes(
        "First finding: the obvious scoreboard lies. On one dataset, the more " +
        "sophisticated system was more accurate overall — ninety-four point five " +
        "percent of its decisions were right, against ninety-two point two. But it " +
        "caught only thirteen percent of the genuinely harmful posts. The simpler, " +
        "less accurate system caught forty-one percent. That happens because harmful " +
        "content is rare — under six percent of the data. A system that flagged " +
        "absolutely nothing would score ninety-four percent accuracy and be " +
        "completely worthless. So accuracy is the wrong scoreboard. What matters is " +
        "how much harm you actually catch, and how clean the queue is that you hand " +
        "a reviewer.");
}

// =====================================================================
// 5  Finding 2
// =====================================================================
{
    const s = darkSlide();
    eyebrow(s, "FINDING 02");
    slideTitle(s, "The two systems were the same");

    s.addText(
        "Measured properly, the gap between them was small enough to be chance. " +
        "They sort content into essentially the same order. The only thing that " +
        "differs is where you draw the cut-off line — how aggressive you are " +
        "willing to be about what reaches a reviewer.",
        {
            x: M, y: 2.25, w: 6.5, h: 2.3,
            fontFace: BODY, fontSize: 19, color: INK, margin: 0, lineSpacing: 31,
        });

    s.addText("One ranks. The other ranks the same way. You are not choosing a model.", {
        x: M, y: 4.75, w: 6.5, h: 0.9,
        fontFace: BODY, fontSize: 15.5, color: MUTED, margin: 0, lineSpacing: 22,
    });

    queueMotif(s, M, 6.05, [1, 4, 5]);

    // Pull quote
    s.addShape(pres.ShapeType.roundRect, {
        x: 7.75, y: 2.15, w: 4.83, h: 4.05, rectRadius: 0.14,
        fill: { color: CARD }, line: { type: "none" },
    });
    s.addText("This isn't an engineering decision.", {
        x: 8.2, y: 2.7, w: 3.95, h: 1.35,
        fontFace: HEAD, fontSize: 28, bold: true, color: MUTED, margin: 0, lineSpacing: 35,
    });
    s.addText("It's a staffing decision.", {
        x: 8.2, y: 4.25, w: 3.95, h: 1.4,
        fontFace: HEAD, fontSize: 34, bold: true, color: CORAL, margin: 0, lineSpacing: 41,
    });

    s.addNotes(
        "Second finding, and this one surprised me. Once I measured them properly, " +
        "the two systems were the same. The difference between them was small enough " +
        "to be chance. They rank content in essentially the same order. What differs " +
        "is only where you draw the cut-off line. That reframes the whole decision. " +
        "Choosing between these two systems isn't an engineering question. It's a " +
        "staffing question: how many reviewers you have rostered is what decides " +
        "where the line goes.");
}

// =====================================================================
// 6  Finding 3 - the headline, inverted for emphasis
// =====================================================================
{
    const s = pres.addSlide();
    s.background = { color: LIGHT };

    s.addText("FINDING 03  ·  THE ONE THAT MATTERS", {
        x: M, y: 0.3, w: W - 2 * M, h: 0.3,
        fontFace: BODY, fontSize: 12, bold: true, color: CHART_R,
        charSpacing: 2.2, margin: 0,
    });
    slideTitle(s, "Then I moved it to a different platform", DARKINK);

    s.addChart(pres.ChartType.bar, [{
        name: "Share of each category flagged",
        labels: ["Genuinely hateful\n(should flag)", "Merely rude\n(should not)", "Ordinary posts\n(should not)"],
        values: [83, 83, 27],
    }], {
        x: M, y: 1.9, w: 7.0, h: 4.25,
        barDir: "col",
        chartColors: [CHART_R, CHART_R, CHART_B],
        showLegend: false,
        showTitle: false,
        showValue: true,
        dataLabelPosition: "outEnd",
        dataLabelFormatCode: '0"%"',
        dataLabelColor: DARKINK,
        dataLabelFontSize: 15,
        dataLabelFontBold: true,
        catAxisLabelColor: "44506B",
        catAxisLabelFontSize: 12.5,
        valAxisLabelColor: "8A94AD",
        valAxisLabelFontSize: 11,
        valAxisMaxVal: 100,
        valAxisMajorUnit: 25,
        valGridLine: { color: "DDE3EF", size: 1 },
        catGridLine: { style: "none" },
        barGapWidthPct: 55,
    });

    s.addShape(pres.ShapeType.roundRect, {
        x: 8.15, y: 1.9, w: 4.43, h: 1.95, rectRadius: 0.12,
        fill: { color: CHART_R }, line: { type: "none" },
    });
    s.addText("73%", {
        x: 8.5, y: 2.05, w: 3.73, h: 0.85,
        fontFace: HEAD, fontSize: 54, bold: true, color: "FFFFFF", margin: 0,
    });
    s.addText("of everything was flagged. The true rate of harmful content was under 6%.", {
        x: 8.5, y: 2.92, w: 3.73, h: 0.85,
        fontFace: BODY, fontSize: 14, color: "FFE9E4", margin: 0, lineSpacing: 19,
    });

    s.addText("It cannot tell them apart.", {
        x: 8.15, y: 4.15, w: 4.43, h: 0.5,
        fontFace: HEAD, fontSize: 25, bold: true, color: DARKINK, margin: 0,
    });
    s.addText(
        "Genuinely hateful posts and merely rude ones were flagged at the identical " +
        "rate — because the data it learned from never separated the two.",
        {
            x: 8.15, y: 4.68, w: 4.43, h: 1.35,
            fontFace: BODY, fontSize: 14.5, color: "44506B", margin: 0, lineSpacing: 21,
        });

    s.addNotes(
        "Now the finding that matters most. I took a system trained on one platform's " +
        "data and pointed it at a different platform. On its home turf it looked " +
        "excellent. On the new data it flagged seventy-three percent of everything " +
        "that came through — when the true rate of harmful content was under six " +
        "percent. And look at how it failed. It flagged genuinely hateful posts " +
        "eighty-three percent of the time, and merely rude posts eighty-three percent " +
        "of the time. The identical rate. It cannot tell them apart, because the data " +
        "it learned from never made that distinction in the first place.");
}

// =====================================================================
// 7  What it costs
// =====================================================================
{
    const s = darkSlide();
    eyebrow(s, "WHY IT MATTERS");
    slideTitle(s, "In production, that is not a slightly worse score");

    const costs = [
        ["Mass wrongful removals", "Three quarters of ordinary posts pulled from a legitimate community."],
        ["An appeals backlog you cannot staff", "Every wrongful removal becomes a complaint, and complaints need people too."],
        ["Regulatory and press attention", "Over-blocking is the failure that makes the news, not under-blocking."],
        ["And it was invisible", "Every test on the original dataset said the system was excellent."],
    ];
    costs.forEach((c, i) => {
        const x = M + (i % 2) * 6.2;
        const y = 2.15 + Math.floor(i / 2) * 2.15;
        s.addShape(pres.ShapeType.roundRect, {
            x, y, w: 5.7, h: 1.82, rectRadius: 0.1,
            fill: { color: i === 3 ? "2B1A22" : CARD }, line: { type: "none" },
        });
        s.addText(c[0], {
            x: x + 0.38, y: y + 0.32, w: 4.95, h: 0.42,
            fontFace: BODY, fontSize: 18, bold: true,
            color: i === 3 ? CORAL : INK, margin: 0,
        });
        s.addText(c[1], {
            x: x + 0.38, y: y + 0.82, w: 4.95, h: 0.75,
            fontFace: BODY, fontSize: 14.5, color: MUTED, margin: 0, lineSpacing: 20,
        });
    });

    s.addNotes(
        "In production that isn't a slightly worse score. That is mass wrongful " +
        "removal of ordinary people's posts. That is an appeals backlog, press " +
        "coverage, and a regulator asking questions. And the part that should worry " +
        "you most: no amount of testing on the original dataset would have caught " +
        "it. It only appeared when I changed the source.");
}

// =====================================================================
// 8  Recommendation
// =====================================================================
{
    const s = darkSlide();
    eyebrow(s, "RECOMMENDATION");
    slideTitle(s, "What I would do");

    const recs = [
        ["01", "Ship the simpler system",
            "It ranks just as well, trains for a fraction of the cost, and when someone appeals a removal you can actually explain why it was flagged."],
        ["02", "Treat the cut-off as an operational dial",
            "Tie it to how many reviewers you have this week. It is a capacity setting, not a fixed property of the model."],
        ["03", "Never sign off on one source of labels",
            "Validate every moderation model against data it has never seen from a platform it was not trained on."],
    ];
    recs.forEach((r, i) => {
        const y = 2.05 + i * 1.42;
        s.addText(r[0], {
            x: M, y: y + 0.02, w: 0.9, h: 0.6,
            fontFace: HEAD, fontSize: 30, bold: true, color: "31456B", margin: 0,
        });
        s.addText(r[1], {
            x: M + 1.0, y, w: 10.6, h: 0.42,
            fontFace: BODY, fontSize: 20, bold: true, color: INK, margin: 0,
        });
        s.addText(r[2], {
            x: M + 1.0, y: y + 0.44, w: 10.6, h: 0.72,
            fontFace: BODY, fontSize: 14.5, color: MUTED, margin: 0, lineSpacing: 20,
        });
    });

    queueMotif(s, M, 6.5, [1, 4, 5]);

    s.addNotes(
        "So, three recommendations. First, ship the simpler system — it ranks just as " +
        "well, costs a fraction as much to train, and when someone appeals a removal " +
        "you can actually explain why it was flagged. Second, treat the cut-off as an " +
        "operational dial tied to how many reviewers you have that week, rather than " +
        "a fixed property of the model. And third, never sign off a moderation model " +
        "on a single source of labelled data.");
}

// =====================================================================
// 9  Caveats and close
// =====================================================================
{
    const s = darkSlide();
    eyebrow(s, "WHAT I WOULD CAVEAT");

    s.addText("Two limits on everything I just said", {
        x: M, y: 0.62, w: W - 2 * M, h: 0.9,
        fontFace: HEAD, fontSize: 36, bold: true, color: INK, margin: 0,
    });

    const caveats = [
        ["English text only",
            "Both collections are written English. The platform I have in mind is short video, in dozens of languages. Nothing here transfers for free."],
        ["Fair on average is not fair",
            "A system that looks even overall can still be far worse for one community. Before launch I would want the error rates broken down by dialect and speaker group."],
    ];
    caveats.forEach((c, i) => {
        const x = M + i * 6.2;
        s.addShape(pres.ShapeType.roundRect, {
            x, y: 1.85, w: 5.7, h: 2.15, rectRadius: 0.12,
            fill: { color: CARD }, line: { type: "none" },
        });
        s.addText(c[0], {
            x: x + 0.35, y: 2.1, w: 5.0, h: 0.42,
            fontFace: BODY, fontSize: 18, bold: true, color: CORAL, margin: 0,
        });
        s.addText(c[1], {
            x: x + 0.35, y: 2.58, w: 5.0, h: 1.25,
            fontFace: BODY, fontSize: 14.5, color: MUTED, margin: 0, lineSpacing: 21,
        });
    });

    s.addText("Measure the queue,", {
        x: M, y: 4.45, w: 11.8, h: 0.8,
        fontFace: HEAD, fontSize: 46, bold: true, color: INK, margin: 0,
    });
    s.addText("not the average.", {
        x: M, y: 5.25, w: 11.8, h: 0.8,
        fontFace: HEAD, fontSize: 46, bold: true, color: CORAL, margin: 0,
    });

    queueMotif(s, M, 6.35, [1, 4, 5]);

    s.addNotes(
        "Two caveats I would put on all of this. Both datasets are English text, and " +
        "the platform I have in mind is short video in many languages. And a system " +
        "that looks fair on average can still be much worse for one particular " +
        "community — so before anything went live I would want the error rates broken " +
        "down by dialect and speaker group, not just the headline number. The single " +
        "line I would leave you with: measure the queue, not the average.");
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
