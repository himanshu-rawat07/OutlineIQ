"""
utils.py

PDF outline / metadata extractor for OutlineIQ.

- Uses PyMuPDF (fitz) to read PDFs.
- Detects headings using font-size heuristics (configurable).
- Extracts first image preview per page (thumbnail, returned as data URI base64).
- Collects hyperlinks.
- Accepts either a file path (str / Path) or raw PDF bytes.

Return:
    title: str
    headings: list[dict]  # {"level": "H1"|"H2"|"H3", "text": str, "page": int, "font_size": float}
    metadata: dict  # {"pages_with_images": [...], "links": [...], "image_previews": [...]}
"""

from __future__ import annotations
import io
import base64
import logging
from typing import Tuple, List, Dict, Union, Optional
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _make_image_preview(img_bytes: bytes, max_size: int = 160) -> str:
    """
    Create a PNG thumbnail from image bytes and return a data URI (base64).
    """
    with Image.open(io.BytesIO(img_bytes)) as img:
        img = img.convert("RGB")
        img.thumbnail((max_size, max_size), Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/png;base64,{b64}"


def _normalize_text(s: str) -> str:
    """Normalize whitespace in extracted text."""
    return " ".join(s.split()).strip()


def extract_outline(
    source: Union[str, Path, bytes],
    *,
    min_h1: float = 18.0,
    min_h2: float = 14.0,
    min_h3: float = 10.0,
    image_preview_max_size: int = 160,
    detect_first_image_only: bool = True,
) -> Tuple[str, List[Dict], Dict]:
    """
    Extract title, headings and metadata from a PDF.

    Args:
        source: file path (str|Path) or raw PDF bytes.
        min_h1, min_h2, min_h3: font-size thresholds (points) to classify headings.
        image_preview_max_size: max dimension of thumbnail in pixels.
        detect_first_image_only: if True, capture only first image per page.

    Returns:
        title, headings_list, metadata_dict
    """
    doc: Optional[fitz.Document] = None
    try:
        if isinstance(source, (bytes, bytearray)):
            doc = fitz.open(stream=source, filetype="pdf")
        else:
            doc = fitz.open(str(source))

        # Title fallback
        title = doc.metadata.get("title") or ""
        title = title.strip() or "Untitled"

        headings: List[Dict] = []
        pages_with_images = set()
        links: List[Dict] = []
        image_previews: List[Dict] = []

        for page_number, page in enumerate(doc, start=1):
            # --- Images ---
            try:
                images = page.get_images(full=True)
                if images:
                    pages_with_images.add(page_number)
                    # Optionally extract only the first image to keep memory low
                    imgs_to_process = images[:1] if detect_first_image_only else images
                    for img_meta in imgs_to_process:
                        xref = img_meta[0]
                        try:
                            base_image = doc.extract_image(xref)
                            img_bytes = base_image.get("image")
                            if img_bytes:
                                preview = _make_image_preview(img_bytes, max_size=image_preview_max_size)
                                image_previews.append({"page": page_number, "preview": preview})
                        except Exception as e_img:
                            logger.debug("Failed to extract/preview image on page %s: %s", page_number, e_img)
            except Exception as e_images:
                logger.debug("Image extraction error on page %s: %s", page_number, e_images)

            # --- Links ---
            try:
                for link in page.get_links():
                    uri = link.get("uri")
                    if uri:
                        links.append({"page": page_number, "uri": uri})
            except Exception as e_links:
                logger.debug("Link extraction error on page %s: %s", page_number, e_links)

            # --- Headings (heuristic by font size) ---
            try:
                page_dict = page.get_text("dict")
                blocks = page_dict.get("blocks", [])
                for block in blocks:
                    if "lines" not in block:
                        continue
                    for line in block["lines"]:
                        spans = line.get("spans", [])
                        if not spans:
                            continue
                        text = " ".join(span.get("text", "") for span in spans).strip()
                        if not text:
                            continue
                        # Determine the largest font size in the line
                        try:
                            max_font = max(float(span.get("size", 0)) for span in spans)
                        except Exception:
                            max_font = 0.0

                        level: Optional[str] = None
                        if max_font >= min_h1:
                            level = "H1"
                        elif max_font >= min_h2:
                            level = "H2"
                        elif max_font >= min_h3:
                            level = "H3"

                        if level:
                            normalized = _normalize_text(text)
                            headings.append({
                                "level": level,
                                "text": normalized,
                                "page": page_number,
                                "font_size": round(max_font, 2)
                            })
            except Exception as e_text:
                logger.debug("Text extraction error on page %s: %s", page_number, e_text)

        # Deduplicate nearby duplicates while preserving order
        seen = set()
        deduped_headings = []
        for h in headings:
            key = (h["level"], h["text"].lower(), h["page"])
            if key not in seen:
                deduped_headings.append(h)
                seen.add(key)

        metadata = {
            "pages_with_images": sorted(pages_with_images),
            "links": links,
            "image_previews": image_previews,
        }

        return title, deduped_headings, metadata

    finally:
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass
