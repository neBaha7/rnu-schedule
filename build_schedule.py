from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)

OUT = "RNU_schedule_10Nov-25Dec_2026.pdf"

CN = "Computer Networks Architecture and Operating Systems"
MATH = "Mathematical and Numerical Methods"
AUT = "Automata Computability and Complexity"
SOOP = "System and Object-Oriented Programming"
JAVA = "Java Development Fundamentals"
DPTF = "Development Process and Tooling Foundations"

# (tint background, dark accent)
COL = {
    CN: ("#DCE9FA", "#1F4E8C"),
    MATH: ("#DDF1E3", "#1E6B3A"),
    AUT: ("#E8E0F5", "#54338F"),
    SOOP: ("#FCE8D2", "#9A5410"),
    JAVA: ("#F9DEDE", "#9B2C2C"),
    DPTF: ("#D9EFEF", "#1B6A6A"),
}
INK = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#6B7785")
LINE = colors.HexColor("#D5DAE0")
HEAD = colors.HexColor("#1F2933")

def tue(): return [("10:00", CN), ("11:45", CN)]
def wed(): return [("10:00", MATH), ("11:45", MATH)]
def thu(): return [("10:00", AUT), ("11:45", AUT), ("13:45", SOOP), ("15:30", SOOP)]
def fri(): return [("09:00", JAVA), ("10:45", DPTF)]

# 15:30 on Thu 12 Nov was cut off in the screenshot -> marked with *
thu12 = [("10:00", AUT), ("11:45", AUT), ("13:45", SOOP), ("15:30 *", SOOP)]

weeks = [
    ("9 - 13 Nov", [("Tue 10 Nov", tue()), ("Wed 11 Nov", wed()),
                    ("Thu 12 Nov", thu12), ("Fri 13 Nov", fri())]),
    ("16 - 20 Nov", [("Tue 17 Nov", tue()), ("Wed 18 Nov", None),
                     ("Thu 19 Nov", thu()), ("Fri 20 Nov", fri())]),
    ("23 - 27 Nov", [("Tue 24 Nov", tue()), ("Wed 25 Nov", wed()),
                     ("Thu 26 Nov", thu()), ("Fri 27 Nov", fri())]),
    ("30 Nov - 4 Dec", [("Tue 1 Dec", tue()), ("Wed 2 Dec", wed()),
                        ("Thu 3 Dec", thu()), ("Fri 4 Dec", fri())]),
    ("7 - 11 Dec", [("Tue 8 Dec", tue()), ("Wed 9 Dec", wed()),
                    ("Thu 10 Dec", thu()), ("Fri 11 Dec", fri())]),
    ("14 - 18 Dec", [("Tue 15 Dec", tue()), ("Wed 16 Dec", wed()),
                     ("Thu 17 Dec", thu()), ("Fri 18 Dec", fri())]),
    ("21 - 25 Dec", [("Tue 22 Dec", tue()), ("Wed 23 Dec", None),
                     ("Thu 24 Dec", thu()), ("Fri 25 Dec", [("09:00", JAVA)])]),
]

H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=INK)
SUB = ParagraphStyle("sub", fontName="Helvetica", fontSize=10, leading=14, textColor=MUTED)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=INK,
                    spaceBefore=16, spaceAfter=8)
BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK,
                      leftIndent=12, bulletIndent=0, spaceAfter=4)
CELL_T = ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=9, leading=11)
CELL_N = ParagraphStyle("cn", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=INK)
TH = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9.5, leading=12,
                    textColor=colors.white, alignment=1)
AG = ParagraphStyle("ag", fontName="Helvetica", fontSize=9, leading=11, textColor=INK)
AGB = ParagraphStyle("agb", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=INK)
AGM = ParagraphStyle("agm", fontName="Helvetica-Oblique", fontSize=9, leading=11, textColor=MUTED)
WK = ParagraphStyle("wk", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=MUTED)


def hexc(h):
    return colors.HexColor(h)


def cell(time, course):
    fg = COL[course][1]
    t = ParagraphStyle("t", parent=CELL_T, textColor=hexc(fg))
    return [Paragraph(time, t), Paragraph(course, CELL_N)]


