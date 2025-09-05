#!/usr/bin/env python3
"""
main.py
Batch processor for OutlineIQ.
Scans PDFs from `input/` and writes JSON results to `output/`.
"""

import os
import json
import time
import logging
from pathlib import Path
from utils import extract_outline

# --- Config ---
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("outlineiq-batch")


def process_pdf(filepath: Path, *, overwrite: bool = True) -> None:
    """
    Process a single PDF and save output JSON.
    """
    try:
        logger.info("Processing: %s", filepath.name)

        # Run extraction
        title, headings, metadata = extract_outline(filepath)

        output_data = {
            "title": title,
            "headings": headings,
            "metadata": metadata,
        }

        out_file = OUTPUT_DIR / f"{filepath.stem}.json"
        if out_file.exists() and not overwrite:
            logger.warning("Skipping %s (output already exists)", out_file.name)
            return

        with out_file.open("w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        logger.info("✅ Saved: %s", out_file)

    except Exception as e:
        logger.exception("❌ Failed to process %s: %s", filepath.name, e)


def main():
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_DIR.exists():
        logger.error("Input folder not found: %s", INPUT_DIR)
        return

    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        logger.warning("No PDFs found in %s", INPUT_DIR)
        return

    logger.info("Found %d PDF(s) in %s", len(pdf_files), INPUT_DIR)

    for pdf_file in pdf_files:
        process_pdf(pdf_file)

    elapsed = time.time() - start_time
    logger.info("✅ All done in %.2f seconds", elapsed)


if __name__ == "__main__":
    main()
