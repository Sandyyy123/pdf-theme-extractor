#!/usr/bin/env python3
"""
PDF Theme Extractor - Main Entry Point
Extracts themes and section hierarchies from PDF batches with page-number mapping.
"""
import argparse
import json
from pathlib import Path
from tqdm import tqdm
from text_extractor import extract_text
from theme_analyzer import ThemeAnalyzer
from heading_detector import detect_headings
from output_builder import build_excel, build_json

def main():
    parser = argparse.ArgumentParser(description="Extract themes and sections from PDF batch")
    parser.add_argument("--input", required=True, help="Directory containing PDFs")
    parser.add_argument("--output", default="results", help="Output directory")
    parser.add_argument("--min-theme-size", type=int, default=10, help="Minimum docs per theme")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = list(input_dir.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {input_dir}")
        return

    print(f"Processing {len(pdfs)} PDFs...")

    # Step 1: Extract text with page boundaries
    docs = {}
    for pdf_path in tqdm(pdfs, desc="Extracting text"):
        docs[pdf_path.name] = extract_text(pdf_path)

    # Step 2: Detect headings per document
    print("Detecting section headings...")
    headings = {name: detect_headings(pages) for name, pages in docs.items()}

    # Step 3: Extract themes across all documents
    print("Running theme analysis (BERTopic)...")
    analyzer = ThemeAnalyzer(min_topic_size=args.min_theme_size)
    themes = analyzer.fit_transform(docs)

    # Step 4: Build outputs
    print("Building Excel workbook...")
    build_excel(themes, headings, output_dir / "theme_index.xlsx")

    print("Building JSON index...")
    build_json(themes, headings, output_dir / "section_hierarchy.json")

    print(f"Done. Results in {output_dir}/")
    print(f"  Themes found: {len(themes)}")
    print(f"  Documents processed: {len(docs)}")

if __name__ == "__main__":
    main()
