"""
SerenLexAI — Contract Risk Analysis PDF Report Generator
---------------------------------------------------------
Usage (standalone):
    from generate_report_pdf import generate_report_pdf
    path = generate_report_pdf(analysis_data, output_path="report.pdf")

LangGraph node usage:
    from generate_report_pdf import generate_report_pdf_node
    builder.add_node("generate_pdf_report", generate_report_pdf_node)
"""

import io
from datetime import datetime, UTC
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import HexColor


# ---------------------------------------------------------------------------
# Brand Colours (SerenLexAI palette)
# ---------------------------------------------------------------------------
BRAND_950   = HexColor("#0D1117")
BRAND_900   = HexColor("#0F1320")
BRAND_800   = HexColor("#161B27")
BRAND_700   = HexColor("#1A1F2E")
BRAND_600   = HexColor("#2D3550")
BRAND_500   = HexColor("#3B4566")
BRAND_400   = HexColor("#556080")

NEUTRAL_900 = HexColor("#1E293B")
NEUTRAL_700 = HexColor("#475569")
NEUTRAL_600 = HexColor("#64748B")
NEUTRAL_500 = HexColor("#94A3B8")
NEUTRAL_400 = HexColor("#CBD5E1")
NEUTRAL_300 = HexColor("#E2E8F0")
NEUTRAL_200 = HexColor("#F1F5F9")
NEUTRAL_100 = HexColor("#F8FAFC")

SURFACE         = HexColor("#F4F6F8")
SURFACE_CARD    = HexColor("#FFFFFF")
SURFACE_DARK    = HexColor("#141824")

RISK_HIGH       = HexColor("#EF4444")
RISK_HIGH_BG    = HexColor("#FEF2F2")
RISK_MEDIUM     = HexColor("#F59E0B")
RISK_MEDIUM_BG  = HexColor("#FFFBEB")
RISK_LOW        = HexColor("#10B981")
RISK_LOW_BG     = HexColor("#ECFDF5")

ACCENT_INDIGO   = HexColor("#6366F1")

BORDER_LIGHT    = HexColor("#E5E7EB")
BORDER_DARK     = HexColor("#2A3347")

PAGE_W, PAGE_H = A4


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def risk_colors(severity: str):
    s = (severity or "").lower()
    if s == "high":
        return RISK_HIGH, RISK_HIGH_BG
    if s == "medium":
        return RISK_MEDIUM, RISK_MEDIUM_BG
    return RISK_LOW, RISK_LOW_BG


def risk_score_color(score: int):
    if score >= 85:
        return RISK_HIGH
    if score >= 50:
        return RISK_MEDIUM
    return RISK_LOW


def overall_risk_label(overall_risk: str) -> str:
    return (overall_risk or "Unknown").upper()


# ---------------------------------------------------------------------------
# Header / Footer drawn on every page
# ---------------------------------------------------------------------------

