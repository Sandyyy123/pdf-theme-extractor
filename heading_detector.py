"""
heading_detector.py - Detect headings (H1-H4) from extracted page text.
Uses regex patterns + heuristic rules (font size proxies, numbering schemes).
"""
import re

# Numbered heading patterns
H1_PATTERN = re.compile(r"^\s*(\d+)\.\s+[A-Z][\w\s&,:;/-]{3,80}$", re.MULTILINE)
H2_PATTERN = re.compile(r"^\s*(\d+\.\d+)\s+[A-Z][\w\s&,:;/-]{3,80}$", re.MULTILINE)
H3_PATTERN = re.compile(r"^\s*(\d+\.\d+\.\d+)\s+[A-Z][\w\s&,:;/-]{2,60}$", re.MULTILINE)
H4_PATTERN = re.compile(r"^\s*(\d+\.\d+\.\d+\.\d+)\s+[A-Z][\w\s&,:;/-]{2,60}$", re.MULTILINE)

LEVEL_MAP = [("H4", H4_PATTERN), ("H3", H3_PATTERN), ("H2", H2_PATTERN), ("H1", H1_PATTERN)]

def detect_headings(pages: list[dict]) -> list[dict]:
    """
    Returns list of: {level, title, number, page_num}
    """
    headings = []
    for page in pages:
        text = page["text"]
        page_num = page["page_num"]
        seen_in_page = set()

        for level, pattern in LEVEL_MAP:
            for m in pattern.finditer(text):
                title = m.group(0).strip()
                if title not in seen_in_page:
                    seen_in_page.add(title)
                    headings.append({
                        "level": level,
                        "number": m.group(1),
                        "title": title,
                        "page_num": page_num
                    })

    return sorted(headings, key=lambda h: h["page_num"])
