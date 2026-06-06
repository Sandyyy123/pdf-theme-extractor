# PDF Theme Extractor

Automated NLP pipeline for extracting themes and section/heading hierarchies from large PDF document batches, with exact page-number mapping.

## What it does

- Extracts text from PDFs (native + OCR fallback via Tesseract)
- Identifies themes using BERTopic neural topic modelling
- Detects heading hierarchies (H1-H4) using regex + heuristic rules
- Maps every theme hit and heading to its exact page number
- Outputs structured Excel workbook + JSON index

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

## Usage

```bash
python main.py --input /path/to/pdfs --output results/
```

## Output

- `theme_index.xlsx` - master theme index + per-document sheets + cross-doc heatmap
- `section_hierarchy.json` - structured heading tree per document
- `qa_report.txt` - spot-check results

## Architecture

```
PDF batch
  -> text_extractor.py   (PyMuPDF + Tesseract OCR)
  -> theme_analyzer.py   (BERTopic + spaCy NER)
  -> heading_detector.py (regex + heuristic H1-H4)
  -> output_builder.py   (openpyxl + JSON)
```

## Stack

| Tool | Role |
|------|------|
| PyMuPDF | Text extraction with page coordinates |
| pdfplumber | Table detection, complex layouts |
| Tesseract | OCR fallback for scanned pages |
| BERTopic | Neural topic modelling |
| spaCy | NER + sentence segmentation |
| scikit-learn | TF-IDF keyword extraction |
| openpyxl | Excel output with formatting |
