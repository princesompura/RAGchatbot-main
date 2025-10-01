"""
Helpers for OCR fallback:
• perform_ocr(pdf_path)  -> full plain‑text
• text_to_pdf(text, out_path)  -> writes text into a new PDF
"""
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from fpdf import FPDF

def perform_ocr(pdf_path: str | Path, lang: str = "eng") -> str:
    images = convert_from_path(str(pdf_path), dpi=300)
    return "\n".join(pytesseract.image_to_string(img, lang=lang) for img in images)

def text_to_pdf(text: str, out_path: str | Path) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    for line in text.splitlines():
        pdf.cell(0, 8, txt=line, ln=True)
    pdf.output(str(out_path))