class SerenLexPageCanvas(rl_canvas.Canvas):
    """Custom canvas that draws header + footer on every page."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_page_chrome(self._pageNumber, total)
            super().showPage()
        super().save()

    def _draw_page_chrome(self, page_num: int, total_pages: int):
        w, h = PAGE_W, PAGE_H

        # ── Header bar ──────────────────────────────────────────────────
        self.setFillColor(BRAND_800)
        self.rect(0, h - 18*mm, w, 18*mm, fill=1, stroke=0)

        # Logo text — SerenLexAI bold
        self.setFillColor(SURFACE_CARD)
        self.setFont("Helvetica-Bold", 13)
        self.drawString(14*mm, h - 11.5*mm, "SerenLexAI")

        # Subtitle on header right
        self.setFont("Helvetica", 8)
        self.setFillColor(NEUTRAL_400)
        self.drawRightString(w - 14*mm, h - 11.5*mm, "Contract Risk Analysis Report")

        # Thin separator line under header
        self.setStrokeColor(NEUTRAL_300)
        self.setLineWidth(0.5)
        self.line(0, h - 18*mm, w, h - 18*mm)

        # ── Footer bar ───────────────────────────────────────────────────
        self.setFillColor(BRAND_900)
        self.rect(0, 0, w, 10*mm, fill=1, stroke=0)

        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(SURFACE_CARD)
        self.drawString(14*mm, 3.5*mm, "SerenLexAI")

        self.setFont("Helvetica", 7)
        self.setFillColor(NEUTRAL_400)
        self.drawCentredString(w / 2, 3.5*mm, "Confidential — For Authorised Use Only")

        self.setFillColor(NEUTRAL_400)
        self.drawRightString(w - 14*mm, 3.5*mm, f"Page {page_num} of {total_pages}")


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def make_styles():
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Helvetica-Bold",
            fontSize=28,
            textColor=SURFACE_CARD,
            leading=36,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontName="Helvetica",
            fontSize=13,
            textColor=NEUTRAL_400,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            fontName="Helvetica",
            fontSize=9,
            textColor=NEUTRAL_600,
            leading=14,
            alignment=TA_CENTER,
        ),
        "section_heading": ParagraphStyle(
            "section_heading",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=BRAND_800,
            leading=18,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=NEUTRAL_900,
            leading=14,
            spaceAfter=4,
        ),
        "body_muted": ParagraphStyle(
            "body_muted",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=NEUTRAL_600,
            leading=13,
            spaceAfter=3,
        ),
        "label": ParagraphStyle(
            "label",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=NEUTRAL_700,
            leading=12,
            spaceAfter=2,
        ),
        "clause_title": ParagraphStyle(
            "clause_title",
            fontName="Helvetica-Bold",
            fontSize=10.5,
            textColor=NEUTRAL_900,
            leading=14,
            spaceAfter=3,
        ),
        "clause_text": ParagraphStyle(
            "clause_text",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=NEUTRAL_700,
            leading=13,
            spaceAfter=4,
        ),
        "risk_badge_high": ParagraphStyle(
            "risk_badge_high",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=RISK_HIGH,
        ),
        "risk_badge_medium": ParagraphStyle(
            "risk_badge_medium",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=RISK_MEDIUM,
        ),
        "risk_badge_low": ParagraphStyle(
            "risk_badge_low",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=RISK_LOW,
        ),
        "anomaly_title": ParagraphStyle(
            "anomaly_title",
            fontName="Helvetica-Bold",
            fontSize=9.5,
            textColor=RISK_HIGH,
            leading=13,
            spaceAfter=2,
        ),
        "footer_note": ParagraphStyle(
            "footer_note",
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=NEUTRAL_500,
            leading=12,
            alignment=TA_CENTER,
        ),
    }


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

CONTENT_TOP    = PAGE_H - 18*mm - 8*mm   # below header
CONTENT_BOTTOM = 10*mm + 6*mm            # above footer
CONTENT_H      = CONTENT_TOP - CONTENT_BOTTOM
MARGIN_L       = 14*mm
MARGIN_R       = 14*mm
CONTENT_W      = PAGE_W - MARGIN_L - MARGIN_R


def build_cover(story, styles, analysis):
    """Clean dark cover page — 2 colours: dark navy bg, white text."""
    story.append(Spacer(1, 12*mm))

    # Logo block — dark bg, white bold text
    logo_data = [[
        Paragraph("SerenLexAI", ParagraphStyle(
            "logo_cover", fontName="Helvetica-Bold", fontSize=20,
            textColor=SURFACE_CARD, alignment=TA_CENTER,
        ))
    ]]
    logo_table = Table(logo_data, colWidths=[CONTENT_W])
    logo_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), BRAND_800),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(logo_table)
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph("Contract Risk Analysis Report", ParagraphStyle(
        "ct", fontName="Helvetica-Bold", fontSize=22, textColor=NEUTRAL_900,
        alignment=TA_CENTER, leading=28, spaceAfter=4,
    )))

    contract_title = analysis.get("title", "Untitled Contract")
    story.append(Paragraph(contract_title, ParagraphStyle(
        "cs", fontName="Helvetica", fontSize=12, textColor=NEUTRAL_600,
        alignment=TA_CENTER, leading=17, spaceAfter=4,
    )))
    story.append(Spacer(1, 8*mm))

    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=NEUTRAL_300, spaceAfter=8*mm))

    # Meta table — white bg, black text
    generated_at = datetime.now().strftime("%d %B %Y, %H:%M UTC")
    meta_rows = [
        ["Analysis ID",  analysis.get("analysis_id", "N/A")],
        ["Source Type",  analysis.get("source_type", "PDF")],
        ["Status",       analysis.get("status", "completed").upper()],
        ["Generated At", generated_at],
    ]
    meta_label_style = ParagraphStyle("ml", fontName="Helvetica-Bold", fontSize=9,
                                      textColor=NEUTRAL_700, leading=13)
    meta_val_style   = ParagraphStyle("mv", fontName="Helvetica", fontSize=9,
                                      textColor=NEUTRAL_900, leading=13)

    meta_data = [[Paragraph(r[0], meta_label_style), Paragraph(r[1], meta_val_style)]
                 for r in meta_rows]

    meta_table = Table(meta_data, colWidths=[CONTENT_W * 0.38, CONTENT_W * 0.62])
    meta_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [SURFACE_CARD, SURFACE]),
        ("TOPPADDING",     (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 7),
        ("LEFTPADDING",    (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 10),
        ("BOX",            (0, 0), (-1, -1), 1, BORDER_LIGHT),
        ("LINEBELOW",      (0, 0), (-1, -2), 0.5, BORDER_LIGHT),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10*mm))

    story.append(Paragraph(
        "This report is confidential and intended solely for the authorised recipient. "
        "AI-generated analysis should be reviewed by a qualified legal professional before acting upon it.",
        ParagraphStyle("disc", fontName="Helvetica-Oblique", fontSize=7.5,
                       textColor=NEUTRAL_500, leading=11, alignment=TA_CENTER)
    ))
    story.append(PageBreak())


def build_executive_summary(story, styles, analysis):
    story.append(Paragraph("Executive Summary", styles["section_heading"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=NEUTRAL_300, spaceAfter=5*mm))

    risk_score    = analysis.get("risk_score", 0)  # still used in backend, not shown
    overall_risk  = analysis.get("overall_risk", "unknown")
    flagged       = analysis.get("flagged_count", 0)
    high_count    = analysis.get("high_count", 0)
    medium_count  = analysis.get("medium_count", 0)
    low_count     = analysis.get("low_count", 0)
    total_clauses = analysis.get("total_clauses", high_count + medium_count + low_count)

    # KPI card styles — number on top, label below, both centered
    num_style = ParagraphStyle(
        "kpi_num", fontName="Helvetica-Bold", fontSize=18,
        textColor=NEUTRAL_900, alignment=TA_CENTER, leading=22, spaceAfter=3,
    )
    lbl_style = ParagraphStyle(
        "kpi_lbl", fontName="Helvetica", fontSize=8,
        textColor=NEUTRAL_600, alignment=TA_CENTER, leading=11,
    )

    def kpi_cell(value, label):
        return [Paragraph(str(value), num_style), Paragraph(label, lbl_style)]

    kpi_data = [[
        kpi_cell(overall_risk_label(overall_risk), "Overall Risk Level"),
        kpi_cell(flagged,                          "Flagged Clauses"),
        kpi_cell(high_count,                       "HIGH Clauses"),
        kpi_cell(total_clauses,                    "Total Clauses"),
    ]]

    kpi_table = Table(kpi_data, colWidths=[CONTENT_W / 4] * 4, rowHeights=[20*mm])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), SURFACE_CARD),
        ("BOX",           (0, 0), (-1, -1), 1, BORDER_LIGHT),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 5*mm))

    # Severity breakdown — simple row, white bg, black text
    story.append(Paragraph("Severity Breakdown", styles["label"]))
    story.append(Spacer(1, 2*mm))

    breakdown_data = [[
        Paragraph(f"HIGH   {high_count} clause{'s' if high_count != 1 else ''}",
                  ParagraphStyle("b1", fontName="Helvetica-Bold", fontSize=9,
                                 textColor=RISK_HIGH, leading=13)),
        Paragraph(f"MEDIUM   {medium_count} clause{'s' if medium_count != 1 else ''}",
                  ParagraphStyle("b2", fontName="Helvetica-Bold", fontSize=9,
                                 textColor=RISK_MEDIUM, leading=13)),
        Paragraph(f"LOW   {low_count} clause{'s' if low_count != 1 else ''}",
                  ParagraphStyle("b3", fontName="Helvetica-Bold", fontSize=9,
                                 textColor=RISK_LOW, leading=13)),
    ]]
    breakdown_table = Table(breakdown_data, colWidths=[CONTENT_W / 3] * 3)
    breakdown_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), SURFACE_CARD),
        ("BOX",           (0, 0), (-1, -1), 1, BORDER_LIGHT),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(breakdown_table)
    story.append(Spacer(1, 8*mm))


def build_clause_section(story, styles, clauses):
    story.append(Paragraph("Clause-by-Clause Risk Analysis", styles["section_heading"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=NEUTRAL_300, spaceAfter=5*mm))

    if not clauses:
        story.append(Paragraph("No clauses were identified in this document.", styles["body_muted"]))
        return

    # Limit the number of LOW-severity clauses shown in the report so that
    # very long contracts do not surface dozens of low-risk indicators.
    MAX_LOW_TO_SHOW = 20

    def _sev(c):
        return str(c.get("severity", "")).lower()

    all_low_indices = [i for i, c in enumerate(clauses) if _sev(c) == "low"]

    if len(all_low_indices) > MAX_LOW_TO_SHOW:
        def _low_score(idx: int) -> int:
            raw = clauses[idx].get("risk_score")
            try:
                return int(raw) if raw is not None else 0
            except (TypeError, ValueError):
                return 0

        # Pick the LOW clauses with the highest numeric risk scores
        sorted_low = sorted(all_low_indices, key=_low_score, reverse=True)
        keep_low = set(sorted_low[:MAX_LOW_TO_SHOW])
    else:
        keep_low = set(all_low_indices)

    filtered_clauses = []
    for i, c in enumerate(clauses):
        s = _sev(c)
        if s in ("high", "medium") or i in keep_low:
            filtered_clauses.append(c)

    for i, clause in enumerate(filtered_clauses):
        severity    = clause.get("severity", "low")
        title       = clause.get("title", f"Clause {i + 1}")
        original    = clause.get("original_text", "")
        explanation = clause.get("risk_explanation", "")
        action      = clause.get("recommended_action", "")
        page        = clause.get("page_number")

        risk_color, _ = risk_colors(severity)

        # Header — dark bg, white text, severity badge right-aligned
        header_data = [[
            Paragraph(
                f"{title}",
                ParagraphStyle("ch", fontName="Helvetica-Bold", fontSize=10,
                               textColor=SURFACE_CARD, leading=14),
            ),
            Paragraph(
                severity.upper(),
                ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8,
                               textColor=risk_color, alignment=TA_RIGHT),
            ),
        ]]
        header_table = Table(header_data, colWidths=[CONTENT_W * 0.78, CONTENT_W * 0.22])
        header_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), BRAND_800),
            ("TOPPADDING",    (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING",   (0, 0), (0, -1), 10),
            ("RIGHTPADDING",  (-1, 0), (-1, -1), 10),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))

        # Sub-header — light gray, black text
        meta_data = [[Paragraph(
            f"Page: {page if page is not None else '—'}",
            ParagraphStyle("cm", fontName="Helvetica", fontSize=8,
                           textColor=NEUTRAL_600, leading=12),
        )]]
        meta_table = Table(meta_data, colWidths=[CONTENT_W])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), SURFACE),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ]))

        # Body rows — alternating white / light gray, black text
        lbl_s = ParagraphStyle("bl", fontName="Helvetica-Bold", fontSize=8,
                               textColor=NEUTRAL_700, leading=12)
        val_s = ParagraphStyle("bv", fontName="Helvetica", fontSize=8.5,
                               textColor=NEUTRAL_900, leading=13)

        body_data = [
            [Paragraph("ORIGINAL TEXT",      lbl_s), Paragraph(original[:500] + ("…" if len(original) > 500 else ""), val_s)],
            [Paragraph("RISK EXPLANATION",   lbl_s), Paragraph(explanation, val_s)],
            [Paragraph("RECOMMENDED ACTION", lbl_s), Paragraph(action, val_s)],
        ]
        body_table = Table(body_data, colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.78])
        body_table.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [SURFACE_CARD, SURFACE]),
            ("TOPPADDING",     (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
            ("LEFTPADDING",    (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",   (0, 0), (-1, -1), 10),
            ("VALIGN",         (0, 0), (-1, -1), "TOP"),
            ("BOX",            (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
            ("LINEBELOW",      (0, 0), (-1, -2), 0.5, BORDER_LIGHT),
        ]))

        block = KeepTogether([header_table, meta_table, body_table, Spacer(1, 5*mm)])
        story.append(block)

    story.append(PageBreak())


def build_anomalies_section(story, styles, anomalies):
    story.append(Paragraph("Anomaly Detection", styles["section_heading"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=NEUTRAL_300, spaceAfter=5*mm))

    if not anomalies:
        story.append(Paragraph(
            "No anomalies detected. The contract appears structurally consistent.",
            ParagraphStyle("ok", fontName="Helvetica", fontSize=9.5,
                           textColor=NEUTRAL_700, leading=14)
        ))
        story.append(Spacer(1, 8*mm))
        return

    for anomaly in anomalies:
        desc    = anomaly.get("description") or str(anomaly)
        a_type  = anomaly.get("type", "Anomaly")
        related = anomaly.get("related_clauses", [])

        # Header row — dark bg, white text
        hdr_data = [[Paragraph(a_type, ParagraphStyle(
            "ah", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=SURFACE_CARD, leading=13,
        ))]]
        hdr_table = Table(hdr_data, colWidths=[CONTENT_W])
        hdr_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), NEUTRAL_900),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ]))

        body_rows = [[Paragraph(desc, ParagraphStyle(
            "ad", fontName="Helvetica", fontSize=8.5,
            textColor=NEUTRAL_900, leading=13,
        ))]]
        if related:
            body_rows.append([Paragraph(
                f"Related clauses: {', '.join(str(r) for r in related)}",
                ParagraphStyle("ar", fontName="Helvetica-Oblique", fontSize=8,
                               textColor=NEUTRAL_600, leading=12),
            )])

        body_table = Table(body_rows, colWidths=[CONTENT_W])
        body_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), SURFACE_CARD),
            ("TOPPADDING",    (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("BOX",           (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ]))

        story.append(KeepTogether([hdr_table, body_table, Spacer(1, 4*mm)]))

    story.append(PageBreak())


def build_raw_text_section(story, styles, raw_text):
    story.append(Paragraph("Extracted Contract Text", styles["section_heading"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=NEUTRAL_300, spaceAfter=5*mm))
    story.append(Paragraph(
        "The following is the full text extracted from the uploaded contract document.",
        styles["body_muted"]
    ))
    story.append(Spacer(1, 3*mm))

    raw_style = ParagraphStyle(
        "raw", fontName="Courier", fontSize=7.5,
        textColor=NEUTRAL_700, leading=11, spaceAfter=3,
    )

    # Chunk into paragraphs on double newlines
    chunks = (raw_text or "").split("\n\n")
    for chunk in chunks:
        chunk = chunk.strip()
        if chunk:
            story.append(Paragraph(chunk.replace("\n", "<br/>"), raw_style))

    story.append(Spacer(1, 6*mm))


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_report_pdf(analysis_data: dict, output_path: str = "serenlex_report.pdf") -> str:
    """
    Generate a branded SerenLexAI PDF report.

    Parameters
    ----------
    analysis_data : dict
        Keys expected (all optional with sensible defaults):
          - analysis_id, title, source_type, status
          - risk_score (int), overall_risk (str)
          - flagged_count, high_count, medium_count, low_count (int)
          - clauses (list of dicts matching backend Clause schema)
          - anomalies (list of dicts)
          - raw_text (str)

    output_path : str
        Where to write the PDF.

    Returns
    -------
    str — the output_path
    """
    styles = make_styles()

    frame = Frame(
        MARGIN_L, CONTENT_BOTTOM,
        CONTENT_W, CONTENT_H,
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
        id="main",
    )
    template = PageTemplate(id="main", frames=[frame])
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        pageTemplates=[template],
        title="SerenLexAI — Contract Risk Report",
        author="SerenLexAI",
        subject=analysis_data.get("title", "Contract Analysis"),
        creator="SerenLexAI Report Engine",
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=18*mm + 8*mm,
        bottomMargin=10*mm + 6*mm,
    )

    story = []

    # 1. Cover page
    build_cover(story, styles, analysis_data)

    # 2. Executive summary
    build_executive_summary(story, styles, analysis_data)

    # 3. Clause analysis
    build_clause_section(story, styles, analysis_data.get("clauses", []))

    # 4. Anomalies
    build_anomalies_section(story, styles, analysis_data.get("anomalies", []))

    # 5. Raw text appendix
    raw_text = analysis_data.get("raw_text", "")
    if raw_text:
        build_raw_text_section(story, styles, raw_text)

    doc.build(story, canvasmaker=SerenLexPageCanvas)
    return output_path


# ---------------------------------------------------------------------------
# LangGraph node — drop-in for graph.add_node("generate_pdf_report", ...)
# ---------------------------------------------------------------------------

def generate_report_pdf_node(state: dict) -> dict:
    """
    LangGraph node that generates the PDF report from final aggregated state.

    Reads from state:
      - analysis_id, risk_score, overall_risk, flagged_count,
        high_count, medium_count, low_count
      - clause_results  (list of ClauseAnalysisResult objects)
      - anomalies       (list)
      - raw_text        (str)
      - final_report    (dict, used for title/source_type/status)

    Writes to state:
      - report_pdf_path (str)
    """
    final = state.get("final_report", {})
    clauses_raw = state.get("clause_results", [])

    def _humanise_clause_type(raw: str | None) -> str | None:
        if not raw:
            return None
        s = str(raw)
        if s.startswith("ClauseType."):
            s = s.split(".", 1)[1]
        s = s.lower()
        mapping = {
            "definitions": "Definitions",
            "liability": "Liability",
            "termination": "Termination",
            "payment": "Payment Terms",
            "confidentiality": "Confidentiality",
            "indemnification": "Indemnification",
            "intellectual_property": "Intellectual Property",
            "governing_law": "Governing Law",
            "force_majeure": "Force Majeure",
            "other": "Other",
        }
        return mapping.get(s)

    # Normalise clause results — support both objects and dicts, and
    # ensure user-facing titles never show internal ClauseType enums.
    clauses = []
    for c in clauses_raw:
        if isinstance(c, dict):
            data = dict(c)
        else:
            data = {
                "title":              getattr(c, "title", ""),
                "severity":           getattr(c, "severity", "low"),
                "original_text":      getattr(c, "original_text", ""),
                "risk_explanation":   getattr(c, "risk_explanation", ""),
                "recommended_action": getattr(c, "recommended_action", ""),
                "clause_type":        getattr(c, "clause_type", ""),
                "position_index":     getattr(c, "position_index", None),
                "page_number":        getattr(c, "page_number", None),
                "risk_score":         getattr(c, "risk_score", None),
            }

        clause_type_raw = data.get("clause_type")
        clause_type_str = str(clause_type_raw) if clause_type_raw is not None else ""
        data["clause_type"] = clause_type_str

        title = (data.get("title") or "").strip()
        if title.startswith("ClauseType.") or not title:
            human = _humanise_clause_type(clause_type_str)
            if human:
                title = human
        if not title:
            title = "Unnamed Clause"
        data["title"] = title

        clauses.append(data)

    raw_risk_score = state.get("risk_score", 0)
    try:
        risk_score = int(raw_risk_score)
    except (TypeError, ValueError):
        risk_score = 0
    risk_score = max(0, min(100, risk_score))

    def _is_valid_count(x):
        return isinstance(x, int) and x >= 0

    # Prefer aggregated counts from state (agentic workflow), fall back to
    # recomputing from clause severities if needed.
    high_state = state.get("high_count")
    med_state = state.get("medium_count")
    low_state = state.get("low_count")

    if _is_valid_count(high_state) and _is_valid_count(med_state) and _is_valid_count(low_state):
        high_count = high_state
        medium_count = med_state
        low_count = low_state
    else:
        def _sev(c):
            return str(c.get("severity", "")).lower()

        high_count = sum(1 for c in clauses if _sev(c) == "high")
        medium_count = sum(1 for c in clauses if _sev(c) == "medium")
        low_count = sum(1 for c in clauses if _sev(c) == "low")

    flagged_state = state.get("flagged_count")
    if _is_valid_count(flagged_state):
        flagged_count = flagged_state
    else:
        flagged_count = high_count + medium_count

    analysis_data = {
        "analysis_id":   state.get("analysis_id", "N/A"),
        "title":         final.get("title", "Untitled Contract"),
        "source_type":   final.get("source_type", "PDF"),
        "status":        final.get("status", "completed"),
        "risk_score":    risk_score,
        "overall_risk":  state.get("overall_risk", "unknown"),
        "flagged_count": flagged_count,
        "high_count":    high_count,
        "medium_count":  medium_count,
        "low_count":     low_count,
        "total_clauses": len(clauses),
        "clauses":       clauses,
        "anomalies":     state.get("anomalies", []),
        "raw_text":      state.get("raw_text", ""),
    }

    output_path = f"reports/{state.get('analysis_id', 'report')}_risk_report.pdf"

    import os
    os.makedirs("reports", exist_ok=True)

    generate_report_pdf(analysis_data, output_path)

    return {"report_pdf_path": output_path}


# ---------------------------------------------------------------------------
# Demo — run directly to preview with sample data
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample = {
        "analysis_id":   "demo-001",
        "title":         "Master Services Agreement — Thorngate Partners LLP",
        "source_type":   "PDF",
        "status":        "completed",
        "risk_score":    72,
        "overall_risk":  "high",
        "flagged_count": 3,
        "high_count":    2,
        "medium_count":  1,
        "low_count":     4,
        "clauses": [
            {
                "title":              "Intellectual Property Rights",
                "severity":           "high",
                "clause_type":        "intellectual_property",
                "position_index":     3,
                "original_text":      (
                    "All Intellectual Property Rights in the Deliverables shall vest in and "
                    "be assigned to the Supplier upon creation, and the Client shall have a "
                    "non-exclusive licence to use such Deliverables solely for its internal "
                    "business purposes."
                ),
                "risk_explanation":   (
                    "IP ownership is retained by the Supplier, not the Client. This means the "
                    "Client does not own work it has commissioned and paid for. If the relationship "
                    "ends, the Client's ability to use deliverables depends entirely on the licence "
                    "terms, which can be revoked."
                ),
                "recommended_action": (
                    "Negotiate for IP assignment to the Client upon full payment, or at minimum "
                    "ensure the licence is irrevocable, royalty-free, and sublicensable."
                ),
            },
            {
                "title":              "Liability Cap",
                "severity":           "high",
                "clause_type":        "liability",
                "position_index":     12,
                "original_text":      (
                    "The Supplier's total aggregate liability under this Agreement shall not exceed "
                    "the fees paid in the three (3) months preceding the event giving rise to the claim."
                ),
                "risk_explanation":   (
                    "A 3-month fee cap is extremely low for a digital transformation engagement. "
                    "In the event of a major failure, the Client could suffer losses far exceeding "
                    "this cap with no meaningful recourse."
                ),
                "recommended_action": (
                    "Negotiate the liability cap to at least 12 months of fees, and ensure "
                    "carve-outs for fraud, wilful misconduct, and data protection breaches."
                ),
            },
            {
                "title":              "Termination for Convenience",
                "severity":           "medium",
                "clause_type":        "termination",
                "position_index":     18,
                "original_text":      (
                    "Either party may terminate this Agreement for convenience on 90 days' written notice."
                ),
                "risk_explanation":   (
                    "While mutual, a 90-day notice for a long-term transformation programme may be "
                    "insufficient to complete critical deliverables or transition to an alternative supplier."
                ),
                "recommended_action": (
                    "Consider extending to 180 days and adding a wind-down clause that ensures "
                    "key deliverables are completed or handed over during the notice period."
                ),
            },
            {
                "title":              "Confidentiality",
                "severity":           "low",
                "clause_type":        "confidentiality",
                "position_index":     6,
                "original_text":      (
                    "Each party shall keep confidential all Confidential Information of the other "
                    "party and shall not disclose it to any third party without prior written consent."
                ),
                "risk_explanation":   "Standard mutual NDA clause. No material risk identified.",
                "recommended_action": "No action required. Clause is balanced and appropriate.",
            },
        ],
        "anomalies": [
            {
                "type":             "Missing Clause",
                "description":      (
                    "No Data Protection or GDPR compliance clause was detected. Given the nature "
                    "of the services, personal data is likely to be processed and a DPA should be included."
                ),
                "related_clauses":  [],
            },
            {
                "type":             "Conflict Detected",
                "description":      (
                    "Clause 12 (Liability) and Clause 18 (Indemnity) contain potentially conflicting "
                    "provisions regarding the financial cap on damages. Legal review is recommended."
                ),
                "related_clauses":  [12, 18],
            },
        ],
        "raw_text": (
            "MASTER SERVICES AGREEMENT\n\n"
            "Ref: TGP-MSA-2024-114 · Draft v0.7 · NOT FOR EXECUTION\n\n"
            "PARTIES\n\n"
            "Service Provider: Thorngate Partners LLP, a limited liability partnership registered "
            "in England and Wales (No. OC412887), whose registered office is at 4th Floor, Meridian "
            "House, 17-19 Canute Road, Southampton, SO14 3AB.\n\n"
            "Client: [CLIENT ENTITY NAME], a company incorporated in [JURISDICTION].\n\n"
            "1. DEFINITIONS AND INTERPRETATION\n\n"
            '"Agreement" means this Master Services Agreement together with all Schedules, Annexures '
            "and Statements of Work attached or incorporated herein from time to time.\n\n"
            '"Business Day" means any day other than a Saturday, Sunday or public holiday in England '
            "and Wales on which clearing banks in the City of London are open for business.\n\n"
            '"Confidential Information" means all information disclosed by one Party to the other '
            "in connection with this Agreement that is designated as confidential..."
        ),
    }

    out = generate_report_pdf(sample, "serenlex_demo_report.pdf")
    print(f"Report generated: {out}")