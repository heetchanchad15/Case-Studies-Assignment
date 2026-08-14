"""
Condition 3 - Bounded Use of Generative AI: declaration form.

NOTE: this reproduces the standard structure of a Condition 3 declaration. If the
template on Canvas uses different headings or fields, transfer this content into
that file rather than submitting this one.
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "AI-Declaration-Condition3.pdf")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=14, leading=17, spaceAfter=3)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=10.5, spaceBefore=11, spaceAfter=4)
BODY = ParagraphStyle("BODY", parent=ss["BodyText"], fontSize=9, leading=12,
                      alignment=TA_JUSTIFY, spaceAfter=5)
CELL = ParagraphStyle("CELL", parent=ss["BodyText"], fontSize=8.2, leading=10.4,
                      spaceAfter=0)
CELLH = ParagraphStyle("CELLH", parent=CELL, fontName="Helvetica-Bold",
                       textColor=colors.white)
META = ParagraphStyle("META", parent=ss["BodyText"], fontSize=9, leading=12, spaceAfter=2)

ACCENT = colors.HexColor("#2A3F6B")
BAND = colors.HexColor("#EDF1F8")


def p(t, s=CELL):
    return Paragraph(t, s)


story = [
    Paragraph("Assessment Declaration &mdash; Condition 3: Bounded Use of "
              "Generative Artificial Intelligence", H1),
    Spacer(1, 5),
]

# ---- student / assessment details -------------------------------------
details = [
    [p("<b>Student name</b>", CELL), p("Heet Chanchad", CELL),
     p("<b>Student number</b>", CELL), p("s4218211", CELL)],
    [p("<b>Course</b>", CELL), p("Case Studies in Data Science", CELL),
     p("<b>Course code</b>", CELL), p("COSC2669 / COSC2816", CELL)],
    [p("<b>Assessment</b>", CELL), p("Individual Task 1: Part 1", CELL),
     p("<b>Date</b>", CELL), p("14 August 2026", CELL)],
]
t = Table(details, colWidths=[28 * mm, 62 * mm, 28 * mm, 62 * mm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B9C4D8")),
    ("BACKGROUND", (0, 0), (0, -1), BAND),
    ("BACKGROUND", (2, 0), (2, -1), BAND),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story += [t, Spacer(1, 4)]

story.append(Paragraph("Declaration of use", H2))
story.append(Paragraph(
    "I declare that generative AI was used in the preparation of this assessment, within "
    "the bounds permitted under Condition 3, and that its use is disclosed in full below. "
    "The tool used was <b>Claude (Anthropic)</b>. No other generative AI tool was used. "
    "I take full responsibility for the content of the submitted work, including any "
    "material that originated as AI output.", BODY))

# ---- the disclosure table ---------------------------------------------
story.append(Paragraph("Where and how it was used", H2))

rows = [[p("Where in the assessment", CELLH), p("How generative AI was used", CELLH),
         p("How I verified, corrected or took ownership of the output", CELLH)]]

use = [
    ("Part 1.1 &mdash; role and job advertisement",
     "Used to search for live machine learning engineer advertisements and to confirm the "
     "listing URL resolved and the role was still open.",
     "I selected the role myself and read the full advertisement. I confirmed the closing "
     "date and the live application link directly on the employer's job board, and quoted "
     "the responsibilities verbatim from the source rather than from any summary."),
    ("Part 1.1 &mdash; written responses",
     "Used to draft and then condense prose to fit the 50-word limits on the industry, "
     "role focus, value, values and diversity questions.",
     "The argument in each response is mine. I checked every claim against the "
     "advertisement text, verified each word count, and rewrote wording that did not "
     "reflect my own position, particularly in the values response."),
    ("Appendix &mdash; cover letter",
     "Used to draft the letter and structure it as a stand-alone document.",
     "All personal details, my degree, my graduation date and my stated motivation are my "
     "own and were checked for accuracy. I removed a claim about meeting the employer's "
     "onboarding window once I confirmed my graduation date does not fall inside it."),
    ("Part 1.2 &mdash; datasets",
     "Used to identify candidate public datasets and to test whether their download URLs "
     "were reachable without an account.",
     "I chose the final two datasets. The sizes, attribute lists and class balances quoted "
     "in Table 1 were produced by running <font face='Courier'>02_profile_data.py</font> "
     "over the downloaded files, not taken from any description."),
    ("Part 1.3 &mdash; analysis code",
     "Used to draft the Python pipeline: dataset download, profiling, the "
     "cross-validation harness, the paired t-test, the cross-corpus transfer test and the "
     "figures.",
     "I ran the code myself and every number in Section 3 comes from that execution, not "
     "from the model. I reviewed the harness specifically to confirm the vectoriser is "
     "fitted inside each fold, since fitting it over the whole corpus would have leaked "
     "test data and inflated every result."),
    ("Part 1.3 &mdash; interpretation",
     "Used to draft the written discussion of the results.",
     "The interpretation is mine, including the decision to treat the two data sources as "
     "complementary about model choice but contradictory about labels, and the "
     "recommendation to ship the simpler model. I corrected drafted text that "
     "overstated the significance of the paired t-test."),
    ("Document production",
     "Used to format the LaTeX sources, assemble the BibTeX entries in ACM style, and "
     "typeset the retrieved job advertisement for the appendix.",
     "I compiled the document and inspected every page. Doing so revealed that the job "
     "advertisement figure was omitting its second page and that the cover letter was "
     "breaking across two pages; both are recorded in Appendix B and were fixed."),
]
for a, b, c in use:
    rows.append([p(a), p(b), p(c)])

t2 = Table(rows, colWidths=[34 * mm, 68 * mm, 78 * mm], repeatRows=1)
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B9C4D8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BAND]),
]))
story += [t2, Spacer(1, 6)]

story.append(Paragraph("What generative AI was <i>not</i> used for", H2))
story.append(Paragraph(
    "It was not used to generate any result, metric, table value or figure reported in "
    "Section 3. Every quantitative claim in this report was produced by executing the code "
    "in the linked repository. It was not used to fabricate or alter data, and it was not "
    "used to write this declaration's account of my own verification steps.", BODY))

story.append(Paragraph("Student statement", H2))
story.append(Paragraph(
    "I confirm that this disclosure is complete and accurate, that I understand the work "
    "submitted is my responsibility regardless of how it was drafted, and that I am able "
    "to explain and defend any part of the submitted analysis, code or written argument if "
    "asked to do so.", BODY))

story.append(Spacer(1, 14))
sig = Table(
    [[p("<b>Signed</b>", CELL), p("Heet Chanchad", CELL),
      p("<b>Date</b>", CELL), p("14 August 2026", CELL)]],
    colWidths=[20 * mm, 70 * mm, 18 * mm, 72 * mm])
sig.setStyle(TableStyle([
    ("LINEBELOW", (1, 0), (1, 0), 0.6, colors.HexColor("#7C8AA5")),
    ("LINEBELOW", (3, 0), (3, 0), 0.6, colors.HexColor("#7C8AA5")),
    ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(sig)

SimpleDocTemplate(OUT, pagesize=A4,
                  leftMargin=16 * mm, rightMargin=16 * mm,
                  topMargin=15 * mm, bottomMargin=15 * mm,
                  title="Condition 3 Bounded Use of Generative AI Declaration",
                  ).build(story)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
