from __future__ import annotations

import re
from typing import Any, Dict, List

import fitz


class PDFParserError(ValueError):
    pass


def _extract_layout_signals(doc: fitz.Document) -> Dict[str, Any]:
    if doc.page_count == 0:
        return {"layout_title": None, "layout_authors": []}

    page = doc[0]
    page_height = float(page.rect.height or 1.0)
    top_limit = page_height * 0.55
    title_zone_limit = page_height * 0.35

    line_items: List[Dict[str, Any]] = []
    blocks = page.get_text("dict").get("blocks", [])
    for block in blocks:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            text = "".join((s.get("text") or "") for s in spans).strip()
            if not text:
                continue
            avg_font = sum(float(s.get("size", 0.0)) for s in spans) / max(1, len(spans))
            y_top = float(line.get("bbox", [0.0, 0.0, 0.0, 0.0])[1])
            line_items.append({"text": text, "font": avg_font, "y": y_top})

    if not line_items:
        return {"layout_title": None, "layout_authors": []}

    title_candidates = [
        item
        for item in line_items
        if item["y"] <= title_zone_limit and 10 <= len(item["text"]) <= 220 and not re.search(r"\babstract\b", item["text"], flags=re.IGNORECASE)
    ]
    if not title_candidates:
        title_candidates = [item for item in line_items if 10 <= len(item["text"]) <= 220]

    title_item = max(title_candidates, key=lambda item: (item["font"], -item["y"]))
    layout_title = title_item["text"]
    title_font = float(title_item["font"])
    title_y = float(title_item["y"])

    author_candidates = []
    for item in line_items:
        text = item["text"]
        if item["y"] <= title_y:
            continue
        if item["y"] > top_limit:
            continue
        if re.search(r"\b(abstract|introduction|keywords?|references?)\b", text, flags=re.IGNORECASE):
            continue
        if len(text) > 140 or len(text) < 4:
            continue
        if any(ch.isdigit() for ch in text):
            continue
        if item["font"] > title_font * 1.02:
            continue
        if item["font"] < title_font * 0.45:
            continue
        author_candidates.append(text)

    author_line = author_candidates[0] if author_candidates else ""
    layout_authors = [part.strip() for part in re.split(r",| and |;|\band\b", author_line, flags=re.IGNORECASE) if part.strip()]
    if any(any(ch.isdigit() for ch in name) for name in layout_authors):
        layout_authors = []

    return {"layout_title": layout_title, "layout_authors": layout_authors[:8]}


def parse_pdf_content(file_bytes: bytes) -> Dict[str, Any]:
    if not file_bytes:
        raise PDFParserError("Uploaded file is empty")

    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            metadata = doc.metadata or {}
            signals = _extract_layout_signals(doc)
            pages = []
            for page in doc:
                extracted = page.get_text("text") or ""
                if extracted.strip():
                    pages.append(extracted.strip())
    except Exception as exc:  # pragma: no cover - defensive branch
        raise PDFParserError("Unable to parse PDF") from exc

    text = "\n\n".join(pages).strip()
    if not text:
        raise PDFParserError("No textual content found in PDF")

    return {
        "raw_text": text,
        "pdf_title": (metadata.get("title") or "").strip() or None,
        "pdf_author": (metadata.get("author") or "").strip() or None,
        "layout_title": signals.get("layout_title"),
        "layout_authors": signals.get("layout_authors") or [],
    }


def parse_pdf_text(file_bytes: bytes) -> str:
    return str(parse_pdf_content(file_bytes)["raw_text"])
