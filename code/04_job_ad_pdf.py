"""
Produce a clean PDF copy of the job advertisement for the report appendix.
Text captured verbatim from the live listing on 14 August 2026.
"""

import os

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "img", "job_advertisement.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

URL = ("https://au.gradconnection.com/employers/tiktok/jobs/"
       "tiktok-machine-learning-engineer-graduate-trust-and-safety-"
       "engineering-2027-start-5/")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=15, spaceAfter=4)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=11.5, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("BODY", parent=ss["BodyText"], fontSize=9.5, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=5)
META = ParagraphStyle("META", parent=ss["BodyText"], fontSize=8.5, leading=11,
                      textColor="#444444", spaceAfter=2)
BULLET = ParagraphStyle("BULLET", parent=BODY, spaceAfter=2)


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(i, BULLET), leftIndent=10) for i in items],
        bulletType="bullet", start="•", leftIndent=12, bulletFontSize=8,
    )


story = [
    Paragraph("Machine Learning Engineer Graduate "
              "(Trust and Safety Engineering) &ndash; 2027 Start", H1),
    Paragraph("<b>Employer:</b> TikTok &nbsp;|&nbsp; <b>Location:</b> Sydney, NSW, Australia "
              "&nbsp;|&nbsp; <b>Job type:</b> Graduate Jobs", META),
    Paragraph("<b>Disciplines:</b> Computer Science, Engineering Software, Information Systems "
              "&nbsp;|&nbsp; <b>Accepts international applicants:</b> Yes", META),
    Paragraph("<b>Closing date:</b> 30 August 2026, 11:59 pm", META),
    Paragraph(f'<b>Source:</b> <link href="{URL}" color="blue">{URL}</link>', META),
    Paragraph("<b>Retrieved:</b> 14 August 2026. Reproduced for academic coursework "
              "(RMIT COSC2669/COSC2816, Individual Task 1).", META),
    Spacer(1, 8),

    Paragraph("Team Introduction", H2),
    Paragraph("Building a world where people can safely discover, create and connect. "
              "The Trust &amp; Safety (T&amp;S) team at TikTok helps ensure that our global "
              "online community is safe and empowered to create and enjoy content across all "
              "of our applications. We have invested heavily in human and machine-based "
              "moderation to remove harmful content quickly and often before it reaches our "
              "general community.", BODY),
    Paragraph("We are looking for talented individuals to join our team in 2027. As a graduate, "
              "you will get opportunities to pursue bold ideas, tackle complex challenges, and "
              "unlock limitless growth. Launch your career where inspiration is infinite at our "
              "Company.", BODY),
    Paragraph("Successful candidates must be able to commit to an onboarding date by end of "
              "year 2027. Please state your availability and graduation date clearly in your "
              "resume.", BODY),
    Paragraph("As a Machine Learning Engineer, you'll have the chance to work with our clients "
              "and teams to address key business problems and identify areas of growth for the "
              "company. With your education and experience, you will be able to take on "
              "real-world challenges from day one.", BODY),

    Paragraph("Responsibilities", H2),
    bullets([
        "Collaborate on research projects within the team or across countries",
        "Work with our world-class engineers to build industry-leading trust and safety "
        "systems for TikTok",
        "Develop and build up highly-scalable classifiers, tools, models and algorithms "
        "leveraging cutting-edge machine learning, computer vision and data mining technologies",
        "Improve our trust and safety strategy and work on model iterations",
        "Collaborate with cross-functional teams to protect TikTok globally",
        "Present research outcomes to internal and/or external audiences",
        "Work with engineering teams to apply technical achievements from our research to "
        "product prototyping",
        "Develop and implement innovative machine learning algorithms to manage business risks "
        "in TikTok's products and platforms",
        "Prototype and explore novel solutions, conduct experiments to validate hypotheses, and "
        "provide insights to Product and Tech teams",
    ]),

    Paragraph("Minimum Qualifications", H2),
    bullets([
        "Currently pursuing your PhD or Master degree in Computer Science or related "
        "engineering field",
        "Solid knowledge in at least one of the following areas: machine learning, pattern "
        "recognition, NLP, data mining, or computer vision",
        "Firm understanding of data structures and algorithms",
        "Great communication and teamwork skills",
    ]),

    Paragraph("Preferred Qualifications", H2),
    bullets([
        "Passion about techniques and solving challenging problems",
        "Previous experience in applications of machine learning, pattern recognition, NLP, "
        "data mining, or computer vision",
    ]),

    Spacer(1, 6),
    Paragraph("By submitting an application for this role, you accept and agree to our global "
              "applicant privacy policy, which may be accessed here: "
              "https://careers.tiktok.com/legal/privacy", META),
    Paragraph("If you have any questions, please reach out to us at "
              "apac-earlycareers@tiktok.com", META),
]

SimpleDocTemplate(OUT, pagesize=A4,
                  leftMargin=20 * mm, rightMargin=20 * mm,
                  topMargin=18 * mm, bottomMargin=18 * mm,
                  title="TikTok - Machine Learning Engineer Graduate "
                        "(Trust and Safety Engineering) - 2027 Start",
                  ).build(story)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
