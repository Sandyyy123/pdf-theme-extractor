"""
text_extractor.py - Extract text from PDFs with page-level granularity.
Falls back to Tesseract OCR for image-based/scanned pages.
"""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

MIN_TEXT_LENGTH = 50  # chars below this -> use OCR

def extract_text(pdf_path) -> list[dict]:
    """
    Returns list of dicts: [{page_num: int, text: str, is_ocr: bool}]
    """
    doc = fitz.open(str(pdf_path))
    pages = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()

        if len(text) < MIN_TEXT_LENGTH:
            # Scanned page - use OCR
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img, lang="eng")
            is_ocr = True
        else:
            is_ocr = False

        pages.append({"page_num": page_num, "text": text.strip(), "is_ocr": is_ocr})

    doc.close()
    return pages
