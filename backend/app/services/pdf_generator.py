import os
import logging
import re
from datetime import datetime, timezone
from fpdf import FPDF

logger = logging.getLogger(__name__)

PDF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)


class BriefPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "AI Daily Pulse — Intelligence Report", align="L")
        self.cell(0, 8, datetime.now(timezone.utc).strftime("%B %d, %Y"), align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"AI Daily Pulse | Page {self.page_no()}/{{nb}}", align="C")


def _clean_text(text: str) -> str:
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r'[^\x20-\x7E\n\r\t]', '', text)
    return text


def generate_brief_pdf(full_summary: str, articles: list[dict], date: datetime) -> str:
    pdf = BriefPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, "AI Daily Pulse", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, date.strftime("Daily Intelligence Report — %A, %B %d, %Y"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    _render_markdown(pdf, full_summary)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "Source Articles", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    for i, article in enumerate(articles, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(0, 0, 0)
        title = _clean_text(f"{i}. {article.get('title', 'Untitled')}")
        pdf.multi_cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 100, 100)
        source = _clean_text(article.get("source", "Unknown"))
        pdf.cell(0, 5, f"Source: {source} | Score: {article.get('score', 0)}", new_x="LMARGIN", new_y="NEXT")

        url = _clean_text(article.get("url", ""))
        if url:
            pdf.set_text_color(0, 102, 204)
            pdf.cell(0, 5, url[:90], new_x="LMARGIN", new_y="NEXT", link=url)

        summary = article.get("summary", "")
        if summary:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(0, 5, _clean_text(summary[:200]), new_x="LMARGIN", new_y="NEXT")

        pdf.ln(3)

    filename = f"ai_daily_pulse_{date.strftime('%Y_%m_%d')}.pdf"
    filepath = os.path.join(PDF_DIR, filename)
    pdf.output(filepath)
    logger.info(f"PDF generated: {filepath}")
    return filepath


def _render_markdown(pdf: FPDF, text: str):
    text = _clean_text(text)
    lines = text.split("\n")

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("# "):
            pdf.set_font("Helvetica", "B", 18)
            pdf.set_text_color(0, 51, 102)
            pdf.ln(4)
            pdf.multi_cell(0, 9, stripped[2:], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif stripped.startswith("## "):
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(0, 72, 140)
            pdf.ln(4)
            pdf.multi_cell(0, 8, stripped[3:], new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)
        elif stripped.startswith("### "):
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(0, 51, 102)
            pdf.ln(2)
            pdf.multi_cell(0, 7, stripped[4:], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(40, 40, 40)
            bullet_text = stripped[2:]
            bold_match = re.match(r'\*\*(.+?)\*\*:?\s*(.*)', bullet_text)
            if bold_match:
                pdf.cell(8, 6, chr(149))
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, bold_match.group(1), new_x="LMARGIN", new_y="NEXT")
                if bold_match.group(2):
                    pdf.set_font("Helvetica", "", 10)
                    pdf.cell(8, 6, "")
                    pdf.multi_cell(0, 6, bold_match.group(2), new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.cell(8, 6, chr(149))
                pdf.multi_cell(0, 6, bullet_text, new_x="LMARGIN", new_y="NEXT")
        elif stripped.startswith("---"):
            pdf.ln(2)
            pdf.set_draw_color(180, 180, 180)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)
        elif stripped == "":
            pdf.ln(3)
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(40, 40, 40)
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)
            pdf.multi_cell(0, 6, clean, new_x="LMARGIN", new_y="NEXT")