def typical_week():
    days = [("Tuesday", tue()), ("Wednesday", wed()), ("Thursday", thu()), ("Friday", fri())]
    data = [[Paragraph(d, TH) for d, _ in days]]
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("INNERGRID", (0, 0), (-1, -1), 2, colors.white),
        ("BOX", (0, 0), (-1, -1), 2, colors.white),
    ]
    for r in range(4):
        row = []
        for c, (_, items) in enumerate(days):
            if r < len(items):
                time, course = items[r]
                row.append(cell(time, course))
                style.append(("BACKGROUND", (c, r + 1), (c, r + 1), hexc(COL[course][0])))
            else:
                row.append("")
        data.append(row)
    w = (A4[0] - 80) / 4
    t = Table(data, colWidths=[w] * 4)
    t.setStyle(TableStyle(style))
    return t


def agenda(weeks):
    data, style = [], [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    for wk, days in weeks:
        r = len(data)
        data.append([Paragraph("WEEK OF " + wk.upper(), WK), "", ""])
        style += [("SPAN", (0, r), (-1, r)),
                  ("BACKGROUND", (0, r), (-1, r), colors.HexColor("#EEF1F4"))]
        for label, items in days:
            if items is None:
                r = len(data)
                data.append([Paragraph(label, AGB),
                             Paragraph({"Wed 18 Nov": "No classes listed (public holiday in Latvia)"}.get(label, "No classes listed"), AGM), ""])
                style += [("SPAN", (1, r), (2, r)),
                          ("LINEABOVE", (0, r), (-1, r), 0.5, LINE)]
                continue
            for i, (time, course) in enumerate(items):
                r = len(data)
                data.append([Paragraph(label if i == 0 else "", AGB),
                             Paragraph(time, AGB), Paragraph(course, AG)])
                style.append(("BACKGROUND", (2, r), (2, r), hexc(COL[course][0])))
                style.append(("LINEBEFORE", (2, r), (2, r), 3, hexc(COL[course][1])))
                if i == 0:
                    style.append(("LINEABOVE", (0, r), (-1, r), 0.5, LINE))
    t = Table(data, colWidths=[78, 52, A4[0] - 80 - 130], repeatRows=0)
    t.setStyle(TableStyle(style))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(40, 24, "Source: schedule.rnu.lv, read on 10 Nov 2026. Start times only.")
    canvas.drawRightString(A4[0] - 40, 24, "Page %d" % doc.page)
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=40, rightMargin=40,
                        topMargin=40, bottomMargin=46,
                        title="Class schedule 10 Nov - 25 Dec 2026", author="Claude")
s = []
s.append(Paragraph("Class schedule", H1))
s.append(Paragraph("10 November - 25 December 2026", SUB))
s.append(Paragraph("A typical week", H2))
s.append(typical_week())
s.append(Spacer(1, 6))
s.append(Paragraph("No classes on Monday, Saturday or Sunday.", SUB))
s.append(Paragraph("Good to know", H2))
notes = [
    "<b>System and Object-Oriented Programming moves to Thursday.</b> It ran on Wednesdays "
    "(28 Oct, 4 Nov) and is listed on Thursdays from 12 Nov.",
    "<b>Wed 18 Nov has no classes</b> (it is a public holiday in Latvia), so there is no "
    "Mathematical and Numerical Methods that week.",
    "<b>* Check Thu 12 Nov, 15:30.</b> This slot was cut off at the bottom of the screenshot. "
    "It is shown because every other Thursday has the same 15:30 class.",
    "<b>Fri 25 Dec lists only Java Development Fundamentals.</b> Nothing is listed after 25 Dec "
    "(the site showed empty weeks up to 10 Jan).",
    "Only start times appeared on the schedule page. Room numbers, lecturers and end times were "
    "not visible, so they are not included.",
]
for n in notes:
    s.append(Paragraph(n, BODY, bulletText="\u2022"))
s.append(PageBreak())
s.append(Paragraph("Day by day", H1))
s.append(Spacer(1, 8))
for w in weeks:
    s.append(KeepTogether([agenda([w]), Spacer(1, 5)]))
doc.build(s, onFirstPage=footer, onLaterPages=footer)
print("ok", OUT)
