import os
import logging
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("./generated_pdfs")


def create_pdf(content: str) -> str:
    """
    Render `content` (plain text / markdown-like headings) to a styled PDF.
    Returns the filename of the created PDF.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"BRD_{timestamp}.pdf"
    filepath = OUTPUT_DIR / filename

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "BRDTitle",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=12,
        textColor=colors.HexColor("#1a1a2e"),
    )
    heading_style = ParagraphStyle(
        "BRDHeading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=14,
        spaceAfter=4,
        textColor=colors.HexColor("#16213e"),
    )
    body_style = ParagraphStyle(
        "BRDBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        spaceAfter=4,
        textColor=colors.HexColor("#2d2d2d"),
    )

    story = []

    for line in content.splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue

        # Detect heading lines (e.g. "1. Executive Summary" or "## Heading")
        is_heading = (
            line.startswith("#")
            or (len(line) <= 80 and line[0].isdigit() and ". " in line[:5])
        )

        clean = line.lstrip("#").strip()

        if is_heading:
            story.append(Paragraph(clean, heading_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
        else:
            # Escape XML special chars for ReportLab
            safe = clean.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe, body_style))

    try:
        doc.build(story)
        logger.info(f"PDF created: {filepath}")
        return str(filepath)
    except Exception as exc:
        logger.exception("PDF build failed")
        raise RuntimeError(f"PDF generation error: {exc}") from exc
